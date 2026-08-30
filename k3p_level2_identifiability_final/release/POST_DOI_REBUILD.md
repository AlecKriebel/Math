# DOI handling after direct deposit

Version 1.0.0 intentionally contains no predicted DOI.  Zenodo's issued DOI
and landing page are the authoritative record metadata.

After publication:

1. Record the issued DOI and landing URL in the release ledger and future
   citation metadata.
2. Download every deposited asset and verify it against `SHA256SUMS`.
3. Do not rebuild, replace, move, or retag version 1.0.0 solely to embed its
   DOI.
4. A later manuscript revision may cite the DOI in its bytes, but it must use
   a new version, immutable commit, tag, manifest, and checksum set.
