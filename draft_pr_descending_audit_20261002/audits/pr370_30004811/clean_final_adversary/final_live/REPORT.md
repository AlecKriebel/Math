# Additive exact-live approval for repaired PR 370

**PASS_EXACT_LIVE_QUALIFIED**, controlled by RECEIPT_gate02. All 134 checks passed. The exact pins are:

* Head: `af92cfc40bbd781fd9a2367214745f6f53a0b12e`
* Authoritative local/API/remote main and PR base: `81185c796181151e49dcf7299a6567ad2abc9695`
* Head/virtual-merge tree: `a5c0a7d1f9229935f56355a302f7dadb551d087c`
* Literal ready PR body SHA-256: `8f4ed19165b1d32c5f89f0359f5a8c6e3d0259e1f847bf4ad59d4ec703dfeca3`

The program captures literal PR/main API responses and remote refs before and after the entire audit. It also checks the actual local main, origin repository, exact head tree/ordered parents and API commit. All identities remained pinned. PR 370 was open, ready, unmerged, and reported mergeable/clean. No merge, release or CI-success conclusion follows from that metadata.

Complete recursive Git tree maps for base and head show exactly 19 changed paths: the 18 original regular target files and QUEUE.md. The target's complete path/mode/blob map is unchanged from original frozen head `567c2e493854b32d0cd325ad96e4c5b69c9c1e1b`. Every target blob's actual local contents were read, and all 18 actual API blob contents were decoded and compared byte for byte. The complete API changed-file projection agrees with the recursive Git delta. All seven candidate JSON objects were fully parsed, and all 29 nested manifest size/hash bindings, exact publication coverage and review-author binding passed.

The ten immutable author files remain byte-identical to author parent `1901d52ea8b47b4dd3c843cb2e02be2c520da7cb`. Historical review provenance is preserved accurately: the four review files are absent from that parent but anchored by the frozen/repaired publication heads and original manifests. The three published family manifests retain their original hashes; all 51 listed original family files and all seven included seals, with their referenced contents, match local bytes and checkpoint/repaired Git objects. The original own-root 18-bound-file PUBLIC_MANIFEST and every original seal/report/log remain byte-for-byte unchanged.

The full base queue matches the independently frozen prior current-main queue from `6466f4a301c94d513435401bf772c285bc7b4c42`. The repaired queue equals exactly the base bytes after changing physical line 410 pipe cells 8 and 9 from `queued, 0/5` to `already_solved, 1/5`. The repaired queue SHA-256 is `c191748daab0e8fda7e634f7c2cbb1821098105a136036452d559fd3945f4871`. Every other byte, including all 27 previously identified unrelated accepted dispositions, is preserved. This is an affirmative credited-resolution disposition with one author turn, not an unsolved disposition.

Seven new primary PDF downloads match every original URL/byte/hash identity. From a private scoped reconstruction of the exact repaired target, the author receipt is byte-exact (5,529 controls), historical review JSON is complete and exact (3,128 controls, seven sources), publication checks pass both source-present and source-free with complete expected JSON, and ten independent symbolic controls pass. The mathematical artifacts are unchanged, so the original sealed proof reconstruction applies directly. Drift-negative controls reject altered head, main, body and readiness; an unrelated queue byte is also rejected.

The controlling program is exact_live_gate.py. PINS, the complete gate02 receipt, limitations, log, both program versions and the preserved gate01 receipt are included in the self-excluded additive public manifest. Raw API/Git streams, newly fetched sources and replay copies remain ignored and private. No candidate/root/old-review file, Git object/index/branch/ref or service state was mutated by this reviewer.

The exact-live review is 100% complete for this observation interval. The root's separately replayed controlling program and actual merge/post-merge checks remain subsequent acceptance steps. No mandatory mathematical or artifact repair is identified for the pinned package. Main/head/body drift invalidates this approval and requires rejection plus a new gate; it must not be silently accepted under these receipts.
