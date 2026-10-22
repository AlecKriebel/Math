# Primary-source and scope gate

Checked 2026-10-03 UTC for problem 5200008 / AMR-051-0008.

## Exact target

The catalogue URL https://www.unsolvedmath.com/problems/5200008 returned HTTP 403 on direct retrieval. The mathematical statement was independently recovered from the full primary paper:

- Bialy, Fierobe, Glutsyuk, Levi, Plakhov, Tabachnikov, *Open problems on billiards and geometric optics*, arXiv:2110.10750v2 (28 October 2021), Alexey Glutsyuk's Problem 2, PDF pp. 6-7: https://arxiv.org/abs/2110.10750v2

It asks whether every smooth Hamiltonian self-map of the phase cylinder is a smooth limit of positive compositions of reflections in a fixed strictly convex hypersurface and arbitrarily prescribed C^k-small deformations. Its accompanying remarks explicitly distinguish words allowing inverses. They also explain the connection to reflection composition questions surrounding Ivrii's conjecture. Those remarks do not identify a positive-word solution.

The target is not caustic symmetry, an elliptic-billiard invariant, or shortest periodic billiards in constant-width bodies. The checked earlier constant-width work has problem ID 30002659 and is distinct: https://github.com/AlecKriebel/Math/pull/471 . Repository searches for the exact ID, code and Glutsyuk returned no existing matching pull request. Exact-ID code and branch searches also returned no match. Such search results are limited evidence, not a proof of exhaustive absence.

## Primary density paper and update check

- Alexey Glutsyuk, *Density of a thin film billiard reflection pseudogroup in a Hamiltonian symplectomorphism pseudogroup*, Israel Journal of Mathematics 258 (2023), 137-184; https://doi.org/10.1007/s11856-023-2470-3 . Primary preprint: https://arxiv.org/abs/2005.02657v5 , revised 16 September 2025.

The arXiv metadata confirms the journal citation, DOI and version. The journal landing-page request was unsuccessful; the complete 47-page primary arXiv PDF was accessible. Section 1.6, p. 13, still poses the positive-semigroup density question. Theorem 1.1 supplies thin-film Lie-algebra density; Theorem 1.13 gives the Perline Hamiltonian formula; Theorem 1.5 and Corollary 1.7 are inverse-allowed pseudogroup conclusions. The definition at the beginning of Section 1.1 reflects at the last intersection, not at a fixed labeled mirror point.

Read in full for the invoked density-to-flow passage: Section 4.1, pp. 39-41, including Propositions 4.2, 4.4, 4.5 and the proofs of Theorem 1.5 and Corollary 1.7. The relevant source statements and their density deductions in Sections 2.4-2.5 and 3.3 were also inspected. The established Lie-algebra theorem is used with credit, not claimed as a new independently formalized proof. PROOF.md supplies the full argument for its additional one-inverse criterion, including the correct square-root scaling for a bracket-flow product and all compact-domain restrictions.

- Albach et al., *Open problems in billiards and quantitative symplectic geometry*, https://arxiv.org/abs/2602.12896v1 (13 February 2026). The optical-transformation question on pp. 19-20 asks a related characterization question and cites the density paper. It supplies no theorem removing inverses in the exact target considered here.

Targeted searches included the exact density title, Glutsyuk with reflections/inverses, positive or pseudo-semigroup billiard terminology, and later 2025-2026 work. No later primary resolution of this exact question was found. This bounded search does not establish worldwide absence of a result. The defensible conclusion is that this attempt has no full resolution, while the September 2025 primary version still explicitly lists the problem.

## Scope safeguards

- The source's local compact-open convergence convention allows approximating domains to exhaust the target domain. No unproved global-domain upgrade is made.
- A circle inverse is Hamiltonian by the explicit formula in PROOF.md. No assertion that every billiard map in every dimension is Hamiltonian is needed.
- Concentric-circle and bounded-length obstructions do not cover arbitrary small nonsymmetric deformations.
- The matrix example is an abstract linear symplectic control; no optical realization is asserted.
- The full source PDFs and extracted full texts are not included in the public packet. Public citations and hashes identify the inspected versions. Only the original mathematical note, scoped attempt summary and reproducible controls are distributed.
