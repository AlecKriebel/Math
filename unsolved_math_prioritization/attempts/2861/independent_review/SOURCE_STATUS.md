# 2861 / KP-3.63: a published geometric method for the Dirac eta invariant

**Status:** credited known-method/source correction; independent review pending. No discovery or new uniform certified algorithm is claimed. The literal request for a computation method is addressed by Lin–Lipnowski's 2021 preprint, published in JEMS in 2025 (online 2024). A stronger, uniformly terminating arbitrary-precision algorithm from an arbitrary triangulation is not certified here.

## 1. Exact question and source repair

[K3, Problem 3.63, printed pp. 176–177](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf) asks for a method to compute the Dirac eta invariant associated with a spin structure on a hyperbolic three-manifold. The remarks specify a closed, oriented manifold with its hyperbolic metric. The target is the real APS eta invariant, rather than merely its residue modulo integers or a reduced eta invariant.

Francesco Lin and Michael Lipnowski, [*Closed geodesics and Frøyshov invariants of hyperbolic three-manifolds*](https://ems.press/journals/jems/articles/14297701), J. Eur. Math. Soc. **27** (2025), 4201–4281, DOI 10.4171/JEMS/1452, provide the required geometric method. The full [published article](https://ems.press/content/serial-article-files/51185) is the source used below. It first appeared as [arXiv:2105.04675](https://arxiv.org/abs/2105.04675) on 10 May 2021. Its introduction, p. 4206, explicitly describes applicability in principle to any hyperbolic three-manifold, while warning about practical feasibility. The relevant ingredients are the spin-lift computation in §2, the odd spinor trace formula (Theorem 3.3), and the eta formula in §4, including p. 4226's treatment of a nonzero kernel.

Their Floer-theoretic applications impose rational-homology-sphere and minimal-L-space hypotheses. These restrictions are not hypotheses of the spin trace formula: Appendix C.2 starts with an arbitrary closed hyperbolic three-manifold group and its lift, and Appendix D treats Gaussian test functions in that generality. Setting the twisting character to zero gives the spin operator for any specified spin structure, regardless of the first Betti number.

The K3 remark that only symmetry-forced zero examples are known is outdated. Lin–Lipnowski give the nonzero value approximately 0.989992 for the unique spin structure on the Weeks manifold, with the explicitly stated accuracy caveat that their number inherits the accuracy of the odd-signature eta computation in Snap. This package does not independently certify those decimal digits.

## 2. Data and normalization

Write the oriented manifold as $Y=\Gamma\backslash\mathbb H^3$, and represent the specified spin structure by a lift

$$\rho_s:\Gamma\longrightarrow\mathrm{SL}_2(\mathbb C)$$

of its orientation-preserving holonomy. The raw invariant is

$$\eta(D_s)=\left.\sum_{\lambda\ne0}\operatorname{sgn}(\lambda)|\lambda|^{-z}\right|_{z=0},$$

where continuation from $\operatorname{Re}z>3$ is understood and eigenvalues have multiplicity. It is not $(\eta+\dim\ker D_s)/2$.

For each nontrivial conjugacy class $[\gamma]$ in $\Gamma$, let $\ell_\gamma>0$ be its length and $\ell_{\gamma,0}$ its primitive length. Thus $\ell_\gamma=m\ell_{\gamma,0}$ for its positive multiplicity $m$. Choose the expanding eigenvalue of $\rho_s(\gamma)$ and write it as

$$\exp(\ell_\gamma/2+i\theta_\gamma),\qquad \theta_\gamma\in\mathbb R/2\pi\mathbb Z.$$

The ordinary rotational holonomy is $2\theta_\gamma$ modulo $2\pi$. Define

$$d_\gamma=|1-e^{\ell_\gamma+2i\theta_\gamma}|\,|1-e^{-\ell_\gamma-2i\theta_\gamma}|
=2(\cosh\ell_\gamma-\cos2\theta_\gamma).$$

All sums below use precisely the nontrivial group-conjugacy-class convention in the published trace formula, including all iterates. In particular, one must not combine inverse classes into unoriented geodesics or discard iterates without adjusting multiplicities.

## 3. The published formula in Gaussian form

For every $L>0$, the spin specialization of Lin–Lipnowski's formula (14) gives

$$\boxed{\displaystyle
\eta(D_s)=-\frac2\pi\sum_{[\gamma]\ne1}
\frac{\ell_{\gamma,0}}{\ell_\gamma}
\frac{\sin\theta_\gamma}{d_\gamma}
 e^{-\ell_\gamma^2/(2L^2)}
+\sum_{\lambda\ne0}\operatorname{sgn}(\lambda)
\operatorname{erfc}\!\left(\frac{L|\lambda|}{\sqrt2}\right).}\tag{1}$$

Both sums converge absolutely. Here is a normalization check, not a new trace-formula proof. Use $G(x)=e^{-x^2/2}$ and the Fourier convention $\widehat G(t)=\int G(x)e^{-itx}\,dx=\sqrt{2\pi}e^{-t^2/2}$. In the source's notation,

$$G_T=\sum_\lambda T\lambda\widehat G(T\lambda)
=2\sum_{[\gamma]\ne1}\ell_{\gamma,0}\frac{\sin\theta_\gamma}{d_\gamma}
\frac1T G'(\ell_\gamma/T).$$

The denominator of (14) is $\int_0^\infty\widehat G(t)\,dt=\pi$. Its geometric integral is

$$\int_0^L\frac1T G'(\ell/T)\frac{dT}{T}=-\frac1\ell e^{-\ell^2/(2L^2)},$$

and each nonzero spectral term in the other integral, after division by $\pi$, is $\operatorname{sgn}(\lambda)\operatorname{erfc}(L|\lambda|/\sqrt2)$. These calculations yield (1). A zero eigenvalue contributes zero to $G_T$ and to the defining eta series; the source expressly checks this. No invertibility assumption or hidden half-kernel correction is required.

## 4. A convergent finite geometric approximation

For completeness, the following elementary consequence makes explicit what the formula computes without retaining an unknown spectrum in its limiting expression. For positive integers $n$, set

$$A_n=-\frac2\pi\sum_{0<\ell_\gamma<4n^2}
\frac{\ell_{\gamma,0}}{\ell_\gamma}
\frac{\sin\theta_\gamma}{d_\gamma}
 e^{-\ell_\gamma^2/(2n^2)}.\tag{2}$$

Then $A_n\to\eta(D_s)$ for every fixed closed oriented spin hyperbolic three-manifold. This is a direct convergence consequence of the published trace formula, not a claim of a new computational technique.

**Spectral remainder.** For $L\ge1$, each summand in absolute value in the second sum of (1) is at most $\operatorname{erfc}(|\lambda|/\sqrt2)$. The Weyl bound $\#\{|\lambda|\le t\}=O_Y(1+t^3)$ and Gaussian decay make these bounds summable. Every nonzero eigenvalue has $\operatorname{erfc}(L|\lambda|/\sqrt2)\to0$, so dominated convergence makes the whole spectral remainder tend to zero. This argument also allows a kernel.

**Geometric remainder.** Let $a>0$ be a lower bound for the systole. There is a constant $C$ such that the number of nontrivial conjugacy classes with length at most $x$ is at most $Ce^{2x}$. One elementary choice follows from a Dirichlet domain contained in $B(o,D)$ and disjoint orbit balls $B(\gamma o,r)$: every class of length at most $x$ has a representative displacing $o$ by at most $x+2D$, hence

$$C=\frac{\pi e^{4D+2r}}{2\operatorname{Vol}(B(r))},\qquad
\operatorname{Vol}(B(r))=\pi(\sinh(2r)-2r)$$

suffices by packing. Distinct classes use distinct representatives. Moreover

$$d_\gamma\ge e^{\ell_\gamma}(1-e^{-a})^2,\qquad
0<\ell_{\gamma,0}/\ell_\gamma\le1.$$

Grouping the omitted classes into intervals $[k,k+1)$, for integer $R$ the absolute omitted geometric contribution at $L=n$ is bounded by

$$\frac{2Ce^2}{\pi(1-e^{-a})^2}
\sum_{k\ge R}\exp\left(k-\frac{k^2}{2n^2}\right).$$

For $R=4n^2$, the first term is $e^{-4n^2}$ and successive-term ratios are at most $e^{-3}$. Thus the omitted geometric contribution is at most

$$\frac{2Ce^2}{\pi(1-e^{-a})^2(1-e^{-3})}e^{-4n^2}.$$

Combining this bound with the spectral remainder proves (2).

## 5. What the computation method does and does not certify

Section 2.2 of the published paper describes how to compute spin-refined lengths from a Dirichlet domain, face-pairing matrices, and representatives of conjugacy classes up to a length cutoff. A lift can be found by choosing signs of generator lifts to satisfy the relations; these sign equations are linear over $\mathbb F_2$. The specified spin structure chooses one lift among the twists by $H^1(Y;\mathbb Z/2)$. Word evaluation in the lift determines the expanding eigenvalue and its half-angle. The finite-first-homology simplification used for enumerating all torsion spin-c characters is unnecessary when computing one genuine spin structure.

Equations (1)–(2) are an all-manifold geometric method. Practical rigorous bounds use the explicit local Weyl estimates of §5, estimates for omitted geodesics, and enough information about the small signed Dirac spectrum. For example, if a positive lower bound $\delta$ for the absolute values of all *nonzero* eigenvalues is certified, local spectral counts and the complementary error function give a quantitative bound on the spectral remainder. A finite-dimensional kernel itself is harmless in (1), but certifying where the nonzero spectrum starts can be difficult.

A convergent sequence alone does not supply a uniform effective stopping rule. This audit does **not** certify a general algorithm that, from every triangulation and tolerance, terminates with a rigorously certified error bound, resolves all kernel questions, and certifies all floating-point geometric input. It also does not claim a finite closed-form answer, an efficient implementation, or a noncompact/cusped extension. If the intended target is strengthened to such a uniform certified algorithm, that stronger target remains outside this package. For the literal K3 request for a method, the credited published work is the appropriate source correction.

## 6. Validation and attribution

Run `python verify.py` in this directory. The deterministic checks test the Gaussian constants, denominator identity, iterate factors, spin-lift sign dependence, and geometric-tail algebra. They are small consistency checks, not a replacement for the analytic trace theorem or an implementation on a hyperbolic manifold. The trace theorem and computation method are credited to Lin–Lipnowski; no campaign priority claim is made.
