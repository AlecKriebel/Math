# 1. Direct boundary-domain and halfspace geometry

## Attempt

Try to turn branching into a missing visual cap on each side of one leaf. First isolate the exact geometric certificate and test whether a weaker boundary condition suffices.

## Lemma 1: ideal domains are exactly halfspace certificates

Let L be a properly embedded plane in H^3, and U one of its two complementary components. Define Omega(U) using the closed-ball compactification as in RESULT.md. Then Omega(U) is open; it is nonempty if and only if U contains an open geodesic halfspace.

Proof. If p has a compactification neighborhood V with V intersect H^3 contained in U, shrink V. Geodesic halfspaces with round ideal caps shrinking to p form a neighborhood basis at p: in the Klein ball these are intersections of the open unit ball with affine halfspaces x dot p > a, as a increases to 1. A sufficiently small one lies in V. Conversely, an interior point of the ideal cap of a geodesic halfspace has a compactification neighborhood with interior part in that halfspace. This proves both directions and openness.

Moreover, S^2 minus Lambda(L) is the disjoint union Omega(U_+) union Omega(U_-). Indeed a point outside the closed limit set has a small connected ball-cap neighborhood disjoint from the closure of L. Its interior part belongs to one complementary component. It cannot belong to both. The reverse containment is immediate. In particular the sign is constant on each connected component of the boundary complement.

The use of a full compactification neighborhood is important: a single escaping ray, or a ball of large finite radius missing L, is insufficient.

## Countercontrol: a horosphere

In the upper-halfspace model take L = {(x,y,z): z=1}. This is a proper plane and Lambda(L)={infinity}. Its lower side z<1 contains the geodesic halfspace x^2+y^2+z^2<r^2 with 0<r<1. Its upper side z>1 contains no geodesic halfspace. Every geodesic plane is either vertical or a hemisphere orthogonal to z=0. Each side of either type contains points with arbitrarily small positive z: for a hemisphere use a point above its center for the inside and a point horizontally outside its defining disk for the outside. Thus no such side lies in z>1.

This plane is not a counterexample to Q10.1: the global closed taut two-sided-branching hypotheses are absent. It rigorously excludes the shortcut “proper limit set gives a halfspace on each side for any embedded leaf.”

## Global branch input and blockage

Calegari's *The Gromov norm and foliations*, Section 2.5, proves the relevant global alternative, using Fenley's limit-set theorem. In the closed taut two-sided setting, a proper limit set for one leaf is enough. That is a global theorem, not the elementary plane lemma above. The same section proves that a leaf limit set with empty interior rules out the non-separated alternative by translating branching leaves and applying the Baire property of the sphere.

The direct attempt provides the exact target Omega(U_+) != empty != Omega(U_-), but produces neither domain from arbitrary branching. Replacing this missing step by the global alternative only moves the gap to proving a proper limit set.
