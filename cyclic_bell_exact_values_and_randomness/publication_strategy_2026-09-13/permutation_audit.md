# Independent adversarial review: permutations, second family, and privacy

Checkpoint: 2026-09-14T00:41Z (2026-09-13 Pacific). Completion estimate: 100% of this bounded manuscript audit; this is not a claim that the research program or external peer review is complete.

## Scope and verdict

I reconstructed the arguments in `main.tex`, Sections 5–9 and Appendices C–E, before consulting any historical audit report. I did not edit the manuscript, contact anyone, or make git changes. This audit is mathematical and computational; a current literature/priority search remains a separate task.

**No mathematical blocker found in the permutation counterexample, its second-family extension, or the stated privacy implications.** The strongest result in this audited scope is an explicit all-dimensional family of admissible exact maximizers of both augmented cyclic Bell functionals, for every d >= 4, with uniform local marginals but a nonuniform designated joint table. Every complex first-harmonic correlator stays fixed. At d = 4, two exact implementations reproduce the table with entries 1/32 and 3/32 and the guessing probability 3/32, rather than 1/16.

The distinction between Bell-value constraints and full-behavior constraints is essential, and the manuscript states it correctly. The construction disproves the scalar-value maximal-randomness implication, assuming the originating conjecture is indeed read with the displayed operator and target pair. It does not refute the source's canonical full-behavior SDP calculations or its d = 3 self-test.

## Independent proof reconstruction

| Claim | Checkable mechanism | Finding / exact limitation |
|---|---|---|
| Conditional permutation theorem | A weighted d-cycle has dth power equal to the product of weights times identity and characteristic polynomial t^d minus that product. The product-one hypotheses ensure order d and simple full root spectrum. | Correct, including repeated equality phases in the labeled data and arbitrary unitary extensions at zeros. It is a sufficient construction, not a classification. |
| Attainment and polar kernels | Writing L = W|L| makes the canonical polar factor WE, with E its support. Thus V|L|^(1/2) = W|L|^(1/2), even at a kernel. With B = conjugate(W), vectorization kills the positive residual. | Correct; the proof does not incorrectly require the canonical polar partial isometry to be unitary. |
| Blind first harmonics | The maximally entangled trace formula reduces all first-harmonic correlators to symmetric sums over phase labels. Each local weighted cycle has zero trace. | Correct. Full higher-harmonic data need not be invariant. |
| First-family admissibility | Equality roots solve z^d = (-1)^(d-1). Their product is 1; product_k(1 + omega^y z_k) = 2, so the polar phase products are also 1. | Correct for both parities. No factor vanishes. |
| Joint table normalization | Gauge phases q satisfy A1 = QXQ*. The target probability is |q-hat_{-(a+b)}|^2/d^3. Parseval sums the Fourier squares to d^2. | Correct d^-3 normalization; each marginal is 1/d and the table sums to 1. |
| Canonical flatness | Canonical q has zero cyclic autocorrelation at every nonzero lag. | Correct in even and odd dimensions, with the chosen parity correction ensuring periodicity. |
| Final-two swap | Only the affected neighboring products in the lag-two autocorrelation change; R2 = (z_(d-1)-z_(d-2))(z_(d-3)-z_0). | Correct; magnitude is 4 sin(pi/d) sin(3pi/d), strictly positive exactly in the claimed d >= 4 regime. |
| Guessing gap | Put x_m = |q-hat_m|^2-d, Delta = max x_m. Mean zero gives d|R2| <= sum |x_m| <= 2(d-1)Delta. | Correct lower bound. It is neither the optimal permutation nor the exact optimized adversarial guessing value. |
| Small dimensions | R1 is the sum of all equality roots and vanishes; conjugacy covers every nonzero autocorrelation for d = 2,3. | Correct boundary statement: this orbit is flat; it does not settle all maximizers in those dimensions. |
| Second-family SOS | Expanding P_l = d lambda_l I - A_l B-hat_l gives dI-F = (1/(2d)) sum P_l* P_l using sum |lambda_l|^2=1 and sum B-hat_l* B-hat_l=d^2 I. | Correct coefficient, adjoint, and normalization. This is inherited source machinery, not new SOS novelty. |
| Second-family phases | Two geometric sums give S_l = d lambda_l r_l. Weighted-cycle products give D_l^d=I, since l(l+d-2+delta_d) is even. | Correct. A1 reduces exactly to the first-family A1, so the same designated table follows. |
| Privacy consequence | Trivial Eve can guess the largest table entry. This finite strategy embeds into the q, qa, and qc adversarial models. | Correct obstruction in all three models; there is no need to solve an Eve optimization to disprove maximal randomness. |
| Endpoint robustness | A deficit-zero biased strategy satisfies every constraint “deficit at most epsilon.” | Correct impossibility of a value-only bound converging to 1/d^2 at zero deficit. Bounds using additional statistics are unaffected. |
| Binary privacy benchmark | The two SOS squares yield the on-state anticommutators. The commuting Eve test operator can be moved through each relation, killing the three nontrivial Fourier moments. | Correct for the finite-dimensional purification scope claimed. Already acknowledged prior art. |
| Private-MUB lemma | Perfect matching moves Bob's projector to Alice; the supported sandwich contributes 1/d; private reference outcome contributes another 1/d. Equality against every Hermitian Eve test operator proves the conditional-state identity. | Correct sufficient criterion. It does not construct a Bell test enforcing its hypotheses. |

## Significant simplification of the ancillary MUB obstruction

The long circulant and Toeplitz proof of the computational-MUB exposure obstruction is unnecessary. Every matrix in the real Hermitian span of PVM projectors unbiased to the computational basis has **constant diagonal**. For the displayed system,

    K_rr = (sum_j x_j + sum_j y_j)/d = Tr(K)/d

for every r. If e_r is an eigenvector with eigenvalue kappa, then kappa = K_rr = Tr(K)/d, the arithmetic mean of the eigenvalues. If a Hermitian K is nonscalar, its smallest eigenvalue is strictly below that mean and its largest strictly above it. This proves the proposition directly. It also applies to any number of PVMs unbiased to the target computational basis; the special half-phase Fourier structure is not needed.

The coefficientwise exposure consequence follows immediately: a computational outcome of nonzero weight cannot attain the largest eigenvalue of its coefficient matrix unless that matrix is scalar. Scalar coefficients cannot select a measurement.

This is an editorial improvement and useful generalization, not a correctness failure. It indicates that this auxiliary obstruction should receive little novelty/impact weight. Moving the low-setting material to a compact appendix would leave the paper's central contribution easier to identify.

## Replayed verification

All commands below ran from `/Users/alec/Documents/Math` under `python3`, with exit code 0. Each command's stdout/stderr was saved in this review folder; canonical verification outputs were not overwritten.

| Command | Saved evidence | Outcome |
|---|---|---|
| `python3 cyclic_bell_exact_values_and_randomness/verification/verify_merged.py` | `evidence/verify_merged_permutation_audit.txt` | Nine groups pass: scalar controls, genuinely partial polar factor, 125 first-/second-family strategies, small-d exhaustive flatness, hostile invalid constructions, target tables, and one-input reconstruction. |
| `python3 cyclic_randomness_counterexample/verify_exact.py` | `evidence/verify_exact_permutation_audit.txt` | Exact Q(zeta_16) first-family admissibility, value, independent projector/Fourier target tables, and first-harmonic agreement pass. |
| `python3 minimum_bell_randomness/verify_second_family_d4_exact.py` | `evidence/verify_second_family_d4_exact_permutation_audit.txt` | Independent exact second-family Fourier compression, order, full SOS identity, value 5, and table pass. |
| `python3 cyclic_bell_exact_values_and_randomness/verification/verify_private_mub_binary.py` | `evidence/verify_private_mub_binary_permutation_audit.txt` | Exact binary SOS and strategy pass; 1,980 composition checks in d=2,...,12 and all three dropped-hypothesis controls pass. |
| `python3 cyclic_bell_exact_values_and_randomness/verification/verify_mub_obstruction.py` | `evidence/verify_mub_obstruction_permutation_audit.txt` | d=2,...,20, 209 computational indices, 1,672 admissible samples pass. |

Finite numerical sweeps are regression evidence, not proofs of all-dimensional statements or arbitrary Eve systems. The all-dimensional conclusions above rest on the reconstructed analytic arguments. The two d=4 certificates supply exact algebraic evidence, but are not proof-assistant kernel checks.

## Consequences for publication, impact, and Lean

- The mathematical significance lies in resolving a concrete exact-value conjecture and exposing a genuine ambiguity in scalar randomness certification for two recently proposed families. It is a focused quantum-information contribution, not presently a general solution of randomness certification or low-setting design.
- The orbit mechanism is more transferable than an isolated numerical counterexample. Its usable content is the explicit product-one criterion plus invariance of the entire first-harmonic matrix, not a claim that every first-harmonic functional has this failure.
- The lower bound on guessing probability tends to its ideal value rapidly with d (the additive guaranteed gap is asymptotic to 6 pi^2/d^5). This does not weaken the exact counterexample, but it does mean the displayed general lower bound alone is not a strong operational high-dimensional loss estimate. The d=4 loss is concrete and appreciable.
- Formalizing the whole paper in Lean is unlikely to be the highest-return next step. It would require substantial complex operator, spectral, tensor-product, and quantum-probability infrastructure to verify results whose current main uncertainty for publication is specialist assessment and novelty, not missing finite checks. Lean also cannot establish novelty or repair a mismatch with a source conjecture's intended scope.
- If a formalization project is desired later, the bounded d=4 cyclotomic matrix/probability certificate is the sensible entry point. State exactly whether it proves only construction/admissibility/table or also the global Bell upper bound: verifying the former alone is not a formal proof of maximality. The all-dimensional Fourier/autocorrelation lemma is another much lighter standalone target than the complete commuting-operator theorem.
- The immediate publication step should be a compact specialist-facing exposition of the exact value, admissible orbit, d=4 certificate, and scalar-versus-full-behavior boundary. The current technical work in this audited scope does not require waiting for Lean. No outreach has been prepared or initiated; only the human researcher may communicate externally.

## Remaining external checks

This audit does not independently establish current priority, journal fit, the exact wording/version history of the source conjecture, or the rigor of the separate support-multiplicity theorem. Those are separate checks and should not be inferred from the passing permutation tests. No proof of the complete maximizing face, optimal guessing probability, general d>=3 minimal-setting construction, or robust near-maximal self-test is supplied by this paper.
