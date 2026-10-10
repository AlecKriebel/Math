# Independent adversarial audit: low degree rigid systems

Date: 2026-10-04. Target: numeric ID 4700001 / AMR-046-0001, inspected queue rank 635.

## Verdict

**PASS for the stated partial mathematics and the explicit unsolved conclusion. NOT a global resolution certificate.** No material mathematical defect was found in the frozen packet. A minor numerical-test hardening issue is recorded in `CORRECTIONS.md`; it does not alter the actual outputs or conclusions.

The frozen packet contains five completed approaches to the full five-real-parameter problem. The global upper bound of two remains unproved, and no rigorous three-cycle example was obtained. This audit verifies those existing claims; it is not a sixth proof-search approach, a novelty claim, or a reason to reopen the exhausted search budget.

## Exact input binding and scope

The original external `FREEZE_MANIFEST.json` has SHA-256:

`c1af53c8f215aff4236e2490d01a81d2502c82e36e6f9c36c5779b00df6972f4`

All eight listed frozen files match their byte counts and SHA-256 values. The complete file bindings are retained in `input-verification.json`. Frozen originals were not modified. The audit performed no repository remote mutation or outside communication. Numerical additions only corroborate the already-claimed constructions.

The audited target is the maximum number of isolated, finite planar periodic orbits of

    x' = -y + x(a + bx + cy + dx^2 + exy),
    y' =  x + y(a + bx + cy + dx^2 + exy),

for arbitrary real a,b,c,d,e. The audit does not discard nonhyperbolic cycles, assume all flows are globally finite, count center continua as limit cycles, or count infinity as a finite planar orbit.

## 1. Reduction and return-domain checks

The angular-speed identity and radial reduction were independently checked algebraically. The origin is the sole equilibrium because the two-dimensional coefficient matrix has determinant 1+F^2. Every other finite periodic orbit has positive radius and angular speed one.

The scalar finite-time existence domain is an interval: if two initial values generate finite solutions through a full period, every intermediate solution stays between them by scalar uniqueness, so it remains in a compact strip and continues through that period. Thus the intervals required by Rolle's theorem really lie inside the return domain; no global-existence hypothesis is being smuggled into the argument. Strictly increasing scalar maps cannot have a periodic point of minimal period greater than one. The positive fixed-point formulation therefore covers all finite planar periodic orbits of the target.

## 2. Schwarzian count for e=0

For nonzero d, the integral of 6d cos(theta)^2 times the positive squared first variation has strict sign d. The identity connecting this Schwarzian with the second derivative of h=1/sqrt(P') has the correct negative sign. Hence h is strictly convex or strictly concave on every relevant interval.

Four distinct real fixed points would create three distinct points with P'=1, which is impossible for this h. A positive periodic radius has the negative auxiliary partner -r(theta+pi), and zero is also a fixed point. Two positive solutions would therefore create five distinct real fixed points. This establishes at most one positive periodic orbit.

The hyperbolicity step also survives scrutiny: for a hypothetical positive nonhyperbolic fixed point, use its negative partner and zero. Rolle points in the two disjoint intervening intervals, together with the positive endpoint where P'=1, give three distinct intersections h=1. Thus a cycle, if present, is hyperbolic. This is stronger than merely bounding transverse sign changes and does not overlook tangent fixed points.

When d=e=0, the reciprocal equation is linear. The period integral excludes positive periodic solutions for a nonzero; when a=0, any positive solution has a neighboring family obtained by shifting the reciprocal initial value, so no member is isolated. The degeneration is correctly handled separately.

## 3. Complete b=c=0 classification

The harmonic coefficients of the unique periodic reciprocal-square solution were independently derived by solving its three linear coefficient equations. The positive-mean condition is essential. Algebra gives

    mean(z)^2 - amplitude(z)^2
      = (d^2 - a^2 e^2) / (4 a^2 (1+a^2)).

For a nonzero, strict positivity is therefore exactly -d/a>0 and d^2>a^2e^2. A positive periodic z gives a unique finite periodic radius, and coordinate conjugacy preserves the multiplier exp(-4*pi*a). The stated stability orientation, stable for a>0 and unstable for a<0, is correct even though it is opposite the origin's stability.

At positive-mean equality, the harmonic solution reaches zero; its reciprocal square root is unbounded and cannot be a finite cycle. At a=0, nonzero d gives unavoidable secular drift. With a=d=0, the positive K-family is nonisolated. These cases cover vanishing coefficients as well as both time/stability orientations.

The independent numerical checks include e=1.99,2,2.01 at a=0.5,d=-1. Their reciprocal minima have respectively positive, zero, and negative sign. Four independent homogeneous controls cover both stable and unstable cycles. These numerical checks corroborate the exact criterion; they do not replace it.

## 4. Epsilon-uniform two-cycle proof

The independent exact checker verifies every coefficient recurrence through order three, all initial/terminal cancellations, and the complete fourth-order coefficient integral. It reproduces

    Q(R) = pi R(-2 alpha + beta R^2 - R^4/2).

For alpha=1/2,beta=2, its positive zeros are sqrt(2-sqrt(2)) and sqrt(2+sqrt(2)), and the derivatives at those zeros are respectively positive and negative.

The use of analytic dependence and division by epsilon^4 is justified. For example, take initial R in [0.5,2.1], which contains both roots, and a containing strip [0.25,2.5]. The rescaled vector field is uniformly O(|epsilon|) on that strip. For sufficiently small |epsilon|, its period-integrated absolute bound is smaller than the distance to the strip boundary, so all those flows stay finite. Standard analytic dependence then applies jointly in epsilon and initial R on a common neighborhood. The first three return coefficients vanish identically there, making division by epsilon^4 analytically removable at zero. The implicit-function theorem and the one-R-derivative expansion follow on this common domain.

Positive simple roots persist for every sufficiently small positive epsilon. The multiplier expansion gives an unstable inner and stable outer hyperbolic cycle. Scaling r=epsilon R is a smooth transverse conjugacy for each fixed epsilon>0 and does not change these multipliers. All relevant radii remain positive and finite.

No value such as epsilon=0.12,0.10,0.07 has been proven below an explicit analytic cutoff. Those finite numerical examples remain nonvalidated controls. The theorem supplies at least two local cycles and no exclusion of additional distant cycles.

## 5. Global identities and the remaining obstruction

The logarithmic, reciprocal, Floquet, and pairwise identities were rederived. In particular,

    integral C r1 r2 = 2*pi*a

for distinct positive periodic solutions has the displayed sign, and the three-solution consequence has a strictly positive weight r2(r3-r1). For nonzero fixed-sign C this forbids the cancellation. For e nonzero, C is indefinite, and positivity of the weight alone does not exclude its weighted integral being zero. An arbitrary positive-weight example of cancellation would not itself construct three cycles, either. The frozen text correctly claims neither implication.

The parameter-a variation formula is positive on the positive finite-flow domain, but ordering return maps in a does not bound the number of intersections of any one map with the identity. The paper does not use this invalid shortcut.

The precise unclosed task is a uniform global two-cycle bound in the indefinite sector with nonzero (b,c), including nonhyperbolic cycles and return-domain boundaries, or a rigorously verified example with at least three finite isolated cycles. None of the audited identities closes that task.

## 6. Replay and independent numerical evidence

Both original scripts completed successfully. The parsed numerical replay is exactly equal to the entire recorded JSON, including parameters, sample arrays, roots, tolerances' refinements, and library-version fields. The bounded scan again has 24 parameter vectors, 31 radii each, maximum one bracketed root, and 227 incomplete sampled flows.

The independent checker contains 50 successful checks. It does not import either supplied script. Its exact symbolic checks add full recurrence coverage. Its numerical component uses a separately implemented fixed-step classical RK4 method with extended-precision arithmetic rather than the original SciPy DOP853 solver. All six refined roots from the three two-cycle controls have the expected stability signs; the largest independently computed return residual is below 4e-16. The four homogeneous controls have residuals below 8e-13. Step doubling is recorded for the two-cycle controls. Scaled displacement checks at epsilon=0.04,0.02,0.01 converge toward the independently verified Q at three fixed scaled radii.

These very small floating-point residuals are **not** rigorous error bounds. The audit does not certify interval enclosures, discover all roots, prove those finite numerical epsilon examples, or turn the 24-vector scan into exclusion evidence. Incomplete flow detection at radius 100 remains a computational cutoff rather than a mathematical blow-up certificate. Tangencies, close roots, unsampled parameters/radii, and return-boundary behavior remain outside the scan's power.

One implementation weakness is retained transparently: the original refinement comparison lacks an explicit equal-count assertion before zip. The audit adds that assertion and confirms that all original/refined lists actually have two roots. See `CORRECTIONS.md`.

## 7. Primary-source and provenance audit

The privately held 2020 and 2024 PDFs independently match the source hashes and byte counts in the frozen metadata. The relevant pages were freshly extracted and freshly rendered from those hashed PDFs, then visually inspected. Source PDFs, extracted text, and images are excluded from this audit package.

- Gasull, *Some open problems in low dimensional dynamical systems*, arXiv:2012.02524, printed/PDF page 3: Problem 1 matches the five-real-parameter target. The preceding discussion identifies the fixed-sign versus indefinite distinction. [Primary source](https://arxiv.org/pdf/2012.02524).
- Gasull, *From Abel's differential equations to Hilbert's 16th problem*, 2024, PDF page 31 / printed page 1372, equations (24)-(25): the two-cycle global maximum is explicitly retained as unknown. The displayed family includes the additional y^2 term; the 2020 reduction and five-parameter Problem 1 supply the relevant connection. The publisher page independently verifies the publication date, 28 September 2024. This is dated status evidence, not a comprehensive 2026 theorem search. [Publisher](https://link.springer.com/article/10.1007/s40863-024-00471-2).
- Gasull, Prohens, Torregrosa, *Limit cycles for rigid cubic systems*, 2005: the publisher abstract says uniqueness for two classified families and at least two cycles in a subfamily of the third. It does not state the missing global upper bound. The DOI reader failed on the first attempt; the indexed publisher article then supplied the abstract. The full 2005 paper was not audited. [Publisher](https://www.sciencedirect.com/science/article/pii/S0022247X04006158).

A bounded title/cubic-rigid/maximum search with recent-year terms did not locate a verified later full resolution. This does not establish that no later result exists. The live catalogue wording, raw dataset corpus hashes, historical repository-readiness checks, and the complete bodies of all neighboring works in `SOURCE_GATE.md` were not independently revalidated in this mathematical audit. Those provenance claims retain the frozen packet's own stated inspection limits; no stronger certification is implied.

## Acceptance boundary

The packet is suitable to describe as an independently checked **unsolved research attempt with rigorous partial results and nonvalidated numerical controls**. It is not suitable to describe as a solved target, a global upper-bound proof, a certified no-three-cycle computation, an explicit validated finite-epsilon construction, or a novelty-certified contribution. No mathematical rewrite of the frozen artifact is required. Preserve the original and attach this audit and its minor test-hardening note without silently rewriting history.
