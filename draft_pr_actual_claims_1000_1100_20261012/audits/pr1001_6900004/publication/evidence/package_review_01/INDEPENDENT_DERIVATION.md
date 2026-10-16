# Independent derivation before comparison with previous verdicts

Timestamp UTC: 2026-10-13T04:01:38.234896+00:00

I first read only research_note.tex, the current README/SUPPLEMENT, metadata,
runner and manifest. I have not yet read the imported previous mathematical or
priority reports or their verdict JSON. The present derivation is independent
of those reports. The supplement did expose mechanisms and prior-credit claims,
so this is an adversarial package review, not a blind rediscovery.

For a present edge e=ij, existence of a stress whose sign pattern is positive
at e and zero elsewhere is equivalent to p_i=p_j: the two equilibrium rows
are opposite endpoint differences. A coordinate-sign-preserving bijection
preserves existence of that pattern in both directions. Membership of the
collision diagonal is constant on an equivalence class, hence on every
connected component of the class.

For a missing pair ij, choose scalar coordinates x_i=t, x_j=0 and distinct
x_k=k+1>=2 for all other vertices, t in [-1/2,1/2]. All actual edge differences
remain nonzero. For collinear p_k=x_k a with a!=0, the vector equilibrium is
equivalent to B D_t w=0. With the stated incidence orientation, initial and
final rows are respectively +(x_v-x_u) and -(x_v-x_u). The map
T_t=D_t^{-1}D_0 and its inverse take kernels onto kernels, because
B D_t T_t=B D_0. Its entries are positive ratios, because each edge difference
stays nonzero with constant sign. This preserves positive, negative and zero
coordinates. The continuous configuration path is contained in the equivalence
class of P(0). The image of an interval is connected in the class's subspace
topology and therefore lies inside one connected component. P(0) belongs to
Delta_ij, while P(1/4) does not. Thus the diagonal is not a union of strata.

This argument handles disconnected graphs and deficient affine span. For an
empty edge set the kernel is the singleton vector space and the same path
works. For n=2 the only nonedge graph is empty; n=1 has one simple graph. The
argument requires d>=1, simple graphs and the full Cartesian domain; it does
not work after deleting collisions. It proves literal equality of partitions
of the same labelled base, not reconstruction from an unlabelled poset of
strata or arbitrary ambient equivalence.

For a forest, repeatedly eliminate a leaf. A noncollapsed incident edge has
zero weight by the leaf equation. A collapsed edge contributes zero force
and has a free coordinate, independent of all other equations. Removing that
leaf reduces the argument. Therefore the stress space is precisely the
coordinate subspace indexed by collapsed edges. It is sign equivalent to
another forest fibre (under a fixed edge correspondence) if and only if its
collapsed edge set corresponds. For the path/star map, the three oriented
edge differences match. The inverse displayed in SUPPLEMENT is correct:
p3=q2+q3-q1, p4=q2+q3+q4-2q1. It is a global linear homeomorphism for any d.
A homeomorphism taking complete equivalence classes bijectively also takes
their connected components bijectively. The trees are nonisomorphic, since
maximal degrees are 2 and 3. This confirms the stated scope counterexample.

No proof defect is found in this independent derivation. Next checks are
original-source fidelity, prior credit, execution and exact package content.
