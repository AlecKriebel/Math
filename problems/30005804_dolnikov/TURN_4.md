# Turn 4: analytic parallel-row theorem for every convex body

Fourth substantive author turn, continuing the exact turn-3 checkpoint
64a67d6d55d8db157edb844c1cb5b1166e0df218. The original problem remains
unresolved. This turn replaces the two trapezoid computations by an analytic
result for every planar convex body and arbitrary real positions along rows.
No novelty claim is made. The proof below is self-contained.

## 1. A row-span inequality

Let K be a nonempty compact convex set, e a fixed direction, and use coordinates
(x,y) with e horizontal. Write D=K-K. Let ell be the maximum length of a
horizontal chord of K. A longest chord exists by compactness. Equivalently,
ell=max{r >= 0 : (r,0) belongs to D}. The same maximum is attained for -K.

Every horizontal chord of D has length at most 2 ell. Indeed, if (u,h) and
(v,h) belong to D, with u<=v, then ((v-u)/2,0) belongs to D by symmetry and
convexity. Thus v-u<=2 ell.

Let A and B be finite nonempty sets of translation vectors satisfying

    a-b belongs to D for every a in A and b in B.                 (1)

This is exactly cross-intersection of the two families of translates of K.
For a nonempty horizontal row A_i of A, let w(A_i) be its x-span; similarly
for a row B_j. The two vectors

    (max_x A_i - min_x B_j, y_i-y_j),
    (min_x A_i - max_x B_j, y_i-y_j)

belong to D. Their horizontal separation gives

    w(A_i)+w(B_j) <= 2 ell.                                      (2)

This uses actual extrema, so equality and boundary touching cause no issue.

## 2. The parallel-row theorem

**Theorem.** Suppose A is contained in r horizontal lines and B in s horizontal
lines, where r,s are positive integers. Under (1), either the A-family is
pierceable by at most r points or the B-family is pierceable by at most s points.
The lines need not be shared by the two families, equally spaced, or integral.

Proof. If each row of A has x-span at most ell, cover each row by a translate of
a longest horizontal chord of -K. This covers A by at most r translates of -K,
and hence pierces {K+a:a in A} by at most r points.

Otherwise some A-row has span greater than ell. By (2), every B-row has span
strictly less than ell. Cover those rows instead, giving at most s points.
Translation-space duality here is exact: t belongs to q-K if and only if q
belongs to K+t. This proves the theorem. If ell=0, (2) forces every nonempty
row on both sides to have span zero, so the first case still applies. QED.

In particular, if each of any two source color families has translation vectors
on at most three lines parallel to one common direction, Dol'nikov's conclusion
holds for one of those colors. This is a restriction on the centers, not a
restriction to a credited body class. It applies to nonsymmetric bodies as well
as symmetric ones. It does not assert that physical translates merely having
three line transversals satisfy this hypothesis.

For an explicit piercing construction, let (u,v),(u+ell,v) be endpoints of a
longest horizontal chord of -K. A row of centers at height h with leftmost
coordinate x is covered by q-K for q=(x-u,h-v), provided its span is at most
ell. Thus the proof returns actual points, without an optimization oracle.

## 3. A two-point theorem for widely spaced rows

Let H=max_y K-min_y K>0. Suppose, separately for each color, its distinct
translation-vector row heights are separated by at least H. The row sets of
A and B need not have the same offset. Under (1), one family is two-pierceable.

First, if one family has only one row, select a vector from the other family.
Its centers are contained in a translate of D, whose intersection with that row
has length at most 2 ell by Section 1. Two longest chords of -K cover this
interval, proving the claim (if ell=0, one point suffices).

Otherwise both have at least two rows. Set span_y A=max_y A-min_y A, and
similarly for B. Since D has vertical extent [-H,H], the two cross inequalities

    max_y A-min_y B <= H,  max_y B-min_y A <= H

give span_y A+span_y B<=2H. Each span is at least H by the separation
hypothesis. Therefore both spans equal H, and each family has exactly two rows.
Apply Section 2 with r=s=2. This proves the claim.

The two-point constant is sharp for this two-color statement. For the unit
square K=[0,1]^2 take A={(-1,0),(1,0)} and B={(0,-1),(0,1)}. Every cross pair
intersects, including corner contacts, whereas each same-color pair is disjoint.
Both families need exactly two piercing points. This is not asserted to be a
sharp example for the original three-color existential statement.

## 4. Consequence for the turn-3 trapezoids

For every real m>=1, put

    K_m=conv{(0,0),(m,0),(1,1),(0,1)}.

Its vertical width is 1. The two-point theorem applies to any two cross-
intersecting finite families with centers in R x Z (or in a translated copy
of that row system). In particular it applies to all integer translates, for
all integer m>=1, including the two nonsymmetric m=2,3 cases of turn 3.
No bound or integrality is imposed on horizontal coordinates.

This strengthens the existential conclusion of turn 3. It does not claim
its stronger intermediate assertion that the common-neighbor lattice set of
each minimal four-piercing obstruction is a singleton, nor does it invalidate
the exact certificate for that assertion.

## 5. Checks, literature, and exact remaining gap

The checker constructs longest chords using rational polygon sections, samples
cross-intersecting row configurations using exact membership in D, applies
both branches of the theorem, and verifies every returned piercing incidence.
It also verifies the sharp square example and finite controls for the entire
parametric trapezoid consequence. These are controls for the analytic proof,
not an exhaustive search over real configurations.

The original OWR contribution was re-opened at
https://ems.press/content/serial-article-files/48651 (printed pages 172-174).
The source still asks about arbitrary real translation vectors. Targeted
searches on 2026-10-03 for Dolnikov with parallel lines, translation vectors,
and trapezoids did not identify this row theorem in the inspected primary
sources. This is not a comprehensive novelty or current-status certification.
The general four-point result remains credited to Martinez-Sandoval and
Roldan-Pensado, https://arxiv.org/abs/2307.07714; the known body classes and
line-transversal results remain as recorded in SOURCE_GATE.md.

The exact gap is that finite real center sets need not lie in three parallel
lines, nor in rows spaced by H. Rationality does not imply the latter: after
clearing denominators, the body is scaled too, so its width relative to the
lattice changes. The row theorem therefore cannot complete the rational
reduction from turn 1. Turn 5 investigates positive-width strips and quantifies
what intersection margin would actually be needed. Original unresolved 4/5.
