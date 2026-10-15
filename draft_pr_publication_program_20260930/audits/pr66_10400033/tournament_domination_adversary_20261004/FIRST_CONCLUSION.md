# First saved conclusion: tournament domination family

Pinned original candidate: head `78f4a7fadac0fd24e147a617956cb409eb6a579e`, candidate SHA256 `fc2be9794873073e6482e8dfe93ccfd6c5d6f8674c2058ba0a8fc900d906d698`.

## Procedural disclosure

Before reading the original verifier, I independently checked the graph edge rule, both listed pattern correspondences, and the degree-variance identity against the candidate. Those checks had not yet been saved. The subsequent batch mistakenly included original SOURCES.md and README.md, whose last paragraphs contain old review-success summaries. Consequently this is **not a pristine saved pre-opinion checkpoint**. No original review proof, review code, old review verdict JSON, sibling finding, or ROOT verdict has been read. This disclosure is a limitation on the independence record; the universal deductions below are checkable on their own.

## Current mathematical conclusion, conditional boundary

The graph domination argument is valid for the formal arrow polynomial with the exact listed patterns and coefficients. It implies the desired knot bound **conditional on** formula (4) being the correctly normalized classical-knot v3 identity. This review has not certified that imported identity or priority. Exact finite diagnostics remain to be executed.

For alternating endpoints of arrows c,d, write the circle order starting at t_c. If t_d lies before h_c, the order is t_c,t_d,h_c,h_d and t_c is outside (t_d,h_d). Otherwise the order is t_c,h_d,h_c,t_d, and t_c lies inside (t_d,h_d). Thus exactly one directed edge is assigned. The rule respects positive cyclic relabeling.

For P, the arrows c=(3,0), a=(5,1), b=(2,4) have only c-a and c-b intersections, with b->c->a. For T, c=(3,0), a=(1,4), b=(5,2) have all intersections, with c->b->a->c. Therefore a P subset contributes probability 1/2 and a T subset contributes probability 1 to the cyclic-triple indicator under fair missing-edge completion. Patterns are disjoint by their intersection counts; the unit is one unordered crossing subset. All remaining triples contribute nonnegative probability. Linearity of expectation needs no independence across triple indicators. The product distribution over missing edges exists for every finite partial graph, regardless of its knot realizability.

If Q is the signed arrow evaluation, the triangle inequality gives |Q| <= N_T + N_P/2 <= E C. Every complete tournament has

    C = binom(n,3) - sum_i binom(d_i,2)
      = n(n^2-1)/24 - (1/2) sum_i (d_i-(n-1)/2)^2.

The first equality counts a transitive triple exactly once at its unique source. Sum d_i=n(n-1)/2 gives the second equality. For odd n the variance term is nonnegative; for even n every summand is at least 1/4, giving C <= n(n^2-4)/24. Taking expectations of the integer per-completion floor bound is valid; it does not round the expectation itself. Even-n integrality follows by putting n=2k, yielding k(k-1)(k+1)/3. The cases n=0,1,2 have no triples and bound zero; formula (9) is used only for n>=1. No assumed geometric realizability or sign uniformity enters this graph theorem.

No graph counterexample found in this initial derivation. Universal graph correctness does not certify the imported knot formula. Finite enumeration, reproduction, and detailed edge cases remain. Review completion estimate: 35%.
