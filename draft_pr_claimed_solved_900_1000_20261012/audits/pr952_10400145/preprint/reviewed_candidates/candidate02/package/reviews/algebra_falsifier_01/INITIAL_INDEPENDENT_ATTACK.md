# Independent initial attack (before candidate or prior reviews)

## Scope and intake

I have authenticated the 33 candidate files mechanically without reading their mathematical contents. I have read only the exact database statement and the publisher source context on printed pp. 490–492. No candidate proof or prior review has yet been read. The source coefficient ring is the cyclotomic completion of Z[q,q^{-1}], and the interpolation variable has nodes q,q^2,... including rank one, whose invariant is set equal to 1.

## Algebraic mechanism

Put h=q-1 and B=Z[h]/(h^2). The coefficient ring has a canonical map to B: for every m>=2 the product (q-1)...(q^m-1) is divisible by h^2, and q is sent to the unit 1+h. Thus one need not assert any completion injectivity to extract first jets.

Let F belong to the inverse limit in t. Its stage-three coordinate is represented by a polynomial P(t) over the coefficient ring and yields all three values at t=q^n for n=1,2,3. After coefficient reduction to B, write P(t)=sum_j (a_j+h b_j)t^j. Since q^n=1+n h in B, P(q^n)=A+h(B_0+n C), where A=sum_j a_j, B_0=sum_j b_j and C=sum_j j a_j. Therefore the constant Taylor term is independent of n and the first Taylor coefficient is affine in n. In particular the first-jet values at ranks one, two, three have zero second difference.

If the normalized perturbative sl_n invariant has first Taylor coefficient equal to a nonzero universal multiple of n(n^2-1) times the Casson invariant, as recalled but NOT YET verified here, the three-rank second difference is nonzero for any homology sphere with nonzero Casson invariant. This would refute the literal interpolation ring. The commonly recalled normalization is n(n^2-1) times Casson, giving coefficients 0,6 lambda,24 lambda and second difference 12 lambda. This is a conditional lead requiring primary-source normalization and a nonzero example, not a claimed verified theorem yet.

## Higher jets and boundaries

At Taylor order d, choose any inverse-limit stage N>d and N at least the largest rank being tested. The Newton polynomial factor of order N has h-adic order at least N after substituting t=q^n; hence the order-d coefficient of P(q^n) is a rational polynomial in n of degree at most d. This gives stronger obstruction families, but first order should suffice.

The stage-three argument works over arbitrary commutative coefficient rings and does not require the completion to be a domain, inverse-limit exactness, a division algorithm for nonmonic polynomials, or torsion-freeness. Monic division does give unique degree<3 representatives. Evaluation must be defined through a sufficiently high stage, since low stages do not evaluate at all ranks. Any proof attempting to evaluate a stage-two coordinate at rank three needs correction.

The obstruction vanishes for the trivial sphere and any zero Casson example, so those are controls rather than counterexamples. In positive characteristic the second difference may vanish accidentally. Over Q[[h]], a renormalized family can satisfy the degree bounds, and an altered coefficient ring with negative h powers can evade them; neither would establish the exact printed ring. A rank shift changes node slopes but still forces an affine first coefficient.

## Falsification targets for candidate intake

1. Verify that the candidate actually uses the printed coefficient ring and rank indexing.
2. Check evaluation through quotient maps, rather than treating an inverse limit as an unrestricted function space.
3. Confirm the first-order Lie algebra coefficient and normalization from primary sources, distinguishing h=q-1 from log(q).
4. Check that any specialization used for the obstruction is genuinely defined on the completed coefficient ring.
5. Check actual values for ranks 1,2,3 and require a nonzero homology-sphere coefficient.
6. Treat the conditional perturbative/unified bridge separately from the elementary algebra; a citation that only gives roots of unity needs an explicit Taylor bridge.

Initial assessment: algebraic obstruction mechanism 70% developed; route review 25%; literal source conclusion unadjudicated pending candidate and primary normalization checks.
