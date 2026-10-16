# Independent geometric, dynamical, and domain audit — PR 256 / k307

Authenticated submitted head: `9445a90b57f76493bd901edc544b09dec393e20f` (parent-supplied). Target: `submitted/unsolved_math_prioritization/attempts/5100017/PROOF.md`. This audit was produced without reading prior independent-review conclusions and without importing the submitted checker. All work in this folder is newly created. No Git, provider, or external-individual communication was used.

Current finding: **no substantive geometric/domain counterexample found** to the submitted theorem under its explicit strict confocal elliptic, least-even-period, signed-quotient domain. The star undefined-circle qualification is mathematically necessary. One small missing converse in the originally submitted four-period discussion was identified and has been repaired in `candidate_repair_01/PROOF.md:99`; that new paragraph has been read directly and verified below. The complete independent all-real Cartesian moment proof is in `ALL_REAL_CARTESIAN_PROOF.md`. Finite reflection computations support, but do not replace, these all-period deductions.

## Target definition and source agreement

The source's k307 is the area centroid of the pedal to the outer polygon. It is different from k306, the arithmetic vertex centroid. The outer polygon sides are the lines tangent to the billiard ellipse at the trajectory vertices. Thus the Cartesian projection used independently here is

`Q_i = M + (1 - (P_ix/a^2,P_iy/b^2) dot M) * (P_ix/a^2,P_iy/b^2) / |(P_ix/a^2,P_iy/b^2)|^2`.

The source defines signed area by the ordered shoelace sum and the centroid by the signed first moment divided by six times that signed area. This quotient is undefined when signed area vanishes, including for a self-intersecting pedal. The signed convention, trajectory order, and tangent-line projection in the candidate agree with that definition.

Primary reads: [arXiv 2004.12497v11](https://arxiv.org/pdf/2004.12497v11), p.3 definitions and p.6 Table 4 / §3.4; [final journal PDF](https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf), printed p.346 Table 4 / §3.4, with signed area on p.343. Both identify even N and arbitrary fixed M for k307. The introduction specifies two confocal ellipses. Neither table explicitly handles zero signed area. The candidate's all-M conclusion for simple families and its defined-domain conclusion for stars must retain this distinction; the table alone should not be read as a defined quotient at a zero denominator.

## Full-domain geometry, independently reconstructed

Write the boundary as `P(u)=(a cos u,b sin u)`. If the next vertex is `P(u+2q)`, a chord tangent to the strict elliptic caustic satisfies

`sin^2 q = lambda*(cos^2(u+q)/a^2 + sin^2(u+q)/b^2)`.

With `r=tan q`, this is a quadratic with coefficient

`A(u)=1-lambda*(sin^2 u/a^2+cos^2 u/b^2)>0`,

linear coefficient `-2 lambda sin u cos u*(1/b^2-1/a^2)`, and strictly negative constant `-lambda*(cos^2 u/a^2+sin^2 u/b^2)`. It has exactly one positive root, giving exactly one `q` in `(0,pi/2)`. The root depends continuously on u and lambda. The other tangent provides the inverse map. Consequently the selected Poncelet map T is a circle homeomorphism; continuous deformation to the identity as lambda decreases to zero shows that it preserves orientation. The coefficients are pi-periodic, so T commutes with the half-turn R. This justifies the circle-map properties used in the candidate without a Jacobi parameterization.

For a least-period N poristic family, `T^N=id` and T has order N. Since T and R commute, the group they generate is finite. A nonidentity finite-order orientation-preserving circle homeomorphism has no fixed point: if it fixes x, cut the circle at x and use that a strictly increasing finite-order interval homeomorphism fixes every point. Hence the finite group acts freely on each of its point orbits. On such a finite cyclically ordered orbit, every orientation-preserving permutation is a cyclic shift; the action is faithful, so the group is cyclic. When N is even, `T^(N/2)` and R are involutions of this same cyclic group and must coincide. Thus opposite trajectory indices really are antipodes for stars as well as simple polygons. No supposition that a star is simple enters the argument.

Orient each chord with its caustic on the left. Since the caustic contains O strictly, `det(P_i,P_(i+1))>0`. Its radial arguments therefore advance by less than pi. The radial parametrization and the outward Gauss map are increasing circle homeomorphisms commuting with half-turn, so the boundary parameter and outward normal increments also lie in `(0,pi)`. This proves that adjacent outer tangent lines are not parallel and that every summand `h_i h_(i+1) sin Delta_i` is positive. In particular `S(0)>0` even for stars. This statement concerns the ordered signed sum and does not assume simplicity.

The submitted normal identity (5) is a direct conversion of the displayed tangency equation. The factors `F+ed=a^2-lambda*(a^2/b^2-1)>b^2` and `F-ed=b^2+lambda*(1-b^2/a^2)>0` exclude every claimed hidden denominator zero in the strict domain. Squaring (5) is used only as a forward implication to the unit-circle relation; it is not used to reconstruct billiards or to choose a square-root branch.

Antipodal pairing in the projection formula cancels all area terms linear in M and the even-degree first-moment terms. With `Z_i=n_i^2` and `w_i=h_i n_i`, projection is `Q_i=z/2+w_i-(bar z/2)Z_i`. The ordered area relation `S(0)=F S_Z/(2d)` for d nonzero follows by telescoping the sine of twice successive normal angles. The resulting area is `S(M)=S(0)*(2F+d|M|^2)/(2F)`. Because S(0) and F are positive, this gives the complete exceptional locus: none for d>=0, and exactly `|M|^2=-2F/d` for d<0. This deduction holds for every phase and every least even N.

The centroid reduction never needs a simple doubled-normal polygon. Its unit-circle first-moment relation is a polynomial identity, valid even if an edge is a diameter or vertices repeat; no division by `Z_i+Z_(i+1)` is needed. For d nonzero, positivity of S(0) proves S_Z nonzero. The independent Cartesian proof expands direct projections and explicitly expresses every surviving linear/cubic coefficient as a doubled-circle cyclic term plus a telescoping single-normal potential. It thereby verifies the whole general moment reduction for arbitrary real admissible normals, not just sampled billiards. Its exact polynomial certificate also checks the squared-support identity, the no-division circle edge identities, the zero constant/quadratic coefficients, and the final centroid quotient assembly.

## Four-period converse: small repair requested

`PROOF.md:99` establishes d=0 implies least period four. At `PROOF.md:252`, the statement that the N=4 case has already been treated implicitly needs the converse as well. Here is the missing argument.

If N=4, antipodal pairing gives `n_2=-n_0`, `h_2=h_0`. Apply (5) to pairs `(n_0,n_1)` and `(n_1,n_2)`. The left sides both equal `d h_0 h_1`. The right sides are negatives of each other: the second normal difference is pi minus the first, and its normal sum is the first sum plus pi. Adding gives `2 d h_0 h_1=0`, hence d=0. Equation (5) now forces every adjacent pair of normals to be orthogonal, so the outer polygon is a rectangle. Direct Cartesian shoelace gives area `2AB` and centroid `M/3` in its side frame. Rotation of the frame preserves the conclusion.

Direct repair check: the newly inserted paragraph at `candidate_repair_01/PROOF.md:99` uses exactly the preceding two-edge argument. Its sign changes, positive support numbers, and conclusion are correct, and it closes the identified converse gap. This was an exposition gap, not a counterexample or an unsupported research mechanism. It also repairs the all-M statement for every simple even family: for N>=6, the half-orbit normals of a winding-one polygon advance through one half-turn in circular order, so their squares form a convex polygon with at least three distinct vertices. The full doubled-normal polygon traverses it twice, giving S_Z>0 and d>0; N=4 gives d=0 by the preceding argument.

## Exact star and genuine undefined centroid

`exact_star_audit.py` starts at `(0,b)` and constructs a tangent to the inner ellipse with slope `sqrt(lambda)`, then propagates using actual ray intersection and specular reflection. It regenerates the proposed normalized vertex list without taking it as an input. Exact unit incoming/outgoing reflection, tangency, eight distinct vertices, antipodes, and winding three are all checked.

For `a^2=221/96`, `b^2=27625/20736`, `lambda=125/96`, its direct Cartesian projection and shoelace expansion give

`S(X,Y)=-sqrt(30)*(20736 X^2+20736 Y^2-123539)/134784`,

`T_x(X,Y)=-sqrt(30)*X*(41472 X^2+41472 Y^2-272935)/109512`,

`T_y(X,Y)=-sqrt(30)*Y*(52992 X^2+52992 Y^2-347633)/97344`,

where T is the unnormalized signed first moment. The exact constants are `d=-120/221`, `F=2795/1728`, `v=7/13`. The exceptional radius squared is `123539/20736`.

At `M=(sqrt(123539)/144,0)=(13 sqrt(731)/144,0)`, area is zero while the first moment is `(221 sqrt(21930)/10368,0)`, which is nonzero. Therefore the quotient is genuinely undefined there, and no finite removable centroid can be silently substituted. This is an exact counterexample to an unqualified defined-point claim that includes this star, while agreeing with the submitted domain-qualified theorem.

## Independent reproducible numerical evidence

`geometric_audit.py` uses an explicit tangent point on the inner ellipse only to initialize direction. Every subsequent step is an outer ray intersection followed by the physical reflection law. The caustic parameter is found from the accumulated boundary-angle closure defect. Each phase is generated afresh. No submitted verification module or Jacobi sampling formula is used.

For each phase, affine Cartesian projection polynomials are multiplied directly in a small monomial dictionary. This extracts every area coefficient through degree two and every first-moment coefficient through degree three. In addition to their claimed values, it checks all absent constant, cross-linear, and quadratic coefficients. It separately evaluates direct shoelace centroids at zero, rational points, points several ellipse radii away, very large M, and (when d<0) on and within 1e-12 relative radius of the exceptional circle. It also checks physical tangency/reflection, closure, winding, least period, antipodes, positive S(0), normal increments, orientation reversal, scale covariance, and phase independence.

Initial completed run: 15 families x 4 phases at 80 decimal digits, periods 4–40, winding 1/3/5, aspect ratios 1.0001–100. Full results are in `BASE_NUMERICAL_RESULTS.json`. Maximum normalized centroid residual was `6.06e-55`; phase difference `5.24e-55`; polynomial coefficient residual `1.24e-66`. Final completed run in `NUMERICAL_RESULTS.json`: 21 families x 4 phases at 110 decimal digits; N up to 200, aspect ratio up to 1,000,000, d approximately +2e-6 and -1e-6, and b^2-lambda approximately 6.25e-20. It checked 2,488 actual reflected edges, 2,184 full polynomial area/moment coefficients, 500 defined centroids, 375 phase comparisons, and 40 exceptional-circle controls. Maximum normalized centroid residual was 9.74e-73 and phase difference 8.34e-73. Increasing precision resolved conditioning in the new extreme-aspect controls; no formula or geometric falsifier survived.

A spurious four-period circle was initially produced by allowing a closure approximation with d about -1e-74 to select the star regime, giving a fictitious radius about 1e37 and amplifying its tiny closure error. The diagnostic now distinguishes exact d=0 from genuinely negative star d. The original erroneous branch and exact observed residual 0.439024390243902439 are preserved and reproduced by `reproduce_spurious_n4_diagnostic.py` and `SPURIOUS_N4_DIAGNOSTIC.json`: d=-4.6511234853e-74, fictitious radius 8.1066353371e36, while direct area remains 3.6. This records a numerical conditioning issue and does not supply a theorem counterexample.

## Remaining gap and disposition

The strongest independently established result here is a complete all-real, all-least-even-period derivation of the geometric pairing, positive origin-pedal area, explicit area and first-moment formula, exact exceptional domain, and phase-independent quotient under the stated strict elliptic assumptions. Its general Cartesian coefficient identities have explicit telescoping witnesses and a separately written proof. The candidate-repair four-period converse is directly verified. The exact reflected 8/3 star supplies a checkable genuine undefined-point example. Finite numerical evidence remains corroboration, not the proof. No remaining correctness gap was found in this geometric/domain approach after the small repair; source-wide priority and final PR disposition remain outside this subaudit.

Keep the strict elliptic caustic, least-even-period, signed-area, and nonzero-area qualifications in any promoted result. A literal defined centroid for arbitrary M in all stars is false. No claim about hyperbolic/degenerate caustics or padded odd orbits follows from this audit. No novelty or publication-priority conclusion is made.
