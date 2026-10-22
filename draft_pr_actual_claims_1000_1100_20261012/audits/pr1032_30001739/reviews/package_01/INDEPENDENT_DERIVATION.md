# Independent derivation recorded before historical audit conclusions

2026-10-17 UTC. This derivation was made after reading the new manuscript and the primary FLO/LM/JPSS/OWR interfaces below, and before reading analytic_01, langlands_01, priority_01 reports or the submitted proof. Those reports will be compared afterwards. Source-credit locator/identity metadata was read to find primary bodies; it was not treated as proof. This is an AI adversarial review, not human peer review.

## Claim and assumptions

F=Q_3, E/F unramified quadratic, smooth admissible complex representations. D_K[a,b] is the essentially square-integrable quotient of the ascending character induction, not the Zelevinsky socle segment. Lengths of (T,D,C,B,A)=([4,6],[2,5],[3,3],[1,4],[0,2]) are (3,4,1,4,3), giving degree15; real centers (5,7/2,3,5/2,1) strictly descend. Thus the normalized standard module has one irreducible cosocle pi and one maximal proper submodule. Its factors and unique quotient are tau invariant. This proves neither distinction nor entire noninduction by itself.

## Scalar from the primary interfaces

FLO published pp200–202 defines gamma(s,X)=epsilon(s,X)L(1-s,X^vee)/L(s,X), N=C_M M, and gives meromorphic inverse/composition identities. Lemma1.1(3),(4) applies to unitary essentially square-integrable factors with the centers inserted in lambda. In a positive center chamber forward M and reverse N are holomorphic; for a linked pair, Im(reverse N)=Ker(forward M), a proper submodule. It does not say reverse M=forward N at the reducibility point.

FLO (4.5), pp224–225, normalizes J by a product of F-side gamma factors. Theorem12.4(4), (12.5), p283, permutes the normalized periods on the generic-compatible individual inducing factors; the Steinberg factors satisfy that condition. Canceling all unaffected gamma factors in the reverse equation leaves

c(u) = unit * gamma(-u, D_i'^vee x D_j' eta^(1+e_i+e_j))/gamma(u,D_i' x D_j'^vee eta^(1+e_i+e_j)).

This agrees with FLO (13.3), p293, including the reverse operator orientation. In particular equal labels correspond to eta; opposite labels correspond to the trivial character. JPSS Theorem8.2(5), pp444–445, with the longer segment first (or by symmetry), gives

L(u,D_F[a,b] x D_F[c,d]^vee chi)= product_{0<=j<min(lengths)} (1-chi(3)*3^(-u-b+c+j))^-1.

JPSS section2.9 pp395–396 makes epsilon an invertible Laurent monomial. Write P_j=b-c-j and Q_j=d-a-j, z=q^-u and zeta=chi(3). Expanding both gammas gives exactly the epsilon-free rational germ

prod_{h in Q}(1-zeta*q^-h/z)(1-zeta*q^(-1-h)/z) / prod_{h in P}(1-zeta*q^-h*z)(1-zeta*q^(-1-h)*z).

At z=1 its order for zeta=1 is count_Q(0,-1)-count_P(0,-1). For zeta=-1 every factor is nonzero. The needed rows independently recompute to

|pair|P|Q|trivial-label order|
|---|---|---|---|
|TD|4,3,2|1,0,-1|2|
|BA|4,3,2|1,0,-1|2|
|TC|3|-1|1|
|DB|4,3,2,1|2,1,0,-1|2|
|CA|3|-1|1|
|DC|2|1|0|
|CB|2|1|0|

For DC and CB the rational germ at zeta=+1 is q^2/(q^2+q+1), and at -1 is q^2/(q^2-q+1). At q=3 these are 9/13 and9/7; at q=9,81/91 and81/73. The F period coefficients are units in both parities. The E-side forward gamma normalizer for either nested swap has positive directional lists {2},{1} and is a unit. Together with chamber holomorphy of forward M, this gives holomorphic forward N; reverse N is already holomorphic. Meromorphic inverse identities therefore specialize to actual two-sided inverses. An unspecified nonzero normalization unit cannot invalidate zero orders or support preservation; these numerical values are not claimed to be the full period coefficient values.

## Complete period basis and odd-cycle exclusion

For each fixed Hermitian matrix x, not only after summing over orbits, FLO Corollary13.6 p291 gives the complete Hom(I_r,C) basis if no earlier segment satisfies a<=c<=b<=d with a later one. All30 pair tests hold for O1=TDCBA, O2=TCDBA, O3=TDBCA. The two changed pairs are strict containments, so FLO's condition remains satisfied although centers in O2/O3 are not descending. FLO (12.1), p283 gives independence of the lift forms on each fixed orbit; simultaneous eta twist changes by a nonzero fixed-orbit scalar via (3.13), p217. Five independent two-choice lifts modulo that simultaneous twist give 2^4=16 coordinates, represented by e_T=0. No quotient functional can escape this full basis.

Swapping DC from O1 to O2 and CB from O1 to O3 uses the two separately established isomorphisms. Their period coefficients are units for all16 labels, so transport is diagonal after segment relabelling and preserves support. These are two separate transports out of O1. There is no assumption that the shared-factor transports commute or that some common swapped order exists. Operators DC and CB do not commute as adjacent permutations; no step multiplies them in the opposite order.

For an exposed linked pair, exact and faithful smooth parabolic induction takes its proper rank-one kernel to a proper full-module submodule K. A standard module with a simple cosocle has one maximal proper submodule, and isomorphism transfers this fact to I2/I3. Therefore K is contained in ker(p_r); no kernel-generation equality is needed. Exactness follows from the compact induction model: at fixed open compact level the relevant double-coset set is finite, and averaging over compact stabilizers over C makes invariants exact; a nonzero inducing vector gives a nonzero local section. This remains valid when the other factors' product is reducible.

Write the pullback of an arbitrary quotient functional in its16 coordinates. It annihilates Im(reverse N). FLO's meromorphic functional equation is specialized after restricting the reverse domain to open-orbit sections. These restricted J's are entire by compact support and (6.6), p242. Their independence at zero follows from (12.1) and that isomorphism; it does not require the full swapped periods to be holomorphic or complete. This yields a_e*c_e(0)=0 separately. Since c_e is a unit for equal labels, each surviving coordinate must have opposite labels across the exposed pair. O1 exposes TD and BA; O2 exposes TC and DB; O3 exposes CA. Support-preserving transport imposes all five constraints on the same segment labels. They form T-D-B-A-C-T; summing over F2 gives0=1. The independent checker lists all16 coordinates and at least one failed edge per coordinate. Removing any one of the five constraints permits exactly one coordinate with e_T=0, which verifies that none is computationally redundant.

Since p1 is surjective, every quotient functional is zero. x was arbitrary; this applies to both Hermitian isometry classes, even though in odd degree their groups can be isomorphic. Finite scalar and coloring calculations corroborate this deduction but do not compute any Hom space or prove FLO.

## Entire noninduction

If a whole normalized parabolic induction were isomorphic to irreducible pi, exactness and preservation of nonzero objects force its inducing data to be irreducible: otherwise a nonzero subobject and quotient would survive. Grouping more than two positive-degree blocks similarly gives a two-factor irreducible entire product. Any factors have unique Langlands multisegments m,n. LM Theorem2.6 and the analogue of Proposition2.5(5), pp10–11, put L(m+n) into L(m)xL(n) with multiplicity1. Irreducibility forces equality to pi; classification injectivity forces m+n=A+B+C+D+T. Equality of cuspidal supports alone would be insufficient. All unordered nontrivial occurrence partitions are therefore the five1/4 partitions and ten2/3 partitions.

The LM precedence relation is a<c<=b+1 and b<d. Left shift means both endpoints of the first segment minus1. LM section5.3 pp35–36 defines X=(u_i prec v_j), Y=(leftshift(u_i) prec v_j), and a Y neighbor (i2,j2) of X(i1,j1) precisely when (i1=i2 and v_j2 prec v_j1) or (j1=j2 and u_i1 prec u_i2). The arrows go in different apparent directions because one varies the second segment and the other the first. The source's ladder Definition5.13 p34 requires strict corresponding endpoint order, not consecutive linkage. Only BC,CD fail the pair ladder test; their complements ADT,ABT are ladders; every partition has a ladder side. Proposition5.20 p38 requires both LC(m,n) and LC(n,m) for irreducibility when one side is a ladder.

LM sectionA.5 pp52–53 supplies the ring involution Z(m)^t=L(m) on the same parameter m. It permutes irreducible basis classes and preserves products, hence preserves the length-one property of their positive expansions. Testing L(m)xL(n) with the same endpoint parameters is justified; replacing m,n by guessed dual multisegments would be wrong.

The independently built graph computes all30 directions, all X/Y/edges, exhaustive injections and every Hall-deficient subset. Every partition has a failing direction with an isolated X vertex, matching the manuscript's singleton Hall strategy. This is a finite instance of the cited theorem, not a proof of a general irreducibility algorithm. Endpoint-grid controls detect shift+1, shift0, reversed first arrow, reversed second arrow, and extra self-edge definitions; some of those wrong conventions still reject all15 target partitions, so that rejection alone cannot calibrate correctness.

## Historical conclusions and limits

OWR14/2011 EMS p734 defines imprimitive as not an entire proper parabolic induction and Conjecture4 predicts2^k total orbit multiplicity. At k=1 the one factor may be pi and its irreducibility condition is automatic: prediction2 versus established0. OWR p729 Conjecture1 states the unrestricted local quasi-split unitary converse; the tau-invariant pi disproves its converse. FLO section3.2 pp214–215 makes the tau-Witt index additive on the unitary-tempered constituents of Langlands data; each individual Steinberg block here is tau-invariant and has index0. Thus index(pi)=0, and FLO Conjecture6.12 p246 would predict distinction on every orbit. The counterexample does not refute the generic/tempered positive results.

The primary dependencies have been checked at their interfaces, not re-proved. No claim of firstness, worldwide novelty, current unresolved status, separate kernel-generation disproof or Luo–Zha nonoverlap follows. The complete Luo–Zha body remains UNKNOWN under explicit human direction; no retrieval is attempted.

## Explicit new finite-coordinate and full-Y certificates

The bit columns below are A,B,C,D with T fixed0. Each listed equal-label edge independently excludes that coordinate.

|ABCD|Failed opposite-label edges|
|---|---|
|0000|TD,DB,BA,AC,CT|
|0001|BA,AC,CT|
|0010|TD,DB,BA|
|0011|BA|
|0100|TD,AC,CT|
|0101|DB,AC,CT|
|0110|TD|
|0111|DB|
|1000|TD,DB,CT|
|1001|CT|
|1010|TD,DB,AC|
|1011|AC|
|1100|TD,BA,CT|
|1101|DB,BA,CT|
|1110|TD,BA,AC|
|1111|DB,BA,AC|

|Failing direction|Isolated X|Entire Y from the new graph|
|---|---|---|
|A→BCDT|('A', 'B')|('A', 'B'),('A', 'D')|
|B→ACDT|('B', 'D')|('B', 'D'),('B', 'T')|
|C→ABDT|('C', 'T')|empty|
|D→ABCT|('D', 'T')|('D', 'T')|
|ABCD→T|('C', 'T')|('B', 'T'),('D', 'T')|
|AB→CDT|('A', 'C')|('A', 'D'),('B', 'D'),('B', 'T')|
|AC→BDT|('A', 'B')|('A', 'B'),('A', 'D')|
|AD→BCT|('A', 'B')|('A', 'B'),('D', 'T')|
|AT→BCD|('A', 'B')|('A', 'B'),('A', 'D')|
|BC→ADT|('B', 'D')|('B', 'D'),('B', 'T')|
|BD→ACT|('D', 'T')|('B', 'T'),('D', 'T')|
|BT→ACD|('B', 'D')|('B', 'D')|
|CD→ABT|('C', 'T')|('D', 'T')|
|ABD→CT|('A', 'C')|('B', 'T'),('D', 'T')|
|ABC→DT|('B', 'D')|('A', 'D'),('B', 'D'),('B', 'T')|

The certificates establish no universal Hom theorem by themselves. The primary-interface derivation above supplies that missing logical bridge. The full graph/Hall/injection data are in independent.normal.json.
