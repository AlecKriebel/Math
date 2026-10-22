# Research log: 20000190

2026-10-04 UTC. Five substantive mathematical routes, not five tool calls.
Source triage began at 15:13. Mathematical development ran approximately
15:17-15:26; packaging followed. Completion estimates below refer to a full,
source-faithful practical pre-candidate resolution, not packet completion.

1. **Determinant-only rejection**, 15:17-15:22. Constructed rank-seven design
   matrices for B+zG and H^(-T)(B+zG). Their cubic polynomials are equal but their
   only real root changes from focal squares (4,25) to (-112/377,-1925/67).
   The scalar determinant mechanism is blocked; using the full pencil is still
   viable. Completion estimate 15%.
2. **Hermite signs with zeros and repeated roots**, 15:18-15:26. Derived the
   indicator with s^2+s, included the sum-of-minor-squares rank filter, and
   implemented at-most-three-dimensional trace forms. Tested off-diagonal
   inertia pivots, squarefree reduction, nonreal conjugates, rank-one roots,
   scale changes and a positive root at infinity. This is a classical extension
   of the imported generic method, not a fresh full solution. Critical q=0
   fibers remain unclassified. Completion estimate 25%.
3. **Critical-fiber and chart analysis**, 15:18-15:26. Built T+z diag(1,2,3)
   with one real determinant root and four zero focal quartics. The root admits
   every common positive focal length. Seven explicit matches have rank-seven
   design and positive depths in a real translated-camera realization. An atlas
   cannot turn an intrinsically nonunique fiber into unique focal functions.
   Full critical classification remains open in this attempt. Estimate 20%.
4. **Direct essential feasibility**, 15:21-15:26. Removed square roots from the
   essential cubic to get the exact three-variable semialgebraic reduction.
   The translation example reduces to a=b; diag(1,2,0) is infeasible for positive
   a,b despite satisfying degenerate zero-calibration relaxations. This supplies
   a theoretical elimination route, but no complete practical implementation
   or runtime advantage. Estimate 25%.
5. **Noise/conditioning route**, 15:21-15:26. Derived M(t)'s rational focal
   values and proved opposite positive/negative behavior arbitrarily close to
   t=-1. Six exact rational approach scales confirm the formulas. A uniform
   fixed absolute tolerance is blocked near this pole; an adaptive certified
   implementation and a stated estimator are still needed. Estimate 25%.

Verification finished with 240 exact assertions. A preliminary check compared
an integer-domain polynomial gcd to 1 instead of checking that its degree was
zero; this verifier-only issue was corrected before the final run. An initial
exploratory camera fixture had a point on the second camera's plane at infinity;
it was discarded, and the final fixtures explicitly test every image denominator.
No claimed proof was promoted on either failed exploratory check.

The attempt stops **unsolved, 5/5**. No remote writes were made by this worker.
A fresh separate audit is required before publishing the frozen packet. No
external communication, merge, release or DOI action is part of this attempt.
