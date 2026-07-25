# Anchored integer-row energy search

This directory is a floating-point discovery experiment.  It combines an
atomic height grid, integer contact/antipode counts, and local harmonic moment
matrices for one anchored code point.

Nothing here is a proof or an upper-bound certificate.  The three JSON files
under `results/` are small diagnostic runs retained so the interrupted lane can
be reconstructed.  A future continuation would need an exact dual, a proof on
the full continuous semialgebraic domain, and an independent verifier before
any output could enter the claims ledger as more than numerical evidence.

Example discovery run:

```sh
python3 search.py --help
```

The script requires NumPy and CVXPY.  It is not part of the exact smoke test.
