# Publication-safety and editorial provenance

## Included

- Complete authored mathematical proofs, accepted audits, acceptance manifests, scope analysis and safe diagnostics
- Public scholarly titles, citations, URLs, manuscript-status observations, source-document hashes and byte counts, and retrieval/inspection metadata
- New reader navigation, precise scope summaries, package-integrity checks and replay evidence

## Excluded

Copied third-party source PDFs, extracted source text and page images; dataset records or contents; private sources, personal material, private coordination files, correspondence and operational ledgers are excluded. Citation metadata naming a source PDF does not mean that PDF is bundled.

## Exact preservation

Every original admitted to the reader is identified in `ORIGINAL_ARTIFACTS.json`. Its bytes and hash are unchanged. There are no editorial transformations to those originals. The original relative proof/audit layout is retained in `accepted/`; self-contained source-context and source-scope collections each retain their own filenames and manifests.

The two primary preserved manifest anchors are:

- `accepted/pass1_audit/ACCEPTANCE_INDEX_MANIFEST.json`: SHA-256 `10ee2c58e2bfc0314531c768ca7daf19739a31a0869d4a7ddd037c26be8e9d96`
- `accepted/pass1_hardy/MANIFEST.json`: SHA-256 `639004491380b086324f5cce2a378226e7080ec18cd8a134bf1147d94dc2d074`

Reader summaries and tools are new files, not silently edited proof versions. Earlier reports remain historical snapshots. Later accepted supplements and the final scope adjudication govern the current overall summary.

The replay harness copies the original programs into temporary directories before execution. Two original spectral programs write a diagnostic beside themselves; isolation prevents alteration of the preserved reports. Forced-failure controls modify only temporary program copies and change check-enforcement inputs, not the originals or mathematical arguments. Their sole purpose is to demonstrate active failure detection in each Python optimization mode.

The root manifest seals the entire public file set except itself. The archive receipt separately pins that manifest and the deterministic archive. Hashes establish exact identity, not mathematical correctness, scholarly novelty, or publication authorization.

No remote publication, repository commit, push, or queue edit is performed by preparing this reader.

## Reviewed edition

The independent integration review preserves every original byte and adds only authored review reports and public verification metadata. Editorial changes to reader navigation and validation are mapped in [the change record](review/EDITORIAL_CHANGES.json). The final source-scope report and original-copy map are additional frozen anchors. Every text file, including validation code, is scanned without a filename-wide exemption; all filesystem entries are classified. These checks support, but cannot replace, the manual content/provenance review recorded in [the independent report](review/INDEPENDENT_INTEGRATION_ACCEPTANCE.md).
