# k818: credited corollary with an essential denominator qualification

2026-10-02. One substantive author turn. Independent review pending. The universal mechanism is inherited from the two explicitly credited reviewed inputs, not a separate discovery.

## Exact theorem

Fix a noncircular ellipse E:x²/a²+y²/b²=1, a>b>0, and a strictly nested nondegenerate confocal elliptical caustic. Consider a primitive billiard Poncelet family of least period N≡2 modulo4, allowing all coprime star winding classes. Fix either original focus F. In traversal order define

 I_i=F+(P_i−F)/|P_i−F|²,
 L_i={X:(P_i−F)·(X−P_i)=0},
 U_i=L_i∩L_(i+1).

Let A,V,B be the signed shoelace areas of P,I,U. Then there are real constants c>0 and k, depending only on the fixed family, such that

 V=c A,       B=k A.                                      (1)

With positive caustic orientation A>0. Consequently either:

- k≠0: B never vanishes, and V/B=c/k is a finite phase-independent number; or
- k=0: B vanishes identically, V never vanishes, and V/B is undefined at every phase.

Thus k818 is a constant quotient on its nonzero-denominator domain, which for each family is either the entire family or empty. There is no cancellation of a0/0 singularity. The homogeneous pair[V:B]=[c:k] is a well-defined constant projective value, including[1:0], but this projective extension is not the source's ordinary finite ratio.

## Full dependencies and domain matching

Input1 is the entire proof of5100046/k805, PR257, SHA256 bcff8a4f73aef132f9621a52eec0f853c94ffe1355cad4e2c30b84b8e63d7ac9, reproduced as inputs/K805_PROOF.md. It proves A/V is positive and constant in precisely the present original-focus, unit-inversion, signed, primitive2-modulo4 setting, including stars. Taking its nonzero reciprocal gives V=cA with c>0. Its generic elliptic-trace argument is already credited to PR207; the present task contributes no independent version of that mechanism.

Input2 is the full5100022/k404 proof, PR255, SHA256 b8edd78d03dac33a7be77837649eef7a8558900b3499774725174836fa54d462, reproduced as inputs/K404_PROOF.md. Sections3–5 prove B=kA for every primitive even period. The subsequent pedal specialization is not needed here. The proof permits k=0, and its independent review explicitly validates the general-even lemma. Applying it at N≡2 modulo4 gives the second identity in(1).

Both corresponding full independent reviews are supplied unchanged. They are prior validation, not independent review of this corollary; a fresh reviewer must check the present source, denominator and hypothesis matching.

All inverse vertices and antipedal intersections are finite. The inversion distance is at least a−sqrt(a²−b²)>0. Consecutive antipedal normals could be dependent only if the original chord passed through F; a tangent to the strictly nested elliptical caustic cannot contain its interior focus. Positivity of A,V follows from the positive oriented edge determinant around a point strictly inside the caustic. Inversion divides such a determinant by two positive squared distances. These arguments do not require the star polygon to bound an unsigned region.

Now(1) gives the two alternatives immediately; division is performed only after k≠0 is imposed. Central symmetry of primitive even orbits interchanges the original foci and preserves the corresponding signed areas, so both foci have the same quotient and the same exceptional case. Reversing traversal negates A,V,B together and preserves the quotient. Repeating an already admissible primitive orbit multiplies all areas by the repetition count; artificially changing primitive parity by repetition is not part of this theorem. Nonunit inversion radius rho multiplies V by rho⁴ and hence the ratio by rho⁴.

## Exact genuine zero-denominator family

The source itself lists a zero-antipedal-area simple six-periodic example at a/b=2. Here is an exact verification independent of its animation. Set a=2,b=1,F=(sqrt3,0), and take the six vertices

 (2,0), (4/3,sqrt5/3), (−4/3,sqrt5/3),
 (−2,0), (−4/3,−sqrt5/3), (4/3,−sqrt5/3).

They are distinct and lie on E. The six segments satisfy specular reflection, and all are tangent to the strict confocal ellipse with semiaxis squares32/9 and5/9. Its focal square difference is3, as for E, and both axes are strictly smaller than those of E. Thus this is an allowed primitive six-orbit, not a degenerate caustic or a repeated lower-period traversal.

Solving the actual antipedal line equations and taking signed shoelace sums gives

 A=20sqrt5/9,       V=15sqrt5/8,       B=0.                  (2)

For auditability the six antipedal vertices are

 (2,(-sqrt5+2sqrt15)/5),
 (−sqrt3,−2sqrt5/5),
 (−2,(-sqrt5−2sqrt15)/5),
 (−2,(sqrt5+2sqrt15)/5),
 (−sqrt3,2sqrt5/5),
 (2,(sqrt5−2sqrt15)/5).

The exact checker verifies incidence, reflection, tangency, finite line determinants, both focus choices and the three areas. Since A is nonzero and the already-proved proportionality coefficient k is phase independent, B=0 at this phase implies B=0 throughout its Poncelet family. V>0 throughout. Thus one must not state a finite everywhere-defined quotient for all admitted families.

## Source and disposition boundaries

The exact table is arXiv2004.12497v11 Table9p11, with definitions in§§2,3.5,3.9: https://arxiv.org/pdf/2004.12497v11 . The ratio is absent from the shorter published companion, so its table numbering cannot be substituted. The source uses signed area, and its Table11p14 already records the special zero-area phenomenon; that observation is credited, not discovered here.

The retained mathematical result is the complete domain-qualified corollary(1)–(2). It is not a new general elliptic-pole result. A natural-domain interpretation of k818 is proved by prior reviewed campaign theorems; a literal finite-valued-for-every-family interpretation requires the explicit qualification above. The final source/disposition decision belongs to separate review. Hyperbolic/circular/degenerate caustics, outer-locus foci and unsigned filled areas are outside this packet. No novelty, human peer-review or formal-certification claim.
