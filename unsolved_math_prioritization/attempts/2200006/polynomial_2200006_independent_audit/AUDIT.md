# Independent adversarial audit: Problem 2200006

## Verdict and scope

**PASS, scoped to the mathematics and evidentiary claims listed below.** No fatal mathematical gap was found, and no correction to the frozen authored packet is required. The correct disposition remains **unsolved, 5/5 approaches**. The exact extremal function, including the exact value at `(k,l)=(2,10)`, is not determined.

The accepted concrete conclusion is

\[
1152\le M(2,10)\le29525.
\]

The credited 1,152-point quartic refutes the separate universal formula `M(k,l)=k^l`. It does not solve the original request to find the maximum. Neither construction optimality, global literature completeness, human peer review, nor formal proof-assistant certification is certified by this audit.

Audit date: 5 October 2026 UTC. The auditor read all ten frozen authored files and all nine proof sections. No authored file was edited. No remote write was performed. No source PDF, extracted source text, source manuscript, dataset content, or private coordination file is included in this audit deliverable.

## Exact freeze audited

- Authored directory: `polynomial_2200006`, ten regular files.
- Authored ZIP: `polynomial_2200006_AUTHORED.zip`, 22,726 bytes.
- ZIP SHA-256: `daa39e563e2269923c5dbf4865090782382483eaab19b66309568e51866e6a28`.
- Authored manifest SHA-256: `db1d4038234a4e1c832a708b948726f7245564956bd5d4a2e8bb21bb015b5475`.
- Every ZIP member matches the corresponding frozen directory file byte for byte. There are exactly ten unique members, with safe relative paths.
- The author's package verifier passes inventory, hashes, and byte-identical deterministic replay, reporting **23,681 checks** and **54 selector-family parameter pairs**.

## Load-bearing upper bound: accepted

The proposition concerns every globally nonnegative real polynomial of degree at most `2k`, not merely sums of squares. It bounds distinct isolated real zeros, even if other real zero components are present. The proof does not silently assume that either the original complex zero set or the original critical locus is finite.

1. **Degenerate isolated zeros survive as nearby minima.** For any finite selection of isolated zeros, disjoint small closed balls have strictly positive boundary values. A uniformly small perturbation `epsilon*sum(x_i^(2k))-b.x` leaves the center values below the boundary values. Compact minimization then supplies an interior local minimum in every ball. No nondegeneracy of the original zeros or Hessians is needed.
2. **Noncompactness is controlled.** The top homogeneous part of a globally nonnegative polynomial is nonnegative. Adding the displayed positive homogeneous term makes it strictly positive on the unit sphere. Euler's identity gives an outward radial component growing as `||x||^(2k)`, hence a gradient norm growing as `||x||^(2k-1)`. The perturbed gradient is proper. A merely coercive potential would not, by itself, justify this claim; the explicit radial estimate does.
3. **Degree is exactly one.** On a sufficiently large sphere, the gradient minus the chosen constant vector has positive scalar product with the radius vector. Straight-line homotopy to the identity stays nonzero on that sphere. Its Brouwer degree is therefore `+1`, including dimension one.
4. **Regular values can also be small.** Sard's theorem gives regular real values in every sufficiently small open ball of target values. Thus regularity can be imposed without destroying the local-minimum separation. The Jacobian is the Hessian; all real critical points are nondegenerate.
5. **The real fiber is finite.** Properness makes the fiber compact. Regularity makes it discrete. A compact discrete fiber here is finite: an infinite compact set would have an accumulation point in the fiber, contradicting its local isolation.
6. **Complex positive-dimensional components do not invalidate Bézout.** An invertible real Jacobian is also invertible over the complex numbers. Each counted real root is therefore an isolated nonsingular complex root. Only those roots are counted. Other complex components are permitted.
7. **The sign count is used in the correct direction.** Let `T_+` and `T_-` count real critical points with positive and negative Hessian determinant. Global degree gives `T_+-T_-=1`. Bézout gives `T_++T_- <= (2k-1)^l`. Every constructed nondegenerate minimum has positive-definite Hessian, so it contributes to `T_+`. The proof does not claim that every positive-determinant critical point is a minimum. Hence the selected number `N` is at most `((2k-1)^l+1)/2`.
8. **No finiteness premise is needed for the original isolated-zero collection.** Applying the bound to every finite selection rules out a larger, or infinite, isolated-zero collection. The zero polynomial has no isolated real zeros when `l>=1`.

### Independent justification of the precise Bézout input

For the critical-point application it suffices to use the following weaker standard consequence, without a theorem about every singular isolated component. If `l` complex polynomials of degrees at most `D` have `T` distinct nonsingular common roots, choose pairwise disjoint neighborhoods of those roots. The complex implicit function theorem preserves one common root in each neighborhood under sufficiently small coefficient perturbations. Choose such a perturbation in the dense generic set of systems of degrees exactly `D` whose projective intersection is finite. Ordinary projective Bézout bounds its total intersection multiplicity by `D^l`, so `T<=D^l`. This argument allows positive-dimensional components in the original complex fiber. The degree-`D` generic perturbation is used only for the complex count, not to preserve the gradient structure or its real minima.

The author's broader isolated-intersection formulation of Bézout is valid. The argument above independently validates exactly the part required for the signed-gradient bound. Standard mathematical inputs remain Sard's theorem, Brouwer degree with its regular-value formula, the complex implicit function theorem, and projective Bézout; none is represented as formally proved by the finite verifier.

### Adversarial examples checked against the logic

- `f=x^4+y^4` has a degenerate isolated zero. Linear perturbation creates a nondegenerate minimum when both linear coefficients are nonzero. Counting the original Hessian signs would fail; the authored proof correctly perturbs first.
- `f=(x^2+y^2)(x-2)^2` is SOS, has an isolated zero at the origin, and also has the noncompact zero line `x=2`. Selecting a small ball around the origin is legitimate; assuming the whole original zero set is compact would not be.
- Put `s=x^2+y^2` and `f=s^2+s`. Its gradient is `2(2s+1)(x,y)`. The only real critical point is the origin, with Hessian `2I`, so zero is a regular real value. Nevertheless its complex critical fiber also contains the curve `s=-1/2`. Real regularity alone does not imply a finite complex fiber. The author's proof does not make that inference.
- The function `-x^2-y^2` has positive Hessian determinant at a strict maximum. Positive local orientation does not characterize minima. The proof requires only the correct inclusion of minima among positive-orientation points.

The last two controls have exact symbolic arithmetic certificates in the independent verifier. They illustrate forbidden shortcuts; they are not counterexamples to the accepted proposition.

## Remaining proof sections

1. **Degree convention: PASS.** A nonzero SOS cannot cancel its top-degree squares. The strictly positive SOS multiplier `(1+sum(x_i^2))^(k-e)` raises degree from `2e` to exactly `2k` without changing any real zero or its isolation. Product summands have the prescribed degree cap. Constant and zero cases are handled.
2. **Grid and sharp elementary cases: PASS.** The coordinate grid has `k^l` distinct zeros. A nonzero univariate summand gives the `l=1` bound, and an affine common-zero set gives the `k=1` bound. The historical planar statement is attributed, not newly proved, and is not used elsewhere.
3. **Conditional degree-`k` Bézout: PASS.** When the complex common-zero set is finite, generic linear combinations cut every remaining positive-dimensional component. After `l` cuts the finite intersection contains the base locus and is bounded by `k^l`. Empty intersections and constant combinations cause no exception. This additional complex-finiteness hypothesis is expressly excluded from the original problem's scope.
4. **Explicit quartic: PASS.** Complete sign analysis leaves exactly nine `t` values. Each slice has two zero radicands and seven strictly positive radicands. Canonical squarefree-radical coordinate encodings independently give 128 distinct points per slice and 1,152 in total. The leading `x_0^4` coefficient is one. Monic adjoining of the nine square-root variables yields a rank-512 free module over `C[t]`; the complex coordinate ring has dimension one. None of this treats isolated real points as isolated complex points.
5. **All-parameter even family: PASS.** The selector roots and sign changes exclude every open real cell outside the retained integers, including both exterior rays. Every interior retained integer has exactly one active zero selector; every block boundary has exactly two. The corner `d=1,m=2` has no positive levels and correctly gives two points. The chosen positive scale places every nonzero well level below every specified endpoint margin. IVT plus degree yields exactly `2d` distinct roots at positive levels and `d` distinct roots at level zero. Summing gives the displayed formula, and the strict-comparison inequality is equivalent to the claimed condition. Odd-degree transfer uses the already proved positive multiplier.
6. **Products and restricted optimization: PASS.** For nonnegative summands in disjoint variable sets, a zero of the sum is exactly a pair of zeros. Degree and finiteness remain admissible. The recurrence is an exact optimization only in the stated selector/grid block library. It is never used as a universal upper bound or an extremality certificate.
7. **Homogenization: PASS.** At `z=0`, the first quadratic forces `x_0=t=0` over the reals, and the rest force every other coordinate to vanish. This is not a projective point. Thus the 1,152 affine points exhaust the real projective zeros in the larger homogeneous variable space.
8. **Unresolved status: PASS.** The upper and lower bounds do not coincide. The packet explicitly withholds both the global maximum and the advertised later low-dimensional claims.

## Independent numerical and algebraic controls

`verify_independent.py` is new audit code. It does not import or execute the author's mathematics verifier. Its only use of the authored mathematical receipt is comparison after independent calculations.

- Expanded integer coefficient polynomials and exact root-multiplicity sign propagation certify all real sign cells, rather than merely testing sample points.
- Exact standard-library rational Sturm sequences check **1,720 distinct positive-level well polynomials** across all **54** author parameter pairs. Every one has the asserted number of simple real roots. Repeated-root controls separately test the zero levels.
- Expanded radicands and canonical squarefree-radical encodings enumerate the **1,152** base points independently.
- A block-size/unbounded-knapsack algorithm computes the restricted optimum through dimension **60**. Independent enumeration by block multiplicities checks every dimension through **24**, extending the author's exhaustive comparison through 20.
- Two-state orientation convolution checks **576** `(k,l)` pairs through `24 x 24`, independently of the author's binomial implementation. This verifies arithmetic, not the topological theorem.
- Exact symbolic controls expose the positive-orientation and complex-fiber shortcuts described above.
- The independent receipt replays byte identically from an unrelated working directory.

The exact independent assertion count is in `independent_results.json`. No finite test suite is claimed to prove the all-parameter results.

## Source and attribution audit

The [primary journal article](https://armj.math.stonybrook.edu/pdf-Springer-final/015-0008-4.pdf), printed page 93, was independently read. It distinguishes Problem 3 from Conjecture 4, uses degree `2k` and summand degree at most `k`, and imposes no complex-finiteness condition. Its actual page span is 91–99. Its newly retrieved PDF byte count and SHA-256 match the authored metadata.

The [designated prior manuscript](https://github.com/DannyExperiments/ottaviani-shapiro-sos-counterexample/blob/main/paper/manuscript.tex), [public release](https://github.com/DannyExperiments/ottaviani-shapiro-sos-counterexample/releases/tag/v1.0.0), citation metadata, and [Zenodo record](https://zenodo.org/records/21875290) confirm DannyExperiments attribution, the 10 August 2026 release, the explicit quartic, and the even-degree family. New archive retrievals confirm the recorded TeX and PDF hashes, sizes, and MD5 metadata. The source's own audit labels are not evidence for this audit's mathematical verdict.

The [later landing page](https://eulersolve.org/papers/amr-014-0019/) was independently read. Its unrefereed status, advertised low-dimensional cases, and blanket general-open wording match the authored description. The last wording conflicts with the earlier higher-dimensional counterexample. No claim in the unavailable later proof is accepted or rejected here. The prior access denial was respected, and no bypass was attempted.

The original 1980 planar proof was not independently inspected. Historical private search outcomes, full-corpus hashes, and author-only retrieval history not directly repeated in this audit remain attributed historical metadata, not fresh independent byte-identity findings. No corpus contents are needed for the proved statements. This qualification does not weaken the direct primary-page match or any accepted mathematics.

## Packaging and negative tests

The unmodified author verifier passes from an unrelated working directory. Five separate temporary copies were altered: proof bytes, frozen count, extra file, missing file, and symlink. Each was rejected by the author verifier. Temporary mutation testing did not modify the authored freeze. Audit inventory and hashes are separately recorded in `MANIFEST.json`; `verify_audit.py` checks them and replays the independent verifier.

## Required corrections and publication disposition

**Required corrections: none. First fatal gap: none found.** Preserve the authored freeze and attach this audit as a separate record. Keep the problem status unsolved with five approaches used. Publish only the scoped bound, credited construction verification, audit code and receipts, source references, and allowed verification metadata. Do not turn this PASS into an exact-solution, global-optimality, novelty, human-review, or formal-certification claim.
