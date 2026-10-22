# Fourth-pass critical-layer structure and a smooth record-scale obstruction

## Result and scope

The unrestricted normalized-supremum conjecture remains unresolved. This fourth shared substantive pass supplies two complementary results.

1. A radial-curvature-defect estimate proves an affirmative result without any angular compactness, Fourier-bandwidth, or variation hypothesis. It identifies rapid radial change of angular shape as a necessary obstruction, in addition to the earlier critical angular variation.
2. Smooth, all-flat, whole-plane subharmonic triples can have strictly negative normalized medians at infinitely many honest record scales, with a harmonic critical-layer limit. Positivity of the limiting planar operator, exponential past growth, smooth flatness, and record normalization do not themselves force a nonnegative median on a selected layer. Every transition and the actual maximum are controlled. The intervening gaps have quotient exactly 2 pi, so this is not a counterexample to the supremum or small-radius-limsup conjecture.

No remote writes or priority claims are made. The source target remains A. Eremenko, *Conjectured inequality for subharmonic functions* (4 April 2015), https://www.math.purdue.edu/~eremenko/dvi/subh1.pdf. Its harmonic and homogeneous affirmative cases are credited prior results. The harmonic median calculation used below was derived in the accepted first pass and is independently rechecked here.

For whole-plane subharmonic u_j with u_j(0)=0, write

U_j(t,theta)=u_j(exp(t+i theta)),

b(t)=B(exp t)=max_(j,theta) U_j(t,theta),

I(exp t)=integral_0^(2 pi) med(U_1,U_2,U_3)(t,theta) dtheta.

All angular integrals are unnormalized. Quotients are evaluated only where the actual B is positive. No equivalence with assigning zero to 0/0 is asserted.

## 1. A radial-curvature-defect inequality

### Theorem 1

Suppose U_j are C^2 near the circle t=t_*, and U_(j,tt)+U_(j,theta theta)>=0 there. For every lambda>0,

I(exp t_*) >= -(1/lambda^2) sum_j ||(U_(j,tt)(t_*,.)-lambda^2 U_j(t_*,.))^+||_1.       (1)

In particular, at a sequence t_k with b(t_k)>0, a choice lambda_k>0 for which

sum_j ||(U_(j,tt)-lambda_k^2 U_j)^+||_1 / [lambda_k^2 b(t_k)] -> 0                    (2)

implies liminf_k I(exp t_k)/b(t_k)>=0. The lambda_k may diverge. No angular compactness or angular-variation bound is used.

### Proof

Fix the circle, abbreviate h_j(theta)=U_j(t_*,theta), and put

R_j(theta)=(U_(j,tt)(t_*,theta)-lambda^2 h_j(theta))^+.

Then h_j''+lambda^2 h_j >= -R_j. Variation of constants on an angular interval of length ell=pi/lambda gives the exact identity

    h_j(theta+ell)+h_j(theta)
    = (1/lambda) integral_0^ell sin(lambda s)[h_j''+lambda^2 h_j](theta+s) ds.

There is no requirement that lambda be an integer or that ell divide the circle length. Since the sine is nonnegative on this interval,

h_j(theta+ell)>=-h_j(theta)-e_j(theta),

e_j(theta)=(1/lambda) integral_0^ell sin(lambda s)R_j(theta+s) ds>=0.

Coordinatewise monotonicity and the maximum-norm Lipschitz property of the median give

med(h(theta+ell))+med(h(theta)) >= -max_j e_j(theta).

Translation preserves the circle integral, and Fubini gives integral e_j=(2/lambda^2) integral R_j. Thus 2 I >= -integral max_j e_j >= -(2/lambda^2) sum_j integral R_j, proving (1). Division by the positive actual b proves (2). QED.

A slightly sharper usable form is I >= -(1/2) integral max_j e_j; (1) is the convenient separable bound. The positive part in (1) is intentional. Replacing it by the negative part is not justified.

### Corollary 2: slow radial change of the angular shape

Let F(t)>0 be C^2 near selected circles and put

U_j=F g_j, beta=F'/F, kappa=F''/F>0.

Then (1), with lambda^2=kappa, gives

I/B >= - F/[B kappa] sum_j ||(g_(j,tt)+2 beta g_(j,t))^+||_1.                       (3)

Consequently, if F/B is bounded, |beta|/sqrt(kappa) is bounded, and

sum_j ||g_(j,t)||_1=o(sqrt(kappa)),

sum_j ||g_(j,tt)||_1=o(kappa),                                                       (4)

along those circles, their normalized median has nonnegative liminf. A weaker sufficient condition is directly that the positive-part expression in (3), divided by kappa, tends to zero.

These assumptions concern radial change, not angular regularity. Angular frequencies and normalized negative parts may remain noncompact and may have variation comparable to sqrt(kappa). For instance, at each plateau center of the accepted third-pass smooth critical-frequency construction, F=exp(-exp(-t)) and the angular cutoff is locally constant. Hence g_t=g_tt=0 there, while its normalized negative parts are not L1-precompact and their variation is critical. More generally, every C^2 subharmonic triple with the indicated slowly changing radial shapes satisfies (3), even when the shapes have unbounded angular frequency.

Conversely, a smooth uniformly negative counterexample I/B<=-epsilon would have to satisfy, at every positive-denominator circle and every lambda>0,

sum_j ||(U_(j,tt)-lambda^2 U_j)^+||_1 >= epsilon lambda^2 B.                        (5)

When a common positive envelope F has kappa>0, this yields the corresponding necessary lower bound for the shape-change expression in (3). This does not assert that such counterexamples exist, or that actual B is twice differentiable; the theorem never differentiates B.

## 2. A half-plane layer with negative boundary median

For j=0,1,2 put phi_j=2 pi j/3 and

H_j(x,y)=exp(x) cos(y+phi_j)+exp(2x) cos(2y+2 phi_j).

Each H_j is harmonic for partial_x^2+partial_y^2, is 2 pi-periodic in y, has zero y-mean, and tends to zero as x->-infinity. Its joint maximum at fixed x is exactly exp(x)+exp(2x), because each summand is bounded by its amplitude and equality occurs at j=0,y=0. Thus for x<=0,

H_j(x,y)/2 <= [exp(x)+exp(2x)]/2 <= exp(x) <= exp(x/2).                           (6)

At x=0 the median numerator and maximum are, separately,

integral_0^(2 pi) med(H_0,H_1,H_2)(0,y) dy = -3 sqrt(3)/2,

max_(j,y) H_j(0,y)=2.

The normalized median is -3 sqrt(3)/4, not -3 sqrt(3)/2. This normalization is material.

For a direct integral check, symmetry reduces to six copies of 0<=y<=pi/3. On this sector the median at equal mode amplitudes is cos(y+2 pi/3)+cos(2y+4 pi/3), apart from equality endpoints. Its sector integral is -sqrt(3)/4; multiplying by six gives -3 sqrt(3)/2.

Thus harmonicity, zero angular means, positivity of the limiting Laplacian, and the one-sided record-type upper bound (6) do not force a nonnegative boundary median. The next theorem shows that this is an attainable critical limit of smooth all-flat admissible functions at honest records.

## 3. Realization by smooth annular packets

### Theorem 3

There exist C-infinity whole-plane subharmonic u_0,u_1,u_2, all flat at zero, and integers n_k->infinity with t_k=-log n_k, such that:

- B(r)>0 for every r>0;
- t_k is an honest record of slope M_k=n_k/2:

  b(s)<=b(t_k) exp[M_k(s-t_k)] for every s<=t_k;

- I(exp t_k)/b(t_k) -> -3 sqrt(3)/4 < 0;
- between these packets there are radii tending to zero where the quotient is exactly 2 pi;
- the rescaled triples converge in C-infinity on every compact subset of R^2:

  U_j(t_k+x/n_k,y/n_k)/b(t_k) -> H_j(x,y)/2.                                      (7)

The angular wavelength and reciprocal record slope are comparable. The exact actual-denominator, all-radii supremum and small-radius limsup for this example are both 2 pi. The negative record sequence cannot refute either conjecture.

### Fixed smooth cutoffs and one packet

Choose C-infinity functions eta,zeta on R such that

0<=eta<=1, eta=0 on (-infinity,0], eta=1 on [1,infinity),

0<=zeta<=1, zeta=1 on [0,1], zeta=0 outside [-1,2].

They can be chosen by the usual smooth step construction. Set

C=2||eta''||_infinity+6||eta'||_infinity,

K_0=3 C exp(2), K=2+6 C exp(2).

For L>=3 let

chi_L(x)=eta(x+L) eta(L-x),

R_L(x)=C[exp(x) zeta(x+L)+exp(2x) zeta(L-x)],

F_L(x)=integral_(-infinity)^x (x-s)R_L(s) ds.

The function chi_L H_j+F_L is smooth and subharmonic on the (x,y) plane:

(partial_x^2+partial_y^2)(chi_L H_j+F_L)
 = chi_L'' H_j+2 chi_L' partial_x H_j+R_L >=0.                                  (8)

Indeed, the transition intervals [-L,-L+1] and [L-1,L] are disjoint. On the first x<0, so both exp(x) and exp(2x) are bounded by exp(x); on the second x>0, so both are bounded by exp(2x). The derivative error is bounded respectively by C exp(x) and C exp(2x), and zeta equals one on the corresponding interval. Off these intervals the cutoff derivative error is zero. This verifies both transitions.

The correction is nonnegative, nondecreasing and convex, vanishes before x=-L-1, and is affine after x=L+1. For x<=0,

0<=F_L(x)<=C exp(x),

F_L(0)<=K_0(L+1) exp(-L), F_L'(0)<=K_0 exp(-L).                                 (9)

The first bound follows from R_L(s)<=C exp(s) for s<=0 and direct integration. The latter bounds integrate the inner correction over [-L-1,-L+2]; the outer correction has not started by zero.

For every x>=-L-1, an all-x upper envelope is

F_L(x)+chi_L(x)[exp(x)+exp(2x)] <= K exp(2L)[1+x+L+1].                            (10)

For x<-L-1 the packet is zero. Indeed, the total mass of R_L is at most 6 C exp(2L+2), all source points are at least -L-1, and the harmonic term is at most 2 exp(2L). These facts give (10) with the stated K.

### Choice of scales

Choose an integer N>=400 sufficiently large that, at n=N,

(C+2) exp(-sqrt(n)/4) <= 1/2,

6K exp(-n/4) <= 1/2,

K_0(sqrt(n)+1) exp(-sqrt(n)) + 6K exp(-n/4) <= exp(-sqrt(n)/2).                    (11)

Such N exists. Each left/right ratio decreases for n>=400, so these inequalities hold for every n>=N. This is a finite choice determined by the fixed cutoff constants; no numerical derivative estimate is presumed.

Set

n_k=N 2^k, L_k=sqrt(n_k), t_k=-log n_k, a_k=exp(-n_k),

x_k(t)=n_k(t-t_k).

The entire support of the kth correction curvature and angular term lies in

J_k=[t_k-(L_k+1)/n_k,t_k+(L_k+1)/n_k].

These intervals are disjoint. Neighboring centers are log 2 apart, whereas the sum of their half-widths is at most 4/sqrt(N)<=1/5<log 2. At most one angular packet or correction-curvature packet is active at a time.

Define on the punctured plane

U_j(t,theta)=sum_(k>=0) a_k [F_(L_k)(x_k(t))
                       +chi_(L_k)(x_k(t)) H_j(x_k(t),n_k theta)].                 (12)

The integer frequencies make this single-valued in theta. Set u_j(0)=0.

### Convergence, global subharmonicity and all-order flatness

Completed inner radial corrections are bounded by exp(-n_k+2 sqrt(n_k)) times a polynomial in n_k, |t| and log n_k. Their series and first t derivatives converge uniformly on compact t intervals by (10). Higher derivatives involve only the locally active correction-curvature packet. Angular terms have disjoint supports and are locally a finite sum. Thus (12) is C-infinity on the punctured plane.

Each summand has nonnegative cylindrical Laplacian by (8), multiplied by a_k n_k^2. Completed radial tails have zero cylindrical Laplacian off their own support intervals. Consequently the cylindrical, and hence planar, Laplacian of (12) is nonnegative.

Here is a flatness bound at the accumulation point. Write Q=exp(-t)=1/r. An active packet has n_k comparable to Q, since |t+log n_k|<=(L_k+1)/n_k tends to zero. Each fixed-order derivative of its smooth factors is bounded by a fixed power of n_k times exp(2 sqrt(n_k)+2), before multiplication by a_k. Conversion to Cartesian derivatives introduces only further fixed powers of 1/r. A completed inner packet has n_k>=c Q for a fixed c>0, and its affine radial tail is bounded by a polynomial in n_k,Q times exp(-n_k+2 sqrt(n_k)); use log(n_k/Q)<=n_k/Q when necessary. Summing over the dyadic n_k gives, for each Cartesian multi-index alpha, constants c_alpha,C_alpha,p_alpha>0 with

|partial^alpha u_j(z)| <= C_alpha exp(-c_alpha/r) r^(-p_alpha)

for all sufficiently small r>0. Outer packets vanish there. Every derivative therefore extends by zero at the origin, proving C-infinity flatness. The smooth Laplacian is zero at zero and nonnegative elsewhere, so the functions are whole-plane subharmonic. No outer extension is needed: beyond J_0 the entire sum is a smooth radial affine function of log r.

## 4. Actual record inequalities

Fix k and abbreviate n=n_k,L=L_k,a=a_k,t_*=t_k,M=n/2. No outer packet indexed below k contributes at any t<=t_*.

### Uniform weighted bound for all inner packets

For l=k+p, p>=1, let sigma_l=t_l-(L_l+1)/n_l. By (10), for every t,

exp[-M(t-t_*)] times the lth packet's upper envelope

    <= K a_l exp(2L_l) exp[M(t_*-sigma_l)](1+n_l/M).

Before sigma_l the packet is zero. After sigma_l use sup_(y>=0)(1+n_l y)exp(-M y)<=1+n_l/M. After division by a, the exponential factor is

exp{-n(2^p-1)+(np log 2)/2+2 sqrt(n 2^p)+(sqrt(n 2^p)+1)/(2^(p+1))}.

For p>=1, 2^p-1-(p log 2)/2 >= 2^(p-2). The square-root and constant terms are at most (9/4)sqrt(n 2^p)+1/4. Since n 2^p>=400, the full exponent is at most -n 2^p/8. Thus the sum of all inner upper envelopes obeys, for every real t,

exp[-M(t-t_*)] sum_(l>k) upper_envelope_l(t) <= a T_k,

T_k=6K exp(-n_k/4).                                                            (13)

The last elementary series estimate is

sum_(p>=1)(1+2^(p+1)) q^(2^p) <= 6q^2, 0<q<=1/4.

It follows from 2^p>=2p and the two geometric series; here q=exp(-n/8). Thus (13) controls the whole past, including every inner transition, rather than only values at t_*.

### Earlier part of the kth packet

For x=n(t-t_*)<=-L/2, (9) and the harmonic amplitude bound give

exp[-M(t-t_*)] times the kth upper envelope
 <= a(C+2) exp(x/2)
 <= a(C+2) exp(-L/4) <= a/2.

The inner contribution is at most a T_k<=a/2. Therefore throughout this region

b(t) exp[-M(t-t_*)] <= a < 2a <= b(t_*).                                          (14)

### Final core ending at t_*

For -L/2<=x<=0 the kth angular cutoff is one and its correction is affine. Every inner packet has completed its transitions, leaving a nonnegative affine radial function. Call the total radial baseline, divided by a, D_k(x). It is nonnegative, nondecreasing, and affine on this core, and

D_k(0) <= K_0(L+1) exp(-L)+T_k <= exp(-L/2).                                      (15)

No inner angular term is active. Since j=0,theta=0 attains both harmonic amplitudes, the actual joint maximum is exactly

b(t)/a=exp(x)+exp(2x)+D_k(x).                                                    (16)

For this x, D_k(x)<=D_k(0)<=exp(-L/2)<=exp(x), and D_k'>=0. Hence

(d/dx)[b(t)/a]-(1/2)b(t)/a
 = (1/2)exp(x)+(3/2)exp(2x)+D_k'(x)-(1/2)D_k(x) >=0.

Thus b(t)exp[-M(t-t_*)] is nondecreasing on the core and is maximal there at t_*. Combining with (14) proves the honest record inequality for every s<=t_*.

The earlier integrated record estimate A(t_k)/b(t_k)<=M_k^(-2) consequently applies as well. Nevertheless the median quotient at these records is negative bounded away from zero.

## 5. Exact median, positive gaps and attainable layer limit

Put delta_k=D_k(0). By (15), delta_k->0. The actual maximum and median integral are exactly

b(t_k)=a_k(2+delta_k),

I(exp t_k)=a_k[2 pi delta_k-3 sqrt(3)/2].                                         (17)

For the median calculation, the integer n_k makes theta -> n_k theta preserve circle integrals, and the common radial baseline adds directly to the median. Consequently

I(exp t_k)/b(t_k)
 = [2 pi delta_k-3 sqrt(3)/2]/(2+delta_k)
 -> -3 sqrt(3)/4.                                                               (18)

Between consecutive J_k all angular terms vanish. Infinitely many completed inner corrections remain strictly positive, so the functions agree with a common positive radial value and the quotient is exactly 2 pi. Also B(r)>0 at every r>0: each component has positive angular mean from these completed radial corrections, independently of the active angular term's sign.

For bounded x,y, the kth cutoff in (12) equals one for all sufficiently large k, its own correction and all derivatives in x tend to zero after division by a_k, and the completed inner baseline is affine with coefficients tending to zero after the same scaling. The latter follows from (13) at the endpoints of a fixed x interval; a nonnegative affine function uniformly tending to zero has derivative tending to zero. All other angular packets vanish. Since b(t_k)/a_k->2, this proves (7) in C-infinity on compact sets.

The limit is genuinely harmonic on the whole rescaled plane, angular-periodic, has the record-compatible past growth (6), and has a strictly negative boundary median. Even smooth local critical-layer convergence does not force median positivity at the selected radius. This does not rule out selecting other radii; the exact positive gaps show why that distinction matters.

## 6. Remaining frontier and verification

The new sufficient condition isolates radial shape change on the reciprocal-curvature scale, independently of angular compactness. The construction shows that this shape change can persist and create genuinely negative medians at honest records in the smooth all-flat class. A full proof would need to exploit connections between layers, or select favorable layers, rather than deduce positivity on every critical layer from local operator positivity and one-sided growth.

No all-radii uniformly negative triple is constructed. No automatic radial-defect smallness, arbitrary tangent compactness, or homogeneous-tangent classification is asserted. The unrestricted conjecture and the persistent coupled-layer regime remain unresolved.

The accompanying verifier independently checks the angular Green multiplier, envelope conjugation, packet Laplacian identity, exact harmonic median numerator and attaining maximum, normalized value, dyadic exponent and geometric-series estimates, and core weighted-monotonicity identity. Supplementary sampled median checks have explicit quadrature-error bounds. The analytical proof above supplies smoothness, infinite-series convergence, honest records, and the all-radii statements.
