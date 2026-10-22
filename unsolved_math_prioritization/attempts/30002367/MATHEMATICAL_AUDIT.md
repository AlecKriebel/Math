# Mathematical audit of the credited prior resolution

**Authorship and review status:** This authored report was prepared with AI assistance and is unrefereed, with no proof-assistant certification. Its mathematical acceptance is scoped to the explicitly named foundations. This report's status is distinct from the bibliographically confirmed journal publication of Hemminger's prior result.

**Target:** 30002367, finite-group mod-p Chow detection/suspension equality.
**Date:** 2026-10-10 UTC. **Text inspected:** Hemminger arXiv:1911.03033v2, 25 pages.

This is an audit and explanation of existing mathematics. The target theorem is credited to Hemminger. A source-proof correction is supplied separately; it does not create a novelty claim for the target. The result is accepted relative to the standard foundational inputs listed in section 7.

## 1. Set-up and definitions

Fix p, k and finite G as in the applicability certificate, and set N=CH^*(BG_k)/p. Let i:\(\mathcal U\to\mathcal U^{top}\) double degrees. The category \(\mathcal U\) consists of unstable modules supported in even topological degrees. Let

\[
\mathrm{Nil}_r=\mathcal U\cap\mathrm{Nil}^{top}_{2r}.
\]

These are Serre localizing subcategories. The n-nilpotent part \(F_nN\) is the largest subobject of N belonging to \(\mathrm{Nil}_n\); existence is part of the nilpotent-filtration/localization theory. It is important that this is a module-theoretic nilpotence filtration, not merely the radical or the maximal ideal-power nilpotence index of the ring N.

Write \(L_n\) for localization away from \(\mathrm{Nil}_n\). Its unit \(\lambda_n:N\to L_nN\) has kernel and cokernel in \(\mathrm{Nil}_n\); its target is \(\mathrm{Nil}_n\)-closed, meaning Hom and Ext^1 from n-nilpotent objects vanish. In particular,

\[
\ker\lambda_n=F_nN. \tag{1}
\]

Indeed, the kernel is n-nilpotent, hence lies in F_nN. Conversely any n-nilpotent submodule maps to zero in the closed target, so F_nN lies in the kernel. This proves (1), including both inclusions.

## 2. Detection is the same injectivity question as localization

Hemminger Theorem 5.6 describes \(L_nN\) as a specific equalizer Q_n in a product of elementary-abelian Chow factors tensored with truncated centralizer Chow factors. Specializing X to a point removes all fixed-locus terms. The canonical component map is precisely \(\mu_E^*\), followed by truncation of centralizer degree to <n.

For n=d+1, the composite \(N\to Q_n\hookrightarrow P_n\) is Totaro's D_d. The second arrow is inclusion of an equalizer, therefore a monomorphism. Thus

\[
D_d\text{ injective}\quad\Longleftrightarrow\quad\lambda_{d+1}\text{ injective}\quad\Longleftrightarrow\quad F_{d+1}N=0.\tag{2}
\]

The equality of kernels needs no surjectivity onto the equalizer and no claim that D_d's image is the entire product. This is the geometric step absent from a purely formal restatement of the conjecture.

## 3. Full reconstruction of Proposition 6.1

The standard nilpotent-filtration theorem says the successive quotients of the topological filtration satisfy

\[
F_s^{top}A/F_{s+1}^{top}A\cong\Sigma_{top}^s R_sA
\]

for an unstable module R_sA, in fact reduced. Hemminger cites Schwartz, Lemma 6.1.4.

For an even object A=iN, the adjacent odd layer is zero in the required sense:

\[
F_{2r+1}^{top}(iN)=F_{2r+2}^{top}(iN).
\tag{3}
\]

Here is a direct parity check. The quotient at topological index 2r+1 is a subquotient of iN, hence is supported in even degrees. By the filtration theorem it is Σ_top^(2r+1)R for a reduced unstable module R, so R is supported in odd degrees. Every unstable module supported only in odd degrees is itself a suspension: shift its grading down once. At p=2 the only newly prohibited square on an element originally of degree 2q+1 is Sq^(2q+1), which has zero target by parity. At odd p the only new instability condition is βP^q=0, likewise true by parity. Thus the desuspended module is unstable. Such an R belongs to Nil_1^top; since it is reduced, it must be zero. This proves (3) without using a compressed lower-operation formula on odd degrees.

It follows from the topological filtration theorem and (3) that

\[
F_rN/F_{r+1}N\cong\Sigma^r R_r
\tag{4}
\]

in the Chow-regraded category. The underlying topological shift in (4) is 2r. The desuspended object is still even and unstable, so it belongs to \(\mathcal U\).

There is some finite B with \(F_{B+1}N=0\), by section 6 below. Also F_0N=N≠0. The decreasing sequence therefore has a greatest integer

\[
e=\max\{r:F_rN\ne0\}.
\]

Equation (2) gives d_det(N)=e. At this largest e, the next term actually vanishes, so (4) yields

\[
0\ne F_eN=F_eN/F_{e+1}N\cong\Sigma^eR_e\hookrightarrow N.
\]

This is a **submodule**, not just a subquotient, and proves that the suspension maximum is at least e.

Conversely, suppose \(0\ne\Sigma^dM\hookrightarrow N\) in \(\mathcal U\). Upon degree doubling it is \(\Sigma_{top}^{2d}iM\), hence belongs to \(\mathrm{Nil}_{2d}^{top}\) by the definition of the nilpotent category generated by suspensions. Thus \(\Sigma^dM\in\mathrm{Nil}_d\), and its nonzero image lies in F_dN. Therefore d≤e. The two inequalities prove the desired equality. The proof requires neither a splitting of the filtration nor a construction of a topological space realizing M.

## 4. Audit of the Lannes-functor computation (Theorem 4.1)

This theorem computes

\[
T_V CH_G^*(X)\cong\prod_{[\rho:V\to G]}CH_{C_G(\rho)}^*(X^\rho).
\tag{5}
\]

Its adjoint is the actual multiplication pullback, not merely an abstract isomorphism. This map-level identification is needed later.

### 4.1 Elementary abelian group, point

Lemma 4.2 computes the left adjoint on the polynomial Chow ring of an elementary abelian group. Free-unstable-algebra adjunction gives the expected product indexed by homomorphisms; tensor compatibility then handles all ranks. The comparison with the topological computation verifies that the natural map itself is an isomorphism. This step uses the external Lannes comparison and the known topological elementary-abelian calculation. Finite-dimensionality per degree is invoked only for these polynomial rings, not for an arbitrary finite-group Chow ring.

### 4.2 Elementary abelian group acting on a smooth scheme

The isotropy-rank filtration is finite. Lemma 4.3 replaces the pushforward from a fixed stratum by an inverse pullback on its Euler-class image. This matters: Chow pushforward is not automatically Steenrod-linear.

For a stratum with stabilizer W⊂S, choose S=W×W'. W' acts freely; W acts trivially on the base. The normal bundle has only nontrivial W-character summands. Each summand's Euler class, after a suitable change of character basis, is a monic polynomial in a polynomial Chow generator. It is therefore a non-zero-divisor over the possibly non-Noetherian coefficient ring. The self-intersection formula identifies the kernel in the localization sequence with that Euler-class image. Pullback is Steenrod-linear, so the resulting short exact sequence is in \(\mathcal U\).

This argument is read and checked against Totaro's actual Theorem 6.7 proof (book pp.67-68), where the monic-polynomial argument is explicit. Exactness of T_V transfers these sequences. On the normal bundle, homotopy invariance, the elementary-abelian point calculation and boundedness of the ordinary Chow ring give (5). Removing the zero section strictly lowers maximal stabilizer rank. Induction terminates and proves Lemma 4.4.

### 4.3 Change of groups and descent

Embed G faithfully into H=GL(n), and let S be the diagonal p-torsion subgroup. The scheme (X×H)/G is smooth, and its S-equivariant Chow ring equals the G-equivariant Chow ring of X×H/S. The transporter decomposition in Lemma 4.5 is compatible with the actual group actions and multiplication maps. Lemma 4.4 therefore proves (5) for X×H/S and X×H/S×H/S.

Lemma 4.6 is a flag-bundle calculation. In mod-p Chow theory, the additional torus torsors replace each first Chern class by its pth multiple, which vanishes. This identifies the relevant rings as base changes from \(CH^*(BGL(n))\) to \(CH^*(BS)\). The latter is finite free and faithful over the symmetric-polynomial subring. Lemma 4.7 is then the first faithfully-flat descent sequence. Applying exact T_V proves the top-row exactness in the proof of (5).

**Source defect and correction.** The printed argument for the bottom row on preprint p.16 incorrectly identifies the centralizer of an arbitrary diagonal elementary abelian subgroup with GL(n−r)×Gm^r, where r is its rank. In general the correct centralizer is the product of GL groups on the distinct character spaces. Moreover the descent diagram must retain mixed components of the fixed locus, and the equivariance group is C_G(λ), not silently C_H(λ).

`CENTRALIZER_DESCENT_CORRECTION.md` gives the complete replacement: rational split transporters, the correct conjugated C_G(λ) action, blockwise flag-bundle presentations, finite faithful freeness, and the mixed-component equalizer. That supplies the needed bottom-row exactness. The two already-known right vertical isomorphisms then identify the kernels, proving (5). This is a local audit correction to the cited proof; we do not certify its uncorrected centralizer sentence.

The field conditions are used here to split all V-character spaces and to identify diagonal p-torsion with a constant elementary abelian group. No assumption p∤|G| is introduced. Because G is finite, all index sets in the applicable proof are finite; exact T_V need only commute with finite products.

## 5. Audit of localization (Theorem 5.6)

The section 5 argument has two parts.

First, each \(CH_E^*\otimes K\) with K concentrated in degrees <n is \(\mathrm{Nil}_n\)-closed (Lemma 5.3). Products and kernels of maps between closed objects are closed. Therefore the equalizer Q_n is closed. These closure assertions follow from the localization/injective theory; the bounded-factor assertion is an imported standard consequence of the Brown-Gitler injective description.

Second, exactness and the nilpotence-detection property of T_V reduce membership of the kernel and cokernel in \(\mathrm{Nil}_n\) to showing that T_V(λ_n) is an isomorphism in degrees <n, for every elementary abelian V. The computation (5), the elementary-abelian polynomial calculation, and T_V's action on bounded modules describe this map componentwise. Below n the indicated truncations do not change those components.

Here is the inverse underlying the source's pp.20-21 proof, specialized to X=point. In the untruncated equalizer, an element has components

\[
x_{E,\rho}\in CH_E^*\otimes CH_{C_G(E)}^*,\qquad\rho:V\to E.
\]

Apply augmentation \(\epsilon_E:CH_E^*\to\mathbb F_p\) to the first factor and call the result z_E,ρ. Write a_E for the multiplication coaction CH^*_{C_G(E)}→CH_E^*⊗CH^*_{C_G(E)}, and Δ_E for the coproduct of CH_E^*. The equalizer relation for the identity morphism of E reads (Δ_E⊗id)x_E,ρ=(id⊗a_E)x_E,ρ. Applying ε_E to the first factor gives x_E,ρ=a_E(z_E,ρ), because (ε_E⊗id)Δ_E is identity. Thus each component is completely recovered from its first-factor augmentation.

Choose one representative λ:V→G of each G-conjugacy class, and put A=im λ. The component indexed by (A,λ) gives z_A,λ in CH^*_{C_G(λ)}. The relation for an inclusion/conjugation A→E implies that z_E,ρ is the restriction/conjugation pullback of z_A,λ whenever λ and ρ are G-conjugate. Therefore all x_E,ρ are recovered from the family (z_A,λ). Conversely every such family yields an equalizer element by the multiplication pullbacks. Augmentation at (im λ,λ) gives a left inverse, since the relevant group map composed with c↦(1,c) is identity. Thus the untruncated sequence is exact; restricting to degrees <n proves the required T_V assertion.

A typographical direction issue in the preprint p.21 should not be propagated: if hAh^{-1}⊂E, the geometric group map is

\[
C_G(E)\longrightarrow C_G(A),\qquad c\longmapsto h^{-1}ch,
\]

and its Chow pullback goes from the A-centralizer ring to the E-centralizer ring. The reverse group inclusion need not exist. With this direction, the elementwise argument above and the source's displayed pullback direction agree. Also a tensor component is a finite sum of simple tensors; the source's compressed homogeneous notation must not be read as asserting tensor rank one.

Hence ker(λ_n) and coker(λ_n) lie in \(\mathrm{Nil}_n\), and Q_n is closed. These are exactly the characterization of localization. There is no assumption of finite generation of CH_G^* over itself or over a polynomial subalgebra in this step.

## 6. Finiteness and absence of circularity

Only a finite upper bound is needed in section 3. Hemminger's Theorem 6.2(a) suffices. For an n-dimensional faithful representation,

\[
CH_G^*\hookrightarrow CH_G^*(GL(n)/S)=CH_S^*(GL(n)/G).
\]

The injection is the faithfully-flat flag descent of Lemma 4.7. The ordinary smooth quotient GL(n)/G has dimension n², since G is finite. The isotropy-rank induction in Lemma 6.5, with no additional torus, gives

\[
d_1(CH_S^*(GL(n)/G))\leq n^2.
\]

For the free stratum this follows from ordinary Chow groups vanishing above the dimension and the bounded-factor closedness lemma. On a stratum with stabilizer W, its ring is \(CH_W^*\otimes CH^*(Z/W')\); the second factor vanishes above the dimension. The normal-bundle complement has smaller stabilizer rank, and the short exact sequences from Lemma 4.3 and closure bounds of Lemma 6.3 finish the induction. Subobjects cannot have larger d0, so d0(N)≤n².

This route uses the formal localization theory and flag descent, not Proposition 6.1 or the conjectured equality. Therefore the proof of the existence of e is not circular. Every finite group has a finite-dimensional faithful representation, for example the regular representation. The sharper numerical bound in part 6.2(c) is unnecessary and is not a dependency certified here. Nor is an optimal n, an algorithm computing d0, or the conjectural finite generation of Chow rings required.

## 7. Explicit external-input boundary

The audit checks the above applications, diagram algebra, localization-to-detection bridge, finite bound route, index conventions, and the terminal filtration argument. It does not claim an independent foundational proof of every cited theorem.

External inputs retained:

- Existence, functoriality, homotopy invariance, localization, self-intersection, and flag/projective-bundle formulas for equivariant Chow groups; the elementary-abelian Chow Kunneth formula. These are the Totaro/Edidin-Graham/Fulton theory used by Hemminger. Totaro's relevant monic-Euler-class and flag arguments were additionally read in the primary book.
- Existence and Adem/Cartan/instability identities of mod-p Chow Steenrod operations over fields of characteristic different from p, including the extension beyond perfect fields. Hemminger cites Brosnan, Voevodsky, Hoyois-Kelly-Østvær, and Riou. Their foundational construction proofs were not rederived here.
- Exactness, tensor compatibility, restriction to even modules, and bounded-module property of Lannes's T-functor; Brown-Gitler injectivity and the vanishing characterization of nilpotent subcategories. These are used with the precise category and grading stated above.
- Existence and localization properties of the nilpotent filtration and the suspension form of its layers, in particular Schwartz's Proposition 6.1.1 and Lemma 6.1.4, as cited by Hemminger. The primary monograph's metadata was verified; a full monograph proof audit was not performed.
- Standard abelian localization and faithfully-flat algebra descent. The required finite-free algebra presentations and the actual corrected equalizer argument are written out in the correction artifact.

A further source-scope qualification matters: preprint p.5 gives a compressed odd-prime lower-operation formula and states the corresponding criterion for arbitrary topological modules. Taken literally, it fails on Σ_top F_p: the degree-one generator is a suspension, but the printed P_0 is P^0, hence identity and not locally nilpotent. This audit does not use that formula on odd-supported modules or certify that sentence as printed. The categorical nilpotent-filtration theorem is the retained standard external input; section 3 supplies a direct parity/desuspension proof for the even-category step.

Similarly, the p.8 statement about the subalgebra generated by the even squares should not be used as a literal isomorphism of subalgebras after regrading. In the actual mod-2 Steenrod algebra, Sq^2 Sq^2=Sq^3 Sq^1 is nonzero, whereas Sq^1 Sq^1=0. The correct degree-doubling description is a statement about the action on even-supported unstable modules, where odd operations act as zero. The audit uses that categorical comparison and the standard even-module T-functor result, not the literal subalgebra assertion.

These are established imported ingredients, not an unsupported restatement of the target. The target-specific geometric theorem and the final deduction are audited above; the exact source defect is preserved and repaired rather than hidden behind the publication label. No assertion is made that the journal version contains the same defect.

## 8. Adversarial checks and disposition

- **False centralizer formula:** rejected; replace with product over character multiplicities. A scalar copy of C_p in GL(2) already contradicts the rank-only formula.
- **Forgetting mixed components:** rejected; individual component descent alone does not make independently descended elements equal. Mixed components enforce equality by faithful freeness.
- **Wrong equivariance group:** rejected; all fixed-locus rings must retain C_G(λ), with its conjugated action.
- **Detection versus definition:** bridge proven by the same map factoring through the equalizer and equality of kernels.
- **Suspension of a quotient:** insufficient until F_{e+1}=0; this vanishing is used explicitly.
- **Off-by-one/factor-of-two:** truncation <d+1 equals ≤d; topological shift 2d equals Chow shift d.
- **Noetherianity:** not assumed; all tensor rings and free bases work over arbitrary coefficient rings.
- **Base field overreach:** excluded; source Conjecture 12.8 itself supplies the same field assumptions.
- **Finite versus p-group:** arbitrary finite G accepted; regular representation and the coarse n² bound suffice.
- **Source status:** prior theorem and journal publication confirmed, publisher PDF full text uninspected, arXiv bytes and dissertation evidence separately identified.

**Conclusion:** accept the credited prior resolution for the precise original target, subject to the listed standard external foundations and using the documented source-proof corrections. No target proof-attempt turn or novelty claim is warranted.
