# T3-2 workload-reactivation certification

This package certifies positive recurrence for every bimolecular weakly
reversible stochastic mass-action network with:

- at most three dynamically active species;
- at most two active linkage classes;
- arbitrary positive reaction-rate constants.

## One-command verification

```bash
./run_all.sh
```

This runs exact self-tests, pytest, the direct C++ atlas, the independent
Python atlas, the clean-room atlas, and a separate independent verifier.

## Build

```bash
cd manuscript
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

The finite computations verify structural certificates and mandatory
regressions. The infinite-state recurrence theorem is proved analytically.

## Scope

No theorem with three active linkage classes, four active species, or
molecularity greater than two is claimed. No literature or priority audit was
performed.
