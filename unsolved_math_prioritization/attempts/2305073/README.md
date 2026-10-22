# Korenblum Riesz-potential majorants: audited partial results

Problem **2305073 / AMR-022-5073**, rank 682. **Unsolved after five substantive approaches (5/5).**

For each fixed real 0 < alpha < 1, the kernel is exactly |x-t|^(-alpha) on the real line and the majorizing measure is a finite positive Borel measure. The original arbitrary-measurable, pointwise characterization remains unresolved.

## Results and scope

- Exact smooth-test duality and least-mass attainment for Lebesgue-almost-everywhere domination; the same criterion applies pointwise to lower semicontinuous obstacles.
- Equimeasurable finite-valued Borel obstacles with opposite majorizability outcomes, excluding rearrangement-only criteria.
- A finite-valued obstacle on a compact null Cantor set with no pointwise majorant. This disproves an a.e. reduction, not the open-ended original characterization problem.
- A constructive interval-cover sufficient condition which is not necessary; arbitrarily small countable-set repair; explicit obstructions to naive point-constraint compactness and sampling.

The singular bounded-potential-measure test is necessary only. No general sufficiency, complete pointwise solution, or novelty claim is made.

## Preserved research and independent review

- [Frozen authored proofs](author/PARTIAL_RESULTS.md) and [five approaches](author/APPROACH_LOG.md).
- [Complete independent audit](audit/INDEPENDENT_AUDIT.md): PASS as partial results, with no blocking mathematical corrections.
- Both original directories and the original six-file audit ZIP remain byte-for-byte unchanged. The authored packet's historical pending-audit statements are preserved; the later audit and [release status](RELEASE_STATUS.json) supply the chronology.
- Original 11,515 exact finite controls and 12,073 independent checks pass with byte-identical output. Finite controls do not replace analytic proofs or constitute formal verification or journal peer review.

## Portable verification

From any working directory, run:

```sh
python3 /path/to/2305073/verify_release.py
python3 -O /path/to/2305073/verify_release.py
```

Only Python's standard library is required, with no network access or source material. The verifier enforces the complete 19-file inventory, both pinned frozen manifests, six ZIP-member byte comparisons, normal and optimized author/audit replays, and fourteen rejecting mutation controls. Its output must match [RELEASE_CHECKS.json](RELEASE_CHECKS.json) byte for byte. The manifest is an integrity inventory, not a signed authentication mechanism.

## Source and publication limits

Primary source: Hayman and Lingham, [Research Problems in Function Theory (New Edition), v2](https://arxiv.org/abs/1809.07200v2), Problem 5.73, printed p.111. Source inspection and bounded literature-search limits are recorded in the frozen source and audit metadata. The 2018 no-progress update does not certify the current global literature status. The recorded source-PDF hash covers cached bytes; fresh remote PDF-byte equality is not claimed.

Only authored mathematics, code, the full audit, and public verification metadata are added. No source PDFs, source-page images, extracted source text, dataset contents, or private coordination records are included. Only this problem's queue Status and Turns cells change; all other existing queue bytes, including its pre-existing header and links, are preserved. This is a draft for review, with no merge, release, DOI, or outreach.
