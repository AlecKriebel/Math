# PR 883 independent artifact and executable-claims audit

Audit date: 2026-10-15. Problem 9900008 / AMR-098-0008. This audit concerns only the frozen, eligible PR 883 head `af25d26e21945a1a132aace5e600485152777070`.

**The original fixed artifact authenticates and its included executions reproduce.** The imported mathematical acceptances are byte-bound historical evidence, not this auditor's mathematical or priority verdict. Several narrow parser/filesystem boundaries in the old checkers are reproducible. They are repairable in a new current publication wrapper and do not constitute counterexamples to the mathematical proof.

## Scope and independence

I read the complete `author/verify.py` and `check_publication.py` before executing either. I then read the proof, source audit, both old audit reports, both acceptance objects, distribution/readme/credit notices, manifests and public verification metadata. The archive code was authenticated as exactly the already-read `author/verify.py`; no additional code body or nested executable archive is present in either included ZIP. I did not use old mathematical verdicts as authority or claim a new independent source-first mathematical reconstruction. Separate agents are assigned those tasks.

No other PR was inspected. Links to related PR 284 occur in the frozen documents; their target contents were not accessed. No candidate file, shared index, branch, corpus, source PDF or foreign work was edited. No Git, Zenodo or Sheets mutation or external communication was performed. The original author count remains 1/5; artifact replay is not an additional central proof-search attempt.

## Exact provenance independently checked

`PROVENANCE_RESULTS.json` records the full safe pin ledger.

1. The supplied external `SOURCE_MANIFEST.json` SHA-256 was independently checked against `53bba0a85fa099146f7bb6d7520bc8a3a423894b702a9e8e4cb9f63ded3a48ab`. All **26 regular files, 211,771 bytes**, match their size/SHA-256 and Git blob pins. Every complete file was also read from the actual immutable head by `git cat-file blob HEAD:path` and compared byte-for-byte. The source has exactly the four expected directories `archives`, `author`, `review1`, `review2`, no symlink or special file. This check relies on the expected head and external manifest supplied to this audit; it is not a new remote eligibility or current-head check.
2. The outer publication manifest has exactly 25 distinct payload rows and covers all source files except itself. Every row matches the externally authenticated bytes.
3. The author ZIP is 18,611 bytes, SHA-256 `bd2a43c1d0de12ea87ba217b3b5316a00e008d1b547992d7bdd038ff695aed9b`, with eight members. The fresh-review ZIP is 15,301 bytes, SHA-256 `ac46400397200608b0b608908a29f8b3917347e32b0a77f5a14496c10cc197cc`, with seven members. Both have unique flat names, closed membership matching their corresponding directories, exact member bytes, valid CRCs, no encryption, symlink, directory or other special member, consistent local/central names and sizes, and no preamble, payload gaps/overlaps or trailing bytes. The local records directly adjoin the central directory, which directly adjoins the final EOCD. No untrusted ZIP extraction was used. The inner manifests bind seven author payloads and six fresh-review payloads, excluding themselves.
4. The three **whole** corpus sizes and SHA-256 values were recomputed by streaming, then strict JSON parsed locally. They match the frozen metadata: catalog 21,735,099 bytes, problems 68,931,837 bytes, reports 80,334,822 bytes. This is whole-file byte authentication, not merely authentication of a selected record. No corpus was copied or redistributed. Only the exact target was substantively selected. The complete target record/report array serialized with default sorted-key JSON is **5,255 bytes**, SHA-256 `5ccf640125437cbff98966972b50bc5f73f19e1ae1735dff8a49829cfbcdc42a`; the actual catalog review hash matches. The actual catalog statement hash matches the complete target statement, SHA-256 `85140471a18e2a6974b1e984ead6f94e6954f1d619201d414dc8be50244c8c54`.
5. All five primary PDFs retrieved by the parent were independently byte-hashed and magic-checked, matching the original source metadata. This verifies the local retrieved bytes and their equality to the frozen pins; it does not claim that this artifact auditor downloaded or mathematically read the papers, that their final publisher editions are identical, or that access-limited editions were recovered. No PDF/text/body is in these public outputs.

The source remained unchanged through the final provenance recheck. Git object contents, immutable source hashes and the expected commit are the external trust layer. An internal list or a checker that is itself replaceable is not an external authenticity guarantee.

## Complete active code assessment

The two active programs use only the standard library. Both use explicit `need` guards rather than Python assertions, so their intended guards survive optimization. Neither sends network requests, reads credentials, runs a shell, or modifies the original inputs in normal replay. The author checker computes exact fractions, the reduced finite target-label algebra, rational window and translation diagnostics, then optional certificate mutation/positive controls. Its integrity path reads the author manifest. Its own header and result explicitly leave universal covariance/measurability claims to `PROOF.md`.

The publication checker reads the manifest, compares archive and directory bytes, checks the fresh acceptance's exact bindings and credit-copy equality, and invokes the included author checker under four modes. Its self-test copies its root into temporary directories and changes five inputs. Those mutations were allowed only in private copies. Its imported acceptance check establishes byte binding and the presence of old labels; it cannot establish that a mathematical verdict is true.

The historical first-audit executable ZIP is not included. The frozen README and input metadata explicitly disclose that omission and say it cannot be replayed. This audit does not recover it, claim its 10,028 independent controls or 48 tamper executions were newly reenacted, or treat its external-manifest hashes as locally verified contents. Two unchanged historical report files are present; their reported counts remain historical testimony. The current included author checks are independently replayable.

## Reproduction results

All executions used the actual `/opt/homebrew/bin/python3`, version 3.14.6, with bytecode writing disabled at the top level. The bare `python` command is a macOS developer-tool stub here and returned an Xcode-license message before executing any audit code; it was not used further. That environment event is not a candidate failure.

`BASELINE_REPLAYS.json` retains complete stdout/stderr and output hashes for **20 direct runs** from a private directory whose name contains spaces:

- Author plain, `--self-test`, `--integrity` in ordinary, `-O`, `-I`, and `-I -O`: 12 direct runs.
- Publication default and `--self-test` in those same four modes: eight direct runs, which themselves perform **64 included author child replays**.

Every run exited zero, emitted no stderr and reported pass. The author outputs reproduce nine quotient cases, 530 exact rational window samples and 361 exact translation-pair samples. Every self-test rejects all 18 declared malformed certificates and accepts its two additional unequal-weight variants. Every publication self-test rejects its five declared file mutations. None of these finite checks is a proof of the uncountable allocation class or a priority determination.

`HISTORICAL_CONSISTENCY.json` separately verifies all 16 stored author mathematical output objects, all eight fresh-review checker output hashes, the exact detailed `checker_rerun.json`, all four stored publication self-test output hashes and result objects, and six fresh-acceptance byte bindings. Those comparisons genuinely reproduce the included output data; they are not new runs of the absent first-audit program.

## New adversarial probes and precise boundaries

`adversarial_controls.py` imports only the two already-read code bodies from the private baseline. `ADVERSARIAL_NORMAL.json` and `ADVERSARIAL_OPTIMIZED.json` each retain **32 probes: three baseline positives, 20 correctly rejected negatives, and nine deliberately accepted boundary probes**. Both suites pass their declared expectations. The 20 rejection cases include same-length/appended proof corruption; altered credit, acceptance, either archive, checker or verifier; missing certificate; root/nested extra files; leaf symlink rejection by the whole publication layer; and incorrect certificate identity/type/scope/arithmetic premises.

The following accepted probes deserve precise documentation:

- The whole publication checker ignores an extra empty directory and a symlink to an extra empty directory. The frozen baseline has neither, and the immutable externally pinned tree check detects both. A current wrapper should enforce a closed directory set as well as a closed file set and reject every symlink/special entry before reading.
- Author-only `--integrity` follows a same-byte symlink payload and ignores a file inside an extra nested directory. The whole publication layer rejects those examples. The author integrity command should remain described as its limited historical layer, not as a robust standalone closed-tree authenticator.
- The JSON loaders use standard `json.loads`, which silently accepts duplicate keys with the final value. A duplicate `schema` key in the unpinned outer manifest is accepted by the publication integrity function. A duplicate certificate `dimension` key with a valid final value is accepted by the actual author CLI. These inputs do not change the final parsed mathematical certificate, but duplicate-key rejection is appropriate for a current reviewable format.
- `expected_preserving_target_labels` is compared by Python equality without an exact integer-type guard. `[[False, True]]` and `[[0.0, 1.0]]` both compare equal to the expected `[[0, 1]]` and pass. These observational label fields do not control the independently recomputed reduced mass equation, so this is a parser/schema issue rather than a false arithmetic theorem. A current certificate schema should require exact integers and exclude booleans/floats.
- Coordinately editing the root README and its editable manifest row passes the internal layer. That is the documented trust boundary, not a hidden mathematical fault: the README itself already says an editable manifest is not an external authenticity anchor. It is rejected by the frozen external source/Git layer. The startup checker and index hash must be authenticated separately before running candidate code.

General code inspection also shows the old reader is not a bounded hostile-filesystem parser: it uses ordinary unbounded `read_bytes` and lacks a race-resistant sandbox. This audit deliberately used authenticated small regular files and private copies. Do not reframe the old tool or this audit as a hostile-code sandbox, a defense against rewriting all trust anchors, or a guarantee under hostile concurrent filesystem mutation. These are deployment assumptions and hardening tasks, not evidence that the fixed baseline is corrupt.

## Current publication recommendations and exact remaining gap

Preserve the original 26 files and two historical ZIPs as immutable historical evidence. For the new preprint package, a separate current wrapper should authenticate an externally supplied startup/index pin, parse JSON strictly with exact schemas/types and finite values, walk a closed regular-file/directory tree without following links, bound file/ZIP reads, and authenticate every archived code body before calling it. Clearly label the old executables as historical supplementary checks. Carry the source-credit addendum, universal proof/finite-diagnostic distinction, AI-assisted/unrefereed disclosures and the boundaries excluding background-randomized, all-Markov, free-action, positive-density and one-dimensional claims.

This audit's strongest verified result is **exact original artifact provenance and reproducibility of all included execution claims**, together with independently demonstrated limitations of the old checking layers. There is no newly observed corrupted original file or failed baseline replay. The exact remaining work is outside this delegated audit: complete the independent mathematical/source gate, perform bounded deep priority review if it passes, prepare the actual preprint and current verification wrapper, and adversarially review the final complete package. This is not final preprint approval, novelty clearance, or authorization to publish before those steps.

## Audit reproduction and public boundary

The two included audit scripts are code artifacts for this specific repository audit. `audit_artifacts.py provenance` requires the frozen source and supplied manifest, the matching immutable Git objects, the three original local corpora and five already retrieved local PDFs. `replays` creates a fresh private baseline and intentionally refuses to overwrite an existing one. `consistency` consumes the saved baseline replay results. `adversarial_controls.py` requires that private baseline; normal and `-O` invocations create and clean their own private temporary fixtures. They are not asserted to be a standalone portable verification package without the declared external inputs. The safe public manifest excludes all private copies, corpus bodies, PDFs and source text. No optional external dependency or omitted historical control is silently represented as a default portable check.


## Parent publication-metadata amendment — 2026-10-15T12:55:06.957125+00:00

Only the two legacy command/error paths listed in PUBLIC_PATH_AMENDMENT.json were normalized for the current public package. Exact original receipts and the prior public-artifact snapshot are preserved privately, with byte counts and hashes recorded. Original subprocess stdout/hash observations, code pins, timestamps, finite decisions and the bounded verdict are unchanged. This is a parent-authored presentation amendment, not a rerun or a new mathematical/whole-package approval. The separate original r1 package and its ISSUES review remain immutable. Amendment completion:100%.
