# Author turn 3: perfect bases and perfect central extensions

## 1. Two scoped theorems

Throughout this turn the action is the **regular** action, W=G^(H) semidirect H. We do not transfer the following coordinate argument to an arbitrary permutation action.

**Theorem A.** Let G be a finitely generated perfect Hopfian group and H a Hopfian group. Every basic self-epimorphism of G wr H is an automorphism, even when G has a nontrivial center.

**Theorem B.** Suppose in addition that G/Z(G) is a finite product of nonabelian simple groups. Then G wr H is Hopfian, without any assumption of basicity and without assuming Z(G) wr H is Hopfian.

In the source's finite-generation setting, the simple quotient factors are finitely generated because they are quotients of G. Theorem B includes quasisimple bases and perfect central products of quasisimple groups. It does not settle arbitrary Hopfian bases or the abelian stable-finiteness obstruction.

The invariant-central-base lemma used in Theorem B is credited to Bradford--Fournier-Facio Lemma5.7. The new proof below uses perfectness to constrain central coordinate mixing, rather than dropping the separate-center hypothesis from their more general Proposition5.8 without justification. No historical novelty claim is made.

## 2. Perfect groups have centerless central quotients

If G is perfect, then G/Z(G) is centerless. Indeed, if aZ(G) is central in that quotient, every [a,g] lies in Z(G). The map g-> [a,g] is then a homomorphism from G into the abelian group Z(G), by the central commutator identity. Perfectness makes it trivial, so a lies in Z(G).

We also use the elementary fact that if P is a subgroup with P Z(G)=G and G is perfect, then P=G:

    G=[G,G]=[P Z(G),P Z(G)]=[P,P]<=P.                            (1)

Neither statement needs finite generation or finiteness of the center.

## 3. Local maps for a basic epimorphism

Let Phi be basic and onto, and put B=G^(H). As in turn1, the induced map alpha on H is an automorphism, F=Phi|_B is onto B, and ker(Phi)<=B. Write Phi(1,h)=(b(h),alpha(h)). The same covariance formula holds:

    F(h.f)=b(h) (alpha(h).F(f)) b(h)^(-1).

Let psi_s(g)=F(i_1(g))(s), and K_s=psi_s(G). Only finitely many s have nontrivial K_s; call that set S. Finite generation of G proves this finite support exactly as in turn1. The normality and covariance arguments of that turn, which do not use centerlessness at this stage, show that the K_s are normal, pairwise commuting, and generate G.

Consequently

    Theta(g)=product_(s in S) psi_s(g)                           (2)

is a homomorphism. We must prove it is onto before invoking Hopficity. Individual coordinate surjectivity onto K_s alone would not suffice.

Because F is surjective, it sends the center of B into itself. That center is Z(G)^(H), so each psi_s sends Z(G) into Z(G). Passing to Q=G/Z(G) therefore gives an onto base map Q^(H)->Q^(H), with the same quotient automorphism and the induced cocycle. By Section2, Q is centerless. Apply the **surjectivity part** of turn1 Sections3--4 to this map: its commuting coordinate images form an internal direct product, and prescribing one output at each support coordinate proves that the induced product endomorphism bar(Theta):Q->Q is onto. This part of that argument uses centerlessness and base surjectivity, but does not use Hopficity of Q. No Hopficity of G/Z(G) is assumed here.

Thus Theta(G) Z(G)=G. Equation (1) gives Theta(G)=G. Since G is Hopfian, Theta is an automorphism.

## 4. Perfectness turns the commuting images into genuine direct factors

Define p_s=psi_s composed with Theta^(-1). Their images are K_s, they commute pairwise, and

    product_s p_s(g)=g for every g in G.                         (3)

We claim each p_s is a genuine projection onto K_s, killing the other K_t.

First p_s is equivariant under all inner automorphisms of G. Its homomorphism property gives

    p_s(g x g^(-1))=p_s(g)p_s(x)p_s(g)^(-1).

But g is the product of p_r(g), and all factors with r!=s commute with K_s. Hence the right side equals g p_s(x) g^(-1).

Fix t!=s and x in K_t. Every z in K_s commutes with x. Inner equivariance now implies z commutes with p_s(x). This element belongs to K_s, so it also commutes with every K_r for r!=s. The K_r generate G, and therefore p_s(x) lies in Z(G).

Each K_t is perfect, being a homomorphic image of perfect G. The homomorphism p_s|_(K_t):K_t->Z(G) must thus be trivial. Applying (3) to x in K_t then gives p_t(x)=x. Thus p_s kills K_t for s!=t and is the identity on K_s. In particular multiplication identifies G with the internal direct product of the K_s.

The kernel argument of turn1 now applies without change: at each output coordinate, a given K_s-factor receives input from a unique lamp coordinate h=alpha^(-1)(y s^(-1)). A kernel element therefore has psi_s(f(h))=1 for every s,h, and injectivity of Theta gives f=1. Since ker(Phi)<=B, Phi is an automorphism. This proves Theorem A.

The explicit inverse and finite-support bounds from turn1 Section5 also apply, with these p_s as the direct-factor projections. The center has not been discarded; perfectness forces all cross-factor homomorphisms into it to vanish.

## 5. The credited invariant-central-base lemma, with a proof

Let G be nonabelian and H Hopfian, and let Phi:W->W be onto. Put N=Phi(B). We first observe that N intersect B projects onto G at every coordinate.

If Phi is basic this follows from Phi(B)=B, already proved using Hopficity of H. If N is non-basic, choose (f,h) in N with h!=1. Commuting it with a lamp at coordinate1 produces an element of N intersect B whose coordinate1 ranges through all of G, because the regular action moves that coordinate to h. Conjugating by the acting group proves the same statement at every coordinate.

Now A=Phi(Z(G)^(H)) is an abelian normal subgroup of W. If A were non-basic, the same commutator argument would make A intersect B project onto nonabelian G, impossible because A is abelian. Hence A<=B. Moreover A commutes with N intersect B, whose coordinate projections are onto G. Every coordinate of A must therefore be central in G:

    Phi(Z(G)^(H)) <= Z(G)^(H).                                  (4)

This is precisely the source's Lemma5.7, with its hypotheses retained. We have recalled the argument to expose the regular-action and nonabelian requirements.

## 6. From a semisimple central quotient to the full theorem

Assume Q=G/Z(G) is a finite product of nonabelian simple groups. By turn2, Q wr H is Hopfian and every self-epimorphism of it is basic.

For any self-epimorphism Phi of W, (4) permits passage to

    bar(Phi): W/Z(G)^(H) = Q wr H --> Q wr H.

It is surjective, hence an automorphism, and it is basic. The preimage in W of the base Q^(H) is exactly G^(H). Therefore Phi sends G^(H) into itself. Theorem A now proves that Phi is injective. This establishes Theorem B.

No inference that arbitrary central extensions of Hopfian groups are Hopfian is made. Perfectness, the Hopficity of G and H, and the finite-simple-product central quotient all remain explicit. No finiteness hypothesis on Z(G), or ring-theoretic condition on Z(G)[H], has been inserted or silently removed.

## 7. An illustrative central product and the danger of independent shifts

A concrete finite example outside the centerless-base class is obtained from K=SL_2(F_5), with center {I,-I}. The exact finite checker verifies |K|=120, perfectness, its two-element center, and simplicity of K/{I,-I} by normal-closure enumeration. Set

    G=(K times K)/<( -I,-I)>.

This is a perfect finite group of order7200. Its center has order2 and its central quotient is the product of two copies of the nonabelian simple group K/{I,-I}. Hence G is Hopfian and Theorem B applies to G wr H for any finitely generated Hopfian H.

The shared center is a real compatibility constraint. Let c be the common image of (-I,I) and (I,-I), a nonidentity central element of G. In a putative factorwise coordinate map, shift the first K-factor to coordinate1 and the second K-factor to a different coordinate h. The source relation (-I,-I)=1 would be sent to c at coordinate1 and c at coordinate h. These do not cancel in a restricted direct product with distinct coordinates. Thus independent shifts of the two central factors need not define a homomorphism at all. This is a failure of that construction, not a non-Hopfian example.

More generally, two homomorphisms from a perfect group into a group K which agree modulo Z(K) must coincide: their pointwise ratio is a homomorphism to Z(K), hence trivial. This explains why central behavior cannot be prescribed independently after the noncentral quotient map has been fixed.

## 8. Third-turn status

Three genuine author turns are complete. The original remains unresolved. We have positive theorems for basic centerless or perfect bases, automatic basicity for finite products of nonabelian simple factors, and a full positive result for the stated perfect central extensions. General nonperfect centers and genuinely mixing epimorphisms outside these quotient classes remain. The fourth and fifth author turns are unconsumed at this checkpoint.
