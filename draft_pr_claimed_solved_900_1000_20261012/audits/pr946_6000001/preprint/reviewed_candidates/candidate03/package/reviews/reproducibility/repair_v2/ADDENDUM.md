# PR946 reproducibility tooling repair v2

This addendum repairs a blocking input-handling defect in the v1 portable tools. The historical manifest SHA-256 is `e535bb4b46e2ebac2d80713b9500eb6748a294fd8ff4d91f748c40f11946b091`; that manifest and all 61 listed payloads remain unchanged. The v1 report and its original failure findings remain historical evidence. Current publication should use these separately authenticated v2 tools.

## Defect and correction

V1 opened executable inputs using O_RDONLY|O_NOFOLLOW before checking the opened object's mode. Opening a FIFO could block indefinitely before fstat rejected it. Its packet scanner also lacked nonblocking opens between directory-entry stat and final object validation. Those are required tooling defects, not mathematical counterexamples.

The v2 gate opens files with O_RDONLY|O_NOFOLLOW|O_NONBLOCK, then requires a regular file using fstat before reading. Original packet reads require the exact known byte size from the unchanged 33-file anchor map. A bounded read obtains at most the expected size plus one byte and rejects changed lengths. Executable inputs use a documented 262,144-byte cap; oversized fstat sizes reject before reading, and growth during a read is bounded to cap plus one and rejected. Directory descriptors and ancestor traversal retain no-follow checks and also use O_NONBLOCK. Worker input authentication uses nonblocking bounded reads, and it executes comparator bytes already authenticated in memory rather than reopening that comparator for execution.

Python opens its script argument before any script code can validate it. Therefore the supported v2 entrypoint is the new, separately externally authenticated **regular launcher**, which authenticates untrusted gate, worker and comparator paths with nonblocking bounded reads before executing any of their code. It materializes trusted copies and executes the authenticated gate bytes. A FIFO supplied as the gate argument is rejected by this launcher. Directly passing an untrusted FIFO as Python's own script argument remains outside the supported entrypoint; no Python script can prevent the interpreter's earlier blocking open. This bootstrap limitation is explicit rather than disguised as a protected direct-script launch.

The gate's original 33 payload byte/hash anchors are identical to v1. The comparator is byte-identical to v1, and the bounded twelve-float criterion is unchanged. Original strict replay failures, the absence of native target turn history, and all mathematical/priority limitations remain as documented in v1. No new proof mechanism, proof turn, native queue transition or live publication operation occurred here.

## Executed checks

- All four positive launcher/gate launches pass. Actual recorded outer optimization levels are **0, 1, 2, 0** for ordinary, O, OO and isolated environment containing PYTHONOPTIMIZE=2. The last environment setting is ignored by -I. Workers and all six original child programs have recorded optimization zero.
- All 15 existing gate negative controls pass, including actual post-copy corruption before worker execution, an intentionally false assertion at actual worker zero, unsafe requested workers 1/2, inventory/special/link errors, changed exact-result types/nonfinite values, and tampered worker/comparator code.
- Fifteen additional nonblocking/cap/marker controls pass under five-second subprocess timeouts, with zero timeouts. These include actual FIFO gate/worker/comparator paths through the launcher, direct-gate FIFO worker/comparator inputs, a listed packet payload replaced by FIFO, and a deterministic regular-entry-stat to FIFO-open race. The forced race rejects the opened nonregular descriptor, rather than blocking. Separate oversized-tool and known-original-size controls reject before payload execution. A controlled post-fstat growing regular file rejects within its bounded read. Three tampered executable payloads containing marker writes are rejected with every marker absent. FIFO input tests also leave all designated markers absent.
- Six executable file-link/ancestor-link controls pass before worker execution. All 32 existing typed comparator negatives pass against the copied, unchanged comparator.
- Final checks reauthenticate all 33 original Git/disk payloads and all 61 historical sealed payloads; both inventories and historical manifest remain unchanged.

The process receipts are in `evidence/PORTABLE_GATE_TESTS.json`, `NONBLOCKING_TESTS.json`, `LINK_TESTS.json` and `FINAL_CHECKPOINT.json`. The source map is `REPAIR_MAP.json`.

## Remaining assumptions

These are finite consistency and input-transport checks, not formal global differential geometry, priority certification, validated floating-point error bounds, or byte-identical numerical replay. There is no OS sandbox. The externally authenticated launcher, trusted local Python/standard library/site packages, kernel, local filesystem and private temporary-directory integrity remain assumptions. No promise is made against a malicious runtime/kernel, blocking filesystem operations outside ordinary local FIFO handling, or unrestricted hostile same-user modification of trusted copied tooling. Bounded opens/read lengths prevent the tested FIFO and regular-file growth defects; they do not make every possible operating-system operation time-bounded.
