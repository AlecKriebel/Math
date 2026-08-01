# Strong level-2 phylogenetic-network identifiability

This directory contains an independent, exact investigation of observational
equivalence for binary strongly tree-child level-2 phylogenetic networks under
JC, K2P, and K3P substitution models.

Milestone 1 is complete: the inherited theta pendant transfer persists with a
full-dimensional regular overlap under JC, but explicit quartic invariants
generically separate the pair under K2P and K3P.  See
`notes/MILESTONE_1_MODEL_ROBUSTNESS.md`.

Milestone 2 is complete at the generator-core level: every nontrivial level-2
blob reduces to a cycle or theta template, and there are exactly five rooted
orientation cores (one cycle and four theta).  See
`notes/MILESTONE_2_GENERATOR_ATLAS.md`.

Claims are labelled `PROVED`, `EXACTLY COMPUTED`, `INTERVAL CERTIFIED`,
`NUMERICALLY OBSERVED`, `CONJECTURED`, or `UNRESOLVED`.

No external literature is used during discovery.

## Replay

Create the local environment once with

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

Then run

```sh
./run_all.sh
```
