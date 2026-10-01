# 5100005: edition-specific k111 and a credited consequence of PR147

Revision 2: source/arithmetic audit awaiting separate review. The original local draft is retained; this revision makes the journal k112 product/ratio discrepancy explicit. **No new proof-search turn or independent discovery is claimed.** The geometric witness is the already-reviewed campaign construction for5100001/PR147.

## 1. Which statement is assigned?

The pinned dataset record5100005, AMR-050-0005, asks whether A′A″ is invariant for even N. This matches **arXiv:2004.12497v11**, Table2, p.5, row k111, where it is marked unproved. P′ is formed from intersections of consecutive tangents to the outer ellipse at orbit vertices. P″ consists of the chord tangency points on the confocal caustic. The areas are signed, as defined in the source's preliminaries.

The published 2021 article has a different row numbered k111: A′A″/A²=1 for **odd** N, marked proved. The old even-N k111 row is absent as such from that table. The journal nevertheless prints A′A″ again in row k112 for all N, beside the dimensionless value [ab/(alpha beta)]²; that is a separate product/ratio discrepancy, not evidence that the product expression disappeared entirely. Its appearance in the expanded preprint is not evidence that the authors formally acknowledged an error or issued an erratum; no such claim is made here. The two editions must not be conflated, and the published odd-N ratio is not the assigned target.

Both table pages were visually inspected. The upstream prior report's suggestion that the same unproved k111 occurs in both tables is not reliable.

## 2. Prior-work and duplication gate

No prior PR or branch specifically for5100005 was found, and its main queue row was untouched. However, the prior campaign's PR147 for5100001 already establishes the relevant primitive four-period geometric pair, its exact common confocal caustic, physical billiard reflection, and an explicit continuous family connecting the examples. Its independent review passed the unchanged proof.

This note reuses that witness with full attribution, rather than claiming a newly discovered orbit family or rerunning its full search. The assigned k111 expression differs from PR147's k107 expression, but the negative consequence uses the same geometry. Treat it as source-aware credited coverage, not another independent mathematical discovery.

Prior proof at immutable commit502de2f863a63ca205814da4194411847797a7c3:

https://github.com/AlecKriebel/Math/blob/502de2f863a63ca205814da4194411847797a7c3/unsolved_math_prioritization/attempts/5100001/COUNTEREXAMPLE.md

Prior separate review:

https://github.com/AlecKriebel/Math/blob/502de2f863a63ca205814da4194411847797a7c3/unsolved_math_prioritization/attempts/5100001/review/REVIEW.md

The proof's SHA256 is d34e4347358f54b20c9cea7d974e2c6a2308a5e69c7abf46de16132d83f9edbd, matching the prior review.

## 3. The known outer/contact area relation

Let the outer ellipse have matrix E=diag(a²,b²), and the caustic have matrix C=diag(alpha²,beta²). Write the line of an orbit edge as n·X=h. Its pole with respect to the outer ellipse, which is the intersection of the two endpoint tangents, is

    T=E n/h.

Since the edge is tangent to the caustic, its contact point is

    S=C n/h=C E^(-1) T.

Consequently the contact polygon is the fixed linear image of the outer tangent polygon, with the same cyclic indexing. Signed areas obey

    A″ = det(C E^(-1)) A′ = (alpha beta/(ab))² A′.          (1)

The exact ratio A′/A″=[ab/(alpha beta)]² is already recorded as proved in arXiv-v11 row k113, credited there to Hellmuth Stachel. The journal k112 row prints a product instead of that ratio alongside the same dimensionless value; we do not silently quote its displayed product as a ratio or certify the authors' intended correction. The elementary polarity calculation above establishes the relation used here and explains its application; it is not presented as a new theorem of this attempt.

## 4. Evaluate the prior primitive four-period pair

Use the prior witness's outer ellipse

    x²/16 + y²/9 = 1

and fixed caustic

    x²/(256/25) + y²/(81/25) = 1.

The squared-axis differences are both144/25, strictly between0 and9, so the caustic is strictly nested, nondegenerate, and confocal. The two counterclockwise orbits are

    D=((4,0),(0,3),(-4,0),(0,-3)),
    R=((16/5,9/5),(-16/5,9/5),(-16/5,-9/5),(16/5,-9/5)).

PR147 establishes primitive period4 and the continuous same-caustic Poncelet family. In particular this is not a doubled two-period trajectory, a change of caustic or winding family, a hyperbolic-caustic limit, or a self-intersection convention. Both polygons and their derived polygons are convex and positively oriented, so signed and ordinary areas agree.

The already-calculated outer areas are A′(D)=48 and A′(R)=50. The factor in (1) is144/625, so

    A″(D)=6912/625,       A″(R)=288/25,
    A′(D)A″(D)=331776/625,
    A′(R)A″(R)=576.

Their positive difference is28224/625. Therefore the **imported even-N arXiv-v11 k111 product is false**, as a direct credited consequence of the prior reviewed witness and the known area relation.

The neighboring k110 product AA″ is a different target. For this pair both its values equal165888/625, consistent with the existing even-period product theorem; these computations do not refute k110. The published odd-N expression also remains outside the present target.

## 5. Exact check and scope

The short standard-library program verify_area_consequence.py recalculates only the target-specific outer/contact polygons and area arithmetic, over exact rational numbers. It checks endpoint ellipse incidence, nondegenerate tangent intersections, exact caustic tangency and interior contact parameters, positive signed areas, the fixed linear map, unequal k111 products, and the equal k110 control. It does not redo the previous proof search or claim to establish a new geometric family.

Recommended classification after source/arithmetic review: **already covered / source-aware consequence of PR147**, with0 new substantive proof-search turns. Do not call this a new independent discovery or imply that the different published k111 has been disproved. No external contact or remote write was made during this audit.

## Primary sources

1. Reznik-Garcia-Koiller, *Eighty New Invariants of N-Periodics in the Elliptic Billiard*, arXiv:2004.12497v11, Table2 p.5, and definitions in Sections2-3.1: https://arxiv.org/abs/2004.12497v11
2. The same authors, *Fifty New Invariants of N-Periodics in the Elliptic Billiard*, Arnold Mathematical Journal7(2021),341-355, Table2 p.345: https://amj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf
3. Prior campaign proof and separate review: https://github.com/AlecKriebel/Math/pull/147, at the immutable file links above
