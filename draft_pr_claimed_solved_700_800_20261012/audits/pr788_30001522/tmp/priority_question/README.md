This is the authored independent priority-question family packet for PR788/problem30001522. Read REPORT.md and VERDICT.json first. It leaves priority unresolved and requests context addition C1. It is not a whole-preprint review, mathematical proof certificate, or permission to publish.

The worker was reused after PR786; fresh initialization failed before session start. The independent initial position and later independent report are frozen. No current peer/root priority conclusions were read before that report. There are zero new proof-search turns; original budget2/5 remains unchanged.

All48 originals and the three intake identity/gate/statement files are externally bound in INPUT_BINDINGS.json. Primary full bodies, extracted texts and one rendered source page live outside this flat packet; SOURCE_LEDGER.json specifies16 retrieved primary versions and actual read scope. Optional body replay checks32 source files plus the rendered page. Core verification reports external_body_replay=false honestly. None of these checks proves absence of an earlier result.

Use externally supplied manifest/checker SHA256 values from the parent-held receipt. Verify the checker hash before executing it. The manifest excludes only itself to avoid a cyclic pin; it binds the checker and every other flat authored file. Files and every root ancestor are opened without following symlinks; file reads are nonblocking and require single-link regular files.

Invocation (absolute paths and external pins supplied by caller):
python3 -B verify_packet.py --packet-root PACKET --intake-root INTAKE --manifest-sha256 MANIFEST_PIN --checker-sha256 CHECKER_PIN
Add --bodies-root BODY_SCRATCH to replay actual source hashes. Repeat with -O to check optimization independence.

Offline controls:
python3 -B negative_controls.py --packet-root PACKET --intake-root INTAKE --bodies-root BODY_SCRATCH --scratch-root OWNED_DISPOSABLE_SCRATCH --output OWNED_RESULT_FILE
Control copies are created and removed only below that explicitly supplied scratch folder. Output must be outside a final sealed packet unless intentionally resealing; the initial stored receipt refers to a provisional manifest. Final manifest/hash and final normal/-O baseline stdout are supplied externally, so no file asserts its own final self-bound receipt.

No filesystem-race adversary or malicious checker execution is claimed safe solely by self-inspection; caller-held pins and a stable read-only snapshot are the trust boundary. No native record, Git file, original, account, or publication was mutated. Scratch bodies are not submission artifacts.
