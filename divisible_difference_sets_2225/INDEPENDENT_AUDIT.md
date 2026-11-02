# Independent audit: Erdős 635 / queue row 1867

Date: 2026-10-21 UTC. This report verifies elementary claims and bounded computations, not novelty or a complete solution.

## Problem and source-status discipline

For integer t>=1, admissibility excludes a<b with d=b-a>=t and d|b. Since d|b iff d|a, the forbidden pairs are exactly consecutive positive multiples kd,(k+1)d, d>=t, k>=1. This is not the primitive-set problem. Real thresholds reduce to their ceilings. Fixed t is essential: if t>N/2 there are no forbidden pairs, because a>=d implies b>=2d>N. Consequently a half-density claim uniform in arbitrary growing t is false.

The source gate at SOURCE_STATUS.md records the fixed-threshold half-density part as already resolved in indexed official discussion and a live repository wiki. It does not supply an inspected original proof or rebuilt Lean artifact. The direct official problem/forum pages were blocked and their indexed status is stale. This audit adds no claim about live October status, primary-proof verification, or Lean correctness. The sharper excess remains unresolved in the checked evidence, not certified globally open.

## Accepted elementary claims

1. All odd integers form an admissible set: their differences are even and cannot divide an odd endpoint.

2. For an even integer x, its odd neighbors in the forbidden graph are exactly the in-range integers x-d and x+d, for odd divisors d of x satisfying d>=t. This follows by parity and the equivalence d|x iff d divides the other endpoint. Write x=2^r u with u odd, r>=1. There is no odd neighbor iff u<t. Necessity uses the explicit lower neighbor x-u>=1, so boundary truncation never invalidates this conclusion.

3. Therefore a set containing every odd integer can add only even numbers with odd part less than t. Conversely such even numbers have no conflicts with the odds, but conflicts among the evens still have to be checked. Selecting all of them is generally invalid: for t=4, both 12 and 16 qualify, but their difference 4 divides 16.

4. For t=2, the eligible evens are exactly 2^k, k>=1. Two such powers have a forbidden edge iff their exponents differ by one: after cancellation, 2^g-1 divides 1 only when g=1. Thus with L=floor(log_2 N), the exact maximum among sets containing all odds is ceil(N/2)+ceil(L/2). The alternating-exponent construction is already recorded in the source gate and is not a new result. This restricted optimum does not establish the unrestricted maximum.

5. More generally, for t>=2 the family consisting of all odds and a subset of the even powers has exact optimum
   ceil(N/2) + min(L,q-1) + ceil(max(0,L-q+1)/2),
   where q=max(1,ceil(log_2 t)). The powers form q-1 initial isolated vertices, truncated at L, followed by a path: edge k--(k+1) is present precisely when 2^k>=t. The formula must not be used at t=1, when the powers also conflict with the odds. At t=1, pairing (1,2),(3,4),... gives the exact unrestricted bound ceil(N/2), attained by odds.

6. A valid t-dependent extension: let t>=2, h=floor(t/2), m*=2h-1, and Q=1+floor(log_2(2m*)). Add to all odds the numbers 2^k m<=N with m odd, m<t, k>=1, k congruent to 1 modulo Q. Same-level pairs cannot be adjacent because an even difference m-n cannot divide odd m. Across levels l<k, an edge forces |2^(k-l)m-n| to divide n, hence 2^(k-l)m<=2n<=2m*. This forces k-l<=Q-1, contrary to the selected levels. The exact number of additions is the sum over odd m<t of max(0,1+floor((floor(log_2(N/m))-1)/Q)). For fixed t this is (h/Q)log_2 N+O_t(1). This is an elementary lower bound with no novelty assertion, not a logarithmic upper bound or a sharp asymptotic.

## Finite computation audit

The supplied exact_check.py builds precisely the forbidden graph: for d from t to N-1, it inserts all edges a,a+d with a a positive multiple of d and a+d<=N. Its component decomposition preserves independence numbers. Its deletion recurrence alpha(S)=max(alpha(S minus v),1+alpha(S minus closed-neighborhood(v))) is exact and uses integer arithmetic. Witness reconstruction follows the selected recurrence branch correctly.

The separate independent_audit.py builds edges by direct examination of all endpoint pairs, checks every supplied witness, and enumerates every subset for N<=18. INDEPENDENT_CHECKS.json records:
- All 305 witnesses in exact_results.json and sampled_t2_results.json checked against the defining relation, size, uniqueness and range.
- All 108 cases N=1,...,18 and t=1,...,6 independently proved optimal by full subset enumeration.
- Odd-neighbor characterizations checked for every even vertex in all 305 cases.
- Restricted-powers formula checked by exhaustive power-subset enumeration in all 255 cases with t>=2.

The N=19,...,50 and sampled N=60,80,100,120,150 optimality values rely on the audited exact recurrence; this auditor has not independently rerun all those larger searches. Their witnesses are lower-bound certificates, not independently checkable upper-bound certificates by themselves. Matching witnesses can separately prove an upper bound N-|matching|, if constructed and checked. A collection of finite equalities, however extensive, does not prove an all-N identity or a sharp logarithmic error term.

## Verdict

ACCEPT the explicitly scoped elementary statements and finite checks above. REJECT any inference of unrestricted all-N optimality, a sharp-excess resolution, novelty of the known logarithmic construction, verification of a primary half-density proof, or verified live status from these artifacts alone. No external publication or queue editing was performed by this auditor.

## Additional upper-bound and finite-state audit

The full RESEARCH_REPORT.md was inspected. Its doubling-forest bound is correct: retaining only edges x--2x gives paths indexed by odd part. At t=1 their independence number is N-floor(N/2)+floor(N/4)-...=2N/3+O(log N). Removing at most t-1 edges increases an independence number by at most t-1, giving the stated weak upper bound, not a sharp half-density estimate. At N=2t the only edge is t--2t, while N<2t has no edges.

There is a valid optional stronger statement solely for the all-odds-containing family. For fixed integer t>=2, its optimum equals ceil(N/2)+rho_t log_2 N+O_t(1), where rho_t is rational and algorithmically computable by a finite state graph. Here is the full justification needed for acceptance.

Set m*=2 floor(t/2)-1 and R=floor(log_2(2m*)). Consider the even vertices 2^k m with m odd and m<t. Same-level vertices have no edges. For k<k+g, two vertices 2^k m,2^(k+g)n have an edge exactly when c=|2^g n-m| divides m and 2^k c>=t. Absolute value is essential: the larger valuation need not give the larger numerical value. The positive integer c, when dividing m, satisfies c<=m, so 2^g n<=2m<=2m* and g<=R. Thus interaction has finite range R. For k>=ceil(log_2 t), the threshold is automatic and adjacency is independent of k. All odd parts occur in every layer k<=floor(log_2(N/m*)); only O_t(1) initial and upper layers are exceptional, changing the optimum by O_t(1) vertices.

In the central layers, states can be taken as every feasible pattern of selected odd parts in the previous R layers. A transition appends a compatible subset in the new layer and drops the oldest; assign weight equal to the appended subset's cardinality. These are finitely many states and integer weights. An all-empty buffer of length R allows passage from any feasible state to any other, so there is no unreachable critical component. Let rho_t be the maximum cycle weight divided by cycle length; it is rational and computable from finitely many simple cycles. Decomposing any long walk into cycles and a bounded-length remainder bounds its weight above by rho_t times its length plus a constant depending only on t. Repeatedly traversing a maximizing cycle, with bounded connecting and residual segments, achieves the reverse bound. This proves the displayed restricted asymptotic after restoring the exceptional layers.

This finite-state result does not imply that a global maximum contains the odds. It gives no unrestricted upper bound on M_t(N), and its literature novelty has not been investigated or claimed.

The final RESTRICTED_TRANSFER_STRUCTURE.md has now been inspected and its complete proof is accepted with the restricted scope above. The final RESEARCH_REPORT.md's matching obstruction is also accepted: every odd prime p>N/2 is isolated for t>=2, so I such vertices force any matching-derived independence upper bound to be at least (N+I)/2. This does not obstruct methods using information beyond a matching. The 232 entries of construction_checks.json were independently reconstructed and directly checked against the forbidden relation by independent_audit.py. These empirical checks supplement, rather than replace, the construction proof.
