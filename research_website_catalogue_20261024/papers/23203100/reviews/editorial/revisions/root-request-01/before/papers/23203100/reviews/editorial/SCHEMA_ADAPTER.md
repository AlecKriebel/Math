# Bounded downstream integration — Zenodo 23203100

This is a preparation note for root review. It does not authorize or claim rendering, a public-page pass, live HTTP/browser verification, deployment or native Sheet edits. The prospective canonical URL in `publication.json` is page metadata; it is not evidence that the page is live. The authoritative Sheet URL must remain blank until root completes the live gates.

## Frozen source layout

Preserve these exact files and their raw bytes:

| Role | Original path relative to this paper | SHA-256 |
|---|---|---|
| API record | `sources/record/zenodo_record.json` | `023aff8aa7f44ba7e522b3d557bbbe9eaaff060990c8b8032c93aed794e78778` |
| HTTP receipts | `sources/record/transport_receipts.json` | `8170b3100a1e00bb4f1c5cb0477079b48dd162cf3d8fcb4b063c87473ba28025` |
| Published PDF | `sources/assets/paper.pdf` | `490c6d4d78eb4c2ae829d06f31df1ed1ace955174acec87279f5d5eb8dee8581` |
| Published supplement | `sources/assets/zenodo-upload-kit.zip` | `e9f9adb0dca6f7776b215672ab97b7f8922aae415d2d9f73afd631259ca40fab` |
| Published TeX | `sources/extracted/zenodo-upload-kit/manuscript/main.tex` | `eda0b20fb843fda3b7b70203b63628e36ebf5d4a1b6c817624d3a5810f9beaab` |

The raw transport receipt is a **list**, not an object with a `files` or `assets` list. Index 0 binds the API JSON (`saved=record/zenodo_record.json`); indices 1 and 2 bind ZIP and PDF (`saved=assets/...`). Each asset entry retains its actual `url`, `saved`, size, MD5, SHA-256, Zenodo checksum, timestamps and headers. A filename is derived from the saved asset basename only in memory and is explicitly recorded in the new configs. No alias, normalized receipt or copied root-level asset has been created. The full source tree has 92 frozen files; the ZIP has 40 regular members, no nested archive and no embedded PDF. The internal inventory covers 39 members plus the inventory itself.

## Small source-reader adapter

The inspected shared implementation is `scripts/render_page.py`, with read-only asset operations in `scripts/published_assets.py`. No file called `render-common-paper` was present in this checkout. If root has a separate wrapper with that name, it should enforce the same bindings. Existing `PublishedAssets` accepts an in-memory standard receipt view, but its `normalized_receipt_view` deliberately rejects this raw list. Existing renderer and checker also assume `sources/receipt.json`, root-level deposited files, and a standard metadata path. Passing these configs to the current scripts unchanged is expected to fail; do not make source aliases to bypass this.

For this record only, a bounded adapter should:

1. Resolve and hash `source_binding.receipt_path` and `source_binding.record_path` against the original paper directory. Require equality with both publication and promotion bindings and the root clearance. Reject traversal, symlinks and paths outside the paper.
2. Read the raw list unchanged. Require the exact three unique `saved` values, status 200, and the metadata entry hash/size matching the actual saved API file. Parse the API object's `metadata` only for title/author/date/version/DOI comparisons; keep creation/update fields from the outer object.
3. Match each original API `files` item by basename, content URL, byte size and checksum to exactly one asset receipt. Require hashes of the actual contained source files under `sources/assets/` to match the receipt, the new config and the root clearance. The new `source_binding.files`/`promotion.source_files` are equal **derived bindings**, not a claim that the raw list has a new schema. Hashes always refer to the original raw receipt bytes.
4. Construct only an ephemeral view, for example `{'record_id':'23203100','files':source_binding['files']}`. Pass `paper/'sources/assets'` as the asset root to `PublishedAssets` with no embedded assets. The owned editorial check exercises that existing helper on precisely this in-memory view and both unchanged assets. Keep the default path behavior for all other papers.
5. Add the exact source path mapping `'23203100': 'extracted/zenodo-upload-kit/manuscript/main.tex'` to the later content checker. Do not move the extracted source or primary cache.

## Absent version and date

`publication.version`, `source_binding.zenodo_version` and `source_binding.manuscript_version` are all JSON null. The actual API metadata has no `version` key. Concept-version index zero is not a version name. The visible labels are **Manuscript dated**, **No version number supplied**, and the explicitly qualified edition note. Printed TeX is exactly `\date{October 6, 2026}`. Declared publication date is `2026-10-06`; raw record creation is `2026-10-07T04:42:47.312983+00:00`, equivalent to the root clearance's Z timestamp. No public-priority inference follows.

The current renderer eagerly evaluates fallback expressions such as `c.get('edition_label','Version '+c['version'])`, even when the explicit label exists. With a null version these expressions raise a TypeError. Root should use lazy explicit defaults and conditionally omit the JSON-LD `version` member when no actual version exists. Do not stringify null as “None”, “null”, “v1” or “1.0”. Update the corresponding checker to require that JSON-LD has **no version property**, rather than fabricate a version for its current mandatory comparison. Existing versioned records should retain their actual values.

## Full abstract

Normalize the complete TeX abstract only by whitespace collapse and `--` to `–`. Require exact equality with `publication.abstract`, `reviews/editorial/ABSTRACT.txt`, `reviews/scope/ORIGINAL_ABSTRACT.txt` and `reviews/scope/PAGE_CONTENT_CANDIDATE.json`'s `abstract`. It has 146 whitespace-separated words and eight complete sentences, including both the literal secrecy refutation and the unrefereed external proof/Lean limitation. The API description is longer and is not the original abstract. The stripped TeX-body and normalized-text SHA-256 values are explicitly bound in the config.

## Five original review schemas and later dependency resolution

Require all five exact report and verdict hashes and parsed verdict objects. Do not manufacture original PASS fields:

- Scope: `status=scope_intake_complete_no_scientific_verdict`; mathematical, priority, promotion and defect decisions remain null; original independent reviews remain marked pending.
- Analytic: `verdict=no_substantive_defect_found_conditional_capacity_consequences_verified`; `publication_clearance=false`; external full-proof validation and Lean build were not performed by that original lane.
- Adversarial: `result=downstream_reduction_verified_with_explicit_external_EPnI_dependency`; `unconditional_global_capacity_clearance=false`; the original exact dependency gap remains in its verdict.
- Later upstream analytic: `status=COMPLETE`, `verdict=PASS`; the full analytic proof is substantively reconstructed, the arbitrary-finite-block VE consequence is cleared, and no machine build is claimed.
- Later upstream adversarial: `status=complete`, `verdict=PASS_UPSTREAM_REQUIRED_VE`; the full central proof is scrutinized, with no unresolved central mathematical gap identified and no formal compilation claim.

The exact root clearance is `verification/root-clearance-23203100-20261025.json`, SHA-256 `e186543476c3a507b7ba5fc59df50432963efce03d6791015eb8f48becb61ca6`. `promotion.root_clearance_record` preserves the entire decision; `scope_gate_resolution` is copied literally. Root separately adjudicated the two later full-proof audits and actual central proof. The positive publication disposition is therefore the literal exact general capacity equalities under the stated models using the credited external theorem. It is not silently replaced with “if an unproved VE premise were assumed.” Original conditional reviewer dispositions are historical evidence and remain unchanged.

## Root content and publication gates

Root must read `PUBLIC_COPY.md` and both complete configs before rendering. Later actual rendered checks must compare visible sections to every `public-sections.json` paragraph and check title/author/ORCID/DOI/date, canonical/citation/scholarly metadata, null-version handling, all three inequalities with one common λ in each region, literal obstruction constants, explicit generated-secret correction, average-photon and finite-gross-forward-resource limits, attribution and honest AI/unrefereed/no-machine-build disclosure. Confirm no follow-up section, audit dates/counts/hashes or private paths appear publicly.

Keep the normal simple personal article template: white background, readable single column, ordinary headings and links. Copy the original PDF and ZIP byte-for-byte through authenticated asset resolution, embed the local PDF, and retain original Zenodo links, direct-open/download access and a searchable PDF. The unchanged shared template currently uses the original-Zenodo PDF link as its download path and gives the ZIP a download attribute; root should also ensure the PDF has an explicit download option when staging. Check actual links, index/sitemap, desktop/mobile and browser presentation, local/live HTTP and byte identity. Native Sheet publication occurs only after the final live/browser gates. No claim of any of those passes is made by this preparation.
