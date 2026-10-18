# Publication package tooling setup

Role: infrastructure author, not an independent final mathematical or release reviewer.

Completion estimate: 100% of the authored tooling implementation; final release readiness remains the root's separate review task.

## Owned files

- `publication/build_package.py`
- `publication/verification/package_common.py`
- `publication/verification/verify_all.py`
- `publication/verification/self_test.py`
- `publication/verification/CONTROL_PLAN.json`
- `publication/verification/EXPECTED_FINITE_SIGNS.stdout.json`
- `publication/verification/PROVENANCE.json`
- `publication/verification/README.md`

The root owns final TeX/PDF/README/license/metadata/deposit, `ROOT_PDF_QA.json`, the authored-member freeze and release decisions. No publication output archives have been built against the actual paper by this author. The only builds were small synthetic fixtures with the real finite diagnostic and explicitly synthetic paper/PDF/metadata inputs. No other audit shard was run, rebuilt or modified. No external communications, Git operations, deposit operations or tracker operations were performed.

## Freeze and replay setup

1. Finish TeX/PDF visual QA. Put the final frozen PDF at `publication/output/pdf/initial-omnific-models.pdf`.
2. Create audit-root `ROOT_PDF_QA.json` with exact `source` and `pdf` pins (`{"bytes": N, "sha256": "64 lowercase hex"}`) for `publication/main.tex` and that PDF, and `pages` as a positive integer. Additional review fields are preserved in the frozen audit file. The builder does not rerender or infer page count.
3. Finish `publication/README.md`, `LICENSE.txt`, `zenodo-metadata.json` and `zenodo-deposit.json`. The latter must be exactly an object with `metadata` and `files`; its metadata object must equal the standalone metadata object, and file paths must be `output/pdf/initial-omnific-models.pdf` then `output/initial-omnific-models-source-and-verification.zip`.
4. Select authored audit members explicitly and freeze them as `publication/verification/AUDIT_MEMBERS.json`, mapping each audit-relative canonical POSIX path to its byte count/SHA-256 pin. Required members are `ROOT_PDF_QA.json` and `verify_finite_signs.py`. Include the current `pr_repair_candidate` edition and proof artifacts as decided by the root; original `inputs` are historical. Exclude all third-party bodies/extracts/renders/raw service responses, private/tmp/cache content, logs, gates and final reviews. Known unsafe paths, body/render extensions, log/gate/final-review names, publication recursion and case collisions are rejected; semantic authorship and third-party content selection still require the root's explicit review.
5. From the audit root, run `python3 -B publication/verification/verify_all.py` and save its complete stdout unchanged to `publication/verification/REPLAY_RECEIPT.json`. Repeat under `python3 -B -O ...` and compare bytes. This authenticates every selected audit member and final PDF/source pins, then performs two full positive stdout comparisons and eight actual mutation process failures. The exact positive baseline has 319 bytes, SHA-256 `293ad3539a8df71d2bc0fe31bb2ae09a0154755424cd148a55c13e10276632c2`.
6. Once QA, metadata, freeze and replay are complete, run `python3 -B publication/build_package.py`. It preflights all three generated destinations before any output writes, validates inputs and the complete replay receipt, builds both archives in memory, then atomically replaces each output and the receipt. Outputs are `publication/output/initial-omnific-models-source-and-verification.zip`, `publication/output/zenodo-upload-kit.zip`, and `publication/PACKAGE_RECEIPT.json`.
7. Extract the source archive under an arbitrary physical directory path, run `python3 -B verification/verify_all.py` (and `-O`), then `python3 -B build_package.py`. Both rebuilt ZIPs must be byte-identical to the originals on the same Python/zlib implementation. The PDF remains a frozen pinned input. Fresh independent final reviewers and all post-freeze gate/operation records stay outside the source archive.

The six final distribution files pinned by `PACKAGE_RECEIPT.json` are TeX, PDF, source ZIP, kit ZIP, standalone metadata and production deposit manifest. The flat kit contains exactly the same PDF and source ZIP, exact metadata bytes, README and portable deposit manifest. Portable versus production deposit metadata are equal; only their payload paths differ. The receipt itself is not recursively archived.

## Scope and security boundaries

The portable runner needs only the standard library and no network. It authenticates every released authored audit file and, in an extracted source archive, every other member via `SOURCE_MANIFEST.json`. Every existing path ancestor from filesystem root is checked, including module paths before import; symlinks and incompatible output/ancestor types fail before generated-file writes. Unsigned manifests provide integrity relative to a trusted external archive checksum, not authenticity against a wholesale rewrite. No concurrent-adversarial-filesystem race defense is claimed.

Private source-body custody checks are explicitly optional and excluded from offline verification; they require independently acquiring the original bodies. The two positive and eight mutation subprocesses are finite diagnostic support only. Legacy family assert programs are historical evidence, not substantive optimized checks. The construction's arbitrary-ordinal, support and proper-class claims remain the written proof's responsibility.

`PROVENANCE.json` marks `a10129f4c09a87460642c36284f300d46d419cab` as the original historical head. It does not claim that this is the current reviewed head. The root can insert the separately verified operative remote head after its update. Original no-correction language is explicitly historical and does not certify the new dependency proof or preprint.

## Validation

The authored small-fixture suite checks ordinary/optimized deterministic builds, exact kit bytes/metadata, arbitrary-root extraction and rebuild, explicit checks under optimization, no bytecode writes even without `-B`, unsafe allowlists, altered authored bytes, a false positive count retaining PASS with an updated baseline pin, a diagnostic with mutation flags suppressed, symlink input/helper/ancestor/output paths, output directories, non-directory output ancestors, and extracted source/PDF-adjacent integrity. Every rejection fixture checks that its complete filesystem snapshot was unchanged after each normal and optimized process. The synthetic PDF does not assess real PDF rendering or page count.

Reports: `self_test_normal.json` and `self_test_optimized.json`. Temporary fixtures live only under `families/package_tooling_01/private` and are removed when each run finishes.
