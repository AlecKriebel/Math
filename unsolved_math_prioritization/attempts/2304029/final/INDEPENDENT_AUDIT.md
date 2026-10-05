# Independent attribution and verifier audit

Audit date: 2026-10-05. Target: 2304029, catalogue rank 678, Function Theory Problem 4.29.

## Decision

**Accept `already_solved` solely as prior-resolution attribution: disproved by Roitman (1983).** The source statement matches the target. This is not an independently verified counterexample, new solution, complete proof inspection, or reconstruction of the lost historical audit.

## Evidence and exact scope

- The [2018 Hayman–Lingham draft](https://arxiv.org/pdf/1809.07200v2), printed p.80 (PDF page 81), was rechecked in text and in a fresh local rendering. Problem 4.29 requires monic P,Q, identical complex zero sets for both the polynomials and their first derivatives, and asks for positive-power equality. Update 4.29 names Roitman; reference [669] supplies the 1983 journal article.
- The [publisher's indexed abstract](https://academic.oup.com/jlms/article-abstract/s2-27/2/248/814337) explicitly reports monic integral polynomials satisfying those hypotheses without the proposed power equality. The publisher page itself could not be fetched in this independent pass. This audit does not present indexed text as a newly inspected full article.
- The [author-profile-linked transcription](https://www.academia.edu/112407536/On_Roots_of_Polynomials_and_of_their_Derivatives) identifies Theorem 8 and the same conclusion. Missing displayed formulas prevent a complete proof audit. The link from the [public author profile](https://independent.academia.edu/RoitmanMoshe) was followed independently.
- The [University of Haifa record](https://cris.haifa.ac.il/en/publications/on-roots-of-polynomials-and-of-their-derivatives/) confirms Moshe Roitman, journal publication in April 1983, volume S2-27(2), pp.248–256, and DOI 10.1112/jlms/s2-27.2.248.

Equal zero sets are not equal multisets. Integer-coefficient witnesses are within the complex-coefficient target. Monicity removes normalization ambiguity. A nonzero scalar in a putative equality P^m=cQ^n would have to be 1 by leading coefficients. No full source PDF or exact witness was obtained in this audit. Failed access was not bypassed.

## Verifier review and correction

The factored derivative formula, squarefree reduction of its complete root support, and exponent proportionality criterion are mathematically correct for exact rational input. In particular, factors with exponent greater than one must remain in the derivative support. The implementation includes them.

One input-control defect was reproduced in the frozen original: direct conversion into SymPy's QQ domain accepted Float input and could change z−1.000000000000001 into z−1. The final verifier now rejects non-exact coefficients before domain conversion. This fixes input integrity; it is not evidence for any counterexample.

All original files were hashed and copied before editing. Their original manifest entries matched those copies. `ORIGINAL_PACKET_MANIFEST.json` records their identities. The final versions are bound by `FILE_MANIFEST.json`.

## Independent controls

`test_factored_witness_independent.py` expands small examples and computes radicals by dividing by a gcd, separately from the subject verifier's squarefree-part implementation. Its power-equality oracle compares irreducible-factor multiplicities normalized by degree rather than copying the verifier's vector cross-products.

- 406 exact expansion/oracle cases passed, including rational roots, reducible factors, non-real roots, simple and repeated roots, and repeated critical points.
- 21 invalid-input controls were rejected, including approximate coefficients.
- A non-expanding control with exponents of order 10^20 passed.
- Original self-tests passed again; syntax compilation passed.
- Independent tests also passed under Python optimization, which cannot disable their explicit checks.

Both algorithms use SymPy 1.14.0. No positive counterexample fixture was tested, and these finite controls are not exhaustive. The mathematical argument supplies general correctness under the input conditions; tests provide implementation controls.

## Dataset binding boundary

The selected metadata record equals the unique matching record in the locally available 15,458-record catalog. Rank, ID, title, and problem number match the intended target. Catalog and PDF byte counts and hashes were recalculated. No upstream dataset contents are included.

The catalog record contains a descriptor and a stored statement hash, not the full statement. That stored hash was not recomputed against an upstream statement. Therefore this audit establishes descriptor-to-primary-problem binding and an exact mathematical source match, **not** byte-identical upstream-corpus or statement-hash verification.

## Publication boundary

This directory contains authored analysis, code, test outcomes, and public verification metadata. It contains no source PDFs, source-page screenshots, copied source text, dataset records, or private coordination files. No remote writes were performed by this audit.
