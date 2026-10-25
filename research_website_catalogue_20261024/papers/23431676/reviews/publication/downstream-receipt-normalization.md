# Read-only downstream receipt compatibility proposal

This is a proposal for the designated renderer/checker owner. No shared code was changed or run by this assignment.

The frozen `sources/receipt.json` for record 23431676 uses `assets`, with two full source entries. Its SHA-256 is `c4ecaf95a88e3cf418f6587396cdb1ad05f191cbe96c6546c990e523f29cb548`. Preserve those exact bytes. The list entries already use the supported `name`, `bytes`, `sha256`, `md5`, and URL fields; no field renaming inside entries is needed.

The current `scripts/published_assets.py` constructor and the renderer/checker loops access `receipt['files']`. Loading this unmodified receipt therefore needs an in-memory view. A narrow compatibility function can deep-copy the parsed object, require either `files` or `assets` to be a list of objects, reject conflicting simultaneous lists, and provide the canonical `files` list in the returned copy. Missing/invalid lists must fail; do not fall back to an empty list. Keep the original parsed receipt available as `raw_receipt`, and calculate receipt bindings from the original file bytes rather than serializing the normalized view.

Proposed dependency-free implementation and its non-mathematical contract checks are in `receipt-normalization-proposal.py`. This is not installed in the shared pipeline. It makes no writes, performs no rendering, and adds no source evidence.

Integration points for the designated owner:

1. Immediately after reading a raw deposited receipt in `render_page.py` and `final-content-check.py`, construct the normalized in-memory view for asset enumeration and `PublishedAssets`. Apply the same helper consistently for related-record receipts if used. Do not rewrite or regenerate a source receipt.
2. Continue validating `promotion.json.source_receipt_sha256` against the raw receipt bytes. The promotion also explicitly records `source_receipt_asset_field: assets`.
3. For this paper, `promotion.json.source_files` and `publication.json.source_binding.files` are exact, complete copies of the original `assets` list, with all entry fields retained. The generic asset-list comparison should use the normalized view; the raw provenance check still uses the frozen receipt hash.
4. Retain existing name/path/duplicate/hash/size checks in `PublishedAssets`; the compatibility function replaces none of them. A conflicting `files`/`assets` list must be rejected even if one would otherwise appear usable.
5. Add the paper's actual TeX path (`sources/published-source/pr1097_support_v1_0/paper.tex`) to the source-driven abstract checker. The complete 125-word abstract has only whitespace and TeX-accent normalization, without omissions. Bind the TeX SHA-256 `daaacbeb3b198a8c13208663a6e49fc417a5b7ec2e7a0bfa62a9a87e42ce7f5f`.
6. Preserve the exact date policy: manuscript/declared edition date `2026-10-15`, visible label `Manuscript dated`, and separate record creation `2026-10-17T05:45:36.045033+00:00`. The manuscript/declared edition date is not evidence of public availability or the website publication date.

The final public wording preserves the binary adjacency and nonnegative binary initial/target configurations, finite nonempty loopless strongly connected directed **multigraphs**, empty and stoppable words, variable vertex count and singleton equality convention. It credits Hujter, Kiss and Tóthmérész for coNP membership and asserts no simple-graph classification. Follow-up is null. Local rendering, source-driven page/asset checks, desktop/mobile/live review, and tracker/redirect decisions remain downstream gates.
