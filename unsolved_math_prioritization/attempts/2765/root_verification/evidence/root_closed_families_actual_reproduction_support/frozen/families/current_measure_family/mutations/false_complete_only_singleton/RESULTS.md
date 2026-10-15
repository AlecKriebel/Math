# Length-function fibers of geodesic currents: scope and reductions

**Status: source-scope hold; the substantive closed-surface problem remains unresolved.**
The statements below are scoped results and classical reductions, not a new
solution of the general closed-surface problem. Independent scoped review passed; see review/REVIEW.md.
AI-assisted and unrefereed; no historical-priority claim.

Target: **2765 / KP-2.17**, K3, Problem 2.17, printed pp. 98–99 [1].

## 1. Conventions and the exact closed-surface target

For Sections 2–4, S is a closed connected oriented surface of genus at least
two. A geodesic current is a nonnegative, invariant Radon measure on the
space of unoriented complete geodesics of the universal cover. A closed
curve denotes its counting current, with traversal multiplicity when
applicable. Signed measures are not allowed.

Let L_X be the Liouville current of a marked hyperbolic metric X. With the
standard intersection form i, the length function of a current μ is

\[
 \ell_X(\mu)=i(\mu,L_X).
\]

For an arbitrary closed geodesic γ, the fiber in question is

\[
 F_\gamma=\{\mu\ge0:
   i(\mu,L_X)=i(\gamma,L_X)\ \text{for every }X\in\mathcal T(S)\}.
 \tag{1.1}
\]

The original target asks whether every point in this fiber is a **finite
convex combination** of closed-curve currents. Neither testing finitely
many metrics nor replacing γ by a simple curve answers that question.
Even finite atomicity alone would require attention to the stated convex
normalization; it should not silently be replaced by an arbitrary positive
linear-combination conclusion.

Length-twin curves already show that the map μ↦(ell_X(μ))_X is not
injective. The source itself records their permitted convex combinations.
It does not say every summand of any possible decomposition must itself
be a length twin. The stronger assertion that F_γ equals the convex hull
of the length twins is therefore not assumed here.

## 2. What metric equality really gives at the Thurston boundary

**Proposition 1.** If μ∈F_γ, then

\[
 i(\mu,\lambda)=i(\gamma,\lambda)
 \qquad\text{for every measured lamination }\lambda.
 \tag{2.1}
\]

For any nonzero λ, Bonahon's current description of Thurston's boundary
supplies positive numbers a_n and hyperbolic metrics X_n with
`a_n L_{X_n} → λ` in the current topology. Multiply the equality in
(1.1) by a_n and use continuity of the intersection form. The case λ=0
is immediate. This proves (2.1).

For **two closed curves**, Leininger [2, Theorem 1.4 and Section 5] proves
that hyperbolic-length equivalence implies simple-intersection equivalence,
but constructs filling pairs showing that the converse fails. His theorem
also relates hyperbolic equivalence to trace equivalence; that relation is
a theorem about curves, not a definition of traces for arbitrary currents.
Jyothis [3, Theorem 1.3 and Remark 1.4] gives further examples with the
same simple-intersection data and self-intersection number which are not
hyperbolically equivalent. Thus replacing all Liouville tests by (2.1)
loses information and cannot complete the argument.

## 3. The simple reference case is rigid

**Proposition 2.** If γ is a positive integer multiple of an essential
simple closed curve α and μ∈F_γ, then μ=γ as currents.

Here is a support proof, included to delimit the easy case. Cut S along
α. Every component has positive genus: a separating essential curve in a
closed surface cuts off positive genus on both sides, and a nonseparating
cut lowers genus by one and creates two boundary circles. In each cut
component choose finitely many simple closed curves filling it relative
to its boundary, meaning that the complementary regions are disks and
boundary-parallel annuli. Such a system is obtained from an interior pants
decomposition by adding simple dual curves across its interior cuffs.
The curves can all be chosen disjoint from α in S. Let A be their union
together with α, realized geodesically in a fixed hyperbolic metric.

Equation (2.1) gives i(μ,δ)=0 for every selected curve δ, including α.
Positivity of the current implies that no geodesic in its support crosses
any lift of δ transversely: a transverse crossing has a small open box of
nearby crossing geodesics, and positive μ-mass in that box would give a
positive contribution to the intersection number.

The relative filling system now forces every supported geodesic to be a
lift of α. Indeed, a complete hyperbolic geodesic cannot remain in a lift
of a compact disk. A lift of a compact boundary-parallel annulus lies in
a bounded-width neighborhood of the corresponding α-axis; a complete
geodesic contained there has the same two ideal endpoints and hence is
that axis. A geodesic following one of the selected interior curves meets
another member of the filling system transversely, so is excluded as well.

The measure μ is consequently supported on the discrete orbit of lifts
of α. Invariance gives one common weight, so μ=bα for some b≥0. Evaluating
at one hyperbolic metric, where α has positive length, gives b equal to the
multiplicity in γ. Hence μ=γ.

This proposition does not cover an arbitrary self-intersecting γ. In
particular, if γ fills S, there is no collection of simple curves disjoint
from γ with which to repeat the zero-intersection support argument.

## 4. Compactness is not the missing atomicity theorem

**Proposition 3.** For closed S, F_γ is a nonempty compact convex set.

Fix X_0. Every μ in the fiber has the same positive X_0-length as γ.
The set of currents with this fixed length is compact: equivalently one
uses flow-invariant, flip-invariant finite measures of fixed mass on the
compact unit tangent bundle, or the standard Liouville-normalized current
compactness theorem [4, Proposition 2.6(1)]. Each condition in (1.1) is
closed and affine by continuity and bilinearity of i. Their intersection
is therefore compact and convex, and contains γ.

This conclusion does not say its extreme points are closed curves.
Krein–Milman alone supplies no such classification. Nor would a limiting
approximation by weighted curves prove finite convex representability.
The unproved step is precisely exclusion of non-atomic, or more general
non-finitely-supported, positive currents in this fiber for a
self-intersecting reference curve. The argument above stops there.

## 5. A counterexample under the complete finite-area punctured convention

The K3 chapter's general surface conventions include finite-type
punctured surfaces, while Problem 2.17 itself does not explicitly say
closed. Current conventions on noncompact surfaces require care.
The following observation is a **scoped counterexample**, not a solution
of the substantive closed genus-at-least-two formulation.

**Proposition 4.** Let S be the thrice-punctured sphere, let metrics mean
complete finite-area hyperbolic metrics, and let currents be Radon
currents on that cusped surface, allowing its Liouville current. Then
there is a non-atomic current with the same length function as a closed
geodesic; it is not a finite convex combination of closed curves.

There is only one marked complete finite-area hyperbolic structure X on
S. This follows, for example, by the classification of the three marked
points on the Riemann sphere under Möbius maps and uniformization;
equivalently, an ideal hyperbolic pair of pants has no length or twist
parameters. All permutations of the three cusps are realized by its
isometries, so allowing an unlabelled marking does not introduce a metric
parameter.

Let L be its Liouville current. It is nonzero and non-atomic, since on
boundary-pair charts it is a smooth measure with density proportional
to `da db / |a-b|²`. It has finite positive X-length. One direct way to
see finiteness is to use its associated invariant measure on T¹X: this
is a constant multiple of Liouville volume, whose total mass is
`2π area(X)=4π²` in the usual oriented-bundle normalization [5, Section
3.1]. The current/flow correspondence normalizes the length of a closed
counting current to its closed-orbit length; the harmless universal
normalization factor does not affect finiteness or the scaling below.
Equivalently, i(L,L) is a finite positive constant proportional to area(X).

Choose a nonperipheral closed geodesic γ and put

\[
 c=\frac{\ell_X(\gamma)}{\ell_X(L)}L.
 \tag{5.1}
\]

The scalar is finite and strictly positive. Since T(S) has just the point
X, (5.1) is equality of the entire metric-length functions, not equality
at a few sampled metrics. A concrete standard model is H²/Γ(2): with

\[
 A=\begin{pmatrix}1&2\\0&1\end{pmatrix},\qquad
 B=\begin{pmatrix}1&0\\2&1\end{pmatrix},
\]

the element AB has trace 6 and gives a closed geodesic of length
`2 arcosh(3)>0`.

Every finite combination of closed counting currents is atomic on a
countable union of lift orbits. The current c is a nonzero non-atomic
measure, so no such combination represents it. This proves the scoped
counterexample.

There is an essential convention boundary. A compact hyperbolic pair of
pants whose three geodesic-boundary lengths are allowed to vary has a
three-parameter metric space, not the singleton used here. Moreover,
working with currents on a compact core with geodesic boundary instead
of currents on its cusped interior changes the current space. Trin
[5, Proposition 2.2] explains why the cusped metric's length function is
not represented by a Liouville current in that compact-core space.
Neither variant is silently identified with Proposition 4.

## 6. Disposition

The broad finite-area punctured reading needs an explicit low-complexity
exclusion or a different current convention. For the closed-surface
version, we have only classical boundary-data reductions, the simple
reference case, and a compact-fiber formulation. No finite-support or
convex-decomposition theorem for an arbitrary closed geodesic was proved.
Retain **unsolved / source-scope hold**, with no novel-solution credit.

## References

1. R. İ. Baykur, R. C. Kirby, D. Ruberman, *K3: A New Problem List in
   Low-Dimensional Topology*, author-hosted preliminary book, Chapter 2
   conventions p. 84 and Problem 2.17 pp. 98–99. Proposed/scribed by
   T. Aougab and P. Patel.
   https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf
2. C. J. Leininger, *Equivalent curves in surfaces*, Geometriae Dedicata
   102 (2003), 151–177, Theorems 1.4, 5.1–5.2 and Corollary 5.4.
   https://arxiv.org/abs/math/0302280
3. M. Jyothis, *Towards Ivanov's meta-conjecture for geodesic currents*,
   arXiv:2309.14532v3, 19 February 2025, Theorem 1.3 and Remark 1.4.
   https://arxiv.org/abs/2309.14532v3
4. M. Burger, A. Iozzi, A. Parreau, M. B. Pozzetti, *Currents, systoles,
   and compactifications of character varieties*, Proc. London Math.
   Soc. 123 (2021), 565–596, especially Section 2 and Proposition 2.6.
   https://people.math.ethz.ch/~burger/pub/2021_Currents_systoles.pdf
5. M. Trin, *Thurston's compactification via geodesic currents: the case
   of non-compact finite area surfaces*, Ann. Inst. Fourier 74 (2024),
   2461–2486; arXiv:2208.10763, Sections 2 and 3.1.
   https://aif.centre-mersenne.org/item/10.5802/aif.3625.pdf


The singleton argument applies to all complete hyperbolic metrics on the thrice-punctured topological surface, without finite area.
