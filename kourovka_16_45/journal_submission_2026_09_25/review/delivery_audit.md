# Independent delivery audit

Final checkpoint: 2026-09-26T04:24:05Z (25 September 2026, America/Los_Angeles).
Scoped completion estimate: **100%** toward a checked journal upload package;
this is not a probability that the theorem is correct or the journal accepts it.

**Disposition: PASS. No unresolved delivery blocker found.**

Frozen final kit: `output/Kourovka16_45_Bulletin_Submission_Kit.zip`

SHA-256:
`153f9e27ed03c814d5242418e0db2b4e38ccea31ffa9706423120fd546b3bd02`

## Scope and independence

This audit checks submission instructions, manuscript and supplement presentation,
metadata, reproducibility packaging, filenames, and distribution hygiene. Separate
agents are reviewing the complete mathematics and literature. This audit does not
claim external human peer review or proof-assistant certification. No journal
account was accessed; no person was contacted; no agreement was accepted; no
submission, commit, push, or original-source edit was performed by this reviewer.

## Checks completed

- Read the full main source and supplement source, README files, cover letter,
  preparation instructions, licensing statements, expected summaries, comparison
  programs and verifier entry points.
- Visually inspected all seven existing main-page renders and all three existing
  supplement-page renders. They have legible mathematics, consistent layout,
  sensible page breaks, and no detected clipping, collision or garbled glyphs.
  Subsequently rendered and inspected all ten current pages in this reviewer's
  own scratch directory. The final snapshot-URL change leaves page 7's rendering
  byte-identical; its final render was inspected once more. The final main PDF
  remains seven pages, and the final note remains three pages.
- Public [OJS instructions](https://journal.austms.org.au/ojs/index.php/Bulletin/about/submissions)
  confirm initial PDF, AMS-LaTeX, author ORCID, keywords, MSC2020, a self-contained
  abstract of at most 200 words, and alphabetic/numerically cited references.
  The package addresses these requirements and labels source/support uploads as
  conditional rather than inventing account-only form labels.
- The [journal preparation page](https://www.cambridge.org/core/journals/bulletin-of-the-australian-mathematical-society/information/author-instructions/preparing-your-materials)
  supports the substantive AI disclosure and repository publication. Formal
  publisher-hosted supplements require prior consultation; the instructions
  appropriately avoid assuming that route has been approved. Human accountability
  and unseen account declarations remain author responsibilities.
- Current expected Python/C++ summaries and the independent summary agree with
  the numerical claims in the README and explanatory supplement: complement 120,
  76 subgroups, 1,215,450 tested four-families, 67,525 triples, 30 line stabilizers,
  affine order 100,920, omission orders 120/6728/10092/16820, degree 5220, and the
  characteristic-11 witness.
- Reconstruction programs do not read saved certificates; comparison programs do.
  Mathematical checks use explicit exception/throw guards, not checks disabled by
  optimized Python execution. No network or shell execution was found in the
  verifiers. Generated outputs are directed to the documented build directory.
- Main/supplement PDF metadata correctly identify title and author; both are
  unencrypted and contain no JavaScript or forms. Initial observed lengths are
  seven and three pages, respectively.
- The official journal class retains its LPPL notice. No third-party paper is
  intended for the source or reproduction upload archive; final archive contents
  will be checked independently.

## Findings and disposition

1. **Resolved:** the initial manuscript cited only the earlier Zenodo
   version while instructions referred to the current public package. The root
   agent inserted the current immutable supplement commit
   `be0f06ee0c61739dcda5629e2c4223e7da7951d3`. The final PDF annotation, source,
   cover letter, metadata, and manifest all use that exact commit. Unauthenticated
   public raw GitHub retrieval of its README and amended verifier returns HTTP
   200 and exactly matches the packaged bytes.
2. **Author metadata confirmed:** the root agent reports explicit human replies
   confirming San Francisco, USA; `me@aleckriebel.com`; no external funding; and no
   competing interests. These are therefore not inferred declarations.
3. **Resolved minor inherited documentation issue:** the first Python verifier's docstring
   points to `proof.tex / proof.pdf`, old filenames absent from the reproduction
   package in the initial candidate. The coordinator corrected this comment and
   published the new immutable snapshot above before building the final package.
   Runtime logic was unchanged, and the complete final package was replayed.
4. **Honest provenance limit:** historical application/model build identifiers were
   not consistently recorded. The disclosure says so rather than fabricating
   versions. Cambridge asks for the tool/version; the omission is transparently
   reported and editorial acceptance cannot be guaranteed.

## Final package gates

| Gate | Result |
|---|---|
| Outer and both inner ZIPs | CRC checks pass; no absolute/traversal paths, symlinks, encrypted entries, duplicate/case-colliding names, build trees, Finder metadata or Git metadata. |
| Allowlisted contents | Eight outer files, sixteen reproduction files, three source files. No unlicensed third-party papers, input drafts, scratch reviews, compiled executable, copied journal agreement or private transcript included. |
| Manifest and checksums | Every outer file matches `evidence/package_manifest.json`, `upload/`, and the bundled `SHA256SUMS`. All sixteen reproduction files equal their reviewed source counterparts. |
| Mathematical review continuity | UTF-8 source substring from `\begin{abstract}` to before `\section*{Reproducibility` hashes to `f183c53d8126b0ac23af28675ad24bae5619221b000e802479dfadb1520ffaf2`, exactly the final referee's reviewed payload. |
| Clean extraction | Extracted outside source directories into a fresh path containing a space. Supplied `make verify` exited successfully. |
| Exact reproduction | All three freshly executed implementations agree with expected files on all 76 actual matrix-subgroup sets; the two Python implementations agree on the complete affine-element digest; all mathematical summaries agree. The fresh C++ summary also equals its expected text byte-for-byte. |
| Expected-data preservation | Every expected file remains byte-identical after replay. Reconstruction reads no expected certificate. |
| Source rebuild | Extracted source builds using the documented Tectonic route. No overfull/underfull box, undefined reference/citation or TeX error was found. All seven pages' extracted text, page dimensions and hyperlink annotations match the kit's PDF. |
| Class provenance | Packaged `baustms.cls` matches the published unchanged SHA-256 `b5e53c7510ed44cd2673e30f7c60b2c09d4fdb77d057e9d61979ed537202fad3`; its LPPL notice is retained. |
| Metadata | Title, author, email, affiliation, ORCID, keywords, classifications, funding/conflict and AI statements agree across source, PDF and copy-ready metadata. Abstract is 122 whitespace-delimited words in metadata, under both 150 and 200. |
| Submission directions | Main PDF identified unambiguously; complete kit is not to be uploaded as the article. Optional source/support/cover-letter steps remain conditional on actual portal fields. |

The preserved machine-readable record `evidence/delivery_audit.json` combines
archive-member hashes, extraction and reproduction results, and the full
verification/rebuild logs. Scratch records and inspected PNGs remain under
`tmp/delivery_audit/`.

The exact manuscript PDF SHA-256 is
`61537c143e3d7da92d50658c0b695ad44af145e3e963b900b225d3f5c1db19a4`.
The exact reproduction-note PDF SHA-256 is
`987fbd9e774b4de6d1c537597d2662a89dae07430a6e7f9633f21e4640252e59`.

Remaining actions belong to the human author: approve and take responsibility
for the mathematics and disclosures, confirm originality/authorship/exclusivity,
read the actual logged-in declarations, enter any further contact details and
submit if desired. The account-only workflow was not accessed or certified.
Missing historical AI build records are disclosed honestly; an editor may ask
for further information. No correctness or journal-acceptance guarantee is made.
