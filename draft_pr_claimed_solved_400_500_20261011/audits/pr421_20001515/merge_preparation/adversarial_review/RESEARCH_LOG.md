# Administrative adversarial review

Scope: independently review only `finalize_pr421.py` and the private synthetic test driver. No live API, network, `gh`, Git mutation, other problem mathematics, or outside communication. Synthetic probes and their temporary fixtures stay in the assigned review directories.

## 2026-10-12T23:58:40Z — checkpoint (35% complete)

- Read the 1,050-line helper and complete synthetic driver independently.
- Reviewed hypothesis: caller-pinned native receipt bytes and JSON pointers bind an accepted package; every candidate read at a new head follows its current selected `claimed_solved` Status; writes preserve current main through immediate Merkle trees; mutation uncertainty is handled by GET-only recovery without retries.
- Success criteria: independently reproduce the existing suite under ordinary and optimized Python, add probes for previously uncovered inconsistent Contents responses and last-moment readiness/merge races, record exact remaining gaps without asserting live readiness or native-receipt authenticity.
- Helper SHA256: `7825c3b6257e5d100dd1884baee371400edc720f3d3d061038eab6e933b23d3b`.
- Driver SHA256: `103f8dee75d321d5f90af61d8d0a5d8782ffb6e1cd335bdbe8551d4f4f745414`.
- Initial deductions: immediate Merkle trees are hash-reproduced and unrelated child subtrees remain opaque. Root evidence pins flow through nested document pins. Safety checks use explicit exceptions, not bare asserts.
- Open probes: `selected_at_head` appears to lack the Contents-to-commit QUEUE binding implemented in `prospective`; the ready mutation has no expected-head server-side condition; response-loss handling may discard a factual merge receipt if current scope has drifted.

## 2026-10-13T00:01:31Z — checkpoint (75% complete)

- Independently reran the complete supplied suite: 31/31 passed under Python 3.14.6, ordinarily and with `-O`. Rehosted its temporary case directories inside the assigned private adversarial-review directory and disabled bytecode writes.
- Four new attack constructions reproduce identically under both modes: an unbound stale Contents Status response allows five selected candidate reads at an actually withdrawn head; a malformed duplicate selected row passes the Status gate and permits five candidate reads before a later QUEUE comparison stops planning; a last-moment head advance is readied before the later gate stops merge; and merge response loss plus current-main scope drift leaves no factual historical merge receipt despite confirming the merge in GETs.
- Preserved original reviewed helper/driver snapshots in the assigned private review folder with their original SHA256 pins.
- `PROBES_NORMAL.json` SHA256: `8c9dd274a909653fddfaa0c307a91148a3f4f52d621d06bb7db00cbbee3b8118`.
- `PROBES_OPTIMIZED.json` SHA256: `cc28cfd473966a67698789308efe2d8c9f46962bb97ef0f846698285e4212f9c`.
- AST inspection found zero bare asserts in helper, driver, and independent probe. No live API, network, gh, or Git mutations occurred.
- Parent acknowledged the gaps and is revising the helper. Exact-head readiness cannot be established atomically by the current GraphQL mutation; a post-response check can prevent merge and record drift but cannot undo the readiness action. This is an operational assumption/limitation requiring truthful documentation, not a property established by synthetic tests.
- Remaining work: independently validate the revisions and record strongest verified administrative result. Native receipt authenticity and actual live state remain explicitly unverified.

## 2026-10-13T00:09:09Z — final checkpoint (100% administrative-review completion)

- Parent froze helper at `374af7a27f08410c44ff2462ee1247a6ba452928007d02d8fe56983986035f6c` and driver at `690f60378ff4bfc389a8d5b31c5432e5a0bf2449e04e059e58cfb37a2d7ebd54`.
- Supplied frozen suite passes 39/39 ordinarily and under `-O`. Independent checks additionally pass five correction/race families, two preservation families, and eight native-evidence-chain cases in both modes.
- Strongest verified result: under explicit source-provenance/API assumptions, tested unbound or malformed Status evidence and broken native joins stop before selected candidate reads/writes; Merkle integration preserves current main outside the allowed overlay and exact accepted-row bytes outside DOI/Findings; response-loss GET recovery preserves factual readiness/merge metadata while withholding current-packet verification after drift.
- The malformed-duplicate correction required extending the root's initial trailing/missing-final-pipe guard to missing/escaped first pipes; all four variants now stop at the early gate.
- Preserved reviewed frozen source snapshots. `EVIDENCE_SHA256.json` pins fourteen source/probe/report artifacts and has SHA256 `bf738a1e118abedec95e8977f48d88bc45228827333bdeaef5dcc655a152eec8`.
- Remaining exact gap: ready POST has no expected-head server-side condition. Pre/post checks and truthful drift receipts work, but an exclusive-branch/no-concurrent-head-writer operational assumption is needed for exact-head readiness. Expected-head PUT merge is server-conditioned and independently rejects the tested final race.
- No remaining reproducible administrative code defect requiring correction before a GET-only live plan was found at the frozen pins. Native provenance, true reviewer independence, actual mathematical acceptance, live remote state, and the operational assumption remain unverified by this subreview.
- Recorded final result in `FINAL_REVIEW.md`. No live actions, external communication, helper/test modification, or other problem work occurred. This percentage refers only to the assigned administrative adversarial review.
