# Frozen independent algebra and reproduction design

Frozen at 2026-10-16 04:13:32 UTC, before reading the submitted proof, code,
independent reviews, favorable reports, or any new family's work.

## Claim under examination

For an outer ellipse with semiaxes a>b>0 and an inner confocal elliptic
caustic E_lambda with 0<lambda<b^2, the product of distances to either fixed
focus from consecutive outer-ellipse-tangent intersections is independent
of phase along every primitive Poncelet billiard orbit whose period N is
divisible by four. The precise indexing and any additional assumptions
will be extracted from the submission; they are not presumed correct.

## Independent mechanism

1. Derive the billiard map from straight-line intersection, Euclidean
   reflection, and the confocal chord tangency discriminant. Generate
   orbits by this map, without using the author's final invariant formula.
2. Obtain resonant caustics by closure/root finding in a geometric rotation
   coordinate. Independently check every chord's tangency, reflection,
   closure, winding number, and primitivity.
3. Obtain consecutive tangent intersections by solving two linear tangent
   equations. Compute distances to both foci directly, and test phase
   dependence using high precision and diverse phases, including axes.
4. Derive exact algebraic identities from tangent intersections and
   elliptic-curve/Jacobi parametrizations only after independent geometric
   testing. Prefer rational/symbolic identities and checkable certificates.
5. Reproduce the original verifier normally and with Python -O, explicitly
   inventorying assertions removed by optimization; distinguish program
   completion from substantive checking.

## Challenges and falsification targets

* Primitive N=4,8,12,16 and a larger multiple of four; multiple winding
  numbers where the same elliptic caustic supports valid billiards.
* Axes ratios near one, moderate eccentricity, and high eccentricity;
  caustics near both admissible boundaries when compatible with resonance.
* Generic and axis phases; both foci; forward and reverse orientation.
* Periods not divisible by four and nonresonant caustics as negative
  controls; separately test deliberately perturbed caustics and geometries.
* Primitive versus repeated covers: do not accept a period claimed by
  merely repeating a smaller cycle; identify whether repetition can make
  an otherwise varying product constant.
* Degenerate or infinite tangent intersections, including antipodal
  adjacent vertices and limiting caustics, must be detected and excluded
  only under explicit hypotheses.
* Detect unsupported equivalences, a hidden closure condition, squaring
  artifacts, sign choices, and division by vanishing factors in proof.
* Record strongest verified result and exact gap; numerical evidence is
  not a proof and successful code execution is not proof validation.

## Artifacts and policy

All work stays in this family folder. No external communication, Git/ref,
PR, or publication changes. No third-party PDFs will be included. Deliver
independent code and stdout, exact derivations/certificates where feasible,
REPORT.md, UTC research log with checkpoint completion estimates, and a
safe SHA-256 manifest of complete deliverables.
