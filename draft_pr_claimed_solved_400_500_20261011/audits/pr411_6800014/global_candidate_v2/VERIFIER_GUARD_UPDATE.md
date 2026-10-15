# PR411 / 6800014 — version 2 software component handoff

**PASS, zero software blockers, 100% of this bounded component task at 2026-10-13T02:32:58.031542+00:00.** The producer and a newly assigned independent software adversary authenticated the same final bytes and replayed normal and optimized entrypoints successfully. Producer additionally repeated all 38 corruption/reproducibility controls against this final sealed bundle; every expected outcome and required diagnostic matched. This external record supersedes the sealed reports' honest 95% pre-custody checkpoint without changing their frozen bytes. Parent v2 software acceptance and later sequential whole-preprint adversaries remain separate.

## Actual custody and replay

| Object | Actual SHA256 |
|---|---|
| `verification_v2/FINAL_SEAL.json` | `6fb571bf3f2e8c36cdea70832efcdab15a48bab75db40e67a9ebce496390e7fb` |
| `verification_v2/PUBLICATION_WHITELIST.json` | `6ea7bf4432ef4659340a94b1077fc804b1203d141fbf4231868f8844644fddf1` |
| Preserved original `verification/FINAL_SEAL.json` | `28ffa75ad2854db27f5793f28421fc3f041bedf3dcd7708e2f5bca0d944552c5` |

The whitelist schema is `pr411-verification-positive-whitelist-v2`, packet version 2: **71 positive files / 73 total**, omitting only the whitelist and final seal from self-custody. The actual seal binds the real whitelist digest. This external digest record and the parent's independent outer custody bind the actual seal. Neither object hashes itself, and no report claims a future own-report seal hash. This is unkeyed integrity under independently authenticated custody; simultaneous replacement of all code, content and custody is outside the boundary. Byte binding does not prove arbitrary prose semantics.

After authenticating custody, use a private Python environment outside the bundle with `sympy==1.14.0`. Exact replay used Python 3.14.6, SymPy 1.14.0, mpmath 1.3.0:

```sh
/path/to/private-venv/bin/python -B /path/to/verification_v2/run_all.py
/path/to/private-venv/bin/python -B -O /path/to/verification_v2/run_all.py
/path/to/private-venv/bin/python -B /path/to/verification_v2/reproduce_controls.py --private-log-dir /path/to/private-control-logs
```

The entrypoint accepts no arguments and locates the package from its own path. A clean relocated archive extraction into a path containing spaces passes in both modes. Both producer and independent final native outputs report 19 original author files, 19 current files, 18 publication-manifest entries, six frozen files, exact original 39 predicates and 54 mandatory evaluations. Final stdout SHA256s are `913b6f625ab3700929deae903074edc796c7dbdeb45bb959d0af9d928c8cdf00` (normal) and `889f7802d30339e497cadabd2755e055d98d5d5fb5ee6685f82fd0a8196d7a5a` (-O). All final 73 bytes and all released v1 55 bytes stayed unchanged across tests.

## Exact change boundary

`global_candidate_v2/author_packet/` and `verification_v2/author_packet/` are exact synchronized nineteen-file current packets. Relative to original PR-head nineteen files, exactly eight paths change: the three previously guarded mathematical scripts plus README, SOURCE_AUDIT, EDITORIAL_CHANGES, RESEARCH_LOG and PUBLICATION_MANIFEST. Relative to v1, only those five prose/metadata files change. All three current mathematical scripts, proofs, six frozen originals, frozen metadata, historical audit and original nineteen inputs remain exact prior bytes.

Among standalone executable code, only `run_all.py` changes: whitelist schema v1→v2 and `SOURCE_AUDIT.md` added to the allowed current prose set. The full AST/source relation has exactly those two substitutions. `guard_relation.py`, `run_checked.py` and `reproduce_controls.py` remain exact v1 bytes; strict nonregular-entry and symlink rejection is preserved. The independent adversary tested all 38 native controls, 65 supplementary child executions and 13 direct path/entry probes; stateful truth, lazy Boolean traps, per-label counts and independently reversed complete original AST all passed. Frozen reports retain authentic provisional custody; independent final native receipts below fulfill their remaining completion condition. No original failed receipt or finding was replaced.

The current source/README prominently supersede old source-version/status interpretations while retaining complete prior text verbatim. Prior publication base, queue-change and v1 software-review values are preserved under explicit `historical_v1_*` keys; current metadata says no v2 queue mutation and distinguishes current review from the copied v1 parent gate. The manifest binds its eighteen other current files; the independent whitelist binds the manifest itself.

Source addenda credit the exact 23 July 2018 existence announcement, identify inspected I arXiv v1/v2 and II v2, and leave inaccessible final journal full texts NOT ATTESTED. Bounded priority coverage remains 40 issued queries / 13 successful primary PDF downloads, PASS_QUALIFIED, with exact separately sealed bibliographic erratum context. Novelty, first assertion, first proof and current community-open claims remain WITHHELD. The actual displayed E_t ratio is `25t^4/(59t^4+32t^2)`, E1=25/91 and E2=25/67; the distinct original 9/17 witness and main proof are unchanged. Separate priority-parent acceptance is not certified by this software component.

Original historical optimized assertion outputs remain NOT CERTIFIED. Two absent historical digest-only byte objects remain UNATTESTED: standalone manifest `f5446c816081c5322e4279bcd9a61dca5bfb63cfacf69d105d1587ed9d93b7fb` and pre-layout checker `eccde3c2a903b1fca0f232e7e392d537479ddd3936281a37e87c4f7e7047be97`. No novelty, human peer-review, publication or whole-preprint acceptance is certified. Source PDFs/raw third-party material/corpora/fixtures/runtime/venv/private state are excluded. The nineteen-file author-proof omission statement does not silently govern separately prepared authored preprint/verification artifacts, which require a positive parent outer delivery whitelist.

## Native final receipts (private, excluded from delivery)

These exact raw receipts preserve commands, return codes, stdout/stderr and diagnostics. They are not replaced by a trusted-true attestation. Parent inspection can authenticate them using these actual hashes:

- `private_sources/verification_repair_v2/FINAL_PRODUCER_VERDICT.json` — `bcae233f4d6d7c03aa4030a0885257625fb22a5e1fcfea63848b54889a0506d9`
- `private_sources/verification_repair_v2/FINAL_NORMAL_NATIVE.json` — `c2292ab9db0d88af6a665a552baa3b3a62116db2d32a03218456f5601822cde1`
- `private_sources/verification_repair_v2/FINAL_OPTIMIZED_NATIVE.json` — `978c20f1a0acb63afa44984d5c1e18d18dc7d67e50eec29c5e1e0cf093eeb63e`
- `private_sources/verification_repair_v2/FINAL_38_CONTROLS_NATIVE.json` — `ef963de6e621292a05ad1898c771248480679270ea5b3c6041054bb8e66aebf9`
- `private_sources/verification_repair_v2/FINAL_SCOPE_GATE.json` — `4a7382df452e9cd0e1ad4219de6b00c882caac64c4c1a35e28bb765f4c27783b`
- `private_sources/verification_repair_v2/software_adversary/FINAL_ZERO_BLOCKER_RECEIPT.json` — `a55c1c7650f168950e9cc7ffbfa9d205ea4c3f8b30e605bcb007a584b6132054`
- `private_sources/verification_repair_v2/software_adversary/FINAL_NORMAL_NATIVE.json` — `9ad90556edac4e4ce9d87df4e0ccab5e82c16c2361d6a912a1856d6a31cc07b9`
- `private_sources/verification_repair_v2/software_adversary/FINAL_OPTIMIZED_NATIVE.json` — `1e2737bdbe79c14803db15291003379ae7e8df232e21ba7577ba25acb929b269`
- `private_sources/verification_repair_v2/software_adversary/FINAL_METADATA_INSPECTION.json` — `269f32e2b469e3fa2df1e8b573a28d9f4826461096e2e715a6ecfcfe943a3e0e`
- `private_sources/verification_repair_v2/software_adversary/FINAL_AUTHENTICATED_CUSTODY.json` — `dbffe95d1dd1b520c5e07f93a205724c146818753eeadeb40e5eb0963a8ae311`

Fresh native final scope gate: 2026-10-13T02:29:13.469707+00:00; PR411 open/draft/unmerged, head/ref `ac8b960bdda61c154cc30d7e3aba70389a9b139e`, branch `research/ricci-pinching-6800014`, exact QUEUE blob `81f397cb34eeb6ce1d3c828992abc0969ab2d74d`, header-derived `claimed_solved`, author turns **2/5**. Zero new author proof-search turns. No source snapshot, Git/index/branch/checkouts/commit/push, live PR/QUEUE, Zenodo/Sheet, external outreach or other-chat message was changed by this component.
