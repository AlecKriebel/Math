# Attempt 2: exact fusion on a procyclic p-subgroup

Date: 2026-10-03. Second substantive proof attempt for KOU-21.136.
No general resolution or novelty claim is made.

Let G be profinite with P(G), and let A = closure(<a>) be isomorphic to Z_p.
Put N = N_G(A), C = C_G(A), and let U be the image of the continuous conjugation
map N -> Aut(A) = Z_p^times. The subgroup N is closed, so U is compact and closed.

## 1. Fusion of generators is exactly a unit-group quotient

The set Gen(A) of topological generators is {a^v : v in Z_p^times}. If
g conjugates a^v to a^w, it conjugates their closed generated subgroups to one
another; both are A. Hence g belongs to N. Conversely, every unit in U comes
from such a conjugation. Under the parameterization v -> a^v, the equivalence
relation induced by G-conjugacy is therefore multiplication by U. In particular

  number of G-classes meeting Gen(A) = [Z_p^times : U].

This identity uses generators. It must not be applied without justification to
arbitrary elements of an arbitrary closed subgroup.

## 2. The induced automorphism image must be open

An infinite metrizable profinite group has cardinal at least c: recursively split
nonempty clopen neighborhoods into two disjoint nonempty clopen neighborhoods;
compactness supplies a point on each binary branch. If a compact group is infinite
and homogeneous, no point is isolated, so this construction never stops. Its
cardinality is at most c by metrizability and compactness.

The quotient Z_p^times/U is a metrizable profinite group. The displayed identity
and P(G) therefore force this quotient to be finite. Thus U is open in Z_p^times.
In particular U is infinite and contains 1+p^k Z_p for some k >= 1 (k >= 2 if
p = 2). This congruence group is torsion-free and isomorphic to additive Z_p.
Consequently U itself has c infinite-order elements.

## 3. Normalizers of infinite procyclic p-subgroups cannot be open

If N were open in G, Attempt 1 would give P(N), and then quotient inheritance
would give P(U). But U is abelian with c infinite-order elements, so P(U) is
false. Thus N_G(A) is not open. In particular no such A can be normal in G.

This argument does not require Wilson's finite-generation theorem. It proves a
useful necessary condition directly from compactness and fusion:

  Every infinite procyclic pro-p subgroup of a hypothetical counterexample has
  an infinite-index normalizer, but that normalizer acts on it through an open
  subgroup of Z_p^times.

The two conclusions are consistent: the normalizer is closed, not open, and the
few-classes property has not been proved to pass to it. Thus the apparently
tempting quotient N/C is not a quotient of G to which inheritance applies.

## Outcome and next direction

There is no counterexample with a normal infinite procyclic pro-p subgroup, or
even one with such a subgroup having open normalizer. The main problem is still
open. Attempt 3 asks whether the required open unit action is incompatible with
a normal abelian subgroup and a torsion quotient, without assuming that A itself
is normal in G.
