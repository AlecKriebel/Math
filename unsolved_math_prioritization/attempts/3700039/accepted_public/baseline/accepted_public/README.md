# Median inequality for three subharmonic functions

## Fourth-pass reader checkpoint

**The unrestricted normalized-supremum conjecture remains unresolved.** This reader contains four documented shared substantive passes on problem 3700039, row 1762, AMR-036-0039. The fourth pass extends the periodic some-phase theorem to an arbitrary changing second-harmonic axis under modulus dominance; gives an affirmative radial-curvature-defect criterion; and realizes arbitrary fixed finite harmonic profiles at genuine record scales of smooth functions flat at the origin. The latter construction transfers the sharp lower endpoint -pi to honest record circles but has positive gaps with quotient 2pi. It is not a counterexample. The lifetime prior attempt count is unknown. Audits, reader assembly and reproduction add no research pass. No historical novelty is claimed.

The credited source is A. Eremenko, [Conjectured inequality for subharmonic functions](https://www.math.purdue.edu/~eremenko/dvi/subh1.pdf), dated 4 April 2015. Its harmonic and homogeneous affirmative cases remain credited prior results. The [corrected third-pass reader](baseline/corrected_public/README.md) and its [independent review](baseline/public/reader_edition_acceptance.md) are preserved once, byte for byte. Their bounded observation about the author's public problem index is not a worldwide literature-status claim. No new status inference is made here.

## Question and actual normalization

For whole-plane subharmonic u_1,u_2,u_3 with u_j(0)=0, put

I(r)=integral_0^(2pi) med(u_1,u_2,u_3)(r exp(i theta)) dtheta,

B(r)=max_(j,theta) u_j(r exp(i theta)).

The target is sup I(r)/B(r)>=0. Ordinary angular measure dtheta is used throughout unless a mean is explicitly divided by 2pi. For a nonzero triple this reader evaluates the quotient on D={r>0:B(r)>0}; the globally zero triple is treated separately as zero equality. The [denominator theorem](baseline/corrected_public/baseline/two_pass/proofs/first_pass_theory.md) gives D=(R_0,infinity) and identifies zero denominators with joint zero disks. No equivalence with assigning zero to every 0/0 quotient is asserted.

A counterexample needs one epsilon>0 with I(r)/B(r)<=-epsilon at every radius in D. Negative individual circles, negative honest records, a negative critical-layer median and even negative numerators at every finite radius are insufficient. The small-radius limsup question remains distinct from the full supremum question.

## Arbitrary second-harmonic phase under dominance

The full [relative-phase proof](proofs/relative_phase.md) and [independent acceptance](audits/relative_phase_acceptance.md) treat

H_j(s,theta)=c(s)+a(s)cos(x_j)+b(s)cos(2x_j)+d(s)sin(2x_j),

x_j=n theta+m s+2pi j/3, L=(omega partial_s+rho)^2+partial_theta^2,

where a,b,d,c are continuous real 2pi-periodic functions, n>=1 and m are integers, rho,omega>0, a^2<=b^2+d^2, and L H_j>=0 distributionally. There is a phase with nonnegative angular median. The second harmonic's axis can change arbitrarily; the first axis remains fixed in this rigid helical frame. There is no differentiability, temporal bandwidth, sign, small-modulation or nonresonance assumption.

With R^2=b^2+d^2 and k=3sqrt(3)/(2pi), the exact normalized angular median is

M(s)/(2pi)=c(s)-k a(s)^2 b(s)/(2R(s)^2),

with fraction zero at R=0. More invariantly, for complex A,B with |A|<=|B|, the oscillating median mean equals -(k/2)Re(A^2/B), continuously defined as zero at A=B=0. The proof counts all strict-dominance crossings, uses their actual switching orientation and primitive sums, and reaches collision and triple-tie boundaries by uniform continuity.

In the cone a nowhere zero and b>0 everywhere, put K=a^2 b/(2R^2) and Gamma=6sqrt(2)/(8+sqrt(2)). Then

average_s[M(s)/(2pi)] >= (Gamma-k) average_s K(s)>0,

Gamma-k>1/40.

Zero and opposite-sign cases are separate and may have equality. Positive degree-two coefficient tests are applied only after full-phase averaging has produced a smooth nonnegative polynomial. The complete helical drift and complex mixing are retained. The linear envelopes are integrated before use; median and phase average are never interchanged. A changing first axis can cancel its linear average even with positive invariant projection, so the arbitrary two-complex-amplitude some-phase problem remains outside this theorem. The dominance hypothesis cannot be dropped from the exact identity.

## Radial-curvature defect without angular compactness

The complete [critical-layer report](proofs/packets/REPORT.md), with its [packet acceptance](audits/harmonic_packet_acceptance.md), proves that for a C2 cylindrical triple U_j near a selected circle, with U_(j,tt)+U_(j,theta theta)>=0, every lambda>0 satisfies

I(exp t) >= -(1/lambda^2) sum_j ||(U_(j,tt)-lambda^2 U_j)^+||_1.

Thus a sequence of positive-denominator circles with the right-hand defect divided by lambda^2 B tending to zero has nonnegative quotient liminf. No angular variation, bandwidth, compactness, integer lambda or differentiability of B is assumed. The positive part is essential.

If U_j=F g_j with positive C2 F, beta=F'/F and kappa=F''/F>0, the defect is F(g_(j,tt)+2 beta g_(j,t)). Bounded F/B and |beta|/sqrt(kappa), together with sum ||g_t||_1=o(sqrt(kappa)) and sum ||g_tt||_1=o(kappa), are sufficient. These conditions allow critical, noncompact angular profiles. Conversely, a smooth uniformly negative counterexample would have a definite radial-curvature defect at every positive-denominator circle and every lambda. This is a necessary obstruction, not an existence claim.

## Negative genuine records and the sharp endpoint

The same [report](proofs/packets/REPORT.md) constructs a smooth whole-plane triple, all flat at zero, with B(r)>0 for every r>0 and honest records t_k of slopes n_k/2, n_k tending to infinity. At these records the quotient tends to -3sqrt(3)/4. The harmonic layer is

H_j(x,y)=exp(x)cos(y+2pi j/3)+exp(2x)cos(2y+4pi j/3).

Its boundary numerator is -3sqrt(3)/2 and its actual maximum is 2. Their ratio is -3sqrt(3)/4. This distinction is retained in the active proof and certificates.

The [fixed-harmonic-profile extension](proofs/packets/HARMONIC_EMBEDDING.md) embeds every fixed nonzero triple of real harmonic polynomials h_j with h_j(0)=0. If C_0 is its actual joint unit-circle maximum and J_0 its median integral, the embedded smooth flat triple has genuine record slopes q n_k for some fixed q>0 and record quotients tending to J_0/C_0. Rescaled profiles converge in C-infinity on compact subsets of the entire layer plane.

Applying the [earlier finite Fejer harmonic construction](baseline/corrected_public/baseline/two_pass/proofs/first_pass_theory.md) shows that, for every epsilon>0, some smooth flat triple has infinitely many honest record quotients tending to a value below -pi+epsilon. This proves sharpness of the universal -pi lower bound over the record class. It does not construct a single fixed triple with limit exactly -pi.

Both packet constructions include positive repairs of every cutoff transition, all infinite radial tails, genuine comparisons against every earlier circle, actual joint maxima and all-order flatness. Between packets all three functions equal a positive radial value; their quotient is exactly 2pi. Consequently their full positive-denominator supremum and small-radius limsup are both 2pi. No unfavorable layer classification alone can settle the selection of favorable radii.

## What remains and where to read

The open frontier includes arbitrary changing first-harmonic axes, nondominant complex amplitudes, changing angular spectra, independent noncyclic triples and persistent coupled radial/angular layers. The general problem also includes nonsmooth subharmonic representatives and unrestricted growth or Riesz mass. The new C2 radial criterion is not asserted for every nonsmooth representative.

The [dependency guide](DEPENDENCIES.md) points to every inherited result used. The [reproduction guide](REPRODUCTION.md) distinguishes exact finite checks from analytic existence and distributional arguments, and the [validation account](VALIDATION.md) states the checks and falsification coverage. The [manifest](MANIFEST.json) binds all and only included public mathematical files. All earlier proof corrections and the corrected third-reader author-certificate link remain preserved.
