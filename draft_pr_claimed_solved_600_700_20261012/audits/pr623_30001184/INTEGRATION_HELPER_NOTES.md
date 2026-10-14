# PR623 operational helper boundary

The helpers are prepared for parent and sequential whole-package adversarial
review. They have not been run against live services. Fixtures use mocked Git
and GWS operations, disposable local copies, and actual unchanged author/audit
replays. No push, merge, Zenodo write, spreadsheet write, branch deletion,
shared index write or shared checkout write occurred during this preparation.

`prepare_integration.py --doi DOI` prepares a reviewable local merge commit
and `INTEGRATION_PREPARED_RECEIPT.json`. `--push` additionally updates only
`research/30001184-generation-only-gns-counterexample` through a non-force push.
It does not merge the PR or delete the branch. Local `main` must remain selected.
The commit has latest fetched remote main and the selected PR head as parents;
its tree changes only attempt `30001184` and the selected QUEUE row. Only Status,
Turns (retained author total 1/5) and Findings change in that row. Other queue
bytes, including their line endings, are preserved.

The initial head gate precedes candidate/native/publication reads. It accepts
only original head `947442c091ae617804c6a0d07b98ff2c50368798` or the exact commit
in this helper's successfully pushed receipt for the same DOI. The latter is
checked against its recorded parents, scope, complete attempt inventory, queue
hash and frozen inner manifests. Unknown concurrent heads require fresh review.
A separate successful-push receipt survives subsequent dry preparations.
Immediate pre-push head and remote-main guards abort on drift. A failed push is
never automatically repeated; inspect an ambiguous remote outcome first.

Execution requires the production/published compact
`ZENODO_PUBLICATION_RECEIPT.json` and `ZENODO_POST_PUBLICATION_INSPECTION.json`,
matching title, DOI, record and exact PDF/ZIP SHA-256 digests, with DOI resolution
confirmed. The package manifest must inventory every ZIP file exactly and reject
duplicate, unsafe, symlink, extra, missing or mis-hashed members. All original 29
candidate files, the local PDF and TeX, and the current source notice must match
their archived counterparts byte-for-byte. The expected publication files are
`gns_generation_counterexample.pdf`, `gns_generation_counterexample.tex`,
`gns_verification.zip`, and `zenodo-deposit.json`. The default notice source is
`publication/CURRENT_PRIORITY_AND_STATUS.md`; `--source-audit` may select an
identical archived notice elsewhere.

The repaired `publication_inputs` interface returns three values: captured
publication-file bytes, captured archive-validated source-notice bytes, and their
validation record. Each publication, notice and compact receipt path is read
exactly once. Receipt parsing, validation and returned SHA values all use the
same captured immutable bytes. Preparation passes the returned notice bytes
directly into `build_current_files`; it does not reopen the notice. The tracker
consumes the same snapshot contract and validation record. A later change to a
path cannot substitute new bytes into the current preparation or attest an
unvalidated receipt; a fresh validation of the changed input still rejects it.
Inventory schema must satisfy `type(schema) is int` and `schema == 1`, rejecting
JSON Boolean or decimal lookalikes as well as unsupported integer versions.

Current wrapper prose credits **Burgarth–Facchi–Hillier** and the established
clock/evaluation/translated-unitary mechanism, framing this result as an explicit
formulation-specific corollary. It disclaims exhaustive first priority,
independent historical development and human peer review. The verified source
problem is Skeide's first module-approach problem, OWR 2009 pp. 542–543,
<https://doi.org/10.4171/OWR/2009/09>; the tracker uses that primary-source DOI
instead of an unverified catalogue page. The current source notice also preserves
the Dive–Mintert–Burgarth antecedent and the exact unresolved boundaries.

All packet13 and audit11 bytes remain unchanged. In particular, proof SHA-256
remains `f2a1b3b4233c2850d8dd79ba17b464d74343aa66e7d22d12104d17fc5470e8a3`.
Only outer publication files are updated or added: README/current source audit,
PUBLICATION.json/PUBLICATION.md, publication.log, the publication payload, and
the outer verifier/inventory. The exact outer allowlist grows from 28 to 35
manifested files plus the manifest itself. Original frozen-manifest pins and
author/independent replay comparisons stay in place. Integrity-only mode is
strengthened to check every frozen file against its pinned inner inventory;
rehashing the outer inventory cannot conceal a modified frozen proof.

`record_tracker.py --doi DOI` performs read-only preparation of the A:D row;
`--apply` dispatches one append only after refreshed exact gid/title/header and
DOI guards. The solution-chat cell stays blank. An existing exact DOI must have
the exact expected row; duplicates or differing rows abort. An unconfirmed marker
is saved before dispatch, and any ambiguous failure blocks a blind retry.
Successful writes require exact target-row readback and a global exact-DOI
uniqueness/range check. Both the spreadsheet ID and gid are pinned.

The operational fixtures do not establish live API availability, permission,
authentication, remote mergeability or a production write outcome. Google Sheets
does not offer an atomic uniqueness constraint through this append API: an
external simultaneous append can still race the last read; the global readback
detects it and leaves reconciliation required. The compact publishing-tool
receipt attests its metadata verification; this helper directly binds the PDF,
ZIP, source TeX and notice to upload digests/archive contents. The local deposit
intent is hashed in the preparation receipt and must remain part of the reviewed
package. Parent approval of the final mathematical/source/publication package
and clean sequential reviews remains the gate before operational execution.

Operational implementation completion estimate: 100%; live execution completion:
0%. Round2 identified mandatory F1 immutable-byte binding and F2 schema-type
repairs; `reviews/operations_02/check_repairs.py` exercises these repairs plus
all 14 earlier operational controls, under normal and optimized Python. Old
round2 evidence and native29 remain untouched. The parent is rebuilding the
paper/ZIP after its portable-verifier/source-locator repairs; predecessor
publication hashes are not final readiness evidence. Rebinding those rebuilt
artifacts and a new independent whole-package round3 remain required before
publication or integration. The discovery/publication program's broader
percentage is maintained by the parent research log.
