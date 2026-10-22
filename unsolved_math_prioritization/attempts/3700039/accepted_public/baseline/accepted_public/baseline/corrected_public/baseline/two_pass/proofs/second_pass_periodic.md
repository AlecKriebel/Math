# Second substantive pass: genuinely two-variable logarithmic phases

## Disposition

**The general periodic-phase problem and the original normalized-supremum conjecture remain unresolved.** This pass proves two affirmative results for genuinely shape-changing periodic profiles, gives an exact admissible example with both negative and positive phases, and proves that a fixed finite-point positivity argument cannot work for the unrestricted periodic cone. No full counterexample is claimed.

The problem is the median conjecture in A. Eremenko, *Conjectured inequality for subharmonic functions* (4 April 2015), https://www.math.purdue.edu/~eremenko/dvi/subh1.pdf. The first-pass report and audits already supplied and checked the source and the positive-denominator convention. The results here use that same convention. The source credits the one-angle homogeneous argument used below; no novelty claim is made for it or for these partial extensions.

## 1. Setup and a positive scalar inverse

Let rho>0 and omega>0. Coordinates s and theta are modulo 2*pi. Write

L_omega = (omega*d_s+rho)^2+d_theta^2.

For continuous real profiles H_j with L_omega H_j>=0 in distributions, put

u_j(r*exp(i*theta))=r^rho H_j(omega*log(r),theta),  u_j(0)=0,

M(s)=integral_0^(2*pi) med(H_1(s,theta),H_2(s,theta),H_3(s,theta)) dtheta.

The polar Laplacian calculation and boundedness of H_j give whole-plane subharmonic functions, continuous at zero. In this class a uniformly negative M would give a genuine counterexample, because its phase is periodic and the positive normalizing maxima are bounded above. Merely having some negative phases is insufficient.

For a real periodic smooth f, the unique periodic solution of

(omega*d_s+rho)^2 a=f

is

a(s)=integral_0^infinity t*exp(-rho*t)*f(s-omega*t) dt.             (1)

Indeed, the inverse of omega*d_s+rho is the same integral without t; integration by parts verifies the equation, and composing the inverses gives (1). The homogeneous solutions are linear combinations of exp(-rho*s/omega) and s*exp(-rho*s/omega), so none is periodic except zero. Thus f>=0 implies a>=0. If f is nonzero and nonnegative, periodicity and strict positivity of the integration kernel give a(s)>0 for every s. Nonnegative convolution and uniform limits extend the non-strict assertion to continuous a with distributional nonnegative right-hand side.

In particular, the angular mean a_j(s)=(1/(2*pi))*integral H_j(s,theta)dtheta is nonnegative at every phase, because its right-hand side is the angular mean of L_omega H_j. This also follows from the submean inequality for the associated planar functions.

## 2. An arbitrary-phase-modulation theorem

### Theorem A: common sign-reversing angular symmetry

Suppose there is a common angular shift alpha for which

H_j(s,theta)=a_j(s)+Q_j(s,theta),
Q_j(s,theta+alpha)=-Q_j(s,theta),   j=1,2,3.

The Q_j may otherwise depend arbitrarily and independently on both variables. If L_omega H_j>=0, then

M(s)>=2*pi*min_j a_j(s)>=0                                      (2)

at every phase s.

**Proof.** Integrating the sign-reversal identity shows that Q_j has angular mean zero. Therefore a_j is the angular mean of H_j and is nonnegative by (1). For fixed s and theta,

H_j(s,theta+alpha)+H_j(s,theta)=2*a_j(s)>=2*min_k a_k(s).

Coordinatewise monotonicity and oddness of the median give

med_j H_j(s,theta+alpha)+med_j H_j(s,theta)>=2*min_k a_k(s).

Integrating, and using invariance of angular measure under translation, gives (2). QED.

An important explicit family is

H_j(s,theta)=a_j(s)+sum over odd k of [A_jk(s)*cos(k*n*theta)+B_jk(s)*sin(k*n*theta)],

with arbitrary periodic coefficient functions and common positive integer n. Use alpha=pi/n. Different relative amplitudes, phases and angular shapes can change with s, so this is not a common rotating-separable ansatz. The theorem does not cover a simultaneous even and odd angular spectrum lacking a common sign-reversing shift.

## 3. Fixed finite forcing becomes positive at high phase frequency

Fix a noninteger rho>0 and three nonzero, nonnegative real trigonometric polynomials F_j(s,theta). Their Fourier convention is

F_j=sum_(m,n) f_j(m,n)*exp(i*(m*s+n*theta)).

For each omega>0 define the unique trigonometric-polynomial solution

H_j,omega=sum_(m,n) f_j(m,n)/((rho+i*omega*m)^2-n^2) *exp(i*(m*s+n*theta)).   (3)

No denominator vanishes: its imaginary part can vanish only when m=0, after which rho noninteger excludes rho=|n|.

Let g_j(theta) be the temporal average of F_j, and let h_j(theta) be the temporal average of H_j,omega. The latter is independent of omega and satisfies

h_j''+rho^2*h_j=g_j>=0.

Put T=pi/rho and

q_j(theta)=(1/rho)*integral_0^T sin(rho*(T-x))*g_j(theta+x) dx,

delta=(1/2)*min_(j,theta) q_j(theta),
S=max_j sum_(m!=0,n) |f_j(m,n)|.                                (4)

Each g_j is a nonzero nonnegative trigonometric polynomial. It cannot vanish on an interval without vanishing identically. Since the sine kernel is strictly positive inside (0,T), each q_j(theta)>0; compactness gives delta>0.

### Theorem B: explicit high-frequency exclusion

For every omega>rho,

M_omega(s)>=2*pi*(delta-S/(omega^2-rho^2))                       (5)

for every phase s. In particular, all median phases are strictly positive whenever

omega^2>rho^2+S/delta.                                         (6)

If S=0, the profiles are independent of s and their median integral is already strictly positive.

**Proof.** The elementary half-period variation-of-constants identity gives

h_j(theta+T)+h_j(theta)=q_j(theta)>=2*delta.

The median pairing argument therefore gives

integral med(h_1,h_2,h_3)>=2*pi*delta.

For m!=0 and omega>rho,

|((rho+i*omega*m)^2-n^2)|
 >=omega^2*m^2+n^2-rho^2
 >=omega^2-rho^2.

Consequently the nonzero-temporal-frequency part R_j=H_j,omega-h_j obeys

sup_(s,theta)|R_j|<=S/(omega^2-rho^2).

The median is 1-Lipschitz in the maximum norm of its three inputs. Integrating that estimate proves (5), and (6) proves strict positivity. QED.

This is a uniform affirmative result over every phase for arbitrary fixed nonzero nonnegative finite Fourier forcings, including square forcings with mixed even/odd angular modes. Its threshold depends on the actual forcing and rho; it is not a uniform restriction on all possible forcings. Allowing the forcing to change with omega defeats the fixed-forcing conclusion. It does not settle intermediate frequencies.

## 4. Exact mixed-sign phase example

The stronger assertion that every admissible doubly periodic profile has M(s)>=0 at every phase is false.

Set rho=3/2, omega=2/25 and take the integer-coefficient polynomial

P(s,theta)=1+2*cos(theta)+6*cos(s-theta)+sin(s-theta)
           -5*sin(s)-5*cos(s+theta)+2*sin(s+theta).

Let F=P^2, and define H by (3) with this forcing. Define three profiles

H_j(s,theta)=H(s,theta+2*pi*j/3),   j=0,1,2.

These are real finite trigonometric polynomials, and

L_omega H_j=P(s,theta+2*pi*j/3)^2>=0

exactly, not merely at a mesh. Their associated planar u_j are therefore whole-plane subharmonic with value zero at zero. The scalar inverse (1) shows their angular means are strictly positive at every phase, so their normalizing circle maxima are positive.

The exact certificate proves

M(0)/(2*pi)<-1/3,       M(pi)/(2*pi)>1.                         (7)

Thus their median integral is negative on the unit circle but positive at r=exp(25*pi/2). The pattern repeats logarithmically. This example satisfies the original supremum assertion with a strictly positive value; it is neither a counterexample nor a proof of the unrestricted periodic problem.

### Verification details

The finite certificate constructs the finite complex Fourier coefficients as pairs of rational numbers and squares P by exact coefficient convolution. It divides by the exact rational complex multipliers and checks every coefficient of L_omega H=P^2.

At phases 0 and pi, each temporal exponential is respectively 1 or (-1)^m, so all angular Fourier coefficients remain rational. Only angular frequencies -2 through 2 occur. At 768 equally spaced angular points, the three median inputs are simply the same slice evaluated at indices k, k+256 and k+512.

The certificate first proves

3.141592653589793238462643383279 < pi < 3.141592653589793238462643383280

using alternating rational bounds in Machin's identity pi=16*atan(1/5)-4*atan(1/239). It uses rational sine and cosine Taylor polynomials through degree 32, with common error at most

4^33/33! + half the displayed pi interval width.

All angular arguments are reduced to [-pi,pi]. Taylor's theorem and the 1-Lipschitz property of sine and cosine justify this bound.

For a slice written a_0+2*sum_(n=1)^2 [Re(a_n)*cos(n*theta)-Im(a_n)*sin(n*theta)], the exact rational derivative bound used is

D=2*sum_(n=1)^2 n*(|Re(a_n)|+|Im(a_n)|).

The median of its three rotations is D-Lipschitz. Equal-grid quadrature for its normalized integral has error at most D*pi/(2*768): integrate the distance to each grid point over its centered cell. The certificate adds the Taylor error and performs the final comparisons to -1/3 and 1 using exact rational arithmetic. No floating-point evaluation is used for acceptance.

The displayed, non-authoritative decimal enclosures of the proved rational bounds are:

- phase 0: -0.454302 < M(0)/(2*pi) < -0.355395;
- phase pi: 1.253598 < M(pi)/(2*pi) < 1.286161.

The exact fractions and angular coefficients are recorded in [the exact phase certificate](../certificates/log_periodic_exact.json). The intentionally conservative displayed endpoints are for readability; the rational file and comparisons are the certificate.

## 5. Why a fixed finite-point extension of angular pairing cannot work

### Theorem C: finite-point positivity obstruction

Let rho>0 be noninteger and omega>0. Choose any finite nonempty list of torus points x_1,...,x_k and positive weights c_1,...,c_k. There is a smooth real periodic H satisfying L_omega H>=0 for which

sum_(a=1)^k c_a*H(x_a)<0.                                    (8)

In particular, there is no universal fixed pair of torus shifts and positive coefficient that gives the pointwise pairing inequality used in the one-angle proof. The statement concerns the full cone; it does not refute special symmetry-based pairing.

**Proof.** The Fourier multipliers of L_omega are all nonzero, as above. They therefore define a periodic fundamental solution G with L_omega G=delta_0, where delta_0 has total mass one with respect to ordinary torus area.

Here is its local singularity with its sign fixed explicitly. Near zero choose the local coordinate y=s/omega. Then

Phi(s,theta)=(1/(2*pi*omega))*exp(-rho*s/omega)
             *log(sqrt((s/omega)^2+theta^2))

satisfies L_omega Phi=delta_0 locally. This follows by conjugating (d_y+rho)^2+d_theta^2 by exp(-rho*y), and using Delta log(sqrt(y^2+theta^2))=2*pi*delta_(0,0), with delta(y)=omega*delta(s).

Multiply Phi by a smooth cutoff equal to one near zero and supported in a coordinate patch. Its image under L_omega is delta_0 plus a smooth periodic function R supported away from zero. Invert L_omega on R by Fourier series. The inverse is smooth: R has rapidly decreasing coefficients and the reciprocal multipliers have at most polynomial growth (indeed decay quadratically at large frequency). Subtracting it from the cutoff fundamental solution constructs G and shows

G(s,theta)=(1/(2*pi*omega))*log(sqrt((s/omega)^2+theta^2))+O(1)

near zero. Thus G tends to negative infinity at its source and is smooth elsewhere.

Merge repeated x_a. Put a nonnegative smooth approximate unit eta_epsilon of total mass one at x_1 and set H_epsilon=G*eta_epsilon, with ordinary area convolution and the indicated translation. Then H_epsilon is real and smooth, and L_omega H_epsilon=eta_epsilon>=0. At x_1 its value tends to negative infinity logarithmically as epsilon decreases to zero. At every other distinct x_a it converges to a finite value. Positivity of the coefficient at x_1 gives (8) for sufficiently small epsilon. QED.

This pinpoints a limitation of one natural analytic route. A proof for the general two-variable periodic class must use more than a fixed positive finite combination of point values on the entire L-subharmonic cone. The theorem does not exclude averaging inequalities, profile-dependent pairings, or a global energy argument.

## 6. Search evidence and the remaining mathematical problem

Floating-point square-forcing searches supplied leads only. They found no certified all-phase negative candidate and do not prove that one is impossible. The integer-coefficient example in Section 4 was reconstructed and certified by exact rational arithmetic; its conclusion is the mixed-sign statement (7).

Remaining open here: prove that an arbitrary admissible doubly periodic triple has some phase M(s)>=0, or find and rigorously certify a triple with M(s)<0 at every phase. Neither is established in this pass. The new affirmative classes do not resolve arbitrary subharmonic functions, and the finite-point obstruction is an obstruction to a proof method, not to the conjecture.
