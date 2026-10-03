# Cancellation models for negative fixed-point colors

## Scope and result

For a permutation of `[N]`, color each fixed point from `[k]` when `k` is a nonnegative integer. Write `A(N,k)` for the resulting count, extended polynomially in `k`.

Blitvić and Bóna ask for an interpretation at negative integer `k`, and separately for an interpretation of `A(2n,k)` at every integer `k` [1, pp. 303–304]. They already record the signed fixed-point interpretation. The negative values at odd sizes are therefore **not** a counterexample to their intended question.

This note gives:

1. An explicit finite, global cancellation construction for the even-size question, including a sign-reversing involution on permutations with negatively colored fixed points. Its surviving objects are ordered pairs of uncancelled, equal-endpoint Motzkin prefixes.
2. A simpler, locally specified colored-walk model for `A(2n,-1)`.
3. An obstruction to extending that particular local model by diagonal sign changes to any integer `k <= -2`.
4. A uniform unsigned graph model at each negative integer `k` for every size `N >= 4(1-k)`, together with odd-size sign information separating this eventual result from the remaining problem.

The global cancellation in item 1 enumerates and orders all prefixes before matching them. It is generic and potentially very inefficient; it is not a bounded-local rule or a new intrinsic characterization of surviving permutations. Under the literal meaning of a finite set of explicitly specified combinatorial objects, it answers the even-size subquestion. We do **not** claim that it meets a stronger intended naturalness requirement, is historically new, or resolves the original all-size question. The conservative overall status is **partial; original problem unresolved**.

The classical permutation/history correspondence and Jacobi coefficients used below are prior mathematics, especially [2, Theorems 1–2 and §4]. The present note gives the needed correspondence directly so that the cancellation maps can be checked without relying on an unspecified bijection.

## 1. Baseline identities and the sign issue

Let `D_j` count derangements of `[j]`, with `D_0=1`. Choosing the fixed-point set gives

\[
A(N,k)=\sum_{f=0}^N {N\choose f}D_{N-f}k^f.
\tag{1}
\]

The standard exponential formula gives, formally,

\[
\sum_{N\ge0}A(N,k)\frac{z^N}{N!}
=\frac{e^{(k-1)z}}{1-z},\qquad
A(N,k)=N!\sum_{j=0}^N\frac{(k-1)^j}{j!}.
\tag{2}
\]

In particular `A(0,k)=1`, and

\[
A(N,k)=N A(N-1,k)+(k-1)^N.
\tag{3}
\]

For `k=-m`, `m>=1`, (1) is the signed cardinality of `m`-colored fixed-point permutations, with sign `(-1)^f`. This signed interpretation is explicitly in [1], not a result of this note.

There is no single sign convention such as `(-1)^N` making every negative-color evaluation nonnegative: `A(1,-1)=-1`, `A(3,-1)=-2`, but `A(5,-1)=8`. Likewise an unsigned model for all `N,k<0`, without any sign qualification, is impossible. The source itself acknowledges this issue and asks for cancellation/interpretation beyond the known difference.

## 2. A fully specified signed permutation/history bijection

Fix `m>=1`. For a permutation `sigma` on `[N]`, scan `i=1,...,N`. At a boundary maintain two ordered lists:

- `U`: earlier sources whose forward edge has not yet ended;
- `L`: earlier targets whose backward edge has not yet started.

Both lists have the same size `h`: among processed vertices, the number of outgoing edges crossing the boundary equals the number of incoming edges crossing it. Lists are ordered by vertex label. Put `a=sigma^{-1}(i)` and `b=sigma(i)`.

- If `a=b=i`, record a horizontal fixed-point step carrying its color in `[m]`; give this step sign `-1`.
- If `a>i` and `b>i`, record an upstep, and append `i` to both lists.
- If `a<i` and `b<i`, record a downstep with an ordered pair `(p,q)` in `[h]^2`, where `p` is the rank of `a` in `U` and `q` the rank of `b` in `L`; remove those entries.
- If `a<i<b`, record a horizontal `U` step with the rank `p` of `a` in `U`; replace that entry by `i` and sort the list.
- If `b<i<a`, record a horizontal `L` step with the rank `q` of `b` in `L`; replace that entry by `i` and sort the list.

All non-fixed-point steps have sign `+1`. The height is `h`. The path starts and ends at zero and never goes below zero.

The inverse is constructive. An upstep opens one forward source and one backward target at the current vertex. A downstep closes the indicated source with the edge `source -> i` and the indicated target with `i -> target`. A horizontal `U` step closes `source -> i` and opens source `i`; a horizontal `L` step closes `i -> target` and opens target `i`. A fixed-point step installs `i -> i` with its color. At the end both lists are empty. Every vertex has exactly one incoming and one outgoing edge, so this is a permutation. The scans are inverse at each stage.

To symmetrize the labels, match each upstep from `h-1` to `h` to its usual stack-matched downstep from `h` to `h-1`. Transfer the first component `p` of that downstep's pair `(p,q)` to the upstep, and retain `q` on the downstep. This is invertible by the same stack matching. The resulting **symmetric histories** have:

- an upstep or downstep across the edge `{h-1,h}`, each with a label in `[h]`;
- horizontal `U` and `L` steps at height `h`, each with a label in `[h]`;
- horizontal fixed-point steps at any height with a label in `[m]` and sign `-1`.

The history sign equals `(-1)^{number of fixed points}`. Reversing a path preserves valid labels and sign because the upward and downward label sets on every edge agree. This symmetry is the reason to move the downstep label.

For `k>=0` use `[k]` positive fixed-point labels instead. At `k=0` there are none. This gives the analogous unsigned history model.

## 3. Explicit prefix cancellation and an even-size involution

For integer `k`, let `P(n,h;k)` be all symmetric histories of length `n`, starting at height zero and ending at `h`, without going below zero. They need not end at zero. Fixed-point labels have cardinality `|k|`, and sign `sgn(k)` when `k!=0`; all other labels have positive sign. These are finite sets; the height never exceeds `n`.

Fix the following total order once and for all. A step is coded by `(next height, type, label)`, where type is `0` for a nonhorizontal step, `1` for a horizontal `U` step, `2` for a horizontal `L` step, and `3` for a fixed-point step. Order complete code words lexicographically.

For each fixed `(n,h,k)`, process this ordered list using a stack:

1. If the stack is empty, or the top has the same sign as the next path, push that path.
2. Otherwise pair the next path with the stack top and pop the top.

Each pair has opposite signs. The stack always contains paths of one sign: this is immediate by induction under both operations. Let `mu` exchange the paired paths, and let `R(n,h;k)` be the remaining stack, regarded as a set. The restriction of `mu` to its paired domain is an involution. Every element of `R(n,h;k)` has the same sign. Neither this algorithm nor membership in `R` is defined using a value of `A`.

Define the unsigned finite set

\[
\mathcal C_{n,k}=
\coprod_{h=0}^n R(n,h;k)\times R(n,h;k).
\tag{4}
\]

An object is an endpoint and an ordered pair of surviving prefixes; discard their common sign.

**Theorem 1 (algorithmic even-size model).** For every `n>=0` and every integer `k`,

\[
|\mathcal C_{n,k}|=A(2n,k).
\tag{5}
\]

**Proof with an explicit cancellation map.** Split a closed symmetric history of length `2n` at its midpoint. It becomes an ordered pair `(P,Q)` in `P(n,h;k)^2`, where `Q` is the reverse of the second half. Reversal is a bijection and the original sign is `sign(P)sign(Q)`.

Apply the following map:

- If `P` is paired by `mu`, replace `P` by `mu(P)` and leave `Q` unchanged.
- Otherwise, if `Q` is paired, leave `P` unchanged and replace `Q` by `mu(Q)`.
- Otherwise, fix the pair.

Paired/unpaired status is invariant under `mu`, so the first applicable case stays the same on a second application. Thus this is an involution. In either nonfixed case exactly one prefix changes sign. In the fixed case both prefixes lie in `R(n,h;k)`, so their signs agree and their product is positive. The fixed points are exactly (4). Signed cardinality is preserved under cancelling the two-element orbits; the original signed cardinality is `A(2n,k)` by §2 and (1). This proves (5). Transporting the map through the explicit bijection in §2 gives an almost-bijection on the original fixed-point-colored permutations, pairing every negative object with a positive object. ∎

For `k>=0` there are no negative paths, so the stack cancels nothing. For `n=0`, (4) has the unique pair of empty paths. Zero net weight causes no special case: both sign populations cancel and `R` is empty.

**Limitation.** This model may require listing exponentially many prefixes. Its survivors depend on the chosen total order. It does not yield a simple pattern-avoidance description or a local fixed-point operation. The same half-path construction works for any symmetric integer signed graph. This genericity is a reason not to claim a new natural negative-color species or a resolution of the report's broader question.

## 4. Jacobi matrix and an explicit integral square identity

Let `J=J(k)` be the infinite symmetric tridiagonal matrix indexed by `h>=0` with

\[
J_{h,h}=2h+k,\qquad J_{h,h+1}=J_{h+1,h}=h+1.
\tag{6}
\]

Every power entry used here is a finite sum of walks, so no infinite-operator convergence is needed. Section 2 gives

\[
A(N,k)=(J^N)_{0,0}.
\tag{7}
\]

Set `c(n,h;k)=(J^n)_{0,h}`. Symmetry and multiplication yield

\[
A(2n,k)=\sum_{h=0}^n c(n,h;k)^2.
\tag{8}
\]

These are integer squares when `k` is an integer. In §3 the signed cardinality of `P(n,h;k)` is `c(n,h;k)`, and `|R(n,h;k)|=|c(n,h;k)|`; Theorem 1 supplies actual objects and an involution, beyond merely writing (8).

For a closed form, define `Q_h(y)=(-1)^h L_h(y)`, with

\[
L_h(y)=\sum_{j=0}^h {h\choose j}\frac{(-y)^j}{j!}.
\]

These ordinary Laguerre polynomials have unit norm and are mutually orthogonal for `e^{-y}dy` on `[0,infinity)`. Integration by parts in Rodrigues' formula gives, for `a>=h`,

\[
\int_0^\infty y^aQ_h(y)e^{-y}dy=a!{a\choose h},
\]

and zero for `a<h`. Equivalently, this follows by inserting the displayed finite polynomial and cancelling finite differences. Multiplication by `x=y+k-1` in the `Q_h` basis has exactly the coefficients (6). Thus

\[
c(n,h;k)=n!\sum_{j=0}^{n-h}
 {n-j\choose h}\frac{(k-1)^j}{j!}.
\tag{9}
\]

Each summand in (9) is integral for integer `k`, since `j<=n`. Equation (8) is also Parseval's identity for the polynomial `x^n`. For instance,

\[
A(4,k)=(k^2+1)^2+[2(k+1)]^2+2^2.
\]

The underlying continued fraction, orthogonal-polynomial model, and positivity mechanism are classical; no priority is claimed for (6)–(9).

## 5. A local unsigned graph when k = -1

Squaring (6) gives, for every real `k`,

\[
\begin{aligned}
(J^2)_{h,h}&=h^2+(2h+k)^2+(h+1)^2,\\
(J^2)_{h,h+1}&=2(h+1)(2h+k+1),\\
(J^2)_{h,h+2}&=(h+1)(h+2).
\end{aligned}
\tag{10}
\]

The matrix is symmetric and other entries vanish. At `k=-1` every entry is a nonnegative integer. Define a colored directed graph on the nonnegative integers, with

- `6h^2-2h+2` loop colors at `h`;
- `4h(h+1)` edge colors for either direction between `h` and `h+1`;
- `(h+1)(h+2)` edge colors for either direction between `h` and `h+2`.

Color labels are simply integers from one to the stated multiplicity. A walk distinguishes the order of its vertices and its edge colors. By (7) and (10):

**Theorem 2.** `A(2n,-1)` counts length-`n` closed colored walks from vertex zero in this graph.

This local model requires no prefix enumeration. It gives `1,2,8,112,5504,...` at `n=0,1,2,3,4`.

The same graph also gives a local interpretation at every odd size at least five. Direct multiplication in (6) gives

\[
J(-1)^5e_0=(8,120,320,480,360,120,0,\ldots)^T=:v.
\tag{10a}
\]

Thus `A(2n+5,-1)` counts length-`n` walks from zero in the same graph, with one of `v_h` terminal colors when the endpoint is `h`. Indeed the count is `e_0^T(J^2)^n v`. At `n=0` this is eight objects. Together with Theorem 2 and the explicit negative values at sizes one and three, this covers the entire `k=-1` sequence with two signed exceptional sizes.

For endpoints `(0,1)`, a direct two-step cancellation at `k=-1` cancels the two negative histories (a fixed-point horizontal before or after the uniquely labeled upstep) against the two positive histories consisting of that upstep and a horizontal `U` or `L` step at height one. This explains the zero multiplicity between zero and one. All other endpoint pairs have nonnegative signed multiplicity by (10); the graph formulation is the definition of the objects in Theorem 2.

## 6. Why a diagonal sign change does not extend Theorem 2

An immediate attempted extension is to replace `K=J(k)^2` by `D K D`, where `D` is diagonal with entries `+1` or `-1`. This preserves the `(0,0)` entries of all powers. But for every integer `k<=-2`, it cannot make all entries nonnegative.

**Proposition 3.** For each integer `k<=-2`, `K` has a cycle of nonzero edges whose product is negative. Consequently no such `D` makes `D K D` entrywise nonnegative.

**Proof.** Products around a cycle do not change under `D`, because every vertex sign appears twice. Distance-two entries of `K` are strictly positive.

If `k=-2s`, `s>=1`, use the triangle `s-1, s, s+1, s-1`. The first distance-one edge is negative, the second positive, and the distance-two edge positive by (10).

If `k=-(2s+1)`, `s>=1`, use the four-cycle `s-1, s, s+2, s+1, s-1`. The first edge is negative; the two distance-two edges and the distance-one edge between `s+1` and `s+2` are positive. The zero edge between `s` and `s+1` is not used. Thus the cycle product is negative in both cases. ∎

This obstructs only a specific matrix/gauge method. It is not evidence against other unsigned models; Theorem 1 already gives a global model.

## 7. Odd sizes: sign structure and the remaining gap

The shifted-exponential identity in [1] is

\[
A(N,k)=\int_0^\infty (y+k-1)^N e^{-y}\,dy.
\tag{11}
\]

Every even moment is strictly positive, including `A(0,k)=1`. Differentiating the finite polynomial or (2) gives

\[
\frac{\partial}{\partial k}A(N,k)=N A(N-1,k).
\tag{12}
\]

Thus, for each odd `N`, `A(N,k)` is strictly increasing on the real line and has exactly one real zero: its derivative is positive and its leading term is `k^N`. This is information about sign, not an interpretation of the integer values.

For a fixed negative integer `k`, write `r=1-k>=2` and `S_N=A(N,k)/N!`. Equation (2) implies eventual positivity, since `S_N -> e^{-r}>0`. More explicitly, the odd subsequence has increments

\[
S_{N+2}-S_N=\frac{r^{N+1}}{(N+1)!}
 \left(1-\frac r{N+2}\right),\qquad N\text{ odd}.
\tag{13}
\]

It first decreases (possibly with one equal step) and thereafter strictly increases to a positive limit. Because `S_1=1-r<0`, it crosses zero at most once and eventually is positive. No assertion that equality never occurs at an integer parameter is needed.

A useful nonnegative-coefficient recurrence after a sign-stable starting range is

\[
A(N,k)=(N-r)A(N-1,k)+r(N-1)A(N-2,k),\quad N\ge2.
\tag{14}
\]

It follows by eliminating `(-r)^{N-1}` between consecutive copies of (3). For `k=-1`, seeds `A(4,-1)=A(5,-1)=8` and (14) give a simple recursive counting class for all sizes `N>=4`: start with eight objects at each of sizes four and five; for `N>=6`, take the disjoint union of `[N-2]` times the size-`N-1` class and `[2(N-1)]` times the size-`N-2` class. At sizes one and three the negative sign must still be recorded. This seeded recursive class is another elementary model, not a natural permutation description or a new theorem about the sequence.

The half-path proof does not solve the odd case. Cutting at unequal lengths gives terms `c(n,h;k)c(n+1,h;k)`, whose signs need not agree. After prefix cancellation the residual pairs can still have both signs. For example, for `k=-1,n=2`, the common-height products are `-4,0,12` and sum to `A(5,-1)=8`. At least one further inter-height cancellation is required. Simply pairing all remaining signed objects in a global ranking would be possible for any signed enumeration, but would not supply the missing structural explanation. We do not count that tautological maneuver as a resolution.

## 8. Uniform eventual unsigned models for every negative integer

The previous global cancellation answers the even finite-set question. A different approach produces nonnegative, finite-band transfer weights at all sufficiently large sizes for each fixed negative color. It does not settle every odd size.

**Lemma 4 (Laguerre linearization with nonnegative integers).** Write

\[
Q_i(y)Q_j(y)=\sum_{h=0}^{i+j}\ell_{ijh}Q_h(y).
\]

Then all `ell_ijh` are nonnegative integers, determined by

\[
\sum_{i,j,h\ge0}\ell_{ijh}u^iv^jw^h
=\frac1{1-uv-uw-vw-2uvw}.
\tag{15}
\]

**Proof.** The generating function of `Q_h=(-1)^h L_h` is
`G(u,y)=(1+u)^{-1} exp(yu/(1+u))`. All integrations below are coefficientwise; every coefficient is a polynomial times `e^{-y}`, so it is a finite factorial calculation. Integrating `G(u,y)G(v,y)` against `e^{-y}dy` gives `1/(1-uv)`, proving orthonormality. Integrating three copies gives the right side of (15). Therefore its coefficients are exactly the expansion coefficients by orthonormality. Expanding the denominator as a geometric series proves nonnegativity and integrality. More concretely, `ell_ijh` counts words over the five-letter alphabet with monomial weights `uv, uw, vw, uvw, uvw`, whose total weight is `u^iv^jw^h`. These classical Laguerre linearization facts are derived here for completeness. ∎

**Lemma 5 (a uniform positive-prefix bound).** Let `k=-m`, `r=m+1`, and `N>=4r-1`. Then `c(N,h;k)>0` for every `0<=h<=N`.

**Proof.** Integrating the Rodrigues expression by parts gives

\[
c(N,h;k)={N\choose h}\int_0^\infty
 (y-r)^{N-h}y^h e^{-y}\,dy.
\tag{16}
\]

If `N-h` is even, the integral is strictly positive. Otherwise, the absolute value of its negative part is at most

\[
\int_0^r(r-y)^{N-h}y^h\,dy
=\frac{r^{N+1}h!(N-h)!}{(N+1)!}
\le\frac{r^{N+1}}{N+1}.
\]

The positive part, after `y=x+r`, is at least
`e^{-r} integral_0^infinity x^N e^{-x} dx = e^{-r}N!`.
Put `M=N+1>=4r`. The elementary bound
`log(M!) >= M log M-M+1` yields

\[
\log\frac{M!}{r^M}
\ge M(\log(M/r)-1)+1
\ge4r(\log4-1)+1>r,
\]

using `log4>5/4`. Thus `e^{-r}N! > r^{N+1}/(N+1)` and the positive part strictly dominates. ∎

**Theorem 6 (eventual nonnegative transfer).** If `k<0` is an integer and `r=1-k`, then `J(k)^N` is entrywise nonnegative for every `N>=4r-1`.

**Proof.** The matrix entry is

\[
(J^N)_{ij}=\int_0^\infty(y-r)^N Q_i(y)Q_j(y)e^{-y}dy
=\sum_{h=0}^{i+j}\ell_{ijh}c(N,h;k).
\tag{17}
\]

For `h>N`, `c(N,h;k)=0` by orthogonality. For the other terms Lemmas 4 and 5 apply. Thus (17) is a sum of nonnegative integers. ∎

This gives a completely specified unsigned walk model, with no value of `A` used as a prescribed multiplicity. Fix `s=4r`, and form a graph on the nonnegative integers with

\[
T_{ij}=\sum_{h=0}^{s}\ell_{ijh}c(s,h;k)
\tag{18}
\]

colors for the directed edge from `i` to `j`, using (9) and (15) to compute the multiplicities. These are nonnegative integers. They vanish for `|i-j|>s`, since `T=J^s`; every bounded-length path enumeration is finite. For `0<=t<s`, give endpoint `h` the number of terminal colors
`v^{(t)}_h=c(s+t,h;k)`, zero for `h>s+t`.

For any `N>=s`, uniquely write `N=qs+t` with `q>=1` and `0<=t<s`. Count walks of length `q-1` from zero in this graph, followed by a terminal color of type `t`. Their count is

\[
e_0^T T^{q-1}v^{(t)}
=e_0^T J^{(q-1)s}J^{s+t}e_0=A(N,k).
\tag{19}
\]

This model has large parameter-dependent blocks and multiplicities, and the positivity proof used an analytic estimate. It is an eventual unsigned interpretation, not a small or intrinsic negative-color arrangement class. It leaves an unbounded family of short odd ranges as `k` varies. The all-size question in the source remains unresolved by this packet; the even-size interpretation in §3 remains explicitly global.

## References and attribution

[1] N. Blitvić and M. Bóna, “A probabilistic interpretation points to new combinatorial results for k-arrangements,” in *Mini-Workshop: Permutation Patterns*, Oberwolfach Reports 21 (2024), pp. 302–304. [Publisher's report](https://ems.press/content/serial-article-files/48646), [DOI](https://doi.org/10.4171/OWR/2024/6). The definitions, recurrence, generating function, integral, signed interpretation and target questions are credited here.

[2] N. Blitvić and E. Steingrímsson, *Permutations, moments, measures*, Transactions of the American Mathematical Society 374 (2021), 5473–5508. [arXiv:2001.00280](https://arxiv.org/abs/2001.00280), [author manuscript](https://strathprints.strath.ac.uk/74210/1/Blitvic_Steingrimsson_TAMS_2020_Permutations_moments_measures.pdf). Their labeled-Motzkin/continued-fraction framework and earlier work cited there supply the classical background. The author manuscript labels the negative-k question Remark 3; the OWR report cites the published numbering Remark 3.8.

[3] [OEIS A000023](https://oeis.org/A000023), the specialization `A(N,-1)`. Its signed interpretation and basic recurrence are prior art, and it lists the second-order recurrence (14) at `r=2`.

This is AI-assisted, unrefereed research exposition and verification. No first-resolution or publication-priority claim is made.
