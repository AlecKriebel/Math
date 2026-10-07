# Round 1 scoped addendum: final documentation and citation corrections

Independent reviewer: complete_review_one. Checked 2026-10-07 UTC. This addendum supplements, and does not overwrite, REVIEW.md and PACKAGE_AUDIT.json. Those files retain the original complete review and its exact candidate chronology. No source manuscript, production manifest, shared Git state, or publication service was changed by this reviewer.

## Exact scope and verdict

I independently compared the current archive with the original round-1 extraction and inventory. Exactly five of the 39 packaged source files changed: four administrative status documents and one priority-note pinpoint citation. The other 34 source files, manuscript, compiled PDF, and production metadata manifest remain byte-identical. I read every changed passage and the corresponding primary-source theorem. No substantive mathematical, framing, attribution, or package issue was introduced by these edits.

This is a scoped review of the changed files and archive reconstruction. It is not a second independent complete-package review, does not replace the fresh round-2 review, and does not broaden the original mathematical verdict: the quantum region is an attributed EPnI consequence; the literal original private positive claim is refuted at zero energy; the positive private region uses the explicitly different generated-secret convention.

## Citation correction

The priority ledger previously identified the general conditional exponential entropy-power inequality as Eq. (13), Theorem III.1. I independently reopened [Falco–De Palma, arXiv:2410.14472v2](https://arxiv.org/html/2410.14472v2) and checked Section III.E: Theorem III.18 is the relevant finite-average-energy multimode conditional result, with finite entropy of the memory and conditional independence of the input systems. Its inequality is Eq. (84), also reproduced as Eq. (108). III.1 is the linear-mixing definition, not this theorem.

The repaired reference is correct. The beam-splitter matrices in Example III.17 and the vacuum specialization in Lemma IV.6, Eqs. (107)–(108), give the exponential entropy-power lower bound. Consequently this citation correction does not turn that literature into a proof of the stronger sharp photon-number inequality. It changes no argument, theorem, or novelty claim in the candidate.

## Administrative edits

README.md, CURRENT_THEOREM.md, DEPENDENCY_LEDGER.md and APPROACH_TABLE.md replace mutable “no deposit yet”/“pending review” assertions with references to separately maintained review and publication receipts. I verified that these edits contain no positive assertion of a completed publication, no new mathematical claim, and no deletion of the original private-model limitation or AI/human-review disclosure. Keeping live operational status outside the immutable mathematical archive is appropriate.

## Exact archive verification

The current deposit archive has SHA256 `e9f9adb0dca6f7776b215672ab97b7f8922aae415d2d9f73afd631259ca40fab`, 114329 bytes, and MD5 `02e5c67a66da959846e0c154c23877d4`. I independently validated all 40 entry names, absence of unsafe or duplicate paths, CRCs, the 39 source-file lengths and SHA256 values, equality of SOURCE_INVENTORY.json with the external inventory, and byte identity of every source entry with its current reviewed local file.

I extracted the current archive to a new review-owned clean directory, supplied the previously independently reviewed and byte-unchanged PDF as manuscript/main.pdf, and ran the archived `python3 code/build_package.py`. The rebuilt ZIP, PDF, and PACKAGE_INVENTORY.json were byte-identical to the current intended uploads. Because only documentation changed, this scoped check did not rerun the mathematical certificates or recompile/re-render the unchanged PDF; the original full review records those checks. The final inventory SHA256 is `5aa6a84709f105de02ec451c2d5c4b38d1e1a0316989919caec3c7b5cf420510`.

Unchanged key files:

- manuscript/main.tex: `eda0b20fb843fda3b7b70203b63628e36ebf5d4a1b6c817624d3a5810f9beaab`.
- publication/paper.pdf: `490c6d4d78eb4c2ae829d06f31df1ed1ace955174acec87279f5d5eb8dee8581` (88566 bytes).
- zenodo-deposit.json: `28f17d3562a835e8f683b71955f63eb6dd771746b0ceb3e15d000d1e9b9960be`.

Changed current source hashes:

| File | SHA256 |
|---|---|
| APPROACH_TABLE.md | `6f503a1d1fb3fccffebcc4f6c024248d4a1fd104ec924728e7fcad6d8d24cf8c` |
| CURRENT_THEOREM.md | `3776ce4a511a328aa4aedaf1567cf8dabc3055b76d340d4cfd8975e304bd7ddf` |
| DEPENDENCY_LEDGER.md | `6eb9b55f065ab6db2f0c26dc90107a59c507d9b3170c8616ca54ee4f0b730d60` |
| README.md | `37b3ddc5f289569d774bfff39b2376734b320e09fe65a4406de0a84868632b07` |
| notes/alternate_priority/PRIORITY_AND_ROUTES.md | `1e1703570ed3587fb481719b5392ff5a23625979b7732714aa751da22bb687be` |

ADDENDUM_PACKAGE_AUDIT.json retains original/current hashes, exact scope, uploads and reconstruction assertions; ADDENDUM_RECONSTRUCTION.log records the executed reconstruction output. The previous complete review and test outputs are preserved.
