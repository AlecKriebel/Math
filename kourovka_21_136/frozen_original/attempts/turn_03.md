# Attempt 3: the soluble-by-torsion case

Date: 2026-10-03. Third substantive proof attempt for KOU-21.136.
This proves a restricted affirmative result, not the unrestricted conjecture.
No priority or novelty claim is made.

## 1. A self-contained p-element reduction inside one procyclic group

Suppose P(G) holds and b has infinite order. Its closed procyclic subgroup B is
the Cartesian product of its procyclic Sylow subgroups B_p. If infinitely many
B_p are nontrivial, choose, for each infinite subset S of those primes, the
element with a generator in coordinate p in S and identity in the other
coordinates. These elements have infinite order and pairwise different prime
supports in their supernatural orders. Conjugation preserves that support, so
they give c different G-classes, a contradiction. Thus B has only finitely many
nontrivial Sylow factors. Since b has infinite order, one of those factors is
Z_p. This obtains an infinite-order p-element inside B without invoking the
global finite-prime theorem of Wilson and Herfort.

## 2. Abelian kernel and torsion quotient

Proposition. Suppose P(G) holds, B is a closed normal abelian subgroup of G, and
G/B is torsion. Then G is torsion.

Proof. If B were not torsion, section 1 supplies A <= B with A isomorphic to Z_p.
Let N = N_G(A) and U = image(N -> Aut(A)). For each n in N, the coset nB has
finite order in G/B, so n^m belongs to B for some positive m depending on n.
Since B is abelian and A <= B, n^m centralizes A. Hence every element of U has
finite order.

The torsion subgroup of Z_p^times is finite. One direct proof uses the
finite-index torsion-free subgroup 1+pZ_p for odd p and 1+4Z_2 for p=2. Its
torsion-freeness follows from the usual binomial valuation calculation:
v_p((1+p^k t)^(p^r)-1) = k+v_p(t)+r, for t nonzero, k>=1 if p is odd and
k>=2 if p=2; powers prime to p preserve the initial valuation. The torsion
subgroup consequently injects into a finite quotient of Z_p^times. Thus U is
finite, contradicting Attempt 2, which requires U to be open and hence infinite.
It follows that B is torsion. Finally, for any g in G, some g^m is in B and has
finite order, so g has finite order. This proves the proposition.

There is no uniform bound on m in this proof, and none is needed. The result
does not tacitly assume that the torsion quotient has finite exponent.

## 3. Induction on a finite soluble normal series

Theorem (restricted case). Suppose P(G) holds and G has a closed normal subgroup
S of finite derived length such that G/S is torsion. Then G is torsion.

Proof by induction on the derived length d of S. For d=0 the assertion is the
hypothesis G/S torsion, since S=1. If d>0, let B be the last nontrivial term of
the closed derived series of S. It is closed, normal in G, and abelian. The
quotient G/B inherits P; its normal subgroup S/B has smaller derived length and
its quotient by S/B is G/S, which is torsion. Induction makes G/B torsion. The
proposition then makes G torsion.

In particular the conjecture holds for soluble profinite groups of finite
derived length and for virtually soluble profinite groups. For the latter take
the core of an open soluble subgroup; it is an open normal soluble subgroup,
and the quotient is finite. This is not an argument for all prosoluble groups:
an inverse limit of finite soluble groups need not have finite derived length.

## Outcome and limitation

The conjecture is established here for the stated soluble-by-torsion class.
Both the fusion calculation and the torsion action obstruction are explicit.
The unrestricted problem remains: the abelian-kernel induction needs a finite
normal series and does not control unbounded derived length or nonsoluble
profinite groups. Attempt 4 will test the natural affine fusion construction as
a potential counterexample and isolate why it fails globally.
