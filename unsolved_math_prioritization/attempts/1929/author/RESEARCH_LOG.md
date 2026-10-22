# Research log: ID 1929 / EP-100

Date: 2026-10-05 UTC. Rank at the verified queue snapshot: 756. Target: uniform linear diameter for planar separated-distance sets. This is a bounded research attempt, not a new-paper claim.

## Source and prior-work checkpoint (16:43-16:50 UTC)

Recovered the exact ID-to-problem identity from the complete pinned corpus. The prior-report dictionary does not contain the exact EP-100 key, and a content scan found no selected-title/Piepmeyer record. Checked actual repository attempts and problems directories, current queue, related-target groups, code index, PR searches, branch search, and commit search. No selected prior attempt was found in those scopes; absence from an index alone was not used as a certificate.

Inspected the original Erdős 1995 formulation and reconstructed the credited Piepmeyer geometry. Inspected the older explicit two-hypothesis formulation in Erdős's combinatorial-geometry paper. Inspected Guth-Katz's published theorem and lattice discussion, and the exact-minimum qualification in the Pach-Radoičić-Vondrák author preprint. Brass's publisher abstract is only a restricted half-strip result; its full proof was not retrieved. Original Kanold proof was not located, so attribution is historical and no exact-source proof identification is asserted.

Direct UnsolvedMath and live Erdős pages could not be retrieved with the web tool. Indexed Erdős status/discussion were inspected with their crawl-age limitation; current accessible formal-conjectures source remains marked open. No denied route was bypassed. No outside person was contacted, and no remote writes were made.

General-target proof completion estimate: 0%. Scope/literature identification completed; this percentage is not a probability of eventual success.

## Approach 1: distance spectrum and energy (16:45-16:51 UTC)

Mechanism: count separated spectrum values and apply distinct-distance incidence results; test whether equality-pattern energy could remove the logarithm.

Outcome: proved k<=D and the precise implication of the imported Guth-Katz theorem. Proved that any finite shape can be dilated to satisfy the hypotheses. Therefore admissibility alone adds no scale-invariant restrictions on equality multiplicities. The known square-grid spectrum also blocks a uniform O(n^3) energy shortcut. No new incidence estimate was obtained.

Gap: a genuinely scale-sensitive input must eliminate the logarithmic loss. General-target completion: 0%.

## Approach 2: shortest pair, two circles, packing (16:45-16:51 UTC)

Mechanism: encode each other point by two distances to a closest pair; use separated radius values and planar circle intersections.

Outcome: proved n-2<=2k(2 floor(m)+1)<=6mD, then D>=sqrt((n-2)(sqrt(n)-1)/12). This reconstructs the known 3/4 exponent and gives a linear bound when m has an additional absolute upper bound.

Gap: minimum distance can grow with n. Packing alone gives the 3/4 exponent. General-target completion: 0%.

## Approach 3: attained unit distance and normalization (16:47-16:52 UTC)

Mechanism: equality in the reverse triangle inequality around an attained unit pair.

Outcome: proved containment in two perpendicular lines and D>=(n-2)/2 for m=1. The 3-4-5 triangle and the reconstructed nine-point example exactly reject the proposed reduction obtained by dividing all coordinates by m. The source's exactly-unit-minimum variant therefore cannot be promoted to the target.

Gap: the target only says m>=1. General-target completion: 0%.

## Approach 4: strip ordering and width (16:49-16:54 UTC)

Mechanism: order horizontal projections in a strip narrower than one; use disjoint disks in a rectangular enlargement for arbitrary fixed width.

Outcome: proved D>=(n-1)sqrt(1-h^2) for h<1, and D>=pi*n/[4(h+1)]-1 for finite h. These are elementary restricted statements; the stronger literature half-strip result is acknowledged without claiming its full proof was audited.

Gap: no reduction to bounded width. Both width and minimum distance must diverge in a hypothetical sublinear-diameter sequence. General-target completion: 0%.

## Approach 5: potential counterexample constructions (16:49-16:54 UTC)

Mechanism: normalize dense square grids; reconstruct the original finite nine-point example exactly.

Outcome: square grids necessarily have diameter of order n once their distance gaps are normalized. Piepmeyer's nine-point construction has distance multiplicities 6,18,6,6 and diameter between 4.663 and 4.664. All 36 pair distances are certified in Q(sqrt(2),sqrt(3)). Its existence only rules out the unqualified all-n inequality D>=n-1.

Gap: no construction with D/n tending to zero, and no construction contradicting the eventual stronger conjecture. General-target completion: 0%.

## Verification checkpoint

The five substantive approach families above are exhausted. No sixth proof-search family is authorized by this attempt. Further checks should audit the frozen retained claims rather than extend the unfinished search. Exact finite controls pass. A first test run found a missing Python comparison operator in the checker; it was added before the successful replay. No mathematical claim changed from that code repair.

Source and author packet preparation: complete at freeze. General problem: unresolved. Independent audit: pending. No remote publication performed by the author worker.
