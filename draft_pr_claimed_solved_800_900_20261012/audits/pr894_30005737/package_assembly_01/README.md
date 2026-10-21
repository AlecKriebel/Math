# PR894 candidate assembly: engineering handoff

`assemble.py` is a standard-library Python >=3.11 two-stage assembler. **It has not been executed; no candidate is created by this handoff.** Neither stage launches subprocesses. The parent reads/authenticates this source and templates, supplies final pinned inputs, captures a genuine full-replay reviewed-tool build, and runs the new integrated whole-publication loop. The earlier independent format PASS is unchanged; this builder is new engineering work.

Only this folder was edited. Reviewed tooling, source/audit envelopes and parent preprint are inputs. No PDF authoring, Git/remote/release action or external communication occurs.

## Explicit input plan

The parent `ASSEMBLY_INPUTS.json` is ready: 4,761 bytes, SHA256 `e29c52293cbba8451e620460a7cf83be2b438694d0ab64b1598161301f3083ea`. Independently confirm that pin. Its exact schema is:

```json
{"schema":"pr894-parent-assembly-inputs-v1","paper":[],"root_receipts":[]}
```

The empty arrays above describe the shape only and are rejected as inputs. Paper rows are exactly `{path, bytes, sha256}`, selecting four authoritative files directly from parent `preprint`: `note.tex`, `metadata.json`, `zenodo-deposit.json`, `post-lie-note.pdf`. The parent-frozen TeX is 15,348 bytes / `07e4dc2b7af5acd42ecd2c59863a67bc1ed722dcf038b8c656683c9c01ed5315`; the four-page PDF is 93,764 bytes / `849aaf7d065061f0fb69e7f3c507d1c5c70301ededa142a61af11cbaddbef74d`. The assembler does not edit them.

Receipt rows are exactly `{source, path, bytes, sha256}`. Destination `path` is a basename under `root_evidence`. Source is the same parent-root filename, except editorial/PDF receipts may explicitly select `preprint/FILENAME`. The parent plan selects all 19 current approved receipts. The required 18 names are enumerated in `REQUIRED_RECEIPTS`: source/native/scope/primary/root-replay/math/artifact/priority/tool-format readbacks, current editorial disposition, and all four sanitized editor/PDF build/render/visual receipts. It also selects `ROOT_CLASSICAL_TOPOLOGY_SOURCE_NOTE.json`; `.md` is the alternative allowed spelling. No future or unlisted approval is guessed or globbed. Receipt contents are copied intact after pin/privacy checks; the parent supplies and reads their approval semantics.

Eight full safe-manifest SHA256/size/row-count pins are hardcoded in `ENVELOPES`. All listed bytes authenticate before copying. Each complete safe payload and its original manifest/schema goes under `verification/audits/FOLDER`. The optional six-file author envelope is selected with its independently supplied manifest pin `4ad42042840cc86a908e51f3f99f99a67f9427bb14e955495c69a83218bd766d`; actual input folder is `note_author_01`, and output is `verification/history/note_author_01`. It is a dated drafting snapshot, distinct from authoritative preprint inputs.

The original 18 files go byte-for-byte under `verification/source`, and their immutable manifest under `root_evidence`. Current reviewed tool/dependencies, real TeX/metadata/deposit and README/history templates complete the verification root. No private/unlisted captures, raw native/primary bodies, wheels/runtimes or rendered pages are copied. Already accepted safe envelopes retain their curated public stdout excerpts and original code completely. The full historical 20-file engineering envelope includes explicit NOT ACTUAL PAPER fixtures and excludes its private 18-source fixture copy; both templates qualify this history and scripts' missing private prerequisites.

## Parent execution sequence

Use the parent's capture helper for all actual processes. Variables are parent-supplied paths/pins. These commands have not been run by this handoff:

```sh
python3 -I -S -B "$A894_ROOT/package_assembly_01/assemble.py" prepare \
  --preprint-dir "$A894_ROOT/preprint" \
  --inputs "$A894_ROOT/ASSEMBLY_INPUTS.json" \
  --inputs-sha256 e29c52293cbba8451e620460a7cf83be2b438694d0ab64b1598161301f3083ea \
  --noteauthor-manifest-sha256 4ad42042840cc86a908e51f3f99f99a67f9427bb14e955495c69a83218bd766d
```

Preparation writes fresh `candidate/` and `private_tmp/prepared-state.json` here. It creates neither verification ZIP nor outer manifest. Independently read back/check the printed startup, package-index and prepared-state pins. The README/history templates contain no cyclic package/current index pin.

Create ordinary nonsymlink **parents** for fresh build/replay/capture outputs outside `candidate` and all original preprint/source/audit input trees. Suitable parents are `package_assembly_01/build-output` and `package_assembly_01/private_tmp`; the ZIP/replay directory themselves must not exist. Default diagnostics need no native/primary input flags. Capture this mandatory actual build:

```sh
python3 -I -S -B "$A894_ROOT/package_assembly_01/candidate/verification/portable.py" build \
  "$PACKAGE_INDEX_SHA256" "$FRESH_BUILD_DIRECTORY/post-lie-verification.zip" \
  --root "$A894_ROOT/package_assembly_01/candidate/verification" \
  --receipt-dir "$FRESH_REPLAY_DIRECTORY"
```

Build always performs the genuine one-wrapper/eight-child replay; unchanged root execution is inside that wrapper. Preserve actual stdout/stderr/process metadata before outcome checks. Finalizer requires the original capture JSON to contain at least `started_utc`, `ended_utc`, integer `pid`, integer `returncode`, `stdout` and `stderr` objects `{bytes,sha256}`; optional `timeout` must be false. Additional capture fields may remain. These fields must derive from the actual process, never synthetic expected output. All raw capture/replay files remain outside the candidate.

```sh
python3 -I -S -B "$A894_ROOT/package_assembly_01/assemble.py" finalize \
  --prepared-state-sha256 "$PREPARED_STATE_SHA256" \
  --zip "$FRESH_BUILD_DIRECTORY/post-lie-verification.zip" \
  --build-stdout "$ACTUAL_BUILD_STDOUT" --build-stderr "$ACTUAL_BUILD_STDERR" \
  --build-process "$ACTUAL_BUILD_PROCESS_JSON" \
  --replay-receipts "$FRESH_REPLAY_DIRECTORY"
```

Finalization reauthenticates the entire closed prepared tree/state; binds actual build stdout/capture to the exact ZIP; validates wrapper and eight child raw receipts, flags and execution markers; checks unchanged frozen source; and independently rebuilds the ZIP with the same stdlib runtime. It copies the exact build ZIP, adds a sanitized outer build binding, and generates `CURRENT_PUBLICATION_MANIFEST.json` **last**. Prepared indexed files and final outputs are never overwritten.

The final closed regular tree has real outer TeX/metadata/deposit/PDF, current tool, README/history, exact current-layout JSON, complete verification tree, exact verification ZIP, sanitized build binding and outer manifest. Names are ASCII relative paths; inventories use exact reviewed schemas and sorted rows. The paper PDF stays separate from the ZIP. Package/current indexes exclude themselves.

Independently authenticate final pins, then run actual `current` in normal and optimized modes with fresh outside receipts and the new whole-publication/adversarial/editorial loop. Final assembly status explicitly leaves that work to the parent. It does not approve release or add mathematical/priority conclusions.

## Limits and preserved incidents

Failures remain inspectable; the script does not delete or recover failed stages. Only the parent decides how to dispose of its own partial assembly. The selected runtime/OS remain trusted; no OS sandbox or general TOCTOU guarantee is supplied. ZIP byte equality requires the same input/Python ZIP/zlib runtime.

New-file creation repeatedly failed with ENOSPC during documentation authoring. A temporary rename of this effort's own log was reversed after the parent freed its own completed duplicate scratch. No foreign/active files or accepted inputs were changed. The log records this. Only static source/structure checks run here; neither assembly stage nor a new tool build ran.
