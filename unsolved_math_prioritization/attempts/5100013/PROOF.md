# k204: the original-pedal area ratio and its exact domain

**5100013 / AMR-050-0013. Full domain-qualified candidate, author turn 1.
Independent review pending. Credited consequence of the prior pedal-trace mechanism.**

## 1. Source target and theorem

Let the billiard ellipse have semiaxes a>b>0 and center O=0. Its fixed caustic
is a strictly nested nondegenerate confocal ellipse of semiaxes alpha>beta>0.
Take a family of least-period N billiard trajectories, with N=2 modulo 4.
For a fixed real point M, project M onto the successive **side lines of the
original orbit** P, in their traversal order, to form its pedal polygon Q_M.
All areas below are signed shoelace areas, not unsigned filled-lobe areas.

There are phase-independent real constants c0>0 and c2, depending on the
family, such that

              A(Q_M)=(c0+c2 |M|²) A(P).                         (1)

The orientation is chosen with turning number 0<tau<N/2; then A(P)>0.
Reversing traversal negates both areas and leaves (1) and the ratio unchanged.
Consequently the source quantity is

              A(P)/A(Q_M)=1/(c0+c2 |M|²)                        (2)

whenever its denominator is nonzero. Every pedal vertex is finite for real
M. The only possible exceptional M form an entire circle: this occurs
exactly when c2<0, at |M|²=-c0/c2. For each point on that circle the pedal
area is zero for **every phase**. If c2>=0 there is no exception.

For convex families c2>0, so (2) is defined for every real M. Primitive
star families are included in (1), and Section 7 gives an exact strictly
noncircular star family with c2<0. Hence the raw quotient cannot be declared
a finite real number for every M in every source family. This does not
refute its invariance on its natural domain. At an exceptional M, A(P)>0
and A(Q_M)=0: it is not a removable 0/0 value or a justified finite extension.

Both source editions retain **Table 3, k204, A/A_M, N=2 modulo4, all M**:
arXiv:2004.12497v11 printedp6 and the published *Fifty New Invariants*,
Arnold Math.J.7(2021), printedp346. Their signed-area and original-pedal
conventions were checked directly. The outer tangent polygon and the inner
contact polygon are not substituted for P. The ellipse pair is nondegenerate;
least period, rather than an arbitrary repeated traversal count, is used.
For this caustic type N=2 cannot occur, so the stated range starts at N=6.

## 2. Prior work, and the new parity specialization

The radial lemma and arbitrary-M pedal-trace argument were previously
proved and separately reviewed in the campaign's k203,a / 5100011,
[PR203](https://github.com/AlecKriebel/Math/pull/203), proof SHA256
`3b8e009c730ce29c59f4240b1b8d52e90970f5061d58d4983512a8979e3ce820`.
Its central-pedal pole mechanism included shared author input from
k203,b / 5100012, [PR204](https://github.com/AlecKriebel/Math/pull/204).
That contribution is author input, not independent review of this target.

The earlier k203,a final theorem concerned N divisible by four. We do not
claim it directly proves a different parity. The underlying meromorphic
argument works for any primitive even N>=4; it is reproduced below, with
each use of parity exposed. For N=2 modulo4 its phase shift instead aligns
with the original area, producing (1). The denominator classification and
exact star exception are also supplied here. This is a shared-method/classical
corollary, not an independent new-discovery claim.

Stachel's canonical parametrization and the DLMF Jacobi identities are
credited primary inputs. Chavez-Caliz's area-product theorem, needed by
the earlier product target, is not needed for this ratio proof.

## 3. Real geometry and radial dependence on M

For a centrally symmetric ordered polygon with N=2m, pair opposite side
lines by central inversion. Write q_i for the foot from O to line i, choose
a unit tangent t_i, and put T_i=t_i t_i^t. The foot from M is q_i+T_i M.
Opposite lines have q_(i+m)=-q_i and T_(i+m)=T_i. All shoelace terms linear
in M therefore cancel. If t_i has angle gamma_i and
Delta_i=gamma_(i+1)-gamma_i, elementary trigonometry gives

 det(T_i M,T_(i+1) M)
  =|M|²/4 [sin(2Delta_i)+sin(2phi-2gamma_i)
                                -sin(2phi-2gamma_(i+1))],

where M=|M|(cos phi,sin phi). The last two terms telescope around the full
ordered polygon. Thus

        A(Q_M)=A(Q_0)+C |M|²,
        C=(1/8) sum_i sin(2Delta_i).                           (3)

This holds for self-intersecting polygons as well. It does not yet assert
that either coefficient divided by A(P) is independent of phase. It does
show invariance under M -> -M and M -> J M for J=diag(1,-1), at each fixed
phase. Choosing the signs of the individual t_i does not affect (3).

Use Stachel's published Theorem4.3/(4.9), p1614, with modulus
k=sqrt(alpha²-beta²)/alpha, k'=beta/alpha, and complete integrals K,K'.
The orbit and contact points are

 P(w+j delta)=(-a sn(w+j delta), b cn(w+j delta)),
 B(w+v+j delta)=(-alpha sn(w+v+j delta), beta cn(w+v+j delta)),

where

 v=2K tau/N in (0,K), delta=2v, gcd(tau,N)=1,
 a=alpha dn(v)/cn(v),             b=beta/cn(v).                 (4)

Jacobi functions use modulus k, not the software parameter k². Since N is
even, tau is odd and m delta=2K tau, so opposite vertices and side lines
are centrally paired. Hence (3) applies.

Define the meromorphic cyclic trace

                   S(u)=sum_(j=0)^(N-1) dn(u+j delta).

The addition theorem gives the exact signed-area identity

 A((-A sn(u+j delta),B cn(u+j delta))_j)
          = A B sn(v)cn(v)/dn(v) S(u).                         (5)

Indeed an edge centered at x has determinant
`2AB sn(v)cn(v)dn(x)/(1-k²sn²(x)sn²(v))`; also
`dn(x-v)+dn(x+v)=2dn(x)dn(v)/(1-k²sn²(x)sn²(v))`.
Summing the half-determinants proves (5). In particular

        A(P(w))=C_A S(w),
        C_A=ab sn(v)cn(v)/dn(v)>0.                             (6)

On the real line dn>0, so S(w)>0. No convexity assumption is used in (5).

## 4. The general-even meromorphic pedal-trace lemma

The tangent line to the caustic at B(u) is n(u)^t X=1, with

 n(u)=(-sn(u)/alpha,cn(u)/beta),        n(u)^t n(u)=dn²(u)/beta².

Its perpendicular foot from M is

 q_M(u)=q_0(u)+[I-n(u)n(u)^t/(n(u)^t n(u))]M,
 q_0(u)=(-alpha k'^2 sn(u),beta cn(u))/dn²(u).                   (7)

For complex u these formulas use the bilinear transpose, not complex
conjugation. The ordered pedal-area function is

 T_M(u)=(1/2)sum_j det(q_M(u+j delta),q_M(u+(j+1)delta)),
        A(Q_M(w))=T_M(w+v).                                  (8)

Its only possible singularities come from zeros of dn, namely
r=K+iK' modulo 2K and 2iK'. At common poles of sn,cn,dn, the vector q_0
is removable and the quotient matrix in (7) is regular. At a zero of dn,
q_M has at most a double pole and is even about that zero. At r, this is
immediate from

 sn(r+z)=dn(z)/(k cn(z)),
 cn(r+z)=-i k'/(k cn(z)),
 dn(r+z)=i k' sn(z)/cn(z).

Period transformations give the same local evenness at every such point.
These are standard Jacobi quarter-period formulas, not numerical assumptions.

If one cyclic vertex is singular, its two neighboring vertices are regular,
because 0<delta<2K. Its incident area terms combine into

 (1/2) det(q_M(r+epsilon),
              q_M(r+epsilon+delta)-q_M(r+epsilon-delta)).       (9)

The second factor is an odd holomorphic function of epsilon and vanishes
at zero. Thus the at-most-double even pole drops to at most a simple pole.
Simultaneous singular vertices differ by N/2 indices, so are nonadjacent
for N>=4. Each incident edge can be assigned to exactly one such vertex;
there is no uncounted product of adjacent singularities. Hence every pole
of T_M is at most simple.

Formula (7) also gives

 q_M(u+2K)=-q_(-M)(u),
 q_M(u+2iK')=J q_(JM)(u),               det J=-1.

The real radial identity (3), extended meromorphically by the identity
theorem, gives T_(-M)=T_(JM)=T_M. Therefore T_M has period 2K and
anti-period 2iK'. Cyclic reindexing gives period delta. Put h=2K/m.
Since 2K=m h and delta=tau h with gcd(tau,m)=1, h is a period by Bezout.
On the compact torus C/(h Z+4iK' Z), T_M has at most two simple poles,
represented by r and r+2iK'.

The comparison function S(u+K) has exactly the same two simple poles,
period h, and anti-period 2iK'. Its residue is nonzero: the m distinct real
translates exhaust the reduced orbit and each occurs twice in the N-term
sum, with identical residues because dn has period 2K. No cancellation
is hidden in this multiplicity. Match the first residue of T_M with a
scalar multiple of S(u+K); anti-periodicity matches the second. The
remaining function is holomorphic on the compact torus, hence constant,
and its anti-periodicity forces that constant to vanish. Thus

                   T_M(u)=c(M) S(u+K).                         (10)

This lemma holds for every fixed real M, including c(M)=0, and for every
primitive even N>=4. The argument has not yet used N=2 modulo4. Since S
is positive on the real line and T_M real, c(M) is real.

## 5. The target parity, and phase-independent coefficients

Now m=N/2 is odd. Both m and tau are odd, so

             K+v=((m+tau)/2)h

is an integer multiple of the trace period h. Equations (8), (10) give
`A(Q_M(w))=c(M) S(w)`. Divide by (6), whose area is never zero, to obtain
phase-independent A(Q_M)/A(P) for every M, including zero pedal area.
Applying (3) at M=0 and at any fixed unit vector then shows that the same
constant has the form c0+c2|M|², with both c0,c2 independent of phase.
This proves (1).

To prove c0>0, consider the continuous angle psi(u) of n(u) for real u.
Direct differentiation gives det(n,n')=dn(u)/(alpha beta)>0, while
n(u+2K)=-n(u). Therefore psi increases by pi over 2K. Because delta lies
strictly between0 and2K, every angle difference psi(u+delta)-psi(u) lies
strictly between0 andpi. The vector q_0 is a positive multiple of n, so
each consecutive determinant in its shoelace sum is strictly positive.
Thus A(Q_0)>0, and c0=A(Q_0)/A(P)>0.

The denominator classification in Section1 now follows immediately from
the real quadratic c0+c2|M|². It is a statement about the whole phase
family, not a numerical zero at one isolated trajectory.

## 6. Convex families have no exceptional real point M

For the convex family tau=1, let Delta_1,...,Delta_m be the successive
side-normal angle changes over half the centrally symmetric polygon.
They are positive and sum to pi; m>=3. We claim

                    sum_(i=1)^m sin(2Delta_i)>0.               (11)

If all Delta_i<=pi/2, every summand is nonnegative and at least one is
positive. Otherwise there is exactly one Delta_j>pi/2. The remaining
positive angles sum to pi-Delta_j<pi/2. For positive x,y with x+y<pi,
`sin x+sin y-sin(x+y)=4sin(x/2)sin(y/2)sin((x+y)/2)>0`.
Applying this repeatedly to twice the remaining angles shows that their
sine sum exceeds sin(2pi-2Delta_j)=-sin(2Delta_j). This proves (11).

The second half of the polygon repeats these differences, so (3) gives
C>0 and c2=C/A(P)>0. Together with c0>0, this proves A(Q_M)>0 for all
real M in every convex source family. Convexity is used only here.

## 7. Exact noncircular star family with an exceptional circle

Take

 k=1/4,    alpha=1,    beta=k'=sqrt(15)/4,
 N=10,     tau=3,      v=3K/5,
 a=dn(v)/cn(v),        b=k'/cn(v).                              (12)

Stachel's theorem gives a genuine primitive ten-period star family because
gcd(3,10)=1. The caustic is strictly inside the billiard ellipse:
`a²-b²=k²>0` and `a²-alpha²=b²-beta²=beta² sn²(v)/cn²(v)>0`.
All quantities in (12) are exact elliptic-function values.

Let theta=am(u,k), so theta'=dn(u) lies between k' and1. For the angle
psi of n=(-sin(theta),cos(theta)/k'),

 dpsi/dtheta = k'/(k'^2 sin²(theta)+cos²(theta)),

which lies between k' and1/k'. Hence dpsi/du lies between k'^2 and1/k'.
The elementary integral bounds pi/2<=K<=pi/(2k') and delta=6K/5 imply
for every real u

       (3pi/5) k'^2 <= psi(u+delta)-psi(u)
                           <= (3pi/5)/k'^2.

With k'^2=15/16, this is

       9pi/16 <= Delta_i <= 16pi/25.

The whole interval is strictly inside (pi/2,pi). Therefore every
sin(2Delta_i)<0, and C<0 in (3), at every phase. Section5 gives
A(Q_0)>0. Define exact positive numbers at, say, phase w=0 by

 B_0=(1/2)sum_j det(q_0(v+j delta),q_0(v+(j+1)delta)),
 C_0=(1/8)sum_j sin(2[psi(v+(j+1)delta)-psi(v+j delta)]),
 rho²=-B_0/C_0 >0.                                            (13)

Equations (12)–(13) are an exact definition, not a floating-point root
certificate. For every fixed M with |M|=rho, equation (1) proves
A(Q_M(w))=0 for all phases w. The feet themselves remain finite because
the real squared normal norm is positive. The numerator A(P(w)) remains
positive. Thus the raw ratio at these M is undefined everywhere in this
strict noncircular star family; its invariant value on other M is (2).
The sign certificate uses rational multiples of pi and exact inequalities,
not an unquantified perturbation from a circle or numerical evidence.

## 8. Scope and reproducibility

Primitive stars, arbitrary fixed M, signed traversal areas and both possible
traversal orientations are retained. Multiple traversals of an already
admissible primitive orbit multiply both areas by the same number and keep
their ratio; repeating an odd primitive orbit to obtain an even listed count
does not meet the hypothesis. Degenerate/hyperbolic caustics and circular
billiards are not silently included in the complex proof.

The prior k203 mechanism and all classical inputs retain full credit. No
historical novelty claim is made. The proof supplies the all-period result;
exact finite algebra and separately labeled numerical controls support its
implementation and conventions. Full separate review is required before
publication or any final source-status correction.
