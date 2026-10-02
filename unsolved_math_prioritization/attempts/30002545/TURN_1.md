# Turn 1: a credited finite combinatorial proof of the leaf limit

**Complete first-turn candidate, pending independent review.** For every n≥2, the leaf probability in the source model is

p_n = (2n−1)/(3n).

Thus p_n tends to 2/3 without any assumption that a limit exists. For n=1 the sole vertex is a leaf, so p_1=1. This is a reconstruction from established contour and ternary-tree bijections, not a claim of a new numerical result or historical priority.

## 1. Two finite classes and a contour word

Put m=n−1≥1. Replace each original decreasing label v∈[n] by n−v. This is a bijection to increasing rooted plane trees with labels 0,1,…,m and root 0. It preserves leaves. Label an edge by its non-root endpoint. Read the edge labels along the depth-first contour, visiting children from left to right and recording an edge both on the way down and on the way up.

Each label i∈[m] occurs twice. All labels between its two occurrences belong to strict descendants of vertex i and are larger than i. Hence the word is a Stirling permutation: a permutation of the multiset {1,1,…,m,m} with all entries between the two occurrences of i larger than i.

Here is a static inverse, with no counting recurrence. In such a word write p_i<q_i for the positions of i. The closed intervals [p_i,q_i] are nested or disjoint. Indeed, a crossing p_i<p_j<q_i<q_j would imply j>i from the first pair and i>j from the second, a contradiction. The parent of interval i is the smallest interval strictly containing it, or the new root 0 if none exists. Order sibling intervals from left to right. This is an increasing plane tree because an interval strictly inside i has larger label. Every parent chain is a strictly increasing chain of finite intervals and terminates at the new root. The contour recovers the given word: entry and exit events are precisely the left and right interval endpoints, in their original order. Conversely, subtree containment in a contour word recovers exactly the original parent relation. These descriptions are mutually inverse for each finite word/tree, without an induction on size.

A vertex i is a leaf exactly when its occurrences are adjacent. Thus the number of leaves is the number of plateaux ii in the word. The root 0 is not a leaf because m≥1.

This is the Koganov–Janson correspondence. Janson's 2008 paper gives the contour description and leaf/plateau correspondence; his 2013 corrigendum credits Koganov's 1996 work.

## 2. The same words code ternary increasing trees

A ternary increasing tree on [m] has root 1 and three distinguished child slots at each vertex, called left, middle and right. Each slot is either empty or contains a subtree; labels increase from parent to child.

Read its contour by recording vertex i once after visiting its left slot and again after visiting its middle slot, and then visiting its right slot. Every label occurs twice. Between the two occurrences of i lies exactly the word from its middle subtree, so every intervening label is larger than i. The resulting word is again a Stirling permutation.

We give a static inverse to make the proof independent of the inductive insertion argument sometimes used to establish this known correspondence. For a label i, let I_i be the maximal contiguous interval of word positions with all entries at least i that contains the two occurrences of i. It is well-defined, since the entries between those occurrences exceed i. Every label occurring in I_i has both its occurrences there: if one occurrence were outside, the pair would straddle a boundary entry smaller than i, contrary to the Stirling condition.

The intervals I_i are distinct and nested or disjoint. To see nesting, if i<j and the intervals meet, the connected interval I_j consists of entries at least j, hence at least i, so it lies in the maximal such component I_i. They cannot be equal because I_i contains the entry i and I_j does not. The interval I_1 is the full word. Give each I_i other than I_1 as parent its smallest strict containing interval.

The two occurrences of i split I_i into three gaps: before, between and after them. Every nonempty gap has a least label j, and its entire gap is I_j. The boundary entries, when present, are i or are smaller than i, so the gap cannot extend in the component of entries at least j. It follows that the maximal proper subintervals of I_i are exactly these at most three nonempty gaps. Place their vertices in the left, middle and right slots respectively. Empty gaps give empty slots. Labels increase along all edges. Parent chains terminate at I_1, so this is a ternary increasing tree.

The word read from the resulting tree is the original endpoint/gap order at every vertex. Conversely, in a contour word from a ternary increasing tree the component I_i is exactly the complete word of the subtree rooted at i: it is contiguous, all its entries are at least i, and any adjacent entry outside that subtree, if present, records a strict ancestor and is smaller than i. Therefore the static inverse recovers the original tree. This establishes the bijection directly for arbitrary finite size.

A plateau ii occurs exactly when the middle slot at i is empty. Consequently, composing the two bijections carries plane-tree leaves to empty middle slots in a ternary increasing tree.

The ternary correspondence is credited to Gessel; Janson–Kuba–Panholzer give its detailed form in Theorem 1 and the plateau/empty-slot correspondence in Theorem 2. The present static inverse is supplied to avoid relying on their optional induction-based verification.

## 3. Threefold symmetry counts leaves

For a ternary increasing tree H let e_L(H), e_M(H), e_R(H) count its empty left, middle and right slots. There are 3m slots and m−1 parent-child edges occupying slots. Hence, for every H,

e_L(H)+e_M(H)+e_R(H) = 3m−(m−1) = 2m+1.

Rotate the three slot names simultaneously at every vertex. This operation is a bijection of the finite class of ternary increasing trees on [m], with inverse the opposite rotation, and it cyclically permutes the three empty-slot counts. It preserves all labels and increasing edge inequalities. Therefore the sums of e_L, e_M and e_R over the whole class are equal. Summing the displayed identity and dividing by three gives

(sum over H of e_M(H)) / (number of H) = (2m+1)/3.

No formula for the number of trees is needed, and no freeness of the rotation action is assumed. The two bijections preserve uniform counting, so this is also the expected number of leaves in the original n-vertex tree. Choosing a uniform vertex gives

p_n = (2m+1)/(3n) = (2n−1)/(3n) → 2/3.

This is a finite bijective/symmetry argument followed by an elementary limit. It uses neither generating functions, an inductive proof or recurrence for the leaf count, nor an assumed existence of the limit. Recursive implementations of finite contour traversals in the accompanying test script are algorithms used to check examples, not steps in the proof of the formula.

## 4. Source correction and credit

The OWR page prints (2n+1)!!/3 as the total number of leaves in T_n; this is inconsistent already at n=2. Bóna–Pittel Example 2.3 correctly gives (2n−1)!!/3 for n≥2. The proof above does not use either enumerative formula. Its exact mean agrees with the corrected formula and the known Janson identities.

The mathematical ingredients are established in the literature and the numerical statement was known before the source question. The contribution here is an explicit method-compliant presentation of their combination. Acceptance of the full source request, especially the meaning of “simple” and the no-induction constraint, requires independent review. No novel theorem is claimed.
