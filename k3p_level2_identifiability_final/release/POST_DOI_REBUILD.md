# Post-DOI rebuild

The first canonical package intentionally contains no invented DOI.  After
Zenodo issues the real DOI:

1. Record the exact DOI and landing URL in the article, supplement, repository
   citation metadata, data/code availability text, and submission packages.
2. Rebuild both PDFs from the updated committed source under the deterministic
   source-reproduction environment.
3. Run quick, full, PDF visual QA, byte-for-byte source reproduction, archive
   construction, archive verification, and clean-clone tests again.
4. Create a new immutable tag; never move the pre-DOI tag.
5. Add and audit an explicitly authorized post-DOI envelope schema; the current
   `k3p-final-release-envelope-v1` builder intentionally accepts only the
   pre-DOI state `NOT_MINTED` and must not be reused to claim a minted DOI.
6. Generate the new post-DOI envelope and checksum set for the new commit/tag.
7. Upload the DOI-bearing journal packages.  Preserve the prior package as a
   superseded immutable snapshot rather than overwriting it.
