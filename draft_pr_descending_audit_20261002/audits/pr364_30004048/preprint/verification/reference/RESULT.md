# 30004048: complete negative symmetry candidate at turn3/5

**Candidate result, pending full independent review:** the exact biconstrained function is not symmetric. In particular,

       |ψ(13/27,14/27)−ψ(14/27,13/27)| >= 1/108.

This concerns the source's universal values over all finite simple tripartite graphs with all four degree constraints. It is not inferred from reversing one graph or from a finite-support optimization. The actual values and their ordering are not evaluated.

## The universal step

For rational θ in(0,1), define d(θ) as the minimum integer maximum row degree of a finite positive rational θ-regular binary incidence template with distinct columns. TURN_3.md proves, in both directions,

                         ψ(1−θ,θ)=1−θ/d(θ).

The lower bound covers every admissible finite graph. Full-reach graphs are separated first; otherwise boundary equality forces exact B–C regularity. Repeated C-neighborhoods are grouped, and the disjoint missing A classes give the integer-degree bound. The upper bound is an explicit positive rational weighting, with a possible zero universal class omitted, followed by an ordinary finite blow-up. The proof does not assume that the infimum defining ψ is attained; rational boundary attainment follows from the integer minimum.

## The explicit credited seed

The top bipartite part of Figure1 in Chudnovsky–Hompe–Scott–Seymour–Spirkl, EJC29(2)(2022),P2.47, printed6, is a13/27-regular seven-type matrix. Its maximum row degree and that of its complement are both4. Therefore d(13/27),d(14/27) are integers between1 and4. The boundary formula places the two values in disjoint sets: equality would require13e=14d, impossible for those integers. The displayed1/108 separation follows directly.

The seed matrix is an existing primary-source example and is explicitly credited. Two162-vertex blow-ups verify the upper bounds95/108 and47/54, respectively. Those bounds are **not claimed exact**; the universal quantization theorem is what proves non-equality.

## Earlier progress and retained distinctions

Turn1 gives an exact rational-parameter reduction and a uniform sampling theorem with explicit degree slack. Turn2 proves that same-support reversal reweighting can fail even at a pair where the universal values are already known equal; its120-vertex graph is not a counterexample. The final proof does not substitute either of these restricted conclusions for the original question.

The original question is Seymour's OWR1/2019 contribution, printed46–47, especially47/PDF43. SOURCE_SCOPE.md preserves real parameters in(0,1], finite simple graphs, distinct reached vertices, universal graph quantifiers and the four constraints. The published paper's φ symmetry, ψ diagonal and minimal-value cases are credited. Hompe's separate preprint was withdrawn after incorporation into the published paper; it is not a later independent solution.

## Status and reproducibility

Three genuine author turns are complete, with43,755 exact finite assertions replaying byte-for-byte. The third supplies a complete negative candidate, so research stops before turns4–5 under the complete-earlier exception. Full independent analytic/source review is required before publication or a resolved-status announcement.

No novelty certification is made. The attached computation verifies source entries, two ordinary graphs, small boundary-extraction cases and the integer gap; it does not replace the universal proof. FINAL_AUTHOR_MANIFEST.json binds the entire public packet and all historical snapshots remain unchanged.
