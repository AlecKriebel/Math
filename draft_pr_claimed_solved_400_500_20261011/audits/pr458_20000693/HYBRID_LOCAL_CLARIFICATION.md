# H1: exact truncated hybrid prime means and the full Euler local model

PR458/problem20000693, frozen87a39f7b4e5ef81aacf98464f86586cc95684d7f. Root proposed verification clarification, pending entire independent Euler report and new whole-candidate review. The frozen author HEURISTIC§5 says the prime component has local mean(1), J_p. That is exact for the full Euler local model, not literally for the sharp truncated P_X in the primary Sahay Theorem1.3, printed5–6. No frozen or actual PR source is edited by this note.

For the primitive core, the exact local analytic function of the sharp cutoff is

  C^*_p,X(z)=exp(sum_{r>=1:p^r<=X} (sum_i a_i psi_i(p)^r) z^r/r).

For the original imprimitive characters, preserve all finite deletion factors:

  C_p,X(z)=product_{i:p|q_i}(1-psi_i(p)z)^{a_i} C^*_p,X(z),
  J_p,X=average_theta |C_p,X(exp(i theta)/sqrt(p))|^2.

The fractional powers use the branch analytic at0 with value1. For each fixed prime, C_p,X tends uniformly on the radius p^-1/2 circle to the full Euler B_p, hence J_p,X->J_p as X->infinity. At bad primes this follows directly from the convergent logarithmic series and the finite analytic nonvanishing deletion factors. At good primes the coefficient absolute values of every truncated exponential are bounded by(A)_r/r!, A=sum a_i, so the Parseval mean has a uniform polynomial-majorant tail. In particular for p<=X outsideS,

  J_p,X=1+|sum_i a_i psi_i(p)|^2/p+O_a(p^-2),

with the SAME first coefficient as J_p. This exact sharp primary definition has no v_X in its prime sum: Sahay's u_X smooths the ZERO kernel. A broader smoothing suggestion from root was corrected after reading the full primary display and is not used here.

Concrete finite-cutoff falsification: one zeta factor of weight1, X=3 and p=2, gives C_2,3(z)=exp(z) and J_2,3=sum_{r>=0}(1/2)^r/(r!)^2, strictly below sum_{r>=0}(1/2)^r=J_2=2. The prime3 has its separate local factor and does not change this prime2 calculation. Sahay's displayed Theorem1.3 assumes X>=2; the endpoint2 is included, and X=3 also supplies an interior example. Equality cannot be rescued by finite-prime equidistribution. More generally the full Euler factor is exp(sum_{r>=1}z^r/r)=(1-z)^-1, and omitted prime powers genuinely affect finite-X coefficients.

There is a checkable bridge for the IDEAL PHASE MODEL. For fixedX, finite-prime equidistribution gives the time mean of the actual weighted P_X factors as the product of these exact J_p,X over primes up toX and the finitely many deletion primes. As X grows past all primes inS, compare this product with product_{p<=X}J_p. OutsideS the quotient's logarithm is O_a(p^-2) uniformly in X>=p, because the p^-1 terms agree, each J>=1, and the uniform remainders are bounded. For each fixedp the quotient tends1. Define the quotient as1 for p>X. Dominated convergence with summable p^-2 proves the sum of logarithmic ratios tends0; the finitely many bad-prime ratios also tend1. Thus

  product_{p<=X} J_p,X / product_{p<=X} J_p ->1.

By the already-verified definition of A and Mertens' theorem,

  product_{p<=X}J_p / (e^gamma logX)^E ->A.

Consequently the iterated fixed-cutoff phase-model limit has the same normalized constant A. This is a deduction about local/ideal phase averages. It proves neither a simultaneous X(T) mean nor weighted prime/zero splitting, unitary modeling, constituent independence or H for actual L-functions. The original model assumptions must remain explicit.

Proposed replacement meaning for HEURISTIC§5: '(1) is the full Euler local model and the fixed-prime infinite-cutoff limit. The actual sharp hybrid prime component has local mean J_p,X. Fixed-cutoff equidistribution gives those truncated phase means exactly; the ideal phase product has normalized constant A as X grows. Matching this with the required simultaneous T/X weighted mean is a hypothesis of the hybrid model.' Equations(1)–(11), the leading prediction, arbitrary fixed moduli/nonnegative weights and prior attribution are unchanged. This addresses a narrow literal finite-cutoff statement; the pending fresh Euler report's required clarification will remain raw, not retroactively erased. Current publication verification/documentation defects remain separate.

2026-10-12T18:10:00Z provenance/primary-read correction: the sealed Euler report describes X=2 as an excluded endpoint and labels the cited theorem X>2. The complete primary display says X>=2, as independently observed by the whole-candidate reviewer and confirmed by root. Preserve that sealed raw report; this note corrects its source-range label without changing H1 or its bridge. See CONTEXT_INDEPENDENCE_CAVEAT.md for reviewer context limitations.
