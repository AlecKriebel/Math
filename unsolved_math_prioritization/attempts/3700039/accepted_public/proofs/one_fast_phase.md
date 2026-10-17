# Final-pass layer selection: a one-fast-phase flat class

## Result and boundary

The unrestricted median normalized-supremum conjecture remains unresolved. This fifth and final shared substantive pass does not establish a general favorable-layer selection theorem, and it does not construct an all-radii uniformly negative triple. It establishes an affirmative theorem for a continuously changing, critical-frequency flat class, with an exact actual-denominator limit. The theorem uses neither normalized angular compactness nor a homogeneous tangent. It also characterizes which leading profiles in this class can be realized by whole-plane smooth flat subharmonic functions, using a common lower-order radial correction rather than separated annular packets.

The target and credited harmonic and homogeneous cases remain A. Eremenko, *Conjectured inequality for subharmonic functions* (4 April 2015), https://www.math.purdue.edu/~eremenko/dvi/subh1.pdf. No historical novelty is claimed. The accepted fourth-pass harmonic-packet results remain intact: their negative honest records and positive gaps cannot resolve the unrestricted problem.

Write

    I(r) = integral_0^(2 pi) med_j u_j(r exp(i theta)) dtheta,
    B(r) = max_(j,theta) u_j(r exp(i theta)).

Angular integrals are unnormalized. Every quotient below uses the actual positive B; no value is assigned to 0/0.

## 1. Precise affirmative theorem

The same single fast phase Q psi(theta) is used by all three components. Fix p>0. Let psi be a smooth real 2 pi-periodic function such that

    {theta : psi'(theta)=0}

has angular Lebesgue measure zero. Let H_0,H_1,H_2 be smooth real functions, 2 pi-periodic in each variable (theta,x), and not all identically zero. Put

    Q = r^(-p),  f = exp(-Q),
    V_j(r,theta) = f H_j(theta,Q psi(theta)).

Suppose V_j are subharmonic for every sufficiently small positive r. Then, with

    B_* = max_(j,theta,x) H_j(theta,x),
    J_* = integral_0^(2 pi) [(1/(2 pi)) integral_0^(2 pi)
                            med_j H_j(theta,x) dx] dtheta,

one has B_*>0, J_*>=0, and

    B(r)/f -> B_*,
    I(r)/B(r) -> J_*/B_* >= 0                                  (1)

as r decreases to zero. In particular, B(r)>0 for all sufficiently small r. The result is unchanged by smooth errors E_j satisfying

    max_(j,theta) |E_j(r,theta)|/f -> 0,
    max_(j,theta) |(partial_t^2+partial_theta^2)E_j|/(Q^2 f) -> 0,
    t=log r,                                                  (2)

provided the full functions V_j+E_j are subharmonic near zero.

The hypotheses permit fast oscillations at every small radius, with changing local angular frequency Q psi'(theta), arbitrary independent triple profiles, and theta-dependent fast-phase shapes. They do not cover arbitrary angular superpositions with multiple independent fast phases.

## 2. Frozen positivity follows from genuine subharmonicity

Partial theta derivatives of H in this section keep x fixed. Direct calculation, using Q_t=-pQ, gives

    (V_j,tt+V_j,theta theta)/(p^2 f)
       = Q^2 P_theta H_j + Q R_(1,j) + R_(2,j),               (3)

evaluated at x=Q psi(theta), where

    a(theta)=psi(theta)^2+psi'(theta)^2/p^2,
    P_theta = a(theta) partial_x^2 - 2 psi(theta) partial_x + 1,
    R_(1,j)=-H_j+(psi+psi''/p^2)H_j,x
                         +(2 psi'/p^2)H_j,theta x,
    R_(2,j)=H_j,theta theta/p^2.

All remainders are uniformly bounded on the compact two-torus. Fix theta with psi(theta)!=0 and any x modulo 2 pi. There is a sequence Q_k tending to positive infinity such that Q_k psi(theta)=x modulo 2 pi. At its radii, subharmonicity, division of (3) by Q_k^2, and passage to the limit give

    P_theta H_j(theta,x)>=0                                  (4)

for every x. The complement of {psi!=0} has empty interior, since an interval of zeros would contradict the measure-zero critical-set hypothesis. Continuity therefore extends (4) to every theta. An error satisfying (2) vanishes in this same calculation. This is an ordinary smooth calculation; no distribution is restricted to an unjustified radial slice.

Integrating (4) over x removes both derivative terms and gives

    average_x H_j(theta,x)>=0                                (5)

for every theta and j.

## 3. Every frozen cone has nonnegative fast-phase median

Fix theta, and abbreviate h_j(x)=H_j(theta,x), b=psi(theta), a=b^2+psi'(theta)^2/p^2. Suppose P h_j>=0 with P=a partial_x^2-2b partial_x+1.

### Nonzero angular phase derivative

When psi'(theta)!=0, set

    beta=b/a,
    gamma=|psi'(theta)|/(p a)>0,
    T=pi/gamma,
    K=exp(beta T)>0.

Conjugating h_j by exp(-beta x), and applying the usual sine-kernel identity on length T, gives the exact formula

    h_j(x+T)+K h_j(x)
       = (1/(a gamma)) integral_0^T
           exp(beta(T-s)) sin(gamma s) (P h_j)(x+s) ds >=0.   (6)

The kernel is nonnegative. T need not divide 2 pi, and beta can have either sign. Periodically extend h_j to apply the formula.

Coordinatewise monotonicity and positive homogeneity of the median imply

    med_j h_j(x+T) >= -K med_j h_j(x).

Integrating over one full period and using translation invariance yields

    (1+K) integral_0^(2 pi) med_j h_j(x) dx >=0.              (7)

The positive factor is 1+K; replacing it by 2 without beta=0 would be an error.

### Zero angular phase derivative

When psi'(theta)=0, one has

    P=(1-b partial_x)^2.

Its inverse on periodic functions is positive:

    h_j(x)=integral_0^infinity s exp(-s)(P h_j)(x+b s) ds.     (8)

The formula follows by composing the two positive inverses of 1-b partial_x. It also covers b=0 directly. Uniqueness follows from the absence of a nonzero periodic solution of the homogeneous equation when b!=0, or from P=1 when b=0. Thus each h_j>=0 in this case.

Equations (7),(8) prove average_x med_j H_j(theta,x)>=0 for every theta, and hence J_*>=0. At the critical points there is no missing elliptic or square-root division case.

## 4. Phase averaging and the actual maximum

For every continuous function G(theta,x), periodic in each variable,

    integral_0^(2 pi) G(theta,Q psi(theta)) dtheta
       -> integral_0^(2 pi) average_x G(theta,x) dtheta.       (9)

Here is a direct proof of the needed oscillatory statement. Uniformly approximate G by a finite sum of x-Fourier modes with continuous theta coefficients. The zeroth mode gives the right-hand side. For a nonzero mode, cover the compact measure-zero set {psi'=0} by a finite union of intervals of arbitrarily small total length. On the remaining finite union of compact intervals, |psi'| is bounded below and psi is monotone on each piece. Changing variable y=psi(theta) makes each integral the Fourier transform at frequency mQ of an L1 function. The Riemann-Lebesgue lemma makes it tend to zero. The removed intervals contribute at most their length times the uniform bound. Let their length, and then the approximation error, tend to zero. This proof makes no assertion about phase mixing when psi is constant on a positive-length interval or when a singular phase pushforward is present.

Apply (9) to the continuous function G=med_j H_j to obtain I(r)/f -> J_*.

For the denominator, let

    b_Q=max_(j,theta) H_j(theta,Q psi(theta)).

Clearly b_Q<=B_*. Given epsilon>0, choose j,theta_0,x_0 with psi'(theta_0)!=0 and H_j(theta_0,x_0)>B_*-epsilon. Such a choice is possible because regular theta points are dense and H is continuous. In a fixed neighborhood of theta_0, psi has a continuous differentiable inverse. For all sufficiently large Q, some integer k_Q makes (x_0+2 pi k_Q)/Q lie within pi/Q of psi(theta_0). Its inverse theta_Q tends to theta_0 and satisfies Q psi(theta_Q)=x_0 modulo 2 pi. Therefore

    liminf_Q b_Q >= H_j(theta_0,x_0)>B_*-epsilon.

This proves b_Q->B_*. Finally (5) implies B_*>0: if all H_j were everywhere nonpositive, their nonnegative x-means would force every H_j to be identically zero, contrary to hypothesis. The errors in (2) change the normalized maxima and median integrals by quantities tending to zero. These facts prove (1), with the actual denominator throughout.

## 5. Converse realization with no annular gaps

The frozen condition (4) is also sufficient for an actual whole-plane realization, after a lower-order common radial repair. Suppose H_j and psi satisfy all of the above smoothness and phase assumptions and (4). Let

    C >= max_(j,theta,x) |R_(1,j)|,
    C >= max_(j,theta,x) |R_(2,j)|,
    C>=0,

and define for r>0

    u_j(r,theta)=exp(-Q)[H_j(theta,Q psi(theta))+C/Q],
    u_j(0)=0.                                                (10)

Since

    (partial_t^2+partial_theta^2)(f/Q)
       =p^2 f(Q+1+1/Q),

equation (3) gives

    (u_j,tt+u_j,theta theta)/(p^2 f)
       =Q^2 P_theta H_j+Q(R_(1,j)+C)+(R_(2,j)+C)+C/Q>=0      (11)

for every Q>0, hence every r>0. The planar Laplacian is the cylindrical one multiplied by r^(-2)>0. All Cartesian derivatives are bounded near zero by exp(-r^(-p)) times a fixed reciprocal power of r. Thus each u_j extends smoothly and flatly at zero, its Laplacian there is zero, and it is whole-plane subharmonic.

The correction C/Q tends to zero in the normalized profile; its normalized cylindrical Laplacian divided by Q^2 tends to zero too. Consequently these realizations have exactly the limit (1). There is no angular cutoff in r, no omitted transition, no separated-packet gap, and no discarded future tail.

## 6. Explicit critical-frequency, noncompact-negative-part example

Set p=1, psi(theta)=sin(theta), Q=1/r, and, for j=0,1,2,

    A(theta)=3 cos(theta)^16,
    H_j(theta,x)=1+A(theta)cos(x+2 pi j/3),
    u_j(r,theta)=exp(-1/r)[1+3 cos(theta)^16
                 cos(sin(theta)/r+2 pi j/3)+768 r],
    u_j(0)=0.                                                (12)

Here a=sin^2(theta)+cos^2(theta)=1. Therefore

    P_theta H_j=1+6 cos(theta)^16 sin(theta)sin(x+2 pi j/3).

For y=|sin(theta)|, the maximum of 6y(1-y^2)^8 is attained at y^2=1/17, and its square is

    36*16^16/17^17 <81/100.

Thus P_theta H_j>1/10 uniformly. Also |A'|<=48 and |A''|<=768, so |R_(1,j)|<=4+2*48=100 and |R_(2,j)|<=768. The choice C=768 in (10) proves whole-plane smooth subharmonicity, with a strictly positive Laplacian off zero.

The actual maximum is explicit for every radius:

    B(r)=exp(-1/r)(4+768 r)>0.                               (13)

Indeed H_j<=4, and j=0,theta=0 attains 4 for every Q. The fast-phase median of the three shifted cosines has zero x-mean: translation x->x+pi negates all three entries. Therefore J_*=2 pi and

    I(r)/B(r) -> pi/2 >0.                                   (14)

This is an affirmative example, not a counterexample. It has genuinely negative component values at all sufficiently small radii, and at theta=0 its actual median is exp(-1/r)(-1/2+768r), which is negative when r<1/1536. A pointwise negative angle is not a negative angular integral.

Its normalized negative parts are not L1-precompact. To verify this, set g_j(theta,x)=H_j(theta,x)^-. The weighted version of (9) implies that

    g_j(theta,Q sin(theta)) -> average_x g_j(theta,x)

weakly against continuous angular tests. The negligible common correction and the denominator tending to 4 give the corresponding weak limit for u_j^-/B. On an interval near theta=0, A(theta)>1, so g_j(theta,x) is a nonconstant function of x. Applying (9) to

    |g_j(theta,x)-average_y g_j(theta,y)|

shows that the L1 distance from the only possible strong limit tends to a strictly positive number (divided by 4). Thus there is no L1-convergent subsequence. The common correction changes negative parts by at most 768/Q before normalization and does not alter this conclusion.

The angular variation of the actual-denominator-normalized profiles and their normalized negative parts on a fixed smaller interval with A>1 and |cos(theta)| bounded below grows at order Q, and its global variation is O(Q). For a direct lower bound, shrink that interval so A>=a_0>1. Choose a fast-phase subinterval where cos(x+2 pi j/3)<-1/a_0 with a fixed strict margin and |sin(x+2 pi j/3)| is bounded below. On this set the component remains negative after the 768/Q correction, for all sufficiently large Q. Its angular derivative has magnitude at least Q A|cos(theta) sin(x+2 pi j/3)|-|A'|. Apply (9) to a nonzero smooth nonnegative weight supported inside these angular and fast-phase intervals. The weighted integral of the leading coefficient has a strictly positive limit, while the amplitude derivative contributes only O(1). This proves a positive lower bound times Q; the global derivative bound gives the matching O(Q) upper bound. Division by 4+768/Q preserves these bounds. This statement is about normalized variation; the raw functions carry the additional vanishing factor exp(-Q). The radial curvature scale of exp(-Q) is sqrt(Q^2-Q)~Q. Thus this example occupies the critical angular/radial scale, rather than the previously sufficient subcritical-variation regime. Its normalized radial shape also changes at orders Q and Q^2. The theorem handles that change through its explicit phase geometry.

## 7. Precise remaining claim

Nothing proved here supplies a one-fast-phase representation for a general smooth flat subharmonic triple, nor for an arbitrary rescaled critical layer. The accepted harmonic-packet embeddings can have essentially arbitrary fixed harmonic triples at their chosen records. Our phase geometry instead constrains the leading profiles at every nearby radius simultaneously through (4).

The unresolved general claim is still: every whole-plane subharmonic triple u_j with u_j(0)=0 has sup_(r:B(r)>0) I(r)/B(r)>=0. Even the remaining smooth all-flat possibility of I(r)/B(r)<=-epsilon at every positive-denominator radius is not ruled out by this pass. Multiple interacting angular phases, nonseparable envelopes, and globally coupled mode transfers need not satisfy the frozen one-dimensional cone or the averaging hypothesis above.

No general transition-mass inequality, distributional radial-defect slicing, automatic compactness, or homogeneous-tangent classification is asserted. The exact contribution is the affirmative theorem, its converse realization, and the critical noncompact example stated above.

## 8. Verification

The accompanying verifier checks the full cylindrical chain rule, the common correction, conjugated operator and weighted half-period identity, repeated-root factorization, exact example forcing, derivative formulas and rational forcing margin, the attained maximum, and finite-exhaustive weighted median pairing. It includes controls that reject omission of the drift, the amplitude derivative, the weighted factor, and the radial correction. General phase averaging, smooth extension, and the noncompactness conclusion rely on the analytic proofs in this report, not on numerical sampling.

The [full independent acceptance](../audits/fast_phase_acceptance.md), [exact author certificate](../certificates/fast_author.json), and [independent audit certificate](../certificates/fast_audit.json) are included.
