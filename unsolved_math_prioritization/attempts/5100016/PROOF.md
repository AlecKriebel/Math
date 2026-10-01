# k304: the outer-pedal area ratio and its exact domain

**5100016 / AMR-050-0016. Full domain-qualified candidate, author turn1.
Independent review pending. Credited companion to the existing pedal-trace work.**

## 1. Exact target and claimed result

Let E be x²/a²+y²/b²=1, a>b>0, with a fixed strictly nested nondegenerate
confocal elliptical caustic C of semiaxes alpha>beta>0. Let P_i traverse
a primitive billiard orbit of least period N divisible by four. Let R_i
be the intersection of the tangents to E at P_i and P_(i+1), so R is the
outer tangent polygon. Its side R_(i-1)R_i is the tangent at P_i.
Project any fixed real M onto those tangent side lines to obtain Q'_M.
Write A'=A(R), B_M=A(Q'_M), using ordered signed shoelace areas.

There are phase-independent real constants c0>0 and c2 such that

                    B_M=(c0+c2 |M|²) A'.                     (1)

For a positively oriented primitive orbit with turning number
0<tau<N/2, A'>0. Reversing traversal negates both areas, leaving the ratio
unchanged. Thus the source ratio is

                    A'/B_M=1/(c0+c2 |M|²)                    (2)

where its denominator is nonzero. Every real foot and outer vertex is
finite. If c2>=0 there is no exceptional real M. If c2<0, exactly the
circle |M|²=-c0/c2 is exceptional, and B_M vanishes identically over the
entire phase family for each M on it. The numerator remains nonzero.
This is a raw undefined quotient, not a removable0/0 value.

For convex families c2>0 when N>=8. At N=4, c2=0 and c0=1/2, so
A'/B_M=2 for every M. Primitive star families are included in (1);
Section7 constructs an exact N=8 star family with an exceptional circle.
The identity and the invariant on its natural domain do not assert that
all raw quotients in every star family are finite.

Both full source editions have the same **Table4, k304**: A'/A'_M,
N=0mod4, all M (arXiv2004.12497v11 p6; final *Fifty New Invariants*,
Arnold Math.J.7(2021), p346). This is the pedal of the **outer tangent
polygon**, not the original billiard chord pedal or the inner polygon.
Signed area, arbitrary fixed M, strict ellipse pair and least period are
kept explicit. Repetition does not supply a missing primitive parity.

## 2. Attribution and why a new pole check is needed

The classical Jacobi/compact-torus method and the radial identity are shared
with reviewed campaign k203,a (5100011, PR203), its shared central-pedal
input k203,b (5100012, PR204), and the related k204 (5100013, PR250) corollary.
The reviewed outer-pedal proof k303,a (5100014, PR201, exact candidate hash
`e48aa989fb9282d09fdf58e7e4f6eee78e757ff0686f4cc35dc691e21f3d1fd3`)
uses a flag-curve version of the adjacent-pole cancellation below for its
other even parity. None of those final target theorems is simply relabeled
as k304; we reproduce the needed calculations with the correct new shift.
The N=4 coincident-pole pattern is checked explicitly.

Stachel's published Theorem4.3/(4.9), p1614, supplies the canonical
parameters. DLMF22.4,22.8,22.13 and22.16 supply the Jacobi identities.
The elementary polarity relation below has also been used in earlier
campaign work. No novelty or priority claim is made, and prior author
contributions do not count as independent review of this package.

## 3. Area trace and radial dependence

Put k=sqrt(alpha²-beta²)/alpha in(0,1), k'=beta/alpha, with complete
integrals K,K'. In Stachel's convention the real orbit and caustic contacts
are

 P(u)=(-a sn u,b cn u),          B(u)=(-alpha sn u,beta cn u),
 v=2K tau/N in(0,K),            delta=2v,
 a=alpha dn(v)/cn(v),           b=beta/cn(v),
 P_i=P(w+i delta),              B_i=B(w+v+i delta).             (3)

The functions use modulus k. Set m=N/2, and S(u)=sum_(i=0)^(N-1)dn(u+i delta).
Since tau is odd, P_(i+m)=-P_i and the tangent side lines are centrally
paired. For any such centrally paired ordered lines, the feet obey

              B_M=B_0+C |M|²,
              C=(1/8)sum_i sin(2Delta_i),                      (4)

where Delta_i is the change of their unit-tangent angles. To check this,
write the foot as q_i+t_i t_i^t M. Opposite q_i cancel the terms linear in M.
The quadratic determinant equals |M|²/4 times
`sin(2Delta_i)+sin(2phi-2gamma_i)-sin(2phi-2gamma_(i+1))`;
the last two terms telescope. Convexity is not used. In particular B_M is
unchanged by M -> -M or by M -> J M, J=diag(1,-1), at a fixed phase.

The Jacobi addition theorem gives

 A((-A sn(u+i delta),B cn(u+i delta))_i)
           =AB sn(v)cn(v)/dn(v) S(u).                          (5)

For an edge centered at x, its determinant is
`2AB sn(v)cn(v)dn(x)/(1-k²sn²(x)sn²(v))`. The dn addition identity turns
this into the sum of the two endpoint dn terms and proves (5).

Polarity identifies the outer vertices with a fixed linear image of the
contact points. The polar of R_i with respect to E is the chord P_i P_(i+1),
which is the tangent to C at B_i. Their normalized equations therefore give

 R_i=diag(a²/alpha²,b²/beta²) B_i.

An antipodal chord cannot touch a strictly nested ellipse, so these outer
vertices are finite. Consequently

 A'(w)=C_R S(w+v),
 C_R=a²b²/(alpha beta) sn(v)cn(v)/dn(v)>0.                       (6)

For real w, S>0, so A'>0, including primitive stars. No area-product theorem
or quotient by a possibly zero pedal area is used.

## 4. Outer pedal vertices: poles are simple, in adjacent pairs

The tangent to E at P(u) is n(u)^t X=1, where

 n(u)=(-sn(u)/a,cn(u)/b),
 q_M(u)=M+(1-n(u)^t M)n(u)/(n(u)^t n(u)).                       (7)

For complex u use the bilinear transpose, never a Hermitian norm. Put
s_v=sn v,c_v=cn v,d_v=dn v and

 D(u)=d_v²-k² c_v² sn²(u),       n(u)^t n(u)=D(u)/(b² d_v²).     (8)

This denominator differs from the inner/chord-pedal denominator dn²(u).
The poles cannot be handled by copying the double-pole even-germ argument.

At a common Jacobi pole iK' modulo2K,2iK', the leading squared normal
coefficient is nonzero, since 1/a²-1/b² is nonzero. Thus n/(n^t n) is
removable and n n^t/(n^t n) is regular; q_M has no pole there.
The zeros of D are precisely

                 r-v and r+v,       r=K+iK',                 (9)

modulo2K and2iK'. Indeed sn(r+z)=dn(z)/(k cn(z)), and sn² is a degree-two
elliptic function on that period lattice. The two displayed zeros are
distinct since0<v<K. Their simplicity can also be seen directly:

               D'(r+v)=-2 k'^2 s_v d_v/c_v !=0,
               D'(r-v)=+2 k'^2 s_v d_v/c_v.

All possible poles of q_M are therefore at most simple. At both of the
points in(9), the normal is exactly

                    n(r-v)=n(r+v)=-(1,i)/(alpha k).            (10)

At real2K translates its sign reverses; at imaginary2iK' translates its
second component reverses. Within either fixed imaginary row, all these
normals span the same isotropic complex line.

Define the meromorphic signed area

 U_M(u)=(1/2)sum_i det(q_M(u+i delta),q_M(u+(i+1)delta));
                         B_M(w)=U_M(w).                       (11)

The two real pole types in(9) differ by delta. Hence adjacent vertices can
be singular simultaneously. If both are singular, their residues in the
same local phase coordinate are scalar multiples of the same normal line
in(10). The coefficient of the possible order-two term in their determinant
is therefore zero. This remains true if one residue vanishes for a special M.
If just one vertex is singular, its determinant has at most a simple pole
already. Thus **each area summand individually** has at most a simple pole.

For N>=8 the four singular indices are two adjacent pairs and their
opposites. For N=4 every index can be singular at once; all four residue
vectors still lie in the same isotropic line, so the same argument applies
to all four edges, including the cyclic last edge. No separation assumption
from the N=2mod4 outer-pedal proof is being reused at N=4.

## 5. Trace uniqueness and the N=0mod4 alignment

As in the real radial identity, the meromorphic area functions satisfy
U_(-M)=U_(JM)=U_M, by the identity theorem. Formula(7) gives

 q_M(u+2K)=-q_(-M)(u),          q_M(u+2iK')=J q_(JM)(u).

Taking determinants shows that U_M has period2K and anti-period2iK'.
Cyclic reindexing adds period delta. With h=2K/m, gcd(tau,m)=1, the real
periods2K=m h and delta=tau h generate h. On the compact torus
C/(h Z+4iK' Z), the two real pole types in(9) coincide because their
difference is delta. There remain at most two simple poles, separated by
2iK'.

The comparison function S(u+K+v) has exactly these two simple poles:
its first pole is at u=iK'-K-v, congruent to r-v modulo2K. The cyclic
trace has nonzero residue there because each of its m distinct real
translates occurs twice with the same residue. It has the same period h
and anti-period2iK'. Subtract a scalar multiple matching the first residue;
the second cancels by anti-periodicity. The remainder is holomorphic on
the compact torus, hence constant, and anti-periodicity makes it zero.
Therefore, for every fixed real M,

                    U_M(u)=d(M) S(u+K+v).                     (12)

The scalar is real; evaluate on the real line, where the trace is positive.
The argument so far is valid for every primitive even N>=4.

Now N is divisible by four, so m is even and K=(m/2)h is a period of S.
Equations(6),(11),(12) imply

                   B_M(w)=d(M) S(w+v)=d(M)A'(w)/C_R.

The phase-independent constant is radial in M by(4). Evaluate at M=0
and one unit vector to obtain exactly c0+c2|M|² in(1).

For positivity of c0, the angle psi(u) of n(u) increases strictly:
`det(n,n')=dn(u)/(ab)>0`, and n(u+2K)=-n(u). Hence each change over
0<delta<2K lies strictly between0 andpi. The origin foot q_0 is a positive
multiple of n, so every consecutive determinant in B_0 is positive.
Thus c0=B_0/A'>0. The complete circle-or-empty denominator classification
in Section1 follows from(1).

## 6. Convex cases, including the four-period boundary case

For tau=1, the half-period normal turns Delta_1,...,Delta_m are positive
and sum to pi. If m>=3, their doubled sine sum is strictly positive.
If all Delta_i<=pi/2 this is immediate; otherwise there is one larger
angle, and the positive remaining angles sum to less thanpi/2. Repeatedly
using

 sin x+sin y-sin(x+y)=4sin(x/2)sin(y/2)sin((x+y)/2)>0

for positive x,y with x+y<pi shows that their sine sum exceeds the absolute
value of the one negative summand. The opposite half repeats this sum.
Thus C>0 in(4) and c2>0 for convex N>=8.

At N=4, m=2 and Delta_2=pi-Delta_1, so C=0 exactly. Formula(1) shows
c0 is phase-independent. At phase w=0 the orbit is on the four axis
endpoints; its outer polygon is the rectangle with vertices(±a,±b), and
the center feet form the axis-endpoint rhombus. Their areas are4ab and2ab.
Therefore c0=1/2, proving the exact all-M ratio2 at N=4.

## 7. Exact strictly noncircular star denominator exception

Choose

 k=1/4, alpha=1, beta=k'=sqrt(15)/4,
 N=8, tau=3, v=3K/4,
 a=dn(v)/cn(v), b=k'/cn(v).                                   (13)

This is a primitive star by Stachel, since gcd(8,3)=1. Strict confocality
follows from a²-b²=k² and
`a²-1=b²-k'^2=k'^2 sn²(v)/cn²(v)>0`.
Let r_E=b/a=k'/dn(v), so k'<=r_E<1. Writing theta=am(u), the angle of
n=(-sin(theta)/a,cos(theta)/b) satisfies

 dpsi/dtheta=r_E/(r_E² sin²(theta)+cos²(theta)).

It lies between r_E and1/r_E, hence between k' and1/k'. Since
theta'=dn(u) lies between k' and1, dpsi/du lies between k'^2 and1/k'.
Together with pi/2<=K<=pi/(2k') and delta=3K/2, this yields

       45pi/64 <= psi(u+delta)-psi(u) <= 4pi/5.

This whole interval is strictly inside(pi/2,pi). Every doubled-angle
sine in(4) is strictly negative, so C<0, while B_0>0. Define, at w=0,

 rho²= - [ (1/2)sum_j det(q_0(j delta),q_0((j+1)delta)) ]
             /[ (1/8)sum_j sin(2[psi((j+1)delta)-psi(j delta)]) ].       (14)

This exact elliptic-function expression is positive and finite. For every
fixed M with |M|=rho, equation(1) proves B_M(w)=0 for all phases. Real
feet remain finite because n^t n>0. The outer area A' stays positive.
No finite raw quotient exists at these M; other M retain the invariant(2).
The sign and all-phase assertion are proved by exact bounds and the identity,
not by numerical near-zero sampling or an unquantified circular limit.

## 8. Interpretation and verification

The theorem proves the target ratio on its natural domain and explains
exactly how the source's all-M wording must be read for star families.
It includes all fixed real M in the division-free identity. Neither a moving
M nor unsigned lobe area is substituted. No assertion is made for hyperbolic
or degenerate caustics; repeated traversal does not replace least period.

Prior campaign/shared-author mechanisms and published primary inputs are
credited. The new parity and adjacent-pole/N4 checks are explicit. Exact
algebra and separately labeled non-interval diagnostics supplement the
written all-period proof, not replace it. A separate independent full review
is required before any PR or status promotion. No novelty claim is made.
