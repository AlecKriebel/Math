# Adversarial verification of the BKV timing implication

Author: Codex independent timing adversary, 2026-10-12 UTC.

## Verdict

**VALID, with an explicit selective-exploration qualification and a separate quenched upgrade.** The proposed simultaneous-infection conclusion is an immediate mathematical addendum to the mechanism of the published proof of Proposition 6.2. It does not need a substantive new recovery-window construction. The published proposition itself states global survival, so the strengthened conclusion should be described as a consequence of its proof, not as a conclusion explicitly stated in the proposition.

No counterexample or unsupported central mathematical gap was found. The points that must be written out are (1) choose first eligible arrows, (2) never reveal the post-arrow recovery residuals in the ray exploration, (3) use finite graphical paths to individual endpoints, and (4) do not infer almost-every-tree positivity merely from an annealed lower bound.

## Evidence reviewed independently

- Actual repository `AGENTS.md` read.
- Published BKV PDF `primary/bkv.degree_penalized2026.pdf`, SHA-256 `320fea7622aadb9658130c5ebad7dba12bef171bbf379400c625f45c19f59922`.
- Complete published pages 46-48 visually inspected, along with their extracted text. These contain Definition 6.1, Proposition 6.2, and its proof (equations (99)-(107)).
- Complete published page 17 visually inspected. Definition 3.1 defines infection through finite infection paths and explicitly does not exclude finite-time explosion.
- No other priority-reviewer report was read. No external communications or Git/provider writes were performed.

## Exact scope and success criteria

Let the offspring distribution have weak power-law exponent `alpha > 0`, as in BKV Definition 1.7, with `P(D >= 1) = 1`. Fix `lambda > 0` and the max penalty exponent `mu >= 0` with `alpha + mu < 1`. Use BKV's down-directed graphical process, which is dominated by its undirected process.

Choose `1 < s1 < s2` and `epsilon > 0` satisfying their tail-comparison condition and

\[
\beta=1-\alpha s_1-\epsilon s_1>0,
\qquad \delta=\beta-\mu s_2>0.
\]

The target is positive probability of infinitely many vertices infected simultaneously at a finite time, including at some finite deterministic time. The proof below also gives the latter for almost every offspring tree, with a deterministic time that may be chosen for that tree. It identifies what is required to obtain a single full-measure event for all `lambda > 0`.

This verification does not claim an analogous conclusion at `alpha + mu = 1`, outside the weak-power-law assumption, or from global survival alone on an arbitrary graph.

## 1. First eligible arrows retain the published success probability

At stage `m`, the current vertex `v_m` has offspring count `L_m`. BKV's event `A1` supplies at least a constant times `L_m^beta` eligible children with offspring counts in `[L_m^s1, L_m^s2]`. Select the same fixed-size subset used in their `A2`, with a deterministic child ordering, and choose the first arrow to that subset after arrival at `v_m`.

This is an admissible specialization of their instruction to choose any eligible child infected before the parent heals. On success it supplies a fresh descendant. In the down-directed tree, each child has only one incoming edge. Inductively the selected vertex was not infected before the selected first arrow; prior visits, reinfections, and merging routes do not enter this exploration.

Let `R_m` be the total ordered-arrow rate to the selected subset. BKV's estimates give

\[
L_m\ge K^{s_1^m},\qquad
R_m\ge r_m:=c\lambda K^{\delta s_1^m}
\]

whenever the prefix exists and `A1` holds. Here `c > 0` is fixed, independent of `m` and `L_m`.

There is a minor degree-bookkeeping issue in the displayed published proof: it defines `D_v=d_v-1` but writes rates with `D_v`. Restoring full degrees changes only `c`. Indeed, if both offspring counts satisfy the stated bounds and `L_m >= 1`, then

\[
\max\{d_{v_m},d_u\}\le 2L_m^{s_2},
\quad r(v_m,u)\ge 2^{-\mu}\lambda L_m^{-\mu s_2}.
\]

After rounding the selected subset size, one may take, for sufficiently large `K`, `c=2^{-mu}/8`. The same exponents and summable errors follow. The root's actual degree is only smaller than this conservative bound.

The published infinite-product argument, with these harmless constant adjustments, gives `P(A) > 0`, where `A` is success of the infinite first-arrow ray. For annealed positivity one can start with the root on `{D_root >= K}`. This avoids needing any extra conditioning analysis of the first high-degree vertex reached by the full process.

## 2. Weighted waiting times are summable without conditioning bias

Write `S_m` for arrival at `v_m`. At an existing stage with `A1`, let `W_m` be the first eligible-arrow wait and `H_m` the first recovery wait after arrival. Given the selective past and the eligible rates,

\[
W_m\sim\operatorname{Exp}(R_m),\qquad
H_m\sim\operatorname{Exp}(1),\qquad W_m\perp H_m.
\]

The step succeeds exactly when `W_m < H_m`, and then `S_(m+1)=S_m+W_m`. In particular,

\[
\mathbb E\left[W_m\mathbf1_{\{W_m<H_m\}}\mid\text{past, rates}\right]
=\frac{R_m}{(R_m+1)^2}\le\frac1{R_m}.
\]

Set the term to zero when the prefix or `A1` fails. For the resulting nonnegative variable `Z_m`, `Z_m=W_m` on `A` and `E[Z_m] <= 1/r_m`. Therefore

\[
\mathbb E\sum_{m\ge0}(m+1)Z_m
\le\sum_{m\ge0}\frac{m+1}{c\lambda K^{\delta s_1^m}}<\infty.
\]

Thus, almost surely on `A`,

\[
\sum_{m\ge0}(m+1)W_m<\infty,
\quad S_\infty=S_0+\sum_{m\ge0}W_m<\infty,
\]

and the identity

\[
\sum_{m\ge0}(S_\infty-S_{m+1})
=\sum_{j\ge1}jW_j<\infty
\]

holds. An assertion about `E[W_m | A]` is unnecessary and would obscure the conditioning issue; the successful-prefix variables handle it directly.

## 3. The unused recovery residuals really are independent

On a successful step set `E_m=H_m-W_m`. Conditional on the rates, the joint density of a first-arrow winner `j`, waiting time `w`, and recovery residual `e` is

\[
r_j\exp\{-(R_m+1)w\}\exp\{-e\}\,dw\,de,
\qquad w,e>0.
\]

The factor `exp(-e) de` is independent of the winner and wait. Conditional on step success, `W_m` has exponential rate `R_m+1`, the winner has probability `r_j/R_m`, and `E_m` is independent `Exp(1)`.

Subsequent first-arrow steps use outgoing-edge processes and healing processes at distinct fresh descendants. They never consult `E_m`, the parent recovery mark after the selected arrow, or any later parent state. Hence finite successful-prefix explorations factor all residuals as independent `Exp(1)` variables. Passing to the infinite successful skeleton preserves the same product law, by cylinder events and monotone-class/limit arguments.

Let `G` be the selective skeleton sigma-field generated by the offspring tree, the selected ray, the waits/arrival times, the winners, and the recorded success indicators, with unused post-success recovery marks excluded. Then **conditional on `G` on `A`, the `E_m` are iid `Exp(1)`**.

The qualification is material: the same statement is false if “past” or “ray data” means the entire contact-process history with old recoveries observed, or if one selects a child using its future recovery behavior. Neither is needed. A retrospective arbitrary child choice could destroy this independence, which is why the adapted first-arrow choice must be explicit.

## 4. Infinitely many simultaneous infections use finite paths

The first recovery time of `v_m` is `S_(m+1)+E_m`. Conditional on the successful skeleton,

\[
\mathbb P\{S_{m+1}+E_m\le S_\infty\mid G\}
=1-e^{-(S_\infty-S_{m+1})}
\le S_\infty-S_{m+1}.
\]

The right-hand side is summable in `m`. Conditional first Borel-Cantelli, which does not even require independence, implies that only finitely many selected vertices recover before `S_infty`. All but finitely many ray vertices are therefore infected simultaneously at `S_infty`.

For each endpoint `v_m`, the path from the initial seed to that vertex uses only finitely many ray arrows. Each earlier ancestor need avoid recovery only until its chosen outgoing arrow; later recovery of that ancestor does not erase the path. For a vertex with first recovery after `S_infty`, append the vertical segment from its arrival to `S_infty`. This is a finite infection path exactly as in BKV Definition 3.1. No path with infinitely many jumps ending at a hypothetical vertex at infinity is used.

For any deterministic `h`, on `A intersect {S_infty < h}`,

\[
\mathbb P\{S_{m+1}+E_m>h\mid G\}
=e^{-(h-S_{m+1})}\ge e^{-h}>0
\]

(all arrival times are nonnegative). These events are conditionally independent. Conditional second Borel-Cantelli gives infinitely many ray vertices with no recovery before `h`; each again has a finite infection path to time `h`.

Since `A` has positive probability and `S_infty < infinity` on `A`, some positive integer `h` satisfies `P(A intersect {S_infty < h}) > 0`. Thus

\[
\mathbb P\{|\xi_h^\downarrow|=\infty\}>0
\]

for a finite deterministic `h`, and downward domination transfers the conclusion to the undirected process. For a particular successful skeleton the same argument at all integers beyond `S_infty` also shows that infinitely many infections persist at every subsequent finite time: use an integer above the desired time and the same recovery-free finite paths.

## 5. Annealed positivity does not alone give almost-every-tree positivity

The expectations and binomial child-count arguments displayed in BKV's proof average over offspring fields. They establish positive annealed probability. The phrase “for a.e. realization in the conditional expectation” on page 48 concerns the conditional lower bound along a growing ray; it is not, by itself, a disintegration proof of positivity for almost every full tree.

A short separate hereditary argument supplies the desired quenched statement. To remove root-degree ambiguity, give every vertex the conservative augmented degree `D_v+1` in the rates. This decreases the actual root-edge rates and agrees with all non-root degrees; child subtrees then have precisely the same rate convention as fresh rooted trees.

Call an offspring tree good when, from its root, the conservative down-directed process has positive probability of reaching by a finite infection path a vertex from which the accelerating first-arrow ray succeeds. Let `q` be the offspring-tree probability of being bad. The annealed root-high-degree construction proves `q < 1`.

If any child subtree is good, the whole tree is good. The root can send an arrow to that child before recovering with strictly positive probability. At that finite arrival time, the graphical field strictly below the child is fresh by independence and time homogeneity; its positive success probability is unchanged. Every rate on the finite root-child bridge is finite and strictly positive.

Conditional on the root offspring number, the child subtrees are iid, and therefore

\[
q\le\mathbb E[q^D].
\]

Because `P(D >= 1)=1` and the weak power-law tail ensures `P(D >= 2)>0`, for `0 < q < 1` one has `E[q^D] < q`. Combined with `q < 1`, this forces `q=0`.

Hence almost every tree has positive graphical probability of a finite bridge followed by the accelerating ray. The waiting-time and residual arguments above apply after that bridge. For each such tree, a countable union over finite integer `h` supplies some deterministic `h=h(T,lambda)` with positive quenched probability of infinitely many infections at `h`.

If a statement requires the full-measure set of trees to work simultaneously for every `lambda > 0`, apply this argument at a sequence of positive rational rates decreasing to zero, intersect the corresponding full-measure sets, and use graphical monotonicity. This does not require an uncountable intersection.

The argument written here guarantees a deterministic time for each fixed tree; it does not silently equate that with a single uniform time for all trees. A further support-at-zero argument for first-arrow sums can strengthen the time quantifier, but is not necessary for the requested positive-probability finite deterministic-time conclusion.

## Exact remaining gap and classification

- Timing/simultaneous-infection implication: **no remaining mathematical gap**, provided the selective skeleton and first-arrow specialization are stated.
- Quenched positivity: **verified by the separate hereditary argument above**, not supplied merely by the displayed annealed calculation.
- Published result versus inferred result: the paper explicitly proves a global-survival proposition and explicitly allows explosion in its definition; the finite-time infinite-infection result is an addendum deduced from its proof.
- Novelty/priority judgment outside this implication: not assessed by this adversary.
- Boundary `alpha + mu >= 1`: this exact route is blocked because its positive exponent `delta` cannot be chosen. No claim there is justified by the argument.

Best-guess completion of this assigned adversarial verification: **100%**.
