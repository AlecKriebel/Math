# Independent audit of C1: marked-defect entropy bound

Date: 2026-10-07. Problem 9700042 / AMR-096-0042, rank 937.

## Verdict and exact scope

**ACCEPTED PARTIAL.** The frozen C1 proof establishes

\[
\limsup_{q\downarrow0}\frac{1-v(1-q)}{\sqrt{2q}}\leq\frac e2
\]

for the directed square-grid maximum-flow model on the cited Aldous page. The argument covers all dual cuts, including nonmonotone ones. The primary page's stated existence of the deterministic L1 flow-density limit is an external premise. No continuum-limit interchange, exact Hammersley shape, historical acceptance, or numerical experiment is used as a proof premise.

This is not a solution of the constant-1 asymptotic. This audit does not certify any separately reported lower bound, any C2 result, publication novelty, or an exhaustive current-literature status claim. The accepted result is an upper bound on the deficit, not by itself a two-sided square-root asymptotic.

There is no mathematical failure requiring a correction. A separate optional patch expands the planar-dual justification and removes the ambiguous phrase “genuinely new,” which could be read as a novelty claim. The frozen original is unchanged. The expanded proof and this report make explicit the treatment of four-valent dual interfaces that was compressed in the original.

## Input pins and reproducibility

The author confirmed these C1 files were frozen and unchanged since assignment. Independently copied audit inputs have the following SHA-256 values:

- `TURN_C1_MARKED_DEFECT_BOUND.md`, 9957 bytes: `f38d6ac74d3abad6f7675a13429f09e0bc6fc8151c137284e4655e8fc0c39120`.
- `verify_resume_turn1.py`, 3644 bytes: `83706824102f00baca75122ae87c9d45723c4ffa18f58df9eb77e0321c37c736`.
- `TURN_C1_CHECKS.json`, 3971 bytes: `022566a4288c89010aa15923c84cc802e9cb0627937eed44144e818905df3b08`.

Line references below refer to that exact original proof. Audit artifacts and hashes are listed in `AUDIT_MANIFEST.json`. Reruns used copies, so the frozen inputs and original author outputs were not overwritten.

## Primary-source model gate

The live primary page was independently opened and fetched on 2026-10-07:

[David Aldous, A discrete Hammersley process as an extreme case of oriented percolation flows](https://www.stat.berkeley.edu/~aldous/Research/OP/hammersley_flow.html).

The fetched HTML is 3576 bytes, SHA-256 `1c3078bb05b25554b7ab7bc12e6d8567b777407b6c6ad24fecfc89715088a301`, and matches the author's source bytes. It specifies independent Bernoulli bond capacities on a finite square, positive-coordinate primal orientation, the two boundary arcs used in C1, normalization by 2n, and L1 convergence to a deterministic v(p). Its stated conjecture is the constant-1 normalized deficit asymptotic. Thus C1 lines 36–45 and 181 use the correct finite model and limiting normalization. In particular, the two boundary corner exclusions are essential and are correct here.

The page's subsequent continuum argument is expressly heuristic. None of those heuristic identities is imported into this audit or the accepted proof.

## 1. Directed planar duality and boundary terms

### Exact edge identification

Set N=n−2. A reflected dual vertex (x,y) denotes the physical face with lower-left corner (x,n−2−y). The costly east dual step crosses

\[
((x+1,n-2-y),(x+1,n-1-y)),
\]

and the costly north dual step crosses

\[
((x,n-2-y),(x+1,n-2-y)).
\]

These maps are injective on unoriented dual edges. Reverse dual arcs cost zero; assigning the primal capacity to both directions would be wrong for a directed cut.

The outer primal boundary changes from prescribed source side to prescribed sink side only on e_L and e_B. All other outer-boundary edges have both endpoints prescribed to the same side. Both distinguished edges point outward from the source side. Their capacities must therefore be added exactly once. For n=2 there is one bounded face and no internal dual step, so T_0=0 and V_2=c_L+c_B, as claimed.

### Every primal cut gives a dual path, including ambiguous faces

Take any feasible primal vertex cut S. For every primal edge whose endpoints have different cut labels, draw its crossing dual segment, directed with S on its right in the original physical embedding. Include two separate outer endpoints at the midpoints of e_L and e_B.

At every bounded face, this directed interface graph has equal indegree and outdegree. This follows by reading the binary labels of the four primal corners cyclically: the numbers of transitions of the two types agree. A checkerboard face has two incoming and two outgoing dual segments, so it causes no failure of this balance argument. At the first outer endpoint there is one outgoing segment; at the second there is one incoming segment. Every other dual vertex is balanced. Consequently a directed route must connect the first endpoint to the second. For example, otherwise the set reachable from the first endpoint has no outgoing arc, contradicting the sum of its outdegree-minus-indegree balances.

Each edge of that route crosses a mixed primal edge once after directed-trail extraction. Its cost is the primal capacity when the primal edge points out of S, and zero when it points into S. In reflected coordinates these are exactly the east/north costly arcs and west/south zero-cost arcs. Hence the route costs at most the entire directed cut. Deleting loops from its internal dual walk preserves endpoints and cannot increase cost. Therefore every cut costs at least c_L+c_B+T_N.

### Every simple dual path gives a primal cut

Embed a vertex-simple dual path in the face centers and extend its ends through the two forced outer crossings. It is a non-self-intersecting crosscut of the primal square, never meeting a primal vertex. The planar separation theorem splits the square into two sides. The side containing the source boundary arc is on the right when the curve is traversed from e_L to e_B. Its primal vertices form a feasible cut. A primal edge crosses the curve exactly when its endpoints are on opposite sides. Its contribution to the directed cut is the costly forward dual contribution, or zero for a reverse contribution, plus the two forced capacities. This proves the reverse inequality.

Thus equation (1) is correct for arbitrary nonnegative capacities, and in particular for the Bernoulli model. Zero-cost cycles are harmless: among shortest walks choose one with least length, which is vertex-simple.

## 2. Defect representation and marked-edge independence

For any simple dual path, net displacement is (N,N). If b is its number of west/south steps, its east/north count is 2N+b. If k of those forward crossings are closed, its cost is 2N+b−k. This proves equation (2), and substituting n=N+2 proves equation (3). The finite all-open flow is 2n−2, not 2n; the difference vanishes after normalization.

If D_N≥d>0, a minimizing simple path yields k≥ceil(d) and b≤k−d≤k. Its k marked closed forward edges are distinct because a vertex-simple path cannot traverse the same unoriented edge twice. For a fixed valid list the event that all marked edges are closed has probability q^k. Their positions and orientations identify distinct primal edges by the preceding edge map. No factor involving unmarked edges is required, and no independence between two different lists is asserted.

Deleting unmarked vertices from a coordinate sequence cannot increase negative variation: (a−c)_+≤(a−b)_++(b−c)_+. Applying this repeatedly, then including the two endpoints, proves that each coordinate of the marked-start list has negative variation at most the path's total backward count b. Marking starting vertices rather than endpoints is consistent with that subsequence argument.

## 3. Coordinate count

Equation (4) is valid. For t negative increments, choose their t locations among k+1. The positive magnitudes, with total B≤k, have binomial(k,t) possibilities by the positive-composition identity, including the t=0 convention. Conditional on these magnitudes, the k+1−t remaining increments are nonnegative and sum to N+B. Their count is binomial(N+B+k−t,k−t), bounded by binomial(N+2k−t,k−t). Counting tuples that exit [0,N] only enlarges the result. All k+1 increments cannot be negative when the total displacement is N≥0.

The ratio identity at lines 97–99 is exact. For every j≥0, (k−j)/(N+2k−j)≤k/(N+2k), so the displayed falling-factorial estimate has the correct direction. The diagonal binomial sum is bounded by the full nonnegative product (1+sqrt(r))^(k+1)(1+sqrt(r))^k. Therefore equation (5), including its exponent 2k+1, is correct.

For two coordinates and k forward orientations, the candidate counts at most 2^k A(N,k)^2 lists. Invalid edges, repeated edges, and unrealizable paths can be discarded before applying probability q^k; using the larger combinatorial count remains an upper bound. This distinction prevents the common incorrect use of q^k for a list containing repetitions. Equation (6) and its exponent 4k+2 are correct.

The actual simple-path union is finite, with k≤(N+1)^2−1. Extending the nonnegative majorant to infinity is legitimate. Convergence is not asserted for arbitrary q; it is established in the small-q range subsequently used.

## 4. Geometric tails and limit order

Fix eta∈(0,1), epsilon>0 before choosing q. Set a and theta as in equations (7) and (8). Conditions a<eta and theta<1 hold for all sufficiently small positive q.

Writing rho=(1+epsilon)^−2, equation (9) follows from binomial(N+2k,k)≤[e(N+2k)/k]^k, N+2k≤(1+2eta)N, k/(N+2k)≤eta, and k≥aN. There is no lost factor of 2 or squared slack. Equation (10) uses (1+sqrt(k/(N+2k)))^(4k+2)≤4·16^k, which gives 32e²q(eta^−1+2)² after including the factor 2q.

More explicitly, for every N≥1 the total upper bound is at most

\[
\frac{(1+\sqrt\eta)^2\rho^{\lceil aN\rceil}}{1-\rho}
+\frac{4\theta^{\lfloor\eta N\rfloor+1}}{1-\theta}.
\]

Empty first ranges cause no problem. This tends to zero exponentially for each fixed eligible q. Since 0≤D_N≤2N,

\[
\frac{\mathbb E D_N}{2N}\leq\frac a2+\Pr(D_N\geq aN),
\]

so the expected-deficit conclusion follows. The exact normalization can also be read as

\[
1-\frac{\mathbb E V_n}{2n}
=\frac{\mathbb E D_{n-2}}{2n}+\frac{4-\mathbb E(c_L+c_B)}{2n}.
\]

The bounded boundary term vanishes and (n−2)/n→1. The cited fixed-q L1 limit then implies the bound on 1−v(1−q). Only after this n→infinity step is q sent to zero, with eta and epsilon still fixed; eta and epsilon are sent to zero last. There is no unsupported uniformity in q and no exchange of the small-density and large-volume limits.

## 5. Independent finite diagnostics

All checks passed. They are implementation and finite-lemma diagnostics, not evidence replacing any proof above.

- The frozen author checker was rerun in a separate directory. Its JSON output is byte-for-byte equal to the pinned original: 4, 64 and 16,384 exhaustive relevant-edge configurations for n=2,3,4; 150 seeded n=5,6 cases; and 20 small coordinate counts.
- A fresh checker imports no author code. It compares Edmonds–Karp max flow on the full primal graph against independently coded dual shortest paths using unreflected face coordinates. It exhausts all 16 n=2 and 4,096 n=3 full-primal configurations, including irrelevant outer-boundary edges.
- It compares another 950 seeded cases for n=4,5,8,15,30, alternating Bernoulli capacities and capacities in {0,1,2,3,4}. The Bernoulli path witnesses additionally check step counts and marked-subsequence variation.
- An independent dynamic program checks 216 coordinate counts, N=1,…,12 and k=1,…,18, against both estimates (4) and (5).
- All 4,096 configurations of the 12 internal dual edges at N=2 are enumerated. Exact rational event probabilities at q=1/1000 and 1/1000000, for thresholds d=1,2,3,4, satisfy the finite list-count bound. The check separately reproduces a four-closed-edge counterexample to the monotone-only reduction.
- Numerical log-space samples verify the constants in (9) and (10). These samples are not a uniform inequality proof; that proof is given above.

Run `python check_independent.py` from this directory to regenerate `INDEPENDENT_CHECKS.json`. The author rerun script resides in `rerun/`.

## 6. Bounded source/novelty check

The [current Aldous index](https://www.stat.berkeley.edu/~aldous/Research/OP/index.html) still places this item among open research problems. The index also cautions that its updates may omit relevant work, so its categorization is not a complete present-day status certification.

Targeted searches used combinations of the exact problem title, “oriented percolation flows,” Aldous and Lenderman, Hammersley and maximal flow, near-one flow asymptotics, and the proposed e/2 constant. The bounded pass found the primary problem page and related but nonidentical Hammersley, last-passage, and undirected-flow literature; it did not identify a source stating this exact e/2 result or a resolution of the exact conjecture. The linked Aldous–Diaconis landing page was opened, but no readable theorem text was returned; no result from that work was used. Search queries and source inspection limits are recorded separately.

This establishes neither originality nor absence of a resolution. The phrase “genuinely new” in line 25 is therefore best replaced with “derived here.” The accepted mathematical upper bound does not depend on the novelty outcome.

## Required downstream limits

1. Label this result a partial upper bound with constant e/2. Do not label the original conjecture solved.
2. Do not combine this verdict with an unaudited lower bound or C2 argument as if they were verified here.
3. Preserve the exact original pins if quoting this acceptance. Any subsequent mathematical changes require review of the changed bytes.
4. The separate clarification patch is optional for correctness but recommended for a self-contained presentation and novelty-safe wording.
5. No publication, repository mutation, or queue edit was performed. Source HTML is retained only as local inspection evidence and is not part of a publication deliverable.
