# Independent audit of the all-rank tangency-complex construction

14 October 2026 UTC. Row 1775 / 30004611, shared substantive pass 2. Qualified mathematical acceptance of the identified construction. This audit is not another mathematical approach, a full-resolution certificate, or a literature-completeness certificate.

## 1. Frozen candidate and verdict

Accepted candidate: `tangency_complex_sequences.md`, 26,964 bytes, SHA-256 `3c11ab4b3eea7f213722ebedec05ec4d1cd19546fa136793735d0efea0b62e67`.

The initially reviewed candidate was 22,044 bytes, SHA-256 `88d435e235a6076b468736c55ba8d04633e395433f6ee4bb7eaa767467be0c08`. The final candidate adds the exact four-plane cokernel calculation and the termwise-acyclicity/dimension-shifting consequences. I independently checked those additions as well as the original construction. No mathematical correction is required.

Accepted results are:

1. The ordinary and Ziegler short exact sequences of the explicit two-term complexes, with the stated ideal-twisted kernels and actual ordinary/Ziegler degree-zero targets.
2. Their six-term exact sequences of cohomology sheaves and the independent matrix presentations of the corrections.
3. The graded stalkwise Tor description of the Ziegler defect, including its full value in the credited four-plane example.
4. The hypercohomology sequences, two-row spectral sequences, termwise acyclicity, and correctly indexed dimension-shifting statements.
5. The support/cohomological bound for the defects and the displayed high-degree tail, beginning exactly where stated.
6. The center-deleted deletion-cohomology formulas in the coloop case, including the dimension-two boundary qualification.

These remain corrected and derived partial constructions. They do not supply an unrestricted short exact sequence consisting only of the three requested original derivation sheaves, do not rule out every alternative construction, and do not resolve Mücksch's broad Problem 6.3. No external freeness-from-cohomology criterion is used or audited here.

## 2. Source and comparison conventions

I read the pass-1 common-poset construction and its independent audit, the source-verification record, and the retained primary text at Mücksch's introductory functor convention, Definition 4.1, and Problem 6.3. The retained arXiv v3 PDF was independently rehashed: 254,251 bytes, SHA-256 `2a4309b567e5113b48124cc4f17feb1c051c4dbb8ffacebd23ed700fd587676b`.

The construction uses the source's covariant functor convention on nonzero flats ordered by geometric inclusion. The closed lower ideal Q of flats contained in H is the nonzero-flat poset of the ordinary restriction. Exact extension by zero along Q→P, including the zero arrows leaving Q, is valid.

For deletion, the closure c(X) is the least deletion flat containing X. Evaluation there computes the direct-image functor from the geometric deletion poset, so the transport is exact and preserves its sheaf cohomology. If deletion is nonessential, that geometric poset retains its nonzero center. It must not be identified with the source-style center-deleted poset. Section 8 treats the latter separately and correctly.

The ideal I has stalk alpha S on Q and S off Q. On an arrow leaving Q its transition is the inclusion alpha S→S. It is stalkwise flat, sufficient to commute tensor with the cohomology sheaves of these complexes; it is not a globally constant (-1) shift. All maps in the accepted result retain these transitions.

The audit does not assert arXiv/version-of-record byte identity, source novelty, or the validity of other theorems from the source paper. The relevant primary reference is Paul Mücksch, *On Yuzvinsky's lattice sheaf cohomology for hyperplane arrangements*, https://arxiv.org/abs/2008.13700v3 .

## 3. Ordinary complex: termwise maps and the connecting correction

Write C'=[Der(S)→K'] and C_H=[N→K'], in degrees 0 and 1. The definition of N by normal evaluation is natural on every poset arrow. The inclusion C_H→C(A) has degree-one map inserting the zero H-row. Its quotient is precisely [i_*R→i_*R] with identity differential, so it is a natural quasi-isomorphism. This does not assert a global splitting.

For the ordinary short exact complex sequence, the degree-zero injection on Q is multiplication alpha Der(S)→N. The quotient is Der(R): a derivation tangent to H induces an arbitrary derivation of R, and its induced derivation is zero exactly when all its coefficients are divisible by alpha. Off Q the injection is the identity.

In degree one, multiplication by alpha is injective on every S/(alpha_L), since L≠H and alpha is nonzero in the domain S/(alpha_L). Its quotient is S/(alpha,alpha_L). Thus the quotient has a separate ordinary row for every original L, even if several L restrict to the same hyperplane. Reducing a tangent derivation induces the derivative of the restricted equation, so the quotient differential is exactly the asserted one.

These maps commute with projections that discard hyperplanes and with the nonunit transitions of I. There is no arrow from P\Q into Q to check; arrows leaving Q have zero quotient transition. The first three maps on cohomology sheaves are the actual pass-1 multiplication and ordinary restriction maps. The connecting homomorphism then identifies the ordinary defect with ker(I⊗T'→T_A). This identification uses the independently presented cokernels T' and T_A, rather than defining them as an image or a chosen restriction defect.

The explicit map [a_L]↦[(0,alpha a_L)] is well-defined: changing a representative by the deletion derivative of eta changes its image by the original derivative of alpha eta, whose H-component vanishes modulo alpha. The shift in its source is T'(-1) on Q, with no such shift off Q.

## 4. Ordinary repeated rows are not Ziegler powers

After the stated normalization, the repeated-row differential factors through the diagonal K(B)→K_rep. That diagonal is injective over every field. Its quotient is W, and the image of the derivative differential lies in the diagonal. Hence T_B→T_rep is injective and its cokernel is exactly W.

A chosen representative in each global restriction fiber gives a compatible retraction on Q, because an entire fiber is either present or absent at a point of Q. No division by the fiber size is needed. Thus the exact sequence 0→T_B→T_rep→W→0 remains valid when the field characteristic divides a multiplicity. The statement makes no identification between these ordinary repeated rows and the power quotients used by the Ziegler complex.

## 5. Grouped complex, all-field kernel, and Tor grading

A derivation theta in W_S kills alpha. For normalized equations l_L=beta_K+c_L alpha in one fiber, theta(l_L)=theta(beta_K). Distinct l_L are relatively prime irreducible elements of the polynomial UFD. Simultaneous divisibility by them is therefore equivalent to divisibility by their product q_K,X. This argument uses relative primality of factors, not a false assertion that their ideals are comaximal.

It proves H^0(C_E)=E at points outside H as well as inside H. Partial fibers off Q cause no problem: if X⊆Y then q_K,Y divides q_K,X, giving the quotient transition and making the fixed derivative row natural. On Q the entire global fiber is present whenever K contains X. Consequently specialization of its product is precisely beta_K raised to the global Ziegler multiplicity. There is no derivative of beta_K^m, no multiplication by m, and no substitution of Euler multiplicity.

Changing an extension of beta_K changes it by a scalar multiple of alpha, invisible to W_S. Scaling beta_K rescales its derivative row by a unit and leaves its principal product ideal unchanged. Thus the choice dependence is exactly the stated natural isomorphism of presentations.

Multiplication by alpha on each S/(q_K,X) is injective because q_K,X has no alpha factor. The quotient on Q is R/(beta_K^m); off Q the quotient is zero. Degree zero specializes W_S to Der(R). This verifies the Ziegler short exact complex sequence, its differential, and every poset transition.

The resulting correction is ker(alpha:U_X(-1)→U_X). The graded resolution S(-1)→S of R identifies it with ordinary module Tor_1^S(U_X,R), including its degree. The identification is natural under the quotient maps defining U. It is not silently identified with functor-category Tor or sheaf cohomology. The termwise injectivity also proves the derived-specialization statement: the cone of alpha on the appropriately shifted complex is quasi-isomorphic to its ordinary quotient C_Z.

For xyz(x+y+z), H={z=0}, the presentation columns (1,0,1) and (0,1,1) reduce U to S/(x,y,x+y+z)=K. Thus the entire Ziegler defect is K(-1), over every field. After the already-described rank-four promotion it is K[w](-1) at the retained bad flat. The ordinary deletion derivative rows are independent over every field, so T'=0 and the ordinary restriction is onto. This is a refinement/control of the credited Abe–Kawanoue example, not a novelty assertion.

## 6. Hypercohomology and the acyclicity additions

The ordinary and Ziegler short exact complex sequences give genuine long exact hypercohomology sequences. Exact extension by zero preserves the restriction hypercohomology. Their spectral sequences have E2^{p,q}=H^p(H^q(C)), q=0,1. The differential from the obstruction row to the derivation row is d2:(p,1)→(p+2,0), exactly as displayed. A six-term exact sheaf sequence cannot instead be concatenated into a cohomology long exact sequence.

The finite cochain model using the coefficient at the final vertex of a strict chain has the correct variance. Its degree-zero differential s_Y−M(X≤Y)s_X agrees with the sheaf's covariant convention. Applying it to the complexes and totalizing gives the asserted exact sequences of total complexes.

The added termwise-acyclicity proof is accepted with the following points independently checked:

- Constant sheaves on P and Q have acyclic nerves because these posets have maxima. Global evaluation Der(S)→R is onto, and S→R is onto, proving acyclicity of N and I respectively.
- Each ordinary hyperplane row is a closed extension of a constant module on a subposet with a maximum. Restriction rows have the same property, or have empty support when the restricted hyperplane is zero.
- To deduce acyclicity of I⊗K', it is essential that ΓK'→ΓK_rep is onto; the candidate proves this componentwise. Acyclicity of the outer coefficient terms alone would not suffice.
- Each grouped row is an exact transport from its fiber arrangement, of rank at most two. For ell≥3 its geometric poset retains a nonzero minimum; arbitrary coefficient sheaves on that poset are acyclic. For ell=2 and a multiple fiber, the punctured fiber poset is a star whose top has zero coefficient, so its cochain groups in positive degree are zero. A singleton fiber has a nonzero minimum instead.
- The global map ΓG→ΓG_Z is onto: it is the sum of S/(q_full)→R/(beta^m) when ell≥3, and its target is zero when ell=2. This additional surjectivity proves acyclicity of I⊗G.

Therefore every displayed two-term complex has hypercohomology zero above degree one. Its spectral sequence yields the exact five-term sequence 0→H^1(M)→hyperH^1(C)→H^0(T)→H^2(M)→0 and isomorphisms H^p(T)→H^{p+2}(M) for p≥1. These are correctly indexed and do not discard the extension differential. For C(A), hyperH^1 is the whole-arrangement matrix cokernel T(A); it need not equal ΓT_A.

The additional H^k(E)→H^k(D_A) isomorphism for k≥1 is also correct: I is acyclic and ΓD_A→ΓI=alpha S is onto by Euler derivation. It does not give a sheaf splitting. No conclusion about freeness is imported from this isomorphism or from these vanishing statements.

## 7. Defect support, tail, and center deletion

The pass-1 all-field rank-two lifting calculation implies zero ordinary and Ziegler defects at codimension at most two. Their remaining support is the lower ideal Q_bad of nonzero flats in H with codimension at least three. Its largest chain has length at most ell−4. Exact extension by zero and the finite cochain model imply H^p(C_def)=0 for p>ell−4. In rank at most three the defect sheaf itself is zero.

In 0→M→i_*D_target→C_def→0, the map H^n(M)→H^n(D_target) is an isomorphism once both H^{n−1}(C_def) and H^n(C_def) vanish, namely for n≥ell−2. Substitution into the other short exact sequence gives exactly the stated tail. The candidate correctly asserts exactness starting at its second displayed term; it does not pretend an unspecified incoming map makes its first term exact. Extending this tail downward would require correction data.

If deletion is nonessential, its center T' is a line transverse to H. Every deletion hyperplane is the pullback of a unique restricted hyperplane, so all multiplicities are one. The order isomorphism X↦X⊕T' from Q to the center-deleted deletion poset is valid, and the decomposition of the source deletion functor into S⊗_R D_B plus the constant S⊗_K T' follows stalkwise with compatible arrows.

Flat scalar extension commutes with the finite cochain complex. The constant summand is acyclic because Q has maximum H. This proves both the positive-degree cohomology formula and its stated degree-zero correction. For ell=2 the deleted center is the only deletion hyperplane, so identifying those global sections with D(A') would be false. The candidate expressly preserves that boundary case.

## 8. Independent finite controls

The independently written `independent_audit/check_tangency.py` builds homogeneous polynomial quotient spaces by modular row reduction and then constructs the actual derivative and restriction matrices. It does not execute any downloaded source program. It checks:

- that ordinary and Ziegler coefficient restrictions land in their named target kernels;
- injectivity of alpha on the condition modules and compatibility with the derivative images;
- the ordinary defect against the kernel of alpha from the deletion obstruction into the original obstruction;
- the Ziegler defect against the graded alpha-torsion/Tor formula;
- equality of repeated-row and ordinary kernels, and the expected repeated-row cokernel increment.

All 55 field/degree/example controls passed, for homogeneous degrees 0 through 4:

1. Credited four-plane arrangement xyz(x+y+z), over F2, F3, F5, F7. The ordinary defect is zero in the checked degrees; the Ziegler defect is one-dimensional exactly in degree one.
2. Five-plane repeated-fiber control z x (x+z) y (x+y+2z), over F2, F3, F5, F7. The repeated x-fiber has multiplicity two. In characteristic two its grouped U is K[z]; in the tested odd characteristics it is K[z]/(z^2), up to a nonzero scalar relation. The checked Ziegler defect is accordingly zero in characteristic two and one-dimensional in degree two in the odd characteristics. The repeated ordinary row contributes one dimension at every tested degree, including characteristic two.
3. Credited seven-plane arrangement z x y (x−z)(y−z)(x−y+z)(x−y−z), over F3, F5, F7. The checked ordinary defect has dimension one in degrees two and three; the Ziegler defect has dimension one in degree three. Each matches its independent correction matrix. Characteristic two is excluded from this seven-plane control because two original hyperplanes coincide there.

These bounded checks corroborate the proofs; they do not replace the arbitrary-field argument, establish unseen degrees by experiment, or constitute new counterexamples or an exhaustive search.

Artifacts:

- `independent_audit/check_tangency.py`: 7,958 bytes, SHA-256 `4dc115fa4ead4ee523b379d00e154a22839b21e213c06170d94160bcc21187df`.
- `independent_audit/finite_checks.json`: 14,577 bytes, SHA-256 `8278296987adb9d760e8807ae610140e481f585680d06f8b9b9ef2d01a14fe0e`.

## 9. Final scope

The accepted construction genuinely identifies the ordinary and Ziegler derivation targets and explicitly presents the additional obstruction sheaves. It is stronger than renaming a restriction image or observing that an arbitrary morphism has a cone. Nevertheless, its extra obstruction terms and derived formulation do not by themselves fulfill the original request for unrestricted short exact sequences of the named original sheaves. That problem remains unresolved by this packet.

It does not certify unrelated source statements or the separately audited complementary report. The examples and earlier row-992 work remain credited.
