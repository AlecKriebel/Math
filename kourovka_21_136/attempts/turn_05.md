# Attempt 5: the class-space topology and the remaining local obstruction

Date: 2026-10-03. Fifth substantive proof attempt for KOU-21.136.
Final research verdict: the unrestricted problem is unresolved in these attempts.

By Attempt 1, a counterexample can be assumed countably based. Let
N_1 >= N_2 >= ... be an open normal neighborhood basis with intersection 1.

## 1. A compact metrizable space of conjugacy classes

Send g in G to the sequence of conjugacy classes of gN_n in the finite groups
G/N_n. The image X is a compact metrizable zero-dimensional space. Two elements
give the same sequence if and only if they are G-conjugate. For the nontrivial
direction, the sets of t satisfying t g t^(-1) = h modulo N_n are nonempty,
closed, and nested; compactness gives an actual conjugator in their intersection.
Thus X is precisely the topological space of conjugacy classes. Write q:G->X.

Let T_m = {g : g^(m!)=1} and F_m=q(T_m). Each F_m is closed, because it is a
continuous image of a compact set into X. The sets F_m are increasing, and

  E = X minus union_m F_m

is exactly the space of infinite-order classes. It is a G_delta subspace of X.

## 2. Fewer than continuum becomes at most countable here

For completeness, the perfect-set step can be proved directly in this setting.
If E is uncountable, discard the points of E having some neighborhood whose
intersection with E is countable. Only countably many points are discarded,
because X has a countable base. Every remaining point has uncountably many
E-points in each neighborhood.

Recursively choose two disjoint clopen children inside each previously chosen
clopen set, each still meeting E uncountably, avoiding F_m at level m, and with
diameters tending to zero. At any stage there are two distinct retained E-points
in the parent; as they lie outside F_m, sufficiently small disjoint clopen
neighborhoods exist. Every infinite binary branch has a unique limit in X by
compactness and shrinking diameter. The limit avoids every F_m. Different
branches give different limits. Hence |E| >= c, contradicting P(G).

Therefore E is at most countable. This does not assume the continuum hypothesis.

## 3. A relative isolated class gives a single-orbit non-torsion coset

A G_delta subspace of a compact metric space is completely metrizable and hence
Baire. One can see completeness directly: with a bounded complete metric d on
X, add the terms

  sum_m 2^(-m) min(1, |1/d(x,F_m) - 1/d(y,F_m)|)

to d on E (omit terms with F_m empty). A Cauchy sequence has a d-limit in X, and
the reciprocal-distance coordinates stay bounded and Cauchy, preventing that
limit from entering any F_m. This metric induces the original topology on E.

If E is nonempty and countable, the Baire theorem shows that some singleton in
E has nonempty interior relative to E: otherwise E is the countable union of
nowhere-dense singletons. Choose such a class q(x), with x of infinite order.
A sufficiently small finite-coordinate cylinder around q(x) meets E only there.
Because the N_n form a descending basis, the cylinder can be taken to specify
one conjugacy class in G/N_n for some n. Consequently

  every infinite-order element of N_n x is G-conjugate to x.

This is only isolation among infinite-order classes. It says nothing of the kind
about all conjugacy classes or about an open orbit in G.

## 4. Why this is not yet a contradiction

In fact an infinite-order conjugacy class has empty interior in any profinite
group. If an open coset Ny, with N open normal in G, were contained in x^G,
conjugate it so its center is
x, keeping N normal. For every open normal L <= N, the finite quotient class
of xL has at least |N/L| elements. Its centralizer therefore has order at most
[G:N]. The order of xL is also at most [G:N]. This uniform finite bound in all
finite quotients would imply x^([G:N]!)=1, a contradiction.

Conjugacy classes are closed, so x^G is nowhere dense. In the special coset N_n x
from section 3, its complement is an open dense set consisting entirely of
torsion elements. Every nonempty open subset of that complement contains a
smaller open coset of finite exponent: choose a compact open coset within it
and apply Baire to its cover by the closed sets T_m. This localized bounded-
exponent conclusion still leaves the non-torsion class itself untouched.

Thus a possible route to the full conjecture is the following unproved local
assertion: no countably based profinite group can have an open coset containing
infinite-order elements, all of which belong to one global conjugacy class.
The present work does not establish that assertion. Dense torsion in the
remaining part of the coset does not imply that the exceptional class is torsion.

## Final scope after five attempts

Established: countably based reduction; the procyclic generator-fusion formula;
the open-normalizer obstruction; the soluble-by-torsion restricted theorem;
the explicit failure of affine counterexamples; and the local isolated-class
reduction above. Ten finite affine controls pass. None is a proof or refutation
for unrestricted profinite groups. No general resolution or novelty is claimed.
