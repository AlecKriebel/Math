# Reviewed source-aware coverage of the old k111 product

**Separate source/arithmetic review: PASS.** The exact arXiv-v11 even-period A′A″ assertion in record5100005 is false as a credited consequence of the geometric witness already reviewed in [PR147](https://github.com/AlecKriebel/Math/pull/147). No new independent discovery or proof-search turn is counted.

The two primitive convex four-period representatives give331776/625 and576 for A′A″, with positive difference28224/625. Their common fixed confocal caustic and continuous Poncelet family were established in the prior reviewed work. The known outer/contact area ratio and the present exact arithmetic audit give this target-specific consequence.

## Current artifacts

- SOURCE_CONSEQUENCE_V2.md: exact reviewed source/coverage note, SHA256 fc2f32c6ad852d753e75334936a444080cdfd0562282d70e16e20592df23969f
- review/FINAL_REVIEW.md: full separate review, including transparent prior sharing of the known polarity observation and a distinct double-root contact check
- verification.json and review/independent_receipt.json: exact author/independent outputs; the independent verifier passes101 assertions
- SOURCE_REVISION_NOTE.md: correction of the initial journal-table reading

The journal's k111 is the different odd-period expression A′A″/A²=1. Its neighboring k112 has a product/ratio discrepancy. This package preserves that distinction and does not claim a refutation of the journal's odd k111 or an author withdrawal/erratum.

The original pending-review headings in frozen files describe their capture time. This result file and the independent review record the subsequent PASS without changing the reviewed text. The earlier local source draft remains historical; V2 is the current conclusion.

## Reproduce

    python3 verify_area_consequence.py
    python3 review/independent_check.py

Both use only Python's standard library. All receipts replay byte-for-byte. Full source articles, rendered pages, cached copies of the prior PR147 proof/review, and unrelated full problem records are excluded. The prior proof/review are linked at immutable commits in V2.

Queue classification: already_solved,0/5, explicitly meaning credited existing-witness coverage. The old target differs from k107, so it is not called a literal duplicate; the shared geometry is not counted twice as an independent discovery. No human peer-review, novelty, or historical-priority certification is asserted.
