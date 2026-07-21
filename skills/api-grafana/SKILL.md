---
name: api-grafana
description: Use Grafana's HTTP API to inspect and manage dashboards, folders, data sources, and alerting resources with permission-aware, guarded writes.
disable-model-invocation: true
---

# Use the Grafana HTTP API

Work against a Grafana instance through its HTTP API. Read the current endpoint documentation before constructing a payload because supported routes and schemas vary by instance.

## Connect Safely

Use these environment variables when available:

- `GRAFANA_URL`: instance URL without a trailing slash.
- `GRAFANA_TOKEN`: service-account token.

Ask for missing values. Keep them in the current process only; never write a token to a file, command history, log, or durable memory. Do not print the token.

Confirm connectivity and inspect the server response:

```bash
curl -fsS \
  -H "Authorization: Bearer $GRAFANA_TOKEN" \
  "$GRAFANA_URL/api/health"
```

Before a write, inspect the token's effective permissions when the endpoint is available:

```bash
curl -fsS \
  -H "Authorization: Bearer $GRAFANA_TOKEN" \
  "$GRAFANA_URL/api/access-control/user/permissions"
```

Apply folder- and resource-scoped permissions exactly. A permission on one folder or UID does not authorize another.

## Select the Supported API

Open the [Grafana HTTP API reference](https://grafana.com/docs/grafana/latest/developer-resources/api-reference/http-api/) and the target instance's `/swagger-ui` before building a payload.

- Newer `/apis` resources and legacy `/api` routes may coexist.
- Prefer the stable API advertised by the target instance; some domains may not have a direct newer equivalent.
- Do not mix a response from one API family with another family's request body.
- Use UID-based routes instead of deprecated numeric-ID or name-based variants.

## Authorization Rules

| Resource or action | Behavior |
|---|---|
| Read, list, search, or analyze | Proceed within granted permissions. |
| Create or update a dashboard or folder | Proceed after reading the current object and validating the target folder. |
| Delete a dashboard | Ask for explicit permission and mention loss of history or restoration options. |
| Delete a folder | Ask for explicit permission and report every known contained resource because deletion can cascade. |
| Create an alert rule | Ask for explicit permission for that rule in the current conversation. |
| Modify or delete an existing alert rule | Produce the candidate payload and diff, then stop. |
| Create, modify, or delete a data source, contact point, policy, template, mute timing, user, team, or organization | Produce the exact payload and request, then stop. |

Do not turn a broad request such as "fix the alerts" into authorization for a write. Never retry a conflict by forcing or overwriting without explicit approval.

## Make Requests

Use fail-fast requests and keep payloads reviewable:

```bash
curl -fsS \
  -H "Authorization: Bearer $GRAFANA_TOKEN" \
  -H "Content-Type: application/json" \
  "$GRAFANA_URL/<path>"
```

For writes:

1. GET the current resource and its containing folder or group.
2. Check effective permissions for the exact target.
3. Build a complete payload from the current documented schema.
4. Show the material diff before sending it.
5. Preserve concurrency, provenance, location, and version metadata.
6. Send one request. On `409`, `412`, or another conflict, stop, re-read, and report the competing change.
7. GET the resource again and verify its location and changed fields.

URL-encode path and query values. Save API responses only when needed for the task, keep credentials out of them, and remove sensitive temporary artifacts when finished.

## Dashboards and Folders

Preserve the full object returned by the latest GET, including:

- the resource UID and namespace;
- folder annotations or folder UID;
- version or resource-version metadata;
- dashboard schema version;
- a meaningful change message when the API supports one.

For the legacy `POST /api/dashboards/db` route:

- Carry `dashboard.version` from the latest GET.
- Carry `meta.folderUid` into the request's top-level `folderUid`; omitting it can move the dashboard to the root folder.
- Keep `overwrite` false unless the user explicitly approves bypassing conflict protection.
- Treat `412 Precondition Failed` as a concurrent edit and re-read before proposing another request.

For the newer dashboard API, preserve `metadata.annotations.grafana.app/folder` and use the stable API version exposed by the instance. Do not guess a schema version for a new dashboard; derive it from current documentation or a compatible dashboard on that instance.

Prefer version history or restore over deletion when undoing dashboard changes.

## Data Sources

List and inspect data sources by UID. Querying through `POST /api/ds/query` is a read operation, but the query itself may be expensive; bound its time range and result size.

Treat data-source configuration as suggest-only. Never return decrypted secrets—Grafana normally redacts them, and that boundary must remain intact.

## Alerting

Read [references/alerting.md](references/alerting.md) before working with alert rules, contact points, notification policies, templates, or mute timings. Alerting routes evolve independently, and an apparently local change can alter routing or evaluation for sibling rules.

## Report

State:

- the instance and API family used, without revealing credentials;
- the resource UIDs and folders inspected or changed;
- the permissions relevant to the operation;
- the exact writes performed or, for suggest-only actions, the payloads left for the user;
- any conflicts, deprecated routes, or unverified assumptions.
