# Independent adversarial review of the old Fourier implication

Review assembled on 2026-10-17 by the independent Fourier adversary subagent. This is an audit of an implication of published analytic estimates. It is not a claim of historical firstness, an earlier printed modular corollary, or a new proof of Gilmer-Kopparty's conditioning estimates.

## Verdict and exact claim

**PASS: the 2014 Gilmer-Kopparty characteristic-function lemmas imply the entire sufficiency claim.** Fix any p in (0,1). Let T_n be the number of unordered triangles in G(n,p), counted once. Put mu_n=E T_n, sigma_n=sqrt(Var T_n), and

\[
\Delta_n(q)=\max_{a\in\mathbb Z/q\mathbb Z}|q\Pr(T_n\equiv a\pmod q)-1|.
\]

For every sequence of positive integers q_n=o(sigma_n), the lemmas give Delta_n(q_n)->0. They actually give, eventually for every q>=2 with 2*pi*sigma_n/q>=1,

\[
\Delta_n(q)\le 2D\zeta(1+\delta)
\left(\frac{q}{2\pi\sigma_n}\right)^{1+\delta},
\tag{1}
\]

where D and delta>0 are fixed once p is fixed. Since sigma_n=Theta_p(n^2), the full range is q_n=o(n^2). There is no unverified mathematical gap in this elementary implication after accepting the source lemmas as imported theorems. Their deep analytic proofs were not reaudited here.

## Source interface and normalization

The fresh [Gilmer-Kopparty author manuscript](https://sites.math.rutgers.edu/~sk1233/triangles.pdf) is dated 6 December 2014. Its 401939 bytes have SHA-256 fd7578b138e1e29b01dcd2cc12a6e4e19150cf2bf1e71bc7f934568c175c9eaa. Definitions on PDF pp.1,4 and the theorem proof on p.5 identify S_n=T_n, R_n=(T_n-mu_n)/sigma_n, and psi_n(t)=E exp(it R_n). The mean p^3*binom(n,3) rules out ordered embeddings or 6T_n. The scale is the actual standard deviation, not the variance. Page 4 fixes p and permits p-dependent constants.

The imported statements on PDF p.6 are

\[
|\psi_n(t)|\le D_4|t|^{-1-\delta_0}
\quad(0<|t|\le n^{0.55}),\qquad
|\psi_n(t)|\le D_5|t|^{-50}
\quad(n^{0.55}\le |t|\le\pi\sigma_n).
\]

Here delta_0>0 and D_4,D_5 depend at most on fixed p, not on q, t or n. The source immediately combines the estimates into a uniform power envelope. Page 13 concludes Lemma 4 and restates Lemma 5, explicitly equating centered and uncentered characteristic-function magnitudes. These pages were visually inspected. This verifies the theorem interfaces and context, not every conditioning argument.

For the deduction it is enough to choose delta=min(delta_0,1), D=max(D_4,D_5). For |t|>=1 each displayed bound is at most D|t|^(-1-delta). Consequently

\[
|\psi_n(t)|\le D|t|^{-1-\delta}\quad
(1\le |t|\le\pi\sigma_n).
\tag{2}
\]

Only sufficiently large n>=3 is needed. The interface is uniform in n; finite initial exceptions, if any convention requires them, have no effect on the claim. No estimate uniform as p approaches 0 or 1 is asserted.

As an independent normalization check, direct covariance counting gives

\[
\mu_n=\binom n3p^3,\qquad
\sigma_n^2=\binom n3p^3(1-p^3)+12\binom n4p^5(1-p).
\tag{3}
\]

Indeed only a triangle with itself or two distinct triangles sharing an edge contribute. The latter covariance is p^5(1-p); unordered such pairs number binom(n,2)binom(n-2,2)=6binom(n,4), and the variance sum doubles them. Thus sigma_n/n^2 -> sqrt(p^5(1-p)/2)>0.

## Independent elementary proof of sufficiency

For q>=2 and integer a, the finite geometric sum is q when T_n-a is divisible by q and zero otherwise. Taking its expectation gives the exact roots-of-unity filter

\[
q\Pr(T_n\equiv a\pmod q)-1
=\sum_{j=1}^{q-1}e^{-2\pi ija/q}\,
\mathbb E e^{2\pi ijT_n/q}.
\tag{4}
\]

Set r_j=j for j<=q/2 and r_j=j-q otherwise, so |r_j|=j_*:=min(j,q-j). Integer-valuedness gives

\[
\mathbb E e^{2\pi ijT_n/q}
=\mathbb E e^{2\pi ir_jT_n/q}
=e^{2\pi ir_j\mu_n/q}
\psi_n(2\pi\sigma_nr_j/q).
\]

The phase has modulus one. Also psi_n(-t) is the conjugate of psi_n(t). Hence

\[
\left|\mathbb E e^{2\pi ijT_n/q}\right|
=|\psi_n(2\pi\sigma_nj_*/q)|.
\tag{5}
\]

This does not assert periodicity of the centered characteristic function: in general psi_n(t+2*pi*sigma_n)=exp(-2*pi*i*mu_n)psi_n(t). Only the uncentered characteristic function was reduced modulo 2*pi, and only magnitudes were then identified.

Write d_n=2*pi*sigma_n/q. If q=o(sigma_n), then d_n->infinity. Eventually every nonzero reduced grid point has absolute value at least 1. Every such point is also at most pi*sigma_n, because j_*<=q/2. Formula (2) therefore applies simultaneously to all q-1 points. Taking absolute values in (4) yields

\[
\Delta_n(q)\le Dd_n^{-1-\delta}
\sum_{j=1}^{q-1}j_*^{-1-\delta}
\le 2Dd_n^{-1-\delta}
\sum_{k=1}^{\infty}k^{-1-\delta}.
\]

This is (1). The last series is finite; if desired use zeta(1+delta)<=1+1/delta to avoid special-function notation. The bound is independent of a and q apart from the displayed power. It tends to zero for every q_n=o(sigma_n).

For q=1 the discrepancy is identically zero. If q_n alternates between 1 and other values, use the zero value at 1 and (1) on the remaining indices. No assumption that q_n grows, is monotone, or is prime was made.

## Attempts to falsify the inference

| Potential failure | Check and resolution |
| --- | --- |
| Wrong model or counting convention | Source mean p^3*binom(n,3), range [0,binom(n,3)], and independent variance (3) are the ordinary count. |
| Standard deviation confused with variance | Source definitions and (3) give sigma_n=Theta_p(n^2). The grid is 2*pi*sigma_n*j/q. |
| Hidden q-dependent constants | D and delta are selected before q and enter only the single power envelope (2). |
| Missing frequencies above n^0.55 | Lemma 5 reaches the entire remaining interval through pi*sigma_n. |
| Gap at n^0.55 or pi*sigma_n | Both lemma intervals include n^0.55; Lemma 5 includes its upper endpoint. |
| Even q, especially q=2 | The j=q/2 term occurs once and lies at pi*sigma_n. The factor two merely overcounts it. |
| Odd/composite q | Each j_*<q/2 occurs exactly twice; no arithmetic assumption is used. |
| Negative frequencies | Reduction uses signed r_j, followed by characteristic-function conjugacy. |
| Nonintegral mean | Centering is used only after reducing the integer T_n, with the phase retained. |
| Bounded or oscillating q | The same inequality applies pointwise and q=1 is exact. |
| Arbitrarily slow sigma_n/q growth | Only d_n>=1 is needed to invoke (2); convergence is the power (q/sigma_n)^(1+delta), with no extra log n factor. |
| Moving p or p=0,1 | Outside the fixed-p claim; neither uniformity nor nonzero variance is available from this argument there. |

The verification script enumerates all graphs for n=3,4,5,6 at p=1/2 and p=2/5: 67728 graph states in total. Integer weights and rational arithmetic check the mean, the variance, and the linear/remainder variance identity below exactly. Fourier identities are then checked numerically for q=1,...,40 and all residues (320 cases, 6560 residues). The maximum filter error was 1.066e-14, below the 1e-10 tolerance; centered-magnitude reduction error was 4.45e-16. A deliberately wrong centered-periodicity invariant fails with gap about 0.3994. These finite checks can expose normalization and algebra errors. They neither prove the asymptotic lemma nor certify its unknown constants.

## Necessity and its historical limit

Necessity does not require a new LLT. Here is a checkable independent classical route. Put Y_e=X_e-p. Expanding the triangle polynomial gives T_n-mu_n=L_n+R_n, where

\[
L_n=(n-2)p^2\sum_eY_e.
\]

The remainder consists of degree-two and degree-three monomials in distinct Y_e. Different edge-set monomials are orthogonal: an edge in their symmetric difference occurs to the first power and has mean zero. Thus

\[
\operatorname{Var}L_n=\binom n2(n-2)^2p^5(1-p),\qquad
\operatorname{Var}R_n=\binom n3p^3(1-p)^2(1+2p)=O_p(n^3).
\]

The degree-two count is 3binom(n,3), each with coefficient p; the degree-three count is binom(n,3), each with coefficient 1. Equations (3) and these identities show Var R_n/sigma_n^2->0 and Var L_n/sigma_n^2->1. The ordinary binomial CLT for the independent edge sum and Chebyshev therefore give Z_n=(T_n-mu_n)/sigma_n => N(0,1).

For q>=2 let P_a=Pr(T_n equiv a mod q). Since the first Fourier coefficient of the uniform residue distribution is zero,

\[
\left|\mathbb E e^{2\pi iT_n/q}\right|
=\left|\sum_a(P_a-1/q)e^{2\pi ia/q}\right|
\le \sum_a|P_a-1/q|\le\Delta_n(q).
\tag{6}
\]

If q_n/sigma_n fails to tend to zero, take a subsequence with q_n/sigma_n>=epsilon>0. On a further subsequence t_n=2*pi*sigma_n/q_n tends to some t in [0,2*pi/epsilon]. Because E|Z_n|<=1,

\[
|\psi_n(t_n)-\psi_n(t)|\le |t_n-t|.
\]

The CLT implies |psi_n(t_n)|->exp(-t^2/2)>0, contradicting (6) if Delta_n(q_n)->0. This covers the possibility q_n/sigma_n->infinity as t=0, and all nonconvergent ratios by subsequences. Consequently the sharp equivalence follows from the old characteristic bounds plus the elementary CLT.

The scale obstruction was already printed in [Alex Scott's 2009 Oberwolfach report, joint work with Atsushi Tateno](https://ems.press/content/serial-article-files/46223), printed p.1279 (PDF p.55). Its displayed Theorem 2 states the smaller sufficiency range q=o(n^2/log n). I independently inspected the primary page; I do not transfer priority for the full modular corollary to that announcement or to Gilmer-Kopparty without a printed passage establishing it.

## Research and priority assessment

The target document's direct Fourier deduction is valid. It is a materially different short implication from a pointwise-LLT/finite-window/Gaussian-mesh deduction: it samples a summable characteristic envelope directly and uses no local mass approximation or tail truncation. That distinction does not create a new deep LLT or analytic mechanism. This particular assembly is dated 2026-10-17, while its decisive inputs are old.

This review supports describing sharp fixed-p triangle modular sufficiency as an implication of the 2014 lemmas. It does not support a claim that the full corollary was explicitly stated there, that a present manuscript is the first to observe it, or that the sharp threshold is a new research discovery. The remaining limitation is reliance on the published deep analytic lemmas, whose full conditioning proofs have not been independently verified here; no unsupported replacement lemma was introduced.
