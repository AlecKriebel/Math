# Independent audit of the planar word lemma

Audit checkpoint: 2026-10-07 04:32:08 UTC.

Source: `/Users/alec/Desktop/math/preprints/A-group-without-fixed-price-October-5-2026/build/planar.tex`, checkout `adc7f1241b42e322a6451854ab7e4b4c146bf78a` (verified by read-only `git rev-parse HEAD`).

Scope: only the planar word lemma and its proof. No source or Git changes, no external communication. Estimated completion of this scoped audit: **100%**. This is an audit-completion estimate, not a claim about completion of the parent research program.

## Claim and boundary conditions

The source assumes a coefficient group H with a finite generating alphabet, L = H * F(U), relator words with at least seven positive, pairwise distinct U generators, at most one common U generator between different relators, and injectivity of H into D = L / <<R>>. For a cyclically H-reduced null word W with an exterior occurrence, it concludes either a full cyclic relator match, including the closing coefficient gap, or two exterior-disjoint relator intervals, each containing at least m(r)-3 exterior occurrences and equal intervening H-valued gaps.

The coefficient group can have torsion and need not be finitely presented. Exterior disjointness is occurrence disjointness. An interval match does not constrain either endpoint's external coefficient gap.

## Result

No counterexample or invalid inference was found in the stated lemma. The proof's tracks, connectivity, dipole cancellation, coefficient-gap equality, and curvature count are sufficient under the stated assumptions.

There is also a checkable strengthening: under the same assumptions, m(r)-3 may be replaced by **m(r)-2**. The same proof with the revised weights below works already for m(r) >= 4. This extra deduction is not needed to validate the source claim and has not been independently audited by a second child agent (an attempted delegation encountered the live-agent limit).

## Exact line findings

- **Lines 68–100, finite filling and minimality:** Membership in the normal closure gives a finite product of conjugates. A finite equality over all true H relations uses finitely many such relations. Enlarging that finite set during replacement preserves the relevant minimality because N is minimized in the actual group L. No finite-presentability assumption on H is silently used.
- **Lines 103–114, tracks:** A generic point in the open U edge has a 1-manifold preimage, with one endpoint for each written exterior occurrence. Arc endpoints have opposite disk-oriented signs. The target near that point has no attached H cell. This works for arbitrary H, including torsion.
- **Lines 118–138, connectedness:** A regular-neighborhood boundary avoids all chosen U points. Its image therefore gives an H element. Capping all relator holes on the side away from O makes that element trivial in D; injectivity makes it trivial in H. Replacing the whole side removes at least one relator disk. Closed tracks do not invalidate this argument.
- **Lines 141–153, inner loops and same-relator dipoles:** Uniform exterior sign excludes an inner loop. For an edge between two copies of the same relator, uniqueness of its U occurrence makes the two boundary loops based at q_u literal inverses, including the coefficient words. The constant joining track introduces no conjugating H element. A neighborhood of the disks and track has null boundary in L, and replacing it is a legitimate N-decreasing operation, even if other tracks cross its boundary.
- **Lines 155–158, simple inner graph:** At most one joining edge between different relator disks follows from the common-generator hypothesis and occurrence uniqueness. Every inner degree is exactly the number of exterior occurrences.
- **Lines 160–186, face equations and exact gaps:** Collapsing the U circles defines the natural map from the finite coefficient presentation to H. A sufficiently thin neighborhood of an arc maps to a small interval around q_u, so its side paths disappear after collapse. A face sector between consecutive endpoints contributes exactly its H-valued gap. A bigon yields the inner gap times the inverse of the W gap equal to 1. Thus equality is exact in H, not merely conjugacy. Closed tracks inside the complementary disk cause no difficulty after the same collapse.
- **Lines 171–177, short faces:** A monogon at O would give adjacent inverse exterior occurrences with trivial coefficient gap, forbidden by cyclic H reduction. A length-two face incident to an inner vertex either uses parallel edges or traverses an edge twice; the latter forces degree one at that inner endpoint. Thus every inner bigon is an inner–O bigon.
- **Lines 193–219, original curvature:** The face bound includes repeated vertex and edge occurrences. With exactly one O occurrence, two neighboring corners contribute 1/2 each, and the remaining inner corners contribute 1/3. With at least two O occurrences there are at most length-2 inner corners, each of weight at most one. Summing the face bounds and using Euler's formula gives total inner contribution at least two.
- **Lines 222–248, original exceptional-gap count:** Any positive vertex has an O edge. Unless all gaps are bigons, it has precisely one exceptional gap. Its h internal edges cost 1+(h-1)/3 when h >= 1, so h <= 3. The other gaps form a single consecutive bigon string exposing m-h >= m-3 letters. If h=0, the string still contains all m letters and omits the exceptional closing gap.
- **Lines 234–240, full match:** If all gaps are bigons, the cyclic adjacency pairs exhaust the rotation at O; any further O half-edge would interrupt one pair. Connectedness then leaves a single relator disk. All cyclic gaps, including the closing one, match.
- **Lines 250–255, two intervals:** Each remaining positive vertex contributes at most one, so total contribution at least two forces at least two such vertices. Every W exterior occurrence has exactly one incident arc, making the extracted intervals exterior-disjoint.

## Concrete falsification attempts

1. **Coefficient conjugation:** For W = h r h^{-1}, the cyclic closing gap contains h^{-1}h, so it agrees with r's closing gap. This cannot falsify full cyclic matching.
2. **Two relators sharing one exterior generator:** Cancelling their shared occurrence leaves an exposed consecutive interval of m(r)-1 letters on each disk. Only endpoint gaps can combine. Strictly intervening gaps retain their original H values, so this cannot falsify the required intervals.
3. **Same-relator copies with a coefficient between them:** A nontrivial coefficient obstructs direct U cancellation and leaves long exposed intervals. If a constant track does join the unique same-U occurrences, the based boundary loops are exact inverses and a dipole cancellation lowers N. There is no residual coefficient-conjugacy defect.
4. **Disconnected clusters, torsion, and closed tracks:** The cluster's surrounding curve lies in H. Injectivity H -> D is precisely what prevents a nontrivial H element from making a disconnected cluster indispensable. No deletion of an individual closed track is required.
5. **Bridges and repeated face walks:** Corner occurrences must be counted with multiplicity. The source does this. A face with one O occurrence and repeated inner vertices still has two neighbor-corner occurrences, both of weight 1/2; a doubled edge cannot be a length-two inner face at degree at least seven.
6. **All-O vertex with one exceptional gap:** Such a vertex exposes all m exterior occurrences in one interval but need not match the closing gap. Its contribution is one, so the global count still produces a second disjoint interval. The proof does not incorrectly promote this case to a full cyclic match.

## Independent stronger curvature count

Give an inner disk the sign + or - according as its boundary reads a relator or its inverse. By lines 110–114 every inner–inner edge joins opposite signs. Thus the subgraph on inner vertices is bipartite, and any facial walk avoiding O has even length. It has length at least four, since inner loops and inner bigons are excluded.

Assign the following weights:

- zero at O and at every corner of a bigon;
- 1/2 at a non-bigon inner corner if at least one incident edge joins inner vertices;
- one at a non-bigon inner corner if both incident edges go to O.

For a face of length l:

- if it is a bigon, its weight is zero = l-2;
- if it avoids O, then l >= 4 and its weight is l/2 <= l-2;
- if it has exactly one occurrence of O, its l-1 inner corners each have weight 1/2, giving (l-1)/2 <= l-2 for l >= 3;
- if it has at least two occurrences of O, its at most l-2 inner corners each have weight at most one.

All these bounds count corner occurrences, not distinct vertices. Repeated walks avoiding O are still even because every traversed inner edge changes the disk sign. A bridge-containing facial walk of length two would have to traverse its sole edge twice, forcing degree one at each endpoint, so no such face can involve an inner vertex of degree at least four. Any longer repeated inner walk is covered by the even-length bound. In a non-bigon face with exactly one O occurrence, an inner corner cannot have O at both neighbors: that would require two O occurrences (the length-two exception was already handled as a bigon). An O loop in a walk of length greater than one likewise contributes at least two O corner occurrences, so it belongs to the last face case. An O-loop monogon is excluded by cyclic H reduction. Thus neither repeated walks, bridges, nor O loops require an omitted case.

Consequently the same Euler calculation gives sum_v (2-c(v)) >= 2.

If m(v) >= 4 and v has no O edge, then c(v) = m(v)/2 >= 2, so it is not positive. For a vertex with O edges, each exceptional gap with no internal edge costs one. An exceptional gap with h >= 1 internal edges costs (h+1)/2. A non-full positive vertex has exactly one exceptional gap, and it contains at most two internal edges. The remaining cyclic string of bigons matches at least m(v)-2 exterior occurrences. Its contribution is at most one. The same total-curvature and endpoint-uniqueness arguments produce two exterior-disjoint such strings.

This establishes the strengthened alternative with m(r)-2 under m(r) >= 4, subject to the same filling and injectivity assumptions already verified above.

## Remaining gap and limitations

There is no unresolved mathematical gap identified in the source lemma. This is a direct proof audit, not a finite search over coefficient groups or all presentations. The strengthened bound has a complete derivation above but should receive a fresh adversarial read before incorporation in the paper. No opinion is offered here on any other section or downstream use of the lemma.
