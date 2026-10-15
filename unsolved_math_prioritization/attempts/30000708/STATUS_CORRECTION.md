# Cramér–Wold uniqueness with an origin singularity: credited source correction

**30000708 / OWR-1461-003. Proposed disposition: already_solved, 0/5 substantive author turns.** This is validation of established results, not a new proof or a classification of every possible injective measure class.

## 1. The original source already reports answers

The imported statement asks under which conditions halfspace values determine
signed measures that can have infinite mass near the origin. In the full
primary report, Lindskog's contribution, joint with Boman, is titled
*Cramér–Wold theorems for measures with a singularity*, OWR 10/2007,
printed pp.582–583. The question is introductory motivation. The same
paragraph immediately reports uniqueness with sufficiently rapid decay at
infinity or suitable cone support, and failure without an added assumption.
It is not presented there as an unanswered request for a necessary-and-
sufficient classification of all measure spaces.

The complete follow-up is Jan Boman and Filip Lindskog, *Support Theorems
for the Radon Transform and Cramér–Wold Theorems*, Journal of Theoretical
Probability 22 (2009), 683–710, DOI 10.1007/s10959-008-0151-0.
The publisher records online publication on 18 March 2008. Its full
arXiv:0802.4373v1 manuscript gives precise signed-measure formulations,
proofs, and counterexamples. We use that explicitly identified full-text
version for theorem numbering; publisher access available here is metadata
and abstract, not the subscription full PDF.

The imported 2026 triage statement that this broad source question remains
unresolved omits the source's own answer and the published follow-up. The
correction below credits those authors and their support-theorem inputs.
It does not claim a new result or a universal iff characterization.

## 2. Measure class and what the data mean

Write X=R^d minus {0}. The paper uses signed measures locally on X:
equivalently, order-zero continuous linear functionals on compactly
supported continuous test functions in X, or signed Radon measures with
finite total variation on each compact subset of X. Both positive and
negative variation can be infinite near the deleted origin. No undefined
infinity-minus-infinity value on the whole space is used.

For the finite-away-from-origin class, require

    |mu|({x:|x|>epsilon})<infinity for every epsilon>0.       (1)

This is **total variation**, not just cancellation in a signed integral.
It is stronger than local finiteness on X, because it controls the tail
at infinity too. The cone theorem below explicitly assumes (1); the
other two stated alternatives imply it.

For every unit vector omega and p<0, let

    H_(omega,p)={x:x·omega<p}.

Its closure avoids the origin, so (1) makes its measure absolutely
well-defined. These are precisely the open halfspaces whose closures
avoid the origin, with the source's orientation convention. Halfspaces
through or containing the origin are not data in this singular setting.
Nor is an unrestricted full one-dimensional pushforward through zero
silently assumed to be a finite measure.

Uniqueness means equality as measures **on X**. An atom or any other
distribution supported at the deleted origin is not determined by these
halfspaces and is not included in the conclusion.

## 3. Established sufficient uniqueness classes

Suppose mu and nu have the same values on all H_(omega,p), p<0.
Each of the following, separately, is a published sufficient condition
for mu=nu on X. The zero-data theorems are applied to their difference.
The paper actually permits almost-everywhere equality of halfspace data;
the all-halfspace version stated here is an immediate weaker corollary.

### A. Rapid total-variation decay at infinity

Both measures are locally finite on X and, for every m>0,

    |mu|({|x|>r})=O(r^(−m)),
    |nu|({|x|>r})=O(r^(−m)) as r→infinity.                    (2)

The constants can depend on m. This is the tail formulation of Definition
1 on manuscript p.7, equivalent to the stated cutoff total-variation
norm condition. It implies (1) by adding compact annuli. It imposes no
finite total mass or moment bound near zero.

**Source:** Theorem 2, p.12, using the exterior Radon support Theorem B,
pp.8–9. The difference remains rapidly decaying. No positivity is needed.

### B. Support in a common strict cone, with finite variation away from zero

Both measures satisfy (1) and are supported in one fixed closed cone Q
such that, for some unit vector v,

    Q minus {0} is contained in {x:x·v>0}.                   (3)

The cone must be the same admissible cone for the comparison, so their
difference retains the support condition. A generic closed halfspace
with its whole boundary plane is not enough. The source's condition
(3), rather than an ambiguous informal use of “proper cone,” is what
is asserted here. No rapid decay or near-zero moment condition is added.

**Source:** Theorem 4, manuscript pp.14–15, using Theorem D, pp.10–11.
This result applies to signed measures, not only nonnegative ones.

### C. A fixed nonintegral homogeneous degree

For a fixed noninteger alpha<−d, both measures are homogeneous with
the paper's density-degree convention:

    <mu,phi(·/r)>=r^(d+alpha)<mu,phi>, r>0,                 (4)

and similarly for nu, for tests compactly supported in X. For a density,
this means f(rx)=r^alpha f(x); the scaling degree of set masses is
d+alpha, not alpha. Local finite variation on annuli and alpha<−d
give (1) by a geometric series.

**Source:** Theorem 3a, p.12, using Theorem C, p.9. The degree must be
fixed for the comparison and nonintegral in this stated theorem.
The neighboring Theorem 3b assumes homogeneity only of the halfspace
data, but explicitly requires the unknown measure to be nonnegative.
That stronger-looking conclusion is not transferred to arbitrary signed
measures. Further parity refinements in the paper are not needed here.

These alternatives are not presented as jointly necessary conditions
for every measure class. They are the concrete established answers
matching the motivating question and the source's reported results.

## 4. Why an unrestricted uniqueness assertion is false

Section 5 of the full manuscript, pp.20–21, gives the classical
complex-power counterexamples and credits earlier Radon literature.
A real signed example in dimension two, with absolutely finite mass
on all sets away from zero, is

    f(x,y)=Re (x+iy)^(−3)
          =(x³−3xy²)/(x²+y²)³,
    dmu=f(x,y) dx dy on R² minus {0}.                       (5)

This is the paper's z^(−k) family at k=3, taking a real part. It is
nonzero, locally integrable away from zero, homogeneous of degree −3,
and bounded in absolute value by |(x,y)|^(−3). Thus its total variation
outside radius epsilon is finite, while it is infinite near zero.
The exponent is integral, so it does not meet alternative C.

For clarity, the source's elementary verification is reproducible.
On a line avoiding zero, write z=e^(i theta)(p+it), p≠0. Its complex
line integral vanishes, because

    d/dt [(i/2)(p+it)^(−2)]=(p+it)^(−3)

and the primitive tends to zero at both infinities. The constant rotation
factor does not affect zero. Since (5) is absolutely integrable over
each avoiding-origin halfspace, Fubini then gives mu(H)=0 for every
such halfspace. Taking real parts preserves the conclusion. Thus mu
and the zero measure have identical data but differ on the punctured
plane. This verifies a published counterexample, not a new discovery.

In particular, local finiteness and finite total variation outside
every origin neighborhood alone do not imply injectivity. A density
bounded by a fixed polynomial tail is not the same as rapid decay to
every order. The paper's higher complex powers provide the corresponding
warning for arbitrarily high but fixed polynomial decay orders.

## 5. Bibliographic and status conclusion

The exact original source is answered by established signed-measure
theorems and explicit failures outside their hypotheses. The original
OWR paragraph already reports this state of affairs. The appropriate
campaign disposition is **already_solved, 0/5**: source verification
does not consume an original proof turn.

The full arXiv v1 has a later PDF compilation date, while the arXiv
version record is 29 February 2008; publication metadata independently
identifies the 2008 online/2009 issue dates. No theorem numbering is
silently attributed to an unread final PDF. The exact source bytes,
access receipts and visual checks are recorded separately.

### Primary references

- Lindskog, joint with Boman, OWR 10/2007, pp.582–583:
  https://ems.press/content/serial-article-files/46092?nt=1
- Full manuscript, Boman–Lindskog, arXiv:0802.4373v1:
  https://arxiv.org/pdf/0802.4373v1
- Publisher metadata and abstract:
  https://link.springer.com/article/10.1007/s10959-008-0151-0
