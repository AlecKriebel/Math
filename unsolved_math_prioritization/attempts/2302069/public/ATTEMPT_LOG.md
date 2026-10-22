# Five substantive approaches

Problem 2302069 / AMR-022-2069. Investigation dated 2026-10-04 UTC.
The entries count mathematical approaches, not retrieval calls. The complete
write-ups are consolidated in `PROOF.md`. Source triage does not claim a
sixth attempt. Completion estimates below are rough progress estimates toward
the exact original goal, not calibrated probabilities or proof guarantees.

## 1. Radial integration, Poisson majorants, and good dilation radii

Recorded 07:44–07:46 UTC. Completion estimate: 5%.

Derived a fixed-dilation comparison and proved the good-radius lemma from
lower order. It gives L(f) ≤ inf_{k>1} k^λ(k+1)/(k−1), with an explicit
minimizer for λ>0. The argument recovers the lower-order-zero case and uses
no characteristic-comparison theorem beyond the displayed Poisson estimate.
The derivative has the same lower order, proved using Cauchy's estimate and
radial integration. All additive logarithmic errors are controlled using
transcendence, not silently discarded for polynomials.

Outcome: rigorous comparison. Gap: the bound remains strictly above 1 at
every positive λ. The quantifiers do not permit taking λ→0 for a fixed f.

## 2. Canonical products and angular loss

Recorded 07:43–07:47 UTC. Completion estimate: 8%.

Used p-subadditivity, a uniform angular kernel bound, and summability of the
zeros to prove m(r,f′/f)→0 for canonical products with exponent of convergence
below 1. Standard Hadamard factorization applies this to every entire
function of order below 1. Decomposed the characteristic difference exactly
into nonnegative loss and gain terms. The gain tends to zero; the required
liminf comparison is equivalent to vanishing relative loss on a subsequence.

Outcome: rigorous estimate and exact gap. This is not a solution by
reformulation: no bound on the normalized loss was obtained for general
complex zero geometry. The forward estimate holds even in a range containing
known counterexamples, so it cannot by itself prove the target.

## 3. Real-zero geometry

Recorded 07:42–07:46 UTC. Completion estimate: 12%.

The imaginary parts of all terms of the logarithmic derivative have the same
sign when the zeros are real. One fixed zero gives an explicit lower bound
for its modulus off the real axis, yielding m(r,f/f′)≤log r+log2+o(1).
Combined with approach 2, this proves convergence of the characteristic ratio
to 1 for the real-zero subclass of order below 1. Zeros at 0, repeated zeros,
and the measure-zero real-axis intersections are handled explicitly.

Outcome: complete subclass theorem. Gap: arbitrary noncollinear zeros lose
the common-sign estimate. No claim is made that this subclass exhausts the
small-order functions.

## 4. Test the minimum-modulus inference

Recorded 07:46–07:49 UTC. Completion estimate: 12%.

Constructed F_N(z)=exp(cN)((1−z)^N−1), for N≡3 modulo 6. A geometric argument
proves min_{|z|=1}|F_N|≥exp(cN)/4 despite F_N(0)=0. Direct characteristic
limits prove a strictly positive ratio gap on that same circle. Dominated
convergence is justified with uniform normalized bounds.

Outcome: a rigorous obstruction to a local inference, even after fixing the
value at 0. It is not a counterexample to the original problem: N varies,
the radius is fixed, and every F_N is a polynomial. A minimum-modulus route
still needs global information about one fixed transcendental function
across unbounded radii.

## 5. Try to lower the order of known counterexamples

Recorded 07:46–07:50 UTC. Completion estimate: 12%.

Proved exact characteristic identities for g(z)=f(z^q), including the
negligible derivative multiplier. This preserves L but multiplies order by
q, so it moves in the wrong direction. A single-valued entire reverse
substitution requires root-of-unity invariance, which is not available here.
Rotation averaging does not preserve a characteristic lower bound and can
annihilate an entire function. Examining the sector-approximation mechanism
also gives no construction at or below its existing order boundary.

Outcome: rigorous invariance and an identified construction barrier. Gap:
no small-order counterexample family and no positive universal threshold.

## Final checkpoint

07:54 UTC. Five approaches completed; full-resolution estimate remains 12%.
The exact problem is unresolved by this packet. The intended queue outcome
is `partial`, `5/5`, changing only the selected row's two corresponding cells.
No automatic exhaustion workflow, remote write, merge, release, DOI deposit,
or external communication was performed during this investigation.
