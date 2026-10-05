# Independent source and mathematical review: 30004365

2026-10-02. Separate review of the frozen one-turn candidate. **PASS for the literal effective-algorithm problem**, with the bibliographic qualification below. No mathematical alteration of the frozen proof is required. This is an AI-assisted mathematical review, not external peer review or a claim of historical novelty.

## Frozen scope and disposition

The reviewed author manifest has SHA256 `11a691554dd5f480561753bf372b54854caddf778d7a493bbff8e0b1dfe6b418`; `TURN_1.md` has SHA256 `61130af734e4d1ad68d292b29546f562858fa6aafc6eb92f2e7d2e3d3c1c0a3a`. All eight files bound by the manifest, the manifest itself, and all eight source-file hashes were checked. The complete author argument, source gate, and verification code were read. Source PDFs and page images are reference material only and are not included in this public review packet.

The proof supplies a terminating, generally impractical algorithm on the promised class of nonzero finite-dimensional gentle bound quivers with quadratic monomial relations. One substantive author turn is recorded. An early full-candidate stop is justified; there is no reason to manufacture four further turns. Recommend a qualified solved/complete-algorithm-candidate disposition after the parent's publication gate, retaining both independent-review status and the absence of an efficiency or production-software claim. This recommendation does not certify priority.

## Source gate

The original Plamondon contribution in OWR 3/2020, printed pages 161–164, was read, including Problem 3.4 on page 163, and the formula page was inspected visually. It asks for an algorithm computing the stated data from the bound quiver. It does not impose a complexity bound or prohibit reconstructing the surface. Accordingly an explicit finite-predicate enumeration with proven termination answers the literal task.

Primary source: https://ems.press/content/serial-article-files/46842 . The workshop was 19–25 January 2020 and the report/volume is designated 2020. The publisher records volume 17(1) as published **10 February 2021**, https://ems.press/journals/owr/issues/1220 . Thus `SOURCE_GATE.md`'s contrast with the imported 2021 label must not be repeated as a claim that the latter is bibliographically erroneous. Preserve the frozen file and append this qualification.

The final Amiot–Plamondon–Schroll (APS) paper, published 14 March 2023, https://doi.org/10.1007/s00029-022-00822-x , was checked at its definitions, winding rule, surface/algebra bijection, Theorem 6.1, Remark 7.2, Theorems 7.3–7.4 and Remark 7.6. Its basis-extraction difficulty is stated explicitly. Palu–Pilaud–Plamondon (PPP), https://arxiv.org/abs/1807.04730 , Definitions 4.6/4.8, Theorem 4.10 and Remark 4.11 supply the credited finite construction. Limited primary-source searches found the same gap statement and special-subclass algorithms, but did not establish a later general solution. This is a bounded literature check, not a priority proof.

## Mathematical audit

### 1. Finite construction and conventions

Local blossom completion is an actual finite operation. Gentleness bounds each incoming/outgoing relation and nonrelation multiplicity by one; hence the original partial two-by-two table extends to the required matching. Distinct auxiliary leaves avoid unwanted identifications. Each lozenge has finitely many labeled sides; the prescribed relation/nonrelation identifications are exact combinatorial operations. The construction must retain the side labels and suppress the auxiliary bivalent points when reading the dissection edges, as specified by PPP; blossom leaves are not additional colored marks.

PPP's green dissection has the input bound quiver and the red dissection is its dual. The candidate explicitly checks the recovered quiver rather than guessing from color names. Finite dimensionality forbids cyclic permitted arrow paths, so the input dissection has no white punctures (also APS Theorem 4.3). Consequently cutting along the *dual* dissection produces disks with one white boundary mark. Black punctures are dual-dissection vertices, not interior white punctures of these disks. Small collars simply truncate corner sectors and do not create holes inside a cut-open disk.

The finite gluing is a polygonal surface, not an arbitrary higher-dimensional recognition problem. Recording sectors resolves loops and repeated incidences. Subdivision gives a finite rational triangulation; link tests and Euler characteristic apply to the resulting genuine surface. The quiver is a promised input, so no decision of finite-dimensionality over an unspecified presentation is being assumed.

### 2. Decidable acceptance and genuine geometry

For each height, bounded rational coordinates, bounded segment count and finitely many triangle/chart labels give a finite set of encodings. Equality of seam parameters is rational equality. Segment containment, endpoints, transverse crossings, overlaps and cyclic orders are finite exact tests. The verifier can reject degenerate encodings; the termination argument supplies nondegenerate ones.

After subdividing at crossings, cutting is implemented by copying incident sides and vertex sectors. Finite graph traversal identifies components and boundary cycles. Rational thin strips and vertex disks produce a regular-neighborhood complex; positive separation of disjoint finite PL pieces permits an effective sufficiently small choice. The genus and boundary calculations therefore do not invoke a homeomorphism oracle.

A pair of embedded curves meeting once in an orientable surface has a once-holed-torus neighborhood. The candidate additionally checks this fact, disjointness of the handle neighborhoods, and connected planar complement. These certificates give the required embedded handle system. Merely checking a symplectic intersection matrix would be insufficient for this purpose; the submitted verifier does more.

### 3. Noncircular termination

The ordinary classification of compact connected orientable surfaces guarantees an embedded handle system. It is used only as an existence theorem, not as the requested algorithm. A generic perturbation puts its finitely many curves transverse to the fixed triangulation and dual dissection, away from all exceptional vertices, collars, and coincident crossing points. A sufficiently fine PL approximation preserves this embedding and crossing pattern. Rational choices can be made within the resulting open constraints, with exactly matching seam coordinates. The finite rational encoding is eventually enumerated.

Every component of an embedded curve cut at successive dual-dissection crossings is a simple proper crosscut of a disk and hence separates it. A noncontractible handle cannot be wholly contained in one such disk. Thus the final acceptance condition does not inadvertently exclude the guaranteed witness. No negative semidecision, unknown stopping bound, missing geometric-basis algorithm, or unproved computability hypothesis is smuggled into the search.

### 4. Winding and exceptional components

The left/right test is topological: cut a polygon along the proper oriented arc and locate its unique white mark on the appropriate side. Local orthogonal smoothing does not alter that side or introduce new intersections. The sum is precisely APS Lemma 3.18 and is not a floating-point turning-angle approximation. Returning to a previously crossed polygon causes no difficulty; the formula applies to the individual simple pieces.

Boundary and puncture parallels are oriented with the retained surface to their right, equivalently the corresponding removed boundary region to their left. This agrees with the conventions preceding APS Theorem 7.3 and Proposition 3.20(5). Black puncture collars meet the incident dual arcs. Original boundary collars meet their incident dual arcs; the sole contractible-boundary exception is a disk component, where a nonzero input still supplies dual arcs ending on the boundary. In particular the isolated field is the disk with two marks of each color and one primal/dual arc. Its collar crosses the dual arc twice. There is no empty-crossing winding convention being used for that case.

The base field is the fixed field of the source, not an added algebraic-closure assumption. Disconnected input is processed by its connected factors. Derived equivalence preserves the indecomposable category blocks; taking the multiset of component keys is sound. Rejecting the empty quiver is explicitly outside the promised nonzero source class.

### 5. Complete comparison key and puncture indexing

The genus-one gcd is nonnegative and includes every peripheral winding plus two. For higher genus the successive parity, peripheral residue and Arf alternatives match the cited classification. Raw winding values for the chosen handle curves are certificates only, not canonical key entries. Boundary records retain the pairing between mark count and winding, with punctures distinguished by zero mark count; every true boundary has a positive mark count.

The printed final Theorem 7.4(2) has a real range discrepancy: its permutation includes punctures but its displayed winding equality stops at the boundary count. The candidate does not silently edit it. Keeping all puncture winding records is sufficient for its displayed conditions, while necessity follows directly from the orientation-preserving homeomorphism and all-simple-curve winding criterion in Theorem 6.1 (or Remark 7.2). This also agrees with the subsequent proof, which treats all peripheral curves. Thus the extra records cannot split an actual derived-equivalence class. There is no reliance on an incomplete workshop summary to suppress necessary paired winding information.

## Supplementary checks and limits

`AUTHOR_REPLAY.json` records a byte-exact author replay: 1,328 assertions. These are finite checks, not an implementation of the full algorithm.

The independent `verify_independent.py` imports no author verification function. Its 32,291 assertions cover:
- 557 connected finite-dimensional gentle quivers with one to three vertices, loops/repeated arrows permitted, and at most `2n-1` arrows, including 202 genus-one inputs;
- side-gluing Euler data checked against independently traversed permitted/forbidden path cycles and blossom endpoint matchings;
- 6,561 rational segment-intersection controls including endpoint/collinearity degeneracies;
- 4,368 Arf-formula controls under symplectic transvections in dimensions two, four and six.

These tests supplement the universal proof audit; they do not turn the exhaustive PL search into tested production software, verify every triangulation/cut implementation, or provide an effective complexity bound. No implementation or efficiency result is inferred from their counts.

## Final recommendation

Accept the frozen candidate as a complete solution of the literal effectiveness request, with existing geometric/classification inputs fully credited, the two valid source dates preserved, and the qualifications above prominent. Keep the submitted proof hash unchanged. Publication and campaign disposition remain with the parent. No merge, release, external submission or contact is authorized by this review.
