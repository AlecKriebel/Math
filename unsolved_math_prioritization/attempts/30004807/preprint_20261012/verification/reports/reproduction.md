# Independent symbolic reproduction and falsification: PR 464

Problem 30004807 / OWR-8415343-010. Frozen PR head: `97b2ed225574ca61bd03cb8db021a533e04938dc`. Review completed 2026-10-12 07:17:40 UTC. Independent-family completion estimate: 100%.

**Result:** the proposed metric, full mixed Einstein tensor, curvature invariant, harmonic lapse family, spatial mass, all-field density cancellation, and oriented boundary functional pass this independent mathematical reproduction. No blocking algebraic or analytic defect was found in the frozen construction. This computation does not independently certify the primary source's conjecture interpretation or historical priority. Those remain separate review requirements before promoting a full-resolution claim.

The selected metric has an ordinary absolutely convergent contracted integral equal to \(-8\pi\) for the stated boundary-reaching radial test. This conclusion uses the specified blown-up boundary smooth structure. It does not assert the same test space after identifying the boundary sphere with a point, nor a counterexample with an added null energy condition.

## Independence and evidence

`INITIAL_HYPOTHESIS.md` was recorded before source formulas or peer/historical verdicts were read. I read the frozen proof and executable programs, then derived the curvature from a generic four-dimensional metric in **area-radius coordinates**, distinct from the author's isotropic-radius calculation and the prior auditor's proper-distance orthonormal route. No author or prior-audit code was imported. Historical manifest metadata was read for hashes; its recorded verdict was not used as mathematical evidence. The historical audit narrative was read only after the independent 67-check result had been obtained.

The new program `areal_metric_controls.py` derives Christoffel symbols and the Ricci tensor from the full metric before imposing the harmonic lapse. It performs 67 exact checks, including all sixteen mixed Einstein components. Its valid normal and optimized runs produce identical JSON bytes. `run_adversarial_controls.py` executes sixteen deliberately false claim inputs in each mode: 32 actual subprocess rejections. Every rejection has the intended exit code 4 and exact `InvalidClaim:EXPECTED_FALSE_CLAIM_REJECTED:<name>` diagnostic. No accidental exception or unexpected crash is counted as a rejection.

Pinned environment: Python 3.14.6, SymPy 1.14.0, mpmath 1.3.0. The private environment and invalid JSON fixtures are excluded from the public whitelist. The published valid programs can reproduce the controls with Python and SymPy 1.14.0; the driver creates any invalid inputs only under its private-case directory.

## Curvature derived in another radial coordinate

Let \(a>0\), \(r>0\), \(f=1+4a/r\), and begin with an arbitrary positive lapse \(L(r)\):
\[
g=-L(r)^2dt^2+f^{-1}dr^2+r^2d\Omega^2.
\]
The full coordinate calculation gives
\[
G^t{}_t=0,\qquad
G^r{}_r=\frac{4a}{r^3}+\frac{2fL'}{rL},
\]
\[
G^\theta{}_\theta=G^\varphi{}_\varphi
=\frac{fL''}{L}+\left(\frac{f'}2+\frac fr\right)\frac{L'}L+\frac{f'}{2r},
\]
with every off-diagonal mixed component zero. The time component vanishes for any lapse because the spatial cumulative mass is constant; zero scalar curvature is established for the harmonic lapse family rather than asserted for arbitrary lapse.

Put \(q=\sqrt f\), \(L=A+Bq\), with \(A,B\ge0\), \(A+B>0\). Since \(r^2qL'=-2aB\), the static harmonic equation holds. Substitution gives
\[
G^\mu{}_\nu=\operatorname{diag}\left(0,\frac{4Aa}{Lr^3},-\frac{2Aa}{Lr^3},-\frac{2Aa}{Lr^3}\right),\qquad R_g=0.
\]
In particular the vacuum endpoint \(A=0,B>0\) has all Einstein components zero. The ultrastatic endpoint \(B=0,A>0\) has a nonzero radial component. The formal \(a=0\) control gives flat curvature; it is not claimed to retain the \(a>0\) inner-boundary geometry.

To compare with the frozen proof, take \(x=\rho-a>0\), \(\rho=x+a\), \(p=x/\rho\), and \(r=x^2/\rho\). The positive branch is explicit:
\[
\sqrt{1+4a/r}=\frac{x+2a}{x},\qquad
\frac{dr}{d\rho}=\frac{x(x+2a)}{\rho^2}>0.
\]
Thus no unjustified square-root sign cancellation enters the computation. Pulling back the spatial radial coefficient yields \(f^{-1}(dr/d\rho)^2=p^4\). At \(A=B=1/2\), \(L=1/p\), and the independently derived components become
\[
\left(0,\frac{2a\rho^2}{x^5},-\frac{a\rho^2}{x^5},-\frac{a\rho^2}{x^5}\right).
\]
The Ricci-square invariant is
\[
\operatorname{Ric}_{\mu\nu}\operatorname{Ric}^{\mu\nu}
=\frac{24A^2a^2}{L^2r^6}
=\frac{6a^2\rho^4}{x^{10}}
\quad(A=B=1/2).
\]
Its leading coefficient is \(6a^6>0\) after multiplying by \(x^{10}\). This establishes invariant curvature blow-up. The radial Einstein component has \(x^5G^\rho{}_\rho\to2a^3\ne0\), so it does not satisfy a strictly improved \(O(x^{-5+\kappa})\), \(\kappa>0\), bound. A zero scalar curvature does not imply flatness.

## Spatial geometry and energy interpretation

The area-radius spatial metric has cumulative/Misner–Sharp mass
\[
\frac r2(1-f)=-2a.
\]
The independent isotropic asymptotic expression gives the same ADM mass. The regular-ZAS mass formula gives \(-2a\), with Euclidean inward derivative \(\partial_\rho p|_{\rho=a}=1/a>0\). The resolution factor is harmonic and vanishes simply at the boundary.

The symbolic check that coordinate-sphere areas vanish is supplementary. The full approaching-surface argument is analytic: for compact surfaces converging in \(C^1\) to the inner sphere, their Euclidean areas remain bounded, while the supremum of \(p^4\) on them tends to zero. Their physical areas therefore tend to zero. This verifies the stated ZAS area property for that full class, rather than inferring it solely from coordinate spheres.

For the selected lapse the radial optical coordinate obeys \(ds/d\rho=p^3\sim x^3/a^3\), so the finite radial boundary has \(s\sim x^4/(4a^3)\). The two-dimensional radial metric is conformal to \(-dt^2+ds^2\); constant-radius tubes have Lorentzian induced metric. These are the construction's timelike-boundary checks. They do not by themselves certify which timelike-singularity definition the primary conjecture imposes; the independent source/geometry review must do that.

With \(T=G/(8\pi)\), the static orthonormal energy density is zero. The angular pressure is negative and the radial pressure positive. An angular null direction therefore violates the null energy condition. This is an actual boundary of the result, not a numerical uncertainty.

## Flux, index placement, and normal orientation

The areal volume density, apart from \(dt\,dr\,d\Omega\), is \(Lr^2/q\). Multiplying by the independently derived radial Einstein component gives
\[
Q_r=\frac{4Aa}{rq}.
\]
A radial vector transforms as \(\psi^r=(dr/d\rho)\psi^\rho\). Consequently
\[
Q_r\psi^r=Q_\rho\psi^\rho,\qquad Q_\rho=\frac{4Aa}{\rho}.
\]
One cannot identify the components \(\psi^r\) and \(\psi^\rho\). In fact, a boundary-reaching test with \(\psi^\rho=1\) has \(\psi^r\to0\), and the finite product remains nonzero because \(Q_r\) diverges. This is a direct check against silently substituting a different boundary smooth structure or test convention.

For \(\psi=\eta(t)\chi(\rho)\partial_\rho\), \(\int\eta=1\), \(\chi=1\) near the boundary and compactly supported, the full contracted density is
\[
4Aa\eta\left(\frac{\chi'}\rho-\frac\chi{\rho^2}\right)
=4Aa\eta\,\partial_\rho(\chi/\rho).
\]
This uses the mixed contraction \(G^\mu{}_\nu\nabla_\mu\psi^\nu\), equivalent to the raised/lowered scalar on the smooth interior. Using an unraised covariant tensor as though it were mixed introduces an erroneous metric factor and fails the negative control.

The exterior domain's inner outward normal points toward decreasing \(\rho\). Integrating the full density gives
\[
4\pi\int_a^\infty 4Aa\,\partial_\rho(\chi/\rho)\,d\rho=-16\pi A.
\]
At \(A=B=1/2\) this is \(-8\pi\). The sign, sphere area factor, lapse coefficient, and invariance under radial coordinate change are independently checked.

## All-field cancellation and absolute convergence

In exterior Cartesian coordinates, let \(u=|z|\), \(n=z/u\). The density obtained from the derived radial and tangential curvature eigenvalues is
\[
D^i{}_j=L p^6G^i{}_j
=2Aa\left(\frac{3z_i z_j}{u^5}-\frac{\delta_{ij}}{u^3}\right).
\]
This matrix is symmetric, traceless, and smooth on \(u\ge a>0\). The new program derives the spatial Christoffel symbols directly from \(h_{ij}=(1-a/u)^4\delta_{ij}\), and checks every component of
\[
\partial_iD^i{}_j=0,\qquad D^i{}_j\Gamma^j{}_{ik}=0.
\]
The full curvature calculation has zero time row and column. Static spatial Christoffel symbols with the time derivative also vanish. Therefore, for every smooth boundary-reaching compactly supported vector field in the stated structure,
\[
G^\mu{}_\nu\nabla_\mu\psi^\nu\,dV_g
=D^i{}_j\partial_i\psi^j\,dt\,d^3z.
\]
On a compact support up to \(u=a\), the right side is bounded and has finite ordinary measure. Its absolute value is integrable. This is a direct analytic argument for all fields; no distributional multiplication or principal-value prescription is used.

The radial and combined angular connection summands have residues \(8A/x\) and \(-8A/x\). Each can diverge logarithmically if integrated separately. The proof must sum the ordinary smooth contraction before integration, as the frozen construction does. The negative controls explicitly reject treating an individual summand as integrable or omitting the angular cancellation.

The independently computed inner normal trace is \(D^i{}_j(-n_i)=-4Aa n_j/u^3\). Integration by parts gives the all-field boundary functional
\[
I(\psi)=-\frac{4A}{a^2}\int_{\mathbb R\times S_a}\langle\psi_{\rm spatial},n\rangle_\delta\,dt\,dA_\delta.
\]
It vanishes for every allowed test exactly when \(A=0\). The parameter \(B\) cancels from the functional even though it affects the lapse. The selected radial test is smooth in Cartesian exterior coordinates because \(a>0\), and its normal boundary trace is nonzero. Compact support confined to the open interior excludes that trace and gives a different, ordinary interior identity.

## Immutable-source and executable replay record

`REPLAY_RECEIPT.json` verifies all thirteen original source files, by both byte count and SHA-256, before and after execution. Six payload references in `FROZEN_INPUTS.json` and five in `AUDIT_MANIFEST.json` are independently verified: eleven extant payload references in total. The four historical executions (author17 and prior35, each normal and optimized) reproduce the exact stored JSON bytes. The frozen release output and historical author-rerun output agree.

One historical reference remains **unattested**: `FROZEN_INPUTS.json` records standalone `author_manifest_sha256=b64fa97f0194f55cf516cb473a032b1a0bda8ab7c8550cc64e32a098ab6c156f`, but no corresponding original manifest path or bytes exist among the thirteen files. I did not reconstruct bytes or claim this hash was checked. This is a provenance limitation, not a gap in checking the available payloads.

The author's final `assert result['all_passed']` disappears under optimized execution. Its seventeen Boolean results still compute and are identical, but an exit-zero status alone would be insufficient. The new replay driver independently requires the exact count, all Boolean values true, the `all_passed` flag, successful process exit, and byte-identical stored output using explicit conditional raises in both modes. The historical separate35 program already uses explicit conditional raise guards. For a future public verification entry point, use an explicit failure guard or this driver rather than relying only on the author's final assert.

## Falsification coverage and remaining limits

The sixteen false claims cover reversed radial sign; a nonzero vacuum defect; a spurious surviving \(B\) coefficient; wrong volume density; covariant-as-mixed contraction; reversed boundary normal; separately integrable divergent summands; omitted angular cancellation; positive mass; omitted sphere area; a falsely improved curvature exponent; scalar-flat-as-flat inference; satisfied NEC; forced zero boundary support; identification of areal/isotropic vector components; and cancellation for a traceful tensor density. Each is actually rejected in both modes. The private fixtures are excluded, while valid programs, results, and rejection diagnostics are whitelisted.

No new original proof-search route was attempted. These are verifications of the frozen proposal. No original snapshot, repository index, Git branch, PR, remote service, or cloud document was modified, and no individual was contacted.

The strongest verified result of this family is the exact, absolutely convergent boundary functional for the stated metric and test space. **No unresolved mathematical gap was found in that result.** The remaining external gates are the exact primary conjecture's scope and source convention, a separate bounded priority audit, and fresh adversarial review of any final preprint/package. This report does not replace those gates or claim first historical priority, formal proof-assistant verification, or human peer review.
