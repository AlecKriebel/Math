# Median inequality for three subharmonic functions

## Final five-pass result

**The unrestricted normalized-supremum conjecture remains unresolved.** This final reader records five documented shared substantive passes on problem 3700039, row 1762, AMR-036-0039. The fifth pass proves a quantitative torus-mean theorem for arbitrary complex two-mode cyclic coefficients under second-harmonic dominance, and an affirmative actual-denominator limit for a one-fast-phase smooth flat class. Both are restricted theorems. There is no sixth research pass, genuine counterexample, or claim of historical novelty. The lifetime prior attempt count is unknown. Auditing, editing, assembly, and reproduction do not add substantive passes.

The credited source is A. Eremenko, [Conjectured inequality for subharmonic functions](https://www.math.purdue.edu/~eremenko/dvi/subh1.pdf), dated 4 April 2015. Its harmonic and homogeneous affirmative cases remain credited prior results. The [fourth-pass reader](baseline/accepted_public/README.md) and its [independent edition acceptance](baseline/public/reader_edition_acceptance.md) are preserved once with their complete earlier proofs, corrections, audits, and certificates. The inherited bounded observation about the author's public problem index is not a claim of worldwide literature status. This final assembly makes no new literature-status inference.

## Original target and denominator convention

For whole-plane subharmonic u_1,u_2,u_3 with u_j(0)=0, define

    I(r)=integral_0^(2pi) med_j u_j(r exp(i theta)) dtheta,
    B(r)=max_(j,theta) u_j(r exp(i theta)).

The target is sup I(r)/B(r)>=0. Angular measure is ordinary dtheta, without normalization by 2pi, unless an average is explicitly displayed. For a nonzero triple the quotient is evaluated only on D={r>0:B(r)>0}; the globally zero triple is treated separately as zero equality. The [denominator theorem](baseline/accepted_public/baseline/corrected_public/baseline/two_pass/proofs/first_pass_theory.md) gives D=(R_0,infinity) and identifies zero denominators with joint zero disks. Assigning zero to every 0/0 is a different convention whose equivalence is not established.

A counterexample must have one epsilon>0 with I(r)/B(r)<=-epsilon at every r in D. Negative individual circles, negative record scales, negative critical layers, and even strictly negative numerators at every finite radius do not suffice. The full supremum and the stronger small-radius question remain distinct.

## Five-pass progression

1. The [first-pass theory](baseline/accepted_public/baseline/corrected_public/baseline/two_pass/proofs/first_pass_theory.md) established the denominator classification, sharp fixed-radius range -pi<=I/B<=2pi, a finite degree-9999 harmonic witness below -0.99pi, and a harmonic triple with negative numerator at every radius but supremum zero. It reduced smooth potential counterexamples to all-flat origins. The [construction results](baseline/accepted_public/baseline/corrected_public/baseline/two_pass/proofs/first_pass_constructions.md) settled common spiral and rotating-separable classes and compact positive logarithmic potentials with polynomial harmonic parts, and gave an exact periodic sufficient-counterexample criterion.
2. The [second-pass reader](baseline/accepted_public/baseline/corrected_public/baseline/two_pass/README.md) proved positive Fejer-smoothing and relative angular-compactness criteria for flat origins and flat-disk boundaries. It showed compactness and simple normalized dilation limits are not automatic. The periodic branch gave a sign-reversal theorem, a fixed-forcing high-frequency theorem, an exactly certified mixed-sign example, and an obstruction to fixed finite torus-point tests.
3. The [third-pass reader](baseline/accepted_public/baseline/corrected_public/README.md) sharpened heat-smoothing estimates, established subcritical normalized-variation and negative-part compactness criteria, and constructed an admissible critical example with noncompact negative parts. Its cyclic real two-harmonic theorem allows arbitrary continuous amplitude modulation and rigid helical drift, including resonances, while retaining the specified relative axes.
4. The [fourth-pass reader](baseline/accepted_public/README.md) allowed arbitrary second-harmonic phase under dominance, proved a local C2 radial-curvature-defect criterion, and embedded arbitrary fixed finite harmonic triples at genuine record scales of whole-plane smooth flat functions. Record ratios approach the sharp lower endpoint -pi across the class. Those constructions have positive radial gaps with quotient 2pi, so their supremum and small-radius limsup are 2pi.
5. The final pass closes the remaining arbitrary-first-axis gap inside the dominance region and treats a continually oscillating one-fast-phase flat class with no separated annular gaps. The complete new proofs and audits follow.

Each historical reader retains its own contemporaneous frontier. In particular, the fourth reader's first-axis obstruction is superseded in the dominance region by the next theorem; it remains a valid diagnosis of that older averaging method.

## Arbitrary complex phases under second-harmonic dominance

The [complete proof](proofs/complex_dominance.md) and [independent acceptance](audits/complex_dominance_acceptance.md) assume rho,omega>0, integer n>=1, continuous 2pi-periodic real c and complex A,B, pointwise |A|<=|B|, and distributional positivity L H_j>=0, where

    L=(omega partial_s+rho)^2+partial_theta^2,
    H_j=c(s)+Re[A(s)exp(i(n theta+2pi j/3))
                    +B(s)exp(2i(n theta+2pi j/3))], j=0,1,2.

Let M(s)=integral med_j H_j(s,theta) dtheta and overline denote ds/(2pi) average. With k=3sqrt(3)/(2pi) and Gamma=6sqrt(2)/(8+sqrt(2)),

    overline[M/(2pi)] >= ((Gamma-k)/2) overline[|A|],
    (Gamma-k)/2 > 1/80.

If A is not identically zero there is a strictly positive phase. If A is identically zero, M(s)=2pi c(s)>=0 at every phase. Arbitrary phase motion, zeros, winding, both resonances, and continuous distributionally admissible coefficients are included. There is no fixed first axis or temporal-bandwidth assumption.

The key coercivity estimate is

    integral |[(omega partial_s+rho)^2-r^2]u| ds
      >= |rho^2-r^2| integral |u| ds.

It follows by factoring into two first-order real-shifted operators and integrating a regularized complex projection. Positive degree-two forcing bounds control mean moduli, not moduli of means. A uniform all-ratio envelope then combines with the accepted exact slice identity

    M(s)/(2pi)=c(s)-(k/2)Re(A(s)^2/B(s)).

The quotient is continuously zero at A=B=0. Temporal mollification is used before dominance enters; dominance need not survive mollification. No nonlinear median is commuted with a phase average. The theorem's constant is not claimed optimal, although the relaxed two-envelope constant is exact.

The author's inverse-product check has a signed-mass algebraic assertion despite its total-variation label. The independent audit explicitly proves and checks absolute TV 1/|rho^2-r^2| above and below resonance. The author check is not presented as independently establishing that absolute value.

## A one-fast-phase flat class with an actual limit

The [full theorem and realization](proofs/one_fast_phase.md), with [complete independent acceptance](audits/fast_phase_acceptance.md), use p>0, Q=r^(-p), f=exp(-Q), a smooth real periodic psi with measure-zero critical set, and smooth real periodic profiles H_j(theta,x), not all zero. All three components share the same phase Q psi(theta). Suppose

    V_j(r,theta)=f H_j(theta,Q psi(theta))

are subharmonic near zero. Then

    B(r)/f -> B_*=max_(j,theta,x) H_j(theta,x)>0,
    I(r)/B(r) -> J_*/B_* >=0,
    J_*=integral_theta average_x med_j H_j(theta,x) dtheta.

The same conclusion holds for smooth errors E_j with uniform |E_j|/f->0 and uniform |E_(j,tt)+E_(j,theta theta)|/(Q^2 f)->0, provided the resulting functions are subharmonic near zero. Here t=log r. These are actual-maximum statements, not coefficient-envelope replacements.

Subharmonicity forces every frozen cone inequality

    [a(theta)partial_x^2-2psi(theta)partial_x+1]H_j>=0,
    a=psi^2+(psi')^2/p^2.

At regular angular phases a weighted positive half-period kernel yields a nonnegative frozen median mean. At stationary phases a repeated-root positive inverse gives componentwise nonnegativity. Phase averaging handles all large real Q, and local inversion near regular angles samples the actual maximum. These analytic arguments, not finite quadrature, establish the limit.

Conversely, every such frozen-positive profile admits the whole-plane smooth flat realization f[H_j(theta,Q psi(theta))+C/Q], with C bounding both explicit remainders. The common lower-order repair gives a nonnegative Laplacian for every Q>0 and preserves the limit. No annular transition or infinite radial tail is discarded.

For p=1, psi=sin(theta), the explicit example is

    u_j=exp(-1/r)[1+3cos(theta)^16 cos(sin(theta)/r+2pi j/3)+768r],
    u_j(0)=0.

Its exact actual maximum is B(r)=exp(-1/r)(4+768r), and I/B->pi/2. It has negative components at every sufficiently small radius and negative actual median at theta=0 for r<1/1536. Its actual-denominator-normalized negative parts have no L1-convergent subsequence as r->0. Their normalized angular variation, and that of the normalized profiles, is of order Q, the critical radial-curvature scale. The raw functions carry the additional vanishing factor exp(-Q). This is an affirmative critical noncompact example.

## Precise final remaining statement

The unresolved claim remains: every whole-plane subharmonic triple u_j with u_j(0)=0 satisfies sup_(r:B(r)>0) I(r)/B(r)>=0 under the convention above. No result here rules out all smooth all-flat triples with I/B<=-epsilon at every positive-denominator radius.

For periodic cyclic profiles, nondominant arbitrary complex amplitudes remain outside the fifth-pass theorem; the inherited angular identity is false outside dominance. Arbitrary independent periodic triples and the unrestricted some-phase assertion also remain unresolved. Multiple interacting fast phases, nonseparable envelopes, changing spectra, and coupled radial/angular mode transfers need not satisfy the one-fast-phase geometry. The general problem includes nonsmooth representatives and unrestricted growth and Riesz mass. The earlier radial-defect criterion remains local C2, without unjustified distributional fixed-circle slicing.

The [dependency account](DEPENDENCIES.md), [reproduction guide](REPRODUCTION.md), [validation account](VALIDATION.md), and [editorial changes](changes/README.md) distinguish inherited results, exact finite calculations, full analytic proofs, and the preserved original texts. The [public manifest](MANIFEST.json) binds exactly the included mathematical reader.
