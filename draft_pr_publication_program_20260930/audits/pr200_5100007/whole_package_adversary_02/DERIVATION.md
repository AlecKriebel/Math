# Independent mathematical reconstruction

This was preserved after reading the current manuscript, contract, verification source and metadata, and before reading supporting proofs, expected outputs, history or priority reports. It is an adversarial reconstruction, not a claim of a new discovery.

## Scope and actual geometry

Take positive alpha>beta, k=c/alpha in (0,1), v in (0,K), and a=alpha dn(v)/cn(v), b=beta/cn(v). These give a²-b²=c², lambda=b²-beta²>0, and lambda<b². The published canonical input still needs primary-source verification.

For the endpoints P(u-v), P(u+v), solve the two actual linear tangent equations. Addition formulas give Q=(-a dn(v)sn(u)/cn(v), b cn(u)/cn(v)). The determinant is nonzero: its magnitude is 2 sn(v)cn(v)dn(u)/(ab[1-k²sn²(u)sn²(v)]), strictly positive on the real axis. Direct substitution gives Qx²/a²+Qy²/b²-1=sn²(v)dn²(u)/cn²(v)>0. Thus Q is finite, outside the ellipse, and cannot equal an internal focus. This establishes strict positive ordinary distances even for star windings; convexity of the ordered polygon is not assumed.

An independent physical-coordinate expansion uses A=a², B=b², d=A-B, lambda=l, outer squared axes U=A²/(A-l), V=B²/(B-l), and S=sn²(u). The paired squared focal-distance product is H=(V+d+(U-V)S)²-4dUS. It factors as (1-dS/(A-l))*[(V+d)²-(A-l)(U-V)²S/d]. Substituting canonical relations makes the first factor dn²(u), and the second a positive constant times dn²(delta)-k²cn²(delta)sn²(u), delta=2v. This is an algebraic identity before closing an orbit.

## Full divisor, including special and collision cases

Use T=C/(2K Z+2iK' Z). The map sn²:T→P1 has degree two, double pole p=iK', and branch values 0,1,1/k²,infinity. dn²=1-k²sn² has a double zero at p+K and double pole p. For delta in (0,2K), cn(delta)=0 exactly at delta=K. Otherwise the second factor is a degree-two elliptic function. The identity sn(p+K+z)=dn(z)/(k cn(z)) locates its zeros at p+K±delta. Their coincidence would require 2delta in 2K Z, which forces delta=K in the allowed interval. Neither equals p nor p+K unless delta=K or a forbidden endpoint. Therefore the generic zeros are distinct and simple; H has exactly divisor 2[p+K]+[p+K+delta]+[p+K-delta]-4[p]. At delta=K the bracket is k'²>0, so H has divisor 2[p+K]-2[p], with no extra hidden zeros or poles.

Close with delta=4K tau/N and gcd(tau,N)=1, 0<tau<N/2. The order of delta on T is L=N/gcd(N,2). Translation of the complete divisor over G=<delta> yields 4 O(p+K)-4 O(p), or coefficient two at the exceptional primitive (N,tau)=(4,1). This counts all factor collisions. Two cosets are identical or disjoint. K belongs to G iff G has even order iff four divides N; this conclusion is independent of the chosen coprime generator, covering all primitive stars. The divisor vanishes exactly in the asserted positive parity. A meromorphic function with zero divisor on the compact torus is a finite nonzero constant. Otherwise its divisor is nonzero, hence the function cannot be constant.

## Return to real lengths and necessity for odd N

Let F(u)=product over j=0,...,L-1 of H(u+jdelta). On the real axis every factor is positive and there are no poles. For all N, Q(u+2K)=-Q(u) gives R-(u)=R+(u+2K), and R+²R-²=F^(N/L). If either real product is phase constant, so is the other, and F^(N/L) equals a constant on a real interval. A real interval contains interior accumulation points in the complex torus away from poles, so the holomorphic identity theorem extends the identity meromorphically. Its divisor would be (N/L)div(F), contradicting the nonzero divisor when four does not divide N. No complex square root or odd-orbit antipodal membership is needed.

If four divides N, N is even and tau is odd. Advancing N/2 steps moves Q by 2Ktau and therefore to -Q inside the same primitive orbit. This gives R+=R->0 and R+²=F. The positive real square root proves constancy. At N4 the same pairing uses the separately checked degree-two H.

## Boundary audit

Repetitions give R^r with positive R, so injectivity prevents a nonconstant primitive orbit from becoming constant. A circle violates the noncircular assumption and indeed gives constant radius a/cos(pi tau/N) for all admitted primitive stars. k=0, k=1, v=0,K, lambda=0,b², collapsed/hyperbolic caustics and N2 are excluded; no argument here extends through them by continuity. Reversal reindexes distance factors. No unsupported general rigidity result is invoked.

Strongest reconstructed result: the stated analytic proof establishes the exact iff criterion, conditional only on the published canonical billiard parametrization and standard Jacobi divisor facts. Remaining tasks: primary input/source verification, independent computed stress checks, complete supporting payload audit and package integrity/PDF review.
