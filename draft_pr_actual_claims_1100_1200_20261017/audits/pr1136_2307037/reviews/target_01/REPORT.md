# PR1136 independent original-target and boundary-family audit

Date: 2026-10-17 (UTC). Reviewer scope: original target, independent sharpness/rearrangement, extreme pole geometries, and boundary quantifiers. Submitted baseline supplied by the parent: `cbbe7826cca914588018c840ba99c6b7a59fa7f5`. No Git/index/ref operation was used to verify or change that baseline. The exact inspected proof is pinned below.

## Verdict and exact scope

**PASS for original-target alignment and the independently checked sharpness/localization deductions. No counterexample or quantifier defect found.** Conditional on Inputs A and B having the exact scopes stated in `inputs/PROOF.md`, its deduction proves the full original Problem 7.37, with the stronger conclusion that S is compact and the explicit constant C = pi(log 2 + 1/e), approximately 3.3333134401. This review does not independently certify the primary-source statements of A and B; those remain clearly identified dependencies, rather than something numerical stress tests can establish. No novelty or priority verdict is made.

This reviewer initially read only `inputs/PROOF.md`, then independently retrieved the original problem. `AUDIT.md`, other reviews, and other agents' outputs were not inspected. All authored files are confined to this review folder. No external human communication, Git mutation, publication, PR, tracker, release, or DOI action occurred.

## 1. Original source and quantifier reconciliation

Fresh source: W. K. Hayman and E. F. Lingham, *Research Problems in Function Theory (New Edition)*, [arXiv:1809.07200v2](https://arxiv.org/abs/1809.07200v2), version dated 21 September 2018. Retrieved PDF: [versioned primary PDF](https://arxiv.org/pdf/1809.07200v2). The full item and neighboring context were read as extracted text and visually on PDF pages 172–173, printed pages 171–172. The primary PDF and extracted primary text remain under the ignored `sources/private/`; rendered page images remain under ignored `tmp/`. No primary-source body is republished here.

The source asks for a single absolute finite C such that each finite rational squared-pole sum

    g(z) = sum_j lambda_j/(z-z_j)^2,
    lambda_j > 0, sum_j lambda_j = 1,

has an exceptional set S(g) of planar area exactly pi for which the displayed area integral over D_R minus S(g) is bounded by 2pi log R + C for every R > 1. It imposes no location, separation, unit-disk, distinctness, equal-weight, connectedness, or minimum-mass hypothesis. Repeated locations are allowed by this unrestricted finite list. S depends on g and is selected before the universal radius quantifier. The source does not demand compactness, so the submitted compactness is a strengthening. The integral of |g| has the ordinary nonnegative area-integral meaning; substituting a principal value would change the target.

The preceding Problem 7.36 concerns the sharp coefficient in the complementary-region transform estimate; its update credits Eremenko–Hamilton with a solution. The continuation of 7.37 explains the implication toward that coefficient and records no reported progress on 7.37 in this edition. That is edition-specific context, not evidence of current priority or novelty. The proof correctly supplies an extra quadrature construction and localization instead of identifying the two problems without an argument.

Exact target comparison:

| Feature | Original item | Submitted proof |
| --- | --- | --- |
| Number of poles | Arbitrary finite n | Arbitrary finite n |
| Weights | Positive, total one | Same; repeated poles combined |
| Pole locations | Unrestricted complex locations | Same |
| Exceptional area | Exactly pi | Exactly pi via null boundary |
| Dependence | One S(g), all R > 1 | S fixed before R; only splitting sets depend on R |
| Integral | Ordinary area integral of nonnegative | Explicit ordinary Lebesgue integral, finite |
| Constant | Absolute finite C | Explicit pi(log 2 + 1/e) |

## 2. Independent potential/field and localization checks

The distinct mechanism used here was disk mean values, layer-cake rearrangement, exact translated-pole formulas, and a far-field expansion. These checks do not infer a universal theorem from finite samples.

### 2.1 Disk identity and ordinary finiteness

For a disk B(a,r) and z outside its closure, the mean-value identity for the holomorphic function w -> (w-z)^(-2) gives

    (1/pi) integral_B(a,r) (w-z)^(-2) dA(w) = r^2/(a-z)^2.

Thus disjoint disks with r_j^2 = lambda_j already give the asserted exterior field without a nontrivial quadrature construction. Overlaps are precisely where replacing multiplicities by one indicator ceases to be automatic: a union of coincident disks has area pi max(lambda_j), not pi sum(lambda_j). The submitted Input B addresses that gap; merely taking their union would not prove the theorem. Combining repeated poles first is algebraically valid and makes the source list intrinsic to g because principal coefficients at distinct poles are unique.

Once Input B supplies an open Omega containing each B(z_j,sqrt(lambda_j)), all poles have neighborhoods in S = closure(Omega). More directly, outside S,

    lambda_j/|z-z_j|^2 <= 1,
    |g(z)| <= n.

Consequently every bounded-domain ordinary integral outside S is finite even before applying the sharp estimate. Tiny but positive masses cause no integrability gap: their neighborhoods shrink with sqrt(lambda_j), but remain positive for each finite input. No principal-value cancellation is needed to remove the poles.

For any z outside S, the test function is holomorphic and bounded on a neighborhood of closure(Omega), even if z lies in a bounded complementary component. Harmonic quadrature for its real and imaginary parts therefore identifies the field on the entire complement, not merely near infinity. No boundary differentiation or simply connectedness assumption is hidden here. The minus sign in the transform is harmless under absolute value; the pi normalization and disk area are essential.

### 2.2 Independent far-source kernel derivation

For rho = |w| > R, rotational symmetry and the geometric series yield

    integral_0^(2pi) [rho^2+r^2-2rho r cos(theta)]^(-1) dtheta
        = 2pi/(rho^2-r^2).

Integrating r dr from zero to R gives

    integral_D_R |z-w|^(-2) dA(z)
        = pi log(rho^2/(rho^2-R^2)).

The formula has degree zero under simultaneous scaling of R and rho. At rho = sqrt(2)R it is exactly pi log 2, and it decreases for larger rho. It remains valid on the splitting circle itself. Tonelli applies to the nonnegative majorant, so no conditional interchange is used. The submitted factor (pi-a) log 2 is correct after division by the transform's pi.

With t = a/pi in [0,1], the submitted local-plus-far estimate is exactly

    I(R)/pi <= 2t log R + log 2 + t log(1/t).

The target excess is bounded because

    [2log R + log 2 + 1/e] - [2t log R + log 2 + t log(1/t)]
       = 2(1-t)log R + 1/e - t log(1/t) >= 0.

This is a direct universal calculus inequality. It covers a=0 by continuity and a=pi directly. At R down to 1 the positive logarithmic term vanishes but the entropy maximum remains bounded; there is no division by log R. The far-pole and near-pole regimes require no separate geometry assumption. E may have arbitrary shape, and F may be disconnected or include points on |w|=sqrt(2)R. S is never reselected with R. The sharp transform estimate is used only for measurable E contained in the larger centered disk, which is exactly its required setting.

## 3. Independent rearrangement proof of coefficient sharpness

This proof uses layer cake, rather than the submitted gain/loss comparison. Take g(z)=z^(-2) and any measurable S with |S|=pi. Let H=D_R minus S and R>1. Tonelli's layer-cake representation, valid even when the integral is infinite, gives

    integral_H |z|^(-2) dA(z)
      = integral_0^infinity |H intersect D_(t^(-1/2))| dt.

For 0<t<R^(-2), the level disk contains D_R, so the integrand is at least pi(R^2-1). For R^(-2)<t<1 it is at least pi(t^(-1)-1), because removing S removes at most pi area. The remaining levels contribute nonnegatively. Therefore

    integral_H |z|^(-2) dA
      >= pi(1-R^(-2))
         + pi integral_(R^(-2))^1 (1/t-1) dt
       = 2pi log R.

This proves the exact all-R lower bound for every measurable area-pi S, including unbounded sets or sets that fail to remove the singularity. Thus the logarithmic coefficient cannot be reduced by trading it for any finite additive constant. Neither compactness nor finiteness of the left side is assumed in this control.

A further universal check applies to every finite normalized positive configuration. Write M=max_j |z_j|. For |z|=r>=2M (with the zero case interpreted directly),

    |g(z)-z^(-2)| <= 10M/r^3,

since |(1-u)^(-2)-1| <= 10|u| for |u|<=1/2 and sum lambda_j=1. Hence ||g(z)|-r^(-2)| <=10M/r^3, which is integrable at infinity. For every compact S removing neighborhoods of the poles,

    integral_(D_R minus S) |g| dA = 2pi log R + c_(g,S) + O(M/R).

This independently confirms that no widely separated or complex pole geometry alters the leading coefficient. It is an asymptotic statement for each fixed finite configuration; its constants need not be uniform in the pole locations.

## 4. A translated-pole boundary obstruction to C=0

This additional check is consistent with the submitted positive C and does not claim its optimality.

For g_a(z)=(z-a)^(-2), let B=B(a,1). If R>|a|+1, polar coordinates centered at a show

    integral_(D_R minus B) |z-a|^(-2) dA = pi log(R^2-|a|^2).

Indeed the two opposite radial exit lengths r_+(theta), r_+(theta+pi) have product R^2-|a|^2, and integrating log r_+ gives the formula. In particular its excess over 2pi log R tends to zero.

For any measurable S of area pi put P=B minus S and Q=S minus B; then |P|=|Q|. If the ordinary integral is locally finite, the excess limit for S is

    D(S) = integral_P (|z-a|^(-2)-1) dA
           + integral_Q (1-|z-a|^(-2)) dA >= 0.

If the first integral diverges, the excess limit is +infinity and a finite-C bound already fails. Otherwise the formula follows by subtracting the B integral and letting R grow; the Q contribution is absolutely integrable because its kernel is at most one and |Q|<=pi. Both displayed integrands are strictly positive off the unit circle. Thus D(S)=0 forces S=B almost everywhere.

If C=0 were possible for g_1, the large-R inequality would force D(S)=0 and hence S=B(1,1) almost everywhere. But at R down to 1 its integral tends to

    J = 2 integral_0^(pi/3) log(2 cos theta) dtheta > 0,

whereas 2pi log R tends to zero. The integrand is strictly positive on (0,pi/3), proving the contradiction without numerical approximations. Numerically J is about 1.0149416064. This establishes that a zero additive constant does not solve the original all-radius problem, even when S can be chosen optimally. It does not identify a numerical positive lower bound for the infimum of all admissible universal constants.

## 5. Adversarial family ledger

| Family/mechanism | Evidence and status | Exact remaining gap |
| --- | --- | --- |
| Repeated arbitrary complex poles | Coefficients at a common pole add exactly; normalized sum unchanged; combined disk radius is sqrt(total mass) | None in this reduction |
| Nearby or coincident unequal poles | Naive disk union fails area and multiplicity; Input B is the stated remedy | Primary-source verification of B belongs to the input audit |
| Tiny positive masses | Exact rational test down to 10^(-30); analytic radius sqrt(lambda)>0 and pointwise bound above | No uniform lower mass is used; lambda=0 may be discarded but is outside the literal positive list |
| Widely separated/far complex poles | Far-source logarithmic formula, no support-radius constant; far-field expansion | No uniform-in-geometry asymptotic error is claimed or needed |
| Pole near/on the unit circle or near a splitting circle | Translated-pole exact formula, positive boundary limit; split circle has area zero and distance from D_R remains positive | No special pole exclusion is assumed |
| R down to 1 | Uniform entropy bound remains finite; C=0 obstruction is explicit | Optimal positive additive constant remains undetermined |
| R to infinity | Layer cake proves exact sharp lower coefficient; normalized expansion independently confirms it | No gap in coefficient sharpness |
| Infinite mass lists / signed or complex weights | Outside target; construction relies on finite positive masses | No extension asserted |
| Naive per-pole triangle bound | Can introduce pi sum lambda_j log(1/lambda_j), unbounded as n grows | Blocked as a universal-constant proof without a new mechanism; not a counterexample to the actual theorem |

## 6. Checkable artifacts, controls, and limitations

`independent_controls.py` and `control_inputs.json` provide exact rational and floating diagnostics. The disk integrals are computed by independent area quadrature, and translated-pole integrals by radial exit geometry. Radial and angular integrations independently check the far-kernel formula; the scale tests cover R=10^(-6), 1, and 10^6. The exact mass controls check repeated poles, unequal masses, and a 10^(-30) mass. These computations are diagnostics, not rigorous numerical error enclosures; the universal deductions above are analytic proofs.

`run_controls.py` performs eight runs: baseline plus three deliberate mathematical errors, each under ordinary Python and `python -O`. Baselines both pass and are byte-identical. All six mutant runs fail as expected: omitting pi from the far-source kernel, introducing an erroneous R^2 factor under scaling, and using radius lambda instead of sqrt(lambda). Guards use explicit exceptions, with no optimization-removable assertions. The source, proof, input, and code hashes are embedded in the baseline output, and the output hashes are listed in the artifact receipt.

One initial diagnostic run used a uniform angular grid for a far translated pole and failed the requested tolerance at a square-root endpoint. This was a quadrature-resolution failure, not a theorem violation. The final code removes that endpoint singularity by an angular substitution, then reruns the full baseline and all mutants. No initial failed numerical output is presented as mathematical evidence.

Reproduce from this directory with `python3 run_controls.py`. This requires Python's standard library and the privately retrieved PDF at the pinned path. The private PDF can be retrieved again from the versioned URL above; its expected SHA256 is recorded in `SOURCE_PROVENANCE.json` and in the control input. No downloaded primary body is tracked as an authored artifact.

Pinned inspected proof SHA256: `32e68249400aad782b77c74405890f9929fc8576ab8a13d59a3b8db75dea9bdc`.

Pinned fresh HL PDF SHA256: `8e28fd4403a07e4e19a9816b7efaafddf9f475d59cf8c34a8255cb03833ed4f0`.

**Strongest verified result:** the submitted theorem has the exact original quantifiers, and its deduction from the explicitly stated Inputs A and B survives the independently proved potential/rearrangement and limiting-family controls. **Remaining gap for an unconditional overall audit verdict:** independent primary-source validation of those two established inputs. No priority conclusion, optimal additive-constant conclusion, external peer-review claim, or inference from finite tests is promoted here.
