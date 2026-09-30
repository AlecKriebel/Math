# Vanishing-density high-degree seeds can defeat any fixed rate disadvantage

**Problem:** 30003677 / OWR-15962-003. **Candidate affirmative existence result in the growing-seed regime explicitly allowed by the source.** Two approaches were considered. Independent review is pending. Priority is unestablished.

## 1. Exact source scope

The complete primary contribution is Mia Deijfen, joint with Daniel Ahlberg, Remco van der Hofstad and Svante Janson, *Competing first passage percolation on the configuration model*, [OWR 57/2017, printed pp. 3442–3443](https://ems.press/content/serial-article-files/46721). The model pairs i.i.d. vertex-degree half-edges uniformly and lets two infections spread irreversibly at fixed positive per-edge rates. The final paragraph explicitly allows initial numbers growing with the graph size and degree-based choices; it asks whether a weaker type can capture a positive fraction from one or more high-degree vertices against a stronger type at a small-degree vertex.

The same question appears in §5 of [Ahlberg–Deijfen–Janson, arXiv:1711.02902 (2017)](https://arxiv.org/abs/1711.02902), subsequently published in Random Structures & Algorithms, DOI [10.1002/rsa.20846](https://doi.org/10.1002/rsa.20846). Its precise assumptions (A1)–(A2) include finite second moment, minimum degree at least two, and a positive probability of degree greater than two. The full preprint was obtained and read. Its exponential passage-time convention gives each edge independent type-specific exponential traversal times; traversing an already occupied vertex cannot recolour it.

The result below uses **a growing but sublinear number of seeds**, every one of whose degrees tends to infinity. The initial fraction of incident half-edges also tends to zero. Selection uses only the degree list before the matching and passage times are sampled. Thus the conclusion is not obtained by initially infecting a positive fraction, isolating the competitor after seeing edges, or choosing seeds after seeing favourable edge weights.

This answers the source's existential possibility question in that permitted regime. It does not determine a single-hub or fixed-number-of-hubs threshold, an optimal seed budget, or a result against an adversarial starting vertex chosen after inspecting the graph or passage times. Those stronger problems are not silently treated as solved.

## 2. The theorem and model

Let `D` be any integer-valued law satisfying

`P(D≥2)=1,   E[D²]<∞,   P(D≥k)>0 for every integer k`.

In particular its support is unbounded and `P(D>2)>0`. Fix any `d₀` with `P(D=d₀)>0`, and fixed rates `0<λ₁<λ₂<∞`.

For each `n`, sample `D₁,…,D_n` independently with law `D`. If their sum is odd, independently choose a uniform vertex and increase its degree by one; write `d_i` for the resulting degree list. This is the standard parity repair used in the primary paper. Conditional on these degrees, sample a uniform perfect matching of the half-edges, giving the configuration multigraph. Independently give each edge `e` weights `X₁(e)~Exp(λ₁)` and `X₂(e)~Exp(λ₂)`, independent across edges and types. Parallel edges are separate transmission channels; loops make no new infection.

**Theorem.** There are deterministic integer thresholds `k_n→∞` and deterministic times `t_n→∞`, depending only on `D,d₀,λ₁,λ₂`, with `t_n=o(log n)`, such that the following holds. Start type 1 at

`S_n={i:d_i≥k_n}`

and type 2 at a uniformly chosen vertex `W_n` of degree `d₀`, using randomness independent of the matching and weights. On the negligible event that no such vertex exists, choose any non-type-1 vertex if available; any convention on this event is immaterial. Then

1. `|S_n|/n→0` in probability and `|S_n|→∞` in probability;
2. `Σ_(i∈S_n)d_i / Σ_i d_i →0` in probability;
3. if `N₁(n,t)` counts type-1 vertices by time `t`, then

   `N₁(n,t_n)/n→1` in probability.

Consequently type 1 ultimately occupies `1−o_P(1)` of all vertices despite its smaller rate. In particular it captures a strictly positive fraction with probability tending to one. The theorem asserts the existence of slowly growing deterministic schedules; it does not supply a sharp asymptotic formula or efficient algorithm for their growth.

## 3. A deterministic path protection lemma

Consider any finite multigraph with fixed nonnegative edge traversal times for each type and disjoint initial sets `S` and `{w}`. Let

`B₂(T)={z:dist_(X₂)(w,z)≤T}`

be the **unopposed** type-2 first-passage ball. Every vertex that has acquired type 2 by time `T` lies in this ball: following its actual infection ancestors gives a type-2 path from `w` whose total traversal time is at most `T`.

Suppose there is a path `P` from some `s∈S` to `v` such that

`Σ_(e∈P)X₁(e)≤T` and `V(P)∩B₂(T)=∅`.

Then `v` has type 1 by time `T`. Indeed, induct along the path in the direction from `s` to `v`. The next vertex cannot have type 2 before `T`; if it already has type 1 there is nothing to prove, and otherwise the type-1 traversal infects it no later than the corresponding cumulative path sum. This argument remains valid if other type-1 paths arrive earlier. It does not incorrectly identify two-type competition with a Voronoi comparison of two independent final distance fields.

All subsequent probability estimates construct such a protected path for a uniform test vertex.

## 4. The two-root local exploration fact

Put `μ=E[D]` and let the size-biased law satisfy

`P(D*=d)=d P(D=d)/μ`,  `ν=E[D*−1]<∞`.

For any **fixed** integers `R,k` and fixed time `T`, the following joint exploration has a limiting coupling with probability tending to one as `n→∞`:

- from an independent uniform test vertex `U_n`, reveal a nonbacktracking path of `R` edges, choosing a forward half-edge by a fixed auxiliary ordering at each new vertex;
- reveal the unopposed type-2 first-passage exploration from the degree-`d₀` vertex `W_n` through time `T`.

In the limit, the first path lies in a rooted tree with root degree `D` and independent subsequent total degrees `D*`. It is independent of a degree-`d₀` rooted continuous-time exploration tree for type 2. The two explored vertex sets are disjoint with probability tending to one. The type-1 weights on the first path are independent `Exp(λ₁)` variables.

Here and below auxiliary path-ordering randomness is only a proof device; it is not information used to choose `S_n`.

### Proof, including why a time ball can be explored finitely

The empirical degree law converges in probability to `D`, and its first and second moments converge to those of `D`. The single parity repair does not change these limits. For the second moment, its difference is at most `(2 max_i D_i+1)/n=o_P(1)`; finite second moment implies `max_i D_i=o_P(sqrt n)`. The number of degree-`d₀` vertices divided by `n` tends to its positive limiting probability.

A fresh uniformly chosen half-edge sees the empirical size-biased degree distribution, which converges in total variation to `D*`. On a countable state space this follows from pointwise convergence of the probabilities and their normalization; convergence of the empirical mean supplies the denominator. For any fixed bound `M` on the total number of exposed half-edges, sampling partners without replacement agrees with independent size-biased sampling up to an error tending to zero. Collisions with previously exposed vertices or the other exploration have probability `O(M²/n)`, because the total degree is at least `2n`. The probability that the initially chosen degree-`d₀` vertex was already exposed is also `O(M/n)` after division by its positive asymptotic degree-class density. These bounds apply conditional on a degree list with the stated empirical properties.

In the limiting time exploration, an active half-edge rings at rate `λ₂` and is replaced by `D*−1` forward half-edges. Starting with `d₀` active half-edges, its expected active population at time `s` is

`d₀ exp(λ₂(ν−1)s)`.

The expected number of ringing events through any fixed `T` is therefore finite, being bounded by the integral of `λ₂` times this expression. Equivalently, the finite-mean continuous-time branching process is nonexplosive. Each event reveals a finite degree, so the total number of exposed half-edges through `T` is finite almost surely. The fixed-length path likewise has only finitely many incident half-edges almost surely.

Choose `M` so large that these two limiting explorations expose at most `M` half-edges with probability at least `1−ε`. Couple the finite-graph explorations until this cutoff, using the preceding finite-sampling argument and the same independent exponential clocks. First let `n→∞` and then `ε→0`. This proves the joint local statement, including disjointness. Continuous edge-weight laws make the fixed time cutoff a continuity event. This is the same finite-time exploration principle proved in §2 of Ahlberg–Deijfen–Janson; the extra fixed-length path and the conditioned root degree require only the finite-exposure modifications just given.

A path always has a forward half-edge in the limiting tree, since `D*−1≥1`. A cycle or premature return in the finite graph is included in the vanishing coupling-error event. No logarithmic-time branching approximation is assumed here.

## 5. Fixed-threshold estimate

For the moment fix `k>d₀`, and infect **all** degree-at-least-`k` vertices initially with type 1. Write

`p_k=P(D*≥k)>0`.

Follow the limiting path from §4 away from its uniform root. Its first `R` non-root vertices have independent total degrees with law `D*`. The probability that none has degree at least `k` is `(1−p_k)^R`. If the root already has degree at least `k`, success is immediate; ignoring that possibility only makes this upper bound more conservative.

On finding a high-degree vertex at distance at most `R`, reverse the path to obtain a route from a type-1 seed to the root. Its type-1 traversal time is bounded by the sum of the first `R` independent exponential weights on the full ray. Denote that sum by `G_R`; it has mean `R/λ₁`, so

`P(G_R>T)≤R/(λ₁ T)`.

For fixed `k,R,T`, §4 also says that the entire path is disjoint from `B₂(T)` with probability `1−o(1)`. The deterministic lemma therefore gives

`limsup_(n→∞) P(U_n is not type 1 by T)
 ≤ (1−p_k)^R + R/(λ₁ T).`                                      (1)

The error here includes the missing degree-`d₀` root event and the negligible possibility that the test root equals it. No independence between the desired weak path and an actual competing infection is presumed: the bound uses the unopposed fast ball and a joint exploration coupling.

Equation (1) is used only with its parameters fixed before taking `n→∞`. The next step handles growing thresholds by a diagonal construction, rather than substitute growing parameters into a fixed-parameter limit without justification.

## 6. Deterministic diagonal schedules

For integers `j≥2`, set `K_j=d₀+j`, `p_j=P(D*≥K_j)`, and `q_j=P(D≥K_j)`. Both probabilities are positive. Choose

`R_j=ceil(j²/p_j)`

and choose finite times recursively so that

`T_j≥j² R_j/λ₁`, `T_j≥T_(j−1)+1`, and `T_j≥j`.

For `0<p≤1`, `(1−p)^R≤1/(1+Rp)`; this follows by applying the elementary binomial inequality to `(1−p)^(-R)` when `p<1`, with `p=1` immediate. Hence both error terms on the right side of (1) are at most `1/j²` for `(K_j,R_j,T_j)`.

There is consequently a deterministic integer `N_j` such that for every `n≥N_j`, the process started at threshold `K_j` satisfies

`P(U_n is not type 1 by T_j)≤3/j²`.                            (2)

Increase the integers `N_j`, if necessary, so that they are strictly increasing and satisfy

`N_j≥4j²/q_j`,  `log N_j≥j T_j`,  `N_j≥j`.

These are finite requirements for each fixed `j`. They depend on the degree law and rates, never on a realized graph, passage times, or future observed degree lists. Define

`J(n)=max{j≥2:N_j≤n}`, `k_n=K_(J(n))`, `t_n=T_(J(n))`

for large enough `n`, with arbitrary harmless choices for the finitely many earlier values. Then `J(n)→∞`, `k_n→∞`, `t_n→∞`, and

`t_n/log n≤1/J(n)→0`.

Let `Z_n=1−N₁(n,t_n)/n`. Conditional on the process, the independent uniform test vertex is missing from type 1 with probability exactly `Z_n`. Thus (2) gives

`E[Z_n]≤3/J(n)²`.

In particular `Z_n→0` in probability; for example `P(Z_n>1/J(n))≤3/J(n)`. This proves the claimed macroscopic victory. It is an expectation identity for a uniform test vertex followed by Markov's inequality, not an unjustified concentration claim from independent vertex indicators.

## 7. The initial resource really vanishes

Before parity repair, the number of degrees at least `k_n` is binomial with parameters `n,q_(J(n))`; repair changes this number by at most one. Therefore

`E[|S_n|/n]≤P(D≥k_n)+1/n→0`.

The mean of the original binomial is at least `4J(n)²`. Its variance is at most its mean. Chebyshev's inequality shows that it is at least half its mean with probability at least `1−1/J(n)²`. Since the repair only increases degrees, `|S_n|≥J(n)` with probability tending to one.

Likewise the expected original total degree at seeds, divided by `n`, is `E[D 1_(D≥k_n)]→0`. If repair moves its chosen vertex across the threshold, the extra counted amount is at most `D_repair+1`; the expected normalized extra is at most `(E[D]+1)/n`. Thus the seed half-edge total divided by `n` tends to zero in probability. Since the full half-edge total is at least `2n`, the initial half-edge fraction also vanishes. Finally every chosen type-1 seed has actual degree at least `k_n`, whereas the competitor has the fixed degree `d₀` on an event of probability tending to one.

For a concrete nonempty family with no parity repair needed, take

`P(D=2m)=2^(-m), m=1,2,…`.

Then `E[D]=4`, `E[D²]=24`, and `P(D=2)=1/2`. Its size-biased tail at `2j` is `(j+1)/2^j`. The theorem applies, for example, to **every** fixed pair of rates with `λ₁<λ₂`, with the stronger infection starting at a degree-two vertex. The deterministic schedules are permitted to depend on those rates.

## 8. What is credited, what remains outside the conclusion

The use of a finite-time branching exploration for the configuration model is established machinery, credited to Ahlberg–Deijfen–Janson and its cited first-passage-percolation literature. The advantage supplied by a sufficiently large sublinear initial population was already studied on random regular graphs by [Antunović–Dekel–Mossel–Peres, arXiv:1109.2575](https://arxiv.org/abs/1109.2575), published Random Structures & Algorithms 50 (2017), 534–583, DOI [10.1002/rsa.20699](https://doi.org/10.1002/rsa.20699); see especially its Theorem 2.6. This candidate neither claims to discover that general phenomenon nor transfers the regular-graph theorem to degree-biased seeds.

The point proved here is an affirmative existence statement with simultaneous degree-only selection, vanishing seed density and vanishing seed half-edge fraction, diverging minimum seed degree, and an arbitrary fixed speed disadvantage. It uses a diagonal local argument and provides no optimal scale. A fixed number of high-degree seeds, prescribed polynomial seed budgets, and sharp rate/degree thresholds are separate unresolved tasks in this package.

Current searches also found a 2026 first-visit **random-walk** location game and work on long-range or infinite-mean competing growth. Those models do not supply this nearest-neighbor finite-variance result. The searches are not an exhaustive novelty audit. The candidate therefore makes no historical priority or human peer-review claim.

The accompanying exact checks concern the deterministic path lemma on finite weighted graphs, the concrete size-biased law, and the diagonal inequalities. They do not establish the stochastic limit theorem by simulation; the limiting proof is §§3–7.
