# Theorem and quantifier ledger

This ledger was reconstructed from the compiled 30-page paper and the LaTeX
source. Statuses are deliberately provisional until independent derivations,
source audit, replay, and cross-checks are complete.

| ID | Location | Exact scope and hypothesis | Conclusion / equality / boundary | Audit status |
|---|---|---|---|---|
| Model orientation and normalization | p. 4, (2.1)-(2.2); `sections/02_model_results.tex:3` | Finite `V={1,...,n}`; loopless weights; every incoming degree positive; row `v` is dead target and column `u` is source; `r>0`. | `P` is loopless row-stochastic; a positive rescaling of one incoming weight-column cancels; dB mutant-parent probability is `f_r(P_{vS})`. | Pending independent transition check. |
| Complete baseline | p. 5, (2.3)-(2.4); source line 24 | Uniform off-diagonal `J_n`; uniformly random initial singleton; `r>0`, with continuity at `r=1`. | Exact fixation formula; value `1/n` at neutrality. | Pending derivation and literal-chain checks. |
| Theorem 1: fitness-two strict local optimality | p. 5, (2.5)-(2.8); source lines 35-74 | For every fixed `n>=3`; every tangent `delta` with zero diagonal and row sums; sufficiently small admissible `epsilon`. | Inverse-mean expansion with no linear term; `R_n^(2)` positive definite; strictly negative fixation Hessian for every nonzero direction; a strict local maximum with an `n`-dependent neighborhood. At `n=2`, all positive weightings tie. | Pending sector proofs and independent Hessians. |
| Theorem 2: complete-support strong-selection correction | p. 6, (2.9)-(2.10); source lines 85-111 | Fixed `n>=3`, fixed positive loopless directed weighting with complete support; `r -> infinity`. | Deficit coefficient `E_dir/[n^2(n-2)r]`; defect zero iff each target's incoming weights are equal; equality class is dynamically identical to `J_n` for every fitness. | Pending derivation. |
| Corollary 3: no fixed finite universal dB amplifier | p. 6; source lines 113-120 | Any fixed finite loopless directed weighting with positive incoming degrees. | Eventually strictly suppressing unless complete support and dynamically equivalent to `J_n`, in which case it ties for all fitness. Does not quantify uniformly over growing families. | Pending cited-theorem and reducible-support checks. |
| Proposition 4: undirected support limit | p. 6, (2.11)-(2.12); source lines 122-136 | Fixed finite connected undirected weighted graph; `r -> infinity`; `s_i` positive support degree. | Limit is the average `s_i/(s_i+1)`; incomplete support has the displayed strictly positive limiting deficit. | Pending limiting-chain check. |
| Theorem 5: weighted triangles | p. 6, (2.13), proof p. 15; source lines 141-147 and `sections/06_low_order.tex` | Every positive undirected weighted triangle; every `r>1`. | Complete graph globally maximizes fixation; equality iff all three edge weights are equal. At `r=1`, all structures tie but this is outside the theorem's strict-benefit domain. | Pending exact reconstruction. |
| Lemma 6: union-dual ergodicity | p. 7; `sections/03_duality_collision.tex:42` | Positive off-diagonal row-stochastic `P`; state space is all proper nonempty ancestral subsets. | Union dual is irreducible and aperiodic. | Pending adversarial path check. |
| Proposition 7: coverage representation | pp. 7-8, (3.7)-(3.9); source line 74 | Same positive-kernel hypothesis; stationary union-dual law. | Exact fixation committor is a coverage probability; `rho=m(P)/n`; all stated completely alternating mixed differences are nonnegative with the exact event formula. | Pending derivation / enumeration. |
| Lemma 8: active collision identity | pp. 8-9, (3.10)-(3.18); source line 108 | Rectangular spaces `Z_n` (including empty cache) and `Y_n` (nonempty cache); `A:Z->Y`, `R:Y->Z`; positive kernel. | `K=RA` on `Y` is irreducible/aperiodic; `M=AR` on `Z`; stationary laws are `eta/m` and `lambda/m`; `nu H=1/m=1/(n rho)`; `K(P)` is linear; conditional collision identity holds. | Pending phase/order and stationary-current checks. |
| Stationary perturbation and first variation | p. 10, (4.1)-(4.6); `sections/04_local_hessian.tex:3` | Fixed `n`, tangent direction, small positive-kernel neighborhood. | Group inverse/resolvent expansion is analytic; rank averaging yields `S Delta S=0` and vanishing first variation; quadratic form is `nu_0 Delta G Delta G q`. | Pending re-derivation. |
| Tangent decomposition | pp. 10-11, (4.7)-(4.10b); source lines 62-105 | Full tangent space at `J_n`. | Orthogonal direct sum of standard, symmetric-balanced, antisymmetric-balanced irreducibles with dimensions `n-1`, `n(n-3)/2`, `(n-1)(n-2)/2`; symmetric sector absent at `n=3`; multiplicity one; standard sector is exactly column imbalance. | Pending independent linear-algebra check. |
| Theorem 9: sector positivity | p. 11 and Appendix A pp. 18-26; source line 107 | Standard for `n>=3` (`N>=2`); symmetric-balanced for `n>=4` (`N>=3`); antisymmetric-balanced for `n>=3` (`N>=2`). | All physical sector scalars are strictly positive. Standard: exact `2<=N<=9`, analytic `N>=10`; antisymmetric: all `N>=2`; symmetric: exact solves `3<=N<=39`, exact margins `40<=N<=287`, analytic certificates `N>=288`. | Pending proof/certificate audit. |
| Lemma 11: finite-state perturbation | pp. 12-13; `sections/05_strong_selection.tex:26` | Finite analytic absorbing chain near `epsilon=0`; transient restriction spectral radius below one; generalized reachable-class hypothesis has bounded fundamental matrix and `O(epsilon)` leakage. | Absorption probabilities analytic; in generalized case, leakage before absorption is `O(epsilon)`. | Pending hypothesis/use check. |
| Lemma 12: fitness monotonicity | p. 16; `sections/07_implications_reproducibility.tex:8` | Any loopless row-stochastic `P`, any initial set, all `r>0`. | dB fixation is nondecreasing in fitness. | Pending coupling boundary check. |
| Proposition 13: support degree must diverge | p. 16, (7.2); source line 38 | Connected undirected weighted graphs `W_n`, order `n->infinity`; for every fixed `r>1`, eventually a dB amplifier. | Average `1/(s_i+1)` tends to zero; support degree of a uniformly chosen vertex diverges in probability. | Pending quantifier check. |
| Lemma 14: strict rank-Poisson gradients | pp. 21-22, (A.6); `appendices/A_sector_certificates.tex:257` | `N>=2`; complete active-rank chain and Poisson solution modulo constants. | `d_1>...>d_{N-1}>0`. | Pending coupling proof audit. |
| Lemma 15: finite exact symmetric-sector certificate | pp. 25-26, (A.33); source line 529 | Exact rational computations for `3<=N<=39` and every integer `40<=N<=287`. | Symmetric scalar positive on `3<=N<=39`; phase margin positive on `40<=N<=287`; exact minimum claimed at `N=40`, with printed rational; verifier hash printed. | Pending hash, source, and exhaustive execution audit. |
| Theorem 16: two symmetric weighted `K_4` families | pp. 27-28, (B.1)-(B.6); `appendices/B_k4_certificate.tex:147` | `G_13(x)` with `x>0`; `G_22(x,y)` with `x,y>0`; every `r>1`; only the two invariant families. | `J_4` maximizes within each family; equality iff `x=1` or `x=y=1`, respectively. No classification of unrestricted weighted `K_4`. | Pending lumping and symbolic reconstruction. |

## Explicit nonclaims

- No global all-kernel or all-undirected-weighting maximality theorem at
  fitness two.
- No local radius uniform in population size.
- No interchange of the fixed-structure `r -> infinity` limit with
  `n -> infinity`.
- No exclusion of growing amplifying families.
- No classification of unrestricted six-edge weighted `K_4` graphs.
- Finite exact computations must not be used to infer any stated infinite
  range; the analytic tails are separate proof obligations.

