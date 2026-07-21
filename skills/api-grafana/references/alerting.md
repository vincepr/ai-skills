# Grafana Alerting API Guardrails

Read the target instance's current Swagger schema and the [Grafana alerting API documentation](https://grafana.com/docs/grafana/latest/alerting/set-up/provision-alerting-resources/http-api-provisioning/) before choosing an endpoint. Legacy provisioning and newer App Platform APIs use different paths and payloads.

## Read and Analyze

Read operations are allowed within the token's effective permissions. Depending on the instance, useful legacy endpoints include:

```text
GET /api/v1/provisioning/alert-rules
GET /api/v1/provisioning/alert-rules/:uid
GET /api/v1/provisioning/folder/:folderUid/rule-groups/:group
GET /api/v1/provisioning/contact-points
GET /api/v1/provisioning/policies
GET /api/v1/provisioning/mute-timings
GET /api/v1/provisioning/templates
```

If provisioning reads are unavailable, inspect the documented ruler or Alertmanager endpoints exposed by that instance. Do not assume an endpoint called by one deployment exists in another.

When analyzing an alert, read its rule, folder, group, data-source queries, labels, annotations, notification-policy matchers, templates, contact points, and mute timings. Explain the resulting evaluation and routing path in plain language.

## Create a Rule

Create a new alert rule only after the user explicitly approves that specific rule in the current conversation.

Before sending a request:

1. Confirm `alert.rules:create` or the equivalent permission is scoped to the target folder.
2. Read sibling rules and the destination group's evaluation interval.
3. Read notification policies to learn the label keys and values that determine routing.
4. Read notification templates to identify required annotation keys.
5. Reuse established folder, group, label, and annotation conventions rather than inventing near-equivalents.
6. Verify that the pending duration is compatible with the evaluation interval.
7. Show the complete payload and summarize who will be notified and under what conditions.

When using the legacy provisioning API, `X-Disable-Provenance: true` can keep supported resources editable in the UI. Use it only when the current documentation and destination group's provenance allow it; a group cannot mix incompatible provenance.

After creation, re-read the rule and group. Verify the rule's folder, group, interval, labels, annotations, and provenance.

## Existing Rules

Do not update, move, or delete an existing alert rule from this skill.

For a requested change:

1. Read the current rule and group.
2. Produce a complete candidate payload.
3. Show a focused diff and explain effects on evaluation and routing.
4. Stop so the user can apply it through their chosen review path.

Rule-group fields can affect every sibling rule. Never assume moving a rule preserves the destination interval; verify the documented behavior for the exact API and instance.

## Routing Resources

Treat contact points, notification policies, templates, and mute timings as suggest-only:

- Read and analyze them freely within granted permissions.
- Produce exact candidate JSON and the corresponding request.
- Do not send POST, PUT, PATCH, or DELETE requests.

A notification-policy update may replace the entire routing tree rather than one branch. Always retrieve and preserve the complete tree when drafting a candidate.

## Failure Handling

- `401`: verify the URL and authorization header without printing the token.
- `403`: inspect effective permissions and resource scope; do not guess or escalate privileges.
- `404`: verify the API family, namespace, folder UID, and resource UID.
- `409` or `412`: treat as concurrent modification; re-read and regenerate the diff.
- Validation failure: compare the payload with the target instance's schema instead of copying another API family's format.
