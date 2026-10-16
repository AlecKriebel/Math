# Independent complex elliptic proof of the odd-period focal-line product

**Proof-chain freeze: 2026-10-16 15:58:22 UTC.** This argument was developed before
reading any submitted PR205 proof, checker, review, or other family's work.
The only external mathematical facts used are the standard Jacobi identities
listed below. No clearance or priority claim about PR205 follows from this file.

## Claim and geometry

Let a>b>0, alpha>beta>0, and

    c^2=a^2-b^2=alpha^2-beta^2,
    lambda=a^2-alpha^2=b^2-beta^2 in (0,b^2).

For any primitive odd-period N billiard orbit in the outer ellipse, tangent to
the inner ellipse, take q_{+,i}, q_{-,i} to be ordinary Euclidean distances
from (+c,0), (-c,0) to the COMPLETE supporting side lines. Then

    (sum_i q_{+,i})(sum_i q_{-,i})

is independent of the phase of the orbit. The winding may be any admissible
coprime tau, including a star-polygon winding. This statement is about a fixed
outer ellipse and fixed caustic. Repeating all sides r times multiplies the
product by r^2, for any positive integer r.

Put k=c/alpha in (0,1), k'=sqrt(1-k^2), K=K(k), K'=K(k'), and suppress k in
Jacobi functions. Let delta in (0,K) be defined by

    sn(delta)=sqrt(lambda)/b.

Then, directly from the definitions,

    cn(delta)=beta/b,
    dn(delta)=a beta/(b alpha),
    alpha=a cn(delta)/dn(delta), beta=b cn(delta).

Parametrize the outer boundary by

    X(u)=(a sn(u), b cn(u)).

The chord with endpoints X(t-delta), X(t+delta) has supporting line

    x sn(t) dn(delta)/a + y cn(t)/b = cn(delta),

or, equivalently,

    L_t: x sn(t)/alpha + y cn(t)/beta = 1.                 (1)

For verification, substitute each endpoint into the first equation and use
the addition formulas for sn and cn. The cross terms cancel; the numerator
becomes cn(delta)[sn(t)^2 dn(delta)^2+cn(t)^2], which equals
cn(delta)[1-k^2 sn(t)^2 sn(delta)^2], the common addition denominator.
Equation (1) is tangent to the caustic because sn(t)^2+cn(t)^2=1.

Conversely, all real tangents to the caustic are represented by (1), since
(sn(t),cn(t)) runs once around the unit circle as t runs through a real period
4K. At X(u), the two distinct caustic tangents are L_{u-delta} and
L_{u+delta}. Thus following consecutive distinct chords makes their parameters
advance by h=2delta, or by -h after reversing orientation. The entire side set
of a primitive orbit is therefore L_{t+jh}, 0<=j<N, with

    h=4K tau/N, gcd(tau,N)=1, 0<tau<N/2.                 (2)

This also shows that the minimal physical N is at least 3. The function identity
proved below permits N=1, but N=1 does not describe a proper-caustic orbit.
All admissible star windings in (2) are included.

The foci are strictly inside the caustic: c<alpha. The line normal in (1) has
length dn(t)/beta on the real axis, and dn(t)>0 there. Since
1 +/- k sn(t)>0, taking the ordinary NONNEGATIVE distance gives, before any
complex continuation,

    q_+(t)=beta(1-k sn(t))/dn(t),
    q_-(t)=beta(1+k sn(t))/dn(t).                        (3)

In particular q_+(t)q_-(t)=beta^2. Neither endpoint distances nor distances to
finite segments are used in (3).

## The complex function, its full period lattice, and its full divisor

Define

    f(z)=(1+k sn(z))/dn(z)=nd(z)+k sd(z).

The needed Jacobi facts are: sn is odd and dn even; dn^2=1-k^2 sn^2;
sn(z+2K)=-sn(z), dn(z+2K)=dn(z); and
sn(z+2iK')=sn(z), dn(z+2iK')=-dn(z). Consequently, as meromorphic identities,

    f(-z)=1/f(z),
    f(z+2K)=1/f(z),
    f(z+2iK')=-f(z).                                    (4)

Thus 4K and 4iK' are periods. Write Lambda=4K Z+4iK' Z and p=K+iK'.
The complete pole set of sn and dn is

    z=2mK+(2n+1)iK'.

At those common poles, nd=1/dn has a zero, while sd=sn/dn is analytic and
nonzero, because sn and dn have simple poles. Hence f has a removable
apparent singularity and a nonzero value there. There is no hidden pole or
zero at a common sn/dn pole.

The complete zero set of dn is

    z=(2m+1)K+(2n+1)iK',

and all these zeros are simple. At p, the quarter-period formulas give
sn(p)=1/k, cn(p)=-i k'/k, dn(p)=0. Thus
dn'(p)=-k^2 sn(p)cn(p)=i k', and f has a simple pole at p, with residue
-2i/k'. Translation by 2K sends this to a simple zero, by (4). Translation
by 2iK' preserves pole/zero type and changes the residue's sign.

For completeness the cancellation at the zero is also algebraic:

    f(z)=dn(z)/(1-k sn(z)).

At a dn zero with sn=-1/k, its denominator is 2; f therefore has a simple
zero. At a dn zero with sn=+1/k, the original numerator is 2; f has a simple
pole. Away from dn zeros and the removable common poles, a zero of the
numerator forces dn=0 by dn^2=(1-k sn)(1+k sn), so no other zeros occur.

The FULL divisor modulo Lambda is therefore

    simple poles: p, p+2iK';
    simple zeros: p+2K, p+2K+2iK'.                       (5)

The exact period lattice is Lambda, not merely a sufficient sublattice.
Indeed every period must preserve the pole set, so it must be
4mK+2niK'. Formula (4) multiplies f by (-1)^n under such a translation, and
f is nonzero and nonconstant. Hence n must be even.

The sole primary reference for the pole/zero and shift inputs is
[DLMF 22.4, Tables 22.4.1–22.4.3](https://dlmf.nist.gov/22.4).
The addition formulas are [DLMF 22.8.1–22.8.3](https://dlmf.nist.gov/22.8),
the square identities are [DLMF 22.6.1](https://dlmf.nist.gov/22.6.E1), and
the derivative is [DLMF 22.13](https://dlmf.nist.gov/22.13).
All product, divisor-cancellation, and billiard deductions here are independent
derivations from those facts.

## Odd cyclic sum and cancellation proof

Let N be any odd positive integer, h=4K tau/N with gcd(tau,N)=1 (for the
abstract N=1 identity, take h=0), and define

    A(z)=sum_{j=0}^{N-1} f(z+jh),
    B(z)=sum_{j=0}^{N-1} f(-z+jh).

The subgroup H={jh mod 4K} equals {4K j/N mod 4K}, so the result is unchanged
by any primitive winding permutation. Both A and B have periods 4K,4iK'
and are antiperiodic under 2iK'. Their product is therefore elliptic and
even has periods 2K,2iK', because (4) interchanges A and B under 2K.

By (5), the only possible poles of A are

    p-jh+2niK', 0<=j<N, n in Z,                         (6)

modulo 4K in the real direction. They are all simple and actually occur:
distinct j cannot coincide modulo 4K because gcd(tau,N)=1, so each pole
belongs to exactly one summand and has nonzero residue. The only possible
poles of B are the negatives of (6). The sets are disjoint for odd N.
For equality of one A-pole and one B-pole modulo Lambda would require

    (j+l)h = 2K mod 4K,

or 2(j+l)tau=N mod 2N, whose left side is even and right side odd.

Put z0=-p=-K-iK'. Equation (4), by direct composition, gives

    f(2z0-w)=-f(w),
    f(z0+v)=-f(z0-v).                                   (7)

Explicitly, 2z0-w=-2K-2iK'-w; reflection and the -2K shift together leave
f(w) unchanged, and the -2iK' shift multiplies it by -1. Also f(z0)=0 by
(5). None of the points z0+jh is a pole, by the preceding parity argument.
Therefore the finite set of analytic values in

    sum_{j=0}^{N-1} f(z0+jh)

cancels exactly in pairs j and N-j by (7), with the j=0 term zero. Its sum
is zero.

At any pole z=p-lh+2niK' of A, reindexing the finite subgroup and using
the imaginary antiperiod gives

    B(z)=(-1)^n sum_j f(z0+(l+j)h)=0.                   (8)

B is analytic at this point because the two pole sets are disjoint. Thus it
has a zero of order at least one, cancelling the simple pole of A in AB.
The same argument with A and B interchanged cancels every pole of B.
There are no other poles, by the complete list (5). AB is consequently a
holomorphic function on the compact torus C/Lambda and is constant.

The constant is not zero: on the real axis every f value is positive. In fact,
at z=0, oddness of sn and evenness of dn cancel the sd terms in the sum, so

    A(0)=B(0)=C_N(k),
    C_N(k)=sum_{j=0}^{N-1} 1/dn(4K j/N)>0,
    A(z)B(z)=C_N(k)^2.                                 (9)

Positivity also shows retrospectively that every zero used in (8) is exactly
simple: a higher zero would force the nonzero constant product to vanish.
There can be no other zeros of either sum. Thus, modulo Lambda, A has the
2N simple poles (6) and the 2N simple zeros at their negatives, while B has
the reverse divisor. The exact period lattice of each sum is
(4K/N)Z+4iK'Z: its pole grid forces a period to lie in
(4K/N)Z+2iK'Z, while the odd imaginary half-translate changes sign.

Applying (3) yields the explicit invariant value

    I=beta^2 [sum_{j=0}^{N-1} 1/dn(4K j/N,k)]^2.         (10)

This proof uses no value of the unknown constant, no unproved multiplication
formula, and no numerical inference. Oddness is used exactly to separate the
two cyclic divisors; even N permits their poles to coincide and the argument
then fails for a concrete reason.

## Boundary cases and exact scope

- Strict a>b and beta>0 ensure 0<k<1 and a compact nonsingular Jacobi torus.
- lambda in (0,b^2) ensures delta in (0,K), distinct chord endpoints, and
  strictly positive real distance numerators. No absolute value is dropped
  after complex continuation; it was removed rigorously on the real family.
- The mathematical N=1 identity is f(z)f(-z)=1; it is not asserted to be a
  physical proper-caustic orbit.
- Coprimality gives the primitive N grid. Nonprimitive odd indexing reduces
  to its primitive odd grid and the indicated repetition-square factor.
- Circle k=0 is outside the strict hypothesis and has the continuous elementary
  limit I=N^2 beta^2. Degenerate k=1 or beta=0 is not covered by the proof.
- The proof does not assert novelty, bibliographic priority, even-period
  invariance, or invariance for vertex/segment distances.

**Strongest independently proved result:** the exact cyclic identity (9), its
complete divisor explanation, and its geometric implication (10), for every
stated proper-caustic primitive odd orbit and star winding.

**Remaining mathematical gap in this argument:** none identified at this
freeze. Independent adversarial verification remains necessary before any
promotion. Finite diagnostics will be recorded separately and do not supply
the universal proof.

## 2026-10-16 16:01 UTC — exact even-period negative control

The exclusion of even primitive periods is substantive. For N=4, h=K,
sum_j f(z+jK) equals its companion and equals

    A(z)=B(z)=2[nd(z)+nd(z+K)]
               =2[1/dn(z)+dn(z)/k'].

Thus at z=0 its squared value is 4(1+1/k')^2, while at z=K/2 it is 16/k'.
The latter uses dn(K/2)^2=k', which follows directly from
dn(K-z)=k'/dn(z) and positivity. Their difference is

    4(1-1/k')^2 > 0, for 0<k<1.

Multiplication by beta^2 supplies two exactly unequal focal-line products of
proper N=4 billiards constructed with delta=K/2. This is an exact negative
control, independent of the finite numeric spread. It is consistent with the
pole collision found above and prevents accidental promotion to all periods.
