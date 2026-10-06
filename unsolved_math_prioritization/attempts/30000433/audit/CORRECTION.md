# A1: Complete the self-handle quotient certificate

Problem 30000433 / OWR-1194-002. Audit supplement, 6 October 2026.

## Finding and scope

Section 5.4 and the function `self_handle` in the frozen author package check that the two puncture boundary vertex sets are disjoint and that no remaining simplex meets both. These checks exclude collapse within a simplex. Alone, they do not exclude unintended identifications between distinct simplices that share vertices outside the boundary. For example, edges `{a,x}` and `{b,x}`, with `a` and `b` paired boundary vertices and `x` an exterior vertex, acquire the same vertex set after gluing. Neither edge meets both boundary sets.

This is a narrow missing certificate condition, not an incorrect manifold or edge count. The independent audit verifies the stronger condition for the actual 600-cell construction. No asserted mathematical conclusion or stored author result changes.

## Additional condition and why it suffices

Let `q` identify the specified pairs of boundary vertices and fix all other vertices. For every simplex of the punctured complex:

1. Its vertices must have distinct images.
2. Every fiber of the map from old simplices to image vertex sets must be a singleton or exactly a pair of simplices on the two boundary components identified by the prescribed simplicial map.

Condition 1 makes the quotient map injective on each simplex. Condition 2 says that assembling the image abstract complex introduces precisely the intended identifications. Thus its realization is the PL boundary gluing, with no accidental additional face identification. This condition is stronger than the original no-mixed-simplex guard, which remains a useful preliminary check.

For the actual self-handle, the exhaustive counts by dimension are:

| Dimension | Old simplices | Image simplices | Prescribed boundary pairs | Extra collisions |
|---|---:|---:|---:|---:|
| 0 | 118 | 106 | 12 | 0 |
| 1 | 696 | 666 | 30 | 0 |
| 2 | 1140 | 1120 | 20 | 0 |
| 3 | 560 | 560 | 0 | 0 |

The audit also verifies that each puncture boundary is induced, their union is exactly the boundary of the complement, and the symmetry is an involutive simplicial automorphism of the full 600-cell boundary. All 20 oriented boundary triangles are reversed by the gluing map. Consequently the original PL-surgery identification as S2 × S1 is justified.

## Proposed insertion in Section 5.4

After the sentence about disjoint boundary vertex sets and no simplex meeting both, insert:

“The quotient is additionally checked in every simplex dimension: two distinct old simplices have the same image vertex set only when they form the prescribed matching pair of boundary simplices. Exactly 12 vertex pairs, 30 edge pairs, and 20 triangle pairs are identified; no other simplex identifications or degeneracies occur. Hence the image abstract simplicial complex realizes the intended PL boundary gluing.”

## Separate code patch and test policy

`verify_quotient_guard.patch` adds this all-simplex fiber check before the self-handle image is constructed. It also clarifies the old guard's comment. The patch is tested on a separate copy; the immutable author ZIP and its manifest are preserved. Its normal and optimized mathematical outputs equal the frozen `results.json` byte for byte.

The guard accepts a positive matching-boundary control and rejects four synthetic negative controls: unintended exterior edge, triangle, and tetrahedron identifications, and collapse of a simplex meeting both boundaries. The first three pass the old no-mixed-simplex test, directly demonstrating the logical gap. These are local guard tests, not claims that the small synthetic inputs are manifolds.

Applying the patch changes `verify.py`, so the old author manifest must reject the modified file. This rejection was verified. Any newly distributed patched author version requires a new manifest and external archive/manifest hash. The audit's own exact checker supplies the missing certificate without rewriting the author freeze.
