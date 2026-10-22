# Variational partial results for the planar de Gennes bound

## Disposition and exact target

**The universal problem remains unresolved after five substantive attempts.**
This note proves only the propositions stated below. In particular, it does not
claim a counterexample, a proof for all smooth domains, or historical novelty.

Let Omega be a bounded connected smooth open subset of R^2. Fix beta > 0 and
A_beta(x,y) = beta(-y,x)/2. Set

    q_beta[u] = integral_Omega |(-i grad - A_beta)u|^2,
    lambda(Omega,beta) = inf_{0 != u in H^1(Omega;C)} q_beta[u]/||u||^2.

This form definition imposes magnetic Neumann conditions on the associated
operator, but imposes no boundary conditions on trial functions. The original
OWR question is whether lambda(Omega,beta) <= Theta_0 beta for every such
Omega and beta. At beta = 0 the assertion is equality. Complex conjugation
identifies the two signs of a field; the source uses nonnegative intensity.
For domains with holes, the specified potential matters: arbitrary additional
closed nonexact forms are not allowed.

The de Gennes constant is the minimum over xi in R of the lowest Neumann
half-line eigenvalue of -d^2/dt^2 + (t-xi)^2. Write xi_0 > 0 for its minimizer
and f > 0 for its normalized ground state. Standard half-line facts used here
are

    -f'' + (t-xi_0)^2 f = Theta_0 f,  f'(0)=0,
    Theta_0 = xi_0^2,  integral (t-xi_0) f^2 = 0,

and Gaussian decay, also for the derivatives needed below. These are established
in the half-line sources in SOURCE_GATE.md. Only the finite certificate in
Section 5 uses the numerical lower bound Theta_0 > 5901/10000.

## 1. Best constant-modulus quadratic-phase test

Let z be the centroid and let

    Sigma = |Omega|^(-1) integral_Omega (x-z)(x-z)^T dx.

Sigma is positive definite. Then

    lambda(Omega,beta) <= beta^2 det(Sigma)/tr(Sigma).                 (1)

Moreover, the right-hand side is the minimum Rayleigh quotient among all
constant-modulus tests exp(i phi), with phi a real polynomial of degree at most
two. Consequently the desired bound holds whenever

    beta det(Sigma)/tr(Sigma) <= Theta_0.                            (2)

Proof. Translating the origin changes the symmetric potential by a constant,
which is the gradient of a linear function. A rotation of determinant one
diagonalizes Sigma, with eigenvalues v_1,v_2 > 0. Write a general residual
potential after subtracting a quadratic gradient as

    A_beta - grad(phi) = (p x - a y, (beta-a)x + q y) + c.

Every affine field of curl beta has this form, and every such field differs
from A_beta by a gradient. Since the coordinates have zero mean and zero
cross moment, its mean squared norm is

    p^2 v_1 + q^2 v_2 + a^2 v_2 + (beta-a)^2 v_1 + |c|^2.

It is minimized by p=q=0, c=0, and a=beta v_1/(v_1+v_2), because

    a^2 v_2 + (beta-a)^2 v_1
      = beta^2 v_1 v_2/(v_1+v_2)
        + (v_1+v_2)(a-beta v_1/(v_1+v_2))^2.

For u=exp(i phi), the Rayleigh quotient is exactly that mean squared norm.
This proves (1), its optimality within the stated trial class, and (2).

For an ellipse of semiaxes a,b, Sigma=diag(a^2/4,b^2/4), so (1) becomes

    lambda <= beta^2 a^2 b^2 / (4(a^2+b^2)).                         (3)

For each fixed domain this covers a nonempty initial field interval. It cannot
settle arbitrarily large fields: its ratio to beta grows linearly with beta.
The optimality assertion concerns this trial class only, not the eigenvalue.

## 2. Half-plane restriction: a valid criterion and a disk obstruction

We first normalize beta=1 by dilation. The gauge A=(xi_0-y,0) differs from
A_1 by the globally exact form d(xi_0 x-xy/2). In this gauge, the test u(x,y)=f(y)
is admissible on any bounded domain in y>0. Put

    h(y)=f'(y)^2+((y-xi_0)^2-Theta_0)f(y)^2=(f(y)f'(y))'.

If m_Omega(y) is the horizontal cross-section length, its exact defect is

    q_1[u]-Theta_0 ||u||^2 = integral_0^infinity m_Omega(y)h(y)dy.    (4)

Thus a negative right side is a sufficient condition for the strict bound.
For a subgraph 0<y<g(x), Fubini's theorem gives the defect

    integral f(g(x)) f'(g(x)) dx < 0.                              (5)

Here f'(t)<0 for t>0. Indeed f''=t(t-2xi_0)f, so f' decreases from zero on
(0,2xi_0), then increases to zero at infinity. Formula (5) is the established
subgraph method of Colbois--Lena--Provenzano--Savo, reproduced to identify the
precise sign mechanism. It applies in the form sense also to bounded Lipschitz
subgraphs; any smooth member of this class is within the target.

One cannot replace a general domain by a subgraph without proving a new
comparison. In fact this particular trial fails even on sufficiently large disks.
Let D_R be the disk centered at (0,R) with radius R, tangent to y=0. Its section
length is m_R(y)=2 sqrt(2Ry-y^2) for 0<y<2R, zero otherwise. Then

    lim_{R->infinity} (q_1[f|D_R]/||f|D_R||^2 - Theta_0)
      = - integral_0^infinity y^(-1/2)f(y)f'(y)dy
          / (2 integral_0^infinity y^(1/2)f(y)^2dy) > 0.            (6)

Proof. Dividing both numerator defect and denominator by sqrt(2R), one has
m_R(y)/sqrt(2R) -> 2 sqrt(y), dominated by 2 sqrt(y). The ODE ground-state
Gaussian decay makes the corresponding products with |h| and f^2 integrable.
Dominated convergence applies. Integration by parts gives

    integral sqrt(y)(f f')' = -(1/2) integral y^(-1/2) f f'.

The endpoint terms vanish. Near zero f'(y)=O(y^2), by its ODE and f'(0)=f''(0)=0;
at infinity they vanish by decay. Both integrals in (6) are finite, and the
numerator is strictly positive since f>0 and f'<0. This proves (6).

This is an obstruction to a proposed proof mechanism, not a counterexample to
the conjecture. In fact the disk bound is a credited prior theorem.

## 3. Disk transplantation and the exact loss on ellipses

The disk case has already been proved by Lena--Sundqvist (May 2026, with an
expanded September 2026 proof). Let E_{a,b} be the ellipse with semiaxes a>=b>0,
and put s=beta ab and

    kappa=(a/b+b/a)/2.

For any real radial profile g and angular mode m, define
u(r,theta)=g(r)exp(i m theta) on the unit disk D. Transplant u by x=(a X,b Y).
Its ellipse Rayleigh quotient is exactly

    Q_E = (kappa/(ab)) Q_D,s[u].                                  (7)

Proof. For T=diag(a,b) and J(x,y)=(-y,x), the identity
T^T J T=ab J shows that the magnetic differential on E pulls back to
T^(-T)(-i grad-A_s) on D. In polar coordinates the two components of that
magnetic differential are exp(i m theta)(-i g' e_r + (m/r-sr/2)g e_theta).
The radial and angular coefficients have zero real cross product. Integrating
cos^2 and sin^2 over a full circle gives equal Cartesian component energies,
each half the total. The Jacobian ab cancels in the quotient, proving (7).

The same calculation works for smooth polynomial profiles used in Section 5.
Taking a disk ground state in one angular sector gives

    lambda(E_{a,b},beta)/beta <= kappa lambda(D,s)/s.                (8)

For a!=b, kappa>1. The strict disk theorem alone does not make the right-hand
side of (8) smaller than Theta_0. Indeed lambda(D,s)/s tends to Theta_0 as
s tends to infinity, so that this *upper estimate* eventually exceeds Theta_0.
That says nothing adverse about the actual ellipse eigenvalue.

Nor can inscribed disks or partitions repair the argument for free. If a domain
is split into subdomains and independent Neumann conditions are introduced on
the cuts, its form domain is enlarged. Hence the first eigenvalue of the split
operator, the minimum of the piece eigenvalues, is <= the original first
eigenvalue. This is the wrong direction for the desired upper bound. Extension
by zero of a Neumann trial is generally not H^1 across the cut. These form-domain
facts specify the missing comparison rather than assuming domain monotonicity.

## 4. Thin circular annuli do not supply the sought counterexample

Fix R>0,beta>0 and let A_h={R-h<|x|<R+h}, 0<h<R/2, with the prescribed
symmetric potential. Then

    lim_{h->0} lambda(A_h,beta)
      = R^(-2) dist(beta R^2/2,Z)^2 <= beta/4.                     (9)

In particular the de Gennes bound holds strictly on all sufficiently thin A_h
for each fixed R and beta. The required thickness may depend on these parameters.

Proof. Fourier decomposition in angle gives radial forms

    integral_{R-h}^{R+h} (|g'|^2+V_m(r)|g|^2) r dr,
    V_m(r)=(m/r-beta r/2)^2,  m in Z.

For each m its first eigenvalue is at least min V_m and at most the weighted
average of V_m, by the constant radial test. Only finitely many m can minimize,
uniformly for small h: r is in [R/2,3R/2], and

    |m/r-beta r/2| >= 2|m|/(3R)-3 beta R/4

whenever the right side is positive; its square diverges as |m| grows, whereas
the m=0 trial has a uniformly bounded energy. On that finite set V_m converges
uniformly to V_m(R) as h->0. Squeezing proves the equality in (9).

For x=beta R^2/2>0 the ratio of this limit to beta is dist(x,Z)^2/(2x).
If x<=1/2, the distance equals x and the ratio is x/2<=1/4. If x>=1/2, the
distance is at most 1/2 and the ratio is at most 1/(8x)<=1/4. Finally
Theta_0>=1/2 follows without a decimal computation: using f in the unshifted
half-line oscillator, whose Neumann ground energy is 1, gives

    1 <= integral (f'^2+t^2 f^2) = Theta_0+xi_0^2=2Theta_0.

The gap between 1/4 and Theta_0 proves the final assertion.

The constant radial test also yields the explicit finite-thickness estimate

    lambda(A_h,beta) <= min_{m in Z} [
       m^2 log((R+h)/(R-h))/(2Rh) - m beta
       + beta^2(R^2+h^2)/4 ].                                    (10)

Its integrals use integral r dr=2Rh, integral dr/r=log((R+h)/(R-h)),
and the weighted mean of r^2 equal to R^2+h^2. This does not establish the
bound for every annulus thickness or every multiply connected domain.
The qualitative thin-tube phenomenon is prior literature; no novelty is claimed.

## 5. Exact finite-field certificate for near-circular ellipses

**Proposition.** For every ellipse E_{a,b} with a>=b>0,

    1 <= a/b <= 101/100,       0 < beta ab <= 131,

one has lambda(E_{a,b},beta) < Theta_0 beta.

This is a finite-field partial result obtained from credited disk witnesses,
not a result for all ellipses or all fields. No historical novelty is asserted.

Let theta_*=5901/10000. We use the published half-line lower bound
Theta_0>=0.590106124>theta_* (Bonnaillie-Noel, Theorem 1.1; see source gate).
The maximum kappa in the aspect-ratio range is exactly 20201/20200.

For s<=4 the constant disk test has quotient s^2/8. Equation (7) gives an
ellipse eigenvalue/field ratio at most kappa*s/8<=kappa/2<theta_*.
For s in [3,131], take the 30 rational profiles in witnesses.json:

    g_m(r)=r^m sum_{j=0}^8 c_j(1-r^2)^j,  m>=1.

These profiles and their covering intervals are the mathematical data of
Lena--Sundqvist, arXiv:2609.08774v1, Appendix A, Tables 1 and 2.
They are finite polynomials in Cartesian coordinates after multiplication by
exp(i m theta), so their origin behavior and H^1 admissibility are immediate.

For c=(c_0,...,c_8), their mass and energy are

    N=c^T M c,
    q_s=c^T K c - m s N + s^2 c^T V c,
    M_jk=(1/2) B(m+1,j+k+1),
    V_jk=(1/8) B(m+2,j+k+1),
    K_jk=m^2 B(m,j+k+1)-m(j+k) B(m+1,j+k)
            +2jk B(m+2,j+k-1).                                  (11)

A term with zero coefficient and a nonpositive Beta-function argument is omitted.
For positive integer arguments B(p,q)=(p-1)!(q-1)!/(p+q-1)!.
These formulas follow by substituting z=r^2 in the radial integrals; the
implementation additionally checks them by expanding g as monomials and
integrating those monomials directly.

At each of the two endpoints of every recorded interval, verify.py proves in
exact Fraction arithmetic both

    q_s-theta_* s N < 0,
    (20201/20200)q_s-theta_* s N < 0.                              (12)

The first checks the source disk data; the second certifies the ellipse margin.
For each fixed profile the second expression is a strictly convex quadratic in
s, with leading coefficient (20201/20200)c^T V c>0. Negativity at the endpoints
therefore proves negativity on the complete real interval, not just a grid.
All intervals abut or overlap and their union covers [3,131]. The magnetic
energy q_s is nonnegative, so replacing 20201/20200 by any smaller admissible
kappa preserves negativity. Combining (7) and (12) gives

    lambda(E,beta)/beta <= kappa q_s/(sN) < theta_* < Theta_0.

Together with the constant test this covers (0,131] and proves the proposition.

## Remaining gap

None of these arguments provides a universally admissible trial of quotient
at most Theta_0 beta at intermediate fields on an arbitrary smooth planar
domain. The exact finite certificate covers one bounded field range and one
narrow ellipse family only. It does not control all ellipse eccentricities,
all smooth deformations, all holes, or fields above 131/(ab) on that family.
The disk theorem and established subgraph/thin-tube results are prior results,
and the generic strong-field asymptotics are not an all-field theorem. The
original universal bound is neither proved nor refuted by this packet.
