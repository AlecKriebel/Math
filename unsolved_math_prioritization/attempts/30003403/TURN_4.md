# Author turn 4: lifting quotients through finite prefixes

**Partial: explicit nonfragmented target classes are covered, but a general uncountable quotient remains missing.** 2026-10-01.

Write D=C*+{0}+C and L=eta_C. Products in this note always have their first coordinate primary. The point of this turn is to obtain actual uncountable quotients and then identify precisely why their recursion does not cover all targets.

## 1. The credited short-product lemma

For nonempty short orders U,V, there is a monotone epimorphism U×V -> V. This is a special case of Polymeris–Martinez-Ranero Lemma 3.4, taking U'=1 and V'=V, and follows from Camerlo–Carroy–Marcone Corollary 2.11 and the preceding definition-by-pieces proposition (their product convention is reversed). Their construction uses a coinitial/cofinal family of V-blocks and clipped target intervals, with separate endpoint cases.

This map is generally **not** the second-coordinate projection. If u<u' and v>v', then (u,v)<(u',v') but projection would reverse their images. We use the established epimorphism lemma, not that false formula. The shortness assumptions hold for every suborder of any finite power of D and for L.

## 2. A quotient-lifting lemma

Suppose that n>=1, q:D^n -> I is a monotone epimorphism, and each nonempty order A_i is a monotone image of L. Then

    L -> sum_(i in I) A_i                                           (1)

is a monotone epimorphism.

Proof. Finite-prefix removal gives an actual order isomorphism L = D^n×L. For each i put J_i=q^(-1){i}. These are nonempty convex short orders, and

    D^n×L = sum_(i in I) (J_i×L).

By Section 1 each J_i×L has an epimorphism h_i onto L. Compose h_i with a given epimorphism L -> A_i. The ordered ranges are disjoint summands of the requested target, so these maps glue without any endpoint interpolation: each domain fiber maps exactly onto its corresponding full target summand. This proves (1). The argument uses no forcing axiom beyond any needed to supply q and the individual maps.

This is the mechanism used in the source proof of Lemma 3.10; it is credited, and here made explicit as a conditional closure rule. It supplies quotient-compatible copies by the section criterion from turn 2, without requiring a retraction onto the original embedding of the target.

## 3. Genuine nonfragmented targets in the quotient class

For every Countryman C, D has monotone epimorphisms onto every nonempty finite order: choose the required finitely many ordered cut points and use consecutive nonempty fibers. Consequently the quotient class of L is closed under finite nonempty ordered sums. In particular L has epimorphisms onto

    L+L,  1+L,  L+1,  1+L+1,  and any nonempty finite sum of copies of L.

These are uncountable targets containing a copy of L, so they are nonfragmented. Under PFA they embed into L by Moore's universality; the preceding maps already exist in ZFC for arbitrary Countryman input. Thus the partial result reaches genuine nonfragmented suborder types, not only the previously settled fragmented class. It does not assert that these examples are new results.

Now impose the additional hypothesis that C is normal and assume MA_(aleph1). The source proof of Lemma 3.10 supplies epimorphisms D^2 -> C and D^2 -> C*. Normal C and C* are strongly surjective by Corollary 3.2; they contain Q because they are uncountable short orders (uncountable scattered orders are not short). Hence D^2 has an epimorphism onto every nonempty countable order K, by composition through Q and the countable quotient fact established in turn 3. It also has an epimorphism onto every nonempty suborder of C or C*.

Applying (1), for **normal input C under MA_(aleph1)**, the quotient class of L is closed under:

- All countable nonempty ordered sums of orders already in that class
- Sums indexed by any nonempty suborder of C or C*, again with every summand already a quotient of L

In particular L has quotients K×L for every nonempty countable K, and C×L and C*×L. These contain L and therefore are nonfragmented. With PFA added, they are suborder types of L. For normal C under PFA, the credited fragmented-target theorem can also supply summands in this closure rule. None of these extensions is asserted for arbitrary nonnormal input C without a separate proof of the required indexing quotient.

## 4. Why finite support does not finish the uncountable recursion

An arbitrary suborder A of L decomposes at the first coordinate as

    A = sum_(d in I) A_d,

where I is a suborder of D and each A_d embeds into L by removing that coordinate. To apply (1), one still needs an available quotient onto I and a quotient L -> A_d for every d. The assertion that the fibers embed into L is insufficient: obtaining their epimorphisms is the unresolved problem itself.

Finite support of each individual point does not give a well-founded induction on these suborders. For A=L, every first-coordinate fiber is again isomorphic to L, so this recursion never decreases its target order type. This is harmless for A=L because the identity is known, but it disproves the proposed general termination argument. A general nonfragmented target may likewise have no decreasing fragmented rank. The rank induction in the published fragmented theorem cannot be extended by simply giving an infinite rank to universal targets.

Nor can one apply the closure rule with I=L merely from the identity L -> L: the rule requires a quotient from a **finite prefix alphabet D^n**, not from L. Replacing that hypothesis by L -> I would require the unsupported absorption/quotient step from L to L×L. Interleaving two finite-support sequences is not an order isomorphism for the first-coordinate-primary lexicographic product: an early coordinate in the second sequence can precede the first difference of the first sequence after interleaving. The accompanying finite check exhibits this reversal explicitly.

## Remaining gap and audit of turn 3

The binary section in turn 3 stops at the first symbol outside its two nonzero branch symbols; eventual zero guarantees that such a symbol occurs. A zero at that first stop is either the tree node itself or lies adjacent to it in the section order. This argument concerns realized cuts, not all Dedekind cuts. The countable-target conclusion follows from the elementary dense-order identification K×Q = Q, valid even when K has endpoints or adjacent pairs. No transfinite conclusion is inferred from the finite diagnostics.

This turn obtains actual maps for finite sums of universal targets and, with normal input and the stated axiom, further countable and Countryman-indexed nonfragmented sums. The general uncountable PFA target remains unresolved: a coherent section or an intrinsic obstruction for arbitrary nonfragmented targets is still absent.

Substantive author turns: 4/5. Estimated completion: 30%. No full solution, no target counterexample, and no novelty claim.
