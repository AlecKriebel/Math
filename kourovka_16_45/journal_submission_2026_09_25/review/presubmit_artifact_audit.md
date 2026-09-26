# Final pre-submission artifact audit

Status: **PASS — updated final package audited with no unresolved artifact correction**.
Review completion: **100% of the assigned final artifact-audit scope**.
Date: 25 September 2026, San Francisco (UTC completion recorded in the machine evidence).

## Exact object reviewed

`output/Kourovka16_45_Bulletin_Submission_Kit.zip`

SHA-256:
`0caefb445fc05456beb9d0b8dcd1351d33d9fd43458f5016b2731ba1319be1d6`

This review performed fresh checks of the current ZIP. A baseline pass preceded the lead reviewer's correction of historical wording and addition of the official Notebook repository link. The revised final kit above was then freshly extracted, rebuilt and rechecked. The baseline kit (`153f9e27ed03c814d5242418e0db2b4e38ccea31ffa9706423120fd546b3bd02`) and its fresh computational replay are preserved in the machine evidence. The reproducibility ZIP is byte-identical between the two kits; rerunning unchanged computations after the prose edit was unnecessary. Earlier delivery reports were not used as substitutes for extraction, rebuilding, replay, or page inspection. No manuscript, upload file, source, expected certificate, or kit was modified. Scratch work is confined to `tmp/presubmit`, including an extraction path containing spaces.

## Archive and correspondence checks

- The outer archive and both nested archives passed CRC checks. Every member has a safe relative path; there are no duplicate member names, symlinks, absolute paths, backslash paths, or traversal components.
- All eight outer members are byte-identical to the corresponding current `upload` files.
- Every entry in the delivered `SHA256SUMS` passes.
- All 16 reproducibility members and all three manuscript-source members are byte-identical to their current source files. No binary executable, generated build directory, private review dump, or unrelated file is present.
- The main PDF exactly matches `output/pdf/kourovka_16_45.pdf`; the note exactly matches `output/pdf/verification_note.pdf` and the current supplement copy.
- The official `baustms.cls` is unchanged, with SHA-256 `b5e53c7510ed44cd2673e30f7c60b2c09d4fdb77d057e9d61979ed537202fad3`.
- All 16 supplement files exactly match their blobs in the cited immutable Git commit `be0f06ee0c61739dcda5629e2c4223e7da7951d3`.

## Fresh source build and computation

The manuscript source extracted from the delivered ZIP was built with the installed Tectonic compiler, with the supplied official class present. It compiled successfully, with no overfull/underfull boxes, undefined references, LaTeX warnings or errors in the final compiler log.

Every one of the seven rebuilt pages has exactly the same extracted text and page dimensions as the submission PDF. All URI links and annotation positions/targets match as well. The PDF metadata correctly names Alec Kriebel and the manuscript title. PDF creation timestamps differ between builds, as expected; binary identity of rebuilt PDFs was not required.

A fresh `make verify` was run from the clean extracted reproducibility archive during this final review, using the documented default commands. The archive is byte-identical in the revised kit. It compiled the C++ implementation and ran both Python implementations successfully. The three freshly generated subgroup collections agree on all 76 actual matrix subgroups, the complete sorted affine-element digest agrees across the two Python implementations, and all mathematical summaries agree with the delivered expected outputs. All six expected files retained their exact initial hashes, so this was reproduction against unchanged references.

The mathematical-body digest is
`edd472fbabb18b1c07e1fba088a39eccf0656dfe2d32baf7835cdc4268514fd4`.
This identifies the abstract-through-proof content reviewed here; the artifact audit is not itself an additional structural-proof certification.

## Visual and practical review

Fresh Poppler renders of all seven revised main-article pages and all three unchanged verification-note pages were individually inspected at 1400-pixel page scale. No clipped text, overlap, missing glyph, broken display, corrupted table, unintended blank page or unreadable reference was found. The standard journal-class typography, running heads and page breaks are coherent. The independent note has readable equations and subgroup-count table.

The abstract in the copy-ready metadata is 122 words. Its mathematics and scope match the PDF. The title, author, affiliation, email, ORCID, MSC codes, funding statement, competing-interest statement, AI-use scope, preprint DOI and current repository snapshot are consistent across the files. The user-confirmed affiliation and declarations are used; no street address, grant, model build identifier, external peer review or proof-assistant certification has been invented.

The revised manuscript, cover letter and metadata consistently disclose the earlier version hosted in the official Notebook repository. The previous wording implying that the online problem had no available solution has been removed. The theorem and every proof paragraph are byte-for-byte unchanged by this correction. The cover letter accurately describes the included seven-page structural paper, public preprint, optional verification material and substantive AI assistance. The manuscript and metadata acknowledge that historical application/model build identifiers were not consistently recorded. The package does not misrepresent those details as known.

The submission guide appropriately distinguishes the initial manuscript from optional referee material and source files, instructs the author not to upload the entire kit as the article, and leaves personal originality/authorship/simultaneous-submission declarations for the human author. It says the logged-in interface was not inspected. No submitted status, editor agreement or publication agreement is falsely represented.

## Limit and conclusion

No unresolved artifact correction remains after the limited recheck of the revised final kit. The checked kit is consistent and reproducible, with clean compiled pages. Live journal-policy assessment and independent mathematical review are separate parallel tasks. This result makes no acceptance prediction and does not replace the author's final reading and journal declarations.

Machine evidence: `evidence/presubmit_artifact_audit.json`.
