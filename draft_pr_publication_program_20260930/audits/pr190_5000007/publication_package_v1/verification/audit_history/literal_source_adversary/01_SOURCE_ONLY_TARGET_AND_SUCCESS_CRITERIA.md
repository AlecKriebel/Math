# Independent literal target and success criteria -- PRE-CANDIDATE SEAL

Created: 2026-10-14 05:21:30 UTC
Case: PR190 / problem 5000007. Original claimed head supplied by coordinator: 0c3346c8ebcb3b967a1d8bf9a283f027b44b738c.
Independence: this assessment was authored before reading any candidate proof, original review, sibling opinion, or root mathematical opinion. Only the task assignment (including the warning to test wording corrections), workspace instructions, and primary sources were available.

## Primary-source identity and scope

Dmitry Fuchs, *Billiard Trajectories in Regular Polygons and Geodesics on Regular Polyhedra*, Arnold Mathematical Journal 7 (2021), 493--517, DOI 10.1007/s40598-020-00170-8. Read from the author/journal-hosted full final PDF at https://amj.math.stonybrook.edu/pdf-Springer-final/020-0170.pdf. Retrieved 2026-10-14 05:21:30 UTC; file SHA256 9550009b3a903727a89abba863c520def9bf900b6bec779b63ef6cc82d43f01d. This is a body-level, not snippet-only, assessment. No primary-source body is designated safe-public.

## Exact target without importing a proposed correction

Conjecture 3.2, printed p.515, concerns ALL short geodesics of type A0 on the regular dodecahedron: starting vertex v and terminal vertex w must never have graph distance 2. The distance is the minimal edge-path length on the 20-vertex dodecahedral graph (p.514); it is not intrinsic metric distance, face distance, Euclidean chord distance, or length of the geodesic. The context lists layers of cardinalities 1,3,6,6,3,1. The text's finite search uses edge length 1, trajectory length <120, a fixed incident starting face, and initial angle <3pi/10, but these are experiment settings, not restrictions in the printed conjecture. It does not ask only about loops, generic directions, or a finite length window.

The exact words of the conjecture are deliberately not reproduced here. The mathematical quantifier is: for every positive-length admissible vertex-to-vertex geodesic gamma in the target type, d_graph(gamma(0),gamma(L)) != 2. A full resolution must justify which A0 is meant using the whole Section 2 definition, not silently replace it by a convenient invariant.

## Necessary source definitions and conventions

- A short polygonal billiard trajectory goes from one polygon vertex to another, possibly the same (Section 1.2, p.495). Section 2.1 unfolds it by reflecting copies of the polygon; endpoint images are reachable. Section 2.3 explicitly tests for no earlier tiled vertex in the open segment, supporting the usual saddle-connection/first-vertex interpretation; passing through a cone vertex is not an admissible continuation. Self-crossings are not excluded.
- A dodecahedral short geodesic likewise starts and ends at vertices; folding face developments gives pentagon short trajectories (p.514). Both same-vertex and different-vertex endpoints are in scope. A path following a single edge is not explicitly excluded: Fig.9 labels polygon sides as short trajectories, and the square discussion also admits axial unit points. Boundaries therefore require treatment, rather than automatic removal.
- The initial regular n-gon has O=(0,0), its first side on positive x, and lies above that side (p.501). Developments lie in the angle of width (n-2)pi/n. Reachability is more than belonging to the cyclotomic coordinate module: an unfolding segment must actually occur without earlier vertices.
- Types Ak have indices modulo n-2. Figure 8 defines alpha at the starting vertex from its outgoing oriented side to the outgoing tangent; at the end pi-beta is the interior angle involving the reverse tangent and the ending oriented side. For n=5, 0<=alpha<=3pi/5 and 2pi/5<=beta<=pi in the normal face representation; strict inequalities apply for face-interior entry/exit. The terminal beta is the external/supplementary convention, not simply a second acute endpoint angle.
- The text immediately before Definition 2.1 states that the relevant angle combination is alpha-beta for even N and alpha+beta for odd N, each a multiple of 2pi/n, for an oriented N-gonal short trajectory. N counts straight pieces. For a trajectory with transverse side crossings, the crossing count is N-1. Thus crossings odd means N even. The source does not license exchanging N and crossing count. A zero-crossing face diagonal has N=1.
- Definition 2.1 gives piecewise angle conditions, and its n=5 specialization distinguishes A0,A1,A2. Figure 9 assigns X0X_(k+1) type Ak with vertices in clockwise order: the two sides are A0, while the two direct pentagon diagonals are A1 and A2. The pentagon reflection exchanges A1/A2 and preserves A0 (pp.507,515).
- Section 2.4 calls reachable n-gons area-preserving linear images with all non-origin vertices reachable. Conjectures 2.3--2.5 assert stronger type/orbit structure; these are conjectures in Fuchs, not proved tools available for free. The text's informal Veech-orbit equivalence is not an unconditional theorem. Section 2.5's type and length assertions 2.6/2.7 are also conjectures in this source.

## A source-internal exceptional-direction issue, found independently

Printed p.506 advertises the shortcut A0 iff beta-alpha=2pi/n, without an alpha restriction. The piecewise formulas and tables also have difference and sum rows. At special angles BOTH difference and sum can be multiples of 2pi/n, so the preceding N-parity convention is indispensable if the types are to form a partition. This is not a minor numerical endpoint issue.

Take the regular unit-side pentagon with X0=(0,0), X4=(1,0), and clockwise vertex order X0,X1,X2,X3,X4. Direct diagonals X0X2 and X0X3 have N=1 and, respectively, (alpha,beta)=(2pi/5,4pi/5) and (pi/5,3pi/5). Both satisfy beta-alpha=2pi/5. Figure 9 nevertheless labels them A1 and A2, not A0. These are valid geodesics through the open interior of one dodecahedron face with no interior vertex; their endpoints are distance 2 in the dodecahedral graph, because the two boundary edges give a two-step path and they are not adjacent. Consequently a literal standalone reading of the p.506 A0 angle shortcut makes Conjecture 3.2 FALSE by a single face diagonal.

Even Definition 2.1, if all four displayed branches are treated as unordered OR conditions without the preceding parity instruction, gives these diagonals both A0 and their Fig.9 type. Thus the PDF does not support a unique literal type partition at these exceptional directions unless the N-parity instruction is used as a selector. A proof may legitimately explain this inconsistency and explicitly state a coherent parity-selected reading, but it must not claim that proving a weakened generic-angle or odd-crossing variant alone resolves the unqualified printed shortcut.

For n=5 under the parity-selected reading, an interior A0 segment must have N even (crossings odd) and beta-alpha=2pi/5. The source's odd-N formulas assign only A1/A2 for strict interior alpha,beta. The one-piece boundary sides are A0 via the identified index A3=A0 and end at graph distance 1. This suggests the exact corrected all-direction target: the parity-selected A0 interior sector plus the edge boundaries, with a proof that no excluded exceptional non-edge trajectories carry the intended A0 label. That identification needs its own argument. It is not enough to assert by definition that A0 means odd crossings and ignore boundary/ambiguous cases.

## Falsifiable success criteria for the forthcoming proof audit

1. Specify the claimed theorem separately from the source correction. Preserve all lengths, all vertices/start faces, self-intersections, returning geodesics, non-generic directions, and source-admitted boundaries.
2. Authenticate every external theorem used for global saddle-connection orbit generation, affine-group lifting, coverings, and finite quotient enumeration. Fuchs's conjectural orbit claims cannot be used circularly.
3. If a double-pentagon edge orbit is used, establish both directions of the identification of the source's intended A0 with that orbit, including exceptional directions and sides, and explain sheet/crossing parity precisely.
4. A graph-distance exclusion requires an actual lift endpoint classification or a sufficient invariant; the set must include all relevant branches of the 60-sheet holonomy cover and be independent of labeling choices.
5. Check the one-face diagonals explicitly. If the claimed resolution uses only beta-alpha=2pi/5 with no N restriction, it fails. If it chooses a parity convention, the report must label that as an interpretation/correction and give the printed-literal counterexample prominently.
6. Verify computational finite closures reproducibly against explicit permutations and topology; no finite numeric search establishes the universal geodesic claim by itself. Distinguish proved equivalence from empirical samples.

Status at seal: source target authenticated; source inconsistency and independent face-diagonal counterexample identified; no candidate read yet. Audit completion estimate: 40%. No conclusion about the candidate's correctness is made before opening it.
