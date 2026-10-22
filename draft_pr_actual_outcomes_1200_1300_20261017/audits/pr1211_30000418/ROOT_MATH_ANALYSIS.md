# Root mathematical reconstruction and source gate

The input claim is a negative answer to the universal arbitrary-list equality
for finite trees, not an interval-list or ordinary-span algorithm claim.
Source: Kohl, OWR7/2006, printed414–416, Conjecture4; primary PDF
https://ems.press/content/serial-article-files/46037?nt=1 . Root read the complete
three-page report text, including Definition1 and the conjecture. Its lists
are arbitrary equal-cardinality sets of natural numbers; the ordinary version
uses {1,...,k}. Kohl dissertation section4.4, printed124, explicitly defines
chi=lambda+1 and repeats the universal tree equality. Root read the relevant
primary text; independent visual/special-family checking is still pending.
No source absence/novelty assertion follows from this check.

The bad assignment is mathematically sound: the three A-list neighbors force
b,d into {1,5}; their distance-two constraint forces distinct choices. The
middle c is3. Graph/list reversal is an actual automorphism, so b=1,d=5 may be
assumed. Then a=4 or5. Its two B-list leaves each have only6 or only3 available,
respectively, because b=1 forbids1 at distance two. They must also be distinct,
a contradiction. This proves the arbitrary-list lower bound6.

The submitted common-palette witness satisfies all edges and every pair of
neighbors. A degree-three vertex cannot be labeled from common palette[4],
because each possible center label leaves at most two permissible neighbor
labels. Thus the ordinary palette minimum is5, zero-based span4.

The universal upper bound is analytic. In breadth-first child-block order a
nonroot sees only its parent among earlier neighbors. This forbids at most
three labels. Among earlier distance-two vertices there are only grandparent
and earlier siblings: at most Delta-1 labels total, because a nonroot parent
has at most Delta-1 children, whereas a root parent has at most Delta children
and no grandparent. Therefore at most Delta+2 labels are forbidden and any
Delta+3-element list has an available label. Root and singleton are immediate.
No probabilistic or finite-list sample is used to establish this quantifier.

Pendant paths at the six original leaves preserve maximum degree3 and all
old pair distances. Along any new path, the parent and grandparent exclude
at most four elements of common[5], so every ordinary witness extends. New
vertices on different attached paths have distance at least4. Restricting
any putative bad-list labeling to the old tree contradicts the fixed bad
assignment. Thus the entire independent six-parameter extension family has
ordinary palette5 and arbitrary-list number6, with unbounded diameter.

The rank-compression direction is also correct: if a compressed instance had
a valid labeling, increasing ranks back to their original distinct sorted
integers preserves unequal values and cannot shrink a positive difference.
The lifted labeling would solve the original bad instance. Original
infeasibility therefore implies compressed infeasibility; compressed
feasibility implies original feasibility. The reverse feasibility direction
is not claimed. For n vertices and k-element lists, at most nk distinct
labels occur, giving the finite completeness bound for future exhaustive
work, without claiming that work has been run.

ROOT_EXACT_VERIFICATION.json is an independent global MRV backtracking check,
using all-pair graph distances rather than the submitted tree-state recurrence.
It finds0 common-palette labelings for sizes1–4,8 for size5,6336 for size6 and0
for the specified bad five-lists. It validates every enumerated complete
witness separately. It rejects edge, distance-two and list-membership
corruptions. A thousand deterministic random six-list greedy runs only check
implementation behavior; they are not the universal six-list proof. Radius3,
diameter6,11 vertices,10 edges and maximum degree3 are independently computed.

Current root conclusion: no mathematical defect found. Separate mathematical
families and original-source visual checks remain pending; no priority gate
or publication readiness is asserted yet.
