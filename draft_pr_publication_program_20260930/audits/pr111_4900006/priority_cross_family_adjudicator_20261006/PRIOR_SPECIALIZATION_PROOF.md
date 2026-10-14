# Independent prior-specialization proof and claim comparison

This note was prepared on 6 October 2026 as a priority verification exercise, not a new central proof-search turn. No statement below is attributed verbatim to Zelik. The finite-dimensional example is a reviewer specialization of the product, torus, and relative-global-attractor mechanisms inspected in the author PDF, pp. 10–12. The author PDF is undated and its numbering differs from the official 2008 journal version. Exact journal-body identity was not verified.

## Intrinsic manifold example

Let M=R×(R/2πZ)^2 with the flat product metric, and define

    w'=-w, theta_1'=1, theta_2'=sqrt(2).

The flow at time t is (e^{-t}w, theta_1+t, theta_2+sqrt(2)t). It is complete and analytic. The divergence in this product metric is -1. The set A={0}×T² is compact and strictly invariant. For any bounded subset E of M, its distance to A after time t is bounded by e^{-t} sup_E |w|, which converges to zero uniformly. A is therefore a global attractor relative to M, and is minimal: phi_t(A)=A, so any closed set attracting A contains A. For example [-1,1]×T² is a bounded absorbing set for every bounded initial set.

An equilibrium would require both angular velocities to vanish, which is impossible. If T>0 were a period, then T=2πm and sqrt(2)T=2πn for integers m,n. The first equation gives m>0; their quotient gives sqrt(2)=n/m, a contradiction. Thus there are no equilibria and no periodic orbits in this phase space.

The intrinsic derivative in the orthonormal product frame is diag(e^{-t},1,1). Its exact singular values are (1,1,e^{-t}) at every point and positive time. The exponents are (0,0,-1), and exterior-volume exponent sums are (0,0,-1). Both nonnegative-partial-sum pointwise Kaplan–Yorke dimension and the fixed-global-index expression have j=2 and dimension 2. The maximum is attained at every point of A, but never on either proposed orbit class because those classes are empty.

The spectrum is constant, so no interchange of a supremum and a limiting operation is involved. Intrinsic, finite-time, uniform, and asymptotic values coincide for this particular example.

## Ambient embedding matching Parker–Goluskin's convention

Take C²×R=R⁵ and the entire linear field

    z_1'=i z_1, z_2'=i sqrt(2) z_2, w'=-w.

Choose its forward-invariant phase B={|z_1|=|z_2|=1}×R. Its flow on B is exactly the manifold flow above under the standard embedding. It has the same compact relative global attractor, A={|z_1|=|z_2|=1,w=0}, and no equilibrium or periodic orbit in B.

The ambient derivative is a direct sum of two orthogonal plane rotations and e^{-t}. Hence its ambient singular values are (1,1,1,1,e^{-t}), its exponents are (0,0,0,0,-1), and its partial sums are (0,0,0,0,-1). Parker–Goluskin v2 expressly permits embedded-manifold domains on p. 2 and takes tangent vectors in ambient Rⁿ on p. 5. Using this particular explicitly supplied entire extension, their Definition 2.3 on p. 7 gives j=4 and dimension 4 over B. Pointwise finite-time Kaplan–Yorke dimension under this ambient extension is also 4. This dimension is not the intrinsic value 2. A normal extension must be specified because an intrinsic field on an embedded manifold alone need not determine all ambient normal derivatives.

## Why this does not supply the PR111 entire-space theorem

If the same linear field is regarded as a flow on all R⁵, its oscillator radii are invariant. There is no compact global attractor on R⁵: any proposed compact K has a finite maximal first radius M, and a point with first radius M+1 stays at that radius forever, at positive distance from K. Thus it fails to attract that bounded singleton. Negative ambient divergence alone does not repair this failure.

PR111 instead proves a compact global attractor attracting every bounded subset of the entire R⁵ phase; its radius dynamics produce a single equilibrium and four periodic circles in that attractor. Its aperiodic torus attains the maximum 203/50 and strictly exceeds all of those actual competitors under two distinct asymptotic dimension conventions. None of these extra features is supplied by the simple restricted-manifold specialization. They are mathematically substantive differences, regardless of whether the stronger example ultimately has research novelty.

## Exact claim/prior-implication table

| Claim | What the read prior and specialization establish | What they do not establish |
|---|---|---|
| Broad imported question with smooth dissipative global-attractor systems and no domain/chaos restriction | An elementary negative answer on a smooth analytic manifold, with an actual compact relative global attractor and no allowed maximizing orbit classes | A previously printed named Eden disproof, or first-date priority for this particular displayed ODE |
| PG v2 p. 7 assertion under its permitted manifold phases and ambient definition | A counterexample over B with dimension 4 after supplying an explicit linear ambient extension | Intrinsic value 2 under the ambient definition; a compact global attractor on all R⁵ |
| Entire R⁵, complete analytic, uniformly negative divergence, compact minimal global attractor | The verified PR111 proof supplies these properties | No such theorem is deduced from Zelik's displayed torus/product passages alone |
| Nonvacuous strict comparison to an actual equilibrium and all actual periodic orbits | PR111 supplies the comparison and exact 203/50 maximum | The manifold specialization has no competitors; it does not prove the stronger comparison theorem was previously published |
| Historical original Eden conjecture | Read sources demonstrate related and narrower questions and a later broad formulation | Unread thesis p. 98 and unread articles cannot be assigned invented quantifiers or results |
| Claimed novel solution of a genuinely open imported problem | Not established: the broad statement is already contradicted by a routine classical specialization and its secondary 'open' label is unreliable | Neither absence of an exact numerical match nor use of standard components proves novelty or nonnovelty of the strengthened example |

The table distinguishes mathematical implication, primary-source attribution, and research novelty. No new unsolved problem is declared by adding the stronger R⁵/competitor hypotheses after the fact.
