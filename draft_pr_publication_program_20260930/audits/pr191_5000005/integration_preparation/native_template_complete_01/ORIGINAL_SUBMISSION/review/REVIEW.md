# Independent review of the signed type rule, 5000005

**Verdict: PASS_COMPLETE_SIGNED_TYPE_RULE. No mandatory mathematical correction.**

The frozen candidate establishes Fuchs's Conjecture 2.6, with the complete
source's segment-parity convention, and also establishes existence of the
first-vertex trajectories in the asserted parallel directions. This is a
separate adversarial AI review, not human peer review or certification of
historical priority. The neighboring length-ratio result in PR152 is not being
used as a proof of this theorem.

Reviewed 2026-10-01. The reviewed `CANDIDATE.md` SHA-256 is
`6d406380552758f7b4292759d62c12cbf2fe7f4c03e358086d6fac938ed10260`.
The author's checker and receipt hashes are respectively
`14f5b3d8e69fccee88a933413da13f9b97dd400f986fe52194c9396f8b750669` and
`9b79444776c09d7d5ae97fcb0bba3568d0d193982276308cffaf41499512645c`.

## 1. Exact target and source convention

I read the relevant portions of the complete
[Fuchs publisher PDF](https://amj.math.stonybrook.edu/pdf-Springer-final/020-0170.pdf),
including rendered pp. 502–503. The source selects the sum relation for an odd
number of segments and the difference relation for an even number before
Definition 2.1. Erasing that selector produces ambiguous numerical branches;
retaining it agrees with the direct-chord labels. The candidate does retain it.
The imported shorthand about A0 is therefore not a replacement for the full
definition. The actual target is Conjecture 2.6 on p. 511, including the even-l
restriction for even n, rather than Conjecture 2.7 on p. 512.

The source's two sides carry the congruent representatives 0 and n-2. I checked
them explicitly, permitting k=n-2 when transcribing the printed branches, then
reducing modulo n-2. No side is lost by an interior-only angle test. For the
hexagon, the explicit p. 506 residue classification, rather than inconsistent
nearby labels in the later prose, supplies the arithmetic check.

## 2. Surface model and common coordinates

The two-copy surface is correct. Reflection of a regular polygon across a side
is a translate of its half-turn, because reflection in the parallel line through
the center is the half-turn composed with a polygon symmetry. Thus the usual
billiard unfolding maps to the alternating P/Q translation surface. Conversely,
following a saddle connection through successive polygon copies and reversing
those reflections folds it back to the billiard path at its initial germ.
For the general n in the cusp argument, all polygon vertices are genuine cone
points. Affine maps preserve them and cannot introduce an intermediate vertex.

Side gluing advances corners `(P,j) -> (Q,j+1) -> (P,j+2)`. This gives the
stated odd single cone and even two cones, with the stated angles and genera.
For the even case the synchronized second base is Q0, not an independently
chosen zero. The physical-direction offset between the two bases is pi.
The lower physical side at `(copy,j)` is `copy*pi-2j*pi/n`, which agrees with
the cone formula in both parities.

The half-turn exchanging copies is compatible with the edge identifications.
It fixes exactly their n midpoints and, in the odd case, the single vertex
class. The count is 2g+2 for n>=5. Riemann–Hurwitz consequently identifies it
as the hyperelliptic involution. Conjugating it by an affine homeomorphism
still gives a map with derivative -I, which is holomorphic on the regular part
and extends across the zeros. Its quotient remains a sphere. Hyperelliptic
uniqueness in genus at least two gives commutation. The excluded torus cases
do not rely on that uniqueness assertion.

## 3. Lemma 1: the intrinsic index is the source type

The terminal P offset is `pi-beta`; the terminal Q offset is its complementary
corner angle `beta-2pi/n`, since the reflected copy reverses the local offset.
For `theta=alpha`, the initial germ has label zero.

There is a direct check of the needed divisibilities. At a P terminal vertex j,
its backward physical direction is `-2j*pi/n+pi-beta`; comparison with
`alpha+pi` yields `s+j=0 mod n`, with `s=n(alpha+beta)/(2pi)`. At a Q terminal
vertex it is `pi-2j*pi/n+beta-2pi/n`; comparison yields `s-j-1=0 mod n`, with
`s=n(beta-alpha)/(2pi)`. Substituting these in the two cone formulas gives
exactly `b=n-1-s` or `b=s-1` modulo N=n-2. No conjectural endpoint matching
is used at this step.

The independent script compares 15,719 feasible corner/angle tuples with the
full parity-selected inequalities, including sides. These are algebraic
controls, not a claim that every formal tuple is realized by a long billiard.
Bisector reflection on the same tuples gives the claimed sign reversal.

## 4. Lemma 2: why the shift is common to both endpoints and cones

An orientation-preserving linear derivative has an angular lift satisfying
`F(x+pi)=F(x)+pi`. On the odd surface there is one cone, so its sheet offset is
one constant for all germs. On the even surface, suppose cone 0 maps to cone h.
Its synchronized lift is `G(x)=F(x)-h*pi+2q*pi` modulo the full cone angle.

The key step is valid: commutation with the half-turn identifies the map on
cone 1 with this same G in synchronized coordinates. It does not merely show
that the two derivatives agree. It rules out an independent second-cone sheet
offset. Since every outgoing or backward germ has `phi-theta` an integral
multiple of pi, both signs and both cones receive `d=-h+2q` modulo N. Thus
`b-a` is invariant.

Labels are genuinely bijective for either directed physical direction. In the
odd case multiplication by 2 is invertible modulo odd N. In the even case
each cone supplies one parity class; together they supply every residue once.
The even case never divides by 2 modulo N.

## 5. Lemma 3 and the scope of cusp reduction

In a polygon symmetry direction, reflection in the perpendicular symmetry axis
sends any nonfixed vertex to a second vertex on the same line. Convexity makes
that chord the entire inward segment before another boundary encounter. At a
fixed vertex the line is supporting, hence has no inward corner germ.
Boundary side descriptions may occur twice, but describe one surface germ.
This accounts for every outgoing germ, not just a subset of convenient chords.

For a chord whose endpoint index difference is q modulo n, the two offsets
are `(n-1-q)*pi/n` and `(q-1)*pi/n`. Their sum is delta. Its physical line
direction `h*pi/n` gives `j+j'=n-1-h mod n`, leading to
`a+b=-h mod N`. I independently enumerated all directed chord descriptions for
n=3 through 32 and all 2n model directions: the resulting relation is a
bijection on all N labels, including agreement of duplicated boundary germs.

The imported classical facts have the precise needed scope.
[Finster v3](https://arxiv.org/abs/1005.4588v3), Sections 3.1–3.2 and Remarks
3.2/3.5, gives the lattice groups and odd/even cusp counts. Her p. 7 explicitly
identifies the even two-polygon cover's group with the opposite-side quotient's
group for n>=8; p. 20 states the two base-group cusp representatives. These are
not the additional cusps of her later covering family. I read and rendered that
base-cusp paragraph. The symmetry directions remain such after changing the
polygon's coordinate normalization.
[Boulanger–Lanneau–Massart](https://www.numdam.org/articles/10.5802/ahl.211/),
Section 1.4, states the general saddle-connection/cusp correspondence. Its own
odd one-cusp family is not being used to assert one cusp for even n.

The original Veech 1989 full text was not recovered in this review. The exact
consequences are read in the complete later primary sources and explicitly
credited to Veech. This is an acknowledged imported-theorem dependency, not a
new proof or a numerical substitute for it.

## 6. Lemma 4 and the signed transformation rule

Cusp reduction supplies one affine automorphism for the whole direction. It
sends every germ to a model germ, so inverse images of the finite model chords
prove existence and the first-vertex property for all original germs. If both
labels increase by d under that map, model matching gives
`a+b=-h-2d`. This proves the asserted endpoint reflection with one common C.

For the original trajectory, `a=0` and `b=k`, hence `C=k`. Apply the surface
rotation through `-ell*pi/n` to the proposed new initial germ. On the odd
surface it exchanges polygon copies when ell is odd; on the even surface only
even ell is needed. Both are genuine gluing-compatible isometries.

The rotated initial label satisfies the exact integer equality
`n*a=t*N+ell`. Reducing with `n=N+2` gives `2a=ell mod N`. Endpoint reflection
then gives intrinsic index `k-2a=k-ell`, and affine invariance identifies it
with the source type of the new trajectory. The integer equality, not modular
division, is what makes this work for even N.

For the negative sign, bisector reflection sends the source angles to
`delta-alpha` and `pi+2pi/n-beta`. The odd parameter changes to `n-s` and the
even parameter to `2-s`, so both types change from k to -k. Composing this with
the positive shift `N-ell` gives `-k-ell`; that shift remains even when required.
The angle interval condition is preserved by this composition. There is no
assumption that an arbitrary shifted ray hits a vertex: that existence was
already proved by Lemma 4 and the isometry.

## 7. Elementary cases and reproducibility

The triangular and square lattice arguments handle n=3,4 separately. For n=6,
the first vertex must be recomputed after a direction change. In primitive
triangular coordinates its multiplier is 1 for `p+q=0,1 mod 3`, and 2 for
`p+q=2 mod 3`. Evaluating the source's type on that first endpoint verifies
`K(p-q,p)=K(p,q)-2` and `K(q,p)=-K(p,q)` modulo 4. No transformation of the
missing honeycomb residue is falsely assumed to preserve reachable points.

The author's **3,276,822** assertions replay exactly, including the receipt
hash. The independent standard-library script passes **441,920** assertions:

- 15,719 full-source type and reflected-type angle cases
- 21,820 directed model chord descriptions and complete label exhaustion
- common-shift checks on both directions/cones with a nonlinear, rational,
  increasing antipodal angular lift and multiple sheet offsets
- actual vertex-rotation alignment and the twice-label congruence, including
  negative shifts and even moduli
- first-vertex and all twelve triangular dihedral operations on 1,024 primitive
  lattice vectors

The independent checker imports no author checker. Re-running it gives the
same JSON receipt. These controls do not prove the classical group theorems,
hyperelliptic uniqueness, or the unbounded-n conclusion. The geometric proof
above and its stated dependencies justify those steps.

## 8. Verdict limits

No substantive gap was found in the new common-label, model-reflection, or
transport steps. The proof answers the full signed rule of Conjecture 2.6,
under the source conventions it states explicitly. It does not establish
neighboring conjectures, a new classical cusp theorem, historical priority, or
human-peer-review acceptance. Keep the reconstruction provenance and source
access qualifications intact. Review and packaging do not consume another
substantive author research turn.
