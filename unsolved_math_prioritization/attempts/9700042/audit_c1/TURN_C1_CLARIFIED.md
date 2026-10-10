# New continuation C1: a marked-defect bound for unrestricted cuts

Date: 2026-10-07. Problem: 9700042 / AMR-096-0042, rank 937.

## Provenance and status

This is a newly authored continuation, not a recovery of the missing historical author or audit archive. Its definitions and proof are given in full below. The historical acceptance of another artifact does not validate this artifact. Independent review is still required. No solution or novelty claim is made.

The canonical corpus statement asks for

\[
1-v(p)\sim\sqrt{2(1-p)}\qquad(p\uparrow1).
\]

The original problem page is David Aldous, “A discrete Hammersley process as an extreme case of oriented percolation flows,” https://www.stat.berkeley.edu/~aldous/Research/OP/hammersley_flow.html (inspected 2026-10-07). It supplies the model and the existence of the deterministic limiting flow density. The new estimate below does not rely on the heuristic continuum approximation on that page.

Historical context only: the recovery report records a previously audited one-sided bound
\[
1-v(p)\geq\frac{\sqrt{1-p^2}}{1+\sqrt{1-p^2}},
\]
and therefore normalized liminf at least 1. Those original bytes have not been recovered, so this continuation neither re-certifies that proof nor counts its reported author turns as freshly verified.

## C1 outcome

The argument below derives the following upper estimate (no novelty claim)

\[
\boxed{\limsup_{q\downarrow0}\frac{1-v(1-q)}{\sqrt{2q}}\leq\frac e2.}
\tag{C1}
\]

Thus it reaches the conjectured square-root scale but leaves a factor of e/2 instead of 1. All cuts, including nonmonotone cuts, are covered. This is a proof submitted for independent review, not yet an accepted result.

## 1. Exact finite model and planar dual reduction

Let n >= 2. The directed primal graph has vertices (x,y) with 0 <= x,y <= n-1 and edges in the positive coordinate directions. An edge is closed independently with probability q and otherwise has capacity 1. The source set consists of the left and bottom boundary vertices excluding the top-left and bottom-right corners. The sink set is the union of the top and right boundaries. Source and sink edges to auxiliary terminals have infinite capacity. Let V_n be the maximum flow.

Two primal edges connect a prescribed source directly to a prescribed sink:

\[
e_L=((0,n-2),(0,n-1)),\quad
e_B=((n-2,0),(n-1,0)).
\]

Write c_L,c_B for their capacities, and put N=n-2. Label the (n-1)^2 bounded primal faces by the dual grid Q_N={0,...,N}^2, reflecting the vertical coordinate. A dual east or north step crosses a primal edge in the direction that contributes to an outward cut; it has cost equal to that primal capacity. The reverse step has cost zero. Distinct unoriented dual edges correspond to distinct primal edges. Let T_N be the minimum cost of a dual path from (0,0) to (N,N), and set T_0=0.

Then

\[
V_n=c_L+c_B+T_N. \tag{1}
\]

Here is the cut argument, including faces where the interface has degree four. Prescribe all source boundary vertices to lie in the source side S and all sink boundary vertices outside S. For each primal edge whose endpoints have different cut labels, draw its dual crossing, oriented with S on its right in the original physical embedding. Include separate exterior endpoints at the midpoints of e_L and e_B. At each bounded primal face the numbers of incoming and outgoing crossings agree, because the transitions between the two binary corner labels alternate cyclically. This includes a checkerboard face, with two incoming and two outgoing crossings. The exterior endpoint at e_L has one outgoing crossing and the endpoint at e_B has one incoming crossing. No other outer-boundary edge has different cut labels at its endpoints.

There is therefore a directed route from the first exterior endpoint to the second: otherwise the vertices reachable from the first endpoint would have no outgoing crossing, contradicting the sum of their outdegree-minus-indegree balances. Extract a directed path, or erase loops from an extracted walk. In reflected face coordinates, its east/north crossings are precisely outward primal crossings; its west/south crossings are inward primal crossings. Its cost is at most the directed cut cost, since only outward crossings contribute and all capacities are nonnegative. This proves that every primal cut costs at least c_L+c_B+T_N.

Conversely, a vertex-simple corner-to-corner face-dual path, extended through its two forced outer-boundary crossings, is a non-self-intersecting crosscut of the primal square and meets no primal vertex. By planar separation, it divides the square into two sides. Take as S the primal vertices on the side containing the prescribed source boundary arc. This arc is on the right of the path traversed from e_L to e_B. The outward cut crossings are exactly the forward dual crossings and e_L,e_B, while the reverse crossings contribute zero. This proves the reverse inequality by max-flow/min-cut. A minimum dual path can be chosen simple because all costs are nonnegative: removing any cycle from a minimizing walk cannot increase its cost. For n=2 the same argument has no internal dual step and gives T_0=0.

For a simple dual path P, let b(P) count its west and south steps and k(P) count its closed east and north steps. Its forward-step count is exactly 2N+b(P), hence its cost equals

\[
2N+b(P)-k(P).
\]

Define

\[
D_N=2N-T_N=\max_P\{k(P)-b(P)\}. \tag{2}
\]

The maximum may be restricted to simple paths. In particular,

\[
(2n-2)-V_n=2-c_L-c_B+D_N. \tag{3}
\]

The often tempting restriction to b=0 is not made. It is false in finite volume; the accompanying exhaustive checker supplies an n=4 counterexample.

## 2. Counting marked positions with bounded negative variation

For positive integers N,k, consider integer coordinate sequences x_0,...,x_{k+1}, with x_0=0, x_{k+1}=N and internal entries in {0,...,N}, whose total negative variation is at most k:

\[
\sum_{i=0}^{k}\max(x_i-x_{i+1},0)\leq k.
\]

Let their number be A(N,k). Then

\[
A(N,k)\leq
\sum_{t=0}^{k}\binom{k+1}{t}\binom{k}{t}
\binom{N+2k-t}{k-t}.
\tag{4}
\]

To prove (4), fix the number t of strictly negative increments. Choose their positions in binom(k+1,t) ways. Their positive magnitudes have sum at most k; the number of such t-tuples is binom(k,t), with the t=0 case interpreted as one. If their sum is B <= k, the other k+1-t increments are nonnegative and sum to N+B. Stars and bars gives binom(N+B+k-t,k-t), at most the last factor in (4). Dropping the restriction that intermediate coordinates remain inside [0,N] only enlarges the count. The case t=k+1 is impossible because the endpoint displacement is nonnegative.

Moreover,

\[
\frac{\binom{N+2k-t}{k-t}}{\binom{N+2k}{k}}
=\frac{(k)_t}{(N+2k)_t}
\leq\left(\frac{k}{N+2k}\right)^t.
\]

Writing r=k/(N+2k), the sum of the diagonal terms of the product of two binomial expansions is at most the full product, so

\[
\sum_t\binom{k+1}{t}\binom{k}{t}r^t
\leq(1+\sqrt r)^{2k+1}.
\]

Thus

\[
A(N,k)\leq\binom{N+2k}{k}
\left(1+\sqrt{\frac{k}{N+2k}}\right)^{2k+1}.
\tag{5}
\]

## 3. A finite probability bound covering backtracking

If D_N >= d > 0, some simple dual path has k closed forward edges and b backward steps, with k-b >= d. In particular k >= d and b <= k. Mark the starting vertices of these k forward edges in the order the path encounters them, and append the two endpoint vertices.

In each coordinate, the negative variation of the marked subsequence is at most the total negative variation of the entire path, hence at most b <= k. There are at most A(N,k)^2 coordinate sequences and 2^k choices of forward-edge orientations. We count only sequences giving distinct edges when taking probabilities; their number is bounded above by this possibly much larger combinatorial count. Since the path is simple, its marked edges really are distinct, and a fixed valid list is simultaneously closed with probability q^k. No independence between different lists is assumed.

A union bound therefore yields

\[
\Pr(D_N\geq d)\leq
\sum_{k=\lceil d\rceil}^{\infty}
(2q)^k\binom{N+2k}{k}^2
\left(1+\sqrt{\frac{k}{N+2k}}\right)^{4k+2}.
\tag{6}
\]

The infinite sum is an upper bound for the finite union over simple paths; it will only be used in a parameter range where the displayed majorant converges. Its purpose is precisely to charge all backward excursions through the variation bound instead of silently deleting them.

## 4. Extracting the asymptotic constant

Fix eta in (0,1) and epsilon > 0. Set

\[
a=e\sqrt{2q}(1+2\eta)(1+\sqrt\eta)^2(1+\epsilon).
\tag{7}
\]

Choose q sufficiently small that a < eta and

\[
\theta=32e^2q(\eta^{-1}+2)^2<1.
\tag{8}
\]

We bound the sum (6), starting at k=ceil(aN), in two ranges.

For aN <= k <= eta N, use binom(N+2k,k) <= [e(N+2k)/k]^k, together with k/(N+2k) <= eta, to get an upper bound on the kth summand of

\[
(1+\sqrt\eta)^2
\left[2qe^2(1+2\eta)^2(1+\sqrt\eta)^4(N/k)^2\right]^k
\leq (1+\sqrt\eta)^2(1+\epsilon)^{-2k}.
\tag{9}
\]

For k > eta N, the same binomial estimate, N/k <= eta^{-1}, and 1+sqrt(k/(N+2k)) <= 2 bound the summand by

\[
4\left[32e^2q(\eta^{-1}+2)^2\right]^k=4\theta^k.
\tag{10}
\]

Both geometric tails tend to zero exponentially in N. Hence

\[
\Pr(D_N\geq aN)\longrightarrow0\quad(N\to\infty). \tag{11}
\]

Always 0 <= D_N <= 2N, since a monotone path exists with cost at most 2N and all costs are nonnegative. It follows that

\[
\limsup_{N\to\infty}\frac{\mathbb E D_N}{2N}\leq\frac a2.
\]

Use (3) and the source-stated L1 convergence V_n/(2n) -> v(1-q):

\[
1-v(1-q)\leq\frac e2\sqrt{2q}
(1+2\eta)(1+\sqrt\eta)^2(1+\epsilon)
\]

for all sufficiently small q depending on eta,epsilon. First take limsup as q decreases to zero, then let eta and epsilon decrease to zero. This proves the candidate estimate (C1).

## 5. Exact unresolved gap and next attempt

The e instead of 2 is the usual first-moment loss in counting increasing point lists: even with b=0, the bound compares (2q)^k N^(2k)/(k!)^2 with 1 and produces k approximately e sqrt(2q) N. Improved handling of backward steps alone cannot remove this loss from the present union bound. Obtaining the conjectured constant requires a correlated longest-chain estimate, plus control of the freedom introduced by backward excursions.

A next approach should retain an exact last-passage shape or its upper-tail estimates for long monotone runs, and pay separately for the relatively rare coordinate decreases. The precise missing estimate is that allowing penalized backward steps changes the infinite-volume defect density by o(sqrt(q)). Neither that estimate nor the required uniform coarse-graining has been proved here.

## Checks and scope

`verify_resume_turn1.py` compares the directed primal min-cut to the dual shortest-path formula and separately checks the elementary coordinate counts. Its output is `TURN_C1_CHECKS.json`. These finite checks support the implementation and reveal incorrect reductions; they do not prove an infinite-volume statement. The mathematical proof is the argument above and remains subject to fresh independent review.
