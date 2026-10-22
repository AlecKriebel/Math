# Second-pass flat-scale analysis of the median inequality

## Result and scope

The unrestricted normalized-supremum conjecture remains unresolved. This report proves an affirmative result for continuous triples at an infinitely flat origin or a flat-disk boundary when their normalized angular profiles are relatively compact in L1. It also identifies the exact angular compactness failure a uniformly negative counterexample would need. Compactness is not assumed silently: explicit smooth admissible examples show it is not automatic. A separate example shows that exact power growth of the maximum does not force homogeneous or rotating-homogeneous dilation limits.

This is part of the second shared substantive pass on row 1762 / 3700039. No priority claim is made for these partial results.

The source target is A. Eremenko, *Conjectured inequality for subharmonic functions* (4 April 2015), https://www.math.purdue.edu/~eremenko/dvi/subh1.pdf. Its homogeneous and harmonic cases are credited prior cases. Write

- u_1,u_2,u_3 for whole-plane subharmonic functions with u_j(0)=0;
- I(r)=integral_0^{2 pi} med(u_1,u_2,u_3)(r exp(i theta)) dtheta;
- B(r)=max_{j,theta} u_j(r exp(i theta)).

As in the accepted first-pass reports, quotients are taken only where B(r)>0. The source does not specify what to do with zero denominators. No equivalence with assigning zero to 0/0 is claimed. The results below concern actual positive-denominator radii.

## 1. A quantitative positive-smoothing lemma

Assume the functions are continuous on the circles under consideration and throughout the inner punctured disk. This includes every triple smooth near the origin and every continuous flat-disk triple. Put

U_j(t,theta)=u_j(exp(t+i theta)),   b(t)=B(exp t).

Suppose, for the t in question,

A(t)=integral_{-infinity}^t (t-s)b(s) ds < infinity.

Let F_N be the nonnegative Fejer kernel of order N, with normalized integral 1, and write U_{j,N}=F_N*U_j for convolution in theta. Its Fourier weights are

w_n=1-|n|/(N+1),  |n|<=N.

Define

K_N=N(N+1)(N+2)/6.

Then, for every angle and every component,

U_{j,N}(t,theta) >= -K_N A(t).                                      (1)

Consequently, with

E_N(t)=sum_{j=1}^3 ||U_j(t,.)-U_{j,N}(t,.)||_L1 / b(t),

where every L1 norm uses the unnormalized measure dtheta on [0,2 pi],

one has at every b(t)>0

I(exp t)/b(t) >= -2 pi K_N A(t)/b(t) - E_N(t).                       (2)

### Proof

Let c_{j,n}(t) be the normalized complex Fourier coefficient of U_j(t,.). Submean at the origin gives a_j(t)=c_{j,0}(t)>=0; the circle maximum gives a_j(t)<=b(t). For n != 0, use the nonnegative function b(t)-U_j(t,theta):

|c_{j,n}(t)| <= b(t)-a_j(t) <= b(t).

It follows that

|partial_theta^2 U_{j,N}(t,theta)|
 <= 2 b(t) sum_{n=1}^N n^2(1-n/(N+1))
 = K_N b(t).                                                       (3)

Also |U_{j,N}(t,theta)| <= (N+1)b(t). The first-pass denominator lemma gives b(t)->0 as t->-infinity. Integrability of A(t) makes

R_j(t,theta)=integral_{-infinity}^t (t-s) partial_theta^2 U_{j,N}(s,theta) ds

convergent, and R_j(t,theta)->0 as t->-infinity. Indeed its absolute value is bounded by K_N A(t), and the weighted-integral tail tends to zero.

The cylindrical Laplacian U_{j,tt}+U_{j,theta theta} is a nonnegative distribution. Positive angular convolution preserves that property. More precisely, for each fixed theta its convolution against F_N is a positive measure in t; this follows by integrating the nonnegative kernel F_N(theta-alpha) against the positive cylindrical Laplacian measure. Thus

W_j(t,theta)=U_{j,N}(t,theta)+R_j(t,theta)

satisfies W_{j,tt}>=0 in the one-dimensional distributional sense. The displayed functions are continuous, so W_j is convex in t. It tends to zero at the left endpoint -infinity. Any convex function with that finite left limit is nondecreasing and is at least its limit. Hence W_j>=0. Therefore

U_{j,N}>=-R_j>=-K_N A,

which proves (1). This argument does not differentiate nonsmooth u_j pointwise or restrict an arbitrary distribution to a slice: the positive convolution defines the required slice measure explicitly.

Finally, coordinatewise monotonicity gives med(U_{1,N},U_{2,N},U_{3,N})>=-K_N A. The median is 1-Lipschitz in the maximum norm on triples, so its integrated error is bounded by the sum of the three L1 smoothing errors. Integration proves (2).

The assumed continuity is sufficient for all displayed circle and convolution expressions. No assertion here silently extends the theorem to arbitrary discontinuous subharmonic representatives.

## 2. Infinite-order origin: record scales with honest normalization

Suppose B(r)>0 at arbitrarily small radii and, for every M>0,

B(r)=o(r^M) as r->0.                                                (4)

Since the positive-denominator domain is an interval, this means B(r)>0 for every r>0. Condition (4) holds whenever all three functions are smooth and flat at zero and do not vanish jointly on a disk.

For each M>0 and each T, the continuous function exp(-Ms)b(s) on s<=T tends to zero at -infinity and is positive at T. It therefore attains a positive maximum at some tau<=T. At this record scale,

b(s)<=b(tau) exp(M(s-tau)),  s<=tau,

and consequently

A(tau)/b(tau)<=integral_0^infinity x exp(-Mx) dx=1/M^2.               (5)

This controls the actual denominator. No homogeneous tangent or compactness of dilates has been presumed.

Assume in addition that the angular smoothing errors vanish uniformly toward the origin:

lim_{N->infinity} limsup_{t->-infinity} E_N(t)=0.                    (6)

Then

limsup_{r->0} I(r)/B(r)>=0.                                        (7)

To prove this, choose N so the eventual error in (6) is as small as desired, then choose M so 2 pi K_N/M^2 is equally small. Record scales tau can be chosen below every specified T, and (2),(5) apply. Taking a sequence of error tolerances tending to zero proves (7).

In particular, finite angular Fourier bandwidth near zero implies (6): the coefficient bound in Section 1 controls all finitely many modes, and Fejer weights converge uniformly to 1 on them. Thus all-flat smooth finite-bandwidth triples are affirmative.

## 3. Flat-disk boundary: a stronger one-sided limit under the same compactness

Suppose R_0>0 is the last joint zero-disk radius, so B(r)=0 for r<=R_0 and B(r)>0 for r>R_0. Put t_0=log R_0. Monotonicity of b gives, for t>t_0,

A(t)=integral_{t_0}^t (t-s)b(s) ds
 <= (t-t_0)^2 b(t)/2.                                             (8)

Therefore (2) becomes

I(exp t)/b(t)>=-pi K_N(t-t_0)^2-E_N(t).                             (9)

If

lim_{N->infinity} limsup_{t downarrow t_0} E_N(t)=0,                (10)

then

liminf_{r downarrow R_0, r>R_0} I(r)/B(r)>=0.                       (11)

This is an actual positive-denominator boundary limit. It proves the normalized supremum assertion for this subclass without assigning a value to any 0/0 radius. The assumption only requires continuity near the boundary and the displayed relative angular compactness; the functions need not have a nonzero finite boundary jet. Finite angular bandwidth is again sufficient.

Indeed the proof yields more than a statement about the median: each component's negative-part L1 norm, divided by B(r), tends to zero at a flat-disk boundary under (10).

## 4. Exact meaning and necessity of the compactness condition

Each normalized angular profile U_j(t,.)/b(t) has L1 norm at most 4 pi: its positive part is bounded in integral by 2 pi and its mean is nonnegative. On the compact circle, uniform convergence under positive Fejer approximate identities is equivalent to relative compactness in L1 for a bounded family. For completeness:

- A relatively compact family has uniform approximate-identity convergence, by covering it with finitely many L1 balls and using the L1 contraction of convolution.
- If the approximation errors are uniform, each fixed-N image lies in a bounded finite-dimensional trigonometric-polynomial family; finite nets for those images give total boundedness of the original family.

Thus (6) or (10) is a precise asymptotic relative L1 compactness condition. Uniform equicontinuity of the normalized profiles is a sufficient, stronger condition. It is not asserted to follow from smoothness of the unnormalized functions.

If a continuous flat-disk triple were a counterexample with

I(r)/B(r)<=-epsilon<0 at every positive-denominator radius,

then (9) forces, for each fixed N,

liminf_{t downarrow t_0} E_N(t)>=epsilon.                           (12)

At an infinite-order origin, (2),(5) force at every selected record scale

E_N(tau)>=epsilon-2 pi K_N/M^2.                                    (13)

Taking large M and arbitrarily small record scales shows that normalized angular compactness must fail there too. This does not prove that such a counterexample exists. It isolates a necessary high-angular-frequency obstruction to this proof strategy.

## 5. Smooth flat examples show that angular compactness is extra

### 5.1 Flat origin

For 0<r<=1/2, define

q(r,theta)=exp(-1/r^2)[1+(1/4)sin(r^(-1)cos theta)],   q(0)=0.

It is positive away from zero and C-infinity flat at zero. Let phi=r^(-1)cos theta and f=exp(-1/r^2). Since phi=Re(1/z) is harmonic off zero,

r^6 Delta q/f
 =4(1-r^2)[1+(1/4)sin phi]
  -r cos theta cos phi -(r^2/4)sin phi
 >=3-r-(13/4)r^2
 >=27/16>0,  0<r<=1/2.                                           (14)

This germ has a C-infinity whole-plane subharmonic extension that leaves it unchanged for r<=1/4. To see this explicitly, choose a smooth radial cutoff chi equal to 1 for r<=1/2 and zero for r>=1. Put w=chi q. Choose a smooth radial p, zero for r<=1/4, whose cylindrical second derivative is

partial_t^2 p(exp t)=exp[-1/(t-log(1/4))^2],  t>log(1/4),

and zero before that point, with zero initial value and derivative. Then p is nonnegative, smooth, and subharmonic, with strictly positive Laplacian on r>1/4. The possibly negative Laplacian of w is confined to the compact annulus 1/2<=r<=1. On that annulus Delta p has a positive minimum, so w+C p is subharmonic for some finite C>=0. It agrees with q for r<=1/4.

Take all three functions equal to this extension. Near zero their maximum is exactly (5/4)exp(-1/r^2), because r^(-1)>=4 allows sin(r^(-1)cos theta) to attain 1. The normalized profile is

4/5+(1/5)sin(r^(-1)cos theta).

As k->infinity, every fixed angular Fourier coefficient of sin(k cos theta) tends to zero, while

integral_0^{2 pi}|sin(k cos theta)|dtheta ->4.

For the Fourier coefficients, change variables x=cos theta on each semicircle and apply the Riemann-Lebesgue lemma to an integrable Chebyshev-weighted function. For the norm, the change of variables gives 2 integral_{-1}^1 |sin(kx)|/sqrt(1-x^2) dx. The absolutely convergent cosine Fourier series of |sin y| has constant term 2/pi. Apply the Riemann-Lebesgue lemma termwise with an arbitrarily small uniformly bounded series tail to obtain the limit 2(2/pi) integral_{-1}^1(1-x^2)^(-1/2) dx=4. It follows that for every fixed N the single-component relative Fejer error tends to 4/5. The normalized angular profiles are not L1-precompact.

This is not a counterexample to the median inequality: all three functions are positive near zero, and their quotient there is exactly 8 pi/5. Its sole purpose is to show that smooth infinite-order flatness does not supply assumption (6).

### 5.2 The same obstruction can occur at a flat-disk boundary

For R_0=1 and t=log r in 0<t<=1/4, set

q(exp(t+i theta))=exp(-1/t^2)[1+(1/4)sin(t^(-1)cos theta)],

and set q=0 on r<=1. The function is smooth and flat across r=1. Writing phi=t^(-1)cos theta, a direct cylindrical-Laplacian calculation gives

t^6 (partial_t^2+partial_theta^2)q / exp(-1/t^2)
 =(4-6t^2)[1+(1/4)sin phi]
  +[-t+(1/2)t^3-(1/4)t^5] cos theta cos phi
  -(1/4)[t^2 cos^2 theta+t^4 sin^2 theta] sin phi.

For 0<t<=1/4 this is bounded below by

3-t-(19/4)t^2-(1/2)t^3-(1/4)t^4-(1/4)t^5>0.                       (15)

A cutoff outside t=1/4 and a sufficiently large smooth convex radial correction beginning at t=1/8 extend it subharmonically to the whole plane, without changing it for 0<t<=1/8 or on r<=1. The extension argument is identical to 5.1 on a compact annulus. The same normalized-profile calculation gives a single-component fixed-N error tending to 4/5 as r decreases to 1. Again all functions can be chosen identical and positive outside the disk, so this is only an obstruction to automatic compactness, not to the conjecture.

## 6. Exact maximum growth does not force homogeneous blow-up

For z=r exp(i theta), r>0, consider

u_1(z)=r^2,
u_2(z)=r^2[1/2+(1/10)cos(log r)cos theta],
u_3(z)=0,

with all values set to zero at z=0. These are continuous whole-plane subharmonic functions. Indeed, for u_2 the cylindrical Laplacian divided by r^2 is

2+(1/10)[2 cos(log r)-4 sin(log r)]cos theta
 >=2-sqrt(20)/10>0.

They are bounded above near zero and extend subharmonically there; their explicit uniform limit is zero. Since 0.4r^2<=u_2<=0.6r^2, one has exactly B(r)=r^2.

Nevertheless, every sequence of normalized dilates with log r_k converging modulo 2 pi to alpha has the locally uniform limit

(|z|^2, |z|^2[1/2+(1/10)cos(alpha+log|z|)cos(arg z)], 0),

with the natural zero value at z=0. None of these triples is homogeneous or common rotating-separable: the magnitude of u_2's angular oscillation varies with log|z| and cannot be obtained by rotating a fixed profile. Thus even an exact regular-variation law for B does not identify a homogeneous/spiral tangent. A proof using that identification requires an additional theorem that the scalar growth law does not itself provide.

This example also satisfies the median inequality, since its median is the positive second component. It supplies a logically precise obstruction to a general blow-up argument, not a negative candidate.

## 7. Remaining issue

The new estimates settle finite angular bandwidth and relatively angular-compact subcases at both flat frontiers. They do not control the joint regime in which angular frequencies escape at the same scales that the denominator changes rapidly. Positive subharmonicity alone does not give the required normalized angular compactness, as Section 5 proves. Noncompact Riesz support and arbitrary multiscale coupling remain available in the unrestricted problem. No normalization-free compactness claim, general homogeneous blow-up classification, or uniformly negative admissible triple has been established.
