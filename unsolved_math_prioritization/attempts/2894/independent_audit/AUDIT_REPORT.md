# Independent acceptance audit: KP-4.18 / ID 2894

Audit date: 6 October 2026. Rank 917. One of five author approaches used.

## Decision

Accept the corrected packet as an **unsolved, split-status literature result**. Part (a) is an affirmative prior result by the cited HU-to-KNV implication. Part (b) remains unresolved in the inspected primary literature. This is mathematical acceptance of the stated implication with its cited theorem dependencies, not an independent verification of every algebraic L-theory input. No new solution or novelty is claimed.

The author freeze is preserved byte-for-byte. Its mathematics is acceptable at this dependency level. A corrected derivative is required for canonical status: the original status and checker insist on `partially_solved`, whereas the combined problem and queue must remain `unsolved`, 1/5, with qualified findings. A second documentation correction adds the ZIP argument to the advertised verification command; the original two-argument invocation never checked the archive.

## Statement and complete-input gate

The complete catalog, problems corpus, and research-results corpus were independently rehashed, parsed, and checked, not merely sampled. Their byte counts are 21,735,099; 68,931,837; and 80,334,822. All supplied SHA-256 pins matched. The exact ID was unique, with rank 917 and number KP-4.18. The complete record/report pair reproduced the default sorted-key Python JSON pin `d3eff8f9d1374e5a0c43ee943e6db924980158282869ebd7c874bd0a243cc429`. The report object is empty; the complete inherited background contains literature triage, not a prior authored proof. That gate passes.

Both subparts match the actual K3 PDF page 204 after the declared NFKC/lowercase/alphanumeric normalization. The raw statement hash and normalized statement hash also match. K3 imposes smoothness and closedness, asks for existence of pairs, and imposes no orientability restriction. The audit does not mistake a nonsimple specified map for a pair admitting no simple equivalence, or a specified nonsimple h-cobordism for endpoints admitting no s-cobordism.

`INPUT_SOURCE_CHECKS.json` contains only verification metadata, not corpus contents. `validate_inputs.py` can replay the whole-input and primary-PDF identity checks with separately supplied inputs.

## Mathematical acceptance

The detailed authored analysis is in `MATH_AUDIT.md`.

- [HU v1](https://arxiv.org/pdf/2602.05003v1), Corollary D, p. 5, gives the strict inclusion ker κ₂ˢ ⊊ ker κ₂ʰ. Corollary 4.9, p. 16, supplies SmallGroup(128,1377), with nonzero simple assembly and zero homotopy assembly. The proof route through Theorem C, Theorem 4.3, Lemmas 4.4–4.7, and Theorem B/Lemma 3.4 was inspected. In particular, the argument does not confuse zero after 2-adic completion with integral vanishing.
- The group is finite and therefore finitely presented. Its oriented assembly maps are compatible with those in [KNV v2](https://arxiv.org/pdf/2405.06637v2), Theorem C, pp. 3 and 20–21. HU's global localization at 2 does not lose information on images of the exponent-2 source H₂(G; Z/2).
- KNV provides smooth, closed, connected, oriented four-manifolds, with fundamental group G*G, that are actually homotopy equivalent and admit no simple homotopy equivalence even after the allowed S²×S² stabilizations. The conclusion is unmarked and also excludes orientation-reversing simple equivalences; changing normal 1-smoothing or orientation cannot erase the nonzero mod-2 obstruction against the zero comparison class. Zero stabilization answers K3 part (a).
- No smooth h-cobordism between those endpoints has been supplied. [KP v2](https://arxiv.org/pdf/2604.27635v2), Question 1.2, p. 1, explicitly retains the general h-versus-s question. Its Theorem A/Corollary B retain finite fundamental group, connectedness and orientation, and their listed extra hypotheses. Finite-cyclic positive cases do not answer the unrestricted question. This supports the recorded unresolved status; it is not a proof from an unsuccessful search that no result can exist.
- The packet's Whitehead torsion composition/set criterion and the implication from an s-cobordism to a simple equivalence are correct. No realization theorem in another dimension or the topological category has been silently substituted for the required smooth four-dimensional result.

The HU source contains local typographical issues discussed in `MATH_AUDIT.md`. They do not change the exponent-2 and parity arguments needed here. The supplied exhaustive parity/model checks concern only local finite group identities; they do not reproduce the GAP group identification or certify L-theory.

## Source audit

All five local primary/reference PDFs reproduce the author-pinned SHA-256 values and sizes. Actual page counts are K3 436, KNV 26, HU 36, KP 9, NNP 56. Fresh text extraction was performed for each, with visual inspection of the decisive statement pages. Official arXiv records were checked on the audit date: HU displayed v1 without a journal reference, KNV displayed the cited PLMS 2025 publication, and KP displayed v2 revised 22 July 2026. We did not independently redownload all PDF bytes; this is a local exact-byte check plus independent content and public-record inspection. The inaccessible live problem-page history remains author-reported and was not needed for statement identity.

No source PDFs, source extracts, dataset contents, private sources, or private coordination are in this package. Public bibliographic citations, hashes, byte counts, inspection metadata, and authored mathematical analysis are included.

## Executable integrity audit

For both the exact original freeze and final corrected derivative:

- Four positives passed: normal Python and `python -O`, each in the original location and a relocated directory containing spaces.
- Twelve original-style negatives rejected: changed status, extra file, missing file, symlink, duplicate manifest key, and archive-byte corruption, each in both modes.
- Thirty additional adversarial controls rejected in both modes: empty directory, symlink root/manifest/archive, manifest path traversal and duplicate inventory, duplicate/traversal/symlink/extra/directory ZIP entries, altered ZIP payload, and rebound false-full-solution, wrong-part-(b), and wrong-turn claims.

For ZIP structure tests the archive digest and size were deliberately rebound in a temporary manifest, so the checks actually reached archive structure/payload logic. For selected semantic tests only the mutated status-file identity was rebound. Every fixture was temporary. These are finite integrity/consistency checks, not theorem certification or proof of correctness for all possible adversarial inputs.

The original author's validation receipt was not treated as evidence of current test success: all tests were independently rerun on the exact supplied final freeze. Complete sanitized results and the replay driver are included.

## Derivative and exact acceptance

`correction.patch` applies to the original eight-file packet. It changes canonical status and its checker, adds explicit strict-kernel/orientation/localization scope, updates audit language, and fixes the documented archive-check invocation. The patch was replayed into a separate extraction and its eight resulting file hashes were compared with the corrected manifest. The original ZIP and original external manifest remain unchanged.

`verify_acceptance.py` pins both retained external manifests before executing either verifier, checks the bound archive, safely extracts exactly the expected eight ordinary files, then runs each checker in normal and optimized mode. This provides an independently pinned replay entrypoint; it is not a signature. The encompassing audit ZIP itself is bound by its separately retained external manifest and receipt. Trust in a mutable manifest alone is insufficient against replacement of both packet and manifest.

No GitHub or queue mutation was performed. Canonical queue recommendation: **unsolved | 1/5**, with part (a)'s cited-theorem affirmative result, HU dependency/preprint status, and part (b)'s unresolved status explicitly stated in Findings.
