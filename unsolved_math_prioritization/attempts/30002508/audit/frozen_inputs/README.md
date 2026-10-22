# Continuity and strict monotonicity of Nyman–Beurling distances

Problem 30002508 (OWR-12866-018), from M. Balazard's questions in Oberwolfach Report 06/2014, p. 390.

**Result: unsolved after five distinct approaches.** The full continuity and strict-decrease questions are not resolved, and no new theorem-level novelty is claimed.

This packet proves the following partial facts:

- Left-continuity and a precise right-jump projection criterion.
- Positivity of the distance at every finite cutoff, using a finite-range Möbius transform.
- Strict increase of the approximation spaces; an exact explanation of why this does not prove strict decrease of the distances.
- Explicit, exactly reproducible rational dual lower bounds.
- Strict improvement from the natural endpoint extension at cutoff 1.

It also distinguishes Jousse's fixed-finite-tuple continuity theorem from the interval-of-generators question and identifies the unbounded-term and unbounded-coefficient obstacles to passing to the limit.

## Files

- `PROOF.md`: statements, proofs, and remaining gaps.
- `SOURCES.md`: primary-source locations and scope checks.
- `RESEARCH_LOG.md`: five approach records with checkpoints.
- `RESULT.json`: machine-readable outcome.
- `verify_controls.py` and `control_results.json`: standard-library exact-rational tests.
- `SHA256SUMS`: file hashes for this author packet.

## Reproduce

From this directory, run `python3 verify_controls.py`. It regenerates `control_results.json`. All witness arithmetic is exact rational arithmetic. The rational sample checks supplement the proof of annihilation for the entire real parameter interval; they are not substituted for that proof.

No computation claims to certify right-continuity or strict monotonicity of the full infinite-dimensional distance.
