# Author turn 5 — scalar global criterion and exhausted outcome

2026-10-03 06:45 UTC. Fifth and final substantive author turn. **EXHAUSTED, global question unresolved.** Completion estimate toward a complete resolution remains 10%, with no implication that another short attempt would suffice.

The final approach attempts to promote the equatorial calculation to a whole-surface certificate by retaining every angular derivative of the Jacobi Dirichlet-to-Neumann value. It produces the following exact criterion, but does not establish its sign globally for the candidate metric.

## A full two-dimensional null-pair criterion

Fix a surface point p and a minimizing nonconjugate tangent v. Rotate the orthonormal tangent basis so v=r e2, r>0. For nearby tangent vectors z=(b,s), write H(z) for the transverse eigenvalue of the first-variable squared-distance Hessian. All partial derivatives below are evaluated at (b,s)=(0,r); they include the change in the geodesic when z varies. They are not derivatives of a fixed one-dimensional curvature profile alone.

The exact matrix is A(z)=I+(H(z)−1)(I−zz^T/|z|²). Its relevant second derivatives are

A11,bb=H_bb−2(H−1)/r²,
A11,bs=H_bs,
A11,ss=H_ss,
A22,bb=2(H−1)/r²,
A22,bs=A22,ss=0,
A12,bb=−2H_b/r,
A12,bs=−H_s/r+(H−1)/r²,
A12,ss=0.

For u=(cosθ,sinθ) and w=(−sinθ,cosθ), direct substitution gives

S(v;u,w)=P cos⁴θ + 2H_bs cos³θ sinθ + R cos²θ sin²θ
          + (4H_b/r)cosθ sin³θ + Q sin⁴θ,

where P=−H_ss, Q=2(1−H)/r², and
R=−H_bb−4H_s/r+6(H−1)/r².

Therefore A3w at this source/endpoint pair is equivalent to nonnegativity on the real line of the quartic

q(t)=P+2H_bs t+R t²+(4H_b/r)t³+Q t⁴,

together with the limiting vertical direction Q>=0. The statement includes arbitrary lengths by homogeneity. At the diagonal use the smooth curvature limit. At an equatorial source/target pair, reflection symmetry removes H_b and H_bs and recovers turn 3.

This criterion is an algebraic expansion of the standard squared-distance Hessian representation, not a claimed new general theorem. It shows precisely why equatorial symmetry does not finish the problem: the two odd coefficients can be nonzero elsewhere, and the even coefficients also change.

## The sharp remaining verification task for the explicit family

For any chosen a in (1/18,1/6), let D_p be the interior tangent injectivity domain of the complete sphere metric g_a from turn 2. To obtain a genuine global counterexample it remains necessary to prove

q_{p,v}(t)>=0 for every p in S², every v in D_p, and every real t,

with the diagonal limits included and H computed from the Jacobi boundary problem along the minimizing g_a-geodesic. This requires both the complete minimizing domain and uniform sign control, including approach to its cut/conjugate boundary. The attempt has neither a proof nor a rigorous counterexample to that assertion. It is not enough to show no conjugate point on a selected geodesic or sample a finite grid.

A global proof of A3w⇒NNCC for arbitrary complete manifolds would have to use an additional global mechanism. The local and exact finite examples rule out proving the implication from only the pointwise null inequality plus local squared-distance realization. The flat-product equivalence of turn 4 reformulates, but does not remove, that global difficulty.

## Final status and retained results

1. Source and prior gate: passed provisionally, with the literal OWR wording distinguished from the global complete-manifold convention in its cited paper.
2. Global original implication: unresolved; no full solution or counterexample claimed.
3. Local restricted-domain implication: an explicit geometric negative example is established in the author calculations, pending independent review.
4. Compact sphere family: smooth, complete, globally positively curved; fails NNCC with exact witness 7/10−8/π² at a=1/10.
5. Its entire equatorial off-cut slice satisfies strict A3w, for every null direction; global A3w remains unverified.
6. Numerical diagnostics: no numerical claim is used as proof. Coarse apparent weak-MTW negatives were unstable or came with unverified/nonminimizing branches.
7. Full work is frozen after 5/5 substantive author turns for independent review. Review may falsify or certify these statements; it is not an extension of the unfinished global proof search.
