# Bounded local primary-text discovery

Checkpoint: 2026-10-06 22:59 PDT (2026-10-07 05:59 UTC).
Researcher: internal independent access agent. No outside individual was contacted.

**Outcome:** No existing complete target article or complete author manuscript was found by this bounded local scan. Assigned local discovery scope: 100% complete. Mandatory complete-article retrieval/read: 0% complete; the published-text dependency gate remains open. These estimates concern this access route only, not mathematical resolution or publication-package progress. Absence from this finite search is not a claim that no legitimate copy exists elsewhere or under an unindexed generic filename.

Target: Jean Roydor, *Banach–Mazur stability of von Neumann algebras*, *Journal of Topology and Analysis* 14(03) (2022), 767–792, DOI [10.1142/S1793525321500151](https://doi.org/10.1142/S1793525321500151). The inclusive journal page span is 26 pages; an author manuscript may have a different page count. No candidate was excluded solely for its page count. Title, author, publication identity, and actual content distinguish slides or a different article from the complete target manuscript.

## Scope and filename evidence

Read-only filename discovery used `rg --files --hidden --no-ignore` separately and only within `/Users/alec/Documents/Math` and `/Users/alec/Desktop/math`. Including ignored files was necessary to discover locally retained third-party sources. Explicit exclusions covered Git internals, `node_modules`, Python/cache/virtual-environment directories, `build`, `_build`, `.build`, `build-*`, `dist`, `target`, `tmp`, and `temp`. No private browser profile, credential store, communications folder, or unrelated home directory was searched. No other project file was read or changed.

The final case-insensitive filename filter was `roydor|s1793525321500151|banach[\W_]*mazur.*stabil|stabil.*banach[\W_]*mazur`, allowing spaces, underscores, and dash variants between Banach and Mazur. At 2026-10-07 05:58:56 UTC the final scan enumerated 1,284,416 filenames in the Documents research root and 124,603 in the Desktop research root. Both commands exited successfully without reported errors.

The Documents root yielded 10 matching filenames, all within this project. Eight were existing Markdown audits, metadata responses, or extracted text; only two were PDFs. The Desktop root yielded no matching filename. An initial scan used a narrower single-separator pattern and did not yet exclude temporary folders; the final scan strengthened the title-variant filter and exclusions without finding another PDF. The complete final filename-match list and exclusion globs are retained in the ignored metadata record below.

## Focused Spotlight content search and its limit

One identical focused PDF-content query was run once per research root, with `mdfind -onlyin` fixing each permitted scope. It required PDF content type and a text-content match for the exact DOI or exact title with either an en dash or ASCII hyphen:

```text
kMDItemContentType == "com.adobe.pdf" &&
(kMDItemTextContent == "*10.1142/S1793525321500151*"cd ||
 kMDItemTextContent == "*Banach–Mazur stability of von Neumann algebras*"cd ||
 kMDItemTextContent == "*Banach-Mazur stability of von Neumann algebras*"cd)
```

Requests began at 2026-10-07 05:58:09 UTC (Documents) and 05:58:13 UTC (Desktop). Both exited with status 0 and no hits or reported errors. However, a scoped metadata check on the already present slide PDF returned `(null)` for both `kMDItemContentType` and `kMDItemTextContent`. Thus the known relevant PDF itself has no searchable content metadata in this environment; the no-hit result is inconclusive for generically named or unindexed PDFs. No whole-library PDF extraction or wider search followed this bounded check.

## Candidate identification

Both filename-matched PDFs were read only sufficiently to identify them: exact original bytes were hashed; Poppler `pdfinfo` checked page count/metadata; `pdftotext` checked the complete first page. Their hashes agree with the earlier primary-source audit.

| Original path | Bytes / pages | SHA-256 | Identification |
|---|---|---|---|
| `sources/roydor/roydor_slides.pdf` in this project | 459,832 / 87 | `b9202a2b4b3b50efc84a3430c593823f8c15404e83a2987be80083dc9028c36a` | Jean Roydor's CIRM October 2020 Beamer slides; correct talk title, but no complete journal article |
| `sources/roydor/ricard_roydor_1108.1970v2.pdf` in this project | 193,449 / 11 | `36eb3ae3204ff33c1e44f785358d743bbaf53b5671438e7e1a9a4fff66fb8a14` | Éric Ricard and Jean Roydor, *A noncommutative Amir–Cambern theorem for von Neumann algebras and nuclear C*-algebras*, arXiv:1108.1970v2 dated 24 June 2013; older completely bounded predecessor |

These are the already downloaded primary slide/comparator sources recorded in `research/roydor_primary.md`. Their exact absolute original paths and first-page identification are preserved in `sources/archival/local_primary_pdf_candidates_20261007.json`. Neither is the target 26-page journal article or an author manuscript of it. No new file was copied, and no license entitlement or access provenance was inferred beyond the already recorded ordinary retrieval history of these sources.

## Remaining gap and preserved record

The next material advance still requires authorized complete primary article/manuscript bytes. Then the theorem, cochain/field conventions, general/nonseparable scope, canonical-predual argument, and handling of type-I summands must be checked in that actual complete text. Bibliographic metadata, citations, an abstract, slides, and the older cb paper do not satisfy the mandatory gate.

Ignored local derived records: `sources/archival/local_primary_filename_scan_20261007.json`, `sources/archival/local_primary_spotlight_scan_20261007.json`, and `sources/archival/local_primary_pdf_candidates_20261007.json`. Existing `sources/archival/.gitignore` excludes them. No external access, download, purchase, authentication, outreach, Git action, other-project mutation, manuscript edit, frozen-review edit, or change to the prior publisher access report occurred.
