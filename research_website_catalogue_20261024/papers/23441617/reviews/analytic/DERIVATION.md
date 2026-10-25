# Direct universal proof and independent boundary controls

The first reconstruction is sealed in INITIAL_ANALYTIC_LEDGER.md. This expanded account concerns the literal all-curve theorem in the actual deposited manuscript; it does not use the archived indirect condenser argument.

## Pointwise finite-energy majorization

Assume a finite-energy Borel density rho admissible for all E-to-F connectors, where E is nonempty compact in [0,1] and F=R\E. On Q=[−2,3]×[−2,2] let h=rho². For k≥0 choose relatively open Ok containing {h>2^k} with excess area at most 2^(−2k−4). Set H=1+sum 2^(k+1)1_Ok and g=sqrt(H). Indicators of open sets are lower semicontinuous; increasing sums and the square root preserve this property. The dyadic sum over {h>2^k} is at most 4h. The constant covers h≤1; for h>1 the same geometric sum majorizes h, including dyadic equality cases, and infinity is retained pointwise. Thus

    g≥max(1,rho),   integral_Q g² ≤20+4 integral_Q rho²+1/4 < infinity.

This is a pointwise construction. Infinity on a null set is not discarded. Dense null spikes are compatible with integrable lsc majorants because the open supersets may be dense and have tiny area.

## Actual weighted distance, measurability and all-path control

Let d(z) be the infimum of g-costs of globally rectifiable paths in Q from E to z; constant paths are permitted and d may be infinite. Set u=min(1,d). For a continuous nonnegative weight, weighted length is the supremum over partition sums of minimum weight on each subcurve times its endpoint chord length. Fine partitions control weight oscillation and refinement approximates variation. Every such finite partition sum is continuous under uniform convergence of curves. This proves lower semicontinuity of weighted length, including multiplicity.

The lsc weight g is an increasing pointwise limit of the continuous functions min(m,inf_y(g(y)+m|x−y|)). Compactness and lower semicontinuity prove convergence even at infinite g-values. Monotone convergence therefore extends weighted-length lower semicontinuity to g.

For endpoints zj→z with liminf d(zj)<infinity, choose near-minimal paths on a bounded-cost subsequence. Since g≥1 their Euclidean lengths are bounded. Constant-speed parametrization gives a common Lipschitz constant. Arzelà–Ascoli in compact Q produces a rectifiable limit starting in compact E and ending at z, with cost no greater than the liminf. Thus d,u are lsc and Borel. No existence of a minimizer for every endpoint is assumed.

Concatenation and reversal yield |u(x)−u(y)|≤integral_beta g on every rectifiable path beta in Q. Infinite distances cause no exception: a finite-cost connection from a finite-distance point would force the other distance finite; two infinite distances give two truncated values equal to one. Almost every coordinate line has integrable g. The inequality on every subsegment proves absolute continuity of the actual restriction of u on that line. Derivatives satisfy |partial_i u|≤g. Slice integration by parts gives the weak derivatives, and |grad u|²≤2g². Hence u∈W^(1,2)(int Q).

Every globally rectifiable auxiliary path from E to a point of F∩Q belongs to the original connector family, regardless of interior plate contacts. Its cost is at least one. Constant paths at E cost zero even when g is infinite there. Therefore actual u is zero on E and one on F∩Q. Take eta smooth, supported in int Q, equal to one near [0,1] on the axis, and extend w=eta(1−u) by zero. It has compact support in W^(1,2)(R²), and its actual vertical ACL trace equals 1_E almost everywhere in x. This only discards a length-null set of vertical lines. It does not declare the exceptional subset of E capacity-null.

## Critical trace and rigidity, with no capacity shortcut

For smooth compactly supported w, take the unitary horizontal Fourier transform W(xi,y). Integrating the derivative of |W|² on y>0 and applying 2ab≤a²+b² gives

    |xi| |W(xi,0)|² ≤ integral_0^infinity (xi²|W|²+|partial_y W|²) dy.

At xi=0 there is no division and the inequality is harmless. Integrate in frequency using Plancherel. To pass from smooth wj to w, the vertical ACL inequality

    |v(x,0)|² ≤ integral_0^infinity (|v|²+|partial_y v|²) dy

shows that actual traces converge in L² for v=wj−w. Subsequential almost-everywhere convergence of their Fourier transforms and Fatou preserve the weighted Fourier bound. Plancherel and Tonelli then give

    integral_R ||f(.+h)−f||²_2 dh/h²
      = C integral_R |xi| |fhat(xi)|² dxi < infinity,

where C=integral_R |exp(it)−1|² dt/t² is finite and positive. This establishes the exact special case required; classical trace references are credited context.

For f=1_E, let N=ceil(2/h)≤3/h for 0<h<1. Since Nh≥2, f and its Nh-translate have disjoint supports. Telescoping in L¹ gives 2|E|≤N||f(.+h)−f||_1. The latter norm equals the squared L² norm for characteristic functions. Consequently ||f(.+h)−f||²_2≥(2/3)|E|h. Its h^−2 integral diverges logarithmically if |E|>0. Thus E has length zero. This is valid for measurable bounded E, including positive-length sets without intervals. It provides no zero-capacity conclusion for null E.

## Null sets: retain every actual endpoint and every curve

Set q=rho+1_B(0,3). It is Borel, finite in L², and admissible for E→F. Fix an arbitrary e∈E and suppose an arbitrary e-to-S2 connector has finite q-cost. Stop it at its first hit of S2. Before that time its image lies in B2, where q≥1. All interior subcurve lengths are bounded by its cost; continuity and endpoint limits extend this to finite total variation of the stopped curve. Thus the stopped curve is globally rectifiable, including its endpoints. After removing constant portions it has an arclength parametrization with integrable q-composition and final distance at least one from e. This argument handles a curve originally allowed to have infinite endpoint length; such a curve cannot have finite q-cost after localization.

For this fixed e, let Ae(r)=integral_circle(e,r) q² ds. Polar integration gives integral_0^delta Ae(r) dr<infinity. Because E has length zero, e+r∈F for almost every r. Among those full-measure good radii there are arbitrarily small r with rAe(r) arbitrarily small; otherwise Ae(r)≥epsilon/r almost everywhere near zero, contradicting its integral. Choose rj decreasing to zero with e+rj∈F and rj Ae(rj)→0. The selection is made for each e, so no endpoint is discarded and no uniform radii across uncountably many e are required.

Let tj be the first arclength exit at radius rj. It exists, and tends to zero: every positive initial arclength interval is nonconstant, hence contains a point a positive distance from e. For sufficiently small radii the first exit occurs before that time. The initial q-cost tends to zero by absolute continuity of the finite cost integral. Join the exit point along a circle centered at e to the real point e+rj. Its q-cost is at most sqrt(2*pi*rj*Ae(rj)), which tends to zero. The concatenation is an actual globally rectifiable connector from E to the original real complement F. Plate contacts inside it are allowed. Its eventual cost below one contradicts admissibility.

Every connector to S2 therefore has infinite q-cost. The densities q/n are admissible for all such curves and their squared energies tend to zero. Hence Mod(E,S2)=0 whenever Mod(E,F)<infinity. No extremal density is required: a finite infimum guarantees some finite-energy admissible density. Empty E gives an empty family of modulus zero. The contrapositive proves the complete stated theorem under either consistent connector convention.

## Independent exact controls and what they establish

For E=[0,1], vertical connectors to the upper semicircle yield Mod(E,S2)≥integral_0^1 dx/sqrt(4−x²)=pi/6. A unit density on 1<|z|<2 is admissible for every connector and has energy3*pi, so the antecedent is genuinely positive and finite. Upper semicircles of radius r<1 join r∈E to −r∈F. Cauchy–Schwarz gives semicircle energy at least 1/(pi*r); integrating over r forces infinite separator energy independently of the full proof.

For f=1_[0,1], the critical translation seminorm truncated at |h|≥epsilon is exactly 4log(1/epsilon)+4. At fractional order s=1/4 the full seminorm is16. This detects that replacing the critical trace with a subcritical one would fail. A logarithmic point singularity rho=1/(r log(1/r)) on 0<r<exp(−1) has squared area integral2*pi and infinite radial cost on every escaping curve; scaling proves the singleton's zero modulus. Infinity at the endpoint alone would not do so: a density infinite only on the real axis has zero cost along an upper semicircle except at its zero-length endpoints and is not admissible.

An integrable model circle energy Ae(r)=1/r on disjoint annuli [2^−j,2^−j(1+2^−j)], zero elsewhere, has total radial integral at most sum2^−j=1. Yet rAe(r)=1 on arbitrarily small spikes and zero along gap radii. Thus only a liminf-zero subsequence follows; a full-limit replacement is false. The spiral t exp(i/t) has speed squared1+t^−2 and infinite endpoint length. q≥1 excludes a finite-cost counterexample of this type. These exact controls test failure modes; they do not replace the preceding all-set, all-curve proof.
