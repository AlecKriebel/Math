# PR38 final frozen replay/builder static adversary

Disposition: **BLOCKED_STATIC_REVISION_REQUIRED**, for the exact frozen sources below. No actual replay, helper import, research program execution, scientific verification, Git operation or external communication was performed. Source AST parsing was syntax inspection only. Root must create reviewed revisions rather than edit a closed source family.

## Exact review basis

- Replay preparation manifest SHA256: `460e735cdecf14e1577959c57bb9cf5afa4b81818565474abfd5a2b28103a2f8`; all seven listed source/doc/input members and exact recursive self-excluding closure matched by direct bytes.
- Collector484 SHA256: `02848c52bbdda64c0656235e2b48d4523e589306d7b21a7712f8b29097ba09ae`.
- Capture125 SHA256: `30dff4700e4c9158a9303860d067801fe261fed8b2acbb7eaa11a472c3c807dc`.
- Inspector147 SHA256: `7ccd54b7af914f717a34bcc18469ba69bae5d1cfa8acd2045110254a9b2619ea`.
- Reconstructed-controls239 SHA256: `13a181a162a1422e5e6df843f98d502db6bb275831f79a9782fd0c26ae472da6`.
- Builder521 SHA256: `dbb81b2573c1ed59845c2a46d11572b86862c5b4cc1eff926ba86fa84bd14bdd`; static closure SHA256: `0aa63f40183ab89166b37d807ce6b38e1e62a5de481fc0aa3d367e8d184d3638`; all four listed members and recursive closure matched.
- Original snapshot SHA256: `2c58f3aa5f73920fa62c7103648deee899db3a12f3f48c940576f99eff74dfe2`. All16 saved bytes/size/SHA256/computed Git-blob SHA1 matched; changed-path array has17 members. No live Git provenance was independently run.
- Root scientific scope certificate SHA256 remains `4e042ef2328c73cf871627ccf15c3ffe98366019c67c34951a7d9a221e1a47fa`, separately read as the root's scientific prerequisite, not an actual-run or independent-primary-reading claim by this reviewer.

Every listed Python source and both README/ROOT_GUARD_CONTRACT texts were read in full. Supporting unchanged current-measure/primary runners and the native importer/pure score definition were read directly.

## S1 — Guaranteed legitimate stdin evidence rejected by builder

The unchanged `current_measure_family/replay_and_controls.py:18–24` loops over all16 original inputs and at line21 invokes `subprocess.check_output(['git','hash-object','--stdin'], input=data, cwd=ROOT)`. Python's check_output routes through the instrumented subprocess.run. `capture_runner.py:85–90` preserves each supplied input as `%03d.stdin` and puts a path/size/SHA row in `nested_runs.json`. The collector's complete recursive support manifest at `collect_root_replays.py:473–478` includes these files.

The CLOSED builder rejects every such member at `prepare_current_packet.py:261`: its explicitly permitted suffixes omit `.stdin`. Therefore a successful legitimate collector cannot pass the current builder. This is a deduction from the unchanged source transport, not a claim that a replay was executed.

Required resolution: a reviewed builder revision must explicitly permit the first-party stdin evidence and independently bind each nested `stdin` row through the same retained path/size/SHA check used for actual streams. Keep full input bytes and existing complete support coverage. Do not exclude or delete stdin to make the build pass. Update the contract/capability text and actual revised-builder pin.

## S2 — Timeout and process-launch failures lose actual execution evidence

At `collect_root_replays.py:204–218`, outer subprocess.run uses `timeout=600`. Run row and complete stream files are written only after subprocess.run returns. A TimeoutExpired or OSError goes directly to the generic handler at419–421: its traceback is kept but its partial stdout/stderr, attempted run row and exact launch failure are not materialized. `finally` deletes the private tree at471. Earlier setup lines142–148 also occur outside the protected try at248, so private/support setup errors lack a final failure receipt.

At `capture_runner.py:73–80`, only CalledProcessError and TimeoutExpired are handled. A nested FileNotFoundError/PermissionError/OSError occurs before the row at81–107, so no nested attempted argv/source/streams/failure row is saved. The wrapper's final outer-generated delta may preserve surrounding inputs, but does not replace the missing attempted-run evidence. The collector's normal real Python3.14 missing-SymPy exit1 path is retained correctly; that does not cover a process-launch failure.

Required resolution: a separately reviewed collector/capture revision must capture source and intended argv/cwd before launching, materialize partial timeout streams and explicit launch failure rows, and protect setup/finalization sufficiently that a failed attempt keeps its available evidence and original failure. Cleanup must follow successful evidence retention; if retention itself fails, preserve the private attempt and report that failure. This finding is a concrete unhandled path, not an observed failed actual run.

## Scope and mechanisms that remain sound on static inspection

The source explicitly distinguishes frozen actual inputs, modern replay transport and unavailable historic snippets. It pins original16/17 and 52+63+54=169 members plus the original three manifests, recursively rejects symlinks and nested unlisted extras, and excludes only exact root self manifests plus authorized top-level caches. It preserves both actual old primary-validator nested-extra PASS mechanisms and strict-root rejection. No closed family is modified.

The inspector reconstructs every15458 importer row from complete149266659-byte raw inputs, checks6701 reports and read-only immutable/query_only SQL, calls only the native pure score function, preserves the complete source object, and distinguishes absent raw report, original literal null, and importer empty fallback. Original accounting stays2/5 with new0/audit0 and current native omission/queued0 explicit. No unseen worker transcript is manufactured.

Both original programs' complete JSON stdout is compared in bytes and objects against author30/reviewer72 receipts and materialized by the collector with accurate labeling. Code/prose controls and genuine default dependency failure have separate semantics. Whole JSON comparisons preserve exact residual qualifications; only the five named clocks and one explicit private prefix are normalized. There is no discovered broad projection or runtime/native wipe.

The builder keeps original16 archive/code/math/source/whole receipts/two turns exact, uses an audit-root dependency anchor, strict recursive evidence/current closure, `.gitignore` capability, local named12-column queue proposal, raced-destination-safe macOS exclusive rename and pending new whole-current source-first gate. The current scientific wording preserves closed genus>=2 reductions, the separately scoped finite-area Radon S_0,3 observation, extended noncompact pairing, pi^2 normalization, finite periodic-orbit support meaning and the unsolved arbitrary-reference/literal complete-only gaps. No full result, extreme-point classification, new DOI or old-PASS transfer is claimed.

These positive observations do not establish actual runtime success, exhaustive importer security against an arbitrary new module, mathematical novelty, or completion of the fresh whole-current gate. This review adds zero proof attempts and leaves the root's15% mathematical partial-progress heuristic unchanged. Static review is100% complete for these frozen pins; operational readiness remains blocked until independently reviewed revisions and actual retained replay evidence resolve S1/S2.
