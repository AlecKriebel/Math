# Coset geometry and virtual-centralizer route

Checkpoint 2026-10-17T20:52:00.408489+00:00. Research completion estimate for either original QI question: **15%**. These are restricted route obstructions, not a solution or a claim of novel priority.

## Exact target

A full answer requires a map between F and the entire product F x Z or F x F satisfying uniform upper and lower quasi-isometry estimates AND coarse surjectivity, or a genuine quasi-isometry invariant separating them. An abstract product embedding, noncommensurability, or failure of a chosen parametrization is insufficient.

## Standard input and notation

Let F be the usual finite dyadic piecewise-linear group, and H=Stab_F(1/2), isomorphic to F x F by restriction and affine rescaling on the two halves. Let H-prime=F-prime_left x F-prime_right. The classical facts used below are that F-prime is infinite simple and consists of elements identity near both endpoints of its interval. They are recorded in Cannon–Floyd–Parry, *Introductory notes on Richard Thompson’s groups*, Enseign.Math.42(1996),215–256, Section4. These external facts are not new claims here. A full fresh download of that article was not obtained in this pass; the publisher’s browser endpoint requested verification, so it was not bypassed. The known facts can also be checked in current primary Thompson-group literature.

## Lemma1: the virtual centralizer of H in F is trivial

First C_F(H-prime) is trivial. Suppose a in F moves x in one of the two open half intervals. Choose a dyadic interval [c,d] compactly contained in that half, containing x in its interior, and disjoint from a(x). An affine rescaling of the standard generator x0 on [c,d], extended by identity, belongs to the corresponding local F-prime and moves every interior point. Its support is exactly (c,d). If a centralizes it, a must preserve its support, forcing a(x) in (c,d), a contradiction. Thus a fixes both open halves pointwise, and continuity also fixes the midpoint; a=1.

The rescaled bump uses finite dyadic pieces: x0(t)=t/2 for0<=t<=1/2, x0(t)=t-1/4 for1/2<=t<=3/4, and x0(t)=2t-1 for3/4<=t<=1. Unlike the Dlab bump, it uses no breakpoint involving division by3. Dyadic c,d keep all its rescaled breakpoints dyadic.

If a has a finite conjugacy orbit under H, C_H(a) has finite index. The action of H on these finitely many cosets kills H-prime: each infinite simple factor has no nontrivial homomorphism to a finite group. Hence H-prime lies in C_H(a), and the previous paragraph gives a=1. Therefore every nonidentity a has an unbounded H-conjugacy orbit in any word metric of F, because finite word balls are finite.

## Proposition2: neither elementary coset-product convention is a QI

Let P be a metric space, s:P->F a set-theoretic section, and give H x P its product metric with any finite-generator word metric on H.

(a) If Psi(h,p)=s(p)h satisfies an upper quasi-isometry estimate with global constants L,C, then s is constant. For fixed p,q, put a=s(p)^-1s(q). The two domain points (h,p),(h,q) have distance d_P(p,q), but their image distance is |h^-1 a h|_F. Thus its H-conjugacy orbit lies in the finite ball of radius L d_P(p,q)+C. Lemma1 gives a=1. This holds for every p,q. In particular the usual left-coset-representative bijection from H times its infinite coset set cannot satisfy the needed upper estimate.

(b) If Psi(h,p)=h s(p) satisfies a global upper estimate, then s(P) is finite. For each generator b in a fixed finite generating set of H, compare (1,p) and (b,p). Their image distance is |s(p)^-1 b s(p)|_F, uniformly bounded by L+C. A finite ball gives only finitely many possible tuples of these conjugates. Equal tuples for s1,s2 imply s2 s1^-1 centralizes H, whose centralizer is trivial by Lemma1. Hence each tuple comes from at most one s, so s(P) is finite. An injective section on an infinite coset set is therefore impossible under the estimate.

These are metric arguments, not an inference that noncommensurable groups cannot be quasi-isometric. They eliminate BOTH simplest ways of treating a coset decomposition as an untwisted product with an independent H-coordinate. They leave open maps that alter the H-coordinate depending on p.

## Other attempted routes and exact gaps

1. Algebraic rigidity alone: finite-index subgroups of F,F x Z,F x F have abelianization ranks2,3,4, so no pair is commensurable. A homomorphic QI would have finite kernel and finite-index image; torsion freeness makes it injective, hence impossible. This is a restricted algebraic obstruction, also independently found by the priority agent. Arbitrary QIs need not be homomorphisms or boundedly close to one.

2. Transporting a product action: a hypothetical QI would transport the product’s commuting translation actions to uniform quasi-actions on F. Concluding that they come from interval homeomorphisms or homomorphisms would require a new quasi-isometric-rigidity theorem. Assuming that conclusion transfers the central difficulty; the route is blocked without a new mechanism. The exact affine-germ centralizer argument from Dlab21.149 has no automatic analogue for arbitrary maps of the word-metric space F.

3. Standard dyadic block embedding: it is already quasi-isometrically embedded by classical work. It has unbounded distance from elements moving the midpoint far into one end. The separate constructive route is deriving an exact distance sequence, so an undistortion theorem alone cannot settle coarse surjectivity.

## Current outcome

Two universal restricted lemmas above are checked on paper and are ready for adversarial review. No full QI or separating invariant has been found. Promising remaining work requires genuinely variable coordinate compensation, a nontrivial coarse-product rigidity obstruction, or a property not already forced equal by mutual quasi-isometric embeddings. No publication gate is open.
