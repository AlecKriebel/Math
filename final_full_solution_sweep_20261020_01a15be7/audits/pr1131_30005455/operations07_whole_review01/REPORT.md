# Independent whole operations07 review — HOLD

The exact operations07 package is **not ready for production**. A fresh actual-parser counterexample overwrites a concurrent saved deposit identity and then certifies successful staging. This is a preservation failure, independent of the infrastructure interruptions described below. No real provider, Git, DOI or spreadsheet mutation occurred.

## Decisive finding: concurrent original-manifest state is overwritten

The source is anchored at manifest `56c0739ae44b83f860ca2e2cf57c06903ba468a42ebb033d4282e8856af98cca`, bootstrap `20c8051641a9334c0efd912b63ca210a0461f6e34abff07135f0d7e67eb011b6`, outer preparation seal `8551344abd63c4edd9cb3dc22c815c1d69e4581f846b0f2db75f4dde0de1cc8a`.

Run `independent_state_race.py` in a fresh copy of this review directory using isolated, no-site, no-bytecode, optimize0 Python; its fresh output directories must not already exist. It uses the actual checked07 loader, real `main` argument parser, the entire inherited account/native/PR/sheet validators, real local runtime intentions, actual durable writers/fsyncs and certificate links. Every network/process adapter is intercepted; the fake account contains the complete pinned197-record historical fixture.

The reviewer injects one ordinary concurrent filesystem event in the fake native delegate's `create` method, immediately after creation of777 has taken effect. Before the shared tool saves its own state, another process writes the **same original-manifest production state key** with id999 and a distinguishing unknown marker. The workflow then:

1. Accepts its legitimate create result777.
2. Overwrites the newly existing999 state with777, losing the marker.
3. Uploads both intended files and updates metadata.
4. Returns ready_to_publish and creates ZENODO_STAGE_VERIFIED.

`CONCURRENT_STATE_RACE_RESULT02.json` contains the exact initial and final objects and outcome: four fake native writes, no error, concurrent_exact_bytes_preserved=false, stage_verified=true. A first separate execution produced the same result; the second is the definitive fully retained capture. The observed failure does not depend on forged approval or changed source, missing priority checks, an optimized interpreter, a malformed provider response, the memory adapter's behavior, or absence of a saved state being misread as proof of no earlier POST.

The mechanism is visible in the reviewed code. `lifecycle07.EdgeDelegate.mutation` checks state absence immediately **before** create, but its postcreate check rechecks local source/approval/history rather than requiring an exclusive installation of new state. The inherited `zenodo.run` retains its original initial state=None decision and calls `save_state` after create returns. The shared `save_state` installs a temporary file with `os.replace`, replacing whatever now occupies that state path. The next upload gates see only777 because999 has already been erased. Runtime intent preservation cannot protect this separate shared state file.

**Required repair:** the initial07 state installation must fail without overwriting if any state appeared after its initial check, preferably by an exclusive atomic creation rather than another check followed by replace. Preserve the concurrently written bytes and the known created777 fact, record an ambiguous/conflicting outcome and require GET-only reconciliation. Audit the two postpublication shared state saves as well: preserve complete then-current unknown state fields and prevent silently replacing a concurrent different identity. The latter publication variants were identified by code inspection, not independently reproduced here. A repaired package needs a fresh independent whole review and exact root adoption; this report grants no authority.

## What was independently inspected and verified

All four production07 modules were read in full, along with source freeze/approval example, the exact new root entry guard and contract. The original05 bootstrap, ops_common, publish_and_ledger, collect_live, native_policy and top-level Zenodo client were read in full; the used read-only Git tree helpers were checked. Unused historical integration mutation paths were not reaudited as newly executable07 actions;07 exposes no integration/merge command.

The outer preparation closure was independently checked:778files and56directories, complete bytes, permission modes and integer nanosecond mtimes, exact path inventory. Deep input readback authenticated196old public payloads,13preserved runtime files,56scientific/support files,5held-context files,6source07payloads,3preserved wrapper files and the shared Zenodo dependency. All14historical private provider seed files and their index rehashed. The original revoked05 authority remains absent under its live name; production07 runtime/approval remains absent. Scientific manuscript correctness and priority are the parent's already accepted work, not newly certified by this operational review.

All145preparation custody cases independently decompressed and verified:32128files and3337514957original bytes, every referenced chunk and original file hash and manifest closure. This replay checked stored metadata and original bytes; the preparer's separately sealed filesystem reconstruction receipt was authenticated, but its complete physical reconstruction was not repeated here. The recorded original container repair and ENOSPC exclusions remain in the untouched preparation package.

The root entry guard SHA is `8e4e7e1ecbe77c272c0cb971bb65beb955dc6aa450ea93d57049aee2dec8b871`. Fresh normal check-only succeeds; -O, -OO and wrong externally supplied driver hash reject. Its explicit flag/__debug__ check precedes project loading. The optimize0 external contract is coherent if root binds and uses that exact entry; it is not intrinsic protection in standalone bootstrap07. This does not repair the state overwrite.

## Other tests and their limits

A broader independent run observed15successful scenario adjudications, including the complete parsed stage→publish→public→ledger positive chain with5fake native writes and1literal append; lost create without another allocation; lost publish with one POST and exact recovery; perwrite-fsync OSError before POST; swallowed publication-summary OSError combined with intent drift or approval revocation; full raw sheet int/Boolean and float/int drift; direct append approval/intent/native-family/full-metadata races;31-second native refresh; postappend metadata drift; and lost append GET-only reconciliation.

That run later hit host ENOSPC while writing a small result file. Its final matrix receipt and full virtual rawcapture custody did not close. The15stored outcome records are explicitly **partial observations**, not a completed independent whole matrix or independent substitutes for the preparer's38normal cases. Two earlier all-filesystem positive attempts also hit ENOSPC and are excluded. All existing physical files from those attempts were retained in exact read-back custody before their own loose copies were retired. No unrelated cleanup occurred.

Only the decisive second state-race execution has a completed fresh virtual capture archive:145capture paths,42unique exact bodies,5119484original body bytes, all read back; archive SHA `9c6be6859b4a053dee4f6b56406f1875962a6dab1be9757f0ff08f0874deff9c`. The unarchived transient captures from the first state-race execution and the interrupted broader matrix are not represented as retained.

## Memory capture adapter: explicit fidelity boundary

Host space failures required a bounded adapter for large, read-only PRIVATE provider captures. Only these APIs change in fake executions:

- Eligible c/pl/live/native/ir.durable calls store the exact same canonical JSON bytes by content hash in memory.
- Path.read_bytes serves those exact stored bytes for captured keys.
- Path.mkdir represents the corresponding private rawcapture directories in memory.

The actual runtime intentions, approval, persisted state, checked source buffers and private pending certificate files retain real filesystem I/O. In particular, the failing saved-state replacement is the actual unmodified shared save_state/os.replace path. All source/approval/context predicates and actual parsed stage/publish/append fake-delegate decisions remain active. Capture hashes and JSON parsing use the original exact bytes; no loaded production path requires a stat predicate for those rawcaptures. No filesystem durability is inferred for memory captures. Their completed second state-race archive supplies exact retrievable bytes and closure separately from physical runtime case custody.

The adapter setup derives only the helper definitions from the pinned preparer harness, with own destinations and20MiB budget. Scenario fault mechanisms and outcome assertions are independently authored. This is deliberate operational falsification, not a fresh mathematical proof review or current live account observation.

## Disposition

**HOLD: concurrent-state preservation failure.** Source07 and the old runtime/scientific package were not edited. No CASE, operational authority, production runtime, upload, DOI reservation, ledger append, PR mutation or Git mutation was created. No publication-ready conclusion is issued. Root must retain its action hold until a revised package passes a new independent review.

Assigned review100%; overall sweep80%. See the manifest and readback receipts for exact evidence closure. The broader incomplete matrix remains incomplete; the fully reproduced preservation counterexample is sufficient for this HOLD.
