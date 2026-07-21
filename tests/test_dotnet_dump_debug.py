import importlib.util
import pathlib
import unittest
from unittest import mock


SCRIPT_PATH = (
    pathlib.Path(__file__).parents[1]
    / "skills"
    / "dotnet-dump-debug"
    / "scripts"
    / "dbg.py"
)
SPEC = importlib.util.spec_from_file_location("dotnet_dump_dbg", SCRIPT_PATH)
DBG = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(DBG)


class PromptParsingTests(unittest.TestCase):
    def test_extracts_complete_prompt_delimited_chunks(self):
        chunks, remainder = DBG.extract_prompt_chunks(
            "startup banner\n> stack output\n> "
        )

        self.assertEqual(["startup banner\n", "stack output\n"], chunks)
        self.assertEqual("", remainder)

    def test_waits_for_a_prompt_split_across_reads(self):
        chunks, remainder = DBG.extract_prompt_chunks("stack output\n>")

        self.assertEqual([], chunks)
        self.assertEqual("stack output\n>", remainder)

        chunks, remainder = DBG.extract_prompt_chunks(remainder + " ")

        self.assertEqual(["stack output\n"], chunks)
        self.assertEqual("", remainder)

    def test_does_not_split_greater_than_text_inside_output(self):
        chunks, remainder = DBG.extract_prompt_chunks("value > threshold\n> ")

        self.assertEqual(["value > threshold\n"], chunks)
        self.assertEqual("", remainder)


class ProcessSelectionTests(unittest.TestCase):
    @mock.patch.object(DBG.subprocess, "check_output", return_value="101\n202\n")
    def test_rejects_ambiguous_name_matches(self, _check_output):
        pid, label, options, error = DBG.resolve_pid(["--name", "worker"])

        self.assertIsNone(pid)
        self.assertIsNone(label)
        self.assertEqual({}, options)
        self.assertIn("multiple processes", error)
        self.assertIn("101", error)
        self.assertIn("202", error)


if __name__ == "__main__":
    unittest.main()
