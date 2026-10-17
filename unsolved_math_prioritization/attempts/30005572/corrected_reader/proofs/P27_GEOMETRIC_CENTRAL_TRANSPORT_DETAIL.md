# Detail: good lower central transport before arithmetic descent

Shared PASS 4, supplement to NONPRINCIPAL_DUAL_BAD_U.md Section 6. This supplies an explicit version of the cancellation implicit in the source's Lemmas 4.1.7-4.1.8. Work over K_A=F(Af), with A proper, q prime to Afc; A need not have injective unit reduction. All equalities of cocycles below may first be taken as equalities of classes in the marked-orbit-regular complex, and then restricted to the strict stabilizer, where regular coboundaries evaluate to zero.

Let i=(i_1,i_2), j=(j_1,j_2) satisfy that q a_{i_u,j_u}=(eta_u), u=1,2. Put rho=diag(eta_1,eta_2):E_i->E_j. The simultaneous q-isogeny Phi_i:E_i->E_i^sigma factors rho=psi Phi_i through a factorwise isomorphism psi, where sigma=R_{Af}(q). Norm of the product theta primitive and the compatible moved shears give

    rho_* C_i = C_j,
    (Phi_i)_* C_i = sigma C_i,                            (D1)

with the group arguments conjugated by the indicated matrices. The second right side lives on the Galois-conjugate model; it is not being confused with a cocycle on the original model.

Choose eta_2' congruent to eta_2 modulo A and to 1 modulo f, and put kappa=R_{Af}((eta_2')). By the source marking rule and its principal Artin rule,

    rho(lambda_i)=psi sigma(lambda_i)=kappa(lambda_j).   (D2)

Here the fractional eta_2 is a unit at A. An integral CRT representative eta_2' exists. Its congruence to 1 modulo f ensures that kappa fixes the definition field, so it acts on the specialization while leaving the generic classes unchanged.

Evaluating (D1) through (D2) gives the exact **upstairs** relation

    lambda_j^* rho_* C_i
       = kappa^{-1} sigma lambda_i^* C_i.               (D3)

On the other hand, pullback through rho gives

    lambda_i^* rho^* = kappa lambda_j^*.                (D4)

Combining (D3)-(D4) and the first equality in (D1) proves that the geometric scalar-ideal pullback operator [q]^* on the h^2 tuple specializes to sigma. The kappa factors cancel at K_A. There is no need to replace kappa by an Artin element at A by assuming descent, and no need to identify Galois invariants with a descended group.

The passage from the h^2 tuple to the usual central operator on the h standard components is the source factorization

    Z_q = <q> [q]^*,

with the component indices as in Lemma 2.3.8(a) and Proposition 5.1.2. The diamond factor is induced by an O-linear isomorphism of the products. Its invariance is an assertion about **weighted geometric cohomology** in the orbit-regular subcomplex: transport one moved primitive, compare with the independently chosen one, and use the regular coboundary from Section 2 of the main note. It is not constant-coefficient diamond invariance. Write delta for the representative of <q>* in the source factorization [q]^*=<q>* Z_q, and choose its lower-right residue lambda to equal the lower-right residue eta_2 of rho, as in Lemma 2.3.8(a). Specialization of delta contributes kappa_delta=R_{Af}((lambda')), where lambda'=lambda modulo A and 1 modulo f. Thus weighted invariance reads kappa_delta times the constant-coefficient transfer equals the unchanged specialized class; the constant-coefficient operator alone contributes kappa_delta^{-1}. In Z_q=(<q>*)^{-1}[q]^*, the composed matrix delta^{-1}rho has lower-right residue 1. Its coefficient factor is kappa_delta^{-1}kappa=1. Accordingly the weighted geometric eigenvalue sigma obtained above is exactly the constant-coefficient eigenvalue of Z_q, without a leftover diamond factor. The local elementary-divisor and marking verification in Section 1 of CONVENTION_AND_PRINCIPAL_RECOVERY.md identifies this composed matrix with the fixed central adelic coset, not merely some operator with the same determinant class. Consequently

    g_{c,A} Z_q = sigma g_{c,A}.                         (D5)

The determinant-one strong approximation and marked-isomorphism arguments do not require injective unit reduction at A. Unit-injectivity was used in the source's arithmetic descent, which is not used here. This proves the first equality of (6.4) in the main note with all coefficient factors kept upstairs.

The other good identity follows from the geometric Hecke class equality in the orbit-regular complex, whose Q+1 branches remain good at A, followed by exactly this marked transport. Thus g T_q=(Q+sigma)g. The equality of inverse and central-twisted good double cosets gives

    T_q^vee=Z_q^{-1}T_q,
    g T_q^vee=(1+Q sigma^{-1})g.

This supplement only concerns q prime to A. It defines no ideal Artin action for q at a modulus divisible by q.
