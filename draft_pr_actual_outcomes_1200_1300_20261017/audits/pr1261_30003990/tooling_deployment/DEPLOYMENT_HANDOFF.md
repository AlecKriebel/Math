# PR1261 actual helper deployment

This seals deployed tooling, not the paper/package or its mathematical,
priority or publication acceptance. Different fresh actual whole-package
reviews remain required. Root owns the manuscript, actual context/metadata,
compile/layout receipts and release actions; this effort did not write them.
No service call, Git mutation, real package preparation or release operation
was performed. The earlier sealed workflow proposal remains byte-identical.

## Actual locations

Eight deployed helpers are in audit `publication/`:

```
prepare_package.py
build_package.py
compile_note.py
verification/verify.py
append_tracker.py
update_pr_publication.py
check_public_downloads.py
workflow_regression.py
```

The operative coordinator is the program-level
`publication_coordinators/pr1261.py`. It derives the program from its own file
and explicitly selects `audits/pr1261_30003990/publication`; it does not assume
it lives inside publication. The tests copy it to that exact program/coordinator
layout and exercise its real release-authentication and actual shared-kit run
with all network clients mocked.

The required workflow gate still contains exactly eight deployed workflow
hashes plus `deposit_coordinator_sha256` and `shared_kit_sha256`. The coordinator
is outside the eight-script directory. `DEPLOYMENT_FREEZE.json` binds all nine
code files, both authored ignore files and this deployment's reports/log.
Root-owned publication artifacts are not authored outputs of this tooling seal.

The seven current/original mathematical files and twelve desired PR paths are
unchanged from the original proposal's contract. The exact four supplied prose
and two structured records are required; PUBLIC_MANIFEST binds the other six.
Historical seven are checked against snapshot SHA256 sizes and Git blob IDs.
Title, metadata, expected page count and proof/priority wording come from root's
explicit context; there is no old problem/DOI or fixed page-count inheritance.

## Explicit registry additions and absolute relocation

Base registry keys are exactly:

```
path, base, entries_key, path_key, size_key, sha256
```

For ordinary relative schemas these six suffice. An optional
`path_mode: "relative"` is accepted. The new relative triples are
`files/relative_path/bytes` and `authored_files/relative_path/bytes`, alongside
the existing explicit allowlist. Absolute fields that accompany selected
relative_path fields are never followed.

The only absolute-membership triples are:

```
members/path/bytes
authored_members/path/bytes
authored_outputs/path/bytes
```

They require `path_mode: "absolute_under_family_root"`. The selected immutable
manifest's `family_root` is the default anchor. The adversary detached cross
actually uses `review_root`, so that registry entry additionally requires
`absolute_root_key: "review_root"`. The optional anchor key is allowlisted to
`family_root` or `review_root`, and is allowed only with the absolute mode.
There is no field/schema guessing.

Absolute normalization is a PurePosixPath string operation: require canonical
absolute anchor/member paths, no traversal/backslashes, an anchor ending with
the registered relative base, and the member strictly inside that anchor.
Convert only to a safe relative name, then read `extracted_root/base/name`.
Original host absolute member paths are never opened, resolved or followed.
Immutable original manifest bytes are retained. The exposed
`manifest_member_name(registry, member, manifest_json)` applies this rule when
root constructs its explicit portable inventory.

The nine actual current manifest schemas authenticated read-only were:

| Path | Selected authored membership | Count |
|---|---|---:|
| reviews/source_question_family/manifest.json | files/relative_path/size_bytes | 7 |
| reviews/analytic_adversary/MANIFEST.json | authored_artifacts/relative_path/bytes | 10 |
| reviews/independent_derivation_adversary/manifest.json | files/relative_path/bytes | 13 |
| reviews/spectral_family/manifest.json | authored_files/relative_path/bytes | 9 |
| reviews/spectral_adversary/MANIFEST.json | files/relative_path/bytes | 9 |
| priority/independent/MANIFEST.json | members/path/bytes, absolute family_root | 15 |
| priority/adversary/MANIFEST.json | authored_files/path/bytes, relative | 29 |
| priority/independent/CROSS_CHALLENGE_MANIFEST.json | authored_members/path/bytes, absolute family_root | 2 |
| priority/adversary/CROSS_CHALLENGE_MANIFEST.json | authored_outputs/path/bytes, absolute review_root | 2 |

Only these selected lists determine membership. Other authenticated-input,
read/source/scratch and outside-anchor arrays remain receipts. The provided
INPUT_FREEZE in a family's authenticated membership can be portable role
`historical_receipt`; this does not pretend it was newly authored or recursively
interpret its input list as retained source-body membership.

`portable_files` must include every selected manifest/member under its safe
relative destination and preserve source_receipt/historical_receipt distinctions.
The checker still requires outside root-manifest, context and snapshot hashes;
coupled outer rewrites fail against nested/context anchors.

## Correct whole-package review policy

Minimum two sequential actual fresh whole-package reviews with different
reviewer IDs. The latest must be literal CLEAN and cover current inputs.
Earlier rounds may be CLEAN or CHANGES_REQUIRED. There is no requirement for
two CLEAN-current rounds after repairing a first review.

Each `reviews` record (and `latest_review`, exactly the final record) supplies:

```
status, actual_review=true, reviewer_id, context_sha256,
report, report_sha256,
verdict, verdict_sha256,
manifest, manifest_sha256,
manifest_schema: {entries_key, path_key, size_key},
input_freeze, input_freeze_sha256
```

Evidence paths are publication-relative paths within this audit's reviews tree.
The explicit reviewer manifest schema must be one of the supported relative
triples; it authenticates retained authored outputs and must include the report
and verdict. Its own digest is the outside record anchor. Report, verdict,
manifest and input inventory are all independently hash-bound.

The literal verdict retains schema `math-pr1261-whole-package-review-v1`,
matching `status`, `actual_review`, `reviewer_id`, `pr=1261`,
`problem_id=30003990`, original_head, `current_context_sha256` equal to that
round's record.context_sha256, input_freeze_sha256 and actual ISO UTC at_utc.
Review timestamps must increase strictly. The latest context equals the actual
gate/current context; earlier context hashes may legitimately differ.

Historical input inventories (`files` plus `external_readonly_inputs`, each
path/bytes/sha256) are authenticated as immutable files and structurally checked.
Their historical member hashes are retained rather than falsely required to
equal repaired current files. Each inventory must bind that round's exact
context hash at the current-context path. Latest member bytes are all checked
against current files, with no such historical exemption.

Every earlier CHANGES_REQUIRED record additionally supplies `resolution` and
`resolution_sha256`, pointing inside this audit to an explicit root-authored
receipt. It must have:

```
schema: math-pr1261-review-resolution-v1
status: RESOLVED
pr, problem_id, original_head, reviewer_id
review_verdict_sha256, review_input_freeze_sha256, review_context_sha256
resolved_context_sha256 (the latest context)
at_utc
items: [{finding, resolution, evidence}, ...]
```

All items are nonempty explicit strings. The receipt must follow the findings
and precede the latest CLEAN review. The latest input inventory also covers
all earlier report/verdict/manifest/input-inventory files and root resolutions.
It covers all eight actual helper files, operative coordinator, shared kit,
source/PDF/ZIP/metadata, compile/layout/build receipts, context/math/priority
gates/snapshot, original/current seven, explicit retained portable files and
every extracted verification-package file. It checks actual original blob
identities and current-edition/context equivalence as well.

No real final review gate or synthetic reviewer record was written at the
actual audit/publication root. Synthetic gates/reviewer records exist only in
discarded ignored fixtures. Root must obtain actual fresh reviewer evidence.

## Replay and publication guards

Reading root_exact_checks.py showed only top-level at_utc varies in its stdout;
program_sha256 and result must remain exact. New comparison
`json_ignore_at_utc` drops only top-level at_utc. Use isolated layout, stdout
output and normal_O_OO mode for root's portable expected stdout record. No
root checker or expected record was edited or generated by this effort.
Nested runtime-looking fields and program hashes remain significant.

Existing analytic `json_ignore_runtime` excludes only its top-level run_utc,
python and optimization fields. Original-submission replay reconstructs a
temporary snapshot/submitted/reviews layout without altering frozen code.
Source-family assertion-based checks still run normal-only on temporary copies
regardless of the outer optimization mode. No general runtime-field ignore,
historical omitted-code replay or infinite theorem certification is claimed.

The actual shared Zenodo kit remains unchanged. Strict verify is installed in
the actual module object performing its actual run: fresh same-known-ID inspect
precedes publication; the kit performs its second GET/strict verification before
its publish POST. Exclusive stage/publish intents permit one attempt; uncertain
or already-published outcomes reconcile the known ID read-only. Actual current
build document/context/gate bindings and archived context/compile/layout bytes
must also match current root records before staging/publication.

Canonical DOI/record identity, all eleven supplied public metadata fields,
artifact hashes, full tracker row/blank B/tab headers/idempotent intent/readback,
and PR actual parent/path/blob/body/remote/no-index/no-force guards remain.
Root user authorization needs no additional consent gate. No GitHub release.

## Validation and remaining work

`DEPLOYMENT_VALIDATION.json` contains the complete synthetic normal/-O/-OO
receipt and read-only actual schema/syntax observations. It also reports any
actual current local metadata projected offline (not public verification).
The replay command is `python -B publication/workflow_regression.py`; fresh
scratch receipts are written only to `tooling_deployment/_local/`, so rerunning
does not edit sealed reports. No service/Git mutation is permitted by the tests.

Root must prepare/build the actual package, obtain different actual fresh
sequential whole-package reviews, resolve findings, construct the real final
gate and perform actual read-only live preflights before any authorized release
operations. This tooling seal grants no approval or clearance. Real PDF/source
quality and live API compatibility remain outside these synthetic tests.

No edits to deployed authored files/reports follow this seal. Outside hashes
for the deployment freeze and handoff/validation are delivered to root.
