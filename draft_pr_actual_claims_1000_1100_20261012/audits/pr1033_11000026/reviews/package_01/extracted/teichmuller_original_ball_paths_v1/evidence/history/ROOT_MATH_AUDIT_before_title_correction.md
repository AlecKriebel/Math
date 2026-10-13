# Root combined mathematical audit of PR #1033

The complete scoped theorem passes the root derivation and two materially
independent fresh reviews. Priority remains a separate pending obligation.
The audited head is `6322305d37b8131f034a1b4c3c5e861e4b04844f`, problem
11000026, Farb Question 3.5. This is an AI mathematical audit, not conventional
human peer review or a proof-assistant certificate.

## Exact quantifiers and conclusion

For each fixed closed oriented surface of genus g >= 2, there is one finite
c_g >= 0, independent of center, radius and endpoints, such that every
closed ball in the actual half-log Teichmüller metric contains a continuous
rectifiable path joining any two of its points with length at most their
ambient distance plus 4c_g. Consequently distance at most k admits length
at most k + 4c_g in that original ball; k = 2 answers the exact question.
No genus-uniform constant, optimal Teichmüller constant, convex geodesic ball,
thickness hypothesis, or replacement metric is asserted.

## General metric deduction

Suppose a geodesic metric space has one c >= 0 such that, for all centers o
and endpoints a,b, some minimizing segment between a,b has radial distance
at most max(d(o,a),d(o,b)) + c everywhere. For R < c, the radial path through
o lies in the closed ball and has length at most 2R <= d(x,y) + 4c.
For R >= c, retreat x and y along minimizing radial segments by
alpha = min(c,d(o,x)) and beta = min(c,d(o,y)), obtaining a and b.
Both new endpoints have radial distance at most R - c: if the original
radial distance was below c the new endpoint is o; otherwise subtract c.
Choose the hypothesized a-to-b segment. Its radial maximum is at most R.
The radial end pieces also lie in the original closed ball. Their
concatenation has length

`alpha + d(a,b) + beta <= d(x,y) + 2alpha + 2beta <= d(x,y) + 4c`.

Parameterizing each piece by arclength and pasting at its matching endpoint
produces an actual continuous rectifiable path. Metric length is additive
over the pieces. Zero-length pieces, x = y, a = b, R = c, R = 0 and c = 0
all satisfy the same construction, with the constant path when appropriate.
There is no infimum-attainment assumption about intrinsic distance, no
continuous selection of geodesics, no properness/completeness requirement
and no assertion about every possible minimizing segment.

The independent metric family derived the same result before reading old
acceptance records. Its exact circle model shows that coefficient 4 is
optimal for the general implication: for circumference C, the least global
radial excess constant is C/4, while endpoints at ambient distance k in the
proper closed arc-ball of radius (C-k)/2 have intrinsic distance C-k.
The excess C-2k tends to 4c. This does not establish optimality in
Teichmüller space. Its unbounded circle bouquet and cone models also expose
why a multiplicative bound or constants depending on the center cannot be
silently substituted for the single global additive constant.

## Exact Teichmüller source interface

Lenzhen–Rafi, *The shape of a Teichmüller geodesic*, JDG 88 (2011),
Theorem 15 and its proof supply one finite K >= 1 depending only on the
fixed topology, with

`Ext_z(curve) <= K max(Ext_a(curve), Ext_b(curve))`

for every simple closed essential curve and every point z on the minimizing
Teichmüller segment from a to b. Their topology-only convention and actual
proof were checked across thick, thin and annular cases; no lower bound on
injectivity radius or curve-dependent constant is acquired. The corresponding
Theorem C/17 radial interpretation agrees with a direct derivation.

Using Kerckhoff's formula in the half-log metric, divide by the positive
Ext_o(curve), take half the logarithm, and then take the supremum over
curves. The elementary inequality sup(max(f,h)) <= max(sup f,sup h) yields

`d(o,z) <= max(d(o,a), d(o,b)) + (log K)/2`.

This gives c_g = (log K)/2, a non-strict bound at the original closed-ball
boundary. No maximizing measured foliation needs to be selected. The
geodesic and normalization interfaces are also explicit in Fortier Bourque–
Rafi, arXiv:1606.05170v3, Section 2 and equation (2.2). The independently
retrieved original Farb book, printed pp. 24–25, specifies intrinsic path
length in the original ball and radius-independent bounds, so the constructed
path meets its literal target.

The source family checked four fresh primary PDFs and nineteen critical
rendered pages, their hashes/versions and exact quantifiers. Its report notes
two upstream presentation slips in Lenzhen–Rafi: a variable switch in the
Theorem 17 proof and a missing orientation qualifier in Definition 12(3).
The complete Theorem 15 proof supplies the appropriate directional choice
and reverses time when necessary, and the direct supremum derivation avoids
the former slip. Neither yields a missing premise in the used theorem.
Foundational published Teichmüller results remain external dependencies;
the audit does not reprove their entire literature.

Known nonconvex Teichmüller balls are consistent with a three-piece path.
Petyt–Zalloum's 2026 wall-space theorem and quasi-isometry discussion do not
contradict the exact-metric assertion. These comparisons check mathematical
compatibility, not priority or current worldwide openness.

## Evidence, independence and remaining gate

The root read the entire submitted proof and the full fresh metric and
source reports/derivations before combining their obligations. The first
family initially had the exact source application as a conditional premise;
the independently derived second family discharges that premise. Old PASS
labels are not premises. The root separately derived the retreat argument
and checked the original question and Lenzhen–Rafi interface.

All eight original authored Git files are preserved and checked against
the exact head and full tree, not merely selected file matches. No original
executable was submitted; the proof is theoretical. New abstract models are
checkable derivations, not an invented replay of missing historical code.
Raw third-party bodies remain private under source raw directories. Authored
source locators/hashes and new reviews are preserved separately.

No actionable mathematical repair remains. A future note should spell out
the curve-supremum derivation for clarity. The result's novelty must now be
tested against exact prior answers, general ball-path lemmas and later
citations of the 2011 theorem. No preprint publication, merge or substantive
novelty promotion has yet occurred for this PR.
