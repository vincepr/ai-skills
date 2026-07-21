#!/usr/bin/env python3
"""Inspect managed state from a persistent dotnet-dump analyze session.

The helper captures a process through the .NET diagnostic IPC port and keeps
the analyzer alive behind a repository-scoped Unix socket. Commands return
JSON so an agent can inspect several parts of the same snapshot efficiently.
"""

import glob
import hashlib
import json
import os
import queue
import re
import socket
import subprocess
import sys
import tempfile
import threading
import time


CACHE_ROOT = os.environ.get("XDG_CACHE_HOME", os.path.expanduser("~/.cache"))
CACHE = os.path.join(CACHE_ROOT, "dotnet-debug")
SESSIONS = os.path.join(CACHE, "sessions")
PROMPT_RE = re.compile(r"(?m)^> ")
LAUNCH_LOG = os.path.join(tempfile.gettempdir(), "dotnet-debug-launch.log")


def extract_prompt_chunks(buffer):
    """Return complete analyzer responses and the unconsumed buffer.

    dotnet-dump analyze prints a line-leading "> " prompt after startup and
    after every command. Wait for the complete prompt because a stream read
    can split the two prompt characters across chunks.
    """
    chunks = []
    while True:
        match = PROMPT_RE.search(buffer)
        if match is None:
            return chunks, buffer
        chunks.append(buffer[:match.start()])
        buffer = buffer[match.end():]


def find_dotnet_dump():
    configured = os.environ.get("DOTNET_DUMP")
    if configured and os.path.exists(configured):
        return configured
    default = os.path.expanduser("~/.dotnet/tools/dotnet-dump")
    if os.path.exists(default):
        return default
    from shutil import which
    return which("dotnet-dump")


class Daemon:
    def __init__(self, session_dir):
        self.session_dir = session_dir
        self.sock_path = os.path.join(session_dir, "daemon.sock")
        with open(os.path.join(session_dir, "target.json"), encoding="utf-8") as target_file:
            self.target = json.load(target_file)
        self.proc = None
        self.lock = threading.RLock()
        self.chunks = queue.Queue()
        self.state = "preparing"
        self.error = None
        self.dump_path = os.path.join(session_dir, "snapshot.dmp")
        self._running = True

    def _collect(self, pid):
        dotnet_dump = find_dotnet_dump()
        if not dotnet_dump:
            raise RuntimeError(
                "dotnet-dump not found; install it with "
                "'dotnet tool install --global dotnet-dump'"
            )
        try:
            os.remove(self.dump_path)
        except FileNotFoundError:
            pass
        dump_type = self.target.get("dump_type", "Heap")
        with open(
            os.path.join(self.session_dir, "collect.log"),
            "w",
            encoding="utf-8",
        ) as log:
            result = subprocess.run(
                [
                    dotnet_dump,
                    "collect",
                    "-p",
                    str(pid),
                    "-o",
                    self.dump_path,
                    "--type",
                    dump_type,
                ],
                stdout=log,
                stderr=subprocess.STDOUT,
                text=True,
                check=False,
            )
        if result.returncode != 0 or not os.path.exists(self.dump_path):
            raise RuntimeError(
                f"dotnet-dump collect failed (see {self.session_dir}/collect.log)"
            )

    def _reader(self):
        descriptor = self.proc.stdout.fileno()
        buffer = ""
        while True:
            try:
                data = os.read(descriptor, 65536)
            except OSError:
                break
            if not data:
                break
            buffer += data.decode("utf-8", "replace")
            complete, buffer = extract_prompt_chunks(buffer)
            for chunk in complete:
                self.chunks.put(chunk)
        if buffer:
            self.chunks.put(buffer)
        self.chunks.put(None)

    def _write(self, value):
        self.proc.stdin.write(value.encode())
        self.proc.stdin.flush()

    def _start_analyze(self):
        dotnet_dump = find_dotnet_dump()
        if not dotnet_dump:
            raise RuntimeError("dotnet-dump not found")
        self.proc = subprocess.Popen(
            [dotnet_dump, "analyze", self.dump_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=0,
        )
        threading.Thread(target=self._reader, daemon=True).start()
        try:
            startup = self.chunks.get(timeout=60)
        except queue.Empty as error:
            raise RuntimeError("dotnet-dump analyze did not show a prompt") from error
        if startup is None:
            raise RuntimeError("dotnet-dump analyze exited during startup")

    def _cmd(self, sos, timeout=60):
        with self.lock:
            if not self.proc or self.proc.poll() is not None:
                return "[analyze session not running]"
            while not self.chunks.empty():
                try:
                    self.chunks.get_nowait()
                except queue.Empty:
                    break
            self._write(sos + "\n")
            try:
                chunk = self.chunks.get(timeout=timeout)
            except queue.Empty:
                return f"[timeout running: {sos}]"
            if chunk is None:
                return "[analyze session ended]"
            return self._clean(chunk)

    @staticmethod
    def _clean(chunk):
        lines = chunk.splitlines()
        while lines and (
            lines[0].strip() == "" or lines[0].lstrip().startswith(">")
        ):
            lines.pop(0)
        while lines and lines[-1].strip() in ("", ">"):
            lines.pop()
        return "\n".join(lines)

    def bringup(self):
        try:
            self._collect(self.target["pid"])
            self._start_analyze()
            with self.lock:
                self.state = "ready"
        except Exception as error:
            with self.lock:
                self.state = "error"
                self.error = str(error)

    def _resnapshot(self):
        if self.proc and self.proc.poll() is None:
            try:
                self._write("exit\n")
            except Exception:
                pass
            try:
                self.proc.terminate()
            except Exception:
                pass
        self.chunks = queue.Queue()
        self._collect(self.target["pid"])
        self._start_analyze()

    def handle(self, request):
        command = request.get("cmd")
        arguments = request.get("args", {}) or {}
        with self.lock:
            state, error = self.state, self.error
        if command == "ping":
            return {"ok": True, "state": state, "error": error}
        if command == "status":
            return {
                "state": state,
                "error": error,
                "pid": self.target.get("pid"),
                "label": self.target.get("label"),
                "dump": self.dump_path,
                "session": self.session_dir,
            }
        if command == "stop":
            self.shutdown()
            return {"ok": True, "stopped": True}
        if state == "preparing":
            return {
                "state": "preparing",
                "note": "collecting dump / starting analyze",
            }
        if state == "error":
            return {"state": "error", "error": error}

        try:
            if command == "resnapshot":
                self._resnapshot()
                return {
                    "ok": True,
                    "note": "fresh snapshot collected",
                    "pid": self.target.get("pid"),
                }
            sos = self._map(command, arguments)
            if sos is None:
                return {"error": f"unknown command: {command}"}
            return {
                "ok": True,
                "command": sos,
                "output": self._cmd(
                    sos,
                    timeout=int(arguments.get("timeout", 60)),
                ),
            }
        except Exception as error:
            return {"error": f"{type(error).__name__}: {error}"}

    @staticmethod
    def _map(command, arguments):
        if command == "stack":
            sos = "clrstack"
            if arguments.get("all"):
                sos += " -all"
            if arguments.get("args"):
                sos += " -a"
            return sos
        if command == "pstacks":
            return "pstacks"
        if command == "threads":
            return "clrthreads"
        if command == "heap":
            sos = "dumpheap"
            if arguments.get("stat"):
                sos += " -stat"
            if arguments.get("type"):
                sos += f" -type {arguments['type']}"
            return sos
        if command == "obj":
            return f"dumpobj {arguments['addr']}"
        if command == "dso":
            return "dso"
        if command == "sos":
            return arguments["raw"]
        return None

    def shutdown(self):
        self._running = False
        if self.proc and self.proc.poll() is None:
            try:
                self._write("exit\n")
            except Exception:
                pass
            try:
                self.proc.terminate()
            except Exception:
                pass
        try:
            os.remove(self.sock_path)
        except FileNotFoundError:
            pass
        if self.target.get("keep_dump") is not True:
            try:
                os.remove(self.dump_path)
            except FileNotFoundError:
                pass

    def serve(self):
        if os.path.exists(self.sock_path):
            os.remove(self.sock_path)
        server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        server.bind(self.sock_path)
        server.listen(8)
        server.settimeout(1.0)
        with open(
            os.path.join(self.session_dir, "daemon.pid"),
            "w",
            encoding="utf-8",
        ) as pid_file:
            pid_file.write(str(os.getpid()))
        threading.Thread(target=self.bringup, daemon=True).start()
        while self._running:
            try:
                connection, _ = server.accept()
            except socket.timeout:
                continue
            except OSError:
                break
            with connection:
                try:
                    buffer = b""
                    while b"\n" not in buffer:
                        chunk = connection.recv(65536)
                        if not chunk:
                            break
                        buffer += chunk
                    request = json.loads(buffer.decode().strip() or "{}")
                    response = self.handle(request)
                    connection.sendall((json.dumps(response) + "\n").encode())
                    if request.get("cmd") == "stop":
                        break
                except Exception as error:
                    try:
                        connection.sendall(
                            (json.dumps({"error": str(error)}) + "\n").encode()
                        )
                    except Exception:
                        pass
        self.shutdown()


def repo_root():
    try:
        output = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
        if output:
            return output
    except Exception:
        pass
    return os.getcwd()


def session_dir_for(root=None):
    root = root or repo_root()
    digest = hashlib.sha1(root.encode()).hexdigest()[:16]
    return os.path.join(SESSIONS, digest)


def daemon_alive(session_dir):
    if not os.path.exists(os.path.join(session_dir, "daemon.sock")):
        return False
    try:
        with open(
            os.path.join(session_dir, "daemon.pid"),
            encoding="utf-8",
        ) as pid_file:
            os.kill(int(pid_file.read().strip()), 0)
        return True
    except Exception:
        return False


def send_to_daemon(request, session_dir=None, timeout=120):
    session_dir = session_dir or session_dir_for()
    sock_path = os.path.join(session_dir, "daemon.sock")
    if not os.path.exists(sock_path):
        return {
            "error": "no active snapshot for this repo "
            "(use 'dbg.py snapshot ...')"
        }
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client.settimeout(timeout)
    try:
        client.connect(sock_path)
        client.sendall((json.dumps(request) + "\n").encode())
        buffer = b""
        while b"\n" not in buffer:
            chunk = client.recv(65536)
            if not chunk:
                break
            buffer += chunk
        return json.loads(buffer.decode().strip() or "{}")
    except Exception as error:
        return {"error": f"daemon communication failed: {error}"}
    finally:
        client.close()


def resolve_pid(arguments):
    index = 0
    dump_type = "Heap"
    keep_dump = False
    launch = None
    launch_args = []
    delay = 0
    pid = None
    label = None
    while index < len(arguments):
        value = arguments[index]
        if value == "--name":
            if index + 1 >= len(arguments):
                return None, None, {}, "--name requires a value"
            pattern = arguments[index + 1]
            try:
                matches = subprocess.check_output(
                    ["pgrep", "-f", pattern],
                    text=True,
                ).split()
            except subprocess.CalledProcessError:
                matches = []
            pids = [match for match in matches if int(match) != os.getpid()]
            if not pids:
                return None, None, {}, f"no process matching {pattern!r}"
            if len(pids) > 1:
                return (
                    None,
                    None,
                    {},
                    f"multiple processes match {pattern!r}: {', '.join(pids)}; "
                    "retry with an explicit PID",
                )
            pid, label, index = (
                int(pids[0]),
                f"name~{pattern}",
                index + 2,
            )
        elif value == "--launch":
            if index + 1 >= len(arguments):
                return None, None, {}, "--launch requires a value"
            launch = arguments[index + 1]
            index += 2
        elif value == "--delay":
            if index + 1 >= len(arguments):
                return None, None, {}, "--delay requires a value"
            delay = float(arguments[index + 1])
            index += 2
        elif value == "--full":
            dump_type = "Full"
            index += 1
        elif value == "--keep-dump":
            keep_dump = True
            index += 1
        elif value == "--":
            launch_args = arguments[index + 1:]
            break
        elif value.isdigit():
            pid, label, index = int(value), f"pid {value}", index + 1
        else:
            index += 1
    if launch is not None:
        pid, label, error = _launch_and_pid(launch, launch_args, delay)
        if error:
            return None, None, {}, error
    if pid is None:
        return (
            None,
            None,
            {},
            "snapshot requires <pid>, --name <substring>, "
            "or --launch <project-or-dll>",
        )
    return (
        pid,
        label,
        {"dump_type": dump_type, "keep_dump": keep_dump},
        None,
    )


def _launch_and_pid(target, arguments, delay):
    dll = None
    if target.endswith(".dll"):
        dll = os.path.abspath(target)
    else:
        project = target
        if os.path.isdir(target):
            projects = glob.glob(os.path.join(target, "*.csproj"))
            if not projects:
                return None, None, f"no .csproj in {target}"
            project = projects[0]
        if not project.endswith(".csproj"):
            return (
                None,
                None,
                f"cannot launch {target} "
                "(pass a .dll, .csproj, or directory)",
            )
        build = subprocess.run(
            ["dotnet", "build", project],
            capture_output=True,
            text=True,
            check=False,
        )
        if build.returncode != 0:
            return (
                None,
                None,
                f"dotnet build failed: "
                f"{build.stdout[-400:]}{build.stderr[-200:]}",
            )
        name = os.path.splitext(os.path.basename(project))[0]
        candidates = glob.glob(
            os.path.join(
                os.path.dirname(os.path.abspath(project)),
                "bin",
                "*",
                "net*",
                f"{name}.dll",
            )
        )
        if not candidates:
            return None, None, f"built but {name}.dll was not found"
        dll = sorted(candidates, key=os.path.getmtime, reverse=True)[0]
    apphost = os.path.splitext(dll)[0]
    command = (
        [apphost]
        if os.path.exists(apphost) and os.access(apphost, os.X_OK)
        else ["dotnet", dll]
    ) + list(arguments)
    launch_log = open(LAUNCH_LOG, "w", encoding="utf-8")
    process = subprocess.Popen(
        command,
        cwd=os.path.dirname(dll),
        stdout=launch_log,
        stderr=subprocess.STDOUT,
        start_new_session=True,
    )
    if delay:
        time.sleep(delay)
    if process.poll() is not None:
        return (
            None,
            None,
            f"launched process exited immediately (see {LAUNCH_LOG})",
        )
    return (
        process.pid,
        f"launched {os.path.basename(dll)} (pid {process.pid})",
        None,
    )


def do_snapshot(arguments):
    pid, label, extra, error = resolve_pid(arguments)
    if error:
        return {"error": error}
    session_dir = session_dir_for()
    if daemon_alive(session_dir):
        return {
            "error": "a snapshot session is already active for this repo; "
            "run 'dbg.py stop' first"
        }
    os.makedirs(session_dir, exist_ok=True)
    for filename in ("daemon.sock", "daemon.pid", "collect.log"):
        try:
            os.remove(os.path.join(session_dir, filename))
        except FileNotFoundError:
            pass
    target = {"pid": pid, "label": label, **extra}
    with open(
        os.path.join(session_dir, "target.json"),
        "w",
        encoding="utf-8",
    ) as target_file:
        json.dump(target, target_file)
    daemon_log = open(
        os.path.join(session_dir, "daemon.log"),
        "w",
        encoding="utf-8",
    )
    subprocess.Popen(
        [
            sys.executable,
            os.path.abspath(__file__),
            "__serve",
            session_dir,
        ],
        stdout=daemon_log,
        stderr=subprocess.STDOUT,
        start_new_session=True,
    )
    deadline = time.time() + 120
    last = {"state": "starting"}
    while time.time() < deadline:
        if os.path.exists(os.path.join(session_dir, "daemon.sock")):
            last = send_to_daemon(
                {"cmd": "status"},
                session_dir,
                timeout=30,
            )
            if last.get("state") not in ("preparing", "starting", None):
                break
        time.sleep(0.4)
    last["_target"] = target
    if last.get("state") == "ready":
        last["next"] = (
            "inspect: dbg.py stack | threads | heap --stat | "
            "obj <address> | dso | sos \"<command>\""
        )
    return last


USAGE = """dbg.py - inspect managed state of a running .NET process

  snapshot <pid> | --name <substring> | --launch <project-or-dll> [--delay S] [-- args]
                              collect a dump and open an analyzer [--full, --keep-dump]
  resnapshot                  collect a fresh dump of the same process
  stack [--all] [--args]      managed call stack
  pstacks                     grouped parallel stacks of all threads
  threads                     managed threads
  heap [--stat] [--type T]    managed heap
  obj <address>               object fields
  dso                         objects on the current stack
  sos "<raw-command>"         run any SOS command
  status | stop               session state or cleanup

This tool inspects snapshots; it does not provide live breakpoints or stepping.
"""


def build_request(command, arguments):
    mapped = {}
    if command == "stack":
        mapped["all"] = "--all" in arguments
        mapped["args"] = "--args" in arguments
    elif command == "heap":
        mapped["stat"] = "--stat" in arguments
        if "--type" in arguments:
            type_index = arguments.index("--type") + 1
            if type_index >= len(arguments):
                raise ValueError("--type requires a value")
            mapped["type"] = arguments[type_index]
    elif command == "obj":
        if not arguments:
            raise ValueError("obj requires an address")
        mapped["addr"] = arguments[0]
    elif command == "sos":
        if not arguments:
            raise ValueError("sos requires a command")
        mapped["raw"] = arguments[0]
    return {"cmd": command, "args": mapped}


def main():
    arguments = sys.argv[1:]
    if not arguments:
        print(USAGE)
        return
    command = arguments[0]
    if command == "__serve":
        Daemon(arguments[1]).serve()
        return
    if command in ("-h", "--help", "help"):
        print(USAGE)
        return
    if command == "snapshot":
        print(json.dumps(do_snapshot(arguments[1:]), indent=2))
        return
    known = {
        "resnapshot",
        "stack",
        "pstacks",
        "threads",
        "heap",
        "obj",
        "dso",
        "sos",
        "status",
        "stop",
        "ping",
    }
    if command not in known:
        print(
            json.dumps(
                {
                    "error": f"unknown command: {command}",
                    "usage": "dbg.py --help",
                }
            )
        )
        sys.exit(2)
    timeout = (
        180
        if command in ("resnapshot", "heap", "pstacks", "status")
        else 90
    )
    try:
        request = build_request(command, arguments[1:])
    except ValueError as error:
        print(json.dumps({"error": str(error)}))
        sys.exit(2)
    print(
        json.dumps(
            send_to_daemon(request, timeout=timeout),
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
