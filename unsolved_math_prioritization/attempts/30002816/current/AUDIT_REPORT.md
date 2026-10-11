# Independent audit: Grassmann degree-one SOS

Date: 9 October 2026 UTC. Target: problem 30002816 / OWR-13498-004, rank 1114.

## Verdict and scope

**ACCEPT the mathematical reduction in the pinned manuscript.** It proves that the real oriented Grassmann orbitope C_(4,12) has no finite semidefinite lift. Therefore the original universal assertion that every supporting function is a sum of squares of affine polynomials of degree at most one fails. The proof establishes existence of a failing rational-coefficient linear functional before comass normalization.

This verdict does not establish priority or novelty, minimal failing dimension, a coefficient-level counterexample, or an exact numerical comass. It uses Fawzi's published theorem as an external mathematical dependency; the audit does not reprove that theorem. No mathematical repair was required. Two prose-formatting corrections and optimization-safe checks were incorporated by the author before the final freeze.

Audited author freeze:

- PROOF.md: 16083 bytes; SHA256 11d39172d04bd9cace099a3c2805a62c253c7e902a44d9584429c0dce758ef60
- All ten manifest-listed files were verified before and after the computational audit. All remained unchanged.
- The final PROOF.md and the other explanatory author documents were read in full. The coordinate certificate and executable were independently checked, rather than trusted from their reported PASS status.

## 1. Original question and degree convention

The original OWR discussion on printed pp.708–709 takes the convex hull of unit simple real k-vectors with both orientations, and formulates its certificates on that orbit modulo its vanishing ideal. Its degree bound D=1 includes constants. Equality is required on the orbit, not on the whole convex body. Its discussion for n at most 7 is computational evidence; the conjecture quantifies over all Grassmann orbitopes. The manuscript preserves these conventions and the full universal quantifier. The target is not weakened to homogeneous-only squares or a selected family of forms. The reported e_1 through e_n wedge on p.708 is incompatible with the displayed exterior degree k and is correctly read as e_1 through e_k. [Original report](https://ems.press/content/serial-article-files/46561).

## 2. Compact moment implication

For any compact X in the unit sphere, J_2 = I(X) intersected with polynomials of degree at most two is finite-dimensional. Thus imposing L_M(g)=0 on a basis creates finitely many affine equations, regardless of whether generators of the entire ideal have been computed.

The definition L_M(p_i p_j)=M_ij is consistent with symmetry: for h=a_0+sum a_i p_i, L_M(h squared)=a^T M a, including the factors of two on off-diagonal coefficients. M_00=1 and the sphere polynomial give trace M=2. Positivity bounds diagonal entries between zero and two and bounds each off-diagonal entry by the geometric mean of the corresponding diagonals. The feasible set is therefore compact. Its linear projection T_X is compact as claimed.

Every rank-one matrix (1,p)(1,p)^T with p in X is feasible, so conv(X) is contained in T_X. An affine-linear SOS for a supporting function differs from that function by an element of J_2, since every term has degree at most two. Evaluation on any feasible M makes the supporting function nonnegative at the projected point. If every supporting function had such a certificate, all projected points would lie in the intersection of the supporting halfspaces, namely conv(X).

This proves the implication the manuscript uses. It does not require strong duality, attainment of a dual SDP, closure of an otherwise nonclosed projection, or a converse theorem about theta bodies. The matrix size for X_(4,12) is binomial(12,4)+1 = 496. Additional affine equations can be imposed within a spectrahedron or encoded by scalar LMI blocks; either convention gives a finite lift.

## 3. Kähler equality and orientations

The real Euclidean convention Je_j=f_j, Jf_j=-e_j makes omega(e_j,f_j)=1. Restricting omega to a real four-plane gives a skew operator whose singular values do not exceed one, since orthogonal projection cannot increase the norm of Jv. Its Pfaffian is the value of omega squared divided by two on the oriented unit four-vector.

Pfaffian value +1 forces both paired singular values to have magnitude one. Consequently the compression preserves the norm of every vector in the plane. The perpendicular component of Jv must vanish, so the plane is J-invariant. Its complex orientation, represented by a,Ja,b,Jb for a complex-orthonormal pair, has Pfaffian +1; the opposite orientation has value -1. This proves both the inequality and the exact equality locus.

If a convex combination has Phi=1, every positive-weight summand has Phi=1. Finite convex combinations suffice, and the convex hull is compact. Thus the exposed face is exactly the hull of positively oriented complex two-planes. No negative orientation is inadvertently included.

## 4. The real-linear embedding

The chosen u_j=(e_j-i f_j)/sqrt(2) span the +i eigenspace of J; their conjugates span its -i eigenspace. The exterior products u_I wedge conjugate(u_J) are a complex basis of the (2,2) summand of the fourth exterior power of the complexification. There are 15 times 15 = 225 of them. This proves injectivity of the complexified coefficient map.

For Hermitian H, conjugation swaps I,J and the two factors of exterior degree two. The latter swap has sign +1. Hence A(H) is real, and restriction gives a real-linear injection from the 225-dimensional real Hermitian space into the 495-dimensional real exterior space. This is the required linear bridge, not merely an identification of generating points by a nonlinear map.

The normalization and sign were independently checked. A(H) is one quarter of the sum written with unnormalized w_j=e_j-i f_j. The identities for a and Ja give a wedge Ja = -i times a-hat wedge conjugate(a-hat). Two factors -i contribute -1, and the middle exterior swap contributes -1 again. Therefore A((a wedge b)(a wedge b)^*) = a wedge Ja wedge b wedge Jb with positive sign.

A decomposable unit complex bivector can be written as the wedge of a complex-orthonormal pair after absorbing a unit scalar. Conversely every positively oriented complex two-plane yields such a projector. Consequently F=A(K). The coefficient of e_i wedge f_i wedge e_j wedge f_j is precisely H_(ij),(ij), so Phi composed with A is trace. This is confirmed on the entire Hermitian basis, including the imaginary off-diagonal columns.

## 5. Exact separable-state section

For the orthogonal split C6=U plus Z with both blocks of dimension three, the pure subspace D consists of exterior-square U plus exterior-square Z; the mixed subspace B=U wedge Z has complex dimension nine.

For every convex representation H=sum lambda_t z_t z_t^* with positive weights, trace(P_D H)=sum lambda_t ||P_D z_t|| squared. If this trace is zero, every term is zero. Thus every participating z_t lies in B. Matrix support alone would not have sufficed to identify the generating set; the manuscript correctly establishes the stronger summand statement.

If a nonzero decomposable bivector a wedge b lies in B, its two pure components vanish. The projections of a,b into each of U and Z therefore span at most a line. Neither span can vanish, since that would make the nonzero bivector both pure and mixed. Writing a,b in the two spanning directions yields a nonzero scalar multiple of x wedge y, with x in U and y in Z. Conversely every such wedge is decomposable and mixed. The unitary map x tensor y to x wedge y therefore identifies these vectors precisely with nonzero rank-one tensors.

Norms multiply because the two blocks are orthogonal, so unit bivectors correspond to product projectors with both factors normalized. The complete convex-hull identity is K_0 isomorphic to Sep(3,3).

The displayed real form Q evaluates on A(H) as the pure-block trace. Its value need not be nonnegative away from the Kähler face. The simultaneous equations Phi=1 and Q=0 are exactly the stated section, so no global-supporting assumption about Q is used.

## 6. External theorem and lift closure operations

Fawzi's published p.1319 uses normalized complex product projectors, matching this section. On p.1320, a semidefinite representation permits a finite Hermitian LMI with extra real variables followed by a linear map. Thus it is an arbitrary projected lift. Theorem 1 on p.1321 excludes it for Sep(3,3); the accompanying discussion explicitly includes that case and distinguishes the result from failure of a particular hierarchy. The publication is Communications in Mathematical Physics 386 (2021), 1319–1335, DOI 10.1007/s00220-021-04163-2. The definition, statement, and relevant discussion were read in both the local published PDF extraction and the public PDF; the theorem page was visually inspected. [Published PDF](https://www.repository.cam.ac.uk/bitstreams/e6e52df9-b317-4616-9462-c79a3cb4844b/download).

An affine section of a lifted set is obtained by imposing its equations on the lifted variables. A linear map of a lift is obtained by composing maps. The inverse of A on its image, followed by the mixed-block identification, is real-linear and extends to the ambient real space. These operations would turn any finite lift of C_(4,12) into a finite lift of the prohibited section. Real symmetric LMIs are a subclass of Hermitian LMIs, so there is no real-versus-complex loophole.

## 7. Rational separating form and calibration

The fixed moment relaxation strictly contains C_(4,12), since equality would itself be a forbidden finite lift. Let x be an exterior point of the body in that relaxation. Strict separation supplies c with a positive gap gamma=c dot x - max_X c dot p.

If ||c'-c|| is less than gamma divided by 2(||x||+1), the change of this gap has magnitude less than gamma/2, because X lies on the unit sphere. Density of rational vectors therefore gives a rational c' with the same strict separation. Any feasible M projecting to x evaluates its supporting function negatively, contradicting the nonnegative value required of an affine SOS. This checks the rational-existence assertion without assuming that the SOS cone itself is closed.

The coordinate simple vectors and their negatives belong to X, so the maximum of a nonzero linear functional is positive. Normalizing by that maximum preserves the failure of SOS and gives comass one. The normalization need not preserve rational coefficients; the manuscript correctly claims rationality before normalization and supplies no explicit coefficient list.

## 8. Harvey–Lawson implication

Question 6.5 on printed p.68 asks for a local completion by differential p-forms of the squared norm identity on all simple p-vectors. Its displayed equation was read visually, not inferred from damaged OCR. Such a completion immediately gives the manuscript's affine SOS identity on unit simple vectors. Conversely the manuscript's comparison at p and -p, followed by a contact point, correctly gives ||a|| squared=1/2 and the orthogonal-projection completion. [Original article](https://archive.ymsc.tsinghua.edu.cn/pacm_download/117/6313-11511_2006_Article_BF02392726.pdf).

Regarded as a constant four-form on R12, the failing comass-one functional is closed. A local collection of completing forms would yield a forbidden pointwise collection at every point. Allowing their coefficients to vary therefore cannot restore the identity. The source question is genuinely addressed.

## 9. Independent exact computation and negative controls

The independent validator uses only the Python standard library, integer pairs for Gaussian integers, exact rational parsing, 4 by 4 determinant expansions, and explicit exception checks. It does not import or execute the author script to construct its reference map.

It verified:

- All 225 real Hermitian-basis columns in the author's certificate, including every exact rational exterior coefficient.
- The full Gram matrix: 15 diagonal entries equal one, 210 equal two, and all off-diagonal entries vanish. Rank is therefore 225.
- Phi equals trace and Q equals the pure-block trace on all 225 columns.
- The projector identity for arbitrary a,b in C6, expanded in 24 independent real variables and all 495 exterior coordinates. There are 11760 nonzero polynomial terms after cancellation. This extends beyond the author's check restricted to opposite three-dimensional blocks.
- All nine mixed Plücker coefficients equal negative twice the corresponding 2 by 2 minors, with other quartets zero.

Three positive runs passed in normal, -O, and -OO modes. Fifteen intended certificate mutants were rejected in each mode, 45 rejections total. They test global orientation, the quarter factor, imaginary conjugation, omitted off-diagonal data, corrupted pure and mixed diagonals, basis labels/orders, duplicate entries, invalid fractions, Gram norms, inverse normalization, omitted columns, and unreviewed schema fields. Each failed at its intended error class, not by timeout or an unrelated execution error.

All three independent runs operated with actual UID and EUID 1000 and zero effective capabilities. The candidate tree and validator were inside read-only mounts; attempts to open an existing candidate file for append and a new candidate file for creation both raised EROFS. The author checker was also regenerated in all three modes with the candidate read-only and only a separate output directory writable. Both generated JSON artifacts matched the frozen author hashes in all modes. Candidate pins were unchanged afterward.

These computations verify the finite coordinate bridge and checker behavior. They do not replace the convex-geometric argument, the source theorem, or the audit of quantifiers.

## 10. Boundaries and disposition

The accepted conclusion is a negative resolution of the stated all-dimensional affine-degree-one SOS conjecture through an explicit dimension-(4,12) reduction and an existential failing form. Lower-dimensional cases are untouched. No third-party source document is included in this audit packet. Source hashes and inspection locations are recorded separately as metadata. No repository, queue, publication, or external-message action was performed by this audit.
