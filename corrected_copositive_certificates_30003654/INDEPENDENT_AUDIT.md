# Independent audit: fixed-degree copositive closure, row 1847

Date: 2026-10-21 UTC. Reviewed `RESEARCH.md`, all five approaches, against locally recovered primary texts of arXiv:1709.03435v1 and arXiv:1909.06689v5. No queue edits or external publication performed. Exact algebra checks are in `check_exact.py` and `EXACT_CHECKS.json`.

## Verdict

ACCEPT the corrected closure theorem, its compact-penalty proof, its independent dual proof, and the exact examples, under the stated hypotheses: closed S in a pointed closed convex cone K; nonzero h of actual degree m≤d nonnegative on S; coefficient closure in the fixed finite-dimensional space R_d[x]. The theorem uses p_[d], not the actual leading part of p. This is a mathematical correction and clarification, not a resolution of the OWR exploratory research question or an established novelty claim.

The literal Theorem 1 defect is confirmed from primary definitions: P_d allows degree at most d; tilde means highest actual degree; no exact-degree assumption excludes p=1+x−y. For h=(xy+1)(x−y)^2 and d=4, the identity p+h=(y−x−1/2)^2+3/4+xy(y−x)^2 proves membership before closure. Actual leading p is negative at (0,1), where leading h vanishes. The corrected p_[4] is zero. The counterexample is exact, not numerical.

## Compactification and proof checks

1. Closedness and convexity of pointed K guarantee a functional a strictly positive on K\{0}. Compactness of K intersect the unit sphere upgrades this to a·x≥c||x||. Convexity cannot simply be deleted: a nonconvex pointed cone need not admit a strictly positive functional. An explicitly assumed positive functional would be a valid alternative hypothesis.
2. The section t+a·u=1, t≥0, u∈K is compact. Taking the closure of normalized S gives C compact even when S is unbounded. For t>0, division u/t and closedness of S recover exactly S. For t=0, normalized horizon directions give precisely S∞ intersect {a·v=1}. The origin is not a point of C and has to be considered separately in formulations of horizon set equality.
3. Degree-d homogenization is a linear isomorphism from R_d[x] to homogeneous degree-d forms in (t,u), so coefficient limits and continuous evaluations match exactly. Homogenizing h at its actual degree m is essential. H≥0 on C follows by continuity from h≥0 on S.
4. The compact penalty is valid: F≥0 where H=0 implies F+epsilon>0 on a sufficiently small H-sublevel. Away from that sublevel, a finite nonnegative multiple of H dominates the bounded negative part of F. Multiplication by L^(d−m), with L=t+a·u=1 on C, restores the degree without altering the argument.
5. L is positive on every nonzero homogenized cone point. Thus odd degrees and odd degree gaps cause no sign problem. A norm-power or a power of t would not be an interchangeable substitute.
6. Empty S is trivial and should be dispatched before taking a maximum over C. Nonzero constant h is included (m=0). The zero polynomial h has no degree and must stay in the separate case C_d=P_d(S), as the draft does.
7. Strict positivity on the entire homogenized zero set gives exact membership. Strict positivity only on finite zeros does not: p=1−xy, h=x², d=2 is strictly positive on Z yet cannot be repaired by any constant multiple of x². For epsilon>0, M=1/(4epsilon) works; the quadratic matrix determinant is exactly epsilon>0.

## Dual proof checks

The evaluation cone is closed because all evaluations take L^d to 1; bounded total mass and compactness of the evaluation image control convergent conic combinations. Finite-dimensional separation identifies it with the dual of forms nonnegative on C. The product subspace is annihilated exactly by positive evaluation combinations supported on H=0: H L^(d−m) belongs to the product subspace and equals H≥0 on C, forcing each positively weighted support value to vanish. Conversely, zero-set evaluations annihilate every product. The bipolar then proves the same closure formula. Restriction kernels do not invalidate this argument. This is a genuinely different proof route, though of the same corrected result.

## Additional independent defect: empty feasible set in printed Theorem 2

The 2017 paper explicitly defines the horizon of the empty set to be empty. Its Theorem 2 has no nonempty-zero-set hypothesis. Take S=K=R_+, h=x²+1, d=2. Then Z=empty, so P_2(Z)=R_2[x]. For any quadratic p=Ax²+Bx+C, choose M sufficiently large that A+M>0 and C+M−B²/[4(A+M)]≥0. Completing the square gives p+M(x²+1)≥0 even on all R. Thus P_2(S)+hR=R_2[x] before closure. Nevertheless Z∞=empty whereas S∞ intersect {h_2=0}={0}. The literal iff in printed Theorem 2 therefore fails for a separate, origin-only reason.

A corrected geometric condition should compare nonzero horizon directions, or assume Z nonempty. The fixed-degree closure theorem itself is not damaged by this issue: p_[2](0)=0 imposes no restriction. Do not assert a fully repaired Theorem 2 equivalence without separately supplying its necessity proof.

## Five approaches and scope

Approach 1 is accepted with the above edge cases. Approach 2's rational formula is an immediate certified consequence of the compact penalty, not an algorithmic complexity bound. Its genuine degree-four obstruction r=(1+x+y)^3(1+x−y) is positive on the diagonal and has degree-four coefficient −1 on the y-axis, hence an exact infinity separator. Approach 3's strict/weak and exact/closure distinctions are correct. Approach 4's dual proof is sound. Approach 5 accurately limits the 2024 result to strong positivity and representation-dependent leading constraints. In that source, Example 4 uses the cubic 1+x³−(y−x)³ and rules out its specified degree-increasing lifting family; it is not the same polynomial as the linear counterexample and does not prove impossibility of all conceivable certificates. The current v5 lifting includes prescribed scaling, so v1 and v5 formulas cannot be interchanged.

Acceptance excludes: a claim that the OWR program is solved, a novelty/priority claim, a claim of finite convergence, a universal practical degree bound for every later hierarchy, an unconditional SOS theorem, or a polynomial-time conclusion.
