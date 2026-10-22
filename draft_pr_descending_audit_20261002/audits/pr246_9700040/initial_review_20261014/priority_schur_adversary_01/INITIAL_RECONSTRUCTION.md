# Independent initial reconstruction

UTC: 2026-10-15 03:52:39 UTC (filesystem creation timestamp; initial hand-entered minute label corrected at finalization). Checkpoint completion estimate: 10% of assigned priority audit.

This note was written after reading only the submitted PROOF.md and enumerating the authenticated-source directory, before reading inherited audit verdicts, ledgers, or source-review conclusions. No other priority family's work has been read.

## Claim under test

For every finite collection of indices and thresholds, the stationary nearest-right left-jump process with deterministic drift dX_i/ds=X_i has survival law

P(X_{r_j}>x_j, all j) = exp(-x_m) sum_{lambda^0=empty subset ... subset lambda^m; lambda^j_1<r_j} s_{lambda^m}(rho_1) product_j s_{lambda^j/lambda^{j-1}}(rho_{x_j-x_{j-1}}),

where rho_t is the exponential specialization p_1=t and p_k=0 for k>1, so s_{lambda/mu}(rho_t)=t^{|lambda|-|mu|} f^{lambda/mu}/(|lambda|-|mu|)!. This is a candidate mathematical identity already independently checked by other families; this audit tests complete earlier coverage, not their verdicts.

## Independent framework reconstruction

1. Let Lambda(x) be the RSK shape of a rate-one marked Poisson process on (0,x] with independent U(0,1) marks. Conditional on N(x)=n, the mark ranks form a uniform permutation. Conditional shape probabilities are Plancherel probabilities.
2. The joint shape chain at x_1<...<x_m has exactly the weight above without row constraints. It is an ascending Schur process with successive positive specializations rho_{Delta_j} and one terminal negative specialization rho_1, normalizer exp(x_m). All negative specializations except the terminal one are trivial.
3. Equivalently, N(x) is a rate-one Poisson clock applied to Plancherel growth on Young diagrams. The discrete one-box transition should be f^{nu}/[(n+1)f^{lambda}], for nu covering lambda; a finite-duration transition should be exp(-Delta) Delta^{|nu|-|lambda|}/(|nu|-|lambda|)! times f^{nu/lambda} f^{nu}/(f^{lambda} (n+1)...|nu|).
4. The candidate variables X_i at a stationary time are the generalized inverse of x -> Lambda_1(x), the first row along this path. Thus the all-index law is a standard first-row barrier event for this special Schur process.
5. To refute novelty of the complete answer, it is insufficient merely to locate the Schur process definition. I must pin either a primary theorem explicitly identifying this barrier law with the drift-jump stationary process, or a complete combination of earlier primary results with a transparent parameter mapping and no unresolved bridge.
6. The likely delicate bridge is stationarity: the candidate uses unit quadrant PPP and Y_i(s)=e^s Z_i(e^s). The map (u,v)->(uv,log v) preserves area and turns the inverse-LIS process into the specified drift-jump dynamics. This is short to check, but may not be stated in Schur-process literature. The audit must distinguish a new bridge from a classical identification already present in Hammersley/patience-sorting sources.

## Adversarial controls planned

- Verify exact specialization convention and endpoint orientation against Okounkov–Reshetikhin and the Poissonized Schur sampling paper.
- Check full path law, not just one-time poissonized Plancherel measure or individual first-row marginal.
- Check whether the earlier formula covers arbitrary sorted-threshold indices, repeated-index events, and the inverse convention X_r>x iff Lambda_1(x)<r.
- Track publication/version dates independently of live problem-list status.
- Reconstruct the Markov path weights and selected exact low-degree coefficients independently of candidate code.

Initial assessment: the determinant sum itself appears exactly a classical Schur path probability. Whether this settles historical priority of the stationary answer is open pending primary-source reading.
