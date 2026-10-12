# Independent audit: focal-pedal ratio equality, 5100034

2026-10-02 UTC. Independent AI mathematical audit.

## Verdict and scope

**PASS: complete proof of the source-corrected ratio equality. No mandatory mathematical revision.**

The frozen candidate proves that the outer focal-pedal area is a positive phase-independent multiple of the original focal-pedal area, with the **same** multiplier at both foci. It follows that the two focal ratios agree for every permitted real orbit. All four areas are strictly positive under positive traversal, so the ratios are defined. The proof covers every primitive least period at least three, including primitive stars, and correctly extends to repeated traversal.

The imported additional assertion that the common focal ratio is phase-constant is separately false. The exact counterexample is valid and does not refute the actual equality. A second independent exact example is supplied with this audit.

This is a fully credited companion consequence of existing campaign mechanisms, not a certification of a new elliptic-function method, historical priority, proposer acceptance, or human peer review.

## Frozen inputs

* Frozen remote commit: `b8394fa1af48055a62d4a2ef0ccb3ee0f8125d2b`
* Candidate folder: `problems/5100034_focal_pedal_equality`
* `TURN_1.md` SHA256: `1abb4eaea5ef795f056ea89636defc99eb48f526cd20012b70d663cbeb2c4a34`
* `FROZEN_MANIFEST.json` SHA256: `74eaad8cb664c8a2c66f79c96f0ffe617a30993ec3e4e419a378556acf8956f2`

All twelve listed author-file entries, plus the frozen manifest itself, were checked. The sixteen source/dependency entries were independently hashed, for 28 listed entries in total. The proof and manifest fetched from the frozen remote commit match the local objects byte-for-byte. No frozen author files were modified.

The reviewer read the complete current proof, both credited dependency proofs and their independent reviews. The all-period conclusion below was checked afresh; the earlier verdicts were not treated as automatic validation of the new statement.

## 1. Primary-source identity and the formulation correction

The two actual table images were visually inspected, and both primary editions were independently opened:

* [arXiv 2004.12497v11](https://arxiv.org/pdf/2004.12497v11), dated 29 October 2020, Table 7, printed p.9: the equality is k606
* [Published Fifty New Invariants](https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf), Arnold Mathematical Journal 7 (2021), Table 7, printed p.349: the same equality is k607

Published k606 denotes the different product of the two outer focal-pedal areas. Formula, construction and edition therefore determine the present target, not an invariant code alone. Section 2 specifies signed shoelace areas. The surrounding model is a strictly nested pair of confocal ellipses, rather than a hyperbolic or collapsed caustic.

The explicit table entry equates two ratios. The surrounding prose uses broader conserved-quantity terminology, but that wording cannot consistently be strengthened to phase constancy of their common value: the exact triangular examples refute that strengthening. The audit accepts the documented formulation correction, not an unannounced narrowing. Under the imported stronger wording there is a counterexample; under the explicit table equality there is a positive proof. These conclusions are kept separate.

## 2. Canonical phase, projection maps and indexing

Stachel's published Theorem 4.3, equation (4.9), and contact-midpoint discussion give the stated parametrization with modulus k, outer semiaxes dn(v)/cn(v), k'/cn(v), and step δ=2v=4Kτ/N. The strict domain 0<k<1 and 0<v<K is retained. The source convention for a numerical Jacobi library uses parameter k², as both numerical checkers correctly do. The published reference is [On the motion of billiards in ellipses](https://doi.org/10.1007/s40879-021-00524-2).

The reviewer recomputed the two perpendicular-foot maps from their actual line normals. The original chord uses the caustic normal at contact phase w+v+iδ. The outer side uses the outer-ellipse tangent normal at vertex phase w+iδ. These are different maps and phases; the candidate does not silently interchange them. Outer tangent intersections produce those tangent lines as consecutive sides, up to a cyclic shift that leaves signed area unchanged.

For real phases, the denominators 1−k sn(u) and a−k sn(u) are strictly positive. Consecutive outer tangents are parallel only at antipodal vertices, which cannot occur for 0<δ<2K. The construction uses orthogonal feet onto entire side lines, not segment-clamped nearest points.

Central inversion has determinant +1, swaps the foci and corresponds to the phase shift 2K. It therefore gives exactly A−(w)=A+(w+2K) and B−(w)=B+(w+2K), without a spurious signed-area minus sign.

## 3. Exhaustive poles and original-foot cancellation

The required periods, poles and quarter shifts agree with [DLMF 22.4](https://dlmf.nist.gov/22.4), with addition identities from [DLMF 22.8](https://dlmf.nist.gov/22.8). The continuation is meromorphic with bilinear determinants and dot products, not Hermitian ones.

Common poles of sn and cn are removable in each foot map: multiplying numerator and denominator by a local coordinate leaves a nonzero denominator limit. Thus they introduce no overlooked poles.

For the original foot, the remaining denominator vanishes at sn(u)=1/k. On the sn torus this is the double root r=K+iK'. Its order can also be checked directly: sn′(r)=0 and sn″(r)=(1−k²)/k≠0. The quarter-shift expressions make both coordinate germs q(r+z) even in z, of pole order at most two.

At a singular original foot, its two neighbors are regular because 0<δ<2K. In particular, a common-Jacobi expression at a neighbor in a low-period case is removable, not another foot pole. The two incident area terms combine into the determinant of q(r+z) and q(r+z+δ)−q(r+z−δ). The latter vector is odd and holomorphic, hence vanishes to at least first order. The apparent double pole is reduced to at most a simple one. Primitivity gives exactly one singular original-foot vertex at a given phase, so this accounts for every incident term and every remaining term.

This local cancellation does not require even period. Restoring the contact-to-vertex shift puts its pole phases at r−v−iδ.

## 4. Outer-foot adjacent poles and cyclic boundary cases

The outer denominator has exactly two roots, r−v and r+v, on the sn torus. They are distinct and simple because 0<v<K. At both points sn and cn take the same respective values, while dn changes sign. The numerator vectors consequently agree and the denominator derivatives are opposite. The two residue vectors are opposite and collinear.

Their separation equals the billiard step δ. Thus an area summand really can have two simultaneous singular endpoints. Its double-pole coefficient is det(R,−R)=0. The other incident summands have only one singular endpoint and at most simple poles. There are exactly two adjacent singular vertices for primitive N≥3; an additional coincidence would force N to divide two. The N=3 cyclic closing edge is included, and N=2 is appropriately excluded as degenerate in this source domain.

The outer trace therefore has the same at-most-simple pole phases r−v−iδ as the original trace. This is a genuine local cancellation, not an assumption that all products contain at most one pole.

## 5. The common all-period torus and residue argument

Both area sums have periods 4K and δ. Coprimality yields L=4K/N by Bezout's identity, for odd and even N alike. On the torus with periods L and 4iK', the only possible pole classes are

    K−v+iK' and K−v+3iK'.

They are distinct, and each has order at most one. The imaginary shift 2iK' fixes sn and negates cn, reflecting the foot map in the x-axis while retaining cyclic order. Hence both signed areas have the same negative imaginary-half-period character. No even-period trace or odd-period final product theorem has been imported outside its parity range.

Real positivity, audited below, excludes the identically-zero trace. If one listed pole were absent, the character would remove the other; compactness would then make the function constant and the negative character would make it zero. Both traces therefore have genuine nonzero simple residues at the two listed poles.

Matching the residue of B to C times that of A at the first pole also matches the second by the character. The difference B−CA is holomorphic on the compact torus and constant, and its negative character forces that constant to vanish. This proves B=CA before dividing by a real area. Evaluation on the real line gives C>0 and real. The phase-shift relation at the other focus supplies the identical C there. The desired ratio equality follows only after positivity has secured its denominators.

## 6. Strict positivity, stars, repetitions and excluded domains

Each focus is strictly inside both confocal ellipses. The vector from a focus to its tangent-line foot is a positive multiple of the outward normal. In the canonical parametrization, the normal angle increases strictly and gains π over an interval of length 2K. Every step δ in (0,2K) therefore advances the normal by an angle strictly between zero and π.

Each consecutive determinant about the focus is positive, including the closing edge interpreted with the lifted canonical phase. Translating a shoelace sum to the focus does not change the area. This proves positivity for original and outer focal pedals, at both foci, even when the orbit is a primitive star. Unsigned lobe area is never substituted for this signed traversal sum.

Reversing traversal negates all four areas and keeps the ratios and positive proportionality constant unchanged. Repeating a shorter nondegenerate orbit multiplies all areas by the repetition count, so the equality survives. The proof's use of primitive period for pole counting is therefore not an unaddressed gap for repeated traversal. No claim is made for a diameter, hyperbolic or collapsed caustic, or an undefined outer intersection. The separate circular observation is harmless because the foci coincide.

## 7. Exact source-correction controls

The author's triangle on x²/21+y²/16=1 has the stated fixed confocal caustic, with positive squared semiaxes 189/25 and 64/25. Its tangent-line support identities, contacts on the segments and reflection law are valid. The four direct pedal areas are positive and have common outer/original multiplier 125/24. Central inversion preserves traversal orientation and is another phase of the same triangular family; it exchanges the two focus ratios, giving R and 1/R with R>1. It is a genuine finite, convex, nonzero-denominator counterexample to phase constancy.

Independently, this audit constructed two different exact 3-periodic triangles on the ellipse with axes 2 and 1, sharing caustic axes

    2(√13−1)/3 and (4−√13)/3.

One triangle is symmetric about the x-axis and the other about the y-axis. Direct line tangency and perpendicular-foot shoelace calculations give ratios

    [2(√13−3)+√3(4−√13)] / [2(√13−3)−√3(4−√13)]

and 1, respectively. The first denominator is positive and its numerator is strictly larger. This independent example is supplementary source-scope verification, not a substitute for the universal equality proof.

## 8. Reproduction, independent checks and limits

* The author's 3,133-assertion exact checker and 1,226-comparison, 70-digit diagnostic checker were rerun from separate copies. Both receipts match byte-for-byte.
* `independent_triangle_check.py` gives 16 exact symbolic assertions for the independently chosen ellipse and two triangles. No author checker is imported.
* `independent_geometry_diagnostics.py` gives 3,717 fresh comparisons over 531 real cases, primitive least periods 3–19, three new moduli and three new phases. It computes actual chord projections, adjacent outer tangent intersections, and actual outer-side projections, including both foci, primitive stars and reversal. The maximum scaled residual at 85 decimal digits is about 1.85×10⁻⁸⁴.

The diagnostics are non-interval computations and are not universal proof certificates. The all-period result rests on the analytic pole/cancellation/positivity argument reviewed above. Source PDFs, full extracted texts and page images are not included in this portable review packet.

## 9. Credit and recommended disposition

The proof accurately credits PR210's outer-foot local cancellation and PR261's original-foot local cancellation and positivity. Their original final conclusions have different targets and parity restrictions; the present common-lattice and residue comparison is checked separately. The classical Stachel and Jacobi inputs are identified explicitly.

A complete first-turn **source-corrected companion-result** disposition is mathematically supported, with the imported stronger phase-constancy claim recorded as false. Do not describe this as a refutation of the source equation, a new independent elliptic-function method, or a verified historical-first solution. No mandatory correction to the frozen candidate is required.
