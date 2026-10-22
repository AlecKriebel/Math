# Proofs of partial results and route obstructions

Throughout, R is a nonzero unital distributive ring; products carry the displayed
parentheses. The full group assumptions are those in `EXACT_TARGET.md`.

## 1. From strong units to nuclear translates

We use one identified literature input: for a ring coordinatising an A2-graded
group, every strong unit u is a Moufang element. This is recorded in Wiedemann,
*Root Graded Groups*, Remark 5.6.11, with attribution to Faulkner, Theorem 13.8.
The three identities, for arbitrary y,z, are

    u(y(uz)) = (u(yu))z,
    ((zu)y)u = z((uy)u),
    (uy)(zu) = (u(yz))u.

This checkpoint does not claim a new proof of that literature theorem.

**Lemma 1.** For every strong unit u and every z, (u,u,z)=(z,u,u)=0.

**Proof.** Put y=1 in the first two displayed identities. They become
u(uz)=(uu)z and (zu)u=z(uu). No cancellation or division by an integer is used. ∎

The nucleus N(R) consists of elements n for which each of
(n,a,b), (a,n,b), and (a,b,n) is zero for every a,b.

**Proposition 2.** If R coordinatises an A2-graded group and
R=R^×+N(R), where R^× denotes the strong units, then R is alternative.

**Proof.** The associator is additive in all three slots. If a=u+n with
u a strong unit and n nuclear, then

    (a,a,z)=(u,u,z)+(u,n,z)+(n,u,z)+(n,n,z)=0.

Similarly (z,a,a)=0. The first term in each expansion vanishes by Lemma 1,
and every other term has n in at least one slot. Thus both alternative laws
hold for all a,z. ∎

In particular it suffices that each element differs from a strong unit by an
integer multiple of 1. Each integer multiple of 1 is nuclear by distributivity
and unitality. The condition that a or 1-a is a strong unit for every a is another
sufficient special case. Division coordinate rings are already covered directly
by Lemma 1 and the trivial zero case.

**Gap.** The grading axioms do not here establish the nuclear-translate condition.
Additive generation by units would not alone justify it: the diagonal associator
is quadratic in its repeated argument, so unproved mixed terms remain.

## 2. Why the positive A2 commutators do not force alternativity

**Proposition 3.** Every unital distributive ring R, even a nonalternative one,
has a faithful positive-root model on H(R)=R×R×R with multiplication

    (a,b,c)(d,e,f)=(a+d,b+e,c+f+ae).

**Proof.** For a third element (g,h,i), the two parenthesisations have the same
first two coordinates. Their final coordinates agree because

    ae+(a+d)h = dh+a(e+h).

This is just distributivity. The identity is (0,0,0), and the inverse of
(a,b,c) is (-a,-b,-c+ab). The root maps

    x12(a)=(a,0,0),  x23(b)=(0,b,0),  x13(c)=(0,0,c)

are additive injections. The third image is central and
[x12(a),x23(b)]=x13(ab). Each element has a unique expression
x12(a)x23(b)x13(c-ab), proving positive-root factorisation. ∎

This is a full group proof, but for only the three positive root groups. It
does not manufacture the negative roots or the required Weyl elements.

For comparison, the standard associative-ring proof in an A3 subsystem uses
roots α,β,γ with α+β, β+γ, and α+β+γ all roots; it can compare
[[x_α(a),x_β(b)],x_γ(c)] and [x_α(a),[x_β(b),x_γ(c)] in one root group.
There are no such positive-root triples in A2. Its positive roots are α,β,α+β,
and none can be added to α+β to obtain a root. Thus transplanting that particular
rank-three argument is unjustified. This does not exclude other uses of
Hall–Witt involving opposite roots; Section 5 uses precisely that distinction.

## 3. Explicit algebraic controls and the invertibility trap

Let R0 be the F2-algebra with basis 1,e,f, with 1 a two-sided identity and

    e²=ef=f²=0,  fe=1.

Distributivity defines all products. It is not alternative: (f,f,e)=f and
(f,e,e)=e. Its only strong unit is 1.

**Proof of the last assertion.** For a=α+βe+γf, left and right multiplication,
in the ordered basis (1,e,f), are respectively

    L_a = [ α γ 0 ; β α 0 ; γ 0 α ],
    R_a = [ α 0 β ; β α 0 ; γ 0 α ].

Both determinants are α(α²+βγ). Thus a strong unit can only be 1, 1+e, or
1+f. A strong inverse must in particular be a two-sided ordinary inverse.
For 1+e that inverse is uniquely 1+e because its multiplication maps are
bijective. But (f(1+e))(1+e)=f+e≠f. Thus it is not a strong inverse.
For 1+f the corresponding failure is (1+f)((1+f)e)=e+f≠e.
The element 1 is a strong unit, completing the proof. ∎

Consequently all strong-unit Moufang identities hold in R0, since they are
identities at u=1 in every unital ring. This refutes the attempted inference
“strong units are Moufang, therefore the whole ring is alternative.” It also
shows why bijective multiplication operators or ordinary inverses cannot be
silently substituted for strong inverses in a generic-unit argument.

R0 is **not** a counterexample to the source problem: Section 5 proves it cannot
coordinatise such a group.

The exhaustive finite calculation in `finite_algebra_controls.py` considers all
8^4=4,096 choices for (e²,ef,fe,f²) in F2³. These are labelled tables, not
isomorphism classes. Exactly 76 are alternative, and in this small family all
76 are associative. Of 3,976 tables satisfying the strong-unit Moufang test,
3,900 are nonalternative. Among those, 3,888 have one strong unit and 12 have two.
These exact finite statements are computational controls, not classifications
of all rings or of all root-graded groups.

## 4. Naive matrix/Lie transfer proves too much

There is a classical alternativity theorem for appropriately root-graded Lie
algebras. An arbitrary abstract root-graded group is not thereby a Lie algebra.
No logarithm, linearisation, or faithful Lie representation is part of the target.

Here is a precise failure of the most elementary attempted linearisation.
Define 3×3 matrix multiplication using R's bilinear product, without assuming
that the matrix product is associative, and define [A,B]=AB-BA.
For A=aE12, B=bE23, C=cE31, direct multiplication gives

    [[A,B],C]+[[B,C],A]+[[C,A],B]
      = (a,b,c)E11 + (b,c,a)E22 + (c,a,b)E33.

The E11 coefficient is exactly (ab)c-a(bc), with no assumptions suppressed.
Thus requiring this full matrix commutator algebra to satisfy Jacobi already
forces R to be associative. A construction that does this cannot prove the
desired general result without excluding the known nonassociative alternative
examples. The symbolic program verifies the displayed identity in the free
unital nonassociative algebra, with no reassociation rule.

A similarly naive action on R³ by elementary shears with entries L_a requires
L_a L_b=L_ab in order for the root commutator relation to hold. Evaluating this
identity at c again forces a(bc)=(ab)c. Therefore the elementary-matrix
representation route has the same obstruction.

**Gap.** A correct Lie-theoretic route would need an additional faithful
construction for every abstract A2-graded group, with its hypotheses verified.
The classical Lie theorem alone supplies no such construction.

## 5. Opposite-root obstruction and the exact universal-group gap

The following argument uses only actual group commutation and injective root
coordinates. It does not assume division, characteristic restrictions, or the
alternative identities being sought.

**Lemma 4.** If x12(a) commutes with x21(d), then for every t in R,

    d(at)=(ta)d=a(dt)=(td)a=0.

**Proof.** An element commuting with each of two elements commutes with their
commutator. Let X=x12(a), Y=x21(d).

- Y commutes with x23(t) (same row) and with X. It therefore commutes with
  [X,x23(t)]=x13(at). Now [Y,x13(at)]=x23(d(at)), giving d(at)=0.
- Y commutes with x31(t) (same column) and with X. It therefore commutes with
  [x31(t),X]=x32(ta). Now [x32(ta),Y]=x31((ta)d), giving (ta)d=0.
- X commutes with x13(t) (same row) and with Y. It therefore commutes with
  [Y,x13(t)]=x23(dt). Now [X,x23(dt)]=x13(a(dt)), giving a(dt)=0.
- X commutes with x32(t) (same column) and with Y. It therefore commutes with
  [x32(t),Y]=x31(td). Now [x31(td),X]=x32((td)a), giving (td)a=0.

Each conclusion uses injectivity of the indicated root map. ∎

**Proposition 5 (fourfold annihilation obstruction).** If R coordinatises an
A2-graded group, then for all a,b,c,t in R,

    ab=ca=0  implies
    (bc)(at)=(ta)(bc)=a((bc)t)=(t(bc))a=0.                 (Z)

**Proof.** Put A=x12(a), B=x23(b), C=x31(c). The zero hypotheses say
[A,B]=[C,A]=1. Hence A commutes with [B,C]=x21(bc). Apply Lemma 4 with
d=bc. ∎

In particular, if ab=ca=0 and bc is a strong unit, then a=0: use t=1 and
apply the inverse of L_bc to (bc)a=0. No claim about the converse is made.

**Corollary 6.** R0 from Section 3 cannot coordinatise an A2-graded group.

**Proof.** Take a=e, b=f, c=e, t=1. Then ab=ca=0 but bc=1 and (bc)(at)=e≠0.
This contradicts (Z). ∎

Filtering the 3,900 nonalternative unit-Moufang survivors by (Z) rejects 3,324
and leaves 576 labelled tables. The filter is applied to all a,b,c,t, not just
basis values; its hypothesis is nonlinear in the tuple of parameters. Every one
of the 76 alternative control tables passes (Z).

A particularly simple surviving algebra R1 has e²=f²=0 and ef=fe=1 over F2.
It has (e,e,f)=e≠0 and only the strong unit 1, but passes (Z). The independent
coordinate program `verify_small_witnesses.py` checks both R0 and R1 without
importing the main enumeration. R1 remains only an algebraic test object.

To state the unresolved group-theoretic obligation exactly, define S(R) by
generators x_ij(a) for all a∈R and i≠j∈{1,2,3}, with the additive relations
and the two root-commutator relations in `EXACT_TARGET.md`.
Write U_ij for the images of the additive maps, which need not yet be injective.

**Proposition 7 (universal reduction).** R coordinatises an A2-graded group
if and only if S(R) has both of the following properties:

(I) every map a↦x_ij(a) is injective;

(N) for every positive system Π and α outside Π, U_α∩U_Π={1}.

**Proof.** If a coordinated group G exists, the defining relations give a
surjective map S(R)→G carrying each root generator to its given coordinate.
This proves (I). If x_α(a) belongs to U_Π in S(R), its image does so in G.
Nondegeneracy in G gives a=0, proving (N).

Conversely suppose (I) and (N). The additive and commutator axioms and
generation follow from the presentation, and nontriviality from R≠0 and (I).
It remains to check Weyl elements. Define

    w_ij=x_ji(-1)x_ij(1)x_ji(-1).

The usual three-factor calculation, using only the displayed presentation and
the two-sided unit, gives for k≠l

    x_kl(a)^w_ij = x_{τ(k),τ(l)}(εa),
    τ=(i j),   ε=-1 if j∈{k,l}, and ε=1 otherwise.

For completeness the four nonopposite cases at (i,j)=(1,2) are
x13(a)→x23(a), x23(a)→x13(-a), x31(a)→x32(a), and
x32(a)→x31(-a). They are obtained by conjugating successively by
x21(-1), x12(1), x21(-1) and collecting the commuting same-row or same-column
factors. For the remaining roots use
x12(a)=[x13(a),x32(1)] and x21(a)=[x23(a),x31(1)]. The four formulas then give
x12(a)→x21(-a) and x21(a)→x12(-a). Relabelling the three indices proves
the general formula. Thus w_ij is a Weyl element. Finally (N) is exactly the
remaining grading axiom. This proves the converse. ∎

The Weyl calculation is also the standard argument discussed by Wiedemann in
Proposition 5.6.6 and Remark 5.6.7; it imposes no unproved alternativity assumption.

**Exact remaining gap.** Either show that (I) and (N) force both alternative
identities for every R, or establish (I) and (N) for a particular nonalternative
ring. Neither property has been established for R1 or for any of the other
575 finite survivors. A presentation always exists, even when its root maps
collapse; merely writing it does not satisfy either obligation. No finite
presentation solver, normal-form theorem, or exhaustive finite-group search was
run or claimed. The full source problem therefore remains unsolved.
