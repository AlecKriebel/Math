# The graded Lie algebra of the seven-dimensional one-point extension

**30002879 / OWR-13681-013. Complete candidate for the source's intended module; independent review pending. Two substantive approaches. Priority unestablished.**

## 1. Exact algebra, source and answer

Let K be any field of characteristic2. Write
\[
 A=K[x,y]/(x^2,y^2),\qquad M=A/(y)=K[x]/(x^2),\qquad
 B=\begin{pmatrix}A&M\\0&K\end{pmatrix}.
\]
The right K-action on M is scalar multiplication. This is the natural nontrivial permutation module KZ₂ in the source: one generator of Z₂×Z₂ acts regularly on KZ₂ and the other acts trivially; x and y are those group generators minus1. Choosing a different nontrivial group quotient merely changes generators of the elementary abelian group.

This module convention is not inferred from the triangular display alone. Hermann, arXiv:1411.0836v2, Section9.6 and Lemma9.7, explicitly identifies the same one-point extension with the seven-dimensional EI-category example of Xu. In its two-arrow permutation module, g interchanges the arrows and h fixes them. Xu's Section3.1 gives the same action. Depending on category-algebra composition conventions the arrows describe a right module; passage to the opposite algebra gives the displayed left-module convention. In characteristic2 the opposite-algebra sign in the Gerstenhaber bracket is immaterial. We compute the displayed triangular algebra directly. The trivial two-dimensional module is a different algebra and is not silently substituted.

Put
\[
 R=K[x,y,u,v]/(x^2,y^2),\qquad |x|=|y|=0,\quad |u|=|v|=1,
 \qquad L=K\cdot1+(y,u)R. \tag{1}
\]
The answer is the graded Lie algebra L with bracket of cohomological degree−1
\[
 [F,G]=F_xG_u+F_uG_x+F_yG_v+F_vG_y. \tag{2}
\]
All coefficients are in K, hence integer coefficients are reduced modulo2. Formal differentiation is well defined modulo x²,y² since those derivatives vanish in characteristic2. In fact the identification also respects the cup product. Equation(2), not just the graded dimensions, specifies the entire Lie structure.

A homogeneous basis is
\[
 HH^0(B):\quad 1,y,xy;
\]
\[
 HH^n(B):\quad x^a y^b u^i v^j,
 \quad a,b\in\{0,1\},\ i+j=n,\quad i\ge1\text{ or }b=1,
 \quad n\ge1. \tag{3}
\]
In particular dim HH⁰(B)=3 and dim HHⁿ(B)=4n+2 for n>=1. For two nonconstant basis monomials the complete structure constants are
\[
\begin{aligned}
[x^ay^bu^iv^j,x^cy^du^kv^l]
={}&(ak+ci)x^{a+c-1}y^{b+d}u^{i+k-1}v^{j+l}\\
&+(bl+dj)x^{a+c}y^{b+d-1}u^{i+k}v^{j+l-1}. \tag{4}
\end{aligned}
\]
A zero coefficient contributes no term; a term with x- or y-exponent at least2 is zero. Negative exponents can occur only in terms with zero coefficient and are discarded. The unit brackets to zero. Formula(4) handles all degrees, including degree0 against positive degrees. The shifted space HH*(B)[1] is the corresponding graded Lie algebra in degree-zero bracket convention.

The source is Reiner Hermann's Question5, OWR24/2015, printed p.1363. It asks for this Lie algebra and whether the coefficient long exact sequence for I=BeB can be used, with e the lower-right idempotent. **Yes:** its map gamma:HH*(B)->HH*(A) is injective and has precisely image L. After computing this image, the Lie bracket is inherited without an extension ambiguity. A sequence of vector-space dimensions alone would not determine a Lie bracket; the multiplicative/brace-compatible comparison map is essential.

Prior credit: Xu2008 already computed the cohomology ring of this example and its non-finite-generation consequence. The group-algebra Gerstenhaber calculation is classical and is restated in Hermann Section9.4. Happel's sequence and the structure-preservation results are also prior work, as documented in Hermann Proposition6.12. We reconstruct the characteristic map and the full resulting bracket here. This does not establish novelty of the explicit presentation.

## 2. The ambient Hochschild algebra and its bracket

We recall enough chain-level detail to fix the coordinates in(1), rather than apply an unspecified polynomial-ring isomorphism.

For D=K[t]/(t²), its free D-bimodule resolution has one generator e_n in each degree n>=0 and differential multiplication by t_left+t_right in every positive degree. Indeed, in D^e the square of this element is zero, and its image and kernel both have K-dimension2; the augmentation is multiplication D^e->D. Tensor the x and y resolutions over K. The resulting free A-bimodule resolution P has
\[
 P_n=\bigoplus_{i+j=n}A^e e_{i,j},\qquad
 d e_{i,j}=(x_L+x_R)e_{i-1,j}+(y_L+y_R)e_{i,j-1}, \tag{5}
\]
with missing negative-index summands zero. It is a resolution by the tensor-product theorem over a field. Applying Hom_{A^e}(-,A) makes the differential zero, so each summand contributes one copy of A.

Let u be the class of the derivation partial_x and v the class of partial_y. These derivations are valid in characteristic2. The comparison from(5) to the normalized bar resolution sends e_{i,j} to the sum of all words with i occurrences of x and j occurrences of y, with outer coefficients1. Terms involving adjacent unlike letters cancel in pairs, while xx and yy are zero, so the differential is exactly(5). This is also the usual shuffle comparison of the two one-variable resolutions.

The cup cochain (partial_x)^{cup i} cup (partial_y)^{cup j} evaluates to1 on e_{i,j} and to0 on the other degree i+j summands: only the word with the first i entries x and the last j entries y contributes. Thus a u^i v^j corresponds exactly to coefficient a on e_{i,j}. These classes give the polynomial presentation HH*(A)=R, with no additional relations; the dimension in every degree follows from(5).

On degree1 classes the Gerstenhaber bracket is the commutator of derivations, and bracketing a derivation with a degree0 element is evaluation. Therefore
\[
 [u,x]=[x,u]=1,\quad [v,y]=[y,v]=1,
\]
and every other bracket between x,y,u,v is zero. The Gerstenhaber biderivation identity, with all signs equal to1 in characteristic2, gives(2) for arbitrary polynomials. This also recovers the credited ambient formula in Hermann Section9.4.

## 3. The characteristic map to Ext_A(M,M)

An A-projective resolution Q of M has Q_n=A for every n>=0, differential multiplication by y in each positive degree, and augmentation A->A/(y). Exactness follows from ker(y:A->A)=yA. After applying Hom_A(-,M), all differentials vanish. The identity shifts between copies of A lift the degree1 extension class, so Yoneda multiplication gives
\[
 \operatorname{Ext}_A^*(M,M)=M[\eta],\qquad |\eta|=1. \tag{6}
\]

The canonical characteristic homomorphism
\[
 \chi:HH^*(A)\longrightarrow\operatorname{Ext}_A^*(M,M)
\]
is induced by tensoring a bimodule extension on the right with M. It is explicitly
\[
 \chi(x)=x,\quad \chi(y)=0,\quad \chi(u)=0,\quad \chi(v)=\eta. \tag{7}
\]
Here is an all-degree verification. The complex P tensor_A M is a projective left-A resolution of M. Its terms are free as left A-modules because M is finite-dimensional over K; it is exact since a projective bimodule resolution of A is split exact as a complex of right A-modules before tensoring with M. The map
\[
 j_n:Q_n\longrightarrow P_n\otimes_A M,\qquad
 j_n(1)=e_{0,n}\otimes1
\]
lifts the identity on M and is a chain map: the only differential on its image is y_L+y_R, and y_R annihilates1 in M. A class a u^i v^j, represented by the coefficient cochain on e_{i,j}, evaluates after this comparison to zero for i>0 and to (a mod y)eta^j for i=0. This proves(7) in every degree and fixes its normalization. In particular chi is surjective in every degree and
\[
 \ker\chi=(y,u)R. \tag{8}
\]

No inference from a few low-degree dimensions is used in this step.

## 4. Injectivity, the degree-zero exception, and the original sequence

The standard one-point-extension exact sequence is
\[
0\to HH^0(B)\to HH^0(A)\oplus K
 \xrightarrow{(a,c)\mapsto \bar a-c} \operatorname{End}_A(M)
 \to HH^1(B)\to HH^1(A)\xrightarrow{\chi_1}\operatorname{Ext}_A^1(M,M)\to\cdots. \tag{9}
\]
The subsequent maps HHⁿ(A)->Ext_Aⁿ(M,M) are chi_n. This is Happel's sequence, with the characteristic-map and Gerstenhaber compatibility recorded in Hermann Proposition6.12. Since End_A(M)=M and the degree-zero map in(9) is onto, and since all chi_n are onto by(7), every map HHⁿ(B)->HHⁿ(A) is injective for n>=1, with image ker chi_n.

At degree zero, the center of B consists of diagonal pairs(a,c) satisfying a mod y=c. Their off-diagonal component is zero, since commuting with the two vertex idempotents kills it. Thus projection onto A is injective and has image K+yA. Combining degree0 and the positive degrees gives exactly K+ker chi=L.

We now identify this with the map gamma in the *original* coefficient sequence, rather than replace that sequence by an unrelated one. Let f=1-e and E=Kf+Ke, a separable subalgebra of B. Use the normalized E-relative bar resolution. Relative cochains with values in B have an all-A-input/A-output component and a mixed component with one M input. Projection onto the former is the usual restriction map in(9).

With coefficients in A=B/I, there is only the all-A-input/A-output component: E-bimodule linearity forces every mixed component and every e-corner output to zero. Hence the entire relative cochain complex with coefficients A identifies with the normalized Hochschild complex of A. The coefficient map B->A is exactly the projection just described. Relative bar cohomology agrees with ordinary Hochschild cohomology because E is separable over K. Therefore the gamma in the question coincides with this injective map.

There is also direct bracket compatibility on these relative cochains. Restricting a brace or insertion to all-A inputs only involves all-A intermediate outputs. Thus restriction commutes with the cup product and every insertion, and hence with the Gerstenhaber bracket. This is consistent with the source's Lemma4 and Hermann's general theorem, but here the triangular decomposition makes the identification explicit.

For clarity, e is stratifying: eBe=K, and Be tensor_K eB -> BeB is visibly an isomorphism; all higher Tor over K vanish. Thus the coefficient sequence in the question is applicable. Its other terms can now be read from exactness:
\[
\operatorname{Ext}_{B^e}^0(B,I)=0,\quad
\operatorname{Ext}_{B^e}^1(B,I)\cong A/(K+yA)\cong M/K,
\]
\[
\operatorname{Ext}_{B^e}^{n+1}(B,I)\cong HH^n(A)/L_n\cong M\eta^n\qquad(n\ge1). \tag{10}
\]
The maps from these Ext groups back into HH*(B) vanish, since gamma is injective. These descriptions use the computed comparison map and exactness; they do not claim that the coefficient Ext groups themselves come with the same Lie bracket.

## 5. Lie closure and complete structure constants

The ideal I_0=(y,u) in R is closed under the bracket of two of its elements. Indeed, its two generators bracket to zero, and the biderivation identity implies [I_0,I_0] subset I_0: in the expansion of [yF,uG], for example, every term still contains y or u. The same applies to [yF,yG] and [uF,uG]. Adding scalar constants changes nothing. Thus L is a graded Lie subalgebra, as is also forced by the injective Hochschild restriction.

Applying(2) to monomials gives(4). Counting(3) gives 4n contributions with i>=1 and two with i=0,b=1, hence4n+2 for n>=1. In degree0 only1,y,xy occur; x alone must not be included. These formulas determine brackets involving all degrees and all coefficient fields of characteristic2. For example [u,xu]=u and [yv,y]=y, while [u,y]=0. They also show why identifying only a nilpotent quotient, or only HH¹, would not answer the source.

The requested Lie algebra has therefore been completely specified. This result does not purport to describe every additional characteristic-two squaring or higher brace operation; those are extra structures beyond the Lie bracket asked for here.

## 6. Verification and provenance

The accompanying exact checker independently forms the E-relative normalized Hochschild differential of the seven-dimensional algebra in low degrees, checks the resulting dimensions, verifies explicit degree1 derivation lifts and their commutators, and tests the all-degree bracket formula's closure and Jacobi identity on finite sets of monomials. Resolution and characteristic-map identities are also checked in bounded degrees. These controls are diagnostics; the all-degree proof is Sections2–5.

Primary sources: [original OWR question, p.1363](https://ems.press/content/serial-article-files/46571?nt=1); [Hermann v2, Proposition6.12, Sections9.4/9.6 and Lemma9.7](https://arxiv.org/abs/1411.0836v2), published Adv.Math.299(2016),687–759, DOI10.1016/j.aim.2016.05.022; [Xu, Section3.1](https://arxiv.org/abs/0805.3295), published Adv.Math.219(2008),1872–1893, DOI10.1016/j.aim.2008.07.014. The earlier ring computation and structural machinery are explicitly credited. No claim of first discovery, external validation, or human peer review is made.
