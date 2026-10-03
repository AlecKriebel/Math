# Independent mathematics before candidate inspection

Primary source first: EMS serial article 46073, Davis (joint Dymara, Januszkiewicz, Okun), OWR 43/2006, printed 2588–2590, visually checked physical PDF pages 10–12. Printed 2589 distinguishes right group modules for cohomology and left group modules for homology. The question on printed 2590 concerns finite generation of the total group-ring coefficient cohomology as a group module for every virtually type FP group.

Conventions: R_G = ZG; a finite-length resolution P_* -> Z is of trivial **left** R_G-modules by finitely generated projectives. C^* = Hom_{R_G}(P_*,R_G) is a complex of **right** R_G-modules by (f r)(p)=f(p)r. FP here means finite length, not merely FP_infinity or finite presentation. Virtually FP means a finite-index FP subgroup. Neither abelian-group finite generation nor ordinary cohomology algebra finite generation is the claim. No original-question solution or present-day literature completeness is inferred below.

## A. Duality-quotient extension closure and exact right action

Let 1 -> N -> G -> Q -> 1, where N has a finite-length finite-projective resolution and Q has such a resolution of length d. Assume H^p(Q;ZQ)=0 for p != d and D_Q=H^d(Q;ZQ) is Z-flat. This is the needed duality-quotient hypothesis. Also assume each A_q=H^q(N;ZN) is finitely generated as a right ZN-module. No Z-flatness of A_q is assumed.

Because P_N is termwise finitely generated projective and ZG is free as a left ZN-module, evaluation is a cochain isomorphism

    Hom_ZN(P_N,ZN) tensor_ZN ZG = Hom_ZN(P_N,ZG).

Flatness of ZG over ZN gives H^q(N;ZG)=A_q tensor_ZN ZG as a right ZG-module. There is simultaneously the quotient Q action used by Hochschild–Serre. In the inhomogeneous bar convention a lift g acts by

    T_g f(n_1,...,n_q)=g f(g^{-1}n_1g,...,g^{-1}n_qg).

This acts on coefficients by left multiplication, so commutes with right multiplication by every element of ZG. For n in N, T_n is chain homotopic to identity; consequently the cohomology action factors through Q. It permutes the direct summands of ZG indexed by N\G transitively. Let j:A_q -> H^q(N;ZG) be the summand inclusion induced by ZN -> ZG. The map

    ZQ tensor_Z A_q -> H^q(N;ZG),   q tensor a -> T_g j(a)

is a left ZQ-module isomorphism and is independent of lift because T_n is identity on cohomology. This is NOT the induction formula with an arbitrary diagonal quotient action left unstated.

To record the commuting right action precisely define c_g on A_q by

    c_g f(n_1,...,n_q)=g f(g^{-1}n_1g,...,g^{-1}n_qg)g^{-1}.

At cohomology c_g c_h=c_{gh} and c_n(a)=a n^{-1}. Thus a*g:=c_{g^{-1}}(a) is a right G action extending the existing right N action, and is semilinear: (a n)*g=(a*g)(g^{-1}ng). The basic relation is

    j(a)g = T_g j(a*g).

Sharifi's independently fetched bound PDF, Theorem 4.3.12 on printed/physical 97, supplies the first-quadrant convergent sequence E_2^{p,q}=H^p(Q;H^q(N;ZG)) => H^{p+q}(G;ZG). Naturality in the coefficient module supplies the commuting right ZG-module action on every page, differential, and filtration. The theorem statement alone does not define the monodromy formulas above; they are derived here.

For a bounded finite-projective Q resolution, its regular dual cochain complex is termwise Z-flat. It has one cohomology group D_Q in degree d, also Z-flat. Tensoring it with any abelian A preserves this concentration. Equivalently the cohomological universal coefficient sequence is

    0 -> H^p(C_Q) tensor_Z A -> H^p(C_Q tensor_Z A)
      -> Tor_1^Z(H^{p+1}(C_Q),A) -> 0.

The Tor term is the exact reason flatness of D_Q is required when A may have torsion. Finite projectivity identifies Hom_ZQ(P_Q,ZQ tensor_Z A) with C_Q tensor_Z A. Therefore E_2 vanishes off column p=d; in that column it is D_Q tensor_Z A_q. There are no incoming or outgoing d_r, r>=2: a putative source or target would have different p. This is a genuine single-column collapse and no unresolved transgression remains. In each total degree the filtration has exactly one possibly nonzero piece, so there is an isomorphism, not merely an unspecified extension:

    H^{d+q}(G;ZG) = D_Q tensor_Z A_q,
    (u tensor a)g=(u bar(g)) tensor (a*g).

For finite generation pick right ZQ-generators u_i of D_Q (top cohomology is a quotient of a finitely generated projective) and right ZN-generators a_j of A_q. Given u_i q tensor a, choose a lift g of q and write a*g^{-1}=sum_j a_j n_j. Then

    u_i q tensor a = sum_j (u_i tensor a_j)(n_j g).

Thus the finitely many u_i tensor a_j generate the right ZG-module. Since N's cohomology is bounded, the total module is finitely generated. The extension G is FP by the finite-projective extension construction (or the usual resolution-of-an-extension argument); the cohomological conclusion above itself does not use an already chosen finite G resolution. This establishes the claimed subclass, not all FP groups.

Boundary checks: Q=1 recovers N. Q=Z has D_Q=Z with trivial orientation, so cohomology shifts by one with the transported right G action. Q finite nontrivial over Z is not a finite-dimensional duality quotient; its torsion cannot be slipped into this argument. If D_Q is not Z-flat, concentration of regular cohomology alone does not justify the collapse: Z --2--> Z, tensor Z/2, creates an extra lower cohomology group. No actual group with this toy complex is asserted.

## B. A finite bad matrix in an ambient FP group ring

Let G=F(a,b) x F(c,d), R=ZG, and chi:G -> Z send a,b,c,d to 1. Set

    x=ab^{-1}, y=cd^{-1}, z=bd^{-1}; H=ker chi.

The free kernel K_A=ker(F(a,b)->Z) is free on x_i=b^i x b^{-i}, i in Z. Likewise K_B is free on y_j=d^j y d^{-j}. Every pair in H can be expressed with these kernels and z; z x_i z^{-1}=x_{i+1}, z y_j z^{-1}=y_{j-1}. Thus

    H=(K_A x K_B) semidirect <z>,

and H is generated by x,y,z. H_2(K_A x K_B;Z)=K_A^ab tensor_Z K_B^ab has basis x_i tensor y_j. The z action shifts (i,j) to (i+1,j-1), so its coinvariants are free abelian on the integer i+j. H_1(K_A x K_B;Z) has no nonzero shift-invariant finitely supported element. The homological sequence for the Z extension has only columns 0 and 1, no differential, and gives

    H_2(H;Z)= direct_sum_{k in Z} Z.

Hence H is not FP_2: a resolution with finite projectives through degree 2 would, after tensoring the trivial coefficient Z, have finite generated abelian chain modules through degree 2 and consequently finitely generated H_2. This proof does not substitute non-finite presentability for non-FP_2.

Consider the right-linear matrix

    M:R^3 -> R,  M(u,v,w)=(x-1)u+(y-1)v+(z-1)w.

Over ZH its image is the right augmentation ideal I_H, since (st-1)=(s-1)t+(t-1). If ker M_H were finitely generated, taking a finite free cover of it would give a finite-projective partial resolution through dimension 2, contrary to H_2 above. Thus ker M_H is not finitely generated. R is a free, faithfully flat left ZH-module; exact tensoring gives ker M=(ker M_H) tensor_ZH R. If this were finitely generated, finitely many tensor expressions involve a finite set of elements of ker M_H; their span K_0 would have (ker M_H/K_0) tensor_ZH R=0, and faithfulness would force ker M_H=K_0. Contradiction. This is an explicit finite right-module matrix over the ring of an FP group whose kernel is not finitely generated.

Universal visible cycles: let v_k=z^k y z^{-k} and r_k=x v_k x^{-1}v_k^{-1}; these are identity in G for EVERY integer k because v_k lies in the second factor. The suffix Fox derivatives satisfy D_s(uv)=D_s(u)v+D_s(v), D_s(s^{-1})=-s^{-1}, and

    r_k-1=sum_{s=x,y,z}(s-1)D_s(r_k)=0.

Thus the displayed vectors are actual integral cycles, not exponent-vector coincidences. Their existence alone does not prove non-finite generation; the homology and faithful-flat descent proof does. Code computes exact words for k=-5,...,5 and records full vectors/residuals, plus counterfeits.

## C. Actual regular cohomology of the SAME ambient group

The left free augmentation resolution from the product of Cayley trees has ranks 1,4,4 in degrees 0,1,2. Its boundary is partial_1(e_s)=(s-1)e_0 and partial_2(e_{s,t})=(s-1)e_t-(t-1)e_s, s in {a,b}, t in {c,d}. The commuting cross-factor letters make partial_1 partial_2=0. Contractibility of the two trees proves that this is an exact augmented resolution universally; a finite evaluation cannot establish this.

The regular dual right-module cochain maps are

    delta_0(f)=((a-1)f,(b-1)f,(c-1)f,(d-1)f),
    delta_1(f_a,f_b,f_c,f_d)_{s,t}=(s-1)f_t-(t-1)f_s.

For each free factor F_2, C_F is 0 -> ZF_2 -> (ZF_2)^2 -> 0. Its delta_0 is injective: a finitely supported regular coefficient fixed under left a must vanish, since a has infinite orbits. Its cokernel D_F is Z-torsion-free: if m v=delta_0(f), reduce modulo m; delta_0 over Z/m is still injective by the same finite-support orbit argument, so f=m f' and v=delta_0(f'). Hence D_F is Z-flat and finitely generated as a right ZF_2-module by the two coordinate classes. Torsion-freeness is sufficient; no unsupported free-abelian decomposition is needed.

The product cochain complex is the tensor totalization of the two factor complexes. Their terms are Z-free and D_F is Z-flat, so the universal coefficient/Kunneth argument gives

    H^0(G;R)=H^1(G;R)=0,
    H^2(G;R)=D_{F(a,b)} tensor_Z D_{F(c,d)}.

The latter is Z-flat and finitely generated by four coordinate classes as a right R-module. This proves G itself is a positive example of the original property. The kernel in B is a syzygy in the induced augmentation presentation of the non-FP_2 subgroup H. It is NOT an identified cohomology group, nor a failed augmentation-resolution syzygy of G. Ambient noncoherence blocks a generic proof that every kernel of finite matrices is finitely generated; it does not produce the original counterexample. Any attempt to realize an arbitrary matrix as regular group cohomology would require a new, independently proved construction maintaining the left augmentation resolution, exactness, finite-projectivity, and specified group-ring action.

## Independence disclosure and strongest result

Before sealing: read only the literal primary EMS source, own freshly fetched sources, and the candidate SOURCE_MANIFEST.json / SOURCE_ADDITION_T4.json for URLs and bound-byte identification, after the literal primary pages. These metadata contained an obsolete Sharifi page locator; the actual fetched bound source was inspected independently at 97. No candidate mathematical prose or code, final/historical verdict, root verdict or sibling verdict was read before this document, code, full output and seal.

Strongest verified result: the duality-quotient extension closure above, and a fully explicit bad kernel over Z[F_2 x F_2] whose same ambient group has finitely generated total regular cohomology. Exact remaining gap: neither mechanism settles whether every virtually FP group satisfies the primary question. General FP kernels are uncontrolled and arbitrary noncoherent matrices have not been realized as regular cohomology of an FP group. Novelty/priority and current unsolved status remain unproved; these are standard-mechanism audit deductions.
