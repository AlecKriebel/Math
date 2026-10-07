# Source, scope and status audit

Checked 2026-10-07 UTC. This is a source-free authored audit. No paper, extract, dataset, local coordination material or copied screenshot is part of the public packet.

## Original question

The relevant source is Wenfei Liu's contribution with Sönke Rollenske, printed p. 1598 of Oberwolfach Report 27/2013. The workshop was 26 May–1 June 2013. The report was published on 17 March 2014, so the volume year 2013 and publication year 2014 are different legitimate dates. DOI: https://doi.org/10.4171/OWR/2013/27 ; publisher: https://ems.press/journals/owr/articles/12490 . The downloaded PDF's printed p. 1598 was inspected as text and as a rendered image.

There are two separate questions. The first asks about rK_U on the Gorenstein locus while allowing reduced boundary. The second asks for failure of very ampleness of 5I(K_X+Δ). The missing Δ in the first question is present in the printed source, not merely a corpus transcription error. Its literal reading fails by PROOF.md §1. Treating K_U as shorthand for a log canonical divisor requires an explicit interpretation. The second question is not resolved by the first one's wording problem.

## Established bounds and exact hypotheses

Write P=K_X+Δ and L=IP. All [LR] statements below use connected complex stable log surfaces with reduced boundary; stability includes ampleness. The following are cited results, not new claims:

- [LR] Theorem 4.1: mL is globally generated for m≥4; m≥3 suffices if I≥2. Further index-one improvements require the listed normalization-volume/nodal or normality hypotheses.
- [LR] Theorem 5.1: mL is very ample for m≥8, birational for m≥6, and very ample for m≥6 when I≥2.
- [LR] Theorem 5.2(iii): mL is very ample for m≥5 if T=D∪Δ is nodal, the normalization is smooth along the conductor, and X\D has only canonical singularities. This includes semi-canonical pairs.
- None of these states that all Gorenstein slc pairs are semi-canonical, or that degree five is universally very ample.

The version inspected is arXiv:1211.1291v4, dated 14 April 2014. The publication is Advances in Mathematics 258 (2014), 69–126, https://doi.org/10.1016/j.aim.2014.03.009 . Its statement and notation are read from the paper, not inferred from the abstract. Relevant locations are §§1–2, Proposition 3.6, Theorems 4.1 and 5.1–5.2, Lemmas 5.4 and 5.6, and Remark 5.8.

These are Cartier-index-multiple statements for projective surfaces. They neither remove the index nor prove a fixed-exponent theorem on an open Gorenstein locus. Reduced-boundary results must not automatically be advertised for arbitrary rational boundary coefficients. Neither birationality nor basepoint-freeness is interchangeable with very ampleness. Surface results do not settle higher-dimensional analogues.

## Later and related results checked

1. Osamu Fujino, Effective basepoint-free theorem for semi-log canonical surfaces. Author PDF: https://www.math.kyoto-u.ac.jp/~fujino/Fujita-type4.pdf . Corollary 1.5 and Remark 5.3 extend the freeness statement to non-reduced boundary coefficients; the very-ampleness discussion in Remark 7.3 gives 12I for surfaces, or 9I when I≥2. It does not supply a universal degree-five theorem.
2. Sönke Rollenske, A new irreducible component of the moduli space of stable Godeaux surfaces, https://arxiv.org/abs/1404.7027 . The introduction explicitly discusses searching for a degree-five counterexample; the constructed family instead has very ample 5K. This is evidence about one family, not a universal resolution.
3. Marco Franciosi, Rita Pardini and Sönke Rollenske, Gorenstein stable surfaces with K_X²=1 and p_g>0, https://arxiv.org/abs/1511.03238 . Propositions 3.6–3.7 give degree-five embeddings in those cases. Their scope excludes arbitrary invariants and non-Gorenstein surfaces.
4. Marco Franciosi and Sönke Rollenske, Canonical rings of Gorenstein stable Godeaux surfaces, https://arxiv.org/abs/1611.06810 . The abstract/record was inspected for its torsion-restricted scope; no blanket theorem was inferred from it.
5. Catanese–Franciosi–Hulek–Reid, Embeddings of curves and surfaces, https://arxiv.org/abs/alg-geom/9607021 . Theorem 1.1 was checked directly in the PDF. It supplies the declared curve-embedding dependency, not an unconditional slc surface theorem.
6. Wenfei Liu's public publication list, https://sites.google.com/site/liubenew/ , was inspected as a status lead. It reports its own last update as 29 March 2026 and lists the 2014 paper. A publication list cannot prove nonexistence of later work.

Targeted searches included the title, stable log surfaces with very ampleness, five/pentacanonical systems, and the indexed 5I formulation. No later credited solution of the unrestricted question was located. This is a bounded-search finding as of the check date, not a proof that no solution exists. The packet therefore remains PARTIAL, with the universal logarithmic problem unresolved.

## Reproducibility and limitations

The hashes and byte counts of retrieved PDFs appear in SOURCE_METADATA.json; the files themselves are excluded. Inspection descriptions identify which parts were actually read. The downloaded PDFs can be retrieved again from their public URLs and checked independently, subject to future server/version changes.

The replay script uses only Python's standard library. It checks the finite arithmetic ranges, weighted monomial counts and local tangent model described in CHECK_RESULTS.json. These tests do not verify the external geometric theorems, all possible stable surfaces, the existence of the two exceptional subcurves, or the absence of a future published solution. PROOF.md identifies every geometric dependency and remaining gap.
