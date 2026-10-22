# Adversarial publication-helper scope audit for PR 872

Decision: **CLEAR after one type-boundary fix**. Completion estimate: **100%**.

This audit covers only the PR 872 / problem 30006628 repository-prefix exception in `prepare_pr_revision.py` and `record_publication_main.py`, together with the strict key guard added in response to this audit. It does not certify the mathematical result, paper, Zenodo upload, Google Sheet row, actual PR head, actual main tree, or production mapping. Those require their separate evidence and checks.

## Exact reviewed changes

The baseline is commit `f38b229e4ff6e03c00cfc3e05ce537c2f63b7834`. I read both current helpers and the entire tree helper and compared the bytes obtained directly from the baseline Git objects. The current tree helper is byte-identical. Removing only the new scope assignment and strict key guard from the current executable AST yields the baseline AST in both other helpers. No other executable change was found.

For positive integer keys, the legacy prefix `random_property_t_30006628/` is selected only when the PR is exactly 872 and the problem ID is exactly 30006628. All other pairs retain `unsolved_math_prioritization/attempts/<pid>/`. The trailing slash prevents sibling-prefix matches. No mapping field can choose an arbitrary scope. The post-publication helper continues to permit explicitly enumerated files in this program's existing effort directory, as it did before this change.

The initial assignment used numeric tuple equality without type validation. Python therefore treats `(872, 30006628.0)` and `(872.0, 30006628)` as equal to the intended pair. The first offline execution admitted a float PID when the synthetic queue was deliberately made to match its string form. This did not establish that a float mapping could operate against the production queue or GitHub CLI, whose string forms normally differ. I reported the mismatch to the root agent. The root agent then added an explicit `type(...) is int` check for both keys and a positive PID check before any external call. The current fixtures reject float, string, boolean, null, zero, and negative inputs as applicable. `INITIAL_FINDING.json`, both input comparisons, and initial/current diffs preserve the finding and fix history. I made no helper edits.

## Adversarial execution

The public `probes.py` executes the complete current helpers and their unchanged tree helper with a deny-by-default in-memory Git/GitHub command model. Every helper subprocess call is intercepted. It constructs disposable local input/receipt files only inside this audit directory. It makes no actual Git command, network call, commit, checkout, index update, branch update, or queue edit. The mocked push cases exercise the helper's push branches without publishing anything.

Both normal Python and optimized Python (`-O`) passed **107 cases each: 92 expected rejections and 15 accepted fixtures, with 1,182 explicit checks per run**. These checks use runtime conditionals, not Python assertions, so optimization does not disable them. Among the explicit checks are 606 evaluations of the two actual prefix expressions across every PR number 800 through 900 and three distinct problem IDs. A case is a helper execution; individual checks and prefix matrix evaluations are not extra executions or independent mathematical verifications.

Accepted fixtures cover the exact legacy pair, the default scope for a different PR/problem under both baseline and current code, normal and mock-push branches, CRLF target rows, the permitted program directory after publication, queued-main preparation, and idempotent acceptance of the same DOI after merge. The baseline rejects the legacy root, and the new exact pair rejects its former default root.

Expected rejections cover changed PR head, closed PR, non-`claimed_solved` exact-head status, noneligible/conflicting current-main dispositions, conflicting DOI, missing/duplicate queue rows, missing final CLEAR acceptance for push, out-of-range PRs, all cross-problem tuple variants, caller-specified prefix fields, neighboring folder names, absolute/traversing/noncanonical/backslash/NUL paths, duplicate destination paths, local leaf symlinks, changed local SHA256, unmerged state, missing merged ancestry, nonproduction/unpublished/incorrect DOI prefix, protected-file hash changes, protected files in the wrong root, and overlap between receipt writes and protected files. Unknown mocked push failures produce one push attempt and fail, without a blind retry.

For successful full-tree runs, the model independently checks correct commit parent(s), target-queue-only rewriting, unchanged foreign queue bytes, and exact preservation of foreign regular, executable, symlink, Gitlink, non-UTF8-name, and tab-name entries. Branch, index, and worktree sentinels remain unchanged. The command model refuses any checkout/index/reset command. Code inspection confirms that the actual helpers use explicit Git object/tree creation, fresh `origin/main`, and nonforce pushes rather than a checkout or staging operation.

## Guard preservation and remaining operational checks

The PR preparation helper still requires OPEN state, the expected head, and exact `claimed_solved` status at that head. It takes the current main queue from the fetched base, rejects a conflicting disposition or DOI, and preserves unrelated main-tree entries. The post-publication helper still requires CLEAR acceptance, caller-provided confirmed production/published data, a Zenodo DOI prefix, MERGED state, and ancestry of the merge in fetched main. It rechecks every caller-enumerated protected SHA256 and refuses to modify a protected file. The scope exception applies to protected paths as well as updated paths; an old-default protected path is rejected for PR 872.

This is a focused regression audit, not a replacement for Git's own implementation or a live integration test. The tree model exercises the actual recursive parser/writer control flow, but no live branch or production endpoint was exercised. The existing separate tree-helper audit remains relevant to real Git behavior. Root must still validate the concrete accepted mapping, actual prepared/merged trees, production record, metadata/files, and final DOI row.

## Pre-existing limitations, separate from this change

No remaining issue was found in the corrected scope delta. The following existing caller and environment assumptions were preserved, not introduced by the exception:

- The mapping supplies the acceptance status, publication confirmation, expected head, and explicit protected inventory. The helpers are not independent reviewers or Zenodo publication verifiers; an omitted protected file is not inferred automatically.
- PR preparation reads `isDraft` but does not reject a non-draft snapshot. This audit's non-draft fixture is accepted, matching the existing behavior. The caller's prior draft gate remains responsible for draft eligibility.
- The DOI check validates the prefix, not a numeric suffix or DOI resolution. A synthetic nonnumeric suffix is accepted in the corresponding limitation fixture; the separate production receipt/readback is essential.
- Local hashing and later blob creation are separate reads. The environment must keep accepted inputs stable between these reads and validate the resulting Git objects. Leaf symlinks are rejected; ancestor symlinks and special-file/TOCTOU hardening are not comprehensively provided. In preparation, the local file is read before the leaf-symlink rejection. These behaviors are unchanged from baseline.
- Queue findings/turn text and PR-to-problem identity come from a trusted mapping. The helpers do not independently authenticate semantic identity or sanitize arbitrary multiline caller prose. Canonical paths are ultimately enforced by the tree helper.
- The post-publication helper's existing program-directory scope is broad enough for its own effort artifacts. It has not been broadened to other repository directories. The caller must continue to enumerate only its own intended artifacts.

None of these limitations expands because of the literal legacy-root exception. None is a license to skip the root process's independent source, SHA256, queue, merge, publication, or readback evidence.

## Reproduction

From the repository root, with the helper bytes pinned in `INPUT_COMPARISON.json`:

```
python3 -I -B draft_pr_claimed_solved_800_900_20261012/audits/pr872_30006628/publication_scope_audit_01/probes.py --output /tmp/pr872_scope_normal.json
python3 -I -B -O draft_pr_claimed_solved_800_900_20261012/audits/pr872_30006628/publication_scope_audit_01/probes.py --output /tmp/pr872_scope_optimized.json
```

The recorded public outputs are `RESULTS_NORMAL.json` and `RESULTS_OPTIMIZED.json`. Each contains every case, expected/actual outcome, intercepted command sequence, and each explicit check. Paths in these records identify already-removed disposable fixture directories; they are provenance, not required external dependencies. Replaying after helper changes intentionally fails the source pin check rather than silently testing different code.
