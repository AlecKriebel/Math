# Final hostile review: order-12, parameter-4 aggregate verifier v3

Date: 2026-07-26  
Reviewer role: independent adversarial verifier reviewer  
Verdict: **PASS for the exact incomplete scope; no aggregate claim**

## Exact frozen review target

The decisive verifier snapshot was:

- `checker.py`: `8b09516c6bff615670acd01bd4083adacb024ab84751d79b8d8ec1a69b0bbc30`
- `cli.py`: `bc4dabbe9a18f50cd070b40fbaf5fc1f62f63b665f6172ff8f057eeacc3df810`
- `parent_reconstruction.py`: `d69baa904f92087ae4c8e46515996a03eb81faa440f0e32d15cfd81831b6afb6`
- `__init__.py`: `b8d10fd40fdfe27617112354d372446d12a3875d41aed1511f338e2ecd64743f`
- `__main__.py`: `0f7d54f3fbb1f79a85eb8110f11793db99da6f3c61ee979de5abe9a1b5f3fdb3`
- aggregate source-set digest: `9ea4397d1526302ca499d9c56af8a0c70ad86234b5e8eb4b9da0a9bcbfa76c46`
- tests: `f7489c395ce4dd439cc11fb91d0fc6b3d87cd491d7b5a07e4384b863279dd583`

No production or verifier artifact was edited during this review.

## Verdict

I found no blocking defect for the verifier's present, explicitly incomplete use. On the exact bytes above, it independently reconstructed the frozen parent and leaf universe, validated the complete v3 run/config/outcome/certificate bindings, audited the 16-cube coverage, and freshly replayed the sole completed leaf's LRAT proof. It then reported exactly:

> `INCOMPLETE_1_OF_16_VERIFIED_NONCLAIM`

and:

> No aggregate SAT/UNSAT claim is made. This report validates exactly 1 of 16 frozen leaves; 15 remain pending.

The command-line exit code was 3, as intended for an incomplete report rather than certified aggregate success. The checker child itself exited 0 and emitted the exact success line `c VERIFIED`.

This is **not** an aggregate UNSAT certificate, an `n=12,k=4` exclusion, or a mathematical result about the γ–θ conjecture. It validates one frozen leaf and the integrity/coverage framework around the still-incomplete run.

## Independent replay evidence

I created a new, initially nonexistent external ledger:

`reviews/order12_k4_v3_aggregate_hostile_replay_8b09516c`

The verifier created it with mode `0700` and its files with mode `0600`. This avoided relying on the earlier historical replay.

- replay manifest: `da860fd368cc0c98a5e5269008eec9e94a87300fa0a7ded5188aad13cdc952df`
- case-1111 record: `0a7e6d41f0a08161e4358888730e5c71bd73af59540ec82f912804c5f5fb7b24`
- source-set current: `true`
- historical producer revalidation: `false`
- fresh children this invocation: 1
- resumed children this invocation: 0
- pinned `lrat-check`: `5d7d77a57457db82e57f2505ea9d0267ff0bceff197235b6edfc8fda1f26c7a2`
- reconstructed leaf CNF: `aafc85341993ed030fe72ba222a4efaa5a02f6ea6fa95519a9dd2ed755b94d1f`
- copied LRAT: `90787a09742237e3c38c8b4f36916b2d0ccbd37be3920feb16ddb3306ec228d0`
- checker/CNF/LRAT hashes matched before, in the private directory, and after
- child exit: 0; stderr empty
- wall time: 0.36429 s
- peak polled RSS: 45.83 MiB
- all live load, memory, responsiveness, and disk gates passed

No CaDiCaL process was launched. Only the pinned proof checker was run.

A second invocation against the same ledger executed zero children, resumed exactly one current-bound record, retained the same record hash, and returned the same incomplete nonclaim. This confirms the intended append-only resumability path for the current state.

## Static and clean-room checks

The verifier runtime imports only the Python standard library and its own clean-room parent reconstruction. It does not import the search, synthesis, runner, or earlier verifier transition cores. References to those files are frozen hash bindings, not executable imports.

The clean-room reconstruction matched the retained parent byte for byte:

- parent: `adbe0c01614bae6cd3aed4ccdcd45a757ca56e7ef9c4f2f280f2d8ef200e40ac`
- 18,381 variables
- 114,742 clauses
- 1,180,016 literal occurrences
- cube variables `(4, 14, 23, 31)`

The partition audit reconstructed all 16 four-bit leaves, enumerated all 16 assignments, and checked all 120 leaf pairs for disjointness. Its coverage-row digest was `4a79409f32950b81587d675fde140e7d335e26e483793d066a7823766d40398e`.

The production bindings were:

- run manifest: `d3c914f38ea3771d65db76ed14e092ea0ce84003b1fff73839e033903361ed60`
- partition: `0cf8129734d5a5ea121a3f26c08b46dcbe2b4a154ef17ce24f50eb8d0266b33f`
- latest checkpoint: `3dbb5c8336528603c73a04066be85ee317978603d8a56c3103853aa126625202`
- checkpoint sequence/count: 2/3
- historical attempts: 1
- completed leaves: only `1111`

The production tree's aggregate file-content digest remained
`adbf66d83bc8b7109d3e3f1c8d502797a73f418f83f2a2c7c1e41b26cda20351`
before and after replay. Its aggregate file-metadata digest likewise remained
`42838a7277de3eb081799f5f45fd9df7a83e5468b5cbdacc47642198720ca645`.

## Adversarial gates reviewed

The final 18-test suite passed under Python 3.14.6. The exercised gates include:

- rejection of v2 attempt schemas and JSON booleans masquerading as integers;
- byte-exact clean-room parent reconstruction;
- exact incomplete and complete-fixture statuses;
- SAT/nonclaim separation and sealed production scope;
- raw and normalized binary-DRAT scanning, including noncanonical varints;
- normalization-report binding to the exact addition stream;
- strict child-output parsing;
- artifact, child-record, replay-record, and policy mutation rejection;
- unexpected root-entry and FIFO rejection without blocking;
- campaign-wide heavy-child locking;
- append-only 16-record fixture replay and resume behavior.

Source inspection additionally confirmed exact run-root/case/attempt inventories, canonical JSON parsing, single-link regular-file checks, checkpoint-chain and attempt/inventory bindings, fresh private checker/CNF/LRAT copies, empty child environment, process-group termination, wall/RSS/file limits, source hashes before and after replay, and terminal success only when all 16 ordered leaves are present and replayed.

## Residual caveats

The verifier contains an explicit compatibility vector for one older verifier source set. That path was not used in this verdict: the decisive hostile evidence came from an empty ledger whose manifest is bound to the current `9ea4397d...` source set and whose proof checker ran during this review. Future publication evidence should likewise distinguish fresh current-bound records from historically revalidated records.

The run remains at 1/16 leaves. The parent-encoding theorem and its assembly into the intended mathematical search universe remain separate obligations even after a future 16/16 aggregate certificate.

Machine-readable review evidence is in
`reviews/order12_k4_v3_aggregate_final_hostile_evidence.json`.
