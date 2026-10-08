# Independent mathematical audit of problem 30003536

Audit date: 2026-10-08 UTC. Target: OWR-15577-004, queue rank 1001.

## Decision

Accept the five approaches as valid partial results and strategy obstructions. The requested global maximum estimate is neither proved nor disproved. The appropriate disposition remains **unsolved, 5/5 author approaches**. This audit is independent of the author derivations and author checker; it is mathematical review with finite computational regression checks, not formal proof verification or peer review.

The frozen author manifest has SHA-256

    bd0c3dbdf92de2f92f3d31ed64033dfe16e188d1ea28ed66b069af2fad8919d6

All 13 frozen files, including that manifest, remain byte-for-byte unchanged. A separate corrected full report and a minimal patch make one regularization convention explicit. They do not change any proposition, estimate, author-turn count, or unresolved disposition.

The only requested clarification is in Section 6: at a point of the infinite plane, the field uses a symmetric *inner principal-value cutoff*, as well as a symmetric outer cutoff. An ordinary Lebesgue integral there is undefined. The original report already says it uses a specific symmetric regularization, and the intended conclusion is correct; the patch states that regularization without leaving the inner cutoff implicit.

## Scope and target

The audited question fixes an integer d >= 3 and an exponent 1 < s < d-1. It asks for C(d,s), independent of the nonnegative smooth compactly supported density f, comparing the global supremum of the **full Euclidean vector norm** of K_s*f with its supremum on the **closed support** of f. Here K_s(z)=z/|z|^(s+1).

No result below replaces that problem with a scalar component, scalar positive potential, signed density, radial-only density class, maximal truncation, operator norm, atomic measure, or infinite flat measure. Auxiliary singular measures are explicitly separated from the admissible final constructions. The zero density is harmless; all divisions by total mass concern nonzero densities.

For an admissible f, |K_s|=|z|^-s is locally integrable because s<d. Splitting a convolution integral near its singularity and using boundedness and compact support of f justifies absolute convergence and continuity. Alternatively, derivatives can be transferred to f to obtain smoothness; no unjustified differentiation of a singular kernel at points of the support is needed. At infinity, the compact support gives decay O(|x|^-s). The support supremum is attained on a compact set. The moment lower bound below makes it positive, so decay also guarantees an attained positive global maximum.

## Approach 1 antisymmetric moment

The double integral containing (x-a) dot K_s(x-y) is absolutely integrable. On S x S, |x-a| <= D and bounded f reduces the singular part to an integral of |x-y|^-s over a bounded ball. Fubini and swapping x,y are therefore legitimate. Averaging leaves

    (1/2) integral integral |x-y|^(1-s) f(x) f(y) dx dy.

The diagonal is null for product Lebesgue measure. Since s>1 and |x-y|<=D, its value is at least M^2 D^(1-s)/2. The unsymmetrized moment is at most D M A_f. Thus A_f>=M/(2D^s), with the coefficient 1/2 and direction of the diameter inequality correct. A nonzero continuous nonnegative density is positive on a ball, so M and D are strictly positive.

Outside the closed support, delta=dist(x,S)>0 and |F_f(x)|<=M delta^-s. Combining the inequalities gives exactly 2(D/delta)^s A_f. The stated far-field localization follows from delta>=|x-a|-D. The near-support deterioration is real: the bound does not control the ratio when delta/D tends to zero. No assertion about a uniform target constant follows.

Decision: accepted, including every Fubini use and the closed-support quantifier.

## Approach 2 scalar potential across many shells

For the unit spherical shell, symmetry forces the vector field to vanish at zero. When |x|<=1/2, the segment joining -y and x-y stays at distance at least 1/2 from zero, so the derivative bound and mean value theorem yield O(|x|). The claimed derivative bound is generous but valid: the radial and tangential eigenvalues of DK_s have magnitudes s and 1 times |z|^(-s-1).

Uniform cap bounds have dimension d-1. Layer-cake integration involves the power d-s-2 near zero, which is integrable precisely when s<d-1. This covers points on the shell, not only points off it. For |x|>=2 the far-field estimate is immediate. On the intermediate annulus the minimum appearing in the statement is bounded below. Hence the single-shell bound, with a constant depending only on d,s, is valid everywhere required.

The weighted shell r_j^s sigma_{r_j} has field bounded by B min(r/r_j,(r_j/r)^s). Summing the outer and inner dyadic regimes gives constants 2 and 1/(1-2^-s), independent of the number N of shells. At the origin, each shell contributes exactly one to the scalar potential and zero to the vector field.

For each fixed N, convolution with a common radial nonnegative probability mollifier of radius r_N/4 produces an admissible radial C_c^infinity density. The shell scalar potentials are bounded globally for this fixed finite collection. Therefore the convolution identity for the vector field follows by *absolute* Fubini, before any cancellation is used. Averaging cannot increase the vector supremum. For every j and every mollifier displacement z, |y+z| <= r_j+r_N/4 <= (5/4)r_j; positivity then yields the asserted scalar lower bound. The support remains compact and avoids the origin, so there is no hidden singular evaluation in J_f(0).

The quantifiers are correct: the vector bound is uniform in N, whereas the mollification radius may depend on N. The ratio J_f(0)/A_f diverges because A_f is positive and at most the uniform vector bound. This invalidates a uniform scalar-majorant estimate, not the vector maximum principle. The already-known radial positive theorem is credited separately.

Decision: accepted.

## Approach 3 off-support local maximum

The latitude probability measure is supported at distance one from zero. All kernel derivatives needed near zero are bounded uniformly on separated compact argument sets, so differentiation under this integral is harmless.

I recomputed the field's second-order Taylor polynomial directly from the expansion of

    (x_i-y_i) (1-2 x dot y+|x|^2)^(-3/2).

The latitude moments give F(0)=-e_1/sqrt(3), DF(0)=diag(0,5/7,...,5/7), D_1^2 F_1=4/sqrt(3), and D_j^2 F_1=11/(7 sqrt(3)) for j>1. The gradient of the squared full vector norm is zero. Its complete Hessian is

    diag(-8/3,-4/147,-4/147,-4/147,-4/147,-4/147,-4/147,-4/147),

with every mixed entry zero. The trace is -20/7. Both the axial and transverse signs are negative; checking only the axial entry would have been insufficient. The independent finite controls check all 64 Hessian entries and all eight gradient entries.

Mollification gives a nonnegative smooth compactly supported density. If epsilon<1/4, its support stays outside the ball of radius 3/4, so the smaller balls used in the proof have positive separation. Uniform convergence of the field and its first two derivatives follows from uniform continuity of kernel derivatives on the separated compact argument set. It implies C^2 convergence of the squared norm.

Negative definiteness at zero persists on a sufficiently small ball. Since the original gradient is zero, strict concavity supplies a positive boundary gap. Uniform convergence preserves that gap; C^2 convergence preserves strict concavity. A maximum of the mollified squared norm is therefore attained at an interior point and is a strict local maximum. The maximizer may move away from zero, and the proof correctly allows it to move. The field value stays positive nearby, so the same conclusion holds for the norm itself if desired.

There is no comparison with the support supremum. A local off-support maximum does not demonstrate failure for C=1 and certainly does not demonstrate failure for every C(d,s). The negative Laplacian does refute subharmonicity of the squared norm in general.

Decision: accepted in exactly this limited sense.

## Approach 4 three-point energy

For collinear points 0,e_1,t e_1, t>1, the three products are t^-s, -(t-1)^-s, and [t(t-1)]^-s. Putting them over a common denominator gives the displayed numerator (t-1)^s-t^s+1. Strict convexity, or the derivative argument in the report, makes that numerator negative for every real s>1. An equilateral triangle gives three positive half-angle contributions, totaling 3/(2 l^(2s)). These configurations exist in the target dimensions. Continuity away from collisions extends the negative sign to open neighborhoods of three distinct points, so the obstruction is not restricted to a null collinear locus.

For fixed smooth compactly supported f, its scalar potential J_f is bounded. For example, split |x-y|<=1, where the bounded density and local integrability suffice, from |x-y|>1, where total mass suffices. Thus the absolute value of the expanded energy is bounded by the integrable expression f(x) J_f(x)^2. Every permuted term is absolutely integrable. Fubini and permutation symmetry give exactly one third of the symmetrized triple integral. Collision sets have zero product Lebesgue measure.

A sign-changing pointwise integrand is consistent with a nonnegative total energy. Negative cross-cluster pieces cannot justify dropping within-cluster contributions. No smooth positive counterexample is claimed from that calculation. Integer-parameter computational checks are correctly distinguished from the analytic all-real-s proof.

Decision: accepted.

## Approach 5 plane model and moving boundary layer

For the d=4,s=2 plane model, the unregularized norm integral diverges logarithmically at infinity, and at on-plane evaluation points it also diverges logarithmically at the origin. Oddness is valid for each finite symmetric annulus; it is not an absolute-integrability argument. The separate patch writes the on-plane field as the limit over rho<|t|<L, with rho decreasing to zero and L increasing to infinity. Each such annular vector integral is zero. Off the plane, symmetric outer tangential cutoffs give zero tangent component; the normal component is absolutely integrable and equals 2 pi v/|v|. The polar antiderivative and the factor 2 pi are correct.

This is an infinite, singular measure outside the target class. The report explicitly declines to infer every technical hypothesis of a reflectionless-measure theorem from this calculation. The model only blocks an indiscriminate rigidity claim that every regularized zero-on-support field must be trivial.

For the smooth approximants, g(u/R) epsilon^-2 h(v/epsilon) is nonnegative, smooth, and compactly supported for every fixed positive R,epsilon. At z_epsilon=(0,epsilon e), the density itself vanishes, but z_epsilon is in its *closed* support: arbitrarily nearby points have g>0 and h>0. This is essential to the lower bound for A_f.

The changes of variables u=epsilon t and v=epsilon w cancel all powers of epsilon in the projected normal field. The resulting expression depends on R and epsilon only through epsilon/R. For almost every w in the unit disk, b=|e-w|>0. The inner two-dimensional integral converges to 2 pi/b by dominated convergence. Its product with 1-w_1 lies between zero and 2 pi, since 0<=1-w_1<=|e-w|. Multiplication by integrable h gives a second legitimate dominated-convergence step. The exceptional boundary point w=e has measure zero and is not used for a pointwise infinite-times-zero substitution.

On the half disk, 1-w_1>=1/2 and |e-w|<=3/2, giving the lower ratio 1/3. Positivity of h there makes L_h strictly positive. Consequently a threshold T(h) exists such that *every* pair R,epsilon with R/epsilon>=T(h) satisfies A_f>=pi L_h. No requirement that epsilon alone tend to zero is hidden in this proposition.

For R=n and epsilon=1/n, local weak convergence to plane measure is valid against continuous compactly supported test functions: g(u/n) is eventually one on the projected compact set, and the normal approximate identity converges by uniform continuity. There is no claim of finite-total-mass weak convergence.

The fixed off-plane field limit also checks. At (0,ae), set b_n=ae-w/n. For n sufficiently large, a/2<=|b_n|<=3a/2. The normal integrand is bounded by a constant times

    (|u|^2+(a/2)^2)^(-3/2) h(w),

which is integrable over the two tangential and two normal integration variables. Dominated convergence sends g(u/n) to one and b_n to ae, giving 2 pi e. Radiality of g cancels the tangential component. In contrast, the moving support evaluations at z_(1/n) have the positive lower bound already proved. Local weak convergence does not control that support supremum.

Decision: accepted, with the explicit principal-value clarification accompanying publication.

## Sources and attribution

The original target was checked visually on printed p.2124 of the official [Oberwolfach Report 34/2017](https://ems.press/content/serial-article-files/46697). The kernel, exponent interval, nonnegative smooth compactly supported class, and vector norm match the report. The workshop contribution is by Benjamin Jaye, joint with Fedor Nazarov.

The [Eiderman–Nazarov preprint](https://arxiv.org/abs/1701.04500v1) uses the opposite kernel sign, which leaves both norms unchanged. Its stated positive radial theorem, single-component obstruction, and signed radial construction are correctly separated in this packet. I checked the relevant theorem statements in the supplied text and visually checked PDF pp.6–7. I did not recertify the complete external proofs. The [publisher record](https://link.springer.com/chapter/10.1007/978-3-319-59078-3_12) confirms the 2018 chapter publication, page range 257–266, and 29 March online date.

The two available source PDFs reproduce the byte counts and SHA-256 identities in SOURCE_METADATA.json. Their text, images, and PDFs are not copied into this audit deliverable. A fresh bounded title/maximum-principle search, including 2025/2026 qualifiers, produced no primary later complete resolution of this exact target. This is a limited negative search, not a certificate that the literature has no solution. Current unsolved *within this packet* is the only mathematical disposition certified here.

The repository/corpus duplicate gate was read for scope and limitations. This audit does not independently recertify the entire external repository inventory or the complete supplied datasets. It retains the author's bounded-search qualification and makes no priority claim.

## Computation and integrity

The supplied author controls replay successfully and reproduce their declared counts: 12,371 finite checks; six positive normal/optimized replays; 36 wrong-claim rejections; 12 malformed-claim rejections; 24 integrity rejections; and three read-only relocations.

The separately authored independent harness adds 4,294 exact checks: 73 complete latitude Taylor/gradient/Hessian checks, 12 genuinely three-dimensional antisymmetric moment identities, 72 geometric three-point checks, 2,880 shell-sum checks at non-dyadic radii, and 1,257 boundary-ratio checks. These use exact rational arithmetic, with an exact quadratic radical extension for the latitude computation.

In normal, -O, and -OO child processes, the harness also records six positive replays, 39 wrong-claim rejections, 24 malformed-claim rejections, 57 integrity/parser/path/inventory rejections, and three read-only relocated replays. The read-only check verifies six actual PermissionError outcomes from attempted file append and creation, rather than relying on mode bits alone. Every relocated payload inventory is unchanged. No source documents or datasets are needed to replay the finite controls.

Checks reject duplicate JSON keys, nonfinite constants, malformed encodings, wrong top-level shapes, optimistic scope changes, wrong signs, path traversal, absolute and nested paths, symlinks, extra inventory entries, missing required files, duplicate paths, Boolean byte counts, and invalid digests. In parser/path negative controls, a deliberately updated local fixture pin lets execution reach the parser; that is not an accepted replacement for the externally pinned original.

The verifier executes only payload code whose bytes have first passed the externally pinned manifest check. Explicit exceptions, rather than optimization-stripped assertions, enforce the checks. No computational result substitutes for the preceding analytic audit.

## Acceptance conditions and publication boundary

The corrected report and minimal patch are separate files. The frozen author claims continue to record that no independent audit had been performed *at the time of author freeze*; this audit does not rewrite that historical field. The separate acceptance record records the later review.

Accept the source-free mathematical report, audit, clarification patch, finite controls, and public metadata with status unsolved and turns 5/5. Preserve the distinctions between local and global maxima, radial and general positive densities, scalar components and the full vector norm, signed and nonnegative densities, and regularized infinite measures versus the exact smooth compact-support class. Do not label the work a solution, counterexample, peer-reviewed result, formal verification, or exhaustive literature/duplicate certification.

No remote repository, branch, pull request, user computer, or third-party data was modified during this audit.
