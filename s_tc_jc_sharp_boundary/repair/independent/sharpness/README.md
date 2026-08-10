# Independent theta-sharpness gate

This directory is a standard-library-only reconstruction of the proposed
four-leaf and all-`n` theta sharpness theorem.  It does not import or execute
the historical graph/Fourier verifiers and does not use inherited status
strings as evidence.

The deterministic verification command, run from the repository root, is:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 python3 s_tc_jc_sharp_boundary/repair/independent/sharpness/verify_sharpness.py --instance s_tc_jc_sharp_boundary/repair/independent/sharpness/instance.json --output s_tc_jc_sharp_boundary/repair/independent/sharpness/certificate.json
```

Expected terminal output begins with `PASS final_verdict=PROVED`.  The exact
certificate hash is recorded in the gate review and `MANIFEST.sha256`.

Files:

- `instance.json`: primitive status-free arcs, points, and orbit labels;
- `verify_sharpness.py`: independent graph, exact-algebra, Fourier, Jacobian,
  invariant, mutation, and cherry-substitution verifier;
- `certificate.json`: canonical deterministic output;
- `verification_output.txt`: short successful transcript;
- `RESEARCH_LOG.md`: checkpoints and convention findings;
- `MANIFEST.sha256`: hashes of the final audit artifacts.

The implementation uses exact `fractions.Fraction` arithmetic, a two-basis
implementation of `Q(beta)`, exact rational intervals, sparse polynomials,
two determinant algorithms, and graph algorithms written in this file.

