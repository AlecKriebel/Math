# Independent website release QA

Checkpoint: 2026-10-24. Completion: **100% of assigned static/content/download review**. Decision: **PASS; no required correction found in the final plain-layout files**. The parent is separately checking the browser presentation and will perform the production smoke check. No website source, deployment, redirect, or Git state was changed by this reviewer.

## Reviewed version

The final review was repeated after the plain blog-style redesign. File identities and the exact timestamp are in `reviewed-file-identities.json`.

- Research index SHA-256: `128b4c24cbe0bc0caac7240cb0b4cccf28b43b1b6cfb8a850d106799b07f0acc`.
- Paper page SHA-256: `254f1caf98c8326f226f1eff1b2ffb53f0d16eda2fc50e61a4f3c0c5e5b5ed7a`.

## Links, responses, and structure

`check_site.py` parsed both pages and followed every local `href`/`src`, including all same-page anchors. All target files exist; all linked fragments resolve; IDs are unique. Twelve distinct preview URLs returned HTTP 200 and bytes exactly equal to their local files: the research index, paper page, stylesheet, PDF, source ZIP, BibTeX, review note, sitemap, robots file, favicon, homepage, and blog index. The removed decorative images are no longer dependencies.

HTML, CSS, PDF, ZIP, plain text, XML, and favicon responses have appropriate local content types. BibTeX is served as `application/octet-stream`, which is suitable for its explicit download link. The PDF is seven pages, as advertised. Production content types and Firebase slash routing remain a post-deployment check; the local Python preview is not evidence of the production response headers.

Both pages have English language declarations, one main landmark and one H1, consistent heading levels, labeled navigation, a working skip-link target, and no unresolved ARIA references. The comparison table has a caption and scoped row/column headers. There are no unlabeled images or generic elements carrying unsupported accessible labels in the final layout. Native link styling/focus behavior remains available. This is a static accessibility check, not screen-reader or formal WCAG certification; visual/keyboard testing belongs to the parent's browser review. The frozen original PDF is untagged and has not been altered.

## Metadata and immutable downloads

All **18 metadata and identity comparisons** in `metadata-results.json` passed. Canonical URLs, Open Graph URLs, JSON-LD URLs, the citation PDF URL, and the two sitemap entries agree. JSON-LD parses correctly. The author, ORCID, title, DOI, version 1.0.0, preprint status, license, and 22 October 2026 publication date agree with the saved public Zenodo record. The webpage creation/modification dates and sitemap last-modified dates consistently use 24 October 2026. BibTeX matches the title, author, DOI, year, month, version, and preprint status. The schema identifies the article prose as CC BY 4.0; the visible text separately identifies verification code as MIT.

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| PDF | 85,728 | `dc0126e8f3da1baf7743b462ac3e6962f5969b5fec4d7451e225a19d9762ef08` |
| Source/verification ZIP | 238,091 | `ee7c9fcf576ef068834662e3d97e679ee1c5578b87db7d230a6facf4ce7d194e` |

Both files are byte-identical to the freshly downloaded source files saved by the parent task, and both match the sizes and MD5 checksums in the saved public Zenodo API record. The ZIP passes its CRC check. Its embedded paper is identical to the separately served PDF. Its certificate has SHA-256 `6573c55f2998f4576a050a0757ca74f1cae9cadfa96ec61c69b181c530f79c4f`. All three hashes agree with `review.txt`.

## Scientific wording and review-note truthfulness

The precise statement, displayed formula, normalization, vertex counts, and square degree agree with the archived manuscript/package and the analytic, certificate, and scope reviews. The page consistently distinguishes the square's proved upper bound from an exact expectation. It states the nonunimodular setting, does not claim a unimodular/Cayley counterexample, and explains why finite-support currents and free exhaustion are essential. It credits prior graph/electrical methods and makes no firstness or human-peer-review claim.

A separate scope reviewer read both page bodies, metadata, and review note and reported PASS; see `../scope/FINAL_SITE_COPY_CHECK.md`. Its scientific verdict was checked against the final simplified wording. The layout rewrite retains the scoped scientific statements.

The review note's factual assertions match the saved evidence:

- The analytic and adversarial reviews report complete free-exhaustion/limit checks and independent exact finite calculations, including a 2,047-vertex case.
- The computational report confirms 3,070 vertices, 19,931 edges, 40 targets, 797,240 integer currents, and 122,800 divergence equations, plus the exact energy and normal/optimized deposited replay.
- The hostile-input report records 161 expected outcomes, including 145 rejections, and documents the parser/API leniencies rather than claiming strict generic JSON validation.
- The scope report supports the unrestricted vertex-transitive question and the explicit normalization convention, with the literature-search limits stated.

The review note appropriately calls these internal AI-assisted checks, distinguishes them from human refereeing and proof-assistant certification, and does not imply that finite computation alone establishes the infinite theorem. Its reproduction commands name scripts that exist at the archive root; the included README supplies the more isolated invocation and Python version requirement.

## Homepage and scope control

The homepage diff equals the intended replacement set exactly: its two old GitHub research links become `/research/`, the card title becomes “Research,” and the short card description is updated. No unrelated homepage content changed. The only other modified tracked public file is `robots.txt`, which adds the research sitemap; the new files are confined to `public/research/`. Firebase configuration is unchanged. The earlier GitHub research archive remains linked and no redirect migration was introduced.

## Evidence and remaining check

- `static-results.json`: exact page hashes, local references, structural facts, schema, HTTP results, and artifact identities.
- `metadata-results.json`: the 18 explicit metadata/identity comparisons.
- `reviewed-file-identities.json`: hashes and sizes for every release-relevant file.
- `check_site.py`: narrow read-only replay of local link, response, structure, and artifact checks.

Before considering the live publication verified, the parent should confirm production HTTP status/content and artifact hashes. That check cannot be performed for these unpublished pages yet. GitHub Pages redirects remain subject to the user's later review gate.
