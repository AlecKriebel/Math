# Final result: original unresolved, five substantive turns

AI-assisted mathematical research; independent full review pending. No novelty or exhaustive current-open certification.

The precise target is BLN Conjecture1, referenced in Bubeck's OWR15/2021 contribution printed862: arbitrary real parameters in a width-k two-layer network with a fixed Lipschitz activation, random signs and generic spherical/normalized-Gaussian inputs, and a conjectured sqrt(n/k) robustness penalty. The source's Gaussian/sphere-norm convention is left explicit rather than silently changed. The separate matching construction question is not this target.

Completed partials:

1. For uniform random circle inputs, an exact distribution for the optimal Lipschitz interpolation constant among all functions, and a high-probability n²/log n geometric lower bound. No fixed-width attainment claim.
2. For fixed-dimensional positive-density charts, a birthday-collision floor of order(n²/log n)^(1/s). This gives the desired lower order in fixed spherical d≤4, and global-norm Gaussian d≤3. Dimension constants are not uniform in growing d.
3. A credited projection-mechanism reconstruction for the actual sphere norm, uniformly over adaptive spans and nonsmooth functions: a fixed-accuracy sqrt(d/rank) floor. When n≫d this still misses the main n/d factor.
4. A log-free sqrt(n/k) sphere bound for bias-free ReLU networks with linearly independent hidden rows, k≤d, arbitrary output coefficients/constant and fixed-accuracy fitting. The proof uses all activation patterns, sphere-to-global homogeneity and an explicit centered subgaussian chaining estimate. Dependent rows, hidden biases and general activations are excluded.
5. A log-free sqrt(n/k) sphere bound for quadratic functions with rank(A)≤k, including all quadratic-neuron widths and hidden biases. A balanced signed matrix removes the radial-constant ambiguity. A fixed globally Lipschitz quadratic-core activation realizes this subclass, but arbitrary units crossing outside the core are not covered.

All probability and infinite-uniformity claims have written proofs. Exact finite controls are supplementary, with their scopes stated in each receipt. Classical tools and the original BLN results are credited. The recent Shmalo preprint is used for context/credit only, not as an unaudited premise or a proof of the entire original conjecture.

The general growing-dimensional arbitrary-activation/parameter problem remains unresolved5/5. Author search stops here. No sixth author turn or final promotion is authorized by this packet.
