# Root initial reconstruction before inherited review verdicts

UTC: 2026-10-15T06:13:32.279554+00:00. Case estimate 10%; hypotheses only, not mathematical or priority clearance.

I read the entire frozen CANDIDATE.md and the complete imported problem/prior-report record. The prior-report object is empty. The native candidate has not yet been tested against controlling source theorems; inherited review conclusions have not been read. This is my independent reconstruction and explicit list of falsifiable obligations.

## Exact claim and success criterion

The imported record asks for the full cylinder-area spectrum, specifically the normalized-area interval [g^(-1/2),2g^(-1/2)]. The candidate specifies the iterated N→∞, then g→∞, horizontal-cylinder law of the principal holomorphic quadratic stratum. The source's complete surrounding contribution must independently support those conventions. A scope narrowing cannot be excused merely by proving a theorem about a convenient ensemble. A source factor discrepancy (4g−4 versus 6g−6) must be resolved, not silently absorbed.

The candidate asserts TV approximation of the entire unordered area multiset by a positive composition/Dirichlet mixture, plus a scale-invariant Poisson point process on every s→0 with gs→∞, with all fixed count moments. The intended mean in the specified window is (log 2)/2, and the zero-count limit is 2^(-1/2). These statements are hypotheses. Proof, exact finite identities, geometric input applicability, and source scope must all pass before a priority audit or manuscript starts.

## Independent derivation of the analytic mechanism

The assembly generating function H=exp(sum ζ(2j)z^j/(2j)) has coefficient normalization h_n. Marking parts with t gives H^t, so the law of the number of parts has pgf [z^n]H^t/h_n. Interchanging the absolutely convergent z-series gives H=(1−z)^(-1/2)B with B analytic to radius 4, B(1)=sqrt(2). The singular coefficient asymptotic therefore has exponent −1/2. The general-t exponent is t/2−1, so the ratio pgf has power (t−1)/2. At t=1.1 and cutoff 0.6 log(2n), Chernoff's exponent is 0.6log(1.1)−0.05≈0.0071861>0; 1/220 is a valid weaker positive bound. This small exponent is enough to suppress every fixed power of log n after Cauchy–Schwarz, provided the asserted geometric pgf is actually uniform at this t and normalized for the same ensemble.

Removing selected components gives exact factorial moments with h_(n−r)/h_n, where r is selected total size. At a mesoscopic part scale q=ns, each fixed number of selected sizes occupies O(q)=o(n), making this ratio uniformly 1+o(1). The harmonic sum of ζ(2j)/(2j) on [aq,bq] tends to (1/2)log(b/a). This derives the unmarked Poisson factorial moments. Repeated size values are handled by falling factorials, not by treating cycle indicators as independent. Multivariate moment determinacy and tightness still need explicit inspection.

Gamma marking with shape 2j has mean 2j and standard deviation sqrt(2j); dividing by 2q yields errors O(q^(-1/2)) when j≈q. The expected sum of errors over relevant sizes is O(q^(-1/2)), since expected counts are weighted harmonically. For j much smaller than q, upper Gamma tails are exp(−c q), multiplied by only log q rather than log n. For j much larger than q, lower tails are exp(−c j); the potential coefficient ratio blowup near j=n is at most O(sqrt n) and is dominated by exp(−c n). This avoids an invalid union bound log n exp(−cq) for arbitrarily slowly growing q. The positive dilation by 2n/T tends to 1 because the Gamma shapes sum exactly to 2n. No independence with the point process is required by Slutsky. It is legitimate to work on (0,∞) with vague convergence; infinitely many limiting atoms accumulate only at zero and infinity.

Distribution convergence does not imply moments. The candidate instead bounds all marked count factorial moments by splitting selected mass at n/2. The small-mass part uses a bounded h-ratio and a uniformly finite marked harmonic sum. In the large-mass part some size exceeds n/(2r), and because q=o(n), its lower Gamma tail is exp(−c_r n); all remaining polynomial/logarithmic losses are harmless. For normalized counts, the event T/(2n)∈[1/2,2] enlarges the marked window by fixed factors; its exponentially small complement is bounded by K≤n. Thus a higher-moment bound supplies uniform integrability. Transferring these moments to geometry additionally requires a uniform latent density comparison on the good set and quantitatively negligible K-moments on the bad set; total variation alone would not suffice.

## Central geometric dependency and exact gaps

The strongest unverified dependency is the source expansion of the one-vertex stable-graph density. Its monomials must have Dirichlet parameters 2j, composition total 3g−3, automorphism 2^k k!, no missing height/label factors, and a relative coefficient estimate uniform over every composition and k up to 0.6log(2n). In addition the graph prefactor D_(g,k) must become asymptotically independent of k. Algebraically its proposed consecutive ratio equals 12(g−k)(3g−3−k)/((6g−5−2k)(6g−6−2k)), which tends uniformly to 1 with accumulated error O(log²g/g). This will be independently checked exactly, then against the source's actual definitions and normalizations.

The multiple-vertex exclusion must be a relative bound within each fixed k, not an unrestricted reading of a corollary outside its valid k range. The finite-genus geometric cylinder-count pgf must genuinely match DGZZ's multicurve measure via its correspondence. Exact finite checks can falsify prefactor and factorial identities, but cannot certify these imported geometric hypotheses or asymptotic novelty.

Boundary checks: fixed genus first; k=1 has an atom at area 1; k>1 has continuous simplex law; the requested window avoids that atom eventually. q→∞ may be arbitrarily slow, q/n→0 may be arbitrarily slow, and both need uniform proofs. No mesoscopic endpoint claim is made for q=O(1) or s≈1. A full-multiset TV approximation would answer more than a single mesoscopic window, but its relation to the original phrase 'full spectrum' requires independent source interpretation. All-direction and diagonal-limit problems must not be imported unless they are part of Problem 2 itself.

## Planned independent falsification families

1. Original source/ensemble/order-of-limits scope, independently before reading the candidate conclusions.
2. Geometric stable-graph/Dirichlet bridge and imported theorem hypotheses, including every constant and label factor.
3. Assembly coefficient/factorial moment asymptotics, quantitative exceptional-set and unbounded-moment transfer.
4. Gamma marking, arbitrarily slow mesoscales, normalized point-process topology and joint moments.

No priority conclusion, preprint, provider mutation, or publication is cleared by this reconstruction. Mathematical and source gaps remain open.
