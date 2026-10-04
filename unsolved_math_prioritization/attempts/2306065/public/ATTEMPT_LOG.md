# Five-approach research log

Target: 2306065 / AMR-022-6065, Hayman–Lingham 6.65. Session: 2026-10-04 UTC. Exactly five substantive approach families were pursued; all remain short of the full target. These are interleaved approaches within one investigation, not five independent reviews. No sixth proof-search approach is represented by subsequent validation.

## Source gate (09:45–09:49 UTC; not a proof turn)

The requested catalogue URL was attempted first: web retrieval was inaccessible and an HTTP request returned 403. The complete selected corpus statement and prior report were read. The primary source was visually checked at printed p.141. Live main, queue, state, attempt directory, related groups and ID/label/title PR searches were checked. The queue row was queued, 0/5. No matching attempt, state item, related-target group or PR was returned. The primary papers were privately obtained and inspected. Barnard's 1975 endpoint conjecture and Pearce's 1991 counterexample were distinguished from the unresolved full optimization. The older corpus prior report contained no proof.

## Turn 1: Explicit slit competitors and endpoint interpolation

Mechanism: construct the Pick map and its square-root transform, compute a3 exactly, and test whether their crossing supplies the full sharp envelope.

Work: substituted the implicit Koebe relation through third order; obtained A3=3−8/M+5/M² and the odd competitor 1−M⁻². Factored their difference as 2(M−1)(M−3)/M². Checked the tie 8/9 at M=3 and known M=5 value 8/5. Compared the endpoint-envelope mechanism with the primary historical sources.

Result: valid lower bound (PROOF §2), but the proposed global envelope is false. Pearce already demonstrated this historically; the rational witness from Turn 5 independently verifies an instance.

Exact gap: no domination of arbitrary starlike maps by either coefficient competitor. Their coefficient crossing cannot replace global extremality.

Outcome: partial. Best-guess progress toward full sharp target: 5% (subjective, not a probability).

## Turn 2: Schwarz–Pick subordination and the equality obstruction

Mechanism: use the known logarithmic subordination to transfer the first two Schwarz coefficients to a3.

Work: proved a3=A2 v+A3 u², |v|≤1−|u|². Factored A2−A3 and established the upper envelope A2 on the entire target interval. Analyzed the equality case ω=ηz² rather than assuming that every subordinate function remains starlike. Differentiation of the implicit Pick relation proves p_M(−r)→0, giving negative real logarithmic derivative for the relaxed equality map. Compactness turns unattainability into a strict inequality.

Result: B(M)<2(1−1/M) for e<M<5; |a2|≤2(1−1/M). Full proof in PROOF §3.

Exact gap: the subordination class strictly contains the target class. The excluded equality case gives no sharp replacement constant or explicit uniform deficit.

Outcome: partial. Estimated full-target progress: 10%.

## Turn 3: Herglotz moments and simultaneous real-part constraints

Mechanism: put f=z exp g, recast starlikeness and boundedness as two positivity conditions, and search for a finite moment/dual solution.

Work: proved the exact analytic equivalence Re(1+zg')>0, Re g≤log M; derived a3=c2+c1²/2 and |c_n|≤2/n. Reconstructed real-coefficient symmetrization and attainment. Derived the logarithmic potential constraint on a probability measure. Tested the common finite-atomic extremizer reduction and proved it incompatible with boundedness: a positive atom produces a radial logarithmic blow-up. Derived the Fejér finite necessary hierarchy, which feeds the certified outer bound in Turn 5.

Result: exact infinite-dimensional formulation and finite outer relaxations. PROOF §§1 and 4.

Exact gap: neither arbitrary truncated moments nor finitely sampled inequalities solve the infinite positivity/boundedness coupling. An optimal measure and a sharp dual majorant are not obtained.

Outcome: partial. Estimated full-target progress: 15%.

## Turn 4: Two-slit accessory parameters and constrained optimization

Mechanism: use Barnard's variational reduction to turn the remaining extremal family into algebraic coefficients constrained by two real integrals.

Work: visually verified the primary square-root formula, reconstructed q1 and q2, and gave exact algebraic controls. Implemented a 256-node quadrature and multi-start constrained search at nine M values. Adaptive integration was separately used to check the recorded integral residuals. At M=3 the search yields approximately 0.9141951229. The c≥−0.999999 cutoff becomes active for larger M and yields values below the explicit Pick competitor, demonstrating lack of global coverage. Preserved both successful local computations and failed global controls.

Result: known finite-parameter reduction, reproducible numerical probe, and an explicit degeneracy obstruction. No numerical value is promoted to an exact extremum. PROOF §6 and SLIT_PROBE.json.

Exact gap: missing global optimization over the true parameter set, control of degenerate slit collisions, and certified sharpness/uniqueness. A small equality residual is not a global optimality certificate.

Outcome: partial. Estimated full-target progress: 15%.

## Turn 5: Exact finite certificates in both directions

Mechanism: use optimization only to discover rational candidates, then replace floating-point evidence with full-domain rational proofs.

Work: a degree-40 sampled polynomial search supplied a candidate logarithm. Shrinking and rounding it yielded WITNESS.json. Exact Bernstein subdivision proves both positivity inequalities over all x∈[−1,1]; rational exponential-tail arithmetic establishes the modulus bound. Separately, degree-40 Fejér necessary inequalities at 201 rational cosine points and 64 c1 slabs yielded LP duals. Rational nonnegative multipliers and exact residual correction certify every slab independently of the optimizer.

Result: 1134162229/1250000000 ≤ B(3) < 957/1000. The witness and all slab bounds are checked using the Python standard library alone. This is a verified partial, not the exact B(3), and not the full e<M<5 target.

Exact gap: the lower and upper bounds do not coincide even at M=3; the true sharp function across the interval is undetermined. Higher truncations would merely continue the same unclosed optimization problem.

Outcome: partial, budget exhausted at 5/5. Recommended target status: unsolved. Estimated full-target progress: 15%, low confidence. Do not count the already-known endpoint-conjecture disproof as a new solution or as an already_solved classification of Problem 6.65.

## Verification boundary

The author reran exact controls and recorded explicit limitations. These checks are not independent review. Publication remains gated on fresh independent audit and a current repository check. No remote state was changed by this investigation.
