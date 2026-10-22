# A simple brace outside asymmetric products of two trivial braces

Alec Kriebel · ORCID https://orcid.org/0009-0001-9320-500X · Version 1.0.0 · 17 October 2026.

This five-page research note gives a full negative answer to Cedó's Problem 9 in Oberwolfach Report 51/2019, printed p.3228 (problem 30004311; OWR-17294-011). The explicit nontrivial simple left brace has order 20,000, abelian additive group C5^4 × C2^5, and metabelian multiplicative group (C5^3 ⋊ C2) × (C2^4 ⋊ C5), with every multiplicative Sylow subgroup abelian. It has no presentation as an asymmetric product of two trivial braces.

The note proves the operations, group structure and simplicity directly. A universal obstruction covers the full admissible symmetric-cocycle definition: every two-trivial-factor product with abelian multiplicative Sylow subgroups has zero triple star products on each additive primary subbrace. In the example (x*x)*x = x^3 is nonzero in the 5-primary subbrace. Established asymmetric/matched-product, radical-ring, logarithm/exponential and orthogonal-action methods are credited. No new general construction formalism is claimed.

## Files

- `main.tex` and `output/pdf/simple-brace-counterexample.pdf`: operative paper and compiled five-page PDF.
- `verification/verify_all.py`, `CONTROL_PLAN.json` and `REPLAY_RECEIPT.json`: portable runner, pinned unchanged programs/results and deterministic execution receipt.
- `audit/inputs/`: all eight original PR artifacts, unchanged. Historical source reviews and acceptance metadata retain their original dates and scope; present reports supersede historical priority summaries.
- `audit/reviews/`: three independent mathematical families and two priority/implication reviews, including exact programs, results, per-seed certificates, source-version records, search ledgers and authored-artifact fingerprints.
- `audit/ROOT_MATHEMATICAL_CHECK.md`, `ROOT_PRIORITY_DECISION.md`, `ROOT_PRIORITY_SOURCE_NOTES.md` and other root notes: independent reconstruction, current priority decision, inspection limits, PDF QA and unchanged-code reproduction receipts.
- `PROVENANCE.json` and `SOURCE_MANIFEST.json`: exact PR/head provenance and member fingerprints. The manifest covers every other source member, excluding itself to avoid circular self-hashing.
- `zenodo-metadata.json` and `zenodo-deposit.json`: exact release metadata and repository-relative deposit manifest. The upload kit contains the PDF, source archive, identical metadata, portable deposit manifest and this README.

Historical receipts retain original repository paths; corresponding packaged files are identified by suffix and matching hashes. Third-party article bodies, extracts, images, raw API responses and private caches are excluded. Bibliographic metadata and authored inspection notes remain included.

## Reproduction

Use Python 3.10 or later with the standard library; no installs or network access are required:

```text
python3 -B verification/verify_all.py
```

The runner executes all four unchanged programs in ordinary and optimized modes (eight runs). `--mode ordinary` or `--mode optimized` selects one mode. Temporary mirrors preserve the supplied package. Before execution the runner verifies proof, checker and expected-result hashes and rejects Python `assert` statements. All original programs already use explicit failures, so no program conversion is needed.

The construction program checks all ring/logarithm ingredients and factored group/lambda identities, with all 19,999 nonzero ideal seeds and deliberately broken controls. The obstruction program tests general cocycle boundary cases, including a nonbilinear cocycle that fails the brace law and a nonabelian Sylow example violating the conclusion. It also checks the original redundant fixed-set and center witnesses. The finite program independently encodes the whole example, emits deterministic per-seed derivations to nine additive generators and tests broader small-cocycle families and mutations. The symbolic program verifies the universal degree-four logarithm/exponential identities over F5[X,Y] modulo total degree five, plus all binary quadratic/action ingredients.

Complete expected mathematical JSON is compared. The symbolic program's expected result is read from the corresponding mode in its historical execution-receipt wrapper; its recorded code hash and successful exit codes are also checked. Only the finite program's `started_utc`, `completed_utc`, `python_version` and per-stage `seconds` are excluded as runtime metadata. Its actual checker hash, proof hash, guard counts, cases and witnesses remain compared. Both finite-program certificate files must match the supplied bytes by length and SHA-256. Ordinary and optimized execution receipts are deterministic; the original expected results retain their historical runtime metadata.

These are finite falsification attempts and checkable certificates, not a substitute for the all-ideal or universal nonpresentation proofs. No enumeration of all 20,000 cubed triples is claimed. Compilation and successful program runs are not formal proof certificates.

## Sources and priority limits

A bounded current primary-source audit identified no prior full answer or verified published full implication. The broad audit contains 88 actual search strings, 64 unique forward-citation records and 23 PDF retrievals including repeated versions. A query-defined 2024–2026 arXiv screen returned 257 records with complete pagination; 155 mathematical titles and relevant abstracts were screened, not all 257 papers read. A focused review checked 11 primary PDFs at recorded boundaries and supplied three newly proved exclusions for plausible prior construction families. The root performed 40 additional queries. Overlapping searches are not summed as globally distinct searches.

The full bodies of Rump 2020 and 2022 were not obtained. Several final-journal-body comparisons, including the 2025 Cedó–Okniński article, are incomplete; inspected preprints are not assumed identical to final versions. Broader consequences are not excluded by abstracts. Citation indexes and the recent query-defined screen are not exhaustive. Exact versions, access failures and inspection boundaries are documented. Historical novelty and exhaustive priority remain uncertified. No human was contacted or outreach prepared.

## Rebuild and status

Run `python3 -B build_package.py` to verify pinned review artifacts, run the eight controls and deterministically rebuild the source archive and upload kit. The frozen operative PDF is an input and is never silently recompiled or replaced. From an extracted source archive, the same command reproduces both archive bytes under the same Python/zlib environment. A different compression runtime may alter ZIP bytes without changing member contents. The builder uses explicit file lists, so subsequent review or publication receipts cannot silently enter a rebuilt release.

To revise the paper, compile `main.tex` with LaTeX or Tectonic, inspect all rendered pages, deliberately replace the operative PDF and update its QA receipt before rebuilding. Compiler-dependent PDF bytes can vary; release fingerprints identify the published files.

AI tools were used extensively in construction, proof development, computation, adversarial verification, literature research and writing. The note and supplements are **unrefereed**. Independent adversarial reviews were AI-assisted; no external human peer review, journal acceptance or formal proof-assistant certification is claimed. Original authored materials are CC BY 4.0; third-party works retain their own rights.
