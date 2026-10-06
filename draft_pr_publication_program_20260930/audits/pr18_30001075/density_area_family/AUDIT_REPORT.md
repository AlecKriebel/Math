# PR18 / 30001075 — density, rank, area, and boundary audit

**Verdict: PASS for this approach family. No mandatory mathematical repair found.**

Frozen candidate: commit `99e403e85d38d92b021198c4a57bbad3cd8775ba`, candidate SHA256 `b04aaf0b5a42d79ad26daf27880774a3f126858ef545b3f366a2b8b62e277252`.

Audit completed: 2026-10-01 UTC. Completion estimate: 100% of the assigned audit, not a novelty or publication-completion estimate.

## Scope and independent sequence

The audited assertion is that the union of lines tangent to three arbitrary pairwise disjoint convex subsets of R3 is contained in a Lebesgue-null set. Tangency requires both meeting the set and containment in a plane bounding a closed halfspace containing it. The stronger countable-2-manifold assertion is excluded. The controlling primary source is [Oberwolfach Report 44/2008](https://ems.press/content/serial-article-files/46191), section 13, printed p. 2552 (PDF page 75, zero-based), Conjecture 4. I checked that page directly after the independent seal; it agrees with the source record and candidate scope.

The candidate and exact source record were read first. The proof was independently reconstructed and tested, then sealed at **2026-10-01 16:58:17 UTC**. Historical review and code were first opened only after that seal. No root or sibling conclusion was consulted. The detailed precomparison reasoning and four analytic falsification controls are preserved in `INDEPENDENT_RECONSTRUCTION.md`, whose sealed SHA256 is `06deee131649b8077296b02cca25fa37f9481b317d8aaef79d126718a74c8a91`.

This was a verification and falsification audit of the existing candidate. It did not create an additional original central-proof attempt, change canonical research records, modify the frozen snapshot, install dependencies, alter Git, publish, or contact any external individual.

## Strongest independently verified result

For **any countable cover by Lipschitz maps from open subsets of R2 into line space**, the portion of each family whose lines are tangent to three disjoint compact convex sets sweeps a set of zero Lebesgue outer measure. This holds for all affine dimensions, after the explicitly null contained-plane and identical-affine-line exceptions have been removed. It does not require injective charts, unique supporting planes, unique contacts, smooth convex boundaries, or an interior in the selected tritangent parameter set.

The existing candidate cap-chart construction supplies the only additional geometric input for the high-dimensional compact case. I inspected that proof directly and found no definite gap; its detailed dedicated-family assessment remains an independent gate rather than a premise borrowed here. Once that cover is accepted, the full theorem follows, including arbitrary nonclosed and unbounded convex sets, by the candidate's countable rational-ball localization. No mathematical gap remains in this assigned measure/rank/area family.

## Gate-by-gate findings

| Gate | Finding and mechanism | Status / exact gap |
|---|---|---|
| Compact tangency and Borel selection | Limit contact points and unit support normals witness tangency. Contained-plane and fixed-line sets are closed, so the retained parameter subset is Borel. | Pass; no measurable contact selection is needed. |
| Density directional sequences | An absent ball of radius proportional to tau near q0+tau h would occupy a fixed positive portion of a ball at q0, contradicting density one. Approximate distance minimizers give qtau=q0+tau h+o(tau). | Pass; the argument applies to every fixed h. |
| Fixed affine shear | Subtracting u(q0)+zv(q0) preserves support/convexity and leaves A,B unchanged. Fresh interior balls are chosen after the shear. | Pass; no erroneous metric-ball invariance is used. |
| Dimension 3 rank contradiction | Onto A+z0B directs a density sequence into a convexly scaled interior ball with radius tau r and error o(tau). | Pass; no boundary smoothness is assumed. |
| Dimension 2 rank contradiction | The exact transverse intersection derivative is -Nx dot (A+z0B)h/Nz. It enters a scaled relative interior disk; every support plane there equals the affine hull. | Pass; transverse denominator remains nonzero locally. |
| Dimension 1 rank restriction | dx is nonzero for a retained affine line. Dotting the intersection equation bounds lambda by O(tau), and the perpendicular component becomes O(tau^2). | Pass at endpoints and nonunique segment contacts. |
| Dimension 0 rank restriction | Fixed point incidence gives A+z0B=0 along density sequences. | Pass. |
| Three contacts | Pairwise disjointness gives three distinct heights. A degree<=2 determinant polynomial with these roots is identically zero. | Pass; no numerical root test is required. |
| Lipschitz sweep | On bounded patches and bounded height intervals, v is bounded and the product z v(q) is Lipschitz. Its derivative is the displayed block matrix. | Pass; countable local exhaustion is sufficient. |
| Exceptional parameters | A 2-null parameter subset times a bounded interval is 3-null; equal-dimensional Lipschitz mapping preserves this nullity. | Pass even if all of E is null. |
| Noninjective area formula | Multiplicity is at least one on the image and the integral of |det DG| is zero. | Pass; no injectivity or nonsmooth Sard theorem is assumed. |
| Point and interval charts | RP2 direction charts handle a point. Positive compact separation and a locally nonzero direction component give smooth open extensions for interval endpoint/corner charts. | Pass; all dimension patterns are exhausted. |
| Arbitrary convex sets | Contact points can be placed inside pairwise disjoint fixed rational balls; closure intersections remain compact, convex, disjoint, and tangent. | Pass even if closures overlap, original distances have infimum zero, or original loci are not measurable. |
| Candidate cap cover, directly inspected | Correct support-gap signs, normal preservation, own/cross estimates, root contraction, and extraction for fixed rational caps were reconstructed. | No definite gap found; detailed cap-family verdict is independently assigned. |

The formulas and logical detail behind this table appear in the sealed reconstruction. Every contact-height rank assertion is made only at parameters that are both density-one points of E and differentiability points of the ambient Lipschitz chart.

## Adversarial controls and boundary stress

The proof's crucial assumptions cannot be weakened casually:

1. **Two disjoint compact planar rectangles:** A=[0,1] x [-1,1] x {0}, B=[-1,1] x [0,1] x {1}. Common tangents through (0,s,0) and (t,0,1) sweep (zt,(1-z)s,z). The determinant is z(z-1), vanishing at two contact heights while the bounded 0<z<1 sweep has volume 2/3. This is a geometric, not merely algebraic, countercontrol to a two-contact or degree-one shortcut.
2. **Three intersections without tangency:** Vertical lines through the radius-1/2 disk meet all three pairwise disjoint radius-1/2 balls centered at heights 0,3,6. Their sweep contains an open cylinder and has determinant one. Full/relative interior entry must contradict actual support tangency, not merely intersection.
3. **No disjointness:** Three copies of the singleton origin admit every line through it, sweeping R3. Three coincident contact heights do not annihilate the determinant polynomial.
4. **No density requirement in the pointwise rank lemma:** For vertical lines u=q,v=0 tangent to the unit ball, E is the unit circle while A=I. Rank two holds at every selected tangent parameter, which has density zero in R2. The swept surface is nevertheless null, exactly as the exceptional-parameter argument predicts.

Further boundary checks include empty sets; point and degenerate interval classification; endpoint contacts; full contact segments; nonunique support normals; planar directions parallel to the affine hull, which must be contained if they meet it; coincident affine hulls of disjoint intervals; overlapping closures; unbounded sets; nonclosed sets; and arbitrarily close contact heights. No generic-contact assumption was found.

Six exact finite controls in `independent_controls.py` pass and are recorded in `independent_controls_results.json`. They verify illustrative determinant and rational-volume identities. They do not establish the density, cap coverage, compactness, or area-formula assertions.

## Imported theorem verification

I obtained and inspected the actual authored [Leon Simon GMT text from Stanford](https://web.stanford.edu/class/math285/ts-gmt). The relevant statements are Ch. 1, Theorem 3.16 with the Euclidean Vitali discussion in 3.11; Ch. 2, Rademacher Theorem 1.4; and Ch. 2, area formulas 3.2–3.4, including multiplicity. The parameters here are Euclidean, E is measurable, the chart domains are open, the sweep is locally Lipschitz, and source and target dimensions are both three. Those hypotheses match. A global-map formulation can be applied through coordinatewise Lipschitz extension from a slightly larger bounded patch. The equal-dimensional case avoids any issue about lower-dimensional image normalizations.

The book PDF and text extraction are ignored cache inputs. Cache SHA256: `e4e2367b5a0555feed16712061b39b534fe554f0c920bb609ab983f3e698b88d`. The exact Euclidean hypotheses were inspected rather than inferred from historical reference labels. No finite code substitutes for them.

## Historical replay after sealing

Both frozen checkers were copied into the ignored `tmp/historical_replay` directory before execution. Their output files therefore landed in the copy. The frozen snapshot was never executed in place or overwritten.

The default Python and bundled runtime lack SymPy, so their initial read-only probes/imports failed. The pre-existing `/Users/alec/Documents/Math/.venv/bin/python` contains SymPy **1.14.0** and ran both scripts successfully with bytecode writing disabled. No package or environment was installed or changed.

| Historical script | Actual replay receipt | Comparison |
|---|---|---|
| `verify.py` | 810 exact support-increment cases; 4 cap-margin models; 81 linear contraction models; symbolic determinant, Vandermonde, swept-Jacobian, two-root and planar-derivative identities | Matches frozen `verification.json`. There is no author receipt of 135 in this snapshot. |
| `review/independent_checks.py` | PASS 36 exact diagnostics | Matches frozen `review/independent_results.json`. |

These are ancillary reproducibility receipts. My analytic conclusion was already sealed before reading the earlier passing review, and that historical agreement did not remove an unresolved proof gap or supply a missing argument.

## Repairs, optional improvements, and remaining uncertainty

**Mandatory mathematical repairs:** none in the assigned family.

**Optional exposition improvements:** cite precise density/Rademacher/area theorem numbers; describe a bounded open-patch exhaustion before applying the area formula; give the nonzero-component denominator explicitly for interval-chart extensions; and include the two-rectangle control to explain why three distinct contacts are decisive. Each is an explanation of an already valid step.

**Remaining mathematical gate outside this family's primary assignment:** the independent exhaustive cap-chart audit. My direct inspection found no gap, but this report is not a substitute for that separately assigned audit.

**Remaining research uncertainty:** historical priority. The candidate's limited negative search is not a certificate of novelty. This family verifies the mathematical mechanism; it does not promote the result to a new discovery, claim external peer review, or establish the stronger manifold conjecture. Publication disposition should incorporate the separate current primary-literature investigation.

## Artifact index

- `INDEPENDENT_RECONSTRUCTION.md`: detailed analytic reconstruction and adversarial controls, sealed before historical comparison.
- `independent_seal.json`: timestamp, independence declaration, and reconstruction/control hashes.
- `independent_controls.py`, `independent_controls_results.json`: six exact finite controls.
- `historical_replay_receipt.json`: reproducibility and frozen-receipt comparison.
- `VERDICT.json`: machine-readable family disposition and exact remaining scope.
- `MANIFEST.json`: hashes for all fifteen frozen source files and all persistent audit artifacts, excluding itself and ignored cache/execution inputs.
- `RESEARCH_LOG.md`: timestamped checkpoints with completion estimates.
