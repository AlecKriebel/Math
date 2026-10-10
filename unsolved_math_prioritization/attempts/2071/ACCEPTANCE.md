# Acceptance of prior EP357 partial bounds

## Decision and exact target

Accept Theorem 2.1, Corollary 2.2, Lemma 3.1, Theorem 3.2 and their combined Theorem 1.1 in the pinned version 1 manuscript by Paratelligent Research Agent and Jeff Pickhardt, within this bounded mathematical audit. No mathematical correction is required. The target uses strictly increasing positive integers in [1,n] and distinct sums for every indexed nonempty consecutive block, including singletons and overlapping blocks.

## Accepted claims

1. For the construction a_i=B+y_i, where y_i are the first k nonnegative integers not congruent to -B modulo 3, B>3k^2/16+k/8+1 suffices for all-block uniqueness.
2. The construction yields liminf f(n)/sqrt(n)>=4/sqrt(3).
3. For 0<=U<V, the selected r-block layers pack into the integer points of (U,V], giving the exact count floor(V)-floor(U).
4. For every positive integer n and every positive integer R, f(n)<=ceil(n/2)+floor(n/(2R))+R(R-1)/2.
5. Taking R=ceil((n/2)^(1/3)) gives f(n)<=n/2+((3/2)2^(-2/3)+o(1))n^(2/3).

Every elementary proof and the passage to arbitrary n are retained in AUDIT.md. No external theorem is required by these main proofs. The accepted original audit is 13,724 bytes, SHA-256 2ae73a98dc3113340a4e2d7370b9d10f4a5af76224313aecf8fc1d0701dfbbad. ACCEPTANCE.json identifies the exact edited public AUDIT.md; its changes concern edition/review framing and historical-check references, with no alteration of the mathematical arguments.

## Required qualifications

The Coppersmith–Phillips 1996 abstract inspected in the audit assumes increasing order. It supports the old bound for f; the additional attribution to arbitrary-order g remains unverified, not disproved. The full CP96 proof was not inspected. Sorting is not a valid general reduction. A weakly increasing candidate satisfying the exact singleton-inclusive uniqueness condition is automatically strictly increasing.

The manuscript is a public AI-assisted manuscript, dated 14 July 2026 on the PDF and published 31 August 2026 according to the landing-page metadata. Its PDF byline names Paratelligent Research Agent and Jeff Pickhardt; the landing structured author field names Jeff Pickhardt. No journal peer-review status was verified. Its exact five-page PDF has 61,836 bytes and SHA-256 632302d4350145aa1b3970bd37b35f01cabc733ddafda191af959a5f5f43e411.

The residual f(n)=o(n) question remains unresolved by this work. Neither a matching growth law nor f(n)~n/2 follows. The source search was bounded, and direct tracker access returned HTTP 403; no fresh tracker-status or exhaustive current-literature claim is made.

These AI-assisted authored documents and their independent internal AI audit are unrefereed. Acceptance here means the bounded mathematical assessment described below. No external human peer review, journal acceptance, formal proof-assistant certification, comprehensive priority search, novelty or priority certification is claimed. The two main bounds are prior results credited to Paratelligent Research Agent and Jeff Pickhardt.

Historical finite checks corroborate the proof formulas and edge cases. All three recorded normal/-O/-OO outputs have identical bytes. No mathematical program was rerun for this edition, and no formal certification was performed. Full written arguments, public citations and verification metadata are distributed; executable programs, detailed outputs, witnesses, certificate contents and source documents are not.
