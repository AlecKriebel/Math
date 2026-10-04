# Sources and scope checks

Problem 30006276 / OWR-14299284-004. Checked 2026-10-04.

## Primary sources

**S1. Aitor Iribar Lopez, “Counting maps to an elliptic curve in several ways.”**
Contribution to *Recent Trends in Algebraic Geometry*, Oberwolfach Report
28/2025, printed pp. 1492-1495. The exact question is Question 1, p. 1492;
the nearby Theorem 1 on p. 1494 concerns special pairs and does not settle it.

- Report DOI: https://doi.org/10.4171/OWR/2025/28
- Official record: https://publications.mfo.de/handle/mfo/4341
- Official report: https://publications.mfo.de/bitstream/handle/mfo/4341/OWR_2025_28.pdf?isAllowed=y&sequence=1
- The original question page was visually inspected, not inferred solely from
  the catalogue's one-sentence summary. The report uses the moduli stack A_g.

**S2. Samir Canning, Sam Molcho, Dragos Oprea, Rahul Pandharipande,
“Tautological projection for cycles on the moduli space of abelian varieties.”**

- https://arxiv.org/abs/2401.15768v4 (20 May 2025)
- Locations: Theorem 1; Theorem 3; Definition 4 and Section 1.4; Theorems 5-6.
- Supplies the tautological-ring presentation, boundary vanishing and the
  compactification-based projection. It does not prove arbitrary
  multiplicativity. The p-rank-zero class discussion is in Section 1.3.

**S3. Aitor Iribar Lopez, “Noether-Lefschetz cycles on the moduli space of
abelian varieties.”**

- Full inspected version: https://arxiv.org/abs/2411.09910v2 (21 November 2025)
- Published article: https://doi.org/10.1017/fmp.2025.10018
  (*Forum of Mathematics, Pi* 14 (2026), e2; online 13 January 2026)
- Locations in the inspected arXiv version: Section 1.3; Theorem 6;
  Proposition 13 and its proof in Section 3.2; Section 5 and Proposition 20.
- Theorem 6 concerns two cycles supported on the nonsimple locus. It does not
  identify the whole Chow ring with the subring on which it proves
  multiplicativity. The distinction between nonsimple and real-multiplication
  Noether-Lefschetz components is explicit in Section 1.2.
- Publisher metadata and statement excerpts were checked. Direct published
  PDF retrieval returned access/rate errors; the mathematical inspection
  used the complete author-posted v2, not a claimed successful PDF retrieval.

**S4. Samir Canning, Lycka Drakengren, Jeremy Feusi, Daniel Holmes,
Aitor Iribar Lopez, Denis Nesterov, Dragos Oprea, Rahul Pandharipande,
Johannes Schmitt, Zheming Sun, “Torelli loci, product cycles, and the
homomorphism conjecture for A_g.”**

- https://arxiv.org/abs/2601.04353v3 (9 June 2026)
- https://arxiv.org/html/2601.04353v3
- Checked locations: Sections 1.1-1.4, 1.7-1.8; Theorem 7; Conjecture 8;
  Proposition 39; Section 5.6.
- Conjecture 8 is the full target. The published calculations and the
  fixed-abelian-variety proposition are not a full answer to it. The
  explicit P(J_g) values used by the verifier are from Section 1.3.
- Version warning: v1 has a separately labeled algebraic-closure-of-Q form
  and numbers the fixed-fibre result Proposition 36. The inspected v3
  replaces the former discussion with specialization and homology remarks
  and numbers the fixed-fibre result Proposition 39. The final note uses v3.
- Some broader mixed-pair results are attributed in this paper to work in
  preparation. The argument of this attempt does not depend on treating
  that unpublished reference as a complete inspected proof.

**S5. Georg Oberdieck, “Gromov-Witten theory of abelian varieties in families
and modular forms.”**

- https://arxiv.org/abs/2608.16737v1 (17 August 2026)
- Checked introduction, Proposition 1.3, Theorem 1.8, and occurrences of the
  tautological projection. Its genus-two projected Gromov-Witten formulas
  are not a theorem that arbitrary Chow products commute with projection.

**S6. Sean Keel, Lorenzo Sadun, “Oort's conjecture for A_g tensor C.”**

- https://arxiv.org/abs/math/0204229v2 (6 March 2003)
- Journal article: https://doi.org/10.1090/S0894-0347-03-00431-4
- Checked Main Theorem 1.1 and Corollary 1.2. The latter excludes the proposed
  compact codimension-g complex subvariety for g>=3. It excludes that proof
  mechanism, not the homomorphism conjecture itself.

**S7. Pierre Deligne, “Theorie de Hodge III.”**

- https://www.numdam.org/articles/10.1007/BF02685881/
- *Publications Mathematiques de l'IHES* 44 (1974), pp. 5-77.
- Proposition 8.2.7, printed p. 40, with the weight argument in Proposition
  8.2.5 on p. 39. This is the precise kernel-comparison input in the audited
  clarification of PROOF.md, Section 3.1. Its application uses a smooth X,
  a proper singular boundary D, and its smooth proper normalization mapping
  surjectively to D. It avoids inferring ordinary cohomology vanishing on a
  singular boundary merely by treating that boundary as smooth.

## Catalogue and bounded literature check

The requested catalogue URL is https://www.unsolvedmath.com/problems/30006276.
It was attempted first. The web tool could not access it and the direct
request returned HTTP 403. Identification therefore used the supplied fixed
catalogue record and was independently checked against S1. No assertion
that the live catalogue page was successfully read is made.

Exact title and “tautological projection”, “homomorphism conjecture”,
“counterexample”, and “homologically trivial” searches led to S2-S6 and
the author's research list. The list linked S4 and did not advertise a full
resolution: https://people-new.math.ethz.ch/~airibar/research.
This is a bounded source check, not a proof that no further paper exists.
The attempt remains unsolved regardless of the limits of a novelty search.

## Computational interpretation

The shipped standard-library verifier checks the formal fixed-surface example,
the lambda_(g-1) annihilator in genera 2-8, the entire partition cutoff over
the finite range g=2-40, the self-product cutoff through g=100, and the
specified right-hand-side polynomial reductions. The all-g cutoff proofs
are in PROOF.md; their validity is not inferred from the finite range.

No downloaded source full text, source PDF, image of a source page, or imported
catalogue corpus is part of this research packet. Citations identify the
underlying works; the packet contains original exposition and exact controls.

The original source account is preserved in author/SOURCES.md. The complete
independent audit is retained in audit/, including its corrections and exact
input binding. The updated source reference above implements correction C2;
the Torelli-compatible compactification qualification implements C3.
