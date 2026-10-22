# Independent audit: Function Theory 6.46

**Qualified PASS for a credited prior-literature resolution.** Target 2306046 / AMR-022-6046, rank 684. This is an independent AI source, scope, elementary-proof, code and frozen-byte audit, completed on 2026-10-05 UTC. It is not human peer review, a new discovery, or verification of the original general proof.

## Exact result and source match

For every normalized univalent holomorphic map of the unit disk with image starlike about zero, write its coefficients as a_n, with a_1=1. The exact target is the two-sided inequality abs(abs(a_(n+1))-abs(a_n)) <= 1 for every integer n >= 1.

Independent visual inspection of [Hayman–Lingham, arXiv:1809.07200v2](https://arxiv.org/pdf/1809.07200v2#page=136) confirms the exterior absolute-value bars in both Problem 6.46 and Update 6.46. The update expressly credits Leung with the complete result. Chapter 6, printed p. 114, supplies the normalization; reference [510], printed p. 234, identifies his article. Historical growth-qualified partial results on the target page are not hypotheses of the final result. The close-to-convex weighted inequality is a different claim.

The [publisher's issue contents](https://academic.oup.com/blms/issue/10/2?browseBy=volume) confirm Yuk Leung, *Successive Coefficients of Starlike Functions*, Bulletin of the London Mathematical Society 10(2), July 1978, pp. 193–196, [DOI 10.1112/blms/10.2.193](https://doi.org/10.1112/blms/10.2.193). The original proof was not retrieved or audited. [Arora–Ponnusamy–Sahoo, arXiv:1903.10232v1](https://arxiv.org/pdf/1903.10232v1#page=2), Theorem A, independently corroborates the inequality, quantifiers and attribution. Its equality-only wording is not imported: the identity map attains the lower endpoint at n=1 but is not a unit-pole two-factor map. This does not contradict the inequality.

Both versioned public PDFs were freshly downloaded with HTTP 200; their bytes and SHA-256 values match the author's records exactly. Relevant pages were inspected visually from these byte-matched sources. No entire-book or full-paper proof audit is claimed.

## Elementary mathematics and exact replay

All five sections of the author's PROOFS.md were checked. The cross-multiplied injectivity factorization, positive-real-part identity, radial-image argument, sine formula and forward/backward inequalities are correct, including coincident poles. Koebe, odd, third-root and identity examples are valid. Scaling and rotation are correctly scoped. The rational modulus predicate correctly handles the nonpositive-T branch before squaring. None of these controls reduces all starlike functions to the two-pole family.

All 23,516 author assertions replayed exactly. An independent audit added 7,840 checks: direct rational-norm oracles in both argument orders, a separately derived squared-norm criterion, convolution-generated coefficients, mathematical mutants and inventory controls. These are modest finite verification controls, not a proof of the general theorem.

Seven mathematical mutants were rejected by the independent oracle. Two survive the author's original suite: using only the upper bound, and deleting the nonpositive-T shortcut. These are coverage limitations, not defects in the frozen predicate. Concrete witnesses and all outcomes appear in EXACT_REPLAY.json.

## Frozen-byte and publication boundary

The external author-manifest pin is 25781fa24baec94cb7087c89e39f7930a97d973a5a4875a57c5a3c6cb8a52411. All nine frozen author files match; total size including the manifest is 32,360 bytes. The author tree remained unchanged.

The author's standalone integrity script does not pin its manifest and accepts a symlink at the manifest path. It also accepts a manifest-only change, coordinated manifest/payload edits, and extra empty directories. The supplied verify_frozen_author.py authenticates the external pin and rejects all non-regular entries, including the manifest. All eight altered-inventory controls are rejected by that stronger gate. Use it as the publication gate.

The commit-pinned queue blob and catalog descriptor agree with the author's recorded hashes. The queue's apparent older descriptor is literal file content, not GitHub response metadata. Saved bounded duplicate-search observations were reviewed; they are not a comprehensive all-branch absence certificate. The full imported problem corpus and prior AI report were not inspected or verified. The exact primary-source resolution remains the disposition basis.

Campaign accounting is one substantive prior-result response out of five. The author's zero fresh-discovery approaches is a different count and remains unchanged. The frozen author's pending-audit fields are historical; this separate audit records the completed review. No artificial five-approach history is asserted.

The publication candidate consists only of the nine author files and the files listed in AUDIT_MANIFEST.json, plus that audit manifest. Source PDFs, source extractions, source-page images, imported dataset contents and private coordination files are excluded. No remote write occurred during this audit.

## Reproduce

From the packet's parent directory:

    python -B audit/verify_frozen_author.py
    python -B audit/replay_audit.py

Both scripts also accept the author directory as their sole positional argument. The first authenticates bytes; the second compares the stored author controls, exercises independent mathematical controls and tests disposable mutated copies. It never modifies the frozen author directory.
