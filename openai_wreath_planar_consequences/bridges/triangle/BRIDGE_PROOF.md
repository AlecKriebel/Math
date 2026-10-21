# Independent triangle bridge audit

Timestamp: 2026-10-07 UTC (2026-10-06 America/Los_Angeles).
Scope: the planar subcase of problem 20001754 / de Laat's AIM Problem 1.32.
This file supplies independent deductions and checks the product comparison.
It does not validate the proposed OpenAI sharp two-point certificate.

## Exact source and claim

The primary AIM HTTP page was freshly retrieved on 2026-10-07 UTC. Its Problem
1.32 specifies Schwartz functions on R^(2n), Fourier value 1 at the origin,
nonnegative Fourier transform, and the three lengths |x|, |y|, |x-y| in
{0} union [1,infinity), excluding the pair (0,0). It does not impose |x+y|.
The original questions ask about equality with the Cohn–Elkies bound,
independent rotational symmetry, and conversions in both directions.

PR #487 at d33ec2f43aa7c59519f0b004202b8cd653ce4fd8 contains a partial-result
packet and its independent review. Its queue row 514 is unsolved, 5/5; that
is the PR-head version, distinct from a current-main queued, 0/5 row. No gate
based on this status is imposed here. All 16 packet files were read, including
both mathematical and sanitized-release review reports and their checks.

Put D={0} union [1,infinity) and

    Ctriangle={(x,y): |x|,|y|,|x-y| in D}\{(0,0)},
    Csquare={(x,y): |x|,|y| in D}\{(0,0)}.

The Fourier transform is integral f(z) exp(-2 pi i <z,w>) dz. Define L_n
and P_n by the exact real-Schwartz primal programs in the user prompt.
For a real function, a real nonnegative Fourier transform forces evenness,
so no additional evenness constraint changes either feasible set.

Both sign sets are closed: their only excluded point is isolated from the
remainder by Euclidean distance at least 1. Ctriangle is contained in
Csquare, so square feasibility implies triangle feasibility. No extra
rotational or rebasing invariance is imposed.

## Poisson lower bounds, without external packing theorems

Let B=[[1,1/2],[0,sqrt(3)/2]] and Lambda=B Z^2. Its covolume is
d=det(B)=sqrt(3)/2. For integers m,n,

    |B(m,n)|^2=m^2+mn+n^2=(m+n/2)^2+3n^2/4.

This is a positive integer unless m=n=0, so every nonzero vector has length
at least 1. Length 1 occurs, for example, at B(1,0), so the minimum is
exactly 1. The dual lattice for the stated Fourier phase is B^(-T) Z^2.

For every feasible g, both lattice sums below converge absolutely, since
g and its Fourier transform are Schwartz. Poisson summation gives

    g(0) >= sum_(v in Lambda) g(v)
         = d^(-1) sum_(w in Lambda*) ghat(w)
         >= d^(-1) ghat(0) = 2/sqrt(3).

The first inequality includes all nonzero minimum-length vectors on the
closed sign boundary |v|=1. Taking the infimum proves L_2>=2/sqrt(3).

For every feasible F and every (u,v) in Lambda^2 other than (0,0), each of
u,v,u-v is a lattice vector. Its norm is either 0 or at least 1. Hence that
pair belongs to Ctriangle. This argument includes u=0, v=0, u=v, u=-v,
collinear pairs, and all norm-1 boundary vectors, without discarding them.
Poisson summation on the product lattice, of covolume d^2, gives

    F(0,0) >= sum_(u,v in Lambda) F(u,v)
           = d^(-2) sum_(s,t in Lambda*) Fhat(s,t)
           >= d^(-2) Fhat(0,0)=4/3.

Taking the infimum proves P_2>=4/3. These deductions require no optimizer
and no assumption that the triangle infimum is attained.

The reciprocal covolume 2/sqrt(3) is number density for minimum distance 1.
The covered-area density for disks of radius 1/2 is
(pi/4)(2/sqrt(3))=pi/(2 sqrt(3)). The usual center-density convention based
on unit-radius rescaling has value 1/(2 sqrt(3)). These quantities must not
be conflated with either raw primal objective.

## Product-program audit and repairs

Cohn–de Laat–Salmon, arXiv:2206.15373v1, Proposition 4.7, proves equality
of a square sign program with the product of two-point values. Its
Definition 4.5 uses continuous integrable functions, minimum distance 2,
and factors vol(B_1^m) vol(B_1^n). Its Theorem 3.1 and Proposition 3.5
identify that continuous value with the Schwartz value for closed sign sets
away from zero. Their Remark 4.9 explicitly leaves primal attainment open.

The naive product g(x)g(y) is unusable: if an even admissible g is negative
at u with |u|>=1, then (u,-u) belongs to Ctriangle but g(u)g(-u)>0.

The primary v1 HTML and PDF have repairable printed slips in this part:

1. The compact packing graph is described with adjacency distance <1,
   while subsequent sphere-density formulas use minimum distance 2 and
   vol(B_1). A consistent proof fixes one threshold throughout.
2. In Lemma 4.8, writing V=vol(C1)vol(C2), positive definiteness of K-1 gives
   integral integral K >= V^2, not the printed lower bound V that is used
   with the subsequent ratio. The correct ratio is g(0)/ghat(0)<=M/V.
3. The compact theta-prime proof uses the indicator of the diagonal as
   a positive definite kernel. In the continuous-kernel definition that
   indicator is discontinuous; on Euclidean compacta it is justified by
   exp(-t|x-y|^2) and dominated convergence, as detailed below.
4. Negativity of the theta dual is imposed on distinct nonadjacent points,
   not on the diagonal. Its informal display omits that qualification.

These slips are not accepted silently and are not asserted to falsify the
product theorem. The following consistent raw-distance-1 argument repairs
the needed inequality. It also replaces reliance on a printed rescaling
factor by an explicit periodic-kernel estimate.

### Compact theta-prime upper product inequality

Use the compact packing graph on Q_r=[0,r]^n, with distinct points adjacent
exactly when their distance is less than 1. A feasible theta-prime measure
is a finite nonnegative positive definite measure on V^2, supported on
diagonal and nonedges, with mass 1 on the diagonal. Positive definiteness
means nonnegative pairing with every continuous positive definite kernel.
The dual minimizes max K(x,x), subject to K-1 positive definite and K<=0
on distinct nonedges. Compact primal-dual equality is the published
de Laat–Vallentin result, using corrected arXiv:1311.3789v3, Section 5.1,
Lemma 10. Its general hierarchy theorem is numbered 1.1 in v3. The specific
measure model and closed-cone argument are independently checked in
DUALITY_AUDIT.md; it is an attributed external result with a checked proof
mechanism.

For a feasible measure mu on the disjunctive product V1*V2, put

    A=mu({x1=y1}),
    nu1=(pi1)_*mu/A,
    nu2(E)=mu({x1=y1} intersect pi2^(-1)(E)).

A>=1 because the full diagonal has mass 1. The pushforward nu1 is positive
definite by testing K1 tensor 1; its diagonal mass is 1. It has the required
nonedge support. The measure nu2 is positive definite: for a continuous
positive definite K2, pair mu with

    exp(-t|x1-y1|^2) K2(x2,y2).

This is a continuous positive definite kernel. Since mu is finite and K2
bounded, dominated convergence as t tends to infinity gives the pairing
with diagonal-indicator times K2, which is nonnegative. Its full diagonal
mass is 1 and its support is allowed. Thus both nu1 and nu2 are feasible.
Their total masses are respectively mu(V1^2 V2^2)/A and A. Therefore

    theta'(V1*V2) <= theta'(V1) theta'(V2).

This proof uses no finite-support assumption on mu. The opposite inequality
follows from tensoring feasible measures but is unnecessary for the upper
comparison used here.

### Explicit compact estimate from a two-point Schwartz function

Let g be a normalized two-point Schwartz function in R^n. Choose T=r+1
and periodize on the T-periodic torus:

    p_T(z)=sum_(k in Z^n) g(z+Tk),
    K_T(x,y)=T^n p_T(x-y),    x,y in Q_r.

The series and its Fourier series converge absolutely; Poisson summation
gives Fourier coefficients ghat(k/T). Thus K_T-1 is positive definite,
since the k=0 coefficient is ghat(0)=1 and the remaining coefficients are
nonnegative. For a distinct nonedge x,y, the k=0 displacement has norm
at least 1. For k!=0, at least one coordinate of x-y+Tk has absolute value
at least T-r=1. Every summand is therefore nonpositive, including equality
at the boundary. K_T is a feasible compact dual kernel and has constant
diagonal T^n sum_k g(Tk). Consequently

    theta'(Q_r)/r^n
      <= (T/r)^n (g(0)+sum_(k!=0)g(Tk)) -> g(0).

The limit follows from Schwartz decay: for N>n,
sum_(k!=0)|g(Tk)|<=C_N T^(-N)sum_(k!=0)|k|^(-N), which tends to zero.
This proves the needed limsup without importing the Cohn–Salmon rescaling
theorem. Infimizing over feasible g gives limsup theta'(Q_r)/r^n<=L_n.

### Averaging a product dual kernel

Let V=Q_r^m times Q_r^n, with total volume W=r^(m+n), and let K be a
continuous feasible dual kernel for the disjunctive graph, of objective M.
Extend K to zero outside V^2 and set

    h(z)=integral K(t+z,t) dt.

The zero extension is positive definite as a kernel: restricting any test
matrix to indices in V gives a positive semidefinite principal block and
zero rows elsewhere. Hence h is positive definite by integrating finite
quadratic forms. It is compactly supported and continuous. For continuity,
compare the integrals at z and z+a on their common domain and its symmetric
difference. Uniform continuity of K controls the common-domain difference;
boundedness of K and translation continuity of cube indicators in L1
control the symmetric difference. Both errors tend to zero as a tends to
zero. In particular h is integrable and has nonnegative Fourier transform.

If (z1,z2) belongs to Csquare, each nonzero displacement coordinate has
norm at least 1 and each zero displacement coordinate is coincident. The
pair (t+z,t), whenever both points belong to V, is a distinct nonedge of
the disjunctive graph. Thus h<=0 on Csquare, including its axes.

The exact normalization calculations are

    h(0)<=MW,
    hhat(0)=integral integral_(V^2) K(s,t) ds dt >= W^2>0.

The second follows by pairing the positive definite kernel K-1 with the
constant test function 1 on V. Therefore h/hhat(0) is continuous feasible
with objective at most M/W. Compact primal-dual equality and the product
inequality above give continuous square-program value at most
theta'(Q_r^m)theta'(Q_r^n)/r^(m+n). Taking the limsup and using the explicit
periodic estimates gives at most L_m L_n.

Finally, Cohn–de Laat–Salmon Theorem 3.1 plus Proposition 3.5 transfers the
continuous infimum to the Schwartz infimum, without a primal-attainment
assertion. Thus in particular

    P_n <= P(Csquare) <= L_n^2.

Their dual tensor and no-gap theorem yield the matching square-program
lower inequality, hence P(Csquare)=L_n^2, but the upper inequality alone
is enough for the present planar deduction. The only non-elementary
retained inputs in this repaired proof are compact theta-prime strong
duality and the closed-sign-set Schwartz/continuous value comparison. Their
proofs and precise model translations are independently checked in
DUALITY_AUDIT.md, including the needed perturbation-envelope continuity.

## Consequence conditional on the sharp two-point input

If a validated admissible planar g has ghat(0)=1 and g(0)=2/sqrt(3), then
the preceding lower bound gives L_2=2/sqrt(3). The product comparison gives
P_2<=L_2^2=4/3; its lattice lower bound gives P_2=4/3. This is a conditional
implication until such a g or a validated replacement input is established.
It does not produce a triangle optimizer, resolve other dimensions, or
give a universal objective-preserving map of optimizers.

## Independent baseline, saturation checks, and failed replacement route

The elementary normalized g(x)=(4/pi)(1-|x|^2)exp(-2|x|^2) is admissible in
R^2: its Fourier transform is

    (1+pi^2|xi|^2/2)exp(-pi^2|xi|^2/2).

It supplies L_2<=4/pi and, through the product comparison, P_2<=16/pi^2.
Hence the unconditional intervals retained at this checkpoint are

    2/sqrt(3)<=L_2<=4/pi,
    4/3<=P_2<=16/pi^2.

If an exact g attains the lower bound, equality in the two absolutely
convergent Poisson inequalities forces g(lambda)=0 at every nonzero Lambda
vector and ghat(lambda*)=0 at every nonzero dual vector. For radial g,
these include g(sqrt(m^2+mn+n^2))=0 and
ghat(2 sqrt(m^2-mn+n^2)/sqrt(3))=0 for all nonzero integer pairs. Every
g root of radius greater than 1 is a local maximum and has radial derivative
zero; Fourier roots have radial derivative zero at every positive radius.
The radius-1 primal root lies on the one-sided sign boundary, so its
derivative need not vanish. These necessary conditions are independent
falsification controls for any proposed sharp certificate, not an existence
proof.

An independent geometric route was considered: use the elementary optimal
planar packing-density theorem as a replacement for the imported analytic
certificate. This does not establish either LP upper infimum; a valid
geometric packing bound supplies no feasible Fourier certificate for this
more restrictive function optimization. Declaring equality from geometric
packing optimality transfers the central difficulty and is blocked. No
independent replacement mechanism proving the sharp two-point upper bound
has been found at this checkpoint.

## Verification and attribution

The primary product proof was checked from both arXiv v1 HTML and the v1
PDF, SHA256 8a98d3f2d55e859a364f5aa9448d17c3535d0f244aee644242872ea7aed023b5.
Fresh primary AIM and immutable PR-head retrievals are recorded separately.
Copies of third-party source excerpts and PR packet files are private audit
inputs under sources/triangle/ and are excluded from publication material.

The bridge is derivative of Cohn–de Laat–Salmon's published product program;
the Poisson lower arguments are standard. The repairs and explicit periodic
estimate here are independent verification work, not claimed literature
novelty. An unconditional sharp planar upper result remains contingent on
the central certificate audit managed by the parent research program.
