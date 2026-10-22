# Independent mathematical audit: Hermite tetranomials

**Problem 2304006 / AMR-022-4006, Hayman–Lingham Problem 4.6**  
**Audit date: 3 October 2026**  
**Disposition: PASS as an unresolved five-attempt report with valid partial results.**

The full arbitrary-degree, complex-coefficient question is not solved by the reviewed work. The complete real-coefficient result, coefficient-uniform bound for each fixed degree pair, and sharp complex cubic result are proved correctly. No mathematical correction is required for these claims. This audit is an independent mathematical and reproducibility review, not a claim of human peer review, novelty, or exhaustive knowledge of the literature.

## 1. Exact question, normalization, and source scope

The polynomial under consideration is
\[
P(z)=1+2z+aH_n(z)+bH_m(z),\qquad a,b\in\mathbb C,\quad 2\le n<m,
\]
where
\[
H_k(z)=(-1)^k e^{z^2}\frac{d^k}{dz^k}e^{-z^2}.
\]
The required constant is independent of both coefficients and both indices. The target is a zero in a closed horizontal strip; it is not an optimal-constant question. Zero coefficients, lower effective degrees, and repeated zeros are allowed.

Printed pp. 73–74 of [Hayman and Lingham, Research Problems in Function Theory, 2018 edition](https://arxiv.org/abs/1809.07200v2) confirm these quantifiers and this physicists' normalization. Problem 4.5 is the separate Sendov problem. Update 4.6 warns of an earlier numbering confusion and reports the editors' lack of progress at the time of that edition. That historical update is not evidence excluding every later solution.

The seven-page [Makai–Turán article (1963)](https://real.mtak.hu/201433/1/cut_MATKUTINT_8_1_-_2_1963_pp157_-_163.pdf) concerns one high Hermite term. Its Theorem I establishes a universal strip for that narrower family; Theorem II supplies half-width \(e^3\) for indices at least 36. The argument uses lower estimates on a circle about an extreme real Hermite zero, an upper estimate about \(-1/2\), overlapping coefficient thresholds, and a finite-degree argument. The stated external Hermite estimates are classical inputs. Nothing in the inspected article proves the two-high-term assertion. The reviewed source discussion respects this distinction.

The contextual citation to [Borcea–Brändén, Theorem 11, pp. 478–479](https://annals.math.princeton.edu/wp-content/uploads/annals-v170-n1-p14-p.pdf#page=16) is accurate: it concerns symmetric multiaffine polynomials on circular domains, with full degree or convexity as an extra condition. Definition 4, p. 473, includes open affine half-planes. The cubic proof below nevertheless supplies its own needed half-plane lemma.

A supplementary bounded search found no primary resolution of the unrestricted question. This is a search result, not a proof of current global literature status.

## 2. Real coefficients: the proof covers every case

For normalized Gaussian measure \(d\gamma=\pi^{-1/2}e^{-x^2}dx\), Rodrigues' formula and repeated integration by parts yield
\[
\int H_k q\,d\gamma=0\quad(\deg q<k).
\]
The Gaussian factor makes every polynomial boundary term vanish. If \(a,b\) are real and \(n\ge3\), this gives
\[
\int P\,d\gamma=1,\quad \int xP\,d\gamma=1,
\quad \int x^2P\,d\gamma=\tfrac12.
\]
Thus \(\int(x-1)^2P\,d\gamma=-1/2\). A real polynomial with no real zero has constant sign; its first integral would make that sign positive. The weighted square integral would then be strictly positive, a contradiction.

For \(n=2\), odd \(m\) and nonzero real \(b\) give an odd-degree real polynomial, hence a real zero. In every other case the odd part is exactly \(2x\). Write \(P=E+2x\) with \(E\) even. If \(P\) has no real zero, its positive Gaussian integral again gives \(P(x)>0\) for all real \(x\). Applying this at \(x\) and \(-x\) implies \(E(x)>2|x|\). Consequently
\[
1=\int E\,d\gamma>2\int|x|\,d\gamma=2/\sqrt\pi>1,
\]
which is impossible. This includes either or both high coefficients being zero.

There is no illicit extension to complex coefficients. Applying the same result to \(\operatorname{Re}P\) only produces a zero of its real part. The cubic extremizer explicitly shows that this need not be a zero of \(P\).

## 3. Perturbative regions and differential elimination

The Taylor bound in `PROOF.md` follows from
\[
H_k^{(j)}=2^j\frac{k!}{(k-j)!}H_{k-j}.
\]
On a circle of radius \(r\) about \(-1/2\), the stated sum bounds \(|H_k|\), while \(|1+2z|=2r\). Its strict coefficient inequality therefore permits Rouché comparison with \(1+2z\), giving exactly one zero in that disk.

For the other region, orthogonality proves that \(H_m\) has \(m\) distinct real zeros: if it had fewer than \(m\) sign changes, multiplying by the product of its sign-changing factors would create a nonzero, constant-sign integrand with multiplier degree below \(m\), contradicting orthogonality. A circle about one root with radius below its distance from every other root contains exactly that root. The product formula gives the stated positive lower bound on \(|H_m|\); the explicit coefficient formula gives the stated upper bound on \(|H_n|\). The resulting strict inequality is therefore a valid second Rouché criterion. These are sufficient regions, not a demonstrated cover of all coefficients.

The warning about cancellation is legitimate: at a point with \(H_m(z_0)\ne0\), choosing \(b=-aH_n(z_0)/H_m(z_0)\) annihilates the sum of the high terms there. This rebuts an unsupported magnitude-only lower bound, without proving that every alternative contour method must fail.

Writing \(L=D^2-2zD\), the eigenvalue equation \(LH_k=-2kH_k\) gives, for all permitted indices,
\[
(L+2n)(L+2m)P=4nm+8(n-1)(m-1)z.
\]
Both high modes vanish. The constant and linear terms can be checked separately, so the formula has no finite-degree restriction. Its real transformed zero supplies no converse zero-location theorem for \(P\). The example \(z^2+T^2\) correctly demonstrates the failure of a generic reverse-derivative inference, while not claiming to disprove a specialized Hermite result.

## 4. Cubic algebra and mixed-half-plane exclusion

For \(n=2,m=3\) and \(b\ne0\), let
\[
P(z)=K\prod_{j=1}^3(z-r_j),\qquad K=8b.
\]
The power coefficients are \(8b,4a,2-12b,1-2a\). Comparing them gives
\[
2s_3+s_2+s_1+\tfrac32=0,
\]
where \(s_j\) are the elementary symmetric functions of the roots. Substituting \(w_j=2r_j+1\) gives exactly
\[
F(w_1,w_2,w_3)=w_1w_2w_3+w_1+w_2+w_3+2=0.
\]
No simplicity assumption was used. Only necessity of this relation is needed for the upper bound; no converse parametrization of all root triples is being assumed.

If \(w_1=x+iy\), \(w_2=v+it\), and \(y,t>\sqrt2\), then \(|w_1w_2|\ge yt>2\), so \(w_1w_2+1\ne0\). Solving the relation for \(w_3\) and taking imaginary parts gives
\[
\operatorname{Im}w_3=
\frac{t(x+1)^2+y(v+1)^2+(y+t)(yt-2)}{|w_1w_2+1|^2}>0.
\]
Every sign is correct. The last term is strictly positive, regardless of the real parts. Complex conjugation supplies the lower-half-plane version because the coefficients of \(F\) are real.

Let \(u>0\) satisfy \(4u^3+3u-1=0\), and put
\[
c_3=\frac{\sqrt3}{2}\sqrt{1+u^2}.
\]
The function defining \(u\) is strictly increasing; its values at 0 and \(1/3\) have opposite signs. Thus the specified positive root is unique and \(0<u<1/3\). In particular \(2c_3>\sqrt2\).

If every cubic root avoided the closed strip of half-width \(c_3\), every \(w_j\) would satisfy \(|\operatorname{Im}w_j|>2c_3\). Two lie in the same half-plane. After conjugation if necessary, the formula forces the third to have positive imaginary part. The assumed absolute lower bound then places all three in the same stricter domain \(D=\{\operatorname{Im}w>2c_3\}\). This last use of the absolute bound is essential and is present in the authored proof.

## 5. Strict half-plane polarization, including degree drops

The stated lemma is valid. Suppose \(f\ne0\), \(\deg f=d\le N\), its roots \(\alpha_j\) satisfy \(\operatorname{Im}\alpha_j\le h\), and \(\operatorname{Im}\zeta>h\). For \(d=0\), the transformed polynomial equals the same nonzero constant. For \(d>0\), a hypothetical zero \(w\) of
\[
g(w)=f(w)+(\zeta-w)f'(w)/N
\]
in the open half-plane gives, with \(S=f'(w)/f(w)\),
\[
S\ne0,\qquad \zeta=w-N/S.
\]
For \(y=\operatorname{Im}w-h>0\), each reciprocal summand in \(S\) satisfies
\[
-\operatorname{Im}\frac1{w-\alpha_j}\ge\frac{y}{|w-\alpha_j|^2}.
\]
Cauchy–Schwarz therefore gives
\[
-\operatorname{Im}S\ge \frac yd|S|^2,
\qquad \operatorname{Im}(N/S)\ge Ny/d\ge y.
\]
It follows that \(\operatorname{Im}\zeta\le h\), a contradiction. This proves nonvanishing, and also rules out the transformed polynomial being identically zero. If \(d=N\), the top coefficient cancels; if \(d<N\), its degree was already at most \(N-1\). Boundary roots of \(f\), repeated roots, and all possible degree drops are covered. Strictness of the open domain has not been silently replaced by a closed-domain assertion.

Now
\[
f(w)=F(w,w,w)=w^3+3w+2
=(w+2u)(w^2-2uw+3+4u^2).
\]
Its roots are \(-2u\) and \(u\pm i\sqrt{3+3u^2}\); hence it has no zero in \(D\). Applying the lemma first with \(N=3,\zeta=w_1\), then with \(N=2,\zeta=w_2\), yields the nonvanishing polynomials
\[
F(w_1,w,w)=w_1w^2+2w+w_1+2,
\]
\[
F(w_1,w_2,w)=w_1w_2w+w+w_1+w_2+2.
\]
Their identities follow by direct differentiation. The latter cannot vanish at \(w_3\in D\), contradicting the root relation. This establishes the upper bound for every genuine cubic in the family.

## 6. Degenerations and exact attainment

When \(b=0,a\ne0\), Vieta gives
\[
(r_1+1/2)(r_2+1/2)=-1/4.
\]
One factor has modulus at most \(1/2\), so the corresponding root has imaginary part of magnitude at most \(1/2<c_3\). The example \(a=(1+i)/4\) is exactly
\[
1+2z+aH_2(z)=(1+i)(z+1/2-i/2)^2,
\]
showing the quadratic bound is sharp. If \(a=b=0\), the zero is \(-1/2\). The case \(a=0,b\ne0\) was already included in the cubic argument.

For cubic attainment define
\[
r=(u-1)/2+ic_3,\quad D_0=\tfrac34+\tfrac32r^2,
\quad K=1/D_0,\quad a=-3rK/4,\quad b=K/8.
\]
Since \(0<u<1/3\), \(\operatorname{Re}r<0\) and \(\operatorname{Im}r>0\). Thus \(r^2\) is nonreal and \(D_0\ne0\); the construction does not require an infinite coefficient. The diagonal relation yields
\[
4r^3+6r^2+6r+3=0.
\]
The defining formula for \(K\) matches the linear coefficient, and the formulas for \(a,b\) match the quadratic and cubic coefficients. Multiplying the displayed equation by \(K/4\) matches the constant coefficient as well. Therefore
\[
1+2z+aH_2(z)+bH_3(z)=K(z-r)^3.
\]
All three zeros have height exactly \(c_3\). Consequently the cubic constant is optimal, not merely a numerical estimate. Exact rational arithmetic places it strictly between 0.903669747 and 0.903669748, in agreement with the stated value 0.9036697472260109. An affirmative universal strip constant would have to be at least this large.

## 7. Fixed-degree compactness and its exact limit

For fixed \(n,m\), suppose a sequence of coefficient pairs made every root escape every disk. Divide the corresponding polynomials by
\(t_j=\max(1,|a_j|,|b_j|)\). A subsequence of their coefficient triples converges to \((\lambda,\alpha,\beta)\) of maximum coordinate modulus 1. The polynomial limit is
\[
Q=\lambda(1+2z)+\alpha H_n+\beta H_m.
\]
The distinct degrees imply that this limit is nonconstant: its degree is \(m\) if \(\beta\ne0\), \(n\) if only \(\alpha\ne0\) among the high coefficients, and 1 otherwise. It cannot collapse to a nonzero constant or the zero polynomial. By the fundamental theorem of algebra it has a finite zero. On a sufficiently small surrounding circle, \(Q\) is nonzero; locally uniform convergence and Rouché force a zero of each sufficiently late normalized polynomial inside that circle. Scaling has not changed its zeros. This contradicts their escape.

Thus each degree pair has a finite coefficient-independent disk radius, and each finite collection of degree pairs admits the maximum of those radii. This says nothing quantitative about the radii as degrees increase.

In the notation
\[
C_{n,m}=\sup_{a,b\in\mathbb C}\min_{P(z)=0}|\operatorname{Im}z|,
\]
the proved facts are \(C_{n,m}<\infty\) for every fixed pair and \(C_{2,3}=c_3\). The real-coefficient restriction has value 0. The unresolved assertion is precisely
\[
\sup_{2\le n<m} C_{n,m}<\infty.
\]
Neither the coefficient compactness argument, the polarization lemma, the Rouché regions, nor the differential identity bridges this unbounded-degree step. A counterexample sequence would need unbounded highest index. No such sequence has been constructed here.

## 8. Reproducibility and limitations

The reviewed version comprises the 15 identified author files. Their checksums were verified before and after the audit. Two independent executions of the supplied verifier passed all 449 exact assertions and produced output byte-identical to each other and to `verification.json`. The count is 25 recurrence, 300 orthogonality, 22 negative-variance, 25 Taylor, 66 elimination, and 11 cubic/constant assertions. Both supplied Python scripts compiled successfully.

An additional independently written checker passed 210 exact controls, including direct Rodrigues construction, simultaneous two-high-term moments, root-coordinate algebra, the mixed-half-plane boundary, successive polar derivatives, the diagonal factorization, nonzero extremizer denominator, quadratic degeneration, and rational constant brackets. The environment used Python 3.12.14 and SymPy 1.14.0.

These finite controls supplement the all-degree analytic reasoning above. They do not prove an unrestricted-degree statement by enumeration. The optional numerical optimization was inspected but not rerun; its finite coefficient box, local search, and approximate roots have no role in the accepted proofs or sharpness certificate.

The five recorded approaches are mathematically distinct: Rouché extension, Gaussian positivity, spectral elimination, complex cubic extremizers, and coefficient compactness. The report's **unsolved, 5/5** disposition accurately describes these completed attempts and the remaining global gap. The partial results support neither an unrestricted solution claim nor a claim of novelty or literature priority.
