# Second independent proof reconstruction and falsification

22 October 2026. This derivation was written after reconstructing the manuscript
and developing a new checker, before reading the first whole review's derivation
or relying on its PASS. It concerns the variable-threshold problem for finite,
loopless, 2-vertex-connected undirected graphs; parallel edges are allowed in the
general language, but the hardness construction is simple. Initial circuit and
one-edge OPEN ears count. The first even ear ends the initial odd prefix.

## Exact original question and standard imports

The complete Sebo contribution on original printed2912--2915 was read from a
freshly downloaded, full-hash-authenticated OWR2014 PDF; printed2914 was rendered
and read. Question4 asks the complexity of computing beta. The actual
Benchetrit--Sebo2015v1 definitions on physical/printed6 specify distinct endpoints,
open ears, the initial circuit as an ear and total ear count m-n+1. Its
Theorem3.2/Question3.3 on13, also rendered/read, identifies the factor-critical
formulation and asks polynomial computability. Section3.2 on14 separates total
odd ears from this initial-prefix objective. This is precisely the manuscript's
question; no assumed P!=NP or fixed-threshold hardness enters its conclusion.

The all-odd OPEN-ear characterization of 2-connected factor-critical graphs is
the explicitly cited classical Lovasz theorem, authenticated in B--S3.2. I did
not retrieve the original1972 proof. Standard explicitly encoded Set Cover
NP-completeness is the second import. Everything about the new reduction is
proved below. Neither import is presented as a novel contribution.

## Factor-critical and cone equivalences

The union of an odd prefix is 2-connected and factor-critical, by the classical
characterization. The first circuit contributes1 to m-n+1. A subsequent open
path of length ell contributes ell edges and ell-1 new vertices, again1;
this includes ell=1. Thus a prefix of q ears gives a factor-critical subgraph
of cyclomatic number q.

Conversely, an eligible subgraph H has an all-odd open decomposition. For any
component C of G-V(H), connectivity gives an old neighbor. If that neighbor
were unique, removing it would disconnect C from the other vertices of H,
contrary to 2-connectivity of G. Two distinct neighbors and a path within C
therefore give an open ear. Repeating includes every vertex, after which each
remaining edge is a one-edge ear. Intermediate unions remain 2-connected.
Hence this decomposition extends to the whole edge set. Adding any missing
induced edges to H preserves all existing deletion matchings and connectivity
and increases m-n+1. The maximum may therefore be taken over induced H.

For connected bipartite B with at least2 vertices, G=z*B is 2-connected: deleting
z leaves B and deleting any other vertex leaves the universal apex. An odd
bipartite graph of at least3 vertices cannot be factor-critical: delete a
vertex from its nonempty smaller side and the remaining side sizes differ.
Thus every eligible induced H contains z and is z*B[S]. Deleting z gives
necessary connectivity and a perfect matching of B[S]. Conversely, such a
connected nonempty perfectly matchable selection has |S|>=2. After deleting a
base vertex u, take its mate v in a perfect matching, replace uv by zv and
leave all other matching edges. Deleting z uses the original matching.
This proves factor-criticality and 2-connectivity. Its cyclomatic count is
|E(B[S])|. The target optimization is therefore ALL induced edges of a
CONNECTED perfectly matchable selection, not matching cardinality/weight.

## Reduction and every exceptional input

Set Cover explicitly lists U, all n sets, and integer budget s. If s<0 the
answer is NO, including empty U. For s>=0, empty U is YES. Nonempty U with no
sets, an uncovered element or s=0 is NO; covered U and s>=n is YES. A triangle
with threshold1 is a fixed YES, while the SAME triangle with threshold2 is a
fixed NO, since its beta is1. Both are simple cones over connected K2. C4 is
not substituted for the fixed NO, since it has no universal apex.

Remaining inputs have m,n>=1, covered U and 1<=s<n. Empty individual sets
and repeated sets remain permitted. Write T=sum_j(1+|A_j|), k=T+n+3,
M=(m+1)k^2, F=M-ks. Since s<=n, k-s>=T+3; in particular k>T, k>s,
k^2>ks+T and F>0. The graph consists of m+1 disjoint K(k,k) blocks, with
distinguished right vertex q_i, and a left connector c_j adjacent to q_0 and
q_i exactly when i belongs to A_j. There are exactly T connector edges.
Every connector meets the root block; coverage joins every element block,
so B is simple, connected and bipartite. Its cone is the required input class.

For a YES cover, delete redundant sets to obtain an inclusion-minimal J,
|J|=r<=s. Each selected set has an element not in any other selected set;
otherwise it could be deleted. Those private elements are distinct.
Keep every right vertex and every block left vertex except one in each
private-element block; retain exactly the selected connectors. Match each
connector to its distinct private q_i. The rest of each modified block is
K(k-1,k-1), and unmodified blocks have internal perfect matchings. This
is an explicit disjoint perfect matching, not an inference from balance.
The induced selection is connected because J covers U and every connector
meets q_0. It has M-kr+sum_(j in J)(1+|A_j|)>=F induced edges.

## Converse with arbitrary partial blocks

Take ANY connected perfectly matchable B[S] with at least F induced edges.
Let r count chosen connectors and a_i,b_i count omitted left/right vertices
of block i. If a block has no internal edge, at most M-k^2 internal edges
remain. Even allowing ALL T connector edges gives M-k^2+T<F. Consequently
each block, including the root, has a selected internal edge. No assumption
that q_i is retained, that all blocks are whole, or that a matching has a
particular normal form is used in this argument.

Global matching balance forces sum_i(a_i-b_i)=r. Internal-edge loss is
d_i=k(a_i+b_i)-a_i*b_i, with the exact identity

    d_i-k(a_i-b_i)=b_i*(2*k-a_i)>=0,  0<=a_i,b_i<=k.

Hence total induced edges <=M-kr+T. Comparing to M-ks gives
k(r-s)<=T<k, so integer r<=s. For each element block, connectivity to the
distinct root block must leave it through a selected connector. Such an
edge exists only for a selected set containing that element. The chosen
r sets cover U. This proves the full converse even when distinguished
vertices are omitted or blocks are retained only partially.

For explicit source length L, m,n,T,k=O(L). There are O(L^2) actual vertices
and O(L^3) actual edges; writing endpoint labels and binary F has polynomial
bit length. No implicit multiplicities or weighted/succinct graph are hidden.
For positive threshold, an NP certificate gives H, connectivity after every
vertex deletion and one perfect matching of H-v for every v. The certificate
and checks are polynomial; its cyclomatic value is checked against t. For
t<=0 valid inputs are immediately YES, and invalid graph encodings can be
rejected in polynomial time. The language is NP-complete.

## Independent computations and falsifiable boundaries

The new independent_hall_tutte.py imports no claimant/preparer/first-review
checker. It compares cone objectives found by augmenting-path matchings and
literal BFS components to factor-criticality tested by the Tutte odd-component
criterion: for every nonempty deletion D, odd_components(H-D)<=|D|-1.
Hall-neighbor subset inequalities independently challenge the bipartite matcher.
Complete-ear searches use a catalog of every simple path/circuit from vertex
permutations (small graphs), or from every actual edge subset (H3), and dynamic
programming over unused edges and the active first-even flag. Complete edge
partitions are emitted as witnesses.

There are26 cone/Tutte comparisons,674 Hall/augment comparisons,104 explicit
set systems,580 preprocessing decisions,124 actual-k gap/size checks,
110 actual-k forward witnesses and93664 exact partial-loss identities.
For the connectivity example, literal physical-subset enumeration examines
all16383 nonempty subsets at k2 and all1048575 nonempty subsets at k3.
At k3,167959 subsets are balanced,29999 perfectly matchable and137960
balanced but unmatchable. It independently finds connected optimum25 and
unrestricted optimum27; the complete search uses no twin-orbit compression.
At k2 connected optimum12 exceeds the false-cover threshold10 for budget1,
so the paper's larger k inequalities are essential. H3's complete edge-subset
catalog gives beta2 and maximum total odd4 with actual complete decompositions.

Eight deliberate false controls challenge omitted initial-circuit/one-edge
counts, balance-as-matching, a stronger false loss bound, closed-ear conventions
(the friendship graph is factor-critical but not2-vertex-connected), dropped
connectivity, too-small k and ignoring the first even ear. All reject.
Normal/-O/-OO outputs are byte-identical. These finite computations can expose
errors but do not prove the universal reduction or certify priority. The proof
above and cited standard inputs carry the unrestricted mathematical claim.

No substantive mathematical defect was identified. Publication priority,
metadata, visual presentation, archive reconstruction and custody are separately
recorded; a PASS is not service-action authority or formal human peer review.
