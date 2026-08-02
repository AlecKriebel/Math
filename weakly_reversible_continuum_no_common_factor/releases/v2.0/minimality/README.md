# Minimality package

`MINIMALITY_ANALYSIS.md` contains the manuscript-ready first-principles
proofs and a conservative audit of unresolved complexity gaps.

The proofs establish:

- three species are necessary without any graph hypothesis;
- stoichiometric rank at least two is always necessary;
- rank three is necessary for a three-species, one-linkage example;
- positive deficiency is necessary under weak reversibility;
- five complexes are necessary for every three-species weakly reversible
  example; and
- at least four reversible pairs are necessary under one linkage (three if
  multiple linkage classes are allowed).

No claim that ten complexes or ten reversible pairs are minimal is made.

The small companion arithmetic check can be run from the repository root:

```sh
.venv/bin/python weakly_reversible_continuum_no_common_factor/minimality/verify_complexity_arithmetic.py
```

It does not enumerate reaction networks and is not used as evidence for a
bounded-support impossibility claim.
