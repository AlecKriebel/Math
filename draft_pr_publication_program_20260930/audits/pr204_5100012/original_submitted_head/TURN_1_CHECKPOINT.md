# Turn 1 checkpoint: the two-pole area mechanism

2026-10-01 05:00 UTC. Complete-looking route, full presentation and separate review pending. This is a substantive author proof attempt, not an independent review of neighboring k203,a.

Fix caustic semiaxes alpha,beta, k=c/alpha, k'=beta/alpha, K,K'. Published canonical parameters give P(w)=(-a sn(w),b cn(w)), a=alpha dn(v)/cn(v), b=beta/cn(v), delta=2v=4K tau/N, gcd(N,tau)=1, 0<tau<N/2. All Jacobi functions use modulus k. Source target: origin pedal, signed areas, least N odd or divisible by4, nondegenerate nested confocal ellipses.

The chord through P(u-v),P(u+v) is the caustic tangent at (-alpha sn u,beta cn u), as verified directly by the addition formulas. Its origin foot is

Q(u)=(-alpha k'^2 sn(u)/dn^2(u), beta cn(u)/dn^2(u)).

Put S(w)=sum_(j=0)^(N-1) dn(w+j delta), and T(u)=1/2 sum_j det(Q(u+j delta),Q(u+(j+1)delta)). Ordinary orbit area A(w)=ab sn(v)cn(v)/dn(v) times S(w), by the dn addition identity and cross products. Origin-pedal area A0(w)=T(w+v).

Let m=N for odd N and m=N/2 for even N, and ell=2K/m. The cyclic sum S has periods ell,4iK' and anti-period2iK'. On this reduced torus its only poles are two simple poles at p=iK' and3p, with nonzero residues: at each original pole all repeated summands have the same residue. S is even. Reflection with its anti-period gives zeros at p+ell/2 and3p+ell/2, which are not poles. These exhaust its degree-two zero divisor, each simple. Thus S(w)S(w+ell/2) has no divisor and is a positive real constant.

Q has only double poles at r=K+iK' and r+2iK' modulo its larger periods; apparent singularities at sn/cn/dn poles are removable. It is even about r. Indeed Jacobi parity and shifts give sn(2r-u)=sn(u), cn(2r-u)=cn(u), dn(2r-u)=-dn(u), so Q(2r-u)=Q(u). The Laurent series at r therefore has no simple-pole term.

At an orbit position u+j delta=r+epsilon, the two incident terms in T combine as

1/2 det(Q(r+epsilon), Q(r+delta+epsilon)-Q(r-delta+epsilon)).

Both neighbor values are analytic, and their difference vanishes at epsilon=0 by reflection symmetry. Consequently the double pole cancels to at most a simple pole. Multiple indices representing the same pole for even N give copies of this cancellation; adjacent vertices are not simultaneously poles because delta is not0mod2K.

T has periods ell,4iK' and anti-period2iK': Q(u+2K)=-Q(u), and Q(u+2iK')=diag(1,-1)Q(u), whose determinant is-1. Thus T and S(u+K) have exactly the same two permitted simple-pole locations on the reduced torus and the same anti-period. Match one residue by a scalar C (allowed to vanish); anti-periodicity matches the other. Their difference is holomorphic on the compact torus, hence constant, and anti-periodicity makes this constant zero. Therefore T(u)=C S(u+K), and A0(w)=C S(w+K+v).

The phase K+v equals a half-period modulo ell precisely in the required cases: (K+v)/ell=(N+2tau)/2 for odd N, and (N/2+tau)/2 for even N. For odd N this is a half-integer, for N divisible by4 it is a half-integer, and for N=2mod4 it is an integer. Hence A(w)A0(w) is constant for the full requested parity. No division by A0 is required; a zero proportionality constant is harmless. Real A is positive for the chosen orientation because S is a sum of positive dn values.

Preliminary65-digit checks for N3,4,5,7,8,9,12 including stars show phase-independent T/S(u+K) and required products; wrong-parity N6,10 show variable products. Numerical checks are not the proof. Completion estimate:80% of the deliverable, pending full frozen artifact, exact controls and independent review.

Shared-author contribution: this two-pole mechanism was communicated to the parallel k203,a author. That author supplied its own centrally symmetric arbitrary-M area reduction; it is not assumed in this origin-only proof. Any extension to arbitrary M and any review of that result must disclose the collaboration rather than count it as independent verification.
