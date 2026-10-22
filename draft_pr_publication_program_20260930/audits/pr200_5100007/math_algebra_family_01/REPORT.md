# Independent algebra, reproduction and geometric falsification report

Scope: PR200 / 5100007 / k115. The frozen design predates all reading of
the submitted proof and verifier. No independent_review, imported favorable
report, root-family report or other new family's mathematics was read.
No Git/ref/PR write, outside individual communication, or publication
action was performed by this family. All authored files are in this folder.

## Assessment

**No counterexample or mathematical gap identified in the exact stated
primitive theorem.** The algebraic factorization, analytic divisor
cancellation, separate N4 degree drop, antipodal pairing and positive
square-root step withstand this family's adversarial review. The needed
canonical billiard translation is independently recovered from Jacobi
addition, physical chord tangency and Euclidean reflection in DERIVATION.md.

**The submitted verifier is unsafe under Python optimization.** Both
assertion sites disappear with -O, while counters and the final PASS keep
printing. A deliberately false first identity is rejected normally and
prints PASS under -O. This is a verification-software limitation, not a
counterexample to the theorem. The independent programs use explicit
exceptions and retain substantive checks under -O.

This report gives mathematical audit evidence, not historical priority,
formal proof-assistant certification, or human peer-review clearance.

## Exact claim, assumptions and boundary

For a>b>0 and fixed 0<λ<b², take the inner confocal ellipse with squared
semiaxes a²−λ,b²−λ. Suppose the billiard family's least period N is
divisible by four. Intersect the two outer tangents at every pair of
consecutive billiard vertices. The product of ordinary positive distances
from these N intersections to either fixed outer focus is phase invariant;
the two focus products are equal. Primitive star trajectories are included.

The least-period condition cannot be replaced by a divisible-by-four
traversal length. For a=3,b=1,λ=9/16, a primitive six-period family has
exact products 20736/343 and 6912/125 at two axis phases. Repeating it twice
gives twelve factors and still unequal products. Degenerate caustics,
hyperbolic caustics and separatrix limits remain outside the exact claim.

## Submitted verifier reproduction

The unmodified source SHA-256 is
bcfacb09e9495ffbf14ebf37ec52390b267399ed747003d83c892b3428b11289;
the proof SHA-256 is
5d31111bf167822783d32aabb1e0bf2766bb372b3a5359739d9c157f8faab030.
Exact copies were replayed in separate assigned-folder subdirectories so
their write to verification.json could not touch the immutable archive.

Normal and optimized executions each exited zero and printed the legacy
25,515 exact labels, 4,181 primitive rotation cases, 702 numerical labels
and maximum error 4.986696415e-85. Under normal Python these checks pass.
Under -O the assertions at source lines 10 and 74 are absent. Function
arguments and numerical computations still run, but their truth/threshold
conditions are unenforced and counts increment unconditionally. Thus
**the optimized run is successful execution, not successful validation**.

optimization_negative_control.py changes only the first submitted check
to False in expressly labeled copies. Normal return code is 1, with the
expected AssertionError. Optimized return code is 0 and printed_PASS=true.
Full stdout/stderr, source copies and replay commands are preserved.

System Python 3.14.6 lacked mpmath. Bundled Python 3.12 also lacked
SymPy/mpmath. This audit installed SymPy 1.14.0 and mpmath 1.3.0 only in
runtime_packages and explicitly inserts that path under -E -B -P. The
legacy output's phrase “Only preinstalled SymPy/mpmath” is the original
script's unchanged self-description and is not true of this replay setup.

## Independent exact evidence

exact_certificates.py passes **306 explicit checks** normally and under
-O, with matching complete output. It does not import author code or use
elliptic functions to construct or iterate its exact sample billiards.

* Direct physical-variable tangent-intersection locus:
  (a²−λ)Q_x²/a⁴+(b²−λ)Q_y²/b⁴=1.
* A rational-function identity factors the paired focal-distance
  polynomial directly in physical squared semiaxes.
* The canonical chord equation, orientation determinant and fixed-caustic
  coefficient are checked independently by exact addition-formula algebra.
* Universal all-phase N4 polynomial reductions give the ordinary product
  4a²b², including generic and axis boundary positions.
* At a²=8,b²=3,λ=24/35, axis and generic phases are exact primitive
  eight-period billiards, both with ordinary product 3200/3. The generic
  phase arithmetic is in QQ(√193); every vertex and outer intersection is
  preserved in exact_certificates.json.
* The exact primitive N6 counterexample above is independently computed
  in QQ(√7) and QQ(√15), proving the repeated-cover limitation.

The Euclidean exact recurrence, line-tangency equation, reflection, closure,
distinct vertices, outer tangent equations, antipodal pairing and focal
product squares are all checked. Positivity recovers ordinary products
without assuming a complex branch of a square root.

## Independent numerical evidence

independent_geometry.py uses **no Jacobi functions**. The first chord is
constructed by affine circle tangency to the inner ellipse; later chords
come from Euclidean reflection and straight-line intersection. Resonances
are found by geometric shooting. Direct line support checks, reflection
versus a newly constructed caustic tangent, closure, winding and vertex
separation are independently verified. Outer intersections come from
solving their two tangent equations. Distances to both foci are calculated
directly, with products accumulated as sums of logarithms.

At 180 decimal digits, 44 shape/period/winding cases were checked at four
phases (0, π/2, π/7 and 0.384123π), yielding 34,498 explicit checks:

* Axis ratios a/b: 1.0001, 1.5, 3 and 10.
* (N,τ): (4,1), (8,1), (8,3), (12,1), (12,5), (16,1), (16,7),
  (32,1), (32,15), (64,1) and (64,31).
* Both foci in every target phase, including ordinary and star trajectories.
* Largest target log-product phase difference: 1.10734447827e-77.
* Largest closure residual, scaled by a: 7.39647239023e-79.
* Largest chord tangency residual: 4.9780828826e-180.
* Largest reflection-versus-direct-tangent residual: 5.81277138729e-141.

Every required residual is below 1e-65. The extreme a/b=10,N=64,τ=31
case has boundary gap 1−λ/b²≈1.008288017e-80 and minimum scaled vertex
separation ≈2.008270915e-40. Its fresh-shooting phase variation is
4.002432104e-82. Separate normal/-O geometric replays test exact N4/N8
caustics, both foci and forward/reverse orientation. A deliberately false
independent guard rejects in both modes.

Finite numerical evidence is not an all-period proof. In particular, the
stored broad JSON λ field has only 125 significant digits, which suffices
to replay the first 43 cases but does not resolve the extreme's 1e-80
boundary gap to the required residual accuracy. The successful broad run
retests the 43 own-checkpoint λ values and freshly shoots that extreme.
extreme_resonance_record.json separately preserves 175 digits from a fresh
180-digit shooting run; its numerical status must not be mistaken for an
interval-arithmetic proof.

## Negative controls and limitations

Six primitive wrong-parity cases (N,τ)=(3,1),(5,1),(6,1),(7,2),(10,3),
(14,5), at a/b=3, show phase variation from 0.0592545963739 to
2.07258901598 in log product. Repeating each just enough to make the
nominal length divisible by four multiplies its variation; it never
restores constancy. Three slightly perturbed resonant caustics show both
nonclosure and phase variation. A separate nonconfocal inner-ellipse
perturbation starts with a truly tangent chord, then fails caustic
preservation after reflection and varies in product by 0.00110367083260825.
These controls show that the numerical procedure can detect false
extensions instead of returning a built-in invariant.

The first full grid attempt stopped after 43 cases because a conservative
1e-35 primitive-separation floor rejected the extreme's genuinely small
separation. The final explicit floor is 1e-70, far below that separation,
and coprime winding is checked. Attempt1 stdout/stderr is retained. A
second run stopped after 32 cases with process exit 120 while shared
storage was full; stdout could not flush a complete report and stderr is
empty. It is not counted as a successful run. Attempt2 is retained. The
completed run resumed only from this family's own first-checkpoint
resonances and recomputed all geometric and product checks.

No third-party source PDF was downloaded or included. Standard analytic
identities were checked at NIST DLMF 22.4 and 22.8; URLs and their exact
role are recorded in DERIVATION.md. Broader literature priority, the source
label k115 and publication-policy clearance belong to other audit work;
this family makes no independent conclusion about them.

## Deliverables and completion

DERIVATION.md gives checkable formulas and the general proof audit;
exact_certificates.json gives complete exact sample vertices and values;
independent_geometry_results.json gives the full completed numerical grid;
reproduction_summary.json and optimization_negative_control.json give the
legacy execution and failure-mode evidence. REPLAY.md explains the runtime
and commands. MANIFEST.json hashes complete authored/replay output files.
The installed runtime_packages tree is a private third-party dependency
cache, excluded from the deliverable manifest and any publication package.

This family's assigned audit goal is complete. No mathematical
counterexample to the stated primitive theorem remains open here; the
verifier's -O failure mode is a concrete issue to repair before treating
optimized execution as verification. Best-guess completion: 100% of this
family's bounded audit, with no claim of overall research/publication
completion.
