# Turn 5: higher-step shared-rate dynamics and the remaining obstruction

Started 2026-10-01 06:25 UTC. The final substantive author turn targets global dynamics of the shared-rate Lck-only family, without substituting the arbitrary-rate bistable witness.

## Exact failure of the one-step cooperative mechanism

Retain free receptor r and every C_i,B_i, eliminate free ligand by m=r+Delta and free enzyme by e=Etot−sum B_i. At an interior point with N≥2, the Jacobian has the directed cycle

B0 → C1 → B1 → B0.

The three derivatives are respectively w+u*C1>0, u*e>0, and −u*C0<0. Their product is strictly negative. Any coordinatewise sign change multiplies the cycle product by the square of a product of signs, preserving its negativity. A Metzler matrix has nonnegative cycle products. Thus no orthant sign change can turn this Jacobian into a cooperative one. This is an exact obstruction to the specific one-step proof route, not a proof against convergence or against a more general cone.

The Jacobian still has zero column sums because r+sum C_i+sum B_i is conserved. However, every bound-enzyme column B_j has a negative off-diagonal entry in another B_i row. Its ordinary induced l1 logarithmic norm therefore has a positive column value: the absolute off-diagonal sum exceeds the unsigned sum by twice the magnitude of those negative terms. Consequently the ordinary stochastic-transition contraction proof also fails to extend directly. A different metric, order cone or Lyapunov function would need a new argument.

## Bounded stability investigation

A locally authored diagnostic scanned 448 exactly parametrized equilibria of the shared-rate family across N=2,3,4,6,10,20,30. For each choice of positive shared rates and free pools, the geometric equilibrium formula sets the conserved totals and ligand-binding rate, so the point tested is an actual equilibrium up to floating arithmetic. No eigenvalue with positive real part above the stated scale threshold was found. The complete parameter exponents and diagnostic results are in shared_stability_scan.json.

This is not a proof of local stability for all parameters, a proof excluding Hopf bifurcations, or any evidence sufficient for global convergence. Floating eigenvalues can be unreliable in stiff regimes, and a stable unique equilibrium would not by itself exclude other invariant sets. The scan is preserved solely as a bounded failed search for a counterexample to guide subsequent work.

## Final exact gap

The shared-rate equilibrium uniqueness theorem of turn 4 does not supply a global attractor theorem. No suitable higher-step contraction, Lyapunov function, or rigorous nonconvergent solution has been obtained. Including ZAP-70 introduces protected states and additional conservation/association reactions, and no dynamical conclusion is transferred to that network. The original OWR paragraph leaves its strongest simplifying assumptions implicit; the precise Lck-only subfamily and the original calibrated core must remain distinguished.

The five-turn original bundle is therefore unresolved. The single-step global convergence, arbitrary-N scalar reduction, exact arbitrary-rate two-step bistability and shared-rate equilibrium uniqueness are separately scoped partial artifacts. All additional claims require independent review before publication. No discovery or clinical claim is made.
