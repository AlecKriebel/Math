# Mixed-type classifying spaces: a bounded reduction, not a solution

Problem 30003800 / OWR-16162-015. Assessment date: 6 October 2026.

**Disposition: unsolved in this investigation, five substantive approaches used.**
The conclusions below are characteristic-zero partial results and deductions from
credited theorems. Neither a general vanishing theorem nor a nonzero unramified
class has been established. No novelty or comprehensive current-openness claim is
made.

## 1. Target and conventions

Let F be algebraically closed. The question in Sanghoon Baek's contribution to
Oberwolfach Report 21/2018, Question 2, printed page 1268, concerns all semisimple
groups with arbitrary Dynkin components. In particular it permits a central
subgroup coupling components of different types. The contribution specifies
coefficients Q/Z(2) on page 1266. Theorem 2 immediately before the question assumes
characteristic zero; the question itself does not restate that hypothesis.

All assertions proved in this report assume **char(F)=0**. This is a restriction,
not a correction silently imposed on the question. Positive-characteristic
p-primary cohomology requires its separate definition and treatment and is not
settled here.

Write

    G = G_sc / mu,     G_sc = product_i S_i,

where each S_i is split, simple and simply connected, and mu is a finite central
subgroup. Splitness follows from algebraic closedness. The notation does not
require mu to be a product of subgroups in individual factors.

Use a generically free representation and its quotient to define F(BG), up to
stable purely transcendental extension. Set

    U(G) = H^3_nr(F(BG)/F, Q/Z(2)).

Unramified means that every residue at a discrete valuation trivial on F vanishes.
For a prime l, U(G){l} denotes the l-primary subgroup. We identify U(G) with
degree-three unramified cohomological invariants of G using evaluation on a
generic torsor. All invariants here are normalized; constants vanish because
H^3(F,Q/Z(2))=0. None of the arguments concern singular cohomology of a
topological classifying space, higher cohomological degrees, or stable rationality
of BG itself.

## 2. Credited inputs and their exact boundaries

The following inputs are used, rather than reproved or claimed as discoveries.

- **M16:** Merkurjev, *Unramified degree three invariants of reductive groups*,
  Adv. Math. 293 (2016), 697-719. Proposition 4.1 identifies unramified invariants
  with U; Corollary 6.3 gives direct-product additivity over our field;
  Proposition 7.1 gives invariance of the l-primary group under a central isogeny
  with kernel of order prime to l; Theorems 8.4 and 11.3 give respectively simple
  group vanishing and odd-primary vanishing. This does not dispose of mixed
  central 2-primary couplings. [Author PDF](https://www.math.ucla.edu/~merkurev/papers/unramnew2.pdf)
- **M18:** Merkurjev's type-A theorem covers arbitrary central quotients of
  products of special linear groups in characteristic zero, including differing
  ranks. [Theorem 1.2](https://www.math.ucla.edu/~merkurev/papers/typeA3.pdf)
- **B19:** Baek's Theorem 1.2 covers products entirely of Spin_(2n+1), entirely
  of Sp_(2n), or entirely of Spin_(2n), with arbitrary central quotient in each
  family. Its three displayed alternatives are not a theorem about arbitrary
  simultaneous mixtures of B, C and D.
  [arXiv:1801.08845](https://arxiv.org/abs/1801.08845)
- **B21:** Baek's exceptional-group theorem covers mixtures among G2, F4, E6,
  E7 and E8. Corollary 4.3 supplies the 2-primary vanishing for
  (Spin_12 x SL_2)^n / mu for arbitrary central mu; Lemma 5.2 uses a
  maximal-rank D6+A1 subgroup to detect E7 invariants. This paper was published
  in J. Pure Appl. Algebra 225 (2021), article 106718. The inspected text is its
  2019 arXiv manuscript, with the indicated manuscript numbering.
  [arXiv:1906.02087](https://arxiv.org/abs/1906.02087)
- **P17:** Petrov's D6+A1 construction gives a subgroup P of simply connected
  E7 that contains Z(E7); P is a central quotient of Spin_12 x SL_2. For
  Pbar=P/Z(E7), H^1(-,Pbar) -> H^1(-,E7_ad) is surjective after a finite
  separable extension of odd degree. This is Theorem 1 of the inspected arXiv v2,
  cited as Proposition 1 by B21.
  [arXiv:1309.7325v2](https://arxiv.org/abs/1309.7325v2)

The publication-year discrepancy in the catalogue is bibliographic: EMS gives
volume year 2018 and publication date 12 April 2019. The report's statement is
not replaced by a homogeneous theorem.

## 3. Product inheritance, with the necessary qualification

**Lemma 3.1.** For split semisimple G1 and G2 over F,

    U(G1 x G2) = U(G1) direct-sum U(G2).

**Proof.** Apply the additivity input to degree-three invariants. Its two summands
are pulled back along the projections and recovered by restricting to the
inclusions with the other torsor trivial. An unramified invariant restricts to an
unramified invariant on either factor. Conversely the sum of pulled-back
unramified invariants is unramified: evaluate at a pair of torsors over any
extension field and apply any residue, which is additive. Generic evaluation
then gives the stated isomorphism. QED.

This is a statement about an actual direct product. The mere disconnection of a
Dynkin diagram does not provide the required product decomposition of G.

**Lemma 3.2 (central partition criterion).** Suppose V=product_j V_j is a
product of semisimple groups and N is a finite central subgroup. If

    N = product_j (N intersect Z(V_j)),

with the factors embedded in their respective coordinates, then

    V/N = product_j [V_j / (N intersect Z(V_j))].

Consequently U(V/N) vanishes if every displayed factor has vanishing U.

**Proof.** The product of quotient maps has kernel exactly the displayed product
of intersections, hence exactly N. The induced quotient isomorphism proves the
first assertion. Iterate Lemma 3.1 for the second. QED.

Testing only pairwise projections is insufficient. In (Z/2)^3 the subgroup
N={(a,b,c):a+b+c=0} has full projection to each pair of coordinates, but has
order four and intersects each single-coordinate subgroup trivially. Thus its
three-factor decomposition fails despite all pairwise projection tests passing.
This elementary example concerns central subgroup structure, not a nonvanishing
unramified cohomology class.

## 4. Exact reduction to the even-center factors

Let mu_2 be the 2-primary subgroup of mu. Since char(F)=0, these finite central
groups are diagonalizable and have the usual primary decomposition. Put
G_(2)=G_sc/mu_2.

**Proposition 4.1.** There is an isomorphism U(G) ~= U(G_(2)). After removing
simple factors whose centers have odd order, the same U is obtained from a
central 2-primary quotient of a product with simple types only

    A_(2r-1), B_n, C_n, D_n, E7.

Use the usual identifications in the small ranks, rather than counting one
simple group twice under different names.

**Proof.** The map G_(2)->G has central kernel mu/mu_2 of odd order. The
prime-to-2 isogeny theorem gives an isomorphism of the 2-primary unramified
invariant groups. All odd-primary groups of both semisimple groups vanish by
the odd-prime theorem. The torsion cohomology group is the direct sum of its
primary parts, so these assertions give the claimed isomorphism of U groups.

Write G_sc=T x V, where T contains exactly the simple factors with centers of
odd order. Every projection of the 2-group mu_2 to Z(T) is trivial. Therefore
mu_2 is actually contained in Z(V) and G_(2)=T x (V/mu_2). Each simple factor
of T has vanishing U by the simple-group theorem, so Lemma 3.1 removes T.
The center orders from the root-data classification are: n+1 for A_n; two for
B_n and C_n; four for D_n; three for E6; two for E7; and one for G2,F4,E8.
Thus precisely the asserted list can remain. QED.

Important consequences include the following.

1. Every possible obstruction in characteristic zero is 2-primary. We do not
   confuse this assertion with the stronger claim that every element has order
   two, which is unnecessary here.
2. All central identifications involving E6 or A_(2r) can be discarded for this
   particular obstruction after the prime-to-2 isogeny step, even if those
   identifications were not initially a product.
3. If the resulting mu_2 satisfies the partition criterion and each block is
   homogeneous of type A, B, C, D or E7, vanishing follows from the credited
   theorems. The criterion applies to the whole central subgroup, not merely
   to its rank or to pairwise data.

## 5. Removing E7 without losing mixed central identifications

We first record a general lifting argument, to keep its exact hypotheses visible.

**Lemma 5.1 (common-kernel lifting).** Suppose S is a subgroup of G, A is a
common central subgroup, and the quotient maps give central exact sequences

    1 -> A -> S -> Sbar -> 1,
    1 -> A -> G -> Gbar -> 1,

whose map on A is the identity. If H^1(-,Sbar)->H^1(-,Gbar) is surjective
after an odd-degree separable extension, then so is H^1(-,S)->H^1(-,G).

**Proof.** Take x in H^1(K,G) and its image xbar. Choose an odd-degree
separable L/K and ybar in H^1(L,Sbar) mapping to xbar_L. The obstruction
to lifting ybar is in H^2(L,A). By naturality and the identity map on A it
equals the obstruction to xbar_L. The latter is zero because x_L is already
a lift. Hence choose a lift y in H^1(L,S). Its image in H^1(L,G) and x_L
have the same image in H^1(L,Gbar). The standard central H^1(L,A) action
is transitive on this fiber. Acting on y by the required A-torsor produces a
lift whose image is x_L. This proves the assertion. QED.

**Lemma 5.2 (detection).** Such odd-degree surjectivity makes pullback on
2-primary cohomological invariants injective, and makes pullback on their
unramified subgroups injective.

**Proof.** If an invariant alpha pulls back to zero, choose L/K and y as in
Lemma 5.1 for any G-torsor x. Naturality gives res_(L/K)(alpha(x))=0.
Corestriction then gives [L:K]alpha(x)=0. Multiplication by an odd number is
injective on a 2-primary torsion group, so alpha(x)=0. This works for every
K and x. Pullback preserves unramifiedness because it evaluates the same
invariant on an induced torsor over the same field. QED.

**Proposition 5.3.** Let R be an arbitrary split simply connected semisimple
group, let E denote split simply connected E7, and let

    G=(R x E^a)/mu

for any central subgroup mu. Let P be Petrov's subgroup of E, and put

    S=(R x P^a)/mu.

Then pullback U(G){2}->U(S){2} is injective. Moreover, S is a central
quotient of R x Spin_12^a x SL_2^a. No coordinatewise assumption on mu is
needed.

**Proof.** Since P contains Z(E), the formula for S makes sense and embeds
S in G. Set A=(Z(R) x Z(E)^a)/mu. This is central in both groups, and the
two quotients by this same A are

    Sbar=R_ad x (P/Z(E))^a,
    Gbar=R_ad x E_ad^a.

Keep the R_ad torsor unchanged. Apply Petrov's odd-degree surjectivity to
the a exceptional coordinates successively. The tower has odd total degree,
so the quotient torsor map satisfies Lemma 5.1. Lemma 5.2 proves detection.

For the last assertion, use the central covering
R x Spin_12^a x SL_2^a -> R x P^a and take the inverse image nu of mu.
This inverse image is central: if an element maps into a central subgroup,
its commutator with the connected covering group lies in the finite central
kernel; the resulting morphism from a connected group to a finite group is
constant and equals the identity at the identity. Thus S is the indicated
central quotient by nu. QED.

**Corollary 5.4.** Over an algebraically closed field of characteristic zero,
universal vanishing for arbitrary mixed semisimple groups is equivalent to
universal vanishing for arbitrary mixtures of classical types A, B, C and D.

**Proof.** The forward implication is specialization. For the converse,
Proposition 4.1 reduces to classical factors and E7. Proposition 5.3 injects
the remaining 2-primary group into that of a central quotient with classical
factors only. The assumed classical mixed-type statement kills the target.
Odd-primary parts were already removed. QED.

This is a reduction to an unsolved task in this investigation, not a verification
of the assumed classical mixed-type statement.

## 6. A genuinely coupled mixed family that does vanish

**Proposition 6.1.** For arbitrary nonnegative integers a,b,c and arbitrary
central mu,

    U((E7^a x Spin_12^b x SL_2^c)/mu)=0.

**Proof.** First consider H=(Spin_12^b x SL_2^c)/mu. If b=c=0 the group
is trivial. Otherwise take n=max(b,c) and add n-b simply connected Spin_12
factors and n-c simply connected SL_2 factors. Extend mu by the identity in
these added coordinates. The enlarged quotient is both H times the added
factors and a group (Spin_12 x SL_2)^n/mu'. Baek's Corollary 4.3 kills its
2-primary unramified group. Restriction along the section H->H times the
added factors is left inverse to pullback along projection, so U(H){2}=0.
Odd-primary vanishing gives U(H)=0. This argument explicitly removes the
equal-multiplicity limitation of the displayed source formulation.

For a>0 apply Proposition 5.3 with R=Spin_12^b x SL_2^c. The target has
only Spin_12 and SL_2 factors with some central quotient, so the preceding
paragraph kills its U. Injectivity and odd-primary vanishing prove the claim.
QED.

Proposition 4.1 also permits arbitrary additional factors A_(2r), E6, G2,
F4 and E8 and arbitrary central identifications with them. For example every
central quotient of E7 x Spin_12 x SL_2 x E6 x SL_3 is covered. This is an
explicit consequence of known inputs, not a claim of a new independent theorem.

## 7. A residue-and-lifting diagnostic for the remaining mixed case

Consider the honest mixed group

    H=(Spin_7 x Sp_6)/diag(mu_2),

of type B3+C3. These factors are not identified by a small-rank exceptional
isomorphism. Both centers have order two. The diagonal subgroup survives
Proposition 4.1 and does not satisfy the product criterion. It is not in the
D6/A1/E7 family of Proposition 6.1.

There is a central exact sequence

    1 -> mu_2 -> H -> SO_7 x PSp_6 -> 1.

The kernel is (mu_2 x mu_2)/diag(mu_2), identified with mu_2 by multiplying
the two coordinates. Accordingly the obstruction of a pair of adjoint torsors
(xi,eta) is

    delta_H(xi,eta)=delta_B(xi)+delta_C(eta) in Br(K)[2].

This follows either by pushing out the product of the two simply connected
central extensions, or directly by lifting Galois cocycles: the two resulting
central 2-cocycles are multiplied in the quotient kernel. Such a pair lifts
to H precisely when this sum is zero.

For an explicit failed independent-factor test, take K=F(x,y) and the quaternion
algebra Q=(x,y). Its Brauer class is nonzero: the residue at x=0 is the square
class of y in F(y), which is nonzero since its y-adic valuation is odd. Let xi
be the trivial SO_7 torsor. Let eta be the PSp_6 torsor corresponding to

    (M_3(Q), transpose tensor canonical-quaternion-involution).

The tensor involution is symplectic and the algebra has degree six. Over a
separable closure this pair is the split symplectic algebra, so it indeed
defines the claimed torsor. Its obstruction for Sp_6->PSp_6 is [Q]: pushing
this central extension to GL_6->PGL_6 identifies that obstruction with the
underlying algebra's Brauer class. Thus delta_H(xi,eta)=[Q] is nonzero, and
the pair cannot be used as an H-torsor.

This calculation exposes a concrete defect in attempting to apply independent
B- and C-type ramification witnesses to a coupled quotient. Splitting Q by a
quadratic extension fixes this lifting issue but does not preserve the desired
2-primary detection argument: restriction followed by corestriction multiplies
by two rather than an invertible odd number.

Crucially, the computation is a **degree-two lifting obstruction**, not a
nonzero element of U(H), and not evidence that U(H) is nonzero. We have not
determined U(H) in this investigation. We also do not claim that this particular
example is open in the entire literature.

## 8. What is still missing

After all five approaches the general coupled classical 2-primary case remains.
A completion by ramification would need a description of all relevant
degree-three invariants for each coupled group, followed by compatible torsor
constructions detecting every nonzero candidate by a residue. A counterexample
would instead need a nonzero degree-three class and a proof of vanishing at
every valuation in the definition of U. Neither requirement has been met.

The positive-characteristic p-primary part and any extension of the preceding
characteristic-zero deductions to it are also outside the result. Theorem
citations about prime-to-characteristic parts must not be used to erase this
qualification.

The search performed through 6 October 2026 found no primary-source theorem
settling the full extracted question. This bounded negative search does not
certify worldwide current openness. There are no numerical experiments or
executable mathematical checkers supporting these proofs; the logical arguments
and stated external theorems are the mathematical evidence.
