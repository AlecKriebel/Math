# Independent audit: orthogonal-pair theta modules and ordinary Jacobi principal series

Public proof-only edition. Recorded audit date: 10 October 2026. This AI-assisted audit is unrefereed; acceptance is not external human peer review, journal acceptance, or formal proof-assistant certification.

## Verdict

**ACCEPTED_PARTIAL_NOT_SOLVED.** The frozen attempt's core partial theorem is correct for the stated chamberwise rational-isotropic subfamily. The conditional extension to other data is correctly identified as conditional. There is no full solution of the originating question and no novelty certificate.

The accepted content is the exact cyclic infinitesimal module

\[
P^{\otimes p}\otimes (A_1/A_1(xd))^{\otimes r},
\]

with trivial residual \(\mathfrak{sl}_2\), its simple essential oscillator socle, an explicit socle injection into the specified normalized Jacobi principal series at parameter \(-1\), and zero Hom from the full module to every specified ordinary smooth or distribution-vector principal series when \(r>0\). The latter obstruction also applies to an arbitrary smooth moderate-growth multiplicity representation in the oscillator tensor product.

The critical additional source assertion involving the *ordinary* Jacobi lowering operator is incompatible with the literal printed formulas. This audit independently confirms the attempt's caution. It does not import that assertion, does not rely on it for convergence or modularity, and does not claim to repair all the affected statements in the source papers.

There are no mathematical blockers to the partial result in its qualified scope. Three interpretation details must remain explicit in any account of acceptance:

1. The arithmetic modularity and discriminant-Weil statements use an integral/even lattice in the relevant source convention. The local differential-module calculation itself only needs a discrete full lattice and the stated analytic expansion. Do not read the source's word “lattice” as permitting arbitrary real-valued forms while still asserting a discriminant Weil representation.
2. The displayed map from the algebraic Hermite socle is an **infinitesimal** injection. Its Schwartz oscillator globalization has the corresponding genuine group-equivariant injection. The finite polynomial-Hermite span is not itself invariant under all real Heisenberg translations.
3. The proof's normalized completion is the usual error-function completion, not a verbatim transcription of every symbol in the 2015 definition. Relative normalization of the sign and error terms matters. These are scope/notation clarifications, not failures of the mathematical conclusions.

## 1. Frozen target and source scope

This audit concerns problem 30003033 / OWR-14211-008. The distributed [PROOF.md](PROOF.md) has 29,202 bytes and SHA-256 `521b18a5fb0f7825a2cbe77e678ad073cd19822e9f6a58e1a4b725400a1d58ee`. Its full accepted mathematical argument is preserved. This edition incorporates the direct rational-ray convergence/differentiation argument in section 4 and the explicit ordinary-lowering Fourier coefficient in section 5 below, while making the accepted arithmetic and infinitesimal/global distinctions explicit. These additions do not expand the accepted partial theorem.

The complete original proof, summary, status, references, and tests were read for the audit. All listed author-payload bytes were independently checked against the original frozen manifest; its verification was also replayed in normal and optimized Python. No original author file, repository file, or queue entry was changed. The original package pin and complete editorial reconstruction are retained in edition-preparation verification.

The actual originating OWR contribution, printed pages 138–139, was read completely and the target page was visually inspected. Its specific data are mutually orthogonal planes spanned by a negative vector and an isotropic vector, one pair per negative direction. It announces first-order positive-direction and second-order negative-direction annihilators, a Jacobi Casimir equation, and an extension interpretation. It asks for a principal-series connection. An unspecified embedding, a modular-completion theorem, or a socle-only result is not a complete answer to that broader question.

The entire 30-page WR15 preprint and entire 18-page WR17 preprint were read, including their final sections. The published WR15 counterpart was compared at the precise operator, subspace, theta-definition, and corollary pages; it was not separately claimed to have been read in full. CR's operator and virtual-Levi sections and Sun's theorem/category/distribution-vector sections were inspected. Exact PDF hashes, sizes, page coverage, and public URLs are recorded in [SOURCE_METADATA.json](SOURCE_METADATA.json).

References:

- OWR, “Analytic properties of some indefinite theta series,” https://doi.org/10.4171/owr/2016/3
- WR15, *H-Harmonic Maaß-Jacobi Forms of Degree 1*, https://arxiv.org/abs/1207.5603v3
- Published WR15, https://doi.org/10.1186/s40687-015-0032-y
- WR17, *Indefinite Theta Series on Cones*, https://arxiv.org/abs/1608.08874v2
- CR, *Harmonic Maaß-Jacobi forms of degree 1 with higher rank indices*, https://arxiv.org/abs/1012.2897v2
- Sun, *On representations of real Jacobi groups*, https://arxiv.org/abs/1004.5508v2
- Zwegers, *Mock Theta Functions*, Definition 2.1 and its following elliptic-variable formula, https://arxiv.org/abs/0807.4834

The last source was independently checked as a normalization cross-check, not as an exhaustive reading of the thesis. Its original thesis date is 2002, while the arXiv version inspected is v1 from 2008.

## 2. Real form, central character, and constants

Take \(B=2q\), with \(q(z)=\sum_j m_jz_j^2\). The proposed Heisenberg law using \(\Omega/2\), central character \(e^{2\pi it}\), and Schrödinger generators

\[
P_j=\partial_{t_j},\qquad Q_j=4\pi i m_jt_j
\]

are compatible: \([P_i,Q_j]=4\pi i m_j\delta_{ij}\). Thus

\[
L_j=(P_j-iQ_j)/2,\quad R_j=(P_j+iQ_j)/2,
\quad [L_i,R_j]=-2\pi m_j\delta_{ij}=\beta_j\delta_{ij}.
\]

The adjoint relation is \(L_j^*=-R_j\). In a positive direction the physical Gaussian is killed by \(L_j\); in a negative direction it is killed by \(R_j\). Reversing this last convention would invalidate the nonembedding proof. The author's choice is correct.

The metaplectic pullback is sufficient in every dimension. The covering kernel acts on the oscillator by \((-1)^n\), so the warning about non-genuineness on this particular double cover for even \(n\) is correct. No group-level action of the full theta extension is silently constructed by the algebraic computation.

For the covariant differential operators, the weight of the input of each successive raising operation must change. Independent differential-operator coefficient calculations in ranks one and two, with symbolic nonzero masses and symbolic weight, check the printed commutators identically on arbitrary functions. Freezing the intermediate weight fails a negative control.

## 3. General-rank virtual Levi and the Casimir shift

This part can be checked without a theta function. Normalize \(x_j=R_j\), \(d_j=L_j/\beta_j\), so \([d_i,x_j]=\delta_{ij}\). The oscillator quadratic expressions have

\[
[H_{\rm osc},E_{\rm osc}]=2E_{\rm osc},\quad
[H_{\rm osc},F_{\rm osc}]=-2F_{\rm osc},\quad
[F_{\rm osc},E_{\rm osc}]=-H_{\rm osc}.
\]

For example, in one coordinate \([d^2,x^2]=4xd+2\), which gives the last identity, including the constant \(1/2\) in the oscillator Cartan. Cross-coordinate terms commute. The oscillator terms have the same commutators with every \(L_j,R_j\) as the corresponding full Jacobi generators. Their differences therefore commute with the Weyl algebra and form a residual \(\mathfrak{sl}_2\). PBW yields the claimed fixed-nonzero-central-character algebra splitting; there is no reliance on an algebraic version of Stone–von Neumann.

The residual Casimir is

\[
\Omega_0=H_0^2-2H_0+4E_0F_0.
\]

CR's virtual-Levi formula and its computed slash action give

\[
\Omega_0=k(k-n-2)+\frac{n(n+4)}4-2C_{k,L}
=(k-n/2)(k-n/2-2)-2C_{k,L}.
\]

This is the author's shift, including sign and factor two. Independently, the coordinate expression of CR equation (2.4), read visually on physical PDF page 6, was implemented as an actual differential operator and compared coefficient by coefficient to the residual construction. The identity passes in ranks one and two for arbitrary formal masses and weight. The check does not merely substitute the oscillator action into the author's chosen normal-ordered Casimir formula.

Consequently \(C_{n/2,L}\Theta=0\), while shifted descendants in the trivial-residual module have eigenvalue

\[
\tfrac12(k-n/2)(k-n/2-2).
\]

The omission of this scalar shift fails the independent negative control. This distinction must survive any shortened statement of the result.

## 4. Independent analytic bound for rational isotropic rays

The proof's analytic input can be justified directly in this orthogonal family, without assuming that absolute convergence alone implies termwise differentiability.

Rescale real coordinates separately on each signature \((1,1)\) plane so its quadratic form is \(\alpha_i^2-\beta_i^2\), its negative vector is along the \(\beta_i\)-axis, and its isotropic vector points in the direction \((1,1)\). The orientation condition \(B(c_i,d_i)<0\) permits this choice with the signs used below. Put \(w=\nu+v/y\) and \(\lambda_i=\alpha_i-\beta_i\). The completed factor is

\[
K_i(w)=-E(2\sqrt y\,\beta_i)-\operatorname{sgn}(\lambda_i).
\]

Decompose it, for estimates only, as

\[
D_i+T_i,
\qquad D_i=-\operatorname{sgn}(\beta_i)-\operatorname{sgn}(\lambda_i),
\quad T_i=\operatorname{sgn}(\beta_i)-E(2\sqrt y\,\beta_i).
\]

The cone contribution \(D_i\) is supported where \(\beta_i\lambda_i\ge0\). On this support

\[
q_i(w)=\lambda_i^2+2|\lambda_i||\beta_i|.
\]

For a rational isotropic ray, \(B(d_i,L)\) is discrete after a fixed rescaling, under the integral-lattice hypothesis. On a compact subset of a chamber avoiding every isotropic sign wall there is therefore one \(\delta>0\) with \(|\lambda_i|\ge\delta\) for every lattice term and every index \(i\). It follows that

\[
q_i(w)\ge\delta(|\lambda_i|+2|\beta_i|)
\ge\delta\sqrt{\alpha_i^2+\beta_i^2}
\]

on the cone support. The complementary tail satisfies

\[
|T_i|\le e^{-4\pi y\beta_i^2}.
\]

Multiplying that tail by the absolute value of the exponential changes the plane's quadratic decay from \(q_i\) to \(q_i+2\beta_i^2=\alpha_i^2+\beta_i^2\). Every differentiated error factor likewise is a polynomial in the lattice coordinates, with coefficients uniformly bounded on the chosen compact set, times this Gaussian. Undifferentiated factors retain the cone-plus-tail bound. Differentiating the holomorphic exponential only introduces additional polynomial factors.

The remaining positive orthogonal space contributes positive-definite Gaussian decay. After expanding the finitely many choices of cone/tail factors, all summands of every prescribed finite derivative are bounded uniformly by

\[
C(1+\|\nu\|)^N e^{-c\|\nu\|},\qquad c>0.
\]

This is summable over any full lattice. In obtaining the bound one uses

\[
|e^{2\pi i(q(\nu)\tau+B(z,\nu))}|
=e^{2\pi yq(v/y)}e^{-2\pi yq(\nu+v/y)};
\]

the first factor is bounded on the compact set. Thus all needed derivatives, and indeed derivatives of every finite order, converge locally normally on such chambers. No rational splitting of the full lattice into the real planes was used.

This verifies the rational-ray part of the claimed analytic input. The argument gives no uniform \(\delta\) for general irrational isotropic data. It therefore does not erase the attempt's irrational-edge boundary. Likewise, the estimate is not a license to differentiate sign jumps across a wall or poles across a singular divisor as if no distributions were created.

## 5. Kernel identities, source discrepancy, and normalization

In the author's negative coordinate, set \(w_j=v_j+y\nu_j\). The nonconstant amplitude is

\[
A=E(-2\sqrt{-m_j}\,w_j/\sqrt y).
\]

Straight differentiation gives

\[
A_y=(\nu_j/2-v_j/(2y))A_v,
\qquad A_{vv}=8\pi m_j(v_j+y\nu_j)A_v/y.
\]

Substitution into the full Wirtinger operators gives \(R_jL_j\) equal to zero on the Fourier term. Positive-direction \(L_j\) vanishes, because the error amplitudes depend only on the negative directions and the isotropic signs are locally constant. The same identities give the holomorphic heat equation and \(F_0\Theta=0\). The Cartan identity follows from the first- and second-order equations at weight \(n/2\). Independent computation differentiates the full exponential-times-error-function Fourier term in real coordinates, for a signature \((1,1)\) plane and generic Fourier coordinates, rather than only testing the already-simplified amplitude identities. It verifies all five relevant equations.

### The additional ordinary-lowering assertion really fails

Visually inspected locations are:

- WR15 preprint physical page 8: ordinary lowering operator (1.5)
- WR15 page 14: the subspace defined by intersection with its kernel
- WR15 page 26: Corollary 3.7 placing the theta function in that subspace
- Published WR15 physical pages 10, 16, and 30: the same chain, with equations (2.5) and Corollary 4.7
- Published WR15 page 26: the underlying theta-kernel definition

The printed operator is the author's \(F=X_-\), not the residual \(F_0\). It has no weight term that could remove the discrepancy.

One can rule out cancellation in the theta sum explicitly. Take the even integral lattice \(\mathbb Z^2\) with \(q(a,b)=a^2-b^2\), \(c=(0,1)\), \(d=(1,1)\). Choose a chamber with \(2(v_+-v_-)/y\notin\mathbb Z\). The zero Fourier mode in the real elliptic variables of the completion is

\[
A(y,v_-)-\sigma,
\quad A=E(-2v_-/\sqrt y),
\]

where \(\sigma\) is chamberwise constant. Directly,

\[
F(A-\sigma)=\frac{yv_-}2A_{v_-}
=-2v_-\sqrt y\,e^{-4\pi v_-^2/y}.
\]

This is nonzero when \(v_-\ne0\). Distinct lattice vectors have distinct elliptic Fourier characters because \(B\) is nondegenerate. Thus other Fourier modes cannot cancel this coefficient. The normally convergent Fourier expansion justifies the uniqueness argument. This establishes nonvanishing on the actual theta function, not only nonvanishing on an isolated formal summand.

The printed WR15 incomplete-gamma normalization can multiply the nonconstant amplitude by a fixed nonzero scalar; that cannot make this derivative vanish. Nor can the printed isotropic sign's omission of the shift create a compensating ordinary derivative inside a fixed chamber. This audit therefore accepts the source caution as a genuine literal incompatibility, without diagnosing how every source theorem should be restated.

### Relative normalization is essential

The normalized \(E\) in the attempt has limiting values \(\pm1\), matching the sign term. Zwegers's Definition 2.1 and its elliptic-variable formula use exactly this normalized error function and the shift \(\nu+v/y\). Orthogonal products give the attempt's kernel. In contrast, an unnormalized incomplete gamma factor must be divided by \(\sqrt\pi\), or its paired sign factor must be scaled by the same amount. Otherwise the cancellation needed for convergence can fail. An overall nonzero scalar is harmless; a relative scalar is not. The attempt explicitly chooses the correct relative normalization, so this does not undermine its own kernel computation.

## 6. Rank-one extension and all-rank faithfulness

The module \(M=A_1/A_1(xd)\) is a quotient by a left ideal. Replacing that ideal by a two-sided ideal would be a fatal change: the Weyl algebra is simple. The author's convention is explicit and correct.

Let \(e_n=x^nv\) for \(n\ge0\), and \(e_{-b}=d^bv\) for \(b\ge1\). The action is well defined on a vector space with this basis:

- \(xe_n=e_{n+1}\) for \(n\ge0\)
- \(xe_{-1}=0\), and \(xe_{-b}=-(b-1)e_{-(b-1)}\) for \(b\ge2\)
- \(de_n=ne_{n-1}\) for \(n\ge1\)
- \(de_0=e_{-1}\), and \(de_{-b}=e_{-(b+1)}\)

The Weyl relation holds at the exceptional weights \(0,-1\) as well as elsewhere. These formulas construct an inverse to the proposed quotient presentation, proving that the displayed spanning vectors really are independent. The subspace on negative labels is \(Q=A_1/A_1x\); the quotient is \(P=A_1/A_1d\).

A lift of the polynomial vacuum to \(M\) has the form \(v+w\), where \(w\) is a finite sum of the negative-label vectors. Its \(d\)-image always has coefficient one at \(e_{-1}\). Hence no lift is killed by \(d\), and the extension does not split.

In the tensor module, \(N_j=x_jd_j\) have one-dimensional joint eigenspaces. Polynomial interpolation in their eigenvalues isolates a nonzero component of any nonzero vector. Positive directions can be moved to weight zero. Each negative direction can be moved to weight \(-1\), with no vanishing step if the correct direction is chosen. Thus every nonzero submodule contains the tensor vacuum of

\[
S=P^{\otimes p}\otimes Q^{\otimes r}.
\]

This proves that \(S\) is simple and essential, and that the full module is indecomposable. Tensoring the rank-one filtrations gives precisely \(2^r\) simple composition factors.

### No special-lattice or theta cancellation gap

Applying all negative lowerings to the completed theta kernel removes every sign term and leaves

\[
\prod_{j>p}(-2\sqrt{-m_jy})
\sum_{\nu\in L}\exp\!\left(\sum_{j>p}4\pi m_j(v_j+y\nu_j)^2/y\right)
 e^{2\pi i(q(\nu)\tau+B(z,\nu))}
\]

in the zero discriminant component. This Gaussian series is smooth and locally normally convergent everywhere on the Jacobi half-space. At \((\tau,z)=(i,0)\) it is a nonzero real constant times

\[
\sum_{\nu\in L}e^{-2\pi q^+(\nu)}>0.
\]

The zero vector alone contributes one before multiplication by the nonzero prefactor. This argument is valid even when the original theta function has a pole at that point: only the smooth shadow is evaluated there. It also applies without an integral direct-product splitting of \(L\). If the image of the socle vanished on a chosen open chamber, its globally real-analytic Gaussian formula would vanish identically, contradicting this positive value.

The surjection from the abstract tensor module to the cyclic theta module therefore has zero kernel: a nonzero kernel would contain the essential socle. This proves both the exact module description and the full cyclic annihilator. No arbitrary scalar combination of discriminant components or torsion-point specialization is covered; such specializations could have cancellations and are not what the attempt asserts.

## 7. Induction parameter and the socle injection

For the upper triangular Borel, conjugation on the unipotent coordinate is multiplication by \(a^2\), so its half-modulus is \(|a|\). Under the stated left-equivariant/right-translation model,

\[
f(bg)=|a|^{s+1}\operatorname{sgn}(a)^\epsilon f(g).
\]

Constants therefore belong at \(s=-1,\epsilon=0\). They are a subrepresentation, not merely a quotient. No opposite-parabolic or unnormalized parameter convention has been substituted.

The tensor identity is also correct. For \(v\otimes f\), the function \(j\mapsto f(g)\omega_B(j)v\) has the required left transformation under \(\widetilde B_2\ltimes H_B\), and right translation applies \(\omega_B(j_0)\) to \(v\) and right translation by \(g_0\) to \(f\). The Heisenberg determinant in the parabolic modulus is one; it contributes no extra shift.

The socle's joint vacuum is killed by \(L_j\) in positive directions and \(R_j\) in negative directions, exactly as the Gaussian

\[
G(t)=\exp(-2\pi\sum_j|m_j|t_j^2).
\]

Its Cartan weight is \((p-r)/2=n/2-r\), agreeing with the weight obtained by applying all \(r\) negative lowerings to the theta generator. Sending that nonzero theta shadow to \(G\) extends to the stated infinitesimal isomorphism of socles. Tensoring with the constant function gives the required injection.

The algebraic polynomial-Hermite span is generally smaller than the entire compact-Cartan-finite subspace of the indefinite oscillator: fixed total weights can contain infinitely many Hermite indices. The attempt correctly avoids an admissibility claim. At the smooth level the completed oscillator has the unambiguous group injection \(v\mapsto v\otimes1\). This proves the precise principal-series relation promised by the partial result, while leaving the full extension untreated by induction.

## 8. Ordinary smooth and distribution-vector obstruction

For \(m_j<0\), put \(q_j=4\pi|m_j|>0\). In its Schrödinger coordinate,

\[
R_j=\tfrac12(\partial_t+q_jt),\qquad
L_j=\tfrac12(\partial_t-q_jt),\qquad
R_jL_j=-\beta_j(N+1).
\]

Its Hermite eigenvalues are \(-\beta_j(\ell+1)\), never zero. The inverse is diagonal multiplication by \(-1/(\beta_j(\ell+1))\). It is continuous on the Schwartz space and on its tempered-distribution dual. The same inverse tensored with the identity acts continuously in every other oscillator variable and in any smooth multiplicity representation. In the principal-series compact model this includes the smooth section space on the compact quotient of the maximal compact subgroup.

On distribution vectors, the relevant space is the strong dual of the smooth contragredient, not the space of all distributions on an arbitrarily chosen noncompact chart. Transposition reverses the operator order and changes the central-character realization; the resulting dual operator still has the same nonzero Hermite spectrum. Equivalently one uses the direct Hermite expansion in tempered distributions, with distribution-valued coefficients in the compact principal-series variable. There is therefore no hidden dual-order kernel.

The theta generator is killed by \(R_jL_j\). Its image under any infinitesimal intertwiner into either ordinary target is killed by an invertible operator, hence is zero. Cyclicity then makes the entire intertwiner zero. This is stronger than merely excluding injective maps, and the parameter is irrelevant. The proof also excludes extending the socle injection to the full module.

The category extension through Sun's theorem is valid with its stated smooth Fréchet/moderate-growth and nondegenerate unitary central-character hypotheses. A closed smooth subquotient that remains in that category has the same tensor description. No assertion about arbitrary nonclosed algebraic subquotients follows, and the attempt correctly disclaims one.

A useful adversarial domain control is

\[
f(t)=e^{q_jt^2/2}.
\]

It is a nonzero ordinary smooth function with \(L_jf=0\), hence \(R_jL_jf=0\). It is not tempered. The independent test includes this example. Thus the spectral argument would fail in an unrestricted smooth-function, meromorphic, hyperfunction, or exponential-growth category. The attempt's definition of distribution vectors and its explicit category boundary are essential, not cosmetic.

Similarly, taking a pole or chamberwise function and extending it as a distribution can add terms supported on the singular locus when differentiated. A chamberwise annihilator cannot simply be promoted to a global distribution-vector equation.

## 9. Reproducibility and negative controls

The following describes the completed audit's historical checks. Edition preparation rechecked frozen byte identities and publication integrity but did not rerun the original mathematical programs or perform new scholarly retrieval, source-text inspection, or literature search. The full analytic arguments remain in this proof and audit; no analytic verdict depends on an omitted executable or raw output. Programs, raw outputs, datasets, copied source documents/text/images, and private coordination material are excluded from this proof-only edition.

The independent script checks 29 assertions under both ordinary Python and Python `-O`. These include universal differential-operator coefficient identities in ranks one and two, residual heat expansion, the coordinate Casimir shift, a full exponential-times-error-function Fourier term, and exact Hermite eigenvalues at symbolic positive frequency. The checks do not import the frozen author's implementation.

Negative controls intentionally reject:

- omission of the Casimir's weight-dependent scalar
- failure to update the weight in successive covariant operations
- the source's extra ordinary-lowering assertion
- extending the no-kernel claim to unrestricted smooth functions

The author's 14 supporting checks were separately replayed in both modes and passed. Frozen-manifest verification was also repeated in both modes, including its tamper, duplicate-entry, and source-path controls. The audit seal separately rejects tampering, missing or duplicate payload entries, unsafe/source paths, external target-hash mismatch, and an upgraded full-solution verdict.

A checker-development transcription initially confused barred/unbarred derivatives in the coordinate Casimir; visual reinspection of CR equation (2.4) corrected that transcription before the final independent runs. No discrepancy in the authored proof was inferred from that transient checker error. Final runs are the sealed evidence.

Finite computational checks support, but do not replace, the general-rank algebra, analytic majorant, essential-socle argument, or continuous-inverse proof supplied above.

## 10. Acceptance boundary

The following remain unresolved by this attempt and by this audit:

- an explicitly defined larger meromorphic/localized induced realization retaining the full extension
- its global intertwining maps, singular support or boundary-value interpretation, and analytic topology
- analytic coverage for every irrational-isotropic datum allowed by the abbreviated OWR announcement
- a complete reconciliation or corrected restatement of all source claims involving the ordinary lowering kernel
- novelty and exhaustive current literature status

The original source already credits the Schrödinger–Weil-extension viewpoint. This audit accepts a correct, explicitly delimited partial mathematical result, not a solution of the original broader connection problem.
