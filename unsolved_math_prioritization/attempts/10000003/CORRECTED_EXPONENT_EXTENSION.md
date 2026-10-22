# Finite-force line equilibria through the exponent (3 + sqrt(5))/2

11 October 2026. Corrected statement and independently checked extension of the mechanism in Alper Ferudun's [arXiv:2610.06944v1](https://arxiv.org/abs/2610.06944v1). This proof exposition and its independent check are AI-assisted.

## Attribution and exact scope

Ferudun's Theorem 1.2 supplies the range `1 < s <= 2`. The extension considered here is `2 < s <= (3 + sqrt(5))/2`, obtained by combining his gap network and spatial cutoff with a little-o particle count and power concavity. His Remark 5.3 identifies the relevant small-gap expression but does not assert the extension. This note does not certify novelty or journal acceptance. The [author's public record](https://eulersolve.org/papers/amr-099-0003/) describes the source as an unrefereed, AI-assisted preprint.

This corrected note makes the nontrivial-configuration assumption explicit. The earlier extension's prose statement did not expressly exclude a singleton. A singleton has zero finite forces but is not a positive-spacing bi-infinite lattice. The proof always used a bi-infinite increasing enumeration, so this is a correction to the standalone statement's scope, not a failure of its proof for nontrivial configurations.

## Theorem

Put

\[
s_* = \frac{3+\sqrt5}{2}.
\]

Fix `1 < s <= s_*`. Let `X` be a subset of the real line containing **at least two distinct points**. Assume that, for every `x in X`,

\[
\sum_{y\in X\setminus\{x\}} |y-x|^{-s}<\infty,
\qquad
\sum_{y\in X\setminus\{x\}}
\operatorname{sgn}(y-x)|y-x|^{-s}=0. \tag{1}
\]

Then there are `b in R` and `h > 0` such that

\[
X=b+h\mathbb Z.
\]

The positive series in (1) is an unordered sum; its finiteness gives absolute convergence of the signed series. Equivalently, each one-sided force is finite and the two one-sided forces are equal. Local finiteness may be added explicitly but follows from (1). No interpretation involving cancellation of two infinite forces is included.

## 1. Ordering and an adjacent-gap bound

Fix `x_0 in X`. Every other point within distance `L` contributes at least `L^{-s}` to the finite positive force there, so every bounded interval contains finitely many points. In particular, `X` is countable. If `X` were bounded above, local finiteness would supply a largest point. All forces at that point have the same sign and at least one is nonzero, contrary to (1). The corresponding argument excludes a lower bound. Thus there is a strictly increasing enumeration `(a_n)_{n in Z}`, with `a_n -> +infinity` as `n -> +infinity` and `a_n -> -infinity` as `n -> -infinity`. Translate so that `a_0=0`, and set `g_n=a_{n+1}-a_n>0`.

Write `F_n^-` and `F_n^+` for the left and right positive force sums; both are finite and equal. For `u=g_{n-1}` and `v=g_n`, comparing particles at `a_n` and `a_{n+1}` gives

\[
F_n^+\le v^{-s}+F_{n+1}^+,
\qquad
F_{n+1}^-\le v^{-s}+(u+v)^{-s}+F_n^--u^{-s}.
\]

Cancel the finite quantity `F_n^-` after using equilibrium. Then

\[
1\le 2(v/u)^{-s}+(1+v/u)^{-s}.
\]

The right-hand side is strictly decreasing from infinity to zero as a function of `v/u`. Its unique value-one root `r=r_s` is greater than one. Consequently `v/u<=r`. Reflection gives the reciprocal bound, so

\[
r^{-1}g_n\le g_{n+1}\le rg_n \quad(n\in\mathbb Z). \tag{2}
\]

This reasoning works for every fixed `s>1`. It gives no assumed global upper or lower gap bound.

## 2. A well-defined transformed network

For `n != j`, put `D=|a_j-a_n|`, `D'=|a_{j+1}-a_{n+1}|`, and

\[
c(n,j)=
\begin{cases}
\dfrac{D^{-s}-(D')^{-s}}{D'-D},&D'\ne D,\\
sD^{-s-1},&D'=D.
\end{cases}
\]

The kernel is positive and symmetric. Subtract the absolutely convergent force equation at `a_{n+1}` from the one at `a_n`, shifting the former's index by one. For `j>n` the distance difference is `D'-D=g_j-g_n`. For `j<n` the distance difference and force sign both reverse. Therefore

\[
\sum_{j\ne n}c(n,j)(g_j-g_n)=0. \tag{3}
\]

Its absolute convergence follows by bounding each summand's absolute value by `D^{-s}+(D')^{-s}`.

By symmetry it suffices to compare distances when `j>n`. For `j=n+1`, (2) gives `D'>=D/r`. For `j>=n+2`,

\[
D\ge g_n+g_{n+1}\ge(1+r^{-1})g_n,
\qquad
D'=D+g_j-g_n\ge D/(1+r).
\]

The mean value theorem consequently gives

\[
c(n,j)\le K D^{-s-1},\qquad K=s(1+r)^{s+1}. \tag{4}
\]

For fixed `n`, every `D` is at least `delta_n=min(g_{n-1},g_n)>0`. Hence

\[
0<\pi(n):=\sum_{j\ne n}c(n,j)
\le K\delta_n^{-1}(F_n^-+F_n^+)<\infty.
\]

Adding `g_n pi(n)` to (3) is legitimate and gives `sum_j c(n,j)g_j=pi(n)g_n`. With `c(n,n)=0`, this defines an irreducible Markov kernel `P(n,j)=c(n,j)/pi(n)` having positive harmonic function `g`.

Define

\[
c^*(n,j)=c(n,j)g_ng_j.
\]

Its row mass is exactly `pi^*(n)=pi(n)g_n^2`, finite and positive. Its Markov kernel is `P^*(n,j)=P(n,j)g_j/g_n`. In particular,

\[
\sum_j P^*(n,j)\frac1{g_j}=\frac1{g_n}. \tag{5}
\]

Thus `1/g` is a genuinely integrable positive harmonic function; no boundedness of `g` or `1/g` is needed.

## 3. Recurrence and Liouville facts with infinitely many neighbors

Let `b` be any symmetric irreducible conductance kernel on a countable state space, with every row mass `mu(x)` in `(0,infinity)`. Its energy is

\[
\mathcal E_b(f)=\frac12\sum_{x,y}b(x,y)(f(x)-f(y))^2.
\]

For a finitely supported `u`, and a function `w` integrable against each conductance row, symmetry gives

\[
\frac12\sum_{x,y}b(x,y)(u(x)-u(y))(w(x)-w(y))
=\sum_xu(x)\sum_yb(x,y)(w(x)-w(y)). \tag{6}
\]

The sum of the absolute values on the left is at most

\[
2\sum_{x\in\operatorname{supp}u}|u(x)|
\sum_yb(x,y)(|w(x)|+|w(y)|)<\infty.
\]

This justifies the rearrangement even with infinitely many neighbors.

Fix an origin `o`, a finitely supported `f` with `f(o)=1`, and a finite set `B` containing its support and `o`. Let `H(x)` be the probability of hitting `o` before leaving `B`, set to zero outside `B`. Then `H(o)=1`, `0<=H<=1`, and `H` is harmonic on `B\{o}`. An irreducible chain exits the finite set `B\{o}` almost surely: from each state there is a positive-probability simple exit path of length at most the set's size, and the minimum of the finitely many path probabilities is positive. Successive blocks bound the probability of remaining forever by a geometric limit.

First-step analysis at `o` shows that `1-PH(o)` is the probability `q` of exiting `B` before returning to `o`. Equation (6) gives

\[
\mathcal E_b(H)=\mu(o)q.
\]

Since `f-H` vanishes at `o` and outside `B`, the mixed energy between `H` and `f-H` is zero. Thus

\[
\mathcal E_b(f)\ge\mathcal E_b(H)
\ge\mu(o)\Pr_o(\text{never return to }o). \tag{7}
\]

All functions used in this minimization are bounded and finitely supported, so their energies are finite. If there exist such `f` with energies tending to zero, (7) proves recurrence.

Finally, for an irreducible recurrent chain and a positive harmonic function `v`, the process `v(X_t)` is an integrable nonnegative martingale. It has an almost-sure finite limit. Recurrence and irreducibility imply infinitely many visits to every state, simultaneously since the state space is countable. The subsequence of visits to each state forces all values of `v` to equal the limit. Hence every positive harmonic function is constant.

## 4. Cutoff estimates valid beyond exponent two

Choose `R` large enough that `(-2R,2R)` contains at least two particles. Let

\[
f_R(n)=\min\{1,\max\{0,2-|a_n|/R\}\}.
\]

It is finitely supported, satisfies `f_R(0)=1`, and has difference bounded by `min(1,|a_j-a_n|/R)`. By (4), its `c^*` energy is at most `K(S_near+S_far)`, where each `S` is the unordered sum of

\[
g_ng_j(f_R(n)-f_R(j))^2(a_j-a_n)^{-s-1},\quad n<j,
\]

over respectively `a_j-a_n<=R` and `a_j-a_n>R`.

For any `p>0` and `n<j`, (2) implies the two integral comparisons

\[
g_j(a_j-a_n)^{-p}
\le(1+r)^p\int_{a_j}^{a_{j+1}}(t-a_n)^{-p}\,dt, \tag{8}
\]

\[
g_n(a_j-a_n)^{-p}
\le r(1+r)^p\int_{a_{n-1}}^{a_n}(a_j-t)^{-p}\,dt. \tag{9}
\]

For (8), the distance throughout the integration interval is at most `(1+r)(a_j-a_n)` because `g_j<=r g_{j-1}<=r(a_j-a_n)`. For (9), use `g_{n-1}<=r g_n<=r(a_j-a_n)` and then `g_n<=r g_{n-1}`. The additional factor `r` in (9) accounts for the different interval length.

### Full far tails

A pair with a nonzero cutoff difference has at least one endpoint in `(-2R,2R)`. Charge it to every such endpoint and replace the squared difference by one. At a fixed left endpoint, (8) with `p=s+1` bounds the entire right tail by `(1+r)^{s+1}R^{-s}/s`; (9) bounds the left tail at a fixed right endpoint by `r` times that quantity. These are infinite-tail estimates: the disjoint integration intervals are contained in the respective half-lines, whose integrals converge. Nonnegative countable additivity, or monotone convergence, justifies the infinite sums.

Let `m<M` be the extreme indices inside `(-2R,2R)`. Their gap weights satisfy

\[
\sum_{|a_n|<2R}g_n=(a_M-a_m)+g_M
\le(1+r)(a_M-a_m)\le4(1+r)R,
\]

because `g_M<=r g_{M-1}<=r(a_M-a_m)`. This explicitly includes the outgoing gap at the support boundary. Therefore

\[
S_{\rm far}\le\frac{4(1+r)^{s+3}}s R^{1-s}. \tag{10}
\]

It tends to zero for every fixed `s>1`.

### Near pairs

For a contributing near pair, both endpoints lie in `(-3R,3R)`. Set

\[
I_R=\{n:|a_n|<3R,\ g_n\le R\},
\quad N_R=|I_R|,\quad\Sigma_R=\sum_{n\in I_R}g_n.
\]

The intervals `[a_n,a_{n+1}]` indexed by `I_R` have disjoint interiors and lie in `(-3R,4R)`, so `Sigma_R<=7R`. For a fixed `n`, all `j>n` with `a_j-a_n<=R` are consecutive. Their integration intervals in (8) start at distance `g_n` and end by distance `(1+r)R`. Apply (8) with `p=s-1` and the Lipschitz cutoff bound to get

\[
S_{\rm near}\le
\frac{(1+r)^{s-1}}{R^2}
\sum_{n\in I_R}g_n\int_{g_n}^{(1+r)R}t^{1-s}\,dt. \tag{11}
\]

No step through (11) requires `s<=2`.

## 5. The new estimate and its endpoint

Let `A(L)=#{n:|a_n|<L}` and `T=sum_{n!=0}|a_n|^{-s}<infinity`. For `L>M>0`,

\[
\frac{A(L)}{L^s}
\le\frac{A(M)}{L^s}+\sum_{|a_n|\ge M}|a_n|^{-s}.
\]

Let `L` tend to infinity and then `M` tend to infinity. Local finiteness controls the first term and convergence of the positive force series controls the second. Thus

\[
A(L)=o(L^s),\qquad N_R\le A(3R)=o(R^s). \tag{12}
\]

Assume now `2<s<3`. For each gap in (11),

\[
\int_{g_n}^{(1+r)R}t^{1-s}\,dt
=\frac{g_n^{2-s}-((1+r)R)^{2-s}}{s-2}
\le\frac{g_n^{2-s}}{s-2}.
\]

The denominator is positive. For `q=3-s in (0,1)`, power concavity gives, if `N_R>0`,

\[
\sum_{n\in I_R}g_n^{3-s}
\le N_R^{s-2}\Sigma_R^{3-s}
\le N_R^{s-2}(7R)^{3-s}.
\]

If `N_R=0`, the near contribution is zero and the same conclusion is understood directly. Combining these inequalities with (11),

\[
S_{\rm near}
\le\frac{(1+r)^{s-1}7^{3-s}}{s-2}
N_R^{s-2}R^{1-s}. \tag{13}
\]

Write `epsilon_R=N_R/R^s`, so `epsilon_R>=0` and `epsilon_R->0` by (12). The power in (13) becomes

\[
S_{\rm near}
\le C_s\epsilon_R^{s-2}R^{s^2-3s+1},
\qquad C_s=\frac{(1+r)^{s-1}7^{3-s}}{s-2}. \tag{14}
\]

The polynomial `s^2-3s+1` is negative for `2<s<s_*` and zero at `s=s_*`. Since `2<s_*<3`, concavity applies also at the endpoint and `s_*-2>0`. Thus (14) tends to zero throughout `2<s<=s_*`; at the endpoint the little-o factor is essential. A mere big-O count would not establish that limit.

By (10), the total cutoff energy tends to zero. Apply (7) to `c^*`. Its chain is recurrent; then (5) and the positive-harmonic Liouville fact force `1/g` to be constant. All gaps equal some `h>0`, and telescoping gives `a_n=a_0+hn` for positive and negative indices. This proves the extended range.

## 6. Completion of the lower range

For clarity, the same estimates also reproduce Ferudun's lower range. If `1<s<2`, integrate (11) from zero instead of `g_n` to obtain

\[
S_{\rm near}\le\frac{7(1+r)}{2-s}R^{1-s}\longrightarrow0.
\]

At `s=2`, (11) contains `sum_n g_n log((1+r)R/g_n)`. Concavity bounds it by `Sigma_R log((1+r)RN_R/Sigma_R)`. For `Lambda=(1+r)RN_R`, the function `z log(Lambda/z)` is increasing through `Lambda/e`, and never exceeds `Lambda/e`. Splitting according as `Lambda>=7eR` or not gives

\[
S_{\rm near}\le\frac{7(1+r)}R
\max\left\{1,\log\frac{(1+r)N_R}{7}\right\}.
\]

The empty-set case is zero. Since `a_0=0`, `N_R<=1+(3R)^2T`; hence this upper bound is `O(log(R)/R)`. Combine with (10) and the same recurrence conclusion.

Conversely, every positive-spacing lattice has equal finite one-sided sums `h^{-s} sum_{k>=1} k^{-s}` for every `s>1`, so it satisfies (1).

## Limits of this deduction

- No conclusion about principal-value equilibria with infinite one-sided forces is proved.
- The set conclusion is independent of labeling; affine dependence on an index requires increasing enumeration.
- For `s>s_*`, the positive power of `R` in (14) cannot be discarded solely from `epsilon_R->0`. This is a limitation of the count-and-concavity estimate, not a counterexample to rigidity at larger exponents.
- Nothing here resolves all strictly decreasing force laws or verifies a global literature-priority claim.

## Primary references

- Alper Ferudun, [*Equilibria of Inverse-Square Repulsion on the Line Are Arithmetic Progressions*, arXiv:2610.06944v1](https://arxiv.org/abs/2610.06944v1), 3 October 2026. Theorem 1.2, Lemmas 2.1-2.4 and 3.1-3.3, Proposition 4.1, Remark 5.3.
- Agelos Georgakopoulos and Mihail N. Kolountzakis, [*On particles in equilibrium on the real line*, arXiv:1604.01649v1](https://arxiv.org/abs/1604.01649v1), 6 April 2016. The finite-one-sided-force convention is explicit on PDF page 2; Theorem 1 handles an attained extremal gap.
- Itai Benjamini, [*Points in equilibrium*](https://arquivo.pt/wayback/20201231041612id_/https://www.wisdom.weizmann.ac.il/~itai/equilibrium.pdf), May 2015, Question 0.1; also [Warwick 2015 problem list](https://warwick.ac.uk/fac/sci/maths/research/events/2014-15/nonsymposium/random/Openprobs.pdf), section 4, Question 5.
