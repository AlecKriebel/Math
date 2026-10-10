# Verification note: Euler and polygonal constructions have the same limit

Accepted source-applicability note after independent AI mathematical audit, 10 October 2026. This note checks the canonical-area applicability of the existing convergence input; it is not an additional lower-bound argument. The rough-range proof and all-H corollary remain unchanged.

The inspected arXiv version of Neuenkirch–Tindel–Unterberger defines its area through analytic approximation. Its Theorem 1.1 establishes that the left sums
\[
 L_m=\sum_{k=0}^{m-1}B^1_{kT/m}(B^2_{(k+1)T/m}-B^2_{kT/m})
\]
converge in (L^2) to that area for every (H\in(1/4,1)), with the Brownian computation given immediately afterward. The canonical iterated integral is conventionally the limit of the integrals of piecewise linear path interpolations. The following elementary calculation verifies that these are the same limit, so the convention in the companion proof is justified without equating two constructions by name alone.

Put (\delta=T/m) and (\Delta_kB^i=B^i_{(k+1)\delta}-B^i_{k\delta}). The classical integral of the polygonal interpolations is exactly
\[
 P_m=L_m+Q_m,\qquad Q_m=\frac12\sum_{k=0}^{m-1}\Delta_kB^1\Delta_kB^2.
\]
The two components are independent, and each has increment covariance
\[
 E[\Delta_jB^i\Delta_kB^i]=\delta^{2H}\rho_H(j-k),\quad
 \rho_H(r)=\frac12\bigl(|r+1|^{2H}+|r-1|^{2H}-2|r|^{2H}\bigr).
\]
Consequently
\[
 E[Q_m]=0,\quad E[Q_m^2]=\frac{\delta^{4H}}4
 \sum_{j,k=0}^{m-1}\rho_H(j-k)^2
 =\frac{\delta^{4H}}4\left[m+2\sum_{r=1}^{m-1}(m-r)\rho_H(r)^2\right].
\]
For (r\ge2), the second-difference formula (or Taylor's theorem) gives
\(|\rho_H(r)|\le C_Hr^{2H-2}\). This includes (H=1/2), where the nonzero-lag values are exactly zero. The finite lag (r=1) is harmless. Summing the resulting powers gives
\[
 E[Q_m^2]\le C_HT^{4H}\begin{cases}
 m^{1-4H},&1/4<H<3/4,\\
 m^{-2}(1+\log m),&H=3/4,\\
 m^{-2},&3/4<H<1.
 \end{cases}
\]
All three expressions tend to zero. Hence (\|P_m-L_m\|_2\to0). Because (L_m) converges in (L^2), (P_m) converges to the same limit, including along the dyadic interpolations used to define the canonical lift. This verifies the exact target convention. At (H=1/2), the independent-component Itô and Stratonovich iterated integrals coincide.

The same calculation also shows why replacing the target by an antisymmetric-area variable is unnecessary. We identify the actual polygonal integral (int B^{1,(m)}\,dB^{2,(m)}), with its one-half diagonal correction, and pass to its limit.

Primary reference: A. Neuenkirch, S. Tindel and J. Unterberger, *Discretizing the fractional Lévy area*, [arXiv:0902.0497](https://arxiv.org/abs/0902.0497), Theorem 1.1, p. 3; journal DOI [10.1016/j.spa.2009.10.007](https://doi.org/10.1016/j.spa.2009.10.007). The original target is OWR41/2012 pp.2524–2525, DOI [10.4171/owr/2012/41](https://doi.org/10.4171/owr/2012/41).
