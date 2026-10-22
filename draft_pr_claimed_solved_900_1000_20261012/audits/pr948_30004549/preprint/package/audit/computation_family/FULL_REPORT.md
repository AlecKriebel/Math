# PR948 computational and packaging audit

Target: PR948/problem30004549 at immutable head `be4313efafa1af5962394e07d8a4debff2e94d92`. This family adds **zero author turns**. Audit completion: **100% of this family's assigned finite computation/package scope**.

The authenticated historical regular-file package reproduces exactly. No computational contradiction to the candidate's local algebra was found. This conclusion is narrower than a global geometric proof or a claim about novelty. Seven profile findings below identify requirements for any new strict publication entry point; none changes the original proof or frozen scripts.

## Authentication and actual order

1. Read ELIGIBILITY_GATE.json, ORIGINAL_SNAPSHOT.json, and ORIGINAL_FILE_RECORDS.json before source/math intake. Matched target, claimed_solved/open/draft fields and immutable head. The controller gate itself was supplied by the parent; its basename receipt was absent directly under A. Parent later clarified the receipt's effort-root location. At2026-10-16T07:02:11.295826+00:00 this family authenticated receipt SHA256 `949cc2aeb77576625bb2f5cbf3b0f799cb09aef02368f8b75d66fe22191b8ba4` against the correction record and crosschecked stable before/after metadata, head, problem, claimed_solved4/5, queue-row binding, and recorded pre-intake/no-mutation flags. This is a late consistency audit of the supplied receipt; this family did not replay the live controller operation or native author history.
2. Bound all24 originals to immutable Git tree mode100644/blob IDs, then compared Git blob bytes, disk regular-file status, disk0644 mode, byte count, and SHA256 against both supplied inventories. Read-only Git calls use process-only gc.auto=0. No checkout, branch, index, shared configuration, fetch, installation, commit, or push was performed.
3. The first source-pin check failed because the assignment called the nested statement hash the full-record file hash. Failed receipt is preserved. Parent corrected this metadata. Authenticated full4190-byte private record SHA256 `5df3868e802d9da72bced3f4606c3ccd9b6610208bcc2a086bf25e082239b34f`; nested UTF-8 statement SHA256 `a5ce90b9c2087f20cd09cb33d9d92ca40039c19a08de3b1c098d10bf75b9179b`; review_hash `b667ba93b244f20bf9dd6b244af355c1b933340bb194c5a18a0d7c27d5ed9bb4`; prior_research empty. The full private record was read and is **excluded from public artifacts**.
4. Read charter, complete candidate proof, all three checker sources, and complete wrapper before executing old code. A combined read truncated checker A/B; both were reread completely before execution.
5. Independently reconstructed the algebra and wrote the bit-mask/matrix checker before reading old audit verdicts or running old checkers. Afterwards read README/credit/expected outputs. Old audit verdict prose was not needed for the conclusion.
6. Authenticated the separately supplied PUBLIC_MANIFEST and wrapper SHA256 pins before old execution. Performed all target mutations in private owned copies. Final reauthentication at **2026-10-16T06:59:31.428747+00:00** confirms all24 originals still match immutable Git and source bindings remain intact.

## Independent mechanism and checkable mathematics

The independent checker represents exterior forms by four-bit masks, rather than importing any preserved checker. With real coordinates `u,v,x,t`, it uses `alpha=du^dx-dv^dt`, `beta=du^dt+dv^dx`, and arbitrary smooth symbolic `R`. It differentiates the exact perturbations, retaining every cutoff derivative. It obtains:

- `d beta_e=0`, `d gamma_e=0`, `d(R v dv)=v d(R dv)`, and `gamma_e=u alpha-v beta_e`.
- In orientation `du^dv^dx^dt`, `alpha^2=2vol`, `alpha beta_e=R_t vol`, and `beta_e^2=2(1-R_x)vol`.
- With `eta=beta_e-(R_t/2)alpha` and `D=1-R_x-R_t^2/4`, the Gram matrix gives `alpha eta=0` and `eta^2=2D vol`. The stated box `|R_x|<=1/4, |R_t|<=1` gives `D>=1/2`.
- Independently recovers the full-cutoff matrix `J=-A^-1 B` from the alternating matrices for alpha and normalized eta. Symbolically checks `J^2=-Id`, anti-invariance of both forms, decomposability, and the conjugate product, using `q^2=D`.
- On the constant-cutoff core, independently differentiates the matrix/coframe and obtains both Nijenhuis and Frobenius coefficients `-epsilon/(2(1-epsilon*x))`, with nonzero value `-epsilon/2` at the origin.

All21 checks pass with identical output bytes in normal, optimized, and isolated modes. The independent checker uses explicit exceptions. Deliberately wrong mixed-wedge signs, gamma-perturbation signs, and omitted cutoff derivatives are detected. This is finite symbolic evidence; compactification, class independence, global gluing, smoothness, and source scope require the separate mathematical families.

## Reproduction and package evidence

Environment actually tested: CPython3.14.6 and SymPy1.14.0, using the supplied existing environment; no install. This does not establish the full README Python3.10+ portability range.

The seven ZIP members exactly match author/ mirrors and the external manifest. Archive SHA256 is `1ba558617ecbd40e4117da22897137118568204852b009bb2c02c99ef2521fc4`. The proof is9997 bytes with SHA256 `50a267656e6a5412a2e14208ada5aec203df4c5385be63b831029188cb1cf39e`.

The frozen wrapper passes `--self-test --run-checkers` under normal, optimized, and isolated Python. Each run returns17 self-tests,9 checker replays, files24, and archive_members7. All three3091-byte outputs are byte-identical to the historical VERIFICATION_RESULTS.json, SHA256 `ddf1aeb2d60ddc798cd16c2637e6f38057f1ca287e3a5d3ef1c15f297a413e57`. The author checker602-byte JSON and audit A249-byte/audit B178-byte outputs also reproduce exactly in all9 direct mode runs. Canonical scalar/list/string types and integer file/member counts were explicitly checked.

The main harness records55 events, with a further8 supplemental events. Wrapper built-in negatives and additional probes reject altered proof/data, wrong size/hash/Git blob, missing/extra members, duplicate members/manifest paths, symlinks, absolute/parent/backslash/dot/repeated-separator/empty paths, incorrect identity/turn count, malformed envelopes, and deliberately wrong mathematics as described below. Malformed JSON with matching sidecar was separately tested; the first malformed-JSON probe had stopped earlier at sidecar validation.

## Stable findings and publication interpretation

| ID | Verified behavior | Historical interpretation | Requirement for a new strict entry point |
|---|---|---|---|
| R948-COMP-01 | Direct audit A/B `-O` accepts deliberately false assertions; normal and forced optimize0 reject. | README discloses this. Old wrapper compiles with optimize0 and its guard passes. | Keep force-enabled assertions and the direct-execution caveat. |
| R948-COMP-02 | Unlisted FIFO passes; listed FIFO blocks until a bounded2s child timeout. | Original24 are independently authenticated regular0644 files. Old inventory is not a complete filesystem-object profile. | Before reads, require bounded regular files, no links/FIFOs, and closed object inventory. |
| R948-COMP-03 | Ambient PYTHONPATH poison is imported by normal children, even with outer wrapper `-I`. A direct isolated child ignores it. | Clean-environment historical replay succeeds. No sandbox was claimed. | Sanitize environment and use cold isolated children; force optimize0. |
| R948-COMP-04 | chmod0755 and ignored declared git_mode120000 are accepted. | Git/disk modes of actual originals were separately verified. | Enforce coherent expected modes or strictly limit byte-integrity claims. |
| R948-COMP-05 | Integral float byte size and float problem ID are accepted; several malformed shapes reject through generic exceptions. | Actual manifest types are correct. | Require exact types excluding bool/float, explicit schema, and coherent metadata. |
| R948-COMP-06 | ZIP helper ignores symlink external attributes; no decompression cap. A bounded256KiB fixture passes. | No extraction occurs; full original archive is externally frozen. No bomb was executed. | Bound archives/members and enforce safe modes/names without extraction. |
| R948-COMP-07 | Coherent README/manifest/sidecar rebind passes internal checks and changes the external manifest hash. | README correctly requires independent Git/manifest authentication. This audit checked it. | Retain an independent immutable trust anchor. Sidecars are not signatures. |

A new strict portable entry point can address COMP02–06 while preserving the frozen historical artifacts. Its implementation and tests are outside this family and require a fresh audit. The old driver must not be relabeled as repaired. No operating-system sandbox or formal-proof guarantee follows from either finite-file checking or Python isolation.

## Preserved failures and operational limits

The initial hash-label mismatch is retained in AUTHENTICATION_FAILURE_INITIAL.json; corrected-input and final successful receipts are separate. HARNESS_INITIAL_FAILURE.json records this audit's wrong runtime-parent path before target execution. HARNESS_IMPORT_CACHE_FAILURE.json records the subsequent private-clone inventory failure after importing the verifier with cache writes enabled. Disabling bytecode writes in the harness and starting from a fresh clone yielded the successful full run; originals were untouched. These are audit setup failures, not target mathematical defects.

Python isolated mode ignores Python environment variables, so PYTHONDONTWRITEBYTECODE alone is insufficient for cold isolated children; explicit `-B` is preferable. A read-only observation found454 SymPy cache files timestamped06:57:16–17 UTC, after this family's successful harness ended06:56:52. Their creator is not attributed; no shared cache was deleted. Curated evidence excludes runtime caches and all scratch fixtures.

## Strongest verified conclusion and remaining gap

The exact historical package's integrity and finite algebra reproduce; the independent local calculations agree, including nonintegrability. No author repair, new construction, priority search, novelty claim, controller-state change, or external communication occurred.

Remaining work belongs to separate scopes: global geometric proof verification, primary-source scope and priority, native author-history provenance, a fresh audit of any new strict publication entry point, and broader runtime portability testing. The old verifier's limits must remain explicit even if a new entry point closes them.

Public distribution is restricted to PUBLIC_ALLOWLIST.json. It excludes tmp, full private source/corpus/primary-source copies, context records, credentials, and any external runtime. MANIFEST.json seals curated payload paths/bytes/SHA256; its checksum is independently reported to the parent. No curated artifact is edited after sealing.
