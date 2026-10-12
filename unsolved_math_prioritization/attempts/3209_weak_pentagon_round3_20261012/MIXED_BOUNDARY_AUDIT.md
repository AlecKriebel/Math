> Editorial scope: This is the complete authored text of the accepted third-round source document, with operational identities and reproduction directions editorially removed or relabeled. Mathematical arguments and finite-scope counts are preserved. References to candidate status, packet contents, or narrower review scope record the original stage; the final combined decision is in [ACCEPTANCE_REPORT.md](ACCEPTANCE_REPORT.md). This public edition contains prose and public verification metadata only. It contains no programs, raw certificates, dataset contents, source documents, or runnable bundle. Original and distributed identities are different; [PUBLIC_MANIFEST.json](PUBLIC_MANIFEST.json) identifies only the files actually distributed.

# Independent acceptance audit: mixed prescribed Clebsch classes

12 October 2026 UTC. Problem 3209, queue row 1752. This is a proof-level audit of the third-continuation mixed-cut packet, not a new claim about the unrestricted Weak pentagon conjecture.

## 1. Verdict, identity, and limits

**ACCEPT, with the external mathematical dependency expressly retained. No mathematical correction to the pinned candidate is required.**

The accepted input is the complete original mathematical report. Its exact input and externally pinned manifest identities are retained outside this edition; they do not identify the editorially transformed public files. The closed input inventory is exactly twelve payload files plus that manifest. Every member’s byte count and digest was checked; all were unchanged at the end. The retained original identity record covers all twelve payloads.

Accepted claims:

- The signed-list reduction and the alternative full-palette reduction are exact for any finite simple triangle-free subcubic graph whose specified cut complement is a matching with exactly one edge on the Y side.
- The specified cut extends if every boundary entity has auxiliary degree at most four. The theorem allows arbitrarily many demands on X.
- The stated 18-vertex graph has an obstructed 5+1 prescribed cut. Its 28-vertex cubic completion has an obstructed 7+1 prescribed cut. Their negative proofs are elementary and independent of the signed-list theorem.
- Both obstructed cuts admit a gain-one switch and are not globally maximum. The exact maximum cuts are 22 and 35; the numbers of normalized global maximizers are 7 and 72.
- All four supplied maps pass direct verification: an unrestricted Clebsch homomorphism and a maximum-cut-prescribed homomorphism for each graph.

Not accepted or inferred: a disproof of the Weak pentagon conjecture; a disproof of the global-maximum-cut strengthening; a universal 4+1 theorem; novelty; comprehensive literature status; any claim from the separate tester's 1+4 lemma. That separate lemma was not used or treated as a premise. No UNSAT conclusion rests on a timeout, solver status, or sampled search.

No candidate input was edited and no publication was performed. Source PDFs, source text, and source-page images were not copied into this audit package.

## 2. External dependency review

The positive theorem uses Thomas Schweser and Michael Stiebitz, [Degree choosable signed graphs, arXiv:1507.04569v1](https://arxiv.org/abs/1507.04569v1), specifically Theorem 2.1(a),(c),(e) and Lemma 2.4, with v1 numbering. The primary PDF has 202,056 bytes and SHA-256 `727b9d254300f36b91c7ff2e02e1538c259ff0075316da2dfffb454ee2da960e`; these bytes were rechecked. The primary abstract page was independently opened, and the local primary text covering graph/list conventions, the required theorem statements, and block-list decomposition (pp. 2–8 and 13–14) was reread. The separate complete-source dependency audit was read in full and pinned; the original report and manifest identities are retained outside this edition.

The external contract is that a connected uncolorable signed degree-list pair has exact list sizes equal to degrees and brick blocks; each block receives an uncolorable block-list assignment whose incident lists unite to the original lists. Across an edge of an uncolorable block, the endpoint lists agree after multiplication by its sign. Graphs are loopless multigraphs, degrees count multiplicity, and lists need not be symmetric. The brick types are balanced complete graphs, balanced odd cycles, unbalanced even cycles, doubled complete graphs, and doubled odd cycles.

This audit checks the application below; it does not independently reprove that source theorem. Source Lemma 2.2 is not a premise. The original list at a cut vertex is never assumed to be its entire block list. Journal publication metadata do not substitute for the inspected v1 locators, and no journal full-text inspection is claimed here.

## 3. Exact reductions: complete scope and orientation checks

Let G be finite, simple, triangle-free and subcubic, with specified cut (X,Y), cut edges B, and matching complement M. The only M-edge within Y is rs. Put J=1111 in F₂⁴. A prescribed extension uses unit-vector differences on B and difference J on every M-edge.

### Cube lemma

For at most three same-parity cube vertices, allowing repetitions, a common opposite-parity cube neighbor exists exactly when no two are antipodal. Necessity follows because two antipodes have disjoint cube neighborhoods. For sufficiency, translate one chosen vertex to zero. Every other distinct allowed vertex has weight two; two such supports intersect unless they are complements. Choose a coordinate in their intersection, or any coordinate of the sole weight-two support, or any coordinate when all vertices coincide. The corresponding unit vector is a common neighbor. An empty set has any cube vertex as a common neighbor. This proof uses the upper bound three, never a false four-vertex version.

Fix an odd h. Its four neighbors contain exactly one representative of each of the four even antipodal pairs. Choose a bijection θ from C={±1,±2,±3,±4} to the eight even vertices with θ(-a)=θ(a)+J and θ(D)=N(h), where D={1,2,3,4}.

### Entities and ordinary constraints

Each X-demand is contracted to an entity; every unmatched X-vertex is a singleton entity. Choose endpoint signs ε_x opposite on each demand and +1 on singletons. A color c_P represents f(x)=θ(ε_x c_P).

For each ordinary y in Y\{r,s}, any two neighbors x,z impose a signed edge with sign -ε_xε_z, interpreted as c_P≠σc_Q. Indeed, equality in the forbidden condition is precisely θ(ε_xc_P)=θ(ε_zc_Q)+J. Two neighbors cannot belong to the same entity, since together with their demand edge they would form a triangle. Thus there are no loops. Repeated same-sign constraints may be deleted; both signs between an entity pair must remain, with multiplicity two in the degree.

At a degree-three ordinary y, the three distinct entities generate a triangle with sign product (-ε_xε_z)(-ε_zε_w)(-ε_wε_x)=-1. Deduplication retains the relevant signed edge for every generated constraint. This fact is used later for balance contradictions.

### Boundary lists and exactness

Let R=N_B(r), T=N_B(s). Triangle-freeness gives R∩T empty and prevents either set from containing both members of a demand. An entity meeting both sets has one endpoint in each. Thus for a boundary endpoint x, the factor a_x=t_xε_x, with t=+1 on R and -1 on T, is consistent throughout its entity. Give that entity list a_xD and every other entity list C. There are at most four boundary incidences and therefore at most four boundary entities. The four-element lists are nonempty, nonsymmetric and disjoint from their negatives.

An L-coloring maps all X vertices as above, takes r to h and s to h+J, and supplies every ordinary y independently using the cube lemma. Independence is valid because there are no other demands inside Y. Conversely, the difference between the parity of a prescribed map and the cut indicator is constant on each connected component. Translate each component to make that difference zero, even when a component has no X vertices. In the rs component, a further even translation takes f(r) to h, automatically taking f(s) to h+J. Pulling back the X labels through θ and ε produces exactly the signed inequalities and the designated lists. Disconnected components and isolated vertices create no omitted condition.

If k counts an entity's incidences with {r,s}, a singleton has auxiliary degree at most 2(3-k), and a paired entity at most 2(4-k). Each ordinary incidence produces at most two constraints and same-sign deduplication can only decrease the degree. Hence every unconstrained entity has degree at most eight, a constrained singleton at most four, and a constrained pair with two incidences at most four. Only a constrained pair with one incidence can have degree five or six against its four-color list.

### Full-palette equivalence

Add a signed edge of sign -a_xa_z between every two distinct boundary entities, retaining the ordinary constraints. Repeated roles of one entity have the same a-sign, so their condition only forbids c=-c and is vacuous because zero is absent. The resulting conditions say that the transformed roles a_xc_P contain no opposite pair.

If these conditions hold, independently exchange the names +i and -i for each magnitude i as needed to put every occurring transformed role in D. The relabeling ψ commutes with negation, so it preserves every equality or inequality c_P=σc_Q and commutes with multiplication by a_x. It yields exactly the boundary lists. This step does not require the relabeling to be a cube automorphism: the signed reduction and the at-most-three-neighbor cube lemma already encode all ordinary constraints. The reverse implication is immediate. Thus this alternative is also exact.

The full-palette graph can have degree nine at a pair with one boundary incidence (six ordinary constraints plus three boundary-role constraints). There is no unproved application of eight-color degree choosability to that graph.

## 4. Positive mixed boundary theorem

Assume every boundary entity has degree at most four in the ordinary signed graph F. Every vertex then has a list at least as large as its degree. Suppose a connected component K is uncolorable. The cited theorem forces each degree to equal its list size, so all degrees are four or eight. Every degree-four vertex is boundary; every degree-eight vertex is an unconstrained pair, since an unconstrained singleton has degree at most six. In particular K has no isolated vertex.

Decompose the uncolorable list pair into block-list pairs using Lemma 2.4. A non-cut vertex belongs to one block, so its block list is its original list. At cut vertices only the union assertion is used. In fact exact degrees and edge partition imply the incident block lists are disjoint, but the following argument does not require choosing an entire original palette at a cut vertex.

Choose an end block Q, or K itself if there is one block. A non-cut vertex has its full degree in Q. Since every brick is regular, Q has regular degree four or eight. Bridges, degree-two cycle bricks and isolated blocks are thereby excluded.

### Degree-eight end block

If Q had a cut vertex, its eight edges inside Q and at least one edge outside would contradict the maximum auxiliary degree eight. Therefore Q=K, an eight-regular brick. The only possibilities are a balanced K₉ and doubled K₅.

All represented entities are unconstrained pairs. Equality in the chain

d_F(P) ≤ sum over ordinary incidences xy of (d_B(y)-1) ≤ 8

forces four ordinary incidences at each pair, two at each represented X-vertex, with every adjacent ordinary Y-vertex of degree three and no incident same-sign deletion. Every neighbor entity of such a Y-vertex lies in K because the generated constraints connect it to the already present entity. This is the required component closure in the original cut graph.

The generated negative-product triangle excludes balanced K₉. In doubled K₅ there are exactly five paired entities, hence ten represented X-vertices with two ordinary incidences each. Every adjacent ordinary Y-vertex has all three neighbors among them. Counting the same incidence set gives 20=3|N_B(X_K)|, impossible. The count is not taken in the auxiliary multigraph.

### Degree-four end block

Every non-cut vertex P is boundary and has inherited block list D or -D. A doubled brick has a positive and a negative edge to a neighbor P′. The edgewise list clause, applied to the uncolorable block-list pair, gives L_Q(P)=L_Q(P′) and L_Q(P)=-L_Q(P′). This would make L_Q(P) symmetric. It contradicts D or -D, regardless of whether P′ is a cut vertex and regardless of its original list. This eliminates doubled K₃ and every doubled odd cycle.

The remaining degree-four brick is a balanced K₅. At a boundary pair P at most three ordinary incidences remain; at a boundary singleton at most two remain. If all these ordinary Y-neighbors had degree at most two, at most three constraints could reach P. Its auxiliary degree is four. Some ordinary Y-neighbor therefore has degree three and generates a negative-product triangle at P. Both triangle edges incident to the non-cut P lie in Q. The entire triangle lies in one block, so its closing edge lies in Q as well. An opposite-sign parallel copy cannot reside in a different block either. Thus Q contains a negative cycle, contradicting balance.

All end-block types have been excluded. Every component is L-colorable and the exact reduction supplies a prescribed extension. This proves the positive theorem assuming exactly the cited external clauses.

If every X-demand that meets R∪T has both endpoints there, it has k=2, while any boundary singleton has k=1. The required degree-four bounds follow, proving the corollary. The candidate's unbounded-demand family is feasible: chain pentagons using distinct unused degree-two vertices and cut bridges, putting the unique Y-demand in an end pentagon and avoiding its two X-neighbors. No finite bound on the number of X-demands is used in the proof.

## 5. Independent reconstruction and elementary obstruction

The 18-vertex graph H has X={0,…,9}, Y={10,…,17}, demands

(0,1), (2,3), (4,5), (6,7), (8,9), (10,11),

and cut neighborhoods

- 10: {0,2}; 11: {5,7}
- 12: {8,1,2}; 13: {8,3,4}
- 14: {9,4,7}; 15: {9,6,1}
- 16: {0,5}; 17: {3,6}

These reconstruct the candidate's JSON exactly, independently of the original graph builder: 18 vertices, 26 edges, 20 cut edges, demand distribution 5+1; vertices 16,17 have degree two and every other vertex degree three. It is connected and simple. The cut part is bipartite, no cut neighborhood contains both ends of an X-demand, and 10 and 11 have disjoint cut neighborhoods; consequently there is no triangle.

Suppose a prescribed map exists. Normalize all X labels to even parity and set A=f(0), B=f(2), C=f(4), D=f(6), E=f(8). Matching partners have the corresponding label plus J. If h=f(10), then f(11)=h+J and A,B,C,D all lie in N(h). Neighborhoods 12,13,14,15,16,17 respectively force A≠B, B≠C, C≠D, D≠A, A≠C, B≠D. For instance A=B would make the images at 1 and 2 antipodal neighbors of 12.

Thus A,B,C,D are the four distinct neighbors of h, one from each even antipodal pair. Neighborhood 12 forbids E=A and E=B+J; 13 forbids E=B and E=C+J; 14 forbids E=C and E=D+J; 15 forbids E=D and E=A+J. All eight even labels are forbidden. This is the desired contradiction. The common neighbor h of four images is supplied by the original boundary equations; it is never inferred from a false four-image cube lemma.

As a separate exact certificate, the ordinary auxiliary graph on entities A,…,E has all six positive edges among A,B,C,D, both signs between E and each of A,B,C,D, and no other edges: fourteen signed edges, degree sequence (5,5,5,5,8), lists D,D,D,D,C. The full-palette boundary operation adds the six negative edges among the first four entities, giving exactly signed doubled K₅. Both signs force all five magnitudes distinct, but the palette has only four magnitudes. This gives the same impossibility without any external graph-coloring theorem.

The 28-vertex completion K adds X vertices 18,…,23; Y vertices 24,…,27; demands (18,19),(20,21); attachments (16,22),(17,23); and cut neighborhoods

24: {18,20,22}; 25: {18,21,23}; 26: {19,20,23}; 27: {19,21,22}.

It reconstructs the candidate's JSON exactly: 28 vertices, 42 edges, 34 cut edges, demand distribution 7+1, all degrees three, connected, simple and triangle-free. H and every original cut/matching status are preserved as an induced subgraph. Any prescribed extension would restrict to the impossible one on H. The completion therefore fails the prescription while remaining cubic. Independently, its ordinary entity degrees are (6,6,6,6,8,6,6,6,6), with 28 ordinary and 34 full-palette signed edges; its first five entities retain the doubled-K₅ obstruction.

## 6. Cut scopes, exact maxima, and explicit positive maps

### Nonglobal prescribed cuts

In both graphs U={0,2,10} has demand boundary {(0,1),(2,3),(10,11)} and cut boundary {(0,16),(2,12)}. Switching U converts three uncut edges into cut edges and two cut edges into uncut edges, a net gain of one. No added completion edge meets U. Neither obstructed cut is globally maximum.

### Exact maxima and counts

An independent Gray-code enumeration of all 2¹⁷ normalized H cuts (vertex 0 fixed to color zero) gives:

- Ports 16,17 equal: maximum 21, attained 30 times.
- Ports unequal: maximum 22, attained 7 times.

An independent Cartesian-product enumeration of all 2¹⁰ new-vertex colorings for each fixed port relation gives gadget maxima 14 with count 1 for equal ports, and 13 with count 6 for unequal ports. The gadget includes both attachment edges and has sixteen edges. Complementing all colors preserves edge cut status, so either absolute color of the first port gives the same result. Old and new edge sets partition the completed graph's edges and share only the two fixed port colors. Therefore K has maximum max(21+14,22+13)=35 and exactly 30·1+7·6=72 normalized maximizers.

For an additional independent check not relying on this factorization, the audited C++ program enumerated all 134,217,728 normalized K cuts. It returned maximum 35, count 72, witness mask 16517114. The complete H run returned maximum 22, count 7, witness mask 85338. The C++ Gray recurrence was cross-checked by direct edge summation at 1,344 points of the K run, including its final state, and on five known small graphs. This is a completed exhaustive enumeration, not a solver or timeout inference. Source, graph inputs, outputs and replay driver were retained outside this public edition.

### Supplied homomorphisms

A vertex list below is indexed by the vertex number. Every edge difference was independently checked against {1,2,4,8,15}.

Unrestricted H:

(0,1,6,2,1,5,4,11,8,7,2,10,9,0,3,5,1,0).

Unrestricted K:

(0,1,6,2,1,5,4,11,8,7,2,10,9,0,3,5,1,0,6,7,10,11,0,1,2,9,5,15).

For the H cut encoded by mask 85338, of size 22, the prescribed map is:

(0,1,6,2,1,5,4,12,8,10,2,13,9,0,14,5,1,0).

For the K cut encoded by mask 16517114, of size 35, the prescribed map is:

(0,1,6,2,1,14,8,7,11,4,2,6,9,3,5,0,15,0,2,13,4,11,7,1,6,3,5,15).

In the last two checks, an edge crossing the encoded cut was required to have unit difference and every other edge difference J. These maps certify that each graph has at least one extendable maximum cut. They do not certify that every maximum cut of either graph extends, still less a universal maximum-cut theorem.

## 7. Verification and fail-closed contract

The independent mixed-graph checker never imports the candidate's code. It reconstructs the literal graphs from the proof, compares them to the pinned JSON, checks their structure and auxiliary reductions, validates all four maps and the switch, and independently computes the separated maximum-cut results. Additional exhaustive checks include:

- 1,170 same-parity cube tuples of lengths zero through three.
- 4,681 signed boundary-role tuples of lengths zero through four, including repeated and opposing roles.
- All 2,048 candidate mixed-list assignments: zero colorings.
- All 32,768 assignments on the full-palette doubled-K₅ reduction: zero colorings.
- All 32,768 assignments on the ordinary graph with all lists enlarged to C: 2,880 colorings. This illustrates why dropping the boundary lists is unsound.
- All 32 entity orientation choices, with lists and edge signs transformed together: 65,536 corresponding list assignments, none valid.

The candidate’s complete original graph verifier was rerun under normal Python, -O and -OO, each time reproducing its retained JSON byte for byte. Its sealed inventory also passed in all three modes. The candidate's deterministic graph builder was executed only in temporary copies and reproduced both graph files byte for byte.

The independent checker and full-enumeration replay each ran in all three Python modes with identical substantive outputs. The compiler uses explicit runtime checks, not assertions. The replay additionally verifies the full C++ results against retained results, verifies its input edge lists against independent construction, tests five known graph maxima, and rejects six malformed-input controls.

The independent mixed-graph rejection suite ran twenty independent rejection controls and seven upstream seal rejection controls in each Python mode. Mutations include missing and extra files/directories, appended and same-length changed payloads, changed manifests, payload and manifest symlinks, forged internally recomputed hashes against the original external pin, graph changes, inconsistent boundary orientations, invalid maps, a falsely prescribed unrestricted map, missing signed constraints, and false maximum values/counts. All mutations occurred in temporary copies or in-memory values. The original frozen input was rechecked afterward. Python assertions are not used for acceptance decisions, so -O/-OO do not disable them.

The independent inventory checker is deliberately stricter than relying on payload digests alone: it requires exactly the known twelve payload names plus the manifest, rejects symlinks including a manifest symlink, checks the external manifest digest and manifest byte count, and checks every payload digest and byte count. It does not accept a changed internal manifest as new authority.

These finite checks corroborate exactly the named constructions and finite algebraic facts. The universal positive theorem is established by its written argument plus the explicit external theorem, not by the finite tests.

## 8. Final accepted frontier

The four-boundary degree-four criterion is valid; the general one-versus-many prescribed-cut extension is false. Degree five at four boundary entities already permits the 18-vertex obstruction. The cubic completion demonstrates that restricting to cubic graphs does not rescue that unrestricted prescription. However, both prescribed cuts are nonglobal and both graphs admit unrestricted Clebsch maps and at least one extendable maximum cut. The unrestricted Weak pentagon target and the proposed universal global-maximum-cut strengthening remain unresolved by this packet. No separate 1+4 lemma is incorporated.
