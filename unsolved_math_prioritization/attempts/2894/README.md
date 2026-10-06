# KP-4.18 / ID 2894: audited prior implication, combined unsolved

Rank 917; one of five proof-attempt turns used. Part (a) has an affirmative prior result, accepted as a cited-theorem implication. Part (b) remains unresolved in the inspected primary literature. No new solution or novelty is claimed.

Hambleton–Ünlü (HU), [v1 Corollary D and Corollary 4.9](https://arxiv.org/pdf/2602.05003v1), supplies a finite group G with strictly unequal simple/homotopy assembly kernels. Kasprowski–Nicholson–Veselá (KNV), [v2 Theorem C](https://arxiv.org/pdf/2405.06637v2), then gives smooth closed four-manifolds that are actually homotopy equivalent but admit no simple homotopy equivalence, even after S² × S² stabilization. Their fundamental group is G*G, not the finite witness G. The audit checks the unmarked and unoriented quantifiers, strict-kernel direction, and oriented integral/2-localized assembly compatibility.

HU remains a public preprint; KNV has the cited PLMS publication. This acceptance does not independently re-prove the underlying L-theory, SK₁, or assembly-map results or reproduce GAP group identification. The local finite parity checks certify only their stated finite identities. [Kupers–Powell v2, revised 22 July 2026](https://arxiv.org/pdf/2604.27635v2), retains part (b)'s h-versus-s question as open. No smooth h-cobordism for the part (a) pair has been supplied.

## Files and historical scope

- `corrected_author/` is the accepted eight-file mathematical packet.
- `original_author/` preserves the eight-file author freeze, including its historical noncanonical `partially_solved` field.
- `independent_audit/AUDIT_REPORT.md` and `MATH_AUDIT.md` give the acceptance analysis, limitations, and local source-typo interpretation.
- `independent_audit/correction.patch` is the actual zero-fuzz patch from original to corrected packet.
- `archives/` preserves all three exact ZIPs and external manifests, the audit receipt, and the pinned bootstrap. The original author receipt is represented only by its hash and size because it contains local temporary paths.
- `PUBLICATION_METADATA.json` distinguishes the current canonical unsolved status from historical snapshots. Statements in immutable original/audit files that no publication or queue mutation had yet occurred describe their freeze time.

No source PDFs, source text extracts, dataset contents, private sources, private personal data, or private coordination files are bundled. Full input and PDF verification requires separately supplied pinned inputs. Corpus/PDF identity checks are not a fresh source download, comprehensive new literature search, or theorem certification.

## Reproduce

From any working directory, use an independently retained SHA-256 of PUBLICATION_MANIFEST.json:

    python3 /path/to/verify_publication.py /path/to/2894 --manifest-sha256 PIN --replay
    python3 -O /path/to/verify_publication.py /path/to/2894 --manifest-sha256 PIN --replay

Optional `--base-queue ORIGINAL_QUEUE --queue UPDATED_QUEUE` checks the complete byte-preserving one-row diff. Optional `--catalog CATALOG --problems PROBLEMS --reports REPORTS --pdf-dir PDF_DIRECTORY` replays all three complete corpus pins, exact record/report pair, all five PDF pins, and primary statement identity. Supply all four input options together. Python standard library, patch, and pdftotext are used; no network requests are made.

The wrapper checks exact inventories and pins before running bound scripts, replays the actual correction patch, tests both packets (four positives, twelve baseline negatives, thirty additional adversarial controls each), and runs acceptance/bootstrap/parity checks in both Python modes. It rejects altered canonical claims and unsafe paths. Hashes establish consistency against separately retained pins, not signatures or mathematical proof certification.

Publication is limited to an open draft PR. No merge, auto-merge, release, DOI, or external outreach is part of this work.
