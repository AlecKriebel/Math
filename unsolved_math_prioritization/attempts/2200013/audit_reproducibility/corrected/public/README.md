# Binomial tropical corners: negative resolution

Problem 2200013 / AMR-021-0013, ranked-program entry 1031.

**Result:** a fully supported rational polynomial of actual degree 200000000000000000100 has at least four distinct negative roots and exactly three distinct binomial-weighted tropical corners. Read PROOF.md for the construction, elementary proof, convention audit, and attribution. The proof specifies the enormous polynomial compactly and never requires expanding it.

This is a consequence of the small-curvature obstruction already established by Forsgård–Novikov–Shapiro, with an explicit reconstructed witness and full-support perturbation. It is not presented as a newly discovered obstruction. The target's repetition as a conjecture in a 2024 source is disclosed and reconciled in PROOF.md.

## Verification contract

Python 3.12+ with standard library only is sufficient. The controls use integers and fractions, no numerical root estimates. They verify five strict signs, seed coefficients, denominator lower bounds, the sign-preserving perturbation estimate, the binomial-ratio bound, strict upper-hull inequalities, and degree/convention data. They do not enumerate all coefficients or prove that there are exactly four real roots.

Basic check, from this directory:

    python -I -B verify_math.py certificate.json

Repeat with -O and -OO. The code contains no assertion-dependent checks. The source-free directory is designed for read-only execution from an unrelated working directory.

For integrity-gated replay, obtain the manifest SHA-256 from a trusted independent handoff, not from a file in the slice you are verifying. First verify the separately supplied bootstrap's hash against that handoff. The bootstrap pins both replay.py and the external manifest, then starts isolated replay. Alternatively, independently verify replay.py's supplied hash and run:

    python -I -B replay.py --root PUBLIC_DIRECTORY --manifest EXTERNAL_MANIFEST --manifest-sha256 TRUSTED_EXTERNAL_DIGEST

The manifest must remain outside this directory. Replay rejects extra/missing files, bad sizes/digests, unsafe filenames, duplicate JSON keys, and symlinked inputs. Isolated Python startup prevents a hostile working directory or PYTHONPATH from shadowing standard-library modules.

The external audit report records normal/-O/-OO runs, genuine nonroot read-only hostile-directory replay, failed write probes, math mutations and packaging mutations. Hash integrity establishes identity, not mathematical correctness; an independent reader must still audit the proof.

## Contents and release boundary

- PROOF.md: authored mathematical argument and references
- certificate.json: compact authored construction parameters
- verify_math.py: exact finite mathematical controls
- replay.py: integrity gate and isolated runner
- RESULT.json: machine-readable scope/status
- sources.json: public source metadata, hashes, and inspection history
- README.md: this file

No third-party source text, source PDFs, source dataset contents, or private coordination material is included. No remote write or publication is performed by these tools.
