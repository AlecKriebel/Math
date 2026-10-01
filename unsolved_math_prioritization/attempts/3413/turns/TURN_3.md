# Turn 3: nonfree strata and the signed case with a positive singleton

**Unreviewed partial. Original hyperbolic/full-symmetry realization unresolved, 3/5.**

This turn proves additional necessary conditions for the original representations and a complete intermediate ambient-unlink classification for signed representations having a positive singleton. The latter does not construct the distinguished hyperbolic component or certify a full symmetry group. Classical fixed-axis, equivariant-unknot and linking inputs are credited explicitly.

## 1. Classical inputs and conventions

A finite group action here is a faithful smooth orientation-preserving action on S3, as provided for the source group by Budney's extension argument. The classical Smith fixed-axis theorem says that a nonidentity finite-order orientation-preserving map of S3 with a fixed point has fixed set an unknotted circle and is conjugate to a rotation about that circle. Its cyclic quotient is S3, with the usual branched-cover local model transverse to the axis. This is the same Smith input used by Budney, Proposition3.5; Boileau–Paoluzzi–Zimmermann explicitly recall the orthogonal-rotation consequence on printed91 of their 2008 paper. We are using smooth actions, not arbitrary wild topological actions.

We also use the following classical consequence of an equivariant disk fibration of the unknot exterior: if a finite abelian group preserves an unknot and its orientation, all its nontrivial elements having fixed axis disjoint from the knot have the same axis, and that axis together with the knot is a Hopf link. This is Paoluzzi2005, Claim2.1 and Remark2.2, printed643, credited there to Hillman and the equivariant fibration theorem of Edmonds–Livingston. The disjoint-axis qualifier is essential; elements fixing the knot pointwise are not in that statement.

Finally we use Turn2's free-cover linking lemma and the elementary reversal lemma in Turn1. The proof below makes the branched-cover normalization separate from the free-cover normalization.

## 2. Branched covering normalization

Let P=C_k act by rotations about an unknot A, and identify S3/P with S3. Suppose disjoint oriented circles K,J, both disjoint from A, are preserved by P. The restriction to either circle is free, hence its quotient map has degree k and its image has connected full preimage. Then

    lk_upstairs(K,J) = k lk_downstairs(barK,barJ).                 (3.1)

To prove this, choose an oriented Seifert surface S for barK, transverse to the quotient branch axis and to barJ. Its full inverse image is an oriented surface branched over S's transverse intersections with the axis, with boundary exactly K. Near a transverse branch point, the model (z,t)->(z^k,t) shows that the lift is still a smooth oriented surface. Every intersection with barJ is away from branching and lifts to k intersections of the same sign on J. Taking the intersection number proves (3.1). Possible closed components of the inverse surface do not change the linking number. Thus pairwise linking zero upstairs remains zero downstairs in this particular invariant-component situation.

This formula is not a claim about arbitrary components with disconnected preimages, and it does not assert that the quotient of an unlink is an unlink. Only the pairwise zero linking needed below is transferred.

## 3. Two positively invariant unlink components force a common fixed axis

**Lemma3.1.** Let a nontrivial finite cyclic group H act on S3 and preserve each of two components K,J of an unlink, with positive orientation on each. Then H itself fixes an unknotted circle pointwise. In particular every element of H is a rotation about that common circle.

Proof. First no nonidentity element of H fixes K pointwise. If h did so, its global fixed set would be exactly K by the Smith theorem. It cannot also fix J pointwise. Since its restriction to J is a finite-order orientation-preserving circle map, it has no fixed point on J. The classical equivariant-unknot statement applied to J would make J and K a Hopf link, contradicting linking zero. The same argument applies to J. Hence the H action on either component is faithful and has no fixed points there.

If H acts freely on all of S3, Turn2 Lemma2.1 already contradicts lk(K,J)=0. Otherwise let A be the axis of a nontrivial element with fixed points. It is disjoint from K and J. Applying the common-axis theorem to the H-invariant unknot K shows that every nonidentity element of H with fixed points has this same axis A.

Let P be the subgroup of H that fixes A pointwise. The preceding paragraph says precisely that P consists of the identity and all elements having fixed points. It is a nontrivial subgroup. The quotient S3/P is S3. The induced H/P action is free: if a coset hP fixed a quotient point, then hx=px for some p in P and some lift x. Therefore p^(-1)h would have a fixed point, so belong to P, forcing h in P. Every element of H preserves the orientation of A, because a reversing circle map would have a fixed point and hence belong to P, which fixes A pointwise. Smoothness in the branched quotient follows from an invariant tubular metric: the commuting group maps the oriented normal coordinate z to alpha(t)z, and after quotienting P the normal coordinate z^|P| transforms smoothly by alpha(t)^|P|. The quotient action is orientation preserving.

The circles barK and barJ are distinct, individually invariant and have linking zero by (3.1). If H/P were nontrivial, the free-cover linking lemma would again give a contradiction. Thus H=P and H fixes A pointwise. QED.

This lemma uses the fact that K and J are unknotted, as well as their linking zero. It is not extended to arbitrary algebraically split knotted components.

**Corollary3.2.** For a positive component orbit of length 1<d<m in the source, the stabilizer <g^d> fixes an axis pointwise.

Indeed, positivity makes the stabilizer preserve each component orientation. Since the full cyclic group is abelian it preserves every one of the d orbit components, so Lemma3.1 applies to two of them.

**Corollary3.3.** If the source representation has at least two positive singleton cycles, the full C_m action is a rotation group fixing a common axis pointwise.

Both corollaries concern the actual ambient group, not merely the image of its signed representation.

## 4. At most two axes and their coprime stabilizer orders

For any fixed axis A of an element of G=C_m, the whole group preserves A because it is abelian. Its restriction preserves the orientation of A. To see this, if m>2 a generator reversing A would have order2 by Turn1's reversal lemma, a contradiction; if m=2 the generator itself fixes its axis pointwise.

For an orientation-preserving finite circle action, any element with a fixed point acts identically on the circle. Thus a different fixed axis cannot meet A: any such intersection would force that element to fix all of A, and its global fixed set would equal A.

Apply Paoluzzi's common-axis statement to the G-invariant unknot A. Every nontrivial group element with a fixed axis other than A is a periodic symmetry with its axis disjoint from A. All such axes must therefore be the same circle B. If B exists, A and B form a Hopf link. This proves that there are at most two distinct axes for all nonidentity elements of G.

Let P_A and P_B denote the full pointwise stabilizers of the axes. Their intersection is trivial: a nonidentity element cannot have two distinct fixed circles. Since G is cyclic,

    gcd(|P_A|,|P_B|)=1.                                        (3.2)

This is derived from the classical unknot theorem and cyclic subgroup arithmetic; a global classification of finite S3 actions is not required.

## 5. A negative cycle determines an axis stabilizer exactly

Suppose a negative cycle occurs. By Turn1, m=2d and the cycle length is d. The involution h=g^d reverses one component K and has exactly two fixed points on that circle. Both lie on its global fixed axis A.

Let e be the order of g's restriction to A. Since g^d=h fixes A pointwise, e divides d. If e<d, a point p in K intersect A would satisfy g^e p=p. But it would then lie both on K and on the distinct component g^e K, impossible. Hence e=d. The kernel of G->Diff(A) consequently has order exactly2:

    P_A=<h>,  |P_A|=2,  order(g on A)=m/2.                    (3.3)

It follows that:

1. If m>2, there is at most one positive singleton. Otherwise Corollary3.3 makes the full G a rotation group about an axis C. Its involution would have that same axis C=A and P_A would have order m, contradicting (3.3).
2. A positive nonsingleton proper orbit of length j has stabilizer order k=m/j. By Corollary3.2 its stabilizer fixes an axis C pointwise. If C=A, then k=2 by (3.3); if C is the other axis B, then k is odd by (3.2). Therefore

       1<j<m and positive  ==>  m/j=2 or m/j is odd.            (3.4)

This condition only applies when a negative cycle is present. In particular it excludes any even stabilizer order greater than2. In 2-adic language the positive proper cycle length either equals m/2 or contains the full power of2 dividing m.

Examples newly excluded beyond Turn1 are C8 with one negative4-cycle and one positive2-cycle, and C12 with one negative6-cycle and one positive3-cycle. Their signed permutations have order exactly m and their negative cycles satisfy Turn1, but the positive orbit stabilizers have order4.

## 6. Negative cycles together with a positive singleton

**Theorem3.4 (necessary source condition).** Suppose m>2 and the source representation has a negative cycle and a positive singleton. Then:

- there is exactly one positive singleton;
- every negative cycle has length d=m/2;
- every other positive cycle has length d or m.

Proof. Only the last point remains. Let U be the positive singleton and J a component in a positive nonsingleton proper orbit of length j. Its nontrivial stabilizer H=<g^j> fixes some axis C pointwise by Corollary3.2.

If C=U, an element generating H is a periodic symmetry of the unknot J with axis U; the common-axis/Hopf-link theorem gives |lk(U,J)|=1, impossible. Thus C differs from U. A generator of H has no fixed point on U, since a finite positive circle action fixing one point would fix the whole circle, forcing U=C. Hence C is a periodic axis for the G-invariant unknot U.

The negative involution axis A also differs from U: it intersects a negative component, whereas U is disjoint from all other components. The same argument makes h a periodic symmetry of U with axis A. Paoluzzi's common-axis statement applied to U forces C=A. Therefore H is a nontrivial subgroup of P_A=C2, so |H|=2 and j=m/2. QED.

For example, C6 with one negative3-cycle, one positive2-cycle and one positive singleton satisfies Turn1 and the even-stabilizer test(3.4), but is excluded by this theorem. C4 with one negative2-cycle and two positive singletons is already excluded by point1 of Section5.

## 7. Sharpness at the ambient-unlink level

**Theorem3.5 (intermediate converse).** For each even m=2d>2, every multiset consisting of k>=1 negative d-cycles, l>=0 positive d-cycles, a>=0 positive m-cycles and exactly one positive singleton is realized by a smooth orientation-preserving C_m action preserving an unlink. Together with Theorem3.4, this classifies the intermediate ambient-unlink problem with a negative cycle and a positive singleton.

Proof. On S3 in C² choose

    g(z,w)=(zeta z,zeta² w), zeta=exp(2pi i/m).

This has order m. The involution h=g^d is (-z,w), with fixed axis A={z=0}. Its full pointwise stabilizer is C2, and g acts on A with order d. The other coordinate circle U={w=0} is invariant and positively rotated; it will be the positive singleton.

Choose an embedded spanning disk D for U meeting A transversely in one point; the two coordinate circles form the standard Hopf link, so such a disk is explicit. The finite union of translates of D meets A in only finitely many points. Choose k+l distinct G-orbits of points on A away from this finite set. Each orbit has d points. Small invariant metric balls around these points can be chosen so that their different images and different chosen orbits are disjoint, and all avoid D and U. Each ball has stabilizer precisely <h>.

At a chosen axis point, use equivariant exponential coordinates (t,x,y), with t tangent to A. The involution is (t,x,y)->(t,-x,-y). For a negative orbit, take a small circle centered at the origin in the (t,x)-plane. Its spanning disk is in the same plane; h preserves the circle and reverses its orientation. Taking the d translates gives a negative d-cycle because the last return is h. For a positive d-cycle take the circle and disk in the normal (x,y)-plane instead; h is a rotation there and preserves its orientation. All these spanning disks lie in the mutually disjoint balls and miss D.

For each desired positive m-cycle choose a free point away from the axes and from the finite union of all disks and their translates. Pick distinct such G-orbits, then sufficiently small disjoint balls, and place one small disk-bounding circle in each ball orbit as in Turn2. This produces positive m-cycles. The resulting disks together with D are mutually disjoint, proving the whole link is an unlink. The signed cycle data are exactly the prescribed ones. QED.

The same local construction for m=2, with no restriction to a single positive fixed component, realizes any numbers of negative singleton circles, positive singleton circles and positive2-cycles as an ambient invariant unlink. Different axis-centered ball disks can be chosen disjoint. Thus m=2 is a genuine exception to the singleton restriction; it cannot be removed from that theorem's hypotheses.

## 8. Exact remaining gap and hyperbolic completion

These arguments rule out additional signed representations and give explicit ambient models attaining the negative-plus-singleton conditions. They still do not provide a hyperbolic link L0 union U whose full oriented-L0, orientation-preserving symmetry group is precisely the chosen C_m.

In particular, none of the ball constructions supplies the distinguished component L0. Adding an arbitrary invariant curve can leave splitting spheres or essential tori, can change the number of components of its quotient lift, and can leave additional symmetries. “Choose a generic equivariant decoration” is not a proof of the required hyperbolicity, unlink preservation and exact full-group statement.

The original Budney discussion, printed19–20, cites Kawauchi's imitation methods for many unsigned representations but explicitly records a limitation for genuinely signed representations. That observation cannot be replaced by an unverified general equivariant hyperbolization theorem. No such theorem satisfying all the present hypotheses has been established in this turn.

There are also unresolved intermediate cases without a positive singleton, including whether different odd stabilizer orders can coexist along the other axis under the unlink requirement. The condition(3.4) is necessary only; it is not asserted sufficient there. The whole original classification remains unresolved3/5. Estimated completion35%, a heuristic that includes the remaining construction gap.

## Sources added or used in this turn

- Budney, arXivmath/0506524v4: finite extension before Definition3.3; Smith use in Proposition3.5; the original realization discussion and Kawauchi limitations, printed19–20.
- Paoluzzi, *Three Covers Determine Hyperbolic Knots* (2005), Claim2.1/Remark2.2, printed643: https://www.i2m.univ-amu.fr/perso/luisa.paoluzzi/jktr05.pdf . This is the precise equivariant-unknot input, not a classification of source representations.
- Boileau–Paoluzzi–Zimmermann, *A characterisation of S3 among homology spheres*, GTMonographs14(2008),83–103, especially the Smith-rotation consequence printed91: https://msp.org/gtm/2008/14/gtm-2008-14-006s.pdf . Only that classical fixed-axis consequence is used, not the paper's stronger hypotheses or classification of general homology spheres.
- Massuyeau's torsion linking pairing input and the covering normalization are recorded in Turn2.

No historical novelty, full source solution, or independently reviewed status is claimed.
