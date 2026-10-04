# Source and status checks

Checked 2026-10-04 UTC. This document records provenance, not a proof that a literature search is exhaustive.

## Exact source and prior record

The requested catalogue entry is [UnsolvedMath 2927](https://www.unsolvedmath.com/problems/2927), KP-4.51. It was attempted first; the live fetch was inaccessible (the saved HTTP response is 403). The task's pinned catalogue corpus contains the exact statement and a dated 2026-08-17 review. No KP-keyed record occurs in the pinned 6,701-entry research-results corpus, so the dated review embedded in the problem record is the prior report available for this target.

The actual source is [K3's author preliminary version](https://bpb-us-e2.wpmucdn.com/websites.umass.edu/dist/b/22144/files/2026/04/K3-problem-list-watermarked.pdf), Problem 4.51, printed pp. 230–231 (PDF pages 230–231, one-based). The pages were rendered and visually checked. The AIM workshop summary named in the catalogue is not substituted for the full statement. Only the relevant mathematical claim is restated; the source PDF is not redistributed.

The prior review mistakenly leaves smoothability of the original HT form as a remaining question, despite also citing [FHMT07](https://doi.org/10.1093/imrn/rnm031), which proves that form nonsmoothable. The unresolved universal target concerns other possible forms and cannot be replaced with that already-excluded example.

## Mathematical sources checked

1. [HT97 author manuscript](https://math.berkeley.edu/~teichner/Papers/form.pdf): Theorem 1 (non-extension), Theorem 2 (rank minus absolute signature at least six), and the exact 4×4 matrix. Published DOI [10.1007/BF02677483](https://doi.org/10.1007/BF02677483).
2. [FHMT07 author copy](https://math.berkeley.edu/~teichner/Papers/Nonsmooth.pdf): Theorems 1.1–1.5, Lemma 2.2, and the Section 2 characteristic-vector construction. The finite-cover obstruction is explicitly attributed to this paper.
3. [Kawauchi 2013](https://doi.org/10.1142/S0218216513500818): Theorem 1.1, double-cover Lemma 2.2, leaf Lemmas 2.3–2.4, Sublemma 2.3.1. Author preprint reached from the [current author bibliography](https://sites.google.com/view/kawauchiwriting); its PDF has deficient text encoding, so the relevant proof pages were rendered and OCRed. Unverified as a full-resolution source.
4. [Kawauchi 2014](https://doi.org/10.1142/S0218216514500291): Corollary 1.2 claims every closed oriented smooth π₁=Z manifold TOP-splits. Author version retrieved from the author's bibliography after the institutional direct download returned a 502 page. Unverified for the full conclusion.
5. [Kawauchi 2018 v1](https://arxiv.org/abs/1804.01380v1): repeats the claimed history and develops definite splitting criteria. It is not independent verification of the earlier descent theorem.
6. Census [v1 (2024)](https://arxiv.org/abs/2412.04768v1), [v2 (13 May 2026)](https://arxiv.org/abs/2412.04768v2), and [journal version (25 February 2026)](https://doi.org/10.1007/s00454-026-00818-w): v1 contains Theorem 7 attributing universal smooth TOP-splitting to Kawauchi; v2 and the journal version omit that passage and the three Kawauchi references. No reason for the removal was established. It is not represented as a retraction or mathematical disproof.

No correction notice attached to the 2013/2014 items was found in the author's bibliography (which displayed an August 2026 update). Failure to find a notice is not evidence that the proofs are correct. Conversely, K3 posing the question does not by itself refute them.

## Distinctions enforced

- “TOP-split” means homeomorphic to (S¹×S³)#N with N simply connected. This implies extension of the equivariant form by examining the universal cover. The converse is part of the cited topological classification.
- Smooth nonsplitting does not contradict TOP-splitting or integral extension.
- A non-extended form realized by a topological manifold is not a smooth counterexample.
- A smooth manifold with boundary carrying such a form does not supply the requested closed manifold; a smooth cap preserving the group and form is additional work.
- No general descent claim is accepted merely from its published statement or later citation.

## Repository duplicate and queue checks

Read-only GitHub checks on main at commit `25aaa7146e257ef5276e80aae60429cf3f4765f9` found rank 596 / ID 2927 queued at 0/5. The own state entry was absent; the exact attempts/2927 contents endpoint returned 404. Code search for 2927, PR searches for 2927 and Hambleton, and branch search for 2927 returned no matches. The related-target group file contains no 2927 group. These checks do not exclude differently named or unindexed duplicates. No remote changes were made during this investigation.

## Provenance and release boundaries

Only original write-ups, an original exact-arithmetic checker and its output belong to the public package. Source PDFs, corpus records, raw page text/OCR, and coordination records are excluded. Public SHA256SUMS hashes precisely the public payload. A separate private source hash manifest is retained for audit.
