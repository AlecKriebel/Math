# The central outer-antipedal centroid identity, with its exact domain

**5100024 / AMR-050-0024 / k406,a. Complete first-turn source-aware candidate; independent review pending.** This is an elementary consequence of classical central symmetry, not a novelty claim.

## 1. Statement and the signed-centroid domain

Fix a strictly nested nondegenerate confocal ellipse pair, with billiard ellipse E centered at O. Let P be an elliptic-billiard polygon of even **least** period N≥4. Primitive star turning numbers are allowed. Let R_i be the intersection of the tangents to E at P_i and P_(i+1), so R is the **outer tangent polygon**. Let Q_i be the intersection of the lines

    L_i: R_i·X=|R_i|²,
    L_(i+1): R_(i+1)·X=|R_(i+1)|²,                    (1)

after placing O at the origin. These are the lines through the outer vertices perpendicular to their position vectors, defining the outer polygon's antipedal with respect to O.

Then all these intersections are finite and unique, and

    C0(Q)=O.                                           (2)

Moreover the signed first-moment numerator of Q vanishes identically. In particular,

    C2(Q)=O whenever the signed area A(Q) is nonzero.   (3)

The signed-area restriction in (3) is the **natural domain of the source's definition**, not an optional new geometric assumption. Its formula is

    A(Q)=1/2 sum_i det(Q_i,Q_(i+1)),
    C2(Q)=[sum_i det(Q_i,Q_(i+1))(Q_i+Q_(i+1))]/[6A(Q)]. (4)

At A(Q)=0, that ordinary signed centroid is undefined. It has a constant extension O from its domain, but an extension must not be confused with the formula being defined there. Section 5 proves that zero-area outer antipedals actually occur among admissible primitive even billiards, so silently asserting nonzero area would be wrong.

This is the exact k406,a row in arXiv:2004.12497v11, Table 5, printed p. 7, and the same k406,a in the published companion, Table 5, printed p. 348. Both tables specify **outer** antipedals, **M=O**, even N, and both vertex and signed-area centroids. Section 2 supplies formula (4); Section 3.5 allows self-intersections. The foci cases and the unprimed k405 vertex-centroid invariant are different targets.

## 2. The even primitive orbit is centrally paired

Use Stachel's canonical parametrization, Theorem 4.3 and equation (4.9), with caustic semiaxes α>β>0, k²=1−β²/α², and real complete integral K=K(k). For some phase w,

    P_i=(-a sn(w+iδ,k), b cn(w+iδ,k)),
    δ=4Kτ/N,  gcd(τ,N)=1,  0<τ<N/2,
    v=δ/2,
    a=α dn(v,k)/cn(v,k),  b=β/cn(v,k).                 (5)

Reversing orientation if needed gives the stated range of τ and does not change the desired centroids. Since N is even and τ is coprime to N, τ is odd. The standard real shifts sn(u+2K)=−sn u and cn(u+2K)=−cn u give

    P_(i+N/2)=−P_i.                                    (6)

This classical half-turn principle was also used in the distinct campaign k405 proof (PR140). It is credited here and applied to a different derived polygon and a different pair of centroids. No focal-centroid formula from that proof is assumed.

## 3. All outer and antipedal vertices are finite

For clarity, finiteness is proved rather than assumed from the drawing. Let t(u)=am(u,k)+π/2 be a continuous eccentric-angle lift, so P(u)=(a cos t(u),b sin t(u)). It is strictly increasing and t(u+2K)=t(u)+π. Since 0<δ<2K, successive increments satisfy

    0<t_(i+1)−t_i<π.

Put m_i=(t_i+t_(i+1))/2 and d_i=(t_(i+1)−t_i)/2. Solving the two ellipse-tangent equations gives

    R_i=(a cos m_i,b sin m_i)/cos d_i.                 (7)

Here 0<d_i<π/2, so R_i is finite and nonzero. Also

    m_(i+1)−m_i=(t_(i+2)−t_i)/2 ∈(0,π).

Consequently

    det(R_i,R_(i+1))
      =ab sin(m_(i+1)−m_i)/(cos d_i cos d_(i+1))>0.   (8)

The two normals in (1) are independent, proving that every Q_i is finite and unique. The argument applies equally to primitive stars, since the unwrapped angle makes the positive winding explicit.

From (6), the opposite pair of tangents is the negative of the original pair. Hence

    R_(i+N/2)=−R_i.

Equation (1) then gives L_(i+N/2)=−L_i, and uniqueness of their adjacent intersections gives

    Q_(i+N/2)=−Q_i.                                    (9)

## 4. Pairwise cancellation of both moments

Equation (9) immediately gives sum_i Q_i=0, proving (2).

Write D_i=det(Q_i,Q_(i+1)). The opposite edge has D_(i+N/2)=D_i, while its endpoint sum is the negative of Q_i+Q_(i+1). Pairing opposite terms therefore gives

    sum_i D_i(Q_i+Q_(i+1))=0.                         (10)

For A(Q)≠0, substituting (10) into the source's signed formula proves (3). This uses signed cross products rather than the unsigned area of the regions of a self-intersecting polygon. No convexity of Q, positivity of its area, or first-variation identity is needed.

Repeating a primitive even polygon preserves both defined centroids. Merely repeating an odd orbit and assigning it an even list length is not the source parity convention and is not asserted here. Hyperbolic or collapsed caustics and two-bounce degeneracies are outside the restored ellipse-pair scope.

## 5. Why the zero-area qualification is genuinely needed

We prove existence analytically; numerical examples are only diagnostics.

### 5.1 The limiting origin antipedal of a smooth ellipse

For a centered ellipse with semiaxes A>B>0, write its point on the ray with unit normal n(φ)=(cosφ,sinφ) as h(φ)n(φ), where

    h(φ)=AB/sqrt(B²cos²φ+A²sin²φ).

The limiting family of perpendicular lines through these points is X·n(φ)=h(φ). Its envelope is

    q(φ)=h(φ)n(φ)+h'(φ)t(φ),
    t(φ)=(-sinφ,cosφ).

It is a smooth parametrized curve even when its derivative vanishes. Its signed area is

    A_lim=1/2 ∫ det(q,q')dφ
         =1/2 ∫ (h²−(h')²)dφ
         =πAB−π(A²−B²)²/(8AB).                       (11)

For the last equality, ∫h²=2πAB. In one quadrant, substituting u=tanφ in ∫(h')² and then t=Au/B gives the factor (A²−B²)²/(AB) times ∫_0^∞ t²/(1+t²)^3 dt=π/16. Multiplying by four yields the stated full integral.

Thus A_lim=π>0 for the unit circle, while for semiaxes (4,1) it is −97π/32<0. Self-intersection and signed area are essential here; this is not a claim of negative ordinary region area.

### 5.2 Realization as a limit of primitive even billiards

Fix caustic semiaxes (α,β) and k∈[0,1). For each even N≥4, set v_N=2K/N and use (5) with τ=1 to obtain an exact primitive N-periodic family. As N→∞, v_N→0 and the billiard ellipse semiaxes tend to (α,β). The original vertices sample one traversal with mesh δ_N=4K/N→0.

The outer-intersection formula (7) extends smoothly to δ=0, with limit the ellipse point. Its parametrized curve R_δ(u), including its first several derivatives, therefore converges to that ellipse. Rewrite the next two perpendicular-line equations as

    R_δ(u)·Q_δ=|R_δ(u)|²,
    [(R_δ(u+δ)−R_δ(u))/δ]·Q_δ
       =[|R_δ(u+δ)|²−|R_δ(u)|²]/δ.                  (12)

Both divided differences extend smoothly to δ=0 (use their integral representations). The determinant of the limiting linear system is det(R,R')=αβ dn(u,k)>0. Thus inversion of (12) is smooth near δ=0. Its limiting equations are R·q=|R|² and R'·q=2R·R'; writing R=h(φ)n(φ) identifies their unique solution with h n+(dh/dφ)t in Section 5.1. Therefore Q_δ converges in C¹ (indeed smoothly) to that envelope. All statements are uniform on the compact parameter period because k is fixed below one and the limiting determinant is bounded away from zero.

Finally, the polygonal area sum is a Riemann sum:

    1/2 sum_j det(Q_N(u_j),Q_N(u_j+δ_N))
       →1/2 ∫ det(q,q')du.

A Taylor expansion with uniformly bounded second derivatives makes the accumulated error O(δ_N). Reparametrizing the limit by φ gives exactly (11).

Now fix α=1 and vary k from zero to k_0=sqrt(15)/4, so β=sqrt(1−k²) varies from 1 to 1/4. For all sufficiently large even N, the area at k=k_0 is negative by (11) and the just-proved convergence. For k=0 it is the positive signed area of a regular circumscribed N-gon (the τ=1 circle case). At that fixed N, the area is continuous in k, and all intersections remain finite by Section 3. The intermediate value theorem therefore gives k_*∈(0,k_0) with A(Q)=0. Its caustic is nondegenerate, its outer ellipse is noncircular, and its billiard orbit has primitive even period N.

This establishes that a literal assertion that the area centroid is defined at every such configuration is untenable. It does not refute the invariant on the domain of the source's formula.

### 5.3 Optional constant extension

For each fixed primitive even (N,τ), the area and moment numerator are real analytic in k and normalized phase wherever 0<k<1. The area is not identically zero, since its circular limit is positive. Thus its zero set has empty interior in this full parameter space. The identically zero centroid on the nonzero-area set has a unique continuous extension O to that full space. This extension is a useful interpretation of the table at a degeneracy, but is not the ordinary quotient in (4) at zero area.

## 6. Checks and credit

The independent source target is an elementary classical symmetry consequence. Stachel supplies the standard canonical billiard parametrization; the centroid identities are direct pairwise cancellations. The continuum negative-pedal calculation is included to document the domain issue, not as a historical-first claim. The adjacent k405/PR140 result concerns the original orbit's antipedal vertex centroid, including foci, and is neither copied as this target nor used to assert the missing signed-area denominator.

The author checker uses exact centrally symmetric rational ellipse polygons for the line and moment identities, arithmetic controls of primitive even rotation numbers, and separate high-precision actual-billiard diagnostics. The finite controls are not a proof of Poncelet dynamics or a certified numerical zero-area root. Section 5 gives the universal existence argument independently of those diagnostics. Separate adversarial review is required before promotion.
