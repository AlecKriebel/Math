# Knots with determinant 4k + 1 and signature four

This packet supplies a complete attributed proof and AI-assisted acceptance audit for problem **10400226 / AMR-103-0226**, the question of Y. Shinohara recorded as Ohtsuki Problem 12.21.

**Accepted conclusion:** for every integer n > 1 with n ≡ 1 (mod 4), there is a tame knot in S³ with determinant n and signature 4. The construction gives genus at most two for nonsquares and for squares having a prime divisor congruent to 3 modulo 4, and genus at most three for the remaining squares. It makes no universal genus-two claim.

## Attribution and limits

The construction is credited to **Alper Ferudun**, *Knots with Signature 4 and Determinant 4k+1: An Answer to a Question of Shinohara*, Theorem 1.1 and Lemmas 3.1–3.2, dated **2 October 2026**, [DOI 10.5281/zenodo.23111900](https://doi.org/10.5281/zenodo.23111900), [manuscript page](https://eulersolve.org/papers/amr-103-0226/). The author describes the manuscript as an **unrefereed, AI-assisted preprint**. These status observations were checked on 11 October 2026.

This packet claims no novelty, human peer review, external refereeing, or certification of the source paper as a whole. Its acceptance covers the stated unrestricted-knot existence theorem. It does not certify ancillary classification, lattice-theoretic, knot-table, minimal-crossing, or software claims.

## Reading the proof

- [PROOF.md](PROOF.md) is the complete expanded proof, preserved byte-for-byte from the accepted audit.
- [CANDIDATE.md](CANDIDATE.md) preserves the original authored reconstruction byte-for-byte. Its closing statement that acceptance is subject to independent review is historical; the subsequent scoped acceptance is recorded in [AUDIT.md](AUDIT.md) and [ACCEPTANCE.json](ACCEPTANCE.json).
- [AUDIT.md](AUDIT.md) gives all twelve independent mathematical checks, numerical diagnostics, source assessment, and acceptance limits.
- [SOURCE_PINS.json](SOURCE_PINS.json), [RETRIEVALS.json](RETRIEVALS.json), and [INPUT_PIN_CHECKS.json](INPUT_PIN_CHECKS.json) contain public-source verification metadata.
- [CHECK_RESULTS.json](CHECK_RESULTS.json) contains aggregate checks. [EDITORIAL_MAP.json](EDITORIAL_MAP.json) identifies presentation-only edits, and [MANIFEST.json](MANIFEST.json) closes the public-file inventory.

The proof explicitly retains classical Seifert-matrix realization, Dirichlet’s theorem for reduced progressions, quadratic reciprocity, the Chinese remainder theorem, and Sylvester’s criterion. The prime-existence step is mathematical and unbounded; it is not inferred from finite searching. In the remaining-square construction, the symmetric determinant is **−n** and the knot determinant is its absolute value **n**. Mirroring handles the opposite signature convention without changing determinant.

## Verification scope

Fresh exact diagnostics passed under ordinary Python, -O, and -OO, with byte-identical full outputs. They cover all 2,500 admissible n from 5 through 10,001 and four further distinct cases, plus 1,427 alternate divisor-branch checks. This is corroborating finite evidence; the proof supplies the all-integer quantifier.

The public directory includes authored mathematics and public bibliographic, inspection, retrieval, hash, and aggregate-check metadata. It includes no copied source documents or extracted source text, inspection images, executable scripts, raw test matrices, or witness datasets. Symbolic matrix formulas remain in the proof because they are essential mathematical content. The manifest lists every public file except itself and is externally sealed; an integrity seal does not constitute mathematical or human authentication.
