# Stable division converse: coordinate-row lifting approach

Problem: rank 1203, corpus 30005477, alias OWR-12697711-012.

Status: **unresolved after one substantive approach (1/5)**. This report proves a degree-dependent consequence of essential normality and a conditional sufficient criterion. It does not prove the converse, exhibit an ideal lacking every stable generating family, or claim a new positive geometric subclass. Novelty of the elementary deductions below is not asserted.

## 1. Source statement and scope

Shamovich's contribution to Oberwolfach Report 15/2023, printed pp. 848–850, defines the Drury–Arveson norm by

\[
 \|z^\alpha\|^2=\frac{\alpha!}{|\alpha|!}.
\]

On printed p. 849 (PDF page 37), the initial ideal is radical and homogeneous. The later stable-division paragraph states Shalit's sufficient condition for a homogeneous ideal without repeating radicality, and asks for its converse. Both readings therefore remain relevant. All deductions here apply to arbitrary homogeneous ideals and hence also to radical ideals.

The source's summation indices repeat the final generator under a sum over a different index. The intended definition is unambiguous from Shalit, Definition 1.1 and Remarks 1.3–1.4: there must exist one finite homogeneous generating family \(F=(f_1,\ldots,f_k)\) and one degree-independent constant \(C\) such that every homogeneous \(h\in I\) admits

\[
 h=\sum_j f_jg_j,\qquad
 \sum_j\|f_jg_j\|^2\le C\|h\|^2.
\]

For homogeneous \(h\), the coefficients may be taken homogeneous of the appropriate degrees by taking the degree of \(h\) in each summand; orthogonal projection cannot increase the sum of squared norms. Nonhomogeneous \(h\) then follows by orthogonality of degrees.

The premise is that every commutator \([S_i,S_j^*]\) of the quotient coordinate tuple on \(H_I=H_d^2\ominus[I]\) is compact. The required conclusion is existence of some suitable family, not stability of an arbitrary prescribed family.

## 2. Prior work, not a new result here

Kennedy, *Essential normality and the decomposability of homogeneous submodules*, arXiv:1202.1797v2, Theorem 3.8, establishes that a prescribed finite homogeneous family is stable exactly when the algebraic sum of its principal closed Hilbert submodules is closed. Shalit, Example 2.6, already gives an unstable generating family for an ideal that has a different stable family. Kennedy, Example 3.11, revisits that example in the closed-sum language.

For completeness, let \(E_{j,n}=f_jH_{n-\deg f_j}\), with \(E_{j,n}=0\) when the index is negative. The addition map

\[
 A_n:\bigoplus_jE_{j,n}\longrightarrow I_n,
 \qquad (u_j)_j\longmapsto\sum_j u_j
\]

is onto. Its optimal squared decomposition constant is

\[
 C_{F,n}=\lambda_{\min}\!\left(
      \left.\sum_jP_{E_{j,n}}\right|_{I_n}\right)^{-1}.
\]

Here \(I_n=I\cap H_n\), and degrees with \(I_n=0\) are omitted. This follows from \(A_nA_n^*=\sum_jP_{E_{j,n}}|_{I_n}\) and the minimum-norm right inverse. Thus Kennedy's condition is equivalently \(\sup_nC_{F,n}<\infty\). The converse problem still asks for existence of a family with that uniform spectral gap.

## 3. Exact relation between compactness and coordinate leakage

Write \(P_n\) for projection from \(H_n\) onto \(I_n\), and \(Q_n=1-P_n\). Put

\[
 M_{j,n}=M_{z_j}|_{H_n}:H_n\to H_{n+1},\qquad
 L_{j,n}=Q_nM_{j,n}^*|_{I_{n+1}}.
\]

Define the column operator

\[
 B_n:I_{n+1}\to(Q_nH_n)^d,
 \qquad B_nh=(L_{1,n}h,\ldots,L_{d,n}h),
 \qquad \varepsilon_n=\|B_n\|^2.
\]

These definitions do not require essential normality.

### Lemma 1: compactness is exactly vanishing leakage

The quotient tuple is essentially normal if and only if \(\varepsilon_n\to0\).

**Proof.** Let \(P\) project onto \([I]\) and \(Q=1-P\). The ideal closure is invariant under each \(M_i\), so \(H_I\) is coinvariant. If \(L_j=QM_j^*P\), direct multiplication gives

\[
 [S_i,S_j^*]-Q[M_i,M_j^*]Q=L_jL_i^*.
\]

The ambient commutators are compact (the standard Drury–Arveson shift result used in both primary sources). Essential normality of the quotient therefore implies compactness of \(L_iL_i^*\), hence of \(L_i\). Conversely, compactness of the \(L_i\) makes the right-hand side compact for every pair.

Each \(L_i\) is the orthogonal block sum of the finite-dimensional maps \(L_{i,n}\), shifting degree down by one. Such an operator is compact exactly when \(\|L_{i,n}\|\to0\). Finally,

\[
 \max_i\|L_{i,n}\|^2\le\varepsilon_n
 \le\sum_i\|L_{i,n}\|^2.
\]

There are finitely many coordinates, proving the equivalence. \(\square\)

### Lemma 2: exact one-step inverse cost

Let \(m\ge1\) bound the degrees of a finite homogeneous generating family of a nonzero proper ideal \(I\). For \(n\ge m\), define

\[
 R_n:(I_n)^d\to I_{n+1},\qquad R_n(u_j)_j=\sum_jz_ju_j.
\]

Then \(R_n\) is onto and

\[
 R_nR_n^*=1_{I_{n+1}}-B_n^*B_n. \tag{1}
\]

In particular \(0\le\varepsilon_n<1\), and every \(h\in I_{n+1}\) admits \(h=\sum_jz_ju_j\), \(u_j\in I_n\), with

\[
 \sum_j\|u_j\|^2\le(1-\varepsilon_n)^{-1}\|h\|^2. \tag{2}
\]

The constant in (2) is optimal for these coefficient norms.

**Proof.** Every homogeneous polynomial coefficient of positive degree is a sum of coordinates times lower-degree polynomials. Applied to a generating family with degrees at most \(m\), this shows \(I_{n+1}=\sum_jz_jI_n\) for \(n\ge m\).

The ambient row \(D_n:(H_n)^d\to H_{n+1}\), \(D_n(v_j)=\sum_jz_jv_j\), is a coisometry. Indeed, on a degree-\(n+1\) monomial,

\[
 M_j^*z^\alpha=\frac{\alpha_j}{n+1}z^{\alpha-e_j},
 \qquad\sum_jM_jM_j^*z^\alpha=z^\alpha.
\]

Consequently \(D_nD_n^*=1\). Splitting its domain into \((I_n)^d\oplus(Q_nH_n)^d\) gives (1). Surjectivity makes \(R_nR_n^*\) positive definite, so its smallest eigenvalue is \(1-\varepsilon_n>0\). The minimum-norm right inverse \(R_n^*(R_nR_n^*)^{-1}\) has squared norm \((1-\varepsilon_n)^{-1}\), proving (2). \(\square\)

This coordinate-angle viewpoint is consistent with the Kennedy–Shamovich angle characterization reported as ongoing joint work on printed p. 850 of the OWR source. It is not presented as an independently novel characterization.

## 4. What the iteration actually proves

Choose an orthonormal basis \(f_1,\ldots,f_r\) of \(I_m\). Adjoin orthonormal bases of all the nonzero spaces \(I_0,\ldots,I_{m-1}\), obtaining one finite homogeneous family \(F\). This is an algebraic generating family for \(I\): lower degrees are covered directly, and \(I_m\) generates the tail because the original generator degrees are at most \(m\).

Define

\[
 P_{m,N}=\prod_{n=m}^{N-1}(1-\varepsilon_n)^{-1}
 \quad(N\ge m),\qquad P_{m,m}=1.
\]

### Proposition 3: a fixed-family, degree-dependent bound

Every \(h\in I_N\), \(N\ge m\), admits coefficients \(g_i\in H_{N-m}\) such that

\[
 h=\sum_{i=1}^rf_ig_i,
 \qquad
 \sum_i\|g_i\|^2\le P_{m,N}\|h\|^2,
 \qquad
 \sum_i\|f_ig_i\|^2\le P_{m,N}\|h\|^2. \tag{3}
\]

For \(N<m\), the adjoined degree-\(N\) orthonormal basis gives the required decomposition with product-energy constant 1.

**Proof.** At \(N=m\), expand in the orthonormal basis, with scalar coefficients; (3) holds with equality for the coefficient sum. Suppose the coefficient estimate is proved in degree \(N\). By Lemma 2, write \(h=\sum_jz_ju_j\) with

\[
 \sum_j\|u_j\|^2\le(1-\varepsilon_N)^{-1}\|h\|^2.
\]

Independently lift each \(u_j\) using the induction hypothesis:

\[
 u_j=\sum_if_ia_{ij},\qquad
 \sum_i\|a_{ij}\|^2\le P_{m,N}\|u_j\|^2,
 \qquad a_{ij}\in H_{N-m}.
\]

Set \(g_i=\sum_jz_ja_{ij}\). The ambient coordinate row is contractive, so

\[
 \sum_i\|g_i\|^2
 \le\sum_{i,j}\|a_{ij}\|^2
 \le P_{m,N}(1-\varepsilon_N)^{-1}\|h\|^2.
\]

This proves the induction, without an extra factor from the number of coordinates or the number of degree-\(m\) basis vectors.

To obtain the second estimate in (3), the homogeneous Bombieri product inequality gives \(\|fg\|\le\|f\|\|g\|\). One elementary justification is the isometric identification of \(H_a\) with the symmetric tensors in \((\mathbb C^d)^{\otimes a}\), where a monomial corresponds to its averaged symmetric elementary tensor. Polynomial multiplication is orthogonal symmetrization of the tensor product, which is contractive. Since \(\|f_i\|=1\), each \(\|f_ig_i\|\le\|g_i\|\). Thus the bound really does apply to the product norms required by stable division. \(\square\)

### Consequence 3a: subexponential loss under the stated premise

If the quotient tuple is essentially normal, Lemma 1 gives \(\varepsilon_n\to0\). Hence

\[
 \log P_{m,N}=\sum_{n=m}^{N-1}-\log(1-\varepsilon_n)=o(N).
\]

Therefore the fixed finite family above gives a degree-dependent product-energy bound \(\exp(o(N))\). More explicitly, for every \(\delta>0\) there is a finite constant \(K_\delta\), independent of \(N\), such that

\[
 \sum_j\|f_jg_j\|^2\le K_\delta e^{\delta N}\|h\|^2
 \qquad(h\in I_N).
\]

This follows from Cesàro averaging of the sequence \(-\log(1-\varepsilon_n)\to0\). The finite initial degrees are absorbed into \(K_\delta\). Neither \(K_\delta\) nor this estimate supplies a uniform bound as \(\delta\downarrow0\).

### Consequence 3b: a conditional sufficient criterion

If

\[
 \sum_{n=m}^\infty\varepsilon_n<\infty, \tag{4}
\]

then \(P_{m,\infty}=\prod_{n=m}^\infty(1-\varepsilon_n)^{-1}<\infty\), and the same fixed family \(F\) is stable with the degree-independent constant

\[
 C=P_{m,\infty}\ge1.
\]

For large \(n\), \(-\log(1-\varepsilon_n)\le2\varepsilon_n\); the remaining finite factors are finite by Lemma 2. This proves convergence of the product. For arbitrary polynomial \(h\in I\), combine the homogeneous decompositions and use orthogonality of their products by total degree.

Condition (4) is an additional quantitative assumption, not a consequence established from essential normality. No claim is made that it furnishes a new nontrivial geometric class. In fact the next example shows it is not necessary even for a principal radical ideal.

The zero ideal and the unit ideal are trivial stable cases and were excluded above only to avoid empty bases or \(m=0\).

## 5. Sharp limitation: a principal radical ideal

Take \(I=(z_1)\subset\mathbb C[z_1,z_2]\), which is radical and has the stable family \(\{z_1\}\) with \(C=1\).

For a normalized degree-\(n+1\) monomial belonging to \(I\), leakage to \(I_n^\perp\) is possible only when the exponent of \(z_1\) is exactly one and the adjoint coordinate is \(M_{z_1}^*\). Thus

\[
 \varepsilon_n=\frac1{n+1}\qquad(n\ge1).
\]

The unit vector

\[
 h_n=\sqrt{n+1}\,z_1z_2^n
\]

attains the bound, since

\[
 M_{z_1}^*h_n=\frac{z_2^n}{\sqrt{n+1}}\in I_n^\perp.
\]

For \(m=1\), the squared coefficient bound from Proposition 3 is

\[
 P_{1,N}=\prod_{n=1}^{N-1}\frac{n+1}{n}=N.
\]

This is even the exact coefficient cost for the normalized vector \(\sqrt N z_1z_2^{N-1}\): its unique coefficient relative to generator \(z_1\) is \(\sqrt N z_2^{N-1}\), of squared norm \(N\). Nevertheless its sole product summand is the vector itself, so the required product-energy constant is 1.

Consequently, the unsummable loss occurs in a trivial positive instance. It neither proves growth of the optimal product-energy constants nor rules out a different generating family or a sharper analysis of the products. The coefficient-to-product contraction in Proposition 3 is valid but can discard precisely the compensation needed for uniformity.

## 6. Additional quantifier calibration: an unstable pair in a prime ideal

This is an elementary diagnostic calculation, not an ideal-level counterexample and not an assertion of essential normality for this ideal.

In \(\mathbb C[x,y,z,w]\), put

\[
 p=x^2+wy,\qquad q=wy^2+z^3,\qquad I=(p,q),\qquad r=x^4+wz^3.
\]

### The ideal is prime and has infinite-dimensional quotient

For lexicographic order \(x>z>y>w\), the leading monomials of \(p,q\) are \(x^2,z^3\). They are relatively prime, so this pair is a Gröbner basis. Standard monomials are \(x^az^by^cw^e\) with \(a<2\), \(b<3\). Multiplication by \(w\) takes distinct standard monomials to distinct standard monomials, so \(w\) is a nonzerodivisor in the quotient.

After inverting \(w\) and eliminating \(y=-x^2/w\), the quotient becomes

\[
 \mathbb C[w,w^{-1},x,z]/(x^4+wz^3).
\]

The polynomial \(x^4+wz^3\) is primitive as a polynomial in \(w\) over \(\mathbb C[x,z]\), since \(x^4\) and \(z^3\) are coprime; it is linear and irreducible over \(\mathbb C(x,z)\). By Gauss's lemma it is irreducible in \(\mathbb C[x,z,w]\), hence prime there, and remains prime upon inverting \(w\). The localized quotient is a domain. The original quotient injects into it because \(w\) is a nonzerodivisor, so it too is a domain. Thus \(I\) is prime, in particular radical. The standard monomials \(w^e\) alone already prove infinite codimension as a vector subspace.

### This particular pair is not stable

The identity

\[
 r=(x^2-wy)p+wq
\]

shows that \(h_n=w^nr\in I\). Any decomposition \(h_n=ap+bq\) differs from

\[
 a_0=w^n(x^2-wy),\qquad b_0=w^{n+1}
\]

by \(a-a_0=tq\), \(b-b_0=-tp\), because \(p,q\) are coprime in the polynomial UFD. Every monomial in a multiple of \(p\) contains \(x\) or \(y\), so the coefficient of the pure monomial \(w^{n+1}\) in \(b\) is forced to be 1. It follows that the coefficient of \(w^{n+2}y^2\) in \(bq\) is 1. Since this monomial is absent from \(h_n\), its coefficient in \(ap\) is \(-1\). Orthogonality of monomials yields

\[
 \|ap\|^2+\|bq\|^2\ge2\|w^{n+2}y^2\|^2
       =\frac{4(n+2)!}{(n+4)!}.
\]

Meanwhile

\[
 \|h_n\|^2
 =\frac{24n!+6(n+1)!}{(n+4)!}
 =\frac{6(n+5)n!}{(n+4)!}.
\]

Hence every such decomposition satisfies

\[
 \frac{\|ap\|^2+\|bq\|^2}{\|h_n\|^2}
 \ge\frac{2(n+1)(n+2)}{3(n+5)}\longrightarrow\infty.
\]

However, adjoining \(r\) as a redundant third generator gives \(h_n=r\,w^n\), with product-energy constant 1 for this entire witness sequence. This calculation does not establish whether \(\{p,q,r\}\) is stable on all of \(I\), and makes no claim that no further finite enlargement works. Its only conclusion is that even primeness and infinite codimension do not remove the generating-family quantifier pitfall.

## 7. Exact stopping point

The premise supplies \(\varepsilon_n\to0\). The coordinate-row construction supplies the finite products \(P_{m,N}\), and thus the subexponential bound. What remains missing is a uniform bound for product-energy decompositions in some finite family. Summability of leakage would suffice by the proved argument but is not necessary and does not follow from the premise here. Even a divergent product of optimal one-step coefficient costs does not imply failure of stable division.

No invariant obstruction surviving every finite homogeneous generating family was found. The prime-ideal example is explicitly repaired on its test sequence by one added generator. The general converse remains unresolved; this report should count only as one attempted approach, not a solution or a strengthened prior-resolution claim.

## Sources

1. Eli Shamovich, *Arveson–Douglas essential normality conjecture: a bridge between operator algebras and algebraic geometry*, contribution to Oberwolfach Report 15/2023, pp. 848–850. https://ems.press/content/serial-article-files/47009
2. Orr Moshe Shalit, *Stable polynomial division and essential normality of graded Hilbert modules*, arXiv:1003.0502v2; Journal of the London Mathematical Society 83 (2011), 273–289. https://arxiv.org/abs/1003.0502v2 ; https://doi.org/10.1112/jlms/jdq054
3. Matthew Kennedy, *Essential normality and the decomposability of homogeneous submodules*, arXiv:1202.1797v2; Transactions of the American Mathematical Society 367 (2015), 293–311. https://arxiv.org/abs/1202.1797v2
