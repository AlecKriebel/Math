# Third-pass concentration and negative-part estimates

## Result and scope

**The unrestricted normalized-supremum conjecture remains unresolved.** This third shared substantive pass replaces the previous cubic angular smoothing loss by a quadratic integrated loss. It proves the conjecture along flat-frontier sequences whose angular variation can escape to infinity but is smaller than the reciprocal radial scale. Only compactness of the normalized negative parts is needed for a second version; arbitrary positive angular oscillations are harmless for that version. Neither compactness condition is automatic: an explicit smooth flat subharmonic construction below has genuinely noncompact negative parts at critical record scales.

No historical novelty claim is made. The target remains A. Eremenko, *Conjectured inequality for subharmonic functions* (4 April 2015), https://www.math.purdue.edu/~eremenko/dvi/subh1.pdf. The source's homogeneous and harmonic cases are credited prior results. All quotients here are evaluated only where the actual denominator B is positive, under the [first-pass convention](../baseline/two_pass/README.md). No equivalence with assigning zero to 0/0 is asserted.

Write

u_j(0)=0,  I(r)=integral med(u_1,u_2,u_3)(r exp(i theta)) dtheta,

B(r)=max_(j,theta) u_j(r exp(i theta)),

U_j(t,theta)=u_j(exp(t+i theta)),  b(t)=B(exp t),

A(t)=integral_(-infinity)^t (t-s)b(s) ds,  a(t)=A(t)/b(t).

Angular integrals use ordinary, unnormalized Lebesgue measure on [0,2 pi]. The [previously audited denominator lemma](../baseline/two_pass/proofs/first_pass_theory.md) gives b>=0, b(t)->0 at negative infinity, circle integrability, and nonnegative angular means. We impose A(t)<infinity whenever using the estimates below. This holds at every selected infinitely-flat record scale and at every finite zero-disk boundary scale.

## 1. A quadratic integrated heat-smoothing inequality

For tau>0 let P_tau be circular heat smoothing, with kernel

k_tau(theta)=sum_(ell in Z) (4 pi tau)^(-1/2) exp(-(theta+2 pi ell)^2/(4 tau)).

It is nonnegative, smooth, symmetric, and has integral one. Put

E_tau(t)=sum_j ||U_j(t,.)-P_tau U_j(t,.)||_1/b(t).

### Theorem 1

For arbitrary whole-plane subharmonic u_j with u_j(0)=0, at every b(t)>0 with A(t)<infinity,

I(exp t)/b(t) >= -3 sqrt(pi/(2 e)) a(t)/tau - E_tau(t)/4.       (1)

In particular, no continuity of the original subharmonic representatives on the circles is required.

### Proof of the smoothing estimate

The real-line heat kernel g_tau satisfies

||g_tau''||_1 = sqrt(2/(pi e))/tau.

Indeed g_tau''(x)=(x^2/(4 tau^2)-1/(2 tau))g_tau(x). Substituting x=sqrt(2 tau)z reduces its norm to E|Z^2-1|/(2 tau), where Z is standard normal; integration at z=+-1 gives E|Z^2-1|=4 exp(-1/2)/sqrt(2 pi). Periodization therefore gives

||k_tau''||_1 <= c_0/tau,  c_0=sqrt(2/(pi e)).                 (2)

For each component, b(s)-U_j(s,.) is nonnegative and its mass is at most 2 pi b(s). Since integral k_tau''=0,

||partial_theta^2 P_tau U_j(s,.)||_1
<= 2 pi b(s)||k_tau''||_1.                                   (3)

Define V_j=P_tau U_j and

R_j(t,theta)=integral_(-infinity)^t (t-s)partial_theta^2 V_j(s,theta) ds.

Positive angular convolution preserves the positive cylindrical Laplacian measure. More explicitly, if mu_j=U_(j,tt)+U_(j,theta theta), then for fixed theta its smoothing is the positive t-measure

nu_(j,theta)(S)=integral_(S x circle) k_tau(theta-alpha) dmu_j(s,alpha).

Testing the distribution identity against eta(t)k_tau(theta-alpha) gives

(V_j+R_j)_(tt)=nu_(j,theta)>=0.

The functions V_j and R_j are continuous; the continuity detail for nonsmooth u is supplied below. Their limits at negative infinity are zero. For V_j, use ||U_j(s,.)||_1<=4 pi b(s) and the bounded heat kernel. For R_j, use the bounded second derivative of that kernel and the integrable weighted tail defining A. Thus V_j+R_j is convex with finite zero left limit, and consequently

V_j>=-R_j.                                                    (4)

The angular mean of R_j is zero. Equations (3),(4) give

||V_j(t,.)^-||_1 <= ||R_j(t,.)^+||_1
= (1/2)||R_j(t,.)||_1
<= pi ||k_tau''||_1 A(t).                                    (5)

Heat smoothing preserves the angular mean. Therefore the positive and negative parts of U_j-V_j have equal integrals, and

||U_j^-||_1 <= ||V_j^-||_1+(1/2)||U_j-V_j||_1.                 (6)

For any three real numbers, including the almost-everywhere finite circle values here,

med(x_1,x_2,x_3) >= -(1/2) sum_j x_j^-.

If the median is negative, at least two numbers have negative parts at least its magnitude; if it is nonnegative the inequality is immediate. Integrating, using (5),(6), summing the three components, and applying (2) proves

I/b >= -(3 pi/2)(c_0/tau)a-E_tau/4,

which is (1).

### Continuity detail for arbitrary subharmonic functions

For every smooth angular kernel K, the weighted angular convolution K*U is finite and continuous on each compact positive-radius annulus. Here is a direct justification rather than a continuity assumption. On a slightly larger annulus, use local Riesz decomposition to write u as a harmonic function plus a logarithmic potential of a finite positive measure with compact support. The smoothed logarithmic kernel is

L_K(r,theta,zeta)=integral K(theta-alpha)log|r exp(i alpha)-zeta| d alpha.

This is jointly continuous and bounded when r ranges over a compact interval away from zero and zeta over a compact set. To verify the only delicate point, truncate the logarithm below at log eta. The truncated integral is continuous. Uniformly in these parameters, the angular length where |r exp(i alpha)-zeta|<eta is O(eta), and the integral of the logarithmic singularity on that set is O(eta(1+|log eta|)). The constants are uniform because r is bounded below. The truncated integrals therefore converge uniformly. Integrating the resulting bounded continuous kernel against the finite Riesz measure proves continuity, and the harmonic summand is immediate. Apply the same argument to K'' for the angular derivative in R_j.

This also justifies the all-radii formulation of (1), rather than merely an almost-everywhere-in-radius statement. The distributional argument constructs each slice measure explicitly; it does not restrict an arbitrary distribution to a line.

## 2. Escaping angular frequency below the radial scale

Let TV denote total variation on the circle, with infinity allowed. At a radius where it is finite put

D(t)=sum_j TV(U_j(t,.))/b(t).

For a periodic BV function f, ||f(. -x)-f||_1<=|x| TV(f). Real Gaussian averaging of this inequality gives

E_tau(t)<=2 sqrt(tau/pi)D(t).                                 (7)

### Theorem 2

At every radius satisfying Theorem 1 and D(t)<infinity,

I(exp t)/b(t) >= -C_* [a(t)D(t)^2]^(1/3),                    (8)

C_* = [81/(16 sqrt(2 pi e))]^(1/3) < 1.0700.

Indeed (1),(7) give C_0 a/x^2+D x/(2 sqrt(pi)), with x=sqrt(tau) and C_0=3 sqrt(pi/(2e)). Its minimum is attained at x^3=4 sqrt(pi)C_0 a/D; substitution gives the displayed constant. If D=0, all three circle profiles are constants with nonnegative means, and the conclusion holds directly.

The criterion is a(t)^(1/2)D(t)->0 along a sequence. It allows D(t)->infinity. It is therefore genuinely different from the earlier fixed-scale angular compactness assumption.

### Flat-origin consequence

At a previously established record scale t for slope M,

b(s)<=b(t)exp(M(s-t)) for s<=t,

one has a(t)<=M^(-2), and (8) becomes

I(exp t)/b(t)>=-C_*[D(t)/M]^(2/3).                            (9)

Consequently, if M_k->infinity and record scales t_k->-infinity can be selected with D(t_k)=o(M_k), the stronger small-radius limsup is nonnegative. This proves the normalized-supremum conjecture for that class, even if normalized angular profiles fail L1 compactness.

Conversely, a uniformly negative counterexample I/B<=-epsilon would have to satisfy

D(t)>= (epsilon/C_*)^(3/2) M                                (10)

at every such record scale with finite D. Infinite variation is not excluded by this necessary condition.

### Positive-denominator zero-disk boundary

If the last joint zero disk has radius R_0>0 and t_0=log R_0, then a(t)<=(t-t_0)^2/2. Hence

I(exp t)/b(t)>=-C_*2^(-1/3)[(t-t_0)D(t)]^(2/3).              (11)

In particular, (t-t_0)D(t)->0 yields a nonnegative lower limit at the actual positive-denominator boundary. The more precise condition a(t)^(1/2)D(t)->0 can be substantially weaker and should be used when available.

### A strict extension beyond angular compactness

The [previously audited smooth flat positive example](../baseline/two_pass/proofs/second_pass_flat_scale.md)

q(r,theta)=exp(-1/r^2)[1+(1/4)sin(r^(-1)cos theta)]

has noncompact normalized angular profiles. For three identical copies and r small, B=(5/4)exp(-1/r^2). At its record r=sqrt(2/M), writing k=1/r gives

D <= (12/5)k = (12/5)sqrt(M/2).

Thus D/M->0 and Theorem 2 applies, although the earlier angular compactness hypothesis fails. The same type of example can have rapid positive oscillations; Section 3 below avoids controlling those oscillations altogether.

## 3. A version that controls only negative angular mass

The following elementary estimate is useful because positive oscillations need no compactness assumption.

### Lemma 3: threshold testing

Let f be integrable on the circle, f<=1, g=f^-, and let P=P_tau. Define

H_tau(g)=integral_R g_tau(x)||g(. -x)-g||_1 dx.

Then

||g||_1 <= ||(Pf)^-||_1+H_tau(g)+2 sqrt(2 pi H_tau(g)).       (12)

**Proof.** Write f=p-g, where 0<=p<=1 and pg=0. For delta>0 put h=min(g/delta,1). Then ph=0, 0<=h<=1, and integral hg>=integral g-2 pi delta. Gaussian averaging and the delta^(-1)-Lipschitz property of the truncation give

||Pg-g||_1<=H_tau(g),

||Ph-h||_1<=H_tau(g)/delta.

By symmetry of P,

integral h Pf = integral p Ph-integral g Ph
<= H_tau(g)/delta-||g||_1+2 pi delta+H_tau(g).

The left side is at least -||(Pf)^-||_1. Rearrange and minimize 2 pi delta+H_tau(g)/delta. If H_tau(g)=0, send delta down to zero. This proves (12). QED.

For our normalized profiles f_j=U_j/b, let g_j=f_j^- and H_j=H_tau(g_j). Combining (5),(12) with the median-negative-parts bound yields

I(exp t)/b(t) >= -3 sqrt(pi/(2 e)) a(t)/tau
                -(1/2)sum_j[H_j+2 sqrt(2 pi H_j)].             (13)

### Corollary 4: negative-part compactness suffices

At an infinitely flat origin, suppose the families of normalized negative parts U_j(t,.)^-/b(t) are asymptotically relatively compact in L1. Then the stronger small-radius normalized limsup is nonnegative. At a zero-disk boundary the same hypothesis gives the nonnegative positive-denominator lower limit. In fact, along the selected origin scales, or throughout the boundary limit respectively, every component's normalized negative-part integral tends to zero.

To see this, a bounded relatively L1-compact family has uniform small-translation continuity. Integrating that modulus against the Gaussian, splitting into a small-translation region and a Gaussian tail, shows H_tau->0 uniformly as tau downarrow zero. The family is bounded because ||g_j||_1<=2 pi. Fix tau first, choose a flat record with a as small as required, and apply (12),(5); or take the zero-disk boundary limit with tau fixed. Finally send tau to zero.

More generally, if D_-(t)=sum_j TV(g_j(t,.)), then H_j<=2 sqrt(tau/pi)TV(g_j). Thus a(t)^(1/2)D_-(t)->0 along any sequence with a(t)->0 is sufficient, by choosing sqrt(tau) much larger than sqrt(a) and much smaller than 1/D_-. The analogous record condition is D_-(t_k)=o(M_k). No control of the normalized positive parts is used.

This is a sufficient condition, not an assertion that subharmonicity implies negative-part compactness. The next construction rules out that assertion even in the smooth all-flat setting.

## 4. A smooth critical-frequency example with noncompact negative parts

### Construction

Choose a C-infinity cutoff eta on R with 0<=eta<=1, eta=1 near zero, and support in [-1,1]. Write

A_1=||eta'||_infinity,  A_2=||eta''||_infinity,

and choose L>=32(1+A_1+sqrt(A_2)). Choose an integer n_0, a power of two, with n_0>=256(L+1). Set

n_k=n_0 2^k,  t_k=-log n_k,

chi_k(t)=eta(n_k(t-t_k)/L),  k>=0.

Their supports are disjoint: their centers are log 2 apart, and each support half-width is at most 1/256. For 0<r<=1/2, define

q(r,theta)=exp(-1/r)[1+2 sum_(k>=0) chi_k(log r)cos(n_k theta)],

q(0)=0.                                                        (14)

At most one term in the sum is nonzero at any positive radius.

### Subharmonicity, with a uniform margin

Put t=log r, Q=exp(-t)=1/r, and f=exp(-Q). Then f_t=Qf and f_tt=(Q^2-Q)f. Outside the supports, q=f and its cylindrical Laplacian is positive because Q>=2. On support k, abbreviate n=n_k and chi=chi_k. Direct differentiation gives

(q_tt+q_theta theta)/f
= Q^2-Q+2[chi(Q^2-Q-n^2)+2Q chi'+chi'']cos(n theta).           (15)

Write h=t-t_k, so |h|<=L/n<=1/256 and Q/n=exp(-h). The elementary estimates exp(|h|)<=2 and |exp(-2h)-1|<=4|h| give

(Q^2-Q)/n^2 >= 1-(2L+2)/n >=127/128,

2|chi(Q^2-Q-n^2)+2Qchi'+chi''|/n^2
<= (8L+4)/n+8A_1/L+2A_2/L^2
<= 1/32+1/4+1/512.

Consequently the cylindrical Laplacian is at least

(363/512)n^2 f>0                                                (16)

on each support. The planar Laplacian differs by the positive factor r^(-2).

Every Cartesian derivative on these annuli is bounded by exp(-1/r) times a fixed reciprocal power of r (depending on the derivative order but not on k). Indeed n_k is comparable to 1/r there; derivatives of chi_k and cos(n_k theta), as well as polar-to-Cartesian conversion, introduce only such powers. The cutoff derivatives of each fixed order have uniform bounds. Outside the supports the same statement is immediate for f. Hence (14) extends to a C-infinity function flat at zero.

A whole-plane smooth subharmonic extension can be made without changing the germ for r<=1/4. Choose a smooth radial cutoff equal to one for r<=1/2 and zero for r>=1, multiply the germ by it, and add a sufficiently large smooth radial subharmonic function which vanishes for r<=1/4 and has strictly positive Laplacian for r>1/4. Its Laplacian dominates the cutoff error on the compact transition annulus. One explicit correction is P(log r), with P(t)=0 for t<=log(1/4) and

P(t)=integral_(log(1/4))^t (t-s)exp[-1/(s-log(1/4))^2] ds

afterward. This is the [audited extension mechanism from the preceding pass](../baseline/two_pass/audits/second_flat_scale_acceptance.md). Negative values of the germ cause no difficulty for that mechanism.

### Exact negative-part obstruction at record scales

Take all three functions equal to the extension. At r_k=1/n_k, chi_k=1, and

B(r_k)=3 exp(-n_k),

q(r_k,theta)/B(r_k)=(1+2cos(n_k theta))/3,

g_k(theta)=(q/B)^- = (-1-2cos(n_k theta))^+/3.                  (17)

For every s<=t_k, b(s)<=3exp(-exp(-s)), and concavity of -exp(-s) gives

b(s)<=b(t_k)exp(n_k(s-t_k)).                                  (18)

Thus t_k is an honest record scale of slope M=n_k, with a(t_k)<=n_k^(-2).

The negative-part integrals are independent of k and strictly positive:

integral g_k dtheta=(2sqrt(3)-2pi/3)/3>0.                      (19)

Every fixed nonzero angular Fourier coefficient of g_k eventually vanishes, since its only frequencies are integer multiples of n_k. Its zeroth coefficient is fixed. If an L1-convergent subsequence existed, its limit would therefore be the constant mean of g_k. But the L1 distance of g_k from that mean is independent of k and strictly positive, by the measure-preserving change theta -> n_k theta. Hence the normalized negative parts are not L1-precompact.

The exact variations are

TV(q/B)=(8/3)n_k,  TV(g_k)=(2/3)n_k.

For the identical triple, D(t_k)=8n_k and D_-(t_k)=2n_k. Their ratios to the record slope do not vanish. This realizes the critical angular/radial regime excluded by the new sufficient conditions, rather than supplying a hidden counterexample to those conditions.

Finally, the angular mean of q is f>0 at every small radius. For three identical copies the median is q, so I(r)>0 there; at r_k the normalized quotient is exactly 2pi/3. This example is affirmative for the original conjecture. It disproves only automatic negative-part compactness, including compactness at the very record scales used in the flat-origin argument.

## 5. The quadratic curvature scale is intrinsic to localized positive smoothing

Let K be a nonnegative C^2 probability kernel on the circle. Represent angles in [-pi,pi] and put sigma^2=integral theta^2 K(theta)dtheta. If 0<sigma<=1/2, choose n=floor(1/sigma). Then n>=1/(2sigma), n sigma<=1, and

integral cos(n theta)K(theta)dtheta >=1-n^2 sigma^2/2>=1/2.

Integrating by parts twice gives

||K''||_1 >= n^2 |integral cos(n theta)K(theta)dtheta|
>=1/(8sigma^2).                                               (20)

Thus the second-derivative L1 cost of positive kernels localized on angular scale sigma cannot be uniformly subquadratic in 1/sigma. The improvement from the former cubic Fejer pointwise cost to the present quadratic integrated cost is genuine; merely substituting more localized positive kernels cannot remove the remaining critical-scale obstruction through this curvature-norm estimate. This is a limitation of that estimate, not a theorem excluding every possible smoothing-based proof.

## 6. Remaining frontier and verification

The new results allow angular frequencies to escape and distinguish negative oscillations from harmless positive ones. They require those negative oscillations, or the full variation in Theorem 2, to be subcritical relative to the radial scale. Section 4 proves that critical negative angular variation really can occur for smooth all-flat admissible functions, so the residual regime cannot be dismissed by regularity or compactness assertions.

No general classification of coupled radial/angular boundary layers, no all-radii uniformly negative triple, and no proof of the unrestricted normalized-supremum assertion is supplied here. The [cyclic two-harmonic theorem](cyclic_two_harmonic.md) treats a separate restricted periodic branch of this same third shared pass.

The [author exact certificate](../certificates/concentration_author.json) checks the Gaussian norm, minimization constant, cutoff-Laplacian identity and margin, record concavity calculation, exact negative-part integral, and exact total variations. The [independent concentration audit](../audits/concentration_acceptance.md) reconstructs the analytic and finite arguments, with its [exact certificate](../certificates/concentration_audit.json). These finite checks supplement rather than replace the measure, compactness, smooth-extension, and limiting arguments above.
