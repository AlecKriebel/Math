# Balanced Ham Sandwich Line: audited bounded partial

Problem **136 / GREEN-048**, rank 879. **Unsolved, 3/5.** The general straight-line discrepancy-at-most-100 question remains unresolved. No universal bound of 2 or 100 and no counterexample to the target is claimed.

## Accepted result and limits

For a finite set of n >= 2 distinct planar points and each exposed hull vertex p, a determined straight line through p has open-half-plane discrepancy at most m_p - 2 + (n mod 2), where m_p is the maximum collinearity through p. Consequently, threshold 100 holds when some exposed p has m_p <= 101, or m_p <= 102 for even n. Centrally symmetric configurations have minimum discrepancy zero. These elementary results do not establish a universal constant independent of collinearity.

- [Corrected result](corrected/RESULT.md), [unchanged proof](corrected/PROOF.md), [three approaches](corrected/APPROACH_LOG.md), and [qualified sources](corrected/SOURCES.md)
- [Full independent audit](independent_audit/AUDIT.md), [separate acceptance](independent_audit/ACCEPTANCE.md), and [actual source-wording patch](independent_audit/SOURCE_WORDING_REPAIR.patch)
- [Publication acceptance](PUBLICATION_ACCEPTANCE.json), [static integrity results](PUBLICATION_TEST_RESULTS.json), and [inventory](PUBLICATION_MANIFEST.json)

The source wording flags an apparent threshold discrepancy. Pinchasi's D=2 example rules out bound 1; it neither proves bound 2 nor excludes another stronger example. Dated source reports support caution, not a definitive correction of Green. Pseudoline counterexamples are not substituted for straight-line realizations. The 2025 computational construction/minimality and full cited asymptotic proofs were not independently reproduced. Literature searches are dated and nonexhaustive.

## Provenance and verification boundary

All three frozen ZIPs and their external manifests are preserved unchanged in `archives/`. Their contents are unpacked in `author_original/`, `corrected/`, and `independent_audit/`. The original author prose is historical, superseded by the separately accepted corrected derivative. Applying the actual patch with `patch -p1` to a fresh original extraction reproduces all six corrected members; five source/provenance files change and PROOF.md is byte-identical. The audit archive also carries a matching accepted-derivative copy.

Historical statements about publication not having occurred and review being pending refer to the freeze time and remain unchanged. This package is AI-assisted and unrefereed. Independent AI mathematical review is not conventional human peer review, formal verification, or a novelty certificate.

Isolated normal and optimized static controls check byte integrity, archive safety, patch replay, acceptance binding, claim scope, complete input/source pins, and the narrow queue edit. No archive code is executed. There is no executable mathematical checker or formal proof certificate in this packet. The audit's finite sanity checks supplement its written analytic review. Matching hashes and passing static tests establish byte custody, not mathematical validity or a CI pass.

Only authored work and public bibliographic/verification metadata are included. Copied source documents/text, raw corpora, source screenshots, private sources and coordination, personal data, and private checker fingerprints are excluded.

Only this queue row's Status and Turns change. Its Findings, existing notes and chat links, every other cell, and unrelated current-main bytes are preserved. No new substantive approach is added. Publication is a draft PR only; no merge, release, DOI, or outreach is performed.
