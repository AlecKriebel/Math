# Independent audit of the stable division coordinate row approach

## Verdict and audited object

**Accepted as a correct partial result and an accurately delimited unsuccessful approach to the full converse.** No mathematical correction to the frozen report is required. The problem remains **UNRESOLVED, 1/5 substantive approaches used**.

The audited argument is [APPROACH_1.md](APPROACH_1.md) for corpus problem **30005477**, rank **1203**, alias **OWR-12697711-012**. This proof-only edition retains the complete substantive mathematical audit; [PROVENANCE.md](PROVENANCE.md) records its editorial boundary.

This audit rederives the mathematical claims, checks the stated quantifiers and boundary cases, and independently inspects the cited primary-source material. Acceptance applies to the retained mathematical argument and the exact editions identified in ACCEPTANCE.md. No novelty certification, proof of the full converse, or ideal-level counterexample is granted.

## 1 Source interpretation and prior attribution

The inspected Oberwolfach contribution uses the norm
\[
\|z^\alpha\|^2=\alpha!/|\alpha|!.
\]
Its printed page 849 first introduces radical homogeneous ideals. Its later stable-division paragraph states the sufficient implication for homogeneous ideals and asks about the converse without explicitly repeating radicality. Preserving both possible scopes is appropriate. All the audited positive deductions hold for arbitrary homogeneous ideals, so they also hold under the narrower radical interpretation. The main quantitative limitation uses a radical principal ideal, and the additional family-level diagnostic uses a prime ideal. Neither example silently replaces the source's ideal-level question with a prescribed-family question.

The repeated final-generator subscripts in the displayed definition on printed page 849 are genuinely present in the rendered source. The frozen report's intended reading is confirmed by Shalit's Definition 1.1 and Remarks 1.2–1.4: the property is existence of one finite generating family and one uniform product-energy constant. The squared-sum convention and the unsquared-sum convention used by Kennedy are equivalent for a fixed finite family, with constants allowed to change. Homogeneous components suffice for a homogeneous family.

Kennedy's Theorem 3.8 is exactly the prior closed-algebraic-sum characterization cited by the report. Shalit's Example 2.6, and Kennedy's corresponding Example 3.11, already distinguish an unstable prescribed generating family from an ideal possessing a stable family. Shalit's Theorem 4.1 supplies the forward essential-normality implication. The angle characterization on printed page 850 is attributed there to ongoing Kennedy–Shamovich work. The report correctly credits these facts and does not claim that they were first established by this approach.

Primary sources inspected:

- Eli Shamovich, *Arveson–Douglas essential normality conjecture: a bridge between operator algebras and algebraic geometry*, Oberwolfach Report 15/2023, printed pp. 848–850. [Public report](https://ems.press/content/serial-article-files/47009).
- Orr Moshe Shalit, *Stable polynomial division and essential normality of graded Hilbert modules*, arXiv:1003.0502v2, especially Definition 1.1, Remarks 1.2–1.4, Example 2.6, and Theorem 4.1. [Versioned source](https://arxiv.org/abs/1003.0502v2).
- Matthew Kennedy, *Essential normality and the decomposability of homogeneous submodules*, arXiv:1202.1797v2, especially Theorem 3.8 and Example 3.11. [Versioned source](https://arxiv.org/abs/1202.1797v2).

The cited primary-source locations were inspected. The rendered OWR page 37, printed page 849, was also visually inspected. SOURCE_LEDGER.json records the public PDF identities and the original retrieval and inspection history. This is a verification of the supplied report and its cited prior work, not an exhaustive current-literature or originality search.

## 2 Fixed family spectral characterization

For a prescribed finite homogeneous family, let
\[
E_{j,n}=f_jH_{n-\deg f_j}\subseteq I_n.
\]
Each is finite dimensional and therefore closed. The addition operator
\[
A_n:\bigoplus_jE_{j,n}\longrightarrow I_n
\]
is surjective because the family algebraically generates the ideal and homogeneous projection selects coefficients of the required degree. Its adjoint sends \(h\in I_n\) to \((P_{E_{j,n}}h)_j\), so
\[
A_nA_n^*=\left.\sum_jP_{E_{j,n}}\right|_{I_n}.
\]
On a nonzero \(I_n\), this positive operator is invertible. The minimum-norm lift of \(h\) is \(A_n^*(A_nA_n^*)^{-1}h\), whose squared norm is
\(\langle(A_nA_n^*)^{-1}h,h\rangle\). Maximizing over unit \(h\) gives exactly the inverse of the smallest eigenvalue, as stated.

Consequently, a uniform spectral gap for this family is equivalent to its stable division. The quantifier remains existence of some finite family; a small eigenvalue for one selected family cannot refute the ideal's stable-division property. Degrees with \(I_n=0\) must be omitted from the inverse-eigenvalue formula, as the report explicitly does.

## 3 Essential normality and leakage

Write \(P\) for the projection onto \([I]\) and \(Q=1-P\). Invariance of \([I]\) implies \(QM_iP=0\), or equivalently coinvariance of its orthogonal complement. For \(S_i=QM_i|_{QH}\) and \(L_i=QM_i^*P\), direct multiplication on \(QH\) gives
\[
[S_i,S_j^*]-Q[M_i,M_j^*]Q=QM_j^*PM_iQ=L_jL_i^*.
\]
The order of the subscripts and the positive sign in the frozen report are correct.

Ambient compactness can also be checked without an external theorem. On homogeneous degree \(N\ge1\),
\[
M_j^*h=N^{-1}\partial_jh,\qquad
[M_i,M_j^*]h=\frac{z_i\partial_jh}{N(N+1)}-\frac{\delta_{ij}}{N+1}h.
\]
Each coordinate multiplier has norm at most one. Therefore the norm of this block is at most \(2/(N+1)\). The degree-zero block is finite dimensional. Since degree spaces are finite dimensional, the ambient commutator is compact.

If all quotient commutators are compact, the diagonal identities imply compactness of \(L_iL_i^*\). This implies compactness of \(L_i\), for example by the polar decomposition and compactness of the square root of a positive compact operator. Conversely, compactness of all \(L_i\) implies compactness of every correction \(L_jL_i^*\), hence of every quotient commutator.

A homogeneous ideal has
\([I]=\bigoplus_{n\ge0}I_n\). Each \(L_i\) is a degree-lowering orthogonal block operator. Its tail norm is exactly the supremum of the norms of its remaining blocks. It is compact if and only if those block norms tend to zero. Necessity follows by applying compactness to unit vectors in distinct homogeneous degrees; sufficiency follows by finite-rank truncation. Finally,
\[
\max_i\|L_{i,n}\|^2\le\|B_n\|^2\le\sum_i\|L_{i,n}\|^2.
\]
There are finitely many coordinates. These observations prove both directions of the asserted equivalence between essential normality and \(\varepsilon_n\to0\). No rate of decay is obtained.

## 4 Exact restricted row identity and inverse cost

Let \(m\ge1\) bound the degrees of a finite homogeneous generating set of a nonzero proper ideal. For \(n\ge m\), every coefficient multiplying an original generator to obtain degree \(n+1\) has positive degree. Splitting it as a sum of coordinates times degree-one-lower polynomials proves
\[
I_{n+1}=\sum_jz_jI_n.
\]
Thus the restricted row \(R_n:(I_n)^d\to I_{n+1}\) is onto.

On degree \(n+1\),
\[
M_j^*z^\alpha=\frac{\alpha_j}{n+1}z^{\alpha-e_j},\qquad
\sum_jM_jM_j^*=1.
\]
In particular, the ambient coordinate row is a coisometry. The precise compressed identity is
\[
R_nR_n^*=P_{n+1}\sum_jM_{j,n}P_nM_{j,n}^*|_{I_{n+1}},
\]
whereas
\[
B_n^*B_n=P_{n+1}\sum_jM_{j,n}Q_nM_{j,n}^*|_{I_{n+1}}.
\]
Adding these expressions gives the identity on \(I_{n+1}\). This makes explicit the output compression implicit in the report's domain-splitting argument; it is a clarification, not a correction.

Surjectivity and finite dimension imply positive definiteness of \(R_nR_n^*\). Since \(B_n^*B_n\) is positive, its largest eigenvalue is \(\varepsilon_n\). Therefore
\[
\lambda_{\min}(R_nR_n^*)=1-\varepsilon_n>0.
\]
The optimal squared norm of a right inverse is exactly \((1-\varepsilon_n)^{-1}\), attained by the minimum-norm right inverse. This is an exact coefficient-norm cost. It is not identified with an optimal product-energy cost.

## 5 Bombieri multiplication and the induction

For \(|\alpha|=a\), symmetrizing an elementary tensor word of multiplicity \(\alpha\) gives an average of \(a!/\alpha!\) distinct orthonormal words. The resulting squared norm is \(\alpha!/a!\), exactly the norm convention used here. Thus the map from degree-\(a\) polynomials to symmetric degree-\(a\) tensors is isometric.

If \(U\) and \(V\) correspond to homogeneous polynomials \(f\) and \(g\), their product corresponds to the orthogonal symmetrization of \(U\otimes V\). This follows first for monomials and then by bilinearity. Orthogonal projection is contractive, so
\[
\|fg\|\le\|f\|\|g\|.
\]
There is no missing binomial coefficient or factorial under this normalized norm. This argument applies when either degree is zero as well.

An orthonormal basis of \(I_m\), together with orthonormal bases of every nonzero \(I_k\), \(k<m\), is finite. It generates the lower degrees directly. The restricted-row surjectivity above shows inductively that \(I_m\) generates every degree above \(m\). Hence the same one finite family works for the whole ideal; the family is not changed as \(N\) varies.

At degree \(m\), orthonormal expansion gives coefficient squared norm exactly \(\|h\|^2\). At the induction step, choose a minimum-norm coordinate lift \((u_j)_j\) of \(h\in I_{N+1}\), and independently decompose each \(u_j\) using the induction hypothesis. Writing the latter coefficients as \(a_{ij}\), set \(g_i=\sum_jz_ja_{ij}\). The ambient row is contractive on the direct sum of coefficient spaces, so
\[
\sum_i\|g_i\|^2\le\sum_{i,j}\|a_{ij}\|^2
\le P_{m,N}\sum_j\|u_j\|^2
\le P_{m,N+1}\|h\|^2.
\]
There is no application of a scalar triangle inequality that would introduce a coordinate-count factor, and summing over basis vectors does not introduce a dimension factor either. Multiplication contraction and \(\|f_i\|=1\) then give the claimed product-energy estimate.

For \(N<m\), use the adjoined orthonormal degree-\(N\) basis with scalar coefficients, obtaining product-energy constant one. Zero homogeneous spaces require no decomposition. For a nonhomogeneous polynomial, combine its finitely many homogeneous decompositions. Within each fixed generator's product, different total degrees are orthogonal, so their squared norms add. The zero ideal is vacuously stable, and the unit ideal has the family \(\{1\}\) and constant one. The report's exclusions and final treatment of these cases are sufficient.

## 6 Quantitative consequences and their exact limit

All factors \((1-\varepsilon_n)^{-1}\) for \(n\ge m\) are finite and at least one. If \(\varepsilon_n\to0\), then \(-\log(1-\varepsilon_n)\to0\), and Cesàro averaging gives
\[
\log P_{m,N}=o(N).
\]
Equivalently, for every fixed \(\delta>0\), an eventually valid \(e^{\delta N}\) estimate can absorb all finitely many exceptional degrees into one finite \(K_\delta\). This proves the claimed fixed-family subexponential degree-dependent estimate. It does not bound \(K_\delta\) uniformly as \(\delta\downarrow0\).

If \(\sum_{n=m}^{\infty}\varepsilon_n<\infty\), then eventually \(\varepsilon_n\le1/2\), and
\(-\log(1-\varepsilon_n)\le2\varepsilon_n\). The logarithmic sum converges, while the finitely many initial factors are finite. The resulting product is a degree-independent stable-division constant for the constructed family, including lower degrees and arbitrary polynomials as above.

Summability is an additional sufficient hypothesis. Neither compactness nor vanishing of individual blocks alone yields it. The audit accepts the conditional implication; it does not upgrade that implication to the full converse or to a newly established geometric subclass.

## 7 Principal radical ideal calibration

For \(I=(z_1)\subset\mathbb C[z_1,z_2]\), an orthonormal degree-\(n+1\) monomial has nonzero leakage precisely when its first exponent is one and the adjoint coordinate is \(M_{z_1}^*\). In that case its squared leakage is \(1/(n+1)\); all other ideal monomials have zero leakage. These images lie in a single orthogonal block, so the operator norm is indeed
\[
\varepsilon_n=1/(n+1),\quad n\ge1,
\]
and the displayed normalized monomial attains it.

For \(m=1\), the inverse factors telescope to \(P_{1,N}=N\). Multiplication by \(z_1\) is algebraically injective, so the coefficient of \(\sqrt N z_1z_2^{N-1}\) relative to this generator is uniquely \(\sqrt N z_2^{N-1}\), whose squared norm is \(N\). Yet there is only one product summand, equal to the target itself, and the stable product-energy constant is exactly one.

The example is radical and essentially normal by the already proved leakage criterion. It conclusively shows both that summable leakage is unnecessary for stable division and that divergent accumulated coefficient costs cannot establish failure of uniform product-energy decompositions. It supplies no counterexample to the converse.

## 8 Prime ideal prescribed family calibration

Put \(p=x^2+wy\), \(q=wy^2+z^3\), and \(r=x^4+wz^3\). With lexicographic order \(x>z>y>w\), the leading monomials of \(p\) and \(q\) are \(x^2\) and \(z^3\). They are coprime; Buchberger's relatively-prime-leading-monomial criterion applies. The resulting standard monomials are precisely \(x^az^by^cw^e\) with \(a<2\), \(b<3\). Multiplication by \(w\) carries this basis injectively to itself, proving that \(w\) is a nonzerodivisor and that localization at its powers is injective.

After localization, eliminating \(y\) gives
\[
\mathbb C[w,w^{-1},x,z]/(x^4+wz^3).
\]
The defining polynomial is primitive in \(\mathbb C[x,z][w]\) because \(x^4\) and \(z^3\) are relatively prime. Over \(\mathbb C(x,z)\), it is a nonconstant linear polynomial in \(w\), hence irreducible. Gauss's lemma yields irreducibility in the polynomial UFD and therefore primality. Its prime ideal does not contain a power of \(w\), so it remains proper and prime after localization. The original quotient embeds in this domain and is a domain. The ideal \((p,q)\) is thus prime, while the independent standard monomials \(w^e\) show that its quotient is infinite dimensional.

The identity
\[
r=(x^2-wy)p+wq
\]
is exact and homogeneous. The polynomials \(p,q\) are coprime: a nonconstant common divisor would have a leading monomial dividing both \(x^2\) and \(z^3\). Therefore any polynomial representation of \(h_n=w^nr\) differs from the given one by the syzygy \((tq,-tp)\).

Every monomial occurring in \(tp\) contains \(x\) or \(y\). Thus the coefficient of pure \(w^{n+1}\) in the coefficient of \(q\) is forced to be one. In its product with \(q\), only the \(wy^2\) term can contribute to \(w^{n+2}y^2\); the \(z^3\) term cannot. Consequently this product has coefficient one on that monomial. The product with \(p\) must have coefficient minus one there, since the target does not contain it. This reasoning also applies to nonhomogeneous coefficient polynomials.

Monomial orthogonality and the stated norm therefore imply
\[
\|ap\|^2+\|bq\|^2\ge\frac{4(n+2)!}{(n+4)!},\qquad
\|h_n\|^2=\frac{6(n+5)n!}{(n+4)!}.
\]
The resulting lower ratio
\[
\frac{2(n+1)(n+2)}{3(n+5)}
\]
is correct and diverges. It is presented as a lower bound, not as the exact minimum. The particular displayed decomposition has ratio one plus this lower bound, which is fully consistent with the report. Thus the prescribed pair is unstable.

Adjoining the redundant generator \(r\) gives a single-product decomposition of every \(h_n\), with product-energy constant one on this witness sequence. This proves only the repair of that sequence. The report correctly does not infer stability of \(\{p,q,r\}\) on the whole ideal, instability of every finite family, or essential normality of this particular prime ideal.

## 9 Acceptance limits

No proof correction is necessary. The accepted deductions are the leakage equivalence, exact one-step coefficient cost, fixed-family finite-product bound, subexponential consequence, summable-leakage sufficient criterion, and the two carefully limited calibration examples.

The unresolved step is a uniform product-energy bound for some finite homogeneous generating family under essential normality alone. The report neither obtains that bound nor proves an invariant obstruction that survives all finite generating families. Its status and approach count must remain **UNRESOLVED, 1/5**. Acceptance of this report does not certify novelty, establish the general converse, certify a present-day literature-wide status, or authorize any additional claim of resolution.
