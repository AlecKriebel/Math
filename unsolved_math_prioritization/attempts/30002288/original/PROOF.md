# Weighted maxima and the fractional infinity-eigenfunction representation

Problem 30002288 / OWR-12336-004. Author's mathematical candidate, 2026-10-06.
Independent audit and external specialist/novelty review are pending.

## Result and scope

The proposed unweighted high-ridge-subset formula is **not exhaustive** whenever
the high ridge contains two distinct points. We give an elementary, pointwise
construction, valid for every fixed exponent `0 < alpha <= 1`, including a
counterexample on a connected bounded planar rectangle. The proof establishes
the full nonlocal viscosity eigenfunction equation, not just minimization of its
limiting Rayleigh quotient.

The second question, whether normalized first fractional p-eigenfunctions always
converge to the maximal high-ridge solution, is **not resolved here**. Our explicit
asymmetric rectangle examples cannot themselves be finite-p subsequential
limits, by reflection symmetry. This observation is not a negative answer to
the second question. No novelty or global literature-completeness claim is made.

## 1. Exact operator and hypotheses

Let Omega be a nonempty bounded open subset of R^n; it may in particular be a
connected bounded Lipschitz domain. Put

    delta(x) = dist(x, R^n \ Omega), for all x in R^n,
    R = max delta > 0,
    Gamma = {x in Omega : delta(x) = R}.

Fix `0 < alpha <= 1`. All functions are extended by zero on the entire complement
of Omega. The operators in this note are

    L+ u(x) = sup_{y in R^n, y != x} (u(y)-u(x))/|y-x|^alpha,
    L- u(x) = inf_{y in R^n, y != x} (u(y)-u(x))/|y-x|^alpha,
    L u(x)  = L+ u(x) + L- u(x).

The eigenfunction equation is

    max{ L u(x), L- u(x) + R^(-alpha) u(x) } = 0.       (E)

A first eigenfunction here means a nonzero continuous function, positive in
Omega, zero outside, satisfying (E) in the viscosity sense. We normalize by
`max u = 1` when comparing representations. The formula under examination is

    F_S(x) = delta(x)^alpha / (delta(x)^alpha + dist(x,S)^alpha),

where S is a nonempty closed subset of Gamma. This is homogeneous up to an
overall positive scalar, which our normalization fixes.

These are the nonlocal operators of Lindgren--Lindqvist [LL], Definition 21 and
Section 10, and the OWR question [OWR], printed page 457. They are not the local
Aronsson infinity-Laplacian. Even alpha=1 does not make the equations identical.

For the finite-p part, the original fractional energy is

    Q_p(v) = (integral over R^n x R^n of
                  |v(y)-v(x)|^p / |y-x|^(alpha*p) dx dy)
             / (integral over R^n of |v|^p),

minimized with zero exterior values in W_0^(s_p,p)(Omega), where
`s_p = alpha - n/p`, `p >= 2`, and `n < alpha*p < n+p`. Alpha is fixed as
`p -> infinity`. In the usual fixed-s convention the denominator exponent is
`n+s*p`; the two conventions are not identical at finite p. The OWR rendering
of s has a typographical inconsistency; the relation above follows from the
energy and [LL], Section 3. With `||u_p||_p=1`, [LL], Proposition 20 and Theorem 23,
give `lambda_p^(1/p) -> R^(-alpha)` and uniform subsequential convergence to a
normalized solution of (E). No simultaneous alpha-limit is used here.

## 2. A global slope lemma proved directly

For z in Gamma define, on all R^n,

    f_z(x) = delta(x)^alpha / (delta(x)^alpha + |x-z|^alpha).

The denominator is at least R^alpha. Indeed,
`R=delta(z) <= delta(x)+|x-z|`, and `a^alpha+b^alpha >= (a+b)^alpha` for
nonnegative a,b. Thus the formula is well-defined everywhere, continuous,
positive in Omega, and zero outside. It takes the value 1 exactly at z.

Fix x in Omega and any y in R^n. Write

    A=delta(x)^alpha, B=|x-z|^alpha,
    C=delta(y)^alpha, D=|y-z|^alpha, H=|x-y|^alpha.

The ordinary distance functions are 1-Lipschitz. Subadditivity of the alpha
power therefore gives `|A-C| <= H` and `|B-D| <= H`. The identity

    C B - A D = C(B-D) + D(C-A)

implies `|C B-A D| <= H(C+D)`. Dividing by the two positive denominators proves

    |f_z(y)-f_z(x)| <= H/(A+B) = (f_z(x)/A) H.          (1)

This estimate includes exterior y, since then C=0. Its denominator bound also
shows that f_z is globally alpha-Hoelder with seminorm at most R^(-alpha).

At a nearest exterior point y_0 to x, `f_z(y_0)=0` and
`|x-y_0|=delta(x)`, so the negative bound is attained. Consequently

    L- f_z(x) = -f_z(x)/delta(x)^alpha.                  (2)

If x != z, taking y=z attains the positive bound in (1), because

    (1-f_z(x))/|x-z|^alpha = 1/(A+B).

Thus `L f_z=0` off z. At z, `L+ f_z(z)=0`: all slopes are nonpositive, and slopes
to points tending to infinity tend to zero. Equation (2) still holds there.
This already verifies (E) for a single profile without appealing to a
representation theorem.

## 3. Finite weighted maxima are eigenfunctions

Choose any finite nonempty collection `z_1,...,z_m` in Gamma and any positive
weights `c_1,...,c_m`. Define

    U(x) = max_{1 <= i <= m} c_i f_{z_i}(x).             (3)

It is continuous, positive in Omega, zero outside and globally alpha-Hoelder.
For x in Omega again write `A=delta(x)^alpha` and `H=|x-y|^alpha`. Applying
(1) to every profile gives

    c_i f_{z_i}(y) <= c_i f_{z_i}(x)(1+H/A)
                   <= U(x)(1+H/A).

Taking the maximum proves the upper estimate. Choose an index i active at x,
so `U(x)=c_i f_{z_i}(x)`. The lower estimate follows from that one profile:

    U(y) >= c_i f_{z_i}(y) >= U(x)(1-H/A).

Hence, for all y,

    -U(x)H/A <= U(y)-U(x) <= U(x)H/A.                  (4)

The negative bound is attained at a nearest exterior point, so

    L- U(x) = -U(x)/delta(x)^alpha,
    L+ U(x) <= U(x)/delta(x)^alpha.                     (5)

In particular `L U <= 0` everywhere in Omega. Also

    L- U(x)+R^(-alpha)U(x)
      = U(x)(R^(-alpha)-delta(x)^(-alpha)) <= 0.        (6)

If `x not in {z_1,...,z_m}`, an active index i has `x != z_i`. Since
`U(z_i) >= c_i`, its slope to z_i is at least

    (c_i-U(x))/|x-z_i|^alpha
       = c_i/(delta(x)^alpha+|x-z_i|^alpha)
       = U(x)/delta(x)^alpha.

The upper bound in (5) forces equality, so `L U(x)=0`. If x is one of the
selected ridge points, then delta(x)=R and (6) is zero. Thus at every x one
branch of (E) is zero and both are nonpositive. Equation (E) holds pointwise.

For completeness, this pointwise result implies the stated viscosity result.
If a global C^1 test phi touches U from below at x, every increment of phi
at x is no larger than the corresponding increment of U. Thus both L+ and
L- for phi are no larger, and both branches of (E) are nonpositive. For a
test touching from above, the inequalities reverse and at least one branch
is nonnegative. These are precisely the supersolution/subsolution conventions
of [LL], Definition 21. The same argument works for locally touching tests
patched by U outside the touching neighborhood. Finiteness follows from the
Hoelder bounds for U and local C^1 regularity for the test, with alpha<=1.

Finally `||U||_infinity=max_i c_i`: the upper bound is immediate from f_z<=1,
and an index of largest weight attains that value at its pole. If that largest
weight is 1, (3) is normalized. Nearest exterior slopes at such a pole show
that its global alpha-Hoelder seminorm is exactly R^(-alpha).

## 4. Counterexamples on every domain with two ridge points

Let a,b be distinct points of Gamma, let d=|a-b|>0, and set

    q = R^alpha/(R^alpha+d^alpha),
    choose q < t < 1,
    U_t = max{ f_a, t f_b }.

Section 3 proves that U_t is a normalized first eigenfunction. Its maximum
set is exactly {a}, since `t f_b <= t < 1` and f_a equals 1 only at a. For every
nonempty closed S subset Gamma, however, the maximum set of F_S is exactly S.
Thus if U_t had the proposed representation, necessarily S={a} and U_t=f_a.
But

    U_t(b) = max{q,t} = t > q = f_a(b),

a contradiction. Multiplication by a positive scalar cannot repair this:
the common normalization forces that scalar to be 1. Allowing a nonclosed
subset would make no difference, because distance only depends on its closure.

There is a continuum of distinct counterexamples, indexed by t in (q,1).
Thus failure is not an artifact of disconnected domains or of a boundary
normalization. When Gamma is a singleton, exhaustiveness is already supplied
by [LL], Corollary 37: every first eigenfunction is constant on that singleton
and is the displayed profile, up to scale. Combining that established result
with our construction gives the exact dichotomy: within these hypotheses, the
unweighted subset formula is exhaustive precisely when Gamma is a singleton.
The counterexample proof itself does not depend on this cited singleton result.

### Explicit connected example

Take `Omega=(-2,2) x (-1,1)`, `a=(-1,0)`, `b=(1,0)`, and `t=3/4`.
Here

    delta(x)=min{2-|x_1|, 1-|x_2|} in Omega,
    R=1, Gamma=[-1,1] x {0}.

For every `0<alpha<=1`, `q=1/(1+2^alpha)<1/2<3/4`. Therefore

    U(x)=max{
       delta(x)^alpha/(delta(x)^alpha+|x-a|^alpha),
       (3/4)delta(x)^alpha/(delta(x)^alpha+|x-b|^alpha)
    }

is the promised example, with U(a)=1 and U(b)=3/4. The domain is connected,
convex, bounded and Lipschitz. The alpha=1/2 instance lies strictly inside the
fractional exponent range, so the negative answer does not rely on an endpoint.

## 5. What is and is not proved about the p-limit

There is a useful elementary selection obstruction. Let T be any Euclidean
isometry preserving Omega. Change of variables shows that Q_p(u composed with T)
equals Q_p(u), and the L^p normalization is preserved. Simplicity of the positive
first finite-p eigenfunction ([LL], Theorem 14, for the regime alpha*p>2*n used for
large p in the limit) therefore implies `u_p composed with T = u_p`. Every uniform
subsequential limit has the same symmetry.

On the rectangle, reflection `T(x_1,x_2)=(-x_1,x_2)` exchanges a and b. The
constructed U has unequal values there and hence cannot be such a subsequential
limit. This prevents conflating a viscosity eigenfunction with a variationally
selected p-limit. It does not select the maximal solution.

As a known-type special case, if the isometries preserving Omega act transitively
on Gamma, every subsequential limit is constant on Gamma. By [LL], Corollary 37,
it is F_Gamma after normalization. Subsequence compactness applied to every
sequence p_j tending to infinity then gives convergence of the whole normalized
family to F_Gamma: a sequence staying a fixed sup-norm distance away would have
a subsequence converging to F_Gamma, a contradiction. This argument includes
the singleton-ridge case. It requires the compactness/simplicity hypotheses
above and asserts no new literature result.

For a general domain with a nontransitive ridge, the proof gives no mechanism
forcing a limit's ridge values to be constant. Neither max-stability of (E)
nor symmetry fills this gap. The general maximal-selection assertion remains
unproved and undisproved in this work. A bounded literature check is not proof
of its current worldwide status.

The later paper [DRS] studies the local operator
`Delta_infinity v = <D^2 v grad v, grad v>` and limits of concave problems with
an exponent tending to one. Its maximal-solution result is not a theorem for
the present full-space fractional operator or the present finite-p limit. Its
closing remarks suggest extensions to nonlocal kernels, but do not identify the
original diagonal p-eigenfunction limit with the maximal solution.

## References

[OWR] Mini-Workshop: The p-Laplacian Operator and Applications, Oberwolfach
Reports 08/2013, especially Peter Lindqvist, Three Nonlinear Eigenvalue Problems,
printed pp. 456--458, fractional question on p. 457.
https://doi.org/10.4171/OWR/2013/08
https://publications.mfo.de/bitstream/handle/mfo/3339/OWR_2013_08.pdf?isAllowed=y&sequence=1

[LL] Erik Lindgren and Peter Lindqvist, Fractional Eigenvalues,
arXiv:1203.4130v2 (23 April 2012), published in Calculus of Variations and Partial
Differential Equations 49 (2014), 795--826.
https://arxiv.org/abs/1203.4130
https://doi.org/10.1007/s00526-013-0600-1

[DRS] Joao Vitor da Silva, Julio D. Rossi and Ariel M. Salort,
Maximal solutions for the infinity-eigenvalue problem,
arXiv:1704.01875v1 (6 April 2017), Sections 1 and 4.
https://arxiv.org/abs/1704.01875
