# Independent acceptance of the third-pass concentration results

## Decision and limits

Accepted at the stated partial-result scope. No mathematical correction to the audited report or its constants is required. The general-subharmonic heat estimate, optimized BV estimate, negative-part-only criteria, smooth critical-frequency construction, and localized positive-kernel curvature obstruction are valid. The unrestricted positive-denominator normalized-supremum conjecture remains unresolved.

This is an adversarial audit of the third shared substantive pass, not an additional research pass. No historical-priority claim is made. The source target remains A. Eremenko, *Conjectured inequality for subharmonic functions* (4 April 2015), https://www.math.purdue.edu/~eremenko/dvi/subh1.pdf. The source's harmonic and homogeneous affirmative cases remain credited prior results. No copied source text is included. All quotients are evaluated only at actual positive denominators; this convention is not identified with assigning zero to 0/0.

Write U_j(t,theta)=u_j(exp(t+i theta)), b(t)=B(exp t), A(t)=integral_{-infinity}^t (t-s)b(s) ds, and a(t)=A(t)/b(t). All angular integrals, L1 norms, and variations below use ordinary, unnormalized dtheta. Previously audited denominator facts supply b>=0, monotonicity, continuity, b(t)->0 at negative infinity, and nonnegative, finite circle means. In particular, for each component,

integral U_j^- <= integral U_j^+ <= 2 pi b,

||U_j||_1 <= 4 pi b,

and the mass of b-U_j is at most 2 pi b.

## 1. General representatives, circle singularities, and positive slices

The extension from continuous functions to arbitrary subharmonic functions is justified. It concerns actual upper-semicontinuous subharmonic representatives, not arbitrary pointwise alterations of an L1 equivalence class.

On a compact positive-radius annulus, choose a slightly larger disk and a compactly supported finite portion of the local Riesz measure covering a neighborhood of the annulus. The function is a harmonic function plus its logarithmic potential on that neighborhood. The relevant smoothed potential kernel is

L_K(r,theta,zeta)=integral K(theta-alpha)log|r exp(i alpha)-zeta| d alpha.

For a smooth circular K this kernel is bounded and jointly continuous when r ranges over a fixed compact interval bounded away from zero and zeta ranges over the compact support. Here is the singularity estimate explicitly. For sufficiently small eta, if the circle meets the eta-ball about zeta, then |zeta| is bounded below and the cosine rule bounds the angular length of the intersection by C eta, uniformly in r and zeta. Otherwise the intersection is empty. The layer-cake estimate then gives

integral_{|r exp(i alpha)-zeta|<eta} log(eta/|r exp(i alpha)-zeta|) d alpha <= C eta.

Equivalently, the untruncated absolute logarithmic tail is O(eta(1+|log eta|)). Multiplying by a bounded K preserves this estimate. Truncating the logarithm below at log eta gives continuous kernels converging uniformly to L_K. Their uniformly bounded limit can be integrated against the finite Riesz measure. Fubini is justified by the same uniform logarithmic integrability. Thus K*U is finite and continuous at every positive radius. Taking K, K', and K'' also justifies the angular derivatives used in the report.

This does not imply radial differentiability of the smoothed function. A useful nonsmooth control is u(z)=log|z-1|, which has u(0)=0 and an actual circle singularity at z=1. Its constant-kernel angular convolution is log(max(r,1))=max(t,0), continuous with a positive derivative jump. The proof requires continuity and distributional convexity, precisely the properties that survive this control.

Let mu_j be the positive Radon measure U_{j,tt}+U_{j,theta theta} on the cylinder. For fixed theta and the positive heat kernel k_tau, define

nu_{j,theta}(S)=integral_{S x circle} k_tau(theta-alpha) dmu_j(s,alpha).

This is a positive, locally finite measure on the t-axis. Testing the two-dimensional identity against eta(t)k_tau(theta-alpha) gives

integral V_j eta'' + integral partial_theta^2 V_j eta = integral eta dnu_{j,theta},

where V_j=k_tau*U_j. This explicitly constructs the slice; no restriction of an arbitrary distribution to a line occurs. Positivity of the smoothing kernel is essential.

Fix a finite T with A(T)<infinity. The weighted tail also implies integrability of b sufficiently far to the left, so A is finite locally on either side of T. Define

R_j(t,theta)=integral_{-infinity}^t(t-s)partial_theta^2 V_j(s,theta) ds.

Kernel boundedness, ||U_j||_1<=4 pi b, and finiteness of A justify the integral, continuity, and R_{j,tt}=partial_theta^2 V_j. Moreover A(t)->0 at negative infinity: for t<=T,

0<=A(t)<=integral_{-infinity}^t(T-s)b(s) ds ->0.

Both V_j and R_j therefore have zero left limits. Hence W_j=V_j+R_j is a continuous convex function with finite zero limit at the left end. Convex secant slopes imply W_j is nondecreasing, so W_j>=0 and V_j>=-R_j at every t and theta. The zero left limit is material; convexity alone would not exclude a negative constant.

## 2. Heat curvature norm and the median sum-deficit factors

For g_tau(x)=(4 pi tau)^(-1/2) exp(-x^2/(4 tau)), g_tau'' changes sign exactly at x=+-sqrt(2 tau). Integrating its absolute value by the primitive g_tau' gives

||g_tau''||_1 = -4 g_tau'(sqrt(2 tau)) = sqrt(2/(pi e))/tau.

Periodization and the triangle inequality give ||k_tau''||_1<=sqrt(2/(pi e))/tau. Equality for the periodized kernel is not claimed or needed.

Because k_tau'' has zero mean, partial_theta^2 V_j=-k_tau''*(b-U_j). Young's inequality and the nonnegative deficit mass give

||partial_theta^2 V_j(s,.)||_1 <= 2 pi b(s)||k_tau''||_1.

Thus ||R_j(t,.)||_1<=2 pi A(t)||k_tau''||_1. Its angular integral is zero by Fubini and the zero integral of the kernel derivative. From V_j>=-R_j,

||V_j^-||_1 <= ||R_j^+||_1 = (1/2)||R_j||_1 <= pi A(t)||k_tau''||_1.

The second half-factor comes from equality of the U_j and V_j means. Pointwise,

U_j^- <= V_j^- + (V_j-U_j)^+.

Since integral(V_j-U_j)=0, its positive integral equals one half of its L1 norm. Consequently

||U_j^-||_1 <= ||V_j^-||_1 + (1/2)||U_j-V_j||_1.

Neither this factor nor its mean-zero hypothesis is disposable. On a two-point space U=(-1,1), V=(0,0) attains equality; on a one-point space U=-1,V=0 the half-error bound fails.

Finally, med(x_1,x_2,x_3)>=-(1/2)sum_j x_j^-: a negative median has at least two negative components of at least its magnitude. The coefficient one half is sharp for (-1,-1,0). The median is integrable because all components are integrable on the circle. Summing and dividing by b>0 gives exactly

I(exp t)/b(t) >= -(3 pi/2)||k_tau''||_1 a(t) - E_tau(t)/4

>= -3 sqrt(pi/(2e)) a(t)/tau - E_tau(t)/4.

The three factors are accounted for separately: three components, half the zero-mean R mass, and the median half-factor. The smoothing-error quarter is the mean-deficit half-factor times the median half-factor. There is no missing normalized-circle factor.

## 3. BV optimization, scales, and ordered limits

For a periodic BV function, ||f(. -x)-f||_1<=|x|TV(f) for every real x, with the circular total variation taken over one period. The real-line Gaussian representation of circular smoothing therefore gives

||f-P_tau f||_1 <= TV(f) integral |x|g_tau(x)dx = 2 sqrt(tau/pi)TV(f).

With x=sqrt(tau), the loss is

C_0 a/x^2 + Dx/(2 sqrt(pi)),  C_0=3 sqrt(pi/(2e)).

It has its unique positive minimum at x^3=4 sqrt(pi) C_0 a/D, and its minimum is C_* (aD^2)^(1/3), with

C_*^3=81/(16 sqrt(2 pi e)),  C_*<1.0700.

No upper restriction on tau was used, so this optimizer is permissible. At b>0, continuity gives A>0. If D=0, each circle profile is an almost-everywhere constant with nonnegative mean; the median integral is nonnegative directly.

At a slope-M record b(s)<=b(t)exp(M(s-t)) for s<=t, the exact moment integral gives a(t)<=1/M^2. Hence

I/B >= -C_* (D/M)^(2/3).

The report correctly requires selected records t_k->-infinity, M_k->infinity, with D(t_k)=o(M_k). It does not call arbitrary radii records or claim an all-small-radii lower bound from these selections. A uniform negative upper bound I/B<=-epsilon forces D(t)>=M(epsilon/C_*)^(3/2) at every such finite-variation record. Merely having I(r)<0 at every radius would not supply this uniform epsilon; the report does not make that mistake.

At a last joint zero disk t_0, all components vanish for t<=t_0 and monotonicity yields a(t)<=(t-t_0)^2/2. This supplies precisely the factor 2^(-1/3) and the sufficient condition (t-t_0)D(t)->0 in the boundary bound. The finer condition sqrt(a(t))D(t)->0 remains valid and can be weaker.

The earlier positive high-frequency example indeed lies outside full-profile compactness while satisfying this BV criterion. Its normalized profile is 4/5+(1/5)sin(k cos theta), so one profile has variation at most 4k/5, and the triple has D<=12k/5. At small records r=sqrt(2/M), k=sqrt(M/2), giving D/M->0. The record assertion applies once r is in the unchanged germ, for example for M>=32. The noncompactness is the previously audited one. The example's positivity makes it affirmative independently; its purpose here is to show that the new sufficient hypothesis admits genuinely noncompact profiles.

## 4. Threshold transfer controls only negative parts

For f<=1, put p=f^+, g=f^-, and h=min(g/delta,1). Then 0<=p<=1, ph=0, and 0<=h<=1. Define H as the Gaussian average of the L1 translation defect of g. Positive averaging and the Lipschitz constant of h as a function of g give

||Pg-g||_1<=H,  ||Ph-h||_1<=H/delta.

Since g-hg<=delta pointwise, integral hg>=||g||_1-2 pi delta. Symmetry of P is what makes the key exchange valid:

integral hPf = integral pPh - integral gPh

= integral p(Ph-h) - integral hPg

<= H/delta - ||g||_1 + 2 pi delta + H.

The left side is at least -||(Pf)^-||_1. Thus

||g||_1 <= ||(Pf)^-||_1 + H + 2 pi delta + H/delta.

For H>0 use delta=sqrt(H/(2 pi)); for H=0 let delta decrease to zero. This yields exactly H+2 sqrt(2 pi H) as the loss. No bound on g in L-infinity and no regularity of p was used. The upper bound p<=1 is essential to the displayed proof and is supplied by the actual B normalization. The quantity H is a Gaussian average of translation defects; the proof does not silently replace it by the generally smaller number ||Pg-g||_1 when controlling h.

Combining this inequality with the component bound in Section 2 and the median half-factor gives the report's equation (13) with unchanged heat coefficient and one half of each negative-part loss.

For a relatively L1-compact family of negative parts, the translation modulus tends to zero uniformly. Also ||g||_1<=2 pi, so every translation defect is at most 4 pi. Given a small angular neighborhood, split the Gaussian average into that neighborhood and its complement. Uniform small-translation continuity controls the former; the Gaussian tail controls the latter. Hence H_tau tends uniformly to zero as tau decreases to zero.

At an all-flat origin, fix tau first and take record slopes tending to infinity, so a/tau tends to zero. Then let tau decrease to zero. At a zero-disk boundary, fix tau first and take t down to t_0; again a/tau vanishes. The final tau limit proves not only the respective median limsup or boundary liminf but also disappearance of each normalized negative-part integral on the claimed scales. These are ordered limits, not an assertion that arbitrary simultaneous choices work.

There is a constructive choice for the report's more general negative-BV criterion. Put D=D_- and x=sqrt(tau) with

x^2=sqrt(a)/(1+D).

If a->0 and sqrt(a)D->0, then

a/x^2=sqrt(a)(1+D)->0,

(xD)^2=sqrt(a)D [D/(1+D)]->0,

and x->0. Since sum H_j<=2xD/sqrt(pi), the sum of H_j and their square roots tends to zero. This also handles D=0 without a division by zero. The informal instruction to put x between sqrt(a) and 1/D thus has a rigorous realization in every stated case.

## 5. Critical-frequency smooth construction

Let eta, A_1, A_2, L, n_0, n_k, t_k and chi_k be as in the audited report. All cutoff derivatives exist and the extension by zero at each support endpoint is smooth. The scale choices imply L/n_k<=1/256. For adjacent supports the total half-width is at most 3/512, whereas log 2>=1/2, so the supports are disjoint with room to spare.

For Q=exp(-t), f=exp(-Q), and q=f(1+2chi cos(n theta)), conjugation of the cylindrical Laplacian gives

(q_tt+q_theta theta)/f

= Q^2-Q + 2[chi''+2Qchi'+(Q^2-Q-n^2)chi]cos(n theta).

This is independently reconstructed in the checker. On a support, h=t-t_k satisfies |h|<=L/n and Q/n=exp(-h). Since exp(-2h)>=1-2h and Q<=2n,

(Q^2-Q)/n^2 >= 1-(2L+2)/n >=127/128.

The bound |exp(-2h)-1|<=4|h| holds throughout |h|<=1/256. Also |chi'|<=A_1 n/L and |chi''|<=A_2 n^2/L^2. Consequently the absolute oscillatory coefficient divided by n^2 is at most

(8L+4)/n + 8A_1/L + 2A_2/L^2

<=1/32+1/4+1/512.

The difference is 363/512, exactly as stated. The derivative and scale assumptions give each of these bounds separately; this is not merely a check of the final subtraction. Outside the supports q=f and the cylindrical Laplacian is f(Q^2-Q)>0 for r<=1/2. There is no overlooked transition annulus with an uncontrolled sign. The planar Laplacian is r^(-2) times the cylindrical one.

At a support center chi=1 and its derivatives vanish, so the minimum coefficient is n^2-3n. This gives a simple control of why critical matching matters: replacing the angular frequency n by 2n, keeping amplitude 2 and the same envelope, would instead give minimum -5n^2-3n and fail subharmonicity. The accepted construction uses the matching frequency n.

### All-order flatness and global extension

On support k, n_k is uniformly comparable to 1/r. A fixed number of radial or angular derivatives introduces only fixed powers of n_k and 1/r, with constants depending on the fixed-order derivatives of eta and L, not on k. Conversion from polar to Cartesian derivatives introduces additional powers of 1/r but no dependence of a different kind. Thus for every Cartesian multi-index alpha there are constants C_alpha,N_alpha with

|partial^alpha q| <= C_alpha exp(-1/r) r^(-N_alpha)

near zero. Outside the supports the same estimate follows from the envelope alone. Smooth compatibility at support boundaries and the exponential domination of every inverse power show that setting q(0)=0 gives a C-infinity function with every derivative zero at the origin. There is no accumulation defect or atom at the origin: its smooth Laplacian equals zero there and is nonnegative elsewhere near it.

For completeness, the germ formula can be continued to all r>0 before applying the outer cutoff: every oscillatory support is already far inside r=1/4, so the continued formula outside them is simply exp(-1/r). Choose a smooth radial cutoff equal to one through r=1/2 and zero for r>=1, and call the product w. Its possible negative Laplacian is confined to the compact annulus [1/2,1]. It is not necessary to multiply an undefined germ outside its domain.

With a_0=log(1/4), define P(t)=0 for t<=a_0 and

P(t)=integral_{a_0}^t(t-s)exp[-1/(s-a_0)^2] ds for t>a_0.

The zero extension is smooth at a_0. For p(r)=P(log r),

Delta p(r)=r^(-2)exp[-1/(log r-a_0)^2]>0 for r>1/4,

and p vanishes for r<=1/4. This Laplacian has a strictly positive minimum on [1/2,1], while the negative part of Delta w has a finite maximum there. A finite C>=0 therefore makes w+Cp smooth and subharmonic on the whole plane, agreeing with the germ on r<=1/4. Negative values of w near zero are irrelevant because its Laplacian is already nonnegative there. No condition at infinity in the target obstructs the correction.

## 6. Honest normalization, record scales, and exact noncompactness

Take the three components identical to that extension. At r_k=1/n_k, the extension leaves the germ unchanged, chi_k=1, and cos(n_k theta) attains one. Therefore the actual maximum and normalized profile are exactly

B(r_k)=3exp(-n_k),

q(r_k,theta)/B(r_k)=(1+2cos(n_k theta))/3.

For every s<=t_k, the germ is unchanged and its actual maximum is at most 3exp(-exp(-s)). The logarithm of this upper envelope is concave. Writing h=s-t_k, the logarithmic ratio to the claimed record tangent is

n_k[1-exp(-h)-h] <=0,

by exp(-h)>=1-h. Equality of the true maximum and the envelope at the center is indispensable and has just been checked. It follows that

b(s)<=b(t_k)exp(n_k(s-t_k)),  s<=t_k.

Thus these are genuine records of slope M=n_k, with a(t_k)<=n_k^(-2), not merely scales having a convenient radial derivative.

The base negative part G(theta)=(-1-2cos theta)^+/3 is supported on [2pi/3,4pi/3]. Its exact integral is

m_1=2sqrt(3)/3-2pi/9>0.

The normalized negative parts are G(n_k theta). Since n_k are integers, multiplication of theta by n_k preserves ordinary circle integrals. Their L1 masses are all m_1. Their only nonzero Fourier frequencies are multiples of n_k, so every fixed nonzero coefficient vanishes identically once n_k exceeds its magnitude. Any putative L1 subsequential limit therefore has only its zeroth coefficient and must be the constant m_1/(2pi), by uniqueness of Fourier coefficients in L1.

The L1 distance from that constant is independent of k and is strictly positive. An explicit lower bound avoids any reliance on numerical oscillatory integration. G vanishes on a set of length 4pi/3. Since G minus its mean has integral zero, its full L1 norm is at least twice its negative deficit on that zero set, namely

||G-m_1/(2pi)||_1 >= (4/3)m_1>0.

This proves nonprecompactness along the actual record scales themselves.

The exact total variations follow from the excursions of the base profiles: (1+2cos theta)/3 goes from 1 to -1/3 and back, giving 8/3 per cycle; its negative part goes from zero to 1/3 and back, giving 2/3. At frequency n_k these become (8/3)n_k and (2/3)n_k. The three identical components consequently give D=8n_k and D_-=2n_k. Neither divided by the record slope tends to zero.

Every angular oscillation has zero mean at every radius, including transitions. Thus the small-radius mean of q is exactly exp(-1/r), and the median of three identical copies is q itself. The normalized median integral at the centers is precisely 2pi/3>0. The construction is affirmative for the target and refutes only automatic negative-part compactness, including at these honest records. It is not a uniformly negative triple or a counterexample to either sufficient criterion.

## 7. The localized positive-kernel obstruction

For a nonnegative C^2 probability kernel K on the circle, with sigma^2=integral_{-pi}^pi theta^2 K(theta)dtheta and 0<sigma<=1/2, put n=floor(1/sigma). Then n>=1/(2sigma) and n sigma<=1. The global elementary inequality cos x>=1-x^2/2 gives

integral cos(n theta)K(theta)dtheta >=1-n^2 sigma^2/2>=1/2.

Twice integrating by parts on the circle is legitimate because K and its first derivative match at the endpoints. Hence

||K''||_1 >= |integral cos(n theta)K''(theta)dtheta|

= n^2 |integral cos(n theta)K(theta)dtheta| >=1/(8sigma^2).

The report properly limits this conclusion to the curvature-norm estimate for localized positive smoothing. It does not claim that every possible smoothing proof or every nonlinear argument must fail in the residual regime.

## 8. Verification disposition

The fresh verifier independently reconstructs the heat curvature norm by boundary derivatives, BV minimization, record and boundary moments, median and equal-mean half-factors, threshold optimization, constructive negative-BV scale choice, conjugated cylindrical operator, individual transition bounds, global radial correction, exact critical-frequency integrals and variations, noncompactness gap, and positive-kernel lower-bound constant. It also tests 9,261 integer median triples and 1,875 rational threshold cases. Meaningful controls reject an incorrect median one-third factor, dropping the mean-zero condition, reversing negative-part contraction without a defect, changing the critical angular frequency to 2n, and inferring radial C1 regularity from angular smoothing.

These checks do not import the author's verifier, and none uses angular quadrature. All analytic issues, including representatives, positive measures, affine integration constants, uniform translation continuity, ordered limits, smooth flatness, whole-plane extension, Fourier uniqueness, and record normalization, are justified in this acceptance rather than inferred from symbolic checks.

The author calculation is separately reconstructed, and independent ordinary, -O and -OO outputs are checked for equality. The [proof text](../proofs/concentration.md) contains the reviewed mathematical statement. No unrestricted theorem, novelty conclusion, publication, or fourth-pass result is certified.
