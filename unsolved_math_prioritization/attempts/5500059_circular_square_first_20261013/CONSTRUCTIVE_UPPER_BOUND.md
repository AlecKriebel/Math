# A rational 92-piece partition with circularity below 1.298322

Problem: Most Circular Partition of a Square, AMR-054-0059 / 5500059.
Date: 2026-10-13.

## Result and scope

There is a finite partition of the square into 92 positive-area closed convex polygons such that every piece has smallest-enclosing-circle radius divided by largest-inscribed-disk radius strictly less than

\[
G=\frac{649161}{500000}=1.298322.
\]

Consequently the infimum of the maximum circularity over all finite convex polygonal partitions is at most 1.298322. This is an explicit feasible upper bound. It neither identifies the optimum nor proves that an optimum is attained by a finite partition. It does not establish equivalence with any infinite-partition formulation.

The construction uses the combinatorial layout of Figure 16 of Damian and O'Rourke, *Partitioning Regular Polygons into Circular Pieces I: Convex Partitions*, arXiv:cs/0304023v2 (2026-02-08), with newly optimized rational vertex coordinates and independently chosen rational disk witnesses. The paper reports 1.29950; the present certified value is smaller by 0.001178. No claim is made here about priority relative to all other literature.

Primary source: https://arxiv.org/abs/cs/0304023v2

The producer's exact checks establish the certificate below. A separately implemented independent checker accepted the frozen coordinate certificate, all 4,186 pair separations, exact area, and all 528 inscribed-disk and 528 enclosing-disk inequalities. Its report is [the exact independent audit](EXACT_CONSTRUCTION_AUDIT.json). The independent checker also rejected 12 adversarial certificate mutations and accepted two benign permutations. This acceptance concerns the explicit upper-bound construction; it does not certify global optimality or literature priority.

## Complete explicit specification

The accompanying `rational_partition_certificate.json` is the full mathematical coordinate certificate. It is data, not an optimization program. Its SHA-256 is

`7be877a90bf7c08e7c872f461fb4f005d8d47d6d58d888363384df2865941b47`.

Use the common denominator

\[
D=10^{12}.
\]

The square is \(S=[-1,1]^2\). The file lists 185 integer vertex pairs \(V_j\). Vertex \(j\) is exactly \(V_j/D\); the vertex numbers and face numbers start at zero. Each of the 92 lists in `faces_counterclockwise` specifies one polygon by its vertices in counterclockwise order. These lists, with the coordinates, specify the entire partition, including the interior.

For face \(i\), `disk_witnesses[i]` supplies integer pairs \(A_i,B_i\) and a positive integer \(q_i\):

- an inscribed disk with center \(a_i=A_i/D\) and radius \(\rho_i=q_i/D\);
- an enclosing disk with center \(b_i=B_i/D\) and radius \(G\rho_i\).

The two centers are independent. Neither disk is asserted to be extremal, and no assumption of concentric disks or tangency between disks is imposed. All vertices, centers, and inscribed radii are rational. The enclosing radius is rational as well.

The optional `partition.svg` visualizes these exact coordinates. Only the coordinate certificate and the inequalities below are needed for the proof.

## Exact verification conditions

For integer vectors, write \(\det(u,v)=u_xv_y-u_yv_x\). For each directed polygon edge \(V\to W\), set \(E=W-V\).

### 1. Strict convexity and containment

Every vertex coordinate belongs to \([-D,D]\). For every face, every directed edge, and every other vertex \(U\) of that face,

\[
\det(E,U-V)>0.
\]

The vertices are distinct. Thus each listed face is exactly the boundary cycle of a strictly convex polygon, with positive area, contained in \(S\). Checking all other vertices, rather than only successive turns, also rules out self-crossing polygonal cycles.

The minimum positive determinant in all these checks is

\[
1069972290622653778920.
\]

### 2. Pairwise disjoint interiors

For each of the \(\binom{92}{2}=4186\) unordered pairs of faces, one directed edge \(V\to W\) of one face has every vertex \(U\) of the other face in its closed exterior half-plane:

\[
\det(W-V,U-V)\le0.
\]

The first face lies in the opposite closed half-plane, and its interior is in the strictly positive half-plane. Hence the two interiors are disjoint. `pair_separation_witnesses.json` records a separating directed edge for each pair, so this part is also a finite, explicit integer certificate.

### 3. Exact coverage of the whole square

The sum of the signed doubled polygon areas, computed directly from the listed cyclic coordinates, is

\[
\sum_i\sum_{j\text{ cyclic in face }i}\det(V_j,V_{j+1})
 =8000000000000000000000000=8D^2.
\]

After division by \(2D^2\), the sum of polygon areas is exactly 4, the area of \(S\). Containment and pairwise disjoint interiors therefore imply that the union has area 4. The union of finitely many closed polygons is closed. If a point of \(S\) were missing, its positive-distance neighborhood relative to \(S\) would contain positive area outside the union, contradicting the area equality. This includes boundary and corner points. Thus the polygons cover all of \(S\).

As a redundant combinatorial check, there are 252 interior undirected edges, each occurring twice in opposite directions, and 24 exterior edges on the square's boundary; no edge has another multiplicity. The planar Euler identity is \(185-276+92=1\).

### 4. Inscribed-disk certificates

For every face \(i\) and every directed edge \(V\to W\), the certificate satisfies

\[
T=\det(W-V,A_i-V)>0,
\qquad
T^2-q_i^2\lVert W-V\rVert^2>0.
\]

These are integer inequalities. They imply that the perpendicular distance from \(a_i\) to every supporting edge line exceeds \(\rho_i\), with the center on the interior side. The disk \(\overline B(a_i,\rho_i)\) is therefore contained in the convex polygon. In particular its true inradius \(r(P_i)\) satisfies \(r(P_i)\ge\rho_i>0\).

The minimum value of the squared integer slack over all faces and edges is

\[
21267508483484519258859509868261049>0.
\]

The smallest inscribed-radius numerator is \(38898884896\), so there are no zero-area or vanishing-radius pieces.

### 5. Enclosing-disk certificates

Put \(g=649161\) and \(h=500000\). For every vertex \(V\) of face \(i\), the certificate satisfies

\[
g^2q_i^2-h^2\lVert V-B_i\rVert^2>0.
\]

Thus every vertex lies strictly inside the disk of center \(b_i\) and radius \(G\rho_i\). A disk is convex, so it contains the convex hull of those vertices, namely the entire polygon. Since there are finitely many vertices, its smallest enclosing radius obeys

\[
R(P_i)\le \max_{V\text{ in }i}\lVert V/D-b_i\rVert<G\rho_i.
\]

The minimum integer slack in the displayed inequality is

\[
804622615113166660805053316>0.
\]

It follows without computing either extremal circle that

\[
\frac{R(P_i)}{r(P_i)}
\le\frac{\max_V\lVert V/D-b_i\rVert}{\rho_i}
<G=1.298322.
\]

This proves the stated finite-partition upper bound.

## Audit and numerical provenance

The geometry was obtained by extracting the planar graph of Figure 16, merging two 0.001-point duplicate drawing coordinates, imposing the square's dihedral symmetry, and optimizing 42 mesh variables together with independent inscribed/enclosing disk witnesses for 14 face orbits. The numerical candidate objective was approximately 1.2983212787961154. All optimization code and raw numerical output are kept separately from the mathematical certificate.

After rounding shared vertex and center coordinates consistently to denominator \(10^{12}\), the chosen inscribed-radius numerators were reduced by 100 integer units beyond flooring. The exact certificate was then checked entirely with arbitrary-precision integer arithmetic. No floating-point test establishes any of the theorem's inequalities. The numerical maximum of the witness ratios, about 1.29832128196, is diagnostic only; the proved bound is the rational value 649161/500000.

The literal vector illustration in the PDF is too coarsened to certify the paper's claimed decimal by itself. Its two duplicate-coordinate discrepancies and the differences between its drawn piece ratios and its labels are reconstruction cautions, not a disproof of the authors' underlying construction. Figure 25 in the paper is only a boundary cover at 1.29650; it is not used here as a full partition. The tangent-indisk conjecture and any source lower bounds are not used in this construction or proof.

## What remains open

The exact optimum, finite attainment, and the relationship between finite and arbitrary infinite partitions remain unresolved by this result. The constructed 92-piece partition is a feasible point, not a global minimizer. Historical substantive attempt counts are not determined by this packet.
