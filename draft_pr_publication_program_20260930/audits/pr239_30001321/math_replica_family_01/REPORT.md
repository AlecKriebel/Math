# Independent replica / heat-kernel audit of PR239

**Verdict: no mandatory mathematical defect found in the assigned mechanism.** This is a bounded family assessment, not overall acceptance of PR239 or a novelty certification.

I independently read the authenticated exact theorem and TURN_1 / TURN_2, derived their core estimates, and wrote fresh exact checks before reading any historical independent_review, supplied checker, or current mathematical family. No such review or checker was subsequently read or executed. Source files were read only. The audited inputs are pinned in INPUT_PINS.json.

The fixed-law two-replica kernel is correct, including the sticky zero site, bias cancellation, and the same-parity half-difference convention. Its reversible weights and holding probabilities justify the spectral monotonicity needed to turn the generating-function bound into the pointwise g_n≤C/√(n+1) bound. The backward difference recurrence proves zero maximality using δ≤a≤1/4. This yields the uniform conditional overlap estimate and the factorial occupation-sum moment bound with repeated times included.

The martingale variance identity is exact. I supplied an independent Fourier derivation of the binomial maximum and adjacent-difference bounds, avoiding reliance on the source's brief ratio sketch. Parity telescoping and signed-measure contraction give the interval gradient bound; splitting the convolution at N/2 and M² gives the variance sum. Window truncation then proves (F) uniformly in deterministic alignment. Its convergence for arbitrary M_N→∞ is legitimate by first fixing R, taking N,M→∞, then letting R grow. It supplies expectation convergence, not the requested tail bound by itself.

The lazy reflection formula and coalescing coupling are also sound on the same-parity lattice. I checked their interfaces to (M)–(P), the old-law concentration exponent arithmetic, and the deterministic moving-strip influence bounds. No hidden uniform-ellipticity, inverse-moment, quenched heat-kernel, or endpoint-mass independence assumption was found there. The full new final-segment closure and the exact match to the primary open-problem statement still deserve their separately assigned audits.

Fresh controls, executed successfully with standard-library rational arithmetic, comprise:

- **37,140 positive checks in 24 families across six fixed laws.** They cover forward/backward kernel agreement and maximality through n=32; the radical generating-function identity through order 32; exact conditional overlap for a nontrivial old mixture; occupation moments through order 8 at length 4; the exact quenched-mean and interval variance identities; parity-aware integer and real interval partitions; and lazy reflection through time 16 from starting half-gaps 1–18.
- **4,098 full finite environment configurations at N=4** were integrated exactly as part of those checks. Their averaged single and paired endpoint laws agree with the separately constructed annealed laws, directly testing the shared-site second-moment probabilities.
- **197 excluded-boundary controls.** They confirm that δ=0 arrows destroy the required smoothing, δ>a can destroy zero maximality but is impossible for this environment model, and opposite-parity endpoints remain disjoint. These controls support the source's stated restrictions; none is an admissible counterexample.

All 37,337 assertions passed. Both final check executions completed with exit 0 and no stderr. The earlier 36,894-check run was superseded only by adding explicit conditional-overlap and occupation-moment tests; no failing test was repaired or suppressed.

The six finite laws include deterministic p=1/100, a symmetric near-arrow mixture on {1/100,99/100}, an asymmetric mixture with q=811/1000, and a strongly biased mixture with q=17/5000. These probe constants and parity but are not an empirical substitute for a proof covering support accumulating at the endpoints. The general derivation depends only on fixed q∈(0,1), δ>0, bounded p and iid freshness, so the absence of uniform ellipticity is justified analytically.

**Exact remaining gap in this family:** none in the replica / overlap / Fourier / coarse-expectation mechanism audited here. This family did not establish priority, authenticate the primary OWR interpretation, decide whether all publication claims are appropriate, or independently certify every line of the separate small-scale closure. No recommended source correction is needed for the assigned inputs.

DERIVATION.md contains checkable general proofs and explicit excluded-boundary counterexamples. The two authored check scripts and their actual outputs are included in the finite manifest. No network, local Git, original global lock, PR/ref/provider/tracker mutation, cleanup, external outreach or other-chat coordination occurred.
