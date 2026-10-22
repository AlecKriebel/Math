# Checkable comparison of the full theorem and proof bridges

This is the auditor's reconstruction, not a reproduction of the manuscript's prose. The comparison uses the frozen submitted proof and the actual Ferudun note0014 v1.0/v1.1 PDF and source bytes. Locations below refer to v1.1's printed pages. The exact scientific computation is supplementary; the universal deductions below do the mathematical work.

## 1. Same geometric objects

Write A=a^2, B=b^2, d=A-B, and 0<lambda<B. Ferudun's caustic has squared semiaxes A-lambda and B-lambda, so its Jacobi modulus k^2=d/(A-lambda) agrees with the candidate's caustic eccentricity. Its delta equals the candidate's v. The definitions in v1.1 p.1 prescribe n(u)=(-sn(u)/a,cn(u)/b), the boundary tangent n(u).X=1, actual successive boundary-tangent intersections, and Q_M=M+(1-M.n)n/(n.n). Hence Q_0=n/(n.n) is exactly the center foot. There is no chord-foot, caustic-contact or negative-pedal substitution. Both use one half of the cyclic determinant sum, so stars retain traversal order.

For h=2delta=4tau K/N, gcd(tau,N)=1, choose 0<tau<N/2. The outer point at the midpoint parameter t of a chord is

    V(t)=(-a dn(delta) sn(t)/cn(delta), b cn(t)/cn(delta)).

Substitution into both endpoint tangent equations gives 1, using sn^2(t)+cn^2(t)=1 and dn^2(delta)=1-k^2 sn^2(delta). Thus the outer polygon is a fixed diagonal image of the orbit shifted by delta, with area factor dn(delta)/cn^2(delta). This is Lemma 3, (5)-(6), p.3. The candidate's polarity formula is the same identity: a/alpha_c=dn(delta)/cn(delta), b/beta_c=1/cn(delta). Neither proof confuses the necessary half-step with zero shift.

## 2. Complete direct-pole mechanism

Let z_p=iK' modulo the Jacobi pole translations and Z=z_p+K. On the common lattice 4K Z+4iK' Z, the orbit coordinates have only simple Jacobi poles. The classical imaginary/quarter shifts make P and n odd about z_p and even about Z. In particular sn(z_p+w)=1/(k sn(w)) and cn(z_p+w)=-i dn(w)/(k sn(w)); at Z the expressions are dn(w)/(k cn(w)) and -ik'/(k cn(w)). These formulas establish the relevant symmetries as meromorphic identities; checking real phases alone would not do so.

Put W=A-d sn^2(u), so n.n=W/(AB). At a Jacobi pole the leading coefficient of n.n is nonzero because a>b, and Q_0=n/(n.n) has a removable zero. The remaining possible poles of Q_0 occur at Z+/-delta modulo 2K Z+2iK' Z. The caustic equations give sn^2(delta)=lambda/B, cn^2(delta)=(B-lambda)/B and dn^2(delta)=A(B-lambda)/(B(A-lambda)). Quarter shifts therefore give sn^2(Z+/-delta)=A/d. The roots of W are simple: there sn^2=A/d, cn^2=-B/d and dn^2=-lambda/(A-lambda) are all nonzero. The order-two property of sn^2 on this lattice exhausts the roots. This removes an otherwise serious hidden-pole gap.

The possible area-pole sets are

    outer: z_p-delta-jh;     center pedal: Z-delta-jh.

The two signs of the individual foot pole differ by h, so they produce one cyclic set. Adjacent orbit vertices cannot both be at Jacobi poles unless N divides 2tau, impossible for primitive N>=3. Thus the outer area has at most simple poles. A potentially double pole in an adjacent foot determinant has both principal parts parallel to n(Z-delta)=n(Z+delta), so its double-pole coefficient vanishes. The only additional adjacent coincidence would require 4delta=0 modulo 2K, hence delta=K/2 and primitive N=4; it is excluded. These facts justify the center-pedal area having at most simple poles, not merely simple point poles. They are in Lemma 4, pp.4-5, and explicitly rechecked for odd N in Section 6, p.6.

The two cyclic pole sets intersect only if K=jh modulo 2K, equivalently

    4tau j=N(2ell+1).

For N odd the right side is odd; for N=2 modulo 4 it is 2 modulo 4. Both contradict the left side. This arithmetic applies to every primitive star winding; no convexity or tau=1 assumption enters.

At a possible outer-area pole u=z_p-delta the center feet are all holomorphic and satisfy Q_(1-j)=-Q_j by oddness. The permutation j -> 1-j reverses cyclic adjacency, while global negation preserves a determinant area. Therefore the center-pedal area vanishes there. For odd N the fixed index is a removable Jacobi-pole value Q=0, not an omitted undefined vertex. At a possible pedal-area pole u=Z-delta, the half-step outer formula reduces its area to a fixed multiple of the area of P(Z+jh). All those points are finite by the same disjointness arithmetic, and P(Z-jh)=P(Z+jh). Reversal j -> -j makes that area zero. Every possible simple pole of the product is consequently removable. The product is holomorphic on a compact nondegenerate torus and hence constant. This checks all analytic bridges of Theorem 2, not just its declaration.

For M=0 no even-orbit central pairing is required. For arbitrary M, the translated foot map is U-R_M, with U odd and R_M even under the primitive even half-orbit shift. Mixed determinants cancel only with that pairing. The v1.0 proof explicitly uses this even hypothesis and does not state or write the odd-period centered proof. The easy availability of a later adaptation does not retrodate its full exact coverage.

## 3. Repetitions, boundaries and signs

For a closed list of length L=rN, both cyclic determinant sums multiply by r, and their product multiplies by r^2. If 4 does not divide L then it cannot divide N. Section 6 p.6 expressly includes this argument. Thus even lists formed by repeating primitive odd orbits are covered by v1.1, although v1.0's arbitrary-M theorem does not cover them. Reversing traversal changes both signs and preserves their product; no spatial sorting or unsigned-face-area convention occurs. Both arguments avoid division by an area, so a vanishing signed pedal area is not a missing exceptional case.

The strict inequalities make all real n.n positive and cn(delta)>0, so real feet and outer points are finite. The circle requires a separate rotation argument: every fixed-step closed orbit is a rotation of a fixed regular star, preserving both signed areas. Ferudun explicitly assumes a>b, so its written Theorem 2 does not itself supply the circular case, nor does the assigned strict-ellipse target require it. No result here covers hyperbolic/focal/degenerate caustics.

The explicit period-four obstruction in v1.1 Proposition 5, pp.6-7, has products 8a^2b^2 and 2(a^2+b^2)^2 for the same caustic lambda=a^2b^2/(a^2+b^2). Their difference is 2(a^2-b^2)^2>0. This is consistent with the accepted candidate's exclusion and is not a counterexample to either exact theorem.

## 4. Relation to the submitted mechanism

The candidate gives an additional pointwise linear map from center feet to edges of a shifted orbit, and then reduces both areas to a cyclic dn trace. Its odd-order trace product is made pole-free by reflected finite zeros. Ferudun instead works with the actual outer and foot maps and their complementary pole sets. Both use credited canonical Jacobi parametrization, tangent projection, reversal, classical shifts and compact-torus constancy. They are distinct proof organizations of the same full theorem. This is evidence of mathematical overlap and different mechanisms; it cannot independently certify non-derivation, first public availability or novelty of either method.

`check_comparison.py` checks both tangent equations and projection identities symbolically, verifies parallel-principal-part cancellation, tests every coprime winding through N=200 against the exact pole-collision criterion and odd fixed-index arithmetic, and checks signed repeated-list scaling. It executes no downloaded scientific code. Universal scope rests on the preceding deductions, not on the finite bound.
