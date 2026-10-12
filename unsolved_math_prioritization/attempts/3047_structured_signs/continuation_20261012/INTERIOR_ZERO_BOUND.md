# Interior-zero restrictions for independently signed partition products

**Later accepted result (12 October 2026).** This note retains the earlier argument and its original mathematical scope. A separate, subsequently accepted [full-ternary theorem](FULL_TERNARY_OBSTRUCTION.md), with [complete independent review](REVIEW_FULL_TERNARY.md), combines coefficient conditions with global Jensen inequalities to exclude the entire ternary-digit family. The earlier statements that these zero-sparsity or finite-budget arguments alone do not do so remain accurate. The unrestricted independent-coefficient problem remains unresolved.


## Scope and conclusions

This is an authored necessary condition for David Newman's unrestricted-partition sign problem. It does not settle that problem, does not contradict the possibility of radial suppression by finitely many arbitrary sign factors, and makes no novelty claim.

Let
\[
f_m(z)=1+\sum_{j\ge1}\epsilon_{m,j}z^j,\qquad \epsilon_{m,j}\in\{-1,1\},
\quad
P(q)=\prod_{m\ge1} f_m(q^m)=\sum_{n\ge0}a_nq^n.
\]
Every sign in every factor is independent. Assume, for the necessary conditions below, that \(|a_n|\le M\) for all \(n\), where \(M\ge1\). Newman's target is \(M=1\).

**Theorem 1 (exact zero inequality).** For every \(t>0\),
\[
\boxed{
\sum_{m\ge1}\ \sum_{\zeta:\ f_m(\zeta)=0,\ 0<|\zeta|<1}
\bigl(-\log|\zeta|-mt\bigr)_+
\le \log M-\frac12\log(1-e^{-2t}).
} \tag{1}
\]
The inner sum counts zeros with their analytic multiplicities. Equal zeros of distinct factors are counted separately. Only finitely many summands are positive for each fixed \(t\).

For \(0<\rho<1\), let \(Z_\rho(N)\) be the total number of zeros in \(|z|\le\rho\), counted with multiplicities, among the **original series** \(f_1,\ldots,f_N\). Set \(\lambda=-\log\rho>0\). Then
\[
\boxed{
Z_\rho(N)\le
\frac{\log M-\tfrac12\log(1-e^{-2t})}{\lambda-Nt}
\quad(0<t<\lambda/N),
} \tag{2}
\]
and consequently
\[
\boxed{
\limsup_{N\to\infty}\frac{Z_\rho(N)}{\log N}
\le\frac1{2\log(1/\rho)}.
} \tag{3}
\]
In particular, the number of indices \(m\le N\) for which \(f_m\) has at least one zero in \(|z|\le\rho\) satisfies the same bounds. Thus a putative solution cannot have a positive-density family of factors with zeros uniformly inside the unit disk. The coefficient bound \(M\) appears explicitly in (1)–(2); it changes the additive lower-order term, not the constant in (3). We do not claim that the constant in (3) is attained.

## 1. Convergence and absence of zero cancellation

For \(|q|\le r<1\),
\[
|f_m(q^m)-1|\le \frac{r^m}{1-r^m}\le\frac{r^m}{1-r}.
\]
The sum over \(m\) converges. Hence the product converges uniformly on every compact disk to an analytic function with \(P(0)=1\). This analytic product agrees with the formal product: a coefficient of degree \(n\) uses only factors \(m\le n\).

For completeness, its tail cannot cancel zeros or introduce extra zeros. On any fixed compact disk, sufficiently late factors have \(|f_m(q^m)-1|\le1/2\). Their analytic logarithms with value zero at \(q=0\) exist, and the series of these logarithms converges uniformly, since \(|\log(1+w)|\le2|w|\) for \(|w|\le1/2\). Their product is therefore the exponential of an analytic function and is nonvanishing. The remaining finite product shows that the zeros of \(P\) are exactly the zeros of its factors, with multiplicities added.

Moreover, \(f_m\) has no zero in \(|z|<1/2\): there \(|f_m(z)-1|<1\). For fixed \(r<1\), every sufficiently large \(m\) has \(r^m<1/2\). Only finitely many original factors can therefore contribute zeros to \(|q|\le r\), and each contributes finitely many. This also proves the finiteness assertion after (1).

## 2. Jensen's identity and the coefficient bound

We recall the needed identity with its short proof. If \(F\) is analytic on the unit disk and \(F(0)=1\), then
\[
\frac1{2\pi}\int_0^{2\pi}\log|F(re^{i\theta})|\,d\theta
=\sum_{\xi:\ F(\xi)=0,\ |\xi|<r}\log\frac r{|\xi|}. \tag{4}
\]
Zeros are counted with multiplicity. First choose a radius having no boundary zero. Divide \(F\) by the finite product of \((1-z/\xi)\) over its zeros inside the circle. The quotient is nonvanishing on the disk bounded by that circle, equals 1 at zero, and has an analytic logarithm. The mean-value property makes its mean log modulus zero. Each divided factor contributes \(\log(r/|\xi|)\): factor out \(-re^{i\theta}/\xi\), and apply the same mean-value property to \(1-(\xi/r)e^{-i\theta}\). This proves (4). Arbitrary radii follow by approaching them through radii without boundary zeros; a zero exactly on the circle has zero contribution. Equivalently the logarithmic singularities in the circle integral are integrable.

Write the left side of (4) as \(J_F(r)\). Concavity of logarithm and orthogonality of the Taylor monomials give
\[
J_P(r)
\le\frac12\log\left(\frac1{2\pi}\int_0^{2\pi}|P(re^{i\theta})|^2\,d\theta\right)
=\frac12\log\sum_{n\ge0}|a_n|^2r^{2n}
\le\log M-\frac12\log(1-r^2). \tag{5}
\]
One can first replace a zero modulus by a positive regularization when applying concavity, then pass to the limit; alternatively apply Jensen's inequality directly to the integrable logarithm. All Taylor and integral operations here take place strictly inside the convergence disk.

A zero \(\zeta\ne0\) of \(f_m\), of multiplicity \(h\), produces exactly \(m\) zeros of \(f_m(q^m)\), each with multiplicity \(h\), at modulus \(|\zeta|^{1/m}\). Composition preserves multiplicity because the derivative of \(q^m\) is nonzero at these roots. Their combined contribution to (4) is
\[
hm\left(\log r-\frac1m\log|\zeta|\right)_+
=h\bigl(m\log r-\log|\zeta|\bigr)_+.
\]
Coincidences with roots from other factors add multiplicities and cannot cause cancellation, by Section 1. Sum these contributions and put \(r=e^{-t}\) in (5). This proves (1).

## 3. The logarithmic count bound

Every zero counted by \(Z_\rho(N)\) contributes at least \(\lambda-Nt>0\) to (1), proving (2).

For sufficiently large \(N\), choose \(t=1/(N\log N)\). Then
\[
\lambda-Nt=\lambda-\frac1{\log N},
\]
and
\[
-\log(1-e^{-2t})
=\log N+\log\log N-\log2+o(1).
\]
Substitution in (2) gives
\[
Z_\rho(N)
\le\frac{\log N+\log\log N+O_{M,\rho}(1)}{2\lambda}, \tag{6}
\]
which implies (3). The choice of \(t\) is legal once \(\log N>1/\lambda\).

One immediate corollary is that a common-factor product \(\prod_{m\ge1}f(q^m)\) with bounded coefficients requires \(f\) to be zero-free in the unit disk: any interior zero would otherwise be counted in every one of the first \(N\) factors. Zero-freeness alone is not sufficient. The companion [common-factor proof](COMMON_FACTOR_OBSTRUCTION.md) excludes that entire class for Newman's exact coefficient alphabet, without assuming any classification of zero-free signed series.

## 4. Ternary-digit consequences, including all sign freedoms

Consider the ternary-digit family, different from the binary-digit family,
\[
f_m(z)=\prod_{j\ge0}
\left(1+u_{m,j}z^{3^j}+v_{m,j}z^{2\cdot3^j}\right),
\qquad u_{m,j},v_{m,j}\in\{-1,1\}. \tag{7}
\]
Unique ternary expansion makes every coefficient of \(f_m\) exactly \(1\) or \(-1\); each digit independently selects the constant, linear, or quadratic term from its block. All signs in (7) are independent across \(m,j\). Thus these are valid original factors, but (7) still restricts the full independently signed problem.

For \(v=+1\), the two possible blocks are \(1+z+z^2\) and \(1-z+z^2\), and all their roots have modulus 1. For \(v=-1\), the two blocks are \(1+z-z^2\) and \(1-z-z^2\). Each has one root of modulus \(\varphi^{-1}\) and one root of modulus \(\varphi\), where \(\varphi=(1+\sqrt5)/2\). These assertions follow immediately by the quadratic formula. Call a block with \(v=-1\) a noncyclotomic block; no classification theorem is being assumed.

Let \(b_n\) count the pairs \((m,j)\) with \(m3^j=n\) and \(v_{m,j}=-1\). Thus
\[
0\le b_n\le d_n:=1+v_3(n).
\]
The full digit-block product is locally uniformly convergent because
\[
\sum_{m,j}r^{m3^j}\le\sum_{m,j}r^{m(j+1)}<\infty.
\]
Its zeros and multiplicities can therefore be treated by exactly the preceding argument. With \(\lambda=\log\varphi\), its exact Jensen sum is
\[
J_P(e^{-t})=\sum_{n\ge1}b_n(\lambda-nt)_+.
\]
Consequently a bounded-coefficient solution in (7) must satisfy
\[
\boxed{
\sum_{n\ge1}b_n(\log\varphi-nt)_+
\le\log M-\frac12\log(1-e^{-2t})\quad(t>0).
} \tag{8}
\]
Writing \(B(N)=\sum_{n\le N}b_n\), equations (2)–(3) apply to \(B\) with \(\lambda=\log\varphi\). In particular,
\[
\limsup_{N\to\infty}\frac{B(N)}{\log N}
\le\frac1{2\log\varphi}.
\]
This rules out positive-density noncyclotomic ternary blocks, not all such blocks. It does not show that their number is finite, and does not prove impossibility for the entire ternary family. The cyclotomic-only subclass is separately excluded by the exact degree-31 calculation in the companion note.

## Source context and limitations

- [David Newman, *Dividing up the unrestricted partitions*, Open Problem Garden](https://www.openproblemgarden.org/op/dividing_up_the_unrestricted_partitions) states the independently signed product and desired alphabet.
- [George E. Andrews and David Newman, *Binary Representations and Theta Function*, Integers 18 (2018), A34](https://math.colgate.edu/~integers/s34/s34.pdf) motivates digit-based constructions but proves identities over its specified sets of dilates. No identity for an odd-only product is substituted for the present full product.

The proofs above are self-contained apart from elementary complex-analysis facts whose specific use is shown. No source text, copied source documents, private data, or coordination records form part of this proof. No source search establishes novelty. In particular, this angular/zero-count restriction does not revive the invalid claim that finitely many arbitrary factors cannot suppress the positive real radius: radial suppression and the distribution of complex zeros are different necessary tests.
