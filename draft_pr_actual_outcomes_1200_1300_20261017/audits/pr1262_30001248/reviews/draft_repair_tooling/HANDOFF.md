# PR1262 same-ID unpublished draft ZIP repair

The actual new operative helper is
program/publication_coordinators/repair_pr1262_draft.py. Its exact source copy is
repair_pr1262_draft.py in this family. INPUT_BINDINGS.json explicitly binds the
operative path/size/SHA256 and identical in-family source copy; the external path
is a receipt, never authored manifest membership. Existing eight helpers,
strict coordinator, postmerge verifier and shared kit were not edited. No
metadata/context/manuscript/current archive, account, Git/index/ref or PR
mutation occurred here. The new helper itself has not made any live request.

## Exact scope and release requirements

Only the saved production deposition23443230, submitted literally false, is in
scope. DRAFT_REPAIR_BASELINE.json supplies the immutable exact known bucket, old
PDF/ZIP names, sizes, MD5/SHA256 and UUIDs, original stage-intent hash and explicit
new metadata-manifest hash. Baseline extras/history fields are documentary
receipts, not followed as membership or alternate schema guesses. The actual
current baseline and original stage intent remained unchanged during tests.

The helper first calls the unchanged strict coordinator's authenticate_release.
The actual current final gate must exist and pass its full latest CLEAN review,
current context/artifacts/helper/shared-kit and complete frozen-input checks.
Additionally, that latest full review freeze MUST separately include the actual
operative repair helper and actual DRAFT_REPAIR_BASELINE.json with exact sizes
and SHA256. This family source copy cannot stand in for the operative input.
No final gate is manufactured. There is currently no new live clearance; root
must finish its new full-package R4 after adding this fourteenth authored
registry, rebuilding and freezing all actual inputs.

The same manifest-path kit state must contain exactly known ID23443230 and no
saved publication. Original stage intent must remain byte-identical. Existing
publish intent/receipt prohibits repair. Exactly eleven current supplied fields
and the exact current two-file manifest are required. The helper checks every
remote supplied field for literal equality before strict actual kit.verify;
content/entity/creator normalization is never silently accepted. The current
explicitly escaped HTML description is already authored/reviewed separately by
root. This helper never updates metadata. Local PDF MD5/SHA256/size and remote
PDF MD5/size/UUID must equal the old immutable baseline. New ZIP SHA256 must
differ from the old ZIP and be bound by the current real release review.

## One-attempt same-record transition

The only possible external mutations are one file-specific DELETE for the
baseline old ZIP UUID and one PUT of the new reviewed ZIP under the identical
filename to the identical pinned bucket. The helper never calls create, copy,
publish, metadata update, edit, discard, newversion or deposition deletion.
Remote supplied metadata, bucket, exact old two-file inventory and both UUIDs
are checked before deleting anything. The canonical production DELETE URL is
constructed from the pinned deposition ID and canonical old ZIP UUID; untrusted
remote action/self links are not used. Bucket must be exact baseline and a
canonical HTTPS production bucket UUID URL. PDF is never uploaded or deleted.

An exclusive DRAFT_REPAIR_INTENT.json is written before DELETE. The actual
current release is reauthenticated and live original draft/head/body/branch and
tracker preflight is repeated before downstream external writes. All remote
metadata, unchanged PDF and same-ID unpublished state are checked again at the
critical transitions. Exclusive DRAFT_REPAIR_UPLOAD_INTENT.json precedes PUT.
Existing attempt intents force GET-only reconciliation, even if an earlier
mutation did not reach the server. They are never overwritten or used as
permission to retry DELETE/PUT. Intents are exclusive local files; this does not
claim hardware-level power-loss durability or a transactional server API.

The official [Zenodo developer documentation](https://developers.zenodo.org/)
instructs deleting an old file before uploading its replacement and documents
file DELETE success as204 with an empty body. The unchanged shared client's
nonempty-JSON contract raises DepositError on that response. The helper catches
that sanitized error without echoing its text, then requires a fresh GET with
only the exact old PDF remaining, exact metadata/bucket/id and literal false
submitted state before it can proceed. An unsuccessful delete, missing/failed
read or any drift cannot initiate an upload. A later invocation is read-only.

Both confirmed and uncertain upload responses require another same-ID GET and
actual strict kit verification of all eleven current fields and exactly the new
two files. If exact, the helper writes or verifies a proper ready_to_publish
STAGE_RECEIPT through the actual coordinator.validate_summary and same saved
kit ID. This is local staging evidence only, never publication. The original
stage intent is preserved. If upload was accepted but its response/readback was
lost, a later inspect can recover this receipt without another PUT. A missing,
old or otherwise nonmatching ZIP reports recovery_required, never silently
retries. No stage receipt is created for an unverified two-file package.

The unchanged coordinator may later publish using that new verified stage
receipt and known saved ID, after its own fresh strict checks and authorized
release gate. This helper does not issue publication.

Commands in the actual deployment, after root's NEW full review gate exists:

```
python3 -B <program>/publication_coordinators/repair_pr1262_draft.py inspect
python3 -B <program>/publication_coordinators/repair_pr1262_draft.py replace
```

Only the initial eligible replace call may mutate. Inspect and any replace call
with an existing intent are GET-only. Root must reconcile unknown state by
read-only known-ID/account evidence rather than deleting intents or retrying.
No extra human consent requirement is introduced by this tooling.

## Offline evidence and limits

OFFLINE_FAULT_RECEIPT.json records identical PASS in normal/-O/-OO. The actual
new helper, actual unchanged strict coordinator methods, actual shared kit and
actual client get/upload routing run against fully mocked network transport.
The actual shared request method is separately exercised with a mocked HTTP204
empty response and produces the expected DepositError. No token is obtained or
sent. Twenty-two metadata controls change each of the eleven fields before
DELETE and again after DELETE before PUT; all stop the next mutation. Twenty-
seven further controls cover ID/publication state, old ZIP/PDF hashes/sizes/
UUIDs, missing/extra/duplicate files, invalid or changed buckets, local PDF/ZIP,
saved ID, missing/wrong helper or baseline frozen inputs, live PR preflight,
original stage intent, prior publish and exclusive attempt state. Seven
scenarios cover normal repair,204delete, accepted-but-lost upload, lost GET after
DELETE or PUT, rejected delete and unaccepted upload. Repeated calls never add
DELETE/PUT, and successful staging satisfies actual validate_summary.

The full real release authenticator and live GitHub/GWS preflight are explicitly
stubbed with synthetic fixture data because the new real full-package gate does
not exist yet. The repair-specific latest frozen-input guards are actually
executed. These fixtures are not actual review evidence, live integration,
publication authorization, a re-audit of the mathematics, or a guarantee against
all possible concurrent server races. Real current artifacts and the helper
must receive the new independent full-package review before use. Source copies
and test bodies are retained for inspection, not automatically executed from
the portable math archive. Root's two exact diagnostic replay contract remains
unchanged.

The authored manifest uses authored_files/path/bytes, contains only relative
in-family actual authored files, and excludes itself. Its outside SHA256 is
handed to root. It creates no recursive current-context/ZIP/final-gate binding;
root will register it, rebuild, then obtain the new complete-package review.
