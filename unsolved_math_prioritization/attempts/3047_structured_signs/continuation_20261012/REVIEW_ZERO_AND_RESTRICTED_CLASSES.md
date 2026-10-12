# Independent review: partition-sign zero sparsity and restricted obstructions

**Later accepted result (12 October 2026).** This note retains the earlier argument and its original mathematical scope. A separate, subsequently accepted [full-ternary theorem](FULL_TERNARY_OBSTRUCTION.md), with [complete independent review](REVIEW_FULL_TERNARY.md), combines coefficient conditions with global Jensen inequalities to exclude the entire ternary-digit family. The earlier statements that these zero-sparsity or finite-budget arguments alone do not do so remain accurate. The unrestricted independent-coefficient problem remains unresolved.


This is the complete substantive independent mathematical and exact-enumeration review of the accepted corrected mathematical version. Editorial changes remove only undistributed artifact identities and incidental provenance; the mathematical reasoning, counts, explicit checks and correction history are preserved. The exhaustive-enumeration programs and raw state certificates used for the historical checks are not distributed in this appendix. The acceptance is independent AI-assisted review, not external human peer review.

## Scope

The original independent-sign problem permits

\[
 f_m(z)=1+\sum_{j\ge1}\epsilon_{m,j}z^j,\qquad
 \epsilon_{m,j}\in\{-1,1\},\qquad
 P(q)=\prod_{m\ge1}f_m(q^m).
\]

There is no requirement connecting different rows or different coefficients within a row. The general zero-sparsity theorem below applies to this full family. The common-factor and ternary-digit results are restricted-family obstructions only. None proves impossibility for the original family.

The earlier [all-binary proof](../BINARY_CLASS_OBSTRUCTION.md) and [general radial caveat](../GENERAL_RADIAL_CAVEAT.md) were read. In particular, arbitrary finitely many active sign factors can produce partition-scale radial suppression. No argument below infers a coefficient obstruction from small values on the positive real radius. The analytic argument controls zero multiplicities and the circle mean of the logarithm through an L² coefficient bound.

## 1. Analytic product and zero multiplicities

For every fixed \(0<r<1\), uniformly for \(|q|\le r\),

\[
 |f_m(q^m)-1|\le\frac{r^m}{1-r^m},\qquad
 \sum_{m\ge1}\frac{r^m}{1-r^m}
 \le\frac{r}{(1-r)^2}<\infty.
\]

Consequently the product converges uniformly on compact subsets of the open unit disk to an analytic function with \(P(0)=1\). Its Taylor coefficients equal those of the formal product: coefficients through degree \(K\) involve only \(m\le K\) and local degrees \(j\le K/m\).

Here is the needed stronger zero statement. On a fixed compact disk, eventually every \(u_m=f_m(q^m)-1\) has modulus less than \(1/2\). The power-series logarithms of \(1+u_m\) then satisfy \(|\log(1+u_m)|\le2|u_m|\). Their sum converges uniformly. The tail of the product is therefore the exponential of an analytic function and is nowhere zero on that disk. Thus all zeros of the full product there come from a finite prefix, with their factor multiplicities added. No cancellation premise, absence-of-coincidence premise, or division by factors is required.

If \(\zeta\ne0\) is a zero of \(f_m\) of multiplicity \(s\), then each of the \(m\) roots of \(q^m=\zeta\) has multiplicity \(s\) in \(f_m(q^m)\). Indeed, the derivative of \(q^m\) is nonzero at these roots. If roots from other factors coincide, the multiplicities add. Since \(f_m(0)=1\), zero itself never arises.

## 2. Jensen–Parseval estimate with boundary radii handled

Suppose \(P(q)=\sum_{k\ge0}p_kq^k\), \(p_0=1\), and \(|p_k|\le M\) for a fixed \(M\ge1\). At a radius \(r\in(0,1)\) with no boundary zero, Jensen's formula and the concavity of the logarithm give

\[
 \sum_{|\alpha|<r}\operatorname{mult}(\alpha)
       \log\frac r{|\alpha|}
 =\frac1{2\pi}\int_0^{2\pi}\log|P(re^{i\theta})|\,d\theta
 \le\frac12\log\!\left(\sum_{k\ge0}|p_k|^2r^{2k}\right)
 \le \log M-\frac12\log(1-r^2). \tag{1}
\]

The equality can be derived directly by factoring the finitely many zeros inside the disk. The remaining nonvanishing analytic factor has harmonic logarithmic modulus. Each linear factor contributes the circle mean \(\log r\), and \(P(0)=1\) cancels the constant terms. Parseval applies because the Taylor series converges uniformly on every smaller closed disk.

The selected-zero inequalities used below also hold at radii containing zeros: approximate the radius by nearby radii with no boundary zeros. The selected finite sums and the upper bound in (1) are continuous, while zeros exactly on the limiting boundary contribute zero. This avoids any unsupported invocation of a boundary-nonzero hypothesis.

The same reasoning gives the exact general zero mass, before applying the coefficient bound:

\[
 J_P(e^{-t})=\sum_{m\ge1}\sum_{\zeta:\,f_m(\zeta)=0,\,0<|\zeta|<1}
              (-\log|\zeta|-mt)_+,
\]

where the inner zeros include analytic multiplicity. Only finitely many summands are positive: every local signed series is nonvanishing for \(|z|<1/2\), since its nonconstant terms have total modulus less than one there. Thus a zero contributing at fixed \(t>0\) requires \(mt\le\log2\), leaving finitely many rows. Each row has finitely many zeros in its relevant compact disk. This proves the author's full exact zero inequality as well as the selected-count consequences.

## 3. General necessary condition for unrestricted independent rows

Fix \(0<\rho<1\), write \(\lambda=\log(1/\rho)>0\), and let \(Z_\rho(N)\) be the total number of zeros, with analytic multiplicities, in \(|z|\le\rho\) among \(f_1,\ldots,f_N\).

For each counted zero, retain all its analytic multiplicity. At \(r=e^{-t}\), its \(m\) lifted roots contribute at least \(\lambda-mt\) when \(mt<\lambda\). Counting just these zeros with their inherited multiplicity, and discarding all other nonnegative terms from (1), yields for every \(0<t<\lambda/N\)

\[
 Z_\rho(N)(\lambda-Nt)
 \le \log M-\frac12\log(1-e^{-2t}). \tag{2}
\]

This explicitly counts original zeros with their multiplicities rather than only distinct locations of product zeros. Coincidences are harmless because multiplicity was justified in Section 1. The number of rows having at least one such zero is at most \(Z_\rho(N)\), so every bound also holds for that weaker count.

In particular, at \(t=\lambda/(2N)\),

\[
 Z_\rho(N)\le
 \frac1\lambda\log\!\left(\frac{M^2}{1-e^{-\lambda/N}}\right)
 \le\frac1\lambda\log\!\left(\frac{M^2(N+\lambda)}{\lambda}\right), \tag{3}
\]

where \(1-e^{-x}\ge x/(1+x)\) follows from \(e^x\ge1+x\).

For the asymptotically sharper constant, first fix \(0<\theta<1\) and put \(t=\theta\lambda/N\). Then

\[
 -\log(1-e^{-2\theta\lambda/N})
 =\log N-\log(2\theta\lambda)+o(1),
\]

so (2) implies

\[
 \limsup_{N\to\infty}\frac{Z_\rho(N)}{\log N}
 \le\frac1{2\lambda(1-\theta)}.
\]

Only after taking this limsup do we let \(\theta\downarrow0\). Therefore

\[
 \boxed{\displaystyle
 \limsup_{N\to\infty}\frac{Z_\rho(N)}{\log N}
 \le\frac1{2\log(1/\rho)}.} \tag{4}
\]

The constant \(M\) is fixed while \(N\to\infty\); it disappears after division by \(\log N\). The argument is valid for each fixed \(\rho\), not uniformly as \(\rho\uparrow1\). It does not bound the number of rows with zeros approaching the unit circle at an arbitrary row-dependent rate. It neither classifies zero-free signed series nor proves an impossibility theorem.

## 4. Ternary-digit products: exact zero mass

The restricted family is

\[
 F_m(q)=\prod_{j\ge0}
       (1+a_{m,j}q^{m3^j}+b_{m,j}q^{2m3^j}),
 \qquad a_{m,j},b_{m,j}\in\{-1,1\}.
\]

Unique ternary expansion proves that every coefficient of each \(F_m\), as a series in \(q^m\), is a sign. These signs are not mutually independent: for example, the coefficient at a two-digit ternary exponent is determined by the corresponding digit choices. This restriction must remain explicit.

For a fixed exponent \(n=m3^j\), exactly \(d_n=1+v_3(n)\) labels occur. The whole product converges uniformly on compact subsets because

\[
 \sum_{n\ge1}d_n(r^n+r^{2n})<\infty.
\]

One may use \(d_n\le n\) to obtain an elementary summable majorant. Formal regrouping is also valid, since only finitely many labels have \(m3^j\le K\).

The blocks with \(b=+1\) are exactly \(1+x+x^2=\Phi_3(x)\) and \(1-x+x^2=\Phi_6(x)\). All their zeros have modulus one. For \(b=-1\), set

\[
 \varphi=(1+\sqrt5)/2,\qquad \lambda=\log\varphi.
\]

The block \(1+a x-x^2\) has one simple root of modulus \(\varphi^{-1}\), specifically \(-a\varphi^{-1}\), and one simple root of modulus \(\varphi\). After substituting \(x=q^n\), exactly \(n\) roots are inside the unit disk, all of modulus \(e^{-\lambda/n}\). Their total Jensen contribution at \(r=e^{-t}\) is precisely

\[
 n\left(\log r+\frac\lambda n\right)_+
 =(\lambda-nt)_+.
\]

Let \(b_n^*\) be the number of \(b=-1\) blocks at exponent \(n\), including all identical labels, so \(0\le b_n^*\le d_n\). The entire Jensen zero sum is exactly

\[
 \boxed{\displaystyle
 \sum_{n\ge1}b_n^*(\lambda-nt)_+.} \tag{5}
\]

Only \(n<\lambda/t\) contribute positively. At an integer cutoff \(n=\lambda/t\), the contribution is zero. Repeated blocks count with multiplicity. The nonzero-tail proof precludes any cancellation by the infinite product.

If total coefficients have modulus at most one, (1) and (5) give

\[
 \sum_{n\ge1}b_n^*(\lambda-nt)_+
 \le -\tfrac12\log(1-e^{-2t}). \tag{6}
\]

Writing \(D(N)=\sum_{n\le N}b_n^*\), equations (2)–(4) apply with \(M=1\) and \(\lambda=\log\varphi\). Thus all the asserted finite bounds and the coefficient \(1/(2\log\varphi)\) in the limsup are justified. Sparse infinitely many defects are not excluded.

## 5. Independent common-factor enumeration

The second restricted family is \(P(q)=\prod_{m\ge1}f(q^m)\), with one common arbitrary signed series \(f(q)=1+\sum_{j\ge1}e_jq^j\). Its within-row signs are arbitrary; its across-row signs are identical. This is different from both the ternary and full independent-row families.

Set

\[
 qf'(q)/f(q)=\sum_{n\ge1}b_nq^n,\qquad
 qP'(q)/P(q)=\sum_{n\ge1}h_nq^n.
\]

Formal inversion is valid because both constant terms are one. The exact recurrences are

\[
 b_n=ne_n-\sum_{k=1}^{n-1}b_ke_{n-k},\qquad
 h_n=\sum_{m\mid n}m b_{n/m},\qquad
 np_n=\sum_{k=1}^nh_kp_{n-k}. \tag{7}
\]

At stage \(n\), all proper-index terms are already known, and \(p_n=A_n+e_n\) for an exactly computed integer residual \(A_n\). Therefore testing both \(e_n=-1,+1\) and retaining exactly those with \(|p_n|\le1\) enumerates every feasible sign prefix. Future signs first enter in their own degree. This proves both soundness and completeness by induction.

The independent implementation did not import or use the author's direct-product routine. It regenerated every feasible prefix from (7), checked every divisibility by \(n\), and compared all author frontiers as sets with duplicate rejection. Results:

- First empty frontier: degree 81.
- Degree-80 frontier: one prefix.
- Total nonempty states, including the root: 1,227.
- Peak frontier: 62, at degree 39.
- Unique parent's degree-81 residual: \(-4\).
- Both final sign choices give \(-5\) or \(-3\).
- The supplied complete witness coefficients agree with (7).

Extending the degree-80 sign prefix arbitrarily gives an infinite common series and preserves its verified coefficient prefix. Thus the obstruction degree is sharp within this common-factor family.

The independent checker rejects deletion of a feasible state, duplication, substitution of an invalid state, removal of the final empty frontier, a changed terminal residual, and a changed witness coefficient. Its complete reports under normal Python, `-O`, and `-OO` are identical. No removable assertions are used.

## 6. Independent ternary finite-budget enumeration

Use block types \((-1,+1),(+1,+1),(-1,-1),(+1,-1)\), where a pair is \((a,b)\). A group at exponent \(n\) is represented by a four-part weak composition of \(d_n\). Every such composition is realizable by distributing the four types among the \(d_n\) labels. Groups at different exponents use disjoint labels. Grouping therefore loses no attainable product.

For a primitive block define

\[
 \frac{x(1+a x+b x^2)'}{1+a x+b x^2}
 =\sum_{k\ge1}\ell_k(a,b)x^k.
\]

Exact polynomial multiplication gives

\[
 \ell_1=a,\quad \ell_2=2b-a^2,\quad
 \ell_k=-a\ell_{k-1}-b\ell_{k-2}\quad(k\ge3). \tag{8}
\]

The group log derivatives are sums of these sequences. At degree \(n\), the proper-divisor contributions determine a residual \(A_n\). A new group with type counts \(c_t\) changes only the coefficient of degree \(n\), among all degrees up to \(n\), by \(\sum_t c_t a_t\). Enumerating all four-part compositions, respecting the total count of \(b=-1\) blocks, and applying the exact coefficient test is complete by the same induction as in Section 5.

An independently implemented log-derivative enumeration, separate from the author's direct multiplication, produces the following exact results:

| Total defect budget | First empty degree | Last nonempty count | Total states | Peak frontier |
|---:|---:|---:|---:|---:|
| 0 | 31 | 2 | 563 | 60 at degree 18 |
| 1 | 42 | 8 | 11,481 | 1,242 at degree 18 |
| 2 | 55 | 8 | 132,203 | 12,448 at degree 18 |

The terminal residuals are respectively:

- Budget 0: \(3,-3\). At degree 31, \(d_{31}=1\); adding \(\pm1\) cannot enter the permitted interval.
- Budget 1: \(10,8,6,4,8,10,4,6\), all parents already using one defect. At degree 42, \(d_{42}=2\); permissible cyclotomic-only slopes are \(-2,0,2\), all inadequate.
- Budget 2: \(-3,-5,-3,-5,3,5,3,5\), all parents already using two defects. At degree 55, \(d_{55}=1\); permissible slopes are \(-1,1\), all inadequate.

Every complete decoded author frontier was compared as an exact set against an independently generated frontier. All 144,247 states across the three budgets match; the comparison does not substitute cardinalities or hash equality for state equality. All certificate witnesses, coefficient arrays, defect counts, terminal residuals, and summary files also match. Seven adversarial mutations per budget are rejected, and the complete verification reports are identical under normal Python, `-O`, and `-OO`. Sharpness is established by any survivor at the preceding degree, extended with only cyclotomic blocks thereafter; it does not use an unproved infinite extension with bounded coefficients.

## 7. Derived lower cutoffs and preserved corrections

For a block of exponent \(n\), changing only its quadratic sign first changes that block at degree \(2n\). Multiplying by other series with constant term one cannot introduce a lower-degree difference. Consequently an array good through degree \(N\) can have every defect with \(n>\lfloor N/2\rfloor\) reset to a nondefective block without affecting that prefix. This is valid for infinitely many replacements by coefficientwise local finiteness. Applying the certified obstructions at \((K,N)=(0,31),(1,42),(2,55)\) proves the necessary conditions

\[
 B(15)\ge1,\qquad B(21)\ge2,\qquad B(27)\ge3
\]

for a hypothetical successful infinite ternary array. These lower bounds and logarithmic upper bounds are compatible.

The first frozen candidate incorrectly called the ternary family “broader-than-binary.” The audit required a correction: the two digit-multiplicative families are incomparable. Ternary signs can have \(e_1=e_2=1,e_3=-1\), violating the binary identity \(e_3=e_1e_2\). Binary signs can have \(e_1=e_2=e_3=1,e_4=-1\), violating the ternary identity \(e_4=e_1e_3\). The accepted corrected version replaces the phrase with precise different-family language and also repairs a Latin-u/Greek-nu notation mismatch. Acceptance applies to this corrected version only.

## Accepted mathematical scope and limitations

The analytic inequalities above are proved, including compact convergence, normalization, multiplicity, cutoff, boundary radii, and order of limits. The common-factor finite obstruction has been independently verified state by state. The finite ternary budgets have independently reproduced complete searches and passed complete comparison to the frozen author certificates.

Neither finite-budget calculations nor logarithmic zero sparsity rule out an infinite ternary assignment with sufficiently sparse defects. Neither the common-factor nor ternary obstructions establish a finite obstruction for the original independent-sign problem. No novelty or literature-priority conclusion is asserted.
