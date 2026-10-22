# Narrow terminal kit publish compatibility review01

Disposition: **PASS for this exact single-use compatibility helper.** No additional required defect found in its bounded source-only review.

The prior runtime CLI mismatch is confirmed in source. Installed lifecycle_common.py lines261–266 adds --check-doi whenever check_doi=True; run_zenodo line279 passes True for publish. Actual zenodo.py lines508–515 declares --check-doi only for inspect, with publish requiring --confirm-id. Parser.parse_args occurs at527, before run(args) at529. Thus an unsupported publish flag is rejected before run begins. The reported exact stderr, empty stdout, no POST, and current ready_to_publish record23389367 remain Root-supplied observations; this review did not inspect live state or execute a command.

The helper corrects this narrow argv mismatch by invoking existing kit_call publish with confirm_id=stage['id'] and check_doi=False. Actual kit publish already requests DOI checking internally: both already-published and newly-confirmed published return paths call published_summary(..., True) at477/502. Omitting the unsupported CLI flag does not disable that code path.

Before the corrected write, the helper revalidates the canonical gate and original PR readiness, checks the parser-failure text/empty-output precondition, binds staged ID23389367 and gate hash, pins exact uploader source, and freshly inspects the same record as ready_to_publish. It sanitizes and validates that draft against gate payloads. It exclusively creates CORRECTED_PUBLISH_ATTEMPT_STARTED.json before invoking publish; a repeated helper invocation cannot perform another corrected write. It checks returned ID continuity and uses canonical save_published for exact published receipt/evidence validation. The original attempt marker is retained. Root has stated that the parser-only failure diagnostics will be preserved before a successful command overwrites the standard stdout/stderr paths; that preservation is outside the helper.

Uploader run reloads the manifest and computes local file hashes, reads the saved draft, validates its record ID/state and --confirm-id, verifies exact metadata/file names/checksums before publication, performs at most one publication call, reads back the same record after a possibly lost response, verifies it again, and creates the published summary with automatic DOI checking. Existing normalization/checksum policy is unchanged.

Exact reviewed sources:

- Helper:2423 bytes; SHA2568bae298e7864ceb6d8bac9f5aacf9c13ff0e37f8596b4b042fe203b82119c398; mode0444.
- Actual /Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py:25740 bytes; SHA256a91f961bcabadb15f92bb738c3194f0277cd47f1f87167ac8db8eb7c4fd3b9ca; observed mode0644. The helper checks this exact SHA256 before its service calls.
- Installed canonical lifecycle_common.py:93289 bytes; SHA256140522d5fefd4049cf098da5133690101d34bf12c271f97af5268330b913975a; mode0444, unchanged from frozen08.

INPUT_PINS.json records complete absolute paths/modes. The independent bounded plan was sealed before reading the helper. SOURCE_CHECKS.py reparses sources as inert AST/text and rechecks hashes, parser placement, supported flags, publish DOI behavior, helper call flags/exclusive marker, and all original payload manifest hashes. Run python3 -B SOURCE_CHECKS.py to reproduce. It imports or executes none of the reviewed input files and makes no service/native/Git call. The original eleven frozen review artifacts were verified unchanged.

Scope is source inspection of the exact compatibility helper, relevant uploader parser/publish/verification logic, and canonical kit_call behavior. No publication, live service claim, Root main path, scientific review, authority creation or general hardening campaign occurred. This PASS applies to the bounded helper correction, not direct reuse of the unchanged incompatible canonical publish argv.

Checkpoint:100% of the narrow review goal complete.
