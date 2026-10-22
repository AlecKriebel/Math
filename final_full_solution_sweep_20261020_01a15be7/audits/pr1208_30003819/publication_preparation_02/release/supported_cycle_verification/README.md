# A singleton-supported cycle correction to Byrnes's differential-poset bound

Alec Kriebel, independent researcher. ORCID: https://orcid.org/0009-0001-9320-500X. Version1.0.0, 22October2026. Unrefereed preprint. The seven-page paper is `paper.pdf`; `main.tex` is its complete editable source.

For every ordinary unweighted r-differential poset and n>=2, the theorem subtracts q_n=beta(H_S) from Byrnes's cumulative upper bound. H_S is the preceding-rank incidence subgraph supported on elements with a singleton successor, retaining all vertices on the other side. Terminal-preserving witness trees prove b_n>=q_n. The correction is nonnegative, depends only on preceding incidences, and is positive and attained on the standard r=3 reflected Y^3 prefix and r=1 reflected Young prefix. Its coefficient one is sharp. A conditional two-witness equality theorem and the all-r rank-three consequence are proved.

This answers the printed request for an improvement of Byrnes's inequality in an incidence-dependent form. It does not prove Stanley's general local recurrence, improve the global Fibonacci envelope, or provide a combinatorial strict-growth proof. Classical incidence counts, graph facts, singleton techniques and Wagner reflection of Young prefixes are credited. Gaetz–Venkataramana Proposition3.4 already contains the exact two-singleton rank-one lemma used in the rank-three deduction. The substantive assertion is the supported-cycle transfer inequality. `ATTRIBUTION.md` records the dated bounded comparison and its limits; no historical firstness, new general mechanism or present worldwide openness is certified.

## Contents and historical scope

- `main.tex`, `paper.pdf`: complete operative paper and frozen PDF.
- `verification/exact_checks.py`, `verification/EXPECTED.json`: independent standard-library exact computations and their complete expected output bytes.
- `reproduce.py`: closed-inventory verification and normal/-O/-OO replays without network use or modification of release inputs.
- `original/`: all eight unchanged authored files from PR1208 at head5b238897f7e3f1008bd44c2cc5b5a01d8fbeae51. `ORIGINAL_BINDING.json` pins their bytes and the supplied base. Their historical labels and reproduction limitations remain historical facts. The new paper treats the original improvement clause separately from the stronger recurrence; it does not edit those earlier records or claim to recover their omitted programs.
- `ATTRIBUTION.md`, `SOURCE_IDENTITIES.json`, `PROVENANCE.json`: authored source comparisons, identities, edition and review limits. Source hashes identify inspected versions; they do not provide an offline proof of literature absence.
- `PDF_VISUAL_QA.json`, `BUILD_RECEIPT.json`: compiler and actual seven-page visual inspection scope, separate from mathematical proof.
- `zenodo-metadata.json`, `zenodo-deposit.json`: matching native metadata and a two-file local deposit manifest. No DOI is reserved or fabricated.
- `SOURCE_MANIFEST.json`: exact closed inventory, hashing every other member. Obtain its digest independently when checking custody.

The original prose/audits and the current paper/code are authored material. Third-party full texts, extracted bodies, source images, full ledger/account responses, access identifiers and private coordination are excluded. The original files mention historical internal packet digests whose absent members are not supplied or newly authenticated by this distribution. Current reproducibility uses the new code and expected output below.

## Reproduce the exact finite checks

Python3.10 or later and its standard library suffice. In a fresh extracted copy run:

```sh
python3 -B reproduce.py
```

Optionally add `--manifest-sha256 HASH` using the independently obtained SOURCE_MANIFEST.json digest. The runner verifies a closed inventory, copies the checker into a temporary directory, and compares complete stdout bytes and empty stderr in normal, -O, and -OO modes against EXPECTED.json. It verifies that all release input bytes remain unchanged. No download, third-party library, compiler or candidate program is required.

Checks include the actual witness trees and components, commutators, edge/cycle identities, all labeled extensions for r=1 through rank7 and r=2,3 through rank3, reflection r=1..5 through rank5, Young's lattice through rank12, sharp examples and negative controls. There are5764 checked witness selections. Every reflection-only run uses first and last witness choices regardless of product size. Enumerated-prefix, Young-lattice and separate sharp-example runs exhaust products of at most2000 choices and use first/last above2000. The proof establishes the arbitrary-choice claim. Finite checks do not prove the general recurrence, exhaustive priority or formal proof certification. Labels are retained: counts are not isomorphism-class counts.

## Rebuild the files and upload kit

In a disposable extracted copy run:

```sh
python3 -B build_package.py
```

It verifies the source package and exact computations, then creates a sibling `output/` directory with the frozen PDF, complete source/verification ZIP and five-member upload kit. The builder uses sorted paths and fixed ZIP timestamps; the same Python/zlib runtime reproduces identical archive bytes. Compression-version differences can change ZIP bytes while preserving members. The frozen PDF is an explicit input; this command does not recompile or publish.

To revise the paper, compile `main.tex` with a LaTeX engine supporting the listed standard packages (the release PDF used official Tectonic0.17.0), render and inspect every page, update source identities/receipts/manifests, and submit the changed package for review. Recompilation can change PDF metadata and bytes. The built-in editor compiler also successfully compiled the source. The bibliography is inline; no external .bib or image files are needed.

The upload kit contains exactly two scientific assets, the native metadata, a portable flat-path deposit manifest and instructions. Repository Zenodo tooling stages/verifies/publishes through distinct later operations. No publication is performed by this package. Fresh whole-package review and release authorization are separate gates; the preparation receipt does not certify them.

## AI involvement and licenses

AI tools were extensively involved in research planning, mathematical exploration and proof development/reconstruction, code and exact computations, source/literature investigation, writing, editing and adversarial verification. Alec Kriebel is the named human author. The paper and materials are unrefereed; there has been no professional independent human peer review, journal acceptance or formal proof-assistant certification. Internal AI reviews do not supply those certifications.

Original prose is CC BY4.0 (see LICENSE-PROSE.txt); code is MIT (LICENSE-CODE.txt). Cited third-party works retain their rights. This source archive is designed to be public only after the required review/release gates; it carries no raw private evidence.
