# PR134 checkpoint v3 deadline repair candidate

**CANDIDATE_READY_FOR_INDEPENDENT_REVIEW**. The new v2 adversary sealed FAIL at2026-10-06T23:25:15.644645+00:00, actual sealer83152. Its sole remaining correction is C4-v2-delayed-journal-deadline: launch and running journal delays could consume the grant/deadline before the writer began or before its stale relative wait started. This v3 candidate addresses that correction while retaining the earlier C1–C6 repairs. It is not an independent PASS and claims no actual checkpoint, grant, lock or writer execution.

Exact candidate operator `700671ac0abfb8bc1403cfbfde4bb9ab26c919367ac1bebe2553770b0f7705bc` (42761bytes); plan `0c27669c14aa907020ccda7510535238147ec79c0b8ce645dd10cff4b0b41dcc` (103841bytes); request `ec2a80395715033be318b65add430367aea35147f393fd8a341be7b9b2b1cb9b` (100204bytes), all mode0644. The complete code remains import-safe and has no assert predicates.

## Deadline repair

The launching event is persisted before launch admission. If that write blocks, the operator then repeats writer invariants, checks the fresh grant window and completion margin, prepares the sanitized environment, and establishes a new absolute monotonic child deadline. It arms an independent watchdog before Popen and checks authority/deadline immediately before spawning. No previously computed relative timeout survives the launch-journal delay.

The watchdog binds the actual child's process group immediately when Popen returns. If spawn/PID publication itself exceeded the absolute deadline, binding signals that group immediately and the run rejects. It remains independently active throughout the potentially blocking running-journal write. The watchdog only signals; it never concurrently communicates or reaps. The main thread alone communicates, stops and reaps the child/group. Communicate receives only the remaining original absolute budget, so running journaling cannot start a fresh stale60second wait.

All exits stop/reap any child or surviving controlled descendants, cancel/join the watchdog, record actual PID, deadline, signal/expiry/join state and inspect failure outcomes without blind retry. The final journal writes after cleanup do not leave an active child that depends on that write finishing. Journal, spawn and wait errors do not produce an execution-success receipt. Actual resource release remains a separate later parent obligation after real full readbacks.

The threat model is cooperative ownership and controlled tools/process groups, as in v2: pinned Git/GitHub CLI, exact sanitized config/environment, exclusive own index/config locks and immutable tree/commit/CAS/push identities. This is not a hard real-time operating-system or filesystem scheduling guarantee. A Popen constructor that has not yet published a PID cannot give the watchdog a process-group identifier to signal; it remains armed and an expired PID is killed/rejected as soon as available. A blocked main journal can delay main-thread reaping after the watchdog kills the group; no success receipt claims cleanup until reaping and watchdog join complete. Arbitrary noncooperative process-group escape or physical file mutation is outside this cooperative contract.

## Exercised controls

Actual deadline-control PID87219 passed seven import-safe nonmutating cases using the exact production run/watchdog logic, a monotonic clock scaled1000times for short test waits, memory-only grant UTC fixtures, mocked Popen/children/group signals, and real joined watchdog threads:

- A launch journal that advances the fixture beyond expiry rejects before any mocked spawn.
- A running journal consuming120scaled seconds triggers the independently armed60second deadline and signals the child while logging is blocked; the child is reaped and the guard joined.
- A25second running journal leaves only about35seconds for communicate; the timeout is never restarted at60.
- Popen returning a PID after120scaled seconds binds and immediately kills/rejects the expired child.
- A running-journal exception stops/reaps the child and joins the watchdog.
- A spawn exception closes and joins the watchdog without a child.
- Ordinary completion within the original absolute deadline succeeds and joins the guard.

Every mocked child is reaped and every real watchdog thread is joined. No real subprocess, signal, grant file, writer or lock was used. The original child mock was corrected to model poll's real wait/reap semantics before the final passing controls; no operative change was inferred from that fixture correction. All28prior pure scope/path/mode/branch/expiry/environment/argument controls also pass, actual controlPID85768. These35local controls support this candidate; independent fresh review remains mandatory. Full runtime object/tree/CAS/index/push operations remain unexecuted.

## Archive, exact inventory and custody

Before any operative v3 edit, actual archivePID84341 validated the full sealed v2 review and created `checkpoint_v2_rejected_20261006` with ten public archive bodies: exact v2 operator/plan/request, old repair3, v2 review3 and ARCHIVE_MANIFEST.json. Its manifest SHA is `6066911cf99ff08f1620fa355c43c0bf4f5e82b3094bbcad1c24d4b7fcad3bfd`. The original v2 repair3 and review3 remain unchanged; their original paths are excluded from this core checkpoint and their immutable copies are included. The v1 archive and original v1 review3 remain exact.

New inventory is190owned pinned bodies: v2's180original inventory with only the operative operator replaced, plus v2archive10. There are nine future bodies (v3review3, v3repair3, plan, request, deterministic handoff) and precisely three existing updates,202total. All199new paths are absent from exact base `f896a8e429d250a94b2c08038237442d58abb9d2`. Actual input preparerPID85777 reauthenticated every new full body/mode, all169unmodified prior new bodies, both archives, original17full bytes/Git blobs, primary HEAD/nine full physical pins, own complete index/base, and full program preimages/prepared postimages. The dated22:54postimages remain unchanged. New priority families, new parent/root findings and corrected science are excluded from the core checkpoint.

Science metadata remains the dated mathematics/source100 gate, original claimed_solved1/5, currentPR134, research case25%, priority in progress without novelty/publication clearance,22completed/11published and active incomplete goal. No new scientific adoption or proof search occurred in this repair.

The v3 schema contract is consistent throughout operator/plan/request: independent result `pr134-checkpoint-v3-operational-adversarial-result/v1`; repair result `pr134-checkpoint-v3-repair-candidate/v1`; peer grant `pr134-authenticated-main-archive-peer-grant/v3`; plan/request/handoff use their corresponding v3 schemas. Trusted message evidence retains `pr134-trusted-peer-grant-message-readback/v1`. The new independent review folder is `checkpoint_protocol_v3_adversary_20261006`, only AUDIT.md/RESULT.json/FINAL_MANIFEST.json public. It must record scope PR134_math_intake_main_archive_only, exact operator/plan pins, verdict, mandatory_corrections, actual_reviewer_PID and no-mutating-operator/no-writer fields. The manifest includes full AUDIT/RESULT pins, scope/operator/plan, self_excluded FINAL_MANIFEST.json and self_checksum_claim false; ignored controls may be explicitly marked.

The downstream actual peer grant must seal all eight non-handoff future bodies after fresh independent PASS, plus all exact grant scope/count/preimage/primary/config bindings. Expected grant/evidence hashes must originate in the actual authenticated peer message/readback. The final handoff equals the deterministic canonical derivation from those pinned authorities and is not circularly back-pinned by the grant. New private authority paths are private_checkpoint_authority_v3_20261006/FRESH_PEER_GRANT.json and TRUSTED_PEER_MESSAGE_READBACK.json. No such actual authority or handoff is generated by this repair.

Only REPORT.md, RESULT.json and FINAL_MANIFEST.json are public from this folder. All helper/control/sandbox/journal receipts are under private_controls with an ignore-all policy, including its own ignore file. Their manifest pins provide local custody without authorizing their archive inclusion. The manifest excludes itself and makes no unsupported self-checksum claim. The actual late execution receipts cannot claim inclusion in the commit they produce.

## Research checkpoint

2026-10-06T23:32:26.631371+00:00: v3 repair and candidate sealing100% complete. Independent v3 operational review, real fresh authenticated peer grant, actual bounded execution/full receipts and explicit owner release remain pending. Research case estimate25%, mathematics/source100%, priority in progress and no novelty clearance. Strongest verified operational result: exact202-path candidate scope and35passing local nonmutating controls, including both adversarial delayed-journal mechanisms. No actual execution result is promoted.
