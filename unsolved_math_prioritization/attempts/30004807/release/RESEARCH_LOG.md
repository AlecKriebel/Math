# Research record

## Status

One substantive construction attempt produced a complete counterexample to the literal regular-ZAS conjecture under the primary paper's boundary-test convention. The five-attempt budget was therefore stopped early. The construction and its verification are separated below from previously known results. Independent adversarial audit is required before treating this candidate as publication-cleared.

## Primary-source reconstruction

The report's conjecture spans the transition from printed p. 2232 to p. 2233. The first page supplies the admissible geometry, while the second explicitly supplies the universal conjecture. The technical paper supplies the boundary-reaching test class. The regular-ZAS definitions were checked against Bray–Jauregui rather than inferred solely from the catalogue.

## Attempt 1: preserve the ZAS slices and vary the lapse

A regular ZAS constrains the spatial metric but does not determine the spacetime lapse. Start with the negative-mass Schwarzschild spatial metric (h=(1-a/\rho)^4\delta).

1. The ultrastatic choice (N=1) has radial Einstein-flux density (4a/\rho), with nonzero limit at the inner boundary. Its full contracted density is integrable, although separately integrating connection summands is not legitimate.
2. To ensure that the example is not merely a bounded-lapse anomaly, use (N=A+B(\rho+a)/(\rho-a)). The static vacuum Hessian identity gives (G^i{}_j=(A/N)\operatorname{Ric}(h)^i{}_j). The source-weighted radial flux is (4Aa/\rho).
3. Normalize (A=B=1/2). Then (N=(1-a/\rho)^{-1}\), the metric is asymptotically flat, the lapse has the same inverse-linear blow-up order as the known vacuum geometry, and a normalized smooth radial test gives the exact integral (-8\pi).
4. Verify the full test space in Cartesian coordinates. The weighted Einstein tensor has a smooth, divergence-free exterior density and a nonzero boundary normal trace. This proves absolute integrability for every source-convention test, not merely a principal-value cancellation for the chosen radial field.

The construction meets the regularity, negative mass, timelike character and curvature-singularity requirements. The counterexample refutes the homogeneous identity. It actually admits an explicit inhomogeneous boundary identity, rather than failing merely because the integral is undefined.

## Independent checks within the construction

- Direct four-dimensional Christoffel-to-Ricci computation for the selected metric reproduces all sixteen mixed Einstein components and scalar curvature zero.
- A three-dimensional conformal calculation plus the static warped-product identities gives the entire lapse family independently.
- The radial test contraction is evaluated explicitly before integration and yields a bounded coordinate density.
- The Cartesian density computation checks absolute convergence for all smooth boundary tests and the exact boundary-functional coefficient.
- The area-radius transformation verifies the negative-mass Schwarzschild spatial metric and mass normalization.
- The vacuum-lapse endpoint is a negative control: its Einstein tensor and defect vanish.

The symbolic checks are modest exact algebra. They do not establish geometric admissibility or a test convention by themselves; those are proved in the manuscript.

## Prior results, not claimed as new

The regular-ZAS resolution and mass definition, the negative-mass Schwarzschild spatial metric, the static-vacuum lapse, the static warped-product curvature formulas, and BKTZ's weak Bianchi sufficient theorem are established background. The construction uses these to exhibit a nonzero boundary defect while keeping the same regular ZAS slices.

## Claim boundary and remaining questions

No claim is made to classify all metrics with a weak Bianchi identity, to supply a charged-particle evolution theory, to refute a matter-restricted conjecture, or to identify a canonical tensor-distribution extension across a collapsed singular worldline. The example violates the null energy condition. Within the stated one-parameter lapse family, however, the homogeneous identity holds exactly at the vacuum endpoint (A=0).

Historical priority remains unestablished. The original sources and a bounded duplicate/literature search are recorded in `SOURCE_GATE.md`.
