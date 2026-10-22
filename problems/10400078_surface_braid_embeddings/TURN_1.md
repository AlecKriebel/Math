# Turn 1 — Two-strand torus: completion and universality make different questions

AI-assisted mathematical proof candidate; independent review pending. Original unresolved 1/5. This is a complete result for explicitly defined standard targets, not a full answer for every closed surface and every strand number.

## 1. Fix the diagram algebras precisely

Use the horizontal labelled-chord algebra described by González–Meneses–Paris, Section1.4. For two strands on the torus, let Λ=π1(T²)=Z². There are no three-distinct-strand or four-distinct-strand relations. After identifying t_(2,1,γ) with t_(1,2,−γ), the chord-only algebra is therefore the free associative algebra

R=Q⟨t_γ : γ∈Λ⟩.

Let H=Λ×Λ=Z⁴ act by (u,v)·t_γ=t_(γ+u−v), as follows directly from the two bead-action formulas in that source. Define

D_pol=R⋊Q[H],
D_hat=R_hat⋊Q[H],

where R_hat is the chord-degree completion. Our elements of D_hat have finite H support, so they also lie in any larger completion allowing degreewise finite bead support. The multiplication convention is (r h)(s k)=r(h·s)hk. These are the pure-braid versions of the published completed crossed product, omitting the symmetric-group factor. No symplectic/augmentation-filtration diagram algebra is substituted.

The exact Ohtsuki question does not explicitly spell out completion. D_hat is the usual completed finite-type target; D_pol is its finite-sum counterpart. We keep both visible rather than infer a missing convention as a full resolution.

## 2. Explicit rational injection into the completed target

There is an injective multiplicative map

P₂(T²) → D_hat^×

defined over Q (in fact its series have integral coefficients).

Proof. The torus group law gives a homeomorphism

Conf₂(T²) → T²×(T²\{0}),    (x,y)↦(x,y−x),

with inverse (x,z)↦(x,x+z). Hence P₂(T²)≅Z²×F₂, since the punctured torus retracts to a wedge of two circles. Choose a free basis x,y for F₂. Choose distinct chord labels 0 and η=(1,0), and put X=t_0,Y=t_η. The subalgebra Q⟨X,Y⟩ is free and embeds degreewise, and therefore after completion, in R_hat.

The classical Magnus map μ:F₂→Q⟨⟨X,Y⟩⟩^× sends x↦1+X,y↦1+Y and their inverses to the corresponding geometric series. For completeness, write a nonidentity reduced word in maximal syllables as x_(i1)^(a1)…x_(ik)^(ak), with each a_j a nonzero integer and adjacent indices distinct. In the product Π(1+X_(ij))^(aj), the coefficient of the alternating-block word X_(i1)…X_(ik) is Πa_j, nonzero over Q. Indeed that target word has k nonempty blocks, so all k factors must contribute a positive power, and total degree k then forces degree one from each. Skipping any factor cannot create k blocks. Thus μ is injective. This is the standard Magnus argument, not a new free-group embedding theorem.

The diagonal subgroup ΔΛ={(u,u):u∈Λ} acts trivially on every t_γ, and hence centralizes R_hat. Define

Θ(u,w)=μ(w)·(u,u).

The commuting factors make Θ a homomorphism. Its chord-degree-zero component is the group-algebra basis element (u,u). If Θ(u,w)=1, that component forces u=0; Magnus injectivity then forces w=1. All coefficients are integers and the map is therefore rational. This proves the assertion.

## 3. No injection into the finite-sum target

In contrast, there is no injective multiplicative map P₂(T²)→D_pol.

First, D_pol is a domain. R is a free associative algebra and has no zero divisors, by its leading-word argument. Totally order the free abelian group H by a translation-invariant lexicographic order. For two finite nonzero crossed-product sums, the product of their greatest H-support terms is the unique greatest support term; its coefficient is a product of a nonzero coefficient and an automorphic image of another, so is nonzero. Therefore their product is nonzero.

The action preserves chord degree. The greatest homogeneous degree in a product is the sum of the greatest degrees, since the leading homogeneous factors have nonzero product in the domain. If u,v are inverse units of D_pol, their greatest degrees sum to zero, so both have degree zero. Consequently every unit is a unit of Q[H]. Conversely those are units in D_pol. Units of the Laurent polynomial ring Q[Z⁴] are precisely nonzero rational multiples of its monomials. One elementary proof compares the greatest and least supports in the same ordered group: their widths add under products, and a product with singleton support forces each factor's support width to be zero. Thus D_pol^×=Q^××Z⁴ is abelian.

But P₂(T²)≅Z²×F₂ is nonabelian, so it cannot embed into this abelian unit group. A group homomorphism into a unital algebra takes values in units. Even if only multiplicativity were stated, an injective map into this domain has nonzero idempotent identity image, hence image identity1, so the same argument applies.

This negative result is expressly for the uncompleted finite-sum target. It must not be promoted as a refutation of the usual completed interpretation.

## 4. Why the positive injection is not a universal expansion

The loop around the missing point of the punctured torus is a commutator of its two free generators, up to inversion and conjugacy. It represents the basic two-strand collision meridian. Under the constructed map,

μ([x,y])=1+XY−YX+terms of degree at least3.

There is no linear chord term. Thus the basic nonzero first-order Vassiliev chord class is not sent to its first-order class, and this construction does not induce the required associated-graded isomorphism of a universal expansion. Its free generators were deliberately encoded into positive chord degree rather than their original strandwise degree-zero beads. Injectivity alone permits this. Bellingeri–Funar's obstruction to universal multiplicativity is therefore consistent with this explicit bare injection.

For comparison, n=1 on any closed surface has the elementary degree-zero group-algebra inclusion π1(Σ)→Q[π1(Σ)], provided that standard bead convention is used. Neither this nor the two-strand torus theorem settles higher n or other positive genera. The sphere has separate low-strand/torsion issues and is not treated here.

## 5. Sources, checks, and status

Primary target definition and bead action: González–Meneses–Paris, https://arxiv.org/abs/math/0006014, Section1.4, pp.3–4 of the manuscript, Theorem1.3. Their universal invariant is a module map with graded algebra isomorphism, not the multiplicative injection constructed here. Bellingeri–Funar, https://arxiv.org/abs/math/0309245 and the author manuscript linked in SOURCE_GATE.md, supplies the separate universal obstruction. The original Kohno problem is Ohtsuki Section3.10 printed443–444, https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf. Classical Magnus embedding is credited; its needed injectivity argument is supplied in full above.

Run `python turn1/check_magnus.py`; stdout is frozen in turn1/verification.json. It checks1,456 reduced words through length6 and their inverse products,680 syllable coefficient identities, and729 bead translations/diagonal centralizations, totaling4,402 exact assertions. These controls supplement, rather than replace, the general proofs.

Original unresolved1/5. Completion and universality qualifications are essential. Informal completion estimate20%; no global injection/nonexistence theorem, originality certification, or source-literal resolution is claimed.
