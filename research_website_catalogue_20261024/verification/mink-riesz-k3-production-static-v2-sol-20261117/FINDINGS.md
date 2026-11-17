No open concrete finding remains in the bounded static review of exact V2
release_three.py, SHA256 83c48bca3761c9fbd49d8b29c42a113e10eebfa58b9793bad84c25644b48b3f9.
The original opaque-stdout finding is resolved for EVERY Git result, including
successful calls whose output later fails parsing. This applies to V2 only; the
original helper and its frozen UNFIT_FOR_EXECUTION finding remain unchanged.

At line 483 subprocess.run captures stdout/stderr as complete bytes. Line 484
now unconditionally base64-encodes each whole buffer into the event. Empty bytes
remain the exact empty string. The opaque parameter no longer suppresses any
stdout. The event precedes return-code rejection at line 486 and the return at
487, so callers cannot begin routing/tree/TREE parsing before the whole observed
stream is represented in evidence. Both command failure and success followed by
parser failure therefore retain the exact stream through this mechanism.

Before a journal exists, event() appends the whole record to TRACE (198–205),
which is included in readonly results (1265) or outer failure stderr (1274), and
is transferred to the fsynced journal at transaction entry (923). With LOG active,
the whole record is written, flushed and fsynced before event returns. This is a
static trace of ordinary success/exception paths. It is not an abrupt-process-
death/storage-fault, runtime, UI or publication certificate.

The passive byte correspondence check establishes that the entire 1279-line
source differs only by preparation-root relocation, new PLAN hash and this
unconditional stdout encoding. The entire PLAN differs only by preparation-root
relocation; TARGETS remains exact. No production helper was imported, executed,
parsed as code, compiled, help-run or tested. Static acceptance is not permission
to run any mode; distinct fresh root adoption/action authority remains required.
