# Universal corks and the five obstructions that do not yet settle them

## Result and target

**Unresolved.** This record concerns catalogue ID 2890, rank 693, KP-4.14, identified with Problem 4.14 in the 2026 K3 problem list, preliminary printed pages 201–202. It is not the problem numbered 4.14 in the 1997 list. No universal cork, obstruction to every possible cork, or new solution is established here. The five approaches below yield scoped deductions and precise missing steps.

The question asks for one compact contractible smooth four-manifold C and one nonextendable boundary diffeomorphism f which, by varying a smooth embedding e:C→X, changes every closed simply connected exotic pair (X,X') into one another. Write Y=∂C, E_e=X\int(e(C)), and

    X(e,f)=E_e ∪_(e∘f) C.

The embedding may depend on both X and X'. Its complement is not required to be simply connected. The map f is fixed; the target does not merely allow an arbitrary boundary map or a power of f for each pair. The K3 definition does not impose Steinness, finite order, or the involution condition.

### Orientation and boundary scope

The displayed K3 question omits the word “oriented.” Its accompanying discussion distinguishes a cork C from −C and explicitly considers allowing either orientation as a different convention. We therefore state all orientation-sensitive deductions below in the usual **oriented, orientation-preserving** convention, rather than silently identifying the two versions. Simply connected manifolds are orientable, but orientability does not remove this distinction. If arbitrary orientation-reversing embeddings are allowed, the two-orientation version must be considered separately; nothing here solves it either.

Ladu's inspected arXiv v3 defines corks using orientation-preserving involutions. Its theorems must not be cited as theorems about every arbitrary-order boundary diffeomorphism without an additional argument. All uses of its named theorems below retain that restriction. By contrast, the elementary complement, stabilization-extension, and gluing lemmas below allow arbitrary orientation-preserving f. Boundary-universal, boundary-relative, fixed-embedding, and closed-universal statements are kept distinct.

## Common elementary facts

Let C be a compact contractible oriented smooth four-manifold and let C lie in the interior of a connected closed oriented smooth four-manifold X. Set E=X\int C.

**Lemma 0.1 (boundary and complement).** Y is an integral homology three-sphere; E is connected; inclusion induces an isomorphism H₂(E;Z)→H₂(X;Z). For every orientation-preserving self-diffeomorphism f of Y, this gives a canonical intersection-form identification H₂(X;Z)≅H₂(X(e,f);Z). Moreover

    π₁(X(e,f)) ≅ π₁(E)/normal(im(π₁(Y)→π₁(E))) ≅ π₁(X).

These group identifications do not require π₁(E)=1.

**Proof.** Poincaré–Lefschetz duality gives H_i(C,Y;Z)≅H^(4−i)(C;Z), which is Z only for i=4. The long exact sequence of (C,Y) consequently gives H₃(Y)=Z, H₂(Y)=H₁(Y)=0, and H₀(Y)=Z. A connected boundary of a codimension-zero submanifold has a connected collar on the exterior side. Any exterior component meeting C meets this collar; any component not meeting C would be a component of X. Thus E is connected.

The Mayer–Vietoris segment H₂(Y)→H₂(E)⊕H₂(C)→H₂(X)→H₁(Y) has zero outer terms and H₂(C)=0, proving the isomorphism; the identical argument applies after regluing. Classes can be represented by smooth closed oriented surfaces in the interior of E: realize a class by a surface map, put it in general position, and resolve its transverse double points by local oriented tubing. Push away from the boundary using a collar. Intersections of representative cycles, and hence the integral pairing, are computed inside E and are independent of the regluing. Finally van Kampen kills the full image of π₁(Y) because π₁(C)=1. Precomposing that image map by the automorphism f_* does not change its image or normal closure. ∎

When X is simply connected, its H₂ is torsion free by duality and the universal coefficient theorem, so the forms here are ordinary unimodular integral forms. The lemma explains why ordinary homology, signature, Euler characteristic, and fundamental group cannot distinguish a cork twist from its original ambient manifold. It proves neither homeomorphism nor diffeomorphism by itself; a homeomorphic conclusion uses the usual extension/classification theorems.

## Approach 1  Adjunction bounds and the cost of changing embeddings

The attempted obstruction was to bound all possible outputs using the fact that a cork has no second homology. The strongest direct bound instead depends on the exterior.

Fix b₂(X)=r>0. Choose integral classes v₁,…,v_r in H₂(E;Z) forming a rational basis and closed embedded oriented representatives Σ_i in int E. Write g_i=g(Σ_i), q_i=v_i² and

    B(E;Σ₁,…,Σ_r)=max_i(2g_i−q_i).

For a closed smooth Z with positive second Betti number, define J_Z as the infimum, over integral rational bases of H₂(Z), of the largest value of 2g_Z(v)−v². We allow the value −∞: no lower bound or nonnegativity is assumed in this elementary argument. When this set of integers is bounded below, its infimum is a minimum and agrees with the adjunction 1-genus used by Yasui. This extended-infimum convention makes the bound below valid without imposing an unproved finiteness assertion.

**Proposition 1.1 (fixed-exterior bound).** For every orientation-preserving boundary gluing f,

    J_(X(e,f)) ≤ B(E;Σ₁,…,Σ_r).

**Proof.** Lemma 0.1 transports the same v_i to a rational basis in every glued manifold, with the same squares q_i. Each Σ_i survives as an embedded surface there, so its minimal genus is at most g_i. Take the maximum of these inequalities and then the infimum over all bases of the glued manifold. ∎

This is the contractible-piece specialization of the mechanism in Yasui, Proposition 3.2. It holds for all gluing maps at one embedding, not just one involution.

**Corollary 1.2 (necessary exterior complexity).** Suppose a fixed (C,f) embedded in a fixed X realizes a sequence X_j with J_(X_j) unbounded. For every realizing sequence e_j and every choice of exterior basis surfaces Σ_(j,i), the numbers B(E_(e_j);Σ_(j,1),…,Σ_(j,r)) are unbounded. In particular, finitely many embeddings cannot realize this sequence, even if each embedding is allowed all boundary diffeomorphisms.

**Proof.** Apply Proposition 1.1 to each j. For finitely many embeddings, choose a basis system once for each, and take the maximum of the finitely many resulting bounds. ∎

**Source check and failed completion.** Yasui's Theorem 1.3 supplies closed examples where no one fixed submanifold with b₁ of its boundary less than n generates all smooth structures by varying gluing maps. It does not keep one abstract cork while allowing arbitrary embeddings. Theorem 1.11 does vary embeddings, but its hypothesis is

    b₂(W)−4b₁(∂W)>11n+10,   n≥1.

For a cork its left side is 0, so the theorem does not apply. Trying to remove the embedding dependence from Proposition 1.1 therefore stops at an unproved uniform bound on exterior basis genera. The topology of C alone gives no such bound in this argument. Corollary 1.2 is a necessary condition on a proposed universal realization, not a contradiction.

## Approach 2  The Floer difference element

In the involutive oriented setting of Ladu, let x_C be the relative mod-2 monopole invariant of C and let F=f_* on its boundary Floer homology. The difference element is Δ_C=x_C−F(x_C). The inspected Proposition 3.2 places Δ_C in reduced grading −1 and states that Δ_C=0 forces preservation, under an intersection-form identification, of every mod-2 Seiberg–Witten invariant of closed simply connected ambient manifolds with b₂⁺≥2. This is an external Floer theorem, not proved by the finite checker.

The elementary mechanism is the linearity identity

    λ(x_C)−λ(F(x_C)) = λ(Δ_C)

for the appropriate complement gluing functional λ. A zero difference element vanishes under every possible λ; this is an embedding-independent obstruction. Ladu's Corollary 1.3 excludes the Akbulut–Yasui family and their orientation reversals from fixed-orientation universality. The published abstract confirms the nonuniversality of the named family. None of this asserts that every cork belongs to the zero-difference class.

**Lemma 2.1 (orientation reversal).** In the oriented convention, if (C,f) is universal, then (−C,f) is universal.

**Proof.** Given an oriented exotic pair (X,X'), apply universality of (C,f) to (−X,−X'), and then reverse all orientations in the resulting decomposition and diffeomorphism. The underlying boundary map is the same. ∎

Consequently, within the involutive setting of Proposition 3.2 and the existence of closed pairs whose mod-2 invariants differ, any universal candidate must escape the zero-difference obstruction in both orientations. This is only a necessary condition.

We tried to extend the obstruction by a dimension count. That step fails for a precise algebraic reason.

**Lemma 2.2 (a nonzero vector has arbitrarily prescribed evaluations).** Let V be a finite-dimensional vector space over F₂ and let 0≠δ∈V. For every m≥1 and every bit vector b∈F₂^m there are linear functionals λ₁,…,λ_m∈V* such that λ_i(δ)=b_i.

**Proof.** Extend δ to a basis, and let μ be its dual coordinate functional. Set λ_i=b_i μ. ∎

Even a fixed nonzero difference vector therefore puts no restriction, from dimension alone, on an arbitrarily long list of values evaluated by independently varying maps. This is an abstract countercontrol to the proposed linear-algebra shortcut. It does not claim that every such functional occurs as a four-manifold complement map. A successful obstruction would have to control the **geometrically realizable** complement maps, including Spin^c data and gradings. We do not have that control.

**Source ambiguity quarantined.** K3 Remark 2 says that allowing either C or −C leaves a version of Akbulut universality open. The inspected older arXiv v3 of Ladu has a stronger-looking two-orientation Theorem 1.2. The publisher's full text was not accessible; only its abstract and preview were verified. We do not reconcile these statements by fiat and do not use the stronger two-orientation conclusion to classify the modified question. In particular no solution of any orientation-flexible variant is claimed.

## Approach 3  Cobordism complexity and capping

For a normal handle decomposition D of a five-dimensional h-cobordism, let A_i be the attaching two-spheres of its three-handles and B_j the belt two-spheres of its two-handles. There are k of each and A_i·B_j=δ_ij. Its Morgan–Szabó complexity is

    c(D)=Σ_(i,j)|A_i∩B_j|−k.

Minimizing over normal decompositions gives c(Z). For endpoints (X,X'), define c_pair(X,X') as the minimum of c(Z) over **all** h-cobordisms with those endpoints. This second minimum is essential. Use only the smooth oriented simply connected setting in which the required h-cobordisms and normal decompositions exist. Ladu's Definitions 4.1–4.2 make these distinctions explicit.

**Lemma 3.1 (parity).** Every c(D) is a nonnegative even integer.

**Proof.** Let p_ij and n_ij count positive and negative intersection points. The algebraic condition says p_ij−n_ij=δ_ij. Therefore p_ij+n_ij=δ_ij+2n_ij. Summing gives c(D)=2Σn_ij. ∎

**Proposition 3.2 (relative-cobordism transfer).** Suppose a fixed contractible C and boundary map f admit a relative h-cobordism Z_C:C→C realizing f on the side boundary, with a normal decomposition of complexity q. Then every oriented cork twist pair (X,X(e,f)) has c_pair≤q.

**Proof.** Glue E×I to the side boundary of Z_C using the original boundary marking and product collars. Choose the direction of the relative side marking so that the outgoing gluing is e∘f. If the opposite convention was used, reverse Z_C; this inverts its relative marking and interchanges attaching and belt spheres, preserving q. The two ends are then X and X(e,f). The inclusions of either end are homotopy equivalences: gluing an h-cobordism to a product along a product side preserves that property, equivalently by the homotopy gluing lemma for these collared CW pairs. The normal Morse function on Z_C extends by the interval coordinate on E×I, adding no critical points. The same handle attaching and belt spheres retain their geometric intersections, yielding a decomposition of complexity q. Minimize over all h-cobordisms of the closed pair. ∎

Ladu's Lemma 4.6 gives this inequality for involutive corks. Thus an unbounded sequence of **minimum pair** complexities for closed exotic pairs would refute universality of any candidate to which the finite relative-cobordism construction applies. The available boundary examples establish that route for the boundary problem, using an invertible cobordism which keeps the relative information recoverable. Arbitrary closed caps do not come with that property.

The attempted closed upgrade fails twice:

1. A chosen inertial cobordism Z:X→X can be complicated even though c_pair(X,X)=0, witnessed by the product. This is an actual logical obstruction to using large c(Z) as a lower bound on the endpoint pair.
2. Ladu's 2025 paper, Theorem 1.2 and Section 6, constructs particular isometries and the corresponding h-cobordisms of arbitrarily large complexity between closed exotic endpoints. It does not show that every isometry, or every h-cobordism between the same endpoints, has that complexity. Its proof tracks the marked isometry R_m. Minimizing over all endpoint identifications is not justified.

**Lemma 3.3 (capping is one-way).** If a diffeomorphism h:A→B agrees on the boundary with a fixed gluing identification, it extends over any common cap by the identity. The converse needs extra hypotheses requiring a diffeomorphism of the capped manifolds to preserve the cap and its boundary marking.

**Proof.** In the forward direction the two maps agree at the identified boundary, and product collars make their union smooth. In the converse direction, a general closed diffeomorphism supplies no restriction A→B unless it sends the designated cap to the designated cap. Even setwise preservation alone gives an uncontrolled boundary self-diffeomorphism. ∎

Hence neither an arbitrary cap nor the newer large-cobordism theorem supplies the missing closed, unmarked lower bound.

## Approach 4  Stabilization distance

Put H=S²×S². Define the relative extension height h(C,f) as the least n≥0 for which f extends to an orientation-preserving diffeomorphism of C#nH, with connected sums taken in its interior. If such an n is not known to exist, regard the height as infinite. Define s(X,X') similarly using a diffeomorphism X#nH≅X'#nH. Existence of some finite relative height is the stabilization result quoted in K3 Remark 4; here the deduction from a specified extension is proved directly, rather than reproving Wall/Gompf theory.

**Proposition 4.1 (relative extension bounds every embedding).** If h(C,f)≤n, then s(X,X(e,f))≤n for every interior embedding.

**Proof.** Perform the n connected sums inside the embedded C. Write j:∂C→∂E for the original boundary marking, C_n=C#nH, and choose F:C_n→C_n with F|∂C=f. The original stabilized manifold is E∪_j C_n and the twisted stabilized manifold is E∪_(j∘f) C_n. The identity on E together with F^−1 on C_n gives a map from the former to the latter: the former identifies c with j(c), while the latter identifies F^−1(c)=f^−1(c) with j(f(f^−1(c)))=j(c). Using collars, arrange both restrictions as product maps near the boundary; their union is a smooth diffeomorphism. ∎

**Corollary 4.2.** A universal candidate of finite height n gives a global bound n for all closed simply connected exotic pairs. A finite menu of candidates with heights n_i gives the bound max n_i if one twist from that menu suffices for every pair. Allowing either orientation of a candidate does not change its height: reverse orientations in an extension and use the orientation-reversing diffeomorphism of H obtained by reflecting one S² factor to identify −H with H.

This deduction is stronger than “each pair eventually stabilizes”: it swaps the dependence of n from the pair to one fixed cork. The reverse implication is unproved; a uniform number of stabilizations does not choose one cork or a common boundary map.

The attempted contradiction would require unbounded s(X,X') among **closed simply connected** pairs. Kang's inspected v3 proves an absolute boundary example surviving one stabilization and explicitly leaves a closed example as Question 1. Guth–Kang's July 2026 accepted version, Theorem 1.8, supplies infinitely many contractible boundary examples surviving one stabilization. Neither is an unbounded closed-distance theorem. Nontrivial stabilized diffeomorphisms or exotically embedded surfaces are also not pairs of nondiffeomorphic closed ambient manifolds. Finally c(Z) counts excess intersections, whereas stabilization complexity counts handles; they must not be identified.

## Approach 5  Constructing a common cork by gluing normalization

The constructive attempt starts from the known pair-dependent cork theorem and asks whether all boundary gluings can be converted to a single model. The following elementary classification states exactly what such a normalization gives when the pieces really are fixed.

Let E and C be fixed compact oriented smooth manifolds with connected boundary, and fix an orientation-reversing marking j:∂C→∂E. For g∈Diff⁺(Y), write X_g=E∪_(j∘g) C. Let Γ=π₀Diff⁺(Y). Define two subgroups:

    A={ [j^−1 a|∂E j] : a∈Diff⁺(E) },
    B={ [b|Y] : b∈Diff⁺(C) }.

**Proposition 5.1 (piece-preserving double-coset classification).** There is an orientation-preserving diffeomorphism X_g→X_h which maps E to E and C to C if and only if

    [h] ∈ A[g]B.

**Proof.** If the diffeomorphism restricts to a on E and b on C, the boundary compatibility is

    a|∂E ∘ j ∘ g = j ∘ h ∘ b|Y.

After conjugation by j, this says h=α g β^−1, with [α]∈A and [β]∈B, so [h] lies in A[g]B. Conversely, an equality of mapping classes of that form can be represented by extending diffeomorphisms a,b. Any residual boundary isotopy is extended over a collar, so after changing a or b in its collar the displayed compatibility is exact. Straightening the maps in product collars and gluing a to b gives the required smooth diffeomorphism. ∎

**Corollary 5.2 (nonextension alone is insufficient).** The condition [f]∉B does not show that twisting a given embedding is effective. If [f]∈A, then X_f≅X_id by a piece-preserving diffeomorphism, even though f may not extend over C.

**Proof.** Take g=id and h=f in Proposition 5.1; since id∈B, membership in A suffices. ∎

This is a conditional gluing statement, not an assertion that arbitrary chosen groups A,B occur for cork exteriors. The exact permutation-group controls illustrate the algebra only.

**Why the universal construction stops.** A cork provided by the pair-dependent decomposition theorem need not be diffeomorphic to a fixed C, and its boundary need not be identified with Y. Proposition 5.1 cannot even be applied before establishing those identifications. Even if a boundary identification is supplied, it only classifies diffeomorphisms preserving the prescribed pieces. The target permits different embeddings and arbitrary final diffeomorphisms, neither of which preserves a preferred splitting. Melvin–Schwartz's finite cork theorem varies the power of its boundary map, and its underlying cork depends on the finite family. The checked final arXiv v2 explicitly reports that several infinite-order results from v1 were removed because of errors; no removed result is used here. There is no compactness principle turning those finite realizations into a single compact cork with one fixed f for all pairs.

The missing constructive theorem would have to produce that one compact smooth pair and compatible embeddings for every exotic pair. We do not have it. Replacing a compact cork by an infinite union, assuming every complement has the same boundary extension group, or retaining a prescribed cap would change the problem.

## What is established and what is not

The complete elementary proofs above establish the complement identifications, an exterior-dependent genus bound and its necessary-growth consequence, linear-algebra limits of a Floer dimension shortcut, orientation reversal, parity and transfer of an assumed relative cobordism, the relative-extension stabilization bound, and a fixed-splitting double-coset criterion. The deep existence, Floer, cork-decomposition, and stable-extension theorems are credited external inputs. They have not been formally verified or reproved here.

No finite calculation produces a smooth four-manifold, computes its Floer invariants, certifies a smooth embedding, or proves a universal quantifier over embeddings. No discovery, priority, or human peer-review claim is made. The exact status is **unsolved after five distinct approaches**. References, manuscript versions, inspection limits, and public-source fingerprints are in SOURCE_VERIFICATION.md and SOURCE_METADATA.json.
