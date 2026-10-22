# Five substantive approaches

Completion estimates below are subjective progress estimates toward the intended unrestricted periodic degree bound, not probabilities, and do not certify novelty. The scoped literal-source counterexample is recorded separately and is not used to evade the five-approach budget.

## 1. Reflection symmetry of spherical circles

Checkpoint 2026-10-04 12:35 UTC. Estimated full-goal completion: 5%.

Mechanism: replace f by a common iterate preserving two putative periodic circles. Irrational rotation rules out a finite intersection, so they are disjoint. Schwarz reflection makes the iterate commute with both circle reflections, hence with a loxodromic Möbius transformation. A Laurent-series coefficient comparison forces degree one, a contradiction.

Artifact: PARTIAL_PROOF.md B, including a direct discriminant calculation for the product of reflections. Exact symbolic identity and 190 rational disjoint-circle samples are replayed by verify.py.

Outcome: complete restricted author proof, at most one periodic spherical circle. Gap: no reflection symmetry is available for a general noncircular analytic curve, and modern definitions exclude circles. It does not bound the remaining curves.

## 2. Critical-point resource charging

Checkpoint 2026-10-04 12:36 UTC. Estimated full-goal completion: 8%.

Mechanism: periodic irrationally rotating curves are disjoint after choosing a common return iterate. Charge each curve containing a critical point of f to that critical point; total critical multiplicity is 2d-2. Extend the charge to cycles meeting Crit(f).

Artifact: PARTIAL_PROOF.md C. An exact cubic Blaschke control verifies the derivative, a double critical point on the unit circle, a finite pole, and total critical multiplicity four.

Outcome: restricted bound for critical-point-containing curves/cycles. Gap: Yang's constructed smooth curves are critical-point-free; a critical orbit's accumulation is not an injective assignment to curves. A cycle charge also does not bound the number of component curves when periods vary. Route blocked as a universal proof.

## 3. Complementary-region pole counting

Checkpoint 2026-10-04 12:39 UTC. Estimated full-goal completion: 25%.

Mechanism: for a finite family of individually invariant curves, normalize an external fixed point to infinity. A bounded complementary region without a pole maps conformally to itself by the argument principle. Julia-set boundaries make it a whole invariant Fatou component, which the irrational boundary dynamics force to be a rotation domain. This contradicts the exclusions. Charge all N bounded complementary regions to the at most d-1 finite pole multiplicities.

Artifact: PARTIAL_PROOF.md A with full topological and analytic steps. Classification dependency is McMullen-Sullivan Theorem 2.1.

Outcome: restricted author candidate N<=d-1 for individually invariant curves; candidate N<=d^L-1 when all periods divide L. Gap: replacing f by f^L changes the degree. For a periodic family f permutes boundary curves and need not preserve each complementary region. Long pole-free transitions cannot be excluded by the fixed-region argument. No degree-only periodic bound or finiteness across all periods follows. This significant restricted result awaits independent audit.

## 4. Analytic linearization across a collar

Checkpoint 2026-10-04 12:40 UTC. Estimated full-goal completion: 25%.

Mechanism: extend an analytic rotation conjugacy from a curve to a univalent annular collar by the identity principle. Iterates on that collar are conjugate to rotations, making it Fatou. Thus a genuine Julia-set curve cannot admit such an analytic conjugacy.

Artifact: PARTIAL_PROOF.md D. The golden-mean quadratic control in the literal-source note illustrates exactly the excluded Fatou-collar case.

Outcome: exact obstruction, not a count. Gap: analyticity of the embedded curve is not a supplied analytic conjugacy for its restricted dynamics; upgrading a topological conjugacy would introduce small-divisor and critical-point hypotheses absent from the target. Assuming the upgrade merely assumes away the difficult cases.

## 5. Simultaneous thickening and deformation dimension

Checkpoint 2026-10-04 12:41 UTC. Estimated full-goal completion: 25%.

Mechanism attempted: thicken each degenerate curve into a positive-modulus annulus, then apply the known cycle bound for genuine Herman rings. An inverse-surgery proposal must extend the boundary conjugacies and make the pulled-back Beltrami structure uniformly bounded while preserving degree and distinct cycles.

Artifact: PARTIAL_PROOF.md E proves that a finite union of smooth curves has area zero, so Beltrami parameters supported only on the curves give no deformation at all. The literature check reads Yang's construction and Lim's Corollary B/Theorem C; neither gives a simultaneous thickening theorem for an arbitrary finite family.

Outcome: blocked. Missing theorem: simultaneous degree-preserving thickening for all relevant curves, with control of their preimages and critical points. Shishikura's genuine-Herman-ring count is a cycle count; his Theorem 5 also provides cubic genuine rings of arbitrary period. Therefore neither a deformation-dimension analogy nor a cycle bound can be silently converted into a component-count bound. The genuine-ring examples are not counterexamples for degenerate rings.

## Final author assessment

Five distinct approaches are completed. The intended unrestricted periodic target remains unsolved in this packet. Keep the invariant-count candidate and the source clarification as partial results, subject to independent audit. Do not allocate an extra proof-search turn during auditing; corrections should repair or remove claims, not reopen the five-turn search budget.
