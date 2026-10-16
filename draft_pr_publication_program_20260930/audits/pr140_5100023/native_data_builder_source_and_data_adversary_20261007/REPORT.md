# PR140 pure native data builder — independent V4 source review

Verdict: **FAIL (SOURCE_ONLY)**. The exact 42,460-byte source SHA256 is 9d40826d276397b8720f3ad3dfb9fbc3929d2a7ce4d7922a040fbf246f9c945a. This review neither evaluates a writer operator nor accepts an actual native installation. Seal recorder PID 26494, UTC 2026-10-07T18:48:08.105704+00:00.

## Mandatory correction C1

At line 333, the guard compares updatedRows with 1 and updatedColumns/updatedCells with 4 without exact integer type checks. Python treats True as equal to 1 and integral floats as equal to their integer counterparts. At line 325, the raw publication size guard has the adjacent floating-point equality gap.

Independent controls changed one pinned synthetic input at a time, recomputed its fixture request pins, and called the exact production build_fixture method. updatedRows=True, updatedRows=1.0, updatedColumns=4.0, updatedCells=4.0, and publication filesize converted to float were all accepted. Each output still truthfully had fixture=True and actual_receipt=False. These are structural-source counterexamples, not forged actual receipt or authority demonstrations. Numeric controls reproduced normally (PID 25812) and under -O (PID 25813).

Require exact type(value) is int before count/size/identity equality and range checks. Apply the repair to adjacent appropriate recid/count/member-size fields while keeping full input/manifest and authority bindings. Preserve the rejected source and actual request/postimages; create a distinct successor. The real prepared input values must be separately verified as valid typed integers during DATA review.

## Evidence and independent scope

The complete source and every one of the 18 preparer source-seal members were read and authenticated by PID 25461. The full immutable accepted backend kernel (25,994 bytes, SHA256 f72aee023f837bad092da58531c2cc069ce2cf094e835d090221107d20f07ab2) was read as text only. No backend module or command was executed.

My fixture design predates reading the preparer's fixture/control sources. It uses 41 independent small synthetic bodies totaling 16,245 bytes, including foreign catalog/state/assessment data, a quoted multiline CSV record with CRLF endings, raw history prefixes, a fourteen-cell QUEUE row and visibly nonpublication package/receipt bodies. It creates no plausible actual service authority.

Normal PID 24678 and optimized PID 24679 each rejected 35 adverse controls: request canonicality and duplicate keys, undeclared/missing bodies, body types and pins, fixture-to-actual API interchange, reviewer identity/hash/findings, publication metadata/files/MD5, tracker cells/B authorization, chronology/original merge head, policy, catalog duplicate/source/turn types, incomplete history, CSV score drift, and QUEUE result/duplicate target. Positive controls verified deterministic input purity, exact fourteen outputs, full readonly preservation, all foreign JSON entries and CSV physical records, QUEUE cells, history/README/log raw prefixes and target source/scores/holds conservation. The fixture's legacy import remained original2/5 with zero new proof-search turns and no original structured-ledger claim.

The accepted backend kernel computes review hashes from the complete source/prior pair, uses fixed source hashes and five-turn policy, and keeps status/turns/source-score fields in separate state/catalog outputs. The candidate's bounded overlay preserves these existing source and planning values. Its explicit literal claimed_solved/imported2 status is a dated adoption of authenticated author effort, not a replayed proof turn or recovered old structured event. No rank, cache, status, assess or sync command was invoked.

## Boundaries and next step

The distinct actual DATA request and fourteen frozen postimages exist, but this SOURCE seal does not accept their contents, normalized-role provenance, canonical repair selection or operation plan. The actual SOURCE path structurally requires the externally accepted full request SHA and fixed original source pair; local structural checks alone cannot authenticate fabricated ROOT/service receipts.

No actual builder API, native writer, provider action, Git/index/ref write, constructor, authority acquisition or external communication occurred. The only child with Git was a bounded readonly immutable blob read. Every instrumented control child exited zero and was reaped, its watchdog joined and process group absent. The initial direct normal run is preserved separately. A first custody-script attempt encountered an immutable-Git registry origin lacking a physical path and failed before any child; the successor read that origin correctly as a bounded immutable blob.

Research checkpoint: SOURCE review 100% complete; candidate preparation estimated 85% until C1 is repaired and independently re-reviewed; native adoption 0% by this review. No advancement past PR140 or completion-count change is authorized. Private controls are ignored and excluded from future public archive bytes. FINAL_MANIFEST lists their full pins for auditability, excludes itself and asserts no self-checksum.
