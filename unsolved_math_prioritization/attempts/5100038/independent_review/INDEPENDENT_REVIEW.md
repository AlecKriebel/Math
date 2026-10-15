# Independent review: inner focal-antipedal invariant k610

**Verdict: PASS_FULL_DOMAIN_QUALIFIED.** No mandatory mathematical or source correction. This verdict concerns the exact arXiv k610 target on its defined geometric locus, with the proof's finite-collapse and missing-intersection qualifications. It does not certify an everywhere-defined quotient, a hyperbolic-caustic extension, or novelty.

Reviewed 2026-10-01 UTC by a separate reviewer uninvolved in this proof's derivation. The reviewer has authored other elliptic-billiard results using different constructions; no contribution to this candidate was made before its freeze. The shared classical symmetry mechanism is explicitly credited by the author.

## Frozen inputs and reproducibility

- `PROOF.md`: SHA-256 `e94f81f280560223485cc7ffbca103960e727108d133e7e9c10334cd9ddb91a7`
- Author `MANIFEST.json`: SHA-256 `dc7f1107ee531e22b34412e374036085c5b440b32ea8f2fad2e0dc9a463ff622`
- All nine listed author-file hashes and lengths match; all three source-PDF hashes match
- The author's checker was inspected before execution. Its 3,310-assertion output reproduces byte-for-byte
- The separate `independent_check.py` passes **13,173 exact assertions** using homogeneous line cross-products, rational arithmetic and exact symbolic algebra. Run `python independent_check.py` with pre-existing SymPy 1.14.0. It reads no author files and needs no local absolute path

Finite controls support the calculations; the universal conclusion follows from the reviewed geometric proof.

## Exact source gate

The pinned arXiv v11 Table 7, printed p.9, visibly lists k610 as the ratio of the double-primed, starred focal areas, value 1, even N. Appendix A Table 12 makes double primes the inner/contact polygon and stars the antipedal construction. Section 3.5 supplies perpendicular lines through the input polygon vertices. Section 2, equation (1), requires signed shoelace area. These are precisely the author's objects.

The final *Fifty New Invariants* Table 7, printed p.349, was separately inspected. It ends at k607 and does not carry this k610 assertion. The author correctly targets the arXiv edition and does not transfer an unrelated final-table label.

Stachel's published 2021 paper, Corollary 4.2(i), printed pp.22–23, gives central symmetry for even N and odd turning number with an elliptical caustic. Its surrounding discussion explains splitting when the turning number and N have a common divisor; hence a primitive even least period has odd turning number. The proof of the corollary identifies the half-period index correspondence. The immediately subsequent hyperbolic-caustic discussion has different symmetry cases, correctly excluded here.

## Universal geometry and domain audit

1. Central inversion sends each ordered billiard side to its half-period partner. Uniqueness of tangency on the nondegenerate ellipse sends each contact R_i to -R_i without reversing traversal. Primitive star classes satisfy the same index relation. An even indexing length obtained by repeating an odd primitive orbit is not silently included.
2. The normal-chord exclusion was independently derived from the dual-conic equation: its confocal parameter is a² sin²(theta)+b² cos²(theta), at least b². A tangent-to-outer-ellipse line also cannot touch the strictly inner caustic. Thus the distinct-consecutive-contact argument does not hide a normal backtracking or grazing case.
3. Each original focus is strictly inside the confocal elliptical caustic, so no contact-focus normal vector vanishes. A zero consecutive determinant gives two distinct parallel perpendicular lines: the two contacts have distinct scalar positions on the line through the focus. It does not produce a nonunique coincident line.
4. The determinant equality at the opposite focus proves equality of the finite-intersection loci. On that locus, central inversion takes each uniquely determined antipedal vertex to its half-period opposite-focus partner. Its determinant is +1, and the cyclic index shift preserves signed shoelace area.
5. Area equality proves quotient 1 only where its denominator is nonzero. Clearing intersection denominators gives the rational equality. The simplified constant expression may be continued algebraically on the generic rational construction, but this does not assign a numerical value to raw 0/0 or produce missing geometric vertices. In a restriction where an area expression vanishes identically, an unreduced geometric quotient would still require its stated defined-locus qualification.

## Genuine four-periodic certificates

The axis diamond has four distinct vertices and equal side lengths, and direct reflection in the ellipse normals gives the next side at every bounce. Its least period is four. The dual-conic tangency equation produces lambda=R/(R+1) in (0,1), axes squared R²/(R+1) and 1/(R+1), and exactly the stated contact rectangle. Thus these are valid convex billiards with strict elliptical caustics, not merely arbitrary centrally symmetric polygons.

The rectangle antipedal formula was independently reconstructed by intersecting homogeneous lines. The resulting signed area is 2x(x²+y²-c²)²/[y(x²-c²)]. Both reductions in R are correct.

At R=2, all eight intersections for the two focal constructions have nonzero determinants; direct exact evaluation places each antipedal at the opposite focus. This is a finite zero-area/zero-area quotient, not a pole.

At R=(1+sqrt(5))/2, positivity and x²=c² imply x=c. The two relevant lines are Y=y and Y=-y with y>0. Their homogeneous intersection has zero last coordinate and nonzero first coordinate. They are genuinely distinct parallel lines. The outer orbit and caustic remain nondegenerate. This is outside the common finite locus, not another finite collapse.

The proof correctly says that these examples vary the ellipse/caustic and do not demonstrate phase variation of a defined quotient in one fixed Poncelet family. Neither is a counterexample to the intended rational invariant.

## Disposition

The unchanged proof is suitable for a claimed-solved, domain-qualified draft for this exact arXiv table row. Preserve the primitive-even elliptical-caustic scope, signed areas, finite and nonzero domains, edition correction, and established-method credit in the publication summary. No unqualified value at exceptional configurations or originality certification follows from this review.
