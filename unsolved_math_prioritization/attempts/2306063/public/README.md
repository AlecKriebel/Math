# Rank 585: Function Theory 6.63

**Unsolved after five substantive approaches.** No general stability theorem or fine-topology counterexample was obtained. No new-result or priority claim is made.

The target concerns arbitrary positive continuous tolerances epsilon(x). The older desk report's replacement by a constant epsilon changes the question. Full scope and the correction are in `PROOF.md` and `SOURCE_GATE.md`.

## What was proved

- Exact uniformization of affine sewings: slope one gives a parabolic end; every other positive slope gives a hyperbolic end.
- A concrete quasiconformal comparison theorem under derivative and displacement bounds, plus admissible fine-small perturbations for which those bounds fail.
- A restricted invariant-one-form reconstruction of the classical expanding-derivative hyperbolicity criterion, with explicit finite-energy estimates.
- Parabolic sewings that agree with a hyperbolic affine sewing on arbitrarily long initial intervals. They disprove compact-open stability, not the question's fine stability.
- The exact exponential reduction to a two-sided real sewing with one side fixed, a fine log-singular positive-side approximation lemma, and the capacity obstruction to applying Bishop's whole-circle theorem directly.

`PROOF.md` includes all proofs and states the remaining gap after each route. `ATTEMPT_LOG.md` records the five attempts and completion estimate. `SOURCE_MANIFEST.json` identifies sources and provenance limits. No downloaded source PDFs, raw corpus, or private coordination records are included here.

## Reproduce controls

Python 3.10+ standard library only; no network, installs, large search, or external credentials are needed.

    python3 verify_manifest.py
    python3 verify.py

The second command should reproduce `CHECKS.json`: 1,718 assertions, with exact rational arithmetic where indicated and separately labeled floating-point diagnostics. These checks validate formula controls; they do not decide an infinite-end type or formally verify the proof. The manifest verifier checks the strict public file inventory and byte hashes.

Publication requires the separate independent mathematical review. The package does not assert that such a review has already happened. No remote changes were made during authoring.
