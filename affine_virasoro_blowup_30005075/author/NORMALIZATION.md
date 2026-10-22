# Repaired normalization for affine–Virasoro sewing

## Status and scope

This note proves an algebraic normalization statement **conditional on the published generic-parameter coset block relation**, Bershtein–Feigin–Trufanov (BFT), Eq. (4.59). It repairs two inconsistent printed formulas in BFT Appendix B and explains the reciprocal-parameter issue in the original Oberwolfach question. This is not a claim of a new blowup theorem. The physical AGT identification and the match to an independently specified gauge-theory normalization are not reproved here.

The original target is Teschner, OWR 16/2022, p. 837, Eq. (2):

\[
\Psi(a,m;w,z;\epsilon_1,\epsilon_2)
=\sum_{j\in\mathbb Z}\Psi(a+\epsilon_1j,m;w,z;\epsilon_1,\epsilon_2-\epsilon_1)
 Z(a+\epsilon_2j,m;z;\epsilon_1-\epsilon_2,\epsilon_2).
\tag{T}
\]

Here \(\Psi\) includes a surface operator. The corpus clean statement omits that detail. A coefficient-free identity requires full rather than unit-leading instanton-only normalization. We distinguish (T) from a defect-free identity and from an analytic identity at every singular specialization.

## 1. Consistent coset conventions

Set \(K=k+2\), and choose
\[
 b^2=-\frac K{K+1},\qquad
 P(\lambda)=-\frac{\lambda+1}{2K}b,\qquad Q=b+b^{-1}.
\]
Then \(Q=-b/K\), \(P(\lambda)=(\lambda+1)Q/2\). The generic coset decomposition uses pairs
\[
 (\lambda+2j,k+1),\qquad (P(\lambda)+jb,b).
\]
For affine Sugawara weight \(H(\lambda,K)=\lambda(\lambda+2)/(4K)\) and Virasoro weight \(\Delta(P)=Q^2/4-P^2\), direct algebra gives
\[
 H(\lambda+2j,K+1)-H(\lambda,K+1)
 +\Delta(P+jb)-\Delta(P)=j^2.\tag{1}
\]
Thus the summand begins at integral total grade \(j^2\).

The source report instead sets \(b_T=i\sqrt{(K+1)/K}\), the reciprocal of the BFT branch \(b=-i\sqrt{K/(K+1)}\). Its printed \(P_T=-P\) is harmless in isolation because conformal weights depend on \(P^2\), but its simultaneous printed shift \(P_T+jb_T\) is not the coset shift. With that literal choice, the grade in (1), minus \(j^2\), is
\[
 \frac{j\big((2K+1)j-\lambda-1\big)}{K(K+1)},\tag{2}
\]
which is generically nonzero and nonintegral. With the printed \(P_T\), the compatible shift is \(P_T-j/b_T\). The report also prints \(Q=1/(i\sqrt{K(K+1)})\), opposite to \(b_T+b_T^{-1}\) on the displayed positive square-root branch; only its square enters the weights. These are source-convention inconsistencies, not counterexamples to (T).

## 2. Rational characters and the local repair

Use independent multiplicative variables \(p,q,u_1,u_2,u_3\), and write
\[
 A=u_1u_2u_3-u_2^2-u_3^2,\quad
 B=\frac{u_1}{u_2u_3}+\frac{u_2}{u_1u_3}+\frac{u_3}{u_1u_2}-u_1^{-2}.
\]
Define
\[
 S(u;p,q)=\frac{p^2q A+B}{(1-p)(1-q)},\qquad
 V(u;p,q)=\frac{p^2q^2 A+B}{(1-p)(1-q)}.\tag{3}
\]
The normalization factors are \(C_S=\mathsf E[S]\), \(C_V=\mathsf E[V]\), with a common multiplicative regularization satisfying
\[
 \mathsf E[f+g]=\mathsf E[f]\mathsf E[g],\qquad
 \mathsf E\left[\sum c_\xi e^{t\xi}\right]=\prod\xi^{-c_\xi}
\tag{4}
\]
for finite characters. One can use BFT's zeta-regularized definition (B.1), on a common domain of definition followed by compatible continuation. All ratios used below reduce to finite characters, so they need no numerical evaluation of infinite determinants. Alternatively (4) may be read as an algebraic multiplicative-character normalization; this does not assert global analytic convergence.

Equation (3) changes the affine numerator in printed BFT (B.4) from \(-u_1^2-u_2^2\) to \(-u_2^2-u_3^2\). This is an explicitly proposed repair, not an unmarked quotation. With the printed numerator, the character-level residual in (B.10) is
\[
 S_{\rm printed}(u;p,q)-S_{\rm printed}(u;p,q/p)-V(u;p/q,q)
 =-\frac{p^2q(u_1^2-u_3^2)}{(p-q)(q-1)}.\tag{5}
\]
It is not the zero rational function. This proves failure of the displayed character-splitting argument; it does not, on its own, establish every analytic interpretation of a regularized-product residual.

With the repaired numerator, the exact rational identity is
\[
 S(u;p,q)=S(u;p,q/p)+V(u;p/q,q).\tag{6}
\]
To check it, separate coefficients of \(A\) and \(B\) and put the two fractions over their common denominator. Both resulting identities have numerator zero. Thus
\[
 C_S(u;p,q)=C_S(u;p,q/p)C_V(u;p/q,q).\tag{7}
\]

## 3. Finite triangle identity, including negative shifts

For any integer \(r\), let
\[
 t_r^{e_1,e_2}(a)=
 \begin{cases}
 \prod_{i,j\ge0,\ i+j<r}(a-ie_1-je_2),&r>0,\\
 1,&r=0,\\
 \prod_{i,j>0,\ i+j\le-r}(a+ie_1+je_2),&r<0.
 \end{cases}\tag{8}
\]
Its degree is \(d(r)=r(r+1)/2\), also when \(r<0\). Set
\[
 D_1=(1-p)(1-q/p),\quad D_2=(1-p/q)(1-q),\quad
 A_r=\frac{p^r-1}{D_1}+\frac{q^r-1}{D_2}.
\]
Finite geometric sums give
\[
 A_r=\begin{cases}
 -\sum_{i,j\ge0,\ i+j<r}p^iq^j,&r>0,\\
 -\sum_{i,j>0,\ i+j\le-r}p^{-i}q^{-j},&r\le0.
 \end{cases}\tag{9}
\]
The second expression is empty for \(r=0,-1\). Also
\[
 \frac qp\frac{p^r-1}{D_1}+\frac{q^r-1}{D_2}=qA_{r-1}.\tag{10}
\]
These formulas follow directly by telescoping rows of each finite triangle; multiplying by \(D_1D_2\) provides a denominator-free verification for every integer \(r\).

Taking \(p=e^{te_1},q=e^{te_2},v=e^{ta}\), (4), (8)–(10) imply
\[
 \mathsf E[v A_r]=(-1)^{d(r)}t_r^{e_1,e_2}(-a),\qquad
 \mathsf E[vqA_{r-1}]=t_{-r}^{e_1,e_2}(a-e_1).\tag{11}
\]
The latter follows by listing the finite factors separately for \(r\ge1\) and \(r\le0\). Thus no positivity restriction on a flux is hidden.

## 4. Three-point ratio and its sign

Let \(l,n,m\in\mathbb Z\). In both factors use the same ordered flux triple \((l,n,m)\). Define
\[
 R_{l,n,m}=S(u_1p^l,u_2p^n,u_3p^m;p,q/p)-S(u;p,q/p)
 +V(u_1q^l,u_2q^n,u_3q^m;p/q,q)-V(u;p/q,q).\tag{12}
\]
The printed BFT (B.6) reverses \(l,m\) in its Virasoro factor. Equation (12) is the aligned version being proved here.

Put \(u_i=e^{ta_i}\),
\[
 r_1=l-n-m,\quad r_2=-l+n-m,\quad r_3=-l-n+m,
 \qquad \sigma=d(r_1)+d(r_2)+d(r_3)-d(-2l).
\]
Apply (11) to the seven monomials in (3). The triple monomial has total shift \(l+n+m\); the two positive-square denominator terms have shifts \(2n,2m\); the negative-square term has shift \(-2l\). This gives the exact result
\[
 \mathsf E[R_{l,n,m}]=(-1)^\sigma
 \frac{t_{-l-n-m}(a_1+a_2+a_3+e_1)
 t_{r_1}(-a_1+a_2+a_3)t_{r_2}(a_1-a_2+a_3)t_{r_3}(a_1+a_2-a_3)}
 {t_{-2l}(2a_1)t_{-2n}(2a_2+e_1)t_{-2m}(2a_3+e_1)}.\tag{13}
\]
All triangles in this equation have periods \((e_1,e_2)\).

For the coset comparison take
\[
 (e_1,e_2)=(1,-K),\quad (a_1,a_2,a_3)=(\lambda/2,\nu/2,\mu/2).
\tag{14}
\]
This ordering is incoming weight, inserted weight, outgoing weight. Scale all factors by \(-K\) and use symmetry of the triangle in its periods. The total degree is zero:
\[
 d(-l-n-m)+\sum_i d(r_i)-d(-2l)-d(-2n)-d(-2m)=0.\tag{15}
\]
Hence no scale factor remains. Writing \(\mathcal C_{m,n,l}(\mu,\nu,\lambda)\) for the normalized three-point coefficient in BFT Theorem 4.5, and \(N_l(\lambda)=\|\tilde u_l(\lambda)\|^2\) for Corollary 3.18, substitution gives
\[
 \mathsf E[R_{l,n,m}]=(-1)^{l+m}
 \frac{\mathcal C_{m,n,l}(\mu,\nu,\lambda)}{N_l(\lambda)}.\tag{16}
\]
For clarity, the incoming denominator change is exactly the norm
\[
 N_l(\lambda)=
 \frac{t_{-2l}^{1,-1/K}(-\lambda/K)}
 {t_{-2l}^{1,-1/K}(-(\lambda+1)/K)}.
\]
The sign in Theorem 4.5 is
\(S=d(l-m+n)+4n(m-n)(m-n-1/2)\).
The difference \(\sigma-S-l-m\) equals
\[
 -l(l+1)+m(m-1)-n(n+1)-2ln-4m^2n+8mn^2+2mn-4n^3,
\]
an even integer. This proves the sign assertion for all integer triples, rather than only the tested examples.

## 5. Four-point sewing

Let \(\Psi_k\) and \(F_b\) have the block conventions of BFT Eq. (4.59), choosing the unshifted highest-vector trilinear constants to be one. Thus \(\mathcal C\) denotes the three-point ratios in Theorem 4.5, consistently with unit-leading block normalization. Define each full prefactor by the two ordered triples
\[
 (\mu_1,\mu_2,\lambda),\qquad (\lambda,\mu_3,\mu_4).
\]
More explicitly, for a given parameter pair use the product
\[
 \mathcal N_S=C_S(u_1,u_2,u;p,q)C_S(u,u_3,u_4;p,q),
\]
and the analogous \(\mathcal N_V\), with \(u_i=e^{t e_1\mu_i/2}\), \(u=e^{t e_1\lambda/2}\). For the Virasoro factor use the equivalent coordinates \(\mu_i=2P_i/Q-1\), \(\lambda=2P/Q-1\). Its periods are \((e_1-e_2,e_2)\), whose sum is the original \(e_1\); use that sum, not the first chart period, in \(u_i=e^{t e_1\mu_i/2}\). Consequently the shifted internal variable is \(u q^j\). In the affine right chart it is \(u p^j\).

Let \(\widehat\Psi=\mathcal N_S\Psi\), \(\widehat F=\mathcal N_VF\). The flux shifts of the two triples are respectively \((0,0,j)\) and \((j,0,0)\). Equations (7) and (16) imply
\[
 \frac{\mathcal N_{S,\mathrm{right},j}\mathcal N_{V,j}}{\mathcal N_{S,\mathrm{left}}}
 =\frac{\mathcal C_{j,0,0}(\lambda,\mu_2,\mu_1)
 \mathcal C_{0,0,j}(\mu_4,\mu_3,\lambda)}{N_j(\lambda)}.
\tag{17}
\]
The two signs are \((-1)^j(-1)^j=1\). This is precisely the coefficient multiplying the \(j\)-summand in BFT (4.59). Multiplying that block relation by the left normalizer proves
\[
 \widehat\Psi_k(\vec\mu,\lambda;x,z)=
 \sum_{j\in\mathbb Z}\widehat\Psi_{k+1}(\vec\mu,\lambda+2j;x,z)
 \widehat F_b(\vec P,P(\lambda)+jb;z).\tag{18}
\]
The proof uses the published generic-parameter coset coefficient theorem; it is not inferred from finite computation. Generic noncritical levels and weights avoid poles of the norms and Gram matrices. Identities are understood as formal block expansions with meromorphic parameter coefficients. Extension to a singular specialization requires a separately defined regularized limit, and is not asserted.

## 6. Blowup parameter dictionary and remaining exact-target issue

Set
\[
 K=-\epsilon_2/\epsilon_1,\quad
 \lambda=2a/\epsilon_1-1,\quad
 d^2=(\epsilon_1-\epsilon_2)\epsilon_2,
 \quad b=\epsilon_2/d,\quad P=a/d.
\tag{19}
\]
Then \(Q=\epsilon_1/d\). The affine chart \((\epsilon_1,\epsilon_2-\epsilon_1)\) has level \(k+1\), and \(a+\epsilon_1j\) gives \(\lambda+2j\). The Virasoro chart \((\epsilon_1-\epsilon_2,\epsilon_2)\) has \(P\mapsto P+jb\). Also
\[
 b_T^2=b^{-2}=\frac{\epsilon_1-\epsilon_2}{\epsilon_2}
 =-\frac{k+3}{k+2},
\]
exactly the parameter-ratio condition asked for. Thus (18) has the full structural and flux form of (T).

This establishes the normalized **conformal-block** identity. To state (T) in a separately chosen instanton-counting convention, one must additionally identify:

1. the four physical masses with the ordered external momenta, including their equivariant half-shifts;
2. the particular regular surface defect and its coordinate \(w\) with \(x\);
3. the abelian \(U(1)\), classical, and one-loop factors in all three charts with a common branch/regularization convention.

BFT identifies its relation as the gauge-theory blowup relation via AGT, and its Appendix B intends to supply the normalization. The repaired calculation above supports that intent, but this packet has not independently proved this last convention-specific gauge dictionary. Alday–Tachikawa (2010), for example, writes an additional operator \(\mathcal K\) and an abelian factor in its surface-block formula (3.23); silently identifying every defect convention with an unmodified affine block would be unjustified. Accordingly, **no full-resolution claim for an independently fixed gauge normalization is made here**. Nor does failure of printed auxiliary formulas imply the underlying published theorem is false.

## References and attribution

- J. Teschner, “Tau-functions, coset constructions and free fermion conformal blocks,” OWR 16/2022, pp. 836–839; target on p. 837. https://doi.org/10.4171/owr/2022/16
- M. Bershtein, B. Feigin, A. Trufanov, “Highest-Weight Vectors and Three-Point Functions in GKO Coset Decomposition,” CMP 406, 142 (2025), Theorem 3.2, Corollary 3.18, Theorem 4.5, Eq. (4.59), Appendix B. https://doi.org/10.1007/s00220-025-05318-1 ; https://arxiv.org/abs/2404.14350 . Their coefficient theorem is the substantive published input.
- N. Nekrasov, “Blowups in BPS/CFT correspondence, and Painlevé VI,” AHP 25 (2024), 1123–1213, Eq. (1). https://arxiv.org/abs/2007.03646
- L. Alday, Y. Tachikawa, “Affine SL(2) conformal blocks from 4d gauge theories,” LMP 94 (2010), 87–114, Eqs. (3.23)–(3.25). https://arxiv.org/abs/1005.4469
- N. Nekrasov, A. Tsymbaliuk, “Surface defects in gauge theory and KZ equation,” LMP 112, 28 (2022). https://doi.org/10.1007/s11005-022-01511-8

The character repair, explicit sign audit and source-convention checks in this packet are local derivations. They should not be advertised as a new proof of a result already credited to BFT.
