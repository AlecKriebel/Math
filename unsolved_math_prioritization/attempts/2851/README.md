# KP-3.53: restricted strong-Heegaard Fano diagnostic

Problem **2851 / KP-3.53**, rank **914**, remains **unsolved**, at **3/5** approaches. The independent audit accepts the original author archive unchanged as a restricted partial result.

## Exact accepted result

The specified positive unweighted 7-by-7 Fano incidence matrix has determinant and permanent 24 and nonplanar support. All 16,384 cyclic-order choices for its fourteen oriented curves have boundary histogram 1:2688, 3:11680, 5:2016. Thus their regular neighborhood has minimum genus nine and cannot embed in a genus-seven surface. This rules out this proposed geometric candidate and a purely algebraic planarity shortcut.

This does not construct a manifold counterexample, classify strong L-spaces, handle arbitrary weighted matrices or local signings, or establish novelty. The all-genus alternating-link branched-cover question remains unresolved. No formal proof assistant or human peer-review certification is claimed.

Read the [original report](original_author/REPORT.md), [attempt log](original_author/ATTEMPT_LOG.md), [full independent audit](independent_audit/INDEPENDENT_AUDIT.md), and [exact acceptance](independent_audit/ACCEPTANCE.json). The independent boundary calculation uses an undirected corner-band graph, separate from the author's boundary-permutation tracer.

## Preserved evidence and verification

Both original ZIPs, all ten author members, all fifteen audit members, external manifests, and the audit receipt are preserved byte-for-byte. The audit ZIP also preserves the original author ZIP and manifest. Historical pending-audit and unpublished fields remain unchanged; [publication metadata](PUBLICATION_METADATA.json) supplies the current canonical unsolved 3/5 disposition.

The replay checks normal and optimized execution, relocation, fifty fixture rejection runs and fourteen artifact-integrity rejection runs. Exact source-input replay verifies three complete local corpus streams, the unique exact record, the empty exact-key report, the complete record/report hash and statement hash, and five local PDF hashes/sizes. These checks reproduce byte pins and previously recorded results; they do not constitute new source retrieval, intellectual inspection, literature search, or mathematical research. Targeted source inspection and its limitations remain in the original audit. No source PDFs, copied source extracts, corpus contents, private sources, or private coordination are included.

## Reproduce

Python 3, standard library only. First authenticate PUBLICATION_MANIFEST.json against the out-of-band SHA-256 in the draft PR description. The verifier cannot authenticate its own replacement. From this directory:

    python3 -B verify_publication.py . --manifest-sha256 HASH --replay
    python3 -B -O verify_publication.py . --manifest-sha256 HASH --replay

The wrapper authenticates all archives and members before extracting and executing code. Explicit fail-closed controls are exercised in both modes; [saved local results](PUBLICATION_TEST_RESULTS.json) record the checks. The --base-queue and --queue options verify that only the target row's Status and Turns cells change, preserving Findings and all unrelated bytes. Optional --catalog, --problems, --research and --pdf-dir arguments repeat exact private-input pins, emitting only match metadata. The PDF directory supplies k3.pdf, greene_levine.pdf, usui.pdf, pfaffian_extended.pdf and agol_chainmail.pdf.

This is a draft research PR. Local verification is distinct from GitHub CI; the PR reports the observed remote checks. No merge, release, DOI, or outside outreach is included.
