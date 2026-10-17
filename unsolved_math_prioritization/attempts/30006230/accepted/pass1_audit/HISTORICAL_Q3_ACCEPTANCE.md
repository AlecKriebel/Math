# Independent acceptance: historical Q=3 with a positive potential

14 October 2026. Additional audit within the same shared PASS1. Exact audited bytes are recorded in `HISTORICAL_Q3_AUDIT_MANIFEST.json`; earlier accepted proofs remain separately pinned.

**PASS.** The proposed remainder-free Hardy–Rellich necessity statement fails in the historical dimension \(Q=3\) even with \(V>0\), \(W>0\), and \(S_3[V]>0\). The exact example is
\[
R=1,\qquad V=r^{3/4},\qquad W=\lambda r^{3/4},
\qquad S_3[V]=\tfrac7{16}r^{-5/4},
\]
where \(\lambda\) is the exact variational constant in the proof, not a numerical approximation. It satisfies the complete original all-test core, with the announced extended-energy convention, while the coefficient-one full-interval Bessel property fails.

## 1. Variational and endpoint checks

The norm \(q_0[w]=\int_0^1r^{11/4}w'^2\) controls \((49/64)\int r^{3/4}w^2\) by the exact weighted Hardy square. Thus its completion is a function space, controls local \(H^1\), and embeds compactly into the target weighted space \(N[w]=\int r^{11/4}w^2\): the near-zero tail is bounded by \((64/49)\delta^2q_0\), while the remaining compact interval has the usual compact inclusion.

The mean is the actual Lebesgue integral, not merely a formal continuous functional. The estimate
\[
\int_0^1|w|\le\int_0^1r|w'|\le2q_0[w]^{1/2}
\]
proves this identification in the completion. Both the unrestricted and mean-zero Rayleigh minima are attained. A nonnegative unrestricted minimizer is strictly positive on the entire interior by ODE uniqueness; every unrestricted minimizer has constant strict sign. Hence an attained mean-zero minimizer cannot attain the same value, proving the strict gap \(\beta>\alpha>0\).

The trial \(1-r^2\) belongs to the completion: the zero-end cutoff costs \(O(\varepsilon^{7/4})\) and the right-end cutoff costs \(O(\varepsilon)\). Its exact quotient is \(465/32<16\). Therefore
\[
\lambda=(\alpha+\min\{\beta,16\})/2
\]
is strictly between the two thresholds and below 16. The form \(q_\lambda=q_0-\lambda N\) is nonnegative on every derivative of a compact radial test and negative on an approximable unrestricted minimizer. Approximation gives an actual negative compact test. The compact-support ground-state identity rules out any positive coefficient-one Bessel solution on \((0,1)\), with no endpoint condition imposed on that hypothetical solution.

## 2. Independent verification of the historical angular basis

The proof does not import a source statement restricted to \(n\ge2\). For the two sheets \(x=\pm r\sqrt{\sin\varphi}\), the angular measure is \(\sin^{1/2}\varphi\,d\varphi\) and the angular operator is
\[
\mathcal L=\partial_\varphi^2+\tfrac12\cot\varphi\,\partial_\varphi.
\]
Splitting into the even and odd sheet subspaces and using \(z=\cos\varphi\), the even sector has weight \((1-z^2)^{-1/4}\). Multiplication by \((1-z^2)^{1/4}\) is an onto isometry from the weight-\(+1/4\) space to that sector's scalar weighted space, supplying the odd basis.

For each weight, orthogonal polynomials are complete by uniform polynomial approximation and density of continuous functions for the finite measure. The symmetric polynomial operator
\[
\mathcal J_\gamma=(1-z^2)\partial_z^2-(2\gamma+2)z\partial_z
\]
has eigenvalue \(-m(m+2\gamma+1)\) on the degree-\(m\) orthogonal polynomial. The endpoint terms vanish because \(\gamma+1>0\). Independent differentiation verifies the conjugation in the odd sector. It follows that the full two-sheet spectrum is exactly
\[
a_k=k(k+1),\quad k=0,1,\ldots,
\]
including both parities, with \(a_k\ge2\) for every nonconstant mode.

Parity of the polynomials shows that each \(r^k\Phi_k\) is a Cartesian polynomial in \(x,t\). The apparent gauge powers are multiples of four, replaced by powers of \(x^4+4t^2\); odd modes have one additional factor \(x\). These functions are Grushin-harmonic and smooth across the entire axis. This is the exact domain property needed for ambient integration by parts.

## 3. Uniform all-mode inequality

Direct expansion and integration by parts yield
\[
F_a[d]=q_\lambda[d']+a\left(2\int r^{3/4}d'^2+
(a-13/16)\int r^{-5/4}d^2-\lambda\int r^{3/4}d^2\right).
\]
All constants, including the original \(V'\) correction, were independently checked. The first term is nonnegative because \(\int d'=0\).

With \(y=r^{3/8}d\), the bracket is exactly
\[
2\int y'^2+(a-41/32)\int r^{-2}y^2-\lambda\int y^2.
\]
For every nonconstant mode \(a\ge2\), the inverse-square coefficient is at least \(23/32>0\). Ordinary Dirichlet Poincare gives a lower bound \((2\pi^2-\lambda)\int y^2>0\), since \(\lambda<16\). This is an all-size proof; no finite mode scan or Bessel-zero estimate is used. The constant mode is covered directly by the constrained form.

## 4. Full original test class, with no axis removal

Some smooth source tests in this historical dimension have infinite left energy. Their core inequality is automatic because the right side is finite on a compact supporting annulus. For a finite-energy source test, positivity and boundedness of \(V\) and \(1/V\) on that annulus give finite unweighted energy too.

The complete angular basis and its ambient-polynomial property allow the exact same ambient integration-by-parts coefficient identification used in the separately accepted current-dimensional example. Parseval gives convergence of angular partial sums in the weighted left energy and in \(\int\psi u^2\). Weighted Cauchy–Schwarz applied to the ambient energy identity then gives convergence in gradient energy. The right-side multiplier is bounded on the common annulus, so the right side converges as well. Nonnegative finite-sum differences therefore pass to every original finite-energy source test. This verifies the whole punctured-plane test class without imposing an artificial pole boundary condition.

## Scope

This acceptance resolves the explicit historical positive-potential core branch negatively, and explains why the separately accepted \(Q\ge4\) nonnegative-potential theorem cannot be extended to \(Q=3\). It does not assert an explanation for the source's later dimension change, contradict a literal theorem whose premise already contains a positive solution, or resolve every possible intended formulation of the informal source question. [Historical primary source](https://arxiv.org/pdf/2404.05510v1), [current primary source](https://arxiv.org/pdf/2404.05510v3)
