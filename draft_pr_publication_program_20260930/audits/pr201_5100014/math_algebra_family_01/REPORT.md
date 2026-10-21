# Independent exact algebra and computational reproduction audit

Problem5100014, k303,a, original candidate SHA256
`e48aa989fb9282d09fdf58e7e4f6eee78e757ff0686f4cc35dc691e21f3d1fd3`.
Audit family: independent physical construction and exact Euclidean algebra.
Prepared2026-10-16 UTC. No original, shared queue, Git state or external
communication was modified. All outputs are confined to this audit directory.

## Assessment

No algebraic or computational counterexample to the **primitive-period**, signed
area, strictly nested nondegenerate confocal-ellipse assertion was found.
The original exact programs and review receipt reproduce byte for byte under
the specified existing Python3.14/SymPy1.14/mpmath1.3 software environment.
The independent physical construction corroborates all primitive windings for
N=6,10,14,18,22 across four aspect ratios, arbitrary and exterior sample M,
and sampled phase changes. These are finite high-precision checks, not interval
certificates or a general proof. The all-N flag-curve argument and its credited
published area-product input require the separate proof/source audit.

Two findings must be retained in any promotion:

1. Least period is indispensable. An exact counterexample below disproves the
   every-M assertion if an odd primitive orbit may merely be repeated to reach
   a traversal count congruent2 mod4. The candidate explicitly excludes this.
2. The original review uses Python `assert`. Under `-O`, its printed PASS and
   counters1757/26568 persist with **no assertion conditions enforced**. Both
   deliberately false algebraic and numerical probes are accepted in that mode.
   The normal replay enforces the checks and passes. New audit checks use
   explicit exceptions and reject false checks in both modes.

## Independence and exact target

The parent received the mechanism freeze at2026-10-16 05:40:33 UTC, before any
candidate code, proof or favorable review was read. Initial persistence failed
because the filesystem was full. The concise freeze was saved after recovery;
RESEARCH_LOG and FAILURE_DIAGNOSTICS retain that sequence. Before candidate
inspection, an explicitly messaged correction distinguished inner-caustic
tangency (which generates P) from outer-boundary tangents (which define P').
The two exact N6 arbitrary-M controls were derived and run normal/-O before
candidate inspection. The physical construction was implemented independently;
candidate reading began after its mechanism and exact low-N controls were
fixed, while the first numerical sweep was running. Its later negative-control
threshold adjustment and diagnostic failure are retained explicitly.

The primary v11 text was read directly, not through an authored sibling report.
Section2, printed p.3, equation1 explicitly makes **all polygon areas signed
shoelace areas**. Section3.4 and Table4 p.6 give k303,a as A'A'_M, N≡2 mod4,
all M, with proof status '?'. P' is formed by intersections of successive
tangents to the **outer** ellipse at the Poncelet vertices. The pedal feet are
perpendicular projections onto those tangent **lines**, including exterior M.
The target concerns neither caustic contact points nor feet on billiard chords.
The imported source statement's traversal/least-period interpretation is
therefore material; the original candidate explicitly says primitive period.
The v11 text itself does **not** spell out "primitive" or "least period": a
full-text term search found no such wording, nor a star/winding/repetition
discussion. Thus the original SOURCE_AUDIT overstates literal source wording
when it calls primitive period an explicit printed-row condition. Least period
is a necessary interpretation, supported by the counterexample here, and must
be stated as such. The candidate's inclusion of primitive stars is supported
by its mechanism and computations, while the source row does not enumerate
their winding scope. This is a scope-interpretation caveat, not a demonstrated
counterexample to the primitive candidate.
N=2 cannot occur here: a two-bounce billiard path is a diameter through the
center, which cannot be tangent to a strictly interior nondegenerate centered
elliptical caustic. The first admissible primitive period is therefore6.

## Exact independent constructions

`exact_independent_controls.py` verifies, using direct two-by-two line solves
and direct perpendicular projections, both axis-symmetric physical hexagons
for a=2,b=1,lambda=4/9. It verifies every boundary point and caustic tangent
chord, every foot's line membership/perpendicularity, orientation reversal,
and triple-traversal area scaling. With M=(m,n), the products are exactly

    A' A'_M = 40(m²+n²+9)/9.

The individual areas agree with the original outputs, but this equality was
established independently before reading them. A discarded speculative
coefficient guess is recorded as a failed hypothesis, not counted as evidence.

`extended_exact_controls.py` generalizes the two axis phases algebraically.
For a,b>0, set t²=b(2a+b) and lambda=a²b²/(a+b)². The physical hexagon begins

    (a,0), (a²/(a+b), bt/(a+b)), (-a²/(a+b), bt/(a+b)),

and is completed by central symmetry. Polynomial reduction modulo
t²−b(2a+b) verifies its boundary and tangency constraints. Its outer tangents
are X=a and ±bX+tY=b(a+b), with their opposites. Direct foot-area calculation
and semiaxis swap for the other phase give the common exact expression

    ab(a+2b)(2a+b) [ (a+b)²+m²+n² ] / (a+b)².

This is an exact arbitrary-semiaxis, arbitrary-M **two-phase** result; it does
not establish constancy for all intermediate phases.

For an exact excluded case, let a=2,b=1 and

    lambda=(8sqrt(13)−20)/9,
    alpha=2(sqrt(13)−1)/3, beta=(4−sqrt(13))/3.

Two physical three-period phases are

    (2,0), (-alpha, sqrt(1−alpha²/4)), (-alpha,-sqrt(1−alpha²/4));
    (0,1), (-2sqrt(1−beta²),-beta), (2sqrt(1−beta²),-beta).

Every boundary and common-caustic equation is checked symbolically. For fixed
M=(1,2), traversing each triangle twice gives nominal N=6 products

    (886+218sqrt(13))/9,    (-164−172sqrt(13))/9.

Their difference is `(350+130sqrt(13))/3`, exactly nonzero. This falsifies an
unrestricted repeated-traversal reading. Odd repetition of an eligible
primitive even orbit instead scales both signed areas by the repetition
factor and preserves constancy; a triple traversal of primitive6 is checked.

## Independent physical phase sweep

`physical_phase_checks.py` does not import a candidate formula or elliptic
parameterization. At each boundary point it solves the two tangent contacts
on the caustic from a normalized unit-circle intersection; it selects the
forward chord and solves its second intersection with the outer ellipse.
A bisection in lambda imposes rational closure from an unwrapped geometric
angle advance. It then solves each consecutive pair of outer tangents and
computes direct Euclidean pedal feet and signed shoelace areas.

At85 decimal digits, normal and optimized runs have identical mathematical
rows. The finite scope is:

- 56 primitive family cases: every coprime winding `1≤k<N/2` for
  N=6,10,14,18,22, at a/b=1.0001,1.3,2,5, b=1.
- Five physical starting phases and four fixed points per case: origin,
  (0.37,−0.81), exterior (17,−23), and a focus; 1120 target product samples.
- One additional eligible repetition case N18,k3, plus direct exact
  reversal and triple-traversal controls.
- Seven excluded parity/odd-period controls and six even repetitions of
  odd periods. The latter all vary; their largest relative phase changes
  range down to1.71455e−5, still vastly larger than numerical residuals.
- An N10,k3 star has positive and negative pedal areas as an exterior M
  crosses a numerically located quadratic zero near M=(4.07993829748,0).
  At three phases the area residual at this numerical root is below3.12e−72;
  values1% below and above have opposite signs. This is a numerical zero
  diagnostic, not an exact or interval certificate for that location.

Maximum relative target product spread is1.244e−66; maximum closure error is
2.157e−65. Explicit exceptions enforce a1e−45 tolerance, comfortably above
roundoff and below observed negative-control variations. Boundary/chord
tangency, foot incidence and perpendicularity are also checked. The source's
signed convention is necessary for interpreting the negative star-pedal
values; zero areas cause no division or failure in these constructions.

## Original artifacts, manifests and counts

The archived original contains24 files totaling54661 bytes, matching intake.
All14 entries in FROZEN_MANIFEST match both hash and size. All6 review-manifest
entries match, and its candidate/author-manifest references are correct.
The original author stdout files (904 and139 bytes) reproduce byte for byte
in normal and optimized runs. The review JSON receipt also reproduces byte
for byte in both modes, including maximum scaled error2.0241020051e−79.

The exact counter1757 is seven symbolic checks plus finite modular/incidence
checks through N1002 and excluded parity through N1000. These finite counters
do not independently prove genus-one geometry. The numerical counter26568
comprises378 each of product, pedal/original-area ratio, and two reversal
checks, plus12528 outer-line incidence,6264 foot incidence,6264 foot
perpendicularity. These groups sum correctly. The original checker uses its
canonical elliptic parameterization; the new physical closure computation
provides a materially different geometric control.

`turn1_exact.py` contains zero assertions: it calculates/prints expressions.
`turn1_generic_six.py` has one closure assertion and prints the other results.
The review checker has two assertion sites, inside `ck` and `close`; all
their compiled assertion opcodes disappear at optimization1. The separate
false-input probe documents this directly. Thus normal replay is evidence
for the recorded conditions; optimized replay is an output-reproduction and
assertion-stripping diagnostic only. It must never be reported as1757/26568
optimized enforced checks.

## Strongest verified result and exact remaining gap

Verified here: exact two-axis N6 formulas for arbitrary real M and arbitrary
positive semiaxes; exact scope counterexample for twice-traversed odd orbits;
exact reproduction of all original executable outputs, receipts and manifests;
finite independent physical corroboration of sampled primitive target
families, stars, extreme points and signed-area behavior; correct attribution
of optimized assertion enforcement. No defect in the displayed elementary
algebra or finite controls was found.

Not established by these computations: the universal all-N/all-phase theorem,
the complex flag-curve pole argument, full applicability of the published
AA' theorem, or historical novelty. The original proof's universal mechanism
is not replaced by a finite sweep. In particular, its common-tangent flags,
quotient pole locations and simple-pole cancellation remain proof obligations
for the independent geometric audit. No circular, hyperbolic, degenerate
caustic, nonprimitive odd-repetition or unsigned-union-area extension is
promoted by this report.

## Reproduction and safe output

Use the existing interpreter, with no installation or copied dependencies:

    /opt/homebrew/opt/python@3.14/bin/python3.14 -E -S -B -P run_all_checks.py

Run it in this report's directory. It reruns all mathematical scripts and
original replays in both modes, captures failures and UTC timing in
fresh_reproduction, and raises on any unexpected result. Existing completed
receipts are retained in this folder. The shared software path is inserted
explicitly; source papers, full source text, dependency trees and private
caches are not copied here. AUTHORED_OUTPUT_MANIFEST.json lists only safe
authored scripts, notes and generated check receipts, excluding itself.
