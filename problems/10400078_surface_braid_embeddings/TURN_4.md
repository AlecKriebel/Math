# Turn 4 — Higher-genus obstruction with natural degree-zero normalization

AI-assisted mathematical proof candidate; independent review pending. Original unresolved4/5. Unlike the torus case, no faithful map with the natural strandwise degree-zero component exists in the following precisely defined completed target for two strands on a closed surface of genus≥2. This is a scoped obstruction, not nonexistence of every bare map in the original question.

## 1. Statement and target topology

Let Σ be a closed oriented surface of genus g≥2, Π=π1(Σ), G=P₂(Σ), and η:G→Π×Π the natural strandwise homomorphism. Let

D_hat(Σ)=Q⟨⟨t_γ:γ∈Π⟩⟩⋊Q[Π×Π],

with bead action (a,b)·t_γ=t_(aγb⁻¹), as in González–Meneses–Paris for two strands. The completion is by chord degree: each homogeneous coefficient is a finite sum of word/bead basis terms. The proof also allows the larger degreewise completion of the whole crossed product, provided this finite-support property in each degree is retained.

Theorem. Any multiplicative homomorphism θ:G→D_hat(Σ)^× whose degree-zero component is the group-algebra basis element η(β) for every β∈G kills the collision meridian c. In particular θ is not injective.

## 2. Meridian and its large centralizer

Choose a Riemannian metric and ε smaller than its injectivity radius. The map

UΣ→Conf₂(Σ),    (p,v)↦(p,exp_p(εv))

from the unit tangent circle bundle is continuous and sends a positively oriented fiber loop to the collision meridian c, up to the harmless orientation choice. The fiber subgroup is central in π1(UΣ): this is an oriented circle bundle, so monodromy acts trivially on π1(S¹). The projection π1(UΣ)→Π is surjective because the fiber is connected. Thus for every u∈Π there is a braid b_u commuting with c and satisfying η(b_u)=(u,u). No splitting of this circle-bundle extension or of a Fadell–Neuwirth extension is assumed.

The meridian c is nontrivial. The forgetful fibration Conf₂(Σ)→Σ has fiber Σ minus one point, and π2(Σ)=0. Its long exact sequence therefore injects π1(Σ\{p}) into G. The boundary meridian in that punctured surface is a nontrivial word in its free group, so its braid image is nontrivial.

We will also use that c is a commutator in G. The surface-braid presentation in Bellingeri–Funar Theorem2.1, handle skew-commutativity relation, writes σ₁²=[a_r,σ₁⁻¹b_rσ₁⁻¹]. Both arguments have trivial strand permutation, so this is a commutator in the pure subgroup; σ₁² is c with the standard convention. Reversing orientation or conjugating does not affect the argument below. This is a use of the explicit presentation, not an inference from that paper's full-braid universal-invariant theorem.

## 3. Finite-support invariant terms

Every nonidentity element of Π has an infinite conjugacy class. Indeed, by the classical hyperbolic surface argument its centralizer is infinite cyclic: a nontrivial deck transformation has an axis, and commuting deck transformations form a discrete translation group on that axis. Such a cyclic group has infinite index in the closed surface group. For example any finite-index subgroup is again a closed surface group with negative Euler characteristic and noncyclic abelianization. This proves the infinite-conjugacy-class assertion. A primary exposition with the axis proof is Lurie's Lecture36, Lemma1, linked below.

A degree-d basis term of D_hat is

t_(γ1)…t_(γd)·(a,b).

Conjugation by the diagonal bead(u,u) conjugates each of γ1,…,γd,a,b by u. If such a tuple has finite orbit, then each coordinate has finite conjugacy class, hence every coordinate equals the identity e. Therefore the only finite-orbit basis term in degree d is t_e^d·(e,e). A finite linear combination invariant under all diagonal conjugations is supported on finite orbits: coefficients are constant on each orbit and its support is finite. Consequently every invariant degree-d coefficient is a scalar multiple of t_e^d.

The finiteness of each homogeneous support is essential here. Arbitrary infinite sums over conjugacy classes are not elements of the stated completion.

## 4. Leading-term contradiction

Since η(c)=1, write θ(c)=1+terms of positive chord degree. Suppose θ(c)≠1 and let d≥1 be the first nonzero degree, with homogeneous coefficient f_d. The completed grading is separated, so such a least degree exists.

For every u, θ(b_u) has degree-zero term(u,u). Since b_u commutes with c, comparison in degree d of θ(b_u)θ(c)θ(b_u)⁻¹=θ(c) shows that f_d is invariant under diagonal conjugation. Positive-degree corrections in θ(b_u) cannot affect this first nonzero degree. Section3 gives f_d=λ t_e^d with λ≠0.

There is a continuous algebra homomorphism

χ:D_hat(Σ)→Q[[z]],    t_γ↦z for every γ,    (a,b)↦1.

It is well defined because the bead action only permutes chord labels, and each homogeneous coefficient has finite support. Because c is a commutator and Q[[z]] is commutative, χ(θ(c))=1. But the first nonzero coefficient of this series is λz^d, a contradiction. Therefore θ(c)=1, completing the theorem.

For genus1 the diagonal conjugation action is trivial, so the finite-orbit conclusion fails; the torus constructions of turns1–3 are consistent with this theorem. Without the natural degree-zero normalization, θ(b_u) need not lead with(u,u), and this proof gives no general nonexistence assertion.

## 5. Controls, sources and scope

`python turn4/check_invariant_terms.py` replays6,041 exact algebraic identity and hypothesis-boundary checks. They use free-group conjugation identities and an abelian negative control; they do not purport to prove the infinite-orbit theorem, tangent-bundle topology or surface meridian nontriviality. Those are established in the argument with the stated classical inputs.

Primary references: González–Meneses–Paris, https://arxiv.org/abs/math/0006014, for the diagram algebra and kernel setting; Bellingeri–Funar, published https://comptes-rendus.academie-sciences.fr/mathematique/item/10.1016/j.crma.2003.11.014.pdf, Theorem2.1 for the actual commutator relation; Lurie, https://math.mit.edu/~lurie/937notes/937Lecture36.pdf, Lemma1 for the cyclic-centralizer axis argument. The circle-bundle and configuration-space maps are described explicitly above, with only their standard homotopy exact sequences used. No novelty certification or original source resolution is claimed.

Original unresolved4/5. Informal completion estimate50%. The final turn will address what can be forced about degree-zero parts of arbitrary maps and record the remaining unrestricted completed case, rather than silently impose normalization on Kohno's question.
