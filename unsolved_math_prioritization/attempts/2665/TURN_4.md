# Turn 4: satellite confinement, framing changes and the remaining band problem

**Unreviewed scoped partial, author turn 4/5. Original KP-1.6 unresolved.**
This turn attacks the satellite exception from turn 3. It proves a useful
reduction for companions without essential annuli, computes the exact effect
of changing the embedding framing, and gives concrete annular normal forms
for the two unresolved pairs. No common-boundary construction is asserted.

## 1. Genus-one confinement at an annulus-free companion

Let K be a genus-one knot, and let T bound a companion solid torus V containing
K, with T essential in the exterior of K. Write J for the nontrivial core knot
of V. Assume E(J)=S^3 minus int(V) has no essential properly embedded annulus.
This holds, in particular, for a hyperbolic companion. Then:

**Confinement lemma.** Every genus-one Seifert surface for K can be isotoped
relative to K into int(V).

Proof. Put a chosen surface F in transverse position with T, minimizing the
number of intersection circles. F is incompressible because it has minimal
genus; both F and T lie in the irreducible exterior of K. The usual innermost
disk argument therefore makes every intersection circle essential in both
surfaces. Suppose some circle were parallel to boundary K in F. An outermost
such annulus would isotope K to a curve on T. A meridional curve is an unknot;
a curve of longitudinal winding one is the core, making T peripheral; a
curve of absolute longitudinal winding at least two is a cable of J with
genus at least two by Schubert's genus inequality. Each contradicts the
hypotheses. Thus no intersection circle is boundary-parallel in F.

All disjoint essential non-boundary-parallel curves on a punctured torus are
parallel nonseparating curves. Cutting along m>0 such curves leaves one pair
of pants containing K and m-1 annuli. The pants lies on the V side, so every
component of F outside V is an annulus. Each is incompressible: its core is essential on F, and the minimal
Seifert surface is pi_1-injective in the knot exterior; a nullhomotopy in
E(J) would also be a nullhomotopy there. Since the companion
exterior is irreducible with incompressible torus boundary, an incompressible
annulus that is boundary-compressible is boundary-parallel. By the annulus-free
hypothesis all these annuli are therefore boundary-parallel. Choose an
innermost product region realizing such a parallelism, relative to the finite
disjoint collection of exterior annuli. Its interior is disjoint from F.
Sliding across it eliminates two intersection circles, contradicting minimality.
It follows that F misses T. Connectedness and boundary K inside V put F in V.

The boundary-parallel-circle argument is the one in Ozawa's *Satellite knots
of free genus one*, Lemma 2.2; inspection shows that that particular argument
only uses genus one and an essential companion torus, not the paper's additional
free-surface hypothesis. We do NOT apply its later free-genus classification
to arbitrary surfaces. Horn's *The first-order genus of a knot*, Theorem 4.7,
uses related confinement arguments for a specified pattern family; no extension
of that theorem's pattern hypotheses is assumed here. The proof above uses
the stronger explicit annulus-free exterior hypothesis instead.

This lemma applies to each member of any finite prescribed family. The
relative isotopies can be chosen separately because the original question
allows intersections between the resulting surfaces. There is no need for
a simultaneous isotopy preserving disjointness of the family.

## 2. Zero-framed untying preserves all contained pairings

Let e_0,e_1:V_abstract -> S^3 be orientation-preserving embeddings of an
abstract solid torus, with their longitude framings specified. For disjoint
oriented cycles alpha,beta in its interior, let w(alpha),w(beta) be their
integer longitudinal windings. Then for a fixed integer f depending only on
the two embeddings and their parametrizations,

 lk(e_1 alpha,e_1 beta)-lk(e_0 alpha,e_0 beta)
       = f w(alpha)w(beta).                            (1)

Here is a chain proof. If alpha is changed by the boundary of an integral
2-chain inside the solid torus, its linking number with beta changes by the
intersection of that chain with beta. The change is identical in both ambient
embeddings, because they preserve orientation. Thus the difference on the
left factors through H_1(V) in each variable. It is bilinear, hence a multiple
of the product since H_1(V)=Z. Testing on two disjoint parallel longitudes
identifies that multiple with their framing difference f. This also proves
that no unrecorded knotting contribution remains.

If F is an oriented surface contained in V with basis gamma_i and positive
push-offs inside V, (1) gives the exact matrix transformation

                 A_1=A_0+f w w^T,                    (2)

where w_i=w(gamma_i). Both its diagonal and off-diagonal entries are included.
In particular, a longitude-preserving, zero-framed re-embedding has f=0 and
preserves the Seifert pairing entry by entry, even for a whole finite family
of intersecting contained surfaces.

Choose e_0 to make V unknotted, matching the preferred longitude of J. Let
P be the resulting untied pattern knot. By the confinement lemma, every
minimal genus-one form type of K occurs on a genus-one surface of P. The
polynomial of a nonsingular genus-one form has degree two, so whenever such
forms are being studied P has genus exactly one. Thus, in that setting,

       {minimal form types of K} subset {minimal form types of P}.      (3)

This is a one-way inclusion, not a claim that every surface of P lies inside
its pattern solid torus. It is enough for the following consequence.

**Extended obstruction.** The determinant -342 pair of turn 3 cannot share
a boundary knot having an annulus-free companion exterior and an atoroidal
zero-framed untied pattern. Otherwise (3) would realize the pair on that
atoroidal pattern, contradicting its arithmetic distance-three obstruction.
Likewise, if the untied pattern is hyperbolic, the N=13 class can have at most
four minimal core form types at that satellite knot, by turn 3.

These statements rule out a substantial simple satellite mechanism. They do
not rule out companions with essential annuli, or an untied pattern that is
itself satellite. No unproved iteration reducing every satellite to an
atoroidal pattern is made.

## 3. A nonzero framing can change the form, but also changes the knot

For A=[[a,b+1],[b,c]] and winding vector w=(x,y), direct expansion of (2) gives

 det(A+f w w^T)=det A+f[c x²-(2b+1)xy+a y²].           (4)

The quadratic f² term cancels. The skew part remains the standard symplectic
matrix. Since a genus-one Alexander polynomial is determined by det A and
its normalization at t=1, equation (4) is also the exact condition for this
re-embedding to retain that polynomial.

For A=V_(N,a), formula (4) simplifies to

                   det change = f y(a y-Nx).          (5)

In particular, w=(1,0) changes only a to a+f and leaves the Alexander
polynomial unchanged. The turn-2 matrices V_(13,1) and V_(13,12) are related
algebraically by f=11 in this formula. The turn-3 matrices V_(37,1) and
V_(37,3) are similarly related by f=2.

But a nonzero framing change is a re-embedding of the pattern and generally
changes its boundary knot. Formula (2) compares surfaces on those two knots;
it does not produce two surfaces on one knot. To use this route, one would
need an actual isotopy identifying the new boundary with the old boundary,
with the required geometric choices. S-equivalence or equality of Alexander
polynomials does not provide such an isotopy. In particular, the current
Liu–Wang band-twist calculations studied in the source gate are not a theorem
asserting this common-boundary identification. The formula pinpoints the
missing geometric condition rather than concealing it.

## 4. Small common-framing normal forms for the annular route

The essential-annulus case is not excluded by a simple self-linking test.
Here are exact basis changes, all of determinant +1.

For the determinant -42 pair, use

 P_1=[[2,-1],[1,0]],             P_12=[[3,-1],[-2,1]].

Then

 P_1^T V_(13,1) P_1 = [[30,-8],[-9,1]],
 P_12^T V_(13,12) P_12 = [[30,-3],[-4,-1]].           (6)

For the determinant -342 pair, use

 Q_1=[[3,-1],[1,0]],             Q_3=[[15,1],[-1,0]].

Then

 Q_1^T V_(37,1) Q_1 = [[120,-21],[-22,1]],
 Q_3^T V_(37,3) Q_3 = [[120,27],[26,3]].             (7)

Thus the first pair has primitive homology vectors of common self-pairing
30, and the second pair has such vectors of self-pairing 120. These are
respectively 5*6 and 8*15, with relatively prime factors, so they are compatible
with the numerical cabling framings of torus-knot annuli. This is only an
arithmetic compatibility test. The calculations do not place those vectors
on actual essential companion annuli, choose a shared embedded band, or
prove equality of either pair of boundary knots.

The remaining data in (6) are different cross-linkings and band self-pairings:
(-8,-9,1) versus (-3,-4,-1). A geometric annulus/band construction would have
to realize this change while keeping one oriented boundary knot. In (7) the
analogous problem changes (-21,-22,1) to (27,26,3). Merely matching the first
self-pairing therefore does not solve the boundary compatibility problem.
Nor is arbitrary replacement of an exterior essential annulus by an annulus
on T justified to preserve its whole Seifert form; formula (1) only applies
to surfaces entirely inside a common solid torus.

## 5. Outcome and final remaining author turn

This turn supplies a proof of confinement for annulus-free companions, a
simultaneous zero-framed untying theorem, and an exact rank-one formula for
the framing-change route. It extends the turn-3 obstruction to a specified
satellite subclass and reduces the residual annular attempts to explicit
small matrices. The determinant -42 and -342 pairs remain unresolved for
unrestricted common boundaries. No genuine invariant excluding every
satellite realization, and no common-boundary annular construction, has
been obtained.

Four substantive author turns have been used. One remains. The final turn
must address that actual geometric compatibility or another unrestricted
mechanism; a further list of atoroidal examples would not close the target.
No speculative percentage completion, novelty claim or full-target promotion.
