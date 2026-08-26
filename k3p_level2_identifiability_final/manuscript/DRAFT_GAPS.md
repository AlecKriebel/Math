# Manuscript draft gaps

This file is deliberately separate from the theorem statements.  It records
integration work that must close before the sources are promoted to a final
submission build.

1. **Post-revision release replay.**  Complete at exact pushed candidate
   commit `7b4cdd3197e6d650abafc263cbc8a568d09ddf9f`: the clean quick/full suites,
   one unified 45-command all-producer replay, two-build source reproduction
   for both PDFs, and deterministic compact/full archive double-builds all
   passed.  The sealed theorem artifacts retain their pre-execution gate list
   to preserve the exact candidate binding; the post-run ledger records the
   completed machine gates.

2. **Author and post-typesetting review.**  Independent mathematical and
   evidence audits of the targeted bridge, sunlet, genericity, and noncut-
   compression revisions pass, as does the commit-bound
   article--supplement--archive cross-check.  Final human author review remains
   required before submission promotion.

3. **Bibliographic/release metadata.**  No DOI or license is asserted.  If a
   real DOI is minted or the user chooses licenses, rebuild the sources from
   that metadata.  Do not invent either.  Journal-specific declarations and
   any corresponding-email field remain outside this mathematical draft
   until supplied by the user.

4. **Remaining typesetting gate.**  The canonical article and reader
   supplement have been compiled with a fixed source timestamp, rendered
   page by page, visually inspected, checked for embedded fonts and TeX
   warnings, and reproduced byte for byte in independent build directories.
   Journal-specific manuscripts and cover letters remain blocked on the
   author-confirmed declaration, address, license, and persistent-archive
   metadata recorded under `submission/`; exact reproduction from the final
   sealed source archives must still be checked after those fields are fixed.
