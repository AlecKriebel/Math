# Research log: 2306072 / Function Theory 6.72

All times UTC, 2026-10-04. This is one substantive proof-attempt response ending in a complete candidate, not five nominal retries. Completion estimate: 95% toward a reviewable research result; the candidate proof and finite controls are complete, but independent mathematical review and historical priority remain unsettled. This estimate is not a probability that the proof is correct.

## 09:45–09:53: source and status gate

- The catalogue URL returned HTTP 403. Recovered the exact two-part question from Hayman–Lingham arXiv:1809.07200v2, printed p.143 / PDF p.144; visually checked the page and Update 6.72.
- The pinned upstream problem and research records were inspected. The latter was only an OPEN-TRIAGE report saying no definitive resolution had been located. It is not proof of present-day openness.
- Read the live repository instructions and queue. The selected row was queued at 0/5; no selected attempt directory or matching PR was found. No exact-ID related-target group was listed.
- Read Duren (1981), including the exact Schiffer differential and the unique trajectory at a simple pole. Located Hibschweiler (1995), whose indexed primary abstract and theorem statement establish only eventual monotonicity. That previously known partial is not a global answer.

## Approaches considered within this response

### Geometric necessary conditions

Tried to combine increasing modulus, the pi/4 radial-angle bound, and an asymptotic half-line. These are too weak on their own: a smooth polar arc can meet all three and reverse its argument. This route was not promoted to a counterexample because it supplies no supporting functional.

### Existing special extremals

Examined point-evaluation, derivative-evaluation, and straight-slit families in the primary literature. Their established monotonicity cannot be extended to arbitrary continuous linear functionals without an additional argument. The rational straight-slit examples were treated as controls, not new results.

### Analyticity near infinity

The local analytic trajectory at a simple pole explains eventual monotonicity and supplies a natural-coordinate parametrization. An infinity-only argument does not forbid bounded turning points. Hibschweiler's prior theorem is compatible with the candidate below.

### Perturbation of an exposed Koebe extremum

Around the functional a2, perturbations by i·epsilon·a3 and i·epsilon·a4 separately give first-order radial-angle profiles t^2/3 and 2t^2−2t^4/5, respectively, with no sign reversal at the chosen test points. Their combination a4−3a3 gives t^2−2t^4/5, which changes sign inside the Koebe slit's parameter interval. This yielded the candidate mechanism.

### Quantitative extremality and trajectory identification

Replaced the formal perturbation by a uniform statement for every actual global maximizer. Coefficient bounds plus the area theorem control its first coefficients; the odd root transform controls its value and derivative at −2/3, putting the actual slit tip inside radius 3/10. Rouché inversion then produces an omitted trajectory segment wholly outside radius 25/81. Exact remainder estimates certify opposite angle signs at t=1 and t=7/4 for epsilon=10^−24.

## 09:54–10:05: candidate derivation and verification

- Derived the complete coefficient functional and its exact rational Schiffer differential.
- Eliminated the need to assume unique or differentiably chosen maximizers.
- Proved the finite-tip gate instead of presuming the formal trajectory remains omitted.
- Made the perturbation parameter explicit and bounded all analytic remainders.
- The signed radial angle changes sign; its magnitude vanishes between positive endpoint values. This covers both conventions for the second question.
- Ran 56 standard-library exact checks successfully, including rejected a3-only, a4-only, zero-perturbation, and oversized-error controls.

## Remaining verification and scope

No mathematical gap is knowingly left in the candidate proof. It depends on the stated classical compactness, coefficient, area, and support-slit/Schiffer theorems. The program does not verify those theorems or their application. An independent reviewer should especially challenge the differential's sign and coefficient extraction, the uniformity over maximizers, the endpoint-distance inequality, the natural-coordinate branch, and the continuation from the simple pole to the actual omitted slit.

No first-resolution or historical-priority claim is made. No individual was contacted. No remote repository change is part of this frozen research package.
