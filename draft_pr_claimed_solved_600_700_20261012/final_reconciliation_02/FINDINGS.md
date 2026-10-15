# Final eight-PR read-only reconciliation

Completed 2026-10-15T08:00:16.955225+00:00. All 106 checks pass with 0 mandatory findings. No external mutations, shared Git checkout/index changes, mathematical reaudit or skipped-PR processing occurred. This artifact does not modify the persistent goal status.

The closed-without-merge PRs [615, 628, 630, 672] match their saved original heads, closure timestamps, exact posted comment bodies and URLs. Every original and accepted GitHub commit still resolves.

The 4 published PRs match their saved accepted heads, actual merge commits, scoped file inventories and selected queue rows. Their production public Zenodo records match every supplied metadata field under explicit native schema mapping and the exact normalization recorded in that same record’s actual production publication receipt. Only PR681 record23387442 may use the exact html.escape(local_description, quote=False) transformation, and only with the singleton plain_text_html_entities receipt and unchanged kit plain-text eligibility; all other fields stay exact. The other three records must retain empty normalization lists. Unknown normalization lists fail. Raw local and native metadata are preserved separately in METADATA_COMPARISON records. Exact public PDF/ZIP downloads match accepted local bytes and saved SHA-256/MD5/size evidence; each DOI resolves to its exact production record.

The spreadsheet ID, Math Puzzles tab, gid 1254632077, header, exact saved A:D rows and global normalized DOI uniqueness all match.

| PR | DOI | Exact tracker row |
| --- | --- | --- |
| #618 | 10.5281/zenodo.23331709 | 'Math Puzzles'!A73:D73 |
| #623 | 10.5281/zenodo.23356540 | 'Math Puzzles'!A88:D88 |
| #662 | 10.5281/zenodo.23384924 | 'Math Puzzles'!A94:D94 |
| #681 | 10.5281/zenodo.23387442 | 'Math Puzzles'!A102:D102 |

Actual record-specific metadata normalization evidence:
- PR #618, 10.5281/zenodo.23331709: []; comparison EXACT.
- PR #623, 10.5281/zenodo.23356540: []; comparison EXACT.
- PR #662, 10.5281/zenodo.23384924: []; comparison EXACT.
- PR #681, 10.5281/zenodo.23387442: [{"field": "description", "kind": "plain_text_html_entities"}]; comparison EXACT_HTML_ESCAPE_QUOTE_FALSE_OF_ELIGIBLE_LOCAL_PLAIN_TEXT.

All spreadsheet responses, including full-column values, all-tab metadata and exact-row requests, are retained only in ignored tmp/ before allowlisted evidence is emitted. Public sheet artifacts contain only our exact matching rows, expected tab/header identities, counts/indices and private-cache hashes. Unexpected row contents remain private. The privacy output scan found no unrelated full rows or other-tab properties.

RECONCILIATION_RESULT.json contains every check. INPUT_BINDINGS.json binds local source receipts, accepted files, reconciliation scripts and private response hashes. EXPECTED_COMPLETED_EIGHT.json preserves the actual completed-eight decision snapshot. Individual JSON readbacks and immutable scoped Git inventories provide checkable evidence. Raw public downloads and raw spreadsheet responses are recoverable under ignored tmp/.

These readbacks establish consistency at their recorded UTC times. They do not re-audit mathematics, strengthen earlier priority conclusions or certify human peer review.
