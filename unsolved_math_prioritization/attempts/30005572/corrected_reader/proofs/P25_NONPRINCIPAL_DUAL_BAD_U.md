# Nonprincipal CM assembly for the dual bad-U norm relation

Shared PASS 4/5, row 1777 / 30005572. Final frozen review draft, including the two supplements named below. This is a restricted arithmetic extension, not a solution of the construction contract. No novelty claim is made.

## 1. Statement and the operator being proved

Let F be imaginary quadratic, let p >= 7, and put L_A=F(A). Let q be **any** prime ideal, Q=Nq, and

    N=M q^n,  n>=1,  (M,q)=1,

with M proper and N admissible (injective reduction of global units). The lower M need not be admissible. Let c be prime to N and retain the actual LSSW auxiliary map f_{c,N} on all standard (r,1) Bianchi components.

Here is the dual convention. At q choose a local uniformizer nu, set y=diag(nu,1) at q and 1 elsewhere, and let U_q be the unnormalized homology correspondence whose constant-coefficient transpose is the y double coset. Define U_q^vee by the **inverse** y^{-1} double coset. This is the unnormalized transposed correspondence, without division by Q. Changing nu does not change either double coset: diag(u,1) belongs to the level group for every local unit u. On homology, U_q^vee carries component [a_r] to [a_r q].

For principal q=(pi), the rational inverse diag(pi^{-1},1) differs from diag(1,pi) by the rational central scalar pi. They give the same correspondence on the symmetric space and the same rational conjugation/transfer. Thus U_q^vee specializes to the operator proved in the accepted PASS 2 and PASS 3 results.

**Theorem A.** In this convention,

    Cor_{L_N/L_M} f_{c,N}(U_q^vee-1)=0.                 (1.1)

Put u_M=|{epsilon in O^times:epsilon=1 mod M}| and

    d=[L_N:L_M]=Q^(n-1)(Q-1)/u_M.

**Theorem B.** If p does not divide d and chi is a character of the prime-to-p ray group trivial on Gal(L_N/L_M), then

    f_{c,N}^chi(U_q^vee-1)=0.                           (1.2)

The existing unaugmented map satisfies the same equation wherever the source supplies an invertible auxiliary factor. A separately existing compactified map inherits it. All limitations concerning ramified characters, wild norm kernels, pure prime-power levels, the 5-primary part, small high levels, and unrestricted compactification remain.

Remark 5.2.10 of the source says only “a dual Hecke operator”; it does not provide an explicit bad-prime double-coset normalization. This note supplies the inverse-correspondence normalization compatible with the accepted principal result. It neither reinterprets the contract as false nor claims that the integral opposite local coset is the inverse coset.

Indeed, if z_q=nu I_2 and v_q=diag(1,nu), then

    v_q=z_q y^{-1}.                                    (1.3)

The integral opposite operator has component shift [a_r q^{-1}], whereas the inverse operator has shift [a_r q]. The central correction in (1.3) must not be dropped for a nonprincipal q. No ideal Artin symbol R_N(q) is used at the bad modulus.

## 2. Inputs and a supported comparison lemma

The accepted PASS 2 proof supplies the trace-fixed Gersten exactness in the coefficient range Z[1/30], the one-coordinate theta norm, and regularity of the comparison of moving primitives. The accepted PASS 3 proof supplies the unit-stabilizer transfer calculation for arbitrary proper M. This argument remains over Z_p, p>=7; it does not assume the separate PASS 4 R-descent or all-prime geometric work. The complete proof includes GEOMETRIC_CENTRAL_TRANSPORT_DETAIL.md and CONVENTION_AND_PRINCIPAL_RECOVERY.md in this directory. The former keeps the good-level coefficient factors upstairs; the latter verifies the exact central double coset and recovers the prior principal formula, including its marking factor.

We record explicitly the comparison needed below. Suppose X and X' are two products of O-CM curves over a common field, u:X->X' is an O-linear isomorphism, and u sends a marked primitive orbit to the marked primitive orbit. Choose moved axis primitives W and W' supported away from their respective orbits, each with boundary Nc^2(0)-X[c]. Then

    u^*W'-W

has zero boundary, is trace-fixed, and has support away from the first orbit. Exactness gives its unique trace-fixed K2 primitive b. Since all the residues of b avoid that orbit, b is regular on an open containing it. The two normalized cocycles differ by the coboundary of b. On the strict subgroup fixing the point, evaluation of this coboundary is zero. Consequently the specialized homomorphisms are transported exactly.

This is a statement about the **specialized homomorphism**, not literal equality of independently chosen axis primitives. For a factorwise isomorphism with the shear transported, the axis primitives themselves agree, by the one-curve theta normalization. The main norm argument below uses this factorwise case.

For later use at a good lower level, an orbit-preserving Steinitz isomorphism exists whenever the two rank-two projective lattices have the same determinant class. Start with a lattice isomorphism. Modulo A it carries the distinguished primitive vector to another primitive vector. SL_2(O/A) acts transitively on primitive vectors (A has semilocal finite quotient), and its required correction lifts to the determinant-one lattice group by strong approximation. Composing gives an isomorphism fixing the distinguished vector modulo A. Only its lower row is prescribed; no impossible prescription of the determinant modulo A is made. The preceding regular-coboundary argument justifies its use on specialized homomorphisms.

## 3. A CM reciprocity lift, not an Artin symbol at a bad ideal

Choose an admissible definition prime f, coprime to N, c and all class representatives, such that b_f=|(O/f)^times| is prime to p. As in PASS 3, take a rational l>3 congruent to 2 modulo p outside the finite excluded set and a prime f above l. Its residue degree is 1 or 2, so b_f is 1 or 3 modulo p.

Write K_A=F(Af). Use the source CM models E_r over F(f), their Hom identifications, and strict row-lattice groups. Since q does not divide f, CM reciprocity supplies a compatible system of F(f)-isogenies

    phi_r:E_r -> E_r^sigma,   ker(phi_r)=E_r[q],          (3.1)

for a single sigma in Gal(F^ab/F) lifting the Frobenius at q on extensions unramified at q. One may choose sigma using a local uniformizer and global idelic reciprocity. The CM isogeny agrees with sigma on prime-to-q torsion. This is the CM isogeny input used in source Lemma 4.1.7, applied to q. The construction only requires a lift; it does not attach an ideal Artin symbol to q at a q-divisible modulus.

Naturality is exact: for every O-linear map t:E_r->E_s,

    t^sigma phi_r = phi_s t.                            (3.2)

Both sides agree on all torsion of order prime to q, hence they agree as morphisms. This proves naturality without selecting incompatible scalar generators.

The restriction of sigma to K_M is the ordinary Artin element R_{Mf}(q), because q is prime to Mf. At K_A with q|A it is just the restriction of the chosen lift. Such a restriction is an actual automorphism, and commutes with all restriction and corestriction maps in this abelian tower.

Choose P_M on E_1 of exact M-order, and choose P_{Mq^j} recursively so that

    phi_1(P_{Aq})=sigma(P_A).                           (3.3)

At the first step, the unique A-torsion point in the fiber is P_A itself: phi_1 agrees with sigma on A-torsion. The other Q-1 points have exact Aq-order. At higher steps all Q fiber points have exact Aq-order. Thus primitive choices in (3.3) exist. Every such point is defined over K_{Aq} by the source's torsion construction.

These markings need not coincide with the source's initially chosen markings. Section 7 proves the comparison and eliminates this apparent change of map.

## 4. Standard-component assembly by factorwise Galois transport

Fix a standard source component r. Let s be characterized by

    [a_s]=[a_r q].                                      (4.1)

The curve E_r^{sigma^{-1}} has this CM class. Choose an F(f)-isomorphism

    iota_r:E_s -> E_r^{sigma^{-1}}.

It exists over F(f): the CM q-isogeny and the source isogenies make the curves F(f)-isogenous, and source Lemma 3.1.1 then makes every isogeny, including an isomorphism, F(f)-defined. Define the q-isogeny

    b_r=phi_r^{sigma^{-1}} iota_r:E_s -> E_r,
    beta_r=diag(b_r,1):E_s x E_1 -> E_r x E_1.           (4.2)

In the source's row-lattice coordinates, b_r is a generator eta_r of q a_r a_s^{-1}. Thus beta_r is exactly a first-coordinate q-isogeny representative; beta_r^{-1} represents the inverse-U correspondence from standard r to standard s.

Apply id x phi_1 to E_r x E_1. Its target is E_r x E_1^sigma. Applying sigma^{-1} to that target gives E_r^{sigma^{-1}} x E_1, which is identified **factorwise** with E_s x E_1 using iota_r. No mixed Steinitz map is needed here.

The induced group degeneracy is

    D_r(gamma)=beta_r gamma beta_r^{-1}.                (4.3)

To check (4.3), use (3.2) for all four matrix entries. If A_r:E_r x E_1 -> (E_s x E_1)^sigma denotes id x phi_1 followed by the factorwise first-coordinate isomorphism, then

    beta_r A_r=Phi_s,   A_r beta_r^sigma=Phi_r,

where Phi_j=diag(phi_j,phi_1). The equality gamma Phi_r=Phi_r gamma^sigma implies

    (A_r^{-1} gamma A_r)^{sigma^{-1}}
        = beta_r gamma beta_r^{-1},

after the stated factorwise identifications. This is precisely (4.3).

The row entries transform as upper-right b -> eta_r b and lower-left c -> c/eta_r. Since eta_r a_s=q a_r, the latter belongs to A a_s whenever c belongs to Aq a_r. Thus D_r carries the strict group at Aq on r to the strict group at A on s. The determinant-class shift is the true inverse shift (4.1), not the shift of the integral opposite local matrix.

Changing iota_r multiplies b_r by a global unit. This is absorbed by a first-coordinate unit in the strict level group, and does not change the homology correspondence or the specialized homomorphism.

## 5. Supported norm identity on the assembled tuple

For every proper A define the geometric specialized homomorphism

    g_{c,A,r}:Gamma^s_{A,r} -> K_2(K_A) tensor Z_p

using P_A and the actual normalized cocycle. No arithmetic descent at a nonadmissible A is asserted.

The one-coordinate norm gives

    (id x phi_1)_* v_{c,(r,1)}=v_{c,(r,1^sigma)}.        (5.1)

The second theta factor on the right is sigma(c theta_1). After the factorwise transport of Section 4, the whole right primitive is sigma of the low standard primitive. This is literal product-model compatibility, justified by theta uniqueness and the norm of a prime-to-c isogeny.

Choose a low moving map x:E_1^sigma->E_r whose value at sigma(P_A) is nonzero, and use x phi_1 at the high level. Such an x may be chosen in c Hom(E_1^sigma,E_r), prime to A. The shears satisfy the same Cartesian identity as in PASS 2. At every fiber point R,

    (x phi_1)(R)=x sigma(P_A) != 0.

Also R is not c-torsion. Thus both moved primitives and the needed translates avoid the full fiber. Trace-fixed Gersten injectivity gives equality of the generic cocycles; regular primitive comparison identifies them with the actual specialized homomorphisms. The argument uses A proper, never a theta value at the origin.

Because Af is admissible, the relative marked fiber over K_A is a single primitive orbit of size Q if q|A, and a primitive orbit of size Q-1 together with P_A if q does not divide A. Proper base change, (4.3), and (5.1) therefore give the **assembled standard-tuple** identities

    Cor_{K_{Aq}/K_A} g_{c,Aq}
        = sigma g_{c,A} D,                     q|A,    (5.2)

    Cor_{K_{Aq}/K_A} g_{c,Aq}
        = sigma g_{c,A} D - g_{c,A} F,          q∤A.    (5.3)

Here F is the forgetful degeneracy, and D includes its component permutation. The sigma in (5.2) is a genuine chosen Galois automorphism, not an undefined R_A(q). In (5.3), sigma|K_A=R_{Af}(q). The missing point in (5.3) is P_A, so its term has no additional Artin factor under these recursive markings.

## 6. Exact dual correspondence identities and cancellation

The following standard unnormalized degeneracy identities are identities of tuples, not separate endomorphisms of one fixed component:

    F U^vee_{q,Aq}=Q D,                                  (6.1)
    D U^vee_{q,Aq}=U^vee_{q,A} D,                q|A,     (6.2)
    D U^vee_{q,Aq}=T^vee_{q,A}D-Z_q^{-1}F,       q∤A.    (6.3)

In (6.3), Z_q is the central adelic correspondence of nu I_2 at the q-free level. Its inverse, not the identity, is the omitted branch.

For (6.1), write g_r=beta_r^{-1}. Representatives are g_r k_t, with k_t lower unipotents in the low group on s and lower entries running through A a_s/q A a_s. If gamma g_r k_t=g_r k_{s(t)}tau_t, then

    tau_t=k_{s(t)}^{-1}D_r(gamma)k_t.

Summing an arbitrary low homomorphism cancels the two k-sums and gives Q times its value at D_r(gamma). This proves (6.1), including the index and component convention.

For (6.2), conjugating the Q representatives gives the Q lower-level representatives; the matrices beta_r and beta_s compose in the required component order. Locally at q this is the same diagonal conjugation as in PASS 2. Away from q they are lattice isomorphisms. Thus the identity is global, without identifying different determinant classes.

For (6.3), the conjugated Q branches comprise all but the last branch of the good inverse double coset. In a local q-basis the omitted branch is diag(1,nu^{-1}); combining it with the degeneracy gives central diag(nu^{-1},nu^{-1}). Hence the omitted correspondence is Z_q^{-1}F. Strong approximation and the determinant-class rule identify these local double cosets with the global ones. Their target class is [a_r q^2], agreeing on both sides. This also explains the central factor that a same-component scalar calculation conceals.

At the proper q-free level A, the source's good geometric Hecke identity and its CM/central compatibility give

    g_{c,A} Z_q = sigma g_{c,A},
    g_{c,A} T^vee_{q,A}=(1+Q sigma^{-1})g_{c,A}.          (6.4)

These identities remain geometric over K_A when A is nonadmissible. GEOMETRIC_CENTRAL_TRANSPORT_DETAIL.md gives the explicit kappa-factor calculation, and CONVENTION_AND_PRINCIPAL_RECOVERY.md Section 1 identifies the assembled map with the exact adelic central coset. Here are the necessary checks. Simultaneous q-isogenies commute with every matrix by (3.2), carry the primitive A-orbit to its sigma-conjugate, and norm the moved product primitive to its sigma-conjugate. They therefore give central transport by sigma on the specialized homomorphism. Replacing a resulting product by a standard determinant-class component can be done by an orbit-preserving lattice isomorphism as in Section 2; the comparison coboundary is regular and evaluates to zero. The diamond step here is **weighted geometric cohomology invariance**, not an assertion that a constant-coefficient diamond has eigenvalue 1. If the comparison diamond delta has lower-right entry lambda, its specialization contributes kappa_delta=R_{Af}((lambda')) with lambda'=lambda modulo A and 1 modulo f. Choose delta with the same lower-right residue as the diagonal representative rho of [q]^*. The constant-coefficient correspondence of delta therefore carries the inverse factor kappa_delta^{-1}; it is not discarded. In the source factorization Z_q=(<q>*)^{-1}[q]^*, the composed matrix delta^{-1}rho has lower-right entry 1 modulo A, so its two coefficient factors cancel. The determinant class and local elementary divisors then identify this exact composed correspondence with Z_q. The Q+1 good cosets preserve the primitive A-orbit, so the source's geometric Hecke equality holds in the orbit-regular subcomplex, just as in Remark 3.4.2. This proves the first equality and the ordinary good eigenvalue Q+sigma. Finally the exact good-coset identity T^vee=Z_q^{-1}T_q proves the second equality. No invariants-equal-descent argument at A is used. Equivalently, when A is admissible these are the source's Section 5.1 identities; the preceding argument isolates why admissibility is unnecessary before descent.

At A=M put C=sigma g_{c,M}D-g_{c,M}F. By (6.1), (6.3), and (6.4),

    C U^vee
      = sigma(1+Q sigma^{-1})gD - sigma sigma^{-1}gF - QgD
      = sigma gD-gF
      = C.                                               (6.5)

Equation (5.3) proves norm-zero at the first step. At higher steps (5.2) and (6.2) give

    Cor_{K_{Aq}/K_A}[g_{c,Aq}(U^vee-1)]
       = sigma [g_{c,A}(U^vee-1)]D.                       (6.6)

Galois automorphisms commute with corestriction in this abelian tower. Iterating (6.6) and then (6.5) gives

    Cor_{K_N/K_M} g_{c,N}(U^vee-1)=0.                    (6.7)

No degree Q or p-power has been cancelled.

## 7. Original markings, local choices, and descent

Any two primitive N-points on E_1 differ by a unique element of (O/N)^times. Choose d in O with that residue and d=1 modulo f. Source Lemma 3.1.4 and Proposition 4.1.2 give

    g_{c,N}^{new}=R_{Nf}((d)) g_{c,N}^{source}.            (7.1)

This is a target automorphism. It commutes with precomposition by the constant-coefficient U^vee. Its restriction to K_M also commutes with the norm, so (6.7) holds for one marking if and only if it holds for the other. Thus it holds for the actual source marking; no rescaled high-level map is substituted in Theorem A. CONVENTION_AND_PRINCIPAL_RECOVERY.md Sections 2-3 explicitly compare local and rational inverse cosets at every tame level prime and show that, at the principal first step, the new high marking is a target Artin translate restricting to R_A((pi)); undoing it recovers precisely the accepted formula g_A D-kappa_A^{-1}g_A F.

A different local uniformizer changes the reciprocity lift sigma by an inertia element at q. It leaves the inverse-U double coset unchanged, as noted in Section 1. It can change the recursive q-primary markings. Equation (7.1) again removes that change, and inertia is trivial at the q-free K_M. The final norm-zero identity is therefore independent of the lift and the marking choices. This is why it was important not to label sigma at high level as an ideal Artin element.

At admissible N, the actual arithmetic source map satisfies

    g_{c,N}^{source}=res_{L_N}^{K_N} f_{c,N}.             (7.2)

The restriction degree b_f is prime to p. With V=U_M, the exact relative ray group is

    Gal(K_N/L_M)=((O/q^n)^times x (O/f)^times)/diag(V).

As proved independently in PASS 3, the projections of V to both factors are injective, and

    L_N intersect K_M=L_M,
    [K_N:L_N K_M]=u_M,
    [K_M:L_M]=b_f/u_M.

The norm/restriction identity is therefore

    Cor_{K_N/K_M} res_{L_N}^{K_N}(z)
        =u_M res_{L_M}^{K_M} Cor_{L_N/L_M}(z).            (7.3)

This argument never required q principal. Both u_M and b_f/u_M are p-adic units. Applying (7.3) to the actual defect and using (6.7)-(7.2) proves Theorem A.

If p∤d and chi is inflated from L_M, the entire relative group acts trivially on its chi-component. Thus res Cor is multiplication by the p-adic unit d on that component. Applying Theorem A proves Theorem B. Auxiliary cancellation is used only at the high admissible level and only where the source proves a smoothing factor invertible. These are exactly the accepted PASS 2/3 cancellation conditions.

## 8. What this does not settle

1. For M=O, the marked lower point is the origin. The support argument does not apply; pure prime-power levels remain open.
2. A nontrivial relative prime-to-p character can lie entirely in the norm kernel. No new equation on those character components follows.
3. At wild depth q|p, n>=2, the relative degree has a p-factor. No cancellation of that factor is claimed.
4. No 5-primary arithmetic construction, nonadmissible high-level map, unrestricted compactification, new integer-ring integrality, or genuine relative theta-symbol prescription is constructed.
5. The integral opposite local operator in (1.3) is not asserted to have eigenvalue 1. Its central factor must be retained. The proved operator is the true inverse correspondence, explicitly compatible with the principal convention already accepted.

## 9. Source and verification boundary

Public primary sources: Lecouturier, Sharifi, Shih and Wang, *Eisenstein cocycles for imaginary quadratic fields*, arXiv:2504.19125v1, https://arxiv.org/pdf/2504.19125v1 ; distinct author-hosted manuscript, https://www.math.ucla.edu/~sharifi/publ/imagquad.pdf . Sections 2.1-2.4, 3.1-3.4, 4.1, 5.1 and Remark 5.2.10 were inspected in the retained author manuscript. Its different bytes are not a claim that it is arXiv v2.

Accepted local inputs: PASS 2 bad-prime proof SHA256 7af38b596ee39ad4447a63eac17ea4c28e0c07177021e4f15277c2b2d5e29e5a; PASS 3 lower-level extension SHA256 88f9e52d3119a446038789c8352d801e2387d78dd8611ea2a2f326fbe72b5d53, with their independent acceptance reports.

The new content requiring independent review is the semilinear standard-component assembly, its inverse-double-coset identification, the low geometric central transport without lower admissibility, and the marking/lift comparison. This draft is not an acceptance report.
