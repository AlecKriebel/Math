# Supplemental adversarial audit: target-parity original/outer area product

Input: `ROOT_AREA_PRODUCT_DEPENDENCY_VERIFICATION_01.md`, 4,973 bytes, SHA-256 `bdcf7dd3414a09c62e1b2878ca2b0faf015771a87a6a3c0d48b9ef3667b4f8ca`.

First read at the real-clock checkpoint **2026-10-16 05:54:45 UTC**. Input hash and size authenticated at **05:55:30 UTC**. This is a bounded post-candidate adversarial verification, not a newly independent research family, discovery, or priority argument. The supplemental input, original submission, original approach freeze, previous reports, and previous `MANIFEST.json` remain unchanged.

## Verdict

**PASS for the stated confocal, primitive N=2m with m odd≥3 hypotheses. No substantive gap or counterexample found; no mathematical repair is required.** The supplemental argument proves AA' constant without needing the published area-product conclusion as an unverified step. The standard complex flag/translation framework remains an explicitly credited input. The proof is a verification of the result credited to Chavez-Caliz, not a new theorem or historical novelty claim.

In particular, the argument checks the local orders required for cancellation; merely knowing that a value is infinite or zero would not have sufficed. It neither divides by an area nor assumes a nonzero product.

## 1. Exact homogeneous model for the polarity and the chord projection

Use homogeneous point coordinates [x:y:z], with

    E: x²/a²+y²/b²−z²=0,
    C: x²/α²+y²/β²−z²=0,
    α²=a²−λ, β²=b²−λ, 0<λ<b²<a².

Represent the chord line as

    l=[u:v:w],       ux+vy−wz=0.

The conic of tangents to C is

    C*: α²u²+β²v²−w²=0.                                  (1.1)

Polarity with respect to E is the invertible projective map

    l ↦ W=[a²u:b²v:w].                                    (1.2)

For a generic chord meeting E at P_i,P_(i+1), its pole W is exactly the intersection of the two tangents to E there: both tangent equations contain W because their contact points lie on l. The identity extends through degenerate flags by the regular projective polarity map. Substituting (1.2) into (1.1) gives

    α²W_x²/a⁴+β²W_y²/b⁴=W_z².

This is the smooth outer-vertex conic claimed by the root. Its real affine part is an ellipse. The maps π:X→E and ρ:X→C* both have degree two: π chooses either tangent through a generic E-point; ρ chooses either E-intersection of a generic C-tangent. The deck involutions are respectively τ and σ. There is no switch between a pole of C and a pole of E here.

## 2. Exact analysis of every possible infinite outer vertex

Equation (1.2) shows that W is infinite **if and only if w=0**. Equation (1.1) then has two distinct points

    [u:v:w]=[β:±iα:0].                                    (2.1)

These are the two projective C-tangents through the affine origin. Their C-contact points lie at infinity; the word “asymptote” here refers to these complex projective lines.

A direction vector for the affine line in (2.1) is (±iα,−β). On that line the E-equation is

    t²(−α²/a²+β²/b²)=1.

The coefficient is

    −α²/a²+β²/b²=λ(1/a²−1/b²) ≠ 0.                       (2.2)

Consequently each such line intersects E at two distinct finite opposite points. It is not tangent to E, and its infinite point does not lie on E. This is the explicit discriminant/unramified check for ρ; strict real nesting alone would not have proved it after complexification.

The intersection of the smooth dual conic (1.1) with w=0 is transverse at either point (2.1): in a chart u≠0, the derivative of α²+β²(v/u)²−(w/u)² with respect to v/u is nonzero. Thus w/u is a local parameter on C* at that point. Because ρ is unramified there, its pullback is also a local parameter on X, up to a nonzero factor. Both affine coordinates of W in (1.2) therefore have at most a simple pole, in fact a nonzero leading pole before any area-sum cancellation. This verifies precisely the pole-order statement needed later.

There cannot be adjacent infinite W_i,W_(i+1). Their two chord lines share the intermediate E-vertex P_(i+1).

- If they are the two different lines (2.1), their intersection is O, and O∉E.
- If they are the same line, the two successive tangent choices to C at P_(i+1) would coincide. That can occur only when P_(i+1) is the line's C-contact point. That point is infinite and is not on E by (2.2). Equivalently, the two finite E-intersections just computed are outside C and have two distinct complex tangents to C.

Hence no outer shoelace determinant has two singular factors. Every possible pole of A' is at most simple. This remains true even if several nonadjacent outer vertices become infinite at the same flag.

## 3. Orbit incidence and disjointness

Use T=τσ, I=T^m, and the audited translation property: nonidentity powers of T have no fixed points, and T has exact order N=2m. The identities σT^j=T^(−j)σ and τT^j=T^(−j)τ are valid with these conventions.

### 3.1 Original-infinity orbits S contain σ-fixed flags

Above either infinite point of E, π is unramified, since that point is not on C. The involution τ exchanges the two flags. Central inversion fixes the base projective point but has no fixed flag, so I exchanges the same two flags. Thus τx=Ix=T^mx. Since σ=τT,

    σx=T^(m−1)x,
    σT^kx=T^(m−1−k)x.

For odd m the congruence 2k≡m−1 (mod 2m) has a solution, giving a σ-fixed flag in that T-orbit. This verifies step 1 of the root proof, with its sign and index shift.

### 3.2 Outer-infinity orbits R contain τ-fixed flags

For a flag on a line (2.1), the two E-intersections are finite and opposite. Central inversion leaves the chord line fixed and exchanges its E-intersections; hence σx=Ix=T^mx. Since τ=Tσ,

    τx=T^(m+1)x,
    τT^kx=T^(m+1−k)x.

For odd m, 2k≡m+1 (mod 2m) is soluble and gives a τ-fixed flag in that orbit. This verifies step 2, again including the necessary opposite index shift.

### 3.3 R∩S is empty

Starting from σz=z gives

    τT^jz=T^(1−j)z.

A τ-fixed point in that orbit would require T^(2j−1)z=z. Freeness of nontrivial translations turns this into 2j≡1 (mod N), impossible for even N. Thus no orbit contains both kinds of fixed flag. Since every member of S contains a σ-fixed flag and every member of R contains a τ-fixed flag, R and S are disjoint.

In particular, every original vertex is finite at every point of R, and every outer vertex is finite at every point of S. No assumption that either set has a specified cardinality is required here. The proof also does not silently identify σ and τ: their distinct roles are essential.

## 4. Palindromic zeros and local cancellation

A and A' are cyclically invariant meromorphic functions and descend to the unramified compact quotient Y=X/<T>. Changing the chosen representative of an orbit does not change either signed area.

At a τ-fixed flag z,

    π(T^jz)=π(T^(−j)z).

Thus the original vertex list P_j is palindromic. Every determinant det(P_j,P_(j+1)) pairs with its negative at index −j−1. At an orbit in R all original vertices are finite by Section 3.3, so this argument is a legitimate equality of finite complex numbers: A=0 there, and A is holomorphic there. Accordingly its zero has order at least one unless A vanishes identically, in which case the product conclusion is immediate.

At a σ-fixed flag z, the analogous identity follows from ρσ=ρ:

    ρ(T^jz)=ρ(T^(−j)z).

Polarity preserves this equality, so the outer vertex list is palindromic. At an orbit in S all W_j are finite, giving A'=0 with A' holomorphic there, again to order at least one unless identically zero.

The original-area pole bound on S is independently sound under the already audited conic hypotheses: each E-coordinate pole is simple because π is unramified at E∞; two consecutive original vertices cannot both be infinite, since their chord would be either the line at infinity or a common tangent at E∞, both excluded. Thus A has at most simple poles on S.

Use a local coordinate t on Y. At a possible pole in R the local orders are

    A=O(t),      A'=O(t^−1),

and at a possible pole in S they are

    A=O(t^−1),   A'=O(t).

If a potential pole cancels earlier, these estimates only improve. Their product is bounded and hence holomorphic in either case. Away from R∪S both areas are holomorphic. Therefore AA' is holomorphic on compact Y and is constant. No residue nonvanishing, exact zero multiplicity, product positivity, or area division is needed.

This verifies root steps 3–6 and the conclusion without appealing to the published AA' conclusion.

## 5. Other adversarial checks and limits

**Primitive stars and reversal.** The argument uses exact order and I=T^m, not convex winding one. It applies to primitive stars in the specified strict confocal pair. Reversal negates both areas, preserving their product. Counting repeated odd orbits as even traversals would invalidate the exact-order hypothesis; the earlier exact counterexample remains relevant.

**Real nonzero-value aside.** It is unnecessary, but correct. Apply (x,y)↦(x/a,y/b), which multiplies signed areas by 1/(ab), and sends tangents to E to tangents of the unit circle. Orient an ordinary real target orbit with the caustic on the left. Each successive angular increment δ_i lies in (0,π): the center lies strictly on the left of every chord, and antipodal chords are excluded. The tangent polygon's signed area is Σ tan(δ_i/2) in the unit-circle coordinates, so its original area is ab Σ tan(δ_i/2)>0. The original area is also positive term by term. Thus the aside covers real primitive stars as well as convex examples.

**Boundary failures have been excluded.** Equations (2.1)–(2.2) rely on λ>0, αβ≠0, and a>b. At λ=0, a=b, or a degenerate caustic, intersections or pole orders can change. For even m the two congruences used to put S and R into fixed-flag orbits are insoluble. The proof therefore establishes exactly the advertised target parity, not all even orders or arbitrary concentric pairs.

**Dependency and credit.** The self-contained target-parity area-product lemma still rests on the smooth flag curve, the translation description, and I=T^m already verified in the candidate/source-family audit. It removes the need to take the AA' theorem's conclusion on trust; it does not remove those explicitly identified inputs. Full credit to Chavez-Caliz's published area-product result is retained. No new priority search or repeated old numerical/symbolic test suite was performed.

## 6. Scoped outcome and safe artifacts

The root supplement is mathematically sound for its stated scope. The derivation above supplies the explicit homogeneous polarity, discriminant, and local-parameter checks that make its most delicate assertions directly checkable. There is no requested mathematical repair. The parent's final mathematical gate remains the parent's decision.

This supplement is recorded separately from the earlier final report and manifest. `SUPPLEMENT_AREA_PRODUCT_MANIFEST_01.json` lists only the new safe authored supplement report and log, hashes the immutable reviewed input by reference, and confirms that the previous manifest hash remains `53dbaabe027f0780ac8e5766beeb750cb9e1daff5f6f0e8c109b9ff3db842493`. It does not include any third-party PDF/text, dependencies, private cache, or mutable native submission.
