# Attempt 4: extracting the conjugator at an anchor subgroup

## Target and outcome

This tests a natural route from a centerless complete special subgroup to a quotient of Aut(W). The route fails: a conjugator map is generally a crossed homomorphism, not a homomorphism. The obstruction below does not refute the original Coxeter-quotient conjecture or the old centerless-clique theorem statement.

## Lemma: a centerless group has no nontrivial automorphism retraction of this form

Let W be any centerless group, and let A≤Aut(W) contain Inn(W). If a homomorphism r:A→Inn(W) restricts to the identity on Inn(W), then A=Inn(W).

Proof. Let f∈ker(r). For every w∈W, the commutator [f,ι_w] is in Inn(W), because Inn(W) is normal, and is in ker(r), because ker(r) is normal. Their intersection is trivial since r is the identity on Inn(W). Hence

ι_{f(w)}=fι_wf⁻¹=ι_w.

Since Z(W)=1, f(w)=w for every w, so f is the identity. Thus ker(r)=1. For any a∈A, the element r(a)⁻¹a lies in ker(r), giving a=r(a)∈Inn(W). ∎

Consequently, if W is centerless with infinite Out(W), a finite-index subgroup A of Aut(W) containing Inn(W) cannot retract onto Inn(W). A successful Coxeter quotient must use a different map; the target only asks for some infinite Coxeter group and does not require such a retraction.

## An explicit failure of the anchor conjugator map

Let

W=⟨a,c,b,d | a²=c²=b²=d²=(ac)³=1⟩
  ≅S₃*C₂*C₂,

and let P=⟨a,c⟩≅S₃. Then P is a centerless maximal complete special subgroup. The free-product normal form gives C_W(P)=Z(P)=1: an element commuting with all of the nontrivial free factor P must lie in P, and then in its center.

Let C(W) denote the clique-conjugating subgroup. For f∈C(W), there is consequently a unique c(f)∈W with

f(x)=c(f)x c(f)⁻¹ for all x∈P.

Composition is read right to left. Direct calculation yields

c(fg)=f(c(g)) c(f),

rather than c(f)c(g).

Choose the partial conjugation τ which fixes a,c,d and sends b to aba⁻¹. It is an automorphism, its inverse is itself, and it lies in C(W). Then

c(τ)=1,    c(ι_b)=b,    c(τι_b)=aba⁻¹≠b.

The inequality follows immediately from reduced free-product normal forms. Thus c is not a group homomorphism.

Equivalently, the anchor gives a semidirect-product decomposition

C(W)=Inn(W)⋊K,

where K fixes P pointwise, but the projection onto the first factor is not a homomorphism when K acts nontrivially on W. Centerlessness ensures uniqueness of the decomposition; it does not remove the action.

## Exact gap

The conjecture requires a genuine epimorphism from a finite-index automorphism subgroup. Unique conjugators, a complement to Inn(W), or a nonabelian cocycle do not supply one. For an infinite-Out group, the retraction lemma rules out a map that fixes all inner automorphisms and has the claimed target Inn(W). No alternative universal quotient was produced in this approach.

## Source-status context

The OWR report contains an earlier centerless-maximal-clique assertion. The current arXiv metadata flags an incomplete earlier Theorem A proof, and the published 2026 paper instead gives its corrected sufficient conditions. The calculation above is an independent audit of a tempting general construction; it is not asserted to identify every detail of the author's earlier proof gap.

- Olga Varghese, arXiv:2003.04111, version history and revision notice. https://arxiv.org/abs/2003.04111
- Olga Varghese, published paper. https://doi.org/10.2140/agt.2026.26.2353
- Original OWR report, pp. 890–891. https://ems.press/content/serial-article-files/46853
