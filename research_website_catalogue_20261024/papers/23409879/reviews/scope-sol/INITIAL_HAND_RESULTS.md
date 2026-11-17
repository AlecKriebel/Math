# Source-first reconstruction and controls

This is an informed source-only reconstruction, not a scientific verdict.
It was written after personally reading all393 actual TeX lines and all six
native PDF pages/text/fresh pixels, and before any current174 root/peer
finding, support program, README, theorem-contract, audit/result/proof ledger
or foreign mathematical body. Source bibliography/priority statements below
are publisher assertions, not independently established provenance.

## Exact target and model

Fix a>b>0 and0<lambda<b^2, alpha^2=a^2-lambda,
beta^2=b^2-lambda, c^2=a^2-b^2=alpha^2-beta^2. The ellipse and
caustic are proper, nested, noncircular, nondegenerate confocal ellipses.
Original foci are (+/-c,0). Assume the physical billiard for this fixed pair
has primitive least period N>=3. For each admissible coprime winding tau,
0<tau<N/2 after reversal, take ALL phases of that family. Q_j is the finite
intersection of the boundary tangents at consecutive impacts, NOT an impact,
pedal foot, inverse image, or a tangent to the caustic. The claim is that
each ordinary positive-distance product R_+ and R_- over exactly the least
N outer vertices is phase-constant iff4 divides N; when constant they agree.
Every admitted star winding is included. An r-fold traversal cannot change
the yes/no constancy of the primitive product. No assertion is made for a
circle, hyperbolic/collapsed caustic, separatrix, N=2 or arbitrary repeated
list length. The locus of Q need not be confocal with E; replacing the foci
by the locus's foci changes the problem.

The principal imports to verify after this freeze are the actual canonical
physical-billiard translation interface, its least-period/star conventions,
and the Jacobi torus/shift/pole identities. Algebra below is reconstructed
using the source's formulas and learned basic Jacobi theory. It does not
pretend those actual primary passages have already been read.

## Canonical variables and physical geometry

Let k^2=c^2/alpha^2 and k'=beta/alpha. Both lie strictly between0 and1.
From b=beta/cn(v), a necessary v has

 sn^2(v)=lambda/b^2=:t in(0,1), cn^2(v)=1-t=:q.

The monotone real sn segment0<v<K provides such v. The other axis equation
is consistent, independently of a numerical billiard:

 alpha^2*(1-k^2*t)/q
 =[(a^2-lambda)b^2-c^2*lambda]/(b^2-lambda)=a^2.

Thus the claimed two axis equations are not independent restrictions that
silently exclude an allowed confocal pair. The remaining physical import is
that P(u)=(-a sn u,b cn u) advances by delta=2v for the actual reflection
map with the stated caustic, covering the real phase circle and star winding.
The source's displayed chord tangent is a direct check of its caustic.

Write s=sn u,z=cn u,d=dn u,h=sn v,C=cn v,D=dn v and
D0=1-k^2*s^2*h^2. On the real axis D0>0, h,C,d>0.
Using sn(u+/-v)=(sCD+/-hzd)/D0 and
cn(u+/-v)=(zC-/+shdD)/D0, the determinant of the two boundary-tangent
rows is, up to orientation,

 2*h*C*d*(s^2*D^2+z^2)/(a*b*D0^2)=2*h*C*d/(a*b*D0)>0.

This calculation includes s=0 or z=0 without dividing by either. Adding
and subtracting the two tangent equations gives exactly the source's system.
Its solution is Q=(-aD*s/C,b*z/C). The original axis equations imply
A=aD/C=a^2/alpha and B=b/C=b^2/beta. Moreover

 Qx^2/a^2+Qy^2/b^2-1
 =(s^2*D^2+z^2-C^2)/C^2=h^2*dn^2(u)/C^2>0.

Every real outer point is therefore finite and strictly outside E. Neither
focus, which lies inside E, is an outer point. There is no zero distance
or sign choice hidden by taking positive products. The offset u0+v in
the outer sequence merely reparametrizes phase. Real antipodal shift2K
sends Q to -Q. The linear Q map has positive A,B, so it has the same4K
real point period as the boundary parametrization, not a hidden2K period.

## Independent coefficient comparison for the paired factor

Put kappa=k^2,t=sn^2(v),q=1-t and

 U=1-2kappa*t+kappa*t^2,
 V=1-2t+kappa*t^2,
 W=1-kappa*t^2.

Direct expansion, not a stored certificate, gives

 A=alpha*(1-kappa*t)/q, B=alpha*k'/q,
 A^2-B^2=alpha^2*kappa*V/q^2,
 B^2+c^2=alpha^2*U/q^2.

For S=sn^2(u), H is

 alpha^4/q^4 * [(U+kappa*V*S)^2-4*kappa*(1-kappa*t)^2*q^2*S].

Its constant and S^2 coefficients equal those of
(1-kappa*S)(U^2-kappa*V^2*S). Equality of S coefficients is exactly
(U+V)^2=4q^2(1-kappa*t)^2, obtained from
U+V=2q(1-kappa*t). This checks the whole quadratic identity.
The source's double-angle identities cn(delta)=V/W and dn(delta)=U/W
then yield H=C_v*dn^2(u)[dn^2(delta)-k^2*cn^2(delta)*sn^2(u)],
where C_v=alpha^4*W^2/q^4>0. Note V can be negative; no assumption
about A>B, convexity or cn(delta)>0 was inserted.

There is also a useful positivity control independent of complex divisors:
for S in[0,1], the bracket is at least
dn^2(delta)-k^2*cn^2(delta)=k'^2>0; dn^2(u)>=k'^2.
Thus H>=C_v*k'^4>0 on the entire real phase circle. H has dimension
length^4; R has length^N. These dimensions agree in every norm identity.

## Torus, collisions and the exceptional degree drop

Conditional on the stated actual Jacobi interfaces, use
T=C/(2K Z+2iK' Z), p=iK'. sn^2 has its one double pole at p;
dn^2 has that pole and a double zero at p+K. For delta not K, the
bracket has a double pole because k^2*cn^2(delta) is nonzero. Its
zeros, from sn(z+K+iK')=dn z/(k cn z), are p+K+/-delta.
Coincidence requires2delta in2K Z; with0<delta<2K the only candidate
is delta=K. Neither zero is p or p+K in the nonexceptional range:
at p it is a pole; at p+K the value is
dn^2(delta)-cn^2(delta)=k'^2*sn^2(delta)>0.
Two distinct zeros exhaust the degree-two bracket zero divisor, so they
are simple. Therefore the full H divisor is

 2[p+K]+[p+K+delta]+[p+K-delta]-4[p].

At delta=K, the bracket is the nonzero constant k'^2. Keeping the
generic four-pole divisor there would be false. The actual divisor is
2[p+K]-2[p]. Closure delta=4K*tau/N and coprimality imply
4tau=N; hence the sole primitive exception is N=4,tau=1.

The exceptional case has a separate real algebra control. V=0 implies
t=1/(1+k'), q=k'/(1+k'), dn^2(v)=k', W=2q, and A=B=alpha(1+k').
The outer locus happens to be a circle in this case, while the ORIGINAL
foci remain distinct. dn(u+K)=k'/dn(u) gives
F=H(u)H(u+K)=C_v^2*k'^6 and R_+=R_-=C_v*k'^3
=4alpha^4*k'*(1+k')^2. At u=0 the four outer points are the axis
points of that circle: direct distance multiplication gives A^4-c^4,
equal to that expression. The tempting expression (A^2-c^2)^2 would
instead be wrong. This is a consistency check, not a new claimed theorem.

## Cyclic subgroup and necessity for odd periods

The real translation subgroup G=<delta> of T has order
L=N/gcd(N,2), because delta/(2K)=2tau/N. For the nonexceptional case,
summing divisors of H(u+jdelta) for j=0,...,L-1 gives

 div F=4 O_(p+K)-4 O_p,
 O_x=sum_(g in G)[x+g].

Translations by +/-delta only permute G; this incorporates collisions
between different factors. The cosets are equal iff K belongs to G and
otherwise disjoint. The relevant uniqueness of order2 is on the REAL
circle R/(2K Z), not on the whole complex torus, which has three nonzero
two-torsion points. Since G is cyclic, K is in it iff L is even, which
is equivalent to4|N. At N=4 the same cancellation uses coefficient2.

Controls before any program: N3 gives L3 and disjoint cosets; N4 L2
with the exceptional degree2; N5 L5; N6 L3; N8 L4; N10 L5; N12 L6.
The same result holds for star generators, e.g.N8,tau3 generates the
same order4 subgroup as tau1; N5,tau2 still has odd order5 and no K.
A noncoprime length12,tau2 is actually least period6, not an eligible
least12 input. This is precisely why repeated list length cannot be used.

No zero/pole coset lies on the real phase circle, since p has imaginary
part K' modulo2K'. A zero divisor makes F holomorphic on a compact
connected torus and therefore constant; positivity fixes a positive value.
A disjoint nonzero divisor makes it nonconstant.

For every N, Q(u+2K)=-Q(u) gives the PHASE identity
R_-(u)=R_+(u+2K), whether or not the antipode belongs to the same orbit.
Also R_+^2 R_-^2=F^(N/L). If either R were constant on real phases,
the other would be constant, so that meromorphic power would be constant
on a real interval. The identity theorem, in a pole-free neighborhood,
would make it constant globally, contradicting the nonzero divisor when
4 does not divide N. This closes the odd-period logical objection without
falsely pairing an antipode inside an odd primitive orbit.

For even N, tau is odd and Ldelta=2K*tau pairs actual orbit points.
Consequently R_+=R_- as functions and R_+^2=F. In particular when4|N,
the unique positive real square root yields constancy. No global complex
square-root branch of the distance was used. The same observation also
shows that equality of the two focal products alone is NOT constancy for
N congruent2 mod4.

## Physical same-caustic six-period control, by hand

Set a=3,b=1,lambda=9/16, c^2=8, alpha^2=135/16,beta^2=7/16.
Both listed six-point orbits have distinct boundary points in the source's
order, so physical reflection plus these distinct points establishes least6.

First orbit: (3,0),(9/4,sqrt7/4),(-9/4,sqrt7/4),then negatives.
Boundary equation at the nonaxis points is9/16+7/16=1. A sloping
chord has line sqrt7*x+3y=3sqrt7; tangency to the caustic follows from
(135/16)*7+(7/16)*9=63=(3sqrt7)^2. The middle chord y=sqrt7/4 is
also tangent. Sign/axis symmetries supply the remaining chords.
At (3,0), incoming/outgoing unit vectors (3/4,sqrt7/4) and
(-3/4,sqrt7/4) satisfy reflection. At P=(9/4,sqrt7/4), incoming
v=(-3/4,sqrt7/4), outgoing(-1,0), normal n=(1,sqrt7)/4:
v dot n=1/4, |n|^2=1/2, so v-2(v dot n)n/|n|^2=v-n=(-1,0).
The remaining impacts follow by the same symmetries.

Second orbit: (0,1),(-3sqrt15/4,1/4),(-3sqrt15/4,-1/4),then negatives.
Boundary membership is15/16+1/16=1. A sloping chord is
-x+sqrt15*y=sqrt15; caustic tangency is
135/16+15*7/16=15. The middle vertical chord is tangent at the left
caustic extremum. At (0,1), incoming/outgoing units
(-sqrt15/4,1/4) and(-sqrt15/4,-1/4) reflect normally. At its next
impact, incoming v=(-sqrt15/4,-1/4), outgoing(0,-1),
n=(-sqrt15/12,1/4), v dot n=1/4 and |n|^2=1/6;
v-3n=(0,-1). Again symmetries give the rest.

Solving actual boundary tangent lines gives first triples of outer points
(3,1/sqrt7),(0,4/sqrt7),(-3,1/sqrt7) and
(-9/sqrt15,1),(-12/sqrt15,0),(-9/sqrt15,-1), then negatives.
For the first triple, H values are288/49,5184/49,288/49.
For the second they are864/25,64/25,864/25. Antipodal pairing gives
ordinary products20736/343 and6912/125; their ratio is375/343, not1.
Two traversals square that nonunit ratio despite nominal length12.
Thus this is a PHYSICAL same-E/same-C countercontrol to a repeated-list
interpretation, not an arbitrary six-tuple, a different caustic or a
computed squared-product mistaken for the ordinary product.

## Boundaries and post-freeze falsification plan

Uniform scaling multiplies R by scale^N and H by scale^4, preserving
the criterion. Reversing the winding permutes factors. Noncoprime labels
must reduce to the least period; positivity makes x->x^r injective, so
repetition cannot restore constancy. A circle has coalesced center foci and
outer-star radius a/cos(pi*tau/N), constant in phase for all admitted N;
it is a real counterexample to removing noncircularity, not to this claim.
lambda0,lambda=b^2,k0,k1,hyperbolic caustics and N2 leave the hypotheses.
At N2, consecutive antipodal boundary tangents would be parallel; the
source's finite-tangent determinant requires v<K. No limiting promotion.

After the seal: read the actual Stachel4.3/(4.9) interface for the entire
proper-confocal/star/least-period physical scope, actual DLMF22.4/22.8
period/pole/shift and addition identities, and targeted Ferudun Theorem1/(5)
for the explicitly overlapping positive-direction credit. Other provenance
and historical dates remain bounded source assertions unless actually
accessed. Do not infer novelty/current openness from searches.

Inspect only necessary original support code/dependencies in full before
at most one meaningful ordinary finite native route. No optimized variant,
installation, retry, harness or numerical campaign. Actual output/exit/error
limits must be retained and inspected. Native finite checks can falsify
implementation/fixtures, not prove all real phases or all N by sampling.
If a substantive full-claim gap remains, record it and defer the original;
do not repair/narrow into a promoted substitute. No current verdict is
fixed by this initial conditional reconstruction. Follow-up defaults null.
