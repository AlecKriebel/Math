# Ohtsuki Problem 7.24: a credited relationship with the original normalization

**Record:** 10400139 / AMR-103-0139. **Author budget:** one substantive turn.
**Proposed disposition:** already solved in the literature, subject to separate full review.
No new invariant, new Jones comparison theorem, or priority claim is made.

## 1. Which invariant is being compared?

Ohtsuki's Section 7.4, printed pp.485–487, concerns a nonempty link in a closed oriented three-manifold, a flat upper-triangular Borel bundle, and odd integers N>1. Its invariant is the Nth power of a state sum, and its reference [43] is Baseilhac–Benedetti, math/0101234. On S³ the bundle is trivial. The question asks for the actual relationship to the N-color Jones evaluation at ζ=exp(2πi/N), with unknot value one. The guess in the following remark is not an additional hypothesis.

Write K_N^old for the invariant defined by equation (2) of math/0101234v2, with its stated orientation convention. The answer in that literal convention is

\[
\boxed{K_N^{\rm old}(S^3,L)=N^{-2N}\,J_N(L)^N.}\tag{1}
\]

Equivalently, put \(\widehat K_N=N^{2N}K_N^{\rm old}\). Then
\[
\widehat K_N(S^3,L)=J_N(L)^N,
\qquad K_N^{\rm old}(S^3,U)=N^{-2N}.\tag{2}
\]
Here U is the unknot. The relationship holds for **all nonempty links**, including split links and zeros of J_N. No division by a link invariant is performed. There is no extension of the old definition to even N in this statement.

The power, normalization and orientation dictionary matter. Kashaev's original normalized three-dimensional sum has a factor N^(2−V); the 2001 sum has N^(−V). The later 2011 letter K_N denotes an **unpowered**, normalized sum, and its orientation convention gives a mirror. The general 2011 quantum hyperbolic invariant H_N has an additional sign ambiguity; it cannot simply be raised to the odd power N to obtain (1).

The substantive theorem identifying the Kashaev/Jones invariants is credited to Kashaev and Murakami–Murakami. Baseilhac–Benedetti (2011) supplies the detailed all-link quantum-hyperbolic comparison, including a root-only version in Corollary 4.6. The argument below supplies the explicit dictionary for the original source's symbols.

## 2. Original state sum and admissible specialization

Fix N=2m+1 and let half=(N+1)/2 denote 1/2 in Z/N. Choose a quasi-regular triangulation T with a Hamiltonian link subcomplex H, a total ordering of its vertices, a full unipotent coboundary cocycle, and an integral charge. This is an admissible special case of the old construction: the bundle on S³ is trivial, and an injective complex-valued vertex cochain gives a full cocycle. Existence and invariance under choice of such data are the published old construction, not an assumption that an arbitrary diagram satisfies its constraints.

Write V for the number of vertices, X(e) for the nonzero upper diagonal cocycle entry and y(e)=X(e)^(1/N), with coherent determinations. On a tetrahedron ordered 0,1,2,3 put
\[
X=y_{03}y_{12},\quad Y=y_{01}y_{23},\quad Z=y_{02}y_{13},
\quad u=X/Z,\quad v=Y/Z.
\]
The coboundary relation gives X^N+Y^N=Z^N, hence u^N+v^N=1. Put a=half·c_0 and c=half·c_1 modulo N for the two reduced charges.

Let R and bar-R be the old unsymmetrized 6j matrices. With face indices γ=α_2, δ=α_0, α=α_3, β=α_1, the old charged tensor for positive ordered-simplex orientation is
\[
 t_+=(Z)^m\,\zeta^{c(\gamma-\alpha)-ac/2}
 R^{\gamma-a,\delta}_{\alpha,\beta-a}.
\]
The negative-orientation tensor is
\[
 t_-=(Z)^m\,\zeta^{c(\gamma-\alpha)+ac/2}
 \bar R^{\alpha,\beta+a}_{\gamma+a,\delta}.
\]
All halves in exponents are taken modulo N. These are the original Proposition 8.5 and equation (7); the 2001 paper calls positive ordered-simplex orientation “index −1”, while the 2002 paper calls it “index +1”. The tensor assigned to it is R in both papers.

The original scalar before taking its Nth power is
\[
 H_N^{\rm old}(T)=N^{-V}
 \prod_{e\notin H}y(e)^{1-N}
 \sum_{\text{face states}}\prod_{\Delta}t_{\sigma(\Delta)}.\tag{3}
\]
Thus K_N^old=(H_N^old)^N. The negative exponent in the edge factor is explicit in the 2001 defining equation and the long 2002 paper, equation (7).

## 3. A closed-triangulation gauge comparison with Kashaev's tensors

This step uses the original Kashaev tensors, whose phase ambiguity is only an Nth root, rather than the later general H_N with a possible sign.

For a regular pair p,q of unipotent cyclic parameters, both papers' Clebsch–Gordan operators have the same state-dependent entries
\[
 \zeta^{\alpha j}\,\omega(x_q,x_p,x_{pq}\mid i,\alpha)
 \delta_{k,i+j}.
\]
Their scalar normalizations differ. Kashaev (1994), (1.13), uses
\[
 \nu_K(p,q)=\langle pq,q\rangle^{1/2},
\]
whereas the old Baseilhac–Benedetti normalization uses
\[
 \nu_o(p,q)=h_o(x_{pq}/x_q),\qquad
 h_o(z)=z^{-m}\frac{\prod_{j=1}^{N-1}(1-z\zeta^j)^{j/N}}
 {\prod_{j=1}^{N-1}(1-\zeta^j)^{j/N}}.
\]
Choose nonsingular parameters, which is enough by invariance and continuation. Set f(p,q)=ν_o(p,q)/ν_K(p,q). Changing these bases multiplies the positive 6j matrix by
\[
 Df(p,q,r)=\frac{f(p,q)f(pq,r)}{f(q,r)f(p,qr)};\tag{4}
\]
it multiplies the inverse matrix by (Df)^−1. This follows immediately by substituting the four scalar basis changes in the defining intertwiner equation, which is (1.19) in Kashaev and (5) in the old paper. Branch choices in the displayed h formulas can at most contribute a tetrahedron-dependent Nth root; they never depend on a face state.

The additional charged normalization is also a face gauge. Kashaev's zero-charge positive tensor is x_qr^(2m)R_K, and the negative tensor is x_pq^(2m)bar-R_K, by (3.4) of the 1994 paper. The charged state-dependent entries are displayed in (4.6)–(4.7) of the 1995 paper. They agree with those in Section 2 above; the two conventions for the scalar ac/2 differ only by ζ^(−ac) for the positive tensor and ζ^(ac) for the negative tensor. In particular, there is no state-dependent factor left over.

Since Z=x_pq x_qr, the ratio of the old positive tensor to Kashaev's positive tensor is, up to that Nth root,
\[
 Df\,(x_{pq}/x_{qr})^m = Dg,
 \qquad g(p,q)=f(p,q)x_{pq}^{m}.\tag{5}
\]
For the negative tensor the ratio is (Dg)^−1. The identity in (5) follows because
\[
 \frac{x_{pq}^m x_{pqr}^m}{x_{qr}^m x_{pqr}^m}
 =(x_{pq}/x_{qr})^m.
\]
This comparison also removes any square-root sign introduced by the auxiliary CG basis: it occurs within the face gauge g and cancels on a closed triangulation.

On a globally ordered closed oriented triangulation, each triangular face appears twice with opposite boundary sign. Consequently
\[
 \prod_{\Delta}(Dg(\Delta))^{\sigma(\Delta)}=1.\tag{6}
\]
This is cancellation of the four face factors, not a claim that a local factor is one. It holds for each face state, so it also holds after summation. The remaining product of local ζ phases is itself an Nth root and is independent of the state.

Kashaev's cocycle sign convention can be matched by negating the chosen vertex cochain. Reversing the sign of an edge root contributes (−1)^(N−1)=1 to the off-link edge factor, since N is odd. His “right” tetrahedron, viewed from vertex 3 toward the counterclockwise face 012, has positive ordered-simplex orientation. It is therefore assigned the same R tensor as in the old convention. This comparison does not reflect L.

Let S_N^K(T) be Kashaev's normalized three-dimensional sum, equation (4.4) of the 1994 paper. Its remaining global factors agree with (3), except that the vertex factor is N^(2−V). Equations (5)–(6) give the **root-only** equality
\[
 H_N^{\rm old}(T)\equiv_{\mu_N}N^{-2}S_N^K(T),\qquad
 K_N^{\rm old}=N^{-2N}(S_N^K)^N.\tag{7}
\]
The second equality is exact. No possible sign has been discarded by taking an odd power.

## 4. The published all-link comparison and the later mirror convention

Kashaev (1995), Theorem 1(2), identifies the Nth power of his planar invariant with Q(S³,L)=(S_N^K)^N for odd N. Murakami–Murakami, Theorem 4.9, identifies the enhanced Kashaev invariant with J_N(L) for every link and every N≥2, with the unknot normalization used here. Combining those statements with (7) gives (1).

There is an important historical qualification: the early comparison/invariance literature left details insufficiently explained. Baseilhac–Benedetti (2011), Remark 2 on p.33, explains why they provide an independent complete proof. Their Section 4 revisits the three-dimensional Kashaev sum and Corollary 4.6, p.65, states the all-link equality with **only powers of ζ_N** remaining. Thus the conclusion is supported by the later detailed result and is not based solely on an earlier informal identification of notation.

For clarity, the later conventions work as follows:

* 2011 equation (30) uses N^(2−V), the normalization of S_N^K. Its K_N is an unpowered scalar, unlike Ohtsuki's K_N.
* 2011 Remark 3 changes the tetrahedron-orientation sign relative to the older BB conventions. Their Corollary 4.6 identifies this later scalar with the Jones/Kashaev invariant of the mirror of L. Applying the later convention to −S³, equivalently the mirror link, gives the original oriented convention used in (7).
* Theorem 1 of that paper alone would allow a sign. Corollary 4.6 explicitly removes that additional ambiguity for the Kashaev sum. Equation (7) has independently tracked its root-only gauge.
* The updated quantum hyperbolic H_N and the Borel/Kashaev state sum have different local symmetrizations. One cannot identify them on every three-manifold merely from their names. Only the all-link S³ specialization is used here.

This also explains why quoting the 2004 Theorem 5.1 without a normalization audit would conceal a universal factor in the literal 2001 definition. The corrected convention dictionary is the point of this packet, not a purported new all-link theorem.

## 5. A second local conversion check

The separate `gauge_check.py` checks (4)–(5) against both explicit finite-sum scalar formulas (1.25) and (1.29) in Kashaev (1994), including all reduced charge pairs for N=3,5,7,9,11 and complex as well as positive-real parameters. It passes 2,925 90-digit diagnostics. These are numerical controls, not the cellular proof.

The computational checks also compare the old charged matrices with the cyclic-dilogarithm matrices in 2011, independently of the CG face cancellation above.

Write
\[
 h_n(u)=\frac{\prod_{j=1}^{N-1}(1-u\zeta^{-j})^{j/N}}
 {\prod_{j=1}^{N-1}(1-\zeta^{-j})^{j/N}}.
\]
Then
\[
 h_o(1/u)^N=h_n(u)^N.\tag{8}
\]
Indeed, pairing each numerator and denominator factor gives
(1−ζ^j/u)/(1−ζ^j)=u^−1(1−uζ^−j)/(1−ζ^−j), and Σj=mN cancels the prefactor u^(mN). This proves that the phase is in μ_N, not merely μ_(2N).

For u^N+v^N=1, the cyclic product satisfies
\[
 \omega(u,v\mid r+s)=\omega(u,v\mid r)\omega(u\zeta^r,v\mid s),
\quad h_n(u\zeta^a)\equiv_{\mu_N}h_n(u)\omega(u,v\mid a).
\]
The latter follows either from 2011 Lemma 6.1(iv), or by comparing the integer exponents of each factor 1−uζ^t after raising to N. It converts the positive charged tensor to Z^m L_N(uζ^(−a),vζ^c), up to a state-independent Nth root. The negative tensor converts to Z^m L_N(uζ^a,vζ^(−c))^−1. Its extra scalar cancels by
\[
 \frac{[u]}{[u\zeta^a]}
 \frac{\omega(u,v\mid a)}{\omega(u/\zeta,v\mid a)}
 =\frac{1-u\zeta^a}{1-u}\frac{1-u}{1-u\zeta^a}=1.
\]
This checks both signs, the half-charge shifts and the absence of a hidden scalar modulus. It is a diagnostic dictionary, not a replacement for the published global theorem.

## 6. Boundary cases and a direct unknot control

* The empty link and even N are outside the original construction and are not claimed.
* For a split link with at least two nonempty parts, the normalized Jones specialization is zero, hence the old invariant is zero. Formulas (1) and (7) remain meaningful. No logarithm, asymptotic conjecture, or division by J_N is needed.
* For the unknot, (7) and the established normalized value S_N^K(U)=1 modulo μ_N give K_N^old(U)=N^(−2N). Thus the guess without the factor cannot hold for the literal equation (2) normalization.
* Choose orientations of link components when defining the standard enhanced, ambient-isotopy Jones invariant. The comparison is to that convention, with unknot value one and all colors N. The resulting Nth power agrees with the old unoriented-link invariant by (7). We do not assert that the unpowered multicomponent Jones value is independent of arbitrary component-orientation choices; any root phase allowed by those choices disappears in the stated Nth-power relationship.

The direct checker `unknot_check.py` uses the boundary of the ordered four-simplex. The Hamiltonian cycle 01,12,23,34,40 bounds the embedded fan of faces 012,023,034, so it is an unknot. It constructs the old tensors directly, with five integer charge triples, sums all 3^10=59,049 face states, and obtains H_3^old=1/9 and K_3^old=1/729 to 80-digit precision. The gauge cancellation on this closed triangulation is checked exactly. This finite complex computation is not an interval proof and does not establish the arbitrary-N theorem; it is a stringent check of the normalization in (1).

## 7. Source errata and disposition

The short 2002 survey prints a positive exponent (N−1)/N on its off-link edge product. This differs from the negative exponent in the original 2001 definition and the long 2002 formula. It also conflicts with the short survey's own projective-invariance assertion if read literally with the referenced tensors: the tetrahedral scaling and edge scaling would add instead of cancel. We therefore bind K_N^old to Ohtsuki's defining reference [43], not to that isolated displayed sign. `SOURCES.md` records this discrepancy explicitly.

The mathematical relationship is already established by the credited literature, with the source normalization made explicit here. This packet requests independent review of the exact convention bridge before any status promotion. Adjacent Problems 7.21 and 7.25, involving global phase refinements and asymptotics, are separate questions and are not resolved by this argument.
