# Independent adversarial metric review

Verdict for the assigned family: **CLEAN**. The submitted general metric lemma
is correct for its exact hypothesis. It produces an actual continuous
rectifiable path in the exact original closed ball, with the claimed ambient
length bound `d(x,y)+4c`, for all centers, all finite nonnegative radii, and all
interior or boundary endpoints. The coefficient 4 is optimal for this abstract
hypothesis. No candidate modification is required for this family.

## Scope, inputs, and independence

PR 1033 / problem 11000026; immutable submitted head
`6322305d37b8131f034a1b4c3c5e861e4b04844f`. The substantive input examined was
`submitted/PROOF.md`, SHA-256
`20b303b8606302a73d4cd57d3ad184eb9c38ffd24dbe7c5539f093d4ce710fda`.
All eight submitted files were verified against `SUBMITTED_PINS.json` at the
beginning and end of this review.

The derivation was reconstructed from the exact submitted claim without reading
old `INDEPENDENT_AUDIT.md`, `ACCEPTANCE.md`, or other fresh-family artifacts.
The substantive Teichmüller theorem is assigned to a distinct fresh family;
its validity is expressly conditional here. The standalone artifacts below
contain the checkable argument rather than a conclusion copied from an earlier
verdict. No external individual was contacted. No candidate, original-file,
Git/main/index/queue, PR, release, or service state was mutated.

## Strongest verified result

One finite constant `c>=0` must work for every center and endpoint pair. For each
triple, only *some chosen minimizing segment* must obey

\[
 d(o,z)\le\max(d(o,a),d(o,b))+c.
\]

Under that hypothesis, the radial retreat amounts are
`alpha=min(c,d(o,x))` and `beta=min(c,d(o,y))`. When `R>=c`, the retreated points
have center distances at most `R-c`; the middle minimizing segment selected by
the hypothesis consequently lies inside the radius-`R` original ball. Radial
tails also stay in that ball. The ambient triangle inequality bounds their
finite concatenation by `d(x,y)+2alpha+2beta<=d(x,y)+4c`.

When `R<c`, the path through the center has length at most `2R` and meets the
claimed bound. This separate case is necessary because an inner radius `R-c`
would otherwise be negative. The submission includes it correctly.

[DERIVATION.md](DERIVATION.md) gives a full arclength parametrization, a direct
partition-sum proof of exact concatenation length, and a boundary-case table.
It covers `R=c`, `c=0`, `R=0`, `x=y`, collapsed radial or middle segments,
interior and boundary endpoints, and nonunique geodesics. The proof uses no
properness, completeness, compactness, global radial retraction, continuous
selection of geodesics, fellow travelling, thin-part assumption, or intrinsic
shortest-path existence. The intrinsic-distance inequalities follow by taking
an infimum over actual paths; attainment of that infimum is not claimed.

## Adversarial checks and incorrect extensions

[ADVERSARIAL_MODELS.md](ADVERSARIAL_MODELS.md) gives three exact examples.

1. A metric circle of circumference `C` has least uniform additive radial
   constant `c=C/4`. For a radius `(C-k)/2` ball, endpoints at ambient distance
   `k` have intrinsic distance `C-k`. Their excess is `4c-2k`, approaching
   `4c`. Thus no universal replacement coefficient below 4 can follow from
   this same hypothesis.
2. Every geodesic metric space has the multiplicative radial bound with factor
   2. A bouquet of circles of growing circumferences nevertheless has sphere
   endpoints at fixed ambient distance 1 whose shortest original-ball paths
   have unbounded lengths. Multiplicative control cannot replace additive
   control.
3. On a fixed flat cone of angle `pi/2`, the tip has radial constant zero, and
   each other center `p` has a finite additive constant `2d(p,tip)`. A sequence
   of centers and balls nevertheless has endpoint distance 1 and intrinsic
   distances tending to infinity. Pointwise finite center-dependent constants
   cannot replace the single constant uniform over all centers.

These examples are deductive constructions, not numerical tests. They test the
hypothesis distinctions without weakening the submitted target claim.

## Exact primary-question reconciliation

The official [Farb volume](https://www.math.uchicago.edu/~farb/papers/mcgbook.pdf),
printed pages 24-25 (zero-based PDF pages 30-31), was independently retrieved
and both complete pages were visually inspected. Page 24 defines almost
convexity by one path-length constant for same-sphere endpoints at distance 2,
uniform over positive radii, with the path staying in the original ball. Page
25 asks: "Is Teich(Σg), endowed with the Teichmüller metric, almost convex?"
The abstract result gives the distance-two constant `2+4c`. The all-center and
every-fixed-k statements are stronger consequences of the submitted bound;
that wording is not presented as a verbatim definition from Farb. No question
about a word metric, a wall metric, or genus-uniform constants has been substituted.

The unchanged primary PDF is in `sources/raw/farb_mcgbook.pdf`; source URL,
SHA-256, size, retrieval timestamp, and page locators are recorded separately in
[sources/SOURCE_PINS.json](sources/SOURCE_PINS.json).

## Actionables ordered by severity

There are **no mathematical repair requirements in the assigned metric family**.
The submitted proof already contains the necessary small-radius split and
handles degenerate segments. The fuller parametrization in this review is
verification support; adding it to the candidate is optional exposition.

Before promoting the *Teichmüller-specific* result, the other assigned family
must independently verify the actual-metric geodesic theorem and the precise
Lenzhen-Rafi input: fixed-topology finite `c_g`, all-center and all-endpoint
uniformity, the non-strict radial inequality on a minimizing segment, the
`(1/2)log K` normalization, and applicability without a thickness restriction.
This is the exact remaining conditional dependency, not a defect found in the
abstract deduction. This family alone does not decide publication novelty or
overall PR acceptance.

## Checkpoint and output integrity

The assigned metric-validation goal is complete: 100%. This percentage does not
measure Teichmüller-source verification, novelty, or overall PR completion.
`INPUT_PINS_INITIAL.json` and `INPUT_PINS_FINAL.json` record all eight input
checks. `RESEARCH_LOG.md` records timestamped progress. No empirical test suite
was needed: the claim and models were checked by explicit metric derivations.
