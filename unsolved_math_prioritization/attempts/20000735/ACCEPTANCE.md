# Acceptance of the Chebyshev Nahm family result

## Decision and boundary

Accepted as a scoped, known family-level result for problem 20000735. The complete proof is `STANDALONE_PROOF.md`; the claim-by-claim review is `AUDIT_REPORT.md`. The broad Bailey-pair, orthogonal-polynomial, and Bloch-group program in AIM Problem 2.4 remains unresolved by this argument. No novelty is claimed.

## Accepted mathematical conclusions

For every integer r ≥ 1, put M = 2r+3, θ = π/M, u_j = sin((j+1)θ)/sin θ, and A_ij = 2 min(i,j). Then A is positive definite and x_i = 1−u_i^(−2) is the unique solution in (0,1)^r of 1−x_i = ∏_j x_j^(A_ij). The recurrence, terminal equality u_(r+1)=u_r, telescoping identities, and strict-convexity argument are proved for arbitrary r. Existence comes from the displayed solution, separately from uniqueness.

The field K = Q(cos(π/M)) is totally real, and ξ_r = Σ_i[x_i] is a torsion element of the ordinary Bloch group B(K). The boundary target is the antisymmetric tensor quotient. Off-diagonal terms cancel, and 2(x_i∧x_i)=0 together with A_ii=2i kills the diagonal terms. Torsion follows from the established number-field rank theorem, using r_2(K)=0. No finite-generation assumption is needed for the implication from vanishing in B(K)⊗Q to elementwise torsion.

For a=1,…,r+1, the Andrews–Gordon unshifted series F_(r,a) have the same A and distinct linear vectors B_i^(a)=max(0,i−a+1). For a<b, their coefficients agree below degree a, and [q^a]F_(r,b)−[q^a]F_(r,a)=1. Thus retaining only the distinguished positive solution and its ordinary A-dependent Bloch class is noninjective on this family. This conclusion includes the terminal endpoint and compares unshifted series only.

## Conventions and established dependencies

The accepted proof uses the Andrews–Gordon product identity in Kirillov's Theorem C, equation (2.1.a), and the Borel–Suslin rank theorem for number-field Bloch groups. The primary rank-zero route uses Borel's Proposition 12.2 and Suslin's Theorem 5.2; Zagier also states the rank/regulator result. Complete citations and page pins are in the proof and `SOURCE_PINS.json`.

Lee's coordinates are y_i=1−x_i. His rationalized boundary target and additional complementary/inverse-symbol relations are not identified with the integral ordinary group. In the ordinary convention, [z]+[1−z]=c_K and 6c_K=0, so complementary sums differ from negatives by r c_K. Extended Bloch classes include branch data that the ordinary class does not specify. The accepted information-loss claim concerns only the stated ordinary assignment.

## Verification and exclusions

Independent exact diagnostics cover algebraic identities at ranks 1–12, all 44 terminal companions at ranks 1–8 through q-degree 48, and 120 pairwise first-difference comparisons. Normal Python, -O, and -OO have identical mathematical outputs; three negative controls reject known wrong substitutions or identifications. These are bounded checks and do not replace the arbitrary-r proofs.

No exact torsion order, general modularity equivalence, arbitrary Bailey-pair dictionary, or loss of information for every possible enhanced construction is accepted. The AIM source already notes that one A may admit multiple B,C; the explicit instance is credited accordingly. No separate source-correction claim is made.

Public source metadata and aggregate check summaries accompany the authored proof and audit. Copied third-party documents, source extracts, page images, raw computational coefficients, scripts, and private coordination material are excluded.
