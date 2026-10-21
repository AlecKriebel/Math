# Independent analytic derivation before candidate exposure

Timestamped completion: 2026-10-12 09:41 UTC; completion estimate 45%.

Exposure: task text, applicable AGENTS.md, candidate TARGET.json and source_manifest.json (metadata only), original source PDF definitions/Table 5, and NIST DLMF §§22.4,22.8,22.13. No submitted PROOF.md, checker, research log, review, receipt or verdict read.

This derivation is independent of the submitted argument. Numerical spot checks are diagnostic and are not used below.

## Claim and notation

Let 0<k<1, l=sqrt(1-k²), K=K(k), J=K(l), p=sn(v), q=cn(v), r=dn(v), a=r/q, b=l/q. Assume N=0 mod4, gcd(N,tau)=1, 0<tau<N/2, v=2K tau/N, delta=2v. Thus p,q,r>0, a²-b²=k², a²-1=b²-l²=l²p²/q². The confocal caustic has axes (1,l). Focus F=(k,0). Parameterize the billiard vertices P(u)=(-a sn u,b cn u). Put t=u+v, so each side/intersection is centered on t+j delta.

The original source defines pedal vertices as perpendicular feet from F to the original polygon sides, and antipedal vertices as consecutive intersections of lines through original vertices perpendicular to P-F. Areas are signed half-sums of consecutive determinants. The target is their product, without primes, for either original focus.

Write s=sn t,c=cn t,d=dn t, E=1-k²p²s², B=l²+k²q⁴, C=l²-k²q⁴. The standard addition laws and shifts used here are documented in [NIST DLMF 22.8](https://dlmf.nist.gov/22.8) and [NIST DLMF 22.4](https://dlmf.nist.gov/22.4). Derivatives are documented in [NIST DLMF 22.13](https://dlmf.nist.gov/22.13).

## Direct line and intersection algebra

Addition laws give s±=(sqr±pcd)/E, c±=(cq∓sdpr)/E. The line joining P(t-v) and P(t+v) is

    -s x + (c/l)y = 1.

Substitution verifies both endpoints, since s²r²+c²=E. Its focus foot is

    Q(t)=((k-s)/(1-ks), l c/(1-ks)).

Q(t) lies on the unit circle by exact algebra. Focus radii satisfy (P(u)-F)·(P(u)-F)=(a+k sn u)². Consequently an antipedal line in focus coordinates Z=X-F is

    (-a sn u-k, b cn u)·Z=(a+k sn u)².

The unnormalized determinant of the lines at u=t±v is

    D(t)=2 b p r d(1+ks)/E.

It is nonzero for every real t: p,r,b,d,E,1+ks are positive. Thus the original real intersections are everywhere well-defined.

Taking the average and the divided difference of the line equations, solving, and using c²=1-s²,d²=1-k²s² gives the antipedal vertex

    R_x(t)=[k r² s²-Bs-kq²]/(q²E),
    R_y(t)=c[C-kBs]/(l q²E).

This is initially derived where D nonzero, hence is the meromorphic continuation by identity. In the divided-difference equation the common factor d cancels; one must not retain dn(t)=0 as a pole. Specifically, the divided difference yields c Z_x+l s Z_y=-2k c(E+ksq²)/E. The average equation determinant is -l E(1+ks), and its numerator cancels the remaining 1+ks. Apparent poles from zero focus distances are likewise removable unless E=0.

## Lattice and involutions

Q and R are meromorphic with common lattice <4K,4iJ>. For either V=Q or R,

    V(t+2iJ)=(V_x(t),-V_y(t)),
    V(2K-t)=(V_x(t),-V_y(t)).

These follow from the sn/cn shifts. Define A_V(t)=1/2 sum_{j=0}^{N-1} det(V(t+j delta),V(t+(j+1)delta)). Reindexing gives A_V(t+delta)=A_V(t), and Bezout with delta=tau*(4K/N), gcd(tau,N)=1 gives h=4K/N as a real period. Its imaginary period is 4iJ. We work on the valid reduced torus Lambda=<h,4iJ>; this need not be asserted to be the full period lattice. Reflection and reversed cyclic order cancel signs to give

    A_V(-t)=A_V(t),  A_V(t+2iJ)=-A_V(t).

Here 2K=(N/2)h, so 2K-t and -t are identical modulo h. Since tau is odd, v=tau*h/2 is h/2 modulo h. Since N/2 is even, K=(N/4)h is 0 modulo h.

## Complete pedal pole support and multiplicity

Q is regular at sn/cn poles (divide numerator and denominator by sn; cn/sn is locally regular). Its only other candidate poles are sn(t)=1/k. In <4K,4iJ> these are z0=K+iJ and z0+2iJ, each a double zero of 1-k sn. This completeness follows from the degree-two sn map on <4K,2iJ> and its branch value 1/k, or directly the DLMF pole/shift table and sn differential equation.

Around z0, sn(z0+z)=dn(z)/(k cn(z)) and cn(z0+z)=-i l/(k cn(z)), so Q(z0+z) is even in z and has leading vector (2/k)(1,i) z^-2. In its trace, exactly one Q-vertex is singular per representative of Lambda. The only incident edge combination is 1/2 det(Q(z0+z),Q(z0+z+delta)-Q(z0+z-delta)). The difference vanishes at z=0 because Q is even around z0. Hence its double pole cancels and A_Q has at most simple poles at iJ and 3iJ on Lambda. This statement includes N=4.

## Complete antipedal pole support and double-pole cancellation

R is regular at sn/cn poles because its numerators and denominator have the same maximal order two. Its only possible poles are E=0. These are all simple: sn(t)=±1/(kp) is not a branch value (0<p<1), and cn(t),dn(t) are nonzero. In one common lattice rectangle, their representatives are

    -v+iJ, v+iJ, 2K-v+iJ, 2K+v+iJ,

and their 2iJ shifts. Completeness also follows by translating sn(z+iJ)=1/(k sn z): E=0 iff sn z=±p, whose four real representatives are ±v and 2K±v. On Lambda all first four points coincide at h/2+iJ, and the other four at h/2+3iJ.

Their residues in t, at epsilon*v+iJ and epsilon*v+2K+iJ (epsilon=±1), are respectively

    U_epsilon=( B(epsilon-p)/(2k p r q³),
                 i(epsilon B-p C)/(2k l p q³) ),
    W_epsilon=( B(epsilon+p)/(2k p r q³),
                 i(epsilon B+p C)/(2k l p q³) ).

These follow by E'(epsilon*v+iJ)=epsilon*2rq/p, sn=epsilon/(kp), cn=-epsilon*i r/(kp). At a common trace pole, the only edges with two singular endpoints for N>4 are U_- to U_+ and W_- to W_+. Their double coefficients cancel exactly:

    det(U_-,U_+)=-i B/(l p r q²),
    det(W_-,W_+)=+i B/(l p r q²).

No other singular adjacency can occur unless 4v=2K. With primitive N and 0<v<K this equality forces N=4,tau=1. In that exceptional case the additional edges have double coefficients zero, because W_-=-U_+ and W_+=-U_-. Thus A_R has at most simple poles at h/2+iJ,h/2+3iJ. This establishes the usually delicate double-pole cancellation without overlooking N=4.

## Product conclusion and zero constants

Any even h-periodic function A with A(t+2iJ)=-A(t) obeys A(x+iJ-z)=-A(x+iJ+z) when 2x is an integer multiple of h. If it is regular at x+iJ, it has a zero there (at least first order).

A_Q is regular at h/2+iJ and h/2+3iJ, so vanishes at both. A_R is regular at iJ and3iJ, so vanishes at both. All poles of each factor are at most simple and occur at zeros of the other. Therefore A_Q A_R is holomorphic on the compact torus Lambda, hence constant. This argument permits either factor to vanish identically and a zero constant; it never divides by an area or assumes a nonzero residue. The star-polygon winding tau is retained throughout as the actual cyclic order. Reversing order changes each area sign and leaves the product unchanged.

For F=(-k,0), original polygon antipodality P(u+2K)=-P(u), with the index shift N/2 because tau is odd, maps each focus construction to the other by X->-X. Determinants are unchanged, so each area itself is equal for the two original foci. This does not claim same-focus pointwise antipodality of R, which is false; the correct relation exchanges foci. Scaling from caustic axes (1,l) multiplies each area by scale² and the product by scale⁴; rigid motions preserve area, orientation reversal changes both signs.

## Exact remaining review work

The independent proof above is conditional only on the supplied elliptic parametrization covering the target billiard family. That geometric coverage should be inspected in the submitted proof and authoritative source. Need now read complete candidate proof, test its exact formula against these independent intersections/poles, reproduce symbolic identities and numerical boundary/star checks, and assess whether its stated divisor reasoning uses the valid reduced torus or an erroneous full-period assertion. No candidate verdict yet.
