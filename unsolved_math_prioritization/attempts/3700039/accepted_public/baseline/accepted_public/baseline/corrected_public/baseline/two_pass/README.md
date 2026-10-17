# Median inequality for three subharmonic functions

## Result and scope

**The unrestricted normalized-supremum conjecture remains unresolved.** This reader edition records exactly the first two documented substantive passes on problem 3700039 (row 1762, AMR-036-0039). It establishes partial affirmative classes, exact diagnostics that rule out false reformulations, and precise obstacles to two proof strategies. It supplies no genuine counterexample and makes no claim of historical novelty. The lifetime number of earlier substantive attempts is unknown.

The source is A. Eremenko, [Conjectured inequality for subharmonic functions](https://www.math.purdue.edu/~eremenko/dvi/subh1.pdf), dated 4 April 2015. The homogeneous and harmonic affirmative cases are credited prior cases in that note. On 13 October 2026 the author's [problem index](https://www.math.purdue.edu/~eremenko/uns1.html) continued to link the note without a resolution annotation. That observation is not a proof of worldwide openness.

## The exact question and denominator convention

For three whole-plane subharmonic functions with u_j(0)=0, let v_2 be their pointwise median and set

I(r)=integral_0^(2*pi) v_2(r exp(i theta)) dtheta,

B(r)=max_(j,theta) u_j(r exp(i theta)).

All angular integrals and L1 norms in this edition use dtheta, without normalization by 2*pi, unless explicitly labeled as an angular mean. The target is sup I(r)/B(r)>=0.

The source leaves zero denominators unspecified. Here a nonzero triple is tested only on D={r>0:B(r)>0}; the globally zero triple is treated separately as zero equality. The first-pass theorem proves D=(R_0,infinity), with R_0>=0, and B=0 exactly on joint zero disks. Assigning numerical value zero to every 0/0 quotient is a weaker convention on nontrivial flat-disk triples; equivalence has not been proved.

Thus a genuine counterexample under this convention must supply one epsilon>0 such that I(r)/B(r)<=-epsilon for every r in D. Negative integrals at isolated radii, negative phases, or even a strictly negative integral at every finite radius do not suffice. Nor does failure of the source's stronger small-radius statement refute the supremum target. The general problem has no power-growth restriction.

## What changed in the first pass

The [theory report](proofs/first_pass_theory.md) proves the denominator classification, the sharp fixed-radius range -pi<=I/B<=2*pi, and an explicit degree-9999 harmonic witness with I(1)/B(1)<-0.99*pi. It also computes an entire harmonic triple with I(r)<0 at every r but sup I/B=0, not attained. Finally, the credited homogeneous argument settles triples with a nonzero finite joint Taylor term. A smooth counterexample would consequently have to be flat at zero.

The [construction report](proofs/first_pass_constructions.md) gives nonnegative median integrals for common [logarithmic spirals](proofs/common_spiral.md) and the broader [common rotating-separable class](proofs/rotating_separable.md). [Compact positive logarithmic potentials with polynomial harmonic parts](proofs/compact_potential.md) also satisfy the supremum assertion. The [log-periodic reduction](proofs/log_periodic_reduction.md) identifies an exact sufficient counterexample certificate: an admissible doubly periodic profile with negative median integral at every phase.

The first pass is independently accepted in the [theory audit](audits/first_theory_acceptance.md) and [construction audit](audits/first_construction_acceptance.md). The rotating-separable proof now explicitly uses positive angular mollification before choosing a radius. Its [original mathematical text](changes/rotating_separable.original.md), [clarified text](changes/rotating_separable.clarified.md), and [reversible mathematical patch](changes/angular_mollification.patch) are included.

## What changed in the second pass

The [flat-scale report](proofs/second_pass_flat_scale.md) proves the positive-smoothing estimate

I(exp t)/b(t)>=-2*pi*K_N*A(t)/b(t)-E_N(t),

where b(t)=B(exp t), A(t)=integral_(-infinity)^t (t-s)b(s) ds, K_N=N(N+1)(N+2)/6, and E_N is the sum of the three relative L1 Fejer errors. It settles continuous infinitely flat origins and flat-disk boundaries when the normalized angular profiles are relatively compact in L1. Finite angular bandwidth suffices. Explicit smooth admissible examples prove that this compactness is extra. Another example has exactly B(r)=r^2 but no homogeneous or common rotating-separable normalized dilation limit.

The [periodic-phase report](proofs/second_pass_periodic.md) settles profiles with a common sign-reversing angular shift and gives a high-phase-frequency exclusion for each fixed nonzero nonnegative finite Fourier forcing. It supplies an exact mixed-sign example with M(0)/(2*pi)<-1/3 and M(pi)/(2*pi)>1. This example satisfies the supremum assertion. Its finite-point obstruction proves that no fixed positive weighted sum of finitely many torus point evaluations can be nonnegative on the whole periodic L-subharmonic cone; it obstructs that method, not the conjecture.

Second-pass mathematical acceptance is recorded separately in [the flat-scale audit](audits/second_flat_scale_acceptance.md) and [the periodic-phase audit](audits/second_periodic_acceptance.md). These audits are verification of the second pass, not additional substantive passes.

## Exact unresolved frontier

For arbitrary continuous flat triples, the estimates do not control angular frequencies escaping at the same scales as the normalizing maximum changes rapidly. A uniformly negative counterexample must violate the stated relative angular compactness. The examples establish that such compactness failure is possible, but their medians are positive.

For the periodic class, it remains to prove the existence of a phase with M(s)>=0, or to certify M(s)<0 for every phase. The fixed-forcing high-frequency threshold is not uniform over forcings; it does not settle intermediate frequencies or forcings varying with frequency. Common sign reversal does not cover general mixed angular spectra. The finite-point obstruction leaves averaging, profile-dependent pairings and global arguments open.

The full problem also permits discontinuous subharmonic representatives, unrestricted multiscale coupling, noncompact or infinite Riesz mass, and nonpolynomial harmonic contributions. The partial theorems do not exhaust those possibilities.

## Proofs and finite certificates

The linked reports contain the full authored analytic proofs. [Reproduction conventions](REPRODUCTION.md) explain all finite arrays, rational bounds, angular normalizations and independent negative controls. Principal certificates are the [first-pass exact calculations](certificates/first_pass_exact.json), [flat-scale constants](certificates/flat_scale_exact.json), [mixed-sign Fourier certificate](certificates/log_periodic_exact.json), and [independent finite checks](certificates/independent_finite_checks.json). These are authored mathematical data, not third-party datasets. Finite checks authenticate the indicated calculations, not the unresolved analytic target.
