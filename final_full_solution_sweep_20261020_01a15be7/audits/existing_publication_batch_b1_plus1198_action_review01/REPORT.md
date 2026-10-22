# Independent review: hold the sixteen-row action

The exact sealed plan and runner are **not accepted**. One known publication identifier is missing from the duplicate gate. All 29 existing-row overlaps and 3 within-batch overlaps were separately compared and concern different mathematical results; that does not cure the operational defect.

## Material finding — missing Park arXiv URL identity

`PROPOSAL.json` lines1056–1098 include the Park paper’s alternate DOI `10.48550/arXiv.1712.09148`, but omit the bare arXiv identifier `1712.09148`. `ops_core.py` lines36–40 compare ordinary aliases as folded full substrings. Therefore an already-entered publication represented by either `https://arxiv.org/abs/1712.09148` or `https://arxiv.org/pdf/1712.09148v1` produces no identity hit. `validate_plan` lines54–55 only require the full alternate DOI and do not catch the missing URL form.

Concrete counterexample: extend the captured 191-row ledger with the valid existing row `['Already entered paper', '', 'https://arxiv.org/abs/1712.09148', '']`. Execute the actual runner in isolated state with exact frozen data and injected read/write transports. All54 publication GET gates and all17 immutable PR checks pass. The full numeric-gid sheet passes UNFORMATTED_VALUE, FORMULA and metadata checks. The duplicate clearance stage accepts it, one fake sixteen-row append occurs, and `RECONCILIATION.json` declares the result verified. The PDF URL gives the same outcome. Both examples reproduce in normal, `-O` and `-OO` modes.

This is a known same-paper identifier already admitted by the plan, rather than an unbounded semantic-title-matching requirement. An existing paper represented by its arXiv URL must require reconciliation before a second journal entry can be appended.

A separate repair proposal should add the bare arXiv lead and validate that all chosen/alternate arXiv DOI identifiers have corresponding URL-compatible leads, including legacy identifier forms as applicable. Repeat these two counterexamples expecting zero write attempts and no action case. Review the new exact bytes with a fresh independent reviewer. This review did not edit the sealed packet or prepare an accepted execution attestation.

## Independent checks and boundaries

All1346 sealed manifest members were rehashed successfully before and after review. The complete production runner, core and imported numeric helper were read before execution. The frozen earlier eight-row runner was read but never executed. Exact16 row arrays, all identity leads and bindings, root scientific adoptions, and the entire 29+3 clearance evidence were inspected. `SEMANTIC_DECISIONS.json` records a distinct, exact-row/pair mathematical reason for each clearance; no blanket author exemption was adopted. Every full43-column evidence row was checked against its baseline row and hash. The exact adopted qualifications and one shared Geneson row for PR1169+1176 were retained.

Each of three Python modes ran24 actual-runner scenarios, including baseline success and the two defective successes above. Negative cases reject a new same-author row, a catalogue identity in column43, a source identity, an old concept/family record, unknown Zenodo fields, concept advancement, unknown registry fields, changed selected PDF, PR1176 body drift, HTTP403, unexpected1198 version-DOI200, formula/value drift and metadata drift. Unknown/malformed write outcomes, old-column43 changes, gaps, reversal, duplicated additions and nonempty native replies stop after the sole fake write; a case blocks every attempted rerun. Read-only mode and actual false production readiness make no writes. The actual durability calls execute and are observed before the fake write. Pure identity, bounded GET retry and narrow Springer UUID controls are explicitly distinguished from full-runner cases in the receipts.

The test used the actual `main`, publication, input, readiness, clearance, request and readback implementations. Only filesystem constants and external transports were redirected; large identical captures use hard links. This is not a live service replay or an independent reconstruction of the accepted mathematical proofs. A fresh live prewrite remains required after repair. Final input drift checks were source-reviewed; this reviewer does not claim an independent injected final-input-drift run.

One nonblocking precision observation: core lines77–81 also retry generic GET transport exceptions up to three attempts, while the prose describes only HTTP429/502/503/504 retries. These remain bounded GETs and do not create a write retry.

`ACTION_REVIEW.json` explicitly withholds approval. Production readiness remains false and the production action directory is absent. No external service call, spreadsheet append, deposit, PR mutation, communication, Git reference/index change or shared-cursor change occurred. Raw sheet rows and private captures remain ignored; public-safe comparisons and summary receipts are separate.

Overall sweep estimate: **79%**. This independent review family: **100%**, completed with a material hold.
