# Credited source-status correction

**Proposed: already_solved0/5, pending independent review.**

The original2010 workshop question asks to compute the irreducible action of a known split central component of a Schurian coherent-configuration algebra without assuming a specially chosen self-adjoint element has distinct roots in the group splitting field. It does not demand a uniform factorization-free polynomial-time algorithm.

Ivanyos–Rónyai–Schicho, *Journal of Algebra*354(2012),211–223, give an explicit algorithm for a number-field algebra promised isomorphic to M_m(K). Its reduced-rank-one output supplies the minimal left ideal and hence the required irreducible action. The original matrix trace form then supplies an exact *-normalization over a finite algebraic extension inside C. `SOURCE_AUDIT.md` verifies this correspondence in detail.

The qualifications are part of the claimed correction:

- K is a genuine splitting field, not merely a character-value field; source character/projector data are supplied at the relevant step
- The algebra action is obtained over K, but a standard-* realization can require positive square roots in a finite extension, as permitted by the source's complex output goal
- The known algorithm terminates for arbitrary finite parameters; its polynomial-time guarantee is only an ff guarantee with the paper's bounded-parameter hypotheses
- Its ff oracle calls factor integers and univariate polynomials over finite fields. This is not an assertion that all factorization is avoided
- No running-time improvement over the source heuristic is proved, and no new algorithm or historical novelty is claimed

The original qualitative question is thereby covered by known work, if the independent reviewer confirms this source interpretation and normalization. Stronger uniformly efficient, all-factorization-free, or strictly original-field orthonormal formulations remain separate. No source executable was run.
