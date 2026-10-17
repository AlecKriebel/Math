# Independent review of adaptive covariance and square influence

Verdict: **PASS within the stated scope**, with no mathematical repair identified. This review establishes Lemmas 3 and 4 and the conditional conclusion in Section 5 from the existence of a total separator of depth at most `16 d^4`. The separator construction, its source fidelity, the original problem's source fidelity, historical priority, and publication eligibility are reviewed elsewhere. A valid separator is an explicit input here, rather than an unproved substitute for the claim under review.

The input is the 13,567-byte `inputs/PROOF.md`, SHA-256 `20bf5956520b2b53bb4b415d7d5683a6ae1cf1273bd36372accbc49fab482da1`, supplied as source head `b1d6bc6ceb66e9c9c98cfae229ee86e5720799e2`. No separate earlier AUDIT, conclusion, review, or code was read. The proof's opening status sentence itself reports prior acceptance; that statement was visible when reading the proof and was not used as evidence. An initial repository status and audit-directory listing exposed unrelated filenames, without reading their contents. No web source or external theorem was consulted for this shard. The proof below and the finite controls were derived independently from the claim and assigned proof, without another reviewer's mathematical conclusions.

## 1. Universal covariance proof

Let `X,Y` be independent uniform sign vectors. The tree is a fixed deterministic total binary tree, with no repeated query on a branch. It reads only `X`. Write its random leaf transcript as

`tau = ((i_1,b_1),...,(i_l,b_l), leaf)`.

The event that this transcript occurs is precisely the cylinder

`X_{i_1}=b_1,...,X_{i_l}=b_l`.

One inclusion is automatic from the recorded answers. For the converse, a vector satisfying these equalities follows the same root query, then the same child, and inductively every subsequent query and stopping decision. No additional restriction on unqueried coordinates is imposed by a deterministic leaf. This statement includes variable stopping and history-dependent query indices.

Let `Z_t` replace the first `t` queried coordinates of `X` by those of `Y`. Conditional on a complete transcript, its queried coordinates in `Z_l` come from independent uniform `Y`; its unqueried coordinates come from independent uniform, unconstrained coordinates of `X`. These two collections are independent. Thus the conditional distribution of `Z_l` is uniform, independent of the entire transcript. Since `h(X)` is a transcript-measurable value,

`E[(h(X)-1/2)u(Z_l)] = (E[h]-1/2) E[u]`.

The cube is finite, so an arbitrary real function `u` has finite sums and all following identities are justified, however large or signed its values are. Subtract the last identity from `E[(h(X)-1/2)u(X)]` and telescope:

`Cov(h,u) = E[(h(X)-1/2) sum_{t=1}^L (u(Z_{t-1})-u(Z_t))]`.

For each nonterminal pre-query transcript `sigma` of length `t-1`, let `i` be its deterministic next query. Conditional on `sigma`, the coordinates already read from `X` are fixed, while all other coordinates of `X` retain their joint product law. In `Z_{t-1}`, each fixed coordinate has already been replaced by its independent `Y` coordinate. Consequently `Z_{t-1}` is uniform on the whole cube under this conditioning. Moreover, `Y_i` is independent of it and uniform: the no-repeat hypothesis puts `i` outside the coordinates previously replaced, and the event `sigma` only concerns `X`. Hence the conditional law of `(Z_{t-1},Z_t)` is exactly that of an independent coordinate resampling pair `(W,W^(i))`.

It is essential here to condition on the **pre-query** transcript, not on the answer to query `i`, a later answer, or the final leaf. The proof uses complete transcripts only for the different terminal-independence statement. It never conflates these two conditionings. It also never runs a tree on the changing hybrids.

Using `|h-1/2|=1/2`, summing over all nonterminal cylinders, and noting that the finite maximum depth bounds the number of terms gives

`|Cov(h,u)| <= (1/2) sum_{t,i} Pr(L>=t,I_t=i) A_i(u)`

`                  = (1/2) sum_i r_i A_i(u)`.

The last equality uses the no-repeat condition, so the expected number of queries to `i` equals its query probability `r_i`. Adaptivity creates no missing independence assumption: conditioned on each cylinder the pair law is fixed, and cylinders with the same next query merely mix identical pair laws. The output need not compute or approximate `u`.

The coefficient `1/2` is optimal. In dimension one take `h(x)=(1+x)/2` and `u(x)=x`. Then `Cov(h,u)=1/2`, `r_1=1`, and independent resampling gives `A_1(u)=1`, attaining equality. Replacing `1/2` by `0.49` fails on this explicit real, signed function.

## 2. Universal square-influence proof

Normalize a nonzero real function `a` so `E[a^2]=1`. Fix coordinate `i`, and write its unique multilinear/Fourier decomposition as

`a(x)=b(x_{-i}) + x_i c(x_{-i})`.

The full Fourier norm, including the constant coefficient, gives

`E[b^2]+E[c^2]=1`, and `rho=RelInf_i(a)=E[c^2]`.

Thus `0<=rho<=1`, without any mean-zero assumption. For a sign flip,

`a(x)^2-a(x^flip_i)^2 = 4 x_i b(x_{-i}) c(x_{-i})`.

Independent resampling leaves the sign unchanged half the time and flips it half the time, so

`A_i(a^2)=2 E[|bc|] <= 2 sqrt(E[b^2] E[c^2])`

`                        =2 sqrt(rho(1-rho)) <=2 sqrt(rho)`.

This decomposition gives an independent derivation of the proof's Parseval/Cauchy bridge and fixes its constants. For a general nonzero normalization, divide by `E[a^2]`; every expression is unchanged by any nonzero real scaling. Negative coefficients and signed values of `a` cause no issue, since the factorization precedes absolute values and Cauchy--Schwarz. Complex values are outside the claim and not inferred.

The endpoints are consistent. If `rho=0`, `a` is independent of coordinate `i`; if `rho=1`, `b=0` and `a=x_i c`, whose square is independent of `i`. In either case `A_i(a^2)=0`. A nonzero constant has every relative influence zero. For `a=3+x_i`, the full norm is `10`, `rho=1/10`, and `A_i(a^2/10)=3/5`, which attains the sharper bound. Omitting the constant from the denominator changes this convention and is not justified by this result.

## 3. Conditional completion of the main claim

Assume nonzero `f,g` have disjoint support and that a total binary separator `h` of depth at most `T` satisfies `h=1` on the support of `f` and `h=0` on that of `g`. Set `u=f^2/E[f^2]`, `v=g^2/E[g^2]`, and `mu=E[h]`. Nonzero functions on the finite cube have strictly positive denominators. Pointwise, `hu=u` and `hv=0`, including every common zero. Therefore

`Cov(h,u)=1-mu`, `Cov(h,v)=-mu`, and their absolute values sum to `1`.

Since a total binary separator has `0<=mu<=1`, neither absolute-value sign is ambiguous. No assertion that the supports cover the cube is used. With

`delta=max_i max(RelInf_i(f),RelInf_i(g))`,

the preceding inequalities and `sum_i r_i=E[L]<=T` yield

`1 <= sum_i r_i (sqrt(RelInf_i(f))+sqrt(RelInf_i(g))) <= 2T sqrt(delta)`.

Because `f,g` are nonzero, the separator takes both output values and `T>=1`. Consequently `delta >= 1/(4T^2)`. Substituting `T<=16d^4` gives exactly `delta>=1/(1024d^8)`. If all relative influences are at most `1/(4096d^8)`, the same right-hand bound is at most `1/2`, a contradiction. The theorem has slack and no endpoint-equality defect in this conversion. The argument needs neither a degree bound on `u,v` nor bounded coefficients; the degree bound is used only by the supplied separator.

## 4. Exact independent finite controls

`exact_controls.py` uses only integers and `fractions.Fraction`; it has no floating point certification and imports no package theorem. Acceptance uses explicit exceptions, not Python `assert` statements. Both ordinary Python and `python -O` execute the same gates.

It recursively enumerates **every** deterministic labeled total tree with no repeated branch query on dimensions 1, 2, and 3. There are respectively 6, 74, and 16,430 trees, including trees with redundant queries. For each tree, every subset of the cube is tested as the indicator function `u`. With `N=2^n`, output-one set `H`, cut set `S`, query counts `q_i=N r_i`, and the number `c_i` of undirected cut-crossing edges in coordinate `i`, the checked integer inequality is

`2 |N |H intersect S| - |H| |S|| <= sum_i q_i c_i`.

This is exactly the stated covariance bound after multiplying by `2N^2`. It makes 4,207,288 all-cut checks. All-real-function coverage for each tested tree follows from an elementary finite layer decomposition: sort the values of an arbitrary real `u`, write it as a constant plus a nonnegative sum of upper-level-set indicators, use covariance linearity and the triangle inequality, and note that each edge's total level-set contribution equals `|u(x)-u(x^flip_i)|`. Thus the cut enumeration checks every real `u` for each finite tree, not merely a sampled list of `u` values.

For every enumerated tree, every independent pair `(X,Y)` is also enumerated. Counters check the full law of the hybrid pair separately at every pre-query cylinder and the full uniform law separately at every terminal cylinder. There are 91,192 pre-query laws and 107,702 terminal laws checked in total. Among dimension-three trees, 7,776 have a history-dependent next coordinate and 13,152 have variable leaf depth. These controls cover actual adaptivity and early stopping.

The square controls enumerate all 6,648 nonzero truth tables with values in `{-1,0,1}` for dimensions 1 through 3. Every such function has a unique real multilinear representation. All 19,848 coordinate checks compare direct edge differences to independently computed Walsh/Fourier influences and Parseval, then check the squared Cauchy bound exactly. They include `rho=0`, `rho=1`, constants, sign changes, and zero values. Additional rational dimension-four functions verify exact invariance under scalings `10^200`, `10^-200`, and `-37/19`; the constant-plus-character case checks the full-norm convention.

Mathematical rejection controls explicitly reject a false smaller covariance coefficient, full-transcript conditioning of a pre-query pair, failure to replace previous query coordinates, and a false square-influence factor. Their mutation modes must return nonzero under both ordinary and optimized Python. The accompanying receipts record their actual exit status.

These finite computations do not establish the universal theorem by themselves. The unrestricted arguments in Sections 1--3 are the proof. They are consistent with the independent exact controls.

## 5. Remaining gap and severity

No gap remains in this shard's universal covariance proof, square-influence bridge, or the derivation of the `1/(1024d^8)` necessary bound and `1/(4096d^8)` sufficient condition **given the stated separator**. There is no actionable mathematical defect identified here and no requested repair. The unreviewed dependency is the existence and exact depth of that separator; this shard makes no unconditional verdict on its proof, source fidelity, novelty, or publication status. No person was contacted and no external communication or publication was initiated.
