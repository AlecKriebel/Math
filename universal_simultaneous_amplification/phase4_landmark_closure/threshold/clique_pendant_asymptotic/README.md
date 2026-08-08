# Growing clique--pendant endpoint asymptotics

This folder proves an asymptotic counterexample to the normalized product
inequality at fitness `r=3/2`.

Let `G_m` be the unweighted graph obtained from `K_{8m+1}` by adjoining `m`
leaves to one distinguished clique vertex.  Then

```text
rho_Bd(G_m,3/2) / rho_Bd(K_{9m+1},3/2) -> 32/27,
rho_dB(G_m,3/2) / rho_dB(K_{9m+1},3/2) -> 8/9,
product                                             -> 256/243 > 1.
```

Thus the product conjecture fails by a nonvanishing asymptotic margin.  The
family is not a simultaneous amplifier: dB is asymptotically suppressing.

- `CLIQUE_PENDANT_ASYMPTOTICS.md` contains the derivation and proof.
- `verify_asymptotic_constants.py` independently checks the exact quotient
  rows on a labelled graph and verifies every displayed algebraic constant.
- `FINITE_SANITY.md` records exact small-`m` absorption solves and separate
  larger sparse diagnostics; neither is used to prove the limits.
- `RESEARCH_LOG.md` records the scope and status.

Replay from the repository root with

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  universal_simultaneous_amplification/phase4_landmark_closure/threshold/clique_pendant_asymptotic/verify_asymptotic_constants.py
```
