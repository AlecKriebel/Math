# Verification companion

The manuscript proves the counterexample for the entire ordinary, uncompleted algebra of complex-valued finite-order link invariants. The scripts are exact finite diagnostics, not a proof by sampled invariants.

## Running the checks

Requires Python 3.10 or newer; standard library only. From this folder run:

```sh
python3 verify.py
python3 -O verify.py
python3 review/independent_checks.py
python3 -O review/independent_checks.py
```

Each command prints JSON and raises an explicit exception on a failed scientific check. The scripts do not write into this folder. Scientific gates use explicit exceptions and remain active with optimization.

The first script checks finite-difference and Newton identities, singular braid exponent expansion and parity, linking-square symmetry and third differences, restriction products, and half-parameter values. The independently developed second script follows individual crossing resolutions, binomial-basis multiplication, four-component matrices, and exact polynomial remainders. The universal statement is proved by the singular-link argument and polynomial uniqueness in the manuscript and proof companion.

## Files and provenance

CANDIDATE.md and review/author_replay/CANDIDATE.md are identical proof companions for the two historical script layouts. nullstellensatz.tex is identical to the manuscript source. PRIORITY_AUDIT.md distinguishes the explicit ideal counterexample from old polynomiality and lists the coverage limits. FRESH_CONTROL_RUNS.json records four fresh baseline executions and four deliberate wrong-half-parameter controls, rejected both normally and with optimization. The baseline scripts respectively passed 8,460 and 20,980 finite checks per run.

Earlier Root reproduction comprised 40 separate runs: eight baseline passes, eight ordinary original-code mutation rejections, eight optimized original-code false accepts, and 16 explicit-guard rejections. Those runs are not relabeled as this package's fresh executions. The original assertion-only implementation was repaired to explicit exceptions; an incomplete historical pilot was excluded. The package retains the repaired scientific loops; only their output placement is adapted for standalone use. The raw historical 40-run records and incomplete pilot are repository-only audit provenance, not files in this archive or runtime dependencies.

AI tools were used extensively in development, drafting, checking, and source audit. The work is unrefereed and has not undergone conventional human peer review. This package contains independently authored material; third-party primary bodies are not redistributed.

License: CC BY 4.0.

The source's indexed linking-number ideal is interpreted in the ordered/labelled theory. The symmetric counterexample and whole-algebra difference proof work both with and without labels. Dated source reports are retained verbatim; source_audit/READING_QUALIFICATION.md supplies the corresponding scope and repository-only reference qualifications.
