# Additive Borel QHI: corrected partial result

Problem **10400135 / AMR-103-0135**, rank 877. **Unsolved, 3/5.** The explicit additive/Thurston-face question is proved for the original 2001 Nth-power Borel invariant. The broader Problem 7.20 remains partial: distinct multiplicative-character and finite-specialization fibers are unclassified.

## Accepted result

For fixed connected closed oriented W, nonempty L, and odd N > 1, the corrected manuscript proves K_N(W,L,rho_a) = K_N(W,L,1) for every complex additive class a. It therefore proves constancy over all real additive cohomology, including the entire Thurston unit sphere and its faces whenever they exist. It also retains the previously claimed diagonal-reduction equality and local holomorphic multiplicative dependence, without classifying global multiplicative fibers.

- [Corrected proof](corrected/PROOF.md), [bounded disposition](corrected/DISPOSITION.md), [three approaches](corrected/APPROACHES.md), and [literature](corrected/LITERATURE.md)
- [Independent mathematical audit](independent_audit/MATHEMATICAL_AUDIT.md), [acceptance](independent_audit/ACCEPTANCE.json), and [exact two-file correction patch](independent_audit/PHASE_ACCOUNTING_CORRECTION.patch)
- [Publication acceptance](PUBLICATION_ACCEPTANCE.json), [static integrity tests](PUBLICATION_TEST_RESULTS.json), and [inventory](PUBLICATION_MANIFEST.json)

The correction separates shared-edge root choices, the halved tensor-charge convention, and fractional-power branches in h. Those h phases are state independent and disappear after the Nth power, giving genuine local holomorphy of K_N. The full-coboundary contraction endpoint stays inside the full-cocycle domain. No canonical unpowered phase or later cusped/reduced invariant is covered.

## Exact provenance and review boundary

All three original ZIPs and their external manifests are preserved unchanged in `archives/`. The five-file original author packet is unpacked in `author_original/` as historical material, the five-file accepted derivative in `corrected/`, and the seven-file audit in `independent_audit/`. The exact patch applies with `patch -p1` to a fresh original-archive extraction and changes only PROOF.md and DISPOSITION.md. Acceptance is bound to the corrected archive and all five corrected file hashes; it is not retroactively attached to the original proof bytes.

Historical freeze fields about absence of publication and review status remain unchanged. The corrected disposition records the bounded independent audit; the proof's caution about further independent review remains appropriate. This is an AI-assisted unrefereed manuscript, not conventional human peer review, formal verification, or a novelty certificate. The proof relies on the original 2001 invariance theorem; the entire source theory was not independently re-proved.

Static isolated normal/optimized controls check byte integrity, archive safety, exact patch replay, acceptance binding, scope, and the narrow queue edit. No archive code is run. No executable mathematical checker, finite QHI experiment, or computational proof certificate is included. Passing static controls is not mathematical proof or a CI-pass claim.

Only authored work and public bibliographic/verification metadata are included. Source PDFs, copied source text, images, raw datasets, private sources, personal data, coordination material, and private checker fingerprints are excluded.

Only this queue row's Status, Turns, and Findings change. Existing notes and chat links, all other cells, and every unrelated current-main byte are preserved. Publication adds no substantive approach. This is a draft PR only; no merge, release, DOI, or outreach is performed.
