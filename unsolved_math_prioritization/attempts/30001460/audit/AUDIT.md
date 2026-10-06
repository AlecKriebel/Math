# Independent adversarial audit: geometric quotients of K-sheets

Date: 2026-10-06. Problem 30001460 / OWR-4332-001, catalog rank 826.

## Verdict

**Accept as a scoped partial result, with one minor wording clarification.** The connected-adjoint-centralizer gluing criterion and its application to every gl_n/sl_n K-sheet survive this audit, with possibly nonseparated scheme targets, algebraically closed characteristic-zero base field, and connected K. The general nonregular arbitrary-type problem is not resolved.

The author ZIP was preserved byte-for-byte: 16,235 bytes, SHA-256 41b212dc7842cdedf598efebf41976351489115363f30ab2cb599cfa93050e34. No mathematical rejection or required change to the theorem was found. This is an independent mathematical review, not a formal proof-assistant certificate or a novelty determination.

## Main failure modes checked

1. **G-orbits versus K-orbits.** An ambient G-orbit can contain several K-orbits. The proof restricts its G-section to one K-saturation U_i. Within this saturation every point is conjugate to its slice value, so a local fiber cannot merge distinct K-orbits. Using the ambient quotient on all S instead would fail already in rank one.
2. **Coverage.** The inspected Bulois–Hivert proposition gives an actual open cover. Nilpotents initially in the closure have the same orbit dimension and hence lie in the sheet, which is closed in the relevant orbit-dimension stratum. Density of a single saturation was not substituted for coverage.
3. **Scheme morphisms.** Reduced locally closed factorization is legitimate. Smooth action covers supply faithful pullback for categoricality and the overlap identities. The supplement spells out inverse morphisms, cocycle domains, universal openness, and the invariant structure sheaf.
4. **Target category.** The quotient is a scheme by open chart gluing. Separatedness is neither proved nor assumed. The doubled-origin line is a positive quotient example and a counterexample only to a separated-target interpretation.
5. **Group choice.** G is adjoint. GL_n nilpotent centralizers are irreducible, and PGL_n nilpotent centralizers are connected. Regular-nilpotent SL_n centralizers have n components. The effective torus coordinate in PGL_2 has weights +1,-1; diag(u,u^-1) in SL_2 has weights +2,-2. Neither covering-group mistake occurs in the frozen proof.
6. **Type-A scope.** The supplement gives intrinsic ambient-sheet containment and separates off the scalar-center eigenspace, so “any involution” does not depend on an unstated choice of center sign.
7. **Literature scope.** The original 2010 question does not explicitly specify separated targets. The published 2025 Hameister–Morrissey result cited through v3 is a regular-locus result. It is not used as a theorem about every nonregular sheet.

## Clarification

The opening summary's phrase “no orbit-separating morphism” should explicitly include “K-invariant.” The detailed argument already does. CLARIFICATION.patch changes only that phrase and was not applied to the preserved freeze. There is no revised theorem or altered classification.

## Independent verification

- All three complete supplied corpora were freshly hashed and parsed. Their byte counts, record counts, and SHA-256 pins match. Rank 826 and problem number OWR-4332-001 match uniquely.
- The full-record/default-sorted-JSON review serialization is 3,264 bytes and hashes to 93431b0f7dfb31ed0a593e4e93b1f50f721e616143e026971b66530bdf2ce11b. The report lookup is absent and correctly falls back to an empty object. The 111-byte statement pin also matches. No dataset content is reproduced.
- A separately authored replay harness was run normally and under Python -O, with identical reports. Each harness run executes four successful baseline/relocation variants and rejects all 24 static tamper variants. Mutated verifier and certificate payloads did not execute.
- An independent SymPy 1.14.0 checker verifies 38 exact matrix/rational identities and five mathematical countercontrols. It was run normally and under -O with identical output. The n=2..8 centralizer controls illustrate the group-choice hazard; the general connectedness argument is mathematical, not inferred from those cases.
- Four local source PDFs were freshly hashed against the recorded pins. Relevant source text was inspected; the OWR question, open-cover proposition, and HM theorem were also visually inspected, and Bulois's theorem/connectedness pages were independently re-rendered and visually checked.
- Public primary-source metadata was rechecked for publication titles/status and the Stacks descent/gluing statements. No exhaustive claim about all later literature or repository history is made.

## What these checks do not prove

File hashes and finite controls do not prove Theorem A, descent, completeness of a literature search, novelty, or a full resolution. The static mutation harness assumes a trusted interpreter and no concurrent hostile filesystem writer. No source PDF, extracted source text, corpus, or private coordination record is included in this audit archive.

## Accepted use

The result may be described as an independently audited partial answer: a connected-centralizer sufficient criterion, all gl_n/sl_n sheets with possibly nonseparated targets, and a rank-one separated obstruction. Preserve the arbitrary-type nonregular limitation whenever reporting the outcome. The proof and review remain deductions from credited published inputs; no novelty is asserted.
