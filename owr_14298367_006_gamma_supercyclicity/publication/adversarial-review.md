# Publication and uploader review

Scope: deposit integrity, metadata correspondence, tracker receipts, and the uploader’s narrowly scoped HTML-encoding comparison. This is not an additional mathematical or external peer review.

## First independent reviewer: zenodo_receipt_review

- Manifest and original kit metadata are equal.
- Independent anonymous public downloads match the kit byte for byte.
- DOI `10.5281/zenodo.22983147` agrees with the publication receipts and tracker row `A8:D8`.
- One actionable tool issue: the initial tag-only guard accepted double-encoded character references (for example, `A &amp; B` becoming `A &amp;amp; B`). This issue did not affect the paper’s plain-text description.
- Accepted correction: require `html.unescape(value) == value` before allowing the escaped alternative; retain exact equality and add named/numeric reference regressions.

## Fresh second reviewer: zenodo_verifier_final_review

Verdict: **No actionable findings in the reviewed diff.** All 25 tests pass. Exact unchanged HTML and pre-encoded entities remain accepted. The paper’s `1 <= p < infinity` text passes with the exact Zenodo escaping. Changed text, lost HTML, double encoding, and changes to other fields remain rejected.

Reviewed source SHA-256: `d95aa524fdda5e55645ec9e7c2e0b15eb1e1832afa2bf1e3dd02cb48e66609d3`.

Reviewed test SHA-256: `e076a46043ef2f71366a2f52fede063438c798dcaa147b036aa0f577a0d7f51c`.

No credentials were accessed by the reviewers and no remote state was changed by them. The parent applied the correction; the reviewers performed read-only checks.
