# New independent adversarial audit of the real square dependency

**Verdict: PASS at ordinary analytic-proof standard for the universal real square increment, with the explicit Abreu-Patil smallest-index wording repair proved below.** No counterexample or central unsupported premise was identified. This is validation of an existing external theorem, with zero new discovery credit and zero new substantive proof-search turns. The parent owns any current metadata correction and its later complete acceptance gate.

Target: PR25, numeric 2800102 / AMR-027-0102, original head `aa99d4a36eff79cbb7aae55ce3ffe4a0eb31af95`. Audit date: 2026-10-01 UTC. Files in this directory are new validation artifacts. The original source-only audit and its real-proof hold remain historical records; this report does not rewrite them.

## Independence, exact scope, and source status

`EARLY_SEAL_v1.md` was written before reading root, sibling, or historical reports/scripts, SHA256 `d457258f2a8b73773eefb66a708f7bae1634adaee0e492b0df728e8bbd9f7ef9`. Before that seal I read the exact [Bandeira 2013 author post](https://afonsobandeira.wordpress.com/2013/11/01/a-conjecture-on-the-singular-values-of-a-gaussian-matrix/), [MIT Open Problem 1.2 handout](https://ocw.mit.edu/courses/18-s096-topics-in-mathematics-of-data-science-fall-2015/a9963e8f7bd9c10b4d48df8115f63116_MIT18_S096F15_Open1.2.pdf), the square dependency chain in [Hutnik 2608.12151v2](https://arxiv.org/abs/2608.12151v2), the supporting proof in [Abreu-Patil 2609.07802v1](https://arxiv.org/abs/2609.07802v1), and published [Livan-Vivo equations (1), (16)-(23)](https://www.actaphys.uj.edu.pl/fulltext?series=Reg&vol=42&page=1081). Fresh independent downloads and hashes are in `SOURCE_RECEIPTS.json`; foreign bytes and renderings stay in ignored `tmp/`. Root source text copies were initially available, but independent PDF downloads were completed before the seal. Formula pages were also inspected as rendered images to resolve signs, indices, and factors.

For independent real entries of variance one, define

\[
 a_N=N^{-3/2}\mathbb E\operatorname{Tr}\sqrt{X_NX_N^T},\qquad N\in\mathbb Z_{\ge1}.
\]

The original conjecture requires `a_(N+1)>=a_N` for every positive integer N. The current real paper claims the stronger reserve `a_(N+1)-a_N>1/(160N^2)`. This audit checks that stronger square claim. It does not replace square size by fixed rectangularity, infer universal truth from finite samples, or certify the continuous-shape transition theorems.

The live official pages checked in `SOURCE_STATUS.json` show no withdrawal marker or citation-journal field for the two current dependencies. Hutnik v2 is the 11 September 2026 revision of the 12 August submission; Abreu-Patil v1 was submitted 7 September, while its manuscript date is 9 September. This is not an assertion of human peer review or absence of publication elsewhere. The separate [old Abreu 1606.00494v3 claim](https://arxiv.org/abs/1606.00494v3) is withdrawn and supplies no monotonicity certificate here.

After sealing, I read `real_family/DERIVATION.md`, `complex_family/BOUND_AUDIT.md`, their actual controls, root reconstruction, original source audit, historical review, and original scripts. Their direct monomial half-moment mechanism overlapped one planned control. To retain materially new falsification, I added: (i) an elementary bivariate Gaussian angular integral determining all square skew moments; (ii) a square-only gamma-product comparison proving decrease of every correction coefficient without shape interpolation; (iii) exact mass/first/second-moment tests against independently counted Wick pairings; and (iv) pointwise joint-law density controls with deliberate odd-border, sign and scaling mutations. These are independent validation mechanisms, not claims of new research novelty.

## 1. Exact Gaussian law, both parities, and the density identity

The singular-value Jacobian for an N by N real matrix gives the positive ordered singular-value density proportional to

\[
 e^{-\sum s_i^2/2}\prod_{i<j}(s_j^2-s_i^2).
\]

Putting `x_i=s_i^2` therefore gives the square LOE law

\[
 \prod_i x_i^{-1/2}e^{-x_i/2}\prod_{i<j}(x_j-x_i),\quad 0<x_1<\cdots<x_N.
\]

This is the actual real variance-one law. Standard complex variance one instead gives the LUE weight `e^-x`. The raw Livan-Vivo joint law uses `e^-x/2` for both beta values, but its function R_2 itself has weight `e^-x`. Thus the real normalized density is `R_1(x/2)/(2N)` while the complex density in our normalization is `R_2(x)/N`. The Jacobian and the extra factor two cancel precisely as in Hutnik Proposition 2.2. The distinction is tested rather than silently treating both displayed source variables as the same random eigenvalue.

Here is a square-only derivation directly from the joint law. Let

\[
 w(x)=x^{-1/2}e^{-x/2},\quad p_j=L_j^{(0)},\quad
 \phi_j=wp_j,\quad \psi_j(x)=\int_0^\infty\operatorname{sgn}(y-x)\phi_j(y)\,dy,
\]

and `B_ij=integral phi_i(x) psi_j(x) dx`, `v_j=integral phi_j`. All integrals are absolutely convergent. Orthogonality for `xw^2=e^-x` gives `integral e^-x p_i p_j=delta_ij`.

**New angular mechanism.** Use the Laguerre generating function and put `x=u^2`, `y=v^2`. For real z,t sufficiently near zero, define `a=(1+z)/(2(1-z))`, `b=(1+t)/(2(1-t))`. Then

\[
 \begin{aligned}
 \mathcal B(z,t)&=\sum_{i,j\ge0}B_{ij}z^it^j\\
 &=\frac4{(1-z)(1-t)}\int_{u,v>0}\operatorname{sgn}(v-u)e^{-au^2-bv^2}\,du\,dv\\
 &=\frac4{\sqrt{(1-z^2)(1-t^2)}}
 \left[\frac\pi2-2\arctan\sqrt{\frac{(1+t)(1-z)}{(1-t)(1+z)}}\right].
 \end{aligned}
\]

The last equality follows by scaling U=sqrt(a)u,V=sqrt(b)v and integrating polar coordinates: the sign switches at angle `arctan sqrt(b/a)`, and the radial integral is 1/2. It is an analytic identity in a neighborhood of zero, so its coefficient identities hold at every pair of finite indices. Let the square-root ratio in this formula be R. Since

`R/(1+R^2)=sqrt((1-z^2)(1-t^2))/(2(1-zt))`,

direct differentiation gives

\[
 (1-t^2)\partial_t\mathcal B-t\mathcal B=-\frac4{1-zt}.
\]

Therefore `(j+1)B_(i,j+1)-jB_(i,j-1)=-4 delta_ij`, with negative indices zero. Antisymmetry and B_00=0 uniquely fix the coefficients. Explicitly,

\[
 B_{2k,2\ell}=B_{2k+1,2\ell+1}=0,
\]

`B_(2k,2ell+1)=0` when ell<k, and otherwise

\[
 B_{2k,2\ell+1}=-\frac4{2k+1}\prod_{a=k+1}^{\ell}\frac{2a}{2a+1}.
\]

This independently integrated generating function verifies the entire square skew-moment premise without importing a continuous-shape LOE formula.

Also `sum_j v_j z^j=sqrt(2pi)(1-z^2)^(-1/2)`, hence `v_(2k)=sqrt(2pi)(1/2)_k/k!`, `v_(2k+1)=0`. Define `D f=xf'+(1-x)f/2`. Elementary Laguerre identities give

`D p_j=((j+1)p_(j+1)-j p_(j-1))/2`.

The preceding coefficient recurrence is exactly `B D=-2I` before truncation. For even N, the omitted column B_(i,N) vanishes for i<N, so `B_N^-1=-D_N/2`. For odd N, use the augmented matrix

\[
 M_N=\begin{pmatrix}B_N&v\\-v^T&0\end{pmatrix}.
\]

The product formulas give `B_(i,N)=-4v_i/(Nv_(N-1))`, `B_N e_(N-1)=0`, and `v^T D_N=0`. Direct multiplication proves

\[
 M_N^{-1}=\begin{pmatrix}
 -D_N/2&-e_{N-1}/v_{N-1}\\
 e_{N-1}^T/v_{N-1}&0
 \end{pmatrix}.
\]

In the top-left block, `B_N(-D_N/2)=I-ve_(N-1)^T/v_(N-1)`; the augmented border supplies the missing rank-one term. Thus the odd case is not an informal continuation of even N.

The determinant of the p_j times the weights is a nonzero constant times the ordered joint law. De Bruijn's pairing expansion integrates it to the Pfaffian of B_N (even) or M_N (odd); normalization cancels the determinant's constant and orientation. Perturb each weight to `w(1+tf)` and differentiate `log Pf=Tr(M^-1 dM)/2`. Initially take bounded f; integrability extends the answer to sqrt(x). The raw one-point densities, of mass N, are

\[
 R_N(x)=-\phi(x)^TB_N^{-1}\psi(x)\quad\text{(even)},
\]

and

\[
 R_N(x)=\tfrac12\phi(x)^TD_N\psi(x)+\phi_{N-1}(x)/v_{N-1}\quad\text{(odd)}.
\]

Signs are fixed by `psi_j'=-2phi_j`. Expanding D_N gives the finite adjacent-pair sum

`sum_(j=0)^(N-2) (j+1)[phi_(j+1)psi_j-phi_j psi_(j+1)]/4`.

Use `psi_(j+1)=j psi_(j-1)/(j+1)-4x phi_j/(j+1)` and the Laguerre three-term recurrence to telescope this sum. It equals

\[
 R_{C,N}(x)+\frac N4\phi_{N-1}(x)\psi_N(x),
 \qquad R_{C,N}(x)=e^{-x}\sum_{j<N}p_j(x)^2.
\]

The odd border is then added as displayed. The recursion starts from

`psi_0=sqrt(2pi)[2 erfc(sqrt(x/2))-1]`, `psi_1=-4x phi_0`.

Iteration gives, for N=2m,

`psi_(2m)=((1/2)_m/m!)psi_0-4x sum_(k=0)^(m-1) a_k phi_(2k+1)`,

`a_k=Gamma(m+1/2)Gamma(k+1)/(2Gamma(k+3/2)Gamma(m+1))`;

for N=2m+1 it gives

`psi_(2m+1)=-4x sum_(k=0)^m a_k phi_(2k)`,

`a_k=Gamma(m+1)Gamma(k+1/2)/(2Gamma(k+1)Gamma(m+3/2))`.

Substitute these into R_N, use Gamma duplication, and divide by N. The result is exactly Hutnik's square Proposition 2.2, with parity-dependent weights

`w_(m,epsilon)=2Gamma(m+1-epsilon/2)/Gamma(m+3/2-epsilon/2)`.

The even initial psi_0 gives the incomplete-Gamma Phi_2 term; the odd augmented border gives its epsilon=1 value. At N=1 the cancellation is particularly decisive:

`R_C,1=e^-x`, `phi_0 psi_1/4=-e^-x`, and the border is `w/sqrt(2pi)`.

Thus `p_R,1=e^-x/2/sqrt(2pi x)`, the correct chi-square-one density. The correction identity

\[
 a_N=C_N-\Xi_N
\]

therefore concerns exactly the desired law in every positive dimension, and not merely a formally similar polynomial ensemble.

## 2. Abel completion, domination, absolute tails, and kernel signs

At square shape put `epsilon=N mod2`. The Beta representation of the weights and the Laguerre generating function yield

\[
 S_{\zeta,\epsilon}(x)=\frac2{\sqrt\pi}\int_0^1
 (1-z^2)^{-1/2}\left[\mathcal L(\zeta z,x)+(-1)^{\epsilon+1}\mathcal L(-\zeta z,x)\right]dz,
\]

where `mathcal L(a,x)=(1-a)^-1 exp(-xa/(1-a))`, `0<zeta<1`.

For fixed x>0 the positive branch is bounded uniformly as zeta rises to one: set `s=1-zeta z`, and use boundedness of `s^-1 exp(-x/s)` on 0<s<=1. The negative branch is bounded by exp(x/2). In both cases the remaining factor `(1-z^2)^(-1/2)` is integrable. Dominated convergence therefore applies pointwise. The changes of variable `(1+z)/(1-z)` and its reciprocal at zeta=1 give

`e^-x S_(1,epsilon)=sqrt(2/x)e^-x/2[2erfc(sqrt(x/2))-1]` for even N,

and `e^-x S_(1,epsilon)=sqrt(2/x)e^-x/2` for odd N,

which are exactly Phi_2.

For the half-moment insertion, expand the fixed p_(N-1) into finitely many monomials x^j and take absolute values before integrating each branch. The x integral is explicitly

\[
 \int_0^\infty x^{j+1/2}e^{-x}\mathcal L(\pm\zeta z,x)dx
 =\Gamma(j+3/2)(1\mp\zeta z)^{j+1/2}.
\]

It is at most `Gamma(j+3/2)2^(j+1/2)`. This is a positive absolute dominator, including the potentially growing negative branch, multiplied by the integrable Beta factor. For each fixed zeta<1 the original series can also be exchanged with x integration: on any generating-function circle of radius A with zeta<A<1, Cauchy's estimate bounds the polynomial coefficient by a constant times `A^-s exp(xA/(1+A))`. Multiplication by e^-x leaves an exponential `exp(-x/(1+A))`; the residual geometric factor `(zeta/A)^s` is summable. Thus no conditional interchange is being smuggled through Abel summation.

The finite parity sum cancels the initial segment; in either parity the remaining indices are `N-1+2u`, u>=1. The correction is consequently a diagonal tail.

Let `sigma_j=(-1/2)_j/j!`, so sigma_0=1 and sigma_j=-b_j with b_j>0 for j>=1. The connection formula and shifted orthogonality give

\[
 Q(r,s)=\int_0^\infty x^{1/2}e^{-x}L_r(x)L_s(x)dx
 =\sum_{j=0}^{\min(r,s)}\sigma_{r-j}\sigma_{s-j}\widehat h_j,
 \quad\widehat h_j=\Gamma(j+3/2)/j!.
\]

Two independently checkable identities are

\[
 b_d-\sum_{t\ge1}b_tb_{t+d}=\kappa_d=\frac1{\pi(d^2-1/4)},\qquad
 \sum_{t\ge1}t b_tb_{t+d}=\frac1{\pi(2d+1)}.
\]

For the first use the absolutely convergent Fourier series of `B(z)=1-sqrt(1-z)` on the unit circle. The positive-d Fourier coefficient of `B(z)(1-B(z^-1))` is minus that of `|1-z|=2sin(theta/2)`, which integrates to the displayed kappa_d. For the second use

`b_n=pi^-1 integral_0^1 x^(n-3/2)(1-x)^(1/2)dx`,

Tonelli, and `xB'(x)=x/(2sqrt(1-x))`. The result is the integral of `x^(d-1/2)/(2pi)`.

Therefore

\[
 -Q(r,r+d)=\widehat h_r K_{r,d},\qquad
 K_{r,d}=\kappa_d+
 \sum_{t=1}^r(1-p_{r,t})b_tb_{t+d}+\sum_{t>r}b_tb_{t+d}>0,
\]

where `p_(r,t)=product_(j=0)^(t-1)(r-j)/(r+1/2-j)`, extended by zero for t>r. Every factor increases with r; subtraction of the two convergent positive expressions therefore proves `K_(r+1,d)<=K_(r,d)`, including r=0. This handles signs and the N=1 starting kernel explicitly.

For fixed r, the finite connection convolution gives `Q(r,s)=O_r(s^-3/2)`. The parity weights are `O(m^-1/2)`. Hence the completed tail is an ordinary absolutely convergent `O_N(m^-2)` series. Its positive reindexing and the subtraction between adjacent dimensions are legitimate ordinary sums, not merely Abel values. Constants may depend on fixed N; no uniform-in-N tail estimate is required for this argument.

Gamma duplication after reindexing yields

\[
 \Xi_N=\sum_{u\ge1}A_{N,u}K_{N-1,2u},\qquad
 A_{N,u}=\frac{\sqrt2}{N^{3/2}}G(N/2)\frac{(N/2)_u}{((N+1)/2)_u},
\]

with `G(x)=Gamma(x+1/4)Gamma(x+3/4)/(Gamma(x)Gamma(x+1/2))`. All coefficient and kernel signs are now fixed before discarding diagonals.

## 3. New square-only comparison of every correction coefficient

The source proves the needed coefficient decrease by shape interpolation. The following independent validation avoids all continuous-shape monotonicity premises. With c=N/2 the exact adjacent ratio is

\[
 R_{N,u}=\left(\frac N{N+1}\right)^{3/2}\frac{2N+1}{2N}
 \prod_{j=0}^{u-1}\frac{(c+j+1/2)^2}{(c+j)(c+j+1)}.
\]

Each product factor exceeds one. Its infinite limit, by the standard Gamma quotient limit, is

`Gamma(c)Gamma(c+1)/Gamma(c+1/2)^2`.

For c>1/4, define

`f(c)=log[Gamma(c+1/2)/Gamma(c)]-0.5log(c-1/4)`.

The digamma integral gives

\[
 f'(c)=\frac12\int_0^\infty e^{-(c-1/4)t}
 [\operatorname{sech}(t/4)-1]dt<0.
\]

Its limit at infinity is zero by the Gamma quotient asymptotic. Thus f(c)>0 and

`Gamma(c+1/2)/Gamma(c)>sqrt(c-1/4)`.

All integrals here converge for c>1/4. The square c=N/2 lies strictly in this domain. It follows that for N>=2,

\[
 R_{N,u}<\left(\frac N{N+1}\right)^{3/2}\frac{2N+1}{2N-1}<1.
\]

The last inequality has positive sides; after squaring, its residue is

`(N+1)^3(2N-1)^2-N^3(2N+1)^2=4N^4-5N^2-N+1`.

Putting N=t+2 gives `4t^4+32t^3+91t^2+107t+43>0` for every t>=0. At N=1 the product limit gives `R_(1,u)<3pi/(8sqrt2)<1`; use pi<22/7 and sqrt2>7/5. Therefore `A_(N,u)>A_(N+1,u)` for EVERY positive N and u, by a universal square argument. No finite diagonal cutoff and no unverified shape extension enters it.

For the quantitative first diagonal, set q(x)=G(x)/sqrt(x). The same standard digamma differences give

`d log q/dx=integral_0^infinity e^-xt[1/(1+e^-t/4)-1/2]dt>0`.

The source's companion upper estimate `g(x)<1/(2x)+1/(16x^2)` is also valid by `tanh(t/8)<t/8`, but this square-only route does not require it. Gamma duplication gives `q(3/2)=(15/16)sqrt(pi/3)>15/16` and `A_(N,1)=q(N/2)/(N+1)`.

The exact adjacent first-diagonal ratio is

\[
 \frac{A_{N+1,1}}{A_{N,1}}=
 \frac{(2N+1)\sqrt{N+1}}{2\sqrt N(N+2)}<1-\frac1{2N},\quad N\ge3.
\]

After squaring, its residue is `4N^3-4N^2-13N+4`; at N=t+3 it is `4t^3+32t^2+71t+37>0`. All denominators and the right side are positive. Hence, using kappa_2=4/(15pi),

\[
 \Xi_N-\Xi_{N+1}>
 (A_{N,1}-A_{N+1,1})\kappa_2>
 \frac1{8\pi N(N+1)},\quad N\ge3.
\]

The first inequality follows by subtracting in common positive coordinates:

`Xi_N-Xi_(N+1)=sum_u (A_Nu-A_(N+1,u))K_(N-1,2u)+sum_u A_(N+1,u)(K_(N-1,2u)-K_(N,2u))`.

Each term is nonnegative and the coefficient gaps are strictly positive. Thus the discarded terms cannot conceal an adverse signed dimension subtraction.

## 4. Supporting complex decrement upper bound, without an imported theorem claim

Write `Y_n=ETr sqrt(G_nG_n*)`, `C_n=Y_n/n^(3/2)`, `Delta_n=C_n-C_(n+1)`, and Y_0=0. The exact square LUE density gives `Y_n=sum_(j<n) integral sqrt(x)e^-x L_j(x)^2 dx`. The finite connection formula of Section 2 therefore gives a positive convolution for the individual moments. Consequently

\[
 H(z)=\sum_{n\ge1}\frac{Y_n}{\sqrt\pi}z^n
 =\frac z2(1-z)^{-5/2}F(z),\qquad
 F(z)={}_2F_1(-1/2,-1/2;1;z),\quad |z|<1.
\]

The power series solves `z(1-z)F''+F'-F/4=0`. Conjugating by the explicit factor `z(1-z)^(-5/2)/2` and comparing coefficients gives

\[
 n^2(Y_{n+1}-2Y_n+Y_{n-1})=\tfrac34Y_n,\quad n\ge1,
 \qquad Y_0=0,\ Y_1=\sqrt\pi/2.
\]

This bridges the actual law to the recurrence by finite orthogonality and a formal/analytic power series; it does not require an unexplained Carlson continuation or the withdrawn old Lemma 1. At n=1 no negative-index value is needed.

The supporting bound needs an exact asymptotic constant, not only the order of Delta_n. [DLMF 15.8.10](https://dlmf.nist.gov/15.8#E10), at a=b=-1/2 and integer excess 2, gives the convergent logarithmic expansion

\[
 F(1-t)=\frac4\pi-\frac t\pi-
 \frac{t^2}{4\pi}\sum_{k\ge0}\frac{(3/2)_k^2}{k!(k+2)!}t^k
 [\log t-\psi(k+1)-\psi(k+3)+2\psi(k+3/2)],
\]

for `0<|t|<1`, `|arg t|<pi`, on the principal branch. In particular its quadratic analytic/log coefficients are `(8log2-5)/(16pi)` and `-1/(8pi)`. F is analytic off `[1,infinity)`. After multiplication by z t^-5/2/2, truncation through index J leaves a remainder analytic in a Delta-domain at 1, bounded by `O_J(|t|^(J-3/2)(1+|log t|))` in closed subsectors. The standard Delta-domain coefficient-transfer theorem therefore gives `O_J(n^(-J+1/2)log n)` for Y_n. Its analyticity hypothesis is explicitly satisfied; a bare real-axis remainder would not suffice.

Coefficient extraction uses

`[z^n](1-z)^a=Gamma(n-a)/(Gamma(-a)Gamma(n+1))`

and its derivative in a. The Gamma ratio expansion applies at fixed real half-integer shifts, within the domain of [DLMF 5.11.13](https://dlmf.nist.gov/5.11#E13). At indices 0,1,2 of H the coefficients are

`c0=2/pi`, `c1=-5/(2pi)`, `c2=(8log2+11)/(32pi)`, `d2=-1/(16pi)`.

The n^-1 contributions cancel. At order n^-2 the three terms contribute respectively `65/(48pi)`, `-15/(8pi)`, and `(log n+gamma+6log2+11/2)/(16pi)`. Thus the constant is exactly -17/(96pi).

For completeness the needed remainder improvement is justified by the recurrence, rather than by pretending differences of O(n^-3) errors cancel. Arbitrary-order coefficient transfer first gives an expansion of the form `Y_n~sum_j n^(3/2-j)(A_j log n+B_j)`. In the recurrence, the leading multiplier at index j is `j(j-2)`, with logarithmic cross term `2(1-j)A_j`; only indices j,j-2,... couple. Index 1 vanishes, and each odd index then vanishes inductively since j(j-2) is nonzero. This is a comparison of valid arbitrary-order expansions. In particular

\[
 C_n=\frac8{3\pi}+\frac{\log n+\gamma+6\log2-17/6}{16\pi n^2}
 +O(\log n/n^4),
\]

and direct subtraction, bounding each remainder separately, gives

\[
 \Delta_n=\frac{\log n+\gamma+6\log2-10/3}{8\pi n^3}
 +O(\log n/n^4).
\]

Now define `q_j=(j+2)^(3/2)-2(j+1)^(3/2)+j^(3/2)-3/(4sqrt(j+1))`, and

`E_n=8pi[n(n+1)]^(3/2)Delta_n-log n`.

The exact recurrence gives, for every d>=2,

`E_d-E_(d-1)=8pi q_(d-1)Y_d-log(d/(d-1))`.

Also `q_j>0`: the centered second difference of x^(3/2) is the triangular-weight average of `3/(4sqrt(j+1+t))`; strict convexity and Jensen prove positivity of the excess over its midpoint.

The independent auxiliary upper bound follows from the positive convolution: `(3/2)_k/k!` increases in k, and the sum of squared connection coefficients is `F(1)=4/pi` by Gauss summation. Extend the finite positive sum, then sum `(3/2)_k/k!` using the binomial identity. This gives

`C_d<8(d+1/2)Gamma(d+1/2)/(3pi d^(3/2)Gamma(d))<8(d+1/2)/(3pi d)`.

The second inequality is strict Gamma log convexity, valid already for d=1. These bounds precede all Delta-sign conclusions.

**Explicit smallest-index repair.** AP Lemma 6 is printed for q_j, j>=2; the subsequent proof at d=2 requires q_1. It is a real omission of stated domain, but its actual coefficient proof covers every `0<t<1`. At `t=1/(j+1)`, its inequality is

\[
 \frac{64}{3t^4}[(1+t)^{3/2}+(1-t)^{3/2}-2-3t^2/4]
 <\frac{-\log(1-t)}{t(1+t/2)}.
\]

The left coefficients at powers t^(2k) are `lambda_k=(128/3)binom(3/2,2k+4)`, with `lambda0=1`, `lambda1=7/24`, `lambda2=33/256`. The ratio comparison with `(k+1)/(k+2)` has positive residue `24k^2+77k+50`. Starting with `lambda3=143/2048<1/12`, induction gives `lambda_k<1/(3(k+1))` for every k>=3.

The right coefficients satisfy

`a_m=integral_0^1 (s^(m+1)-(-1/2)^(m+1))/(s+1/2) ds`.

Consequently `a_(2k)>1/(3(k+1))`, while

`a_(2k+1)=sum_(r=0)^k 4^-r[1/(2k+2-2r)-1/(2(2k+1-2r))]>=0`.

Each bracket is nonnegative. The exceptional comparisons are `a0=lambda0`, `a2=1/3>7/24`, `a4=19/120>33/256`. Both series converge for `0<t<1`; their coefficientwise comparison is strict for positive t. This is a universal proof, including t=1/2 and hence q_1. The needed repaired estimate is therefore

`q_(d-1)<3log(d/(d-1))/(64sqrt(d)(d+1/2))`, for EVERY d>=2.

Combining it with the auxiliary C_d upper bound proves `E_d<E_(d-1)` for every d>=2. The verified asymptotic gives `E_n -> C0=gamma+6log2-10/3`, so E_n>C0. Since C0>0 (gamma>0 and log2>2/3), this proves Delta_n>0. Together with the independently known limit it gives `C_d>8/(3pi)`.

Only now use this lower bound. The binomial expansion of q_(d-1) has strictly positive even coefficients starting at fourth order, so `q_(d-1)>3/(64d^(5/2))`. Hence `8pi q_(d-1)Y_d>1/d` and

`E_(d-1)-E_d<log(d/(d-1))-1/d`.

Both sides are positive. Summing to infinity, using the established E limit and the definition of gamma, gives

`E_n-C0<H_n-log n-gamma`.

After substitution this is precisely the real paper's supporting upper bound:

\[
 0<\Delta_n<\frac{H_n+6\log2-10/3}{8\pi[n(n+1)]^{3/2}},\qquad n\ge1.
\]

The argument is noncircular: positive convolution gives the auxiliary upper bound; coefficient comparison and the verified E limit give the lower Delta sign; that sign and the common limit give the C lower bound; the first q coefficient then gives the desired Delta upper bound. No real theorem is used to establish its complex dependency.

## 5. Uniform real reserve and the exact finite exceptions

Subtracting the verified complex upper bound from Section 3 gives, for N>=3,

\[
 a_{N+1}-a_N>
 \frac{\sqrt{N(N+1)}-H_N-(6\log2-10/3)}{8\pi[N(N+1)]^{3/2}}.
\]

Use log2<7/10. At N=4, `H4+6log2-10/3<59/20<3`. The left side grows by `1/(N+1)` while `3N/4` grows by 3/4, proving `H_N+6log2-10/3<3N/4` for all N>=4. Since sqrt(N(N+1))>N, the preceding reserve exceeds

`(N/(N+1))^(3/2)/(32pi N^2)>1/(160N^2)`.

For the last inequality use `N/(N+1)>=4/5`, `(4/5)^(3/2)>7/10`, pi<22/7, and `7/(10*32*(22/7))>1/160`. This is an induction and exact rational comparison, not a finite harmonic test.

For N=1,2,3, direct finite density integration, now under the universally verified joint law, gives the raw half moments

\[
 Y^R_1=\sqrt{2/\pi},\quad
 Y^R_2=\sqrt\pi(2-\sqrt2/2),\quad
 Y^R_3=3\sqrt\pi/2+2\sqrt{2/\pi},\quad
 Y^R_4=\sqrt\pi(153/32-3\sqrt2/4).
\]

The first is the scalar Gaussian law. Independently, for N=2 the singular-value polar law has radial density proportional to `r^3e^-r^2/2` and angular weight `-cos(2theta)` on `[pi/4,pi/2]`. Its mean radius is `3sqrt(2pi)/4`; the weighted angular mean of sin(theta)+cos(theta) is `(4sqrt2-2)/3`, giving exactly Y^R_2.

For the finite density integrations, expand L into rational monomials and use Gamma half-integer values. In the even incomplete-Gamma term let `I_j=integral x^j e^-x/2 erfc(sqrt(x/2))dx`. Integration by parts gives `I0=2-sqrt2` and `I_j=2jI_(j-1)-sqrt2 Gamma(j+1/2)/sqrtpi`. The odd border needs only `integral x^j e^-x/2 dx=2^(j+1)j!`. These exact formulas produce the four displayed moments in `controls.py`; they are not fitted values.

Machin's alternating arctangent formula rigorously encloses pi, and integer square roots enclose every radical. Rational interval subtraction in `CONTROL_RECEIPTS.json` proves `a_(N+1)-a_N>1/(160N^2)` for N=1,2,3. Its interval endpoints and targets are retained in full. For example the actual increments are approximately 0.01232, 0.00857, and 0.00555, well above 0.00625, 0.0015625, and 0.00069444. These decimals are illustrative; only the rational enclosure decides the finite pass.

Thus the quantified proof and the finite exceptions cover EVERY integer N>=1. The convergence to 8/(3pi) follows from square Marchenko-Pastur convergence with uniform integrability: the expected empirical first eigenvalue moment of XX^T/N is exactly one, bounding the discarded square-root tail above threshold M by 1/sqrt(M). It does not depend on a continuous-shape theorem.

## 6. New controls, limits, and parent-owned disposition

`controls.py` completes **862 executed assertions**. The count is transparent: 216 are repeated angular coefficient checks inside integer-moment evaluation; it is not 862 independent theorem proofs. Its new controls include:

- Exact density mass, ETrW and ETrW^2 for N=1..16, agreeing with N, N^2 and N^2(2N+1). The last values follow independently from the three Wick pairings of four real entries. These test the law and scaling with statistics different from the original half moment.
- Exact inversion of the joint-law skew/Pfaffian matrices in both parities, and 80 pointwise density comparisons for N=1..10 at x=0.0001,0.1,0.5,1,2,4,8,16. These use a separate Pfaffian route and the printed density, with 85-digit Decimal arithmetic. They are finite high-precision diagnostics, explicitly not formal interval certificates or universal positivity evidence.
- Forty-nine deliberately corrupted density variants are rejected: omitted odd border, even incomplete-Gamma expression at odd size, reversed orthogonal correction, wrong real variance rescaling, missing Jacobian and omitted dimension normalization. This shows the direct-law control can detect the vulnerable parity and scaling mistakes.
- Exact finite half moments and rational interval reserves N1..3, plus transcription controls for the new square-only gamma-product polynomial and the supporting AP coefficient induction.

The universal conclusions come from Sections 1-5, with named standard identities/theorems used in their proper domains. The bounded computations are falsification and reproducibility controls. The report is not a formal proof-assistant certificate and does not claim every theorem in either preprint is correct.

`HISTORICAL_REPLAY_RECEIPTS.json` reproduces the original 383/383/53 controls from unchanged copies in this audit's ignored tmp. Their limited source-consistency scope is preserved. The original scripts never claimed a full real proof. No root or historical verdict is treated as a proof premise; their derivations were independently checked after the seal.

**Strongest verified result:** the exact original real square statistic satisfies the external paper's strict universal reserve `a_(N+1)-a_N>1/(160N^2)` for every N>=1, after a checkable boundary-domain clarification of AP Lemma 6. **Exact remaining mathematical gap for this square result:** none identified at ordinary analytic-proof standard. **Theorem-false evidence:** none found. **Remaining process requirement:** the parent-owned complete gate, including both original directions, source/history/budget consistency, and any current correction. This report alone does not approve a PR merge or mutate global status.

The historical source audit accurately retained an incomplete-certification hold when written. A current already-solved-by-external-work correction can now be considered by the parent without awarding campaign solution credit, creating a new paper, consuming proof-search attempts, issuing a release or DOI, or erasing that historical hold. No outside individual was contacted; no Git, PR, canonical-state, or publication mutation was performed by this auditor.
