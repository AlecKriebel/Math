# Independent fifth-pass geometry and completion audit

Problem row 1757 / 5500059 / AMR0540059. Audit date: 2026-10-13. No novelty claim.

## Accepted findings and limits

The final exact certificate is accepted as a **partial** 136-cell extension, retaining all 56 coarsened boundary cells and adding 80 genuine hexagons, each with circularity strictly below 64439/50000. It covers the entire square boundary and approximately 32.24892181598% of the square area. A neighborhood of the square center is still uncovered. It is not a partition of the whole square.

The new independently reconstructed pair table has exactly 9,180 rows: 8,972 empty intersections and 208 complete shared edges. There are no isolated point contacts, partially shared edges, or interior overlaps. All 144 two-cell vertices of the remaining inner boundary have a free angle above the necessary single-cell angle threshold. This avoids one immediate obstruction but gives no sufficient condition for completion.

The separate three-cell rejected collar is also accepted as an exact obstruction **to preserving those three cells** in a finite completion of circularity at most 13/10. Its narrow free angle does not invalidate the 136-cell variable-seam collar.

Retaining the 136 cells in any finite convex completion below sqrt(2) requires at least 310 additional pentagons and at least 446 cells altogether. These are necessary counts, with no assertion of attainability. The entire near-critical square problem remains open. The separate complete-square upper bound below 1.295516 is not replaced or improved.

## Exact frozen inputs

The audit retained and checked the complete final producer inputs. This publication includes the authored proofs, exact certificates and mathematical checks, while the full original inputs remain separately preserved. The following proof identity is rebound to this edition's reference-normalized text; certificate identities remain unchanged:

- Final completion-status proof: 11,618 bytes, SHA-256 `560c8c319d22cfdb80ad874f6503efb4a116a4f7334815b0f8c159812d5d1907`.
- Complete coarsened-boundary certificate: 77,009 bytes, SHA-256 `6e7136b295451a6bd8c49c04440f319dce534c94f91484eac21530e53492393e`.
- Partial-collar certificate: 18,958 bytes, SHA-256 `d028fc1ab1cbeff1f439db04a9e1b9858f960c06a57b1cb6c0f66f7af0bbffea`.
- Rejected local-collar certificate: 4,576 bytes, SHA-256 `15fa66b6ea16ef3474b2c13ca8c5dd50c73fe9bf1b5f48829adc5805c8c128c8`.

The complete fixed-patch Euler proof and prior independent boundary review were read, not merely their summaries. The geometric checks below do not trust the producer's acceptance booleans or floating-point discovery output. The original complete-square upper bound is prior context, not a claim newly reconstructed by this audit.

## Independent implementation and disk witnesses

The independently authored geometry verifier is a standard-library rational checker. It imports no producer verifier, numerical optimizer, or floating geometry library. It independently reconstructs all eight boundary types, ten cap types, and 136 placed cells.

For each canonical polygon, every nonincident vertex lies strictly in the inward half-plane of every directed edge. This proves global convexity and excludes collinear redundant corners, rather than relying on consecutive-turn signs alone. There are 962 such nonincident support tests. All vertices are distinct. Every squared witness inradius is positive.

For every directed edge e beginning at a, with witness incenter I and squared witness radius r2, the checker verifies

    det(e,I-a)>0,
    det(e,I-a)^2 >= r2 (e dot e).

Thus the entire witness disk lies in every supporting half-plane. Every vertex v also satisfies

    (v-O) dot (v-O) < gamma^2 r2.

Convexity of the enclosing disk then places the entire polygon strictly inside the proposed bound. The actual inradius can only be larger and the actual circumradius smaller. No equality between the two centers, optimality of the witnesses, or tangency of every original support is assumed.

Each placement is independently checked to be a positive rational scale, translation, optional reflection, and integer quarter-turn. Reflection reverses the vertex order to restore counterclockwise orientation. The 80 cap placements are distinct, use the eight occurrences of the specified boundary type, and retain the entire prescribed base edge. All placed vertices lie in the exact square. The original 56 polygons are included unchanged.

## Pair intersections, full edges, and the residual cycle

For every unordered pair, the independent algorithm searches coordinate axes and exact normals of actual polygon edges. All projection comparisons use Fraction arithmetic. A strict separating gap proves empty intersection. At a supporting-line equality, the checker intersects the exact one-dimensional support-face intervals. A positive-length intersection is accepted only when it is the complete same edge of both polygons. This determines the full intersection, since any intersection must lie on that separating line.

The 208 resulting full shared edges divide into 56 original interfaces, 80 base edges, and 72 new cap/cap seams. Their oriented occurrences are opposite. The checker separately replays every one of the producer's 9,180 stored edge-axis witnesses, checking pair identities, duplicate exclusion, edge indices, ordering, and exact separation inequalities.

The remaining edge inventory contains 60 outer-square edges and 592 inner edges. On each of the four square sides, 15 exact intervals tile from zero to the square side length, with no gaps or overlaps. Thus square-boundary coverage is checked directly rather than inferred from the number of cells.

Every vertex of the residual inner graph has degree two, and an explicit traversal reaches every vertex. Pair intersection classification precludes crossings and unintended self-contacts. Therefore it is one simple cycle. It has 448 one-cell vertices and 144 two-cell vertices. The genuine-side count is

    1068 = 60 + 2(208) + 592.

Exact shoelace areas reproduce the producer's two full rational area fractions. The old fraction is approximately 0.3199339167052989 and the new one approximately 0.3224892181598094. The increase is positive and the total is less than one. More strongly, the square center strictly violates at least one support inequality of every cell. Finiteness and strictness imply an open neighborhood of the center remains uncovered.

## Necessary angles and every new tip

For any cell of circularity at most gamma, normalize a contained disk to radius one. If a vertex angle is alpha, its distance to the incenter is at least csc(alpha/2). An enclosing circle containing that disk and the vertex has radius at least (1+csc(alpha/2))/2, even with an independent center. Thus

    alpha >= 2 arcsin(1/(2gamma-1)).

The threshold is acute for the target gamma. Let c=1-2/(2gamma-1)^2>0. For two nonzero free-sector rays u,v, write D=u dot v and A=(u dot u)(v dot v). The smaller sector is above the threshold when D<=0 or D^2<c^2 A.

It is essential to identify the free sector, rather than just compute a smaller angle. The checker finds the two exact endpoints of each entire shared edge and the nonshared neighboring rays at the selected endpoint. Their positive sum lies in the smaller sector. Exact support signs place that sum exterior to both incident cells. Degenerate parallel sectors are excluded.

This calculation is applied to the nine canonical new seam tips, the two canonical collar endpoints, and independently to **all 144 two-cell vertices** of the global residual cycle. Every one passes. Rationalized angles close to 79 degrees are not asserted to equal or exceed precisely 79 degrees; the accepted statement is the exact necessary-threshold comparison. No circle fit or global extendibility follows merely from passing it.

## The local nonextendible three-cell example

The rejected local certificate's first polygon is verified to equal the complete canonical fixed boundary polygon. All three cells have valid strict disk witnesses; each pair intersects in a complete common edge with disjoint interiors. At the new hexagon/hexagon tip, the same exterior-sector method recovers the supplied rays exactly, and the fixed parent does not cover the tip.

For the free sector, the checker obtains D>0 and

    1024 D^2 > 49 A,

so cos(phi)>7/32. But cos(2 arcsin(5/8))=7/32, and at circularity 13/10 every genuine angle is at least 2 arcsin(5/8). Hence this free sector is too small for even one permitted cell. Splitting it among more cells cannot help.

A finite full convex completion would have to cover a neighborhood of the tip. Cells not containing the tip cannot approach it arbitrarily closely, because there are finitely many closed cells. Any new cell containing it has an incident angle inside the available wedge, contradicting the angle bound. This establishes the precise local preservation obstruction. It says nothing about other collars that change those polygons.

## Euler burden and the unresolved endpoint

The [published fixed-patch argument](../5500059_circular_square_fourth_20261013/FIXED_PATCH_INTERIOR_OBSTRUCTION.md) allows T-junctions. For the full finite boundary graph, let N,V,E denote its counts, X the sum of degree minus three over interior vertices, and C the extra side incidences created by subdividing straight genuine sides. Connectedness follows, for example, from a generic path through cell interiors crossing shared edge segments. With 60 outer edges, four degree-two square corners, and all other square-boundary vertices of degree three,

    V-E+N=1,
    2E=3V-4+X,
    sum(6-s_i)=58+2X+C.

The exact old/new interfaces fill the existing one-sided outer neighborhoods, so no new positive-area cell can touch the square boundary or add a boundary vertex. The 136 fixed cells contribute 1068-6(136)=252 excess genuine sides. Thus the remaining cells satisfy

    sum_added(6-s_i)=310+2X+C.

The independently reviewed perimeter argument R/r>=sec(pi/s_i) applies with unrelated incenter and circumcenter. It excludes triangles and quadrilaterals below sqrt(2). Therefore at least 310 further pentagons and 446 total cells are necessary. At a ceiling at most 13/10, every angle exceeds 72 degrees, so interior degrees are at most four; four-cell vertices have no flat incidence, while each flat incidence is a single degree-three T-junction. Hence X=V4 and C=T and

    P5=310+sum_(k>=7)(k-6)Pk+2V4+T.

Additional hexagons do not lower the budget. The counts are not sufficient, and no completion or finite stopping rule is supplied. This fifth and final pass closes with the full near-critical partition problem open, without starting a sixth research pass.

## Controls and preservation

Fifteen hostile geometry controls reject invalid support orientation, a false target, outside/new or old incenter witnesses, an invalid circumcenter, oversized indisk, missing/duplicate placements, a genuinely overlapping duplicate boundary cell, zero scale, an out-of-square translation, a false entire-base claim, and false tip/ray data. Cyclic reindexing of all ten cap polygons is a benign control and passes.

The mode replay checks byte-identical outputs in normal, -O and -OO Python modes, including all hostile controls. The separate pentagon review supplies its own rational checker and controls. The external preservation receipt records actual extraction and independent actual-byte-store reconstruction into different trees, full file-hash verification, and restored-tree replays. Those receipts, rather than this narrative alone, establish successful preservation.
