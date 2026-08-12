# Website update draft

This directory contains a prepared, **undeployed** version-1.2.0 replacement
for `docs/papers/minimum-bell-setting-complexity/index.html`.

Before deployment:

1. replace all five current-version DOI tokens: paper, review PDF, source,
   checksum, and software;
2. replace the release-tag, `NEW_PUBLICATION_PDF_SHA256`, and every v1.1 tag
   link intended to describe the current v1.2 source or verifier;
3. update `citation_publication_date`, JSON-LD `datePublished` and
   `dateModified`, and the visible prepared/release date to the actual public
   release date;
4. copy the final version-1.2.0 paper and review PDFs into the live page;
5. regenerate the live page SHA-256 file;
6. validate HTML and JSON-LD and inspect desktop/mobile layouts;
7. preserve the visible table of July 30 version-1.1.0 DOI records;
8. commit and deploy only after author approval.

No live `docs/` file was changed in preparing this draft.
