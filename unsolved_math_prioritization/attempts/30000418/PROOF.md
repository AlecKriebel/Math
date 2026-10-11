# A five-list obstruction on an eleven-vertex tree

This AI-assisted manuscript is unrefereed. Acceptance records an independent internal AI audit, not external human peer review, journal acceptance, or formal proof-assistant certification.

The complete human-readable proof, explicit graph, bad lists, ordinary labeling, infinite family and logical audit are retained. This is not a computational reproduction package: raw state tables, Hall-certificate datasets, enumeration tables, executable code, copied source documents and images, and private coordination material are omitted. Historical counts and hashes are supporting metadata. The historical computations cannot be reproduced from this edition alone; all mathematical conclusions rest on the written proofs.

The stated universal tree-equality conjecture is answered negatively. No historical novelty, priority, minimal-order, exhaustive-literature-review, or current-openness claim is made.

## Result and status

For the tree T below, the ordinary L(2,1) palette-size parameter is 5 and its arbitrary-list parameter is 6:

χ^(2,1)(T) = 5 < 6 = χ_ℓ^(2,1)(T).

This is a counterexample to Conjecture 4 in Anja Kohl, “Some notes on L(d,s)-list labellings of trees and cacti,” Oberwolfach Report 7/2006, printed pp. 414–416, specifically p. 416, and the same statement as Conjecture 4.4 in Kohl's 2006 dissertation, printed p. 124. The original convention counts a common palette {1,…,k}; its ordinary parameter is the usual minimum span plus one. Thus the corresponding ordinary span is 4, while the list cardinality required is 6. All lists below are five-element subsets of the positive integers. They are not all intervals.

This edition presents the complete authored proof, accepted without mathematical correction by the accompanying independent internal AI audit. The original executable checks are described only as historical corroboration. The bounded subsequent-literature search is not a current-openness or priority certificate.

## 1. The tree and a bad five-list assignment

Start with the five-vertex path a–b–c–d–e. Attach two leaves a₁,a₂ to a, one leaf b₁ to b, one leaf d₁ to d, and two leaves e₁,e₂ to e. There are eleven vertices, ten edges, and maximum degree three. It is a finite simple connected acyclic graph; attaching leaves to a path preserves these properties.

Let A={1,2,3,4,5} and B={1,3,4,5,6}. Assign list A to a,b,c,d,e,b₁,d₁. Assign list B to a₁,a₂,e₁,e₂. Thus every vertex receives exactly five permissible labels.

An admissible labeling f must choose f(v) from its assigned list, satisfy |f(u)−f(v)|≥2 on every edge, and satisfy f(u)≠f(v) for every pair at graph distance two.

## 2. Human proof that the five-list assignment is impossible

All three neighbors of b have list A. Their labels must be pairwise different, because every pair of these neighbors is at distance two. If f(b) were 2, 3, or 4, then only two elements of A would differ from f(b) by at least two. Those three neighbors could not all receive different labels. Consequently f(b)∈{1,5}. The same argument at d gives f(d)∈{1,5}.

The vertices b and d are at distance two, so their labels differ. The only element of A at distance at least two from both 1 and 5 is 3. Hence f(c)=3. The tree and the list assignment are invariant under reversing the spine, so we may assume f(b)=1 and f(d)=5.

Vertex a is adjacent to b and at distance two from c. Its list A therefore permits only f(a)∈{4,5}.

- If f(a)=4, the labels in B at distance at least two from 4 are {1,6}. Each of a₁,a₂ is at distance two from b, whose label is 1. Both leaves are therefore forced to label 6.
- If f(a)=5, the labels in B at distance at least two from 5 are {1,3}. Again label 1 is forbidden by b, so both leaves are forced to label 3.

In either case a₁ and a₂ receive the same label although they are at distance two. This contradiction proves that the specified five-list assignment has no L(2,1)-labeling. In particular χ_ℓ^(2,1)(T)≥6.

## 3. Exact ordinary value

Use only the common palette A and assign the spine a,b,c,d,e the labels 1,5,3,1,5, respectively. Give a₁,a₂ labels 3,4; b₁ label 2; d₁ label 4; and e₁,e₂ labels 2,3. Every edge has label difference at least two. The labels on the neighbor set of each vertex are pairwise different, which checks every distance-two constraint in a tree. Thus χ^(2,1)(T)≤5.

Conversely, with common palette {1,2,3,4}, a degree-three vertex has at most two palette elements differing from its own label by at least two. Its three pairwise-distance-two neighbors need three distinct such labels. This is impossible, so χ^(2,1)(T)≥5.

Therefore χ^(2,1)(T)=5. This lower bound uses the actual degree-three vertices of this tree and is not asserted for the isolated-vertex case.

## 4. Exact list value: a self-contained six-list upper bound

More generally, any finite tree of maximum degree Δ has an L(2,1)-labeling from arbitrary lists of size Δ+3. Root the tree and label vertices in nondecreasing depth, processing the children of each parent consecutively. At the moment a non-root vertex v is labeled, its already labeled neighbors consist only of its parent. This excludes at most three integer labels. Its already labeled vertices at distance two consist of its grandparent, if present, and its earlier siblings.

If v's parent is the root, there are at most Δ−1 earlier siblings and no grandparent. Otherwise there are at most Δ−2 earlier siblings and one grandparent. In either case, at most Δ−1 further labels are excluded. Altogether at most Δ+2 list elements are forbidden. A list of Δ+3 elements therefore has an available label. The root itself may be given any label. The one-vertex tree is immediate.

For this tree Δ=3, so arbitrary six-element lists always suffice. Together with Section 2 this proves χ_ℓ^(2,1)(T)=6, without relying on an unaudited external upper-bound proof.

## 5. An infinite family

Extend any of the six original leaves by a pendant path of any nonnegative length, independently. The resulting tree T′ still has maximum degree three. The original ordinary five-label witness extends successively along each added path: an added vertex sees its already labeled parent and one grandparent, which forbid at most four labels of A. Different appended paths have no new distance-two constraint between their new vertices. Hence χ^(2,1)(T′)=5.

Give the original eleven vertices the bad lists from Section 1 and every new vertex any five-element list, for example A. Distances among original vertices are unchanged, so a list labeling of T′ would restrict to a list labeling ruled out in Section 2. Thus χ_ℓ^(2,1)(T′)≥6. Section 4 gives the reverse inequality. This yields infinitely many finite-tree counterexamples, including arbitrarily large diameter.

## 6. Historical certificate method and its limits

The original certificates used vertices 0,…,10, corresponding to a,a₁,b,b₁,c,d,d₁,e,e₁,e₂,a₂. They recorded the edges and lists specified above, an ordinary witness, and the dynamic-programming states for both the bad assignment and the common five-element lists. Those raw certificates are not distributed here; the following retains the mathematical recurrence and historical verification scope.

Root the tree at vertex 0. A state (v,p,q) says that v has label q, its external parent has label p (or null at the root), and the whole descendant subtree can be labeled. For every child w, its allowable root labels are those r with a feasible child state (w,q,r) and r≠p. Labels at distinct children must be distinct. Consequently feasibility is exactly the existence of a system of distinct representatives of these child-label sets.

In the historical certificates, each feasible state supplied distinct child labels, and each infeasible state supplied a Hall-deficient subset of children and its exact union of allowable labels. The independent audit checked every state, every positive witness, every Hall union, the completeness of the state table, and the root outcome. It used explicit exceptions rather than assertions and ran under normal Python, -O, and -OO. A separate global backtracking algorithm also checked the bad assignment without the tree-state recurrence. No mathematical program was rerun during editorial preparation.

No computation is needed for the proof in Sections 1–5. The finite-state search was a discovery mechanism only. No minimality or all-list theorem is inferred from the exploratory search's stopping point.

## 7. Finite-label bound for future exhaustive work

For any fixed n-vertex graph and positive integer k, any bad assignment of k-element integer lists can be replaced by a bad assignment with labels in {1,…,nk}. Sort the union of all labels and replace each by its rank. If the rank-labeled instance had an admissible labeling, lifting each rank to its original label would preserve unequal labels and would not decrease any positive integer difference. In particular rank difference at least two lifts to original difference at least two. The lifted labeling would contradict the original bad assignment.

Conversely, assignments contained in {1,…,nk} are among all assignments. Thus testing every k-subset of that finite palette at every vertex would be complete for that fixed graph. Rank compression need not preserve feasibility in the other direction: it may create a new difference-one conflict. This directionality is deliberate. No such exhaustive nk-palette test is claimed here.

## Sources

- Anja Kohl, “Some notes on L(d,s)-list labellings of trees and cacti,” Oberwolfach Report 7/2006, pp. 414–416. https://doi.org/10.4171/owr/2006/07 . Exact PDF: https://ems.press/content/serial-article-files/46037?nt=1 .
- Anja Kohl, 2006 dissertation, Section 4.4, Conjecture 4.4, printed p.124; historical special-case results on printed pp.125–130. https://webdoc.sub.gwdg.de/ebook/dissts/Freiberg/Kohl2006.pdf .
- Hasunuma, Ishii, Ono and Uno, “A Linear Time Algorithm for L(2,1)-Labeling of Trees,” https://arxiv.org/abs/0810.0906 . This ordinary-span algorithm does not establish an all-list guarantee and is not used in the proof.
