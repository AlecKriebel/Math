# Frozen native operator v1: source lifecycle FAIL

SOURCE-only FAIL for 51857 bytes, SHA256 9e9769eed24ca24f2b8502032d45709f3b9bac63e25f7f5b790ef10a35697602. Mandatory N1: load_inputs allows the three PROGRAM paths in native_acceptance, which does not call completion_inputs. A plan can therefore publish/install premature program completion metadata in the native phase. Mandatory N2: final_metadata checks only a nonempty PROGRAM intersection, allowing an inconsistent one-file completion update. The intended contract separates native14/selected repairs from complete program3 final metadata after actual native receipts.

In-memory admission probes reproduced both cases normally (actual PID 18122, 2026-10-07T18:35:10.371100+00:00) and with optimization (actual PID 18130, 2026-10-07T18:35:10.477174+00:00). The custody/archive/resource helpers are deliberately stubbed to isolate these member-family predicates. These are source boundary counterexamples, not actual plan, service or native-data claims. Candidate main/publish/install and provider/Git were never invoked.

The preparer agreed both repairs are mandatory and will preserve this v1 source/seal while preparing a distinct successor. Required source changes: forbid PROGRAM entirely in native_acceptance; require PROGRAM<=paths for final_metadata after its real completion prerequisite. Interim checkpoints may use own audit files. The exact repaired source needs a fresh independent review; this FAIL must not be reinterpreted as PASS.

Sealed by actual PID 18524 at 2026-10-07T18:35:43.551786+00:00. Bounded failure identification estimate100%; overall operator clearance incomplete. Original v1/seal untouched; no shared native/global/ref/index/service mutation. No actual postimages or publication approval.
