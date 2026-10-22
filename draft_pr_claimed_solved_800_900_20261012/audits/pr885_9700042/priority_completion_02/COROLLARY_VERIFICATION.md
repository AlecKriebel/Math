# Adversarial verification of the old-input corollary

This verification was undertaken after receiving the proposed mechanism and reading preserved derivations. It is independent checking, not independent discovery. Its operative primary source is Basdevant--Gouere--Theret, arXiv:2106.12266v1, Sections 2.2--2.5 and 3.3--3.4. The actual 967612-byte PDF has SHA256 `9d78c8dd86aaa62dbaa7bfcaf40195c901c3cc9dee025bffd4a6e29af64339ba`. Exact equations below refer to that v1, not to an unexamined journal PDF.

## Contract and lower bound

The supplied exact finite dual on `Q_N={0,...,N}^2` charges 0 for marked NE traversals, 1 for unmarked NE traversals, and 0 for every reverse traversal. With independent mark probability q and corner passage value T_N, write `D_N=2N-T_N`. Conservation of coordinate sum gives `D_N=K-B` on any minimizing path, where K counts marked forward steps and B counts backward steps. Nonnegative costs and minimum length among minimizers give a simple path. Consequently `0<=D_N<=2N`.

Extend all outgoing marks independently outside the square. A site is Y-open when either outgoing NE edge is marked. The pairs of edge variables at different tails are disjoint, so Y is iid Bernoulli with `r=2q-q^2`. Let A_r(M) be the longest strictly coordinate-increasing chain of open sites in `[0,M)^2`, with an open origin allowed. This is the site score in the old source with `d1=2,d2=0`.

A strict chain in `[0,N)^2` can select one marked outgoing edge at each tail and join them monotonically. Each following tail is at least one unit larger in both coordinates, and every selected edge lies in Q_N. Thus `A_r(N)<=D_N` exactly. BGT Lemmas 5 and 10 and its Section 3.4 planar constant identification give `sigma_r=lim_M E[A_r(M)]/M` and `sigma_r/sqrt(r)->2`. The stronger exact Bernoulli-chain formula is unnecessary here.

## Upper encoding and the two cancellations

Set `M=N+1`. List all Y-open vertices of the simple target minimizer except the terminal and origin, in visit order, as b(1),...,b(p). Set b(0)=0 and virtual b(p+1)=(M,M). All actual vertices are strictly below this virtual endpoint. Use exactly the source's greedy strict subsequence; let a be its number of gaps, ell_k its intervening-site counts, and `L=sum ell_k`. Then `p=a-1+L`.

The origin indicator I0 occurs in both inequalities `K<=p+I0` and `A_r(M)>=a-1+I0`. The first uses one forward departure per tail on a simple path, including double-open tails. The second includes the origin precisely when it is open. Hence

`D_N-A_r(M)<=L-B`. (1)

For each nonlast gap between strictly ordered real anchors u,w, let B_k and K_k count the actual segment's backward steps and marked forward steps. A monotone competitor can collect a first reward if u is open: strict integer separation ensures either outgoing marked edge fits inside the rectangle [u,w]. If a_k is that open indicator, local optimality and the one-reward-per-tail count imply

`|w-u|_1+B_k-K_k <= |w-u|_1-a_k`, `K_k<=ell_k+a_k`, and therefore `B_k<=ell_k`.

A splice may intersect the rest of the path, but would still be an admissible walk; removing cycles cannot increase its cost. Thus local optimality does not require globally disjoint replacements. Any overshoot of the last intervening site beyond the next anchor in the other coordinate is at most B_k and hence ell_k. This is stronger than Lemma 19 Item 4, which allows `2(ell_k+1)`. The last block instead satisfies that condition geometrically, since every real coordinate is at most N<M. Empty blocks also satisfy it.

Use the source's individual-increment quantity

`X=sum_(k,i) |g(k,i)_(j_k)| + sum_(k,i) (g(k,i)_(other))_-`.

The distinguished-coordinate prefix has nonpositive net displacement. Its absolute coordinate variation is at most twice its backward variation, and sampled absolute increments are no larger. In the other coordinate, the negative part of each sampled increment is bounded by that subpath's actual backward variation. The prefixes for different blocks are disjoint in traversal time. Thus, even when distinguished directions vary between blocks,

`X<=2B` and `2(D_N-A_r(M))<=2L-X`. (2)

This confirms the correct stronger per-increment X, not the negative part of a net sum. No claim `X<=B` is made or needed.

## Literal numerical-sum inclusion

For each fixed delta>0, the event `D_N>A_r(M)+delta M sqrt(r)` produces distinct open sites and encoding satisfying:

1. `sum ||h(k)||_1=2M` (old Item 1).
2. No vertical variables (Item 2 is vacuous).
3. The distinguished prefix sum is nonpositive (Item 3; the old sum drops its indicator).
4. The bound verified above.
5. `0<=-X+1+2L-t M sqrt(r)` with `t=2delta`, by (2).

For a fixed valid list, the probability its p sites are open is exactly `r^p`. The origin need not be prescribed. This is precisely the numerical m=0 weight of (33). It does **not** require the actual anchors to have zero double-open sites: it prescribes zero double-open conditions. Simplicity supplies distinct tails. The numerical sum may include extra invalid encodings; this only increases it. The named ordinary-FPP event and its geodesic reward count are not prerequisites for this numerical inclusion.

There is a real notational point in the old source: its event uses an edge-parameter threshold, while the displayed W expression uses the grouped site parameter. To avoid claiming an incorrect literal same-eta substitution, define the numerical Item 5 threshold explicitly as `t M sqrt(r)`, as above. The printed Chernoff multiplication then has exactly the following specialization. With `K(s)=(1+exp(-s))/(1-exp(-s))`, beta=2gamma and alpha>gamma sqrt(r), put

`H=r e^2 exp(2gamma sqrt(r)) K(beta sqrt(r)) K(gamma sqrt(r))`,

`J=r exp(2gamma sqrt(r)+2alpha) e^2 K(alpha) [K(gamma sqrt(r))+K(alpha-gamma sqrt(r))]`.

The fixed-encoding sum is at most

`r^-1 exp(2+alpha+(2beta-alpha t)M sqrt(r)) H^a J^L`.

I checked this directly against the source's multiplier calculation: Item 1 contributes `exp(beta sqrt(r)(2M-sum||h||))`; Item 4 contributes `exp(gamma sqrt(r)sum(2ell+2+h_other-sum g_other))`; Item 5 contributes `exp(alpha(1+2L-t M sqrt(r)-X))`. Summing distinguished g gives K(alpha); summing other g gives at most the displayed two K terms; summing h gives the beta/gamma K factors. The source's e^2 factors are harmless overestimates of the now-vacuous vertical constraint. The threshold enters only through `exp(-alpha t M sqrt(r))`. This independently validates using r units without a new probabilistic kernel or a q-dependent hidden limit exchange.

Choose beta=2gamma with `4e^2/(beta gamma)=1/16` and alpha t-2beta=1. Then `H->1/16`, `J=O(sqrt(r))`. For all sufficiently small fixed r, H<=1/8, J<=1/2 and alpha>gamma sqrt(r). Summing two possible distinguished directions per gap and all ell vectors leaves `sum_(a>=1)(1/2)^a=1`. Thus

`P{D_N>A_r(N+1)+delta(N+1)sqrt(r)} <= e^(2+alpha)/r * exp(-(N+1)sqrt(r))`. (3)

This is the already published numerical counting mechanism specialized to its m=0 slice. It is not a consequence of identifying the target time constant with the source's symmetric-FPP time constant.

## Expectations, limits, scope

At fixed sufficiently small r, (3), `D_N<=2N`, and `A_r>=0` give

`E[D_N]<=E[A_r(N+1)]+delta(N+1)sqrt(r)+2N P{the event in (3)}`.

Let N tend to infinity first. Together with the lower comparison this gives `sigma_r<=lim E[D_N]/N<=sigma_r+delta sqrt(r)` whenever the supplied flow limit exists. Then let q decrease to zero and delta decrease to zero, using r/(2q)->1. The supplied finite identity `V_n=c_L+c_B+T_(n-2)` and bounded terminal terms convert this into `1-v(1-q)~sqrt(2q)`.

No unsupported model-comparison step remains in this corollary. This audit did not rederive the original finite duality or certify every proof in the old source. Its independently checked conclusion is conditional on that supplied duality and fixed-q limit, exactly as stated. The positive source evidence supports old-input derivability; it does not establish an older explicit statement, historical recognition, earliest discoverer, or a current-openness certificate.
