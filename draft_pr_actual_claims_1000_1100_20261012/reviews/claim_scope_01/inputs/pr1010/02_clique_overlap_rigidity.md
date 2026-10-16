# Attempt 2: finite-centralizer overlap rigidity

## Target and outcome

This is a sufficient criterion for finite Out(W), and hence for the requested infinite Coxeter quotient of a finite-index subgroup of Aut(W). It is not a universal criterion. No novelty claim is made.

Use the finite-edge graph convention and let Δ₁,…,Δₖ be all maximal complete subgraphs. Let C(W) be the finite-index clique-conjugating subgroup from Mihalik–Tschantz, Theorem 28.

## Proposition: a finite-centralizer spanning tree suffices

Suppose there is a tree T on the maximal cliques such that, for every edge {i,j} of T,

C_W(W_{Δᵢ∩Δⱼ}) is finite.

Then

[C(W):Inn(W)] ≤ ∏_{{i,j}∈E(T)} |C_W(W_{Δᵢ∩Δⱼ})|.

In particular, Out(W) is finite. If W is infinite, Aut(W) virtually surjects onto an infinite irreducible special factor of W.

Proof. Root T at Δ₁. Given f∈C(W), compose on the left by an inner automorphism so that the normalized automorphism f₀ restricts to the identity on W_{Δ₁}. Choose its conjugator w₁ to be 1. For each other clique choose wᵢ with f₀(x)=wᵢxwᵢ⁻¹ on W_{Δᵢ}.

If i is the parent of j, equality of these two expressions on W_{Δᵢ∩Δⱼ} gives

wⱼ⁻¹wᵢ ∈ C_W(W_{Δᵢ∩Δⱼ}).

Thus, once wᵢ is chosen, wⱼ belongs to the finite set wᵢ C_W(W_{Δᵢ∩Δⱼ}). Starting from w₁=1 and following T leaves at most the displayed product of possible conjugator tuples. Each tuple determines at most one automorphism because the maximal cliques cover the generating set. Consequently every coset modulo Inn(W) has a representative in a set with at most that many elements. This proves the bound.

The finite index of C(W) gives finiteness of Out(W). Finally choose an infinite irreducible standard factor W₀ of W. Its center is trivial, so Inn(W)≅W/Z(W) surjects onto W₀; Inn(W) has finite index in Aut(W). ∎

The proof allows finite centralizers rather than only trivial ones, and only needs selected pairwise overlaps connecting all maximal cliques. It does not require that every multiple intersection have trivial centralizer.

## Checkable boundary example

Let W=⟨a,b,c | a²=b²=c²=(ab)³=(bc)³=1⟩. Its finite-edge graph is the path a—b—c with both labels 3. Here

W≅S₃ *_{⟨b⟩} S₃.

The intersection of its two maximal complete subgroups is ⟨b⟩, and C_W(b)=⟨b⟩ has order 2. To see this, use the Bass–Serre tree of the displayed amalgam. In either S₃ factor, the normalizer of the transposition subgroup ⟨b⟩ is that subgroup itself. Therefore b fixes exactly the base edge: at each endpoint there is no other b-fixed adjacent edge, and any further fixed edge would force a connecting fixed path. An element centralizing b preserves this fixed edge and is therefore in its stabilizer ⟨b⟩.

The proposition gives [C(W):Inn(W)]≤2. The group W is infinite because it contains the special subgroup ⟨a,c⟩≅D∞. It therefore satisfies the original quotient conclusion. This example also shows why replacing “finite centralizer” by “trivial centralizer” loses valid cases.

## Exact gap

Nothing here proves that the finite-centralizer overlap graph is connected for every Coxeter diagram with infinite Out, or that a surviving infinite centralizer supplies a quotient of the whole finite-index automorphism group. If the available overlap centralizers are infinite, the tuple-counting argument has infinitely many possibilities and produces no index bound. The invariant missing step would be a separate structural theorem controlling those centralizers and their induced automorphisms.

## Sources

- M. Mihalik and S. Tschantz, Visual decompositions of Coxeter groups, Theorem 28. https://doi.org/10.4171/GGD/53 ; author preprint https://arxiv.org/abs/math/0703439
- O. Varghese, Coxeter quotients of the automorphism group of a Coxeter group, Algebraic & Geometric Topology 26 (2026), 2353–2362, Theorems 2.7–2.8 and Lemma 1.3. https://doi.org/10.2140/agt.2026.26.2353
