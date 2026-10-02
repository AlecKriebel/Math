# Turn 2 — A faithful completed torus map preserving strandwise degree zero

AI-assisted mathematical proof candidate; independent review pending. Original unresolved 2/5. This improves the explicitly completed two-strand torus result, without claiming a universal expansion or a result for other genera/strand numbers.

## 1. Target and normalization

Retain D_hat=Q⟨⟨t_γ:γ∈Z²⟩⟩⋊Q[Z²×Z²] from turn1. An element (u,v) acts on t_γ by translation γ↦γ+u−v. Let U=(0,e1) and V=(0,e2) be degree-zero bead elements, so U and V commute and shift chord labels by −e1 and −e2.

Under the configuration homeomorphism (x,y)↦(x,y−x), identify P₂(T²)=Z²×F(x,y). The natural map recording each strand's torus loop is

η(u,w)=(u,u+ab(w)),

where ab(x)=e1 and ab(y)=e2. We construct an injective rational homomorphism Θ whose chord-degree-zero component is exactly η, rather than the smaller diagonal projection used in turn1.

Define Φ:F(x,y)→D_hat^× by

Φ(x)=U,    Φ(y)=(1+t_0)V,

and set Θ(u,w)=(u,u)Φ(w). The diagonal bead subgroup centralizes both the chord algebra and all bead elements, so this is a homomorphism. Its degree-zero component is η by construction. The main issue is injectivity.

## 2. A free-group lattice-path lemma

Let F(Z) be the free group with basis {z_γ:γ∈Z²}. Let H=Z² act by h·z_γ=z_(γ−h). Define

ψ:F(x,y)→F(Z)⋊H,    x↦(1,e1), y↦(z_0,e2).

Then ψ is injective.

Proof. Follow the lattice path starting at0 whose letters x,x⁻¹ move right/left and y,y⁻¹ move up/down. A positive vertical edge beginning at position p contributes z_(−p). A negative vertical edge ending at position p contributes z_(−p)⁻¹. Horizontal edges contribute no free letter. The resulting product of vertical-edge labels, together with the final displacement, is exactly ψ(w), by the semidirect-product multiplication rule.

Suppose w is a nonempty freely reduced word. If it contains no vertical letter, it is a nonzero power of x and has nonzero displacement. Otherwise examine consecutive vertical letters in its label word. If separated by a nonempty horizontal block in w, that block is a nonzero power of x, so the two vertical edges lie in different columns and their z-labels cannot cancel. If no horizontal block separates them, they belong to one maximal vertical run. A freely reduced run consists entirely of upward or entirely of downward steps. Its consecutive labels have the same exponent sign and cannot cancel. Therefore the entire vertical-label word is already freely reduced and nonempty. Its free-group component is nontrivial, proving injectivity. This proof applies to arbitrarily long words, not just the finite checker.

## 3. Equivariant Magnus embedding and faithfulness

The classical Magnus map z_γ↦1+t_γ embeds F(Z) into the units of the completed free associative algebra. Its injectivity is proved by the finite-syllable coefficient argument in turn1; any particular group word uses only finitely many of the generators, so the countable basis causes no difficulty. Relabelling the generators commutes with this embedding. Thus it is H-equivariant and induces an injective map

F(Z)⋊H → Q⟨⟨t_γ⟩⟩⋊Q[H].

Here injectivity follows directly from the unique group-algebra support: an image equal to1 has displacement0 and then has trivial free-group component. Identify H with the second-strand bead subgroup of D_hat. Composing with ψ gives precisely Φ, proving Φ injective.

Finally Θ(u,w)=1 forces u=0 by the first bead coordinate of its degree-zero component, and then Φ(w)=1 forces w=1. This proves the claimed rational injection with the natural strandwise degree-zero map. All coefficients are integral. The group factor and target algebra are exactly those defined in turn1; no completion of the bead group algebra is used.

## 4. The first-order limitation is explicit

For the collision meridian c=[x,y], up to the usual orientation convention,

Φ(c)=(1+t_(−e1))(1+t_0)⁻¹
     =1+t_(−e1)−t_0+terms of degree at least2.

Thus its linear symbol is a difference of two chord labels, not the canonical single meridian chord. More generally, for w∈ker(ab:F₂→Z²), the sum of coefficients of all linear chord terms in Φ(w) is the signed number of vertical steps of the closed lattice path, hence0. This is a direct obstruction to a surjective normalized first-order expansion: a single standard chord has coefficient sum1.

To see the same obstruction on the full first filtered quotient, group a finite linear combination of braids by their common strandwise degree-zero element h=(u,u+ab(w)). Within such a group the vertical exponent sum of w is fixed. If the combination lies in the kernel of the degree-zero map, its scalar coefficients sum to0 in each h block. Consequently the total linear-chord coefficient in each bead block of its image is0. The degree-one target element t_0 with identity bead support has coefficient sum1 and cannot be in that first-order image. This proves failure of surjectivity, independently of whether the first-order map is injective.

The completed homomorphism respects the filtration by powers of the kernel of the strandwise degree-zero map: it sends that kernel into positive chord degree and hence its dth power into degree at least d. It is nevertheless not an associated-graded isomorphism. We do not call it a universal Vassiliev expansion. The separate Bellingeri–Funar obstruction and the source's omission of explicit universality remain as explained in the gate; no contradiction with a canonical universal-expansion theorem is asserted.

## 5. Checks, credit and status

`python turn2/check_lattice_embedding.py` exactly checks the path formula and absence of free cancellations for all4,373 reduced words of length≤7, including the identity. It tests2,809 products of words through length3 and the explicit commutator formula, totaling15,930 assertions. The frozen stdout is turn2/verification.json. These controls supplement the general reduced-word proof.

The diagram crossed-product action is credited to González–Meneses–Paris, https://arxiv.org/abs/math/0006014, Section1.4. The formal-series faithfulness is the classical Magnus embedding, with its needed proof supplied here and in turn1. The torus configuration splitting is the elementary difference-coordinate homeomorphism. No historical novelty is claimed for the construction or these ingredients.

Original unresolved2/5; only the explicitly completed two-strand torus case is affirmative, now with its natural degree-zero map. Informal completion estimate30%. Higher strand numbers, other positive genera, and exact source completion/universality conventions remain outside this result.
