# Offline validation of PR1261 tooling proposal

Final checkpoint: 2026-10-17T21:37:05.914625+00:00. Completion estimate: **100% of the delegated
offline tooling proposal**; actual mathematical/priority acceptance, real
paper/artifact assembly and release readiness are unadjudicated here.

`WORKFLOW_REGRESSION_RECEIPT.json` reports PASS in normal, -O and -OO
interpreters with identical result payloads. All nine current code hashes
match the receipt. These tests create fabricated metadata, fake Tectonic and
pdfinfo programs, synthetic PDF bytes and explicitly synthetic reviewer/gate
records only inside ignored `_local/` temporary fixtures, then remove them.
No actual gate or metadata was written at the research audit/publication root.

Enumerated invalid-case rejections per interpreter:

| Family | Rejected cases |
|---|---:|
| context/portable | 30 |
| document assurance | 11 |
| actual reviewer/workflow gate | 13 |
| canonical publication identity | 9 |
| full tracker row/range | 8 |
| each supplied public metadata field | 11 |
| saved PR identity/actual tree | 19 |
| Total | 101 |

Additional full-main/control-flow checks include:

- Complete synthetic compile, prepare, build and portable verifier mains;
  original seven/current seven and six-entry public manifests; dynamic
  three-page fixture with no fixed eight-page assumption. Source-family
  assertions execute in normal mode under every outer mode. Analytic-layout
  fixture reconstructs original snapshot/submitted paths on a temporary copy.
- Actual unchanged shared Zenodo kit.run, with all client methods and DOI
  resolver mocked, performs synthetic stage/inspect/publish. A normalization
  introduced between fresh inspection and the kit's second GET is rejected
  before any publish POST. An unresolved publish intent refuses retry. A lost
  publish response and failed follow-up GET recover the published known ID
  with exactly one total POST. A second stage is blocked by its saved intent.
- The complete tracker main rejects a renamed designated gid before append,
  recovers one accepted append with lost response without appending twice,
  refuses duplicates/full-row collisions, and checks blank B and exact A:D.
- Complete public-download checker main uses a mocked public record and exact
  public artifact bytes. Every one of the eleven supplied metadata fields is
  projected and independently corrupted/rejected; content normalization fails.
- Complete PR update main exercises saved-intent recovery, actual mocked
  parent/path/blob reads, final-body/remote readback and completed idempotent
  recovery. The desired map contains exactly twelve paths (seven plus five).
  Unknown body changes and lost edit responses are tested. The mock permits
  only read-only Git operations; no shared index, force push or real Git
  mutation occurs. Fresh object/tree creation/push is not claimed tested.
- Coupled outer-manifest/payload changes still fail against nested immutable
  anchors; changed registry/context fails against outside context anchor.
  Escaped bases, unsafe relative paths, unsupported schema selection and unused
  absolute-path substitution fail closed. Raw source inventory fields remain
  receipt-only and are not recursively treated as retained source manifests.
- Reviewer tests reject missing/extra/stale eight-script coverage, coordinator
  or actual shared-kit drift, absent/nonactual/nonclean/current-evidence
  mismatch and insufficient sequential whole-package reviews. Document tests
  update outer anchors too and still reject failed/stale compile, partial
  all-page inspection, positive wrong page count and missing actual times.

`SCRIPT_SYNTAX_AND_INPUT_AUDIT.json` separately authenticates the **actual**
read-only original seven submitted file bytes/Git blobs and six-entry original
PUBLIC_MANIFEST, and the **actual** custom source-family seven authored files
plus analytic ten authored files. It uses the selected relative_path and
explicit size keys, ignoring the manifests' absolute-path/scratch inventory
fields. This is byte validation only, not mathematical validation. All thirteen
initial template/input observations remained byte-identical. All nine authored
programs parse; guard enforcement contains no Python assert statements. A
read-only branch observation is `main`.

Limits: no actual paper or metadata existed here. The regression rerun will
compare actual local metadata offline if deployed beside a future
zenodo-deposit.json, but current receipt states it was absent. No real TeX/PDF
compilation/rendering, live original-body positive preflight, real Git object
construction, GWS/Zenodo/GitHub integration or release action was performed.
The tests cannot certify actual new mathematical/priority facts, authorship of
future reviewer assertions, future API compatibility or public DOI resolution.
Different fresh independent full-package reviewers must inspect the actual
final sources/artifacts/receipts before release. No reviewer approval is granted
by this proposal or its synthetic fixtures.
