# Numerical search in the 18-antipode / five-cycle branch

This is an unrestricted floating-point realization search inside the exact
structural branch with 18 antipodal pairs and a five-point residual cycle.
The objective is the largest of the projective-line, line/core, residual-chord,
and transformed cycle loads.  A value at most `1/2` would give a genuine
41-point construction.

No feasible construction was found.  The best stored common load is about
`0.54248`, safely above `1/2`.  The two portfolios retain seeds, coordinates,
software metadata, and search histories; they are negative numerical evidence,
not a nonexistence proof.

The script requires NumPy and SciPy.  Recompute a portfolio with:

```sh
python3 search.py --help
```
