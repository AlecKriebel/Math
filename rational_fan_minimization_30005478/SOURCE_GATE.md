# Source gate: row 1843, 30005478 / OWR-12697711-014

Checked 2026-10-21 UTC. **Source identity and exact problem recovered; no general resolution verified.**

## Exact target and provenance

The authoritative source is Jan Draisma, “Amoeba dimensions,” in *New Directions in Real Algebraic Geometry*, Oberwolfach Report 15/2023, pp. 854–857. Open question 1 is on printed p. 856 (PDF page 44), immediately after Corollary 4. DOI: https://doi.org/10.4171/OWR/2023/15 ; publisher PDF: https://ems.press/content/serial-article-files/47009 . The PDF page was rendered and visually checked, including the closure bar in Theorem 3.

Precisely: given a d-dimensional rational polyhedral fan with support F ⊆ R^n, find an algorithm computing

    a_Q(F) = min { 2 dim_R(U + F) − dim_R U : U ⊆ R^n is spanned by rational vectors }.

The question asks for a terminating algorithm, not a polynomial-time bound, approximation, or visualization. It asks for the integer value; it does not explicitly demand a minimizing basis. The 2023 question does NOT state balancing, realizability, or connectedness assumptions. It also does not explicitly impose purity beyond its wording “d-dimensional.” Do not silently narrow to tropicalizations of varieties, matroid fans, or pure balanced fans.

The exact dataset ID and source key have one matching problem record. Its cleaned statement matches this target. Its original_statement runs into the following linear-space section, which is context, not part of Open question 1. Existing local corpus bytes were freshly hashed, not freshly downloaded. No matching key was found in research_results.json. See DATASET_METADATA.json; dataset contents are not included.

## Objects and field conventions

The geometric motivation uses an irreducible closed algebraic subvariety X ⊆ (C*)^n. Its ordinary Archimedean amoeba is A(X) = Log(X), with Log(z)_i = log|z_i|. Its dimension is the real dimension of the semialgebraic set |X| = {(|z_1|,...,|z_n|): z ∈ X}; coordinatewise logarithm is a diffeomorphism and preserves this dimension. This is not the dimension of X(C) as a complex variety, a volume, a complement component count, or a dimension of the real locus X(R).

Trop(X) here is constant-coefficient tropicalization, equivalently the asymptotic limit of t^(-1) A(X) as t → infinity, not a choice of arbitrary nontrivial valuation on C. Its real polyhedral dimension equals dim_C X. The tropical support generally does not itself equal the amoeba. The requested expression may be larger than dim Trop(X).

## Source structural result

OWR Theorem 3, credited to Draisma–Rau–Yuen, identifies dim_R A(X) with min_T(2 dim_C closure(T·X) − dim_C T), over algebraic subtori T ⊆ (C*)^n. The bar is Zariski closure. Corollary 4 converts this to a_Q(Trop(X)). Thus the tropical fan determines amoeba dimension, but an infinite minimization formula is not automatically an effective algorithm.

Underlying paper: Draisma–Rau–Yuen, *The dimension of an amoeba*, Bulletin of the London Mathematical Society 52 (2020), 16–23, https://doi.org/10.1112/blms.12301 ; https://arxiv.org/abs/1812.08149 . Its Corollary 7 is the tropical formula. Question 14 asks an older, narrower version on balanced pure-dimensional rational polyhedral complexes connected in codimension one. The closing discussion specifically identifies rational incidence constraints as the obstacle: dropping rationality permits real quantifier elimination, which does not establish rational feasibility. Equations for X over a number field instead allow computing |X| by real algebraic methods; that changes the input and is not the fan-only question.

## Encoding and mathematical acceptance conditions

The OWR source specifies no file format or formal bit model for a general fan. A faithful effective model is a finite list of cones given by rational generators, with rational bases for lineality, or equivalent rational homogeneous inequalities; rational numerators and denominators have finite binary encodings. This is an explicit implementation convention, not additional source wording. Cone weights are not used by the expression.

For each cone C_i, compute its rational linear span L_i. For any candidate rational U,

    dim(U + F) = max_i dim(U + L_i).

Consequently fixed-candidate values reduce to exact matrix ranks. The optimization is over all rational subspaces in all dimensions 0,...,n, not only existing rays or faces. For a nonempty fan of dimension d, d ≤ a_Q(F) ≤ min(2d,n). These elementary bounds and rank evaluation do not give a stopping rule for exhaustive enumeration. A solution must justify finite completion and rational optimality, or give a valid negative computability result. Real QE, a numerical optimizer, bounded-height enumeration, and an unproved finite candidate-subspace restriction fail this gate.

## Known special case and later-source check

Draisma–Eggleston–Pendavingh–Rau–Yuen, *The amoeba dimension of a linear space*, https://arxiv.org/abs/2303.13143 (v3, 21 November 2023), Proceedings AMS 152 (2024), 2385–2401, https://doi.org/10.1090/proc/16744 : for V ⊆ C^n with V ∩ (C*)^n nonempty, the answer is the minimum over partitions of [n] of the sum of 2 rank(P_i) − 1. The precise algorithmic corollary uses a matrix over Q(i), with no zero column, and polynomial time in its bit length. A polynomial number of matroid-rank oracle evaluations computes the partition expression for arbitrary loopless matroids. The identification with the fan minimization for arbitrary, possibly nonrealizable matroids is a separate conjecture in this paper. This result is already represented in OWR Theorem 5 and is not a solution for arbitrary fans.

A later primary claim was found: Alper Ferudun, *The Amoeba Dimension of an Arbitrary Loopless Matroid*, 30 September 2026, https://eulersolve.org/papers/owr-12697711-015/ , DOI https://doi.org/10.5281/zenodo.23058144 . The landing page and PDF explicitly label it unrefereed. Its scope is adjacent Open question 2 / source key -015, claiming the partition formula for all loopless matroids, using a Bernstein theorem and a cone inequality. The PDF explicitly notes that the related inequality can be strict on other fans. This source has been inspected for scope, not independently proof-audited, and is neither accepted here as a theorem nor a solution to -014.

Searches on 2026-10-21 included the exact title and source key; amoeba dimension / rational fan / algorithm; amoeba fan computability with 2025–2026 terms; the original paper; and the later linear-space paper. No primary source establishing a general terminating algorithm for the specified arbitrary rational fan input was located. This is a bounded literature-search result, not proof that no resolution exists.

## Gate decision

Proceed only on the general rational-subspace algorithm question above. Do not report the existing linear-space algorithm or the adjacent 2026 matroid preprint as full completion. The principal falsification target is a hidden replacement of rational subspaces by real ones. No source PDFs, extracted source text, page renderings, or dataset contents are included; source hashes and retrieval/inspection facts are in SOURCE_METADATA.json.
