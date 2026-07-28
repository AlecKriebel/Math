# Noncommutative Comparative Statics

This folder contains a foundational research program for **noncommutative
comparative statics (NCS)**: the study of how locally chosen repairs of a
constrained system compose when its external conditions change.

The central question is not only “what equilibrium corresponds to this
parameter?” but:

> If two external changes are compatible, do the system's least-disruptive
> responses commute, and how much persistent order-debt remains when they do
> not?

The proposed field is deliberately positioned between comparative statics,
variational analysis, rate-independent systems, differential geometry,
rewriting/confluence theory, and algorithmic recourse. Standard smooth
connection theory is a limiting case, not a novelty claim.

## Status

This is an honestly delimited **candidate research program**, not a claim that
an established branch or a new deep theorem has already been created.
Adversarial review found exact prior-art collisions for the initial smooth
geometry, pseudoinverse rectification, and guard-margin results. Those pieces
are retained only as imported baselines.

The surviving proposal is the combined modeling discipline:

1. declare which external intervention paths mean the same thing;
2. model how a current state is carried along each path;
3. report directional failure, common failure, and successful-outcome
   discrepancy separately;
4. compare reset and carry semantics, scaling regimes, and rectifiability;
5. test longer compositions prospectively.

Its field status should depend on future partial-functor stability theorems
and cross-domain empirical successes.

The finished 17-page paper is at
[`output/pdf/paper.pdf`](output/pdf/paper.pdf). The complete adversarial audit
trail is in `reviews/`, and the timestamped decision record is
`RESEARCH_LOG.md`.

## Folder map

- `RESEARCH_LOG.md` — timestamped decisions and checkpoints.
- `checkpoints/` — frozen checkpoint statements.
- `reviews/` — adversarial reviews and dispositions.
- `paper/` — LaTeX source and bibliography.
- `examples/` — exact and numerical worked examples.
- `examples/archive/` — checks retained from the explicitly rejected first
  foundation draft.
- `output/pdf/` — final rendered paper.
- `tmp/pdfs/` — temporary page renders used for visual verification.

No external communication is initiated by this project.

## Reproduce the formal checks

The current verification script declares its two dependencies in
`examples/requirements.txt`. In an isolated Python environment:

```text
python -m pip install -r examples/requirements.txt
python examples/verify_revised_foundations.py \
  --output examples/results/revised_foundation_checks.json
```
