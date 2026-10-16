# DS objectwise-kernel / socle-filtration audit

This package gives a source-normalized mathematical audit of OWR Conjecture 9 (52/2018). It does not settle the full conjecture, and claims no novelty.

- `MATHEMATICAL_AUDIT.md`: exact category/scalar/rank/socle conventions; credited first-layer consequence; explicit failures of two tempting proof shortcuts; restricted tensor-product and localization diagnostics; exact remaining gap.
- `check_examples.py`: standard-library exact checks of the finite diagnostic examples. Run with `python3 check_examples.py`, `python3 -O check_examples.py`, and `python3 -OO check_examples.py`.
- `SOURCE_METADATA.json`: public source titles, URLs, locally retrieved PDF byte counts and SHA-256 hashes, inspection scope, and version warnings. The PDFs and source text are not part of this package.
- `VERIFICATION.json`: final run receipts and verification limits.
- `MANIFEST.json`: SHA-256 and byte count of the other package files.

This is an author self-audit, not independent acceptance. The checker does not verify imported representation-theory theorems, every integer parameter by enumeration, current openness, or the full socle-filtration conjecture. Its algebraic identities and their stated scope are explained in the mathematical audit.
