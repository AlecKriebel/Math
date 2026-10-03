# Attempt 5: Can a conference graph force an early obstruction?

Timestamp: 2026-10-03 14:02 UTC. Budget: 5/5. Exact-target completion estimate: 5%; full resolution achieved: 0%.

Conference graphs are the sharp known first-contraction examples. Try to force the proposed upper bound D=(n-1)/2 to fail at the second contraction. Write n=4k+1, k>=1. Every original vertex pair has disagreement size 2k.

## Triple-part obstruction
For a triple T, let e(T) be its induced edge count and let r(T) be the number of vertices outside T having a mixed neighbourhood on T. Sum the disagreement sizes over the three pairs of T. An external vertex contributes 0 if uniform on T and 2 if mixed. Internal third-vertex contributions total 0 when e(T) is 0 or 3, and 2 when e(T) is 1 or 2. Therefore

r(T)=3k-1 if e(T) is 1 or 2, and r(T)=3k otherwise.

Thus for k>=2, a second contraction overlapping the first pair produces a triple-part of red degree at least 3k-1>2k. A width-2k sequence must start with two disjoint pairs. This is a direct special case of the early-pair structure in Heinrich et al., Lemma 4.2, and is credited accordingly.

## Exact count of safe disjoint second contractions
Fix the first pair {u,v}. Partition the remaining vertices into A (common neighbours), B (common nonneighbours), C (u-only neighbours), and E (v-only neighbours). Conference parameters give {|A|,|B|}={k-1,k} and |C|=|E|=k, regardless of whether u,v are adjacent.

The second pair {x,y} is unsafe at the ceiling 2k exactly when its 2-by-2 adjacency rectangle to {u,v} has two equal nonconstant rows or columns. In terms of these four classes, the forbidden choices are:

- two vertices in C;
- two vertices in E;
- one vertex in A and one in B.

Indeed a homogeneous rectangle gives update (0,0); one or three edges gives (0,0); a diagonal two-edge rectangle gives (-1,-1); and a row- or column-constant nonhomogeneous rectangle gives (+1,-1) or (-1,+1). Each pair started at 2k, so exactly the last type violates the ceiling. Other singleton red degrees are at most 2<=2k.

There are 2*choose(k,2)+k(k-1)=2k(k-1) forbidden second pairs. Therefore every first contraction has exactly

choose(4k-1,2)-2k(k-1) = 6k^2-4k+1

safe disjoint second contractions. In particular a two-step obstruction is impossible in any conference graph. Direct controls verify the formula, every pair rectangle, and every triple for prime-order Paley graphs of orders 5,13,17,29.

Outcome: the obvious conference-graph disproof route fails quantitatively. There are many safe second steps, but this does not ensure a sequence through all later stages. Later active pairs create simultaneous prefix constraints absent from the two-step argument. The original maximum M(n), and the universal sharp upper bound, remain unresolved by this five-turn effort. No additional proof search is counted as verification; further work needs a materially new mechanism or a separately authorized budget.
