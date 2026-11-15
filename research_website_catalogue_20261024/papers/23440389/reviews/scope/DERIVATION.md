# Supplementary checkable derivations

These are my deductions, written after the initial reconstruction; the initial proof and exposure boundary remain immutable.

## Admissible-state induction

Fix a root of a finite tree and finite positive-integer lists. For nonroot v with parent u, only states p in L(u), q in L(v), |p-q|>=2 are locally admissible. At the root p=null and q in L(v). Set all other states to zero. Let C(v) be the children. Then

F_v(p,q) = sum over tuples (r_w : w in C(v)) of product F_w(q,r_w),

where r_w are pairwise distinct, r_w in L(w), |r_w-q|>=2, and r_w!=p when p is not null. This counts full descendant labelings extending the local state. At a leaf, the empty product gives one exactly on admissible states. For induction, each child subtree is counted by its own F. Between different child subtrees the shortest cross-distance is two only between their child roots, already made distinct; all remaining cross-distances are at least three. The external parent is at distance two from child roots, enforced by r_w!=p; it is farther from all deeper descendants. This establishes necessity, sufficiency and unique counting, with no overlap of alternatives. Summing F_root(null,q) over its list counts complete labelings.

The supplied optional routine omits a general-purpose outer guard but does not accept arbitrary external states through its public tree_count interface: root q ranges over its own list and every recursive child call is produced from a list/edge/grandparent-admissible tuple. Thus its reachable-state calculation matches the guarded recurrence. My own routine additionally rejects invalid q/parent-edge states explicitly. Neither code interface is an assertion that an arbitrary invalid external triple is feasible. The corrected deposited prose expressly defines the fully guarded domain.

## Exact eight common-five labelings

At b,d all neighbor lists are A, so the same endpoint forcing gives opposite 1 and5 and c=3. Choose b=1,d=5. Then a in {4,5}. If a=4, both its A-leaves must be2 (the edge permits1,2, and their distance-two b=1 excludes1), impossible. Hence a=5 and its two leaves use2,3 in either order. Likewise e=1 and its two leaves use3,4 in either order. The middle pendant vertices are forced b1=4,d1=2 by their edge and other distance-two neighbors. All four choices satisfy every constraint. Reversing the spine gives four more, disjoint because b,d swap labels. Thus exactly8, with no quotient by graph or label symmetries.

## Universal lists and the infinite family

For arbitrary lists the forbidden-label bound counts actual integers rather than palette positions. If a parent label is1, the nonexistent positive0 contributes no exclusion; duplicates among forbidden values can only help. Hence sparse, overlapping or translated lists need no extra assumption. For a singleton there is no nonroot step. The finite breadth-first argument terminates without compactness or any infinite-tree premise.

For six independent pendant lengths m_i, old T remains isometric. Distances between new vertices on different paths are at least1+2+1=4 because distinct old leaves have old distance at least2. An added path can therefore be extended independently using five labels. Choosing one length tending to infinity produces pairwise unbounded diameters, so the family is genuinely infinite, not merely many descriptions of a bounded set. A bad list assignment on the old isometric subtree remains bad under every list assignment to new vertices by restriction.

## Rank compression: exact direction

For the union S={s_1<...<s_m} of all lists, distinct integers satisfy s_j-s_i>=j-i. A valid compressed labeling using rank i therefore lifts to s_i with all edge gaps>=2 and all distance-two inequalities preserved. Contraposition gives: original infeasible implies compressed infeasible. With n vertices and k-element lists, m<=nk, so existence of an arbitrary bad assignment implies existence of a bad assignment using {1,...,nk}. This is an existential reduction and does not establish per-instance equivalence. The edge lists {1},{3} are feasible but their compressed versions {1},{2} are not. No finite all-assignment scan has been performed or claimed.

## Older cyclic figure, not a tree instance

Read directly from actual FS2001 printed14/Figure4: two length-three rails joined at both ends, with a triangular tip on each end. This gives n=10,m=12, connected cycle rank m-n+1=3. In the literal indexing in INDEPENDENT_CHECKS.json, the ordinary labels are [1,4,2,5,5,2,4,1,3,3]. Only left tip8 has {1,2,4,5,6}; the other nine lists are A. A generic whole-graph search independently counts zero list solutions. This earlier general-graph separation deserves credit, while its cycles preclude using that graph itself to refute the tree-only universal statement. No assertion about every possible reduction of that mechanism or historical first tree counterexample is made.
