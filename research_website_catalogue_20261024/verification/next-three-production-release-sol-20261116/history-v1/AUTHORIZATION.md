# Separate future root authorizations

Neither authorization file exists at preparation. No authority is inferred from this document, old receipts, private-stage adoption or successful read-only checks. Root full-body review precedes every first execution of a current helper version.

The helper accepts only default, `--verify-installed`, `--install` or `--publish`. Default performs offline read-only Git/byte/topology checks in the exact647/99/100 or661/102/103 phase and prints `preflight_SHA256`. It writes nothing. The installed verifier is likewise read-only. Neither contacts the remote. After scoped publication changes W master/index, the pinned pre-publication helper is intentionally obsolete; do not replay its defaults on the new baseline.

Root may later create `INSTALL_AUTHORIZATION.json` for one filesystem transaction. Required common keys are exactly those constructed in `authorization()`:

- `schema`: `fixed16-root-authorization-v1`.
- `action`: `INSTALL_EXACT16_FILESYSTEM` for installation or `PUBLISH_EXACT16_GIT` for Git publication.
- Exact current `plan_SHA256`, `helper_SHA256`, root-adoption path/bytes/SHA object and phase-appropriate actual `preflight_SHA256`.
- `scope_paths`: the exact sorted sixteen strings from root adoption.
- `concurrency`: `ROOT_SERIALIZED_NO_OTHER_W_WRITER`.
- `old_lock_disposition`: `RETAIN_COMPLETED_OLD_LOCK_USE_NEW_ISOLATED_TRANSACTION_LOCKS`.
- `deployment_authorized`: false; `Sheet_authorized`: false; `AA`: null; `follow_up`: null.
- `expires_UTC`: a future timezone-qualified ISO timestamp.

Installation permits no extra keys. Git publication uses a separate `GIT_AUTHORIZATION.json`, requires the installed preflight and additionally binds exactly `author_name`, `author_email`, `commit_date` and `installation_SUCCESS`. Identity strings are supplied literally by root, not inferred here; commit date must have a timezone. The installation receipt must be an exact path/bytes/SHA pin to this effort's `transactions/<authorization-SHA>/SUCCESS.json`, with completed661/102/103 status and this precise plan hash. A failed/partial filesystem run does not qualify.

Both transactions create fixed isolated new locks, authorization-hash transaction directories and fsynced journals exclusively. They never release the old completed lock. Failed or uncertain states preserve all owned locks and partials for root inspection; no retry, overwrite, ref/index rollback or cleanup mode exists. Git object writes may precede shared-ref publication, and an interrupted Git transaction may leave unreachable objects or an owned index lock. After a CAS attempt, preserve journal/index/ref facts and let root inspect actual state; do not invent success or automatically restore a ref. A remote push failure leaves its exact local commit/index in place.

The helper implements coordinated serial publication with repeated bounded snapshots and held-file/directory checks. It does not claim isolation from a hostile concurrent process. Filesystem publication makes each aggregate replacement atomic; it does not claim simultaneous atomicity of both aggregates or all sixteen paths. The Git CAS and atomic index replacement are individually atomic, with a journaled intermediate interval while the exclusive Git index lock remains held. Subsequent deployment/live/browser/Sheet work remains a separate root workflow.
