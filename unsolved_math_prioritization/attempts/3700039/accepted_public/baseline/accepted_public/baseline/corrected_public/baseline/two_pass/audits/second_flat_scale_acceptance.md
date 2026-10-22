# Independent acceptance of the flat-scale partial results

## Decision and scope

Accepted under the stated continuity, flatness, and relative angular L1-compactness hypotheses. No mathematical correction to the audited report is required. The quantitative smoothing estimate, the two flat-frontier consequences, the explicit failures of automatic angular compactness, and the obstruction to an automatic homogeneous blow-up are valid. The unrestricted positive-denominator normalized-supremum conjecture remains unresolved.

This acceptance audits the second substantive pass; it adds no third research pass and makes no priority claim. The source target is A. Eremenko, *Conjectured inequality for subharmonic functions* (4 April 2015), [public source](https://www.math.purdue.edu/~eremenko/dvi/subh1.pdf). Its homogeneous and harmonic affirmative cases remain credited prior results. The source states no convention for zero denominators. Every quotient below is evaluated only where B(r)>0; nothing here identifies that convention with assigning zero to 0/0.

For three whole-plane subharmonic functions u_j with u_j(0)=0, set

I(r) = integral_0^{2 pi} med(u_1,u_2,u_3)(r exp(i theta)) dtheta,

B(r) = max_{j,theta} u_j(r exp(i theta)),

U_j(t,theta) = u_j(exp(t+i theta)), and b(t)=B(exp t).

All L1 norms in this acceptance use the unnormalized measure dtheta. The first-pass denominator classification supplies b>=0, monotonicity, continuity, b(t)->0 at negative infinity, and a positive-denominator set of the form (R_0,infinity), except for the globally zero triple.

## 1. The positive-smoothing estimate has the correct constants

Fix N. Use the genuinely nonnegative Fejer kernel k_N with integral 1 against dtheta:

k_N(theta) = (1/(2 pi)) sum_{|n|<=N} (1-|n|/(N+1)) exp(i n theta).

Thus U_{j,N}(t,theta)=integral k_N(theta-alpha)U_j(t,alpha)dalpha. This explicit convention is equivalent to the report's normalized convolution convention.

For normalized Fourier coefficients c_{j,n}, the mean a_j=c_{j,0} satisfies 0<=a_j<=b. Since b-U_j is nonnegative, every nonzero coefficient satisfies

|c_{j,n}| <= (1/(2 pi)) integral(b-U_j)dtheta = b-a_j <= b.

No pointwise lower bound on U_j is being presumed. Conjugate frequencies produce the factor 2 in

|partial_theta^2 U_{j,N}| <= 2 b sum_{n=1}^N n^2(1-n/(N+1))

= b N(N+1)(N+2)/6.

Writing K_N=N(N+1)(N+2)/6, the calculation is exact. Independently, the power-sum expressions give

2[N(N+1)(2N+1)/6 - N^2(N+1)^2/(4(N+1))] = K_N.

The coefficient absolute sum also gives |U_{j,N}|<=(N+1)b. This is enough to establish its zero left limit; no derivative limit for the original subharmonic functions is required.

### The positive-distribution step really is one-dimensional

Let mu_j be the positive Radon measure representing the cylindrical Laplacian U_{j,tt}+U_{j,theta theta}. For each fixed theta, define a measure on the t-axis by

nu_{j,theta}(A) = integral_{A x circle} k_N(theta-alpha) dmu_j(s,alpha).

It is positive and locally finite. For a smooth compactly supported test function eta(t), the distribution identity, tested against eta(t)k_N(theta-alpha), yields

integral U_{j,N}(t,theta) eta''(t)dt
+ integral partial_theta^2 U_{j,N}(t,theta) eta(t)dt
= integral eta(t) dnu_{j,theta}(t).

This is an explicit weighted measure construction. It does not restrict an arbitrary distribution to a slice. The positivity of k_N is essential: the order-one Dirichlet projection kernel is negative at angle pi and would not justify this argument.

Suppose A(T)=integral_{-infinity}^T (T-s)b(s)ds is finite. For t<=T put

R_j(t,theta)=integral_{-infinity}^t (t-s)partial_theta^2 U_{j,N}(s,theta)ds.

It is well-defined, its second t derivative equals partial_theta^2 U_{j,N}, and |R_j|<=K_N A(t). Moreover

0<=A(t)<=integral_{-infinity}^t (T-s)b(s)ds ->0 as t->-infinity.

The integrable dominating tail proves the limit without an unjustified differentiation at the origin. Hence W_j=U_{j,N}+R_j is continuous, has W_j''=nu_{j,theta}>=0 distributionally, and tends to zero at negative infinity. It is a convex function with finite left limit. Such a function is nondecreasing: take the left endpoint of a secant to negative infinity in the convex secant-slope inequality. Therefore W_j>=0 and

U_{j,N}(t,theta)>=-R_j(t,theta)>=-K_N A(t).

The zero left limit removes both affine integration constants. Convexity alone would be insufficient, as the constant function -1 demonstrates.

Coordinatewise monotonicity of the median gives the same pointwise lower bound for the median of the smoothed triple. The median's maximum-norm Lipschitz inequality and the sum of component L1 errors then give exactly

I(exp t)/b(t) >= -2 pi K_N A(t)/b(t) - E_N(t),

E_N(t)=sum_j ||U_j(t,.)-U_{j,N}(t,.)||_1/b(t).

The factor 2 pi belongs in the first term because I is not an averaged circle integral. Continuity on the stated punctured neighborhood suffices for this proof. An extension to arbitrary discontinuous subharmonic representatives has not been silently made.

## 2. Infinite-order origin: record scales and limit order

Assume b(t)>0 and e^{-Mt}b(t)->0 at negative infinity for every M>0. Fix M>0 and T. The continuous function g_M(s)=e^{-Ms}b(s), s<=T, tends to zero at the left endpoint and is positive at T. Choose a finite left cutoff before which g_M<g_M(T)/2. A maximum on the remaining compact interval is a positive global maximum on (-infinity,T]. Denote one maximizing location by tau<=T. Then, for s<=tau,

b(s)<=b(tau)e^{M(s-tau)}.

Consequently

A(tau)/b(tau)<=integral_0^infinity x e^{-Mx}dx=1/M^2.

This proves both existence and the correct comparison direction. As T is taken arbitrarily negative, the selected tau are arbitrarily negative. There is no need to differentiate b or assume it has a limiting logarithmic derivative.

The order of choices in the report is valid. Given an error tolerance delta>0, first choose one fixed N with limsup_{t->-infinity} E_N(t)<delta. Then take M large enough that 2 pi K_N/M^2<delta. Finally choose record scales beyond the eventual-error threshold and beyond any prescribed negative T. At those radii I/B>-2 delta. Letting delta decrease to zero proves the claimed limsup>=0. One does not send N to infinity while holding M fixed.

The record selection is substantive. For the superflat scalar example b(t)=exp(-exp(-2t)), M=8, T=0, log g_M=-8t-exp(-2t) has its maximum at tau=-log 2 rather than T. The exact difference log g_M(tau)-log g_M(0)=log 256-3 is positive. An estimate that simply declared every chosen radius a record would fail even for this elementary test.

If the triple is smooth and all-flat at the origin, its maximum is o(r^M) for every M by uniform Taylor remainders. The additional condition that it is not jointly zero on a disk supplies B>0 arbitrarily close to zero. Finite angular bandwidth is a sufficient special case of the angular condition, because the normalized finitely many Fourier coefficients are bounded and their Fejer weights tend uniformly to 1.

## 3. A joint zero disk supplies all boundary constants

If the last joint zero disk has radius R_0>0, write t_0=log R_0. The denominator lemma makes every U_j identically zero for t<=t_0; in particular, there is no unaccounted boundary value or incoming affine term. For t>t_0, monotonicity gives

A(t)=integral_{t_0}^t(t-s)b(s)ds <= b(t)(t-t_0)^2/2.

Therefore

I(exp t)/b(t)>=-pi K_N(t-t_0)^2-E_N(t).

Under lim_{N->infinity} limsup_{t downarrow t_0} E_N(t)=0, fix N first and take the boundary limit before letting N increase. This yields the stated liminf>=0 on actual positive-denominator radii.

The stronger componentwise assertion is also justified. Since U_{j,N}>=-K_N A,

||(U_j)^-||_1/b <= 2 pi K_N A/b + ||U_j-U_{j,N}||_1/b.

The same ordered limits make the right side tend to zero. A negative outgoing derivative hidden at the boundary cannot evade this proof: it would contribute a negative jump measure to W_j'', contradicting positivity.

## 4. The compactness hypothesis is neither vacuous nor automatic

For f=U_j/b, one has f<=1 and integral f>=0. Thus

||f||_1 = 2 integral f^+ - integral f <=4 pi.

Positive normalized convolution is an L1 contraction. On a relatively compact family, approximation by Fejer kernels is uniform: take a finite L1 net, approximate its finitely many members, and use the contraction to transfer the estimate. Conversely, uniform approximation errors let one approximate the entire family by one bounded finite-dimensional trigonometric-polynomial family, which has finite nets; hence the original family is totally bounded.

The asymptotic limsup formulation causes no quantifier gap. For any desired error, the hypothesis gives one N and a sufficiently close tail where the errors are uniformly small. That tail is approximated by a bounded finite-dimensional family. On any remaining closed t-interval inside the punctured neighborhood, continuity of U and positivity of b make t -> U_j(t,.)/b(t) continuous into L1, so that part of the family is compact. Combining the two gives the appropriate relative compactness near the endpoint. Conversely, compactness near the endpoint immediately yields the displayed asymptotic condition.

The necessary obstruction to a uniformly negative counterexample also follows with the reported strength. If I/B<=-epsilon on every positive-denominator radius, then at a zero-disk boundary

liminf_{t downarrow t_0} E_N(t)>=epsilon

for each fixed N. At the infinitely flat origin the conclusion applies on the selected record scales:

E_N(tau)>=epsilon-2 pi K_N/M^2.

This is not an all-small-radii lower bound for the origin errors. The report correctly retains the record-scale qualification.

## 5. The high-frequency smooth flat examples are valid

### 5.1 Origin germ: independent Cartesian derivation

On the punctured plane put R=x^2+y^2, H=1/R and phi=x/R. The germ is

q=exp(-H)(1+(1/4)sin phi).

The elementary product identity is

Delta q/exp(-H)
= (|grad H|^2-Delta H)(1+(1/4)sin phi)
+ (1/4)(Delta phi-2 grad H dot grad phi)cos phi
- (1/4)|grad phi|^2 sin phi.

Direct Cartesian differentiation gives

Delta phi=0, |grad phi|^2=R^{-2},

|grad H|^2-Delta H=4(1-R)/R^3,

Delta phi-2 grad H dot grad phi=-4x/R^3.

Multiplying by r^6 produces precisely the report's polar identity. On 0<r<=1/2 its lower bound is

3-r-(13/4)r^2 >=27/16>0.

Thus the local subharmonicity calculation is correct. The germ is strictly positive since its bracket lies between 3/4 and 5/4.

Every Cartesian derivative of the punctured-plane formula is exp(-1/r^2) times a finite sum bounded by a power of 1/r: derivatives of the rational phase and envelope have polynomial reciprocal growth, while sine and cosine are bounded. Consequently every derivative tends to zero faster than every power of r. Setting q(0)=0 therefore gives a C-infinity function flat to every order at the origin, not merely a continuous function with a small amplitude.

For the global extension, use the same explicit punctured-plane formula outside the germ, choose 0<=chi<=1 with chi=1 on r<=1/2 and chi=0 on r>=1, and put w=chi q. Its possible negative Laplacian is confined to the compact annulus 1/2<=r<=1. Let a=log(1/4), and define

P(t)=0 for t<=a,

P(t)=integral_a^t (t-s)exp[-1/(s-a)^2]ds for t>a.

Then p(r)=P(log r) is identically zero on r<=1/4, is smooth across that circle, and satisfies

Delta p(r)=r^{-2}exp[-1/(log r-a)^2]>0 for r>1/4.

Its Laplacian has a positive minimum on the possible negative annulus, so a sufficiently large finite C makes w+Cp globally smooth and subharmonic. The extension agrees with q for r<=1/4. Since chi>=0 and p>=0, it can also be chosen positive at every r>0. No decay or growth condition at infinity is required by the target.

### 5.2 Exact maximum, exact quotient, and the L1 defect

For k=1/r>=4, the interval [-k,k] contains pi/2, so some theta has sin(k cos theta)=1. For three identical copies of the extension, at those small radii

B(r)=(5/4)exp(-1/r^2),

q/B=4/5+(1/5)sin(k cos theta).

The sine term integrates to zero exactly by theta -> theta+pi. Hence the normalized median integral is exactly 8 pi/5, which is positive.

For each fixed angular Fourier mode, the sine term's coefficient tends to zero. Its odd sine-in-theta part vanishes by reflection; its cosine coefficients can be written as oscillatory integrals against the integrable Chebyshev weights on [-1,1]. The Riemann-Lebesgue argument is therefore applicable, including at the integrable square-root singularities at the endpoints. For each fixed N, Fejer smoothing of this sine term tends uniformly to zero.

The unnormalized L1 norm has a different limit:

integral_0^{2 pi}|sin(k cos theta)|dtheta
=2 integral_{-1}^1 |sin(kx)|/sqrt(1-x^2)dx ->4.

A fully controlled averaging proof uses

|sin y|=2/pi -(4/pi) sum_{m>=1} cos(2my)/(4m^2-1).

The coefficients are absolutely summable, and their tail telescopes:

sum_{m>J}1/(4m^2-1)=1/[2(2J+1)].

The series tail is therefore uniformly small; each of its finitely many retained nonconstant terms tends to zero after integration against the integrable weight. The remaining constant term gives 2(2/pi)pi=4. This proves, without angular quadrature,

||q/B-F_N*(q/B)||_1 ->4/5

for every fixed N. For the identical triple, the sum E_N tends to 12/5. Under averaged angular measure the single-component number would instead be 2/(5 pi), so preserving the report's unnormalized convention is material.

Every putative L1-convergent subsequence of the normalized profiles would have the constant 4/5 as its limit, by the fixed-mode limits. Its distance from that constant tends to 4/5 rather than zero. This proves nonprecompactness and exhibits failure of the additional hypothesis, not failure of the median inequality.

### 5.3 Zero-disk boundary germ and extension

In coordinates t=log r>0, take

q=exp(-1/t^2)(1+(1/4)sin(t^{-1}cos theta)),

and q=0 for r<=1. The same derivative argument on an annular coordinate neighborhood proves smooth flat extension across r=1. An independent phase/envelope calculation gives the three factors

t^6[(H_t)^2-H_{tt}]=4-6t^2,

t^6[phi_{tt}+phi_{theta theta}-2H_t phi_t]/4
=(-t+t^3/2-t^5/4)cos theta,

t^6[(phi_t)^2+(phi_theta)^2]/4
=(t^2 cos^2 theta+t^4 sin^2 theta)/4.

They reproduce the report's full cylindrical-Laplacian identity. On 0<t<=1/4 the quoted polynomial lower bound decreases and at its right endpoint equals exactly

10011/4096>0.

The conversion to the planar Laplacian multiplies by r^{-2}>0, preserving positivity. Choose a nonnegative cutoff equal to 1 through t=1/4 and zero after a later finite t, and a convex radial correction beginning at t=1/8. Its positive cylindrical second derivative dominates the cutoff error on the intervening compact annulus just as above. The result is a whole-plane C-infinity subharmonic function, equal to zero on r<=1 and unchanged on 0<t<=1/8; it may be kept positive at all r>1. There is no delta mass at the gluing boundary because all derivatives vanish there.

Now k=1/t tends to infinity. The same exact normalization, mean calculation, fixed-mode limits, and L1 error 4/5 apply. The example is affirmative for the median conjecture and is a counterexample only to automatic normalized angular compactness.

## 6. Exact power growth does not imply a homogeneous tangent

For the reported triple

u_1=r^2,

u_2=r^2[1/2+(1/10)cos(log r)cos theta],

u_3=0,

the conjugated cylindrical Laplacian on the bracket of u_2 is

partial_t^2+4 partial_t+4+partial_theta^2.

It yields

2+(1/10)(2 cos t-4 sin t)cos theta >=2-sqrt(20)/10>0.

Thus u_2 is subharmonic off the origin. It extends continuously with value zero and subharmonically through the origin: u_2=O(r^2) and its radial derivative is O(r), so the boundary terms in the distributional integration-by-parts formula tend to zero as a deleted circle shrinks. There is no negative point mass. The other components are plainly subharmonic.

The bounds 0.4r^2<=u_2<=0.6r^2 imply B(r)=r^2 exactly. For normalized dilates u_j(r_k z)/B(r_k), a phase limit log r_k modulo 2 pi -> alpha gives the displayed triple locally uniformly. Indeed the cosine dependence is uniformly Lipschitz in its phase, so the u_2 difference on |z|<=L is bounded by (L^2/10) times the phase discrepancy, including near z=0.

The nonhomogeneity claim can be tested without any topology argument. Since the first component is r^2, a homogeneous representation would have degree 2, and any common rotating-separable representation would have its radial factor proportional to r^2. But the angular variance of u_2/r^2 on a circle of logarithmic radius t is

(pi/100)cos^2(alpha+t).

This variance is invariant under angular rotation and changes between pi/100 and zero as t varies. It therefore cannot come from one fixed angular profile under any rotation, including a common spiral rotation. Every phase-limit triple fails the claimed homogeneous/rotating-separable form. Allowing an additional common rotation of the dilates cannot repair the varying angular amplitude.

This is a continuous admissible example, not a claim of smooth flatness at the origin. Its median is u_2 and has positive normalized integral pi. It validly refutes only the automatic inference from exact scalar growth to a homogeneous or common rotating-separable blow-up.

## 7. Verification disposition

A fresh independent checker reconstructs the Fejer constants, record and boundary moments, Cartesian origin invariants, cylindrical boundary invariants, positive endpoint margins, absolute-sine series constants, normalization factors, and conjugated log-periodic operator. It includes negative controls against signed smoothing, omission of conjugate-frequency factors, treating arbitrary scales as records, and confusing averaged with unnormalized L1. It does not import the author's verifier or use angular quadrature. The median stability implementation is also checked exhaustively on 15,625 finite test pairs; its general proof remains the elementary maximum-norm monotonicity argument.

The analytic assertions concerning positive measures, integration constants, compactness, smooth flat extensions, oscillatory limits, and nonhomogeneous tangents have been audited above rather than delegated to the symbolic checker.

No unrestricted theorem, novelty conclusion, uniform-negative admissible triple, or third-pass investigation is certified. The remaining uncontrolled regime is still the simultaneous escape of angular frequency and scale under only general subharmonicity.
