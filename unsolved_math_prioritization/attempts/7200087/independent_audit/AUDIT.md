# Independent audit: 7200087 / AMR-071-0087

Audit date: 3 October 2026. Frozen author manifest SHA-256:
`62fdca9246fb83a3bff4df9424dd9c54700d722336e28b146878157e358c1597`.

## Verdict

**PASS, with the existing scope qualifications mandatory.** The frozen certificate proves the literal at-least-one-edge existence statement under the explicitly declared acoptic convention permitting overarching face pairs. It is a credited prior result, with **0 original mathematical attempt turns**, not a new discovery. No mathematical repair to the integer witness or its exact verifier is required.

**HOLD for any unqualified resolution claim, for the current exactly-one-edge question, or for a claim that the live detail site's statement/status was independently verified.** The source convention must remain explicit wherever `already_solved` is used. The current stricter problem is not resolved by this witness. Neither the audit nor the author task establishes the exact historical date when Wikipedia's wording changed.

The frozen author directory has not been changed. All six payload file hashes and byte counts match its manifest. A fresh execution reproduces `VERIFICATION.json` exactly. No remote writes were made.

## 1. Wording, provenance, and allowed intersections

The supplied catalog record and the queue receipt identify the at-least-one wording: the target asks for a nonconvex polyhedron without self-intersections, with more than seven faces and each pair sharing an edge. Its provenance names Wikipedia revision 1366636767, accessed 29 July 2026. This independently audits the available pinned **record**, not the inaccessible historical webpage. A direct request for that revision failed through web retrieval; a normal MediaWiki revision API request returned HTTP 403. The live [UnsolvedMath detail page](https://www.unsolvedmath.com/problems/7200087) could not be retrieved. Those gaps must not be described as successful source verification.

The [current Wikipedia list](https://en.wikipedia.org/wiki/List_of_unsolved_problems_in_mathematics#Euclidean_geometry), inspected during this audit, expressly requires a unique shared edge for each pair. The [current Szilassi article](https://en.wikipedia.org/wiki/Szilassi_polyhedron#Complete_face_adjacency) retains the broader question box alongside discussion of the stricter case. These endpoints support a wording discrepancy; they do not establish a timestamped edit history or the intent of an inaccessible historical author.

[Grünbaum–Szilassi (2009), introduction](https://faculty.washington.edu/moishe/branko/BG277%20Toroidal%20complexes.pdf), explicitly uses a geometric convention allowing an intersection with multiple components, provided each component is a whole edge or vertex of both faces. Individual faces remain simple planar polygons, adjacent faces are noncoplanar, and the faces at each vertex form a circuit. Thus the certificate's broader convention has a genuine primary-source precedent. The witness meets these conditions; it is not merely an abstract map or an arrangement of intersecting polygons.

[Arseneva et al. (2024), Sections 1–2](https://link.springer.com/article/10.1007/s00454-023-00537-6), use a stricter model: a nonempty pairwise contact must be just a common corner or a complete common side. Their closing discussion of complete adjacency graphs is within that model. Their general graph construction permits boundary edges and does not by itself supply a closed surface. Consequently it cannot be substituted either for this certificate or for a solution to the stricter closed-surface problem.

The [2026 integer preprint](https://arxiv.org/html/2609.17700v1), Section 2, uses the strict intersection definition, whereas its abstract, Section 5, multiplicity matrix, and actual data admit doubled contacts. This is a real definitional inconsistency. The certificate correctly avoids adopting that definition and does not present the witness as non-overarching. Its proof is supplied by exact data verification under the stated broader convention.

The [Röst–Vígh preprint](https://arxiv.org/html/2609.32998v1), dated 26 September 2026, independently distinguishes the broader question from the stricter open case and gives a different eight-face construction. This audit checked that source's statement and scope, but does not certify its second coordinate table. Its result is corroboration, not an assumption needed for the present proof.

## 2. Complete input and author-checker review

All 72 integer coordinate entries and all 72 cyclic face-walk entries were compared against the complete primary HTML tables. Eight plane equations were checked against the source and independently against the coordinates and derived face normals. The stored primary HTML hash is `0df15456e4e152e9da3bd89717e115c1834159dbedda30c8754cd290f9e4ba2b`. The comparison imports no author verification functions.

The author checker was read in full, not merely replayed. For these fixed inputs its reasoning is sound:

- Distinct vertices, nonzero face areas, noncollinear adjacent edges, and exact rejection of every nonadjacent boundary-edge intersection prove that each projected face is a simple polygon. Projection along a nonzero normal coordinate is injective on the plane. The bounded region is a disk.
- Edge incidence, compatible signs, triangular links, and graph connectivity establish a connected closed orientable abstract surface. Link checks exclude pinches; mere edge multiplicity would not suffice.
- Every pair of supporting planes has a nonzero normal cross product. The computed rational line is valid and its chosen coordinate parameter is injective.
- Every possible membership change along that line occurs at a listed boundary crossing or endpoint. Boundary intervals and tangencies are included. Exact point-in-polygon tests on every open cell, plus isolated endpoints, therefore determine the full closed section. Compactness excludes membership beyond the extreme cuts. This is exhaustive subdivision, not numerical sampling.
- Interval-union comparison checks the full intersection, and the additional edge-union equality excludes extra isolated contacts. The disconnected-component check ensures the doubled edges are genuinely disjoint.

There are no floating-point tolerances or third-party dependencies. Assertions must be enabled; the script explicitly rejects `-O`. Its interface is a fixed-witness certificate, not a general-purpose validator of arbitrary user input. For example, it does not need a general parser for invalid vertex labels because the fully inspected witness uses exactly the labels 1–24.

## 3. Independent geometric and topological certificate

`check_triangulation.py` takes a separately transcribed source witness and does not import or call the author checker. It follows a different geometric route:

1. Derive supporting normals directly from vertices and recheck every face's planarity and simple boundary.
2. Ear-triangulate every simple nonagon using exact determinant signs and closed-triangle ear exclusion. Each yields seven triangles; their summed signed area equals the polygon area.
3. Check **all 1,540 pairs of the 56 triangles**. For the 168 same-face pairs, exact convex half-plane clipping gives precisely their common simplex. For the 1,372 pairs from different faces, intersect each convex triangle with the other plane using exact signed endpoint distances. Parameterize the common line by scalar product with its direction, and intersect the resulting closed intervals. No polygon ray casting, sampled polygon-section intervals, or solved line origin is used.
4. Require each geometric triangle intersection to equal exactly the common vertex, common edge, or empty set specified by triangle incidence. This proves the triangulated surface is geometrically embedded, and therefore proves all 28 original face-pair intersection claims.
5. Independently solve the face orientation constraints, check connected vertex links, and repeat topology checks on the triangulation.

Results:

- 24 vertices, 36 polygon edges, eight simple planar disk faces;
- 56 triangles and 84 triangulation edges, each with two incidences;
- every original vertex link is a triangle, and every triangulated link is a single cycle;
- connected, closed, orientable, embedded surface; Euler characteristic -4, genus 3;
- original compatible orientations `(+, +, -, -, -, -, +, +)`;
- reflex counts `(2, 2, 3, 3, 3, 3, 2, 2)`;
- 20 original face pairs share one complete edge and eight share two disjoint collinear complete edges;
- zero unintended intersections of any dimension;
- independent signed-volume sanity check gives absolute volume 4,455,360 in the supplied coordinate units.

The doubled pairs are `(1,4), (1,5), (2,3), (2,6), (3,7), (4,8), (5,7), (6,8)`, forming the claimed eight-cycle. The genus already rules out a convex solid; each face also has reflex corners.

Ten independent controls pass: two self-crossing polygons (including one with nonzero signed area), coordinate and boundary-order corruptions, transverse triangle intersection, tangency, full shared edge, separated triangles, a nontrivial invertible affine transformation, and simultaneous face permutation/cyclic shifts/reversals. The affine map has determinant 7 and scales the computed volume by 7 while preserving all contacts.

This is a finite exact certificate supported by elementary planar and manifold topology. It is not a machine-checked proof-assistant formalization. The source papers' authority or preprint review status is not used to fill a computational gap.

## 4. Additional independent verification of the 2020 construction

The [OSF record](https://api.osf.io/v2/preprints/hvtey/) and [primary-file metadata](https://api.osf.io/v2/files/5ea3ea6476188b006091a571/) were independently refetched. They give publication on 25 April 2020 and modification of the currently served file on 29 April 2020. The PDF was freshly downloaded from its public OSF link; its 508,088 bytes and SHA-256 `636e7ca7215c7b876e54640e00ce200d3bcbfb253f76ed43b09479212dfc626a` match the frozen source. These dates support the April 2020 credit; they do not justify assigning every detail in the later-modified file specifically to 25 April.

Pages 5–6 were visually inspected. Tables 5–6 supply rational coordinates and face vertex sets, rather than cyclic boundary walks. `check_2020_tables.py` independently transcribes those complete tables and enumerates face/vertex incidence isomorphisms to the 2026 walks. There are eight set-incidence candidates. Four pass the full exact geometric verification; the other four do not supply simple valid boundary walks. This distinction avoids incorrectly treating incidence sets as ordered polygons.

Recovered valid walks, both label maps, and a second full 1,540-triangle-pair verification are recorded in `2020-results.json`. The old coordinates themselves therefore give the same kind of embedded genus-3, eight-face, completely edge-adjacent surface. This strengthens the prior-result credit beyond merely trusting a claim in the 2026 introduction. It is reconstruction and verification of published data, not a new polyhedron.

One additional source error should be noted in any expanded historical account: the 2020 Section 3 prose says a face has one doubled neighbor. Its exact data give **two** doubled neighbors per face. The current frozen certificate already uses the correct multiplicities, so this requires no witness repair. A short note in the source audit would improve source transparency.

## 5. Mandatory publication boundaries and suggested repair

Retain all of the following qualifications in any resulting entry:

1. The affirmative answer is for the pinned at-least-one wording **under the stated acoptic convention allowing overarching faces**. A bare statement that the modern open problem is solved is not approved.
2. Eight face pairs have two disconnected collinear common edges. The exactly-one/non-overarching variant remains unresolved here.
3. Cite Mizhaev's April 2020 construction and 2026 integer certificate; use Röst–Vígh only as corroborating literature unless independently certifying its coordinates. Preserve 0/5 original attempt turns and no novelty claim.
4. Disclose the integer paper's strict-definition inconsistency. Its data are valid under the broader definition, not its Section 2 wording as written.
5. Do not claim to have read the inaccessible pinned revision or live detail page, or to have established an exact wording-change date.
6. Keep the corrected convex maximum of four and the Császár/Szilassi distinction. The genus formula needs both uniqueness of each shared edge and trivalence; combinatorial duality alone supplies no geometric realization.

**Suggested, nonblocking addition:** append the 2020 multiplicity typo and the successful independent reconstruction to `SOURCE_AUDIT.md`, with attribution. If that frozen file is changed, regenerate its manifest and identify the revised payload before publication. No change is necessary to the frozen mathematical theorem or checker.

## Reproduction

Run with Python 3 and assertions enabled:

```
python3 check_source_tables.py
python3 check_triangulation.py
python3 check_2020_tables.py
```

The source-table check uses the existing nonpublication source directory. The two geometric scripts contain all required mathematical data and need only the Python standard library. Source fetch receipts are audit evidence, not publication payload; do not republish original PDFs, HTML, screenshots, or third-party metadata dumps.
