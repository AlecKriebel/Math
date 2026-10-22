# EP-839 / 2334: separated-block obstruction and endpoint repair

## Result and unresolved questions

For a strictly increasing sequence of positive integers, admissibility here means that no term equals a sum of at least two consecutive earlier terms. Both original questions remain unresolved for arbitrary admissible sequences: lower natural density zero, and H_A(x)/log x tending to zero. Neither novelty nor priority is asserted.

The complete authored proof and independent audit establish:

1. Prefix-sum-separated blocks B_r contained in [m_r,Cm_r], C>1, satisfy H_A(x) <= (log C/log 2) log log x + O_C(1). No avoidance assumption is needed. Prefix-sum separation alone forces lower density zero.
2. An explicit admissible width-two construction has H_A(x)=log log x+O(1), lower density zero and upper density 1/2. The asymptotic holds for all x.
3. Freud's finite blocks have count 76y-7 and total 7436y²-1406y+70. The finite construction remains valid.
4. For every T>=4 divisible by 4, the printed infinite extension retains consecutive terms (2L+T-2) and (2L+2T+2) and their sum 4L+3T. The full symbolic proof and the sum-polynomial derivation of the source's own seed T=6100 are retained.
5. For every admissible prefix of total T>=3, lowering the last deletion interval's left endpoint from 4L+3T+1 to 4L+3T repairs the extension. The repaired sequence still has upper density 19/36 and has H_A(x)=gamma log log x+O(1), where gamma=[log 2+(19/12)log(9/8)]/log 4.

The restricted separated-block architecture is not known here to contain every admissible sequence. Its obstruction therefore does not solve either original question.

## Two distinct corrections

The substantive correction repairs one endpoint in Freud's printed infinite-extension recipe. It does not invalidate the finite 19/36 construction or existence of an infinite upper-density-19/36 example.

The independent audit also corrected one sentence in our note: at T=4 the left C-bridge term is C's first element, rather than strictly interior. The public PROOF.md already includes this minor wording correction. CORRECTION.patch is a zero-context patch against the original authored note identified in ACCEPTANCE.md; it records only that sentence change and is not meant to be applied again to the corrected publication proof.

## Files and review limits

- PROOF.md: complete accepted written proofs, with only edition framing and the stated editorial omissions
- AUDIT.md: independent mathematical audit and historical verification summary
- ACCEPTANCE.md: exact decision, correction distinctions and scope limits
- CORRECTION.patch: minimal authored-note wording correction, without adjacent private context
- SOURCES.json: public citations, source byte identities and historical inspection scope
- VERIFICATION.json: historical test counts, hashes and match results
- MANIFEST.json: exact eight-file inventory, with hashes of the other seven

Optional large numerical witness values and small finite seed examples are omitted; the complete symbolic witness and all universal arguments are retained. No source PDF, scan, OCR, copied source text, program, raw dataset, detailed computational certificate or private coordination record is distributed. Historical test programs were not rerun during edition preparation. Their runs are not reproducible from this prose-and-metadata edition alone.

This is AI-assisted, unrefereed work. Acceptance denotes an independent internal AI mathematical audit, not external human peer review, journal acceptance or proof-assistant certification.
