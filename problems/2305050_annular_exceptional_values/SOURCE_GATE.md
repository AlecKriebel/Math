# Source and prior-work gate

Checked 2026-10-03 UTC.

## Exact primary target

- Catalogue locator: https://www.unsolvedmath.com/problems/2305050 (AMR-022-5050).
- The live request returned HTTP 403. A previously pinned catalogue record was used only to identify the problem and its cited primary source. Its generated status summary was not accepted as mathematical evidence.
- Hayman–Lingham, [arXiv:1809.07200](https://arxiv.org/abs/1809.07200), PDF leaf 105 / printed p. 104: Problem 5.50 and its update were read and visually checked. The update credits Carroll's countably infinite example. Reference [145] identifies the 1979 paper.
- The imported statement's unusual cardinal symbol is interpreted as countable infinity, consistently with the primary update and the resolving paper.

## Resolving primary publication

F. W. Carroll, *A strongly annular function with countably many singular values*, Math. Scand. 44 (1979), 330–334, [DOI 10.7146/math.scand.a-11814](https://doi.org/10.7146/math.scand.a-11814).

The publisher's complete five-page PDF was obtained and all pages read visually. Scope:

- p. 330: definitions, countability fact, and Theorem 2.
- pp. 330–331: cap geometry and Lemma A.
- pp. 331–333: all five invariants in Theorem 1, initial stage, inductive approximation, coefficient system and gap-closing argument.
- pp. 333–334: complete supplied proof of Lemma A, with its stated Arakelian approximation dependency.

The paper's definition of singular values agrees with the problem's S(f). The result is explicitly countably infinite, and strong annularity implies the required annularity.

## Supporting primary publication

A. Osada, *On the distribution of a-points of a strongly annular function*, Pacific J. Math. 68 (1977), 491–496. The full mathematical paper was read, with displayed formulas on pp. 493–495 checked against page images. Its p. 491 gives the disjointness/countability implication, attributing it to Koebe–Gross. Its two-value construction is background, not the source of the countably infinite conclusion.

Arakelian approximation and Koebe–Gross are credited external theorem inputs; their original foundational proofs are not independently re-proved here. This is a checked application and attribution of an established theorem, not an assertion of a new construction from elementary facts.

## Prior repository work

Read-only checks in AlecKriebel/Math were performed before drafting:

- Exact ID, exact code, the combination “5.50” and “annular”, and “Carroll” found no matching PR in all states.
- “annular” found PRs 322 and 375, whose returned titles and bodies concern unrelated probability problems.
- Exact-ID branch and commit searches found no results.
- Default-branch code searches for the ID, “annular”, and “Carroll” returned no results. These are not treated as exhaustive, because search-index coverage can be incomplete.
- The actual root directory listing and the complete, nontruncated 580-entry `problems` subtree were checked; neither contained a matching ID/topic path.
- The target queue row separately read `queued`, `0/5`. That row alone was not used as evidence that no prior PR exists.
- The whole-repository recursive tree request failed with a transport error. The checks above support “no matching prior work found”, not a guarantee of exhaustive repository history.

## Decision

The exact mathematical target has a published affirmative solution. Proposed disposition: `already_solved`, `1/5`. The remaining work is independent checking and repository integration of this attribution note, not further attempts to resolve the original problem. No original theorem, priority claim, or present-day exhaustive literature search is asserted.
