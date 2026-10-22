# Independent review: 5100004 / k110

Date: 2026-10-01. **Verdict: PASS for the full source-corrected constancy claim.**

Reviewed `CANDIDATE.md`, SHA-256

    4e921ea0229b7a982ad4d4f7c58b9f62950e404b37377de37bb340b9a2f64c58

No mathematical revision is required. The appropriate assessment is a credited application of a published theorem (`already_solved`), not a novelty claim. The proof concerns the original source's nondegenerate confocal ellipse pair, signed polygon areas, and even primitive period. The imported catalogue's less explicit wording must not be used to silently enlarge this scope to hyperbolic caustics or repeated odd primitive orbits.

## 1. Exact source match

I read the frozen candidate and source audit, the imported statement, and the relevant full primary texts. I independently rendered and inspected both Table 2 pages and the low-period proposition.

- Reznik–Garcia–Koiller, [arXiv:2004.12497v11](https://arxiv.org/pdf/2004.12497v11), Table 2, printed p. 5: k110 is the constancy of AA'' for even N.
- The [published companion](https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf), Arnold Math. J. 7 (2021), 341–355, Table 2, p. 345: the same k110 target. Section 1 specifies a pair of confocal ellipses; Section 2 assumes a>b>0, defines the contact polygon, and uses signed area.
- Chavez-Caliz, [More About Areas and Centers of Poncelet Polygons](https://armj.math.stonybrook.edu/pdf-Springer-final/020-0154.pdf), Arnold Math. J. 7 (2021), 91–106: Theorem 3, p. 93, repeated and proved as Theorem 6, p. 104, is precisely constancy of AA' for even Poncelet period between concentric ellipses in general position. Equation (5) is algebraic shoelace area. The definition of general position on p. 94 is transversality of the complex projective conics. The flag-curve proof uses order N; retaining the candidate's least-period qualification is essential.

The application therefore has a complete accessible published input. The private communication credited for a neighboring ratio is unnecessary. This review checks the theorem's actual hypotheses and its application; it does not present the published theorem as a new result.

## 2. Polarity calculation

Write B=diag(1/a²,1/b²) and D=diag(1/alpha²,1/beta²). If T_i is the intersection of the two outer tangents, the line xᵀBT_i=1 contains P_i and P_(i+1). Its equality to the caustic tangent xᵀDS_i=1, with identical nonzero constant normalization, forces DS_i=BT_i.

Hence S_i=M T_i for the same matrix M=diag(alpha²/a²,beta²/b²) at every index. This is a pointwise equality in traversal order, not an assertion about reordered vertices or only absolute area. Every determinant term in the shoelace sum is multiplied by det M. Thus

    A'' = alpha² beta²/(a² b²) A'.

This equality needs neither parity nor a division by polygon area. It is valid for crossing polygons and zero signed areas. The finite-vertex condition is justified: parallel outer tangent lines would come from antipodal endpoints; their chord passes through the center and cannot be tangent to the strictly interior nondegenerate ellipse. Coincident consecutive vertices are excluded by the specified billiard orbit.

## 3. General position is proved, not inferred from one sample

For c²=a²−b²>0 and 0<lambda<b², the common complex points have

    x²=a² alpha²/c²,   y²=−b² beta²/c².

Both coordinates are nonzero, giving four distinct finite points. The coefficient determinant at infinity is

    1/(a² beta²)−1/(b² alpha²)
      = lambda c²/(a² b² alpha² beta²) > 0.

There are no common points at infinity. At every affine intersection the gradient determinant is 4xy times this nonzero number. All intersections are therefore transverse for every pair in the stated range. No generic-specialization argument, continuity extension, or unverified limiting theorem is needed.

The published theorem now applies to P and its actual tangent polygon T. Multiplying its constant AA' by the fixed det M proves k110. The proof does not assume the conjectured AA'' identity at any step.

## 4. Scope and edge cases

- Signed shoelace area is indispensable. Ordinary unsigned area of the union of star-polygon lobes is a different quantity and is not covered.
- Repeated traversal of an even primitive orbit multiplies both areas by the repetition count and the product by its square. Merely traversing an odd primitive orbit twice does not satisfy the theorem's even-order hypothesis.
- N=2 cannot occur for a strictly interior nondegenerate elliptical caustic. The excluded antipodal construction would require a center-crossing tangent.
- The source assumes a>b. If one separately includes a circle with a concentric circular caustic, each fixed-period family consists of rigid rotations of a regular star, so constancy is immediate. This does not rely on complex transversality surviving a=b.
- Degenerate caustics and hyperbolic caustics are outside the source-corrected assertion reviewed here. The candidate explicitly records that limit and does not imply a result for them.
- The full result is credited as an elementary consequence of Chavez-Caliz's published theorem. This review does not certify priority or a comprehensive absence of earlier explicit k110 proofs.

## 5. Edition and normalization warnings confirmed

The arXiv-v11 table lists A'/A'' at k113. The published companion's k112 instead visibly prints A'A'' with the same dimensionless value. The frozen source audit describes the actual pixels correctly. The candidate derives the ratio independently and never relies on that printed product. The k110 row itself is unchanged between editions. Neighboring k111 numbering changes must not be conflated with this target or with the separate angle-product counterexample work.

In [Garcia–Reznik's accepted manuscript](https://ami.uni-eszterhazy.hu/uploads/papers/finalpdf/AMI_online_1216.pdf), Proposition 4.9, printed p. 10, visibly gives coefficient 2 in the displayed N=4 k110 value. Its preceding definitions identify A'' as the contact-polygon signed area. Directly computing the axis quadrilateral instead gives coefficient 8: A=2ab, A'=4ab, A''=4a³b³/(a²+b²)². This factor-four discrepancy is real under the specified conventions and affects only that displayed normalization, not the constancy deduction.

For a=4,b=3, the axis quadrilateral yields areas 24, 48, 6912/625; the second rectangular phase gives 576/25, 50, 288/25. Both AA'' products are 165888/625. Their A'A'' products differ, which independently guards against replacing the ratio by a product.

## 6. Independent controls and provenance

I independently authored `independent_check.py` using only the Python standard library. It passed **2,532 exact assertions**:

- 36 rational Pythagorean choices, with both four-period phases checked for outer-ellipse incidence, outer tangent intersections, inner tangency, signed area transfer and common AA'';
- coefficient-2 and product-versus-ratio negative controls;
- 108 strict confocal pairs checking the exact complex-intersection and transversality identities;
- signed-area covariance on ordinary, crossing, reversed and zero-area arbitrary polygons, explicitly not presented as billiard trajectories;
- two exact six-period controls in separately implemented quadratic fields, reproducing AA''=12800/729 in both phases.

The author's checker was inspected but not executed. Its reported 4,267 assertions are not counted as my independent run. The author's four- and six-period values agree with the independently computed values. Finite checks corroborate implementation and normalization; the general-N result follows from the analytic proof and published theorem, not interpolation or numerical evidence.

All 17 frozen author-artifact hashes and byte sizes match `frozen_artifacts.json`. All four source PDF hashes and their extracted-text hashes match `source_manifest.json`. No frozen author file was edited. Reading copies, extracted full texts and page images are not publication artifacts. The independent public artifacts are this review, the checker, its JSON output, and their checksum list.

The review is complete (100% of the scoped audit). No remaining mathematical blocker was found. Publication remains the coordinator's action; this review itself made no remote changes.
