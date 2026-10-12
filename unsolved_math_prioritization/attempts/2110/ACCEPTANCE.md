# Acceptance of the density one distinct consecutive products reconstruction

## Decision and exact target

Accept the complete authored reconstruction for problem 2110 / EP-421: there is a strictly increasing positive-integer sequence of natural density one with pairwise distinct products over all nonempty consecutive index blocks. The conclusion is proved analytically, using the explicitly identified published and standard theorems. The independent computational-assistant audit and a second computational-assistant review checked the complete proof. This is an assessment of the authored reconstruction, not human review, peer review, or external scholarly acceptance.

## Credit and scope

The retained-prime construction, stable witnesses, split-product argument, and parent-gap organization are credited to Przemek Chojecki, *Distinct Consecutive Products*, dated 13 July 2026: https://ulam.ai/research/erdos421-sol.pdf. Its first-page footnote credits GPT-5.6 Sol for discovering the proof while iterating on the author's previous attempts. No novelty is claimed for this reconstruction. The public manuscript's sharper exponent and every argument in that manuscript are not certified here.

The reconstruction uses Jia's published 1996 almost-all short-interval theorem, fixes theta=3/50, and replaces the source's multiscale sum by an explicit one-step recurrence. The two published analytic theorems are imported with their stated quantifiers; their full proofs are not re-audited. Li's newer prime-interval preprint and any claimed Lean artifact are not dependencies.

## Checked mathematical obligations

1. The stable retained-prime construction has distinct products for all finite nonempty blocks. Cancellation gives separated witnesses, and a rejected gap's prime endpoint can always be retained.
2. Raw witnesses are full integer intervals. Nonraw witnesses cross a prior rejected gap, giving a finite parent forest with stable retained adjacencies.
3. Jia's exceptional-integer-start estimate bounds total long-gap length by O(sqrt(X)+X(log X)^(-B)) for compatible fixed B>2 and eta<3/50.
4. Weighted initial forms force every absolute component of each split-product curve to have degree at least two. The coefficient- and degree-uniform CCDN theorem, together with Galois conjugacy and Bézout, gives the stated raw-short-gap count.
5. Fixed-parent out-degree, unequal-edge contraction, the long-parent count, and the impossibility of a long-to-short equal edge give all parent estimates.
6. Fixed-multiplier equal-chain compression counts endpoints without assuming independent branching or bounded depth. The three covering cases exhaust all short rejected gaps.
7. The explicit recurrence closes at alpha=93/100. Total rejected short-gap length is O(X^(99/100)); the long-gap estimate and the final boundary-gap argument give natural density one.

## Finite verification boundary and editorial correction

Exact checks were rerun in normal Python, -O, and -OO; all outputs are byte-identical to the audited aggregate summary. The independent checker uses explicit exceptions, not removable assertions. Counts remain unchanged: 391 retained integers through 503; 74 accepted and 21 rejected gaps; 46 collision pairs; 12 raw vertices and 9 selected unequal edges; 3,944 necessary edge configurations; and 7,884 weighted-degree cases.

The original summary records one short prime gap, correctly. The original audit prose incorrectly said there were none. The sole short gap is (2,3), with empty interior, and it is accepted. There are no eligible short child gaps and no selected equal chains in this range. The finite no-long-to-short-equal check is consequently vacuous for the asymptotic mechanism, and no general equal-chain or density claim is inferred from these tests. The public audit and summary correct this wording while preserving all counts and the complete mathematical argument.

See PROOF.md for the standalone reconstruction, AUDIT.md for the complete independent proof audit, CHECK_SUMMARY.json for aggregate checks, and EDITORIAL_MAP.json for the bounded changes from the accepted inputs.
