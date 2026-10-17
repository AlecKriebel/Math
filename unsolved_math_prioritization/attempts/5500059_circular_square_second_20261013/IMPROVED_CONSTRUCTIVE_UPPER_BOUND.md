# A rational 100-piece partition with circularity below 1.296046

Problem: Most Circular Partition of a Square, AMR-054-0059 / 5500059.
Date: 2026-10-13. Second newly documented substantive construction pass in this continuation. Earlier lifetime attempt count is unknown.

## Theorem and scope

There is a partition of the square into 100 positive-area closed convex polygons for which every cell's smallest enclosing-circle radius divided by its largest inscribed-disk radius is strictly less than

\[
U=\frac{648023}{500000}=1.296046.
\]

Consequently the infimum over all finite convex polygonal partitions is at most 1.296046. This improves the first-pass rational 92-piece bound 1.298322 by 0.002276. It also improves the complete-square bound 1.29950 reported by Damian and O'Rourke in the identified source below. These are comparisons of explicit bounds, not claims of global novelty, optimality, or finite attainment. The value of the infimum is not determined here.

The square is fully covered, including its interior. A boundary-only cover or a local junction does not suffice for this theorem, and neither is used as a substitute for the coverage proof.

## Source and topology provenance

Mirela Damian and Joseph O'Rourke, *Partitioning Regular Polygons into Circular Pieces I: Convex Partitions*, arXiv:cs/0304023v2 (2026-02-08), Figure 16: https://arxiv.org/abs/cs/0304023v2.

The previous 92-cell rational construction optimized that figure's combinatorial layout. The present construction changes the topology before optimization: each of its four diagonal interior octagons is replaced by three cells, raising the total from 92 to 100. This introduces one new junction along each of two edges adjoining side-boundary cells, so those boundary cells gain a seventh side. The third subdivided edge faces the interior. Four vertices are added for each replaced octagon: three edge-subdivision vertices and one interior three-way junction. Thus the vertex count rises from 185 to 201.

For a completely reproducible description using the previous certificate's numbering, one representative octagon had boundary cycle

    [18, 38, 48, 54, 52, 46, 42, 25].

Subdivide the edges (38,48), (52,46), and (25,18), then connect their new subdivision vertices to one interior junction. The three new face cycles consist of each consecutive arc between subdivision vertices followed by that junction. Apply the same operation to the other three dihedral copies. Their geometry is then optimized simultaneously with the rest of the mesh. The final edges are not constrained to retain their initial subdivision lines: all listed final cells are strictly convex.

This topology description is provenance only. The complete final rational coordinate certificate below, independent of the previous figure or certificate, is the specification used in the proof. No third-party source text or source figure is needed for its verification.

## Complete exact specification

The accompanying `rational_partition_certificate.json` contains:

- common coordinate denominator D = 10^12;
- the square [-1,1]^2;
- 201 integer vertex pairs V_j, representing V_j/D;
- 100 counterclockwise polygon vertex cycles, with indices beginning at zero;
- for each cell i, integer centers A_i and B_i and a positive integer q_i.

The cell's witness indisk has center A_i/D and radius rho_i=q_i/D. Its witness enclosing disk has center B_i/D and radius U rho_i. The centers are separate and need not be equal; neither disk is assumed extremal. No tangency between cells' indisks is required.

Frozen certificate SHA-256:

    351a1b2bb5c3d922e36e4cd8f6b4c421cdce4fb3f1b05f49dab39268e1355b40

All coordinates, centers and radii are rational. The proof uses only the integer inequalities stated next. The optional SVG is explanatory, not an input to acceptance.

## Exact geometric verification and proof

For integer vectors define det(u,v)=u_x v_y-u_y v_x. Every assertion in this section was checked with arbitrary-precision integers, without floating-point tolerance.

### Strict convexity and containment

All coordinate components lie in [-D,D]. Every face has distinct vertex indices. For each directed edge V to W and each other vertex Z of its face,

\[
\det(W-V,Z-V)>0.
\]

Therefore the listed cycle is the positively oriented boundary of a strictly convex, positive-area polygon, contained in the square. Using every other vertex rather than merely successive turns also excludes a self-crossing cycle. The minimum positive determinant among these tests is

    1047226246554168952791.

### Pairwise disjoint interiors

For each of the 100*99/2 = 4950 unordered pairs of faces, a directed edge V to W of one face was found with

\[
\det(W-V,Z-V)\leq 0
\]

for every vertex Z of the other face. The first face's interior is in the strictly positive half-plane, whereas the other face is in the nonpositive half-plane. Their interiors are disjoint. `pair_separation_witnesses.json` records the corresponding supporting face and directed edge for all 4950 pairs.

### Exact coverage

Summing the doubled shoelace areas gives exactly

\[
\sum_i\sum_{j\text{ cyclic in face }i}\det(V_j,V_{j+1})
=8000000000000000000000000=8D^2.
\]

Hence the sum of the actual cell areas is 4. The cells lie in [-1,1]^2 and have pairwise disjoint interiors, so their union has the square's area. This finite union is closed. If any point of the square were omitted, a relatively open neighborhood in the square would also be omitted and would have positive planar area, even if the point lay at an edge or corner. This contradicts equality of areas. The cells therefore cover the entire square.

As redundant combinatorial checks, there are 276 interior undirected edges, each occurring twice with opposite orientations, and 24 boundary edges on the square. Every directed edge occurs once. The planar Euler identity is 201-300+100=1.

### Inscribed disks

For every directed edge V to W of cell i, write E=W-V and T=det(E,A_i-V). The certificate satisfies

\[
T>0,\qquad T^2-q_i^2\lVert E\rVert^2>0.
\]

Thus A_i/D is on the interior side of every supporting line and has distance strictly exceeding q_i/D from each such line. The disk of center A_i/D and radius rho_i=q_i/D is contained in their intersection, which is the cell. Its true inradius satisfies r_i>=rho_i>0.

All 576 inscribed-disk inequalities are strict. Their minimum squared integer slack is

    25059339088594949021238019471065531.

The least indisk radius numerator is 41861305589, so every cell has a positive witness radius.

### Enclosing disks

Put g=648023 and h=500000. For every vertex V of cell i,

\[
g^2q_i^2-h^2\lVert V-B_i\rVert^2>0.
\]

Hence every cell vertex lies strictly within the disk of center B_i/D and radius U rho_i. Its convexity implies that the disk contains the whole polygon. There are finitely many vertices, so the true circumradius satisfies

\[
R_i\leq\max_{V\text{ in cell }i}\lVert V/D-B_i/D\rVert<U\rho_i.
\]

All 576 inequalities are strict, with minimum integer slack

    1015689497729169821880099209.

Consequently

\[
\frac{R_i}{r_i}\leq\frac{\max_V\lVert V/D-B_i/D\rVert}{\rho_i}<U=1.296046
\]

for every cell. This proves the theorem.

## Discovery versus proof

The new mesh was obtained by the stated octagon splits and a symmetry-constrained nonlinear optimization over shared mesh coordinates and independent incenter, enclosing-center and radius witnesses. There are 46 independent mesh coordinates and 15 face orbits. The numerical candidate objective was approximately 1.2960451024464796. It is discovery evidence only.

Shared vertices and centers were rounded consistently to denominator 10^12, and each indisk radius numerator was reduced by 100 units beyond flooring. Exact certification then proved the rational bound 1.296046. The diagnostic maximum of the resulting witness ratios is approximately 1.2960451055724806; it is not the stated exact bound and is not used in the proof.

A pre-existing independently implemented certificate checker was also replayed on this new input, without importing the producer's optimization, rounding or checking functions. It accepted the geometry and rejected 12 deliberate corruptions while accepting two benign relabeling/order changes. Normal Python, Python -O, and Python -OO produced identical reports. `INDEPENDENT_CHECKER_REPLAY.json` records that replay. A replay by the producer is not represented as a new independent human or worker audit; any later independent review must pin this changed input explicitly.

## Remaining limits

This construction gives no global lower bound, no global minimization certificate, no finite-attainment result, and no equivalence with infinite partitions. The previous lower-bound theory and non-tangent local patch are separate results and are not needed in this proof. No exhaustive literature or priority claim is made. The mathematical coordinate certificate is a complete, finite, independently checkable upper-bound witness.
