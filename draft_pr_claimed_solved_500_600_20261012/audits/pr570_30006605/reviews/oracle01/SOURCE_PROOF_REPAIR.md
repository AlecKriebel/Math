# Explicit scoped repair and independent proof checks for the BDH import

This document is a reviewer's derivation, not a claim that the original typeset proof was reproduced without correction, or that all cited classical algorithms have been independently formalized. It concerns Theorem 1 of arXiv:2410.10235v1 only. Its separate section 5 distance-oracle algorithm is not used by the candidate and is not modified here.

## Literal source issue and checkable finite control

The convention on p. 4 is log=ln. The dimension bound on p. 7 is d<=log_2 n. Pages 18 and 24 replace the latter by ell<=ln n, where ell is a wide-ladder size. The p. 24 proof thereby asserts that two copies of all slices have total size at most n. This is a substantive intermediate inequality, not just an interchangeable base in a final asymptotic expression.

There is an explicit succinct finite example falsifying this literal recursive-volume bound. Let n=10^12, ell=30, q=2^30=1,073,741,824, t=17,000,000,000, and s=n-q-30t=488,926,258,176. Take Q_30, attach t pendant leaves at each of its 30 unit-vector vertices e_i, and attach s pendant leaves at its zero vertex o. Attaching a leaf to a median graph preserves medianity: triples avoiding the leaf retain their median, and a triple including the leaf and two old vertices has the same median as the triple with its attachment vertex substituted. Repeating this proves that the entire explicitly specified graph is median.

Every core coordinate cut has a minority of size 2^29+t=17,536,870,912; all other cuts have singleton minorities. Since e^7>1000 (already a finite positive Taylor partial sum exceeds 1000), ln(10^12)<28. Therefore every core minority is strictly below n/(2 ln n), as 56*(2^29+t)=982,064,771,072<n. All cuts are unbalanced under the literal v1 threshold. The zero vertex lies in every majority halfspace and is the unique unweighted median. Give the all-one cube antipode the arrival weight n and all other vertices weight zero. This makes the antipode the unique weighted farthest vertex from o, and its wide ladder comprises all 30 coordinate cuts. The union of their minority halfspaces has size q-1+30t=511,073,741,823. The slices partition this union, so two copies have size 1,022,147,483,646>n. `controls.py` certifies these strict inequalities using exact rational arithmetic. This does not disprove correctness of the original algorithm or Theorem 1; it refutes the literal per-level-volume estimate for the written threshold.

## A single consistent implementable replacement

For all recursive instances of size N>=3, set

    L(N)=ceil(log_2 N),   f(N)=2 L(N).

Determine L(N) by the bit length of N-1. A Theta class is balanced precisely when f(N)*min(|H'|,|H''|)>=N. Otherwise it is unbalanced. Never compute a real logarithm in an algorithmic comparison. For N<=2, use the original direct base case before evaluating f. If a total-domain definition is wanted, set f(N)=2 max(1,ceil(log_2 N)). This also repairs the original formal mismatch between its integer-valued f declaration and its later real-valued choice 2 ln N.

Use this f consistently in the balanced/unbalanced tests, the name of the unbalanced family, all minority-size bounds, slice-size bounds and recursive-volume/depth proof. No graph, weight, objective or target restriction changes.

## Checks of every proof-bearing step in sections 3-4

1. **Definition 12 / choice of separator.** A balanced cut yields nonempty gated median halfspaces partitioning N vertices, with each size at most N(1-1/f(N)). The comparison above tests its existence using the same halfspace-size algorithm. The structural preprocessing does not depend on f or arrival weights.

2. **Lemma 16 / stopping depth.** For N>=3, L(N)<=2 log_2 N, hence f(N)<=4 log_2 N=(4/ln 2)ln N. Set lambda=4/ln 2>2. Every child size is at most N(1-1/f(N))<=N(1-1/(lambda ln N)). This is exactly the upper-envelope recurrence in Lemma 16. The function N(1-1/(lambda ln N)) is increasing on N>=3; its derivative is 1-(ln N-1)/(lambda(ln N)^2)>0. Thus the level maximum obeys that recurrence too. Lemma 16 applies and gives depth O(ln^2 N). Sizes one and two terminate rather than evaluating a logarithmic recurrence.

3. **Theorem 3 / balanced merge.** It uses only gatedness and the fact that the weight is added at the arrival vertex: for x in one halfspace and y in the other, d(x,y)+omega(y)=d(x,g(x))+d(g(x),y)+omega(y). The maximum over the opposite halfspace is d(x,g(x))+E(g(x)); max with the within-halfspace output is exact. The threshold and positivity of omega play no role. Nonnegative integer weights remain valid by restriction.

4. **Lemma 17 / unique median.** In an all-unbalanced instance f(N)>=2. An egalitarian cut would be balanced because its smaller side is N/2>=N/f(N). Thus no egalitarian cut exists. The majority-rule description of the median set and its interval property give a unique vertex v0 in all majority halfspaces, exactly as in the source. These are cited structural median facts, not new assumptions about the profile.

5. **Definition 14, Lemma 18 / dominance branch and ties.** Choose a maximizer u_max of d(v0,u)+omega(u), giving v0 priority in a tie. If u_max=v0 then for every x,y,

       d(x,y)+omega(y) <= d(x,v0)+d(v0,y)+omega(y)
                         <= d(x,v0)+omega(v0).

   The right side is attained by y=v0, including x=v0. The returned formula is exact. Zero weights are permitted; for a connected graph of size at least two an all-zero profile cannot trigger u_max=v0, but the same formula remains valid whenever this branch's dominance inequality is met. The N<=2 base handles all-zero singleton inputs.

6. **Wide ladder / Lemma 19.** The ladder consists of classes adjacent to v0 separating it from u_max. These are pairwise orthogonal, so ell<=d<=log_2 N<=L(N). It is nonempty when u_max!=v0: any first edge of a shortest v0-u_max path supplies a class. The source's shortest-path argument can be replaced with this short independent median argument. If the ladder of x misses the wide ladder and v0 is not on an x-u_max geodesic, let m be the median of (v0,x,u_max). Then m!=v0. A first neighbor z along a v0-m geodesic belongs both to I(v0,x) and I(v0,u_max), since m belongs to both intervals and the distance equalities extend that geodesic. The class of v0z is adjacent to v0 and separates it from both x and u_max, contradicting the disjoint ladders. Therefore v0 lies on an x-u_max geodesic. Triangle inequality then gives E(x)<=d(x,v0)+E(v0), with equality at u_max. No balance constant enters this argument. The x=v0 case is immediate, with empty ladder.

7. **Large sets / Lemmas 20-22 / nonempty slices.** Let minority halfspaces H_i' be indexed by the wide ladder. G_i is the intersection of the first i complementary majorities; it contains v0 and is gated. S_i=G_i intersect H_{i+1}' is also gated. It is nonempty: the cube supplied by the pairwise orthogonal incident classes at v0 contains the sign pattern with only coordinate i+1 on the minority side. G_{i+1} remains nonempty because it contains v0. Thus all actually used intersections are nonempty and all recursive graphs are gated, connected median induced subgraphs. The source's Lemma 21 is stated for isometric subgraphs; only the gated median case is needed, and that case inherits restricted Theta classes. An arbitrary isometric nonmedian subgraph would not be needed or justified by the paper's square-generated Theta definition (C6 inside Q3 illustrates why that broader wording is best avoided).

8. **Minority and slice counts / Lemma 23.** Each minority has strictly fewer than N/f(N) vertices. Hence |S_i|<N/f(N), and |G_i|>=N-iN/f(N). Since ell<=L(N), |G_ell|>=N/2. The slices are pairwise disjoint and partition exactly the vertices whose ladder intersects the wide ladder. Thus

       2 sum_i |S_i| <= 2 ell N/f(N) <= N.

   This is the exact bound required for duplicated recursive calls. Every slice child also has size at most N/f(N)<=N(1-1/f(N)), because f(N)>=2.

9. **Definition 18 / fiber arrival weights.** For each slice within G_i, assign a boundary gate z the maximum of d(z,y)+omega(y) over the nonempty outside open fiber; retain omega at nonboundary vertices. Boundary fibers are nonempty because the restricted Theta cut has an edge crossing at each boundary vertex. All new weights are nonnegative integers. The boundary maximum can be smaller than omega(z); this is why BOTH original-weight and fiber-weight recursive calls are required. No monotonicity omega*>=omega is assumed. Zero values are allowed at every stage.

10. **Theorem 4 / Corollary 3.** For x in S_i, gatedness makes every outside contribution equal d(x,g(y))+[d(g(y),y)+omega(y)]. Maximizing fiber by fiber is exactly represented by omega*. A nonboundary omega* value represents an actual original inside vertex, so it cannot create an excessive fictitious value. The maximum of the original-weight and fiber-weight slice eccentricities is therefore precisely the G_i eccentricity. For an x in a later slice, compare its previously computed G_{i+1} value with d(x,g_{S_i}(x))+E_{(S_i,omega)}(g_{S_i}(x)). The same identity holds for all zero/tied weights. Final G_ell outputs are already exact by item 6. No f-dependent identity is used.

11. **Construction time and recursion.** The source's cited O(m) Theta/halfspace/median procedures are unchanged. Ladder sets and slices are computed in O(N log^2 N). For each of at most log_2 N slices, a multisource BFS in G_i computes all gates and gate distances; one scan forms the fiber maxima before their recursive calls. Merging also takes one scan/BFS per slice. Therefore nonrecursive work is O(N log^2 N), using m<=N log_2 N. Balanced nodes cost no more. Recursive child volumes sum to at most N by items 1 and 8. Thus each level's total cost is O(n log^2 n), and item 2 supplies O(log^2 n) levels: total O(n log^4 n). Empty recursive instances never arise. The all-zero and dominance branches shorten the recursion.

12. **Weight/word bounds for the candidate calls.** Initially omega in [0,n-1]. A fiber update adds a graph distance at most n-1 to a prior maximum. Along a recursion path there are O(log^2 n) levels, so all internal weights are at most O(n log^2 n). Graph distances, IDs, counts (including the candidate's n^2 row-entry total), and these weights need O(log n) bits. Thus a standard O(log n)-bit-word RAM supports the imported bounded-weight calls without hiding arbitrary real weight arithmetic in BDH. Classical structural routines remain cited imports, and a machine-checked implementation of them is not supplied here.

## Published-version access and status

On 2026-10-15, one normal web opening of the official SODA DOI https://doi.org/10.1137/1.9781611978322.52 returned inaccessible from the web tool. I did not retry this route or use a bypass. The legally public primary arXiv v1 PDF and its HTML both confirm the convention and offending estimates. I cannot say whether the published SODA typesetting already corrected them. The correction above establishes the needed theorem by an explicit consistent mechanism, while retaining all classical imported structural lemmas as stated dependencies.

## Additional preserved correction: Lemma 16's displayed proof

A final visual recheck of original PDF p. 13 confirms a second typeset proof error: after bounding s_r by a product with factors 1-1/(lambda ln s_i), it upper-bounds that product using the factor with s_r. Because s_i>=s_r, that factor comparison goes in the opposite direction. The statement's O(log^2 n) consequence is nevertheless correct. Replace the product estimate by the following self-contained argument, which supersedes any reliance above on the literal displayed proof.

Let N be the root size and lambda=4/ln 2. Along every recursion path, while the current size s_i>=3, the repaired threshold gives

    s_{i+1} <= s_i (1-1/(lambda ln s_i))
              <= s_i (1-1/(lambda ln N)).

The second inequality follows from s_i<=N. Therefore, as long as a nonterminal path persists through h steps,

    s_h <= N (1-1/(lambda ln N))^h
         <= N exp(-h/(lambda ln N)).

For h=ceil(lambda (ln N)^2), this is at most 1, so the path must already reach the N<=2 base case. The recurrence envelope's positivity at N>=3 follows from lambda ln N>1; all actual child graphs are independently nonempty by item 7. This gives a complete O(log^2 N) depth proof with harmless integer rounding. It uses neither the erroneous product direction nor the original log-base inequality. This additional source correction was discovered after the first checkpoint and is retained explicitly.
