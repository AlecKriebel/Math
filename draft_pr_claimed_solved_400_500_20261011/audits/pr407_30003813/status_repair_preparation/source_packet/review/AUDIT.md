# Independent audit: signed adjacent-sum h-star certificate

Date: 2026-10-03. Target: UnsolvedMath 30003813 / OWR-16164-005.

## Verdict

**PASS.** The frozen candidate proves its theorem for every positive dimension,
every adjacent-sum sign sequence, and every permitted natural labeling. It supplies
a finite, explicit coefficient interpretation that answers the literal request in
the original OWR paragraph. There is no mathematical gap or mandatory mathematical
repair.

This verdict is specifically an approval of a **classical-corollary combinatorial
interpretation**, not a novelty finding, a verified historical resolution claim,
or a construction of a statistic on the original cyclic-order objects. Those
limitations already appear clearly in the candidate and must remain in any
public-facing statement. No additional cyclic-order result is needed to satisfy
the wording actually printed in OWR.

The mathematical audit was independent of the authored candidate. The audited
version is identified by its manifest below.

## Frozen object and integrity

Audited original version: the seven files bound by the candidate manifest below.

SHA-256 of its `MANIFEST.sha256`:

`778ed8c2540fb54f35832390c03380dbb4118c09b2e055b8273cf4fce716d52c`

All seven listed files matched their digests. The manifest plus those files makes
eight files in the frozen packet. The supplied verifier was run with maximum
dimension 8, with output outside the frozen directory; its JSON reproduced the
committed `verification.json` byte-for-byte. Its reported 255 sign patterns,
46,233 permutation words, 2,558 Ehrhart evaluations, 79,657 pointwise reflection
checks, and 12,195 tie-sort checks were reproduced.

## Exact original target

I read the concluding paragraph of the Josuat-Verges abstract in the official
OWR report text and visually inspected the rendered printed page 1410 (PDF page
30). Its definition is exactly the cube with one chosen weak adjacent-sum
inequality for every index from 1 through n-1. It asks for the combinatorics of
the h-star polynomial. It does not impose cyclic adjacency, an additional wrap
edge, a cyclic-order statistic, a preferred labeling, or a novelty condition.

The surrounding abstract motivates h-star through cyclic-order statistics for a
related family. That motivation makes a cyclic-order refinement potentially
interesting, but does not turn it into a condition in the final question.
Interpreting the final request as demanding only such a refinement would add a
restriction absent from the source. The candidate's careful literal-target claim
is therefore justified. Its explicit sign convention is necessary and correct;
the original paragraph does not name which sign means which inequality.

The supplied corrected problem record agrees with this source. Its older
placeholder-only triage assessment does not accurately describe the supplied
corrected statement, and the candidate properly declines to rely on it.

## All-dimensions proof audit

1. **Reflection and all signs.** Reflecting the even coordinates sends
   x_i+x_(i+1)-1 to y_i-y_(i+1) for odd i and to y_(i+1)-y_i for even i.
   Each of the four entries in the orientation table is correct. No sign
   symmetry or special pattern assumption is being substituted for this check.

2. **Poset and nonemptiness.** An orientation of a path is acyclic. Its
   transitive closure is consequently a partial order and admits a linear
   extension. The proposed minimal-vertex labeling algorithm terminates.

3. **Exact descent class.** A bijection from vertices to ranks is order
   preserving precisely when its adjacent entries have descent set
   D = {odd i with sign +} union {even i with sign -}. Checking path edges
   suffices for the transitive closure. The word of vertices in increasing rank
   is sigma inverse, not sigma. Thus alpha composed with sigma inverse is the
   correctly ordered label word in the displayed formula. There is no inverse
   or composition-order error.

4. **Lattice and full dimension.** The extension simplices are contained in
   the order polytope, have integral suffix-indicator vertices, and have a
   nonempty Euclidean interior. Sorting coordinates with a natural-label tie
   rule covers the entire order polytope, including boundaries. Since the
   polytope is convex, the finite simplex union is the convex hull of the
   integral vertices from these simplices. This proves integrality; any one
   full-dimensional simplex proves full dimension. The inverse reflection
   preserves both conclusions. No unproved general triangulation theorem is
   required for this argument.

5. **Dilations, including zero.** The map on m-dilates is T_m, with even
   coordinate m-x_i. Reusing T_1 for other dilations would be incorrect, but the
   candidate explicitly avoids that mistake. T_m is an integral affine
   involution and gives exactly the stated lattice-point bijection. At m=0
   both sets consist of the origin.

6. **Disjoint boundary partition.** Lexicographic sorting by (value,label)
   gives a unique extension. For a fixed extension, the coordinates are weakly
   increasing and are strictly increasing at every descent of its label word.
   Conversely, an equal-coordinate block with no adjacent label descent is
   strictly increasing in labels throughout, so these conditions recover the
   original sorting order. This proves necessity, sufficiency, exhaustion and
   disjointness. Nonadjacent equal-coordinate ties do not create a gap.

7. **Counting and generating series.** Subtracting the number of preceding
   required strict steps transforms each assigned sequence bijectively into a
   weak sequence from 0 through m-d. This gives binomial(m+n-d,n), or zero for
   m<d. The generating function is z^d/(1-z)^(n+1), with no endpoint shift.
   Summing establishes the full displayed h-star formula.

8. **Every natural labeling.** The partition proof holds for each admissible
   alpha separately, while its lattice-counting left side is fixed. Thus the
   distribution, not each individual word's statistic, is independent of
   alpha. The candidate makes this distinction correctly.

9. **Small and special cases.** Dimension one, both dimension-two signs,
   alternating sign words, constant coefficient one, sign complementation,
   coordinate reversal, and the nonpalindromic mixed-sign example all check.
   The warning against raw vertex-index descents is valid.

## Attribution and literature scope

I checked the supplied primary-source text for Stanley (1986), Definition 1.1,
Corollary 1.3, Theorem 4.1, and the triangulation discussion; and Coons-Sullivant
(2023), Theorem 16 and its adjacent natural-label example. These support the
candidate's classical attribution and composition convention.

I also checked AJR (2020), Theorems 2.5 and 2.9 and Remark 2.6. The signed-family
sign convention is opposite to this candidate's and its dimension is sign-word
length plus one. Theorem 2.5 supplies integrality and volume for that family.
Theorem 2.9 concerns the separate upper-consecutive-sum family. Remark 2.6's
statement about not arising as chain polytopes does not prohibit the affine
order-polytope equivalence used here. The candidate does not conflate these
results.

The prior-attempt and current-literature searches recorded in SOURCE_GATE were
not rerun against remote services in this audit. No absence-of-literature or
priority assertion is established by this review. This is not a mathematical
blocker, because the candidate explicitly makes no novelty or historical
closure claim.

## Independent controls

`independent_controls.py` was written separately, without importing any authored
verifier function. It works directly with exact permutation descent classes,
constructs a reference alpha by reversing descending runs of the identity, and
uses explicit dense transition matrices in the original x coordinates. It also
performs direct grid enumeration and the reverse half-open partition map.

All controls passed:

- 127 sign patterns in dimensions 1 through 7
- Every natural labeling in those dimensions: 5,913 labelings total
- 679,917 ordered alpha/sigma pairs within identical descent classes
- 1,277 dense original-coordinate lattice counts, m=0 through n+3
- 253 independent direct-grid counts, inspecting 2,006,709 points, n<=5
- 245 exhaustive reverse boundary-partition cases, with 16,829 reconstructed
  points; all admissible labelings for n<=4 and a fixed one for n=5, m=0..4
- 217 strict-interior counts agreeing with Ehrhart reciprocity, n<=5, m=1..7
- 127 degree/codegree controls using the longest directed chain
- Three negative controls: raw labels, an inadmissible labeling, and the
  incorrect reuse of T_1 at dilation two

The reciprocal-count and degree checks are independent diagnostics, not new
claims needed by the candidate. These finite checks supplement rather than
replace the all-dimensions proof audit.

The first audit-script execution completed the main controls and then hit a
reviewer-side generator/tuple TypeError in the final negative control. That
harness-only error was corrected; the complete corrected script then passed.
It neither revealed nor required any change to the candidate theorem or proof.

## Repairs and release scope

**Required mathematical repairs: none.**

Optional editorial cleanup: in Section 4, replace “Equation (9), with (1)
replaced by m” by “Equation (9), with the constant 1 replaced by m”. The existing
wording is understandable but resembles a reference to equation (1).

The frozen README, proof heading, and status JSON still say independent review
is pending. Preserve that frozen historical object. If preparing a new release,
update the review status and manifest in that new release and include/link this
audit record. This is release bookkeeping, not another substantive author
attempt or a mathematical repair.

Approved concise claim: “A complete classical-corollary answer to the literal
OWR request: every h-star coefficient counts explicitly specified permutations
in a fixed descent class.” Avoid implying a newly discovered theorem, verified
historical closure, or a cyclic-order-specific refinement.
