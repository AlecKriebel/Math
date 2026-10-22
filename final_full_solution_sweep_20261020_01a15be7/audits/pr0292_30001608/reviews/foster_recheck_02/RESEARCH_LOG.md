# Independent Foster recheck 02

## 2026-10-21T03:19:30.664964+00:00 — independent checkpoint, 12% complete

Scope: independently falsify the mathematical positive-recurrence claim at fixed real load lambda > 0. This checkpoint precedes reading TURN_4, inherited review verdicts, or author checkers. Only the model and review task supplied by the parent have been used. No external individual has been contacted. No publication clearance is asserted.

State is (a,b,x,y) in nonnegative integers, D=x+y+1. The download transitions preserve U=a+x and V=b+y. Direct generator algebra gives

- L U = lambda/2 - x(y+1)/D; L V = lambda/2 - y(x+1)/D.
- L(U-V)=(y-x)/D.
- L(U+V)=lambda-(2xy+x+y)/D.
- L(x+y)=[a(x+1)+b(y+1)-2xy-x-y]/D.

Independent initial falsification: the total-population linear drift alone fails whenever one completed type is absent and lambda > 1. An unbounded one-type corridor is therefore the central analytic difficulty. When min(x,y) is sufficiently large, the total-population drift is uniformly negative. In the corridor y bounded, x large, the b download rate b(y+1)/D can be arbitrarily small for bounded b, so a successful pointwise Lyapunov argument needs a corrector that captures b accumulation and eventual escape; finite population simulation or a truncation cannot establish it. U and V have bounded upward rates, suggesting polynomial rather than exponential escape growth.

Next: inspect the proposed certificate, independently derive its generator identities, and stress exact integer and signed cutoff interfaces. Current strongest result: the displayed generator identities and identification of the unstable linear-drift corridor. Exact remaining gap: an all-state coercive Lyapunov certificate with uniform negative drift at each fixed lambda > 0.

## 2026-10-21T03:21:41.778308+00:00 — analytic checkpoint, 70% complete

Re-derived every certificate component through the all-state three-region inequality, and supplied an explicit localized Dynkin passage for the CTMC. No analytic gap found for the exact six-rate model. This estimate measures this review task, not discovery of the theorem. Remaining: independent exact boundary and negative diagnostics, original control replay, byte hashes, final consistency review. Author checker and original independent checker were inspected only after the independent initial derivation and rounded/Poisson rederivation were recorded; their code will not be imported by the new diagnostic implementation.

## 2026-10-21T03:28:10.337261+00:00 — validation checkpoint, 95% complete

New exact tests pass: 315,600 assertions across 11,330 state evaluations at lambda=1/1,000,000, 3/17, 11/4, 55/8. The corrector is reconstructed through a killed tridiagonal linear-system solve and separately checked at R and R+1. Twenty deliberately mutated claims are rejected, including actual positive departure-correction witnesses. The original turn 1–4 and portable independent controls were each executed fresh from frozen source without writes (-B), and all passed. Turn 1–4 replay JSON equals the frozen saved JSON exactly. Package verifier passes 72 checks. All 40 source files match SOURCE_SNAPSHOT at head 1198534928f4c2bf8bf758c9ceb16edaa3a496e8.

Implementation note: the first attempt to write the new diagnostic used an incorrect relative path from the review directory; it failed before executing any tests. The path was corrected. Subsequent completed diagnostic executions exited zero. No scientific failure was suppressed.

No analytic gap found; final consistency check and report/manifest remain. Mathematical acceptance here is limited to the exact CTMC and this proof, not source priority, novelty, or publication permission.

## 2026-10-21T03:28:43.442236+00:00 — final checkpoint, 100% complete

Final independent mathematical review is complete. Verdict: no analytic gap found, no proof repair required, exact fixed-real-load theorem supported by the checked global Foster proof. Fresh executable evidence: 315,600 exact assertions, 11,330 state evaluations, 20 expected-failure controls; all original controls and 72 package checks pass; 40 source hashes match the pinned snapshot. FINAL_REVIEW.md and FINAL_REVIEW.json give the scope, limitations, and exact conclusion. Source/priority and publication decisions remain outside this task. Evidence manifest and a read-only consistency checker permit later byte-level verification.
