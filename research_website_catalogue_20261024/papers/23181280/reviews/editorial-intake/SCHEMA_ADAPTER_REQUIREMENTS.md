# Private schema/consumer requirements — pending root clearance

This file specifies a future adapter; it is not an implemented helper, renderer patch or publication configuration. All current scientific/publication adoption gates remain false. Canonical site URL, AA and follow-up remain null. The selected source URL is a bibliographic Zenodo URL, not an assigned site canonical.

## Preserve the exact original interfaces

The actual source record is `sources/zenodo-record.raw.json`; do not create a `record.json` alias. The original `api-receipt.json` is a five-entry list with record/latest/versions transport entries and two real published-file transport entries. Each published-file entry includes its full `api_file_object`; the endpoint entries do not. The separate `record-transport.json` duplicates actual record transport facts in its own original shape. Preserve every field, original case, full headers, paths, timestamps and all five entries. Never replace these with a generic receipt or invent fields named `status`, `url`, `actual_file_object` or HTTP facts that are absent from this interface.

A future read-only in-memory consumer may authenticate the original record/latest/versions objects, match the two actual `files` entries by exact `key`, advertised size/MD5 and actual `links.self`, and compare the full PDF/ZIP bytes and SHA256 pins. Use the actual file objects; do not infer content URLs from a guessed filename convention. No original JSON, filesystem alias, on-disk normalized record or synthesized transport history may be written.

All three full custom verdict objects are copied byte-for-byte under `original-objects/reviews/{scope,analytic,adversarial}` with their original filenames/case. Their differing disposition strings, arrays, nested objects, false publication gates, null gaps, original prose and receipts remain unchanged. A later exact root clearance and editorial adoption must be separate explicit authority objects. An adapter cannot fill a missing generic PASS, rewrite original fields to satisfy a generic validator, or treat these favorable family findings as present root authorization.

## Reader/source/citation contract

The sole selected reader is the complete four-page outer `root_dependent_spanning_trees.pdf`. The one embedded ZIP PDF is byte-identical; it does not provide a second edition or justify rebuilding the reader. The entire 47-member `root_dependent_spanning_trees_support.zip` must be the unchanged support download. The page must not export a hand-picked script bundle or its private intake objects. Preserve all archive license notices and historical source metadata within that complete archive.

After separate authorization, the existing simple blog layout should expose one full local PDF iframe, a direct local open link, two explicit PDF download links (unchanged local file and actual Zenodo original), both complete-ZIP links, selected-record DOI and exactly prepared BibTeX. The full original abstract must be ordinary visible/indexable prose, with only whitespace and TeX nonbreaking-space presentation changes. Keep the entire actual title, sole author/ORCID, declared 6 October 2026 date, version 1.0, unrefereed status and CC BY 4.0 header/schema label. API creation/update timestamps are separate private provenance, not publication-priority evidence.

The future checker must validate the whole model: one common undirected tree; every entire root orientation charged; all explicitly binary-encoded costs; strong NP-completeness for both stated alphabets; the equivalent inward transpose; no Problem 2 or unrestricted MAXSAT identity. No code implementation or site testing is claimed in this intake.
