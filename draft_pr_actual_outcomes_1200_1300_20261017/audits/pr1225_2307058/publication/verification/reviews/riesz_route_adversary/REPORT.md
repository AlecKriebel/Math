# Independent adversarial verification of the frozen Riesz route

**Verdict: PASS for the stated mathematical implication and curve conventions.** No repair is required. This verdict concerns mathematical validity of this frozen reconstruction, not novelty, priority, present-day problem status, external human review, or formal certification.

## Scope and success criterion

The input is the complete `source_question_family/DERIVATION.md`, frozen before this review. The claim is: for compact E contained in the real interval [0,1], positive planar arclength 2-modulus of the family from E to the circle of radius 2 implies infinite 2-modulus of the family from E to the real complement of E. Densities are nonnegative extended-valued Borel functions, with their actual pointwise values used in curve integrals. Both globally rectifiable curves and curves locally rectifiable in the open parameter interval with endpoint limits are covered, as are strong and modulus-almost-everywhere admissibility.

Success means a complete analytic implication with no unsupported capacity equivalence, exceptional-point replacement, or transfer to an equally difficult unproved assertion. I independently checked every mathematical step and the constants in (6), (9), and (10). I did not use the separately evaluated small-circle proof or read any other review or priority-family body.

The exact source question was checked in [Hayman–Lingham, arXiv:1809.07200v2, Problem 7.58](https://arxiv.org/html/1809.07200v2), line 5002 in the returned HTML, and against the family's saved text of PDF page 179, printed page 178. It agrees with the claim just stated. The historical update supplies no evidence about present status.

## Authentication

The parent supplied the first three anchor hashes below. They all match, and every file enumerated by `MANIFEST.json` also matches both its SHA-256 and recorded byte count.

| Input relative to `../source_question_family/` | Bytes | SHA-256 |
|---|---:|---|
| `MANIFEST.json` | — | `3767e6d810fdaf17d33235bbc12c642cc28f94741a9ca3a74ad7f87032403ea2` |
| `DERIVATION.md` | 11792 | `7e96ef42b0b45f250b087dbbef06d4d975af62d2aa7e035728a8d381b0da543d` |
| `REPORT.md` | 3947 | `cd0ebff0da2a276e7eb0ab91ee3e5a8c5d6815754a3af5fd9a0b02b2462c0dab` |
| `.gitignore` | 15 | `9520c0d9e31acd48934658a5daacf553854f446f1869c8efa4cc5904332f7401` |
| `RESEARCH_LOG.md` | 4864 | `2f22ea324b674e5978eef29a5c6ada15805c494e6d839ac2c7ef965b8ea447f5` |
| `SOURCES.md` | 2094 | `f5271cc28385bece4e0df85fad1922897f822c2917bc72bfaff9998154d6b5ea` |

Additional evidence hashes:

- Project `AGENTS.md`: `b01836a23a64025ea4c7c383f018346b3a0f3fa1a1e812c613e931be1f0ff71d`.
- Family `MANIFEST.sha256`: `76c9679994b1a0f5246f3687bbcfd2cfde0da79f110417fab16deb95d28c1d2a`; its content correctly names the manifest anchor.
- Family saved original PDF: `8e28fd4403a07e4e19a9816b7efaafddf9f475d59cf8c34a8255cb03833ed4f0`; only hashed in this review, not opened or rendered.
- Family saved `source_bodies/problem_7_58_page179.txt`: `160a22a42a7ed37d0cdfb64b03eaff4a6ae1d2d6cf0c1b2d4756c626604a3fd1`; inspected, including incidental neighboring text.

The supplied manifest intentionally excludes downloaded source bodies. Their hashes above record the separate source evidence inspected or hashed by this review and do not expand that manifest's scope.

## 1. Pointwise majorization, including all integer scales

Reference: derivation lines 21–31. Write q = rho times the indicator of the fixed bounded square, with the zero extension understood literally. For every a in (0,infinity),

    a <= sum_{k in Z} 2^k 1_{a > 2^k} <= 2a.

At a dyadic equality the sum equals a, so the strict level-set inequality causes no loss. At a=0 the sum is zero; at a=infinity it is infinity. The negative tail is a convergent geometric series, so using every integer k is legitimate.

Each level set A_k has finite area, because it lies in the fixed square. Outer regularity gives open U_k containing A_k with arbitrarily small excess area. Choose positive tolerances so that the sum of 2^k times their square roots is finite; no nestedness is required. Since

    1_{U_k} = 1_{A_k} + 1_{U_k minus A_k},

the dyadic bound and Minkowski's inequality for nonnegative partial sums give the claimed L2 bound. Monotone convergence finishes the countable sum. Indicators of open sets are lower semicontinuous; the supremum of their finite nonnegative partial sums is lower semicontinuous too. Adding the indicator of a bounded open square containing D gives g at least one on D and finite L2 norm.

This is a pointwise construction. In particular a value infinity on an area-null set is retained, even if the set is dense. No curve integral is justified by replacing a density merely almost everywhere.

## 2. The noncompact starting plate and weighted distance

Reference: lines 35–52. Auxiliary paths in the definition of d include constant paths. A constant path has zero arclength and zero integral even where g is infinity. These auxiliary paths are not the nonconstant connecting family used in the modulus. This standard path convention gives d=0 on F_D immediately.

Every nonconstant path from F_D to E reverses to an admissibility test curve, so its g-length is at least one. Thus u=1 on E. Concatenating an almost-minimizing path with a prescribed path sigma gives

    d(w) <= d(z) + integral_sigma g

whenever the right side is finite. Reversing sigma and truncating by min(1,d) gives the asserted absolute difference bound, including when one or both distances are infinite. There is no subtraction of two infinities.

Here are details behind the measurability claim. For compact K contained in D, let S_a(K) be the set of endpoints reachable from K by a path of g-length at most a, for finite a>=0. Every such path has Euclidean length at most a because g>=1. Parametrize on [0,1] at constant Euclidean speed, allowing zero speed. All such parametrizations are a-Lipschitz, have images in compact D, and start in K. Arzela–Ascoli supplies a uniformly converging subsequence in every endpoint sequence.

Weighted length is lower semicontinuous under this convergence. One elementary proof is the following. For a continuous nonnegative weight b on D, its weighted length equals the supremum over finite partitions of

    sum_i (inf_{t in [t_(i-1),t_i]} b(gamma(t)))
          * |gamma(t_i)-gamma(t_(i-1))|.

The inequality from right to left is immediate. Equality follows by uniform continuity of b along the curve and approximation of length by sufficiently fine chord sums; further refinement never decreases a sum. Every fixed-partition expression is continuous for uniform curve convergence. The supremum is therefore lower semicontinuous. Increasing continuous nonnegative approximations b_m to the extended lower-semicontinuous g, followed by monotone convergence against arclength, give the same property for g. The limiting path remains admissible for S_a(K), proving this set is compact. The same compactness proves attainment whenever the distance from K is finite, by starting with paths of cost at most a+1 and letting their costs decrease.

The compact sets K_j in the frozen derivation exhaust F_D: a point outside the closed E has positive distance from E. Consequently

    {d<a} = union_{j>=1, rational 0<=q<a} S_q(K_j)

for a>0; for a<=0 it is empty. This is Borel. There is no assumption that the starting plate itself is compact, nor an uncountable projection measurability shortcut.

## 3. The actual ACL trace and the critical rigidity step

Reference: lines 52–79. On almost every vertical or horizontal line, g is integrable on its D-segment by Fubini. The endpoint inequality bounds every increment of u on that segment by the integral of g between the endpoints. Absolute continuity of the latter integral proves absolute continuity of the actual function u on the segment, with each coordinate derivative bounded by g almost everywhere. Borel measurability, boundedness, and the ACL characterization now give u in W^(1,2)(interior D), with squared gradient bounded by 2g^2. The factor two is harmless and the frozen text does not claim the stronger bound on the full gradient.

Choose the smooth cutoff eta with compact support inside D and eta=1 near E. Its zero-extended product v belongs to W^(1,2)(R2). On the real line, the actual pointwise product is 1_E, since u=0 at every point of F_D and u=1 at every point of E. To verify that this actual value is also the Sobolev trace, use the already established vertical ACL property. For an absolutely continuous slice a on [0,1],

    |a(0)|^2 <= 2 integral_0^1 (|a(y)|^2 + |a'(y)|^2) dy.

It follows by writing a(0)=a(y)-integral_0^y a' and then integrating y. After integrating the slice inequality in x, evaluation at zero is a bounded map from W^(1,2) to L2 of the line. Applied to smooth approximants and their differences, it shows that their traces converge to these actual ACL values in L2. Thus the trace identification does not rely on choosing pointwise representatives on E after the fact.

For a smooth approximant, let a(y)=v-hat(xi,y). Integration of minus the derivative of |a|^2 gives

    |xi| |a(0)|^2 <= integral_0^infinity (|a'|^2 + xi^2 |a|^2) dy.

The assertion at xi=0 is trivial. Integrate xi using Plancherel. The bounded trace map just proved and approximation give finite integral of |xi| times the squared Fourier transform of the actual trace. Plancherel for translations, and Tonelli, then give the finite double integral in (4). More explicitly, the inner translation integral is

    integral_R |exp(i xi h)-1|^2 / h^2 dh = 2 pi |xi|.

For a characteristic function, the squared L2 translation difference equals the L1 translation difference D(h). Finiteness of integral_0^1 D(h)/h^2 dh implies a sequence h_n decreasing to zero with D(h_n)/h_n tending to zero: a positive lower bound on that ratio for all sufficiently small h would force logarithmic divergence. For any smooth compactly supported psi,

    integral 1_E(t) psi'(t) dt
      = lim_n integral [1_E(t-h_n)-1_E(t)] psi(t)/h_n dt = 0.

The absolute value is bounded by the claimed sup-norm factor. Hence the distributional derivative is zero. Mollification, or the elementary zero-derivative theorem, makes 1_E constant almost everywhere; integrability and bounded support make the constant zero. This proves |E|=0 without identifying line length with capacity.

## 4. The local Riesz endpoint lemma

Reference: lines 83–113. The zero extension f=g1_O is lower semicontinuous: inside O this follows from g, and at a point outside O its value is zero and the liminf of nonnegative values is at least zero. Its support is contained in the closed radius-3/2 ball. Values on the boundary are defined as zero; no product infinity-times-zero is being used.

For the displayed infimum approximation f_n, the infimum term is n-Lipschitz, nonnegative, and no greater than f by taking w=z. Truncation at n preserves continuity. Both n and the coefficient n in the infimum increase, so the sequence increases. Its convergence to f follows from lower semicontinuity: if f(z)>a, some neighborhood of z has f>a, and for large n every w outside that neighborhood has n|z-w|>a while the cap n>a. Each f_n is zero off O and has compact support. This also handles f(z)=infinity.

For bounded compactly supported f_n, the potential v_n=|.|^(-1)*f_n is finite and continuous. The kernel is locally integrable, its near-origin contribution is uniformly small by boundedness of f_n, and translation continuity of the remaining truncated kernel proves continuity. Monotone convergence gives v_n increasing to I1 f. If I1 f is infinity at every point of compact E, the increasing open sets {v_n>2T} cover E for every T. A finite subcover and monotonicity supply a single n for the entire E. This is the exact uniformity needed for admissibility.

The low-frequency Fourier point deserves care: v_n itself is generally not globally L2. The frozen argument only needs its distributional gradient to be L2. With the stated transform convention,

    |x|^(-1) = (1/sqrt(pi)) integral_0^infinity t^(-1/2) exp(-t|x|^2) dt,
    Fourier[exp(-t|x|^2)](xi) = (pi/t) exp(-|xi|^2/(4t)).

Integration yields exactly 2pi/|xi| as a tempered distribution. The transform on the frequency side is locally integrable at zero in two dimensions. Convolution with the compactly supported integrable f_n is legitimate distributionally, and differentiation gives

    Fourier[partial_j v_n](xi) = 2pi i xi_j/|xi| * f_n-hat(xi).

The multiplier is bounded. Summing the two component Plancherel identities gives

    ||gradient v_n||_2^2 = (2pi)^2 ||f_n||_2^2.

There is no appeal to global L2 integrability of v_n, omission of a low-frequency divergent norm, or unexplained zero-frequency mass.

For x in the cutoff support inside the radius-2 ball and z in the support of f_n, |x-z|<7/2<4. Therefore v_n there equals convolution with the truncated kernel 1_{|.|<4}/|.|, whose L1 norm is 8pi. Young's inequality gives the local L2 estimate exactly as stated. Taking the usual smooth cutoff with values between zero and one, one may choose

    C = 2pi + 8pi ||gradient eta_0||_infinity

in the gradient bound for eta_0 v_n. This constant is independent of n and T.

The product is continuous, compactly supported strictly inside the radius-2 ball, and in W^(1,2). Convolution with a nonnegative unit-mass smooth mollifier uniformly approximates it and does not increase the gradient L2 norm. Choose the scale less than the support's positive distance to the complement of the ball and so small that the uniform error is less than T/2. Its value at every point of E is then greater than 3T/2. Compactness and continuity give a neighborhood of E on which the smoothed function is at least T. Dividing by T produces precisely the smooth test function in (8).

Its gradient is directly admissible: along an arclength parametrization of a rectifiable test curve, the integral of the gradient norm bounds the absolute change of the smooth function, which is at least one between E and the circle. For a locally rectifiable curve, apply this inequality on compact interior parameter intervals and pass to the endpoint limits. Thus the assumed infinite potential everywhere would make the original modulus zero. Positive original modulus supplies a genuine point x in E with finite local I1 f. No condenser equivalence is introduced at this step.

## 5. Exact short-polygon estimates

Reference: lines 117–145. Choose r sufficiently small that the two-segment polygon is in O. Since |E|=0, deleting E from the base interval changes neither its length 2r nor any nonnegative Lebesgue integral over the endpoint parameter. This statement remains true for extended-valued integrands.

For the first segment the average, using |Q_r|=2r^2, is at most

    (sqrt(2)/(2r)) integral f(w)
       [integral_{|w-x|/(sqrt(2)r)}^1 t^(-2) dt] dw,

with w restricted to the ball of radius sqrt(2)r. The Jacobian t^2 is correct, and the omitted geometric restriction w in x+t(Q_r-x) can only increase this nonnegative integral. The inner integral is at most sqrt(2)r/|w-x|. Multiplication leaves exactly 1/|w-x|. The value w=x is an area-null exception and both sides are interpreted by nonnegative integration. This proves (9) with coefficient one.

For the second segment, scale by r and put F(w)=r f(x+rw); then ||F|| on (-1,1) times (0,1) equals ||f|| on Q_r. At unit scale, the averaging normalization is 1/4 and the segment speed is at most sqrt(5). For each t in (0,1), the map

    (a,b) -> w=((1-t)y+ta,tb)

has determinant t^2. A point w=(u,v) can occur only when t>v, and the allowable y set has length

    L(u,t) = length((-1,1) intersect ((u-t)/(1-t),(u+t)/(1-t))).

It is at most 4t for t<=1/2 and at most 2 for t>=1/2. Hence the averaging kernel K is zero outside the unit rectangle and satisfies

    K(u,v) <= integral_v^1 L(u,t)/t^2 dt
           <= 4 log(1/v)+8,       0<v<1.

For v<1/2 the sharper bound is 4log(1/(2v))+2, and for v>=1/2 it is 2/v-2. Both imply the frozen upper bound. Its squared norm is exactly

    2 integral_0^1 (4 log(1/v)+8)^2 dv
      = 2 (16*2 + 64*1 + 64) = 320.

Cauchy–Schwarz yields (sqrt(5)/4)*sqrt(320)=10, which verifies (10), including its normalization. Parameter values t=0,1 carry no parameter measure, so no singular endpoint Jacobian is used. All transformations are Tonelli transformations of nonnegative Borel functions; exceptional infinite pointwise values are retained.

At the chosen finite-potential point, the local first-segment bound tends to zero by absolute continuity of the integrable function f(w)/|w-x|. The second bound tends to zero by absolute continuity of the integral of f^2. Their sum is the mean total polygonal cost. Once that mean is below one, some endpoint pair has cost below one. The resulting path is nonconstant, globally rectifiable, and has all interior points strictly above the real axis. Its terminal point is outside E. On this entire path f=g>=rho pointwise, so it contradicts rho-admissibility. Nothing is inferred solely from an almost-everywhere comparison.

## 6. Exceptional curves, endpoint conventions, and boundary cases

Reference: lines 147–155. If a nonnegative Borel density is admissible outside a family Gamma_0 of zero modulus, choose admissible h_j for that family with ||h_j||_2<=2^(-j). Minkowski and monotone convergence give h=sum h_j in L2, and curvewise Tonelli gives integral_gamma h=infinity for every gamma in Gamma_0. Thus rho+epsilon h is strongly admissible with finite energy. The strong impossibility proved above rules out finite weak admissible energy as well. The same repair also gives equality of weak and strong infima when needed, by letting epsilon tend to zero.

The proof applies separately to the globally and locally rectifiable conventions. In either case every auxiliary D-path and final polygon used for contradiction is a permitted globally rectifiable test curve; in the positive-modulus step, the smooth gradients are admissible for the entire corresponding original curve class. No equality of the two curve-family moduli is required. Endpoint values are never charged as atoms. Restricting the upper-half-plane polygon to any compact interior parameter interval and passing to endpoint limits is consistent with the specified local convention.

Empty E has zero original modulus and does not meet the hypothesis. A set with positive line length is eliminated by the trace argument, while a zero-length set with positive original modulus is handled by the finite-potential lemma. A singleton or a polar set is not erroneously declared to have positive original modulus. A finite-energy singular density can have infinite potential at a singleton; the original-modulus step correctly prevents applying the finite-point conclusion without its hypothesis. Infinite densities on area-null sets and dense null sets are allowed throughout.

The implicit inclusion of constant auxiliary distance paths is a standard definition rather than a missing mathematical lemma. It is distinct from allowing constant curves between disjoint plates, which is impossible and is not used. No change to the theorem, proof, or verdict is required for this clarification.

## Inspection ledger and outcome

- Fully inspected frozen derivation, report, sources ledger, research log, and manifest; the `.gitignore` and manifest sidecar were authenticated.
- Read the original arXiv HTML using read-only browsing. Automatic metadata and neighboring problem snippets appeared; none was used for the proof. Inspected only the saved original-question page text among source bodies; the original PDF was hashed only. The other background source bodies were not opened.
- A filename search exposed names of `analytic_adversary` and `submitted` files while locating the correct source-family directory. No contents were opened. No candidate, other review, or new priority-family analysis contributed to this verdict.
- Used analytic derivations, not numerical tests, to verify all estimates. No code/data output substitutes for the proof.
- No mathematical issue remains unresolved within the stated scope. The strongest verified result is the full original implication under all four combinations of the stated rectifiability and admissibility conventions. No novelty, priority, or present-status conclusion follows from this audit.
- Verification checkpoint: **100% complete** for this frozen-route adversarial check, as of the timestamp in `VERDICT.json`. The wider research/publication goal is outside this percentage.
