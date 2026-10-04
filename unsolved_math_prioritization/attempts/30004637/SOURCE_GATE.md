# Source and prior-work gate

Checked 2026-10-04 UTC. Rank 560; ID 30004637; OWR-4990379-007.

## Identification

The requested catalogue page, https://www.unsolvedmath.com/problems/30004637 ,
returned HTTP 403 on direct retrieval. Web opening failed too. No denial was
bypassed. Its matching record was recovered from the independently public
Ulam AI dataset, pinned at revision
`372682f27c1b0d3d39e75fa63ad7932c7a2e1bde`:

https://huggingface.co/datasets/ulamai/UnsolvedMath/blob/372682f27c1b0d3d39e75fa63ad7932c7a2e1bde/problems.json

The local problems JSON SHA-256 is
`37067f43734b76ee886b032469836767c34d892de14397ce6aa71da01500e252`, matching the
pinned tree's LFS hash. The record maps the requested title and ID to the OWR
report below. Its generated August 2026 “open” assessment checked only that
report and is not mathematical authority. The pinned `research_results.json`
has no entry for this problem code, ID, or report code. Its hash is recorded in
`SOURCE_MANIFEST.json`. Neither corpus nor extracted rows are included in this
public packet.

## Primary question

A. Baradat, joint with H. Lavenant, “Regularized unbalanced optimal transport
and the large deviations of the branching Brownian motion,” in *Applications
of Optimal Transportation in the Natural Sciences*, OWR 10/2021, pp. 552–555.

- https://doi.org/10.4171/OWR/2021/10
- https://ems.press/content/serial-article-files/46885

The entire four-page contribution was read. Printed p. 555, §3.2, was also
rendered and visually checked. The target is the preceding dynamical RUOT
functional, with diffusion and a growth penalty determined by the offspring
law. The report asks for a fast algorithm without specifying complexity or an
accuracy model. Our note preserves that target and labels finite-grid and
binary-offspring restrictions explicitly.

## Later work and exact scope

A. Baradat and H. Lavenant,
https://arxiv.org/abs/2111.01666v2 , 13 December 2021, is the latest version
shown by arXiv on the check date. The complete §6.3, pp. 115–122, and relevant
Appendix A growth-penalty formulas were read, including the full proof of
Lemma 6.17. Printed p. 122 was visually checked. The authors already construct
a dynamical convex-optimization method and supply code. Remark 6.14 leaves
continuum convergence untreated; finite-grid optimization does not settle that
issue. The derivative and monotonicity corrections in our Proposition 1 are
obtained by direct differentiation, not by copying a faulty displayed formula.
No unrestricted Douglas–Rachford convergence statement is imported.

The publisher confirms the 2025 Astérisque monograph, volume 458:
https://doi.org/10.24033/ast.1247 . Its official sample and description were
checked. Full 2025 text was not available through that sample, so no claim is
made that its proof details or typographical errors coincide with the preprint.
Our mathematical dependencies are proved in full in `PROOF.md`.

J. Ying et al., https://arxiv.org/abs/2605.00545v2 , was checked at the latest
version shown by arXiv, 10 June 2026. Sections 3.4, 4.6 and 7, Appendix B.3 and
its formulas, and Appendix C.11 were inspected in the full paper. The method
uses a WFR approximation for the RUOT semi-coupling; C.11 supplies small
numerical comparisons. We found no error guarantee there settling the general
OWR target. A prior v1 read was superseded by this v2 check; v1's parameter
formulas are not used.

The author project page https://sophtang.github.io/branch-sbm/ was also checked:
its displayed objective is a branched multi-target model with state potential
and learned branch weights. It does not establish an exact algorithm for the
OWR offspring-penalty objective. No theorem in that work is used here.

Searches for the exact title, branching Schrödinger algorithms, and branching
Brownian RUOT convergence were performed. This is a bounded literature check,
not a claim to have exhaustively classified all algorithms as of this date.
No full resolution was verified.

## Actual repository history and attempt check

The following was checked beyond the live QUEUE row:

- The live `unsolved_math_prioritization/QUEUE.md` row has rank 560, ID
  30004637, status `queued`, and turns `0/5`.
- At main tree `fd3ccfc6435ef2f76ad371c119756c8ce080dfed`, an untruncated root
  tree had no matching named effort. The full recursive repository tree was
  truncated and was NOT accepted as evidence of absence.
- Separate untruncated recursive trees for `problems/` (652 entries) and
  `unsolved_math_prioritization/` (14,699 entries) had no path containing
  `30004637`, `4990379`, or `branching_brownian`.
- The pinned queue `state.json` contains no entry for this ID; its
  `history.jsonl` contains no matching history entry.
- The exact row in `review_v2/reviews_5.json` was read. It is only a desk
  review proposing convex dual splitting, with iteration complexity and
  discretization control explicitly left as gaps. It is not a previous proof.
- `review_v2/related_target_groups.json` contains no group for this ID.
- Connector searches over all PR states by ID, report code, “Branching
  Brownian,” and “unbalanced transport” returned no PR. Commit search by ID
  and branch search by ID returned none. Code search was also tried but is
  not treated as exhaustive because index completeness was not verified.

These are bounded negative checks, not proof that no obscure branch or unrelated
filename could contain an unindexed attempt. No existing same-problem attempt
was found, and no existing PR was duplicated or modified.

## Publication boundary

Only the author-written files under this packet's `public/` directory are
proposed for publication at `unsolved_math_prioritization/attempts/30004637/`.
Downloaded papers, page images, source extractions, corpora, and raw tool results
stay local. Source hashes and public URLs are attribution/provenance only.
The requested own-row queue delta is `partial`, `5/5`; it changes only those
two cells. No `queue.py` execution, automatic exhaustion marker, merge, release,
or external correspondence has occurred. Independent review is a separate gate
before any remote write.
