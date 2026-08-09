# Theorem-to-artifact map

All paths are relative to the repository root. Historical verifiers remain in
their original source packages; the canonical scripts supplement rather than
replace them.

| Claim/result | Manuscript location | Analytic dependency | Exact or regression artifact |
|---|---|---|---|
| Source $d\sqrt2$ bound, $M_d$ strategy, and NPA comparison | Introduction; Table `tab:contributions`; Table `tab:exact-values` | Primary-source theorem, conjecture, and numerical table; exact radical evaluation for $d=2,\ldots,6$ | `cyclic_bell_exact_values_and_randomness/verification/verify_exact_benchmarks.py` |
| Polar identity in commuting algebras | Lemma `lem:polar` | Strong-limit construction of support and canonical partial isometry; bicommutant inclusion; polar support calculus | `cyclic_bell_exact_values_and_randomness/verification/verify_merged.py` (genuine nonunitary partial-isometry case); `cyclic_bell_tsirelson_bound/verify_certificate.py` |
| Scalar extremum and equality roots | Lemma `lem:scalar`; Appendix `app:scalar` | Parity-split trigonometric sum | `cyclic_bell_exact_values_and_randomness/verification/verify_merged.py`; `cyclic_bell_tsirelson_bound/verify_certificate.py` |
| Exact $q,qa,qc$ first reduced value | Theorem `thm:exact` | Polar identity, scalar extremum, continuous functional calculus, finite source attainment | `cyclic_bell_tsirelson_bound/verify_certificate.py`; `cyclic_bell_tsirelson_bound/tests/test_certificate.py`; source-convention checks in `verify_exact_benchmarks.py` |
| Global equality certificate | Equation `eq:global-certificate` | Exact sum of positive factors and spectral calculus | `cyclic_bell_tsirelson_bound/verify_certificate.py` (`global_certificate`, `commuting_certificate`) |
| First augmented value | Corollary `cor:first-augmented` | Exact reduced value and aligned source strategy | `cyclic_bell_tsirelson_bound/verify_certificate.py` (`bell_values`) |
| Canonical attainment and source Fourier formulas | Appendix `app:attainment` | Weyl relations, weighted-cycle product, trace identity | `cyclic_bell_tsirelson_bound/verify_certificate.py`; `cyclic_bell_exact_values_and_randomness/verification/verify_exact_benchmarks.py` |
| Equal supported multiplicities for every attained finite-dimensional tensor-product exact maximizer of the first augmented family, and $d\mid\dim K$ | Theorem `thm:support-rigidity`; Appendix `app:rigidity-proof` | Positive residuals, Schmidt-support cancellation, kernel-safe polar stabilizers, adjacent-phase reflections, reflection-product rank lemma | `cyclic_bell_exact_values_and_randomness/verification/verify_rigidity.py`; audit reconstruction in `audit/RIGIDITY_RESTORATION_AUDIT.md` |
| Conditional phase permutations | Theorem `thm:permutation` | Polar theorem, paired product hypotheses, weighted-cycle identity, maximally entangled trace identity | `cyclic_bell_exact_values_and_randomness/verification/verify_merged.py`; `cyclic_randomness_counterexample/cycle_family.py`; `cyclic_randomness_counterexample/test_cases.py` |
| First-family products and visible correlators | Equations `eq:cyclic-products`--`eq:visible-correlators` | Root-polynomial products and conditional permutation theorem | `cyclic_randomness_counterexample/test_cases.py`; `cyclic_randomness_counterexample/compare_reference_behavior.py` |
| Target distribution | Equation `eq:target-table` | Weighted-shift spectral projectors and finite Fourier transform | `cyclic_randomness_counterexample/verify_exact.py`; `cyclic_randomness_counterexample/test_cases.py` |
| All-$d\ge4$ biased first-family maximizers | Theorem `thm:biased` | Target DFT, lag-two autocorrelation, elementary max-versus-$\ell^1$ estimate | `cyclic_bell_exact_values_and_randomness/verification/verify_merged.py`; `cyclic_randomness_counterexample/test_cases.py` |
| Exact $d=4$ table, guessing probability, and entropy | Appendix `app:d4`; equations `eq:d4-table`, `eq:d4-entropy` | Exact cyclotomic arithmetic and $H_{\min}=-\log_2G$ for trivial Eve | `cyclic_randomness_counterexample/verify_exact.py`; `minimum_bell_randomness/verify_second_family_d4_exact.py`; entropy check in `verification/verify_exact_benchmarks.py` |
| Second-family SOS and $q,qa,qc$ value | Equation `eq:second-sos` and adjacent value display | Credited source-v3 SOS with prefactor $1/(2d)$, Fourier orthogonality, coefficient norm, commuting reading | `minimum_bell_randomness/verify_second_family_d4_exact.py`; `minimum_bell_randomness/second_family_discovery.py` |
| Second-family permutation maximizers | Theorem `thm:second` | Exact Fourier compression, weighted-cycle parity, full source-v3 SOS, target-table transfer | `minimum_bell_randomness/verify_second_family_d4_exact.py`; `minimum_bell_randomness/second_family_discovery.py`; `minimum_bell_randomness/test_cases.py` |
| Main-versus-appendix second-family conventions | Theorem `thm:second`; Appendix `app:conventions` | Consistent all-Bob adjunction is Bob outcome inversion; no termwise mixing | `verification/verify_exact_benchmarks.py`; `minimum_bell_randomness/verify_second_family_d4_exact.py` |
| Model-indexed value-only guessing bound | Equation `eq:gval-model`; equation `eq:value-conditioned` | Finite witness embeds into $q,qa,qc$; trivial-Eve guessing lower bound | Both exact $d=4$ verifiers and `verification/verify_merged.py` |
| Precise Conjecture 2 counterexample | Randomness section, displayed scalar-value implication | First augmented exact maximum, nonuniform exact target table, normalization remark | `cyclic_randomness_counterexample/verify_exact.py`; normalization checks in `verification/verify_exact_benchmarks.py` |
| Behavior-level nonuniqueness | Corollary `cor:behavior-nonunique` | Uniform versus nonuniform entry multiset under local output permutations | Exact target-table verifiers above |
| Endpoint robustness | Corollary following `cor:behavior-nonunique` | Zero-deficit biased witness is feasible for every “deficit at most $\varepsilon$” set | No finite test needed beyond exact witness replay |
| One-input baseline | Proposition `prop:one-input` | Explicit local model and pure projective Eve flag | `cyclic_bell_exact_values_and_randomness/verification/verify_merged.py`; historical `minimum_bell_randomness/STRUCTURAL_RESULTS.md` |
| Binary $2\times2$ value and private outputs | Theorem `thm:binary-benchmark`; Appendix `app:binary` | Two-square commuting SOS; on-state anticommutation; operator-valued Fourier inversion | `cyclic_bell_exact_values_and_randomness/verification/verify_private_mub_binary.py`; `minimum_bell_randomness/verify_binary_2x2.py` |
| Private-MUB sufficient criterion | Lemma `lem:private-mub` | Private reference states, perfect matching, state-supported MUB sandwich, test-operator duality | `cyclic_bell_exact_values_and_randomness/verification/verify_private_mub_binary.py`; audit in `audit/LOW_SETTING_RESTORATION_AUDIT.md` |
| Scoped ideal-table and computational-MUB obstructions | Appendix `app:settings`; Proposition `prop:mub` | Fourier overlaps and circulant/corner-block spectral argument | `minimum_bell_randomness/satwap_ideal_audit.py`; `verification/verify_mub_obstruction.py` |

## Focused replay commands

```sh
(cd cyclic_bell_exact_values_and_randomness && python3 verification/verify_merged.py)
(cd cyclic_bell_exact_values_and_randomness && python3 verification/verify_rigidity.py)
(cd cyclic_bell_exact_values_and_randomness && python3 verification/verify_exact_benchmarks.py)
(cd cyclic_bell_exact_values_and_randomness && python3 verification/verify_private_mub_binary.py)
(cd cyclic_randomness_counterexample && python3 verify_exact.py)
(cd minimum_bell_randomness && python3 verify_second_family_d4_exact.py)
```

## Full canonical replay

```sh
cd cyclic_bell_exact_values_and_randomness
./reproduce.sh
```

The full wrapper additionally runs preserved setting regressions, historical
integrity manifests, the manuscript and summary builds, PDF metadata checks,
website validation, and the canonical package manifest. Passing any finite
suite does not replace the analytic proofs.
