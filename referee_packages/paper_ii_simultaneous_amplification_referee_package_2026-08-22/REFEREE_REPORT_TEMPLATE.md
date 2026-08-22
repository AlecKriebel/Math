# Independent referee report template

## Recommendation

Choose exactly one after completing the review:

- fully validated
- valid after minor corrections
- major correction required
- invalid
- inconclusive / review incomplete

## Package and environment record

- Package manifest result:
- Source archive and internal manifest result:
- Scientific source commit/annotated unsigned tag checked:
- Git blob/mode comparison completed, and provenance limitation:
- Operating system and architecture:
- Python, SymPy, and mpmath versions:
- Tectonic and Poppler versions:
- Commands and exit statuses:
- Checks not completed, with reasons:

## Theorem-by-theorem validation

| Claim or proof component | Status | Independent reasoning or check | Location | Finding |
|---|---|---|---|---|
| Main theorem and numerical `R_sim` lower bound |  |  |  |  |
| Model, baselines, and quantifiers |  |  |  |  |
| Effective graph construction |  |  |  |  |
| Strong lumping and weak-cut trace |  |  |  |  |
| Establishment and core confinement |  |  |  |  |
| Bd and dB cleanup |  |  |  |  |
| Pendant initialization |  |  |  |  |
| Reciprocal invasion estimates |  |  |  |  |
| Gate rates and global sweep |  |  |  |  |
| Response expansion |  |  |  |  |
| Sextic optimization |  |  |  |  |
| Rational specialization |  |  |  |  |
| Final diagonal quantifier transfer |  |  |  |  |

## Code inspection and execution

| Program | Intended claim | Source-audit result | Execution result | Independence or coverage limitation |
|---|---|---|---|---|
| `verify_leading_algebra.py` |  |  |  |  |
| `verify_hybrid_lumping.py` |  |  |  |  |
| `verify_hybrid_coefficients.py` |  |  |  |  |
| `verify_paper_claims.py` |  |  |  |  |
| `verify_referee_package.py` |  |  |  |  |
| `verify_git_binding.py` |  |  |  |  |
| `run_all_referee_checks.sh` |  |  |  |  |
| `bootstrap_replay.sh` and `replay.sh` |  |  |  |  |
| `tests/test_verifier_fail_closed.py` |  |  |  |  |
| `build.sh` and `requirements.txt` |  |  |  |  |
| `release_bundle.sh` and `bundle_manifest.py` |  |  |  |  |

## Findings

For each finding, record severity, exact theorem/page/equation or file/line,
reasoning, and a counterexample or reproduction command when applicable.
Separate mathematical defects, code defects, reproducibility defects,
exposition issues, and optional suggestions.

## Proof--software consistency

State whether the programs check exactly the claims attributed to them and
whether any manuscript conclusion relies on a computation outside the stated
certificate boundary.

## Unresolved assumptions

List every assumption, cited fact, environment requirement, or check that was
not independently resolved.

## Final rationale

Explain why the selected recommendation follows from the evidence above.
