# Bounded concurrent GET prefetch: independent design assessment

UTC: 2026-10-17T22:33:23Z. Conceptual assessment100%; implementation/source
acceptance0%. No proposed new source has been reviewed or executed here.

**Conclusion:** a fresh composite GET observer can preserve the exact frozen
271-file logical packet and its per-invocation actual-native-body policy.
The design does not inherently require a logical packet rebuild. It DOES
require a separately pinned, fully reviewed operational extension and
explicit Root acceptance of each new callsite. Existing old source/logical
gates alone do not approve the new implementation.

This conclusion is conditional on every requirement below. It is not an
operational gate, candidate authorization, Root CAS, live-lock proof, sync
permission, terminal receipt or213 intake authority.

## Existing contracts actually inspected

I rehashed the unchanged old driver43897/16e5e3a15cc4cf34554aabf0b094b34996064c1abb05c008e26b47b00bf18ce8,
model33579/d8d749b9f45f24077668d60c916a431bf807f58df8189843f89c00026baca0f7,
primitives16405/5971428cd56b4fbbabb41a985f6a36599aea4f69e46fa048f88b971e405d9df9,
core4719/c71575a580c43fea8d302c978e0b6c340a16474779ffeb4671e77b967cf6e2ce,
and logical manifest160868/e33d6e10e015fbffcdd9a568dee8d2752fdc628d73acf04d8cbae1fec45ac200.

I read the complete relevant API, GetOnly, read_blob, NativeBodyProofs,
Seed/Runtime, parent_state, body_associations, verify_immutable, candidate,
lease_guard, reservation, accepted-verifications, actual-CAS, hold-CAS and
sync definitions and their relevant callsites. This is a mechanism analysis;
it is not another full-source audit or new execution of those definitions.

NativeBodyProofs deliberately accepts a generic observer. It keys its local
body cache by that observer's identity, calls the observer through GetOnly,
and validates the observer's actual_GET_origins against retained actual raw
stdout/stderr/receipt bodies and canonical blob contents. It does not require
the observer to be an instance of OriginalAPI. Thus a composite observer is
possible if its workers are newly owned actual-GET transports of that one
observer invocation. Merely copying origins from an unrelated API would
violate the policy despite passing some structural checks.

OriginalAPI already caches only immutable commit/tree/blob routes in memory
within its own instance. It does not cache ref/PR/compare routes. Its counters,
cache and journal numbering are not a supported concurrently shared object.

## Required observer ownership and cache boundary

1. Construct every OriginalAPI worker freshly inside one FastAPI lifetime,
   with mutateFalse and a fresh exclusive disjoint B journal. Do not accept
   preexisting workers, construction-writer API, old cache/origin maps or a
   previous FastAPI instance as input. Bind logical/admission/extension-gate
   pins and an explicit unique operation/run identity. Never reuse that
   observer for another admission, candidate, process, proof or restart.

2. Give each worker sole serial ownership of its OriginalAPI object.
   Stable OID partitions are sufficient; do not call one OriginalAPI from
   multiple threads and hope its counters or dictionary updates are safe.
   Use a hard worker/aggregate-call/byte/deadline budget. Account for both
   concurrent proof groups in the global dispatch cap. A dedicated control
   API counts toward the declared bound; alternatively use one already-owned
   worker serially after the prefetch barrier.

3. Prefetch only validated unique native blob OIDs enumerated from the fixed
   manifest. Source bytes may supply the desired OID and SHA256/length oracle,
   never the returned body or raw response. Every selected unique OID must
   actually be fetched in this FastAPI invocation; duplicate selected paths
   can share that same actual GET only inside this instance. No disk-cache,
   earlier candidate proof, other proof, other process or cross-run reuse.

4. Retain the exact OriginalAPI origin record and full raw receipt/stdout/
   stderr in that worker's journal. Independently validate route/host/repo,
   successful strict-typed exit, native SHA1, encoding/size/base64/body and
   desired SHA256/length before accepting it into the aggregate. The aggregate
   records those unchanged origins as delegates owned by this observer; it
   must not manufacture a claim that a separate wrapper performed another
   wire GET or replace raw bytes with a reserialized/synthetic envelope.

5. A barrier must join and successfully validate every prefetch result before
   exposing the selected cache to the unchanged verifier. Keep canonical
   response bytes and their pins; return fresh decoded objects, not shared
   mutable dictionaries. Freeze the completed selected-origin map before the
   verifier traverses it. The old NativeBodyProofs must then revalidate every
   retained raw origin unchanged through the FastAPI observer.

6. FastAPI must expose correctly associated fresh origins for ALL blob reads,
   not just prefetched selected bodies: current PR QUEUE, parent Main QUEUE,
   old progress/log preimages, and any new descendant QUEUE OID also pass
   through NativeBodyProofs. Nonprefetched bodies may use a serial owned
   control worker with the same full provenance validation and aggregation.
   Key caches by exact immutable route/OID, never by logical file path or a
   guessed current QUEUE body.

7. Keep ref/PR/compare requests uncached and perform them through an owned
   actual OriginalAPI every time. Never manufacture or suppress Main's
   before/after observations, bypass a stale parent, replace PR metadata,
   substitute a source body or prepopulate the old API/pool dictionaries.

8. A single error, timeout, cancellation, provenance failure, unknown GET
   outcome or gate/source change permanently fails the composite proof.
   Stop scheduling new work; cancel queued work and join/reap in-flight
   subprocesses under bounded cleanup. Preserve all actual journals,
   including completed late GETs. No fallback to another worker and no
   retry/restart within the same proof to turn partial success into PASS.
   Do not permit late workers to mutate a published aggregate or write after
   a terminal failure record.

## Explicit new operational authority required

Old Runtime.refresh authenticates the OLD driver/model/source closure and
existing Root gates. It does not authenticate a new wrapper file or new
candidate-copy code. A new separately Root-owned source acceptance must bind
the exact new code, unchanged old modules, unchanged logical manifest/gate,
independent review, lifetime/journal rules, and exact approved operation
families. The executing new source must actually recheck those pins/gates,
not just state them in a final report.

For a candidate-copy operation, verify the entire new function against old
candidate: preserve original writer-lock acquisition, both lease guards,
all refresh/local-state checks, OID/admission reservations, exact tree/commit
requests, OriginalAPI sequential mutateTrue POSTs, no retry, and post-proof
guards. The intended delta is the distinct read-only observer and its
prefetch. Keep the mutation-capable OriginalAPI inaccessible to FastAPI.

Because copied code is a new effectful source, supplement its per-effect
guard with new-code/source-gate checks before reservations and each immutable
POST, and around final proof/receipt effects. Old rt.refresh alone is
insufficient for that new authority boundary. No global monkeypatching of
e.API, NativeBodyProofs, read_blob, Runtime.refresh, protected predicates or
frozen source variables is acceptable.

Keep both full proofs independent: separate Seed/Runtime/FastAPI instances,
fresh worker journals, actual GETs and origin maps. Do not concurrently share
Runtime.pool, its mutable admission/refresh fields or worker objects. The
second proof may start after the actual commit POST is successfully recorded;
predicted candidate identity is not evidence that creation succeeded. The
Root pre-CAS review must verify distinct worker/origin sets, not just distinct
report filenames. Existing accepted_verifications checks two report paths
and semantics but does not by itself prove transport independence.

Record old protocol pins AND the new executed operational source/gate/run
bindings. Do not label a new candidate-copy as an exact invocation of the old
CLI merely because it imports the old Seed. Source-only acceptance of an
extension does not supersede the logical selection or allow a PR/ref writer.

## Hold/sync performance and unchanged guards

The old functions accept an observer. Passing a reviewed FastAPI to unchanged
sync is possible, but it is a new approved callsite: all actual-CAS checks,
coherent R observations, original stable lock, per-effect guards, prefix/
preimage checks, per-file installs, receipt/pointer checks and external Root
terminal requirement remain byte-exact.

There is another important bottleneck: old hold_CAS invokes main_closure
after the actual CAS. That closure authenticates every selected body between
before/after Main reads. A fresh slow OriginalAPI there can still take about
90seconds and fail when foreign Main moves, even after a successful CAS.
Leaving the hold function unchanged is compatible with a separately reviewed
caller supplying its own fresh-prefetched FastAPI observer. If the caller
keeps the original slow observer, the new plan does not remove this remaining
post-CAS concurrency failure. The observer choice for hold must therefore
be explicitly reviewed/accepted if used; do not silently assume sync's
prefetch accelerates an earlier hold invocation.

All worker threads must have joined before main-thread held-lock/signal
handling or verifier use; workers must not acquire or replace the original
lock. Prefetch before a lease does not prove a fresh Main lease. Actual
lease_guard and Root expected-SHA/forceFalse CAS remain decisive. Fast reads
increase the chance of finishing within a stable interval; no20second
performance bound or progress guarantee under arbitrary foreign writers
has been established. A stale CAS must still fail without override,
redispatch or coordination with the other chats.

## Logical rebuild boundary and carry-forward

A logical rebuild is unnecessary only while all271 target bytes, target
paths, exact preimages, five local proposals,53/37 memberships,last211,
protected nodes/QUEUE policies, old source11 closure and logical semantics
remain byte-exact. Parent/date/derived tree/candidate/new journals still
need the existing fresh explicit admission checks.

Adding the new wrapper to the CURRENT271 archive, changing any old source,
policy, selected bytes, scope, cache semantics, proof requirements or five
views WOULD require a new logical packet and exact review. The operational
extension cannot be smuggled in as approved parent-only parameterization.

Keeping newly reviewed operational source/acceptance/actual-run records
outside this checkpoint's frozen selection, with explicit natural-path
carry-forward at the next checkpoint, is consistent with the existing Root
operational-receipt pattern. Say so plainly: the current archive contains
the reviewed old source, while an additional separately accepted operation
was actually executed. Retain a finite public source/review/gate closure and
actual ownership/provenance metadata; private raw worker journals remain
retained locally and must not be exported wholesale.

## Mandatory implementation-review checks still outstanding

A fresh source review should execute the actual new observer/candidate-copy
under finite owned controls, covering worker limits and disjoint journals;
duplicate OID aliases; new observer fresh GETs; forbidden cross-proof origin
reuse; changed raw receipt/body/route/size; mutation-capability denial; cache
aliasing; mutable ref/PR/compare freshness; one-worker failure and late
completion; source/gate change before both POST boundaries; unchanged
one-use/lease refusal; and hold/sync observers with foreign movement and a
new descendant QUEUE OID. The completed proof must still pass the unchanged
full immutable verifier with real primitive-generated synthetic envelopes
in a clearly disclosed fixture. Fixture outcomes are not real GET/CAS/
lock/session evidence.

No conceptual objection remains under those requirements, but no concrete
new source or operational run is approved by this document. All work here
was filesystem reading, rehashing and own-folder documentation. No network,
Git, provider, PR, native mutation, Root gate, original-lock acquisition,
existing-five write, other-chat coordination or numerical advancement ran.
Actual accounting remains53/37,last211,cursor212; goal incomplete.
