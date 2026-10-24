# Kourovka 21.139 — homology, L², Alexander, and finite-cover mechanisms

**Checkpoint:** 2026-10-17 21:40 UTC. **Status:** partial deductions, no full resolution. **Best-guess completion toward the full discovery goal: 10%.** The central positivity/classification gap remains. This report does not claim novelty for the elementary reductions or known results below.

## Exact target and conventions

Let G be hyperbolic and virtually compact special. Define vb₂(G)=sup{dim_Q H₂(H;Q):[G:H]<∞}. The target is to prove or disprove that vb₂(G)<∞ forces G virtually free or virtually a closed surface group. Every finite-index subgroup is quantified; boundedness on a cyclic tower or sublinear growth on a residual tower is insufficient. Finite and virtually cyclic groups satisfy the virtually-free alternative.

The following deductions have checkable proofs. Main background sources are [Haglund–Wise](https://www.imo.universite-paris-saclay.fr/~frederic.haglund/special%28corrected%29.pdf), [Arzhantseva](https://www.mat.univie.ac.at/~arjantseva/Abs/quasi.pdf), [Lück](https://www.math.uni-bonn.de/people/lueck/data/r.pdf), and [Kielak–Linton](https://link.springer.com/article/10.1007/s00039-024-00687-6). Source snapshots and hashes are recorded in sources_homology/manifest.json. The independently checked algebra appears in homology_adversarial.md.

## 1. Finite-index passage and stabilization

For K≤H of finite index, inclusion followed by homological transfer is multiplication by [H:K] on H₂(H;Q). Consequently b₂(K)≥b₂(H). If G₀≤G has finite index, every finite-index H≤G has H∩G₀ of finite index in G₀. Hence

    vb₂(G₀)=vb₂(G).

Thus one may pass to a torsion-free compact-special G₀ without losing the hypothesis or changing the desired virtual conclusion. A compact nonpositively curved cube complex is a finite K(G₀,1). The special group embeds in a right-angled Artin group and is residually finite. Further finite-index passage remains allowed. Finite groups are disposed of separately.

If C=vb₂(G)<∞, it is an attained integer. Choose finite-index G₁ with b₂(G₁)=C. For every finite-index H≤G₁, the inequalities C≤b₂(H)≤C give equality. Transfer/restriction implies that

    res: H²(G₁;Q) → H²(H;Q)

is an isomorphism. If H is normal, the deck action G₁/H on H²(H;Q) is trivial: every class is the restriction of a G₁-class. The finite-quotient Hochschild–Serre spectral sequence over Q therefore gives, for every finite-image rational representation V of G₁,

    H²(G₁;V) ≅ H²(G₁;Q) ⊗ V^{G₁}.

In particular H²(G₁;V)=0 when V has no invariant vectors. This is a stronger finite-cover obstruction than L²-vanishing, but no theorem identifying all hyperbolic special groups satisfying it has been established here. Extending this statement from finite-image representations to arbitrary coefficients would be an unsupported step.

## 2. Quasiconvex homology amplification

**Lemma.** Let G be torsion-free, hyperbolic, and compact special. If A≤G is infinite-index quasiconvex and b₂(A)>0, then vb₂(G)=∞.

**Proof.** Arzhantseva's Theorem 1 provides g such that B=⟨A,g⟩≅A*Z is quasiconvex. For n≥1, let B_n be the kernel of B→Z/n which kills A and sends g to 1. Bass–Serre theory, or the n-sheeted cover of a wedge K(A,1)∨S¹, gives

    B_n ≅ A * gAg⁻¹ * ... * g^{n−1}Ag^{1−n} * Z.

In degrees at least two, free-product rational homology is the direct sum of factor homologies. Therefore b₂(B_n)=n b₂(A). The quasiconvex group B is a virtual retract of G by Haglund–Wise's canonical completion/retraction construction. If r:U→B is such a retraction, then U_n=r⁻¹(B_n) has finite index in U and r|_{U_n}:U_n→B_n is a retraction. Inclusion injects H₂(B_n;Q) into H₂(U_n;Q). Thus b₂(U_n)≥n b₂(A), proving the lemma. ∎

The same reasoning works if some finite-index subgroup A'≤A has positive b₂: A' remains infinite-index quasiconvex in G. It also works for virtually compact-special G after intersecting with a compact-special finite-index subgroup; positive rational b₂ survives that intersection by transfer.

**Necessary consequence of the problem hypothesis:** every infinite-index quasiconvex subgroup A has vb₂(A)=0. In particular an infinite-index quasiconvex closed orientable surface subgroup contradicts boundedness. This supplies a conditional proof of the target for any class where every non-virtually-free/non-virtually-surface group has such a subgroup.

**Exact gap:** one-endedness or nonfreeness does not, from the arguments above, produce a positive virtual second-homology class in a quasiconvex subgroup. Treating that missing implication as a lemma would transfer the central difficulty. The familiar surface-subgroup existence question cannot be silently assumed. Fruchter–Morales prove the target for hyperbolic graphs of free groups with cyclic edge groups and for residually free groups, but those are restricted classes; see their [Theorem A / Theorem 3.5](https://arxiv.org/html/2209.14925v3).

## 3. What L² approximation really supplies

Take an infinite torsion-free compact-special finite-index subgroup G₀ and a nested normal residual chain N_i with intersection 1. Its indices tend to infinity. Lück's approximation theorem gives

    b₂⁽²⁾(G₀) = lim_i b₂(N_i)/[G₀:N_i] = 0.

This is a necessary consequence, not an equivalent reformulation. The surface*circle example in §5 has b₂⁽²⁾=0 and vb₂=∞.

If cd_Q(G₀)≤2, Kielak–Linton Theorem 1.1 now yields that G₀ is virtually free-by-cyclic. In their usage the free kernel **need not be finitely generated**; their introduction states this explicitly. Their equivalent embedding in a finitely-generated-free-by-cyclic group also does not imply that the embedded subgroup has a finite-rank free kernel. Closed hyperbolic surface groups are a decisive control: they satisfy the theorem, but the kernel of an epimorphism to Z is an infinitely generated free group.

The 2026 [Fisher–Sánchez-Peralta preprint](https://arxiv.org/html/2603.16763v1), Corollary 1.6, additionally identifies second L²-vanishing with coherence in rational dimension at most two. It does not replace free-by-cyclic by free/surface. Its discussion explicitly preserves the infinitely generated kernel convention.

For dimension ≥3, b₂⁽²⁾=0 is not a top-dimensional statement. No cohomological-dimension bound follows from this one vanishing condition. Theorems requiring all higher L²-Betti numbers to vanish cannot be invoked using only b₂⁽²⁾=0.

## 4. Euler characteristic eliminates finite-rank fibers in the surviving dimension-two case

A non-elementary hyperbolic virtually compact-special group is large: choose a quasiconvex nonabelian free subgroup and use a virtual retraction onto it. Pulling back finite-index free subgroups produces arbitrarily large b₁ in finite-index subgroups. This argument uses no assertion that arbitrary finitely generated subgroups are quasiconvex.

Suppose cd_Q(G₀)≤2. Ordinary rational Euler characteristic gives, for every H≤G₀ of finite index d,

    b₂(H) = b₁(H) − 1 + d χ(G₀).

If χ(G₀)≥0, unbounded virtual b₁ forces unbounded b₂. Therefore every non-elementary candidate satisfying the problem hypothesis must have χ(G₀)<0. Since b₂⁽²⁾=0, L² Euler characteristic then gives

    b₁⁽²⁾(G₀)=−χ(G₀)>0.

This is compatible with surfaces and free groups. It also explains why Fisher's FP₂ virtual-fibering theorem cannot finish the surviving case: the theorem requires vanishing through degrees 0,1,2, while degree 1 is positive here.

If a finite-index subgroup were F_r⋊Z with r finite, then χ=0. Thus no non-elementary group with such a finite-rank fiber can satisfy bounded vb₂. This excludes finite-rank atoroidal free-group mapping tori, but not general infinite-rank free-by-cyclic groups supplied by Kielak–Linton.

## 5. Alexander and cyclic-cover constraints, with countercontrols

Let X be a finite K(G₀,1), let χ:G₀→Z be an epimorphism, let K=kerχ, and let Λ=Q[t,t⁻¹]. Set A_i=H_i(K;Q)=H_i(X^χ;Q). Each A_i is a finitely generated Λ-module. Write A_i≅Λ^{r_i}⊕T_i, with T_i torsion and therefore finite-dimensional over Q.

For the cyclic cover G_n=χ⁻¹(nZ), the short exact universal-coefficient sequence over the PID Λ is

    0 → A₂/(tⁿ−1)A₂ → H₂(G_n;Q)
      → ker(tⁿ−1:A₁→A₁) → 0.

Taking dimensions yields the exact formula

    b₂(G_n) = n r₂ + dim_Q(T₂/(tⁿ−1)T₂)
                    + dim_Q ker(tⁿ−1:T₁→T₁).

The last two terms are uniformly bounded, so bounded b₂ along this particular cyclic tower is equivalent to r₂=0. Under the actual problem hypothesis this condition must hold for **every character of every finite-index subgroup**. After the stabilization in §1, the exact constant b₂(G_n)=C additionally excludes all cyclotomic factors Φ_m(t), m>1, from T₁ and T₂; powers of t−1 and noncyclotomic torsion are not excluded by this calculation.

### Countercontrol A: L²-vanishing allows cyclic linear growth

Let S_g be a closed orientable surface of genus g≥2 and G=π₁(S_g)*⟨u⟩. This is hyperbolic and virtually compact special. Let χ kill the surface factor and send u to 1. The infinite cyclic cover of S_g∨S¹ is a line with one copy of S_g at each integer. Consequently

    A₂≅Λ,   A₁≅Λ^{2g},   b₂(G_n)=n.

Nevertheless b₂⁽²⁾(G)=0. One elementary check uses the aspherical presentation with single relator R=∏[a_i,b_i]: a Fox derivative coordinate of d₂ is 1−a₁b₁a₁⁻¹. Translation by the infinite-order element a₁b₁a₁⁻¹ has no nonzero invariant vector in ℓ²(G), so this coordinate operator, and hence d₂, is injective. There are no higher cells. This example stays within the hyperbolic virtually compact-special class and refutes the proposed shortcut b₂⁽²⁾=0⇒r₂=0. It is not a counterexample to Kourovka 21.139, because it fails boundedness.

### Countercontrol B: a bounded cyclic tower allows unbounded virtual b₂

For any finite-rank free-by-cyclic group G=F_r⋊_φ Z, Wang/Lyndon–Hochschild–Serre gives

    b₂(F_r⋊_{φⁿ} Z)=dim ker(φ_*ⁿ−I:H₁(F_r;Q)→H₁(F_r;Q))≤r.

For a non-elementary hyperbolic example, virtual compact specialness implies largeness, while χ(G)=0 gives b₂(H)=b₁(H)−1 in every finite-index subgroup. Hence vb₂(G)=∞ despite the displayed uniform bound along its standard cyclic tower. No numerical experiment on that tower can certify the actual hypothesis.

Likewise, for a closed orientable surface bundle M→S¹ with fiber S_g, every cyclic cover has b₂≤2g+1, from the Wang sequence. A closed hyperbolic such M has virtually compact-special fundamental group, is large, and satisfies b₂=b₁ by Poincaré duality, so vb₂=∞. Lück's [mapping-torus theorem](https://www.math.uni-bonn.de/people/lueck/data/ball.pdf) gives vanishing L²-Betti numbers. This is a dimension-three control against deriving cd≤2 from b₂⁽²⁾=0.

## 6. Approach status and exact remaining work

| Mechanism | Verified consequence | Status / exact gap |
|---|---|---|
| Rational transfer | vb₂ invariant under finite-index passage; eventual exact stabilization | Verified |
| Finite-image coefficients | H²(G₁;V)=H²(G₁;Q)⊗V^{G₁} below a maximal cover | Verified; no classification theorem supplied |
| Quasiconvex retraction amplification | Infinite-index quasiconvex positive virtual H₂ forces vb₂=∞ | Verified; positivity for arbitrary nonfree quasiconvex groups missing |
| Lück approximation | b₂⁽²⁾=0 | Verified necessary condition; converse false in the target class |
| RFRS / Kielak–Linton | Under cd_Q≤2, virtually free-by-cyclic and coherent | Verified restricted reduction; free kernel may be infinite rank |
| Euler characteristic / largeness | In non-elementary cd≤2 case, χ<0 and b₁⁽²⁾>0 | Verified; finite-rank fiber excluded |
| Alexander modules | r₂(χ)=0 for every virtual character; stronger torsion restrictions after stabilization | Verified necessary conditions; no sufficiency/classification argument |
| High-dimensional dimension drop | Would require more than degree-two L² vanishing | Blocked as a proposed shortcut |
| Surface/one-ended positivity substitution | Would close amplification route if established in needed generality | Blocked pending a materially new positivity mechanism |

Strongest verified conclusion: every hypothetical non-elementary counterexample has no infinite-index quasiconvex subgroup of positive virtual second Betti number. If its virtual rational cohomological dimension is at most two, it is coherent and virtually free-by-cyclic with negative Euler characteristic and positive first L²-Betti number; any relevant free kernel is necessarily infinite rank.

No counterexample satisfying all hypothesis gates was found. No full proof was found. The precise unresolved task is to derive free/surface structure from these much stronger all-cover conditions, or to construct a group satisfying them outside those virtual classes. None of the existing reductions replaces that task.
