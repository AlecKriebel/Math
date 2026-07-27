# Claims ledger

| ID | Claim | Status | Verification |
|---|---|---|---|
| C-001 | For arbitrary tensor-product unitaries on arbitrary Hilbert spaces, `I_d <= 2*csc(pi/(2d))*I`. | **General theorem** | Exact bounded-operator partial-isometry polar certificate and scalar functional calculus, reproduced in the manuscript. |
| C-002 | Scalar equality occurs exactly at `z^d=(-1)^(d-1)`. | **General theorem** | Complete odd/even cosine-grid proof. |
| C-003 | The maximum of the augmented operator under the displayed definitions is `2*csc(pi/(2d))+1`. | **General theorem** | C-001 plus the unitary real-part bound; attained by C-006. |
| C-004 | Every ordering of the equality roots yields the displayed weighted-shift maximizer on `C^d tensor C^d`. | **General theorem** | Root products, weighted-shift power identity, exact polar factorization, and maximally entangled trace identity. |
| C-005 | The target table of a weighted-shift maximizer is `|qhat_{-(a+b)}|^2/d^3`. | **General theorem** | Explicit eigenvectors and transposed-projector calculation. |
| C-006 | The order `(0,1,...,d-3,d-1,d-2)` produces a nonuniform target table for every `d>=4`. | **General theorem** | Exact nonzero second autocorrelation. |
| C-007 | Both local marginals of that target table equal `1/d`. | **General theorem** | Parseval and the fact that `a+b` traverses every Fourier index. |
| C-008 | The family satisfies `G >= 1/d^2 + 2*sin(pi/d)*sin(3*pi/d)/(d^2*(d-1)) > 1/d^2`. | **Certified infinite counterexample family** | Exact autocorrelation magnitude, Fourier inversion, Parseval, and the mean-zero positive-entry estimate. |
| C-009 | After correcting the printed normalization typo, the Bell-value reading of Conjecture 2 is false for every `d>=4` for the displayed first augmented family. | **General disproof** | C-003 and C-008; Eve is one-dimensional. This does not refute randomness of the fixed canonical full behavior. |
| C-010 | At `d=4`, the sparse monomial observables are admissible and attain `2*csc(pi/8)+1`. | **Exact finite case / machine-checked** | Exact arithmetic in `Q(zeta_16)`; `verify_exact.py`. |
| C-011 | Their target probabilities alternate between `1/32` and `3/32`, so `G=3/32>1/16`. | **Exact counterexample / machine-checked** | Exact projector and separately structured Fourier calculations. |
| C-012 | Every finite-dimensional exact augmented maximizer has equal supported multiplicities for all equality roots, hence `d | dim(supp rho_A)`. | **General theorem** | Repaired support-range polar argument plus reflection-product rank lemma in the Appendix. |
| C-013 | The first augmented family has a unique maximizing behavior for `d>=4`. | **Disproved** | C-004 through C-011 give maximizers with distinct target tables. |
| C-014 | A guessing upper bound depending only on Bell value or Bell deficit and converging to `1/d^2` at zero deficit holds for `d>=4`. | **Disproved** | Exact nonuniform maximizers already violate the limiting endpoint; bounds using additional observed statistics are not excluded. |
| C-015 | The swapped-final-pair family attains the worst guessing probability over the maximizing face. | **Speculation / unresolved** | The construction supplies a lower bound on the worst case, not an optimum. |
| C-016 | Maximal violation certifies maximal randomness at `d=2` or `d=3`. | **Unresolved here** | The present family is uniform there; other maximizers are not classified. |
| C-017 | No public equivalent counterexample predates this release. | **Not established** | A targeted audit found none, but cannot rule out unindexed, unpublished, or concurrent work. |
| C-018 | The historical equality-variety search locates a gauge-equivalent nonuniform `d=4` component. | **Numerically supported** | `discovery_search.py`; not used by the proof. |
| C-019 | The supplied finite regression suite passes for canonical `d=2,...,12`, nonuniform `d=4,...,12`, and every root ordering at `d=2,3`. | **Computationally verified** | `test_cases.py`; floating-point and secondary. |
| C-020 | The cyclic ordering reproduces the reference Eq. (13)/(15)/(45) full behavior through `d=12`, while the root swap preserves the Bell-visible first harmonics and changes the full behavior for `d=4,...,12`. | **Computationally verified** | `compare_reference_behavior.py`; the first-harmonic ordering invariance is also proved analytically in the manuscript. |
| C-021 | Every root ordering in this weighted-shift family has a uniform target table for `d=2,3`. | **Exact finite cases** | Direct two-point Fourier check for `d=2` and vanishing cyclic autocorrelations for `d=3`. This does not classify all maximizers. |
| C-022 | At `d=4`, the cyclic and root-swapped maximizers have exactly identical first harmonics in every Bell term but target tables `1/16` and alternating `1/32,3/32`. | **Exact finite case / machine-checked** | Exact arithmetic in `Q(zeta_16)` in `verify_exact.py`. |
