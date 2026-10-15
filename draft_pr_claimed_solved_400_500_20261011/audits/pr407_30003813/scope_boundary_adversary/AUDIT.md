# Independent target-scope and boundary audit of PR 407

Reviewed frozen head `e3f8838a8eac68bbd186fc0234ac2e2a49194626`, problem
30003813 / OWR-16164-005. The frozen exact-head queue gate is
`claimed_solved`, 1/5 author attempts. This audit consumes no author
proof-search attempt and does not determine historical priority.

**Verdict: PASS for the precise literal-scope mathematical claim.** No
mathematical blocker or required repair was found. Each coefficient of the
signed adjacent-sum polytope's h-star polynomial counts exactly the
permutations in the stated descent class, weighted by the descents of
`alpha composed with inverse(sigma)`, for every positive dimension, every
sign sequence, and every permitted natural labeling alpha. The
independence of alpha is equality of distributions, not equality of every
individual term's exponent.

## Independent target authentication

All 13 frozen public files were read, and their size, SHA-256 and Git blob
identities were independently recomputed against `SOURCE_RECEIPT.json`.
They belong to native immediate subtree
`b4ee3347c6587b07348b836858c29d7812ebe421` under the declared frozen head.
The source packet, original mathematical proof, original audit, and
executable checkers were preserved without modification.

The official original [OWR report](https://publications.mfo.de/bitstream/handle/mfo/3645/OWR_2018_23.pdf?isAllowed=y&sequence=1)
was independently retrieved as an HTTP-200 PDF. Its 1,293,303 bytes have
SHA-256 `28cc8b4c6c445cee7def413c46dac52011589b294c4f0578251d78167295526c`.
I read the complete Josuat-Verges/Ayyer/Ramassamy abstract on printed
pages 1408-1410 and inspected a fresh rendering of printed page 1410
(PDF page 30). Native source custody, text extraction and rendering are
private evidence; third-party PDF bytes are not proposed for redistribution.

The original target is the cube with, for each index 1 through n-1, a
chosen weak upper or lower adjacent-sum inequality. It neither introduces
a closing edge from n to 1 nor expressly requires a statistic on cyclic
orders. Its surrounding discussion does motivate refinements using cyclic
orders for a related family. Therefore a cyclic-order refinement may be
interesting, but it is not an explicit condition in this printed question.
The claimed permutation interpretation is a defensible answer to the
literal request, with the existing scope qualification retained.

This is a scope judgment about an open-ended question, not proof that
every broader intention of its original authors has been addressed.
The submission correctly declines a cyclic-order-specific result, a new
swap statistic, completion of the broader research program, novelty, or
historically certified closure. These limitations must remain in any
promoted description. This audit does not turn them into positive claims.

## All-dimensions adversarial proof assessment

1. Reflecting only the even coordinates sends each source inequality to
   precisely the indicated oriented path comparison. I separately checked
   all four parity/sign cases. Neither constant signs nor a special family
   replaces the arbitrary sign sequence. The linear part is integral
   diagonal with determinant plus or minus one, and the translation is
   integral. On dilates the translation must be m, as correctly specified.

2. Any path orientation is acyclic, so its transitive closure is a poset.
   A rank permutation is order-preserving exactly when its adjacent
   descent set equals the declared D. This imposes every generating edge,
   and therefore all transitive comparisons. The deterministic minimal
   vertex procedure constructs a permitted alpha; no unresolved labeling
   search is hidden in the formula.

3. Each extension region is the full-dimensional simplex whose vertices
   are zero and the integral suffix indicators. Every point is captured
   by sorting coordinates and breaking ties with a natural labeling.
   Convexity then proves that the union is exactly the convex hull of
   those integral vertices. This establishes integrality and full dimension
   before the Ehrhart numerator is used; the argument does not assume
   those properties merely because the polytope is defined by integer
   inequalities.

4. The lexicographic key `(coordinate,natural label)` gives a unique
   extension. Its equal-value blocks have increasing labels. Conversely,
   strict growth at every label descent ensures every equal-value block
   has no adjacent descent and thus is increasing in labels. This proves
   both directions of the boundary partition, including nonadjacent ties,
   cube endpoints, and intersections of multiple adjacent-sum hyperplanes.
   There is no ignored boundary multiplicity.

5. Removing the number of preceding mandatory strict steps gives exactly
   a weak sequence in `[0,m-d]`. There are `binomial(m+n-d,n)` such
   sequences when m is at least d, and none otherwise. At m=0 only the
   unique label-increasing word survives; both dilated polytopes consist
   of the origin. No negative-top binomial convention is implicitly used.

6. The corresponding series is `z^d/(1-z)^(n+1)`. Thus the coefficient
   interpretation follows from a disjoint lattice partition, rather than
   from merely defining a statistic in terms of the unknown h-star
   coefficients. The relation from extension words to rank permutations
   is `w_j=sigma^{-1}(j)`, so the composition order in the theorem is
   correct. A finite check independently detects its incorrect alternative.

7. The preceding partition works separately for every natural labeling,
   with the same original-coordinate lattice count. Hence all these
   generating functions have the same numerator. This establishes
   distribution invariance for every n without assuming wordwise
   invariance or drawing an all-n inference from finite tests.

8. Dimension one gives the unit interval and numerator 1. Both
   dimension-two signs give integral triangles and numerator 1.
   Alternating signs produce a total order. Sign complement and reversal
   are actual affine lattice symmetries of the original family. No
   palindromicity assumption is imposed on arbitrary signs; the example
   `n=4, signs=--+` has numerator `1+2z` and is correctly nonpalindromic.

These deductions confirm the stated all-positive-dimensions theorem.
Strict interior reciprocity is not needed to prove it; it was checked
independently as a falsification control below.

## New independent exact computation

`check_boundaries.py` was written for this audit and imports neither
submitted checker. Its primary lattice mechanism generates original cube
points directly and assigns a point to every admissible sign sequence;
ties are assigned to both weak inequality choices. It does not use the
submitted lattice dynamic program, an order-polytope lattice-count
routine, or the claimed formula as a lattice oracle.

The completed standard-library run passed:

- Every sign word in dimensions 1 through 8: 255 patterns.
- Every permitted natural labeling in those dimensions: 46,233 labelings.
- Every ordered alpha/sigma pair with matching required descent set:
  23,816,045 pairs.
- Direct original-coordinate cube enumeration through dimension 6,
  dilations 0 through n+2: 1,045,363 inspected points and 510 count checks.
- Independently extracted full Ehrhart numerators for all 63 sign
  patterns through dimension 6, including the zero coefficient of z^n.
- Strict original-coordinate interior enumeration through dimension 6:
  198,117 inspected strict cube points and 447 reciprocity count checks.
- Degree/codegree comparison using the observed first nonempty interior
  dilation, not a poset height input: 63 checks.
- Forward boundary sorting and exact point reconstruction using every
  natural labeling through dimension 5 and dilations 0 through 3:
  33,690 assignments, including 76,402 adjacent equal-value ties.
- Global sign complement and reversal controls for all 255 patterns.

Six explicit negative controls demonstrate sensitivity to errors:

- In dimension 3 with signs `--`, alpha `132` and beta `231` both give
  numerator `1+z`. For sigma `132`, the exponent changes from 0 to 1.
  The theorem correctly promises distribution invariance only.
- For alpha `132` in that example, replacing `sigma^{-1}` by `sigma`
  changes the enumerator from `1+z` to `1+z^2`.
- Using raw vertex indices as labels gives `2z` instead of `1+z`.
- Adding a closing upper-bound edge to the same example changes the
  dilation-one lattice count from 5 to 4. The printed problem has no such edge.
- Replacing the weak upper adjacent-sum inequality for the dimension-two
  triangle by a strict one changes the dilation-one cube count from 3 to 1.
- Reusing the unit-dilation reflection at dilation two sends a valid
  original point outside the target cube.

The new checker uses explicit `require` failures rather than Python
assertions, so optimized execution still checks every predicate. A second
native run under `-O` also passed, with identical semantic results and
empty stderr. Its private exact command, native output digests and return
code are bound by `OPTIMIZED_REPLAY.json`.

All arithmetic is exact integer arithmetic. The finite range is evidence
for the controls, not an empirical replacement for the all-n deduction.

## Strongest conclusion, gaps, and disposition limits

The strongest verified mathematical result is exactly the submitted
all-dimensions finite permutation interpretation for the literal signed
adjacency target. No unresolved mathematical step or required repair was
found. The route is not blocked and does not transfer a central difficulty
to an unsupported claim.

Historical priority, whether a published theorem explicitly or implicitly
already resolves this exact family, and any decision to keep the problem
status `claimed_solved` are outside this assigned family. The method is
plainly classical, and the submission already credits that fact. A
separate priority audit must determine the resulting status before any
publication or merge decision. This mathematical PASS alone authorizes
none of those actions.

No remote mutation, source edit, repository-index change, publication,
outreach, or new proof-search author turn was performed by this reviewer.
