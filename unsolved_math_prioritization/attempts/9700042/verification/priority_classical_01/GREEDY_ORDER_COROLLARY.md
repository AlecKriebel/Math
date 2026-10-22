# An old-input corollary for the order, not the sharp coefficient

Martin, *Linear growth for greedy lattice animals*, Theorem 1.1 and (1.7), supplies an almost-sure limiting maximal site weight per animal vertex bounded by C times the integral of the d-th root of the upper distribution tail. In dimension two with Bernoulli(r) site weights this bound is C sqrt(r), for an absolute C. The author-hosted 2001 preprint (published 2002) body and printed p. 2 have been inspected. No explicit optimal C is supplied by this statement.

Here is a complete elementary model map for what this input does establish about the target. Extend the dual edge-mark field to Z². At every vertex z let Y_z be the indicator that at least one of its two outgoing forward edges is marked. The Y_z are independent Bernoulli(r) with r=1−(1−q)². Distinct z use disjoint original Bernoulli variables.

For a simple path P from (0,0) to (N,N), write b for backward steps and k for marked forward edges. Its total number of steps is m=2N+2b; its visited vertices form an animal of m+1 sites containing the origin. Each forward mark is attached to a different starting vertex along this simple path. Therefore k ≤ sum_{z in P}Y_z ≤ A(m+1), where A(s) is the maximum Bernoulli site weight of an s-vertex animal containing the origin.

For any a>C sqrt(r), almost surely there is s₀ such that A(s)≤as for every s≥s₀. This is simultaneous in s and thus applies to every such path for every N with 2N+1≥s₀. An optimal target path can be taken simple with nonnegative reward, so b≤k. Consequently

k ≤ a(2N+2b+1) ≤ a(2N+2k+1).

When a<1/2 this yields k≤a(2N+1)/(1−2a), hence D_N/(2N)≤a(1+1/(2N))/(1−2a) almost surely for all sufficiently large N. Because 0≤D_N/(2N)≤1, the expected limsup is bounded by a/(1−2a). Use the source-premised fixed-q flow limit to obtain

g(q) ≤ a/(1−2a).

Let a decrease to C sqrt(r), for q sufficiently small. Since r~2q, this proves g(q)=O(sqrt(q)), and also k,b=O(sqrt(q)N) on optimal nonnegative paths at fixed q, almost surely eventually. It gives no constant-one conclusion.

Thus the square-root upper *order* and qualitative sparse-path mark/backtracking control are already elementary consequences of classical greedy-animal estimates. This does not show that C1's particular e/2 normalized bound, its explicit finite tail, or the full C4 theorem were previously written or proved. This derived corollary is a priority/model-mapping check, not another attempt to prove the sharp target.
