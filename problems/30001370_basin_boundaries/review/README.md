# Review reproduction

This independent AI-assisted review contains no raw source PDFs or private coordination material. The analytic verdict is in ADVERSARIAL_REVIEW.md.

Run `python check_independent.py` using Python's standard library and compare stdout byte-for-byte with INDEPENDENT_CHECKS.json. The author replays require SymPy (reviewed with 1.14) and are recorded in AUTHOR_REPLAY.json. Source hashes and immutable remote raw Git blob checks are recorded in INTEGRITY.json and REMOTE_BINDING.json. The finite controls complement, rather than replace, the analytic source/proof audit.
