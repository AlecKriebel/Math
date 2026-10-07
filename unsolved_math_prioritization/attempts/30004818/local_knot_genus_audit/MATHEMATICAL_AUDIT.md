# Independent mathematical audit: local-knot genus, problem 30004818

Date: 7 October 2026. Scope: the five retained partial arguments in the frozen author package identified by `input_pins.json`.

## Disposition

All five retained mathematical partial results are accepted within their stated hypotheses. No mathematical correction is required to their conclusions. Several conventions and proof details are made explicit below; a separate optional clarification patch records them without editing the originals. The final existence question remains unresolved by this work: there is neither a construction of an orientable-product genus saving nor a proof of equality for all knots and orientable three-manifolds.

This is a source-scoped mathematical audit, not a claim of novelty, human review, or machine-checked formal proof. Arithmetic and hash checks below establish only the things they actually test. They do not certify the geometric or Floer arguments.

## 1. Exact problem and source boundary

Ruppik's contribution to *Oberwolfach Report 42/2021*, pp. 2358–2360, explicitly works in the smooth category. Its Theorem 1 constructs a punctured torus for the sum of two same-handed trefoils in a nonorientable three-manifold product. Question 1 asks whether the same phenomenon occurs for an orientable three-manifold. The classical comparison genus is two. The requested surface is compact, connected, orientable, and smoothly properly embedded, has one local boundary knot at one end of the product, and has no other boundary. This is the bounding-genus interpretation stated explicitly in Klug–Ruppik, §2, pp. 4–5. It is not a statement about arbitrary fillings, nonorientable surfaces, or nonlocal null-homologous knots.

The question itself does not assume the three-manifold is closed. The author's closed-manifold reduction is valid: the projection of the compact surface and its local ball lie in the interior of a compact codimension-zero oriented submanifold N; its oriented double contains the same surface in its product. If the original ambient three-manifold has boundary, the stipulated properness and sole local boundary ensure that the surface avoids its side boundary. Thus proving an obstruction for all closed oriented M would obstruct the full existential target.

The puncturing/capping equivalence with a genus-g cobordism between K and a local unknot is also valid. Remove an interior disk from the surface and extend its new boundary along a thin tube about an arc reaching the opposite boundary level. A generic arc avoids the two-dimensional surface in the four-manifold. The tube is an annulus, so genus is unchanged. The transported boundary is an unknot in a small ball; the reverse construction caps it locally.

Primary sources checked:

- Ruppik, *Concordances in (non-orientable 3-manifold) × [0,1]*, OWR 42/2021, pp. 2358–2360, Question 1: https://ems.press/content/serial-article-files/46920 ; https://doi.org/10.4171/OWR/2021/42 .
- Klug–Ruppik, *Deep and shallow slice knots in 4-manifolds*, arXiv:2009.03053v3, §2, Proposition 2.2 and following discussion: https://arxiv.org/abs/2009.03053 .
- Park–Wu–Yang, *Local Knots, ν⁺-Sharp Knots, and Rational Slice Genus*, arXiv:2603.18619v1, pp. 1–2 and Theorem 1.1: https://arxiv.org/abs/2603.18619 . This March 2026 source explicitly describes the full question as open and proves equality for ν⁺-sharp knots in rational homology spheres. Its local/null-homologous genus is explicitly the ordinary connected oriented bounding-surface genus. The audit does not promote that partial theorem to arbitrary M or arbitrary K, or claim exhaustive later-literature coverage.

## 2. Approach 1: finite image and the exact cover calculation

**Accepted.** Let W=M minus an open three-ball D. A suitable D exists disjoint from both the local ball and the projection of F: the image of the smooth two-dimensional compact surface under projection into M has empty interior, and M minus the local ball contains a nonempty open set. Puncturing leaves the fundamental group unchanged.

The exact cited input is Boden–Nagel, arXiv:1606.06404v1, **Lemma 2.10**, pp. 6–7. Its hypotheses are: W is connected, oriented, compact, and has boundary diffeomorphic to S². Its conclusion is a smooth compression of the universal cover into D³, with a chosen boundary sphere mapped orientation-preservingly to ∂D³. Primeness occurs in the preceding Lemma 2.9 and is not an additional hypothesis of Lemma 2.10. Consequently the universal cover of the punctured closed oriented M used here embeds smoothly in S³. An embedding of the unpunctured universal cover into S³ is not being assumed. Later-source numbering 2.11 does not change which theorem is used.

For a connected component of the inverse image of F in the universal cover product, the covering subgroup is the kernel of π₁(F)→π₁(M). Its index is |H|=d. Therefore the lifted surface is compact and is a d-sheeted cover of F. It is not generally a lift of the original surface with unchanged topology. Because the boundary loop is null-homotopic in the local ball, its monodromy is the identity. The inverse image has d boundary circles, all mapping with degree one. The formula is consequently

    2 − 2g(tilde F) − d = d(1 − 2g),
    g(tilde F) = 1 + d(g − 1).

If g=0 then necessarily d=1; the negative values obtained by inserting impossible d>1 disk cases have no geometric meaning.

The d lifted boundary circles lie in distinct lifts of the local ball. Under an orientation-preserving compression their images lie in disjoint balls in S³ and are the same oriented classical knot K. The orientability assumption rules out replacing some copies by mirrors through orientation monodromy. A finite collection of such balls can be positioned in the standard split configuration. Choose the standard connected-sum bands in a newly added bottom collar. Their interiors avoid the old surface, and their d−1 saddle attachments give

    χ = d(1 − 2g) − (d−1) = 1 − 2dg.

Thus the resulting connected one-boundary surface has genus dg and proves g₄(#ᵈK)≤dg. Subadditivity of classical four-genus and its subadditive limit give g_st(K)≤g. The additive-invariant corollary and the finite-image obstruction for stable-genus-sharp knots follow exactly as written.

Infinite image yields a noncompact infinite-sheeted lift; neither residual finiteness nor an unconstructed group action repairs this. The example of the figure-eight knot only demonstrates the distinction between stable and ordinary genus. No unrestricted equality follows from A1.

Source: Boden–Nagel, *Concordance group of virtual knots*, Lemma 2.10 and its definition of compression: https://arxiv.org/abs/1606.06404 ; https://doi.org/10.1090/proc/13667 .

## 3. Approach 2: image-subgroup covers and hyperbolic manifolds

**Accepted.** For H equal to the image subgroup, the ordinary lifting criterion applies to the original embedding F→M×I. Its lift is injective because any coincidence projects to a coincidence of the original embedding. It is smooth because the covering is a local diffeomorphism. Compactness supplies the needed embedding/properness properties even when M_H itself is noncompact and its embedding in S³ is not proper. The local boundary lies in one lifted ball. An orientation-preserving smooth embedding M_H→S³ therefore produces a classical genus-g bounding surface without a multiplicative loss.

For a complete orientable hyperbolic M=H³/Γ, Γ is discrete and torsion-free in Isom⁺(H³). Every nontrivial abelian subgroup is either loxodromic cyclic or parabolic of rank one or two. Culler–Shalen, §1.5, p. 8 of the accessed author PDF, states this classification for maximal abelian subgroups; subgroups give the asserted list. The supplied elementary centralizer argument is valid. In the loxodromic case a discrete subgroup of R×SO(2) has a finite kernel under translation; torsion-freeness makes that kernel trivial. Bounded translation with compact rotational coordinate would otherwise give infinitely many elements in a compact set and contradict discreteness. The translation image is therefore discrete cyclic. In the parabolic case the centralizer is the translation plane, whose discrete subgroups have ranks at most two. Elliptic elements are excluded by discreteness and torsion-freeness.

The author's models are genuine smooth models for the entire quotients:

- trivial subgroup: R³;
- loxodromic cyclic: straighten its rotation in normal coordinates along the axis to obtain S¹×R²;
- parabolic cyclic: S¹×R×(0,∞), also S¹×R²;
- parabolic rank two: T²×(0,∞), also T²×R.

R³, the open solid torus, and the interior of a tubular neighborhood of an embedded torus all embed smoothly in S³. No finite-volume hypothesis is needed. This establishes the abelian-image theorem for every complete orientable hyperbolic M in the statement.

For a punctured torus, the boundary relation [a,b] maps to the identity because the boundary is local. The image generated by a and b is thus abelian. Consequently a genus-one saving is impossible in these hyperbolic products; any strict saving there requires product genus at least two, classical genus at least three, and nonabelian image for every minimizing saving surface. For higher genus a product of commutators being trivial does not imply that the image is abelian. The author's [x,y][y,x] example is a valid explicit counterexample to that attempted implication. The tube-added local-unknot surface shows that locality alone does not force a proper image subgroup, without asserting that this surface minimizes genus.

Source: Culler–Shalen, *Paradoxical decompositions, 2-generator Kleinian groups, and volumes of hyperbolic 3-manifolds*, §1.5: https://homepages.math.uic.edu/~culler/papers/log3/log3.pdf .

## 4. Approach 3: equivariance, companion concordance, and intersection cost

**Accepted as conditional constructions and obstructions; no existence construction is certified.** In the antipodal double-cover test, nontrivial image in π₁(RP³)=Z/2 makes the full lifted surface connected. For a genus-one one-boundary quotient it has genus one and two boundary components. The action must be free, orientation-preserving on the surface, and exchange the lifted local balls and their boundary knots. These are necessary geometric conditions beyond an equality in the classical concordance group.

An annulus has χ=0. A free orientation-preserving involution exchanging its two boundary components would give an orientable quotient with one boundary component and χ=0. Such a surface would require 1−2g=0, impossible for integral g. The orientation-reversing quotient is a Möbius band and is outside the problem. Adding a tube changes the Euler characteristic appropriately but does not construct the required action or change its orientation on an unchanged open subsurface. The general d-fold genus-one formula is equally correct.

For the companion criterion, fix the actual annular parallel link J₊⊔J₋ and its opposite annulus-induced orientations. J₋ is an orientation reverse of a parallel, not a mirrored concordance inverse. A punctured annulus, placed at varying height in M×I, supplies the pair of pants from a local unknot to these parallels. The local strip insertion justified in §6 below ties K into its small boundary and its J₊ boundary with compatible signs. It supplies the asserted embedded P_K with χ=−1.

If the two specified components of L_K and L_0 cobound **two disjoint embedded annuli**, stacking them between P_K and a final pushed-in annulus produces one connected orientable surface with one boundary and χ=−1, hence genus one. Choose orientations so each glued boundary is oppositely oriented; reversing the final surface orientation if necessary gives the designated orientation of K. Successive product intervals make the interiors of the three pieces disjoint.

An ordinary absorbing knot concordance is insufficient. Given only A, keep the prescribed spectator cylinder C. After transversality and collar arrangements, all extra intersections are precisely the r interior points of A∩C. After stacking, their preimages belong to the single connected abstract surface. Oriented smoothing of each double point removes two disks and inserts an annulus; it lowers Euler characteristic by two, keeps the final boundary, and increases genus by one. This works for either sign of transverse intersection. The resulting bound is therefore 1+r, not one. No Whitney-disk or cancellation hypothesis has been silently inserted.

The sanity check is independently supported by Davis–Nagel–Park–Ray. Theorem A identifies all winding-one knots in S¹×S² with the essential core up to smooth concordance. Theorem 2.5, p. 6, transfers arbitrary prescribed two-boundary surface types between local knots to and from the classical product. Taking one boundary to be the local unknot gives the required genus equality. Hence any such absorbing annulus with the prescribed spectator in this product must satisfy r≥g₄(K)−1. This validates the author's diagnosis of the missing disjointness condition.

McDonald–Miller Proposition 2.9 gives disks in punctured Spin(RP³); Remark 2.10 gives genus at most one in punctured RP³×S¹. Neither says that the completed surface is in RP³×I. Their tangle/product stages are not a verified substitute for the required disjoint companion concordance.

Sources:

- Davis–Nagel–Park–Ray, *Concordance of knots in S¹×S²*, Theorems A and 2.5: https://arxiv.org/abs/1707.04542 ; primary PDF directly read at https://arxiv.org/pdf/1707.04542 .
- McDonald–Miller, *Constructing knots with low rational genera*, Construction 2.8, Proposition 2.9, and Remark 2.10: https://arxiv.org/html/2511.15900v1 .

## 5. Approach 4: relative classes and product intersections

**Accepted integrally, including torsion in H₁(M).** For W=M×I with M closed and oriented, one boundary inclusion is a homotopy equivalence. Hence H₂(∂W;Z)→H₂(W;Z) is onto. Exactness implies that H₂(W,∂W;Z)→H₁(∂W;Z) is injective. The relative fundamental class of F maps to the class of its local boundary K, which vanishes integrally. Therefore [F]_rel=0. No passage to rational coefficients or torsion-freeness assumption occurs.

The absolute intersection pairing factors through the zero map H₂(W)→H₂(W,∂W), so it vanishes. Alternatively, push representatives into distinct time levels. Pairing a closed surface with the relative class of F gives zero, for embedded or proper immersed F. Consequently a closed oriented surface cannot meet F in exactly one transverse point. This excludes an algebraic dual of that precise type and the direct application of the dual-sphere construction under consideration. It does not prohibit pairs of intersections of opposite signs and does not supply Whitney disks.

The distinction between relative and absolute classes is preserved correctly. Tubing a local unknot disk to a coordinate torus in T³×I produces a local-boundary surface whose cap class is the nonzero coordinate-torus class, while its relative class is zero. Thus cap classes cannot be deleted from the later Floer computation.

The transverse coordinate tori in T⁴ have intersection one. A neighborhood carrying both closed tori and this intersection cannot embed in an oriented product with zero absolute intersection form. McDonald–Miller Proposition 2.14 uses precisely this intersecting-tori input. The audit accepts only the obstruction to transporting that configuration; it does not assert that every surface obtainable by some filling construction has no different product realization.

The disk-bundle illustration is also correct: the oriented double is the associated S²-bundle over S²; a section of square p and a fiber give matrix [[p,1],[1,0]], of determinant −1. A surgery trace or a closed double is not a product collar. Surgeries away from a surface can change the ambient four-manifold without changing the surface and therefore do not establish the desired product statement.

## 6. Approach 5, first part: the concordance-group norm

**Accepted.** The point requiring a geometric construction is local-knot propagation, not the addition of two arbitrary bounding surfaces in a common four-manifold.

Here are explicit local coordinates for that step. Let γ be a properly embedded arc on a connected oriented cobordism S, joining its incoming and outgoing boundaries. Its tubular neighborhood in the oriented four-manifold has the form D³×[0,1], with endpoint D³'s lying in the two boundary levels, and with S meeting the neighborhood in a straight diameter of D³ times [0,1]. Choose the coordinates product-like near the endpoint collars. A trivialization along the interval can be chosen to take the oriented normal data to those of this straight strip. Replace the diameter by a fixed properly embedded long-knot arc representing J, unchanged near its two endpoints, and take its product with [0,1]. The replacement is an embedded strip; it agrees with the old strip near the two vertical attaching edges and glues smoothly after collar adjustment. Its topology is unchanged. Orientability of the ambient product ensures that the oriented local ball coordinates at the incoming and outgoing ends agree, so the same J is tied into both boundary knots.

This operation has no disjoint spectator and no assertion that two separately chosen surfaces can be made disjoint. Applying it to K→U gives K#J→J without genus cost. Stack a J→U cobordism in a subsequent product interval. This proves subadditivity. Classical local concordances prove invariance under classical concordance. For symmetry, propagate −K, prepend a local slice concordance U→K#−K, and reverse the resulting U→−K cobordism. This proves q_M(−K)≤q_M(K), and exchanging K and −K proves equality. The zero set is exactly the classical slice class by the local disk theorem (also recovered by A1 with g=0,d=1). The local embedding upper bound is immediate.

Thus q_M is a definite, symmetric, subadditive integer-valued group norm, in the customary length-function sense, bounded by g₄. No homogeneity is asserted. The countermodel ceil(|n|/2) on Z is indeed symmetric, definite, and subadditive. Equality of zero sets or injectivity therefore cannot force isometry. Stable limits lose all finite-order classes. These observations identify a genuine limit of the attempted argument rather than resolve the target.

## 7. Approach 5, second part: the Floer lower bound

**Accepted for every closed connected oriented M.** A dedicated primary-source audit is supplied in `floer/`; the essential checks and conventions are recorded here.

Work with F₂ coefficients. Closed oriented three-manifolds have nonzero hat Heegaard Floer homology in some Spinᶜ structure. The source package invokes this standard theorem; an explicit citation is Alishahi–Lipshitz, *Bordered Floer homology and incompressible surfaces*, Theorem 1.2, p. 1526, with proof pp. 1542–1543: https://www.numdam.org/item/10.5802/aif.3276.pdf . Conjugation preserves nonvanishing; the relevant symmetry is Ozsváth–Szabó, *Holomorphic disks and three-manifold invariants: properties and applications*, Theorem 2.4: https://annals.math.princeton.edu/wp-content/uploads/annals-v159-n3-p04.pdf .

The local unknot with its local spanning disk has Alexander filtration zero. One may realize this using a local doubly pointed unknot diagram. The local decomposition (M,K)=(M,U)#(S³,K), with local Seifert surfaces, then yields τ_α(M,K)=τ(K) for every nonzero α in any nonzero Spinᶜ summand. Hedden–Raoux Proposition 2.6 gives the exact connected-sum formula for nonzero Floer classes over F₂, and Remark 2.7 identifies the boundary-summed Seifert normalization. No assertion that conjugation preserves τ for arbitrary nonlocal knots is needed: each conjugate class again belongs to a local knot, for which the same independent calculation applies.

Hedden–Raoux Theorem 1, pp. 2–3, requires a compact oriented cobordism W, rationally null-homologous boundary knots, an oriented properly embedded surface Σ with boundary −K_in⊔K_out, and a Spinᶜ cobordism map carrying a nonzero α to a nonzero β. There is no definiteness assumption and no condition that the chosen absolute cap class vanish. Their Theorem 4.1, p. 24, explicitly uses

    A = [S_in + Σ − S_out],
    <c₁(t),A> + A² + 2(τ_β(K_out)−τ_α(K_in)) ≤ 2g(Σ).

The product map is the identity for the standard product basepoint path. If basepoint transport along a different path is retained, the resulting map is an automorphism, which is equally sufficient: the two local τ values are independent of the chosen nonzero input and output classes. This removes any hidden dependence on the omitted pointed-cobordism convention.

Convert F to Σ:U→K. Its cap class A need not be zero, but A²=0 by A4. Pull back a Spinᶜ structure with nonzero hat homology. The two applications, in t and its conjugate, give

    c + 2τ(K) ≤ 2g,
    −c + 2τ(K) ≤ 2g,

where c=<c₁(t),A>. Add them to obtain τ(K)≤g. For the opposite direction set R(x,t)=(x,1−t), and orient the reversed cobordism as −R(Σ); its boundary is −K⊔U. Apply the same product argument in that direction, with its own cap class. Its τ difference is −τ(K), and the two conjugate applications give −τ(K)≤g. Therefore |τ(K)|≤g. Minimizing over F proves the claimed bound.

This checks all three essential distinctions: relative vanishing does not erase A; conjugation, rather than an unsupported zero-pairing assertion, cancels the Chern term; and reversing the cobordism changes the τ difference without silently mirroring K. The resulting equality for τ-sharp knots, including sums of equally handed trefoils, is valid. Extension of this obstruction from closed M to the full existential setting follows from the compactness/doubling reduction in §1.

Source: Hedden–Raoux, *Knot Floer homology and relative adjunction inequalities*, arXiv:2009.05462v2, Theorems 1 and 4.1, Proposition 2.6, Remark 2.7: https://arxiv.org/abs/2009.05462 ; https://doi.org/10.1007/s00029-022-00810-1 .

## 8. Torsion family and remaining gap

Miller, *Amphichiral knots with large 4-genus*, Theorem 1.1 and Corollary 1.2, supplies strongly negative amphichiral knots of smooth concordance order two and arbitrarily large topological four-genus, hence arbitrarily large smooth four-genus. Their stable smooth genus is zero because twice each class is slice. Every real additive concordance invariant, including τ, vanishes on them. This verifies the claimed surviving test family, not a product realization.

Neither rational slice disks, punctured Spin(RP³) disks, punctured RP³×S¹ surfaces, nor a nonequivariant classical slice disk for #²K supplies the product surface required by the OWR question. A free equivariant surface with the stipulated local boundary orbit, or a companion-link concordance satisfying the stated disjointness/intersection bound, remains to be constructed. These are examples of surviving avenues, not an exhaustive classification of possibilities.

Source: Miller, Theorem 1.1 and Corollary 1.2: https://arxiv.org/abs/2011.09346 ; https://doi.org/10.1112/blms.12588 .

## 9. Reproducibility and editorial disposition

All seven authored-file byte counts and SHA-256 values match the supplied manifest. All ten retained primary PDFs were rehashed and freshly extracted with `pdftotext -layout`; each extraction was byte-identical to its saved text. The temporary re-extractions were removed after comparison. These checks establish correspondence between the inspected local texts and the pinned PDFs, not an exhaustive authenticity proof or theorem certification. Primary web pages/PDF text independently corroborated the relevant source statements. Two attempted OWR web screenshots failed with cache-miss errors; no visual screenshot verification is claimed or required for the textual claims reviewed here.

Independent finite checks pass: 601 valid finite-cover genus cases; all 23 saved equivariant arithmetic records; 1,001 smoothing Euler computations; 40,401 triangle inequalities for the norm countermodel; and 2,001 disk-bundle determinant samples. The formulas are also justified algebraically in the audit. The original verification files contain summaries, not runnable author proof scripts, so these are independent reconstructions rather than claimed replays of an unavailable script.

The source report's final statement that only one author approach has been completed is a stale snapshot. The completion report and manifest correctly record five. The optional patch changes that sentence to an explicit historical note and adds the cited Floer conventions and strip model. It makes no mathematical enlargement and is not required for acceptance of the retained conclusions. Originals remain unchanged. No repository publication, queue alteration, or claim of a full solution is included in this audit.
