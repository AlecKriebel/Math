# Rank 549 / 30000552 / OWR-1319-022

**Disposition: already_solved; 1/5 substantive source-and-proof verification.**

The general cocompact-metric implication is false, by Breuillard's published counterexample in [Groups, Geometry, and Dynamics 8 (2014), §8.3(A)](https://doi.org/10.4171/GGD/244). On R×H3(R), two complete length metrics under the same discrete cocompact lattice action satisfy a uniform square-root difference bound, but the difference equals 4√t on explicit points. This package supplies a self-contained reconstruction and verifies the exact 2006 question. It makes no novelty claim.

- `PROOF.md`: complete construction, metric properties, cocompactness, uniform quantifiers and counterexample
- `SOURCE_GATE.md` and `SOURCES.json`: primary-source identity, access limitations and attribution
- `ATTEMPT_LOG.md`: one substantive prior-resolution verification and reason for stopping
- `verify.py` and `checks.json`: reproducible exact-arithmetic supplemental controls
- `SHA256SUMS`: author-package freeze; excludes itself

Run `python3 verify.py --check checks.json` and `sha256sum -c SHA256SUMS` from this directory. Standard-library Python 3 is sufficient. Finite checks supplement the written proof; they cannot establish the universal analytic claims on their own.

No source PDFs, website copies, extracted source text or unrelated records belong in this public package. Independent mathematical review, when supplied, should be identified separately and should not be described as external peer review.
