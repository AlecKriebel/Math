# Research log

All times 2026-10-04 UTC. Estimates below concern progress toward an
unconditional resolution of the exact target; they are subjective planning
estimates, not mathematical confidence levels.

## 14:20 — Source and duplicate gate

The requested catalogue page was inaccessible. The frozen catalogue record
identified OWR 51/2017, p.3065, and the primary PDF confirmed the polynomial,
the line Re(s)=1, and the quantifier over all real heights. Checked the live
target row and exact-ID repository/PR/branch results; no earlier target
attempt was found. Read the existing individual desk assessment. Its warning
that phase density does not imply exact cancellation is correct. No source
report for this OWR ID appeared in the older AMR/AIM research-report corpus.

Estimated progress toward full resolution: 2%.

## 14:24 — Approach 1: half-plane domination

Derived the sharp rightmost zero boundary using triangle equality,
logarithmic independence and a Kronecker/Rouché argument. This gives zeros
strictly right of one, but neither proves nor refutes zeros on the target
line. Subsequently checked the classical background in Erdős–Ingham.
The half-plane route is closed as a proposed full proof.

Estimated progress toward full resolution: 5%.

## 14:25 — Approach 2: exact torus geometry

Constructed and checked an algebraic torus zero with phases
-1, (-289+i sqrt(6479))/300, (-161-i sqrt(6479))/180. Density then proves
the infimum of |D(1+it)| is zero. A positive uniform-separation route is
therefore impossible. Exact orbit intersection is still unknown.

Estimated progress toward full resolution: 5%.

## 14:27 — Approach 3: phase and derivative constraints

Derived the 1/30 deficit identity, three individual angular restrictions,
and a positive real-derivative bound at any hypothetical line zero.
Created an adaptive outward-interval cover excluding all |t|<=10000.
The zero-bearing polynomial 1+2*2^(-s) correctly produces an unresolved
interval. A high-precision exploratory root to the right of the line was
upgraded to an explicit small Rouché disk certificate; the floating root
finder is not a proof dependency. A first script execution had a Python
type error from applying float.hex to the initial integer zero endpoint;
the initial endpoint was changed to 0.0 before the successful full runs.

Estimated progress toward full resolution: 8%.

## 14:29 — Approach 4: Tauberian reconstruction

Worked out the monotone positive oscillatory function produced by a
hypothetical line zero and verified its exact 61/30 identity. Checked the
zero-below-one convention separately and explained why a zero with real
part greater than one does not yield the required monotone function.
The original 1964 scan confirms this is a classical construction. It is
recorded as a credited reconstruction, not a new equivalence theorem.

Estimated progress toward full resolution: 5%.

## 14:31 — Approach 5: arithmetic elimination

Eliminated two phases using the equation and its conjugate. The phase field
at a hypothetical zero would have transcendence degree exactly one, and
every individual phase would be transcendental by the six exponentials
theorem. Full Schanuel gives a six-versus-five transcendence-degree
contradiction and hence conditional nonvanishing. No unconditional theorem
was substituted for Schanuel. The remaining arithmetic case is explicit.

Estimated progress toward full resolution: 10%.

## 14:34 — Source reconciliation and packet preparation

Read Yip's complete paper: the infinite-sequence disproof expressly leaves
the finite {2,3,5} case open. Verified the repeated target in OWR 51/2025;
record 30006466 includes this same subquestion plus unrelated questions.
Inspected the original Erdős–Ingham theorem and source question visually.
Prepared the five-approach note, exact/interval controls and replay output.
The exact question is unresolved, with the five substantive approaches
exhausted. No additional proof-search family is counted as verification.
Any subsequent review should check this frozen material rather than
silently add a sixth attempt.

Estimated progress toward full resolution: 10%; unconditional full result
not obtained. Final disposition: unsolved, 5/5.
