# Problem 2.19: reconstructed partial results

Packet: `2302019-reconstruction-20261005-v1`.

## 1. Exact target and classical inputs

Let K >= 0 and A,B >= 0. Let F(A,B,K) consist of entire functions of
exponential type at most K whose real-axis restrictions satisfy
|f(t)| <= A for t < 0 and |f(t)| <= B for t > 0. Exponential type at most K
means that, for every epsilon > 0, |f(z)| <= C_epsilon exp((K+epsilon)|z|).
Set S(A,B,K;z) = sup{|f(z)| : f in F(A,B,K)}.

This is the fixed-nonreal-point sharp-bound question in Hayman--Lingham
Problem 2.19. The common real-axis bound makes this type convention
equivalent here to the displayed source convention |f(z)| <= C exp(K|z|):
the classical vertical bound below supplies C = max(A,B).

Two standard theorems are used as classical inputs, not claimed as new:

1. If an entire function has exponential type at most K and real-axis
   supremum at most M, then |f(x+iy)| <= M exp(K|y|).
2. Bernstein's inequality in the same class is |f'(x)| <= K M for x real.

The first is the bounded-real-axis Phragmen--Lindelof estimate, recorded in
the equal-cap part of Problem 2.19. The second is stated explicitly on
p. 545 of Eremenko's 1988 paper. Montel's theorem, the identity theorem,
and the bounded-analytic maximum principle are also standard inputs.
All subsequent deductions are proved here. None determines S in general.

Boundary cases are exact. If A or B is zero, the identity theorem gives
f = 0. If K = 0, the vertical estimate and Liouville give constants and
S = min(A,B). If A = B > 0, S(z) = A exp(K|Im z|), achieved at an upper
point by A exp(-iKz) and at a lower point by A exp(iKz).

Henceforth A,B,K > 0. Reflection deals with A > B, so statements using a
ramp or an asymmetric witness are written for A < B. Complex conjugation
of coefficients deals with the lower half-plane.

## 2. Compactness, attainment, and elementary bounds

Put M = max(A,B). The vertical estimate bounds every f in F on every
compact set by the same constant. Montel therefore gives a locally
uniformly convergent subsequence from every sequence in F. Its limit is
entire, retains both real-axis caps pointwise, and retains
|f(x+iy)| <= M exp(K|y|). Consequently the limit again belongs to F.
Thus F is compact in the compact-open topology. Evaluation is continuous,
so S(A,B,K;z) is attained at every fixed z.

For every z,

    min(A,B) exp(K|Im z|) <= S(A,B,K;z)
                            <= max(A,B) exp(K|Im z|).

The lower bound uses the appropriate signed exponential, which has
constant real-axis modulus min(A,B). These are comparison bounds,
not an asserted formula for S.

## 3. Poisson step bound and strict failure of its equality case

For z = x+iy with y > 0 put theta = Arg z in (0,pi) and

    U_step(z) = exp(Ky) A^(theta/pi) B^(1-theta/pi).

Then |f(z)| <= U_step(z) for every f in F. To prove this without
assuming a boundary integral formula for log|f|, set

    g(z) = exp(iKz) f(z),
    alpha = (log A - log B)/pi,
    O(z) = B exp(-i alpha Log z),

where Log is the upper-half-plane branch. The vertical estimate makes
g bounded. Also |O(z)| = B exp(alpha theta), so both O and 1/O are
bounded in the upper half-plane. On either open real half-axis,
|g/O| <= 1. The bounded-analytic maximum principle, or its disk version
with exceptional boundary points 0 and infinity, gives |g/O| <= 1.
This proves the bound.

If A != B, equality cannot hold for any f at any nonreal point. Equality
at an upper point would make g/O a unimodular constant by the maximum
modulus principle. The resulting f would have boundary modulus B on
every positive real point and A on every negative real point. Continuity
of the entire f at zero would then force A = B, a contradiction.
The lower half-plane follows by conjugation.

Compactness makes this a strict supremum statement:

    S(A,B,K;z) < U_step(z),  Im z > 0, A != B.

Indeed, the continuous evaluation maximum is attained, so a sequence
approaching equality cannot evade the preceding contradiction. This
argument must not be replaced by the generally invalid inference
that individual strict inequalities alone imply a strict supremum gap.

The step bound here is a simple half-plane relaxation. We do not identify
it with the exact Gol'dberg--Levin subharmonic solution or assert that
our improvement is new relative to that solution.

## 4. An explicit ramp improvement

Suppose 0 < A < B and K > 0. Continuity at zero gives |f(0)| <= A.
Bernstein with M=B and the fundamental theorem of calculus give, for t>0,

    |f(t)| <= |f(0)| + integral_0^t |f'(s)| ds <= A + KBt.

Define L = (B-A)/(KB) and

    E(t) = A                    for t <= 0,
           A + KBt              for 0 <= t <= L,
           B                    for t >= L.

For z=x+iy, y>0, let

    V(z) = (1/pi) integral_R [y/((t-x)^2+y^2)] log E(t) dt.

The integral is finite; log E is bounded and continuous, and its Poisson
extension V has a harmonic conjugate in the upper half-plane. Thus
Q=exp(V+i V_tilde) is holomorphic and zero-free, with Q and 1/Q bounded.
The boundary modulus is E(t). Applying the same bounded-analytic maximum
principle to exp(iKz)f(z)/Q(z) proves

    |f(z)| <= U_ramp(z) := exp(Ky+V(z))
             = U_step(z) exp(-D(z)),

where

    D(z) = (1/pi) integral_0^L
           [y/((t-x)^2+y^2)] log(B/(A+KBt)) dt > 0.

Positivity follows because the integrand is positive on (0,L).
The following closed elementary lower bound avoids numerical integration:

    D(z) >= d(z) := L*y*log(2B/(A+B))
                     / [2*pi*((|x|+L/2)^2+y^2)] > 0.

Indeed, restrict the integral to [0,L/2]. On that interval,
A+KBt <= (A+B)/2 and |t-x| <= |x|+L/2. Therefore

    S(A,B,K;z) <= U_ramp(z) <= U_step(z) exp(-d(z)) < U_step(z).

These bounds apply at all nonreal points using |y| in the kernels; for
A>B reflect the real variable and exchange A,B. We make no equality or
optimality assertion for the ramp bound. Even replacing E by a pointwise
sharp real-axis envelope would not by itself solve the nonreal problem:
attainability of the analytic Poisson relaxation would still need proof.

## 5. A globally admissible integrated-sinc witness

Let a=K/4, delta=min(A,B-A)>0, and define the entire functions

    s(w) = sin(w)/w, s(0)=1,
    J_a(z) = integral_0^z s(at)^2 dt,
    F(z) = A + (2a delta/pi) J_a(z).

Path independence follows from the entire integrand. On the real axis
J_a is odd and strictly increasing: its derivative is nonnegative, with
only isolated zeros. The standard sinc integral is

    integral_0^infinity (sin u/u)^2 du = pi/2.

For completeness, integrate by parts to reduce it to
integral_0^infinity sin(2u)/u du. For epsilon>0 its exponentially damped
version is arctan(2/epsilon), obtained by differentiating with respect to
the frequency, evaluating the elementary Laplace cosine integral, and
integrating from frequency zero. Dirichlet's test gives the undamped
improper integral and the Abel limit, hence pi/2. Boundary terms vanish
at zero and infinity. It follows that J_a(+-infinity)=+-pi/(2a).

Consequently F(x) lies in (A-delta,A) for x<0 and (A,A+delta) for x>0.
Since delta<=A and A+delta<=B, F satisfies the two global modulus caps.
Its half-axis suprema are A and A+delta, respectively; the smaller
supremum is approached at zero from below.

To verify the required type directly, use

    s(w) = integral_0^1 cos(vw) dv,
    |s(w)| <= exp(|Im w|).

Along the straight integration path, |J_a(z)| <= |z| exp(2a|z|).
Because 2a=K/2<K, r exp(Kr/2) <= C_K exp(Kr) for all r>=0.
Thus |F(z)| <= C exp(K|z|), so F is an admissible entire function.
This type margin avoids any assumption about bounded primitives at
the limiting type. This witness is not claimed to be extremal for S.

There is a useful exact quantitative separation at x*=1/K. For
0<=t<=1/K, 0<=at<=1/4 and the elementary alternating Taylor bound gives

    s(at) >= 1-(at)^2/6 >= 95/96.

Therefore

    F(1/K)-A >= delta/(2*pi) * (95/96)^2
               > (9025/73728) delta,

where the final strict inequality uses pi<4. The same positive margin
also shows that the asymmetry is not merely a difference at infinity.

## 6. Finite real-frequency sums cannot supply the missing approximation

Let p(t)=sum_{j=1}^N c_j exp(i lambda_j t), lambda_j real, c_j complex.
Then

    sup_{t<0}|p(t)| = sup_{t>0}|p(t)| = sup_{t in R}|p(t)|.

Here is an elementary recurrence proof. Write beta_j=lambda_j/(2*pi).
For each positive integer Q, the Q^N+1 torus points n beta, 0<=n<=Q^N,
fall into Q^N cubes of side 1/Q. Two share a cube, yielding an integer
q_Q in [1,Q^N] such that the distance of each q_Q beta_j to an integer
is at most 1/Q. If q_Q has an unbounded subsequence, choose it so that
q_Q tends to infinity. Otherwise a fixed positive integer q repeats for
unbounded Q and all q beta_j are integers; its increasing multiples
give exact common periods. In either case there are T_n->+infinity with
exp(i lambda_j T_n)->1 simultaneously for all j.

For any fixed t0, p(t0+T_n)->p(t0) and p(t0-T_n)->p(t0). For large n
these evaluation points are respectively positive and negative. Each
half-axis supremum is therefore at least |p(t0)|. Taking the supremum
over t0 proves the claim. Empty and constant sums obey the same formula.

If p is globally admissible for F(A,B,K), it follows that
|p(t)|<=min(A,B) on the whole real line. Thus when A<B the witness F of
Section 5 satisfies, for every such p,

    |F(1/K)-p(1/K)| >= F(1/K)-A > (9025/73728) delta.

In particular, no sequence of globally admissible finite real-frequency
sums can converge to F locally uniformly on C. Pointwise convergence
at 1/K would already contradict the displayed gap.

There is a slightly stronger formulation. Such approximation is impossible
even locally uniformly on any nonempty open subset of C. If convergence
held there, the common bound |p(x+iy)|<=A exp(K|y|) would give a subsequence
converging locally uniformly on all C to an entire G. On that open set
G=F; the identity theorem gives G=F everywhere. But |G(t)|<=A on R,
contradicting Section 5. The common type K and global admissibility are
essential hypotheses in this argument.

Finite-window sampling or quadrature approximations without these global
caps are not covered by the obstruction and cannot certify admissibility.
This closes a proposed approximation route; it does not resolve the
sharp nonreal-point problem.

## 7. Scope and unresolved step

The compact extremal class, strict Poisson relaxation gap, explicit ramp
improvement, admissible asymmetric witness, and finite-frequency
obstruction are the reconstructed claims. Classical inputs and the known
real-axis solution are credited. No novelty or priority claim is made.
An exact formula or complete characterization of the maximizing entire
function at a general nonreal point remains unproved in this packet.

The accompanying finite checks test formulas, boundary cases, and
examples. They do not replace the proofs of the infinite-dimensional
claims, certify floating-point quadrature, or establish the target.
