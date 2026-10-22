# Independent original-scope, correctness and priority audit: PR1372 / 30002726

Pinned head `d34aba3697196aff2e4fc06e29f71afb5d793499`;15actual paths. Audit date22October2026. This is an independent machine-assisted mathematical audit, not human peer review or formal verification. Earlier closed audit folders remain immutable.

## Disposition

The main cone/Set Cover reduction survives independent derivation and adversarial checks. It proves the full stated variable-threshold decision result: deciding β(G)>=t is NP-complete, even for simple2-vertex-connected graphs with a universal vertex whose deletion leaves a connected bipartite graph. β is the number of **initial consecutive odd ears in an open ear-decomposition**, with the initial circuit and one-edge ears counted. The first even ear ends the counted prefix.

One small preprocessing output should be repaired for a literal reduction whose every output stays in that restricted graph class: the manuscript's suggested fixed NO instance C4 has no universal vertex. Replace it with a triangle at threshold2; a triangle at threshold1 remains a fixed YES instance. Both are cones over K2 and satisfy the claimed restricted hypotheses. The hard nontrivial Set Cover construction itself has no identified gap. This repair requires no new mechanism and does not weaken the theorem.

The result is a full complexity classification of the requested decision problem, and an NP-hardness answer to the original request to compute β. It does not prove P≠NP, fixed-threshold hardness, total-odd-ear hardness, closed-ear hardness, or arbitrary-matroid hardness.

No authenticated earlier publication proving this entire β result was found. Priority and novelty remain unestablished; no `already_solved` row is proposed. In particular, neither the original-question DOI nor a dependency/related-matching DOI is a full-answer publication of the new reduction.

## Fresh duplicate checks and original target

Before substantive mathematics, a fresh read-only GWS CLI read at13:42:19.782084UTC checked numeric sheet1254632077, all43columns,191rows. It found no exact or semantic target hit. Response SHA-256 `446ba179ebbb49bee9cf4cf5619a09b1ea2e41fdb5c8ce2431ec44b5e8d86371`. Local publication policy/catalog/assessment/queue checks found only the original question, not a solution DOI. Public exact-ID/source-key/title/DOI searches were also started before proof analysis. Receipts are in GWS_DUPLICATE_CHECK.json and LOCAL_PUBLICATION_DEDUP.json.

The original is András Sebő's contribution “Problems about uniform covers, with tours and detours,” printed2912–2915 in OWR2014/51. Printed2914, Question4 asks for the complexity of β, described there as the maximum starting odd-ear sequence. The adjacent text expressly invokes open ears and2-vertex-connectivity. That page was read in a fresh primary PDF and visually rendered; the entire contribution and references were read. [Original report](https://ems.press/content/serial-article-files/46541).

The subsequent joint Benchetrit–Sebő paper gives the precise conventions in §1.1: finite undirected loopless graphs, parallel edges permitted;2-connectivity means vertex connectivity with at least3vertices; ears are open, the initial circuit counts, and the ear number is |E|-|V|+1. Proposition1.13 permits extension of a subgraph's decomposition. Theorem3.2 states the2-connected factor-critical/all-odd-ear characterization, and §3.1 explicitly equates the maximum initial odd prefix with the maximum ear number of such a subgraph. Its Question3.3 is the polynomial-computability question. [Actual primary paper](https://arxiv.org/pdf/1509.05586v1).

The preprint's ear-definition sentence contains an evident ambient-graph letter slip; the intended incidence and fresh-edge convention is fixed by its open qualifier, ear-number identity, extension proposition and the author's explicit2016 exposition. Repeating an already used edge is not a different legitimate reading: it contradicts the asserted fixed ear count. The author's exposition also explicitly excludes attachment at a single vertex. [Benchetrit's primary exposition](https://matroidunion.org/?p=1769). No satellite-only, spanning-subgraph or total-ear condition is being added.

## Independent structural derivation

An all-odd open prefix has a2-connected union H. Its first odd circuit is factor-critical. Adding an odd path with2r internal vertices preserves factor-criticality: if an old vertex is deleted, use its near-perfect matching in the old H and match the new internal path vertices in consecutive pairs. If an internal vertex is deleted, match the two resulting path pieces in alternating pairs, allocating one old endpoint to the path and using a near-perfect matching of H omitting that endpoint. The parity of the deleted internal index chooses the endpoint. This proves directly the needed forward structural implication.

Every ear, including the initial circuit, contributes one to |E(H)|-|V(H)|+1. Conversely the established Lovász theorem as stated in Benchetrit–Sebő Theorem3.2 supplies an all-odd open decomposition of every2-connected factor-critical H. Its original1972proof was not recovered here; this classical structural theorem is an explicit established import, not a new unsupported algorithmic assumption.

For completeness, extension to a2-connected G is elementary. If H is not spanning, each component of G-V(H) has at least two distinct neighbors in H, or its unique neighbor would be a cut vertex. A path through such a component between two distinct old neighbors is a new open ear. Repeating grows the vertex set; remaining unused edges are one-edge ears. This extends the original prefix, regardless of the later ear parities. It also explains why one-edge ears must be allowed. Thus

    β(G) = max_H ( |E(H)|-|V(H)|+1 ),

where H is2-connected and factor-critical, with zero for the empty candidate family. The backward implication is exactly the classical import, and is not a claim that all factor-critical graphs admit an open decomposition without2-connectivity.

For a fixed vertex set, adding the missing induced edges preserves every supplied vertex-deletion matching and2-connectivity, and increases the objective. Hence the maximum can be taken over induced H. This monotonicity is about adding edges on an existing vertex set; it does not assert that adding arbitrary vertices preserves factor-criticality.

Now let B be connected bipartite with at least2vertices and let G=z*B be its simple cone. No2-connected factor-critical H can lie wholly in B. Indeed factor-critical order is odd; in a connected odd-order bipartite graph, deleting a vertex from its smaller nonempty class leaves unequal class sizes, precluding a perfect matching. Every eligible H therefore contains z, and the induced completion is z*B[S].

For nonempty perfectly matchable S, |S| is even and at least2. The cone z*B[S] is2-connected exactly when B[S] is connected: deleting z is the necessity; deleting any other vertex leaves connectivity through z. It is factor-critical exactly when B[S] has a perfect matching M. Necessity is deletion of z. For deletion of u∈S, remove its M-edge uv and match v to z instead; deletion of z uses M itself. Finally

    |E(z*B[S])|-|V(z*B[S])|+1 = |E(B[S])|.

Therefore

    β(z*B) = max {|E(B[S])| : S≠∅, B[S] connected and perfectly matchable}.

The nonempty restriction excludes the empty matching convention. Connected B has an edge, so this maximum exists and is at least1. All graphs produced by the reduction satisfy these exact hypotheses.

## Independent verification of the hard reduction

Use explicit finite Set Cover data U={1,...,m}, A1,...,An and budget s, after trivial-case preprocessing so that m,n>=1,1<=s<=n and the union is U. Karp's original completeness theorem, Set Covering definition and Node Cover→Set Covering map were read in a facsimile reprint, with original printed94 and98 visually inspected. [Primary paper facsimile](https://www.cs.umd.edu/~gasarch/BLOGPAPERS/Karp.pdf). This is the standard established NP-completeness import, not a theorem about the new ear objective.

Empty U, absent sets, uncovered elements, zero/negative budgets and oversized budgets are decidable immediately. The fixed outputs above keep **all** branches inside the claimed simple cone class. Empty and duplicate members of an otherwise nontrivial family remain allowed.

Set

    T = Σ_j(1+|A_j|),    k=T+n+3,
    M=(m+1)k²,           F=M-ks.

Then k>T, k>s and k²>ks+T, since k-s>=T+3. Also F>0. Here k is a block-size parameter, not a fixed decision threshold.

Take m+1 disjoint K_(k,k) blocks Q0,...,Qm. In each choose a distinguished right vertex q_i. Add one left connector c_j for every set, adjacent to q0 and q_i for i∈A_j. There are no other interblock edges. The resulting B is simple, bipartite and connected: every connector meets q0; every element block has an incident connector because the union is U. It has exactly2k(m+1)+n vertices and M+T edges. Output its simple cone G and threshold F.

### Forward direction, including the matching obligation

From a cover of size<=s remove redundant sets to obtain an inclusion-minimal cover J, |J|=r<=s. Every selected set has a private element; otherwise its deletion preserves coverage. Private elements of two selected sets cannot coincide, because each is absent from every other selected set.

Select all block vertices and the r chosen connectors, omitting one left vertex in each private-element block. Match each connector to the distinguished right vertex of its private block. In that block the remaining internal vertices form K_(k-1,k-1), and all other blocks match internally. This is an explicit perfect matching, not merely a bipartition balance argument.

Each retained block remains connected because k>=2; all selected connectors meet the root, and coverage links every element block to some connector. Thus B[S] is connected. Exactly r distinct left omissions lose kr block edges, while all right vertices and chosen connector incidences remain. Its edge number is

    M-kr+Σ_(j∈J)(1+|A_j|) >= M-ks=F.

The cone identity proves β(G)>=F. Redundant or empty original sets create no exception, since the chosen cover was made inclusion-minimal.

### Converse, including arbitrary partial blocks

Suppose connected perfectly matchable B[S] has at least F edges. Let r be its number of selected connectors. Write a_i,b_i for omitted left/right vertices of Q_i. This covers every possible S, including omissions of distinguished right vertices and entire blocks.

If a block retained no internal edge, total edges would be at most M-k²+T<F. Thus each block, including the root, retains an internal edge. No unproved claim that blocks are selected whole is used.

A perfect matching forces equal selected left/right cardinalities:

    Σ_i(a_i-b_i)=r.

The internal edge loss of block i is d_i=k(a_i+b_i)-a_i b_i. Its exact identity

    d_i-k(a_i-b_i)=b_i(2k-a_i)>=0

holds even for arbitrary omissions on both sides. Summing yields Σd_i>=kr. Since all connector edges together number only T,

    F <= |E(B[S])| <= M-kr+T,
    k(r-s)<=T<k.

Integer r,s therefore satisfy r<=s. Finally every element block has selected vertices joined by an internal edge and is distinct from the retained root block. Connectivity forces a path out of it; its only external edges go from q_i to selected connectors c_j with i∈A_j. Hence at least one chosen set contains each element i. These r sets cover U within the budget.

This proves the exact many-one equivalence. The converse explicitly allows partial blocks; the inequality is not a heuristic that “large blocks must be nearly full.”

## Encoding and NP verification

Let L be the ordinary explicit Set Cover encoding length. After covering-union preprocessing, m is at most the number of incidences; n and T are O(L), so k=O(L). The output has O(L²) vertices and O(L³) explicitly listed edges. F has polynomial bit length (indeed logarithmic in that polynomial bound). Renumbering element labels is polynomial. No binary-encoded enormous multiplicity, weight, parallel bundle, implicit graph or fixed-threshold assumption is used.

An NP certificate consists of a subgraph H plus a perfect matching in H-v for each v∈V(H). A verifier checks H⊆G, at least3vertices, connectivity after each vertex deletion, the supplied disjoint matching edges covering every remaining vertex, and |E(H)|-|V(H)|+1>=t. Certificate length is polynomial. Threshold t<=0 is trivial; a very large binary threshold can be compared with the graph's ear count in polynomial time. The theorem therefore applies to the loopless multigraph class as well, with NP-hardness already on the simple subclass.

## Independent finite controls

The audit-authored exact checker imports no author program and uses integers, exhaustive subsets, perfect-matching recursion and a direct complete-ear-decomposition dynamic program. Its ear search records the first-even cutoff and all unused one-edge ears. Thus it compares the **original objective**, rather than only rechecking the factor-critical reformulation against itself.

The saved results contain32 connected bipartite bases/cones where direct complete-ear β, induced factor-critical optimization and the cone expression agree. The K2,2 cone has β=4; an otherwise identical mutant that does not count one-edge ears yields2. There are436 covered set systems and1270 threshold decisions, seven full induced-subset guards allowing arbitrary partial blocks, six explicit full-actual-k private-element matching witnesses, and5524 exact omission-identity checks. The block normal-form optimizer used for larger finite guards is separately compared with actual full induced-subset enumeration on the seven small constructions; its results are not the universal hardness proof.

Normal,-O,-OO runs produce byte-identical SHA-256 `01a86031cafb92f486f66b5584b2d4ea150c32964e1c5e4b3c39b5a203cf7686`. All checks use explicit exceptions. These controls are finite debugging evidence, not a claim of formal verification or a substitute for the derivation above.

## Priority audit and exact remaining uncertainty

Besides the original and Benchetrit–Sebő partial results, actual primary bodies were inspected for the2019 constrained-ear paper, the2026 joins/matroid paper, and two independently discovered alternative matching formulations. They do not establish the full target:

- Havet–Nisse use closed-cycle attachments as well as open ears and study prescribed/forbidden lengths or all-even ears; those hardness results do not maximize an initial odd open prefix. [Primary paper](https://dmtcs.episciences.org/articles/5626/download).
- Bai–Bérczi–Nalam2026 define a maximum join and minimum total even-lobe parameter. Their cographic/sparse-paving hardness is for that join parameter, not graph β. The definitions, relevant hardness statements and conclusion were read in the actual body. [Primary paper](https://arxiv.org/pdf/2608.01059v1).
- Sharifov2010, DOI10.1051/ro/2010004, actually optimizes the weight of all induced edges in a perfectly matchable bipartite subgraph, but does **not** require the selected subgraph to be connected. The problem definition and §4 algorithm/proof were inspected. This omission matters even when input B is connected: take three K3,3 blocks and two singleton-element connectors. All block vertices alone attain27 induced edges with a perfect matching, in three components. Any selected connector loses at least3 block edges and adds at most2, so27 is the unconstrained optimum. Connected optimum is25: retaining all three blocks needs both connectors, and the balanced matching construction attains27-6+4; omitting a block cannot reach25. [Actual published body](https://www.numdam.org/item/RO_2010__44_1_27_0.pdf).
- Gomes et al., arXiv2202.04746v1, prove hardness of weighted connected matchings, including nonnegative binary weights on bipartite graphs. I read the actual §3.1 construction and both reduction lemmas. Their objective is the sum of weights of **matching edges**, rather than all edges induced by the matching's endpoints. On a square, two perfect matchings of the same vertex set can have weights1 and0 while their induced edge count is4 in both cases. Thus this is substantial related prior hardness, not an identity with the cone objective. A publisher DOI lead10.1016/j.tcs.2025.115149 returned403; no claim of reading that journal body is made. [Inspected primary preprint](https://arxiv.org/pdf/2202.04746).

No searched primary source supplies the missing full prior theorem or an already-published bridge to exactly β. Finding a related NP-hard matching objective is not sufficient to assign its DOI as a publication of this new ear reduction. Conversely these bounded failures to locate a prior result do not establish novelty. The strongest verified mathematical result is the full variable-threshold NP-completeness theorem with the routine fixed-NO preprocessing replacement. The remaining material uncertainty is literature priority, with classical structural imports and access limits explicitly recorded. There is no unresolved central mathematical claim in the main reduction identified by this audit.

No service/ledger/PR/publication/Git/index/ref/STATE mutation, outside contact, other-agent coordination or author-code execution occurred. Assigned audit completion100%; parent sweep80%.
