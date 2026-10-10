# Independent source and scope review: 10400228

**Final verdict: PASS_COMPLETE_CREDITED_SOURCE_RESULT; already_solved at 0/5 substantive author turns.** The requested source-URL correction has been verified. No mathematical correction is required.

Reviewed KNOWN_RESULT.md SHA-256: `3ea640a5237e509ed6492e2468b21114cfd0b5db9ee93ca633eeec54f5ac2bc1`. Review date: 1 October 2026. I did not contribute to the author's construction or source-status route. The only requested change is a PDF locator correction.

## Exact original question

Problem 12.23 on printed p.541 of Ohtsuki's collection asks for a lower bound on maximal Seifert-surface Euler characteristic at a fixed signature for positive links. The page and its following remark were visually checked. The question is not restricted to knots, positive braid closures, a fixed number of components, or special alternating links.

Stoimenow's own 2006 discussion, pp.2351–2352, confirms the maximal Euler-characteristic convention and explicitly tracks split factors. The intended surfaces may be disconnected and have no closed components. Allowing sphere components would destroy the meaning of a finite maximal Euler characteristic. Requiring connected surfaces for all split links would instead produce another question: the r-component unlink has connected-surface maximum 2-r, which is unbounded below at signature zero. The manuscript correctly avoids both convention errors.

## Published input and edition check

The full Baader–Dehornoy–Liechti arXiv versions were read. Theorem 2 expressly treats all positive links, despite the title's focus on knots. The first version, dated 6 March 2015, gives b_1/48 <= sigma <= b_1. The revised version, dated 15 May 2018, gives b_1/24 <= sigma <= b_1. The definition directly below it minimizes the first Betti number over Seifert surfaces. The sign footnote uses the convention positive on positive links; the positive-link definition concerns oriented positive diagrams, not merely braids.

The revised theorem's proof is Section 3, with the Gordon–Litherland setup and canonical-surface discussion in Section 2. The proof and the stated link scope were inspected rather than inferred from the abstract. The author-hosted 2017 manuscript also has the constant 24. Its local version date must not be called the arXiv revision date. The HAL file contains a repository cover and the revised arXiv manuscript.

The arXiv record confirms publication in Bulletin of the London Mathematical Society 50 (2018), 166–173, DOI 10.1112/blms.12124. The final publisher-typeset PDF was not inspected; the author discloses that limit. Both complete arXiv versions already suffice to classify this as a known affirmative answer. This audit does not claim a new proof of the published signature estimate or novelty for its elementary consequence.

## The full link implication is valid

For a Betti-minimizing admissible surface F, every component has boundary, so H_2(F)=0 and chi(F)=b_0(F)-b_1(F). For a nonempty link b_0(F)>=1. Thus

    chi(L) >= chi(F) >= 1-b_1(L) >= 1-24 sigma(L).

The extrema exist because the relevant integer sets are nonempty, the first Betti numbers are nonnegative, and Euler characteristic is bounded above by the boundary-component count. No common optimizer of chi and b_1 is assumed. In particular, replacing chi(L)>=1-b_1(L) with an equality would be unjustified in this generality; the manuscript does not do that.

This proves boundedness below for each fixed signature regardless of the number of link or surface components. Split unknots cause no problem: they have zero first Betti number, zero signature and positive Euler characteristic. If sigma=0, the cited bound forces a union of disks as a minimizing surface. The empty-link convention is handled separately by the weaker chi>=-24|sigma| statement. Reversing the signature sign convention replaces sigma with its magnitude.

No conclusion about slice surfaces, arbitrary quasipositive links, or finiteness of all positive link types at a fixed signature is asserted. The exact source question is fully covered by the credited theorem and the displayed implication. The older constant 48 alone gives the same qualitative resolution.

## Verification and provenance

The initial 12 author entries and six complete PDF hashes matched. The author's 229,310-control output reproduces byte-for-byte. A separate componentwise surface calculation passes 27,392 exact controls, including disconnected unlink and separate-optimizer checks. These are arithmetic convention controls, not evidence proving the signature theorem.

One metadata inconsistency was identified: the pinned Ohtsuki print PDF bytes were initially associated with the screen PDF URL. The correct locator for SHA-256 cf7c5e29b818e647496e888378db7a8620be5386f357691c4c48b51f1ca1f5fe is the publisher URL ending in 024p.pdf. The author was asked to preserve the original manifest, correct this locator and refreeze; no mathematical file changes were requested. The accepted replacement FROZEN_MANIFEST.json has SHA-256 9382dcc5af7c28479fddc671262c248f95a787643869581a7e4330d7811adad4. All 16 entries and six PDFs match; only the current source manifest and SOURCES.md locator changed among the original entries. The original manifest and two source files are preserved byte-for-byte in the historical directory. FINAL_HASH_CHECK.json records the recheck. No blocker remains.

The public result should remain a credited literature correction, already_solved at 0/5, rather than an original signature discovery. Source PDFs, extracted texts and page renderings are reading material and are excluded from this review's portable files.

## Direct primary references

[Ohtsuki, print PDF, p.541](https://msp.org/gtm/2002/04/gtm-2002-04-024p.pdf); [Stoimenow, 2006, pp.2351–2352](https://msp.org/agt/2006/6-5/agt-v6-n5-p12-p.pdf); [BDL first version](https://arxiv.org/pdf/1503.01946v1); [BDL revised version](https://arxiv.org/pdf/1503.01946v2); [arXiv publication record](https://arxiv.org/abs/1503.01946).
