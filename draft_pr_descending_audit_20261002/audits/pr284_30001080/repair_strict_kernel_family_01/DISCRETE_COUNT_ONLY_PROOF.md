# New turn 3 partial theorem: discrete count-only Cox sufficiency

This is a fresh derivation, not a historical PASS. It does not settle the non-discrete source target. No claim of priority, novelty, or publication readiness is made. Independent adversarial checking is pending.

## Statement

Let G be a countable discrete Abelian group and P a sigma-finite measure on its canonical space M* of nonzero locally finite measures. Assume P is invariant under every Poisson-averaged count-only invariant counting-mass-preserving Markov transport. Then P satisfies the full canonical Mecke identity. Conversely Mecke implies the assumed invariance by the credited transport-invariance theorem.

The proof permits infinite total P, arbitrary zero and positive atom masses, counting multiplicities, finite-order group elements and arbitrary period subgroups. It uses neither alpha gates nor extra marks or an intensity background. On discrete G local finiteness makes every alpha{s} finite. Write theta_d alpha(B)=alpha(B+d).

## Genuine count-only family and exact density

Choose a proper invariant metric and U(s,t) equal to the union of the two closed distance-d(s,t) balls. For a counting measure eta pair distinct singletons s,t iff eta(U(s,t))=2. Each point has at most one partner: two possible partners force at least three points in the larger pair ball, including ties. The pairs are disjoint transpositions, multiple atoms and other points stay fixed. Retain a pair only if t-s belongs to {d,-d}, for a fixed nonzero d. This is a deterministic count-only invariant matching preserving eta. Extend it by identity on noncounting measures if all-state preservation is required.

For d != -d mix the matching with identity in equal proportions. For d=-d use the matching itself. After inserting the root and averaging over Pi_alpha, both cases admit the same two-direction formula

    K_d(alpha,0,.) = p_+(alpha) delta_d + p_-(alpha) delta_-d
                    + (1-p_+-p_-) delta_0,
    p_+(alpha) = (1/2) alpha{d} exp[-alpha(U(0,d))],
    p_-(alpha) = (1/2) alpha{-d} exp[-alpha(U(0,-d))].

When d=-d the two contributions coincide and add to the unthinned matching probability. The formula follows from ordinary Poisson Campbell-Mecke: after inserting root and partner, the original process must vanish on U. It includes both endpoint atom void factors. U is compact and alpha(U)<infinity, so all positive endpoint masses have positive jumps. The construction itself proves the row bound. Symmetry of the spatial density exp[-alpha U(s,t)] proves alpha-preservation. Nothing in the gate depends on alpha.

## Eliminate root-zero states using finite subtraction

Let A={alpha:alpha{0}=0}. Every off-diagonal jump lands at a state with positive root mass; hence there are no off-diagonal incoming jumps to A. For any finite-P set D contained in A, invariance under K_d and subtraction of its finite holding contribution give

    integral_D (p_++p_-) dP = 0.

A countable finite-P partition and all countably many nonzero d imply P(A)=0: a nonzero discrete alpha with root mass zero has alpha{d}>0 for at least one nonzero d. The trivial group is immediate.

Set nu(dalpha)=P(dalpha)/alpha{0} on A-complement and zero on A. This is sigma-finite, and equivalent to P. Fix d and write S=theta_d. Put

    c(alpha)=(1/2) alpha{0} alpha{d} exp[-alpha(U(0,d))].

The endpoint void factors give the uniform bound

    0 <= c(alpha) <= (1/2) e^-2,

because xy exp[-x-y] <= e^-2 for x,y>=0. Covariance and symmetry give the backward conductance c_-(alpha)=c(S^-1 alpha).

## Signed-current lemma with legitimate localization

Define positive measures

    M=c nu=P p_+,
    N=c S^-1_*nu = S^-1_*(P p_-).

Both M and N are bounded by P; for N this follows from K_d invariance (it is one incoming term). Likewise S_*M and S_*N are bounded by P. On every finite-P set, the invariant equation after finite holding subtraction is

    S_*M + N = M + S_*N.

Thus J=M-N is a locally finite signed measure with sigma-finite positive and negative parts, and S_*J=J. This equality is meant on common finite-P covers; no global infinity-minus-infinity is used. Pushforward of Jordan decomposition under a Borel bijection gives S-invariance of J^+ and J^-.

Suppose L=J^+ is nonzero. Since L<<nu and both are sigma-finite, write the Lebesgue decomposition nu=v L+nu_s, where 0<=v<infinity L-a.e. S-invariance of L implies S^-1_*nu has absolutely continuous density v(S alpha); the pushed singular part remains singular. Taking absolutely continuous parts of J=c(nu-S^-1_*nu) with respect to L gives

    1=c(alpha)[v(alpha)-v(S alpha)]    L-a.e.

In particular c>0 L-a.e. and

    v(alpha)-v(S alpha) >= 2 e^2.

The countable intersection of its S-shifts is still L-full. Iterating forces v(S^n alpha)<=v(alpha)-2n e^2, impossible for finite nonnegative v. Hence J^+=0. For J^- the same argument runs backwards. Therefore J=0. This excludes positive transient harmonic currents without assuming finite total P, recurrence of P, ergodicity, a measurable orbit quotient, or uniqueness of infinite invariant measures.

This also handles zeros of c: any nonzero current would have to live where c>0 at all iterates. Finite-order shifts and period shifts are included; iteration around a finite cycle already yields the contradiction.

## Deweight and conclude

From J=0,

    c nu = c S^-1_*nu.

Multiply these nonnegative equal measures by 2 exp[alpha(U(0,d))], finite pointwise. This gives

    P(dalpha) alpha{d}
      = S^-1_*[P(dalpha) alpha{-d}],

including the zero-endpoint regions, where both fluxes vanish. Equivalently, Campbell measure at displacement d agrees with its reversal. The d=0 equality is automatic. Summing over countably many d gives full Mecke for every nonnegative product test, then every nonnegative measurable test.

## Exact limit of this theorem

For diffuse alpha on non-discrete G the fixed-displacement family has alpha{d}=0 and hence gives only the identity kernel. The discrete current proof cannot be transferred by claiming irreducibility, invariant-law uniqueness, or a common endpoint normalizing mass. General displacement-band tests give integrated flux equations, but the needed common factorization M=c nu, N=c S^-1_*nu and bounded reciprocal resistance are unproved. This is the remaining global repair gap. A discrete theorem is not a solution of the full LCA target.
