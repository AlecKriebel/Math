# Five substantive approaches — problem 30006308

Date: 2026-10-04 UTC. These are five mathematical approaches within this
investigation, not five claimed historical browser-model sessions. Result:
**unresolved**, with precise partial results and gaps. No full-resolution claim.

## 1. Normalize the actual published higher-degree equations

Inspected the current Ilten–Robins proof and explicit degree supports, rather
than treating nonquadratic obstruction as a counterexample. In the four-variable
example the degree-3,5,7 equation equals `t4(t3-t1t2t4)^2`; an invertible
coordinate change removes the higher terms. The rank-four quadratic and
product-ideal examples admit analogous triangular changes. Corrected the
version-number shift and the missing t7 in the printed v5 hull display.

Outcome: these examples are conical. Mixed degrees in a chosen presentation
and nonformality of a controlling DGLA do not disprove tangent-cone determination.
Gap: the displayed coordinate changes have not been extended to arbitrary fans.

## 2. Force a common positive scalar weight

Proved that an equivariant hull presentation with a one-parameter subgroup
assigning the same positive weight to every tangent variable has a homogeneous
ideal and equals its completed tangent cone. Tested the criterion against the
four-character example. The exact relation `u3=u1+u2+u4` forbids equal positive
weights, even though that example is conical.

Outcome: a valid sufficient criterion, not a universal proof. Positive unequal
weights and lattice homogeneity must not be substituted for ordinary homogeneity.

## 3. Construct and reject a plausible equivariant counterexample shortcut

Built the exact formal ring
`k[[t1,t2,t3,t4]]/(t4(t3^2-t1^2t2^2t4^2))` using the same lattice weights.
All individual weight directions extend along coordinate axes. Factoring proves
it is reduced with three components, while its completed tangent cone is
nonreduced with two. This rigorously refutes the shortcut that these two formal
properties alone imply conicality.

Outcome: a countermodel for an inference, not a toric counterexample. Missing
step: realize that ring as the hull of a smooth complete toric variety. No such
realization is asserted, and no full-resolution status is warranted.

## 4. Compare genuine toric examples with the same complex counts

For `X(3,-4,3)` and `X(4,-4,3)`, solved the ray inequalities and computed all
contributing complexes. Both have counts `(1,2,3,7)` for abstract type, embedded
support, distinguished-ray/support pair, and ray-character pair, with tangent
dimension seven. Recomputed the needed quadratic cycle coefficients, exhaustively
checked all compatible obstruction monomials using positive weight bounds,
and applied explicit triangular changes to recover the two published hulls.
They have one and two minimal primes respectively.

Outcome: exact numerical determination from any of these counts, or their tuple,
is impossible. The hull examples are prior work, not newly discovered examples.
Gap: Question 5 asks for “any relation,” so this does not rule out bounds or
relations involving character or incidence data, and does not settle the
catalogue's two-question item.

## 5. Analyze a genuinely resonant toric fan and isolate its residual series

For `X(2,-4,4)`, computed nine tangent directions, one obstruction degree,
and the unique compatible quadratic monomial `xy` with nonzero coefficient -2.
Found a zero-weight pair `dq`, so weight arguments provide no finite all-order
cutoff. Exhibited the permitted residual quintic `c^2 p^2 q` involving neither
quadratic-pair variable. The formal splitting argument reduces the unknown hull
equation to `XY+G` in the other seven parameters.

Outcome: an explicit remaining all-order task. Neither G nor the normalized
quintic coefficient was computed. Infinite compatible multiples such as
`xy(dq)^n` need not be essential, and a raw higher coefficient before the
quadratic-pair elimination would not suffice. No all-order termination or
nonconicality certificate has been obtained.

## Reproducible checks and final disposition

`verify.py` completed successfully using Python 3.12.14 and SymPy 1.14.0. It checks
24 smooth-cone determinants, first-order support counts for the three fans,
complete finite obstruction-degree supports for the first two examples, their
quadratic cycle coefficients, exact normalization identities, the countermodel's
weight and factorization identities, and the resonant candidate's finite data.
The script initially exposed a coefficient slip for the resonant candidate:
its correct cycle coefficient is -2, not the -1 in the other examples. The proof
and final saved verification agree on -2.

The remaining gap is mathematical, not a failed numerical search: no universal
all-order elimination theorem or actual toric counterexample has been proved.
The broad component-relation question also remains open within this work.
Recommended queue disposition after review: `unsolved`, `5/5`; retain the
partial results and source qualifications. Publication is limited to a draft PR,
after independent review; no merge, release, or outreach is included.
