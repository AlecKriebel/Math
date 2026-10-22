# Corrections to the frozen author packet

These corrections apply to a future working/publication copy. The frozen ZIP and original files remain unchanged.

## C1. Actual assertion count (required reporting correction)

In verify.py the first accepted-triple loop executes five assert statements, at original lines 18, 19, 20, 22, and 23, but increments its counter by six at line 24. There are 1,120 accepted triples.

- Change that n+=6 to n+=5.
- In CONTROL_RESULTS.json, change exponent_and_moment_identities from 6720 to 5600.
- Change total_exact_assertions from 8700 to 7580.
- Any new freeze metadata or publication summary must use the corrected count or explicitly identify 8,700 as the original erroneous reported count.

All actual assertions passed. The saved result otherwise reproduces exactly. Chained comparisons and conjunctions remain single Python assert statements, consistently with the other families; no alternative subcomparison-count convention is being imposed.

## C2. Fixed metric rescaling (recommended precision correction)

For an index-h regularly varying gauge, multiplying a metric by c multiplies its Hausdorff measure by c^h. For arbitrary gauges, instead use the exact relation H^g_(c d)=H^{g(c dot)}_d. Replacing the gauge by g(r/c) preserves the same represented measure. Thus existence of some scalar exact gauge is unaffected by the constant metric convention, but arbitrary fixed-gauge measures need not be related by one scalar.

The sentence in Proposition 2's metric warning is correct in its immediate regularly varying context. The patch makes that context explicit and prevents the sentence from being read as a claim about every irregular gauge.

## C3. Radius convergence (optional exposition)

In Approach 5, the inverse branches on a disk of fixed radius omit a fixed pole. Koebe's quarter theorem bounds their derivatives at the fixed preimage x, so 1/D_j stays bounded. Since d_j tends to zero, the radii K d_j/D_j tend to zero. This may be added to the text if a fully explicit density argument is desired. It neither repairs a failed theorem nor supplies the quantitative recurrence estimate still missing.

## Preserved caveats

Keep the basin-attraction qualification, the distinction between derivative-zero critical points and poles, the arbitrary-gauge gap, the distinction between global ball bounds and exact representation, and the conformal/invariant-measure distinction. Preserve UNSOLVED and 5/5 exhausted. No change to the author's mathematical conclusion is warranted.

CORRECTIONS.patch changes only C1 and C2. The overlay's revised payload hashes are recorded in AUDIT_BINDING.json. The audit does not authorize relabeling the original frozen bytes as corrected.
