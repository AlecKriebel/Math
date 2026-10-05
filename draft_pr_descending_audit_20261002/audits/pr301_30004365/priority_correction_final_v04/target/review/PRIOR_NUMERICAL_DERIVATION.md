# Independent derivation of the direct numerical mechanism

Checkpoint: 2026-10-05 12:44 UTC. Best estimate 85% of assigned priority audit complete. This is an audit deduction from inspected prior source code and established surface invariants; it is not attributed as a theorem proved in an unavailable thesis. No other priority report was read before deriving it.

## Exact conditional claim

Given the correct finite marked ribbon cellulation of a connected gentle algebra, including all zero-marked ends, its line-field orbit invariants can be computed by finitely many graph, local-order and finite-field operations. The QPA (June 2024 source) and String Applet (archived March 2025 source) already provide explicit algorithms for the numerical step. The numerical mechanism does not require an unbounded search for a rational PL geometric handle system.

## Tree/cotree argument

Cap every end of a compact core by a disk, giving a closed oriented genus-g surface and a cellular ribbon graph G. Let D be a spanning tree in its dual. Remove primal edges dual to D, obtaining G0. The complement of G0 is one disk: each dual-tree edge merges two distinct disk faces, and after F-1 such operations all F faces have merged. Consequently G0 is connected and has E0=E-F+1 edges. Choose a spanning tree T in G0. For every edge e not in T, use e plus the unique tree path between its endpoints as a based graph cycle. There are E0-(V-1)=E-F-V+2=2g such cycles by Euler's formula. Cutting out a regular neighborhood of T yields the usual one-vertex polygonal schema; these cycles form a basis of H1 of the capped surface. Their pairwise intersection pairing is nondegenerate. Each cycle has a finite embedded representative on the original compact core, and its winding number is a sum of finitely many contributions at ribbon vertices.

This is exactly the mechanism of archived `surfaceHomologyBasis`: remove the dual spanning-tree arrows, take a primal spanning tree, and return the non-tree-edge fundamental cycles. The associated `spanningTree` stores the unique tree paths explicitly. This is constructive homology, not mere existence of a geometric basis.

## Which winding data suffice

For genus one, the winding numbers on these two handle representatives, together with each end's w+2, give the gcd invariant. Every other nonseparating curve differs through integral basis combinations and boundary terms; the correction terms are those already present in the published LP/APS genus-one classification.

For genus at least two and even end windings, the mod-2 winding obstruction is determined on the 2g handle generators (the end classes have zero obstruction). When every end winding is 2 mod 4 and handle windings are even, LP's quadratic refinement descends to H1 of the capped surface over F2. On a basis x_i, q(x_i)=w(x_i)/2+1 mod2 and its polarization is the intersection form. Thus the entire quadratic form is known from finite winding/intersection data. Finite symplectic elimination of the nondegenerate pairing computes Arf; each elimination reduces dimension by two. The String Applet explicitly forms this matrix and performs that elimination. A geometric symplectic basis is unnecessary for merely obtaining these numerical values. If desired, the QPA cut-a-handle method explicitly constructs geometric handle pairs instead.

## Finite predicates and scope

Graph searches visit finite vertices/edges. Unique tree paths have bounded length. Fundamental cycles have bounded length; local winding uses finite cyclic order. Two distinct fundamental cycles share tree paths but have distinct non-tree edges, so any maximal common-path search must exit in a finite number of steps. The pairing and quadratic arithmetic use finite matrices of dimension 2g. AG end cycles are finite arrow/thread orbits and retain multiplicity, including forbidden cycles corresponding to punctures. The scalar arithmetic is integer gcd and F2 arithmetic.

This establishes effectivity of the conditional numerical step. It does not formally certify every line of either software's gentle-input constructor, exceptional isolated-vertex conventions, floating precision at unrealistic input sizes, or decision comparator. The bounded replays supplement, rather than prove, the universal conditional deduction. The candidate's exact geometric-certificate search may still be a distinct presentation; this family did not find that particular search in prior literature.
