# Theorem-to-artifact map

All paths are relative to the repository root.  Historical verifiers are preserved in place; the canonical `reproduce.sh` should call or independently replay them without deleting them.

| Claim/result | Manuscript location | Analytic dependency | Exact or regression artifact |
|---|---|---|---|
| CBR-003 polar identity | `main.tex`, Lemma `lem:polar` | Polar support calculus in commuting von Neumann algebras | `cyclic_bell_exact_values_and_randomness/verification/verify_merged.py` (genuine partial-isometry kernel case); `cyclic_bell_tsirelson_bound/verify_certificate.py` (`polar_sos`) |
| CBR-004 scalar extremum | `main.tex`, Lemma `lem:scalar`; Appendix `app:scalar` | Trigonometric parity split | `cyclic_bell_tsirelson_bound/verify_certificate.py` (`scalar`, `exact_symbolic`) |
| CBR-005 exact \(q,q_a,q_c\) value | `main.tex`, Theorem `thm:exact` | CBR-003, CBR-004, functional calculus, CBR-008 | `cyclic_bell_tsirelson_bound/verify_certificate.py`; `tests/test_certificate.py` |
| CBR-006 global gap/equality boundary | `main.tex`, equation `eq:global-certificate` | Exact sum of positive factors and spectral calculus | `cyclic_bell_tsirelson_bound/verify_certificate.py` (`global_certificate`, `commuting_certificate`) |
| CBR-007 first augmentation | `main.tex`, Corollary `cor:first-augmented` | CBR-005 and aligned attaining strategy | `cyclic_bell_tsirelson_bound/verify_certificate.py` (`bell_values`) |
| CBR-008 canonical attainment | `main.tex`, Appendix `app:attainment` | Weyl relations and weighted-cycle product | `cyclic_bell_tsirelson_bound/verify_certificate.py` (`weyl_and_bob`) |
| CBR-009 conditional phase permutations | `main.tex`, Theorem `thm:permutation` | Polar theorem, product hypotheses, trace identity | `cyclic_bell_exact_values_and_randomness/verification/verify_merged.py` (reversed/random/adversarial cases); `cyclic_randomness_counterexample/cycle_family.py`; `test_cases.py` |
| CBR-010 first-family admissibility and visible correlators | `main.tex`, equations `eq:cyclic-products`--`eq:visible-correlators` | Polynomial products and CBR-009 | `cyclic_randomness_counterexample/test_cases.py`; `compare_reference_behavior.py` |
| CBR-011 target distribution | `main.tex`, equation `eq:target-table` | Weighted-shift projectors and Fourier transform | `cyclic_randomness_counterexample/verify_exact.py`; `test_cases.py` |
| CBR-012 all-\(d\) biased maximizers | `main.tex`, Theorem `thm:biased` | CBR-010/011 and lag-two autocorrelation | `cyclic_randomness_counterexample/test_cases.py`; `minimum_bell_randomness/test_cases.py` |
| CBR-013 exact \(d=4\) table | `main.tex`, Appendix `app:d4` | Exact cyclotomic arithmetic | `cyclic_randomness_counterexample/verify_exact.py`; `minimum_bell_randomness/verify_second_family_d4_exact.py` |
| CBR-014 second-family SOS/value | `main.tex`, equation `eq:second-sos` | Fourier orthogonality and coefficient norm | `minimum_bell_randomness/verify_second_family_d4_exact.py`; `second_family_discovery.py` |
| CBR-015 second-family permutations | `main.tex`, Theorem `thm:second` | Geometric sum, order parity, CBR-014 | `minimum_bell_randomness/verify_second_family_d4_exact.py`; `second_family_discovery.py`; `test_cases.py` |
| CBR-016/017 value-only guessing consequences | `main.tex`, `sec:randomness` | CBR-012 and CBR-015 plus elementary guessing bound | Target tables in both exact \(d=4\) verifiers |
| CBR-019 one-input baseline | `main.tex`, Proposition `prop:one-input` | Explicit local model and flagged purification | `cyclic_bell_exact_values_and_randomness/verification/verify_merged.py`; historical derivation in `minimum_bell_randomness/STRUCTURAL_RESULTS.md` |
| CBR-020/021 scoped ideal-table obstructions | `main.tex`, Appendix `app:settings` | Fourier overlaps | `minimum_bell_randomness/satwap_ideal_audit.py` |
| CBR-022 computational-MUB obstruction | `main.tex`, Proposition `prop:mub` | Circulant/corner-block spectral proof | Historical derivation in `minimum_bell_randomness/manuscript.tex`; finite nullspace replay described in `STRUCTURAL_RESULTS.md` |
| CBR-023 binary calibration | `main.tex`, setting discussion/remark | Exact two-square SOS and Fourier moments | `minimum_bell_randomness/verify_binary_2x2.py` |

## Shortest replay commands

```sh
(cd cyclic_bell_exact_values_and_randomness && python3 verification/verify_merged.py)
(cd cyclic_randomness_counterexample && python verify_exact.py)
(cd minimum_bell_randomness && python verify_second_family_d4_exact.py)
```

## Full preserved replay commands

```sh
(cd cyclic_bell_tsirelson_bound && python verify_certificate.py)
(cd cyclic_bell_tsirelson_bound && python -m unittest discover -s tests -v)
(cd cyclic_randomness_counterexample && python test_cases.py)
(cd minimum_bell_randomness && python second_family_discovery.py)
(cd minimum_bell_randomness && python test_cases.py)
(cd minimum_bell_randomness && python satwap_ideal_audit.py)
(cd minimum_bell_randomness && python verify_binary_2x2.py)
```

Use the environment selected by the canonical reproduction script; NumPy/SymPy-dependent historical scripts require their declared dependencies.  Passing these commands does not replace the analytic proofs.
