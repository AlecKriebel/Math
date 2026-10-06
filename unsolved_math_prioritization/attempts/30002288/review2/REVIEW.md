# Independent second review: fractional infinity eigenfunctions

Problem 30002288 / OWR-12336-004, rank 840. Review date: 2026-10-06.

## Decisions and exact scope

1. **ACCEPT the corrected core mathematical argument**, archive SHA-256 `4acbfd16b42c4d155ae422823d4ea4937d542b8a574ca781a13aa58fa9193ec8` (12,405 bytes). Finite positive weighted maxima of point-ridge profiles satisfy the full-space nonlocal infinity-eigenfunction equation. Unequal weights give counterexamples to the proposed unweighted high-ridge-subset representation on every bounded open set whose high ridge is not a singleton. The connected rectangle example works for every fixed `0 < alpha <= 1`.
2. **Separately ACCEPT the V2 Rayleigh supplement**, archive SHA-256 `c83da041a8cc4caeb35308e7c531cdd510e5d83f8c9e8f5805541fe6495e0cd5` (3,425 bytes). Its claims of admissibility and root-level Rayleigh asymptotics are correct for the exact kernel and measure specified. This acceptance is independently reasoned below and is not inherited from acceptance of the counterexample.
3. **General finite-p maximal selection remains UNRESOLVED BY THIS WORK.** The compound outcome is partial. No claim of worldwide open status, novelty, priority, external specialist endorsement, or proof-assistant certification is made.

The original core archive remains unchanged: SHA-256 `ba1f6ed2632036cb0e0efa1ce62e1c3824bb8c14e34e036e15c66402ec73d1d2` (12,226 bytes). One precise wording correction was required: the original paragraph called global tests merely C^1 and claimed finiteness from local regularity; admissible global tests must be restricted to the source's C_0^1 class. Unbounded C^1 tests can have infinite nonlocal tails. The correction does not alter the construction or any slope calculation. The exact patch was applied with zero fuzz to a fresh original extraction; all resulting member bytes equal the corrected archive. The corrected argument was actually rerun under isolated normal and optimized execution, including relocation and hostile controls.

This review's mathematical assessment was completed independently before inspecting the other reviewer's correction. Only the exact correction and its frozen bytes were subsequently inspected for acceptance; no other mathematical audit report was used to determine the result.

## Primary-source alignment

The original OWR 08/2013 question, printed pages 456-457, specifies the whole-space quotient and zero exterior values, then asks both representation exhaustiveness and finite-p maximal selection. Its displayed relation for s is typographically inconsistent; the kernel exponent instead determines `s_p=alpha-n/p`.

Lindgren-Lindqvist, *Fractional Eigenvalues*, arXiv:1203.4130v2, matches the operator and conventions used here. Section 7 fixes `0<alpha<=1`; Theorem 14 gives finite-p simplicity when `alpha*p>2*n`; Proposition 20 gives the eigenvalue root limit; Definition 21 uses C_0^1 global tests with the supersolution inequalities directed downward; Theorem 23 supplies normalized subsequential convergence. Corollary 37 gives the profile for eigenfunctions constant on the high ridge. These are the only imported ingredients for the symmetry/singleton consequences. The counterexample is verified directly below.

Da Silva-Rossi-Salort, arXiv:1704.01875v1, Theorem 1.3 concerns the local infinity-Laplacian and a concave-exponent limit. Printed page 4 explicitly distinguishes a conjecture about ordinary local p-ground states. Section 4's suggested nonlocal extensions do not establish the present diagonal fractional limit. This is a scope check, not a literature-completeness claim.

Primary links and byte-level inspection metadata are in SOURCE_CHECKS.json. The OWR question, Definition 21, and DRS Theorem 1.3/conjecture were also visually inspected. No downloaded source text, PDF, or rendered source image is included here.

## Independent continuum verification of the core

### Geometry and one-profile slopes

Let Omega be nonempty, bounded and open, with `delta(x)=dist(x,R^n\Omega)` defined on all of R^n. Then delta is continuous and 1-Lipschitz, has compact support, and attains a positive maximum R. Its high ridge Gamma is a nonempty compact subset of Omega. No convexity, connectedness, or boundary smoothness is needed for the direct construction. Those additional properties hold for the explicit rectangle.

Fix z in Gamma and set `f_z(x)=delta(x)^alpha/(delta(x)^alpha+|x-z|^alpha)`. The inequality `R<=delta(x)+|x-z|` and subadditivity of the alpha power show the denominator is at least R^alpha everywhere, including the exterior. Hence f_z is continuous, zero outside Omega, positive inside, and equals 1 exactly at z.

For x inside Omega and arbitrary y in R^n, use A=delta(x)^alpha, B=|x-z|^alpha, C=delta(y)^alpha, D=|y-z|^alpha, H=|x-y|^alpha. The distance and power inequalities give `|A-C|<=H` and `|B-D|<=H`. Since

    C/(C+D)-A/(A+B) = (CB-AD)/((A+B)(C+D)),
    CB-AD = C(B-D)+D(C-A),

its absolute value is at most `H/(A+B)=f_z(x)*H/A`. The same argument with x and y exchanged supplies the symmetric endpoint bound when needed. Both denominators are positive, and this derivation does not discard exterior points.

The infimum slope equals `-f_z(x)/A`: the bound holds globally and equality occurs at a nearest complement point. Such a point exists since the complement is closed and nonempty. At x different from z, the slope to z equals `f_z(x)/A`, so the supremum equals that bound too. At z all slopes are nonpositive and slopes to infinity tend to zero; thus the supremum is zero. This checks every point of a single profile.

### Finite weighted maxima and switching points

Let `U=max_i c_i f_{z_i}` for finitely many positive c_i and z_i in Gamma. At a fixed x inside Omega, the upper one-profile bound applies to every i, hence

    U(y) <= U(x)(1+H/A).

Choosing any active index at x supplies the lower bound

    U(y) >= U(x)(1-H/A).

The lower multiplier can be negative; the inequality still holds and no sign-based reversal is made. These inequalities handle arbitrary changes of the active index at y. They are not an appeal to a general maximum-stability principle for nonlinear equations.

It follows that `L^-U(x)=-U(x)/A` and `L^+U(x)<=U(x)/A`, with the former attained at a nearest exterior point. If x is not a selected pole, an active profile has a distinct pole z_i. The slope to that pole is at least

    (c_i-U(x))/|x-z_i|^alpha = U(x)/A.

The already established global upper bound forces equality. In particular, this argument automatically ensures that an active component has its prescribed value at its own pole; domination of a component elsewhere is not being ignored. Thus `L^+U+L^-U=0` away from the selected poles. At a selected pole, delta=R and the eigenvalue branch is exactly zero. At every point both branches are nonpositive and at least one is zero:

    max{L^+U+L^-U, L^-U+R^(-alpha)U}=0.

An unselected ridge point satisfies the first branch by the active-pole argument and also has equality in the eigenvalue branch. A selected pole need not be a global maximum; the eigenvalue-branch reasoning still applies. Arbitrary ties, redundant profiles and repeated poles introduce no gap.

### Viscosity passage and the endpoint alpha=1

For an admissible global test phi in C_0^1 touching from below, phi(x)=U(x) and phi(y)<=U(y) for every y. Each test increment is at most the corresponding U increment. Therefore both sup and inf are ordered in the same direction. Their sum and the eigenvalue branch are nonpositive, exactly as required for a supersolution in the source's convention. The inequalities reverse for a test from above, and the zero branch for U supplies a nonnegative branch for the test.

For a locally touching test patched by U outside a small touching neighborhood, the same global ordering holds. The patched function is bounded, even if it has a jump on the patch boundary; that boundary remains a positive distance from x. Near x, local C^1 regularity bounds the quotient by a constant times `|y-x|^(1-alpha)`. Away from x, boundedness controls it. Thus the sup and inf are finite, including when alpha=1. No derivative of U is required at a switch or ridge corner.

The correction to C_0^1 is consequently exact and sufficient. Unrestricted unbounded C^1 functions are unnecessary and are not accepted as the global test class. At alpha=1 the operator remains the full-space supremum-plus-infimum of Lipschitz slopes; it does not become the local Aronsson operator.

### Normalization and nonrepresentation

The norm of U is max_i c_i. The global alpha-Hoelder seminorm is at most `(max_i c_i)R^(-alpha)` because each profile has that scaled bound and a finite maximum preserves a common bound. For a largest-weight pole and its nearest exterior point, equality is attained. The normalized seminorm is therefore exactly R^(-alpha).

For distinct a,b in Gamma, put `q=R^alpha/(R^alpha+|a-b|^alpha)` and take q<t<1. Then `U_t=max(f_a,t*f_b)` has maximum set exactly {a}, but U_t(b)=t>q=f_a(b). For a nonempty closed S in Gamma, the normalized unweighted profile has maximum set precisely S: its denominator equals its numerator exactly when the distance to S is zero. Therefore a putative representation of U_t would force S={a}, contradicting its value at b. A nonclosed S only changes S to its closure, and an overall scalar is fixed by normalization.

On `(-2,2)x(-1,1)`, the inradius is 1 and the ridge is `[-1,1]x{0}`. With a=(-1,0), b=(1,0), t=3/4, the threshold `1/(1+2^alpha)` is strictly below 1/2 for every alpha>0. This is a connected convex Lipschitz counterexample for every exponent claimed. At alpha=1 the two profiles tie exactly at x=(2/7,0), U=7/16; both pole slopes equal 7/16, and a nearest-boundary slope is -7/16. That exact nongrid switch was separately checked.

The singleton-ridge converse follows from the cited constant-on-ridge uniqueness result: every function is trivially constant on a singleton. It is not needed to refute the original representation question.

## Separate independent audit of the Rayleigh V2 supplement

### Kernel, measure, and global integrability

The energy numerator is the ordinary product-Lebesgue integral of `g(x,y)^p`, where `g=|U(y)-U(x)|/|y-x|^alpha`. It contains no additional inverse-power factor in the measure. The identity `n+s_p*p=alpha*p` holds with `s_p=alpha-n/p`. For each fixed alpha in (0,1], sufficiently large p gives `0<s_p<1`.

Let E be the compact support of U and K its exact alpha-Hoelder seminorm. If g is nonzero, at least one coordinate is in E. For |x-y|<=1 the contributing pairs are contained in the union of two sets each having measure at most `|E|*|B_1|`; on them g<=K. There is no diagonal or boundary-crossing divergence. The diagonal is null, and pairs crossing the boundary obey the same global Hoelder estimate.

For |x-y|>1, normalized U lies in [0,1], so even the stronger bound `g<=|x-y|^(-alpha)` holds; the supplement's bound with 2 is harmless. The double integral is bounded by twice a finite support-volume factor times the radial tail integral. That tail converges exactly when alpha*p_0>n. Hence choosing `p_0>max(1,n/alpha)` proves g belongs to L^(p_0) intersect L-infinity on the entire product space. This includes exterior-interior pairs at arbitrarily large distances.

When alpha=1 the near quotient is bounded by a Lipschitz constant and the far exponent is n-1-p_0<-1. The finite-p space is still fractional with s_p=1-n/p; no local W^(1,p) energy is substituted.

### Essential supremum and the norm limit

At a largest-weight ridge pole z and a nearest exterior point y_0, the distinct-point quotient equals K. The function g is continuous on the open set x!=y because U is globally continuous. Every level strictly below K therefore has a positive-measure neighborhood near that extremal pair. This is true even when y_0 lies on a measure-zero boundary: continuity concerns the full ambient product space, not the boundary alone. Thus the essential supremum equals K.

For p>=p_0, integration of `g^p<=K^(p-p_0)g^p_0` yields the correct upper norm bound. A positive-measure superlevel set gives the matching lower limit. Therefore `||g||_p -> K`. The same argument for continuous, compactly supported U with maximum 1 gives `||U||_p -> 1`. Consequently

    Q_p(U)^(1/p) -> K = R^(-alpha).

Together with the independently source-checked eigenvalue limit this gives `Q_p(U)^(1/p)/lambda_p^(1/p) -> 1`. It does not give the unrooted quotient limit or convergence of minimizers.

### Admissibility and zero-boundary closure

For fixed sufficiently large p, the integrability just proved gives full-space W^(s_p,p) membership of U. Define `U_epsilon=(U-epsilon)_+`. Its support is contained in the closed level set {U>=epsilon}, which is compactly contained in Omega: continuity, zero exterior values and boundedness establish positive distance from the complement. If epsilon is above the maximum, the zero function causes no exception.

The error equals min(U,epsilon), tends pointwise to zero and is bounded in L^p by U. Its difference quotient is at most g because min(t,epsilon) is a 1-Lipschitz scalar map. Dominated convergence applies to both the L^p term and the full product-space fractional seminorm. Thus U_epsilon tends to U in the full-space fractional Sobolev norm.

For a fixed epsilon, standard compactly supported mollifiers with radius smaller than the distance of its support to the complement stay inside Omega. Translation continuity in L^p and in the Gagliardo seminorm yields convergence of those mollifications in W^(s_p,p). A diagonal choice gives C_c^infinity(Omega) approximants. This proves the claimed zero-boundary closure rather than assuming a trace theorem or a regular boundary. It is stronger than merely checking pointwise zero exterior values.

**No mathematical correction is required for the V2 supplement.** Its exact frozen bytes are accepted for this separate claim only.

## What remains unresolved

A domain-preserving Euclidean isometry leaves both energy and normalization invariant. For large p, simplicity of the positive first eigenfunction therefore makes it invariant. Uniform limits preserve that invariance. The rectangle reflection exchanges a and b, while the constructed example has values 1 and 3/4 there, so that example cannot be a finite-p subsequential limit. This does not show failure of maximal selection.

If the isometry group is transitive on the high ridge, every subsequential limit is constant there, and the cited uniqueness representation identifies it with F_Gamma. Compactness for every sequence plus uniqueness of the possible limit implies full-family convergence in that special case. On a general ridge the argument supplies no reason for equal ridge values. Leading-order root-energy coincidence cannot provide that missing reason because it holds even for the reflection-excluded examples.

All five bounded approaches remain concluded. This audit does not introduce or claim a sixth selection approach.

## Computational and artifact verification

CONTROL_RESULTS.json records 83 independently run controls: 36 each for original and corrected core payloads, one fresh exact patch application, and ten V2 data-only inventory controls. Positive controls include normal, optimized, relocated, and isolated hostile-cwd/PYTHONPATH runs. Negative controls cover extra modules, startup customization, caches, directories, missing or altered members, altered entrypoints, symlink members/roots/ancestors, bad root types, changed external manifests/archives, and execution without isolated/no-site flags. Altered executable controls were rejected before hostile markers could run.

The independent diagnostic program additionally checks 4,473 exact rational ratio instances, the exact switch described above, 2,025 contraction cases, 544,986 sampled full-space slope pairs in two and three dimensional boxes and a disconnected nonunit one-dimensional example, 2,835 nearest-exterior equalities, 2,746 active-pole equalities, and 16 exact tail-parameter identities. The floating-point tolerance is 2e-10. These tests corroborate the analytic argument; finite sampling is never used as proof of the global or viscosity claims.

The separately pinned review bootstrap validates this review packet's strict flat inventory and all member bytes before executing the independent diagnostics. The external validation receipt records its normal/optimized/relocation/hostile-control reruns. All original inputs are preserved. The trust boundary assumes a trustworthy Python standard library and stable regular files during preflight and execution; no defense against concurrent hostile operating-system mutation is asserted.
