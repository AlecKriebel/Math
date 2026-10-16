# Scope boundary for the PR883 source/scope decision

The decision covers Thorisson Problem 4.1 and the native PID9900008 statement under the primary pointwise allocation definition.

| Feature/test | Exact verified position |
|---|---|
| Ambient group | Counterexample on R², inside LCSC Hausdorff Abelian source domain |
| Joint random element X | Constant, trivial action; explicitly allowed arbitrary random element |
| Measure ξ | Nonzero, diffuse/atomless, locally finite Radon, σ-finite, infinite total mass |
| Root | In support; no zero-window normalization in witness |
| Singularity | Singular relative to Haar, supported on countably many horizontal lines |
| Convex hull | Full R²; failure is not lack of full-dimensional convex hull |
| Support | Not full Haar support; source does not require it |
| Stationarity | Q itself is not stationary; source does not assume it; ξ is flow-adapted |
| Intensity | Q does not require a stationary intensity; optional uniform-phase model has finite positive intensity 3 |
| Action | Jointly Borel; stabilizer R×Z; not free; horizontal invariant direction |
| Information in π | Arbitrary measurable function of the complete original pair; canonical phase is observable from ξ |
| Covariance | Pointwise for every state and translation, as in 2009 Example 3.4 and induced source formula |
| Preservation | Handles both everywhere-state and Q-a.e.-state equality of pushed measures |
| Spatial null sets | Equality of measures only; root still constrained by exact horizontal covariance |
| Allocation regularity | All measurable maps; no bijectivity, injectivity, continuity, locality or monotonicity imposed |
| Independent stationary background | Not covered; explicit stronger/different premise |
| General Markov kernels | Not covered; this law fails an explicit preserving Markov kernel |
| Weighted kernels | Not covered; separate established characterization |
| Cox-projected tests | Not covered or certified |
| Positive-density/one-dimensional/no-invariant-direction variants | Not refuted by this example |
| Novelty and historical priority | Not certified; prior product lift and unequal-weight mechanisms credited |
| Current presentation | Mathematical/source PASS with existing credit addendum retained |
| Root-level action | No merge, publication, release, queue, or live-site decision is made |

No additional source restriction was found that excludes the submitted example. An allocation theory defined only modulo spatial null sets without a specified covariant origin representative would require a distinct formulation and is not the primary test audited here.
