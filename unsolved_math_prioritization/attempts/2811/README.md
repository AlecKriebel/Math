# KP-3.13: audited surface triple-point partials

Problem **2811 / KP-3.13**, rank **910**, remains **unsolved**, with **3/5** substantive approaches used. The original author packet is accepted unchanged.

## Accepted scope

- Conditional finite-cover fiber multiplicity and the regular-deck triple criterion.
- Persistence of transverse triple points under sufficiently small C1 perturbations.
- A finite determinant-grid exception set from two applicable surgery-slope criteria.

There is no universal construction satisfying the at-most-two-preimages condition, and no obstruction to every candidate surface in a target. No complete solution, counterexample, historical novelty, exhaustive current-open-status certification, formal proof, or human peer review is claimed.

Read the [original proof](original_author/PROOF.md), [source report](original_author/REPORT.md), [approach log](original_author/APPROACH_LOG.md), [full independent audit](independent_audit/AUDIT_REPORT.md), and [exact binding](independent_audit/BINDING.json). The [current audit status](independent_audit/AUDIT_STATUS.json) records acceptance without repair. [Publication metadata](PUBLICATION_METADATA.json) supplies the canonical queue disposition. The frozen author pending-audit fields and audit not-published fields are historical bytes and are preserved.

## Verification and its limits

The original author controls cover 574 regular-fiber subsets, 1,400 slope cases and 1,728 affine cases. Independent controls add 1,808 group subsets, 8,832 slope cases and 5,103 affine systems (15,743 cases). These are finite exact sanity checks, not formal proofs or certificates of geometric existence. The mathematical all-size arguments and independent review are in the proof and audit.

Both original ZIPs, their external manifests, the original author receipt, all 10 author members and all 12 audit members are retained byte-for-byte. The audit embeds the same original author ZIP, manifest and receipt. The publication wrapper checks this chain, exact inventories, scope, and fail-closed controls. Only this queue row's Status and Turns change; Findings and all unrelated queue bytes remain unchanged.

Source/corpus replays rehash the three complete local corpora, the exact record/report pair and statement, and five separately held source PDFs. Only public hashes, sizes and match results are published. Source texts, PDFs and corpus contents are excluded. Li remains public web PDF text extraction only, with no local PDF or visual claim. Publication replays do not represent a new source reading or literature search.

## Reproduce

Python 3.10+, standard library only. Authenticate PUBLICATION_MANIFEST.json against an independently obtained SHA-256 before trusting extracted code. A verifier cannot authenticate its own replacement. Run from this folder:

    python3 -B verify_publication.py . --manifest-sha256 HASH --replay
    python3 -B -O verify_publication.py . --manifest-sha256 HASH --replay

The HASH is supplied out of band in the PR description. Both modes check the public files, replay the author and audit finite controls from fresh authenticated extractions, and challenge the audit with 16 integrity negatives per mode. The frozen independent checker also challenges the author with 20 negatives per mode. Publication wrapper negatives are reported separately in PUBLICATION_TEST_RESULTS.json.

Optional --base-queue and --queue arguments check the complete queue byte delta. Optional --catalog, --problems, --research-reports and --source-dir arguments replay all private input hashes without publishing their contents. The source directory contains k3.pdf, cooper_long.pdf, kahn_markovic.pdf, agol.pdf and agol_published.pdf. Outputs contain public metadata only.

This is a draft research PR. Local replay is distinct from GitHub CI; remote checks and final draft state are reported separately. No merge, release, DOI or external outreach is included.
