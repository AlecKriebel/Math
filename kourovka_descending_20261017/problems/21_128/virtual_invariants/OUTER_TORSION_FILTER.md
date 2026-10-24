# Virtual outer torsion is automatic; commensurator torsion is different

Checkpoint: 2026-10-24 UTC. All claims below concern the pure central quotients Q_F and Q_H. No solution of 21.128 or novelty claim is made.

## A. The known periodic-element test has a genuine missing step

[Soroko, Theorem 7 and Table 1](https://arxiv.org/abs/2009.10471v4) proves that the full central quotient A[F4]/Z(A[F4]) has nontrivial torsion orders 2,3,4,6, whereas A[H4]/Z(A[H4]) has orders 2,3,5,6,10,15. In particular the latter contains an element of order 15. These are full central quotients, not the torsion-free groups Q_T=P_T/Z(P_T).

By [Cumplido–Paris, Proposition 3.1](https://doi.org/10.4171/RMI/1282), full central quotients embed in their own abstract commensurators, and commensurability of the original Artin groups is equivalent to commensurability of these quotients. Since Q_T has finite index in the corresponding full central quotient, their abstract commensurators are isomorphic. Therefore a positive answer to 21.128 would force Comm(Q_F) to contain an element of order 15, hence one of order 5.

Proving that Comm(Q_F) has no order-five element would consequently prove a negative answer. The known order list for A[F4]/Z(A[F4]) does **not** prove that assertion: its ambient abstract commensurator may contain additional finite-order elements. No rigidity theorem identifying Comm(Q_F) with that full quotient, its automorphism group, or a known finite extension was established here. Treating such an identification as an assumption transfers the central difficulty and is a blocked route.

## B. In fact virtual Out torsion cannot supply that missing step

**Lemma.** Suppose G is torsion-free, center-free, has unique roots, and surjects onto Z. For every m≥1, G has a normal index-m subgroup V such that Out(V) contains an element of exact order m. The automorphism used to produce it represents an element of infinite order in Comm(G).

**Proof.** Let q:G→Z be the epimorphism, choose x with q(x)=1, and let V=q⁻¹(mZ). First C_G(V)=1. If y centralizes V, then for any g∈G some positive power g^k belongs to V. Thus (ygy⁻¹)^k=g^k. Unique roots imply ygy⁻¹=g, so y∈Z(G)=1.

Conjugation by x preserves V. Its m-th power is conjugation by x^m∈V, so its outer class has order dividing m. If its k-th power is inner by v∈V, then v⁻¹x^k centralizes V, hence is 1. Therefore x^k=v∈V, forcing m to divide k. The outer order is exactly m.

In Comm(G) this same automorphism is the restriction of conjugation by x on all of G. If its k-th power were the identity commensuration, x^k would centralize a finite-index subgroup. The preceding unique-root argument would give x^k∈Z(G)=1, contradicting q(x^k)=k for k>0. Thus its commensurator order is infinite. ∎

The hypotheses apply to Q_F and Q_H. Their centers are trivial; they are torsion-free and bi-orderable by the pure central quotient facts summarized in [Soroko, Proposition 3](https://arxiv.org/abs/2009.10471v4), using Marin's theorem. A bi-orderable group has unique roots: if a<b, multiplying inequalities on both sides repeatedly gives a^n<b^n for n>0. Finally FREE_RETRACT_FILTER.md gives Q_T→F2→Z.

For m=5 this proves that both targets have a finite-index subgroup with an outer automorphism of order five. It supplies no finite-order automorphism of that subgroup and no finite-order commensuration. For m>1, in the explicit coset of Aut(V) obtained by composing conjugation by x with an inner automorphism of V, none has finite order: such a composite is conjugation by vx for some v∈V, and a finite power being trivial on V would force a power of vx to be 1 in torsion-free G. But q(vx) lies in mZ+1, so vx≠1. This is an explicit obstruction to confusing a cyclic deck action in Out(V) with its realization by finite-order automorphisms. The restriction m>1 is necessary for this coset assertion: when m=1, V=G and choosing v=x⁻¹ makes conjugation by vx the identity. The chosen conjugation by x still has infinite order in Comm(G), and its outer class has order one, exactly as in the lemma.

## C. What would have to be proved about actual finite-order automorphisms

For clarity, a finite-order commensuration can be realized on a further finite-index subgroup as an actual finite-order automorphism. Here is the elementary cyclic case. Represent an order-k commensuration by f:U→V. There is a finite-index W on which all iterates through f^k are defined and f^k is the identity. The subgroup

H = ⋂_(i=0)^(k−1) f^i(W)

has finite index, lies in the domains needed, and f(H)=H because f^k(W)=W. Thus f restricts to an automorphism of H of order dividing k. Its order is exactly k, since a smaller order would lower the original commensurator order.

Conversely, an automorphism of a finite-index subgroup of a unique-root group that is the identity on another finite-index subgroup is itself the identity. Apply the root argument to each g using a power of g in that subgroup. Thus in this setting an actual order-k automorphism represents order k in Comm(G).

For Q_F, the missing order-five exclusion is therefore equivalent to excluding actual order-five automorphisms of **all** finite-index subgroups. The lemma in section B shows why merely computing finite-order classes in Out of such subgroups cannot do this. No such uniform exclusion or positive construction was proved.
