# Partial results for the finite Riesz-potential majorant problem

## 0. Statement, notation, and status

Fix a real number `0 < alpha < 1`. Put

\[
 k_\alpha(s)=|s|^{-\alpha},\qquad
 T\mu(x)=\int_{\mathbb R}k_\alpha(x-t)\,d\mu(t),
\]

with `k_alpha(0)=+infinity`. Here `mu` is a nonnegative finite Borel measure on `R`; its mass is denoted by `M`. Values of the potential in `[0,+infinity]` are allowed. The zero measure has zero potential, including at every point. We use positive in the nonnegative-measure sense, allowing the zero measure for mass-attainment statements. Excluding the zero measure would not change existence of a majorant, since a nonzero positive measure can always be added. For a nonnegative integrable density `phi`, `T phi` means `T(phi dx)`.

The target is an intrinsic characterization of nonnegative measurable pointwise obstacles `f` for which `f <= T mu` everywhere for some such measure. The source does not specify a probability normalization, compact support, absolute continuity, or an almost-everywhere exception. We impose none of those on the target. Whenever singular-measure pairings are used below the obstacle is explicitly Borel. The almost-everywhere theorem allows any Lebesgue-measurable obstacle. All separating examples below are finite-valued Borel functions, so no ambiguity about extended-valued obstacles or completions is needed for the negative conclusions.

The proofs here settle useful special cases and disprove candidate simplifications. They do not settle the full target. The methods are elementary potential estimates, measure duality, interval constructions, and Cantor measures; no novelty is asserted. Standard Tonelli, dominated convergence, Banach-Alaoglu, finite-dimensional separation, and Riesz representation are used explicitly. No external theorem about Riesz capacity is required.

## 1. Universal necessary bounds

### Lemma 1.1: an integral bound on arbitrary sets

If a Lebesgue-measurable set `E` has finite length `L`, then, for every `t`,

\[
 \int_E |x-t|^{-\alpha}\,dx
 \le C_\alpha L^{1-\alpha},
 \qquad C_\alpha=\frac{2^\alpha}{1-\alpha}.
 \tag{1}
\]

For `L=0` the integral is zero. For `L>0`, layer cake bounds the left side by

\[
 \int_0^\infty\min\{L,2s^{-1/\alpha}\}\,ds
 =\frac{2^\alpha}{1-\alpha}L^{1-\alpha}.
\]

Equivalently, the centered interval of length `L` maximizes the integral of this symmetric decreasing kernel. By Tonelli,

\[
 \int_E T\mu\,dx\le C_\alpha M L^{1-\alpha}.
 \tag{2}
\]

In particular every finite-measure potential is locally integrable, and is finite Lebesgue-almost everywhere. Every pointwise or almost-everywhere dominated obstacle obeys (2). Applying it to finite subsets of `{f>lambda}` gives

\[
 |\{f>\lambda\}|\le (C_\alpha M/\lambda)^{1/\alpha}
 \quad(\lambda>0).
 \tag{3}
\]

To justify finiteness of the set before using its total measure, intersect with `[-R,R]` and then let `R` increase. Thus weak `L^(1/alpha)` is necessary. It will not be sufficient.

### Lemma 1.2: bounded-potential tests

Let `f` be nonnegative Borel, and let `nu` be a finite nonnegative Borel measure with `T nu <= B` everywhere, where `B<infinity`. If `f <= T mu` everywhere, then

\[
 \int f\,d\nu\le \int T\mu\,d\nu
 =\int T\nu\,d\mu\le BM.
 \tag{4}
\]

This is Tonelli for the nonnegative symmetric kernel, including its diagonal singularity. If `nu` is absolutely continuous, the same conclusion follows from Lebesgue-almost-everywhere domination. For singular `nu`, almost-everywhere domination in Lebesgue measure is not enough.

The statement applies to finite `nu`; any test constructed below is finite. For a general Lebesgue-measurable `f`, integration against a singular Borel measure need not be defined without specifying a representative or a completion. We do not silently use (4) in that generality.

## 2. Equimeasurable obstacles with opposite answers

This section works for every fixed `alpha` in `(0,1)`.

Set

\[
 q=2^{-1/\alpha},\quad \ell_n=q^n,\quad a_n=2^n,
 \quad I_n=[3n,3n+\ell_n],\qquad n\ge1.
\]

Because `q<1/2`, the intervals are disjoint and have length less than `1/2`. Define

\[
 f_{\rm sep}(x)=\sum_{n\ge1}a_n\mathbf1_{I_n}(x).
 \tag{5}
\]

It is finite-valued and Borel. Its integral is `sum (2q)^n < infinity`. Its distribution function is bounded by a constant times `lambda^(-1/alpha)`, as follows either by summing the geometric tail of the interval lengths or from the rearranged majorant constructed below.

### Proposition 2.1: the separated function has no majorant

Define

\[
 d\nu_n(x)=\ell_n^{\alpha-1}\mathbf1_{I_n}(x)\,dx,
 \qquad \nu=\sum_{n\ge1}\nu_n.
\]

Then `nu_n(R)=ell_n^alpha=2^(-n)` and `nu(R)=1`. By (1),

\[
 T\nu_n(t)\le C_\alpha\quad\hbox{for every }t.
 \tag{6}
\]

For each `n`, put `J_n=(3n-1,3n+1)`. These open intervals are disjoint. If `t` belongs to `J_n`, its distance to every `I_m`, `m != n`, exceeds `1`, so their total contribution to `T nu(t)` is at most `1`. The contribution from `I_n` is bounded by (6). If `t` is outside all the `J_n`, its distance to every `I_n` is at least `1/2`, so `T nu(t) <= 2^alpha`. Consequently the convenient uniform bound

\[
 T\nu(t)\le B_\alpha:=C_\alpha+2^\alpha
 \tag{7}
\]

holds everywhere. On the other hand,

\[
 \int f_{\rm sep}\,d\nu
 =\sum_{n\ge1}a_n\ell_n^\alpha
 =\sum_{n\ge1}1=+\infty.
 \tag{8}
\]

Since `nu` is absolutely continuous, (4) rules out a finite-measure majorant even in the Lebesgue-almost-everywhere sense. More quantitatively, its first `N` component tests force the mass of a majorant of the first `N` spikes to be at least `N/B_alpha`.

### Proposition 2.2: an equimeasurable function has an atomic majorant

Let

\[
 H_n=\sum_{k\ge n}\ell_k=\frac{q^n}{1-q},
 \qquad A_n=(H_{n+1},H_n].
\]

The intervals `A_n` have length `ell_n` and are disjoint. Define

\[
 f_{\rm near}(x)=\sum_{n\ge1}a_n\mathbf1_{A_n}(x),
 \qquad f_{\rm near}(0)=0.
 \tag{9}
\]

It is zero outside their union. It is finite-valued and Borel, and its level-set lengths agree exactly with those of (5), up to irrelevant endpoint sets of Lebesgue measure zero. For `x in A_n`,

\[
 a_n x^\alpha\le a_n H_n^\alpha=(1-q)^{-\alpha}.
\]

Thus, with `c=(1-q)^(-alpha)`,

\[
 f_{\rm near}(x)\le c|x|^{-\alpha}=T(c\delta_0)(x)
 \tag{10}
\]

at every nonzero `x`, and also at zero under the stated convention. Formula (3) then proves the weak endpoint assertion for both equimeasurable functions.

**Consequence.** No criterion depending only on the Lebesgue distribution function, the decreasing rearrangement, or membership and norms in rearrangement-invariant spaces can characterize the target class. This is a counterexample to those candidate criteria, not to the open-ended source problem.

## 3. An exact dual theorem for almost-everywhere domination

For a nonnegative Lebesgue-measurable function `f`, define

\[
 D_\alpha(f)=\sup\left\{\int f(x)\phi(x)\,dx:
  \phi\in C_c^\infty(\mathbb R),\ \phi\ge0,
  \|T\phi\|_\infty\le1\right\}.
 \tag{11}
\]

All integrals are nonnegative extended integrals. The zero test is allowed. If the value is finite, a smooth nonnegative cutoff positive on any chosen compact interval shows `f` is locally integrable. For every such smooth `phi`, `T phi` is bounded, continuous, and vanishes at infinity: near the kernel singularity use its local integrability and boundedness of the density; away from it use dominated convergence; at infinity use compactness of the density's support. Thus `T phi` belongs to `C_0(R)`.

### Theorem 3.1

For every real `C>=0`, the following are equivalent:

1. `D_alpha(f) <= C`.
2. There is a finite nonnegative Borel measure `mu` with `mu(R)<=C` and `T mu >= f` Lebesgue-almost everywhere.

If the value in (11) is finite, it equals the least possible mass in (2), and that least mass is attained.

**Proof.** Direction (2) to (1) is (4) with `nu=phi dx`.

For the converse, let `P_C` be the positive part of the closed mass-`C` ball of `C_0(R)^*`. By Banach-Alaoglu and the Riesz representation theorem it is a compact space, in the weak-star topology, of finite positive Borel measures. Positivity is weak-star closed. Loss of mass to infinity is permitted; the inequality is a mass upper bound, not a prescribed total mass.

For each nonnegative smooth compactly supported `phi`, impose the closed condition

\[
 \int T\phi\,d\mu\ge \int f\phi\,dx.
 \tag{12}
\]

It is closed because `T phi` is in `C_0(R)`. We prove the finite-intersection property. For tests `phi_1,...,phi_m`, let `y_i=int f phi_i`, and let `S` be the compact convex set of vectors `(int T phi_i dmu)_i` for `mu in P_C`. If `S` did not intersect `y+R_+^m`, finite-dimensional strict separation would give coefficients `b_i>=0` such that

\[
 \sup_{\mu\in P_C}\sum_i b_i\int T\phi_i\,d\mu
 <\sum_i b_i y_i.
 \tag{13}
\]

The coefficients must be nonnegative because the other separated set is unbounded in every positive coordinate direction. With `Phi=sum b_i phi_i`, the left side is exactly `C ||T Phi||_infinity`: a positive measure of mass `C` can be placed at a maximum of the nonnegative `C_0` function `T Phi` (or use the supremum directly). The right side is `int f Phi`, which is at most `C ||T Phi||_infinity` by (11) and scaling. The zero-function case is immediate. This contradicts (13).

Compactness now supplies one measure satisfying (12) for every test. Tonelli and (2) show `T mu` is locally integrable, and (12) becomes `int (T mu-f)phi >=0` for all nonnegative smooth compactly supported tests. Therefore `T mu-f>=0` Lebesgue-almost everywhere. Finally take `C=D_alpha(f)` to obtain attainment and use the already-proved necessity for equality of optimal values. This includes `D_alpha(f)=0`. QED.

### Lemma 3.2: local averages recover every potential value

For `A_r h(x)=(2r)^(-1) int_(x-r)^(x+r) h(y)dy`,

\[
 \lim_{r\downarrow0}A_r(T\mu)(x)=T\mu(x)
 \quad\hbox{at every }x,
 \tag{14}
\]

including points where the right side is infinite.

For a fixed `s`, `A_r k_alpha(s)` tends to `k_alpha(s)`, including infinity at `s=0`. Uniformly in `r`,

\[
 A_r k_\alpha(s)\le
 \frac{2^\alpha}{1-\alpha}k_\alpha(s).
 \tag{15}
\]

For `|s|>=2r`, use `|s-u|>=|s|/2`. For `0<|s|<2r`, (1) applied to an interval of length `2r` gives `A_r k_alpha(s)<=r^(-alpha)/(1-alpha)`, which implies (15). At `s=0` the bound has an infinite right side. If `T mu(x)<infinity`, dominated convergence against `mu` proves (14); an atom at `x` is then impossible. If `T mu(x)=infinity`, Fatou's lemma yields an infinite lower limit and proves (14) as an extended-valued assertion.

### Corollary 3.3: lower semicontinuous obstacles

If `f` is nonnegative lower semicontinuous, Theorem 3.1 holds with **everywhere** in place of **almost everywhere**, with the same mass and attainment conclusions.

Indeed lower semicontinuity implies `f(x)<=liminf A_r f(x)`. Almost-everywhere domination implies `A_r f(x)<=A_r T mu(x)` for every `r>0`, and (14) gives the assertion. The reasoning also works when `f(x)=infinity`, by testing every finite lower bound near `x`.

Every `T mu` itself is lower semicontinuous by Fatou's lemma. Consequently one can reformulate the original question as existence of a lower semicontinuous `g>=f` with `D_alpha(g)<infinity`. We do **not** count that existential-envelope reformulation as the requested intrinsic characterization of arbitrary measurable `f`.

## 4. Why the almost-everywhere theorem does not solve the pointwise problem

### Proposition 4.1: harmless countable exceptional sets

If `E={x_1,x_2,...}` is countable and `epsilon>0`, the measure

\[
 \sigma=\epsilon\sum_{j\ge1}2^{-j}\delta_{x_j}
 \tag{16}
\]

has mass at most `epsilon` and infinite potential at each `x_j`. Finite sets are handled by truncating the sum. Thus any prescribed nonnegative values supported on a countable set can be dominated with arbitrarily small positive mass. A countable exceptional set in a known majorant can be repaired by adding (16).

This does not imply that arbitrary Lebesgue-null sets can be repaired.

### Proposition 4.2: a compact null-set obstruction, for every alpha

Choose `r` with `2^(-1/alpha)<r<1/2`. Construct the two-interval Cantor set `E` using the contractions `x -> r x` and `x -> 1-r+r x`, and let `nu` be its uniform probability measure: each level-`n` basic interval has mass `2^(-n)` and length `r^n`. The coding is unique because the two child intervals are separated. The measure has no atoms, since masses of nested basic intervals tend to zero. The total lengths `(2r)^n` tend to zero, so `E` is Lebesgue null.

We give a direct uniform bound on `T nu`, without invoking a capacity theorem. Distinct level-`n` basic intervals have separating gaps of length at least `(1-2r)r^(n-1)` for `n>=1`. An interval of length `2r^n` can meet at most

\[
 K_r=2+\frac{2r}{1-2r}
\]

of these intervals, with this noninteger expression used simply as an upper bound on the integer count. To see it, if `m` intervals are met, the `m-2` internal gaps already lie inside the test interval; hence `(m-2)(1-2r)r^(n-1)<=2r^n`. Therefore

\[
 \nu(B(x,r^n))\le K_r2^{-n}
 \quad(n\ge0),
 \tag{17}
\]

where for `n=0` the bound follows from total mass one. Split the potential into distances at least one and the annuli `r^(n+1)<=|x-t|<r^n`. Boundary distances can be assigned to one adjacent annulus; the estimate is unaffected. There is no contribution from a diagonal atom. It follows that

\[
 T\nu(x)\le
 1+K_r r^{-\alpha}\sum_{n\ge0}
       (r^{-\alpha}/2)^n
 =1+\frac{K_r r^{-\alpha}}{1-r^{-\alpha}/2}
 =:B_{\alpha,r}<\infty,
 \tag{18}
\]

uniformly in `x`. The denominator is positive by the choice of `r`.

Let `E_n` consist of Cantor points whose first `n-1` digits are left and whose `n`th digit is right. These sets are Borel and pairwise disjoint, `nu(E_n)=2^(-n)`, and their union is `E\{0}`. Set

\[
 f_E(x)=\begin{cases}
 2^n,&x\in E_n,\\
 0,&x\notin\bigcup_{n\ge1}E_n.
 \end{cases}
 \tag{19}
\]

This is a finite-valued nonnegative Borel function, equal to zero Lebesgue-almost everywhere. Nevertheless `int f_E dnu=sum 1=infinity`. Equations (4) and (18) rule out any everywhere finite-measure majorant.

In particular `D_alpha(f_E)=0`, while no pointwise majorant exists. Hence an assertion that (11) characterizes the original measurable pointwise class would be false, not merely unproved.

For a completely rational construction of the geometry at `alpha=1/2`, take `r=1/3`. Then `K_r=4`, `sqrt(3)<7/4`, and `sqrt(3)/2<7/8`. Formula (18) gives the convenient exact coarse bound `T nu<57`. The first `N` levels of (19) force mass at least `N/57` for any majorant. These constants are intentionally nonsharp.

## 5. An explicit sufficient interval-cover criterion and its limitation

### Proposition 5.1

Suppose there are bounded nondegenerate intervals `I_j` of length `L_j`, centers `c_j`, and coefficients `b_j>=0` such that

\[
 f(x)\le\sum_j b_j\mathbf1_{I_j}(x)
 \quad\hbox{everywhere},\qquad
 \sum_j b_j L_j^\alpha<\infty.
 \tag{20}
\]

Then the finite atomic measure

\[
 \mu=\sum_j b_j(L_j/2)^\alpha\delta_{c_j}
 \tag{21}
\]

dominates `f` pointwise. Indeed each summand contributes at least `b_j` on its own interval; the inequality is also valid at the center because the atom's potential there is infinite. Its mass is `2^(-alpha) sum b_j L_j^alpha`. Endpoint conventions for the intervals do not affect the bound. Zero coefficients can be discarded to avoid a symbolic `0 times infinity`.

This permits overlap and arbitrary countably many intervals. A separate countable exceptional set can be covered using (16). It is a constructive sufficient test using only scalar costs and interval coverage.

### Proposition 5.2: this test is strictly stronger than majorizability

Define

\[
 h(x)=|x|^{-\alpha}\mathbf1_{\{0<|x|\le1\}}(x),
 \qquad h(0)=0.
\]

It is finite-valued and dominated pointwise by `T delta_0`. Let

\[
 w(x)=|x|^{\alpha-1}\mathbf1_{\{0<|x|\le1\}}(x).
\]

For every interval `I` of length `L`, symmetric decreasing rearrangement, or the layer-cake proof of (1) with exponent `1-alpha`, gives

\[
 \int_I w\,dx\le \frac{2^{1-\alpha}}{\alpha}L^\alpha.
 \tag{22}
\]

But `int h w dx=2 int_0^1 dx/x=infinity`. If a cover satisfying (20) existed, Tonelli and (22) would make that integral finite. This contradiction proves strictness. Adding a countable repair does not alter this integral contradiction. A sum of interval costs cannot be treated as a necessary condition merely because it constructs a valid majorant.

## 6. The general dual route and the finite-constraint trap

For a nonnegative Borel obstacle, Lemma 1.2 proves the necessary condition

\[
 \sup\{\int f\,d\nu:\nu\ge0\text{ finite Borel},\ T\nu\le1\}<\infty.
 \tag{23}
\]

Unlike (11), this condition detects the Cantor obstruction. No sufficiency proof of (23) for arbitrary Borel pointwise obstacles is supplied here. Its equality with a suitable outer majorant capacity, any required capacitability theorem, and a repair of exceptional sets would need to be established with precisely the stated kernel and quantifiers. They are not consequences of the finite-dimensional argument alone.

In particular, copying the compactness proof of Theorem 3.1 and replacing (12) with point constraints fails. For any point `x`, the measures `epsilon delta_x` tend weak-star to zero as `epsilon` tends to zero, while their potentials are infinite at `x`. Thus `{mu:T mu(x)>=1}` is not weak-star closed.

Every finite set of constraints, even with arbitrarily large target values, is feasible with arbitrarily small mass by atoms. The same is true of every countable set, including a dense countable set, by (16). Yet the everywhere obstacle `f=1` is impossible: applying (2) to `[-R,R]` would require

\[
 2R\le C_\alpha M(2R)^{1-\alpha}
 \quad\hbox{for all }R,
\]

or `(2R)^alpha<=C_alpha M`, a contradiction as `R` increases. Consequently finite or dense-countable point sampling cannot certify the intended infinite system. Lower semicontinuity of the potential does not repair this failure; values on a dense set do not force its values from below at all other points.

There is also a mass-attainment distinction. For `f=1_{\{0\}}`, the infimum of pointwise-majorant masses is zero, but no zero-mass measure majorizes it. Theorem 3.1's mass attainment is therefore not transferable to arbitrary pointwise obstacles.

## 7. What remains unresolved

We have a complete smooth-test answer for the almost-everywhere variant and for lower semicontinuous obstacles, but no complete answer for arbitrary measurable pointwise obstacles. The separated-spike example excludes rearrangement-only answers. The Cantor example excludes an almost-everywhere reduction. The atom example excludes naive pointwise weak-star compactness and finite sampling. The interval-cover criterion is constructive but not necessary.

The five approaches leave a specific gap: prove or replace a sufficient singular-measure/outer-capacity criterion which deals with all pointwise exceptional sets and does not merely restate existence of the desired measure or of an unspecified potential majorant. No source-attribution finding is represented as inspection of a full external proof, and no finite computation is represented as establishing these analytic theorems.

