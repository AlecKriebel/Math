# Reproduce without modifying frozen evidence

This checkpoint remains unsolved after five approaches. The author packet
and independent audit are unchanged, separately hash-bound artifacts.
The independent audit accepts the partial results and finite checks; it
is not expert peer review and does not establish the universal inequality.

Run in a disposable copy because verification scripts regenerate JSON.
From this directory:

```sh
work=$(mktemp -d)
cp -R submission audit-independent "$work/"
cp -R "$work/submission" "$work/audit-independent/reproduction"
python3 "$work/submission/verify.py"
python3 "$work/audit-independent/independent_checks.py"
```

The first verifier needs Python's standard library. The second needs
mpmath. Optional optimizer replays also require NumPy and SciPy; see
submission/exploratory/ENVIRONMENT.json for the recorded versions, seeds,
coefficient truncations, and search limits.

The published exact grid is certified using rational arithmetic. The
80-digit and independently reproduced 120-digit checks of saved optimizer
points are diagnostic calculations, not interval certificates. The formal
Robertson control violates the proposed coefficient inequality but is
explicitly proved nonunivalent, so it is not a counterexample to the target.

Interpret regenerated Python-version metadata separately from arithmetic
results if using a different Python interpreter. Validate original file
bytes against submission/MANIFEST.json and audit-independent/AUDIT_MANIFEST.json
before the disposable replay. Do not overwrite frozen outputs.
