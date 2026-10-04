# Rubel's L-atoms: verification and a planar-domain consequence

Problem **2305055 / AMR-022-5055**, queue rank 576.

The unit-disk conjecture has a prior public proof: DannyExperiments,
*Rubel's L-atoms on the disk and a several-variable counterexample*,
Version 2.1, public release 1.0.0 (5 August 2026). This packet reconstructs
and checks the relevant argument rather than claiming a new disk solution.

The conclusion is affirmative: a nonconstant holomorphic function on the
disk is an L-atom precisely when it is injective. The proof uses ordinary
Runge approximation and Rouché's theorem to construct a surjective ordered
partner separating a nontrivial fiber.

A separately identified elementary consequence covers **every plane domain**,
bounded or unbounded, when source-boundary approach means leaving every compact
subset. The additional separator is

\[
b(z)=\frac{\alpha(z)-c}{(z-p)^m},\qquad
c=\alpha(p)=\alpha(q),\ p\ne q,\quad m=\operatorname{ord}_p(\alpha-c).
\]

Its singularity at p is removable, it is bounded on inverse images of compact
subsets of the actual range of alpha, and it separates p from q. No originality
claim is made for this consequence. Arbitrary open Riemann surfaces and other
interpretations of the general-domain question are not classified here.

## Files

- `PROOF.md`: complete reconstruction, including the infinite construction
- `EXACT_CLAIM.md`: definitions, ordering direction, scope and exclusions
- `SOURCE_AUDIT.md`, `sources.json`: provenance, prior work and literature limits
- `APPROACH_LOG.md`: one substantive source-verification/reconstruction turn
- `verify.py`, `verification.json`: reproducible exact finite controls
- `STATUS.json`: frozen author disposition, pending independent review
- `SHA256SUMS`: integrity manifest for the author packet

## Reproduce

Run `python3 verify.py` from this directory. Its JSON output must match
`verification.json`. Run `sha256sum -c SHA256SUMS` to check the frozen files.
Python 3.10+ and its standard library suffice.

The controls check algebra, summable error bounds, model zero locations and
deliberately invalid shortcuts. They do not construct the infinite Runge
approximant or mechanically prove the analytic theorem. The complete proof is
the mathematical evidence.

This is AI-assisted, unrefereed mathematical work. The external release's AI
audits and partial Lean core are not treated as proof certificates. This
author packet still requires an independent mathematical audit.

Prior source: [immutable manuscript](https://github.com/DannyExperiments/rubel-l-atoms/blob/65b6668e63e7fa3aec7ff28e36396f0a59af2aa9/paper/manuscript.tex).
Original problem: [Hayman–Lingham, Problem 5.55, p. 106](https://arxiv.org/pdf/1809.07200v2).
