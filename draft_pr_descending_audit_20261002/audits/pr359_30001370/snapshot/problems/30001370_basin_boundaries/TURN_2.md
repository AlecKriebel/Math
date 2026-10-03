# Author turn 2: the actual stable functional, and the L1 obstruction

Status: partial, 2/5 substantive author turns. The common-boundary question
is still unresolved. This turn reconstructs the linear stable splitting and
identifies exactly what it does not imply about the nonlinear map.

## 1. Source precision and an exact test of the proposed kernel

Lemma 14 and Proposition 5 of the inspected Bardet–Keller–Zweimüller
arXiv:0812.4040v1, pp. 30–32, give the derivative at 1 as

    Q f=P_0 f+B x phi(f),       phi(f)=integral x f(x) dx,
    lambda=1/2+B/12>1.                                      (1)

These are directional derivatives, also derivatives from BV to L1 at the
stated smooth points. The proposition's concluding variance estimate for
f in ker(phi) of zero mass is correct for that one application. Its use
as a stable-subspace description needs an additional argument: ker(phi)
is not Q-invariant. For example, with

    f(x)=x³−(3/20)x,

one has integral f=phi(f)=0, whereas

    P_0 f=x³/8+(3/160)x,     phi(P_0 f)=1/320.               (2)

Thus the displayed one-step estimate cannot simply be iterated inside
that kernel. This is a precision concerning the inspected preprint proof,
not a claim that its hyperbolicity conclusion or the basin conjecture is
false. The actual invariant kernel and a direct proof follow.

## 2. Resolvent functional and exact rank-one identity

Let L1_0={f in L1: integral f=0}. Define the continuous functional

    L(f)=sum_{k≥0} lambda^(−k) phi(P_0^k f).                 (3)

This converges absolutely in operator norm, since ||P_0||≤1 and
||phi||≤1/2. In particular ||L||≤lambda/[2(lambda−1)]. It can also be
written as integration against the bounded measurable function

    g(x)=sum_{k≥0} lambda^(−k) T_0^k(x).                    (4)

Only null-set choices at dyadic endpoints are involved. We have

    L(P_0 f)=lambda[L(f)−phi(f)],
    L(x)=(1/12)/(1−1/(2lambda))=lambda/B,
    L(Qf)=lambda L(f).                                    (5)

Thus

    E f=(B/lambda)L(f)x,       H=ker L intersect L1_0       (6)

give a bounded projection E onto the unstable line span{x}, with
ker E=H. The space H is Q-invariant. Every f in L1_0 decomposes uniquely
as E f+(I−E)f.

For every integer n≥0 there is the exact identity

    Q^n f=P_0^n f+B x sum_{k=0}^{n−1}
                         lambda^(n−1−k) phi(P_0^k f).      (7)

The empty sum is zero. To prove (7), apply Q, use Qx=lambda x,
and Q(P_0^n f)=P_0^(n+1)f+B x phi(P_0^n f). Equations (3) and (7) give,
for f in H,

    Q^n f=P_0^n f−B x sum_{j≥0}
                         lambda^(−1−j) phi(P_0^(n+j) f).  (8)

Since ||x||_1=1/4,

    ||Q^n f||_1 ≤ [1+B/(8(lambda−1))] ||P_0^n f||_1.       (9)

The doubling transfer operator is exact on L1_0: approximate f by its
conditional expectation on the partition into 2^m equal subintervals.
For n≥m its image under P_0^n is its integral, zero; contraction and L1
convergence of these conditional expectations imply P_0^n f→0. Therefore
Q^n f→0 for every f in H. If L(f)≠0, (5) instead implies
||Q^n f||_1≥lambda^n |L(f)|/||L||, so no other vector is stable.

**Theorem.** H is exactly the strong stable subspace of Q on L1_0;
it has codimension one, and span{x} is its unstable complement.

## 3. What changes in BV, and what fails in L1 operator norm

For zero-mass BV functions, ||f||_1≤Var(f), and
Var(P_0^n f)≤2^(−n) Var(f). Applying variation directly to (8),
using Var(x)=1 and |phi(P_0^(n+j)f)|≤2^(−n−j−1)Var(f), yields

    Var(Q^n f)≤2^(−n)[1+B/(2lambda−1)] Var(f)
             =7·2^(−n) Var(f),      f in H intersect BV.   (10)

Thus the intended linear stable conclusion is rigorously valid in BV
with its correct invariant kernel. This still does not make the nonlinear
map Fréchet differentiable from BV to BV or from L1 to L1.

There is no analogous uniform exponential contraction on H with the L1
norm. For m≥0 let

    c_m(x)=cos(2 pi 2^m (x+1/2)).

Each c_m is symmetric, has integral zero, and has L(c_m)=0 because all its
P_0 iterates are symmetric. For 0≤n≤m,

    Q^n c_m=P_0^n c_m=c_{m−n},    ||c_m||_1=2/pi.

Consequently ||Q^n|_H||_{L1→L1}≥1 for every n. Each individual c_m is
annihilated after m+1 steps, so this is entirely consistent with strong
stability. It rules out replacing that stability by a uniform norm
contraction in a nonlinear graph-transform argument.

## 4. The remaining nonlinear gap

The operator Q describes directional behavior at 1. For a general small
f with 1+f≥0, the nonlinear expansion also contains

    (P_{r(1+f)}−P_0)f.

Strong parameter continuity for each fixed f does not give a remainder
o(||f||_1) uniformly over all such f. The moving branches are precisely
why the primary source distinguishes the derivative spaces. The resolvent
functional (3) repairs the linear splitting, but supplies neither a local
L1 separating stable manifold nor a uniform modulus for the backward
sections from turn 1. Claiming either would assume the missing step.

The next route will use self-consistent finite-cylinder approximations and
check whether they can be kept on the central basin. Merely approximating
D by densities whose finite iterates enter D' will not itself settle that
central-basin constraint.
