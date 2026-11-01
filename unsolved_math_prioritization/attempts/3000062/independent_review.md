# Independent adversarial review

Date: 2026-10-21. Target: the exact orientation-compatible integer multicover problem, ID 3000062. Reviewed `algorithmic_audit.md`, the source gate, and both exact-arithmetic check scripts. No publication or queue mutation was performed.

## Disposition

The audited reductions, counterexamples, exhaustive method, and restricted SCC construction are mathematically sound, subject to the minor edge-case/editorial clarifications below. They do **not** establish a polynomial-time algorithm for the unrestricted binary-encoded problem. No hardness classification for that exact problem was established either. Existence and the indegree-one case must remain explicitly identified as prior results, not a new resolution.

## Claims checked independently

1. **Exact fixed-point formulation.** Nonnegative cover feasibility is exactly x >= F(x); the specified incoming witness at each positive coordinate supplies equality there, while a zero coordinate necessarily has F_v(x)=0. Sources and self-loops are handled correctly.

2. **Exact rounding.** Nearest-integer ties-to-even rounding is monotone, fixes zero and every integer, and satisfies R(W-z)=W-R(z) for even integer W, including negative arguments and tie cases. It therefore commutes with this finite-max map. The conclusion applies to an exact real fixed point, not automatically to an approximation.

3. **Robust rounding.** The adjustable-threshold argument is valid. Each phi(I_v) is a closed interval of length at most epsilon because phi is continuous and 1-Lipschitz. When n epsilon < 1, their finite union leaves an open gap in (0,1), containing an efficiently representable rational choice of t. No coordinate segment meets a rounding threshold. Reflection by an even W preserves both thresholds and their even-valued boundary convention. Thus the rounded vector is an exact integer fixed point. Forbidden interval extrema can be obtained from endpoints and any contained integer, so there is no scan proportional to the weight magnitude. The missing step remains computation of the requisite approximate fixed point in polynomial binary-input time.

4. **Obstructions.** Verified the unique wrong minimum-sum LP solution, nonconvexity of the fixed-point set, failure of the midpoint of a genuine two-cycle, and failure of arbitrary incoming-policy selection. Independently derived the two-vertex family with weights 2K+2 and 2K: even iterates from zero are (2t,0), until saturation. Its Theta(K) iteration count is exponential in the input bit length. These examples refute the named shortcuts, not all possible LP encodings or policy algorithms.

5. **Policies and SCCs.** Adding selected zero/incoming equalities to all cover inequalities and nonnegativity gives a complete finite enumeration with polynomial work per policy, but exponentially many policies in general. The SCC procedure is sound when every nontrivial SCC is an internal directed cycle. Fixed upstream integer coordinates yield integer baselines. If not every internal cycle equality holds, some baseline must be active, justifying the anchor enumeration. The odd-cycle parity and even-cycle interval arguments preserve integrality. Singleton loops and parallel-arc maxima need, and receive, explicit treatment.

6. **Contraction and norm caveats.** The discounted-map residual estimate is valid but leaves an inverse-discount dependence proportional to weight magnitude in the simple iteration bound. Fixed ties-to-even rounding can fail at arbitrarily small residual. The two-leaf star expands finite l_p distances by 2^(1/p), so a theorem for nonexpansiveness in an even finite l_p norm does not directly apply.

## Literature boundary

The primary [Chen–Li–Yannakakis 2026 manuscript](https://arxiv.org/html/2602.10296v1) explicitly distinguishes polynomial query complexity from time-efficient computation: its general query-point search is expensive, and its time bound O(log^(ceil(k/2))(1/epsilon)) is for fixed dimension. This is not a polynomial-time solver for growing n here. The [Daskalakis–Farina–Zhang 2026 manuscript](https://arxiv.org/html/2607.23863v1) gives a polynomial-time result for even finite l_p norms; the expansion example above blocks its direct use. Neither source establishes a resolution or hardness theorem for this exact graph problem.

## Verification and minor clarifications

- Independently reran `check_algorithms.py`; its output exactly matched the saved JSON: 679 scalar identity checks, 729 digraphs, and 2,241 half-grid fixed points.
- Independently reran `check_robust_rounding.py`: 624 eligible approximate fixed points among 30,000 seeded trials all rounded exactly. These finite checks support implementation consistency only; the mathematical arguments carry the general claims.
- The final report now treats n=0 and M=0 as trivial before writing 1/n or 1/(nM).
- The final baseline statement correctly says that R fixes integer b_v and therefore commutes with max(b_v,·). Noninteger baselines require separate treatment. An earlier tautological phrasing was corrected; it was an editorial error, not a flaw in the construction.

Final status: **restricted results and algorithmic audit accepted; unrestricted polynomial-time construction NOT SOLVED by this work.**
