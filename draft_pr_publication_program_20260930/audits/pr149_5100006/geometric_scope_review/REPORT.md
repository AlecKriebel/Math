# PR149 / 5100006: independent real-geometry and scope review

Reviewed original `PROOF.md` SHA-256 `f70821b0d44e96f6be9427f906cecc5d1aff8bbd7ab09a71ddec9d75d31ef2d5`.

**Scoped verdict: PASS for the submitted primitive, strictly nested confocal-ellipse theorem.** The bridge from the physical billiard family to the Jacobi cyclic product is correct for every real phase, for simple and star orbits, and for either orientation. No sibling theorem is needed. The restriction to **least period** is essential. If “N-periodic” only means return after N steps, the unrestricted source-record wording admits an exact counterexample below. Retain the primitive convention prominently in any promoted claim.

This review independently checks the geometric bridge and source scope. It does not claim an independent priority search or replace the separate audit of the complex divisor argument. Submitted review verdicts and submitted verifier outputs were not used.

## 1. Primary source and exact physical assumptions

The source defines its elliptic billiard using a confocal ellipse pair, with outer semiaxes a>b>0. Its Table 2, printed p.5, identifies k114 as the product of the ordinary focal distances d1,i, with N=2 modulo 4. Its definitions do not expressly say “least period.” Thus the primitive convention is an explicit qualification needed to avoid a broader, false reading. The source does not require a hyperbolic-caustic extension. [Reznik–Garcia–Koiller, v11](https://arxiv.org/pdf/2004.12497v11).

Stachel's published Theorem 4.3 and (4.9), printed p.1614, use the caustic eccentricity as Jacobi modulus, parametrize the outer ellipse by (-a sn u,b cn u), and identify the vertex advance as 2v. The period and axis formulas in the submission agree. [Stachel, published paper](https://doi.org/10.1007/s40879-021-00524-2), [author preprint](https://arxiv.org/pdf/2105.03624).

Write the outer ellipse as E and the caustic as C, with

    a>b>0, alpha>beta>0,
    a²-b² = alpha²-beta² = c² > 0,
    a>alpha, b>beta.

The common positive difference lambda=a²-alpha²=b²-beta² ensures strict nesting. Put k=c/alpha in (0,1), K=K(k), and use Jacobi **modulus k**, equivalently parameter k² in a numerical implementation.

The source PDFs were read from the primary-source cache only. Their hashes match the original submission's manifest:

- Stachel published PDF: `9121028d7295435740cebb25ec60abe1a0dcc4e96686c226b1b6533bd49515d8`.
- Source v11 PDF: `c56bb4ea29734ed04ee153206bb8619286df544714fd3f77fe97bdc945dfe1da`.

## 2. Independent reconstruction of the real tangent chord

For this fixed pair, there is a unique v in (0,K) with

    cn(v,k)=beta/b,
    b=beta/cn v,
    a=alpha dn v/cn v.                                  (G1)

Uniqueness follows from strict decrease of cn from 1 to 0 on [0,K]. The last formula follows from confocality and dn² v=1-k² sn² v. Conversely (G1) makes a²-b²=c² and a>alpha, b>beta, since dn² v-cn² v=(1-k²)sn² v>0.

Define P(u)=(-a sn u,b cn u) and Q(U)=(-alpha sn U,beta cn U). The tangent to C at Q(U) has equation

    -x sn U/alpha + y cn U/beta = 1.

Both P(U-v) and P(U+v) lie on this line. Indeed, writing s=sn U, q=cn U, t=sn v, r=cn v, d=dn v, the Jacobi addition formulas give

    (d/r) s sn(U±v) + (1/r) q cn(U±v)
      = (d²s²+q²)/(1-k²s²t²) = 1.                       (G2)

The terms odd in the ± sign cancel. The denominator is positive on the real line. The endpoints are distinct because 0<2v<2K<4K. Also Q(U) is strictly inside E, since

    Qx²/a² + Qy²/b²
      = (alpha²/a²)sn² U + (beta²/b²)cn² U < 1.

Consequently Q(U) lies between the two intersections of its tangent line with E. These are actual billiard chords tangent to the specified caustic, rather than tangents only to an extension of a side.

## 3. Independent reflection and completeness check

One can verify the elastic reflection law without importing a sibling result. From a point P=(x,y) on E, the direction d=(dx,dy) of a line tangent to C obeys the zero-discriminant equation

    dᵀ M d = 0,
    M = [[beta²-y², xy], [xy, alpha²-x²]].               (G3)

An irrelevant positive scalar has been suppressed. Let n=(x/a²,y/b²) be the outer normal and t=(-y/b²,x/a²) its perpendicular. Direct algebra gives

    nᵀ M t
      = xy c²/(a²b²) [1-x²/a²-y²/b²] = 0.              (G4)

Thus (G3) is invariant under reflection across the normal (and the tangent). Because P is outside C,

    det M = alpha² beta² [1-x²/alpha²-y²/beta²] < 0,

so there are two distinct tangent lines, interchanged by the reflection. The two inward chord rays are symmetric about the normal, which is precisely the billiard reflection condition after changing the sign of the incoming ray.

Equations (G2)–(G4) show that the physical orbit through P(u) advances by +2v, or by -2v for the reversed orientation. The real map u modulo 4K to P(u) is bijective: the Jacobi amplitude is strictly increasing, has derivative dn u>0, and advances by 2pi over 4K. Every point of E and both possible oriented caustic-tangent states are therefore represented. At each point the two tangents already found exhaust the possibilities. There are no additional physical family members or omitted phases.

Since C contains the center in its interior, its tangent chord does not pass through the center. For the chosen positive orientation each chord advances the polar angle by an amount between 0 and pi. This gives 0<tau<N/2, and allows self-intersecting stars when tau>1.

## 4. Exact least period and antipodal pairing

By real injectivity, P(u+N·2v)=P(u) holds exactly when N·2v is a multiple of 4K. The least period is N exactly when

    v=2K tau/N, gcd(tau,N)=1, 0<tau<N/2.                (G5)

This is independent of u. The winding number is tau because the accumulated amplitude advance is 2pi tau. Changing orientation reverses the same finite vertex set and does not affect a product.

For N=2m=2 modulo 4, m is odd. Coprimality forces tau odd and gcd(tau,m)=1. Then

    P(u+m·2v)=P(u+2K tau)=-P(u).                        (G6)

The N distinct vertices pair antipodally, including the star cases. This is a deduction from the full real parametrization, not an assumed central symmetry from an earlier campaign.

## 5. Ordinary focal distances and normalization

For any real P=(x,y) on E,

    |P-(c,0)|² = (a-cx/a)²,
    |P-(-c,0)|² = (a+cx/a)².

Both linear expressions are at least a-c>0. Thus they equal the **ordinary**, positive distances, without a signed-distance or square-root convention. At P(u) they become a+c sn u and a-c sn u. Pairing P and -P gives

    |P-f+| |(-P)-f+| = a²-c²sn² u = F(u).

Consequently both original one-focus products are exactly

    R(u)=product(j=0,...,m-1) F(u+2jv).                 (G7)

Every real factor F is between b² and a². The equality is valid at axis vertices and every other phase; its real positivity does not depend on a complex branch. This establishes the geometric object to which the submitted divisor argument applies.

## 6. Exact counterexample if repeated odd orbits are admitted

Take

    a=√15, b=√7, c=√8,
    alpha²=135/16, beta²=7/16.

This is a strictly nested, nondegenerate confocal pair, with lambda=105/16. Consider the triangle

    T=((a,0),(-3a/4,7/4),(-3a/4,-7/4)).

Its vertices lie on E. Its sides are x=-3a/4 and x±a y=a. They are tangent to C: the first is x=-alpha, and the support value for the other two is

    alpha²+a²beta² = 135/16+105/16 = a².

At the upper off-axis vertex, the inward unit directions are (a/4,-1/4) and (0,-1); their sum (a/4,-5/4) is five times the inward outer normal (a/20,-1/4). The lower vertex follows by reflection; the axial vertex follows by symmetry. Thus T is a genuine primitive three-bounce billiard with this caustic. Its central reflection -T is another member of the same family.

For the focus (c,0), the ordinary three-vertex products are respectively

    H(T)=(a-c)(a+3c/4)² = 15a/2+3c,
    H(-T)=(a+c)(a-3c/4)² = 15a/2-3c.

Traversing each triangle twice creates return-period-six sequences. Their one-focus products differ by

    H(T)²-H(-T)² = 90ac = 180√30 > 0.                  (G8)

Therefore “returns after N steps, N=2 modulo 4” is false. The submitted proof explicitly excludes this case and its theorem is unaffected. Any unqualified downstream source-record status must say that k114 is established under the primitive/least-period interpretation. Repetition of an orbit already satisfying the theorem preserves its constancy, but does not establish the criterion for a different least period.

## 7. Parity and boundary checks

Dropping the N=2 modulo 4 condition also fails physically. For arbitrary a>b>0, the confocal caustic

    alpha=a²/√(a²+b²), beta=b²/√(a²+b²)

admits both a four-vertex axial rhombus and the four-vertex rectangle (±alpha,±beta). Their focal products are a²b² and 4a⁴b⁴/(a²+b²)² respectively, unequal when a>b. For the control a²=15,b²=7, the exact products are 105 and 11025/121. Both constructions have least period four and the same caustic.

The boundaries introduce no hidden admitted case:

- N=2 would require v=K and cn v=0, impossible for a finite outer ellipse with positive beta. A two-bounce trajectory has no strictly nested nondegenerate elliptical caustic of this type.
- v=0 makes the outer ellipse coalesce with its caustic and the vertex map stationary. It is excluded by strict nesting; a fixed finite positive least period never includes it.
- beta=0 gives a degenerate caustic and k=1. The elliptic torus and real parametrization used in the submission are not being asserted at that endpoint. Hyperbolic and degenerate caustics remain outside the claim.
- a=b gives coincident foci. This lies outside the source's a>b assumption but the extra circle statement is directly valid: every focal distance equals a, so the product is a^N for every orbit and phase. No elliptic-function limiting argument is needed.

The adjacent dn(u+2K) sign typo also appears in the published text on printed p.1613. The correct sn/cn sign changes used for (G6) are present and are sufficient. No incorrect dn shift is used by this geometric bridge. The original wording about a preprint typo is true but could be clarified to mention the published occurrence as well.

## 8. Supplementary numerical diagnostics and repair

An independently written `geometry_checks.py`, importing no submitted code, tested 80 primitive rational rotations across N=6,10,14,18,22,26 and k=0.001,0.2,0.6,0.99, with six phases each and star turns included. It checks confocality, both endpoint tangent equations, reflection, antipodal pairing, direct Euclidean focal distances against the linear formula, focus equality, pairing equality, and phase constancy. At 80 decimal digits the largest residual was about 5.36e-79. Exact controls (G8) and the four-bounce construction were also numerically replayed. These finite tests support the deductions; they do not prove all phases or periods. Results are preserved in `geometry_check_results.json`.

Replay requires Python and mpmath 1.3.0; the temporary dependency was installed only in this review folder for execution. The exact deductions in Sections 2–7 are the checkable mathematical artifacts and do not depend on numerical sampling.

**Repair needed:** no change to the submitted theorem's geometric hypotheses or focal normalization. Promoted text must retain “least period N” and “strictly nested nondegenerate confocal elliptical caustic”; if the original corpus statement is treated as allowing repetitions, amend it explicitly or label the proven result as the primitive interpretation and preserve (G8) as the falsification of the broader reading. Optional citation clarification: the dn sign typo is present in both the preprint and published paper. Priority remains unresolved by this review.
