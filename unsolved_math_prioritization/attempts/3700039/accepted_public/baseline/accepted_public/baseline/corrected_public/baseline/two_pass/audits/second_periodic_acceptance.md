# Independent audit: two-variable logarithmic-phase results

## Decision

**Accepted at the stated partial-result scope. No theorem-level correction is required.** The common sign-reversing symmetry theorem, fixed-forcing high-frequency theorem, exact mixed-sign phase example, and positive finite-point obstruction are valid under their stated hypotheses. The unrestricted some-phase question and the original normalized-supremum conjecture remain unresolved.

This is an adversarial audit of the second shared substantive pass, not an additional proof-search pass. The source is A. Eremenko, *Conjectured inequality for subharmonic functions*, 4 April 2015, https://www.math.purdue.edu/~eremenko/dvi/subh1.pdf. The harmonic and homogeneous cases remain credited prior results. No historical novelty claim is made for the audited extensions.

The normalized assertion is interpreted only at radii with positive normalizing maximum. The exact example below has such a maximum at every radius, so its conclusions do not depend on assigning a value to 0/0.

## 1. Operator, realizability, and scalar positivity

Write

    L_omega = omega^2 partial_s^2 + 2 rho omega partial_s
              + rho^2 + partial_theta^2,

where rho, omega > 0 and both coordinates have period 2 pi. For a smooth periodic H, direct differentiation gives

    Delta[r^rho H(omega log r, theta)]
      = r^(rho-2) (L_omega H)(omega log r, theta).

The same subharmonicity conclusion holds for continuous H with distributional L_omega H >= 0. Convolve H on the torus with nonnegative smooth approximate identities. These convolutions converge uniformly, commute with L_omega, and have pointwise nonnegative L_omega. The corresponding functions on the punctured plane are therefore subharmonic, and converge locally uniformly to the desired function. Boundedness of H and rho > 0 give uniform convergence to 0 at the origin. The bounded-above removable-singularity theorem supplies the subharmonic extension with value 0. In particular, no unverified restriction of a measure to a fixed phase and no hidden negative atom at the origin are being used.

For D = omega partial_s + rho, define

    (Rf)(s) = integral_0^infinity exp(-rho t) f(s-omega t) dt.

Integration by parts gives DRf = f. Composing two copies of R, with the change of variable t = t_1+t_2, gives

    D^(-2)f(s) = integral_0^infinity t exp(-rho t) f(s-omega t) dt.

This verifies both the orientation of the temporal shift and the positive kernel. There is no periodic homogeneous solution of D^2 a = 0 except zero, because its solutions have the form exp(-rho s/omega)(A+Bs). Thus the periodic inverse is unique. A nonnegative smooth f gives a >= 0; if f is nonzero, periodicity makes the positive integral strictly positive at every s. Mollifying a itself proves the non-strict statement when a is merely continuous and D^2 a is a nonnegative distribution.

The angular average a_j(s) of H_j satisfies D^2 a_j equal to the angular average of L_omega H_j, in distributions. It is consequently nonnegative at every phase. This use of angular averaging is valid even when the original right-hand side is a measure.

For the Fourier mode exp(i(ms+n theta)), the multiplier is

    d_mn = rho^2-omega^2 m^2-n^2 + 2 i rho omega m.

It vanishes exactly when m = 0 and rho = |n|. The noninteger restriction in the inversion theorems is therefore sufficient and cannot silently be dropped. At integer rho the angular modes exp(±i rho theta) form a kernel, with compatibility and uniqueness issues absent from the audited statements. The symmetry theorem itself requires no noninteger restriction.

## 2. Common sign-reversing angular symmetry

Theorem A is accepted for every continuous admissible triple with a common shift alpha and

    H_j(s,theta) = a_j(s)+Q_j(s,theta),
    Q_j(s,theta+alpha) = -Q_j(s,theta).

Translation invariance of integration shows that every Q_j has zero angular mean, so a_j is exactly the nonnegative angular average established above. Let a_* = min_j a_j(s). The componentwise inequality

    H_j(s,theta+alpha) >= 2 a_* - H_j(s,theta)

and the coordinatewise monotonicity and sign-reversal identity of the median imply

    med_j H_j(s,theta+alpha) >= 2 a_* - med_j H_j(s,theta).

After angular integration, the left integral equals the unshifted one, giving M(s) >= 2 pi a_* >= 0. This proof does not require alpha to have any particular rational relation to 2 pi. If an irrational alpha forces a continuous Q_j to be zero, the conclusion simply specializes to that degenerate case.

A common odd multiple spectrum of n has the required shift pi/n. The temporal coefficients can change relative amplitudes and angular shapes independently, provided the resulting profiles remain continuous and satisfy L_omega H_j >= 0. “Arbitrary modulation” does not mean that an arbitrary choice of coefficients automatically satisfies that positivity constraint. Mixing even and odd angular frequencies without a common sign-reversing shift is outside this theorem.

## 3. Fixed finite forcing at high temporal frequency

Theorem B is accepted for fixed noninteger rho > 0 and fixed, nonzero, nonnegative real trigonometric polynomials F_1, F_2, F_3. Each g_j, the temporal average of F_j, is a nonnegative trigonometric polynomial. It is nonzero: if its integral in s vanished for every theta, continuity and nonnegativity of F_j would force F_j to vanish everywhere.

The temporal-average solution h_j is independent of omega and solves h_j''+rho^2 h_j = g_j. Variation of constants over T = pi/rho gives the exact identity

    h_j(theta+T)+h_j(theta)
       = (1/rho) integral_0^T sin(rho(T-x)) g_j(theta+x) dx
       = q_j(theta).

The sine kernel is strictly positive in the interior, whether or not T exceeds an angular period. A nonzero trigonometric polynomial cannot vanish on an interval, so q_j(theta) > 0 at every theta. Continuity and compactness then imply

    delta = (1/2) min_(j,theta) q_j(theta) > 0.

Median pairing gives the lower bound 2 pi delta for the angular median integral of the h_j. For m != 0 and omega > rho, the real part of d_mn is negative and

    |d_mn| >= omega^2 m^2+n^2-rho^2 >= omega^2-rho^2.

For S = max_j sum_(m != 0,n) |f_j(m,n)|, the finite Fourier sum consequently gives

    sup_(s,theta,j) |H_j,omega(s,theta)-h_j(theta)|
       <= S/(omega^2-rho^2).

The median is 1-Lipschitz for the maximum norm on its three arguments. Integrating the preceding uniform error proves

    M_omega(s) >= 2 pi [delta-S/(omega^2-rho^2)]

for every phase, including at median ties. The strict threshold omega^2 > rho^2+S/delta is correct.

Important boundary checks:

- Every F_j must be nonzero for the displayed delta to be strictly positive. Allowing two zero forcings gives the identically zero median and disproves any unrestricted strict-positivity extension.
- If S = 0, each forcing and solution is independent of s. The lower bound 2 pi delta holds directly at every omega > 0, without using the singular-looking high-frequency denominator.
- The conclusion is for a fixed forcing as omega changes. It is not a forcing-independent threshold, nor a conclusion for intermediate frequencies.
- Forcing with changing Fourier support or coefficients is not controlled by holding the original S and delta fixed.

## 4. Exact example and an independent reconstruction

The specified polynomial is

    P(s,theta) = 1+2 cos(theta)+6 cos(s-theta)+sin(s-theta)
                 -5 sin(s)-5 cos(s+theta)+2 sin(s+theta),

with rho = 3/2 and omega = 2/25. Its square is a nonnegative forcing at every point, independent of sampling. The multiplier check above gives a unique real finite Fourier solution H of L_omega H = P^2. Angular translation commutes with L_omega, so the three rotations by 0, 2 pi/3, and 4 pi/3 are admissible.

### Independent algebra

The independent reconstruction first uses addition identities to write

    P = A(theta)+B(theta) cos(s)+C(theta) sin(s),
    A = 1+2 cos(theta),
    B = cos(theta)+sin(theta),
    C = -5+3 cos(theta)+11 sin(theta).

It squares this expression in real temporal harmonics:

    constant: A^2+(B^2+C^2)/2,
    cos(s): 2AB,                 sin(s): 2AC,
    cos(2s): (B^2-C^2)/2,        sin(2s): BC.

For temporal frequency m > 0 and angular frequency n, put

    a = rho^2-omega^2 m^2-n^2,   b = 2 rho omega m.

If the forcing has cosine and sine coefficients c and d, respectively, then the solution coefficients U,V must satisfy

    aU+bV = c,   aV-bU = d.

The audit uses U = (ac-bd)/(a^2+b^2), V = (bc+ad)/(a^2+b^2), and checks both equations exactly. At phases 0 and pi the sine terms vanish and the cosine signs are respectively (+1,+1) and (-1,+1). All independently reconstructed angular coefficients agree exactly with the supplied certificate. This also independently fixes the potentially consequential sign of the drift term.

### Independent rational quadrature

The audit uses 600 angular nodes rather than the construction's 768. A separate alternating-series calculation in Machin's identity proves the coarser enclosure

    103993/33102 < pi < 104348/33215.

Machin's branch is correct: for a = atan(1/5), tan(4a) = 120/119, so tan(4a-atan(1/239)) = 1, and that angle lies in (0,pi/2).

The audit reduces each angular argument modulo 2 pi to [-pi,pi], substitutes the rational midpoint of this enclosure, and uses the degree-25 Taylor polynomials, evaluated by Horner's rule. The cosine polynomial has highest nonzero degree 24 and the sine polynomial degree 25. Since all relevant derivatives have magnitude at most one and the argument has magnitude less than 4, both trigonometric errors are bounded by

    4^26/26! + (pi_upper-pi_lower)/2.

The second term also bounds argument substitution after reduction, since the coefficient of pi is in [-1,1]. The phase-slice error is bounded by twice this error times the sum of absolute real and imaginary parts of its positive angular coefficients.

For slice coefficients z_n, a derivative bound is 2 sum_(n=1)^2 n |z_n|. The audit obtains rational upper bounds on |z_n| using integer square roots and exact comparison. Thus its derivative estimate is computed differently and is slightly sharper than the construction's real/imaginary L1 estimate.

The median of three D-Lipschitz rotations remains D-Lipschitz, even at crossing points. For a centered cell of length 2 pi/N, integrating D times distance to its node gives normalized quadrature error at most D pi/(2N). Rotations by one third of a turn land exactly on the 600-node grid. The median is evaluated as the sum of the three inputs minus their minimum and maximum, rather than by the construction's sorting expression. Its 1-Lipschitz property transfers the input evaluation error without an extra factor of three.

All acceptance comparisons are rational. Outward rounding of the independently proved enclosures gives

    -0.454831 < M(0)/(2 pi) < -0.354875 < -1/3,
     1 < 1.252288 < M(pi)/(2 pi) < 1.287355.

The [independent audit certificate](../certificates/periodic_audit_exact.json) records the exact rational grid average, errors, outward endpoints, and angular coefficients. The decimal display is not the basis of acceptance.

### Review of the original certificate

The construction's 768-node certificate is also sound. Its degree-32 cosine and degree-31 sine polynomials are both correctly regarded as degree-32 Taylor polynomials, since the degree-32 sine coefficient is zero. Therefore the common remainder 4^33/33! is legitimate for both. Its rational pi interval, reduction modulo the angular grid, real/conjugate coefficient checks, L1 derivative bound, median Lipschitz bound, and centered-cell error all have the correct orientation and constants. The supplied exact rational endpoints prove the asserted strict comparisons to -1/3 and 1.

Meaningful negative controls passed: reversing the drift sign fails the exact operator identity; altering the constant solution coefficient fails that identity; swapping the positive and negative phase conclusions fails; a 12-node grid has a certified interval crossing zero and therefore cannot certify negativity; a positive constant produces the exact integral 1 and is not classified as negative. An additional integer-rho resonance control records the omitted-inversion case.

### Consequence and limitation

The angular average of P^2 is nonnegative and not identically zero. The scalar inverse is therefore strictly positive at every phase, so each rotated profile has positive angular average and a positive circle maximum. Whole-plane realizability follows from Section 1. Phase pi corresponds to r = exp(pi/omega) = exp(25 pi/2), while phase zero occurs at r = 1.

The example disproves a proposed stronger assertion of nonnegative median integral at every phase. Its strictly positive phase proves that it is **not** a counterexample to the original supremum assertion or to the some-phase assertion. Continuity also supplies open intervals of each sign, but no conclusion about all remaining phases is needed or claimed.

## 5. Positive finite-point obstruction

Theorem C is accepted for noninteger rho > 0, omega > 0, and any nonempty finite family of points with positive weights.

First, inversion on periodic distributions is legitimate. For m^2+n^2 sufficiently large,

    |d_mn| >= omega^2 m^2+n^2-rho^2
             >= c (m^2+n^2)

for some c > 0 depending on omega. The finitely many remaining multipliers are nonzero by noninteger rho. There is thus no high-frequency small-divisor issue, and a smooth right-hand side has a smooth inverse. Real right-hand sides give real solutions by conjugate symmetry.

To check the logarithmic sign and mass normalization, set y = s/omega locally. Then omega partial_s = partial_y and

    [(partial_y+rho)^2+partial_theta^2](exp(-rho y)v)
       = exp(-rho y) Delta_(y,theta) v.

Since Delta log(sqrt(y^2+theta^2)) = 2 pi delta(y) delta(theta), and delta(y) = omega delta(s),

    Phi(s,theta) = [exp(-rho s/omega)/(2 pi omega)]
                  log(sqrt((s/omega)^2+theta^2))

satisfies L_omega Phi = delta(s) delta(theta) for ordinary area measure. In particular, the singularity is negative infinity, not positive infinity, and its normalization has the necessary factor 1/omega.

A smooth local cutoff equal to one near zero produces L_omega(chi Phi) = delta_0+R with smooth periodic R supported away from zero. Define G = chi Phi-L_omega^(-1)R. It is a real periodic Green function, smooth away from zero. The difference between exp(-rho s/omega) times the logarithm and the logarithm itself is bounded near zero, since it is O(|s| |log distance|). Hence

    G(s,theta) = (1/(2 pi omega))
                log(sqrt((s/omega)^2+theta^2)) + O(1).

Merge repeated evaluation points, which preserves positive weights. Use a nonnegative smooth bump of mass one, rescale it by epsilon in a small coordinate patch around the first point x_1, and convolve with G using ordinary torus area. The resulting H_epsilon is real and smooth with L_omega H_epsilon equal to that nonnegative bump. At x_1, the change of variables in the logarithmic integral gives

    H_epsilon(x_1) = (log epsilon)/(2 pi omega)+O(1) -> -infinity.

The logarithm is locally integrable, so convolution is legitimate. At every other distinct evaluation point it converges to the finite value G(x_a-x_1). The weighted sum therefore tends to negative infinity and is negative for small enough epsilon.

This establishes the stated failure of any universal fixed positive finite sum of point evaluations. It includes a fixed positive two-point pairing. It does not invalidate Theorem A, which restricts the profiles to a symmetry subclass; it does not rule out integral averages, profile-dependent pairings, or global inequalities. The noninteger restriction is retained throughout the construction, rather than assuming that a Green inverse exists at resonance.

## 6. Search material and final scope

Exploratory floating-point searches supply no continuum sign certificate and do not enter the mathematical acceptance.

For a continuous periodic triple, strictly negative M at every phase would imply a uniform negative maximum of M. Combined with a bounded positive normalizing maximum, that would genuinely violate the normalized-supremum assertion. No such triple is supplied here. Conversely, a negative value at a single phase cannot do so. The report consistently preserves this distinction.

## Reproduction

The complete arithmetic conventions and exact data are in [Reproduction conventions](../REPRODUCTION.md) and the [independent audit certificate](../certificates/periodic_audit_exact.json). The analytic arguments above remain essential parts of this acceptance.
