# A polynomial versus superpolynomial gap in vertex-distribution-free graph testing

Alec Kriebel · ORCID https://orcid.org/0009-0001-9320-500X · Version 1.0.0 · 17 October 2026.

The five-page research note gives a full negative answer to Gishboliner–Shapira's comparison question: Oberwolfach Report 19/2019, Problem 5, printed p.1139; later arXiv:1905.09903v5, Problem 5.6. The fixed property is K4-freeness intersected with the ability to become 3-colorable after deleting at most one vertex. Its classical canonical tester has polynomial sample and adjacency costs on all nonempty finite inputs. Its VDF worst-case **total sample-plus-adjacency cost** is superpolynomial, against adaptive two-sided testers, even with size, every name, full positive rational weights and the apex supplied.

The note proves the classical bound and a factor-36 reduction from ordinary triangle-freeness. It explicitly imports and credits Alon–Shapira's established two-sided triangle lower bound. Triangle hardness, local parity constructions, colorability sampling and heavy-vertex phenomena have prior sources. The possible contribution is the fixed property and its weighted comparison argument. A sample-only lower bound with unlimited free arbitrary-name adjacency queries is not asserted. No polynomial running-time claim is made.

## Files

- `main.tex` and `output/pdf/vdf-testing-gap.pdf`: operative research note and compiled five-page PDF.
- `verification/verify_all.py`: portable standard-library runner for six finite control programs, with immutable expected mathematical results under `verification/expected/`.
- `audit/inputs/PROOF.md`: unchanged pinned original self-contained proof, including the explicit rational hard family, arithmetic construction and direct adaptive parity/exposure argument. Its historical source review and metadata remain separately labeled by their original dates. The new note uses the shorter cover reduction derived during the present audit.
- `audit/reviews/`: three independent original mathematical families, the additional cover-reduction adversary, and two priority/implication reviews; reports, original programs, exact outputs, query/source ledgers and fingerprints.
- `audit/ROOT_PRIORITY_DECISION.md` and other root notes: independent reconstruction, source checks, limitations, and reproduction receipts. Historical receipts retain their original repository paths; the supplied corresponding artifacts are identified by matching suffixes and hashes.
- `PROVENANCE.json` and `SOURCE_MANIFEST.json`: pinned PR/head provenance and exact archive-member fingerprints. The source manifest covers every other source-archive member and excludes itself to avoid self-reference.
- `zenodo-metadata.json`: exact deposit metadata. The separate upload kit contains the PDF, this source/verification archive, the matching portable deposit manifest, metadata and this README.

## Verification

Use Python 3.10 or later; no additional packages or network access are required:

```text
python3 -B verification/verify_all.py
```

The default runs every control in ordinary and optimized Python modes. `--mode ordinary` or `--mode optimized` selects one mode. The runner uses temporary copies so the package stays unchanged. It verifies checker hashes, rejects any remaining Python `assert` statements, executes the programs and compares their complete mathematical results with the supplied expected JSON. The cover program's elapsed time and self-reported original script hash are excluded from mathematical comparison; its actual public code hash is separately verified. All case data, optimal edit costs and witnesses remain compared.

The six programs test: all graphs through six vertices and color-list steps; all-size high-precision parameter/coupon controls; arbitrary weighted repairs and arithmetic/parity/wheel constructions; exhaustive finite adaptive-query policies and posterior symmetry; exact tripartite-cover triangle hitting sets for all 76 graphs through four vertices including the empty graph; and 75 nonempty cover/apex controls including every arbitrary-edit target on at most five vertices. These checks are finite falsification attempts. Universal claims rest on the written proofs and the explicitly cited classical theorem.

Historical reviewer programs use assertions where originally written and are retained unchanged with their hashes. Public checking copies are mechanically converted into explicit conditional failures. `verification/VERIFIER_PROVENANCE.json` records original/public hashes, the number of replaced assertions and comparison exclusions; the converter is included. The original checks were first reproduced unmodified in ordinary mode. Converted copies are checked in both modes. Generic false-guard controls are recorded in the root receipts. Neither a successful finite run nor compilation is a proof certificate.

## Sources and priority limits

The current broad audit contains 72 actual search strings and 41 retrieval receipts; the focused implication audit and root's 17 queries are separate and overlap. Counts are not summed as globally distinct searches. Primary bodies and current version histories were checked, including the original workshop report, GS arXiv v5/ECCC revision 2/author manuscripts, Goldreich's October 2021 revision, Alon–Shapira's two-sided theorem, AKKR's older parity construction, Fei's August 2026 v2 and recent standard-model testing work.

No earlier full comparison answer or verified previously published full consequence was identified. This is bounded evidence, with priority and novelty uncertified. The official 2021 GS journal version-of-record body was unavailable; inspected manuscripts were not assumed identical to it. Forward-citation retrieval was incomplete, and the original full Behrend and Ruzsa–Szemerédi articles were not recovered. All inspection limits and unsuccessful retrievals are retained in the source ledgers. The original direct proof supplies the needed combinatorial constructions in full. Third-party article bodies, extracts, images and private caches are excluded from this package.

## Rebuild and status

Compile `main.tex` with a standard LaTeX setup or Tectonic, writing `output/pdf/main.pdf`; then run `python3 -B build_package.py` to build the two archives. It verifies the original review-artifact fingerprints, regenerates the explicit-guard copies, runs all twelve checks and creates member manifests. The live-repository deposit manifest is resolved relative to this folder; the upload kit's manifest uses filenames beside itself. A rebuild can change PDF metadata or compiler-dependent bytes; release fingerprints identify the exact published files.

AI tools were used extensively in development, verification, literature review and writing. The note, proofs and supplements are unrefereed. Independent adversarial reviews were AI-assisted; no external human peer review, journal acceptance or formal proof-assistant certification is claimed. Original authored materials are licensed CC BY 4.0; third-party works retain their own rights.
