# Partial results for Function Theory 5.60

**Status: unsolved.** These are self-contained partial results and reductions, not a complete solution and not a novelty claim. Independent review is pending. All powers use the analytic branch equal to 1 at the origin. Write \(D=\{z:|z|<1\}\).

## 1. Exact target and normalization

For real \(\alpha,\beta\ge1\), put
\[
 K_{\alpha,\beta,x}(z)=(1+xz)^\alpha(1-z)^{-\beta}.
\]
For every analytic \(\phi\) on \(D\), does
\[
 (\phi*K_{\alpha,\beta,x})(z)\ne0
 \quad (|x|=1,\ z\in D)
 \tag{H}
\]
imply the same assertion with \(\alpha\) replaced by \(\alpha-1\)? Here \(*\) means coefficientwise multiplication. The question includes every real noninteger \(\alpha>1\), every real \(\beta\ge1\), and all analytic \(\phi\), without coefficient-sign restrictions. At \(z=0\), (H) implies \(\phi(0)\ne0\); divide by this constant and write \(\phi(z)=\sum_{n\ge0}a_nz^n\), \(a_0=1\).

The exact primary source is Hayman–Lingham, *Research Problems in Function Theory (New Edition)*, arXiv:1809.07200, Problem and Update 5.60, printed pp. 107–108. It records the integer-\(\alpha\) case as known, citing Sheil-Small (1980). It does not report a solution of the noninteger case. No later full resolution was located in the bounded source search described in SOURCE_GATE.md.

## 2. A bidisc reformulation

Define
\[
 F_{\alpha,\beta}(u,v)=\sum_{k,j\ge0}
 a_{k+j}{\alpha\choose k}\frac{(\beta)_j}{j!}u^kv^j.
 \tag{1}
\]
This series is analytic on \(D^2\). Indeed, on \(|u|,|v|\le r<R<1\), Cauchy's estimate gives \(|a_n|\le M_RR^{-n}\), and the absolute double series is at most
\[
 M_R\left(\sum_{k\ge0}|{\alpha\choose k}|(r/R)^k\right)
 \left(\sum_{j\ge0}\frac{(\beta)_j}{j!}(r/R)^j\right)<\infty.
\]
Termwise differentiation is therefore valid on compact subsets. Also
\[
 F_{\alpha,\beta}(xz,z)=(\phi*K_{\alpha,\beta,x})(z).
 \tag{2}
\]

**Lemma 1 (equal-radius tori suffice).** An analytic \(F:D^2\to\mathbb C\) with \(F(0,0)=1\) is zero-free on \(D^2\) if it is zero-free whenever \(|u|=|v|<1\).

**Proof.** Fix \(0<r<1\). For \(0\le t\le r\) let \(H_t(U,V)=F(tU,tV)\). For each \(|V|=1\), the function of \(U\) has no boundary zeros by assumption (and at \(t=0\) it is 1). Its number of zeros in \(|U|<1\), counted by the argument principle, is a continuous integer-valued function of \(t\), hence is zero. Consequently \(H_t(U,V)\ne0\) for \(|U|\le1,|V|=1\), for all \(t\le r\). Now fix any \(|U|\le1\) and apply the same homotopy/argument-principle argument to the variable \(V\). It has no boundary zeros for any \(t\), and at \(t=0\) no interior zeros. Thus \(H_r\ne0\) on the closed bidisc. Taking all \(r<1\) proves the claim. Analyticity on a neighborhood of each closed radius-\(r\) bidisc justifies the integrals. ∎

By (2) and Lemma 1, (H) is equivalent to
\[
 F_{\alpha,\beta}(u,v)\ne0\quad ((u,v)\in D^2).
 \tag{3}
\]
The desired conclusion has exactly the same equivalence, including when \(\alpha-1=0\).

The binomial identity
\[
 {\alpha-1\choose k}=(1-k/\alpha){\alpha\choose k}
\]
gives the exact lowering identity
\[
 F_{\alpha-1,\beta}=F_{\alpha,\beta}
 -\frac{u}{\alpha}\,\partial_uF_{\alpha,\beta}.
 \tag{4}
\]

## 3. An affirmative degree range

**Lemma 2.** If a nonzero polynomial \(p\) of degree \(d\) has no zeros in \(D\), then
\[
 \mathop{\rm Re}\frac{up'(u)}{p(u)}<d/2\quad (u\in D)
 \tag{5}
\]
when \(d>0\); the left side is zero if \(d=0\).

**Proof.** Factor \(p(u)=c\prod_{\ell=1}^d(u-\zeta_\ell)\), where \(|\zeta_\ell|\ge1\). Each term satisfies
\[
 \frac12-\mathop{\rm Re}\frac{u}{u-\zeta_\ell}
 =\frac{|\zeta_\ell|^2-|u|^2}{2|\zeta_\ell-u|^2}>0.
\]
Sum over the roots. ∎

**Theorem 3.** The implication in Problem 5.60 holds if either

1. \(\alpha\) is a positive integer, with arbitrary analytic \(\phi\); or
2. \(\phi\) is a polynomial of degree \(N\le2\alpha\), with arbitrary real \(\alpha,\beta\ge1\).

**Proof.** Assume (H). For fixed \(v\in D\), the function \(p(u)=F_{\alpha,\beta}(u,v)\) has no zeros in \(D\). In case 1, \({\alpha\choose k}=0\) for \(k>\alpha\), so \(p\) has degree at most \(\alpha\), even if \(\phi\) is an infinite series. In case 2 its degree is at most \(N\le2\alpha\). Lemma 2 gives \(\mathop{\rm Re}(up'/p)<\alpha\), with the constant case immediate. Hence \(1-up'/(\alpha p)\ne0\). Equation (4) and (2) give the conclusion. ∎

For example, all quadratic \(\phi\) are covered for every allowed \(\alpha\); cubic \(\phi\) are covered for \(\alpha\ge3/2\). No assertion of novelty is made for this degree observation. The integer case is prior knowledge recorded in the source.

**The general zero-free-polynomial argument stops exactly at this threshold.** For any integer \(N>2\alpha\), the zero-free polynomial \(p(u)=(1+u)^N\) has
\[
 p(u)-\frac u\alpha p'(u)
 =(1+u)^{N-1}\left(1+(1-N/\alpha)u\right),
\]
a zero at \(u=\alpha/(N-\alpha)\in(0,1)\). This is a counterexample to an unrestricted operator-preservation statement, **not** to Problem 5.60: taking \(F(u,v)=p(u)\) does not have the coefficient structure (1). In fact, if a function (1) is independent of \(v\), its coefficients of \(u^0v^j\), namely \(a_j(\beta)_j/j!\), force \(a_j=0\) for every \(j\ge1\).

## 4. A precise obstruction to dilation averaging

One possible approach would express the lowering step as an average of contractions in the \(u\)-variable. For noninteger \(\alpha\), no finite complex Borel measure \(\mu\) on the closed unit disc can satisfy
\[
 F_{\alpha-1,\beta}(u,v)
 =\int F_{\alpha,\beta}(tu,v)\,d\mu(t)
 \tag{6}
\]
for every analytic \(\phi\).

Indeed, apply (6) at \(v=0\) to \(\phi(z)=z^n\). All \({\alpha\choose n}\) are nonzero because \(\alpha\) is not an integer. Thus
\[
 \int t^n\,d\mu(t)=1-n/\alpha\qquad(n\ge0).
\]
The left side has modulus at most the total variation \(\|\mu\|\); the right side is unbounded. Contradiction. This rules out this universal averaging mechanism, not all integral methods. Moreover, even positive averages of normalized zero-free functions need not remain zero-free: the mean of \((1+u)^3\) and \((1-u)^3\) is \(1+3u^2\), which vanishes inside \(D\).

## 5. The structural differential equation

The lift (1) satisfies
\[
 (u+v)F_{uv}=\alpha F_v-\beta F_u.
 \tag{7}
\]
For proof, the coefficient of \(u^kv^j\) in \(F_u\) is
\(a_{k+j+1}(\alpha-k){\alpha\choose k}(\beta)_j/j!\), and that in \(F_v\) is
\(a_{k+j+1}(\beta+j){\alpha\choose k}(\beta)_j/j!\). Thus
\((\beta+v\partial_v)F_u=(\alpha-u\partial_u)F_v\), which is (7).

A further exact restriction is
\[
 F(-v,v)=\sum_{n\ge0}a_n(-1)^n{\alpha-\beta\choose n}v^n,
 \tag{8}
\]
because the product of generating kernels there is \((1-vt)^{\alpha-\beta}\). In particular, \(F(-v,v)=1\) when \(\alpha=\beta\).

Under (3), (4) shows that the exact remaining avoidance condition is
\[
 \frac{uF_u(u,v)}{F(u,v)}\ne\alpha\quad((u,v)\in D^2).
 \tag{9}
\]
The stronger half-plane bound \(\mathop{\rm Re}(uF_u/F)<\alpha\) would suffice, but is **not proved** in the unrestricted noninteger case. Equations (7) and (8) record additional structure that a genuine counterexample must obey; merely citing (9) would restate the main difficulty. No maximum principle yielding the required bound has been established here.

## 6. Reduction to robust polynomial counterexamples

**Theorem 4.** If Problem 5.60 has a counterexample, it has one for which \(\phi\) is a polynomial with \(a_0=1\), the premise lift is nonzero even on the closed bidisc, \(\alpha>1\) is noninteger rational, \(\beta\ge1\) is rational, and every coefficient of \(\phi\) has rational real and imaginary parts. Its degree necessarily exceeds \(2\alpha\).

**Proof.** Start with any counterexample. Write the failed conclusion as a zero at \(x_0,z_0\) with \(|x_0|=1\), \(|z_0|<1\). Necessarily \(z_0\ne0\). Choose \(|z_0|<s<1\) and replace \(\phi(z)\) by \(\phi(sz)\). Its premise lift is \(F_{\alpha,\beta}(su,sv)\), zero-free on a neighborhood of the closed bidisc by Lemma 1. On that compact set it has a positive minimum modulus \(m\). Its lowered convolution at fixed \(x_0\) has a zero at \(z_0/s\in D\).

The Taylor polynomials of \(\phi(sz)\) induce lifts converging uniformly on the closed bidisc, for both exponents, by the absolute-series estimate preceding Lemma 1 (or the same estimate with radius of analyticity greater than 1). Thus sufficiently high Taylor polynomials have premise error less than \(m/2\), and their premise lifts are zero-free on the closed bidisc. Choose a small circle about \(z_0/s\), contained in \(D\), on which the limiting lowered convolution has no zeros. It is not identically zero because its value at 0 is 1. Rouché's theorem retains a lowered zero inside this circle for all sufficiently high Taylor polynomials.

Now fix one such polynomial. Its premise has a positive compact minimum, and the lowered function is nonzero on the chosen small circle. All involved polynomial coefficients depend continuously on \(\alpha,\beta\) and on the finitely many coefficients of \(\phi\). Sufficiently small perturbations therefore preserve the premise and, by Rouché, the failed conclusion. Theorem 3 excludes integer \(\alpha\), so \(\alpha>1\) is noninteger and can be perturbed to a nearby noninteger rational. Perturb \(\beta>1\) to a rational greater than 1; if \(\beta=1\), keep it fixed. Approximate every nonconstant coefficient by a Gaussian rational and keep \(a_0=1\). The desired properties persist. Finally Theorem 3 forces the degree to exceed \(2\alpha\). ∎

This supplies a countable, finite-dimensional counterexample target. It does not bound the necessary degree or establish that any counterexample exists.

## 7. Computational controls and exact gap

`verify.py` checks the finite algebraic identities using exact rational arithmetic, including lowering, (7), (8), the degree-barrier example, and selected root-location inequalities. It is not a proof checker for the analytic lemmas or a substitute for reviewing the written proof.

`search.py` explores rational parameter pairs and Gaussian-integer polynomial coefficients, computing the least root modulus of the premise and conclusion as \(x\) ranges over a finite unit-circle grid. It tests 1,152 polynomials in degrees 3, 4, 6, and 8, omitting degree/parameter pairs already covered by Theorem 3. The grid has 96 phases; ten selected cases are repeated at 4,096 phases. No sampled radius ratio below 1 was found. Sampling and floating-point roots do not certify the full hypothesis for any nontrivial example, and do not prove absence of counterexamples. Exact parameters, seed, outputs and limits are in SEARCH.json.

**Remaining gap:** prove the lowering implication for all polynomial \(\phi\) of degree \(N>2\alpha\) and noninteger \(\alpha>1\), uniformly for \(\beta\ge1\), or find one valid counterexample. By Theorem 4 this is enough for the full analytic problem. None of the five approaches here closes that gap.
