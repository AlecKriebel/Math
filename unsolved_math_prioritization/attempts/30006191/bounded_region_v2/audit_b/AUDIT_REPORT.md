# Independent full proof audit of the bounded region fermion counterexample

Problem 30006191 / OWR-14299085-005. Independent review B. 7 October 2026.

## Verdict

**ACCEPT the frozen revision 2 proof for its stated existential claim. No mathematical correction is required.**

The proof gives a fixed bounded interaction region in three-dimensional continuum fermionic Fock space, a fixed real even smooth compactly supported interaction potential, a fixed normalized test function, and explicit normalized Slater states at times tending to zero. The annihilation difference applied to those varying states has norm tending to 2, as does its operator norm. Both density-density and normal-ordered conventions are covered. The argument does not use a prior full-space discontinuity theorem.

This verdict does not assert novelty, priority, discontinuity in every dimension or for every potential, a fixed-density state construction, failure on a fixed vector or fixed normal state, or non-invariance of the CAR algebra. It is a mathematical audit, not a publication or priority determination.

## Frozen input and independence

The reviewed proof is `BOUNDED_REGION_PROOF.md`, 12,771 bytes, SHA-256:

`2b7c22cfc54049a9e51fe5eb4eb283ba911e6f27e8b6e4dc9557927bc04d7350`.

The associated `AUTHOR_MANIFEST.json` is 1,172 bytes, SHA-256:

`d6a0862cbf2f6500cc5fd7ee2239e0e8a2c5864c9d09a6cd9a13b1b4f99176ef`.

All six files listed in that manifest match their declared byte counts and hashes. The seven-file input packet contains exactly the listed files and the manifest. The complete theorem and every argument in Sections 1–7 were read and checked. The input files were not edited. This review did not consult the other new bounded-region audit. The independent verification program was written separately and imports no author verification code.

## Source and model alignment

The official [Oberwolfach Report 7/2025](https://ems.press/content/serial-article-files/51350), DOI [10.4171/owr/2025/7](https://doi.org/10.4171/owr/2025/7), was inspected in extracted text and rendered printed pages 364, 365 and 371. The kinetic energy acts on the whole space; the interaction is restricted to a bounded region. Page 365 specifies norm continuity for each fixed observable as the relevant notion of strong continuity. Page 371 asks for an interaction and states exhibiting its failure. The fixed-density bosonic problem in subsection 2.1 is separate from the fermionic subsection 2.2 and supplies no extra hypothesis here. These distinctions agree with the audited theorem.

Oliver Siebert's [Discontinuity of Continuum Fermion Dynamics](https://arxiv.org/abs/2609.34402) is relevant prior literature. The official record and [version 1 HTML](https://arxiv.org/html/2609.34402v1) were inspected; the record lists submission on 28 September 2026, version 1, and no journal reference. The retained PDF title-page date is 29 September 2026. It is credited as background, and no theorem from it is needed for the proof under review. The official record for [On the thermodynamic limit of interacting fermions in the continuum](https://arxiv.org/abs/2409.10495) confirms version 2 of 24 February 2025 and the stated 2025 Letters in Mathematical Physics publication.

The three retained PDF byte counts and SHA-256 values match the author's source manifest. Those checks identify retained bytes; they are not a claim of a second fresh PDF download. Historical corpus-wide counts and corpus hashes were not recomputed in this mathematical audit and are not mathematical premises.

## Full analytical review

### 1. The potential and both interaction conventions

The two bump arguments in the denominator are \(81-|x|^2\) and \(|x|^2-64\). They cannot both be nonpositive. Consequently the denominator is everywhere strictly positive, including at the two transition radii. Smoothness follows from the flat smooth bump construction and the polynomial argument \(|x|^2\). The potential is radial, real, nonnegative, bounded by 1, equal to 1 on the radius-8 closed ball, and zero outside the radius-9 open ball.

For \(\Lambda=B(0,4)\), every difference of two points of \(\Lambda\) lies in \(B(0,8)\). Thus each ordered pair of particles inside \(\Lambda\) contributes exactly 1. The density-density expression, rigorously interpreted sectorwise as the ordered-pair multiplication operator, is \(L_n^2\). The diagonal contribution is \(L_n\), because \(V(0)=1\); removing it gives \(L_n(L_n-1)\). The proof does not accidentally omit a contact term or replace a local number operator by total particle number in the claimed Hamiltonian.

### 2. Self-adjointness and the direct sum

On the antisymmetric \(n\)-particle space, \(T_n=\sum_j(-\Delta_j)\) is self-adjoint with the usual whole-space kinetic domain. The local-number polynomial is a real bounded multiplication operator on that sector, invariant under particle permutations. Bounded perturbation therefore gives self-adjointness of \(H_n^{(\sigma)}\) on \(D(T_n)\). The same conclusion for \(K_n^{(\sigma)}\) is immediate.

The direct-sum realization has domain consisting of vectors \((\eta_n)\) with \(\eta_n\in D(H_n^{(\sigma)})\) and \(\sum_n\|H_n^{(\sigma)}\eta_n\|^2<\infty\). That realization is self-adjoint. Sectorwise boundedness need not be uniform in \(n\), and the proof does not require it. The sectorwise definition also avoids any unjustified equality of maximal direct-sum domains with an unexamined intersection of domains of two unbounded Fock-space operators. Smooth finite-particle Slaters are in every sector domain used.

### 3. The comparison polynomial

Substituting \(L_n=n-M_n\) gives exactly

\[
L_n(L_n-\sigma)-n(n-\sigma)=-M_n(2n-\sigma-M_n).
\]

For \(0\le m\le n\), \(n\ge1\), and \(\sigma\in\{0,1\}\), the second factor lies between 0 and \(2n\). Functional calculus therefore gives \(\|(H_n-K_n)\Phi\|\le2n\|M_n\Phi\|\). The exceptional vacuum sector is explicitly zero and never enters the estimates. The bound is valid for both conventions and does not assert smallness in operator norm uniformly across sectors.

### 4. Explicit packing and uniformity

The proposed \(f\) is nonzero, smooth and compactly supported in the radius-\(1/3\) closed ball. Its normalization is finite and positive. The fixed cube \(Q\) is disjoint from that support and lies strictly inside \(B(0,3)\). The example for \(\varphi\) is nonzero and has compact support inside the unit cube. Scaling it into distinct subcubes produces exactly normalized pairwise orthogonal smooth orbitals, also orthogonal to \(f\).

The kinetic energy of one scaled orbital is \(\ell_N^{-2}\|\nabla\varphi\|^2\), and \(\ell_N^{-2}=4m_N^2\). Since \(m_N\le2N^{1/3}\), the summed kinetic energy is at most \(16\|\nabla\varphi\|^2N^{5/3}\). Adding \(f\) changes this only by a fixed amount. The normalized exterior-product convention and the CAR then give \(\|\Psi_N\|=\|\Xi_N\|=1\) and \(a(f)\Psi_N=0\). No packing radius, potential, cutoff function or test function changes with \(N\).

### 5. Free leakage and commutator domains

There is a fixed smooth cutoff equal to 1 on \(B(0,3)\) and compactly supported in \(B(0,4)\). Its first and second derivatives are bounded. The commutator is a first-order differential operator mapping \(H^1\) boundedly into \(L^2\), with a constant depending only on the fixed cutoff.

For \(U(s)=e^{-ish}\), differentiating \(U(s-r)\chi U(r)g\) gives \(iU(s-r)[h,\chi]U(r)g\). Integrating and rearranging yields the minus-\(i\) sign in equation (4). All differentiation is valid on the smooth initial orbitals because the free group preserves \(H^2\) and cutoff multiplication preserves \(H^2\). The subsequent estimate uses only the conserved \(H^1\) norm. No hidden \(N\)-dependent \(H^2\) constant is introduced.

The relations \(\chi g=g\) and \(q\chi=0\) give the stated leakage norm bound. Summing its square over the freely propagated orbitals gives \(\lambda_n(s)\le C s^2n^{5/3}\). Free propagation preserves their orthonormality exactly. The proof uses no finite propagation speed for Schrödinger evolution.

### 6. Slater variance and the leaked number

Expanding \(M^2\) as one-particle diagonal terms and two-particle off-diagonal terms produces

\[
\langle M^2\rangle=\lambda^2+\lambda-\operatorname{Tr}(PqPq).
\]

The exchange term is essential and has the stated sign. Since \(q=q^*=q^2\), the variance equals \(\operatorname{Tr}(Pq(1-P)q)\), which is nonnegative and at most \(\operatorname{Tr}(Pq)=\lambda\). Finite rank of \(P\) makes every trace well-defined. The resulting estimate on \(\|M\Phi\|\) is a second-moment bound, not a substitution of the first moment for the second moment.

The proof applies the identity only to the free Slaters, never to an interacting evolution presumed to remain Slater. This distinction is crucial. In a general correlated state, a small expected leaked number need not control its second moment in the way needed here.

### 7. Sector Duhamel comparison and rates

For fixed \(n\), \(H_n-K_n\) is bounded. The exact Duhamel identity is valid on all sector vectors. Its orientation puts the comparison evolution on the initial state inside the integrand, so the existing free-Slater estimates apply. The scalar phase relating \(e^{-isK_n}\Phi_n\) to \(e^{-isT_n}\Phi_n\) does not affect the leaked-number norm.

Multiplication by \(2n\), followed by integration, produces the two powers \(n^{11/6}t^2\) and \(n^{8/3}t^3\). At \(t_N=\pi/(2N+1-\sigma)\), both \(n=N\) and \(n=N+1\) are comparable to \(N\), and both observation times are comparable to \(N^{-1}\) uniformly for \(N\ge1\). The errors are therefore \(O(N^{-1/6}+N^{-1/3})\), tending to zero.

This is enough despite the total kinetic energy growing as \(N^{5/3}\): the argument compares interacting and free evolutions, not either evolution to the initial vector. In dimension \(d\), the corresponding error exponents are \(-1/2+1/d\) and \(-1+2/d\); this estimate supplies decay exactly when \(d>2\). No endpoint claim is hidden.

### 8. Matrix element and both evolution signs

With the inner product linear in its second argument,

\[
F_N^H(t)=\langle e^{-itH}\Xi_N,a^*(f)e^{-itH}\Psi_N\rangle.
\]

Both comparison errors are therefore of the already estimated forward Schrödinger form. Replacing the two vectors separately yields their sum as an error bound, with coefficient 1. There is no unestimated mixed state.

The reference scalar-energy difference is \((N+1)(N+1-\sigma)-N(N-\sigma)=2N+1-\sigma\). Free covariance gives \(a^*(e^{ith}f)\). The CAR and \(a(f)\Psi_N=0\) imply

\[
\langle a^*(f)\Psi_N,a^*(e^{ith}f)\Psi_N\rangle=\langle f,e^{ith}f\rangle.
\]

The evolved \(f\) need not be orthogonal to the occupied orbitals. The chosen time makes the scalar phase exactly \(-1\), while the last scalar product tends to 1 by strong one-particle continuity. Thus the matrix element tends to \(-1\), compared with 1 at zero.

### 9. Operator norm and the actual annihilation witness

The creation difference has norm at most \(2\|a^*(f)\|=2\), and its matrix element between the two unit vectors tends to \(-2\). The norm therefore tends to 2. Taking adjoints transfers the operator norm to the annihilation difference. More strongly, the adjoint matrix-element identity supplies the lower bound directly on \(D_N^{(\sigma)}\Xi_N\), with the correct conjugation. Its norm also tends to 2. This verifies the theorem's state-level assertion, not only an unspecified supremum over states.

### 10. Topology and state quantifiers

The observable, potential and bounded interaction region remain fixed; the state and time vary with \(N\). Such variation is valid for witnessing failure of operator-norm continuity. Each \(\omega_N\) is a normalized vector state, and \(\omega_N(D_N^*D_N)\to4\) follows exactly from the established vector norm.

For every fixed vector, unitary strong continuity instead gives \(D(t)\eta\to0\). The proof explicitly states this. For completeness, every fixed normal state has the same vanishing quadratic expectation: write a density matrix as \(\rho=\sum_j p_j|\eta_j\rangle\langle\eta_j|\), use \(\|D(t)\eta_j\|^2\to0\), and dominate by \(4\|f\|^2\) in the summable weights. Nothing in the audited proof contradicts that fact or needs a fixed normal-state discontinuity.

## Adversarial controls and reproducibility

The independent program constructs CAR creation matrices from occupation-bit signs on seven modes, with a 128-dimensional Fock space. Its complex non-diagonal positive one-particle Hamiltonian does not preserve the chosen inside subspace. Initial orbitals are rotated inside that subspace, so the tests are not limited to diagonal occupation states. Both ordering conventions and generic times are included; generic times are important because a wrong phase sign is invisible at a phase of exactly \(\pi\).

The run includes:

- Exact matrix CAR checks.
- 24 reference matrix-element and phase cases.
- 48 first- and second-moment cases, including nonzero exchange terms.
- 16 vector-valued Duhamel identities checked by 40-node Gauss-Legendre quadrature.
- Independent free covariance, two-vector comparison and annihilation-adjoint checks.
- Detection of deliberately wrong covariance sign, sector-phase sign and missing normal-order correction.
- Detection of the false replacement of the second moment by the mean.
- Explicit correlated-state and rare-leakage controls showing why the Slater variance estimate and leaked-number control cannot be omitted.
- Exact rational dimension exponents and 16,768 sector-polynomial cases.
- Packing inequalities checked at cube-boundary particle numbers.
- Frozen author-file fingerprints and optional retained-source PDF fingerprints.

All controls passed. The largest vector Duhamel residual was \(6.17\times10^{-14}\); the largest reference matrix-element residual was \(2.52\times10^{-14}\). The evolved test orbital had occupied-space overlap as large as 0.243, so the CAR test genuinely exercises the case where post-evolution orthogonality fails. The author's own verification program also passed when rerun with source-byte validation.

To reproduce, run:

`OPENBLAS_NUM_THREADS=1 python independent_checks.py --author-dir PATH_TO_PUBLIC_V2 --source-dir PATH_TO_RETAINED_PDFS`

Omit the optional source directory to check the public author packet and finite controls without retained PDFs. NumPy and SciPy are required. The output records the Python and NumPy versions. The raw results are in `INDEPENDENT_RESULTS.json` and `AUTHOR_RESULTS.json`.

Finite-dimensional numerical identities do not prove the continuum limit. The acceptance decision rests on the full analytical verification above; the controls target algebra, signs, ordering, normalization, and implementation integrity.

## Findings and disposition

- Critical or major mathematical findings: none.
- Required proof corrections: none.
- Optional correction patch: none issued because no correction is needed.
- Source and scope alignment: pass for the bounded-region existential \(d=3\) statement.
- Prior full-space theorem dependency: none.
- Fixed-state discontinuity claim: absent and explicitly disclaimed.
- Original packet preservation: all reviewed author bytes remain unchanged.
- Publication action: none performed by this review.

The original bounded-region obstruction is closed by this self-contained construction within the theorem's stated scope. A broader literature-priority determination remains separate.
