# Scope and normalization after independent review

## Precise claim

The claimed negative resolution concerns universal preservation of **total-space** positivity by Naumann's published defining equation (13), for the weight \(\phi\) of a metric on \(\mathcal O_E(r)\), with both the Monge–Ampère volume and the anticanonical volume normalized to probability measures.

The source already defines this flow. The catalogue's shorter construction question therefore omits the substantive remaining issue, which is stated at the end of the 2017 report contribution and again in the published article, Section 3.3. The [proof](public/PROOF.md) addresses that positivity question, with a smooth positive metric on \(\mathcal O_E(1)\) and its \(r\)-th power as initial data.

The source's finite-time smooth-existence theorem, including smooth dependence on the base, is the analytic input. The construction does not rely on infinite-time convergence or horizontal regularity of a limit. It is not a claim about the Griffiths conjecture or historical priority.

## Direct equation and a stationary-product test

For fiber dimension one, compatible frames give

\[
\phi_t=\log(\phi_{z\bar z})+\phi+
\log\int e^{-\phi}dA_z+C.
\]

The coefficient of \(\phi\) is one. Constants in the curvature convention or fixed fiber volume change only \(C\).

The independently checked positive product weight

\[
\phi_{\mathrm{prod}}=2\log(1+|s|^2)+2\log(1+|z|^2)
\]

on \(\mathcal O(2,2)\) is stationary under equation (13), because the two probability measures coincide on every fiber. At \(s=0\), its geodesic curvature is \(c=2\), its fiber Laplacian and Kodaira–Spencer terms vanish, and

\[
\partial_s\partial_{\bar s}\log\int e^{-\phi_{\mathrm{prod}}}dA_z=-2.
\]

Thus a literal reading of the published equation (14), with the same metric and time conventions and its displayed \(r c\) term, gives \(2\cdot2-2=2\), whereas stationarity requires zero. This contradiction does not depend on the counterexample or a Laplacian-sign convention. It establishes a convention discrepancy without asserting an unsupported editorial or typographical explanation.

## A possible root-metric and time convention

If instead \(\psi=\phi/r\) is the root-metric weight and \(\tau=t/r\), the scalar flow becomes

\[
\psi_\tau=\log\psi_{z\bar z}+r\psi+
\log\int e^{-r\psi}dA_z+C'.
\]

This simultaneous change explains how a reaction term with coefficient \(r\) can occur. With the original time, all terms of this root-weight equation must be divided by \(r\). No undocumented intended convention is attributed to the source.

The proof uses the explicit defining equation (13) and differentiates it directly. The [full independent audit, Section 2](audit/ADVERSARIAL_AUDIT.md#2-defining-equation-normalization-and-the-printed-evolution-equation), supplies the stationary-product and rescaling checks. Positive scalar rescaling of curvature and positive reparameterization of time preserve the fact of positivity loss, although its numerical time and coefficient must then be translated.

## Reviewed outcome

For \(E=\mathcal O(1)\oplus\mathcal O(1)\) and the initial metric in the frozen proof, the exact horizontal curvature is

\[
c(0,0,t)=\frac1{96}-\frac{1-e^{-2t}}{24}.
\]

It equals \(-1/96\) at \(t=(\log2)/2\). The initial metric is strictly positive everywhere on the compact product; its universal normalized Hessian determinant bound is \(1/64+(159/32)p>0\). These facts and the precise source normalization passed independent adversarial review.
