# Independent adversarial audit: quantitative lattice squares, ID 30001694

Date: 2026-10-05 UTC. Target descriptor: OWR-4798-010; supplied catalog rank 706.

## Verdict

PASS for the explicitly partial mathematical record and the exact original 4x4 certificate, with two documented defects in historical validation tools. The controlling release decision is the independent strict validator included with this audit. It accepts the exact original packet and rejects all 17 adversarial controls. The original verifiers remain unchanged historical artifacts and must not be described as passing a complete adversarial validation audit.

The universal conjecture remains unresolved by this record. Five bounded approach families have been audited; the appropriate research outcome remains unsolved, five of five approaches consumed. No sixth mathematical search route was attempted. No novelty, global-openness certification, or reproduction of the published n<=13 search is established.

No substantive flaw was found in the authored integer-block, rounding, unit-chord surgery, rectangle, quarter-turn, or conditional compactness proofs. No admissible counterexample was found. The actual certificate has exactly the intended 9,349 rows with correct maxima and witnesses.

## Exact inputs and source limits

The input ZIP has 61,552 bytes and SHA-256 20635fa3e641d5df4ae3ad88bc439a9aed34d31d6eac8dcbcf563087c7f8e1fc. Its 15 entries consist of the root manifest and 14 declared payload files. Every original payload hash and byte count was independently checked before and after testing. Experiments operated on read-only inputs or disposable copies; the original ZIP and payload bytes are unchanged.

The original OWR report was inspected at printed pages 362-363, including the displayed constants on page 362 and the approximation discussion on page 363. The local public-source PDF hash and size agree with the frozen source metadata. The target is a Jordan-boundary unit-cell union, with the largest open axis-parallel interior-square side s, and a square of any orientation whose four vertices are boundary lattice points. The even and odd constants agree with the packet. [Tverberg, OWR 08/2011](https://ems.press/content/serial-article-files/46323)

The publisher-indexed HTML text independently confirms that the 2014 Conjecture C is this same target, Theorems 2 and 3 supply the credited lattice and chord reductions, and Theorem 4 is bounded by o(J)<=13. The article's n denotes cell-box side length, with an (n+1)-by-(n+1) vertex grid. [Pettersson, Tverberg and Östergård, DCG 51 (2014), 722-728](https://link.springer.com/article/10.1007/s00454-014-9578-5)

The publisher PDF body remains uninspected. Its previously denied download was not retried or routed through an alternative. The exact UnsolvedMath webpage and raw prior AI/dataset records remain uninspected. Catalog statement/review hashes are inherited identifiers, not newly verified raw-source bindings. This audit does not independently certify the historical repository-search observations or the newer-paper survey. None is a premise of the audited elementary proofs or finite certificate.

No scholarly PDF, extracted source text, source image, raw dataset record, private personal data, or private coordination material is included in the public audit bundle.

## Finding F1: out-of-domain certificate rows are accepted historically

Location: original verify.py, check_certificate, lines 53-73, particularly the lookup construction at 55-56 and the range loop at 58.

Reproducer: copy the first legitimate CSV row, set its mask to 0 or 65536, and append it. The resulting certificate contains 9,350 rows. The historical verifier still returns passed=true and admissible=9349. It visits only keys in 1..65535, checks duplicates, but never requires that all supplied keys lie in this range or that all supplied rows were consumed.

Impact: the authored statement that the historical replay checks for all missing or extra rows is too strong. This does not invalidate the original 9,349-row certificate, whose exact row set has now been independently verified. It does not affect any mathematical lemma, computed maximum, or target conclusion.

Controlling correction: strict_release_validator.py requires canonical integer fields, the exact key domain, uniqueness, exactly 9,349 rows, and equality with the full independently reconstructed admissible-mask set before checking all parameters and witnesses. It rejects both out-of-range additions, a negative mask, duplicate/missing rows, and an equal-count replacement by an invalid in-range mask. The historical file is retained unchanged; readers must use the strict validator for release acceptance.

A direct maintenance patch to a future version of the historical verifier would reject any key outside 1..65535 and require len(rows)==count after enumeration, with regression tests for those cases. That patch was not applied to frozen bytes.

## Finding F2: nested manifests escape the historical allowlist

Location: original verify_manifest.py, line 7.

Reproducer: in a disposable packet copy add extra/MANIFEST.json containing arbitrary bytes. The historical manifest checker still prints that all 14 payload files match, because its filename filter excludes any file named MANIFEST.json at any depth.

Impact: the historical allowlist check is not exact. The original archive itself has no hidden or unlisted member, so its current contents and hashes remain correct.

Controlling correction: the strict validator checks the exact ZIP member set, rejects duplicate member names, requires exactly the declared 14 payload names, exempts only the root MANIFEST.json, rejects duplicate JSON object keys, and checks every declared byte count and hash. It rejects both nested manifests and ordinary unexpected files. A future historical patch should exempt the exact root path rather than every matching basename.

## Proof review by approach

### 1. Integer blocks and boundary contact

Lemma 1.1 is valid. A real open axis-parallel square intersects the interiors of precisely a rectangular set of unit cells indexed from floor of its lower coordinates to ceil of its upper coordinates, minus one. All these cells must be occupied. The open interior of their closed rectangular union lies in int(P), including its interior grid seams. The integer rectangle has both side lengths at least the original side and contains an integer-aligned square at least that large. Finite support then gives an attained positive integer maximum. This does not assume its corners lie on the boundary.

Counterexample 1.2 is valid: mask 1651 has s=2 and the indicated maximizing block has its (1,1) corner interior because all four incident cells are occupied.

Counterexample 1.3 is valid: mask 886 is an admissible seven-cell polyomino. Its listed row-wise boundary points match independently. Its four boundary lattice squares have squared sides 5, 5, 2, 2; none is axis-aligned. Thus the displayed rotated square realizes M^2=5, and this example defeats an axis-only strategy, not the conjecture. The largest filled block has side 2.

Residual: no mechanism forces a sufficiently large rotated boundary square for a general maximum block.

### 2. Rounding and continuous existence

The square parametrization and all three integral-coordinate cases are valid, without sign restrictions on the two side-vector parameters. At least three parallel selected coordinates force the relevant offsets integral and give a common fractional coordinate, so a single translation reaches the endpoints of the actual containing unit edges. At a lattice vertex no translation is needed. The adjacent two-and-two case forces all coordinates integral immediately.

In the alternating case, k=a+b and l=y-b are integers. The four moving coordinates have matching fractional parts up to sign. Both floor/ceiling values of b reach endpoints of the same original unit edges, with the prescribed opposite motions. The squared-side function is convex; at least one endpoint is nonshrinking. Selecting that endpoint preserves positivity even when the other endpoint degenerates. The proof does not mistakenly select an arbitrary endpoint.

Independent rational controls cover 21,700 alternating cases and 10,800 parallel cases, including negative parameters, integral endpoints and 1,050 cases with a degenerate endpoint. There are 7,350 examples requiring each respective endpoint. These controls support the algebraic proof; they do not replace its unbounded argument.

The compactness sentence is sound when degenerate square tuples are included in the closed constraint set; a known positive square then forces a positive maximum. Polygonal square existence is explicitly an external credited premise. The separate s=1 argument is elementary and correct: an interior lattice corner would force a filled 2-by-2 block, so any occupied unit cell supplies four boundary corners when s=1.

Residual: rounding preserves or improves an already available scale. It does not prove the required scale for general s.

### 3. Unit-chord surgery and topology

The minimal-perimeter argument is valid. A non-boundary unit lattice segment between boundary vertices has no interior intersection with another grid edge: perpendicular grid intersections occur at lattice points, and collinear overlap would be an existing unit edge. Its interior is therefore entirely inside or outside the Jordan curve.

The two old arcs together with the chord are simple cycles; bipartiteness and nonconsecutiveness ensure each old arc has at least three edges, so each new perimeter is at most L-2. A new segment of length one adds no lattice point, hence each new boundary lattice-point set is a subset of the old one.

For the chosen integer-aligned open maximum square, a horizontal or vertical unit segment meeting its interior would have at least one endpoint in that interior. Integer coordinate alignment is essential here. When s=1, no integer transverse coordinate can lie strictly between the sides. Thus the boundary-endpoint chord cannot intersect that chosen open square.

Interior surgery separates the old domain into two Jordan domains; the connected open square lies in one. Exterior surgery produces nested bounded domains with the old domain equal to their difference, and the larger contains the old domain. In both cases the selected new s is no smaller and its M is no larger. Each bounded simple grid domain is again a finite unit-cell union of the intended type. The strict counterexample inequality is preserved.

Independent exact ray-cast surgery controls checked every unit chord of every admissible 4x4 mask: 42,824 interior and 10,248 exterior instances. Both loops were checked for admissibility, shorter perimeter, boundary-vertex inclusion, the appropriate partition/nesting relation, M nonincrease and the required s preservation. This is a bounded stress test of the authored general topological argument.

Residual: chordless grid cycles are not bounded in size; no finite reduction to the tested range follows.

### 4. Rectangles and quarter turns

For rectangles, the explicit square gives M>=min(w,h), while the projection width of an arbitrary oriented side-t square is t(|sin(theta)|+|cos(theta)|)>=t. This proves the upper bound. Convexity of the rectangle justifies bounding a boundary-vertex square's entire convex hull here; that argument would not extend to a nonconvex general polyomino.

For quarter turns, a farthest point exists by compactness, cannot be interior, and can be chosen at an edge endpoint by convexity of squared distance. A lattice-preserving quarter turn sends it to four distinct boundary lattice points. Averaging distances from the four corners of a maximum interior square gives r^2>=s^2/2, so the orbit square has side at least s. The center condition is correct: cx+cy and cy-cx are integral, equivalently both coordinates are integers or both are half-integers.

Independent bounded checks cover 100 translated rectangular masks and all 39 quarter-turn-invariant admissible masks in the box. All 74,792 dihedral-image checks preserve the computed parameters.

Residual: no argument transfers these orbit points back from a symmetrized object to an arbitrary original boundary.

### 5. Finite certification and admissibility

The author's exposed-edge implementation toggles each cell edge, correctly retaining exactly edges incident to one occupied cell. Edge-connected occupied cells plus a connected boundary graph of degree two characterize a single embedded grid cycle. Grid edges cannot cross except at common endpoints. A diagonal pinch gives degree four and is excluded; a hole gives an additional boundary component and is excluded; disconnected cells are separately excluded.

The author's alternate implementation uses occupied-cell flood fill, a one-cell padded complement flood fill and an explicit exclusion of the two alternating occupied quadrants at a grid vertex. The padding is sufficient for the explicitly fixed 4x4 input domain. Holes and pinches require separate tests: excluding one alone does not imply the other. With both excluded and connected interior, the boundary is one embedded circle. These functions are fixed-box tools, not generic unbounded-polyomino APIs.

The new implementation uses union-find cell connectivity, the cubical Euler count V-E+F=1 and explicit alternating-link exclusion. For a connected planar cell complex without a pinch, the Euler count is 1 minus its number of holes. Boundary edges are constructed from absent neighboring cells rather than by toggling. Largest filled blocks use precomputed bit masks. All 12,650 four-subsets of the 25 lattice vertices are checked geometrically; exactly 50 are squares, and boundary membership is then tested for each polyomino. This avoids either author's method of generating candidate squares from side or diagonal pairs.

All three admissibility predicates agree on all 65,536 masks including the empty mask. The 65,535 nonempty masks give 9,349 admissible objects and 56,186 rejections. Counts for s=1,2,3,4 are 2,932; 6,034; 382; 1. Every one of the original 9,349 block and maximum-square witnesses matches the independent result. The minimum M^2/s^2 is 8/9, first at mask 16366. No symmetry quotient is taken.

The computation is strictly bounded and smaller than the cited published range. The independent implementation and controls strengthen reproducibility, not the mathematical frontier.

## Conditional approximation statement

The authored compactness statement is valid under its explicit common compact set, Hausdorff convergence and uniform positive side bound. The square equations and membership pass to a subsequential limit, and the positive bound prevents collapse. The packet correctly declines to infer inradius convergence or domain inclusion merely from arbitrary Hausdorff convergence. No missing approximation theorem is silently supplied by the finite computation.

## Release and status dependencies

The original packet may be retained as a historical partial record only together with the controlling strict-validation result and these two corrections to its validation claims. Its pending-audit fields remain historical; the present verdict is separate. No original mathematical or certificate byte needed modification.

A changed input ZIP, changed certificate, or modified proof text would require a new exact binding and appropriate delta audit. Passing the strict validator proves the stated finite certificate and integrity claims only. It does not make the universal target solved or the elementary results novel.

## Reproduce

With Python 3.10+ and the two audit scripts in one directory:

    python strict_release_validator.py /path/to/polyomino_30001694_FROZEN_PUBLIC_PACKET.zip --controls

This is the controlling command; it neither imports nor executes historical verifier code. It is also tested with python -O, because its mandatory checks use explicit exceptions rather than removable assertions.

For the extended geometric controls and historical defect reproductions, first extract the original archive unchanged into a separate directory, then run:

    python independent_controls.py --original /path/to/original --out /path/to/new-results

The latter script intentionally records accepted historical attack cases as defects rather than presenting them as passes. See INDEPENDENT_RESULTS.json, STRICT_VALIDATION_RESULTS.json and NEGATIVE_CONTROLS.json for machine-readable outcomes.
