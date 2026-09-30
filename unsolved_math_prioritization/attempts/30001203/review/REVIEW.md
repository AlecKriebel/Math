# Independent adversarial review: negatively curved observability metric

**Verdict: PASS_COMPLETE_COUNTEREXAMPLE.** The frozen construction meets
the original manifold hypotheses and disproves the asserted implication to
global observability. No mandatory mathematical correction was identified.
This is a separate AI review, not human peer review or a determination of
historical priority.

Reviewed on 2026-09-30 using GPT-6 Astra at xhigh effort. The exact reviewed
`COUNTEREXAMPLE.md` has SHA-256
`59f1adc87e67fc25dbeb9c753d940b36fb8450eb0f51f6027662a9a95f62bed0`.
The original reviewed bytes are preserved under `author_replay/`.

The publication snapshot `e22eb257358431f1c7e4dbdb2c8550c26972da1b24a573581aed8f84c14db0dd` is also covered. An exact byte comparison confirms that only the opening review-status sentence and link changed; every mathematical byte and the verifier remain unchanged. The updated receipt differs only in the artifact hash. This narrow follow-up was checked on 2026-09-30.

## 1. Original scope and the uniformity issue

Krener's full contribution on printed pp.674–675 of
[OWR 11/2009](https://ems.press/content/serial-article-files/46211) was
read and both pages were inspected visually. It explicitly describes
local state coordinates on an $n$-dimensional manifold and an output
in $\mathbb R^p$. Global observability is injectivity of the initial-state
to output-history map. The conjecture assumes that the exact local
observability Gramian, for some fixed positive observation time, is uniformly
positive definite and bounded, and that its metric is complete with uniformly
negative curvature.

There is no global Euclidean-chart assumption, simple-connectivity condition,
upper bound on output dimension, or requirement that the vector field be
nonzero. The related Krener–Ide paper's Euclidean calculations and examples
do not add hypotheses to the workshop's explicit manifold formulation.
The counterexample uses the exact differential Gramian, not the empirical
finite-difference approximation discussed later in that related paper.

The candidate addresses the coordinate meaning of uniform bounds correctly.
On a manifold a comparison of metric matrices must refer to specified
coordinates or a background metric. Compactness gives positive lower and
finite upper bounds relative to any fixed smooth background metric.
Moreover the exhibited finite atlas has the same explicit coefficient
bounds in every chart. These meet both ordinary interpretations without
demanding invariant matrix eigenvalues under arbitrary coordinate rescaling.
Such a latter demand would fail even for a Euclidean metric and is not a
coherent extra hypothesis of the source.

## 2. Construction and imported theorems

A regular hyperbolic octagon with the standard genus-two side pairing and
angles $\pi/4$ gives a closed smooth hyperbolic surface. The eight corners
produce total angle $2\pi$, so no cone point is present. The standard
construction is also described in
[Hitchman's author-hosted account, Example 7.7.11](https://mphitchman.com/geometry/section7-7.html).

The homomorphism from the genus-two surface group to $\mathbb Z/2$
sends its relator to zero and is onto because $a_1$ has nonzero image.
Its kernel has index two. The hypotheses of
[Hatcher, Proposition 1.36](https://pi.math.cornell.edu/~hatcher/AT/AT.pdf)
hold for a surface and realize the connected cover. The smooth structure
is transported by covering charts. A finite cover of this compact base is
compact and has no boundary; orientation also lifts. The Euler characteristic
calculation $2(-2)=-4$ correctly gives genus three.

[Nash's original compact embedding theorem](https://sites.math.rutgers.edu/~feehan/teaching/math866/nash.pdf),
Theorem 2 on printed p.59, was inspected visually. It permits $k=\infty$
and gives ambient dimension $n(3n+11)/2$, hence 17 for a surface. Thus the
map $e$ is a smooth isometric **embedding**, with both an injective
differential and global injectivity. A $C^1$ embedding would not provide
the asserted smooth setup, but that weaker theorem is not being used.
The review imports the established smooth theorem; it does not reconstruct
Nash's iteration or compute an embedding numerically.

## 3. Exact observed system and Gramian

For $f=0$, the flow is the identity for all real times and the variational
flow is the identity on each tangent space. Every trajectory remains in any
chart containing its initial point, so there is no chart-switching term to
overlook. With $h=e\circ\pi$, the derivative is $de\circ d\pi$, and
the actual Gramian is

\[
P_T(v,w)=\int_0^T\langle dh(v),dh(w)\rangle\,dt
=T\langle de(d\pi v),de(d\pi w)\rangle
=T\pi^*g(v,w).
\]

In particular $P_1=\widetilde g$ exactly. This establishes the required
connection between the observed dynamics and the metric, rather than merely
choosing a negatively curved metric unrelated to an observation map.
The ordinary Euclidean output inner product used by Nash is exactly the
one in the Gramian. The source's output-scaling remark imposes no contrary
restriction; if identity noise covariance is specified, these Euclidean
coordinates already use that normalization.

The covering is a local diffeomorphism and $e$ is an embedding, so
$h$ is locally injective. Its derivative has rank two at every point.
The output history is the constant function with value $h(x)$, giving
local observability on every interval of positive length.

On the other hand, the two lifts of every base point have identical output
values and identical histories for all real times. Since $e$ is globally
injective, there are exactly two states for each attained history. The
counterexample does not rely on a short observation window or a loss of
differential rank.

## 4. Global metric hypotheses

Pullback by the covering makes it a local isometry. Consequently the
Gaussian curvature is $-1$; in dimension two this is also sectional
curvature. The resulting smooth Riemannian metric is complete because its
state manifold is compact. This is geodesic completeness of the Gramian
metric, not merely existence of the system's constant trajectories.

For a fixed background metric $q$, the $q$-unit tangent bundle is compact.
The strictly positive continuous function $\widetilde g(v,v)$ on that
bundle has a positive minimum and finite maximum, establishing $cq\le P_1\le Cq$.

For the coordinate version, each point has a centered Poincaré-disk chart
with sufficiently small image, contained in the Euclidean disk of radius
$1/2$. These neighborhoods cover the manifold; compactness supplies a
finite subcover. The local formula gives

\[
P_1=\frac{4}{(1-r^2)^2}I,
\qquad 4I\le P_1\le\frac{64}{9}I.
\]

This argument does not require all chart radii to be equal. It also does
not assert that a single global Euclidean chart exists. As a check for
the whole interval $0\le s=r^2\le1/4$, the two differences factor as

\[
\frac4{(1-s)^2}-4=\frac{4s(2-s)}{(1-s)^2}\ge0,
\quad
\frac{64}9-\frac4{(1-s)^2}
=\frac{4(1-4s)(7-4s)}{9(1-s)^2}\ge0.
\]

For every other fixed $T>0$, scaling the metric by $T$ preserves
completeness and gives curvature $-1/T$. This is still uniformly negative
over all states. The source asks about one fixed observation time; it does
not ask for a curvature bound independent of every possible $T$.

## 5. Independent verification and recommendation

All five hashes in the submitted freeze manifest match. The author's
873 exact assertions reproduce `author_replay/verification.json` byte for
byte. The independent checker imports no author code and verifies the
curvature via the conformal Laplacian formula, the whole-interval metric
bounds, exact Möbius chart isometries, surface-group monodromy as permutations,
and the all-time Gramian identity and its nonlinear-coordinate pullback.
Its **108 exact assertions pass**. Finite checks supplement the source
theorems and the argument above; they do not establish global embedding or
cover existence by experiment.

The full literal manifold conjecture is refuted by the construction, with no
identified mathematical gap. Record 30001204 refers to the same original
question and should remain a duplicate rather than a second result.
The bounded primary-source search did not locate an earlier explicit
resolution, but that is not a historical-priority certificate.

Recommended publication language is a complete counterexample candidate
that passed a separate adversarial AI review, with priority unconfirmed and
no human peer review. Retain the exact manifold scope, the fixed-atlas and
background-metric interpretation of uniformity, the smooth Nash theorem,
and attribution of the classical ingredients. No mandatory change to the
frozen mathematical artifact is required.

Reproduce with `python author_replay/verify.py` and
`python independent_checks.py`, comparing stdout with the respective JSON
receipts. Keep `author_replay/COUNTEREXAMPLE.md`, which is a required hash
dependency. Source PDFs and rendered third-party pages are not part of the
public review bundle.
