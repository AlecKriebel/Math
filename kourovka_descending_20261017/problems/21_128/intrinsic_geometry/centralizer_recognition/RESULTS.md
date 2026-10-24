# Centralizers and the missing recognition theorem for 21.128

Checkpoint: 2026-10-24 20:29 UTC. Completion estimate toward a complete solution of
21.128 from this route: **10%**. Outcome: rigorous forward lemmas and a precise
classification gap, **not a solution**. No originality claim is made for the lemmas.

Write A_T for a spherical Artin group, P_T for its pure subgroup, and
Q_T=P_T/Z(P_T). All commensurability below is abstract commensurability.

## 1. A genuinely finite-index-natural centralizer invariant

For an element g of a group G set

    SC_G(g) = union over m>=1 of C_G(g^m).

This union is a subgroup: C_G(g^m) and C_G(g^n) are contained in
C_G(g^lcm(m,n)). It is unchanged on replacing g by any nonzero power. If U has
finite index in G and g belongs to U, then

    SC_U(g) = U intersect SC_G(g),

and this has finite index in SC_G(g). An isomorphism f:U -> V carries SC_U(g)
isomorphically onto SC_V(f(g)). Every g in G has a positive power in U. Therefore
the set of abstract commensurability classes of stable element centralizers is an
abstract commensurability invariant of G. This statement does not assert that a
specific word, generator, or parabolic is recognized.

In a linear group SC_G(g) is the centralizer of one power of g. Here is a short
proof independent of any effectiveness question. Embed G in GL_d(K), and consider
the ascending chain of vector spaces

    C_End(K^d)(g^(1!)) <= C_End(K^d)(g^(2!)) <= ... .

A strictly increasing chain has at most d^2 increases, so this chain eventually
stabilizes. Every positive integer divides a sufficiently large factorial. Thus
the union of all power commutants equals one factorial-power commutant, and
intersecting with G gives the assertion. This is only an existence proof of the
stabilizing power.

Cumplido--Gonzalez-Meneses--Perego, arXiv:2510.00713v2, Theorem 30 (PDF pp18--20),
prove the stronger fact that the entire sequence of power centralizers in a
spherical Artin group is periodic, with computable period. The current v2 is dated
8 October 2025. Their theorem is not a classification of the resulting groups.

For finite-index invariants involving the center of SC, the safe object is its
**virtual center**, VZ(H)={h in H : [H:C_H(h)] is finite}. For finite-index L<=H,

    VZ(L)=L intersect VZ(H).

Indeed, a subgroup of finite index in L also has finite index in H, and the reverse
direction follows by intersection. The ordinary center need not have this
finite-index property in arbitrary groups. Moreover L/VZ(L) is naturally a
finite-index subgroup of H/VZ(H), so the stable-centralizer spectrum may also
record abstract commensurability classes of these virtual-center quotients.

### Pure central quotients: no power ambiguity remains

Marin, *Sur les representations de Krammer generiques*, Ann. Inst. Fourier57
(2007), 1883--1925, DOI10.5802/aif.2317, Theorem3 (printedp1889/PDF8), proves
biorderability of every pure spherical Artin group P_T. Soroko,
arXiv:2009.10471v4, Proposition3(3),(4), records the genuine splitting
P_T=Q_T x Z(P_T) and the consequent biorderability of Q_T. These primary
statements have now also been read directly for this family; their cached
PDF hashes are in SOURCE_MANIFEST.json. Only biorderability is used below.

In a biordered group, x<y implies x^n<y^n for positive n, by two-sided order
invariance and induction. Thus x^n=y^n implies x=y. If h centralizes g^n,
then (hgh^-1)^n=g^n, so h centralizes g. Consequently, for all g in Q_T,

    C_Q_T(g^n)=C_Q_T(g),  n != 0,
    SC_Q_T(g)=C_Q_T(g).

Moreover VZ(K)=Z(K) for every subgroup K<=Q_T. An element in VZ(K) centralizes
a finite-index subgroup of K, which contains a positive power of each x in K.
Unique roots then imply that it centralizes x itself. The reverse inclusion is
immediate. This is a simplification of the intrinsic invariant, not a
classification of the centralizers that occur.

## 2. Exact centralizers of maximal irreducible parabolic centers

Let A=A_T for T=F4 or H4, with standard generating set S, |S|=4. Let X be a
three-element subset and B=A_X. First B need not be irreducible. The Garside
element Delta_S is central, and generates Z(A); its Coxeter image is -Id.

### Normalizer lemma

    N_A(B) = B x <Delta_S>.

Proof. Ajbal--Godelle, arXiv:1605.07097v1, Theorem 1.3 gives
N_A(B)=B QZ_A(B), where QZ permutes X under conjugation. If q is in QZ_A(B), then
Delta_S^N q is positive for a sufficiently large N and still permutes X. By their
Definition 2.3 and Proposition 2.4, it factors into positive elementary ribbons.
At X each elementary ribbon indexed by t in X lies in B and leaves X unchanged.
For the single t outside X, the component X(t) of X union {t}=S containing t is S,
so its ribbon is Delta_S Delta_X^{-1}. It belongs to B<Delta_S>, and leaves X
unchanged because Delta_S is central and Delta_X permutes X. Induction along the
factorization shows q belongs to B<Delta_S>.

Finally B intersect <Delta_S> is trivial. If Delta_S^k=u v^{-1}, u,v positive in B,
replace by the inverse if necessary to assume k>0. Then Delta_S^k v=u is an
equality of positive Artin monoid elements. Its left side has support S and its
right side has support contained in X. Positive Artin relations preserve support,
and the positive monoid injects into A, a contradiction. This proves the direct
product assertion.

Now suppose B is irreducible, and put u_X=Delta_X^2. This element is pure and
generates Z(P_X), where P_X=P_T intersect B. For every nonzero integer m,

    C_A(u_X^m) = N_A(B) = B x <Delta_S>.

The first equality is Ajbal--Godelle Proposition 3.1(i)(a),(ii), a restatement of
the established spherical ribbon/normalizer results. It can also be seen using
power invariance of parabolic closure: PC(u_X^m)=B, so centralizing it normalizes
B; a normalizer preserves its positive central generator, since the length
homomorphism (every standard generator maps to 1) prevents inversion.

### Pure quotient lemma

The embedding P_X -> Q_T is injective, and for every nonzero m,

    C_Q_T(bar(u_X)^m) = P_X.                    (1)

The notation on the right denotes that embedded image. To check all quotient
issues, first C_A(P_T)=Z(A): P_T contains s^2 for every standard generator s, and
C_A(s^2)=N_A(<s>)=C_A(s). The last equality follows because an automorphism of
<s> sends s to s or s^{-1}, and length excludes s^{-1}. Thus
Z(P_T)=P_T intersect Z(A)=<Delta_S^2>.

If an element p Delta_S^k of N_A(B) is pure, its Coxeter image satisfies
pi(p)(-Id)^k=1. But W_X fixes a nonzero line pointwise, so -Id is not in W_X.
Consequently k is even and p is in P_X. Hence

    N_A(B) intersect P_T = P_X x <Delta_S^2>.

No extra centralizers appear on taking the quotient: if lifts a,b have commuting
images modulo <Delta_S^2>, their commutator is Delta_S^{2r}. Applying length gives
0=2r length(Delta_S), so r=0. Quotienting the displayed pure normalizer proves
(1), and also proves injectivity of P_X.

For a finite-index U<=Q_T, let B_U=U intersect P_X. Then

    C_U(B_U)=U intersect <bar(u_X)>,
    C_U(C_U(B_U))=B_U,                           (2)
    VZ(B_U)=Z(B_U)=B_U intersect <bar(u_X)>.

For the first equality, lift the purported centralizer to P_T. B_U has finite
index in B, so it contains a power of every standard generator of B. Centralizers
of powers of such generators equal their centralizers as above, and length again
removes any central commutator introduced by quotienting. Therefore this lift
centralizes B. Its centralizer in N_A(B)=B x <Delta_S> is
Z(B) x <Delta_S>; the pure intersection and quotient leave <bar(u_X)>.
The second equality follows from (1), because U intersect <bar(u_X)> contains a
nontrivial power of bar(u_X). The virtual-center assertion follows by applying
the same generator-power argument to any finite-index subgroup of B_U.

In particular, an arbitrary finite-index isomorphism sends B_U to a subgroup that
is the power-stable centralizer of a single element, has virtual center of rank
one, and is self-double-centralizing. This is a forward implication. An arbitrary
centralizer is already closed under the double-centralizer operation, since
C(C(C(E)))=C(E). Thus double-centralizer closure alone is a very weak converse.

## 3. Consequence for the F4/H4 comparison, and the actual gap

The maximal irreducible standard parabolics in F4 have type B3; those in H4 have
types A3 and H3. Equation (1) implies that Q_H4 has a stable centralizer
isomorphic to P_H3. If A_F4 and A_H4 are commensurable, the finite-index reduction
to pure central quotients carries this centralizer to a stable centralizer in
Q_F4 abstractly commensurable with P_H3. The group P_H3 is not commensurable with
P_A3 or P_B3, by the established spherical Artin commensurability results of
Cumplido--Paris. This does **not** exclude all stable centralizers in Q_F4.

A possible sufficient theorem would classify all stable centralizers in Q_F4
having rational cohomological dimension three, virtual-center rank one, and
strongly indecomposable center quotient. No such theorem was established here or
found in the primary sources audited. Specifically:

* Nonparabolic elements with empty algebraic canonical reduction system have not
  been shown here to have virtually cyclic stable centralizer. The historical
  analogue was explicitly posed as an open issue by Paris. The 2025 canonical
  reduction paper provides a definition, invariance under conjugation/powers,
  and algorithms; it does not provide the missing full centralizer decomposition.
* Even restricting to **parabolic-center** centralizers, rank-one parabolics of
  F4 supply another group. Davis--Huang identifies the pure centralizer using the
  rank-three restricted arrangement (F4,A1), not merely B3. It has thirteen
  hyperplanes and exponents (1,5,7), and is nonsupersolvable. See Amend--Hoge--
  Roehrle, arXiv:1311.0620v2, Lemma 3.3(iii), Lemma 3.4/Table 3.
* Nonsupersolvability and the exponent list are **not** asserted to be abstract
  commensurability invariants. They therefore neither prove nor refute that this
  restricted-arrangement group is commensurable with P_B3 or P_H3. That is a
  separate unproved comparison. Omitting this profile invalidates an exhaustive
  list before even addressing arbitrary elements.

Rank-two irreducible parabolic centers have normal and restricted rank-two
arrangements, so their pure centralizers modulo the global center are virtually
Z times two nonabelian free factors. A proposed strongly indecomposable-center-
quotient filter should exclude these product profiles. It still must justify the
filter and cover the rank-one restricted-arrangement profile and all nonparabolic
elements. This paragraph is a route diagnosis, not an exhaustive classification.

## 4. An A3 test refuting intrinsic recovery of raw parabolic rank

Let G=B4/Z(B4), and identify its finite-index pure subgroup H=P4/Z(P4) with
PMod(S_0,5). Label the capped boundary puncture 0 and the other punctures 1,2,3,4.
Let c separate {1,2,3} from {0,4}. The subgroup of pure braids supported in the
three-punctured disk is a pure rank-two irreducible Artin parabolic P3. Cutting
along c shows

    C_H(T_c)=P3 ~= F2 x Z,

with virtual center generated by the boundary twist T_c. The complementary side
is a pair of pants and adds no independent mapping classes.

Choose an orientation-preserving sphere mapping class f swapping punctures 0 and
1 and preserving the other labels. Conjugation by f is an automorphism of H. It
sends c to d separating {0,2,3} from {1,4}. Viewed from the capped-boundary label 0,
the disk side of d contains **two** of the finite punctures. Thus T_d is a power
of a rank-one parabolic generator, whereas T_c is a rank-two parabolic center.
Their centralizers in H are isomorphic via conjugation by f.

Moreover f P3 f^{-1}=C_H(T_d) is not internally commensurable with any proper
rank-two irreducible parabolic intersection in H. Such an intersection has virtual
center generated by a twist about a curve whose disk side contains three finite
punctures. Internal commensurability forces their virtual centers to be internally
commensurable. Nonzero powers of Dehn twists about different curves are unequal
(for example their canonical reduction systems are different). The disk sides
contain two and three finite punctures, respectively, so those curves cannot be
isotopic. Reducible rank-two parabolics are abelian and cannot be commensurable
with F2 x Z.

This is not a noncommensurability counterexample to 21.128: both subgroups in the
example are abstractly isomorphic. It refutes a universal claim that finite-index
isomorphisms preserve the rank, or the actual subgroup, of the original disk
parabolics in central quotients. Preservation of a larger family of twist lines
is compatible with this example, but does not restore the lost rank labels.

## 5. Publication gate

Closed. No affirmative commensurability construction, noncommensurability
invariant separating all possibilities, or complete original solution results.
The maximal-parabolic calculations can be used in a later proof if an actual
intrinsic recognition/classification mechanism is supplied. The route must not
be reopened just by renaming that missing theorem as a hypothesis.
