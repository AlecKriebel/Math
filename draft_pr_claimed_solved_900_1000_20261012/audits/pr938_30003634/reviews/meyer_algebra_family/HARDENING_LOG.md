# Code-hardening log

2026-10-15T08:38:09.394902+00:00 UTC. Completion of this code-hardening request:100%. Mathematical family completion remains100%; broader topological/source dependencies are unchanged.

The parent root identified optimization-removable checks and implicit result writes in the three new public programs after reading the mathematical report. This was a verification-code defect and has been repaired. No new source/math search or positive proof-search turn was undertaken.

The superseded external `PUBLIC_MAP.json` seal is SHA256 `fdef3b2c42f877192921622330166c2986a513cb90be927bb1b7014b78c1cf31`, **13 entries**. Its bytes and all formerly mapped files were archived privately before edits. This old seal remains a historical external pin; the final new seal supersedes it for reuse. It is not silently replaced in the research history.

Changes:

- Every optimization-removable check in reproduce.py, compare_after.py and authenticate.py became an explicit condition/VerificationError branch. All four present public programs, including the test harness, contain no AST Assert nodes.
- All three result programs default to complete JSON on stdout, with no implicit curated-result write. A write requires `--output PATH`. Authentication no longer executes on import. The comparison child uses stdout and the active Python optimization level.
- INDEPENDENT_RESULTS.json and INDEPENDENCE_CHECKPOINT.json remain byte-identical to their original independent checkpoint. The checkpoint's original implementation SHA256 remains a historical version pin. The current implementation is authenticated by the new external public-map seal, with baseline-equivalence evidence below.
- The exact arithmetic, construction, claims, source theorem, conventions and -2 result did not change.

Verification completed 2026-10-15T08:37:01.214728+00:00:

- Normal Python, -O, -OO, and an actual environment-inherited PYTHONOPTIMIZE=2 parent/child each passed reproduce.py, compare_after.py and authenticate.py: **12 direct valid replays**. Full initial mathematical JSON agrees after removing UTC only. The inherited2 probe records parent flags2, child flags2, environment value2, and no child override flag.
- Each mode rejected five deliberately false controls via explicit VerificationError: expected witness signature0, a nonsymmetric form, an expected Meyer form with the wrong sign, a wrong proof SHA256 checked against the actual immutable original files, and a wrong certificate cocycle term: **20 rejections**.
- Default runs and all rejection controls preserved every existing family top-level file and added none. No original file or Git/service state was mutated.
- Final selected-original reauthentication: 2026-10-15T08:38:09.382625+00:00, 44 actual Git blobs/44 disk files, bytes/modes/closed inventory and pins equal, branch main.

Program transition pins:

- reproduce.py: old `f5b29eb7e7385a261e8671a5d6a7feb6ecf8e1bfd25170ef2a0e79d2930a72ee` -> hardened `51ee7bb4e6878119073159579313e371fca8f33a889e2952c035c10e3b468660`.
- compare_after.py: old `0fce88ad179a950e15410b75df3dc13df0d7895efef610c3a433f77265ffa7a3` -> hardened `8e79568f6d80958cd5f3d006708307681591bf36cf13f0b129683ed218e48a51`.
- authenticate.py: old `c110af0cf7c6c23cb616eb58ce28873f7bc07a2c0ef18c4de76fb6fadefbdf1c` -> hardened `b11a0afa6796b07bdd1efc41f93b2cd70d9e654a636126b0deb2b97c88f9f9c1`.

The new curated map includes this log, HARDENING_RESULTS.json and hardening_checks.py, and excludes itself and all private/raw/body/render/cache/replay files. Its digest/count are delivered externally after all mapped files settle. Original author accounting1/5; audit adds0 positive proof-search turns.
