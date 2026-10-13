# Independent acceptance audit: fifth-pass one-fast-phase theorem

## Decision

**ACCEPT the mathematical theorem, the converse realization, and the explicit example, at the exact stated restricted scope. No mathematical correction patch is needed.**

The [full one-fast-phase proof](../proofs/one_fast_phase.md) is included, with its normalized-variation wording made explicit. This audit verifies the fifth and final substantive pass and adds no sixth research pass.

The unrestricted subharmonic median conjecture remains unresolved. Neither this audit nor the accepted report supplies a general layer-selection theorem or excludes every smooth all-flat, all-positive-denominator-radius uniformly negative triple.

## Verification results

- The submitted finite calculations were independently replayed with Python 3.12.14 in normal, `-O`, and `-OO` modes. Each completed successfully with 35 controls and 46,305 weighted-median cases.
- The three regenerated outputs match the [author certificate](../certificates/fast_author.json) byte for byte.
- The [independent audit certificate](../certificates/fast_audit.json) independently reconstructs the algebra without importing or executing the submitted verifier: 60 exact controls and 16,875 additional weighted-median cases on a different rational grid. It passes in normal, `-O`, and `-OO` modes with identical output bytes.
- The independent reconstruction uses an arbitrary local two-jet, an adjoint Green kernel calculation, positive-inverse integration by parts, exact rational margin checks, and explicit mutation controls. In particular, its signed drift variable is unrestricted, so acceptance does not depend on the submitted verifier's use of positive symbols in some algebraic tests.
- Executable controls do not prove the general averaging, maximum-sampling, smooth-extension, or noncompactness assertions. Those obligations are checked analytically below.

## 1. Full cylindrical chain rule

Write `Q=r^(-p)`, `t=log r`, `f=exp(-Q)`, and `x=Q psi(theta)`, with `p>0`. Thus `Q_t=-pQ` and `f_t=pQf`. Holding the slow angle fixed during radial differentiation gives

    V_t = pQf(H-psi H_x),
    V_tt/(p^2 f)
      = Q^2(H-2 psi H_x+psi^2 H_xx)-Q(H-psi H_x).

Holding Q fixed during angular differentiation gives

    V_theta theta/f
      = H_theta theta+2Q psi' H_theta x
        +Q psi'' H_x+Q^2(psi')^2 H_xx.

Adding these expressions produces exactly the submitted `P_theta`, `R_1`, and `R_2`. In particular, the drift is `-2 psi H_x`; the mixed slow/fast derivative is `2 psi' H_theta x/p^2`; the first radial derivative contributes both `-H` and `psi H_x`; and the second angular phase derivative contributes `psi'' H_x/p^2`. No additional `H_theta` term exists.

The independent local-jet check differentiates an arbitrary quadratic Taylor polynomial of H centered at an independently fixed point, composed with an arbitrary quadratic Taylor polynomial of psi. This reconstructs every derivative that can occur in this second-order calculation. It also rejects omission of six distinct nonzero terms at rational nondegenerate test data, including negative psi.

The planar Laplacian is `r^(-2)(partial_t^2+partial_theta^2)`, so its sign agrees with the cylindrical expression for every positive radius.

## 2. Subharmonicity forces the entire frozen cone

Fix an angle with `psi(theta) != 0` and an arbitrary target phase modulo `2 pi`. If psi is positive, let the phase integer tend to positive infinity; if psi is negative, let that integer tend to negative infinity. In either case, a sequence of **positive** Q tending to infinity attains the target phase exactly.

At those radii, subharmonicity and the chain rule give

    0 <= P_theta H_j(theta,x) + R_1/Q + R_2/Q^2.

The remainders are bounded because H and psi are smooth on compact periodic domains. Passing to the limit yields the frozen inequality for every phase x. The zero set of psi cannot contain an interval: such an interval would belong to the critical set of psi, contradicting its measure-zero hypothesis. Consequently angles with nonzero psi are dense. Continuity of the coefficients and profiles extends the inequality to all angles, including simultaneous zeros of psi and psi'.

The allowed error condition is sufficient exactly as written. It bounds the **sum** `E_tt+E_theta theta`; separate bounds on those two terms are unnecessary. Division by `p^2 Q^2 f` makes its contribution tend to zero uniformly. The first error condition separately supplies stability of the later maximum and median limits. These conditions alone need not imply arbitrary derivative control on an otherwise unspecified error, and the report does not use them to establish such a claim.

Integrating the frozen inequality over the periodic fast variable annihilates both derivative terms, giving a nonnegative fast-variable mean for each H_j at each angle. No radial restriction of a distribution is involved; the functions under discussion are smooth at positive radii.

## 3. Positivity of the frozen median

### Nonstationary angle

When `d=psi'(theta) != 0`, set `b=psi(theta)` and `a=b^2+d^2/p^2>0`. Then

    beta=b/a,    gamma=|d|/(pa)>0,
    beta^2+gamma^2=1/a,    T=pi/gamma.

Conjugation by `exp(-beta x)` turns P into `a(partial_x^2+gamma^2)`. Equivalently, on `0<s<T`, the kernel

    k(s)=exp(beta(T-s)) sin(gamma s)/(a gamma)

satisfies the adjoint equation `a k''+2b k'+k=0`, vanishes at both endpoints, and has

    a k'(0)=exp(beta T),    a k'(T)=-1.

Two integrations by parts therefore give exactly

    h(x+T)+exp(beta T)h(x) = integral_0^T k(s)(Ph)(x+s) ds.

The kernel is nonnegative. This argument works for either sign of beta, all positive T, and any relationship between T and the period. Periodic extension supplies all translated values.

For the three components, this proves coordinatewise `h_j(x+T)>=-K h_j(x)` with `K=exp(beta T)>0`. The median is monotone in every coordinate, and the median of the coordinatewise negative of a triple is the negative of its median. Hence

    med h(x+T) >= -K med h(x).

Integrating over one full period and using translation invariance yields `(1+K) integral med h>=0`. The coefficient is indeed `1+K`, not 2. The submitted proof's elementary median step is valid; the finite grids are supplementary controls rather than its logical foundation.

### Stationary angle

When d=0, P is `(1-b partial_x)^2`. For a smooth periodic g define

    R_b g(x)=integral_0^infinity exp(-s)g(x+bs) ds.

Integration by parts shows `(1-b partial_x)R_b g=g`. Composing twice gives the nonnegative kernel `s exp(-s)` in the report. The formula remains valid when b is negative; when b=0 it is simply multiplication by a kernel of total mass 1. For b nonzero the only periodic solution of the homogeneous repeated-root equation is zero, since its solutions have the form `(c_1+c_2 x)exp(x/b)`. Thus the integral really recovers h, rather than one of several periodic solutions.

If Ph is nonnegative, h is nonnegative at such an angle. This handles the degenerate case `a=b=d=0` as well, where P is the identity. There is no missing sign, vanishing coefficient, or division-by-zero case. Therefore every angle has a nonnegative mean frozen median, and `J_*>=0` follows.

## 4. Averaging, the actual denominator, and perturbations

### Averaging

A continuous two-variable periodic G admits uniform approximation by finite Fourier sums in its fast variable with continuous coefficients in its slow variable. This follows, for example, by the uniformly convergent Fejer approximation in the fast variable on the compact two-torus.

For a nonzero Fourier mode, cover the compact measure-zero critical set of psi by finitely many open angular intervals with arbitrarily small total length. Split at the angular-period endpoint if necessary. On the finite union of complementary closed intervals, psi' is bounded away from zero and has a constant sign on each nondegenerate interval. The change of variables `y=psi(theta)` produces a compactly supported L1 coefficient, including the absolute Jacobian. Its Fourier transform at the real frequency `mQ` tends to zero by the Riemann-Lebesgue lemma. This is a limit for all real Q tending to infinity, not merely an integer subsequence.

The omitted intervals contribute at most their total length times the uniform coefficient bound. Taking the frequency limit first, then shrinking their total length, then removing the uniform approximation error proves the asserted averaging identity. It applies to the continuous median, to products with continuous angular tests, and to the continuous absolute-value expression used in the noncompactness argument. The proof does not require finitely many critical points or a uniform global lower bound on `|psi'|`.

The measure-zero critical-set assumption is doing genuine work. The audit does not replace it by mere nonconstancy or assume averaging for a singular phase pushforward.

### Actual maximum

The regular angles are dense because a measure-zero set has no interior. Therefore a maximum of any H_j on the compact two-torus can be approximated arbitrarily closely by one at a regular angle, retaining the chosen fast phase. At such an angle, psi has a local inverse on an open image interval.

For every sufficiently large real Q, rounding `(Q psi(theta_0)-x_0)/(2 pi)` to an integer supplies a target `(x_0+2 pi k_Q)/Q` within `pi/Q` of `psi(theta_0)`. It is eventually inside that inverse's image. The resulting angles converge to theta_0 and attain the fast phase exactly. This gives the required liminf for **all** large Q; the limsup is the immediate pointwise bound by B_*.

If `B_*<=0`, all profiles would be nonpositive. Their already proved nonnegative fast-variable means would then force every profile to vanish identically, contradicting the hypothesis. Hence `B_*>0`, and the actual circle maximum is positive at all sufficiently small radii.

The maximum and median are each 1-Lipschitz in the componentwise sup norm. Thus errors with `max |E_j|/f ->0` change the normalized maximum by o(1) and the normalized angular median integral by at most `2 pi o(1)`. This completes the quotient argument with the actual denominator throughout.

## 5. Converse realization, every radius, and noninteger p

Direct radial differentiation gives

    (partial_t^2+partial_theta^2)(f/Q)
       =p^2 f(Q+1+1/Q).

Taking C at least both global absolute remainder bounds gives the exact lower-bound decomposition

    Q^2 PH_j + Q(R_1+C) + (R_2+C) + C/Q >= 0.

Each term is nonnegative for every Q>0. This is not a large-Q estimate and does not leave an uncontrolled intermediate- or large-radius region. It proves the all-radius realization directly, without a gluing argument.

Every fixed Cartesian derivative of `f H(theta,Q psi(theta))` at positive radius is a finite sum bounded in magnitude by `exp(-r^(-p))` times a fixed real power of r. The same is true of the correction `C r^p exp(-r^(-p))`. For every p>0, the exponential tends to zero faster than every reciprocal power of r. Consequently all derivatives tend to zero at the origin, and the standard removable smooth-flat extension has every derivative zero there. Integer p is unnecessary: real powers of r are smooth away from the origin, and the flat envelope removes their origin singularities. The Laplacian is zero at the origin and nonnegative everywhere else.

No regularity condition at a point called infinity is required for a whole-plane smooth function; all finite positive radii are already covered. The correction is lower order in normalized value, and its normalized cylindrical Laplacian divided by Q^2 is `p^2(1/Q+1/Q^2+1/Q^3)`, tending to zero. It therefore preserves the established asymptotic limit.

The report correctly distinguishes necessity for an uncorrected or admissibly perturbed realization from sufficiency after a lower-order radial correction. It does not assert that frozen positivity alone makes the uncorrected V subharmonic.

## 6. Exact example and rational positivity margin

For `p=1`, `psi=sin(theta)`, and `A=3 cos(theta)^16`, a is identically 1. For each shifted phase the exact frozen forcing is

    1+6 cos(theta)^16 sin(theta) sin(x+2 pi j/3).

The nonnegative envelope `6y(1-y^2)^8`, on `0<=y<=1`, has derivative `6(1-y^2)^7(1-17y^2)`. Its sole interior maximum occurs at `y^2=1/17`; the endpoints give zero. The square of that maximum is exactly

    664082786653543858176 / 827240261886336764177 < 81/100.

Thus every frozen forcing is strictly greater than 1/10. This conclusion is exact and does not rely on a decimal estimate or a numerical search.

The exact amplitude derivatives are

    A'=-48 cos(theta)^15 sin(theta),
    A''=720 cos(theta)^14 sin(theta)^2-48 cos(theta)^16.

The triangle bounds 48 and 768 are valid, even though they are not optimal. Since `psi+psi''=0`, the first remainder is `-H+2 cos(theta)H_theta x`; hence its absolute value is at most `4+96=100`. The second remainder is bounded by 768. Taking C=768 yields the strictly positive lower bound

    (1/10)Q^2+668Q+768/Q > 0

for the normalized cylindrical Laplacian at every Q>0. Thus each example component is smooth and whole-plane subharmonic, with strictly positive Laplacian off the origin.

All profiles are bounded above by 4, and component j=0 at theta=0 has phase zero and amplitude 3 for every Q. Therefore the exact actual denominator is `f(4+768/Q)`, with no asymptotic maximization substitution. The median of the three shifted cosines changes sign under `x -> x+pi`; its mean is zero. Since A is nonnegative, its addition and scaling inside the median give mean profile 1 at every angle. Therefore `J_*=2 pi`, `B_*=4`, and the quotient tends to `pi/2`.

At theta=0 the two components with j=1,2 have profile `-1/2+768/Q`, so the actual median there is negative when `r<1/1536`. The example has negative component regions for every component at all sufficiently small radii; the j=0 phase can be attained at nearby regular angles. These facts do not contradict the positive limiting integral.

## 7. Negative-part noncompactness and critical variation

Let `g_j(theta,x)=max(-H_j(theta,x),0)` and `m_j(theta)=average_x g_j(theta,x)`. Averaging against every continuous angular test shows that `g_j(theta,Q sin(theta))` converges weakly, in this test sense, to m_j. The actual normalized negative part is

    max(-H_j(theta,Q sin(theta))-768/Q,0)/(4+768/Q).

Its difference from `g_j(theta,Q sin(theta))/4` tends uniformly to zero: taking a negative part is 1-Lipschitz, and the profiles are uniformly bounded. Therefore any L1 strong subsequential limit as Q tends to infinity must equal `m_j/4`, since continuous tests determine an L1 function up to null sets.

On an open angular interval around zero, A>1. At every such angle g_j is a nonconstant continuous function of phase, because H_j takes both positive and negative values. Hence its average absolute deviation from its phase mean is strictly positive there. Averaging the continuous function `|g_j-m_j|` proves that the L1 distance from the only possible strong limit tends to a strictly positive number, divided by 4. This rules out every L1-convergent subsequence along radii tending to zero, and hence proves failure of L1 precompactness. It does not claim that a sequence of radii converging to a nonzero radius lacks a convergent subsequence.

The variation statement concerns the actual-denominator-normalized angular profiles and their normalized negative parts. The included proof now states that normalization explicitly. For an explicit set of constants, on `|theta|<=1/8`, the elementary cosine estimate and Bernoulli's inequality give

    cos(theta)>=127/128,    A(theta)>=21/8.

Choose a compact fast-phase interval inside `3 pi/4 < x+2 pi j/3 < 5 pi/6`. There `cos(x+2 pi j/3)<-2/3` and `sin(x+2 pi j/3)>1/2`. The uncorrected profile is at most -3/4. For Q>2048, the correction is less than 3/8, so this is strictly within the negative branch. On that branch the angular derivative magnitude is bounded below by

    Q A |cos(theta) sin(x+2 pi j/3)|-|A'|.

A nonzero smooth nonnegative weight bounded above by 1, supported inside these angular and phase intervals, has a strictly positive averaged leading coefficient. The averaging theorem therefore gives a positive constant times Q lower bound for variation, up to an O(1) loss. The global chain-rule derivative gives an O(Q) upper bound. Dividing by the actual normalized denominator `4+768/Q`, bounded away from zero and infinity for large Q, preserves both bounds.

The envelope's normalized radial curvature is `Q^2-Q`, whose square root is asymptotic to Q. Thus the normalized angular variation has the same asymptotic scale; it is not subcritical. The normalized smooth profiles also have radial first and second derivative scales Q and Q^2, as direct differentiation of their fast phase shows. This verifies the report's intended contrast with compact or slowly varying normalized profiles without invoking any missing compactness theorem.

## 8. Scope and disposition

All accepted conclusions require a common single phase `Q psi(theta)`, smooth fixed periodic profiles, and the stated measure-zero critical-set assumption. The admissible perturbation statement requires the explicitly written value and cylindrical-Laplacian smallness conditions. It does not cover arbitrary multiple-phase superpositions, nonseparable radial envelopes, or general critical layers.

The exact example establishes an affirmative critical-frequency, noncompact-negative-part regime, not a counterexample. The report's broader conjecture status is unchanged. No historical novelty or external-source authentication claim is made by this audit.

**Final disposition:** mathematical acceptance. The reader makes the normalized-variation convention explicit without changing the theorem, example, or analytic proof. The [reproduction guide](../REPRODUCTION.md) distinguishes exact original output from its metadata-only public projection.
