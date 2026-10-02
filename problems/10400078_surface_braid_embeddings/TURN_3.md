# Turn 3 — The exact proper graded image in the two-strand torus case

AI-assisted mathematical proof candidate; independent review pending. Original unresolved3/5. We analyze the specific completed map of turn2, not an arbitrary surface-braid map or a universal tangle functor.

## 1. A free basis for the braiding kernel

Write G=P₂(T²)=Z²×F(x,y), H=Z⁴ and K=ker η=F(x,y)′. The universal abelian cover of the two-circle wedge is the square grid with vertices(i,j)∈Z² and horizontal/vertical directed edges. Its fundamental group is K. Choose a spanning tree consisting of every horizontal edge and the vertical edges in column0. Its tree path from0 to(i,j) is y^j x^i. Standard graph collapse gives a free basis

r_(i,j)=y^j x^i y x^(−i)y^(−j−1),    i≠0, j∈Z,

and put r_(0,j)=1. Define the based grid-face loops

q_(i,j)=y^j x^i [x,y] x^(−i)y^(−j),    i,j∈Z.

Direct multiplication gives q_(i,j)=r_(i+1,j) r_(i,j)⁻¹. Conversely,

r_(i,j)=q_(i−1,j)…q_(0,j) for i>0,
r_(i,j)=q_(i,j)⁻¹…q_(−1,j)⁻¹ for i<0.

These are mutually inverse substitutions between the free groups on the two indicated sets, each using finite words. Thus the q_(i,j) form another free basis of K. This is elementary graph/Schreier theory, not a new freeness theorem.

## 2. Filtration and its tensor description

Let J=ker(Q[G]→Q[H]) and I=ker(Q[K]→Q). A set-theoretic coset section s:H→G gives a vector-space decomposition Q[G]=⊕_h Q[K]s(h). Normality of K implies

J^d=⊕_h I^d s(h).

Indeed J=I Q[G], and conjugation by G preserves I and all its powers, proving the assertion by multiplication and induction. This is the same kernel-ideal decomposition used by González–Meneses–Paris Proposition2.2 for the Vassiliev filtration. Restricting the full-braid decomposition to the pure permutation sector gives the present case.

For a free group with basis q_(i,j), its augmentation associated graded over Q is the tensor algebra T(V), where V has basis e_(i,j) represented by q_(i,j)−1. One can see this directly: products of these augmentation generators span each quotient; the Magnus substitution q_(i,j)↦1+X_(i,j) sends their length-d products to the distinct degree-d words, proving linear independence. This is the classical Magnus–Fox tensor description.

Consequently, as a graded vector space, gr_J Q[G] is T(V)⊗Q[H]. The algebra structure incorporates the H action by conjugation. We will not need an unproved splitting of G itself: the section is only a linear decomposition, and any section cocycle is1 modulo the positive ideal.

## 3. Leading symbols of the explicit map

Let Θ be the turn2 map and let W have basis t_(a,b), so gr D_hat=T(W)⋊Q[H]. Conjugation by the degree-zero part of the whisker y^j x^i shifts every chord label by −(i,j). The first-order formula for [x,y] therefore gives

Θ(q_(i,j))−1 = t_(−i−1,−j)−t_(−i,−j) + terms of degree≥2.

Define L:V→W by this displayed difference. It is injective. For each fixed row, a finite linear combination of successive differences can vanish only if all its coefficients are equal along the entire infinite row, hence zero because the support is finite. Equivalently, choose an extreme column of a nonzero finitely supported combination and inspect its outer endpoint coefficient.

Its image W₀ is exactly the subspace of finite chord combinations whose coefficient sum vanishes separately in every horizontal row. The inclusion is immediate; the converse follows by finite telescoping within each row. Thus W/W₀ has one independent quotient class per row and is nonzero.

The associated-graded map of Θ is, under the preceding decompositions, T(L)⊗id_(Q[H]). To justify this, augmentation generators have the displayed leading images, their ordered products give tensor products, and s(h) has degree-zero term h. No higher section correction contributes in that leading degree. Tensor powers of an injective linear map over Q are injective; alternatively extend a basis of W₀ to one of W and inspect words. Hence the graded map is injective in every degree. Its image is the proper graded subalgebra

T(W₀)⋊Q[H] ⊂ T(W)⋊Q[H].

Translation of labels preserves W₀, so the displayed crossed-product image is stable under the H action. Its degree-one part is already proper, and in higher degrees it consists exactly of tensors all of whose factors lie in W₀.

## 4. Consequences and exact limitation

The map on Q[G] is strictly filtered: Θ⁻¹(F^d D_hat)=J^d for every d. If an element is not in J^d, select its first nonzero J-graded component of degree below d; graded injectivity prevents its image from lying in F^d. The converse is filteredness. Therefore every finite quotient Q[G]/J^d injects into D_hat/F^d.

The J filtration is separated, either by the classical Magnus–Fox separation for the free group K together with the coset decomposition, or by the published surface-braid separation theorem of González–Meneses–Paris (Theorem1.2 and Proposition2.2). Consequently the linear extension of Θ is itself an injective Q-algebra map, strengthening the group injectivity from turn2.

This proves an injective, proper associated-graded image, **not** an isomorphism to the full prescribed diagram algebra. We retain this precise wording rather than use 'universal' without a definition. A convention phrased only in terms of linear-functional factorization is not automatically identical to a convention demanding a graded isomorphism onto a specified target. The published Bellingeri–Funar theorem is stated for the full braid group B(Σ,n); no extension of this pure-group construction to that group or to tangle functoriality has been proved. We do not claim a correction to that paper, and we do not silently treat a later citation to a pure-group obstruction as a proof against this explicit construction. Independent review should check these distinctions carefully.

## 5. Reproducibility, credit and source addition

Run `python turn3/check_filtered_image.py`; stdout is frozen in turn3/verification.json. It checks81 grid-face basis substitutions and their linear symbols, inverse basis changes, and18 exact rational difference-matrix ranks, totaling360 new assertions. The imported turn2 path implementation replays its older controls silently; those are not counted again. General tensor injectivity follows from the proof, not the bounded ranks.

Sources: González–Meneses–Paris https://arxiv.org/abs/math/0006014, Theorem1.2 and Proposition2.2; the classical Magnus–Fox group-ring embedding and tensor description, also reviewed with proof in Ara–Dicks, Universal localizations embedded in power-series rings, https://webhomes.maths.ed.ac.uk/~v1ranick/power.pdf, Sections2.3–2.12. The now-recovered published Bellingeri–Funar paper is https://comptes-rendus.academie-sciences.fr/mathematique/item/10.1016/j.crma.2003.11.014.pdf, C.R.Math.338(2004),157–162, published online30December2003. Its full-group theorem and target/universality definitions were checked directly; no source PDF is included in the public packet.

Original unresolved3/5. Informal completion estimate40%; the exact higher-genus obstruction and broader bare-map scope remain for subsequent author turns. No novelty certification.
