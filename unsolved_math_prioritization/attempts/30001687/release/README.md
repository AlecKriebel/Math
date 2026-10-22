# Spectral Thickness of Fibonacci Hamiltonians

- Upstream ID: **30001687**; code: **OWR-4793-001**; queue rank: **620**.
- Disposition: **unsolved** after **5/5** substantive routes.
- No full proof, spectral counterexample, or novel discovery is claimed.

The order-of-magnitude weak-coupling statement is already a theorem: the spectral thickness is bounded above and below by positive constants times `1/lambda`. The unresolved part of this investigation is whether thickness is nonincreasing for every positive coupling. A precise asymptotic constant is a stronger question and is not supplied by the cited theorem.

`PROOF.md` states the exact target, gives elementary obstruction proofs and a conditional finite-gap monotonicity lemma, and identifies the missing uniform estimate. `RESEARCH_LOG.md` records the five distinct routes. `SOURCES.md` identifies the primary sources and the limits of the literature check.

## Reproduce

Requires Python 3, NumPy and SciPy:

```sh
OPENBLAS_NUM_THREADS=1 python compute_controls.py --output replay.json
```

The exact rational controls check 1,536 finite-gap configurations, six middle-third Cantor construction levels, and 120 transfer-matrix identities. Nine free-operator calibrations and thirty-six finite spectral-approximation cases use floating-point arithmetic. They are not interval-certified bounds on infinite-spectrum thickness. Small roundoff differences between numerical-library versions are expected.

## Audit reconciliation

This corrected release preserves the initial author freeze in `original_author/` and the complete original independent audit in `audit/original/`, byte for byte. `CHANGE_LEDGER.md` and `CORRECTIONS.diff` identify every changed author file. The finite-gap lemma now explicitly requires a nonempty collection and C1 regularity of all hull and gap endpoints. The blocker formula handles equal-size ties explicitly, and the sufficient presentation comparison requires a bijection covering every presentation. A separately written true-gap exhaustion proof clarifies the generic limiting step without identifying the numerical covers with true-gap fillers or asserting a uniform coupling comparison.

`AUTHOR_SHA256SUMS` binds the seven current author files; `SHA256SUMS` binds the entire corrected release, including preserved originals and audit files. The original audit accepts the unsolved disposition subject to the recorded corrections. Binding review of this corrected release remains pending. No remote writes have been performed.


To rerun the preserved audit in this release layout (requires SymPy), use:

```sh
(cd original_author && sha256sum -c SHA256SUMS)
(cd audit/original && sha256sum -c SHA256SUMS)
OPENBLAS_NUM_THREADS=1 python audit/original/independent_controls.py --author original_author --output audit_replay.json
```

The archived audit's README retains its original sibling-directory instructions as historical evidence; the commands above adapt the paths without modifying that archive. Write generated replay outputs outside the release when rechecking its full manifest.
