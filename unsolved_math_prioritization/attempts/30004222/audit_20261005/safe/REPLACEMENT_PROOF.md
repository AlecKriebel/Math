# Corrected source bridge and normalization argument

Problem 30004222 / OWR-17135-015, rank 718. Independent mathematical replacement for the normalization-dependent portions of the frozen dossier. This text does not alter the frozen dossier and makes no novelty claim.

## Statement and conventions

Fix n >= 2 and a dominant integral gl_n weight lambda=(lambda_1,...,lambda_n). Let mu be a 0-1 vector with k ones, 0<k<n, and assume lambda+mu is dominant. Define

- I(mu) = {(a,b): a<b, mu_a=0, mu_b=1};
- d_ab = lambda_a-lambda_b+b-a;
- [m] = q^(m-1)+q^(m-3)+...+q^(1-m), for m>=1;
- K(lambda,mu) = product over I(mu) of [d_ab]/[d_ab-1].

The identity under discussion is that the preferred light-ladder local intersection scalar kappa equals K. It concerns the fixed, linear reflection pairing and the diagrammatic normalization used by Elias. It is first an identity over Q(q), with regular characteristic-zero q=1 specialization. It does not assert the existence of all clasps at roots of unity or in positive characteristic.

Martin and Spencer's Theorem 5.11 in *Cell modules for type A webs* is the published all-rank type-A prior result. However, its displayed normalization notation is internally inconsistent. The correct relation for the multiplicative normalizer N' defined in their Eq. (5.15) is

    kappa = (N')^(-2), not (N')^2.

The proof below isolates and repairs that step explicitly. It relies on identified representation-theoretic results of their paper; it does not pretend to reprove quantum skew Howe duality or the lowering-operator basis theorem.

## 1. Original root statement and domain

Take positive roots alpha_ab=e_a-e_b for a<b and rho_a-rho_b=b-a. Then

    <lambda+rho,alpha_ab> = d_ab,
    <lambda+rho+mu,alpha_ab> = d_ab+mu_a-mu_b.

The denominator is exactly one less than the numerator precisely for I(mu). This is the criterion in Elias's 2019 Oberwolfach contribution, pp. 2428-2429. It avoids any ambiguity concerning the direction of the permutation w_mu. It also agrees with Elias's original Claims 3.14-3.15 and Conjecture 3.16 in *Light ladders and clasp conjectures*.

Because lambda is dominant integral, d_ab >= b-a. Equality d_ab=1 can occur only when b=a+1 and lambda_a=lambda_b. If that pair belongs to I(mu), lambda+mu is not dominant. Conversely any adjacent failure of dominance of lambda+mu must have lambda_a=lambda_(a+1), mu_a=0, and mu_(a+1)=1, producing denominator zero. Thus admissibility is exactly what rules out these zero integers, and all denominator indices for admissible data are positive.

The finite Laurent sum gives [m] at q=1 equal to m. Consequently K specializes regularly to the classical product d_ab/(d_ab-1) in the 2019 question. Adding c to all lambda_i preserves all d_ab. Dominant integral gl_n weights with negative last entry can therefore be reduced to partitions by a determinant twist while preserving the specified type-A scalar convention. Type A_(n-1) corresponds to gl_n/sl_n here; there is no rank cutoff. No even/odd restriction on n or on a dominant integral gl_n weight is introduced.

The sign in the preliminary sl_2 Temperley-Lieb example of the 2019 report is not a counterexample: the report itself distinguishes that cap/cup convention from the positive gl_2 normalization of its final conjecture. The current claim uses the latter. Nor should q be replaced by -q silently: each selected-root ratio changes sign, so K(-q)=(-1)^(|I(mu)|)K(q).

## 2. Horizontal-strip product, independently proved

Let sigma subset tau be partitions with tau/sigma a horizontal strip. Pad both to s rows with sigma_s=0 and tau_(s+1)=0. Such a padding is always possible; adding a final zero row suffices. Let N_i=tau_i-sigma_i, c_ik=tau_i-tau_k+k-i, alpha=sigma^t and beta=tau^t. Pad alpha and beta to width tau_1 and put mu=beta-alpha. This mu is 0-1 and both alpha and beta are dominant.

For each new box in row i and column b, sigma_i<b<=tau_i and its old column height is i-1. An unchanged column a<b has height h in both shapes. Its factor in K(alpha,mu) is

    [h-i+b-a+1]/[h-i+b-a].

Multiplying over all new columns b in row i telescopes to

    [h-i+tau_i-a+1]/[h-i+sigma_i-a+1].

Every unchanged column to the left is accounted for exactly once. Group such columns by h=k-1. Their indices are tau_k<a<=sigma_(k-1), where k>i. On substituting a=tau_k+ell, their product is

    P_i = product_(k=i+1..s) product_(ell=1..sigma_(k-1)-tau_k)
          [c_ik-ell]/[c_ik-N_i-ell].

Thus K(alpha,mu)=product_i P_i. The potential k=s+1 group is empty because sigma_s=0. If one instead stops padding at r rows with sigma_r>0, a k=r+1 group MUST be included. This is precisely the bottom-row correction already present in the frozen dossier. All numerator and denominator indices are positive by the preceding root-domain argument; alternatively, interlacing tau_i>=sigma_i>=tau_(i+1) verifies this directly.

For i=s, P_s is empty. For N_i=0, P_i=1. These cases require no division by a zero quantum integer.

## 3. A clean, fixed-step lowering norm identity

For x>=d>=0 write H(x,d)=product_(h=0..d-1)[x-h], with H(x,0)=1. Then the symmetric quantum binomial is

    Cq(x,d)=H(x,d)/[d]!.

For each i<s define

    B_i = product_(k=i+1..s) Cq(c_ik-1,N_i)
          / product_(k=i+1..s-1) Cq(c_ik+N_k,N_i),
    B = product_(i=1..s-1) B_i.

These binomials are defined: N_i<=tau_i-tau_(i+1), so c_ik-1>=N_i for k>i, and c_ik+N_k>=N_i.

We now prove B=K without using the desired intersection formula. In the kth factor of P_i set

    x=c_ik-1,
    L=sigma_(k-1)-tau_k.

Interlacing gives L>=0 and x-L=c_(i,k-1)+N_(k-1)>=N_i, including the case k=i+1 where this equals N_i. Factorial cancellation therefore gives the exact rational identity

    H(x,L)/H(x-N_i,L) = H(x,N_i)/H(x-L,N_i).

Consequently

    P_i = product_(k=i+1..s)
          H(c_ik-1,N_i)/H(c_(i,k-1)+N_(k-1),N_i).

For k=i+1 the denominator is H(N_i,N_i)=[N_i]!. Reindexing the remaining denominators yields

    P_i = H(c_(i,s)-1,N_i)/[N_i]!
          * product_(k=i+1..s-1)
            H(c_ik-1,N_i)/H(c_ik+N_k,N_i)
        = B_i.

Multiplication over i proves B=K. This argument establishes an unrestricted algebraic identity of the displayed products, not merely a numerical check.

Now apply Martin-Spencer Eq. (5.15) at the single final step j=s. In their notation M^s_ik=0 and M^(s-1)_ik=N_k-N_i. Its displayed quotient inside the braces is exactly B, and its exponent is -1/2. Hence

    N'(T';T)=B^(-1/2), and (N'(T';T))^(-2)=B=K.

There is no product over earlier steps j<s here and no need to invoke the problematic all-j expression in Eq. (5.38). Square roots can be interpreted in a field extension for the orthonormal basis; the identity B=K and the resulting intersection scalar lie in Q(q).

## 4. Why B is the intersection scalar, without circularity

The representation-theoretic inputs are as follows.

1. Section 5, Theorem 5.1: quantum skew Howe duality identifies the relevant endomorphism spaces with images of U_q(gl_m). The algebra generators are normalized as in Cautis-Kamnitzer-Morrison.
2. Section 5.1, Eq. (5.4): the contravariant form on the lowering-operator side agrees with the cellular reflection form on the web side. This prevents an unrecorded scalar multiple between the two pairings.
3. Lemma 5.4: the extremal projector maps to the clasp, using the independently characterized leading identity coefficient and annihilation properties. This does not require the conjectured numerical value of kappa.
4. Section 5.4, the comparison following Eqs. (5.14)-(5.16), with Eqs. (5.17)-(5.22): the projector times the product of divided powers maps to the prescribed clasped light-ladder step with coefficient one. Using ordinary powers would introduce factorials and would not support this conclusion.
5. Lemma 5.7: multiplying those unnormalized lowering steps by N' gives an orthonormal basis. This is the external lowering-operator norm theorem, attributed there to Tolstoy and Quesne.
6. Section 4, Eq. (4.4): adjoining a clasped step multiplies the norm by the actual local intersection scalar kappa. This follows from composition and the definition of kappa, not its conjectured root product.

Use a path of tableaux and normalize its parent vector to norm one. Inputs 2-4 identify the unnormalized next step with the web step, and input 6 says its squared norm is kappa. By input 5 the next vector multiplied by N' has norm one. The reflection/contravariant form is scalar-linear, so

    1 = (N')^2 kappa.

Therefore kappa=(N')^(-2)=B, and Section 3 proves B=K independently. Equivalently, compare norms along the whole tableau path: the web norm is the product of actual kappas, the normalization multiplier is the product of N's, and division by the corresponding identity for the parent path isolates the same equation. For j<s the earlier normalizers in T and T' really are identical: c_ik(tau)+M_ik^j(T)=T_i^(j)-T_k^(j)+k-i, and c_ik(tau)+M_ik^(j-1)(T)+N_(i,j)=T_i^(j)-T_k^(j-1)+k-i. Both depend only on the same two partial shapes, which T and T' share. This verifies the parent-path cancellation explicitly. The induction uses no assumed root formula at any earlier step.

The proof's coverage is not limited to special tableaux. Given a horizontal strip sigma subset tau, pad to s with sigma_s=0, fill each old row i with the entry i, and put s in all new boxes. Rows are weakly increasing and columns strictly increasing: new boxes occupy distinct columns and have no box below them, while all old entries above them are smaller than s. Thus every required strip is realized by a legal parent/child tableau. The transposed construction covers all admissible vertical strips of the original exterior-power problem.

This repairs the normalization step of the published argument while explicitly retaining its stated representation-theoretic dependencies. It is neither a standalone elementary proof of those dependencies nor a newly claimed purely combinatorial solution.

## 5. Exact small counterexample to the frozen normalization sentence

Take T=[1,2] and T'=[1]. Then s=2, tau=(2,0), sigma=(1,0), N_1=1 and c_12=3. The fixed-step quotient B is Cq(2,1)=[2]. The web data are lambda=(1,0), mu=(0,1), lambda+mu=(1,1), so K=[2]. This scalar is also the elementary split-merge coefficient Cq(2,1), and on the lowering side it is the norm of fv in the highest-weight-two U_q(sl_2) representation: <fv,fv>=<v,efv>=[2] for unit v.

Eq. (5.15) gives (N')^2=1/[2]. At q=1, kappa=2 and (N')^2=1/2; at q=2, kappa=5/2 and (N')^2=2/5. Thus neither a choice of square-root sign nor a matter of typography in extracted text resolves the discrepancy.

For the additional all-j issue, T=[1,2,3], T'=[1,2] has terminal B=3 at q=1 but product of all step B's equal to 6. A single-step formula cannot retain that all-j product without dividing by the parent's product.

## 6. Necessary replacement language

Replace any assertion that Lemma 5.10's literal (N')^2 is kappa with:

The fixed-step multiplicative normalizer of Eq. (5.15) satisfies (N')^(-2)=kappa. Its inverse square is the unnormalized squared norm B. Direct q-factorial cancellation gives B equal to the selected-root product. Printed Lemma 5.10 and Eq. (5.38) use an inconsistent normalization label; their desired root product is recovered by the explicit fixed-step calculation above. The theorem application additionally uses form compatibility, extremal-projector/clasp identification, the divided-power/light-ladder comparison, and the independent orthonormal-basis theorem.

For the partition restatement use old weight alpha, new weight beta, beta-alpha 0-1:

    kappa_alpha^beta = product_(a<b, beta_a=alpha_a, beta_b=alpha_b+1)
                      [alpha_a-alpha_b+b-a]/[alpha_a-alpha_b+b-a-1].

Both the inclusion condition and the old-shape axial distance matter. Changing only the impossible priming condition in printed Eq. (2.15) is insufficient.

## Sources and extent

- Original 2019 question: https://doi.org/10.4171/owr/2019/39 ; report PDF https://ems.press/content/serial-article-files/46818?nt=1
- Elias's original definitions, Claims 3.14-3.15 and Conjecture 3.16: https://arxiv.org/abs/1510.06840
- Martin-Spencer published paper: https://link.springer.com/article/10.1007/s00209-026-03990-0 ; inspected PDF https://link.springer.com/content/pdf/10.1007/s00209-026-03990-0.pdf
- Inspected matching preprint: https://arxiv.org/abs/2210.09639v4

This replacement independently proves the elementary product identities and fixes the normalization inference. The cited foundational representation-theoretic inputs were inspected at their use in Martin-Spencer, but their original sources and every diagrammatic reduction were not independently reproved. The result remains a qualified prior-formula attribution, with explicit representation-theoretic dependencies; it does not certify every interpretation of the request for a combinatorial explanation.
