# Research log

All times are UTC on 4 October 2026. Progress percentages concern completion of the scoped verification goal, not a probability that the mathematics is correct.

## Readiness checkpoint 1702 UTC

Progress estimate: 15 percent. Read current repository guidance. The live queue blob aac1b5bc7e0a719f7c3bd5673e77793dc79cdf52 has rank657/ID30000510/OWR-1275-010 queued at 0/5. The current state file has no record for the target. Bounded repository code, PR and commit searches found no actual prior attempt. The catalogue page was unavailable, so the authorized existing corpus snapshot was used as a locator. This is not a prior-attempt skip.

## Approach 1 prior-result verification 1703 to 1712 UTC

Progress estimate at 1704: 60 percent. Search found Alper Ferudun's 1 October 2026 preprint, which already claims the full singular-cohomology and component answer. Retrieved the actual reading PDF and archival metadata from Zenodo, checked its published MD5 against the downloaded bytes, and separately retrieved the original EMS report. Visually inspected the exact primary statement on printed page1607. The report imposes adjacent inequality and at least three values, and retains labels; it does not specify coefficients or a cohomology theory.

Mechanism A: normalized pair slice. Normalize the first two adjacent values to infinity and zero. The residual group consists of positive dilations. A third finite nonzero value gives explicit local trivializations, so the map from the pair slice to B_n is a contractible-fiber bundle. Angular coordinates identify each slice with a nonempty convex region, except that the even middle slice has one interior point removed. Its radial retraction yields the sphere and every component count and singular group.

Mechanism B: compact-subgroup cross-check. Independently followed the prior paper's other quotient X_n^*/PSO(2), in which winding levels are open hypersimplices and the excluded alternating configurations form a line segment in the middle level. The map to B_n has fiber PSO(2)\PSL(2,R), a hyperbolic plane. The removed line has codimension n-2, again giving a sphere of dimension n-3. This is a cross-check of the same prior result, not a separately credited new result.

Adversarial issue: neither a free action nor contractible orbits alone would justify the homotopy conclusion, and the even middle quotient is non-Hausdorff. Checked explicit local products in the prior paper and reconstructed them. Inspected the cited finite-cube proof of Hatcher Proposition4.48 and the weak-equivalence homology/cohomology statement Proposition4.21. These do not impose a Hausdorff base. No strong homotopy equivalence or unexamined cohomology comparison is promoted.

Progress estimate at 1706: 85 percent. The prior result is verified for ordinary singular cohomology with every abelian coefficient group and for the component count. This triggers the allowed early stop before five approaches. Exactly one substantive research turn is recorded; no four unused attempts are fabricated. The result remains attributed to the prior preprint, which is unrefereed.

Progress estimate at 1712: 100 percent of author-side verification and packaging. Authored PROOF.md includes every mathematical step of the normalized-slice route, a rational sup-norm deformation, the cohomology ring consequence, low-n boundaries and an explicit non-Hausdorff control. Fresh exact code passed 3312 projective-invariance controls, 552 reflection controls, 189 slice-existence controls, 36 alternating-locus controls, 2800 radial controls (including 700 stationary-sphere controls), and 24 degeneration-sequence controls. Finite checking is supplementary only. Downloaded research code was not executed.

## Scope and stopping decision

Disposition: prior result verified, complete for the ordinary singular reading of the original question. There is no claim of mathematical novelty, first resolution, peer review, or a prior user attempt. The preprint's remaining Cech/de Rham/strong-homotopy questions are not this task's new research target. The author packet is frozen for a fresh independent audit before any publication. No remote write or DOI release was performed.
