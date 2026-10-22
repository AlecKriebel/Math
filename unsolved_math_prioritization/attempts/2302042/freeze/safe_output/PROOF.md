# Reconstructing the Gol'dberg-Eremenko example

## 1. Target and scope

For a nonconstant entire function F, a finite asymptotic value a is a limit
of F along a curve escaping every compact subset of the plane. Write n(r,a)
for the number of a-points in |z| <= r, with multiplicity, and n_gamma(r,a)
for those on a specified asymptotic curve. The question asks for several
distinct values and curves with n_gamma(r,a)/n(r,a) tending to positive
constants, and asks whether all those constants can equal 1.

The following proves the positive-ratio part. It does not prove a universal
inequality for arbitrary entire functions or curves. The literature-status
answer to the second part is recorded separately in Section 8.

**Theorem (Gol'dberg-Eremenko example).** For each integer n >= 2, set

    F_n(z) = integral from 0 to z of sin(t^n)/t^n dt,
    zeta = exp(pi i/n),
    A = integral from 0 to infinity of sin(x^n)/x^n dx,
    a_k = zeta^k A,    gamma_k = {zeta^k x: x >= 0},
    k = 0,...,2n-1.

Then F_n is entire of order n, A > 0, the a_k are distinct finite
asymptotic values along gamma_k, and

    n_gamma_k(r,a_k) = r^n/pi + O(1),
    n(r,a_k) = (2n/pi) r^n + o(r^n).

Consequently each ratio tends to 1/(2n), and their sum is 1.

Attribution: this exact construction and these constants appear in
Gol'dberg-Eremenko (1980), Section 3, pp. 531-532, equations (3.5)-(3.9).
The argument below reconstructs them, using a subharmonic scaling argument
for the total count rather than relying on an undocumented appeal to
completely regular growth. This presentation makes no priority claim.

## 2. Entire extension, symmetry, and order upper bound

The singularity of sin(t^n)/t^n at zero is removable, with value 1. Termwise
integration on compact sets gives the entire series

    F_n(z) = sum over j >= 0 of
      (-1)^j z^(2nj+1) / ((2j+1)! (2nj+1)).

Every exponent is congruent to 1 modulo 2n, hence

    F_n(zeta^k z) = zeta^k F_n(z).

The integral identity sin(w)/w = integral_0^1 cos(sw) ds gives
|sin(w)/w| <= exp(|w|), including w=0. Integration along a radial segment
therefore yields |F_n(z)| <= |z| exp(|z|^n). In particular its order is at
most n. A lower bound, establishing that the order is exactly n, follows
from Section 5.

## 3. Positive limit and distinct asymptotic values

Under u=x^n,

    A = (1/n) integral_0^infinity u^(1/n-2) sin(u) du.

This is integrable at zero since the integrand behaves like u^(1/n-1), and
absolutely integrable at infinity since 1/n-2 < -1. Let

    L_j = (1/n) integral_(j pi)^((j+1)pi)
                       u^(1/n-2) |sin(u)| du,   j >= 0.

These numbers are positive and strictly decreasing: after translating
u by pi, the absolute sine is unchanged and the positive weight is
strictly smaller. Also L_j tends to zero. Thus

    A = L_0 - L_1 + L_2 - L_3 + ... > 0.

For completeness, integrating by parts and evaluating the cosine integral
gives A = Gamma(1/n) cos(pi/(2n))/(n-1). The explicit gamma evaluation is
not used in the proof: positivity and convergence already suffice.

The symmetry in Section 2 now implies F_n(zeta^k x) -> zeta^k A. Since A
is nonzero and the powers of zeta are distinct, all 2n values are distinct.
The theorem asserts these values, without needing an exclusion of other
asymptotic values.

## 4. Exact ray counting

Put x_j=(j pi)^(1/n). The alternating-tail criterion above shows that
A-F_n(x_j) has sign (-1)^j. On each open interval (x_j,x_(j+1)),
F_n'(x)=sin(x^n)/x^n has the constant nonzero sign (-1)^j.
The intermediate value theorem and strict monotonicity therefore give
exactly one solution of F_n(x)=A in each such interval. Every solution
is simple because the derivative is nonzero there; no endpoint is a
solution. There are no other positive-ray points.

The number of complete intervals below r differs by a bounded amount
from r^n/pi. Thus n_gamma_0(r,A)=r^n/pi+O(1). Rotation by zeta^k sends
these simple A-points bijectively to a_k-points on gamma_k. This proves
the ray-count formula for every k. Including or excluding the origin
has no effect, since F_n(0)=0 != a_k.

There is also no multiplicity ambiguity in the denominator for these
values. Every critical point is a rotation of some x_j with j>=1.
The alternating partial sums F_n(x_j) are positive and are never A.
Its critical value therefore has the form zeta^k c with c>0 and c!=A;
it cannot equal any a_s. The origin is not critical. Thus all a_k-points
of F_n, on or off the designated ray, are simple.

## 5. Uniform sector asymptotics

Fix a compact angular subinterval of 0 < arg(z) < pi/n. In this sector
Im(z^n)>0. Split sin(t^n) into its two exponential terms and start the
radial integrals at radius 1, absorbing the initial entire integral into
a bounded term. The exp(i t^n) term has bounded radial integral, whereas
exp(-i t^n) grows exponentially.

For the growing integral one integration by parts gives a leading term

    integral t^(-n) exp(-i t^n) dt
      = (i/n) z^(1-2n) exp(-i z^n)
        - (i/n)(1-2n) integral t^(-2n) exp(-i t^n) dt.

These integrals follow the radial segment at the fixed argument. A second
integration by parts bounds the remainder relative to the leading term
by O(|z|^(-n)), uniformly on the chosen compact angular subinterval.
One direct justification of the bound is to split the radial integral
at |z|/2: its initial part is exponentially smaller, and on the remaining
part the exponent's radial derivative has size comparable to |z|^(n-1),
with positive real growth bounded below uniformly in the subinterval.
The finite lower-end terms are exponentially negligible. Consequently

    F_n(z) = -(1/(2n)) z^(1-2n) exp(-i z^n)
                                      (1+O(|z|^(-n))).

For the adjacent sectors, rotate by zeta or conjugate, using the real
series coefficients. It follows, locally uniformly on every closed
subsector avoiding the rays arg(z)=k pi/n, that for every fixed a in C,

    R^(-n) log|F_n(Rz)-a| -> U(z) := |Im(z^n)|

as R -> infinity, uniformly also for |z| bounded above and bounded away
from zero. Subtracting fixed a does not change the limit, because F_n(Rz)
is exponentially large there. The positive value of U in any such sector
and the upper bound in Section 2 imply that F_n has order exactly n.

## 6. Total zero count by subharmonic scaling

We explicitly use two standard results of subharmonic function theory:

1. A locally uniformly upper-bounded sequence of subharmonic functions on
   a connected domain has a subsequence converging in L1_loc, or a
   subsequence tending locally uniformly to minus infinity. A fixed open
   set on which the sequence has a finite locally uniform limit excludes
   the second alternative. This compactness principle also applies after
   taking an arbitrary subsequence.
2. Distributionally, (1/(2 pi)) Delta log|g| is the zero-counting measure
   of a nonzero holomorphic function g, with multiplicity. L1_loc
   convergence permits distributional differentiation. The resulting
   positive measures converge weakly on compactly supported continuous
   test functions.

Set u_R(z)=R^(-n) log|F_n(Rz)-a|. Section 2 gives locally uniform upper
bounds on u_R for R>=1. Section 5 excludes divergence to minus infinity.
Take any sequence R_j tending to infinity and apply compactness. Every
L1_loc subsequential limit agrees almost everywhere with U on the
complement of the finitely many rays and the origin, by Section 5.
Those exceptional sets have planar measure zero. Thus every subsequential
limit is U in L1_loc. Uniqueness and sequential compactness show that
u_R -> U in L1_loc as R -> infinity, without selecting special radii.

The Riesz measure mu=(1/(2 pi)) Delta U is supported on the 2n rays.
On either side of a ray U equals one of the harmonic functions
+Im(z^n) and -Im(z^n). At radius t>0 the jump in its normal derivative
is 2n t^(n-1), so its measure on each ray is

    (n/pi) t^(n-1) dt.

There is no atom at the origin: the outward flux on a circle of radius
epsilon is O(epsilon^n) and tends to zero. Each ray contributes mass
1/pi inside the unit disk, so mu(D)=2n/pi. Its boundary circle has zero
mu-measure, since each ray measure is absolutely continuous in t.

By the zero-measure identity,

    mu_R = (1/(2 pi)) Delta u_R
         = R^(-n) sum_(F_n(w)=a) multiplicity(w) delta_(w/R).

The preceding L1_loc convergence implies weak convergence mu_R -> mu.
The unit disk is a continuity set of mu; sandwiching its indicator between
continuous compactly supported functions yields

    n(R,a)/R^n = mu_R({|z|<=1}) -> 2n/pi.

This is valid for every fixed a, hence in particular all a_k. It justifies
the nonintegrated zero count and does not silently replace it by an
integrated Nevanlinna counting function.

## 7. Ratios, arbitrary finite selections, and limits of the result

Divide the ray count by the total count to obtain b_k=1/(2n). The sum
over all 2n selected values is 1. Given l>=2, choose n>=max(2,ceil(l/2))
and retain any l of these distinct value/path pairs. Their ratios remain
positive, settling the existence question in its ordinary reading that
the function has the listed l values. We do not assert exact realization
of every vector of positive ratios with sum <=1, prescribed values,
prescribed curves, exact odd cardinality of the full asymptotic-value
set, or an arbitrary prescribed nonintegral order.

## 8. Attributed answer to simultaneous density one

Hayman-Lingham, arXiv:1809.07200v2 (2018 draft), printed p.39, Update 2.42,
reports Barsegyan's bound sum(b_k)<=1 for entire functions. If l>=2 and
all b_k were 1, their sum would be l>1, contradicting that reported bound.
The draft also reports a meromorphic bound of 2; it is not used for the
entire-function conclusion.

This is a deduction from an attributed literature assertion. The original
Barsegyan theorem, its proof, and any precise hypotheses omitted from that
update have not been independently checked. SOURCE_VERIFICATION.json
records the bibliographic venue discrepancy. The fresh audit should judge
this status as attribution-only, not as a full proof verification of the
universal inequality. The positive-ratio reconstruction above is logically
independent of that inequality.
