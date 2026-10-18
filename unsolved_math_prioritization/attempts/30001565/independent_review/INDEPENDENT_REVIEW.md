# Independent full source and algorithm-correspondence review

Verdict: **PASS_FULL_CREDITED_QUALITATIVE_SOURCE_TARGET**, recommended **already_solved0/5**. No mandatory correction.

This verdict binds SOURCE_AUDIT.md SHA-256
`5419fe3b2fe9e5d12e3d0bd9e782e7ee508f41e3015a723f4fcab58263298663`
and FROZEN_MANIFEST.json SHA-256
`d683f0cbb0852c9b27570fe5902273717adff8c570825e61174b22a049c5aec6`.

All ten author artifacts and five pinned reading inputs match. The189-assertion author receipt replays byte-identically. A separately authored checker passes6,594 exact controls. The reviewer did not contribute to the construction; the pre-freeze message about reduced/ambient rank and arbitrary eigenvector selection was an audit question, not an alternative author algorithm. No source software was executed.

## 1. Exact source scope

I read the original contribution on printed pp.2251–2253 and visually inspected the setup and question. The relevant step is Schurian: the group/permutation representation, a splitting field and the character-based central component construction have already been introduced. The desired output is an irreducible complex star representation of each occurring central component, of dimension equal to its multiplicity m_chi.

The source's heuristic assumes a special self-adjoint element with the required distinct eigenvalues in the group splitting field. It asks for an alternative without that assumption. It does not state a uniform polynomial-bit bound, require a practical speedup, prohibit all polynomial/integer factorization, or require an orthonormal realization over an arbitrarily prescribed field. Accordingly the known general split-algebra algorithm, followed by the verified star normalization, answers the literal qualitative assumption-removal question. Those stronger algorithmic and field constraints remain outside this verdict.

The source's regular component acts on a space of dimension m_chi squared and has repeated physical eigenvalue multiplicities. One must not read its short heuristic as a theorem that arbitrary selected eigenvectors always span an invariant submodule. In M_2, the eigenvectors E_11,E_22 of left multiplication by diag(1,2) span a space not preserved by left multiplication by E_12. The candidate uses a minimal left ideal instead and explicitly bypasses this issue.

## 2. Published algorithm and termination contract

The complete pinned Ivanyos–Rónyai–Schicho author manuscript was read: Theorem1, the following unbounded-parameter remark, the rational-case algorithm and lemmas, the general number-field rank-one existence argument, lattice-coefficient bound and finite search/corner reductions. The final2012 Journal of Algebra metadata and abstract independently confirm the published theorem. A complete final-layout PDF was not available in this audit; that access distinction is accurately recorded.

The input promise is a structure-constant K-algebra isomorphic to M_m(K), with K an exactly represented algebraic number field. It is not an algorithm that first proves an arbitrary central simple algebra is split. For the promised input, the source constructs a reduced-rank-one element and an explicit isomorphism. The finite enumeration is justified by a bounded rank-one element in a maximal order, the lower bound for nonsingular short vectors, and the reduced-basis coefficient bound. Corner reductions strictly lower the matrix size. These are actual termination arguments, not empirical evidence from examples.

The polynomial-time theorem is an ff statement under bounded number-field degree/discriminant and bounded matrix degree, or fixed field and bounded degree in the final abstract. Its oracles factor integers and univariate polynomials over finite fields. The source explicitly retains a terminating construction when those parameters vary, without the uniform polynomial guarantee. Replacing each factoring oracle by a terminating exact factorization procedure retains qualitative termination. It does not turn the result into a factorization-free or uniformly polynomial algorithm. The candidate states these distinctions correctly, including the real/complex embedding and maximal-order subroutines.

The rendered author-PDF date differs from the arXiv version record; neither date is silently used as a new theorem edition. The exact reading bytes and version are pinned.

## 3. Matching the Schurian component to the promise

Over a genuine splitting field K in characteristic zero, the permutation module decomposes into absolutely irreducible group modules with multiplicity spaces. Its commutant is the direct sum of M_(m_chi)(K), not matrices of size equal to the group-character degrees. The orbital matrices span that commutant. The standard central idempotent obtained from the supplied character data projects to each isotypic component, and e_chi A_K is therefore the promised split full-matrix algebra.

Gaussian elimination on the explicit matrices e_chi A_i supplies a basis and structure constants. No special self-adjoint X, roots of its polynomial, or generic eigenvector assumption is needed for this input conversion.

A character-value field alone would be insufficient because of possible Schur-index obstructions. The candidate does not confuse it with a true splitting field. It also does not charge no cost for constructing a field or character table that the source step assumes available. If conjugation stability is needed, the finite compositum with the conjugate field is effective and remains a splitting extension. The stated application to a non-Schurian algebra is explicitly conditional on a supplied split component and field; it is not a claim that every rational coherent algebra is split.

## 4. Minimal ideal and full irreducible action

For reduced-rank-one x in B isomorphic to M_m(K), the left ideal Bx has dimension m. Gaussian elimination on b_j x computes a basis, and exact left multiplication gives the representation. Simplicity makes its kernel zero; the dimensions of B and End_K(Bx) are both m squared, so the image is the full matrix algebra. After extending to C it remains irreducible.

Reduced rank must not be replaced by ambient matrix rank. In an embedding I_r tensor M_m, a reduced-rank-one element has physical rank r but generates an m-dimensional minimal left ideal. Both checker sets verify this distinction. The independent regular-S3 example has central-component dimension4, minimal-ideal dimension2 and physical rank2, directly in an actual Schurian orbital algebra.

The source basis action extends to the full original algebra by the central projection. Its identity acts as the identity on the selected ideal. Thus the output is a representation of the requested source algebra, not just an unexplained action of an abstract corner.

## 5. Trace-Gram star normalization

For the ideal basis u_i in the original matrix embedding, H_ij=Tr(u_i^*u_j) is positive-definite Hermitian at the chosen complex embedding. Linear independence ensures positivity; the argument uses the actual positive matrix involution, not an arbitrary abstract involution. The ideal need not be star closed: it is a left ideal, hence is invariant under multiplication by a and a^*.

The inherited adjoint identity is R(a)^*H=H R(a^*). An exact factor C with C^*C=H gives phi(a)=C R(a) C^(-1), for which phi(a^*)=phi(a)^*. This is valid for all basis elements and therefore for the full complex algebra after scalar extension. Irreducibility and dimension are unchanged.

Positive Hermitian elimination can require square roots of positive real algebraic pivots. Adjoining them gives a finite exact extension inside C, stable under conjugation when the base is made stable first. The unnormalized action remains over K; the standard-star realization need not. This is allowed by the original complex output goal, which already notes quadratic normalization irrationals.

The rational S3 boundary control is correct. Its invariant symmetric forms form a one-dimensional line with determinant square class3. A rational change of basis to standard orthogonality would force3 to be a rational square, even allowing a rational scalar on the invariant form. The example therefore supports the stated field caveat rather than defeating the complex output algorithm.

## 6. Later software and verification boundaries

The full JOSS2020 RepnDecomp paper corroborates exact decomposition, unitarization and commutant tools in cyclotomic arithmetic. Current primary documentation distinguishes its implemented unitarization/LDL routines and centralizer routines from an explicitly unimplemented Dixon decomposition placeholder. The candidate does not rely on that placeholder, does not execute downloaded software and does not substitute a software claim for the split-algebra theorem.

Independent controls reconstruct the regular-S3 left and right actions, central idempotent, minimal ideal, multiplication table and trace Gram matrix; they verify standard-star normalization and full matrix image. Further Gaussian-rational changes of basis and repeated matrix embeddings check general multiplicities, and the eigenvector negative control detects the invalid shortcut described above. These finite tests do not prove ISR termination or its complexity; those were checked from the full source argument.

The complete qualitative source correspondence passes as a credited zero-author-turn correction. Preserve all supplied-field, complexity, factorization and finite-extension qualifications. The parent retains the publication gate. No practical performance, uniform polynomial, arbitrary-prescribed-field orthonormality or historical novelty claim is certified.
