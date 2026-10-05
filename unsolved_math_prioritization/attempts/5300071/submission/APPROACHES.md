# Five substantive approaches

The five-turn allocation below counts mathematical approach families, not tool
calls. Source recovery is recorded separately. Each attempt ended without a
complete candidate for the intended general conjecture; no sixth search turn
was used. Completion estimates are heuristic fractions toward a full proof,
not calibrated probabilities.

1. **Local logarithmic-derivative trapping** (checkpoint 2026-10-04T16:28:00Z,
   estimated completion 10%). Factor out the selected root and bound the other
   logarithmic derivative using root separation. Obtain the explicit common
   disk r=m*delta/(4d-3m) and radial contraction factor squared 1-8h/(25m).
   This proves a genuine all-h local statement, including multiplicity. Gap:
   separation can collapse and the disk does not reach the exterior circles.
   Route blocked as a complete solution without a new global access mechanism.

2. **Exact invariant geometry via affine/Mobius conjugacy** (checkpoint
   2026-10-04T16:28:59Z, estimated completion 15%). Solve the single-root case
   and the two-distinct-root equal-multiplicity family. Derive parameter-
   independent Voronoi half-planes and the exact disk factor
   w(w+1-t)/(1+(1-t)w); prove convergence there. This yields c=2 for the full
   radius and parameter range in that subfamily. Unequal multiplicity and
   three or more roots are not covered. The circle-center ambiguity has an
   elementary counterexample only under the unintended arbitrary-center
   reading. Neither restriction is counted as solving the original target.

3. **Blaschke channel indices and monotonicity** (checkpoint
   2026-10-04T16:29:35Z, estimated completion 10%). Derive the conditional
   fixed-h identity sum 1/(mu_j-1)=2m/h-1. Compare the inspected classical
   channel estimates with what an intersection estimate would require.
   Construct the exact interval example for z(z^2-1): 1/2 is in the immediate
   basin of zero for h=1/2 but maps to -1 for h=1. Thus one proposed nesting
   direction fails. Abstract rotating semicircles show why individual length
   bounds do not imply a common length bound. Gap: parameter-coherent channel
   geometry, with all global model hypotheses checked.

4. **Newton flow, Euler shadowing, and parameter compactness** (checkpoint
   2026-10-04T16:30:00Z, estimated completion 10%). Derive the exact flow
   identity f(z(t))=exp(-t)f(z(0)). On a chosen compact pole-free trajectory
   family, finite-time Euler convergence plus a strict trapping disk yields a
   small-step certificate. Track its dependencies: pole clearance, derivative
   bounds, time horizon, and entry margin. Compactness in h only applies after
   a common starting set is known. Gap: neither these constants nor the
   common exterior set are controlled by degree alone, and h=0 is not an
   attracting-map endpoint. No unsupported global shadowing theorem is used.

5. **Finite adversarial basin survey and exact algebra controls** (checkpoint
   2026-10-04T16:31:51Z, estimated completion 10%). Execute the standard-library
   verifier. Exact checks cover 788 local inequality instances, 245 rational-
   complex conjugacy instances, 1,225 radius identities and the full interval
   nesting control. Sample 2,048 circle points at each of R=3,10,100 for five
   h values for z(z^2-1). The root-label agreements do not vanish, but they are
   convergence samples, not immediate-component, arc-length, or continuum-h
   proofs. The experiment finds no counterexample and is not positive evidence
   sufficient to close the gap. The five-approach budget is complete.
