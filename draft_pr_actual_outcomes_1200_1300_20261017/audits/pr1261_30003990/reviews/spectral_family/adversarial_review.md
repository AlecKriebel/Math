# Internal adversarial audit before sealing

This is a self-audit of the isolated family mechanism, not independent cross-family verification. No other family or candidate was consulted. The parent workflow must provide the separate independent adversarial review before promotion.

1. **Could the whole claim be hidden inside the endpoint import?** The imported theorem concerns Christoffel functions under full local interval doubling, a genuinely standard approximation-theory hypothesis. The hard geometry is checked explicitly by central projection and polar integration. The endpoint bound is independently derived using a cardinal polynomial and a shell-to-endpoint mass comparison. No endpoint-zero conjecture is left unverified.

2. **Does endpoint cumulative volume imply the needed doubling?** No. The spike construction in report Section 7 disproves this inference. The successful route separately proves pairwise density inequalities and then checks every interval I with 2I inside the local interval. The anchored-only route is marked blocked.

3. **Could the central projection miss small-level points?** No: h(x)>=b||x||^2 forces all small-level points into a small Euclidean neighborhood, while a dot x>=0 gives 0<=u<=t/A. The explicit inverse projection therefore has uniformly small z. Positivity of G_u on this full neighborhood proves h(0,z)<=h(u,z), so all points are covered by the graph used in the density formula.

4. **Is moving along a level graph assumed to stay inside K?** The proof instead moves along the straight segment to a fixed interior e. Keeping the central-projection coordinate z fixed parametrizes exactly that segment. The level-t point has parameter u_t>=u_s and u_t<1, so it lies on the segment. This is the precise use of convexity.

5. **Is there an omitted coarea curvature factor?** The complete change-of-variable factor is (A/||a||)(1-u)^(n-1)/G_u. It includes both the central-projection volume Jacobian and the inverse derivative in the level parameter. Uniform bounds are taken on the entire required coordinate neighborhood.

6. **Does the origin-polar inequality have the right sign?** For alpha>=0, s/t=(R_s/R_t)(alpha+bR_s)/(alpha+bR_t)<=R_s/R_t. The denominator in the polar density is larger at t than at s. These two facts give w(s)>=(s/t)^(n-1)w(t), hence the required upper growth at increasing t. There is no use of negative alpha: first-order optimality excludes it on every active ray.

7. **Could the angular domain or boundary be nonsmooth or nonsimple?** Only measurable domains and their inclusion are used. Convexity supplies a positive solid-angle interior cone in the zero-gradient case. A square-pyramid apex with four rays in dimension three was also checked numerically. Boundary smoothness is absent from all analytic hypotheses.

8. **Could the density formulas disagree at exceptional levels?** Each is a legitimate Lebesgue-density version. Equalities and pairwise comparisons can be taken on their common full-measure set; changing exceptional values does not change any interval measure or subsequent argument. No atom occurs because the nonconstant quadratic has level sets of n-dimensional Lebesgue measure zero.

9. **Are degree and Gaussian quadrature indexing correct?** A degree-N orthogonal zero couples to lambda_(N-1), via exact Gaussian quadrature for ell_1^2 of degree 2N-2. The spectral trial p has degree m=floor(r/2), so p(h)^2 has degree 4m<=2r. Every coefficient can be real, and the positive normalization factor gives a global SOS.

10. **Does a local endpoint suffice?** It would not. Here 0 is the global left support endpoint because h>=0 on all of K; its zero is uniquely at 0. The smallest orthogonal zero tends to this endpoint by a separate Rayleigh test, so the Christoffel theorem is applied only after its local evaluation hypothesis holds.

11. **Can stationary or nonunique minimizers break the argument?** Stationary minimizers use the separate power-density case. Nonunique minimizers of f are allowed because the chosen positive quadratic term isolates one minimizer for h. Constants are permitted to deteriorate for objectives whose nonzero gradients approach zero.

12. **Can numerical stability manufacture the evidence?** The calculations do not use ill-conditioned monomial moment matrices. They use full reorthogonalization and compare two quadrature resolutions, with independent direct-domain moment integrals. They remain floating-point evidence; the proof is analytic and does not depend on numerical asymptotics.

Outcome: no internal counterexample or logical gap identified, conditional on the explicitly inspected standard Christoffel theorem. The full source-question upper-rate mechanism is complete. Independent external-to-this-family review and priority clearance remain unperformed and must not be implied by this audit.
