# Dynamic Monge–Kantorovich convergence: partial mathematical audit

Problem identifier: 30003937. Source question: OWR-16414-001, Mario Putti's contribution, printed pp. 2398–2400 of Oberwolfach Report 39/2018, https://doi.org/10.4171/owr/2018/39.

This is the explicitly corrected audit derivative of the preserved frozen_v1 packet (source-free ZIP SHA-256 c88c89e69795002ca9c12cc6c8212587d9853c9a1fc58431cd21fbfe37119b3f). The corrections qualify an imported local-restart dependency and make several hypotheses explicit. They do not add a sixth proof-search approach or change the unresolved disposition.

## Disposition

The unrestricted continuum beta=1 convergence target remains unresolved by this work. Five distinct substantive approaches were completed; the allotted search is exhausted. No complete candidate proof, positive-initial-density counterexample, verified later resolution, or novelty claim is supplied.

The exact system is

    −div(μ∇u)=f,      μ_t=μ(|∇u|−1),
    μ(0)=μ₀>0,       μ∂ₙu=0,       ∫u=0.

The analytic scope is the referenced local theory: a bounded smooth convex domain, bounded mean-zero forcing (compactly supported for the source setting), and strictly positive Hölder initial density. The OWR source does not specify a convergence topology or a unique potential. Neither omission is used as a negative resolution.

## Results and limits

1. `conditional_entropy.md`: for an existing regular trajectory and a feasible optimal comparator, H'≤C−S−R and 0≤S(t)−C≤H₀/t throughout its interval of existence. If the trajectory is global, its energy converges to the optimal value. Weak-measure density convergence additionally requires the stated unique-minimizer theorem on the precise compact measure space. Weighted potential convergence does not imply unweighted potential convergence.
2. `continuation.md`: finite-time loss of a positive lower bound cannot cause the first breakdown. A uniform Hölder norm yields a positive C^δ endpoint; continuation additionally assumes a valid local restart theorem in that class. The inspected preprint's claimed C^δ-Lipschitz flux proof uses a generic modulus estimate that is false, so this audit does not independently certify that restart theorem. Energy, mass, and even uniform ellipticity do not control that norm, as an explicit sequence of exact elliptic states shows.
3. `variational_route.md`: an exact convex nonlinear dissipation representation of the reaction law, and a rigorous frozen bounded-state variational step. Global iteration, spatial compactness, and nonlinear identification remain unproved. A weak-limit elliptic example rules out a naive product passage.
4. `fixed_flux_cases.md`: global explicit solutions and exponential Hölder density convergence on an interval and for radial data on a ball. Mean-zero potentials converge uniformly and in W^(1,p) for every finite p. These remain separately identified special cases.
5. `potential_selection.md`: an explicit nonconvergent, nongauge mean-zero potential family with stationary optimal density in the enlarged class allowing zero initial conductivity. The strict-positivity hypothesis excludes this example from the original target. It illustrates a genuine selection difficulty in the degenerate limiting system.

## Imported mathematics and attribution

The original DMK papers state local well-posedness, elliptic-map estimates, positivity, and energy identities. The source-proof caveat in `continuation.md` prevents this audit from independently certifying the reported C^δ local-restart argument. The entropy calculation only assumes an existing regular trajectory; the fixed-flux formulas directly construct their trajectories. Optimal-transport duality and transport-density uniqueness are imported where expressly assumed; they are not reproved or silently extended to boundary measures. Finite-dimensional entropy arguments precede this work. The 2022 transport-energy metric flow and the 2023 variational FEM scheme are not automatically the original continuum reaction flow. The source audit records these distinctions and the inspected manuscript versions.

## Verification limits

The written derivations are the mathematical artifacts. The accompanying standard-library checker performs exact bounded rational and polynomial regression checks for the algebra and explicit constructions, plus integrity and read-only tests. Those computations do not prove a PDE existence, compactness, or unrestricted convergence theorem. Independent mathematical review is still required before relying on any partial lemma.

The public packet contains authored analysis, check code, and bibliographic/hash metadata only. It contains no third-party PDF/text bodies, source dataset contents, or private coordination material.
