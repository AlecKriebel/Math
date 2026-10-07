# Independent bowtie tube and face audit

## Verdict

No mathematical error was found in the tube enumeration, its stated completeness argument, or the qualified image-type discussion in authored approach 5.

- Exactly **37** proper tube translation classes occur, with sizes **6, 10, 12, 9** for sizes 2, 3, 4, 5.
- The claimed span bound 16 is valid. The largest span actually occurring is 7.
- A separate exact periodic-cycle certificate confirms face codimension counts **1, 37, 189, 304, 152**. The original finite-window computation agrees, but its finite-window test alone is not a general certificate.
- All **49 combinatorial predicted product-face types** occur. This does **not** verify that each open face maps onto its predicted product-face interior, or identify the source-defined common-refinement stratification.
- The statement that a mixed connected tube must contain a representative of residue 2 is valid, with “mixed” meaning it contains both a residue from {1,3} and one from {4,5}.

All work here is independent audit material. Original files were neither executed as programs nor edited. No publication was performed.

## Sources inspected

The local supplied text of Pavel Galashin, *Totally nonnegative critical varieties*, arXiv:2110.08548v2, was inspected at Definition 2.4, Definitions 3.1–3.2, Section 3.2, Definition 3.5, Theorem 3.7, Lemma 3.10, the affine-poset construction in Section 3.4, and Definition 4.9. Public citation: https://arxiv.org/abs/2110.08548v2.

The mathematical claims audited are in `authored/05_boundary_face_quotient_attempt.md`; the original programs and saved data are in `checks/enumerate_bowtie_tubes.py`, `checks/enumerate_bowtie_faces.py`, `checks/bowtie_tubes.json`, and `checks/bowtie_faces_exploratory.json`, all under the supplied problem directory. Approach 2 was consulted only for the declared interpretation of the two triangle factors.

## 1. Poset reconstruction and exact tube completeness

Independently interlacing the chord endpoints in Definition 2.4 for fbar=(3,1,5,2,4) gives crossings 12,13,23,24,25,45. The source's periodic crossing-relation construction therefore has the same transitive closure as the six covering edges, repeated with period 5,

    1 -> 2 -> 3 -> 6
    2 -> 4 -> 5 -> 7.

The additional edges arising directly from crossings are transitive consequences of these edges. Conversely all six displayed edges occur among the crossing generators. No displayed edge admits an alternative nontrivial increasing path, so these are the ambient Hasse edges. Their jumps are at most 3; the less sharp bound 4 for all crossing generators used by the original report is nevertheless correct.

A tube has at most five elements by residue uniqueness. If a subset is order-convex, a covering relation in its restricted order must also be an ambient cover: an intermediate ambient element would be forced into the subset by convexity and would contradict the restricted cover. Thus a convex connected subset is connected using ambient Hasse edges. A spanning tree on at most five vertices has at most four edges. The difference between its maximum and minimum labels is at most the sum of the absolute jumps along their tree path, hence at most 4 times 4 = 16. Translating by 5 uniquely normalizes the minimum into {1,2,3,4,5}.

Every generating edge increases its integer label. Therefore every intermediate vertex of a comparability path from a to b lies in the ordinary integer interval [a,b]. The original closure window [-30,40] contains every relevant path and every possible convexity witness for its search, whose largest possible label is 21. Its closure computation is therefore exact for this search. Its comparability-graph connectivity test is equivalent to connectivity of the restricted poset, and convexity identifies the latter with the required ambient-cover connectivity. There is no missing finite-window qualification in the tube result.

The independent program uses a different enumeration: start from each normalized minimum and recursively extend subsets along the six Hasse edges, retaining residue uniqueness and then testing convexity. Every connected set admits such an extension order, so this finds all tubes without assuming a numerical span cutoff. The result agrees set-for-set with the saved original list.

## 2. Exact reconstruction of the infinite order

Write an integer as r+5t with r in {1,...,5}. Represent each cover by a directed residue edge whose weight is its increase in period: the edges 3 -> 1 and 5 -> 2 have weight 1 and the remaining four edges have weight 0. Let d(r,s) be the shortest-path weight, including d(r,r)=0. The exact matrix is

    0 0 0 0 0
    1 0 0 0 0
    1 1 0 1 1
    2 1 1 0 0
    2 1 1 1 0.

For distinct integers x=r+5t and y=s+5u, x is below y in the poset exactly when u-t >= d(r,s). Necessity follows by projecting a cover path to the residue graph. For sufficiency, a shortest residue path lifts to an actual cover path with displacement d(r,s). Each residue lies on a directed cycle of total weight 1, so appending such cycles realizes every larger integer displacement. The excluded equal-integer case turns non-strict reachability into strict order. This proves that the audit program's order test is exact on all integers, with no closure window.

## 3. Exact periodic acyclicity certificate

For selected tube representatives A_i, define w(i,j) as the smallest integer k such that A_i and A_j+5k are disjoint and some element of the former is strictly below some element of the latter. This minimum exists: sufficiently negative shifts put the target entirely below the source in integer order, while the affine-poset property gives comparable pairs for sufficiently positive shifts.

An edge in the infinite directed tubing graph is a quotient edge i -> j with an integer shift k >= w(i,j), though not every larger shift needs to be an edge. Every i has an actual shift-1 self-edge: A_i and A_i+5 are disjoint by residue uniqueness, and p is below p+5 for each p in A_i.

The infinite graph is acyclic if and only if every directed simple cycle in the finite weighted quotient has **strictly positive** total minimum weight:

1. A zero-weight quotient closed walk using actual minimum edges lifts to a closed walk in the infinite graph and thus contains a directed cycle.
2. A negative-weight quotient closed walk lifts to a path from A_i to a negative translate of itself. Appending the available shift-1 self-edges closes it, again producing a directed cycle.
3. Conversely, a directed cycle in the infinite graph projects to a quotient closed walk with total actual shift zero. Replacing actual edge shifts by their minima gives total weight at most zero. Every finite quotient closed walk decomposes into directed simple cycles, so at least one of those has nonpositive total minimum weight.

The independent program checks all simple quotient cycles, including loops, for all candidate collections of at most four tube classes. Nesting/disjointness is checked for **all** translates: a translate can intersect only at one of the finitely many shifts (a-b)/5 where a and b have the same residue. The source face theorem supplies the dimension-four bound on the number of classes in a proper tubing.

In this example every pairwise nested/disjoint candidate passed the exact global acyclicity test. Counts by collection size were 37,189,304,152. The original five-translate acyclicity test agreed on every candidate, and the exact retained face set matches the saved original face set. This is an independent certificate for this particular output, not a validation of finite-window acyclicity as a general method.

## 4. Image labels and their precise scope

Lemma 3.10 evaluates a circular-chain sine vector at its minimal containing tube. Together with the collision-block description of a fixed open compactification face, it supports the three cases used in approach 5:

- Three distinct positions at the circular root scale give a strict triangle-side triple, hence a point of the triangle interior.
- Three distinct positions at a finite linear scale give a degenerate triangle-side triple with a unique longest side, hence a point of the corresponding open edge.
- A pair still colliding at that scale gives one zero side and two equal nonzero sides, hence the corresponding vertex.

The independent label implementation fixes an actual representative of one residue, examines exactly aligned containers and children, and does not rely on the original finite translate window. It matches every saved face label and obtains all 49 pairs of the seven nonempty triangle-face types.

This verifies the combinatorial prediction and supports **containment in the corresponding product-face interior** for each open source face, assuming the separately audited two-factor measurement model. It does not supply an inverse construction for an arbitrary pair of target points. In particular:

- 49 distinct labels are not 49 certified exact face-image sets.
- Nonempty occurrence of every label does not prove surjectivity of any individual source face onto its entire predicted product stratum.
- Euler and simple-polytope numerical identities are consistency checks, not substitutes for the periodic certificate or a geometric image theorem.
- The source's common refinement of open-face images can be finer than the product-face partition unless the missing image-surjectivity/stratification argument is established.

## 5. Mixed-tube observation

Delete every integer congruent to 2 modulo 5 from the Hasse graph. The remaining edges connect only residues {1,3} to each other or residues {4,5} to each other; indeed the remaining components are pairs joined by 3+5t -- 6+5t or 4+5t -- 5+5t. A connected ambient Hasse subgraph meeting both residue groups must therefore pass through a residue-2 vertex. Because convex connected tubes are connected in the ambient Hasse graph, the claimed shared-strand condition follows. It does not by itself prove simultaneous realization of local shape parameters subject to all child collisions.

## Reproduction

Run `python critical_variety_audit/tubes/independent_audit.py` from the workspace. The script reads the original saved JSON only for comparison, writes only `independent_results.json` beside itself, and uses Python's standard library. No original script is imported or executed. The JSON includes the exact tube list, shortest-shift matrix, candidate counts, exact face counts, comparison mismatches, and all combinatorial predicted image labels.
