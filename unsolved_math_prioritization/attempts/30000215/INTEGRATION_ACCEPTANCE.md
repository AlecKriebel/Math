# Independent integration acceptance

Date: 14 October 2026 UTC. Target: row 1782 / 30000215 / OWR-822-007.

## Verdict

**ACCEPTED for local integration, with the validator hardening described below.** This is a packaging, source-interface, and executable-enforcement review of an already accepted proof. It adds **zero mathematical passes**, makes no new mathematical claim, and performs no remote publication or repository change.

The unchanged mathematical acceptance is [ACCEPTANCE.md](ACCEPTANCE.md). Its subject remains [PROOF.md](PROOF.md), 15940 bytes, SHA-256 `6ec0d8fbf2e583e02fd775e24be762144d09ae3e8de9a835a80856e27527746e`. All twelve original authored inputs were independently compared with their original files, the supplied reader, and this reader. Every comparison is byte-identical.

## Scope and formula integration

The reader summaries agree with the accepted proof and its audit:

- For each integer n >= 3, the specified balanced integer-coordinate four-ray drawings of K(3,n) and K(4,n) have respectively q(n) and 2q(n) crossings, with q(n) = floor(n/2) floor((n-1)/2).
- The statement quantifies over every simultaneous assignment of all sets A_e, without compatibility conditions. Independent edge pairs are unordered and vertex-disjoint. The index count is 2 binom(m,2) binom(n,2).
- With p(e,f) = (|e intersect A_f| + |f intersect A_e|) mod 2 and b = c xor p, the accepted statement is wt(b) >= wt(c), equivalently N_11 <= N_01. The reader preserves the direction, parity, indexing, and multiplicity conventions.
- The result applies to the specified nice drawings. No summary expands it to arbitrary drawings, unrestricted K(m,n), or a complete classification. The analytic proof supplies the universal quantifier; finite replays do not.
- The original existential question is affirmatively addressed at this scope. The recorded disposition remains `claimed_solved`, 1/5. Known nonplanar positive cases predate this submission. No novelty, first solution, priority, global openness, or external peer-review claim is made.

These are consistency checks against the existing accepted text, not a fresh derivation or a new mathematical audit.

## Citations and provenance

The original question was rechecked in [OWR 17/2005, printed p. 983](https://ems.press/content/serial-article-files/45990?nt=1). The exact Theorem 1 interface was checked in the pinned six-page [Székely publisher paper](https://amc-journal.eu/index.php/amc/article/download/43/30), including visual inspection of printed p. 33. The current web tool could not retrieve that publisher endpoint; the retained public-source PDF matched its recorded byte count and digest.

Primary-paper checks confirm the scope of the cited known positive cases and the distinction between independent-odd and pair-crossing results. Seven pinned public-source PDFs were rehashed and freshly extracted locally. Source documents and extracted text were not added to this package. The 2026 general complete-bipartite manuscript remains an unreviewed ordinary point-count claim, outside the proof's premises; neither its mathematics nor formalization was audited. No global current-status or novelty search was added.

[SOURCE_LINK_REVIEW.json](SOURCE_LINK_REVIEW.json) records every external URL appearing in the supplied Markdown, the additional pinned raw-PDF URL from the source manifest, citation observations, and retrieval limitations. Some publisher/DOI endpoints were unavailable through the web tool; that is not described as a dead link or as successful fresh retrieval. Historical source reports and version records remain unchanged.

## Validator defect and narrow correction

The supplied validator accepted certain resealed changes to nonmathematical evidence: unknown tamper-test modes, incorrect outer optimization metadata, duplicated positive-validation modes, an incorrect preservation source basename, and a Boolean in place of a recorded compilation optimization integer. The five reproduced input failures are recorded in [INTEGRATION_EVIDENCE.json](INTEGRATION_EVIDENCE.json).

The correction binds the complete bytes of the existing PRESERVATION_MAP.json, REPLAY_REPORT.json, and TEST_REPORT.json to fixed validator pins. These immutable historical records already describe the supplied 22-file reader. They must not be silently rewritten or relabeled when assembling a larger package. Fresh evidence for the expanded 27-file reader is stored separately. Twelve resealed-metadata mutations in each interpreter mode are now rejected, for 36 additional regression cases.

The original checker, replay wrapper, test runner, proof, audit, and source reports remain unchanged. The modified files are the validator and two explanatory reader documents, plus the regenerated manifest. Five review artifacts are added. [REVIEW_CHANGE_MAP.json](REVIEW_CHANGE_MAP.json) gives the complete input-to-review map and explains the noncircular sealing convention.

## Replay and assertion-enforcement acceptance

All three outer interpreter modes, normal, -O, and -OO, pass the strict validator and produce byte-identical supplemental results through the unchanged replay wrapper. The wrapper explicitly compiles the original source with `dont_inherit=True, optimize=0`.

Each replay retains sixteen source assertion sites and, on the review interpreter, seventeen assertion-failure instructions. The supplemental output remains 14223 bytes, SHA-256 `5ea80af62ea2a954e12f49f91f626e8bb9a8749e65e2192edc7cbf01a5228e83`: 60 geometry cases, 1650 local K(3,3) restrictions, 1792 seeded assignments, and the bounded K(3,3) image diagnostic of rank 17 and minimum weight 1.

The original suite freshly confirms 48 isolated assertion failures and 54 rejected packet mutations. The independent review runner separately confirms all sixteen sites in each outer mode, another 48 isolated failures. Its direct optimized-compilation negative controls show zero assertion-failure instructions at optimize=1 and optimize=2. Those stripped compilations are **not** called assertions-enforced tests, and no mathematical execution is claimed for them.

The probes intentionally modify only temporary in-memory AST assertion conditions. They establish enforcement and do not add mathematical evidence. The full per-case records, commands' structured results, and limitations are in INTEGRATION_EVIDENCE.json. Run `python review_checks.py` to repeat the integration checks without modifying the packet. Original instructions remain in [VERIFICATION.md](VERIFICATION.md).

## Inventory, links, and publication boundary

The supplied archive was independently verified at 41651 bytes and SHA-256 `371b8937b49e7ee86abdd32008f2a2559a671476f82c4d74f66073e43ff56682`; its manifest pin is `738f38fee0e4f79c7435f9af3550d1fa7074b29e6333171df2fca99d3b7eb0e8`. Its exact 22-entry regular-file inventory matched the supplied directory byte for byte.

The final MANIFEST.json covers all 26 other public files. The mathematical audit binds the proof and acceptance report; PROOF_PINS.json binds those two files and the audit manifest; SOURCE_PUBLIC_FILES.json binds its original three source-review artifacts. All eight nested local digest bindings were independently verified. The smaller historical inventories are not represented as full-reader manifests. Every local Markdown link resolves within this flat public directory.

The final archive contains only the 27 public regular files. The external seal records its digest and byte count, the manifest digest, exact member coverage, a deterministic rebuild, a byte-identical restoration, and fresh full review results from the restored tree. An archive cannot embed its own final digest without a circular dependency; the final pins therefore remain in the external receipt.

The package contains authored proof/review text, executable checks, and public verification metadata. No copied third-party source document, extracted source file, source image, dataset contents, private personal information, or private coordination record is included. Existing short attributed quotations in the supplied authored reports remain unchanged. No files were published remotely.

## Limits

Acceptance is relative to the preserved proof's existing mathematical review and to trusted validator/external-seal bytes. Checksums are not signatures. Passing finite checks does not prove the infinite-family theorem. This integration review does not certify novelty, general complete-bipartite results, or the current status of every related problem.
