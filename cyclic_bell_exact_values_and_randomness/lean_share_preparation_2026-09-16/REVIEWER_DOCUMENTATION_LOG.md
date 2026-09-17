# Reviewer documentation checkpoint

2026-09-17 03:34 UTC (2026-09-16 Pacific).

Bounded task: rewrite only lean_formalization/README.md, REVIEWER_GUIDE.md,
COVERAGE.md, and AXIOMS.md for a self-contained external review package.
Completion estimate: 100% of this documentation subtask; package cleanup and
fresh verification remain parent-owned.

The README now introduces the manuscript, pinned source hash, toolchain,
bundled reference paths, reproduction commands, and package layout. The
reviewer guide leads with the literal source coefficients and clock/transpose
conventions, then follows actual models and values, both inequality families,
permutation blindness, reduced-support rigidity, adversarial quantities, and
settings tables. COVERAGE consolidates the claim map and explicitly retains
limits on polar existence, proof-by-proof correspondence, finite privacy,
outer guessing optima, external self-testing, and exposure scope. AXIOMS
separates kernel/axiom evidence, regression controls, static scans, and
manuscript correspondence.

Checks: all named underscore-style theorem identifiers in the new documents
were checked against reference/expected_theorems.json; no missing theorem was
found. Every local Markdown link resolves except the parent-planned
verification/ directory and verification/README.md, which were not yet created
at this checkpoint. Bundled manuscript source/PDF links already resolve. No
links to removed history, development logs, or repair-audit folders remain.
No claims of human independent review or exhaustive line-by-line formalization
were added. No Lean source, scripts, manifests, evidence, or other package
files were edited by this subtask. No outreach text was written or sent.

Follow-up checkpoint: prerequisite text now specifies Python 3.10+, the official
elan installation link, and the pinned toolchain installation command. AXIOMS
also describes fresh-build report parsing and the optional identical standalone
repeat. Package documentation edits are frozen. The bounded read-only parser
review is recorded separately in AXIOM_BUILD_PARSER_REVIEW.md.
