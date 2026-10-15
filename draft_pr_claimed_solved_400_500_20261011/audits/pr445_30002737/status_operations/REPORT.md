# PR445 QUEUE classification operations review

The fixed helper is prepared and tested for the single administrative correction `claimed_solved` → `already_solved` on problem `30002737`, PR445, branch `research/diffraction-dynamical-30002737`, frozen head `3242c84e06db7e99012c7fe581adde5c3f89fc89`. No remote mutation was performed. Apply is unapproved until the root provides its final positive gate and an externally trusted SHA-256 expectation.

## Exact scope and checks

`classify_pr445.py prepare` checks fresh OPEN/DRAFT/main-base metadata, exact branch/ref HEAD, frozen QUEUE hash and exact numeric-ID row. It derives Status/Turns/DOI columns from the header. It verifies all twelve frozen original remote bodies by length and SHA-256, additionally checking immutable Git blob identity and regular-file mode via cached nonrecursive tree paths. The original source receipt is pinned literally to SHA-256 `31ccb9e3e153117812391ca028e2ea458d30eb6ac44699ec575f7a0e07292913`.

The proposed QUEUE bytes change only the selected status text. Rank/other columns, `1/5`, blank DOI, line endings, and every other row byte remain identical. The before SHA-256 is `77c2813566f4eaf2f9bd22e59206f7c8540de8668f5cb649c3abddd8995db24c`; after is `0e5cfa237c47bf64ee456d544c7b1853567e7df35b49da8191c6f978c84d49cb`.

Apply verifies the entire root gate and every declared review binding before mutations. Paths are constrained to the actual PR445 case, excluding symlinks and `..`; duplicate JSON keys, duplicate roles, boolean PR integers, integer approval flags, missing required roles and hash changes are refused. The required roles are `root_disposition`, `priority`, and `numeric_certificate_adversary`; additional unique roles are permitted and fully hash checked. These checks bind the root's decision without independently inferring mathematics, novelty, or paper readiness from review content.

One Git blob, tree, and commit are created. Before PATCH, exact nonrecursive ancestor-tree comparisons require every sibling entry unchanged, establishing that all original source paths and all non-QUEUE entries remain unchanged. The actual commit parent/tree and GitHub commit comparison must show precisely the expected QUEUE modification. A fresh metadata/ref check immediately precedes the single `force:false` ref PATCH. That PATCH is not compare-and-swap; no claim is made that the earlier check is atomic.

After any PATCH attempt, only one branch-ref plus QUEUE reconciliation and essential commit/diff metadata readback occur. No source body or mathematical/review artifact is read afterward. A lost, malformed, or wrong PATCH response is retained explicitly, and an applied state reconciled from readback returns exit 3 rather than pretending the response succeeded. No mutation is retried. Uncertain object POST responses halt with their transaction record preserved.

## Executed evidence

The final offline suite ran 45 materially distinct scenarios in normal Python and `python -O`: **90 actual raw child executions, including 6 positive executions; every asserted behavioral check passed**. `RAW_EXECUTIONS.json` contains the actual argv, exit status, stdout/stderr, and API-call metadata for every run. Counts are computed from these executions. Synthetic source/API/gate fixtures and full stub state remain ignored under `../private_sources/status_operations/`; no foreign fixture body is published.

Controls include changed HEAD/status/branch/DOI/source bytes, closed/nondraft/wrong-base/wrong-repository PRs, malformed gate identities and structural bindings, duplicate JSON keys, invalid source size, truncated trees, changes to other paths, a changed HEAD after object creation, malformed/lost object responses, lost/malformed/wrong PATCH responses, one-time reconciliation, failed post-PATCH integrity checks, and attempts to select another PR. Normal and optimized runs have the same enforcement because checks do not depend on Python assertions.

The first actual live prepare refused safely: the repository-wide recursive tree was truncated. `LIVE_PREPARE_TRUNCATED.json` preserves that failure, with zero mutations. Whole-repository recursive reads were replaced with exact nonrecursive ancestor/sibling comparisons. The revised actual live prepare passed at 2026-10-12T21:29:55.490986+00:00 with 24 GET calls, twelve original byte matches, exact eligible scope, and zero mutations. `LIVE_PREPARE.json` preserves its actual receipt. An earlier 90-control development run is retained privately; final control counts refer to the sealed implementation's rerun.

## Final root gate contract and use

The gate schema is `pr445_queue_classification_gate_v1`; exact string fields are `repo`, `problem_id`, `source_head`, `branch`, `from_status`, `to_status`, and `source_receipt_sha256`. `pr` must be integer 445; `approved` and `genuine_accepted_certificate` must be JSON true. `review_bindings` contains `{role,path,sha256}` objects. Paths may be absolute within the PR445 case or relative to that case. The gate itself must also be a nonsymlink regular file within the case.

For read-only preflight, run `python3 classify_pr445.py prepare` from this folder. Root may later use `python3 classify_pr445.py apply --gate FINAL_ROOT_GATE.json --expected-gate-sha256 <externally-trusted-digest>` and preserve stdout as the operation receipt. No final gate or digest is supplied by this operations review. The synthetic private gates are controls, never root approval.

The digest is a caller-supplied trust boundary. Replacing both the gate and expected digest replaces that trust; the helper does not claim immunity against its trusted caller changing the expectation. Current scope is a low-impact classification correction only. It does not approve publication, create a DOI, mark ready, merge, close, modify prose or proof artifacts, or communicate externally.

Checkpoint: 2026-10-12T21:32:23.531872+00:00. Best-guess completion: **100% for helper preparation and its own executable controls; 95% for operational readiness pending independent adversarial review and final root gate; 0% of the actual remote correction performed**.
