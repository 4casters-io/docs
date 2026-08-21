# sources/ — machine-owned snapshots

These files are the documents the services serve (`/openapi.json`,
`/asyncapi.json`), snapshotted by the docs reconciler
(backgroundjobs-ts `docs-reconciler`) whenever every pod of a service agrees
on a new document. `sources.lock` (repo root) records each source's hash,
the combined hash, and when it was observed.

**Do not edit anything under `sources/` by hand.** The reconciler will
overwrite it on its next pass; endpoint documentation lives in the services
(the definition form in core-api's `validatedRequestHandler`), not here.

Manual snapshot (same function the reconciler runs): `4c docs snapshot`.
To hold a source at its current snapshot during an incident, set
`"pinned": true` for it in `sources.lock` and commit.
