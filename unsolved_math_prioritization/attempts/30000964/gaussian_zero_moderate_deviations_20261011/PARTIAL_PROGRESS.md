# Gaussian zero moderate deviations: one bounded attempt

Problem 30000964 / OWR-1970-002. Inspection date: 2026-10-11 UTC.

## Outcome and limits

The requested sharp asymptotic is **not resolved** here. This attempt proves a non-sharp, two-sided quadratic-speed bound over the full range `1 << c << r`, including the requested interval `r/(log r)^2 << c << r`:

\[
-\frac{\zeta(3)}2
\ \leq\ \liminf_{r\to\infty}\frac{\log\mathbb P(Y_r>c)}{c^2}
\ \leq\ \limsup_{r\to\infty}\frac{\log\mathbb P(Y_r>c)}{c^2}
\ \leq\ -\frac{3\zeta(3)}{\pi^2},                         \tag{A}
\]

where

\[
Y_r=\frac{r Z_0(h_r)}{\sigma\|\Delta h\|_2},\qquad
\sigma=\frac14\sqrt{\frac{\zeta(3)}\pi}.
\]

The constants are approximately -0.6010284516 and -0.3653814847; the target -1/2 lies strictly between them. Both bounds apply to either tail by replacing h with -h. These are authored deductions from established Gaussian inequalities and explicit computations, not a claim that these bounds are new to the literature. No counterexample is produced. The outstanding task is the exact coefficient, not merely quadratic exponential scale.

## 1. Exact primary question and existing theorem range

The official report is *Stochastic Analysis*, Oberwolfach Reports 5 (2008), 1361–1424, DOI 10.4171/OWR/2008/25; publisher publication date 31 March 2009. Tsirelson's contribution occupies printed pp. 1367–1369. Printed p. 1368 was also visually inspected.

The model is

\[
F(z)=\sum_{k\ge0}\zeta_k\frac{z^k}{\sqrt{k!}},\qquad
\mathbb E|\zeta_k|^2=1,
\]

with independent circular complex Gaussian coefficients. For fixed real h in C_c^2(C), put h_r(z)=h(z/r) and

\[
Z_0(h_r)=\sum_{F(a)=0}h(a/r)-\frac{r^2}\pi\int_{\mathbb C}h.
\]

Assume H:=||Delta h||_2>0. The source's first question on p. 1368 asks whether the Gaussian logarithmic-tail equivalence extends to **r/(log r)^2 << c << r**. Its separate second question concerns general stationary fields and is not the present problem. An earlier transcription incorrectly starts at (log r)^2; the verified source correctly preserves r/(log r)^2.

Theorem 1.5 and Corollary 1.6 of Tsirelson, arXiv:1810.05673v2 (13 September 2019), have, respectively,

\[
\lambda(\log r)^d\to0,\qquad
\frac{(c(\log r)^d)^2}{r^d}\to0.
\]

For d=2 the second condition is c(log r)^2/r -> 0. In arXiv:1909.03238v2 (19 September 2019), equations (1.5) and (1.6), printed p. 3, explicitly retain the same restrictions for zero statistics. Theorem 5.25, pp. 48–49, supplies splittability of the logarithmic GEF field. Part V p. 3 identifies its results as detailed proofs of the earlier results, rather than a removal of the logarithmic restriction.

Example: c=r/log r is in the requested interval but gives c(log r)^2/r=log r -> infinity. Neither theorem applies. Convergence at each fixed c or control of fixed-order cumulants cannot repair this mismatch.

## 2. Reduction to a logarithmic Gaussian field

Write

\[
G(z)=e^{-|z|^2/2}F(z),\qquad X(z)=\log|G(z)|+\gamma/2,
\qquad w=\Delta h,
\]

and S_r=integral w(z/r)X(z) dA(z). The distributional zero-counting identity gives

\[
Z_0(h_r)=\frac{S_r}{2\pi r^2},\qquad
Y_r=\frac{S_r}{a r},\qquad
 a=\frac12\sqrt{\pi\zeta(3)}H.                            \tag{2.1}
\]

All integrals are real area integrals. The log singularities are locally integrable, and finite first absolute moments also justify the integrals in probability.

Use a complex Hilbert space H_0=ell^2 and unit coherent vectors k_z with

\[
|\langle k_z,k_y\rangle|^2=e^{-|z-y|^2},\qquad
\int_{\mathbb C}|k_z\rangle\langle k_z|\,dA(z)=\pi I.     \tag{2.2}
\]

Here the last equality is a weak operator identity. It follows directly by integrating monomials: integral exp(-|z|^2) z^j conjugate(z)^k /sqrt(j!k!) dA = pi delta_jk. Thus no unproved continuous-frame estimate is needed. We realize G(z) as the complex isonormal Gaussian evaluation at k_z. Inner-product conventions may conjugate the kernel but leave all operators and absolute-square identities unchanged.

For two jointly proper normalized complex Gaussians with correlation modulus rho, Nazarov–Sodin, arXiv:1003.4251v1, Lemma 2.2, gives

\[
\operatorname{Cov}(\log|\eta_1|,\log|\eta_2|)
=\frac14\sum_{m\ge1}\frac{\rho^{2m}}{m^2}
=\frac14\operatorname{Li}_2(\rho^2).                     \tag{2.3}
\]

In particular, the integrated covariance of X is pi zeta(3)/4. Dominated convergence using (2.3) yields Var(S_r)/r^2 -> a^2, checking every normalization in (2.1).

## 3. A Laplace bound without a logarithmic restriction

### Lemma 3.1

For every real continuous compactly supported v on C and real lambda with
pi |lambda| ||v||_infinity < 2,

\[
\log\mathbb E\exp\left(\lambda\int v(z)X(z)\,dA(z)\right)
\leq\frac1\pi\int K(\pi\lambda v(z))\,dA(z),             \tag{3.1}
\]

where

\[
K(s)=\log\Gamma(1+s/2)+\gamma s/2,\quad s>-2.
\]

The RHS vanishes off the support of v. A more general admissible domain is possible, but the displayed symmetric domain suffices.

**Proof, including the continuum passage.** Theorem 1(i) of Chen–Dafnis–Paouris, arXiv:1306.2410v2, is the following finite-dimensional Gaussian Hölder inequality: for a centered Gaussian block vector with identity diagonal covariance blocks, joint covariance T, positive p_i, and T <= diag(p_i I),

\[
\mathbb E\prod_i f_i(\eta_i)\leq
\prod_i(\mathbb E f_i(\eta_i)^{p_i})^{1/p_i}
\]

for nonnegative measurable f_i. Complex Gaussians are treated as their two real coordinates scaled to have identity covariance.

Enclose supp(v) in a compact rectangle D and partition D into cells Q_i with areas d_i and mesh tending to zero. Let

\[
\bar k_i=d_i^{-1}\int_{Q_i}k_z\,dA(z),\quad
b_i=d_i\|\bar k_i\|^2,\quad u_i=\bar k_i/\|\bar k_i\|.
\]

Omit zero b_i. Cauchy–Schwarz and (2.2) give

\[
\sum_i b_i |u_i\rangle\langle u_i|
=\sum_i d_i|\bar k_i\rangle\langle\bar k_i|
\leq\int_D |k_z\rangle\langle k_z|\,dA(z)\leq\pi I.     \tag{3.2}
\]

For eta_i the proper standard complex Gaussian evaluation at u_i, (3.2) is equivalent to the required block covariance inequality with p_i=pi/b_i: this is the usual equivalence of the Gram-operator bound and the frame-operator bound, also after realification. In particular b_i<=pi and p_i>=1. Put X_i=log|eta_i|+gamma/2 and choose sample points z_i in Q_i. Applying the finite inequality to
f_i=exp(lambda b_i v(z_i)X_i) yields

\[
\log\mathbb E e^{\lambda\sum_i b_i v(z_i)X_i}
\leq\sum_i\frac{b_i}\pi K(\pi\lambda v(z_i)).             \tag{3.3}
\]

The map z -> k_z is norm-continuous and uniformly so on fixed D. Consequently ||bar k_i|| -> 1 uniformly and u_i -> k_z uniformly for z in Q_i. Corresponding Gaussian evaluations converge in L^2 uniformly; their log moduli converge in L^1 uniformly. For the latter assertion, first truncate the logarithm to a bounded continuous function of modulus, then remove the truncation using the common complex-normal marginal law and its finite second log moment. Thus the sum inside (3.3) converges in L^1 to integral vX. Select an almost surely convergent subsequence and apply Fatou to the nonnegative exponentials. The RHS is a Riemann sum converging to the RHS of (3.1). Finally, |eta|^2 is exponential of mean one, so E exp(s(log|eta|+gamma/2)) = exp(gamma s/2) Gamma(1+s/2). This proves the lemma. No assumption of independence of field restrictions to disjoint cells was made.

### Corollary 3.2: the upper bound in (A)

Uniformly for s in a fixed small interval,

\[
K(s)=\frac{\zeta(2)}8s^2+O(|s|^3)
=\frac{\pi^2}{48}s^2+O(|s|^3).
\]

Apply (3.1) to v(z)=w(z/r). For lambda -> 0,

\[
\log\mathbb E e^{\lambda S_r}
\leq\frac{\pi^3}{48}\lambda^2r^2 H^2
   +O_h(|\lambda|^3r^2).                                \tag{3.4}
\]

Let c -> infinity and c/r -> 0, and put lambda=kappa c/(ar), for a fixed positive kappa. By (2.1),

\[
\limsup\frac1{c^2}\log\mathbb E e^{\kappa cY_r}
\leq \frac{\beta\kappa^2}2,
\qquad \beta=\frac{\pi^2}{6\zeta(3)}.
\]

Chernoff's inequality, optimized at kappa=1/beta, gives
limsup c^-2 log P(Y_r>c) <= -1/(2 beta) = -3 zeta(3)/pi^2.
The remainder divided by c^2 is O_h(c/r), so this calculation really does cover the requested regime.

## 4. A Gaussian covariance tilt: the lower bound

Define the self-adjoint trace-class operator

\[
A_r=\int w(z/r)|k_z\rangle\langle k_z|\,dA(z).
\]

It satisfies

\[
\|A_r\|\leq M:=\pi\|w\|_\infty,
\quad \|A_r\|_1\leq r^2\|w\|_1,
\]

and

\[
D_r:=\operatorname{Tr}A_r^2
=\iint w(z/r)w(y/r)e^{-|z-y|^2}\,dA(z)dA(y)
\sim\pi r^2H^2.                                         \tag{4.1}
\]

The last assertion follows by L^2 continuity under translations and dominated convergence after y=z+u. It holds despite the sign changes in w.

The real quadratic statistic

\[
Q_r=\int w(z/r)(|G(z)|^2-1)\,dA(z)
\]

has the distribution sum_j alpha_j(|eta_j|^2-1), where alpha_j are the eigenvalues of A_r and eta_j are independent standard complex Gaussians. Absolute summability of alpha_j makes this representation L^1-convergent. It can also be obtained by finite-rank approximation of the defining integral. For |t|M<1,

\[
L_r(t):=\log\mathbb E e^{tQ_r}
=-t\operatorname{Tr}A_r-\log\det(I-tA_r)
=\sum_{m\ge2}\frac{t^m}{m}\operatorname{Tr}A_r^m.          \tag{4.2}
\]

Let P_t have density exp(t Q_r-L_r(t)) relative to P. By diagonalizing A_r, P_t is a centered proper Gaussian law on the coefficient process with covariance
C_t=(I-t A_r)^-1. The density construction, rather than a formal infinite product, defines this measure; (4.2) normalizes it. The finite-coordinate tilted laws, or their characteristic functions, identify the asserted covariance. For |t|M<=1/2 its eigenvalues lie between 2/3 and 2.

### 4.1 Tilted mean

Under P_t, G(z) has variance v_t(z)=<C_t k_z,k_z>. Scaling a complex Gaussian gives

\[
\mathbb E_t X(z)=\tfrac12\log v_t(z).
\]

The resolvent and the logarithm Taylor expansions, uniformly in z and r, yield

\[
\log v_t(z)=t\langle A_rk_z,k_z\rangle+O_h(t^2),
\]

hence

\[
\mathbb E_t S_r=\frac t2 D_r+O_h(t^2r^2).                 \tag{4.3}
\]

### 4.2 Tilted variance, with uniform control

Let K_t(z,y)=<C_t k_z,k_y>. The normalized tilted field is still jointly proper complex Gaussian. By (2.3), using Li_2(u)<=zeta(2)u on [0,1] and v_t>=1/2,

\[
|\operatorname{Cov}_t(X(z),X(y))|
\leq\zeta(2)|K_t(z,y)|^2.
\]

Let D be any fixed bounded rectangle containing supp(w). From (2.2),

\[
\int_{\mathbb C}|K_t(z,y)|^2\,dA(y)
=\pi\|C_t k_z\|^2\leq4\pi.
\]

Therefore

\[
\operatorname{Var}_t S_r
\leq\zeta(2)\|w\|_\infty^2
 \int_{rD}\int_{\mathbb C}|K_t(z,y)|^2\,dA(y)dA(z)
\leq4\pi\zeta(2)\|w\|_\infty^2 |D|r^2.                  \tag{4.4}
\]

This explicitly avoids any unproved mixing property of the tilted field.

### 4.3 Entropy cost and tail lower bound

Since |Tr A_r^m| <= M^(m-2) D_r for m>=2, (4.2) implies uniformly for t -> 0

\[
\mathcal H(P_t\mid P)=tL_r'(t)-L_r(t)
=\frac{t^2}{2}D_r+O_h(|t|^3D_r).                         \tag{4.5}
\]

Fix epsilon>0, b_r=ar c, and choose

\[
t_r=\frac{2(1+\epsilon)b_r}{D_r}.
\]

By (4.1), t_r=O_h(c/r)->0. Equations (4.3) and (4.4) show

\[
\mathbb E_{t_r}S_r=(1+\epsilon)b_r+o(b_r),\qquad
P_{t_r}(S_r>b_r)\to1,
\]

because r^2/b_r^2=O_h(c^-2)->0. If E_r={S_r>b_r}, p_r=P_t(E_r), and q_r=P(E_r), binary relative entropy gives

\[
\mathcal H(P_t\mid P)\geq p_r\log(1/q_r)-\log2.
\]

Thus log q_r >= -(H(P_t|P)+log2)/p_r. By (4.1) and (4.5),

\[
\liminf\frac{\log q_r}{c^2}
\geq-\frac{2(1+\epsilon)^2a^2}{\pi H^2}
=-\frac{\zeta(3)}2(1+\epsilon)^2.
\]

Let epsilon decrease to zero after taking the liminf. This proves the lower bound in (A), including strict `>` thresholds.

## 5. Precisely why this attempt stops short

The upper bound treats the log functional using the general Gaussian Hölder inequality and pays effective variance

\[
\frac{\pi^3}{24}H^2=\frac{\pi^2}{6\zeta(3)}a^2>a^2.
\]

The lower bound tilts only a quadratic Gaussian statistic. The first nonconstant Laguerre term of log|eta| is (|eta|^2-1)/2; its spatial variance density is pi/4, while the total is pi zeta(3)/4. Its fraction 1/zeta(3) explains the cost zeta(3)/2 instead of 1/2. These quantified losses are methodological, not evidence that the target coefficient is false.

One sufficient missing estimate is

\[
\frac1{r^2\lambda^2}\log\mathbb E e^{\lambda S_r}
\longrightarrow\frac{a^2}2
\quad(r\to\infty,\ \lambda\to0),                         \tag{5.1}
\]

without the condition lambda(log r)^2 -> 0. For the desired tail it suffices to establish (5.1) at lambda=kappa c/(ar) for each fixed real kappa. It would give the quadratic limiting scaled log-MGF and then the sharp moderate-deviation rate. Neither (3.4) nor the quadratic covariance tilt proves (5.1).

An all-order cumulant route would need uniform analytic control at this moving parameter, not merely the vanishing of each fixed standardized cumulant. Another tempting route, applying strong-mixing theorems to field restrictions, cannot be justified simply from the small pointwise covariance of G: an analytic function is determined by its restriction to any nonempty open set. The arguments above do not assume such mixing.

## 6. Current literature screen and noncoverage checks

A targeted web search on 2026-10-11 used combinations of Gaussian entire function, moderate deviations, linear statistics, cumulants, Tsirelson, and years 2020–2026; follow-up searches checked Gaussian Hölder/Brascamp–Lieb exponential moment methods. No primary source establishing the sharp requested regime was located. This is a bounded negative search result, not a proof of present-day open status or an exhaustive bibliography.

- Tsirelson IV and V, pinned versions above: actual formulas and applicability checked, not just abstracts.
- Nazarov–Sodin, arXiv:1003.4251v1: Lemmas 2.1–2.2 read for the log covariance/chaos identities. It is a CLT paper and is not being claimed to supply the missing MDP.
- Chen–Dafnis–Paouris, arXiv:1306.2410v2: Theorem 1(i) and its hypotheses read. It supplies a Gaussian product inequality, not an existing theorem claiming (A) for GEF zeros.
- Nishry–Wennman, *The forbidden region for random zeros: Appearance of quadrature domains*, DOI 10.1002/cpa.22142 (first online 2 October 2023), publisher abstract and Section 9.8 read. Section 9.8.2 concerns a hole-conditioned event with a linear-statistic discrepancy epsilon L^2; Remark 9.10 requires L^-1 log L=o(epsilon). Formula (9.4) also has an O(L^2 log^2 L) error. This does not supply the present unconditional shrinking-deviation sharp asymptotic. No inference from its title alone was used.
- Nishry, *Complex Gaussian Zeros and Eigenvalues*, Lecture Notes in Mathematics 2365 (2025), pp. 133–180, DOI 10.1007/978-3-031-87264-8_4: author-institution publication metadata and abstract only inspected. Full chapter was not read; it is not evidence for a sharp MDP claim.
- Kuryliak–Skaskiv, *Entire Gaussian Functions: Probability of Zeros Absence*, Axioms 12 (2023), 255, DOI 10.3390/axioms12030255: publisher abstract/introduction inspected. It concerns hole probabilities for other/general coefficient sequences, not this test-function moderate-deviation regime.

Source hashes, sizes, retrieval notes, and exact inspection limits are in SOURCE_METADATA.json. Source documents and extracts are not included.

## 7. Audit and reproducibility boundary

The proofs above are mathematical arguments. The separately authored numerical sanity check only checks constants and, for h(z)=(1-|z|^2)_+^4, the finite-radius diagonal quadratic-tilt operator. It verifies the predicted trace and normalization numerically; it is not a proof verifier. No Monte Carlo tail evidence is used.

Primary public links:

- Official report: https://ems.press/journals/owr/articles/1970 ; PDF https://ems.press/content/serial-article-files/46171?nt=1
- Earlier theorem: https://arxiv.org/abs/0801.1050v1
- Hierarchical IV: https://arxiv.org/abs/1810.05673v2
- Hierarchical V: https://arxiv.org/abs/1909.03238v2
- Gaussian Hölder input: https://arxiv.org/abs/1306.2410v2
- Log-covariance input: https://arxiv.org/abs/1003.4251v1
- Hole-conditioned noncoverage comparison: https://onlinelibrary.wiley.com/doi/10.1002/cpa.22142
- 2025 chapter metadata: https://cris.tau.ac.il/en/publications/complex-gaussian-zeros-and-eigenvalues/
- Hole-probability noncoverage comparison: https://www.mdpi.com/2075-1680/12/3/255
