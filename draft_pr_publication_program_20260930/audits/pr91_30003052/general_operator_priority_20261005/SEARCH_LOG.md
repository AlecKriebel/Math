# Search log

Searches were executed in the order below from 2026-10-05 19:13 UTC to 19:21 UTC. Literal query strings, including quotation marks and filters, are preserved in EXACT_QUERY_INPUTS.json (43 queries across 11 batches); the normalized terms below provide a readable index. Raw outputs preserve returned source snippets, reference metadata, source URLs, and error outcomes. A returned result is discovery evidence, not proof-read evidence.

## Batch 01

Raw result: SEARCH_01_RAW.json

- Operator Theoretic Aspects of Ergodic Theory pdf Eisner Farkas Haase Nagel equicontinuous
- Kitover spectrum composition operator C(K) compact dynamical system spectrum
- Koopman linear unit ball spectrum composition operator
- composition operators contractions continuous functions spectrum linear

## Batch 02

Raw result: SEARCH_02_RAW.json

- composition operators C(K) spectrum periodic
- Kitover The spectrum of disjointness preserving operators
- composition operators C(X) spectra compact Hausdorff
- equicontinuous Koopman point spectrum continuous

## Batch 03

Raw result: SEARCH_03_RAW.json

- Kitover Spectrum of weighted composition operators: part 1 pdf
- Koopman equicontinuous Jacobs continuous spectrum
- composition operator spectrum C(X) Kawamura
- spectrum composition operators non-surjective C(K)

## Batch 04

Raw result: SEARCH_04_RAW.json

- Spectrum of weighted composition operators 2011 Kitover pdf -site:citeseerx.ist.psu.edu -site:researchgate.net
- Kitover s11217 639
- Kawamura composition operators spectrum continuous
- On the isomorphism problem for non-minimal transformations with discrete spectrum arxiv

## Batch 05

Raw result: SEARCH_05_RAW.json

- Kitover Spectrum Positivity 15 10.1007
- Spectrum of weighted composition operators: Part 1
- composition operator C(X) point spectrum compact
- equicontinuous spectrum linear systems Koopman

## Batch 06

Raw result: SEARCH_06_RAW.json

- s11117-010-0106-4 pdf
- Kitover 3.23 3.12 spectrum
- Spectral properties of weighted homomorphisms of algebras of continuous functions
- Kawamura Spectra of composition operators

## Batch 07

Raw result: SEARCH_07_RAW.json

- Le spectre des operateurs de composition Montador
- Kitover 107 89 1982 mathnet
- Jacobs de Leeuw Glicksberg C(K) projection Koopman
- Koopman continuous attractor peripheral spectrum

## Batch 08

Raw result: SEARCH_08_RAW.json

- Le Spectre des Opérateurs de Composition Sur C[0,1] Cambridge
- The spectral properties of weighted homomorphisms Kitover mathnet
- On the isomorphism problem for non-minimal arxiv.org

## Batch 09

Raw result: SEARCH_09_RAW.json

- Spectrum of weighted composition operators: part 1 Kitover -site:citeseerx.ist.psu.edu -site:researchgate.net -site:eurekamag.com
- Kitover composition 0106
- Kitover 3.10 3.12 2011
- On the isomorphism problem for non-minimal transformations with discrete spectrum pdf -site:researchgate.net

## Batch 10

Raw result: SEARCH_10_RAW.json

- Koopman peripheral factor continuous linear
- composition operator equicontinuous eigenvalues
- Koopman stable reversible A ball
- linear Koopman C(U) spectrum

## Batch 11

Raw result: SEARCH_11_RAW.json

- composition operator asymptotic eigenfunctions continuous
- Koopman asymptotic pairs
- unimodular eigenfunctions equicontinuous projection
- Kitover spectrum C(K) point spectrum

## Adaptive opens and HTTP retrieval

- OPEN_01_RAW.json: ScienceDirect PartVII open403; generic Springer search inaccessible.
- OPEN_02_RAW.json: primary KitoverPartI landing page opened successfully; subscription preview only, with title, online date and broad abstract/reference list.
- OPEN_03_RAW.json: Montador DOI inaccessible to web reader; MathNet person page inaccessible; Edeko primary publisher article read; Batch08 includes full-text HTML click that returned a short no-login landing page.
- RETRIEVAL_01.json: EFHN author PDF and PartVII arXiv primary PDF successfully fetched, with hashes and actual HTTP statuses.
- RETRIEVAL_02.json: PartI attempted PDF returned HTML rather than a PDF. It was renamed sources/kitover2011_pdf_attempt.html; metadata is not silently promoted to full-source access.
- CROSSREF_2011_RAW.json: direct Crossref bibliography query established DOI and date; not theorem evidence.
- RETRIEVAL_03.json: primary-linked Crossref/Montador/Edeko metadata retrievals; MathNet403 recorded.
- RETRIEVAL_04.json: Montador primary publisher PDF fetched; obsolete Edeko PDF path404.
- RETRIEVAL_05.json: Edeko primary publisher export endpoint fetched genuine PDF; direct PartVII journal PDF/HTML403.
- RETRIEVAL_06.json: Küster2021 institutional PDF fetched.
- EXTRACTION_01.json: actual successful pdftotext commands for EFHN/PartVII, with argv and return codes. Later text extractions executed in retrieval scripts and are evidenced by the tool's successful checked subprocess execution and retained text; final manifest independently checks all genuine PDF files.
- RENDER_01.json, RENDER_02.json, RENDER_03.json: actual pdftoppm command outcomes, including first EFHN pages rendered before the +18 offset was identified and correct relevant pages rendered afterwards. Wrong-offset renders are not represented as relevant theorem inspection.

The primary-source date cutoff is 2026-10-05. No individual was contacted. False-negative searches and subscription previews do not prove worldwide absence.

