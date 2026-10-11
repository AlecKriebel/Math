# Monochromatic empty triangles: independently accepted local obstructions

Problem 3081 / OPG-2435, queue rank 926. **Unsolved, 2/5 substantive approaches.**

The unchanged original and its exact independent acceptance are preserved in full. Read [the author report](original/REPORT.md), [the complete audit](audit/AUDIT_REPORT.md), and [the exact acceptance](audit/ACCEPTANCE.json).

## What is established

- For every k >= 1, the parabola construction reuses one opposite-color blocker in 2k+1 pivot-fan incidences. It defeats constant blocker capacity for that proof route. Its empty-triangle count is binom(2k+1,3)-k^2, which is cubic; it is not an asymptotic counterexample.
- A balanced eight-point certificate has E0=0 and E1=8. It obstructs unconditional local conversion of almost-empty triangles into empty ones; it does not supply arbitrarily large empty-free sets.
- The original quadratic conjecture remains unresolved. No new asymptotic bound, exhaustive literature coverage, or novelty claim is made.

## Source and validation boundaries

The audit independently checks the three complete corpus identities and eight pinned source files. Explicit September 2026 v2 PDFs were matched to the original source pins. The quadratic almost-empty result concerns E0+E1; the cited truly empty lower bound concerns E0 of order n^(4/3). Both 2026 sources are preprints. See [public source metadata](audit/SOURCE_AUDIT.json).

The frozen audit records 38 actual full-input cases: six expected successes and 32 expected failures. Its four later frozen, source-free replays are separately preserved in the independent audit receipt; the source-free author replay contains 32 cases. These counts are not combined into a claim that the asymptotic conjecture has been checked.

## Reproduction

Authenticate verify_publication.py against its externally supplied SHA-256 before running it. The wrapper pins PUBLICATION_MANIFEST.json, the original and audit ZIPs, both external manifests, and the frozen audit receipt. It rejects changed, missing, unexpected, hidden, or nonregular members and authenticates all files before executing any archived code. Internal self-consistency alone does not authenticate a changed wrapper.

    python3 -I -B verify_publication.py
    python3 -I -B -O verify_publication.py

For complete locally authorized inputs, provide both directories:

    python3 -I -B verify_publication.py --corpus-dir /authorized/corpora --source-dir /authorized/sources

The corpus directory contains catalog.json, problems.json, and research_results.json. The source directory contains the eight successfully retrieved filenames in original/SOURCE_VERIFICATION.json. Inputs are copied to fresh temporary sibling directories for isolated normal/optimized replay. No source or corpus contents are printed or published. Omit both arguments for source-free geometry and integrity replay; this does not verify absent private inputs.

The wrapper is an integrity and replay tool, not a formal proof assistant. The all-k result also depends on its written mathematical proof. Published originals retain their historical statements that publication had not yet occurred; this wrapper and research log document the later packaging step without rewriting history.
