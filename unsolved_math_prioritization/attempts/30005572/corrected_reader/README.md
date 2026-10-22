# Eisenstein maps from Bianchi homology to K2

This is a complete partial-results reader for problem 30005572, frozen on 14 October 2026. The original full construction remains **UNSOLVED**. No novelty claim is made.

Start with [READER.md](READER.md). It explains the construction target, the strongest precisely restricted results, their relationships, and the remaining obligations. [PROOF_INDEX.md](PROOF_INDEX.md) links 34 full proof and addendum texts, their dependencies, two essential mathematical qualifications, and 22 internal acceptance reports.

These are AI-authored arguments subjected to separate internal AI mathematical review. The review records are not journal peer review, human expert validation, or formal proof-assistant certificates. Every result must be read with its hypotheses and the source-sign and model-transport qualifications.

## Contents

- [Reader](READER.md): coherent overview and mathematical scope
- [Full proof index](PROOF_INDEX.md): complete arguments and dependencies
- [Corrections](CORRECTIONS.md): rejected steps, repairs, and preserved limitations
- [References](REFERENCES.md): public scholarly sources and inspection boundaries
- [Checks](CHECKS.md): 21 runnable finite algebra and example checks
- [Preservation inventory](PRESERVATION_INVENTORY.json): original and derivative hashes
- [Sanitization inventory](SANITIZATION_INVENTORY.json): exact neutral transformation metadata
- [File manifest](FILE_MANIFEST.json): hashes and sizes of the distributable files

All five shared mathematical passes are complete. This edition assembles their accepted results; it does not add a further mathematical claim. The public reader contains no source PDFs or copied source documents, raw dataset, private coordination files, private storage paths, or original mixed manifests. Public source metadata and inspection limitations are retained.

## Reproduce the finite checks

Use Python 3 with SymPy installed in your chosen environment. From this directory:

    python run_checks.py --optimized --output /tmp/eisenstein-checks.json

The runner copies each script into a fresh temporary directory, preserves its frozen expected output, and compares the resulting JSON. It never writes into the original mathematical workspace. Assertion-based checks run only without optimization; explicit-runtime checks also run with -O and -OO. See [CHECKS.md](CHECKS.md) for the verification boundary.

## Packaging status correction

This separately preserved derivative corrects stale preliminary acceptance-status wording for P25–P27 in the index and preservation inventory. The completed formal internal report A16 was already included and pins all three proof texts. All proofs, qualifications, internal review reports, checks, and source metadata are unchanged from the input reader. See the [explicit change mapping](PACKAGING_CORRECTIONS.json). VALIDATION.json and REPLAY_RESULTS.json retain the original assembly records; independent packaging verification is supplied with this derivative.
