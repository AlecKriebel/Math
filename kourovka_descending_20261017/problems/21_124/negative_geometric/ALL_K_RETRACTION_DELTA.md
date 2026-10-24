# Explicit finite holonomy detects a for every positive parameter

UTC: 2026-10-24T22:29:33Z. Proposed exact partial theorem; fresh independent review requested. No complete Kourovka solution or novelty claim.

## Theorem

For every integer k≥1, the cyclic subgroup <a> of

G_k=<a,b,c,t | tat^-1=a, tbt^-1=ba^k, tct^-1=caba^-1b^-1>

is a virtual retract. These groups are CAT(0) by Delage2602.08759v3 Theorem4.1. Thus the attempt to disprove virtual specialness by showing that this particular cyclic subgroup is not a virtual retract fails for the whole family, not merely for the previously found k=3,4 small-cover witnesses.

The cases k=1,2 already have explicit integral four-/two-sheet witnesses in FINITE_HOLONOMY_FILTER.md. Here is a uniform finite-holonomy construction for every k≥2.

## Explicit permutation module

Let V=R^(3k), with its standard orthonormal coordinate basis indexed by pairs (j,i), j∈Z/3 and i∈Z/k. A permutation acts on column vectors by permuting basis vectors. Define:

- P(j,i)=(j,i+1), rotating each of the three blocks;
- B(j,i)=(j+1,i), cycling the three blocks;
- C is the involution swapping (0,0) with(1,0), (1,1) with(2,0), and(2,1) with(0,1), and fixing all other coordinates.

The six listed positions are distinct for k≥2. P and B commute, P^k=I, and C^-1=C. Let E=(I+P+...+P^(k-1))/k be blockwise averaging. On the P-fixed subspace one has

E C T = T - (2I-B-B^-1)T/k.                             (1)

Indeed each block has k-2 unchanged entries and one entry arriving from each of the two other blocks.

Choose T to be the vector with constant value k on block0 and0 on the other two blocks. Put

A=(B^-1-I)T/k,  D=(C^-1-I)T,
R=D-(I-B)A.

These are integral vectors. A is P-fixed and has block values(-1,0,1), so A≠0. Equation(1) and

(I-B)(B^-1-I)=B+B^-1-2I

show ER=0. Hence there is an integral vector u with

(P-I)u=R.                                                (2)

For a completely explicit choice set u_(j,0)=0 and u_(j,i)=-sum_(h=1)^i R_(j,h) for1≤i<k. The zero sum of R in every block makes equation(2) hold also at i=0.

## Affine homomorphism and exact relations

In V⋊Q, where Q=<P,B,C> is a finite subgroup of S_(3k), define

rho(a)=(A,P), rho(b)=(u,B), rho(c)=(0,C), rho(t)=(T,I).

Since P fixes A,T, a commutes with t and rho(a)^k=(kA,I). Moreover

rho(t b t^-1)=(u+(I-B)T,B)
             =(u+kBA,B)=rho(b a^k).

Because P and B commute, the commutator rho([a,b]) is a translation, with vector

(I-B)A+(P-I)u=D.

Consequently

rho(t c t^-1)=((I-C)T,C)=(CD,C)=rho(c[a,b]).

Thus rho is a homomorphism. All translation coordinates are integral, so its image lies in Z^(3k)⋊Q. The element a has infinite order in this image because kA≠0.

## A literal virtual retraction, without assuming all cyclic subgroups retract

Let L≤G_k be the inverse image of V⋊<P> under rho. It has finite index, because Q is finite, and contains a. Define

ell(v)=-(1/k)sum_(i=0)^(k-1) v_(0,i).

This functional is P-invariant and ell(A)=1. Hence chi:L→(1/k)Z, given by chi(g)=ell(the translation vector of rho(g)), is a homomorphism and chi(a)=1. The subgroup L'=chi^-1(Z) has finite index in L and contains a. The formula g↦a^{chi(g)} is a retraction L'→<a>.

This constructs only the virtual retraction of <a>. It does not establish(VRC) for all cyclic subgroups, any RAAG embedding, or virtual specialness of G_k. It is compatible with G_k for k>2 failing to be RFRS itself: the finite part P of a is nontrivial, and the relevant finite-index subgroup containing a is not required to be normal in G_k. The frozen normal-cover obstruction and this positive virtual retraction deliberately occupy different quantifiers.

## Checkable artifacts and remaining mechanisms

check_uniform_retraction.py verifies all affine equations by exact integer arithmetic for k=2,...,40, plus the actual full lifted-relator cocycle on the3k-point permutation cover for k=3,5,7. The proof above handles every k≥2, independently of those finite tests.

The remaining negative search would need a different cyclic element, another finite-index-persistent invariant, or a different CAT(0) family. Merely insisting that a's finite holonomy vanish is now a disproved route for the target. No paper/publication is justified by this partial result alone.
