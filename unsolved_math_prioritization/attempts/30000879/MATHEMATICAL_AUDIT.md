# Mathematical audit of nilpotent twist restrictions

## Scope and conclusion

This is an independent audit of the partial results in `RESEARCH_NOTE.md`, problem 30000879. The reviewed bytes have SHA-256 `734a12ebaa684e20feaba65d7e31db4dbb8892d58ffd02c2fc5b0a7315ab0807` and size 19,481. The conclusion is acceptance of the stated partial results, with a terminology-only coset clarification. This audit does not undertake a new attempt to solve the remaining conjecture.

The underlying question concerns a torsion-free nilpotent group G with finite integral cohomological dimension n, a class α in H²(G,C×), and the global dimension r of the twisted group algebra. It asks for a subgroup on which the class vanishes and whose ordinary complex group algebra has global dimension r. Finite generation is absent from the source hypothesis. The source reports an affirmative answer when r = n, without identifying its proof on the problem page. That prior-status statement is credited, not imported as an audited proof. [1]

The note consistently uses left global dimension. The arguments can be repeated for right modules; this is not an assertion of left-right equality for arbitrary rings. Restriction of α means vanishing of its cohomology class, not pointwise triviality of a chosen representative. No GK, Krull, or topological dimension enters the proof.

## Subgroup freeness and the bimodule splitting

Let B = C^{a|H}H and R = C^aG. For a representative t of an orbit Ht, the map B → Bu_t, b ↦ bu_t, is a left B-module isomorphism: the homogeneous vectors u_hu_t are nonzero scalar multiples of the distinct u_ht. Thus R is the direct sum of the free left modules Bu_t. Similarly, the orbits tH produce the free right summands u_tB. This remains true for a nonnormal H and an infinite index.

Under conventional terminology Ht is a right coset and tH is a left coset. Lemma 1 reverses these two verbal labels while retaining the correct notation and decompositions. The separate patch reverses only the labels; it does not change the mathematics.

The complement V spanned by homogeneous vectors outside H is stable under left and right multiplication by B. Indeed h₁gh₂ ∈ H with h₁,h₂ ∈ H would force g ∈ H. Hence R = B ⊕ V as B-bimodules, and restriction of R ⊗_B M contains M as a B-module direct summand for every left B-module M.

Right B-freeness makes induction exact. Induction sends projectives to projectives because R ⊗_B B is R, and direct summands and sums are preserved. Left B-freeness makes restriction of an R-projective B-projective. A restricted length-r resolution of R ⊗_B M therefore bounds the projective dimension of its direct summand M by r. No arbitrary-subring monotonicity is assumed. Cohomological triviality on H supplies the needed cochain rescaling from B to CH.

**Finding:** Lemma 1 and its use in all subsequent inequalities are correct.

## The final twisted diagonal tensor argument

Let P• → Z be a length-n projective ZG-resolution. Tensoring over Z with C is exact, since C is flat over Z, and yields a projective CG-resolution of C. A direct summand of a free ZG-module becomes a direct summand of a free CG-module; no finite generation of the projectives is needed.

For a CG-module P and an R-module M, define u_h(p ⊗ m) = hp ⊗ u_hm. The composition of u_h and u_k acts as a(h,k)u_hk, so this is genuinely an R-action. In the free case the map

    Φ(u_g ⊗ m) = g ⊗ u_gm

from R ⊗_C M with its free action to CG ⊗_C M with the diagonal action is R-linear. Explicitly, both Φ(u_hu_g ⊗ m) and u_hΦ(u_g ⊗ m) equal a(h,g)hg ⊗ u_hgm. Its inverse on the g-component is g ⊗ v ↦ u_g ⊗ u_g^{-1}v. Every u_g acts invertibly, since the cocycle values are nonzero. Choosing a vector-space basis of M identifies the source with a direct sum of copies of R.

A CG-equivariant splitting remains equivariant for the diagonal action after tensoring with M. Thus P ⊗_C M is R-projective whenever P is CG-projective. Tensoring the resolution with the arbitrary vector space M is exact, and C ⊗_C M with its diagonal action identifies with M. Therefore pd_R(M) ≤ n for every M and gldim(R) ≤ n. The argument needs only cd_C(G) ≤ cd_Z(G); it does not identify these invariants.

**Finding:** The final addition is correct, including cocycle orientation, invertibility, projective summands, and arbitrary-module scope.

## Countability without finite generation

Restriction of a projective ZG-resolution to a subgroup stays projective because ZG is free over the subgroup ring. Consequently G contains no copy of Z^{n+1}; the standard Koszul resolution and nonzero top cohomology give cd_Z(Z^k) = k.

A maximal abelian normal subgroup A exists by Zorn's lemma. Its centralizer C is normal in G. If C/A is nontrivial, it is a nontrivial normal subgroup of the nilpotent group G/A. The last nonzero iterated commutator of that subgroup with G/A is nontrivial and central. One may therefore choose x in C outside A with xA central in G/A. Then ⟨A,x⟩ is abelian, since x centralizes A, and normal, since conjugates of x lie in xA. This contradicts maximality. Thus C_G(A) = A. This argument does not require that G/A be torsion-free.

The torsion-free abelian group A injects into Q ⊗_Z A. Its rational rank is at most n, or finitely many independent elements would generate a forbidden Z^{n+1}. A therefore embeds in a finite-dimensional rational vector space and is countable. Automorphisms extend uniquely to that vector space, embedding Aut(A) in GL_t(Q), which is countable. Conjugation embeds G/A in Aut(A). A countable group of cosets of a countable subgroup gives a countable G. If t = 0, then A = 1 and the self-centralizing argument forces G = 1, so there is no rank-zero exception.

**Finding:** Lemma 2 is valid for the full printed hypothesis and imports no finite-rank structure theorem.

## The telescope and the dimension jump

An exhaustion by subgroups generated by initial segments of an enumeration is cofinal among all finitely generated subgroups. Lemma 1 therefore identifies the local supremum d with the supremum along the exhaustion. Since the preceding diagonal argument gives finite r and subgroup monotonicity gives d ≤ r, d is a nonnegative integer, and at least one finitely generated subgroup realizes it.

For an arbitrary R-module M, the modules N_i = R ⊗_{R_i} M have projective dimension at most d, by right R_i-freeness. The transition maps are well-defined R-linear maps. They need not be injective, and the proof does not use injectivity.

The natural map colim N_i → M is surjective. If a finite tensor sum represents an element in its kernel, all its finitely many coefficients lie in one later R_k. In N_k, the sum becomes 1 ⊗ Σ r_jm_j = 0. This verifies injectivity without a finite-generation condition on M.

For T(ι_i x) = ι_i x − ι_{i+1}f_i(x), the first coordinate of a finitely supported kernel vector is x₁, so x₁ = 0; each later coordinate then forces the next x_i to vanish. Hence T is injective even for noninjective bonding maps. Its cokernel imposes exactly the direct-limit relations. Direct sums of length-d projective resolutions remain projective resolutions, and the Ext sequence of the telescope gives pd_R(M) ≤ d + 1.

Thus d ≤ r ≤ d + 1 is proved for all modules. If r = d and a realizing finitely generated K has a subgroup witness, that subgroup also lies in G. If r = d + 1, any finitely generated H with trivial restriction has gldim(CH) ≤ d and cannot witness r. This does not settle the finitely generated problem or guarantee a witness in the jump case.

Osofsky's Proposition 2.1 records the countable direct-limit bound, and its proof is referred to Berstein. Osofsky explicitly uses right modules on p. 315; the left analogue follows by applying the result to opposite rings. The note's independently checked left-module telescope directly proves the precise claim used here, so that older uninspected proof is not a dependency. [2]

**Finding:** Theorem 3 and Corollary 4 are correct. Countability is of G and the indexing chain, not of the coefficient field or of M.

## The rational augmentation ideal

Every finitely generated subgroup of Q is cyclic, possibly trivial, so the local complex global-dimension supremum is 1. Theorem 3 supplies an upper bound of 2 for CQ.

For either coefficient domain A = C or A = Z, A[Q] is a domain: the largest rational exponent in a nonzero finite sum determines a nonzero leading term of a product. Its augmentation ideal I is not finitely generated. A finite generating set would have support in a cyclic subgroup H. Since its generators have augmentation zero, it would imply I ⊆ A[Q]I_H. But A[Q]/A[Q]I_H is A[Q/H]. The latter has a nonzero augmentation ideal because Q/H is nontrivial, contradicting that inclusion. This also handles a proposed generating set supported only at the identity.

The proof that a nonzero projective ideal J in a commutative domain R must be finitely generated is valid. Choose a split embedding j into a free direct sum and a nonzero x in J. Over the fraction field, J has dimension one, so every j(y) is a scalar multiple of j(x). Any coordinate outside the finite support of j(x) vanishes in the fraction field and hence in R. The retraction restricted to the finitely many remaining coordinates therefore surjects onto J. No noetherian assumption is used.

Thus I is nonprojective. If the trivial module in 0 → I → R → A → 0 had projective dimension at most one, dimension shifting would give Ext¹_R(I,X) = Ext²_R(A,X) = 0 for all X; I would be projective. This contradiction supplies the lower bound two.

For the integral upper bound, apply the telescope only to the trivial ZQ-module. Its restriction to each nontrivial cyclic H has a length-one ZH-resolution. Inducing gives projective dimension at most one for ZQ ⊗_{ZH} Z, and the telescope gives pd_{ZQ}(Z) ≤ 2. It is unnecessary and would be incorrect here to replace this module-specific assertion by a claim that every ZH-module has projective dimension at most one. Combining the bounds yields cd_Z(Q) = 2, as claimed.

**Finding:** Both gldim(CQ) = 2 and cd_Z(Q) = 2 are justified. H = Q is a witness for the original trivial-twist question; this is a reduction obstruction, not a counterexample.

## Central extension splitting at the claimed depth

The cocycle extension E has central kernel C×. Since the image of γ_{c+1}(E) is trivial, that subgroup is central and γ_{c+2}(E) = 1. The usual lower-central commutator inclusion gives [γ_m(E),γ_m(E)] ⊆ γ_{2m}(E) = 1 when 2m ≥ c + 2.

Surjectivity of E → G implies γ_m(E) maps onto γ_m(G): each commutator and every product of such commutators lifts. The complete preimage of γ_m(G) is therefore C×γ_m(E), which is abelian. Merely knowing γ_m(G) itself was abelian would not suffice; the proof correctly establishes abelianness of the preimage.

Divisibility of C× gives its injectivity as an abelian group by the one-element extension argument. The proof's minimal positive k exists whenever the integer subgroup of multiples of x lying in B is nonzero; its generator is exactly what ensures the root choice extends consistently. Extending the identity on C× gives a retraction from the preimage. Its kernel maps injectively and surjectively to γ_m(G), and hence is a section. This is vanishing of the restricted extension class.

**Finding:** Theorem 5 works for any nilpotent G of class at most c ≥ 1, including groups with torsion or without finite generation. Corollary 6 uses equality only as a sufficient condition. For class one its particular subgroup is trivial, so no broad abelian-case resolution is implicit.

## Every-class sharpness of the cutoff

For U = UT_{c+2}(Z), let U_i consist of matrices whose entries at distances below i vanish. Products and commutators show [U_i,U_j] ⊆ U_{i+j}. Elementary matrices at every distance at least i are iterated commutators of length i, using [1 + aE_{pq},1 + bE_{qr}] = 1 + abE_{pr}. Such elementary matrices generate U_i by successively eliminating entries. Hence γ_i(U) = U_i.

The final term U_{c+1} is exactly the central infinite cyclic subgroup generated by z = 1 + E_{1,c+2}. Quotienting by it kills class c + 1 but leaves a nonzero distance-c entry, so G has class c, including c = 1. If u is not in ⟨z⟩, its first nonzero superdiagonal has distance at most c. In every positive power u^k, that diagonal is multiplied by k, since products of two off-diagonal terms have larger distance. Thus no nontrivial quotient element has finite order.

The superdiagonal filtration has finitely many free-abelian coordinate factors, and removing the top coordinate does not introduce torsion. Refining each factor yields a finite series with infinite cyclic factors. For completeness, finite integral cohomological dimension follows by induction: if N is normal in L and L/N ≅ Z, then W = ZL ⊗_{ZN} Z has projective dimension at most cd_Z(N), and 0 → W → W → Z → 0, with map t − 1 on the quotient module, is exact. Therefore cd_Z(L) ≤ cd_Z(N) + 1. This verifies the finite-resolution assertion without a Hirsch-length formula.

Each coset of ⟨z⟩ has exactly one representative with top-right entry zero. Multiplying two representatives changes that entry by the stated integer sum ω. Because z is central, the associative law is precisely the cocycle identity for ω. Thus 2^ω is normalized and C×-valued, even for negative integer exponents.

Let j = floor((c + 1)/2). The selected x and y have distances j and c + 1 − j, both at least j. Their commutator is z, so their images commute, and their two surviving coordinates recover arbitrary integer exponents. They generate Z² in γ_j(G). The two cocycle values are 2 and 1. On any commuting pair, a coboundary has equal values in the two orders, so this ratio detects a nonzero restricted class. This works for every c, including both parity cases and the class-one endpoint.

**Finding:** Theorem 7 proves sharpness of the universal splitting depth. It neither computes the twisted global dimensions of this family nor supplies a counterexample to the original conjecture.

## The isolator obstruction

The coordinate multiplication for P is associative because 2ab′ is bilinear. It has inverse (−a,−b,−t + 2ab). Its center consists exactly of (0,0,t), and [x,y] = (0,0,2), giving the asserted derived subgroup. The power formula is

    (a,b,t)^k = (ka,kb,kt + k(k − 1)ab).

It proves torsion-freeness. A power can lie in the derived subgroup only if a = b = 0; conversely every central element squares into that subgroup. Applying this in both factors proves that the isolator is exactly ⟨z₁,z₂⟩, while [G,G] is generated by their squares.

Central-coordinate parity is a homomorphism to (Z/2)² because the product defect is even. The stated sign cocycle is bilinear over F₂. It is pointwise trivial on the derived subgroup, whose parity is zero, yet has commutator ratio −1 on z₁,z₂. A coboundary cannot have that ratio on the commuting central pair.

**Finding:** The example is valid and refutes the stated isolator strengthening, while respecting Theorem 5.

## Boundaries and final acceptance

Every nontrivial torsion-free group contains an infinite cyclic subgroup. Lifting its generator to the central extension and taking integer powers splits the restriction. Together with Lemma 1 this gives r ≥ 1 for nontrivial G and supplies a witness when r = 1. If r = 0, G must be trivial, and the trivial subgroup is already a witness. Thus the omitted degenerate boundary causes no gap.

The accepted results leave 2 ≤ r < n unaddressed once the source's r = n result is credited. Neither a finitely generated reduction nor an automatic lower-central witness is promoted to a general proof. No theorem from quantum-torus literature, no unverified Hirsch-length formula, and no unaudited r = n proof is used. Finite tests supplement the deductions above; acceptance rests on the mathematical arguments.

## Sources

[1] *Mini-Workshop: Arithmetik von Gruppenringen*, Oberwolfach Report 55/2007, E. Aljadeff's Problem 3, printed p. 3171, PDF p. 23. [Publisher PDF](https://ems.press/content/serial-article-files/46141).

[2] B. L. Osofsky, *Upper bounds on homological dimensions*, Nagoya Mathematical Journal 32 (1968), 315–322, Proposition 2.1 and Theorem 2.3, printed pp. 320–321. [DOI](https://doi.org/10.1017/S002776300002674X).
