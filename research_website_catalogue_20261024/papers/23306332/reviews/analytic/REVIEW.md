# Analytic review: Nonunique nearest stable complex quadratics

**Analytic verdict: the four mathematical claims pass this lane under their
stated conventions. No substantive proof defect or central mathematical gap
was found.** Specific ancillary historical attributions have bounded original
source access gaps. This report gives no publication, priority, firstness, or
present-day openness clearance.

Reviewed work: Alec Kriebel, *Nonunique nearest stable complex quadratics*,
Zenodo record 23306332, version 1.0, published 11 October 2026,
DOI `10.5281/zenodo.23306332`. The actual six-page PDF and complete current
TeX were read. All six PDF pages were individually rendered and visually
inspected. The PDF SHA-256 is
`6439bda84f32d9a5ac1680e184975df159f51f8c7e44e609fa873dfa8ae78e1f`;
the verification ZIP SHA-256 is
`2fc6b62d67ab6681c36f7d3806db549073a3f0b2e0d039817f997fab9eb96dee`.

## Claim assessment

| Claim | Assessment and controlling evidence |
|---|---|
| C1: monic complex stable set fails prox-regularity; arbitrarily near zero there are unstable targets with multiple attained global nearest stable points, for every fixed real SPD metric | Verified. The simple active-root derivatives supply actual proximal normals for each fixed path point. Their limit violates every local quadratic support inequality at zero. Continuity of the complete quadratic radical gives closure and attainment. The original PRT2000 Theorem 1.3(a),(k), including its finite-dimensional weak-closedness condition, supplies the global projection conclusion. |
| C2: corresponding full exact-degree statement at `(ell,a,b)=(1,0,0)` | Verified. Both real leading-coefficient directions are differentiated explicitly. The nonzero-leading domain is locally closed. A compact ball within it permits the closed-set projection theorem; the R/3 versus 2R/3 comparison excludes every stable competitor outside the ball and its boundary, proving global attainment and coincidence of minimizers. |
| C3: whole abscissa epigraph fails set prox-regularity in monic and full degree, in every fixed coefficient/height SPD metric | Verified. Scaled smooth normal covectors `(n_t,-1/gamma_t)` tend to `(n_0,0)`. Cubic support again exceeds quartic squared displacement. Covectors are distinguished correctly from their metric representatives, including mixed height/coefficient metrics. |
| C4: monic abscissa is function prox-regular at zero relative to each finite limiting subgradient in the real Euclidean coefficient metric | Verified. The ray/zero subdifferentials of Phi are computed directly; a real smooth diffeomorphism gives exact coefficient subdifferentials. Bounded finite subgradients force nearby discriminants onto the negative ray. Convex normal support and the exact quadratic discriminant remainder give a common local lower quadratic bound, with strictness after increasing curvature. |

The full independent derivation, including every radical, real derivative,
normal support estimate, neighborhood quantifier, and closure/localization
step, is in [INDEPENDENT_DERIVATION.md](INDEPENDENT_DERIVATION.md).

## Scope and boundary checks

The source uses complex coefficients and closed-left-half-plane stability;
imaginary-axis and double roots are included. The monic metric is any fixed
real SPD matrix on `(Re a, Im a, Re b, Im b)`, with arbitrary cross terms.
Full degree has six real coordinates and excludes ell=0. Height metrics may
mix height and coefficient coordinates. Singular, indefinite, varying
metrics, arbitrary norms, nonlinear parameter metrics, general degrees, and
a real-only classification are outside the claims.

The exact chart is `x>=0, U>=0, V^2<=x^2 U`, where
`a=x+iy`, `U=Re b+y^2/4`, `V=Im b-xy/2`. Both nonnegativity inequalities
matter at degenerate boundaries. In the real monic slice this becomes the
convex orthant, whose nearest point is unique for every SPD metric. Thus
the complex witness is not a real-quadratic counterexample.

There is no explicit unstable target/minimizer triple in the manuscript.
That omission is compatible with its stated existential theorem: PRT's
closed-set equivalence yields non-single-valued global projection in every
neighborhood, and finite-dimensional closure/compact localization yields
attainment. A stable target has only itself at distance zero. The proof
therefore establishes ties among all complex stable competitors, rather than
just competing real local minima.

## Primary reference interfaces

Lewis2003 Section 8, printed pp166-168, explicitly takes complex polynomials,
orthonormal real basis `{z^k,i z^k}`, and the stable monic set
`z^(n+1)+p` with root real parts at most zero. Quadratics correspond to n=1.
Its final question asks set prox-regularity. Both the author version and the
publisher's printed pp104-106 of the OWR contribution were read; the short
Question 1 itself omits coefficient field, normalization, and metric. The
manuscript's qualified complex interpretation is accurate.

PRT2000 Definition 1.1, Proposition 1.2 and Theorem 1.3(a),(k) were checked
in the actual original, with selected relevant proof bodies. The theorem
requires a closed set and base point in it; local relative weak closedness
for (k) is automatic in finite dimension. Its projection is the global
metric projection. The monic set satisfies these hypotheses; full degree
uses the compact clipped set and then proves equality with the original
global minimization problem near the base.

PR2010 Definition 1.1 localizes base points, function values and subgradients
near a specified finite subgradient. The paper's scalar and coefficient
estimate is uniform on a stronger local set and supplies the requested
strict inequality using curvature M+1. PR2010 p205 identifies the epigraph
normal `(v0,-1)`, which is different from the horizontal limiting covector
used to disprove whole-set epigraph prox-regularity.

One non-load-bearing citation imprecision should be retained as a caveat:
PR2010 Theorem 3.1 is a sufficient prox-regularity composition theorem under
C^2, horizon-CQ and outer-function prox-regularity hypotheses; it does not
state an unconditional exact subdifferential equality. The manuscript's
explicit two-sided diffeomorphism/lower-support argument independently
establishes the equality it needs, so no central proof step depends on
misreading that theorem.

Orban de Xivry's definitions, nearest-system formulation (2.3), complex
monic coefficient formulation (4.14), coefficient objective (4.16),
reflection-coefficient comparison and weighted objective discussion were
read in bounded sections of the 214-page thesis. These establish relevant
earlier complex coefficient approximation work; they do not certify absence
of the present local theorem from all literature. Burke-Overton and
Burke-Lewis-Overton introductory conventions and the related Kirillov-Overton
real-quartic Whitney-umbrella geometry were also checked. No full novelty
audit is claimed.

The actual original Cross, Moses-Liu, and Bottema bodies were not available
for body-level checking in the supplied primary cache. Specific statements
about Cross's example and Moses-Liu's recognition of global nonuniqueness
are therefore not independently certified by this lane. Kirillov-Overton
supports related Bottema credit, but cannot replace the original body.
These ancillary access gaps do not supply a counterexample or central
mathematical gap, and they prevent a firstness/present-openness conclusion.

## Independent evidence and reproducibility

Fresh [independent_exact.py](evidence/independent_exact.py) does not import
submitted code. It completed **4305 exact rational assertions**, including:

- 625 complex-root chart cases with stable, unstable, repeated, and
  imaginary-axis examples;
- all six real implicit-root derivative components at 64 nondyadic rational
  path parameters, including both leading-coefficient directions;
- fixed mixed SPD metric controls in dimensions 4, 5, 6 and 7, with exact
  support/metric inequalities and an independent tilted height-normal
  representative;
- exact radical inequalities evaluated by sign-aware squaring, 609 full
  coefficient supports, exact inverse/differential identities, and both
  sides of the negative ray;
- rejected variants omitting either necessary stability nonnegativity
  condition, omitting the quadratic discriminant correction, and using
  half the required adverse curvature.

The independent result is [independent_exact.json](evidence/independent_exact.json).
These finite controls strengthen falsifiability and expose sign/branch/
curvature errors. They do not replace the proof of an infinite quantifier.

Both current submitted mathematical scripts were read completely and
statically before execution. Byte-identical copies were placed in the owned
`quarantine/` folder and run using isolated Python there. Both exited zero:
the exact helper executed 2005 rational assertions; the 90-digit Decimal
helper reported 45 boundary cases and 1200 coefficient support cases.
The Decimal calculations are not interval-certified. Their authored status
literals are not independent mathematical conclusions. The detailed command,
hash, exit and output receipts are in
[reproduction-receipt.json](evidence/reproduction-receipt.json).

No expected-output file, authored priority/provenance memorandum, sibling
review conclusion, or historical acceptance judgment was used as proof.
Allowed scope locator/claim-map/read-ledger files were consulted to locate
current sources and original primary bodies. Attempts to add a distinct
function-audit descendant were rejected by the team concurrency limit; this
report remains a single analytic lane, not a claim of independent human
peer review or a substitute for the parent's separate adversarial gate.

## Custody, strongest verified result, and remaining gap

The before/after inventories confirm **all 17 original source files are
unchanged**, including the published PDF, ZIP and all 12 regular extracted
package members. Opaque priority/provenance and expected-output files were
hashed for custody without reading their bodies. Only this analytic review
folder was written. No repair, source edit, Git operation, release,
communication/outreach, Sheet, site, browser or deployment action was taken.

The strongest verified result is C1-C4 exactly as scoped above. There is no
remaining central mathematical gap identified by this lane. The remaining
gap is bounded historical-body/priority coverage and a minor nonessential
composition-citation imprecision. Full publication decisions and any public
wording about historical novelty belong to the parent review process.

The timestamped [RESEARCH_LOG.md](RESEARCH_LOG.md),
[primary-read-ledger.json](primary-read-ledger.json),
[reader-manifest.json](reader-manifest.json),
[source-custody-before.json](source-custody-before.json),
[source-custody-after.json](source-custody-after.json) and
[SEAL.json](SEAL.json) preserve the audit trail. Completion of this analytic
lane: **100%**.
