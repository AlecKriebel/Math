# Checkable prior implication and candidate-scope comparison

These are priority-comparison deductions from identified primary results. They do not revalidate the candidate proof or claim that any unnumbered corollary below was separately printed.

## 1. Two separated first-order atoms forbid every deterministic center

Suppose `V_n/n => p delta_A+(1-p)delta_B`, with `A!=B` and `0<p<1`. Let `alpha_n=o(n)`, positive, and let `c_n` be any deterministic real sequence. Put `d=|A-B|` and choose the disjoint open intervals `J_A=(A-d/8,A+d/8)`, `J_B=(B-d/8,B+d/8)`. Their boundary points have zero limiting probability, so their probabilities tend to `p` and `1-p`.

For each fixed `M<infinity`, the interval `I_n=[(c_n-M alpha_n)/n,(c_n+M alpha_n)/n]` has length `2M alpha_n/n ->0`. Eventually it intersects at most one of `J_A,J_B`, uniformly over `c_n`. Therefore

`liminf_n P(|V_n-c_n|>M alpha_n) >= min(p,1-p) >0`.

This holds for every `M` and contradicts tightness. No boundedness, convergence, or asymptotic formula for `c_n` was assumed. Random centers are not covered: the interval would then be selected using the same outcome as `V_n`.

## 2. Exact published boundary example in the candidate source

Use the candidate's `mu=(1/2,1/2)` and `P=((3/4,1/4),(1/4,3/4))`. Let

`a=00 111...`, `b=01 000...`, `t0=F(a)=F(b)=P(S starts 00)=3/8`.

The empty prefix contributes1 and the common prefix0 contributes1/2 to the string mean `m`. The remaining geometric sums give

`m(a)=1+1/2+(1/2)(3/4)[1+(1/4)/(1-3/4)]=9/4`,

`m(b)=1+1/2+(1/2)(1/4)[1+(1/4)/(1-3/4)]=7/4`.

These are the endpoint formulas in [2017 Proposition2.1(i)](https://arxiv.org/pdf/1605.02352v2), pp10–11, evaluated at an actual boundary. For `k_n=floor(n t0)+1`, `sqrt(n)(k_n/n-t0)->0`. Proposition2.5(iii), p14, yields

`Y_n(k_n)/n => (delta_(9/4)+delta_(7/4))/2`.

Section1 then proves non-tightness for **every deterministic center**, even for any sublinear scale. In particular, the all-center `sqrt(n)` claim is an unsupported-free exact corollary of an identified earlier theorem at this fixed boundary. It also subsumes the standard center, midpoint center, and any deterministic expected-profile center.

The concrete calculation corrects the frozen first assessment's arithmetic typo. The rank is3/8;7/8 belongs to neither of these adjacent coding strings. [COMPARISON_CHECK_RESULTS.json](COMPARISON_CHECK_RESULTS.json) records exact rational checks without numerical approximations.

## 3. Earlier finite-prefix derivation from the thesis's proved ingredients

[Leckey's thesis](https://d-nb.info/107268702X/34), Lemma5.2.4 and the iterated recurrence(5.12)/(5.16), provide a linear expected worst-cost bound for row-initial continuation sources and the finite-prefix cost decomposition. This argument shows what those ingredients already imply; it is this audit's derivation, not a numbered thesis theorem.

Let `v=W1 000...`, `v-=W0 111...`, `tau=F(v)=F(v-)` be a fixed interior boundary of depth `ell=|W|+1`. For fixed `L>=ell`, truncate the algorithm's prefix tolls after depth `L-1`. Given the prefix counts, the remaining selected-subtree cost is nonnegative and its conditional expectation is at most `C` times the largest depth-L count. The row-initial bound applies because conditioning on a finite prefix leaves the Markov continuation with the row of its last state. Thus, denoting this remainder by `R_(n,L)`,

`limsup_n E R_(n,L)/n <= C max_(|w|=L) pi(w) <= C p_max^(L-1)`.

For a general initial law the root recursion adds one toll and leaves exactly those continuation laws; the same remainder bound holds. For each fixed finite depth, all normalized cylinder counts converge to their strictly positive probabilities. The selected prefix is consequently, with probability tending to1, one of `v^(L), (v-)^(L)`; other depth-L intervals have endpoints a fixed distance from `tau`.

Let `B_n` count strings lexicographically at or below `v-`. It is `Bin(n,tau)`. For `k_n=floor(n tau)+1`, the selected rank lies on the left if and only if `B_n>=k_n`, and `P(B_n>=k_n)->1/2` by the binomial CLT. All prefix choices on the left and right are controlled by this same event. For fixed L the truncated normalized cost therefore has the form

`M_(L,-) 1_(B_n>=k_n)+M_(L,+) 1_(B_n<k_n)+o_P(1)`,

where `M_(L,-)=sum_(r=0)^(L-1) pi((v-)^(r))` and `M_(L,+)=sum_(r=0)^(L-1) pi(v^(r))`. Singleton stopping changes no fixed-depth term asymptotically, since the finitely many positive cylinder counts eventually exceed1.

Let first `n->infinity`, then `L->infinity`. The geometric remainder bound and Markov's inequality make the discarded cost uniformly negligible on scale n; the finite sums tend to `m(v-),m(v)`. For example, applying bounded Lipschitz test functions bounds the truncation error by `E R_(n,L)/n` and proves

`Y_n(k_n)/n => (delta_(m(v-))+delta_(m(v)))/2`.

This produces the same concrete boundary example as Section2, using only the thesis's proved ingredients and elementary binomial laws/CLT. Its mean-only theorem is not falsely described as a printed mixture theorem. The process-norm theorem is not used to infer a marginal. This is positive evidence for an earlier boundary derivation, without asserting an earliest historical date outside the checked corpus.

## 4. Why the candidate continuity rank is not this theorem's special case

The candidate code has infinitely many zeros and ones, so it is neither eventually-zero nor eventually-one. Its `t=F(v)` lies outside `F(Sigma_0^infinity)` and is a continuity point of `m o h`. Sections2–3 assume one **fixed boundary** tau; those hypotheses do not contain this t.

The published uniform string CLT [Theorem1.2](https://arxiv.org/pdf/1605.02352v2), p5, implies `||X_n||=O_P(1)`, where `X_n(s)=[Z_n(s)-n m(s)]/sqrt(n)`. Since `Y_n(k)=Z_n(S_(k))`, for deterministic `c_n` we have the exact identity

`[Y_n(k)-c_n]/sqrt(n) = X_n(S_(k)) + sqrt(n)[m(S_(k))-m(h(t))] + [n m(h(t))-c_n]/sqrt(n)`.

The CLT bounds the first summand, and the nonboundary LLN controls the second only before multiplication by `sqrt(n)`. Continuity alone supplies no rate. Changing-depth boundary displacement is the missing ingredient in a proposed direct specialization.

The candidate supplies `tau_j->t`, endpoint jump `A_j-B_j=P_j`, displacement scale `w_j=P_j q^j` with `q=3/4`, and `n_j=ceil(w_j^-2)`. Its stated geometry has `0<t-tau_j<P_j q^(2j)/12`, hence

`(t-tau_j)/w_j < q^j/12 ->0`, while `P_j/w_j=q^-j ->infinity`.

Thus the jump goes to zero, consistent with continuity, but dominates the order-statistic scale; `sqrt(n_j) P_j~q^-j`. The candidate must further prove the local band widths are negligible and both branch probabilities stay positive along the chosen sequence. Those are additional estimates; a fixed-boundary theorem cannot be applied uniformly at moving depths merely by citing its statement. The proof's elementary uniform cost bound is weaker than the earlier string CLT, so the construction's new scope should be attributed to its rank geometry and diagonal control, not to a new general uniform fluctuation theorem.

This comparison identifies exactly where direct substitution fails and what extra work is claimed. It does not establish that no existing paper, generic consequence, or other derivation already supplies the same explicit rank. An independently checked construction can be a useful refinement while historical novelty remains unresolved.

## 5. Scope boundaries

The known countable dense boundary set has measure zero. Adding one explicitly coded continuity point proves neither positive-measure nor a.e. failure. It also does not classify all nonboundary marginals. The string CLT evaluates a fixed string; replacing that string by an empirical selected string changes the center. The random center `n m(S_(k))` is permitted in Proposition2.8 and excluded by the candidate's deterministic-center quantifier. These claims are logically compatible.
