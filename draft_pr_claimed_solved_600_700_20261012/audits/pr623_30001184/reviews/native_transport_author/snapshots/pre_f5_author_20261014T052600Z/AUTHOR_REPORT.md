# PR623 native transport repair report

**All requested author repairs are implemented: 47 offline tests pass under normal Python and 47 under `-O`, with zero failures/errors. Fresh independent review is required before execution. No live upload, commit, publication or other Zenodo mutation was made by this author.**

The prior author version contained real F1/F2/F3 defects; the parent later identified operational F4. Its original source, tests, report, receipt and log are preserved at `snapshots/original_author_20261014T044110Z/`, with a dated snapshot receipt. The independent review and its reproducers are unchanged. The earlier PASS label described an insufficient test model; this report supersedes it.

## Scope and preserved kit behavior

Production own recovered initial draft **23356540**, the original manifest, and the exact reviewed PDF/ZIP are the only supported inputs. No create/delete/edit/version/metadata PUT, account search, sandbox or alternative manifest/record route exists. File initialize/content/commit and publication are the only mutating endpoints, pinned to this ID and the two names.

The repository kit source executes without edits from one SHA-256-checked byte snapshot in a fresh isolated module, with the correct absolute `__file__`, ROOT, credential and state paths. The actual `load_manifest`, `run`, exact metadata/file verifier, publication readback, DOI resolver and receipt construction remain unchanged; no kit function is replaced. The dispatcher permits only production check/stage/inspect/publish. Native `update()` re-reads and verifies already-exact metadata without PUT.

## F1: code and manifest snapshots

The reviewed `run_native_transport.py` bootstrap captures adapter source once, verifies its literal SHA-256 pin before any adapter statement executes, and compiles those same bytes in a fresh module. It never reuses `sys.modules['native_transport']`; direct adapter script entry refuses dispatch. The adapter does the same for the kit before any kit top-level execution, using standard-library hashing rather than unverified kit methods. It neither imports nor replaces `sys.modules['zenodo']`. A pathname swap or restoration after capture cannot replace executed bytes.

The manifest is captured once and hashed before parsing. The unchanged kit receives an immutable Path protocol whose `read_text()` returns those exact bytes. Relative paths resolve only to the captured reviewed payloads. The kit still parses the manifest, validates names/limits and computes both checksums; it never reopens the mutable manifest or payload sources. Production state uses the original absolute manifest string.

The bootstrap is the trusted entry point. `LAUNCH_INSTRUCTIONS.md` gives a parent invocation that itself captures/hash-checks/executes the bootstrap in one operation, avoiding a pathname-check/reopen race at the entry point. Its approved inline Python text is the root of trust. Shared bytecode writes are disabled; captured compile/exec does not use repository module caches.

Controls cover stale preloaded modules, rejection before unreviewed top-level side effects, single-read kit/adapter source swaps, exactly one manifest and one read per payload, later path/manifest drift without mutable reopens, direct script refusal, and unsupported workflow/environment rejection.

## F2: automatic DOI and OAI

Confirmed publication requires version DOI **10.5281/zenodo.23356540** with DataCite provider and, when present, the exact DataCite client; and precisely **`{"identifier":"oai:zenodo.org:23356540","provider":"oai"}`**. Unknown schemes, wrong IDs/providers/clients, extra fields, malformed shapes and explicit null DOI clients are rejected. An empty initial-draft PID map remains valid. Assigned/reserved identifiers alone never establish publication.

The official [OAI provider](https://github.com/inveniosoftware/invenio-rdm-records/blob/master/invenio_rdm_records/services/pids/providers/oai.py) derives its identifier from configured prefix and record ID. The official [publication PID component](https://github.com/inveniosoftware/invenio-rdm-records/blob/master/invenio_rdm_records/services/components/pids.py) supplies required schemes. Review1's preserved primary evidence establishes DOI/OAI creation from empty PIDs for this public initial record. The parent's filtered deployed calibration binds the legitimate DOI/OAI shape on prior own record 23331709, SHA-256 `0cefe0f05e05507d594066a4d4103891e0ec480337e8cd62a9093c1f38cdfdff`.

The backend now generates both PIDs. Normal publication, lost-response recovery, read-only inspect and repeated publication exercise the actual kit receipt over this complete map. Thirteen hostile/missing PID cases remain rejected.

## F3: immutable transmitted payloads

Each PDF/ZIP source is read once into immutable bytes before client construction. Size, SHA-256 and pinned MD5 are checked on those exact bytes. A mixed or changed capture is rejected before upload. A read-only frozen file protocol supplies stat/open to the existing kit transport; all transmitted chunks come from checked immutable bytes, with no second mutable pathname stat/open. Raw Path payloads are rejected. The original kit verifier still runs after transfer, and the adapter independently downloads completed native content for SHA-256 verification.

Positive controls replace a private source immediately before PUT, and replace plus modify its inode while the actual unchanged kit sends successive 1,024-byte chunks. Transmitted size, SHA-256 and MD5 remain exact while the pathname's bytes change. Negative controls reject changed/mixed captures, raw Paths and snapshot mutation before API writes. Committed checksums are computed from actual transmitted bytes. No original paper/archive source was modified.

## F4: supported native download negotiation

Completed/pending content GET uses `Accept: */*`, while content PUT remains `Content-Type: application/octet-stream`. There is no alternate-endpoint/redirect/authentication fallback or automatic request retry. HTTP 200, exact byte bounds and SHA-256 are still required.

The parent's preserved filtered calibration on its already accepted own PR618 PDF returned HTTP 406/88-byte JSON for octet-stream acceptance, then HTTP 200 with the exact known 69,859-byte PDF for wildcard acceptance. The successful SHA-256 is `f09744993126d2d7e195115ae65046054626c6a5197566146340dc5bfea9ce82`; no redirects, authorization or mutations were involved in those parent public reads. `NATIVE_PUBLISHED_CONTENT_CALIBRATION.json` and `NATIVE_PUBLISHED_CONTENT_WILDCARD_CALIBRATION.json` remain unchanged and are hash-bound in this author's source/input receipts. This author did not contact that other record.

A negotiation-aware fake endpoint returns 406 if the actual download header is wrong and yields bytes only for wildcard acceptance. The real reader must produce the reviewed SHA-256 with one request. The actual kit streaming control independently verifies upload Content-Type remains octet-stream. This repairs a deployed compatibility failure, without claiming that own draft 23356540 has uploaded content yet.

## O1: sync barriers and precise limits

Every mutation has atomically saved intent before dispatch: temporary-file flush/fsync, replacement, journal-directory fsync and parent-directory fsync. New directory chains also receive directory/parent barriers. Any sync/storage failure sets a process fail-stop flag; later reads cannot enable another mutation in that process. Real fsync instrumentation confirms all barriers precede every modeled dispatch. File, directory, parent and post-acknowledgment failure controls stop later writes. Fresh-client restart still prohibits repeating uncertain operations.

These are software barriers under the OS/filesystem contract. **No destructive power-loss, kernel-crash, hardware-cache or storage-rollback test was conducted or claimed.** Ordinary process-interruption recovery is tested. The unchanged kit's separate final publication receipt retains atomic replacement without fsync, and `receipt_saved` retains its exact kit meaning. Receipt failure does not fabricate unpublication. The synced attempt journal independently prohibits blind repetition; a later read-only inspect can regenerate a confirmed receipt. This is not a claim that all local files have power-loss guarantees.

## Ambiguity, live evidence and unchanged inputs

No initialize/content/commit/publish operation is automatically sent twice, even after restart. Lost initialize requires its registered key readback. Lost content PUT requires independently verified pending SHA-256 or stops without PUT/commit retry. A valid content acknowledgment permits reversible commit, then exact committed size/MD5/downloaded-SHA checks before publication. Lost commit requires completed readback. Lost publish uses the kit's independent native published readback; an unchanged draft receives no repeated POST.

The repaired-source read-only preflight at **2026-10-14T05:04:14.082315Z** confirms exact pinned native metadata, unpublished draft 23356540 and zero completed/pending files. `REPAIRED_READONLY_PREFLIGHT.json` is a preflight, not a publication/readiness receipt. Numeric `0` for `access.embargo.active` is rejected; only Boolean `False` is allowed.

`REPAIR_INPUT_RECHECK.json` confirms **45/45** publication pins and **29/29** native pins unchanged, all 18 original-review artifact pins unchanged, and the original author snapshot intact. Native original-commit identity was independently established by review1; these checks preserve its exact bytes. No shared paper/ZIP/metadata/helper/global kit/index/branch/remote/tracker was edited. Full downloaded sources remain in ignored tmp.

## Remaining gap

A new independent adversary must review the repaired source/bootstrap/tests/receipts. Production file acknowledgments, pending-content availability after ambiguous PUT, this draft's actual final representation, external DOI registration/resolution and the final real kit receipt remain unexecuted. Unexpected shapes fail closed; no replacement deposit, metadata simplification, delete/reupload or weakened check is supported. The local lock does not prevent other-machine/browser edits, and no server-atomic read/publish transaction is claimed.

Assigned author repair work: **100%**. Estimated operational readiness: **85%**, pending fresh review and live boundaries. Publication itself remains unfinished.
