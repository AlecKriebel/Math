# Statement, source, and scope audit

Checked 2026-10-07. This is a source-grounded authored audit, not a copied source extract. Source PDFs, page images, full-text extracts, corpus records, and private coordination material are not members of this packet.

## Identity and exact target

The full supplied problem corpus identifies numeric ID 30005990 with code OWR-14298587-002 and the title *Boundary Frequency Gap for Optimal Partitions*. The queue row is rank 958. The complete research-results corpus was parsed and searched; no entry matching this ID, code, or exact title was found. Dataset byte counts, complete SHA-256 hashes, record counts, and match results appear in source_metadata.json. These are identity checks, not endorsements of the corpus's mathematical assessment.

The primary workshop contribution is Bozhidar Velichkov's joint-work report with Roberto Ognibene, printed pp.2120-2123 in Oberwolfach Report 37/2024. The workshop occurred in August 2024; the journal issue was published in February 2025. The original model minimizes the sum of first Dirichlet eigenvalues of mutually disjoint open cells inside a bounded container, equivalently normalized nonnegative segregated H^1_0 functions. The report's boundary-gap discussion is on printed p.2122.

The rendered primary PDF confirms a notation inconsistency: the displayed set uses the threshold 2+delta_d, but the following conjectural endpoint is labeled delta_d=5/2. We separate threshold beta_d from additive gap g_d. The geometry corresponds to beta_d=5/2, or g_d=1/2. The supplied cleaned statement preserves the ambiguous symbol, so that cleaned statement is not a sufficient substitute for inspecting the original formula.

## Exact imported analytic hypotheses

1. Ognibene-Velichkov, *Boundary regularity of the free interface in spectral optimal partition problems*, arXiv:2404.05698v1, 8 April 2024. Inspected Definition 4.3 and Proposition 6.13, together with Assumption 2.1 and Lemma 4.4. Their half-space class consists of homogeneous local Dirichlet minimizers with zero flat trace. The spectral blow-up theorem requires the stated boundary modulus conditions; C^(1,alpha), alpha>0, is a covered sufficient case. The packet does not extend it to arbitrary C^1 containers.

2. Ognibene-Velichkov, *Structure of the free interfaces near triple junction singularities in harmonic maps and optimal partition problems*, arXiv:2412.00781v5, 7 September 2026; journal reference Arch. Rational Mech. Anal. 250, 77 (2026). Inspected Section 2, Theorems 2.1/2.4, Proposition 3.5, Corollary 3.6 and Section 1.2. The needed S class is exactly the pair of distributional segregated inequalities. The 3/2 gap, Y classification and full-sphere min-max input are credited. The p=1 spherical sum conjecture is not treated as proved.

3. Wang-Zhang, *Some new results in competing systems with many species* (2010). Theorem 1.6 and its discussion identify solutions of the segregated inequalities with energy-minimizing tree-valued harmonic maps; Section 6 proves the assertion. Its scope covers arbitrary dimension and number of species. The local-to-fixed-boundary approximation needed for the tY half-space construction is nevertheless proved in PROOF.md.

4. Ognibene-Velichkov, *A survey on the optimal partition problem*, arXiv:2510.08241; published in La Matematica 5 (2026), DOI 10.1007/s44007-025-00176-8. Inspected Sections 3.2 and 3.3, especially admissible boundary frequencies in Section 3.3.5. This inspected source still gives an unspecified positive gap above 2. Its definition of admissible frequency is through homogeneous half-space minimizers; that does not prove realization by an actual bounded-domain spectral optimizer.

5. NIST DLMF Sections 10.2 and 10.21 were inspected for the Bessel equation, power series, and first positive zero used in Approach 5. They supply special-function facts, not a spectral partition optimality theorem.

## Literature and novelty boundary

Bounded current searches used the exact problem code/title, boundary-frequency/optimal-partition terms, the two authors' boundary-gap papers, the 2026 survey, and dimensional-lifting terms. No primary source resolving the exact bounded-domain spectral-attainment assertion was located. This is not an exhaustive literature or novelty certification. The 2026 revision of the interior paper was inspected directly, rather than assuming an older abstract's scope.

The authored contributions in this packet are deductions and constructions whose proofs are supplied. The interior regularity theory, interior 3/2 gap, Y classification, S=M theorem, spectral blow-up compactness, Bessel theory, and standard variational facts remain credited external inputs. Reproducible finite checks cannot certify these imported analytic theorems.

## Why the overall status is unsolved

The sharp B_gamma classification and cone-class attainment would settle the interpretation in which the target is solely the class of admissible tangent configurations. The original wording also describes attainment in the spectral problem. We retain that as an additional obligation and use the more conservative status **unsolved, 5/5**. Neither a cone minimizer, a spherical min-max optimizer, an asymptotic thin-domain limit, nor a shape-stationary eigenfunction partition is promoted to a globally minimizing bounded-domain spectral partition.

## Source links

- OWR primary: https://doi.org/10.4171/OWR/2024/37
- OWR official PDF: https://publications.mfo.de/bitstream/handle/mfo/4251/OWR_2024_37.pdf?isAllowed=y&sequence=1
- Boundary paper: https://arxiv.org/abs/2404.05698v1
- Interior paper: https://arxiv.org/abs/2412.00781v5
- Interior journal: https://doi.org/10.1007/s00205-026-02221-4
- Wang-Zhang article: https://doi.org/10.1016/j.anihpc.2009.11.004
- Wang-Zhang official PDF: https://ems.press/content/serial-article-files/16218
- Survey: https://arxiv.org/abs/2510.08241
- Survey journal: https://doi.org/10.1007/s44007-025-00176-8
- DLMF: https://dlmf.nist.gov/10.2 ; https://dlmf.nist.gov/10.21
