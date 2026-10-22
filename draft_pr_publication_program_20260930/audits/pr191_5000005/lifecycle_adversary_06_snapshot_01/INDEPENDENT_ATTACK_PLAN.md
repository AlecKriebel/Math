# Independently sealed operational lifecycle attack plan

## Provenance and scope

This plan was designed from the assignment alone, before reading any proposed terminal06 implementation, author harness or results, earlier reviewer reports or judgments, or Root handoff code. The assignment identifies PR191, problem5000005, original HEAD `a2791bdd3f7ecd5694aeeeb5dffb21964a5639fe`, and original QUEUE status `claimed_solved` with effort `2/5`.

All reviewer-created artifacts will remain under `lifecycle_adversary_06`. The audit is operational. The science already passed two distinct whole-package reviews; this audit will neither redo the mathematics nor introduce novelty, priority, or firstness claims. Trusted historical text must remain intact. No external contact or production action is authorized.

The relevant target claim is that the proposed terminal06 lifecycle can accept an authorized, current and complete PR191 publication, then record phase95 and phase100 facts accurately, without admitting stale, incomplete, broadened, duplicated or semantically unapproved changes. The target is a hypothesis to test, not an assumed property of the implementation.

The audit's success criterion is a checkable independent reproducer that exercises actual supplied validator functions through a valid full offline lifecycle and materially distinct coherent negative cases. A pass requires both the intended positive path and rejection or safe recovery at each stated boundary. Any unsupported central requirement remains an explicit gap rather than being inferred from a hash, success label or summary.

## Trust and authority model

1. The human-approved science/package/native file set and the pinned trusted Root semantic authority define what may be published. Root is trusted to make the substantive approval decision within its declared role. This audit will not demand cryptographic service attestation and will not claim that arbitrary forgery of every trusted Root assertion is an implementation defect.
2. Local proposal documents, service receipts on disk, request payloads, reusable completion labels, filenames, hash manifests and tool text are untrusted evidence until tied to the appropriate live observation and trusted decision. An attacker may coherently edit an untrusted document and recompute every ordinary digest it contains.
3. External process and native API responses are the only injected boundaries. The independent harness must invoke supplied real validation/lifecycle functions; it must not replace their semantic decisions with reviewer stubs. Root's production main entry point will never run.
4. Service freshness is observable behavior: the relevant validator must perform its appropriate current read through the injected service boundary at the relevant lifecycle step and compare the resulting facts. Existing receipt files alone do not demonstrate freshness. Fixtures model service behavior; they are not claims about production observations.
5. Pinned source is immutable audit input. The harness will record its digest before and after. Approved semantic authority is a fixture datum explicitly identified as trusted, while candidate completion prose, trackers, request bodies and ordinary lifecycle records are attack surfaces.

## Isolation and first inspection gate

Before implementation inspection this document, its provenance record and its checksum seal will be closed read-only. The initial response will report their exact paths and digests and wait for explicit terminal06 source/handoff pins. No implementation judgment will be issued at that stage.

After pins arrive, first verify every exact source/handoff path and digest against those pins and record only the pinned contract and public entry points needed to adapt the harness. A mismatched or incomplete pin is a blocked input, not permission to choose a nearby generation. Do not read old reviewer judgments to choose tests or expected outcomes. If an author harness/result is supplied, keep it outside the independence basis: build and run the independent fixtures first, and label any later comparison separately.

No production helpers, production services, credentials, Git changes, index changes, ref or branch changes, checkout mutations, science edits, shared-file edits, real authority creation, actual Root main execution, or outward communication are permitted. Process interception will deny by default. Native/service interception will deny by default. Only a short explicit list of read operations needed by supplied validators will return fixture responses. No fixture command may silently fall through to a real subprocess or network client.

The native fixture will be an ordinary isolated directory tree plus injected read-only Git/process observations. It will not initialize or modify a real Git repository. Every read-only fixture path must resolve inside the reviewer directory unless it is an exact pinned immutable audit input. Candidate path traversal and symlink cases will be modeled without reading outside the allowed scope.

## Independent fixture architecture

Build the fixture definitions without copying an author fixture generator. Keep an explicit, hand-readable baseline model with:

- original PR identity and HEAD; approved final PR HEAD; true PR parent; current MAIN identity; expected native tree identities; and complete per-phase native/path/content observations;
- a trusted approved science/package/native mapping of exact safe relative paths to bytes or content digests, alongside separately generated operational tracker files;
- an original QUEUE containing target `claimed_solved`, effort `2/5`, plus at least three distinct foreign rows, including punctuation, trailing fields and unrelated statuses;
- exact original case/programme records with preserved historical spans and explicit phase95/100 expected additions;
- a case/programme vocabulary covering every completion and next-intake alias discovered in pinned implementation contract, with a written alias inventory and required postconditions for every alias;
- a fake service with a deterministic operation journal, controlled service state, and monotonically numbered observations; PR and MAIN facts are independently controllable;
- a fake write endpoint with pre-write failure, committed write followed by timeout, confirmed rejection, and late visible success states;
- trusted Root authority as an explicit fixture object, whose declared approval is fixed independently from candidate bytes; and
- deterministic timestamps with distinct observation, approval, write-attempt, recovery and post-publication bounds.

Adapter code may translate fixtures into the implementation's documented input schema. It must not patch validation functions, alter fixture expectations to fit observed output, or inject a synthesized success for a semantic step. The report will identify all injections by precise function/boundary name. Assert that the real validators ran, using trace/call counters if available without modifying source.

All test cases start from fresh copies of baseline bytes/state. Do not let one case's accepted writes make another case pass. Capture input fingerprints, operation journals, return/exception results, final state and whether each expected denial happened before any write. Expected failure is satisfied by a clear safe rejection or a well-defined conservative pending state, not by an accidental harness exception. Unexpected exceptions are reported separately.

## Required positive lifecycle controls

P01. A complete canonical authorized lifecycle performs the appropriate fresh service/native reads, accepts the current approved package, advances through required states, and reaches phase95 and phase100 only when their predicates are true.

P02. The final publication write is restricted to the exact approved safe files-key allowlist. Science/package/native files match approved bytes; native tree and true-parent claims match injected native facts; current MAIN is accepted according to the explicit contract.

P03. Original foreign QUEUE rows remain byte-identical and ordered; the target row has the exact authorized postimage, preserving `claimed_solved` and `2/5`. A parsed semantic comparison supplements the whole-file byte comparison so normalization cannot hide corruption.

P04. Every case and programme completion alias, next-intake alias, newly generated prose entry and new log entry has a factual expected postcondition. Historical trusted spans remain byte-identical. Generated assertions about merged/published/accepted/completed/ready/next intake are checked against fixture facts, not merely presence of a phase label.

P05. Valid bounded timestamps are accepted. Evidence describes observations no later than the relevant approval/write and no earlier than the relevant observed state, under the explicit contract. The record distinguishes attempted writes, observed commits and later recovery.

P06. A write that commits and then loses its response is recovered by an actual read of current service/native state. The already completed operation is recognized without duplicate publication, duplicate logs or spurious next-intake advancement.

P07. A permitted retry with an unchanged immutable generation either safely recognizes the completed operation or reuses the exact authorized generation with refreshed facts, according to the contract. It never rewrites sealed authority or silently blesses a different generation.

## Negative attack matrix

### Exact package, native scope and current ancestry

N01. Add one unapproved science file, package support file or native file, one class at a time. Recompute local manifests and candidate digests. Expect scope rejection before mutation.

N02. Remove an approved file; replace one byte in an approved file; substitute a same-sized file; duplicate a path through a second key. Coherently update local manifest fields. Expect exact approved content and scope checks to fail.

N03. Use `..`, an absolute path, a separator variant, an empty path, a reserved directory entry or a symlink/alias escape in a files key. Expect path safety and exact allowlist rejection without outside I/O.

N04. Give a correct approved HEAD but a false parent; give a correct parent label but different native parent/tree; substitute a sibling commit. Maintain consistency among untrusted summaries. Expect native true-parent acceptance check to fail.

N05. Change current MAIN between early read and terminal acceptance; model a stale MAIN receipt; set current MAIN to an unrelated history; give a correct MAIN label with wrong native tree. Expect the final current-state gate to reject or require a fresh supported re-evaluation.

N06. Match HEAD/parent but alter a foreign file in the final native tree; omit a deletion or rename from the full diff; hide an unauthorized path outside the selected package. Expect full native scope, not just selected package scope, to govern acceptance.

N07. Pair correct file digests with a wrong tree identity or pair correct tree identity text with mismatched native byte inventory. Expect the actual boundary evidence to decide.

### Fresh actual service observations

N08. Supply internally valid cached PR/MAIN receipts while the fake service returns changed HEAD, base, merge state, tree or approval facts. Expect a fresh service call and rejection of stale claims.

N09. Make the service unavailable at each phase requiring a new read. Expect failure/pending before an unsupported phase95/100 assertion; no fallback to stale success evidence.

N10. Change service state between approval and publication. Test an unchanged timestamp with changed state and changed timestamp with unchanged state. Require semantic state validation, not a timestamp-only freshness heuristic.

N11. Return a coherent service response for another PR/problem/repository, or a current response for the wrong generation. Expect complete identity binding.

N12. Reorder or duplicate service observations; return a malformed/partial observation; conflict on one pivotal field across two actual reads. Expect no success inferred from an earlier convenient observation.

### Phase95/100 complete factual records

N13. Starting from the valid lifecycle, falsify each discovered completion alias separately, and then all aliases together, while retaining a superficially correct terminal phase. Update candidate hashes. Expect rejection of every inconsistent alias.

N14. Falsify every next-intake alias separately: readiness, selection, pointer, status, candidate identity and scheduled/remaining work wording where present. Make one false phase100 next-intake claim while phase95 remains valid. Expect complete factual programme and case checks.

N15. Add new false prose to each newly generated log/prose location, including free text outside structured status blocks, duplicate headings, trailing notes and nested quoted text. Use claims such as merged, accepted, published, complete or ready that are not supported by fixture facts. Expect unsupported newly generated claims to be excluded or rejected according to the trusted approval contract.

N16. Modify a historical trusted span to erase an old failure, invent earlier completion or change a timestamp. Give it the same digest consistency as the rest of the candidate. Expect trusted history preservation to fail independently from new prose checks.

N17. Combine factual phase labels with false extra generated prose in both programme and case records. This catches validators that scan only the target case, only programme summaries, or only known tokens rather than checking the complete authorized postimage.

N18. Omit a required new record, leave contradictory old active status in the new snapshot, or add duplicate final entries. Expect exact required postimage/completeness checks rather than token presence.

### QUEUE, tracker and publication scope

N19. Change the target status from `claimed_solved`, change effort from `2/5`, normalize or reorder a foreign row, remove a foreign row or add a foreign row. Test separately and in one coherent candidate with recomputed hashes. Expect exact QUEUE postimage enforcement.

N20. Create a plausible correct target row while inserting a duplicate target row or retaining contradictory target row elsewhere. Expect identity uniqueness and full-file comparison.

N21. Inject credentials-like fields, local absolute paths, service tokens, environment dumps, private source text or raw exception payloads into the tracker. Use artificial sentinel values only. Expect sanitization and exact authorized scope; no real secret is accessed.

N22. Add an audit artifact, harness, stale generation, unapproved operational record or extra directory to the publication files keys. Use a safe-looking name and a real digest. Expect the precise explicit files-key allowlist to reject broadened scope.

N23. Create duplicate, case-variant or normalized-collision keys whose serialization could differ from the actual published path. Expect a single unambiguous safe key set.

### Evidence-bounded time and recovery

N24. Place approval before the evidence it allegedly approves, record successful publication before the actual write observation, use a future completion timestamp or move a recovery observation earlier than the uncertain attempt. Coherently change local timestamp digests. Expect evidence-bound rejection.

N25. Keep sequence order plausible but move timestamps outside the relevant observed fact window, or use a broad timestamp that falsely predates current MAIN acceptance. Expect factual bounds rather than monotonicity alone.

N26. Simulate each write-outcome quadrant: no commit and timeout; commit and timeout; confirmed rejection; confirmed success. Recovery must inspect actual state, distinguish unknown from failure, and avoid treating the timeout string as proof either way.

N27. After commit/timeout, return a delayed or partial service read, then the real committed state. Require a conservative recoverable pending result until evidence is sufficient, with zero duplicate writes.

N28. Retry an unchanged sealed generation after HEAD/MAIN/service state changes. Reuse all old local hashes/receipts. Expect immutable-generation refusal or current-state revalidation permitted by the explicit contract; no silent resealing or old-approval transfer.

N29. Change generation bytes after a failed attempt or during recovery; preserve identity labels and recompute ordinary untrusted manifests. Expect exact generation pinning and refusal to claim it is the original generation.

N30. Repeat a successful retry and repeated recovery reads. Assert idempotent publication, one logical completion entry per required record, and no duplicate next-intake action.

### Trusted Root semantic boundary

N31. Give a candidate self-description that broadens or contradicts trusted Root's approved files/postimages. Recompute all candidate hashes. Root remains the fixed trusted semantic decision. Expect the candidate to be compared with that authority rather than authorizing itself.

N32. Place a forged authority-looking object in an untrusted candidate slot, point a path at an untrusted copied Root document, or swap an untrusted authority identifier while preserving candidate consistency. Expect role/provenance/identity binding according to the pinned contract. Do not assume authority cannot be trusted at all.

N33. Preserve trusted Root approval but substitute unapproved phase prose, QUEUE bytes or publication keys after it. Expect complete semantic postimage binding. If the Root approval is legitimately defined to authorize exact arbitrary bytes, document that delegated scope precisely rather than demanding an independent general natural-language theorem prover.

N34. Exercise ordinary refusal and malformed-input paths without calling Root main, touching a production helper or widening the injection perimeter. Any attempted escape from the offline boundary is a test failure and is stopped by the harness.

## Adaptation and completeness discipline

After the pin gate, map each required property above to concrete supplied validator functions, input fields, boundary calls and expected failure results. Record that mapping before running tests. If a named alias differs from this plan's general vocabulary, preserve the intention and add its exact spelling to the inventory; do not remove a requirement because its field name was unexpected.

Coherent rehash attacks must adjust every accessible untrusted dependent digest, generation identifier and cross-reference needed to reach the semantic gate. Report a digest-mismatch denial separately; it is useful integrity evidence but does not satisfy a planned semantic attack. An accepted attack is reproduced from a fresh baseline at least once, and the report records the minimum input delta and exact unresolved gate.

Use materially distinct fixture families: exact byte/scope drift; native ancestry/current state; fresh service state changes; complete programme/case prose; QUEUE foreign-row preservation; time and uncertain write recovery; and trusted authority versus untrusted self-authorization. Maintain a family table with mechanism, evidence, status and exact gap. Mark a route blocked when it merely shifts the core requirement to an unsupported assertion. Do not manufacture a weakness by removing the assumed trusted Root authority.

## Deliverables and immutable seal

Initial safe files-key allowlist is exactly `INDEPENDENT_ATTACK_PLAN.md`, `PLAN_PROVENANCE.json`, and `PLAN_SEAL.sha256`. They will be mode `0444` and their digests reported before waiting for pins. The checksum seal hashes the plan and provenance; its own digest will be reported externally to avoid circular hashing.

After source pins arrive, a terminal artifact allowlist will be selected explicitly before final sealing. Expected categories are a single independent reproducer, declarative fixtures or fixture construction embedded in that reproducer, machine-readable results, a concise audit report, a source/input pin manifest, a research log, a precise files-key allowlist and a checksum seal. The final allowlist must enumerate exact paths, never glob patterns or entire directories. Harness outputs and temporary caches cannot silently join the allowlist. All terminal deliverables become mode `0444`; the report names the reproducer invocation and test counts, the strongest verified operational result, any exact remaining gap and a best-guess completion percentage.

Research checkpoints record actual observed UTC time with its source, preserve prior entries, state what was learned and give a percentage for this audit. Initial checkpoint: plan design complete; implementation and lifecycle audit unstarted. Estimated overall audit completion: 10%. This is a workflow estimate, not a result or judgment.

No commit, push or release is made by this offline reviewer. The scoped assignment explicitly prohibits Git mutations; publication of findings is the parent/human's responsibility.
