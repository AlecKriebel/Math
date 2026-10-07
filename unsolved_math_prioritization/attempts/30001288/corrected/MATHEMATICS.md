# Five mathematical approaches to the connected comparison

All varieties in Approaches 1–4 are smooth, connected, and projective over \(\mathbf C\), unless a different object is explicitly introduced. We use the notation and rational conventions of `FORMULATION.md`. Classical inputs are credited; the special-case applications are not claimed to be new. Source retrieval, the inherited-attempt gate, the literal wording defect, and packaging are not counted as author approaches.

## Approach 1. Divisors: calculate the representing sheaf

**Goal.** Establish the comparison by constructing the two targets algebraically when \(p=1\), rather than comparing only their dimensions.

Let \(X\) be smooth projective. On a smooth test scheme \(U\), codimension-one Chow classes on \(U\times X\) are line bundles. The relative Picard functor is the sheafification of

\[
U\longmapsto\operatorname{Pic}(U\times X)/\operatorname{Pic}(U).
\]

The pullback term from \(U\) disappears under sheafification because line bundles are locally trivial. Thus \(F_X^1\) is the rationalized Picard sheaf. This identification respects pullbacks and transfers: norm of line bundles is the codimension-one transfer. A complex point of \(X\) gives rigidification, and the ordinary relative Picard scheme represents the resulting sheaf.

The exact sequence

\[
0\to\operatorname{Pic}^0_X\to\operatorname{Pic}_X
 \to\underline{NS^1(X)}\to0
\]

has an abelian variety on the left and a finitely generated discrete group on the right. Therefore \((\operatorname{Pic}_X)_{\mathbf Q}\) is 1-motivic. The reflector fixes it, giving

\[
A_X^1=(\operatorname{Pic}^0_X)_{\mathbf Q}.
\]

The divisor morphic Abel–Jacobi map is the classical divisor map [W, Example 5.5]. For divisors the latter sends a line bundle algebraically equivalent to zero to its point of \(\operatorname{Pic}^0_X\); its target is exactly \(\operatorname{Pic}^0_X(\mathbf C)\). The identity on these line bundles supplies the canonical isomorphism after rationalizing.

**Result.** The repaired comparison holds for divisors on every smooth projective complex variety, with full source \(\operatorname{Pic}_X\) and connected source \(\operatorname{Pic}^0_X\) explicitly distinguished. This agrees with [ABV, Proposition 3.3.2] in the relevant degree. The following localization calculation extends this first approach to every smooth punctured projective curve.

### Localization control: an open curve and its boundary periods

Let \(C\) be a smooth connected projective curve, \(D=\{p_1,\ldots,p_n\}\) a nonempty set of distinct complex points, and \(U=C\setminus D\). Here \(U\) is the variety whose Chow sheaf we examine; write \(T\) for a smooth test scheme. Chow localization on \(T\times C\), followed by exact rational sheafification, gives

\[
\underline{\mathbf Q}^{n}\xrightarrow{e_i\mapsto[\mathcal O_C(p_i)]}
(\operatorname{Pic}_C)_{\mathbf Q}\longrightarrow F_U^1\longrightarrow0.
\]

Indeed, its first term is the sheaf associated to \(CH^0(T\times D)_{\mathbf Q}\), and the two other presheaves are \(CH^1(T\times C)_{\mathbf Q}\) and \(CH^1(T\times U)_{\mathbf Q}\). The category of 1-motivic sheaves is closed under cokernels [ABV, §1.3], so Alb fixes \(F_U^1\). Choosing \(p_1\) splits the degree map on \(\operatorname{Pic}_C\). In this splitting the boundary columns are \(([p_i-p_1],1)\). Eliminating the degree coordinate yields

\[
F_U^1\simeq
(J(C))_{\mathbf Q}/
\operatorname{im}\left(
\underline{\mathbf Q}^{n-1}\xrightarrow{e_i\mapsto[p_i-p_1]}(J(C))_{\mathbf Q}
\right).
\tag{1.1}
\]

The degree coordinate is entirely killed, so this sheaf is connected. Replacing \(p_1\) changes only the chosen generators of the intrinsic group of degree-zero divisors supported on \(D\).

On the Lawson side, the zero-cycle theorem is
\(L_0H_1(U)=H_1^{\mathrm{BM}}(U,\mathbf Z)\), with Borel–Moore homology; substituting ordinary homology here is an error. Its localization sequence of mixed Hodge structures is

\[
0\to H_1(C,\mathbf Z)\to H_1^{\mathrm{BM}}(U,\mathbf Z)
\to\ker(\mathbf Z^n\xrightarrow{\sum}\mathbf Z)\to0.
\tag{1.2}
\]

The last group has Hodge type \((0,0)\). The boundary map from its \(\Gamma\) group to \(J(H_1(C))\) is precisely the Abel–Jacobi class of a degree-zero divisor supported on \(D\). This follows directly from Walker's definition by the localization extension [W, §3 and Definition 5.2]. Since the Jacobian of a type-\((0,0)\) lattice is zero, the six-term exact sequence gives

\[
J_0^{\mathrm{mor}}(U)=J(C)(\mathbf C)/
\langle[p_i-p_1]:2\le i\le n\rangle_{\mathbf Z}.
\tag{1.3}
\]

Rationalizing (1.3) gives exactly the complex points of (1.1). Evaluation at \(\operatorname{Spec}\mathbf C\) is exact here, so no sheaf-versus-point quotient is being suppressed. Localization compatibility of the Abel–Jacobi map makes this isomorphism compatible with the maps from divisor classes. Every divisor class on \(U\) has a degree-zero lift on \(C\), by adding a multiple of \(p_1\); hence the source is algebraically trivial and these maps cover all classes.

For \(U=\mathbf P^1\setminus D\), both these targets vanish for every \(n\ge1\). In particular, \(U=\mathbf G_m\) gives zero, even though its ordinary generalized Albanese has identity component \(\mathbf G_m\). For \(U=E\setminus\{0,e\}\), with \(E\) elliptic and \(e\) nontorsion, both rational targets are \(E(\mathbf C)_{\mathbf Q}/\mathbf Qe\). The generalized Albanese of this punctured curve instead fits into an extension by a one-dimensional torus. Thus replacing the full cycle-theoretic target of a nonproper variety by its ordinary generalized Albanese would not be a valid localization argument.

This explicit calculation proves the repaired equality for smooth open curves and tests the period-quotient mechanism. General localization has additional terms: [ABV, Proposition 3.3.3] is a long exact sequence of **derived** higher Picard sheaves. Merely applying an underived reflector to an open/closed decomposition does not produce a general five-lemma proof.

**Where this approach stops.** In higher codimension, a Chow variety parametrizing effective cycles is not a representing group scheme for the Chow sheaf. Replacing it by an abelian variety assumes the missing representability/comparison. The line-bundle quotient argument does not generalize by changing the superscript.

## Approach 2. Zero-cycles: duality and the universal Albanese

**Goal.** Use the homological motive rather than the divisor Picard functor.

Suppose \(\dim X=d\), and put \(p=d\). Smooth proper motivic duality gives

\[
\underline{\operatorname{Hom}}(M(X),\mathbf Q(d)[2d])\simeq M(X).
\]

Taking zeroth homotopy sheaves identifies \(F_X^d\) with \(h_0M(X)\). For any 1-motivic sheaf \(G\), homotopy invariance identifies morphisms out of \(h_0M(X)\) with morphisms out of the representable sheaf with transfers. The universal property of the Serre–Albanese scheme then gives

\[
\operatorname{Hom}(\operatorname{Alb}(F_X^d),G)
 \simeq \operatorname{Hom}((\operatorname{Alb}_X)_{\mathbf Q},G).
\]

Hence \(\operatorname{Alb}(F_X^d)\simeq(\operatorname{Alb}_X)_{\mathbf Q}\). This is the \(r=0\) case of the higher-Albanese calculation [ABV, Proposition 3.3.5 and Remark 3.3.6]. The component group is \(\mathbf Q\), induced by degree; its connected kernel is the ordinary Albanese variety rationalized.

On the Lawson side \(r=d-p=0\), so

\[
L_0H_1(X)=H_1(X,\mathbf Z),\qquad
J_0^{\mathrm{mor}}(X)=J(H_1(X,\mathbf Z))
 =\operatorname{Alb}^0_X(\mathbf C).
\]

The zero-cycle comparison and map are the classical Albanese construction [W, Example 5.5]. Both maps send \([x]-[x_0]\) to the based Albanese image of \(x\). Such differences generate degree-zero zero-cycles, so compatibility determines the isomorphism. Its statement on degree-zero cycles does not depend on the chosen base point.

**Result.** The repaired comparison holds for zero-cycles on every smooth projective complex variety.

**Where this approach stops.** For \(0<r<d-1\), the internal Hom used in the higher-Albanese definition need not be the motive of a variety. The degree-zero calculation cannot replace this potentially non-geometric object by \(M(X)\). No conservativity or finiteness statement for that internal Hom has been established here.

## Approach 3. Projective bundles over curves: all codimensions in an infinite family

**Goal.** Move beyond divisors and zero-cycles by using explicit correspondences and projective-bundle decompositions.

Let \(C\) be a smooth connected projective curve, \(m\ge0\), and \(X=C\times\mathbf P^m\). Let \(h\) be the hyperplane class. For \(1\le p\le m+1\), the Chow projective-bundle formula on every \(U\) gives

\[
F_X^p\simeq\bigoplus_{j=0}^{m}F_C^{p-j}h^j.
\]

For \(q>1\), \(F_C^q=0\): its stalk at a function field \(K\) is \(CH^q(C_K)_{\mathbf Q}=0\), and a homotopy-invariant Chow sheaf is determined by these unramified restrictions. For \(q<0\) it is zero by definition. The remaining terms are \(F_C^0=\underline{\mathbf Q}\) and \(F_C^1=(\operatorname{Pic}_C)_{\mathbf Q}\). Thus the full sheaf is

\[
F_X^p\simeq
\begin{cases}
\underline{\mathbf Q}\oplus(\operatorname{Pic}_C)_{\mathbf Q},&1\le p\le m,\\
(\operatorname{Pic}_C)_{\mathbf Q},&p=m+1.
\end{cases}
\]

This is already 1-motivic. Its connected part is always \((J(C))_{\mathbf Q}\). The two independent rational component classes in the interior range are the horizontal and vertical Chow classes; they must not be collapsed to a single degree class.

For the other target let \(r=m+1-p\), so \(0\le r\le m\). The Lawson projective-bundle theorem gives

\[
L_rH_{2r+1}(C\times\mathbf P^m)
\simeq\bigoplus_{i=0}^{m}
 L_{r-i}H_{2r+1-2i}(C).
\]

We use the conventional extension to negative Lawson indices by singular homology, as in [N, Theorem 2.4 and Proposition 2.5]. If \(i>r\), the homological degree is negative, so the summand vanishes. If \(r-i>1\), the curve has no cycles of that dimension. If \(r-i=1\), the top-dimensional cycle space of \(C\) is discrete, so its first homotopy group vanishes. Only \(i=r\) survives, giving \(H_1(C,\mathbf Z)\).

The surviving isomorphism is induced by external product with \([\mathbf P^r]\). This is a morphism of the normalized IMHSs by [W, Theorem 4.22(5)]. The projective-bundle calculation proves that its underlying group map is bijective, so it is an isomorphism in the abelian category of IMHSs; its inverse is therefore also a morphism of IMHSs. On Chow groups, that inverse is intersection with \(h^r\) followed by projection to \(C\). On a term \(\beta\times[\mathbf P^i]\), the projector with exponent \(j\) vanishes for \(j\ne i\): excess intersection gives zero when \(j>i\), and projection of a positive-dimensional fiber gives zero when \(j<i\). For \(j=i\) it returns \(\beta\). This also checks the twist and degree alignment.

Taking Jacobians and using the same correspondence on Chow groups produces the required map-compatible isomorphism

\[
A_{C\times\mathbf P^m}^p(\mathbf C)
 \simeq J(C)(\mathbf C)\otimes\mathbf Q
 \simeq W_{C\times\mathbf P^m}^p
\quad(1\le p\le m+1).
\]

**Result.** The repaired comparison holds in every nontrivial codimension for products of a smooth projective curve with any projective space. For \(m\ge2\) this includes intermediate codimensions, not just the two preceding cases.

**Where this approach stops.** The projective-bundle formula reduces a bundle to its base. It does not reduce an arbitrary smooth projective variety to a curve. A Chow–Künneth decomposition into curve and Tate summands is an additional hypothesis, not a consequence of the comparison problem.

## Approach 4. All curve correspondences: identify the exact missing relations

**Goal.** Construct a common explicit generator group for both targets and isolate the comparison kernel.

Write \(V=CH^p(X)_{\mathrm{alg}}\otimes\mathbf Q\). Range over pairs \((C,\Gamma)\), where \(C\) is a smooth connected projective curve and \(\Gamma\in CH^p(C\times X)\). There is a set of isomorphism representatives. Form

\[
B=\bigoplus_{(C,\Gamma)}J(C)(\mathbf C)\otimes\mathbf Q.
\]

The Abel theorem on curves identifies \(CH_0(C)^0\) with \(J(C)(\mathbf C)\). The correspondence therefore defines \(\gamma_{C,\Gamma}:J(C)(\mathbf C)_{\mathbf Q}\to V\). Their direct sum \(\gamma:B\to V\) is surjective: algebraic equivalence is generated by differences of fibers of curve families; one may normalize and complete the parameter curves, taking the closure of the family. Rational equivalence has already been factored out on each curve. This is a statement about algebraic equivalence, not a claim that Chow groups are generated by a single curve.

The unit \(u:F_X^p\to\operatorname{Alb}(F_X^p)\) is an epimorphism of sheaves. To see this, present a sheaf as the colimit of the sheaves represented by its sections. Each representable sheaf maps epimorphically to its Serre–Albanese sheaf [ABV, Lemma 1.3.3]; the colimit formula [ABV, Proposition 1.3.11] expresses the unit as the colimit of these maps. Colimits of 1-motivic sheaves are computed in the ambient sheaf category, and colimits preserve epimorphisms. Thus the unit is an epimorphism. Over \(\mathbf C\), evaluating an étale sheaf epimorphism at \(\operatorname{Spec}\mathbf C\) is surjective, because every cover has a section.

The identity \(\pi_0\operatorname{Alb}(F)=\pi_0F\), proved in `FORMULATION.md`, now shows that the induced map

\[
u:V\longrightarrow A_X^p(\mathbf C)
\]

is surjective as well. Indeed, lift a connected target point along \(u\). Its lift has zero Néron–Severi class, hence is algebraically trivial. The equality of Néron–Severi classes uses [ABV, Theorem 3.1.4] or [OWR, Example 4].

Walker supplies another surjection \(\phi:V\to W_X^p\). Define

\[
a=u\gamma,\quad w=\phi\gamma,\quad
R_A=\ker a,\quad R_W=\ker w,\quad R_{\mathrm{rat}}=\ker\gamma.
\]

Then \(R_{\mathrm{rat}}\subseteq R_A\cap R_W\), and

\[
A_X^p(\mathbf C)=B/R_A,\qquad W_X^p=B/R_W.
\]

**Relation criterion.** A unique isomorphism \(A_X^p(\mathbf C)\to W_X^p\) compatible with all curve correspondences exists if and only if \(R_A=R_W\). If only \(R_A\subseteq R_W\) is known, the conclusion is a surjection with kernel \(R_W/R_A\).

**Proof.** A compatible map must send \(a(b)\) to \(w(b)\). This is well-defined precisely when \(\ker a\subseteq\ker w\); surjectivity follows from that of \(w\). Its kernel and the isomorphism criterion follow from the first isomorphism theorem. Uniqueness follows from surjectivity of \(a\). ∎

A concrete warning shows why the common generators alone do not finish the proof. Let \(B=\mathbf Q^2\), \(a(x,y)=x\), and \(w(x,y)=y\). Both quotients are one-dimensional rational vector spaces, but there is no isomorphism compatible with the identity on the common generator group, since their kernels are distinct. One can equally arrange a common subgroup of known relations (for example zero) without forcing equality of the two larger kernels.

**Result.** The general smooth-projective question reduces to a specific equality of relation subgroups. Both surjectivities and all the quotient identifications above have been justified.

**Unclosed step.** The construction does not prove either inclusion between \(R_A\) and \(R_W\) in general. In particular it does not show that every relation imposed by étale sheafification and the Albanese reflector is exactly a Hodge/period relation coming from the Lawson cycle space. Claiming that both targets are universal without specifying the same target category would simply assume that step.

## Approach 5. Hodge exact sequences: retain the full Lawson kernel

**Goal.** Try to replace the full morphic target by a finite-dimensional Hodge-theoretic target and determine exactly what would be lost.

Let \(r=d-p\), and consider the morphism of IMHSs

\[
L=L_rH_{2r+1}(X)\longrightarrow H_{2r+1}(X,\mathbf Z(r)).
\]

Its image is the coniveau/niveau piece \(N=N_{r+1}H_{2r+1}(X,\mathbf Z(r))\). Put \(K=\ker(L\to N)\). Applying \(\operatorname{Hom}_{\mathrm{IMHS}}(\mathbf Z(0),-)\) and its derived functors gives

\[
\Gamma(N)\longrightarrow J(K)\longrightarrow J(L)
 \longrightarrow J(N)\longrightarrow0.
\]

Here \(\operatorname{Ext}^2(\mathbf Z(0),K)=0\) in the bounded countable ind-MHS category used by Walker. Since \(X\) is smooth projective, \(N\) has pure weight \(-1\) modulo torsion. A morphism from the weight-zero object \(\mathbf Z(0)\) has torsion image. Thus \(\Gamma(N)\) is finite, and tensoring with \(\mathbf Q\) yields the short exact sequence

\[
0\longrightarrow J(K)\otimes\mathbf Q
 \longrightarrow J_r^{\mathrm{mor}}(X)\otimes\mathbf Q
 \longrightarrow J(N)\otimes\mathbf Q\longrightarrow0.\tag{*}
\]

This derivation uses the IMHS Jacobian formalism in [W, §3]; it is not an inference from equality of rational Betti numbers.

The finite-dimensional target called the Walker intermediate Jacobian in [S] and [ACV] is \(J(N)\), written cohomologically as \(J(N^{p-1}H^{2p-1}(X,\mathbf Z(p)))\). Its descent and regularity leave \(J(K)\) untouched. That kernel can survive rationalization: Walker's Theorem 6.2 constructs smooth projective products \(X=Y\times C\) for suitable higher-dimensional \(Y\), with a nonzero vector-space/countable-group contribution in the kernel of the map to the classical algebraic Jacobian. The intermediate map \(J(N)\to J_a\) is an isogeny; its finite kernel cannot absorb that non-torsion contribution. By (*) this forces \(J(K)\otimes\mathbf Q\ne0\) for those examples.

It would also be wrong to throw away the weight-zero part of an IMHS before taking its Jacobian. If

\[
0\to H\to E\to\mathbf Z(0)\to0
\]

is an extension with \(H\) of weight \(-1\), its extension class is a point \(e\in J(H)\). The connecting homomorphism sends \(1\) to \(e\), and \(J(\mathbf Z(0))=0\). The same long exact sequence gives

\[
J(E)=J(H)/\mathbf Z e.
\]

After rationalization, the quotient is \(J(H)_{\mathbf Q}/\mathbf Q e\). Thus a weight-zero quotient can impose an essential period relation even though its own Jacobian vanishes. This is exactly the kind of relation the preceding curve-presentation approach must recover.

Nor does such a quotient automatically lie outside the motivic target category. If \(A\) is an abelian variety and \(e\in A(\mathbf C)\) is nontorsion, the rational sheaf morphism \(\underline{\mathbf Q}\to A_{\mathbf Q}\) defined by \(e\) has a 1-motivic cokernel. By right exactness of \(\pi_0\), that cokernel is connected; its complex points are \(A(\mathbf C)_{\mathbf Q}/\mathbf Qe\). A 1-motivic sheaf need not be a finite-type abelian variety. Therefore the existence of the Lawson kernel is an obstruction to a shortcut, not a counterexample to the corrected conjecture.

**Result.** The exact extra term omitted by the later finite Walker target is \(J(K)_{\mathbf Q}\). The period-quotient calculation explains why comparing only weight \(-1\) pieces or only abelian-variety quotients is insufficient.

**Unclosed step.** Identify this full kernel and all its period relations on the Chow-sheaf side, and then prove the equality \(R_A=R_W\) from Approach 4. Neither the descent theorem nor rationalizing the coniveau lattice provides that equality.

## Overall conclusion

Approaches 1–3 establish map-compatible special cases (including the separately checked nonproper curve localization) of the explicitly repaired comparison. Approach 4 isolates the precise general relation problem, and Approach 5 derives a nonvanishing obstruction to the finite-dimensional replacement and a model for the missing period relations. No step yields the required general identification. The literal source formula's projective-line obstruction remains a separate formulation finding, not a substitute for resolving the connected question.
