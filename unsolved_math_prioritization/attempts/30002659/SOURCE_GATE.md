# Exact source and readiness gate

Problem 30002659 / OWR-13110-001, queue rank 438. Checked 2026-10-03 (UTC).

## Target and definitions

For every Euclidean convex body of constant width 1, in every dimension n >= 3, must **every** shortest closed generalized billiard trajectory have period 2? The length assertion alone is insufficient unless its equality cases exclude all higher-period minimizers. Bodies may be nonsmooth. A generalized reflection at x_i means that

    n_i = (u_(i-1) - u_i) / |u_(i-1) - u_i|

is an outward unit supporting normal, where u_i = (x_(i+1)-x_i)/|x_(i+1)-x_i|. Consecutive vertices are distinct. For shortest trajectories, redundant repetitions and zero-length edges are omitted. The planar theorem and the period-at-most-n+1 theorem are credited inputs, not discoveries here.

## Primary source

Arseniy Akopyan's contribution, joint work with Alexey Balitskiy, Roman Karasev and Anastasia Sharipova, in *Discrete Geometry*, Oberwolfach Report 40/2014, pp. 2241–2243. The corollary and immediately following open question are on printed p. 2242 (PDF page 8). Roman Karasev's contribution restates the same Euclidean target on printed p. 2258 (PDF page 24, Theorem 10 and the following paragraph).

- Original report: https://publications.mfo.de/handle/mfo/3430
- DOI: https://doi.org/10.4171/OWR/2014/40
- PDF: https://publications.mfo.de/bitstream/handle/mfo/3430/OWR_2014_40.pdf?isAllowed=y&sequence=1

The report is from the 31 August–6 September **2014** workshop, not a 2015 workshop. The generalization is Euclidean; nearby assertions about asymmetric norms are separate.

The live problem URL https://www.unsolvedmath.com/problems/30002659 was attempted first and returned inaccessible through the web tool. The authorized immutable UnsolvedMath fallback was read at revision 37e53eabe540fb458758e198be61634bd02ee008. problems.json SHA-256: 04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf. research_results.json SHA-256: 8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b. Both cached hashes were recomputed. There is no matching research-results entry keyed by this ID or problem code, nor an exact-ID/title match in its values. The imported problem's August 2026 literature triage is background, not proof.

## Current literature check

- D. Bezdek and K. Bezdek, *Shortest billiard trajectories*, Geometriae Dedicata 141 (2009), 197–206. https://doi.org/10.1007/s10711-009-9353-6 ; accessible author manuscript https://arxiv.org/abs/1110.4324 . Theorem 1.1 gives existence and the n+1 period bound; Lemmas 2.3–2.4 supply the translation obstruction. Theorem 1.2 concerns planar fat disk-polygons.
- D. Tsodikovich, *An analogue of the Blaschke–Santaló inequality for billiard dynamics*, Israel Journal of Mathematics 264 (2024), 429–460. https://doi.org/10.1007/s11856-024-2634-9 ; https://arxiv.org/abs/2204.06209 . Remark 2 following Theorem 2 (arXiv PDF p. 3) explicitly still describes the all-dimensional constant-width statement as conjectured.
- Searches including 2025, 2026, higher dimension, counterexample and four-bounce variants located no later resolution. This is a dated search result, not a guarantee of completeness.

## Prior-attempt and duplicate gate

The main-branch QUEUE.md row was queued, 0/5. The complete unsolved_math_prioritization tree (9,376 entries, not truncated) has no attempt folder for 30002659. Root folders, the problems tree and reports tree had no matching ID/code/title path. GitHub code/commit/branch/PR searches for the numeric ID and constant-width title returned no prior substantive attempt. Broader billiard PRs concern confocal elliptic-billiard invariant identities, distinct targets. The related-target-groups file contains no group for this problem. No matching upstream research-results record was located. Imported catalog/desk assessments do not count as Alec's proof attempts.

## Success criterion and budget

A full resolution must either prove the bound and all equality cases for every dimension, or give a verified constant-width body whose shortest trajectory is not 2-periodic. A trajectory of length strictly less than 2 suffices for a counterexample because all period-2 trajectories have length 2. A feasible primitive higher-period trajectory of length exactly 2 also suffices by a dichotomy: either it is minimizing, or the minimum is below 2 and no two-bounce orbit minimizes. Attempt 2 gives the explicit argument. Five substantive author attempts are available; source checks, independent review and packaging do not add proof turns. Public artifacts omit downloaded papers and corpus files. No historical novelty or human peer-review claim is made.
