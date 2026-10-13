# Median inequality for three subharmonic functions

## Third pass reader checkpoint

**The unrestricted normalized-supremum conjecture remains unresolved.** This edition contains three documented shared substantive passes on problem 3700039, row 1762, AMR-036-0039. The third pass adds affirmative results for subcritical angular variation, compact negative parts, and a genuinely changing cyclic two-harmonic class. A smooth critical-frequency example shows why the remaining concentration regime cannot be discarded. None of these results supplies a counterexample. The lifetime number of earlier attempts is unknown; independent audits and this reader assembly do not add research passes. No historical novelty claim is made.

The source is A. Eremenko, [Conjectured inequality for subharmonic functions](https://www.math.purdue.edu/~eremenko/dvi/subh1.pdf), dated 4 April 2015. The harmonic and homogeneous affirmative cases are credited prior results. The [historical two-pass reader](baseline/two_pass/README.md) and its [independent acceptance](baseline/review/reader_edition_acceptance.md) are preserved unchanged. Their observation that the author's [problem index](https://www.math.purdue.edu/~eremenko/uns1.html) linked the note on 13 October 2026 without a resolution annotation is a bounded source observation, not proof of worldwide openness. This edition makes no additional literature-status inference.

## Question and normalization

Let u_1,u_2,u_3 be whole-plane subharmonic functions with u_j(0)=0. Define

I(r)=integral_0^(2 pi) med(u_1,u_2,u_3)(r exp(i theta)) dtheta,

B(r)=max_(j,theta) u_j(r exp(i theta)).

The target is sup I(r)/B(r)>=0. Angular integrals and L1 norms use ordinary dtheta unless explicitly divided by 2 pi. The source does not specify a zero-denominator convention. This reader tests a nonzero triple only on D={r>0:B(r)>0}; the globally zero triple is treated separately as zero equality. The [denominator theorem](baseline/two_pass/proofs/first_pass_theory.md) gives D=(R_0,infinity) and identifies B=0 with joint zero disks. No equivalence with assigning zero to every 0/0 quotient has been asserted.

A genuine counterexample would require one epsilon>0 with I(r)/B(r)<=-epsilon at every radius in D. A negative circle, a negative phase, or negative integrals at every finite radius can coexist with normalized supremum zero. The stronger small-radius assertion remains distinct from the supremum target. There is no general power-growth hypothesis.

## What the first two passes established

The unchanged [two-pass reader](baseline/two_pass/README.md) gives all earlier proofs and audits. These include the sharp fixed-radius range -pi<=I/B<=2 pi; a degree-9999 harmonic negative-circle witness; a harmonic triple with I(r)<0 at every finite radius but supremum zero; the finite-jet reduction; common spiral and rotating-separable classes; compact positive logarithmic potentials with polynomial harmonic parts; and a log-periodic sufficient counterexample criterion.

The second pass gave positive Fejer smoothing and angular-compactness criteria, explicit failures of automatic compactness and simple dilation limits, a fixed-forcing high-frequency periodic result, a rationally certified mixed-sign phase example, and a Green-function obstruction to fixed finite torus-point tests. Those scope restrictions remain in force. The exact mixed-sign certificate has M(0)/(2 pi)<-1/3 and M(pi)/(2 pi)>1 and is affirmative for the supremum target.

## Concentration results in the third pass

The full [concentration proof](proofs/concentration.md) and [independent audit](audits/concentration_acceptance.md) apply heat smoothing to actual subharmonic representatives, including nonsmooth circle singularities. Write

U_j(t,theta)=u_j(exp(t+i theta)), b(t)=B(exp t),

A(t)=integral_(-infinity)^t (t-s)b(s) ds, a(t)=A(t)/b(t).

At b(t)>0 and A(t)<infinity, with circular heat smoothing P_tau and E_tau=sum_j||U_j-P_tau U_j||_1/b,

I(exp t)/b(t) >= -3 sqrt(pi/(2e)) a(t)/tau - E_tau(t)/4.

For finite D(t)=sum_j TV(U_j(t,.))/b(t), optimization gives

I(exp t)/b(t) >= -C_* [a(t)D(t)^2]^(1/3),

C_*^3=81/(16 sqrt(2 pi e)), C_*<1.0700.

At an infinitely-flat record of slope M, a<=M^(-2). Thus D=o(M) along selected records implies a nonnegative small-radius limsup, even when D diverges and full normalized angular profiles are noncompact. At a last zero-disk boundary t_0, the sufficient condition is (t-t_0)D(t)->0, or the finer condition sqrt(a)D->0.

A separate threshold-transfer estimate needs compactness only of the normalized negative parts. It yields the same respective origin limsup and positive-denominator boundary lower-limit conclusions. The negative-variation condition sqrt(a)D_minus->0 with a->0 also suffices. The proof fixes the smoothing scale before taking the record or boundary limit, then sends the smoothing scale to zero; it makes no unproved joint-limit exchange.

The smooth flat critical example has, at genuine record slopes n_k,

q/B=(1+2cos(n_k theta))/3,

integral (q/B)^- dtheta=2sqrt(3)/3-2pi/9>0,

D=8n_k, D_minus=2n_k.

Its negative parts are noncompact even at those records. Yet three identical copies have normalized median integral 2pi/3 at the records and positive small-radius means. This example excludes automatic negative-part compactness, not the conjecture. The lower bound ||K''||_1>=1/(8sigma^2) for localized positive probability kernels identifies the quadratic curvature cost of this estimate; it does not rule out other smoothing or nonlinear methods.

## Cyclic two harmonic results in the third pass

The full [cyclic proof](proofs/cyclic_two_harmonic.md) and [independent audit](audits/cyclic_acceptance.md) consider

L=(omega partial_s+rho)^2+partial_theta^2,

H_j=c(s)+a(s)cos(n theta+m s+2pi j/3)
       +b(s)cos(2n theta+2m s+4pi j/3).

Here a,b,c are arbitrary continuous real 2pi-periodic functions, n is a positive integer, m is any integer, and rho,omega>0. Distributional positivity L H_j>=0 implies a phase with nonnegative angular median integral. Resonance is allowed; no temporal bandwidth, small-modulation, or fixed-forcing hypothesis is needed. The relative harmonic axes have the displayed fixed relation and the common drift is rigid.

When b>0 everywhere and a is nowhere zero, there is the stronger positive-average estimate

average_s[M(s)/(2pi)] >= (d-k) average_s F(|a|,b)>0,

k=3sqrt(3)/(2pi), d=3(1+sqrt(2))/8, d-k>1/40,

where the full three-branch F is given in the proof. All other sign and zero cases are handled separately using c>=0 and the exact signed median formula. A universal strict-positive conclusion in the zero cases would be false.

The argument uses F<=b and F<=(2-sqrt(2))|a| before averaging. It does not commute the median or F with phase averaging. Distributional forcing is tested with smooth nonnegative functions. Full-phase averaging produces a smooth angular polynomial, followed by positive reflection and pointwise evaluation. The description by circles or helices is the limit of these smooth tests, including the full covering multiplicity for n>1, never a direct pairing between singular measures. This interpretation is recorded in the [precise clarification](changes/README.md) and its [mathematical patch](changes/helical_test_clarification.patch).

## Remaining frontier

The concentration estimates leave coupled radial and angular oscillations at critical scale, including noncompact negative parts. Such behavior is possible for admissible smooth functions, but no uniformly negative triple has been certified. The periodic theorem leaves arbitrary relative axes, nonuniform common drift, changing angular spectra, and independent noncyclic triples. Neither a universal nonnegative full-torus median average nor the unrestricted some-phase assertion follows.

The general problem also includes discontinuous subharmonic representatives, arbitrary multiscale coupling, noncompact or infinite Riesz mass, and nonpolynomial harmonic contributions. The partial affirmative classes do not exhaust these possibilities.

## Full proofs and exact verification

All prior public mathematical files are included once, unchanged, in the [two-pass baseline](baseline/two_pass/README.md), accompanied by the unchanged [independent acceptance supplement](baseline/review/reader_edition_acceptance.md). The new analytic proofs and both new full audits are linked above. The [reproduction guide](REPRODUCTION.md) explains the finite certificates and their limitations; the [validation report](VALIDATION.md) records independent reconstruction and falsification coverage. The [public manifest](MANIFEST.json) binds only included public files and public baseline manifests.
