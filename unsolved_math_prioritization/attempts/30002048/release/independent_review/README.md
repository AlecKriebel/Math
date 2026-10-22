# Independent audit packet

The scoped exceptional-unit results pass independent exact verification. One ancillary mathematical sentence and one notation ambiguity need correction. The all-degree conjecture remains unresolved.

- AUDIT.md: complete adversarial review, proof boundaries, source attribution, and exact corrections.
- independent_verify.py: fresh standard-library-only verifier; no author-code imports or dependence.
- independent_results.json: complete CRT, quartic, resultant, and irreducibility certificates.
- proposed_corrections.patch: two precise corrections, deliberately not applied to the frozen originals.
- STATUS.json: machine-readable disposition.
- SOURCES.json: source identity and provenance, without source text or source documents.
- VALIDATION.txt: frozen identity and reproduction checks.
- run.txt: independent standalone/comparison run information.
- MANIFEST.sha256: audit artifact hashes.

Run `python3 independent_verify.py` independently, or use `--author-json ../author/results.json` to compare every relevant author mathematical field after reconstructing it. Do not use Python -O. No network access, external library, source PDF, or author program is needed.
