# PR66 native integration preparation

Preparation only. ROOT must review the final gate contract, code and exact
byte plan before executing anything. The operator has not been invoked.
The v1 planned documents contain intended future accepted wording; their
presence is not evidence that integration occurred.

The sources adapt the successful PR65 operator and independent readback, with
the actual PR66 schema verified separately: 25 regular `100644` attempt blobs;
26 incoming paths including the queue; `prior_upstream_report` present as an
object and `upstream_report` absent; three turn-1 ledger events; original
status `turns_used:1` and no `turn_limit`; original queue literal `1/5`.

The sequential ROOT phases are:

1. Finish the scientific/priority disposition and any separately reviewed v2
   packet/plan. Preserve all v1 files. Read every relevant actual review. Create
   the gate described by `GATE_SCHEMA.md`, binding current operators and selected
   prospective/operational byte plan. Obtain a new real other-writer freeze
   after that gate. Confirm native main equals remote main and the entire index
   is empty.
2. Run `python3 -E -B ROOT_integrate_attributed_prior_result_20261004.py merge`.
   The exact-head merge has two parents `[fresh native base, submitted head]`,
   imports the 25 original blobs unchanged and changes only the 10400033 queue
   row from the current native queue. It pushes ordinary `origin main`.
3. Run `python3 -E -B ROOT_readback_attributed_acceptance_20261004.py merge`.
   Review its actual PASS receipt and captured streams. This readback requires
   independent GitHub confirmation that the original head was merged.
4. Run `python3 -E -B ROOT_integrate_attributed_prior_result_20261004.py mirror`.
   The separate child commit changes exactly five paths: native
   `CURRENT_RESULT.md`, `CURRENT_PRIORITY_SPECIALIZATION.md`, `acceptance.json`,
   `state.json`, `history.jsonl`. It creates one present-day import event;
   original proof/status/ledger/source files are unchanged. Existing state
   entry text is retained, and all other entries and the exact history prefix
   are verified. The budget remains one substantive turn out of five.
5. ROOT separately corrects the accepted PR title and body using the selected
   plan's exact title and planned `PR_BODY.md`, preserving real command
   cwd/PID/argv/UTC and output streams. Do this only after the actual mirror
   receipt. The prepared native operator contains no GitHub write command.
6. Run `python3 -E -B ROOT_readback_attributed_acceptance_20261004.py acceptance`.
   It independently verifies the exact native and remote commits, both merge
   parents, original native/committed bodies and modes, five-file acceptance,
   current raw/SQL/wrapper typed pair, one real event, history/state preservation
   and exact accepted PR title/body. It writes only its own readback receipt.
7. ROOT reviews actual results, checkpoints the audit/progress separately,
   then explicitly releases the shared window. Neither source marks the program
   complete, edits progress, appends a DOI row or creates a release.

Run the commands from the repository root with absolute script paths or from
this directory. Subprocesses always use actual repository-root cwd. Every
future native or readback command receives separate retained stdout/stderr and
an actual PID/time/argv receipt. Repeated phase receipts fail closed rather than
replace earlier receipts. A failed operation retains partial state for ROOT to
inspect; it performs no reset, abort, stash, forced push, branch switch or
worktree creation.

Foreign tracked dirty files are saved as exact whole bytes and lstat modes,
with exact foreign index entries; their comparisons use byte equality, not
hash equality alone. All ownership exclusions are limited to the native
26 merge and five mirror paths. The audit/program paths are not silently
treated as writer-owned exclusions. The entire other-writer acknowledgement
body is constant, including across merge-to-mirror continuity.

Limits: these are prepared sources and static checks, not executed integration
or independent scientific clearance. The actual root gate, active writer
freeze and final priority v2 decision remain external prerequisites. Readback
can fail while GitHub is still reporting an older merge state; retain the
failed actual streams and inspect before a new attempt. This task performed no
new central proof search and contacted no external individual.
