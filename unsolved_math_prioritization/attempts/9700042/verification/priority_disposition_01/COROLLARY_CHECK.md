# Independent priority/disposition report: PR885 / PID9700042

This is an initial disposition, not a final whole-preprint CLEAR. The original candidate remains at its frozen 5/5 proof-search status. No new original proof-search allowance is asserted or spent here. No other current priority-family folder or candidate/audit verdict was read.

## Decision

**The 2021 BGT public paper supplies a complete corollary of its existing strict-chain asymptotics and its unchanged universal numerical counting sum (33), once routine target-specific path bookkeeping is supplied.** Its named symmetric-FPP theorem does not directly identify the target model. The corollary does not need a new probabilistic kernel, a new interchange-of-limits argument, a weighted-backstep theorem, or a general extension of BGT's central comparison lemma.

This is meaningful adverse priority evidence against presenting the target asymptotic as a substantial new asymptotic-discovery theorem. It is **not** evidence that BGT stated the canonical flow problem, that anyone previously recognized this corollary, or that the original conjecture's public open-status premise is demonstrably false. Therefore do not automatically change the queue status to `already_solved`. A short, explicitly attributed corollary/application note could be honest; a paper whose novelty is a new central detour estimate would overstate what remains new. Whether such a short note is worthwhile under the user's novel-contribution scope requires the parent disposition and final independent checks.

## Source and prior-status precision

The mathematical inputs below were checked in the supplied original 28-page arXiv:2106.12266v1 (23 June 2021), not merely an abstract or summary. The relevant source is Anne-Laure Basdevant, Jean-Baptiste Gouere and Marie Theret, *First-order behavior of the time constant in Bernoulli first-passage percolation*. Publication metadata identifies the AAP 2022 version, 32(6), 4535--4567, DOI [10.1214/22-AAP1795](https://doi.org/10.1214/22-AAP1795), as also listed by the [authors' institute](https://www.idpoisson.fr/en/publications/). The final published mathematical text was not available through the checked wrapper. Thus exact equation-number and unchanged-text assertions here refer to v1; publication metadata alone does not certify that every equation survived unchanged in the journal version. The public 2021 v1 already suffices for the priority limitation established here.

Checked old inputs:

- BGT Sections 2.2--2.3: strict coordinatewise chains of independent open sites; mean score `sigma_r`; Lemma 10 and the planar Hammersley constant in Section 3.4 give `sigma_r((1,1))/sqrt(r) -> 2`.
- BGT Section 2.5, especially (19)/(20): the geometric quantity below; the source's negative part is per increment.
- BGT Section 3.3, Lemma 19 and (33): a numerical sum over encoded open-site sequences, with weights `binom(h-1,m) r^(m+h-1+L)` and indicators of Items 1,2,4,5. The displayed Chernoff calculation bounds that sum, for every fixed positive threshold parameter eta and all sufficiently small r, by `C_eta/r * exp(-n sqrt(r))`. This numerical estimate can be applied to any event producing sequences with those constraints; it is not limited to the source's original event.

## Exact corollary and finite comparison

Let each northeast edge in the integer square `Q_N={0,...,N}^2` be a reward edge independently with probability q. A forward reward edge costs zero, another forward edge costs one, and a reverse southwest step costs zero. Let `T_N` be the minimum corner-to-corner cost and `D_N=2N-T_N`.

Extend the reward environment independently to all northeast edges of the lattice. A vertex x is tail-open if at least one of `x -> x+e_1`, `x -> x+e_2` is a reward edge. These vertex indicators are independent, with

`r=1-(1-q)^2`.

Let `A_r(a)` be the maximum length of a strictly increasing coordinatewise sequence of tail-open vertices in `[0,a)^2`, allowing the origin as its first term. This is exactly BGT's site score `S_r^D((a,a))`, and also their bond score in the case d1=2,d2=0. A double-open tail still contributes at most one member to a strict chain.

For each delta>0, there are `r_0(delta)>0` and finite `C_delta` such that, for r below this threshold and all N>=1,

`P{D_N > A_r(N+1) + delta (N+1) sqrt(r)} <= (C_delta/r) exp(-(N+1)sqrt(r)).`  (C)

Also, deterministically,

`A_r(N) <= D_N`.  (L)

### Proof of the lower comparison (L)

At each tail in a strict chain choose one available northeast reward edge. Strict increases of both tail coordinates ensure the chosen edge head is coordinatewise no larger than the next tail. Since each tail has both coordinates <N, every chosen edge lies in Q_N. Join these edges by northeast steps to form a corner-to-corner monotone path. Its deficit is at least the chain length.

### Simple geodesic, endpoint, and encoding

Choose a minimum-cost path of minimum length among minimizers. All step costs are nonnegative and deleting a cycle cannot increase cost, so this path is simple. Let K be its number of forward reward edges and B its number of backward steps. Conservation of total coordinate displacement gives

`D_N=K-B`.

Set `n=N+1` and artificial terminal `z=(n,n)`. The actual endpoint is `z^-=(N,N)`, and every vertex of the confined path is strictly below z in both coordinates. Thus BGT's nice-path convention holds exactly; no upper-bound clipping argument is needed.

List all tail-open path vertices except the actual terminal and the origin, in traversal order, as `b(1),...,b(p)`; set `b(0)=0` and `b(p+1)=z`. Use BGT's greedy strict subsequence `b(i_0),...,b(i_h)`, with `i_0=0`, `i_h=p+1`. For block k define `ell_k=i_(k+1)-i_k-1`, `c(k,i)=b(i_k+i)` for i from 0 through ell_k, `h(k)=c(k+1,0)-c(k,0)`, and `g(k,i)=c(k,i)-c(k,i-1)`. Let `L=sum ell_k`, so `p=h-1+L`.

If ell_k>0, choose `j_k` for which the last non-anchor tail satisfies `c(k,ell_k)_(j_k) <= c(k,0)_(j_k)`; such a coordinate exists by greedy construction. If ell_k=0 choose either coordinate. Define precisely the source's geometric quantity

`X=sum_k sum_i |g(k,i)_(j_k)| + sum_k sum_(j != j_k) sum_i (g(k,i)_j)_-`.

### The stronger target reward count cancels the weaker backward penalty

Let `a_0` be one if the origin is tail-open and zero otherwise. A simple target path can collect at most one forward reward from any visited tail. Therefore

`K <= p+a_0`.

The `h-1` real greedy anchors form a strict chain; include the origin also when it is open. Consequently

`A_r(n) >= h-1+a_0`, and hence `D_N-A_r(n) <= L-B`.  (R)

This is the decisive target-specific improvement over symmetric bond FPP. Double-open sites do not require an extra reward count because a simple directed traversal can leave a vertex forward at most once.

For each block's distinguished coordinate, the prefix ending at its last non-anchor has nonpositive net displacement in that coordinate. Its total forward movement is therefore no greater than its total backward movement. The triangle inequality gives `sum_i |g_(j_k)| <= 2 B_(k,j_k)`. For the other coordinate, `sum_i (g_j)_- <= B_(k,j)`. Prefixes in different blocks are disjoint in traversal time. Thus

`X <= 2B`.  (G)

Combining (R) and (G),

`2(D_N-A_r(n)) <= 2L-X`.  (E)

The factor two in (G) is real; replacing it by one without the reward-count improvement would be an error. The present argument does not make that replacement.

### Exact fit to the old sequence constraints

Take the m=0 numerical summand of BGT (33), with d1=2,d2=0 and endpoint direction `(1,1)`:

1. `sum_k ||h(k)||_1=2n=n||(1,1)||_1`, so Item 1 holds with equality.
2. There are no vertical coordinates; Item 2 is vacuous.
3. The chosen distinguished coordinate gives Item 3, although the published sum does not use its indicator.
4. For a nonterminal block, the actual subpath joins strictly ordered real anchors within Q_N. Its cost is `||h(k)||_1+B_k-K_k`. A northeast competitor can collect a reward immediately from its starting anchor if that anchor is open; strict coordinate increase ensures that reward edge stays within the rectangle between the anchors. Thus its cost is at most `||h(k)||_1-a_k`. Simplicity gives `K_k<=ell_k+a_k`, so `B_k<=ell_k`. If the last non-anchor overshoots the next anchor in the other coordinate, the return costs at least that many backward steps. Therefore `c(k,ell_k)_j-c(k+1,0)_j<=ell_k`, stronger than Item 4's allowance `2(ell_k+1)`. In the terminal block, every real tail has coordinate <=N<n, so Item 4 follows directly. Empty blocks cause no difficulty.
5. On the event in (C), (E) gives `-X+2L>2 delta n sqrt(r)`. This implies the old Item 5 with m=0 and eta=`2delta`, whose right side allows the additional constant +1.

Here **m=0 does not assert that the actual anchors have no double-open sites**. We use the numerical m=0 summand, with no prescribed double-open sites. For a fixed distinct tail sequence the probability all its p tails are open is exactly `r^p`, which is exactly that summand's weight. Double-open anchors remain allowed. The original self-avoiding path guarantees distinct tails; extending the ensuing numerical sum to invalid encodings only enlarges it.

Thus the union bound for the anomalous target event is bounded by a subset of the nonnegative m=0 terms of the old sum (33), and hence by the complete sum already estimated there. This proves (C) with the published numerical kernel and unchanged parameter choice. No model identification with symmetric FPP is used.

For a checkable extraction of that numerical assertion, put `K(s)=(1+exp(-s))/(1-exp(-s))`, choose `beta=2gamma`, `4e^2/(beta gamma)=1/16`, and `alpha eta-2beta=1`. The m=0 fixed-block bound printed after (33), with d1=2,d2=0, is

`W(h,ell,j) <= e^(2+alpha)/r * exp((2beta-alpha eta)n sqrt(r)) * H(r)^h * J(r)^L`,

where

`H(r)=r e^2 exp(2gamma sqrt(r)) K(beta sqrt(r)) K(gamma sqrt(r))`,

`J(r)=r exp(2gamma sqrt(r)+2alpha) e^2 K(alpha) [K(gamma sqrt(r))+K(alpha-gamma sqrt(r))]`.

Here `H(r)->1/16` and `J(r)=O(sqrt(r))`. For sufficiently small r use `H<=1/8`, `J<=1/2`. Summing the two choices of distinguished coordinate per block multiplies by `2^h`; summing each ell>=0 multiplies by at most `2^h`. The remaining `sum_(h>=1) (1/2)^h` is one. This is exactly the source calculation restricted to m=0, giving `e^(2+alpha)/r * exp(-n sqrt(r))`. No new summation estimate is introduced. BGT's event notation alternates between the edge parameter and the tail-open parameter at the threshold; a fixed multiplicative rescaling of eta absorbs this. The displayed numerical extraction above explicitly uses the threshold `eta n sqrt(r)` and removes any notational ambiguity.

### Expectations, order of limits, and the flow normalization

`0<=D_N<=2N`, while `A_r` is nonnegative. Therefore (C) and (L), first letting N tend to infinity at **fixed** small r, give

`sigma_r <= liminf E[D_N]/N <= limsup E[D_N]/N <= sigma_r+delta sqrt(r)`.

Letting r tend to zero and then delta tend to zero, and using the old `sigma_r/sqrt(r)->2`, yields

`lim_(q->0) (lim E[D_N]/(2N))/sqrt(r) = 1`.

The supplied exact finite dual identity is `V_n=c_L+c_B+T_(n-2)`, with bounded terminal contributions. Consequently `1-v(1-q)=lim E[D_N]/(2N)`. Since `r=2q-q^2`, this is exactly

`1-v(1-q) ~ sqrt(2q)`.

The finite dual identity itself is an input of this disposition and has not been independently rederived here. The corollary fully resolves the supplied exact dual; promoting the canonical original-model result still requires the parent to retain its independent finite-duality verification.

## Boundary and falsification ledger

| Issue | Checked resolution / remaining limitation |
|---|---|
| Direction | Only northeast zero edges create rewards; southwest steps create none. This is why the sharper tail count applies. |
| Cycle rewards | Nonnegative costs permit a simple minimizing path; repeated tails cannot artificially produce independent rewards. |
| Origin | Included in chain iff open; the same `a_0` occurs in both reward count and chain lower bound and cancels exactly. |
| Actual terminal | Excluded from visited tail list; it is `(N,N)`, with artificial strict terminal `(N+1,N+1)`. No terminal reward is charged to the path. |
| Boundary edges | Independent extension may make boundary tails open; this only enlarges the upper chain score. For nonterminal blocks a strict real successor forces both start coordinates <N. Lower-score tails lie in `[0,N)^2`, so all selected reward edges are genuine square edges. |
| Confinement | Actual paths and local monotone competitors remain inside Q_N. No infinite-volume geodesic-confinement assertion is invoked. |
| Double-open tails | One reward per simple forward departure; m=0 means zero prescribed double marks in the numerical union bound, not an event excluding doubles. |
| Empty chain/block | h=1 and ell=0 are admitted; artificial terminal ensures greedy termination. N>=1 suffices. N=0 is irrelevant to the limit. |
| Signs | X uses per-increment negative parts, visually confirmed in the source. |
| Order of limits | N first at fixed r, then r down to zero; exponential tail makes the expectation comparison valid. No interchange is assumed. |
| Exact original dual | Supplied input; not freshly checked by this agent. |
| Prior recognition | No evidence found or claimed that the canonical corollary was previously stated; mathematical derivability from old inputs is weaker than documented prior resolution. |
| Published-version identity | Metadata verified; equation identity checked only in 2021 v1. |

## Promotion recommendation

Retain the finite corollary (C), its explicit attribution to BGT's numerical bound, and the precise original-duality input as the strongest checked artifact. Obtain adversarial review of the one-reward-per-tail cancellation and the m=0 interpretation before any public promotion. An attributed short application note may be useful; calling this a new central first-order comparison would not be justified. This report alone does not authorize a paper, queue reclassification, release, or final CLEAR.

The accompanying dependency-free finite falsification check passed 8,224 exhaustive N=1,2 environment/extension cases and 3,000 seeded random N=3,4,5 cases. It checked the exact per-increment X, local backward-step bounds, origin cancellation, and both finite score comparisons. The selected minimizing paths included 423 cases with backward steps, so the verification was not confined to monotone paths. Finite verification is supporting evidence for bookkeeping only; the proof above and the old counting sum supply the asymptotic conclusion.
