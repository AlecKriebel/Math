# PR53 original preparation: source-status correction, not a reconstructed counterexample

Prepared 2026-10-03 UTC, on main, for ROOT's later sequential audit. No merge, acceptance, native status update, Git index/ref change, external communication, paper, or upload was performed.

## Exact target and strongest verified finding

Record 30000671 / OWR-1453-004 asks whether complete commutative local Noetherian rings A and B must be isomorphic when A/m^r and B/n^r are isomorphic for every positive integer r. The individual isomorphisms are not required to be compatible. There is no domain or residue-field restriction.

I independently read the complete relevant contribution on printed p.106 / PDF p.24 of the [official 2007 report](https://publications.mfo.de/bitstream/handle/mfo/2988/OWR_2007_02.pdf?isAllowed=y&sequence=1), then inspected my fresh rendering. It explicitly reports Gabber's negative answer in the unrestricted setting. Its zero-characteristic examples have residue transcendence degree one; its positive-characteristic examples have infinite residue transcendence degree. It separates the integral-domain restriction and reports an affirmative result for residue fields algebraic over their prime fields. These source statements match the PR's scope and credit.

The [author's institutional publication record](https://experts.illinois.edu/en/publications/isomorphism-of-complete-local-noetherian-rings-and-strong-approxi/) corroborates the negative answer and positive residue-field condition, and identifies the 2008 paper in Proceedings of the AMS 136(10), 3435–3448, DOI 10.1090/S0002-9939-08-09401-X.

This supports already_solved as a prior negative answer to the extracted unrestricted question. It does not independently prove Gabber's construction. The full 2008 article remains inaccessible in this preparation; the report does not contain the construction. No present-day status for the separate domain restriction is asserted. No new paper is warranted for this source correction.

## Independent elementary audit

My approach and scope were saved in INITIAL_SCOPE.md before reading the historical review conclusions. Let a_r and b_r be the reduction maps of the quotient systems, and suppose phi_r are compatible isomorphisms: b_r phi_(r+1) = phi_r a_r. Coordinatewise application therefore maps coherent sequences to coherent sequences and preserves ring operations. Multiplying the compatibility identity on the appropriate sides by inverses gives a_r phi_(r+1)^(-1) = phi_r^(-1) b_r. Hence the coordinatewise inverse is defined on the inverse limit and is a two-sided inverse. Completeness in the separated maximal-ideal-adic sense identifies A and B with their limits. This proves the PR's conditional observation for all such compatible families; it does not select one from arbitrary levelwise isomorphisms.

For each positive r, the filtration of A/m^r has factors m^j/m^(j+1), for 0 ≤ j < r. Noetherianity makes these finitely generated A-modules, and m annihilates each factor. They are therefore finite-dimensional over A/m, yielding finite length and an Artinian quotient. This is unrelated to finite cardinality when A/m is infinite: Q[[t]]/(t) is already infinite. In particular, a compactness argument requiring finite level sets cannot be inserted without an extra assumption. Levelwise nonempty isomorphism sets also do not by themselves establish surjectivity of their transition maps.

The order-one quotient identifies the residue fields up to isomorphism. Algebraicity over the prime field is invariant under that isomorphism; it does not require a chosen common coefficient field. Algebraic closedness, perfectness, equicharacteristic, and finite transcendence degree cannot silently replace algebraicity over the prime field. No noncommutative, reduced-ring, integral-domain, or arbitrary transcendental-residue-field extension is proved here.

## Authentication and reproduction

The real draft remains OPEN with head d49a1bd56d8cc268159331e5ce868e258a32bb58. Its reported base ref is c6975ca76f9f667f1250ba403d0e6da2aafe14d0; the actual GitHub compare merge base is 60292bed09f59236aa192cb17aa138f7b4750e1a. The complete diff has twelve files: eleven small attempt files plus QUEUE.md. All eleven original changed attempt bodies (27,683 bytes) were authenticated through the head commit, selective tree chain, and blob API, and their computed Git blob SHA-1 and SHA-256 match GITHUB_AUTHENTICATION.json. original_archive retains these bytes unchanged.

The PR contains no executable proof checker or computational certificate. Historical author checker reproduction is therefore not applicable. Actual source-integrity checks are recorded separately as source checks, with true child PID, literal argv, start/end UTC, and complete stdout/stderr. ORIGINAL_SCOPE_CHECKS.json verifies the original zero-attempt budget, empty turns.jsonl, hashes, raw source correspondence, one-cell status change plus findings, and the metadata-only pre-review/post-review source-note change. It does not certify historical counterexample mathematics. The raw problem and report files matched the pinned source manifest; they were read but not copied.

The fresh source download is 472,577 bytes, SHA-256 b1001aadcbbf3a8c35707b4b58cddbce46132e7ecb7601869e676d5f702f805d, matching the original manifest. The 56-page PDF was transiently downloaded for hashing and one-page rendering; it was removed afterward. private_primary_reference contains only the selected page image and renderer outputs and must stay outside any publication/canonical attempt package. It is research evidence, not submitted content.

## Required precision repairs in any operative package

1. The raw research_results.json dictionary has **no OWR-1453-004 key**. SQLite's selected report is a non-NULL TEXT value containing the literal "{}". source_record.json's research_result_for_code:null and historical source_verification.json's null must be identified as serialized absence markers. The historical review's phrase "associated research-report entry is null" is imprecise. Preserve the archive and apply SOURCE_PRECISION_QUALIFICATIONS.md globally to current wrappers and any metadata describing the prior report.
2. The original PR body says only the attempt folder changed, while its final diff also changes QUEUE.md. The historical SOURCE_AUDIT.md statement about no shared queue/state edit describes the earlier source gate; it is not an accurate description of the complete final PR. Use accepted_pr_body_draft.md or equivalent explicit final-diff wording.

These are repairable provenance/presentation issues; no discrepancy was found in the advertised mathematical scope or source-status correction. No acceptance decision is made by this preparation. ROOT still needs its firsthand reconciliation and any separately assigned adversarial review before promoting it.

## Custody and limits

The initial authentication attempt failed during shared ENOSPC. Its partial files and unfinished capture are retained under historical_failed_authentication; no completed outer capture or recovered child PID/UTC is invented. The retry completed normally. Old completed captures bind their recorded prelaunch operator; Python child snapshots were added only for later captures, and are not claimed retrospectively for earlier ones. The fresh download script later received a metadata-only header filter; the actual download/capture and selected-page digest remain independently recorded. No old source snapshot is presented as a new execution.

DOI routes and the AMS page/PDF produced web-tool access errors; these current failures are not mislabeled as newly observed HTTP 403. The earlier PR's 403 is retained as its historical claim. The institutional page opened directly in this review. Bounded title/DOI searches disclosed no correction withdrawing the credited negative answer, but this is not an exhaustive literature audit. Literal exact-statement matching found no second pinned record; semantic duplicates and the old author's all-state PR gate were not independently re-audited here.

Preparation estimate: 100% of this original-only handoff, with no ROOT approval and no completion claim for the broader PR publication goal. Original substantive proof attempts: 0/5; new proof-attempt responses: 0. No separate original assistant-response count is inferred.
