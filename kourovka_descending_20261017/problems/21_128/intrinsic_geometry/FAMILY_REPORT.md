# Intrinsic geometry family — Kourovka21.128

Checkpoint 2026-10-24. Completion estimate toward an actual resolution: **10%**.
Outcome: **unsolved**. The arguments below give genuine finite-index invariants,
forward centralizer calculations and exact structural data. They do not decide
whether A[F4] and A[H4] are abstractly commensurable. Publication gate is closed.
No originality claim is made for any bounded lemma in this family.

## Accepted mechanisms and bounded results

1. **A rational cyclic commutation graph and centralizer spectrum.**
   INTRINSIC_GRAPH.md proves that the graph of internal commensurability classes
   of infinite cyclic subgroups, with edges witnessed by commuting powers
   generating Z^2, is carried isomorphically through every finite-index inclusion.
   Decorate a vertex by the abstract commensurability class of its stable
   centralizer and its virtual-center quotient; these decorations also survive
   every finite-index isomorphism. This is a real invariant, not an assumption
   that Artin parabolics are characteristic. All spherical pure central quotients
   Q_T are biorderable, so in our case every power has the same centralizer and
   every subgroup's virtual center equals its ordinary center. The underlying
   invariant does not require biorderability.

2. **Exact maximal-parabolic centralizers.**
   For T=F4,H4, S its standard four generators, and a maximal irreducible
   X subset S, the embedded pure parabolic satisfies

       C_{Q_T}(bar(Delta_X^2)^m)=P_X,  m != 0.

   centralizer_recognition/RESULTS.md proves all quotient and purity details.
   The full normalizer is A_X x Z(A_T): positivity and the actual spherical
   ribbon factorization force every maximal-parabolic ribbon to remain in this
   product. The global Coxeter longest element is -Id, which cannot belong to
   proper W_X; hence the pure intersection is P_X x <Delta_S^2>. A commutator
   introduced by quotienting cannot be a nonzero central power, because length
   kills commutators and is nonzero on Delta_S. Finite-index intersections remain
   power-stable centralizers with cyclic virtual center and are self-double-
   centralizing. None of these forward facts characterizes all centralizers.

3. **Complete exact arrangement census.**
   arrangement_incidence.py works in Q(phi), phi^2=phi+1, using normalized
   exterior-power coordinates. The explicit simple reflection bases have the
   F4/H4 Coxeter Gram matrices, preserve the complete 24/60-mirror lists, and
   generate those lists from the simple mirrors. verify_incidence.py uses
   Q(sqrt5), Gaussian elimination, reflection closure, complete pair coverage,
   and exact independent-triple counting. It imports neither producer.

   | Type | Rank-two multiplicities: count | Rank-three localization types: count |
   | --- | --- | --- |
   | F4 | 2:72, 3:32, 4:18 | B3:24, A2 x A1:96 |
   | H4 | 2:450, 3:200, 5:72 | H3:60, A3:300, A2 x A1:600, I2(5) x A1:360 |

   There are 122/722 rank-two flats and 120/1320 rank-three flats. The rank-three
   certificate covers all 1,920/33,300 independent triples exactly. Independent
   verification PASS is preserved in independent_verification.json; a fresh
   adversary reproduced it separately. Rank-three type names agree with the
   elementary Coxeter parabolic classification; the exact certificate itself
   records mirror multiplicity/incidence profiles.

4. **Restricted arrangements expose an omitted centralizer profile.**
   A selected mirror restriction has 13 planes in F4 and 31 in H4. Their full
   rank-two multiplicity profiles are respectively {2:12,3:4,4:9} and
   {2:60,3:40,5:6,6:15}. Projective Betti profiles are (1,12,35) and (1,30,209),
   giving Euler characteristics 24 and 180. The F4 other mirror orbit has the
   same restriction type by Amend--Hoge--Roehrle Lemma3.3(iii); that orbit equality
   comes from the primary theorem, rather than the one-selected-mirror
   computation. No statement that ordinary Betti/Euler values are absolute
   commensurability invariants is made.

   Davis--Huang describes chosen Hopf-center centralizers through normal and
   restricted arrangements. Rank-one centers therefore supply the restricted
   arrangement profile, besides the B3 maximal-parabolic profile. A purported
   exhaustive F4 centralizer list containing only B3 is unjustified even before
   considering arbitrary nonparabolic elements.

5. **A genuine resonance obstruction to the known product profile.**
   RESONANCE_PRODUCT_OBSTRUCTION.md proves that each projective restriction
   group G13,G31 is not commensurable with F_r x F_s, r,s>=2. Each has three local
   isotropic subspaces of H1, dimension at least two, with pairwise nonzero cross
   cups. A hypothetical finite-index product has resonance equal to the union
   of its two free-factor subspaces. Injective rational restriction in H1 and H2
   forces each of the three subspaces into one factor and every pair into
   different factors, a contradiction. Exact zero/nonzero integer cup witnesses
   are in resonance_certificate.json. The classifying-map H1/H2 argument
   explicitly connects arrangement-space cups with group cups without assuming
   unproved asphericity. The claim does not extend to all conceivable product
   factors, and does not compare either restriction group with the H3 group.

## Failed or blocked routes, with their exact obstructions

* **Raw parabolic recognition.** Even in the A3 pure central quotient an
  automorphism induced by swapping the capped puncture with an interior puncture
  exchanges centers of different raw disk-parabolic ranks. The two centralizers
  are abstractly isomorphic. This falsifies a universal rank-preservation lemma;
  it is not an F4/H4 counterexample. See centralizer_recognition/RESULTS.md §4.
* **Calling the bordification nerve algebraic.** Davis--Huang Def1.11 selects
  parabolics through normal-arrangement disk inclusions, then Def1.14 selects
  their Hopf centers. Prop5.11 and Thm5.12 identify this already selected family
  with a chosen boundary nerve and describe its stabilizers. They provide no
  theorem that an arbitrary isomorphism of finite-index subgroups preserves
  the selected family. Exact primary locators are in DAVIS_HUANG_SCOPE_AUDIT.md.
* **Recovering Coxeter labels from local free ranks or resonance dimensions.**
  A dihedral pure Artin group with m mirrors is Z x F_(m-1), m>=3. For any m,m'
  these are commensurable: choose d=lcm(m-2,m'-2), then the free factors have
  finite-index subgroups of common rank d+1. In particular m4 and m5 have a
  common Z x F7 subgroup, with free-factor indices 3 and 2. Their degree-one
  resonance dimensions 3 and 4 therefore are not finite-index invariants.
  The obstruction in item5 uses the shape of a hypothetical product cover,
  not invariance of ordinary resonance.
* **Rank-two boundary profiles.** The exact restriction-line counts at
  irreducible rank-two flats are F4: (m,k)=(3,6),(4,4), and H4:(3,12),(5,10).
  Davis--Huang's product description, modulo the global Hopf circle, gives
  groups virtually Z x F_(m-1) x F_(k-1). All have two nonabelian free factors,
  and all are abstractly commensurable. Thus these chosen local product pieces
  cannot distinguish the two ambient groups by their individual classes.
* **Unknown arbitrary centralizers.** The stable-centralizer invariant is now
  defined correctly, but its complete spectrum in Q_F4 has not been computed.
  Having a large centralizer has not been proved to force one of the designated
  boundary types. Double-centralizer closure by itself is weak: every
  centralizer is closed under the double-centralizer operation.

## Remaining mathematical target

Q_H4 has a stable centralizer isomorphic to P_H3. The established spherical
classification separates P_H3 from P_B3 and P_A3. To turn the present mechanism
into a negative solution, one must exclude **every** stable centralizer in Q_F4
that could be commensurable with P_H3. That needs an exhaustive intrinsic
classification, and also a comparison with the rank-one 13-plane restriction
profile. Neither is proved. Rephrasing those missing statements as hypotheses
would merely transfer the central difficulty. No affirmative finite-index
isomorphism was constructed either.

## Reproduction and review

Run the producer scripts with explicit --output paths if regenerating data.
The committed certificates can be checked directly with

    python3 verify_incidence.py --output /absolute/path/to/check.json

The local script uses only the Python standard library. The independent
adversary's separate output, exterior-basis cup checker, boundary-profile
checker, source audit and verdict are in fresh_intrinsic_audit/. Consult its
final AUDIT.md and frozen input manifest for the reviewed scope. No human peer
review or formal proof-assistant verification is claimed.
