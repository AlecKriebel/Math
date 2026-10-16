# PR1071 bounded WHOLE03-P3-01 portability repair

Completed 16 October 2026 UTC. Candidate: literal `NEWpreprint_v1_0` at submitted
head `fc37aa5169a0fe6adae0a254c9ee6c1531a2911f`, problem30002170. This is a
bounded support repair, with finite adverse controls and custody verification.
It is not a complete whole-package review, a fresh mathematical/priority audit,
human review, formal certificate, or readiness/publication authority.

**WHOLE03-P3-01 is bounded-repaired. The final current archive passes all four
installed runtime/wrapper-mode suites.** Root must independently adopt this
repair, then obtain a **NEW COMPLETE whole04**, followed by root terminal
adoption. Three full reviews have finished (minimum two); whole03 found one
P3. This focused repair does not count as whole04 or clear that review gate.
`publication_ready=false`, `issues_resolved=false`, `published=false`; all
services remain held after PR1032. The new `PORTABILITY_REPAIR_STATUS.json`
governs current workflow. Every older CASE status, counter, review, terminal
record and ROOT seal retains its exact dated bytes and historical meaning.

Current support ZIP: **1,773,348 bytes**, **182 members**, SHA256
`11a16cbe77cc084cf1ac50f4396159ad7ddd3b301a888adbf5b38613d771dbeb`.
The unchanged seven-page PDF is93,113 bytes, SHA256
`33b90a4d846db58ea93efd453c13455fbeb3a29dcaa3e4cc49a68c0a8ebdff5b`.
Unchanged TeX is20,792 bytes, SHA256
`4ffbe0d65609213fd91aecf675661ff278e4e1bd5037db8836f1291f5bdc1d78`.
The original incoming1,597,595-byte support ZIP, SHA256
`807f4b259966b3d32a2cb9be40c52886658a445a95944123653aa5ce62559903`,
is retained exactly in local `before/` and excluded from the distribution.

## Finding and chosen support contract

I read the complete whole03 REPORT and `PYTHON311_PORTABILITY.json` before
choosing the repair, together with ROOT's whole03 adoption, current README,
SUPPLEMENT, entire original checker/baseline, operative checker/verifier,
path policy, archive/PDF entry points, copy/manifest/binding interfaces and
earlier custody-resolution mechanisms. This repair uses whole03/root evidence
as evidence of the original defect; it does not claim a new independent proof
or a repeat of whole03 source reading, rendering or actual PDF compilation.

The former README promised Python3.9+ while the wrapper required exact equality
of every non-utc JSON value. Installed CPython3.11.8 produced26 differing
covariance floats, maximum absolute difference2.220446049250313e-16. Whole03
and ROOT actually reproduced both documented failures. The exact rational,
normalization and sampled constant values agreed. These observations are
consistent with Python3.12's documented change to float summation; complete
causality is not asserted or needed for this reproduced contract defect.

The standard-library interfaces are now explicitly validated on **installed
CPython3.11.8 and CPython3.14.6**, on this binary64 platform. Other versions and
platforms are unvalidated; the blanket Python3.9+ promise is withdrawn. This
does not claim that other runtimes fail, nor that syntax compatibility alone
establishes support. The original checker and frozen expected JSON stay exact.

The new `result_guard` recursively visits every non-utc container and leaf:

- Every dict key set, list length, type, exact rational string, integer index,
  normalization identity, prose value and H sample input agrees exactly.
- All actual and expected floats must be finite. NaN and either infinity fail.
- Only covariance `direct`, `grouped`, `difference` outputs use
  `COVARIANCE_ABS_TOL=2^-49=1.7763568394002505e-15`, with zero relative tolerance.
- Only the numeric radical norm and `D_H`, `Pbar_f`, `Pbar_g`, `c_H` outputs use
  `DERIVED_REL_TOL=2^-47=7.105427357601002e-15`, with zero absolute tolerance.
  The exact predicate is
  `abs(actual-baseline)<=relative*max(abs(actual),abs(baseline))`.
- Every other float is exact. Positive norm, constant and covariance values
  are independently required positive. Each stored covariance residual equals
  `direct-grouped` exactly and has absolute value at most2^-49.

Per complete result, **258 leaves** are covered:115 exact nonfloat leaves,
34 exact floats (the sample H values),25 relative-policy derived floats and
84 absolute-policy covariance floats. Missing or extra containers/fields,
length/type changes and altered exact identities reject. Only the top-level
utc is ignored; no floating field is silently omitted. The exact area pairing,
Fourier conjugation, journal-version boundary and normalization guards remain.

The covariance envelope is eight binary64 epsilons, eight times the observed
maximum drift and below one tenth of the historical program's2e-14 absolute
identity threshold. The relative envelope is32 epsilons, a deliberately small
named diagnostic margin for elementary/libm rounding, checked at every frozen
sample on both named runtimes. These are explicit finite acceptance policies,
**not proved error bounds, interval enclosures, universal numerical accuracy
certificates, or guarantees for other H,m, libm implementations or platforms**.
Perturbations inside the stated policy may be accepted by design. The unchanged
analytic argument supplies the universal theorem.

The original normal subprocess retains its assertions. Its optimized subprocess
disables them; unconditional wrapper guards supply complete explicit
schema/exact/toleranced validation. Within each runtime the actual normal and
optimized non-utc JSON must additionally agree exactly. Receipt wording now
reports that contract honestly, rather than claiming exact baseline equality
across runtimes. The outer wrapper itself passes both with and without `-O`.

## Permitted changes, current gate and custody

Before candidate mutation, `BASELINE_INPUT_PINS.json` hash-froze **all763**
existing regular audit files. Exact before bytes of every one of the **nine**
necessary changed interfaces were saved: README, SUPPLEMENT, checker, verifier,
copy map, package manifest, ZIP, sidecar and upload binding. All replacements
of operative interfaces and generated assets were atomic. The **754** other
entry files remain byte-exact. Only **16** new candidate paths were added.
`CHANGE_INVENTORY.json` binds every before/current identity and new path;
`PROTECTED_UNCHANGED.json` enumerates all754 unchanged entry files.

The verifier continues to validate every historical preparation/current/
terminal/whole02/CASE record. It then requires the separate current portability
state: three completed full reviews/minimum two, whole03 one P3, this bounded
finding fixed, root repair adoption required, NEW COMPLETE whole04 incomplete
and required, root terminal adoption required, every readiness/publication flag
false and hold1032. It binds the exact whole03/root authored evidence and root
output-inventory hash. Coherent outer-manifest status mutations demonstrate
semantic enforcement beyond simple hash checking. README and SUPPLEMENT now
state this current gate and qualify old two-review/current-gate prose as dated
history. Historical JSON statuses and seals were never rewritten.

All **128** earlier source/copy rows keep their values and order. Twelve exact
authored copies are appended: seven prior interface snapshots plus complete
safe authored whole03 REPORT/verdict/output inventory/seal and ROOT adoption.
All **140** actual source/copy pairs are independently rehashed and byte-equal.
The distributed finding evidence clearly identifies those complete safe
authored records and their exact provenance. It adds no raw command stream,
third-party body/text/pixels, runtime, old ZIP or service payload.

`HISTORICAL_STAGE_RESOLUTION.json` preserves the values/order of all **2,788**
original terminal references and all **1,558** later terminal references, and
resolves each of the **4,346** rows to freshly checked exact current/before
bytes. Every original stage is also checked against its actual immutable
source array, rather than accepting an earlier all-pass banner.
`PRIOR_LATEST_INPUT_OUTPUT_PIN_RESOLUTION.json` additionally resolves **3,158**
case-repair/whole03 baseline, protected, current-candidate/current-audit, core,
output and external-input rows to exact bytes. Submitted nine-file identities
are checked from retained original snapshots; no new Git-object read is claimed.

All **72** individual omission rows across the four unchanged/extended ledgers
are rehashed to exact retained bytes:39 prior omissions plus33 new whole03/old
archive omissions. No omitted historical program is claimed newly replayed.
Old program/source bodies remain local; no outside communication was prepared
or initiated. `CURRENT_CANDIDATE_PINS.json` and `CURRENT_AUDIT_PINS.json` cover
every current regular candidate and all779 current audit files outside this
effort. The narrower explicit package manifest defines archive membership.

The actual `publication/zenodo-deposit.json` is byte-exact, as are bare metadata,
both metadata wrappers, scholarly citation and every bibliographic field. Native
metadata objects agree exactly and native selection remains unchanged paper.pdf
plus the same-named current ZIP. Included deposit.json remains historical
metadata wrapper. Only the required archive byte count/SHA and manifest SHA
changed in external UPLOAD_BINDINGS; all other binding fields stay exact.

## Actual final-current execution and adverse controls

Each of four final-current suites runs separately on installed3.11.8/3.14.6,
outer ordinary/`-O`. `COMMANDS_<tag>.json` retains every actual timestamp, exact
argv/cwd, exit code, expected outcome and full stdout/stderr;
`CONTROLS_<tag>.json` binds the actual checker receipt and runtime identity;
`GUARDS_<tag>.json` records each actual finite guard case.

The **356 final support commands** comprise **28 expected zero exits**, **324
expected rejections**, and **four deliberate compiler-sentinel exits91**. All
match their expected outcomes. Each wrapper actually runs the byte-exact
historical checker in normal and optimized subpasses. All eight computed final
result JSONs are retained as `RESULT_<tag>_<submode>.json`. Both runtime families
pass the complete contract; same-runtime non-utc result equality is exact.

The **5,724** direct result-guard cases (1,431 per suite) include removal and
null-type mutation of every non-utc field/list element, changed exact leaves,
NaN/+inf/-inf and gross mutation of every float, one-ulp changes of every exact
H sample input, extra root/nested fields, zero/negative constants, exact pairing
tozero, residual inconsistency inside the covariance envelope, both signed exact
absolute boundaries and adjacent rejected outside values, and both last-inside/
adjacent-outside relative boundaries. Six accepted controls per suite are the
two UTC exclusions and four intended within-boundary controls; the remaining
1,425 reject. Three additional source-fault controls per suite reject removed
conjugation, journal Eq30 boundary and convergence qualification. Actual wrapper
receipts retain their own deliberate conjugation/source/pairing controls too.

Both runtimes/modes exercise clean default absent bindings, actual canonical
strict-present bindings, explicitly required valid bindings, optional explicit
missing bindings, required missing bindings, malformed/corrupt PDF/ZIP/manifest
bindings, missing archives and binding symlinks. Current deterministic builds
match the final ZIP byte-for-byte. Fourteen coherent current-status mutations
per suite reject attempted readiness/publication promotion, review-count/gate
changes, root-adoption removal, finding erasure and hold changes.

Every writer is actually exercised on canonical/case-aliased internal paths,
nested aliases, absent multilevel internal parents, reversed script-root case,
parent traversal, existing files/directories, hardlinks, symlinks/dangling
leaves, linked parents and absent external parents. `Path.samefile` and actual
device/inode values establish the case-insensitive premise; these controls use
only the owned extraction, never canonical audit inodes. All reject before
output/compiler side effects and canaries stay exact. Fourteen reused-directory
child filename aliases reject before writes. Safe external aliases build valid
archives, while the positive external PDF preflight reaches the local executable
sentinel and exits91. **No actual PDF compiler, render or PDF marker runs.**

Identical/malformed bootstrap-manifest symlinks and manifest directories reject
before parsing or archive creation. An ordinary member symlink rejects too.
All182 extracted members are restored/rehashed exactly at the end of
every suite. These remain static local preflights; no concurrent-race or
arbitrary-executable guarantee is asserted.

`INDEPENDENT_CLOSED_ZIP.json` reconstructs the explicit final ZIP independently,
closes its ZipFile, then compares bytes. It checks every lexicographic member,
payload SHA/CRC, testzip result, central and raw local headers, local raw payload,
Unix create-system, fixed2026-10-14 timestamp, stored compression, regular0644
mode and terminal EOCD/comment. The comparison occurs after close.

`NATIVE_REPOSITORY_LOCAL_CHECK.json` records four actual normal/optimized
3.11/3.14 calls to the repository's actual
`/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py check`. Each passes and
selects the exact current PDF/ZIP. The inspected dispatch returns this local
manifest/file summary before state, token, client or network branches. The
word production in its summary identifies manifest environment; this command
performs no remote action. No staging, deposit, DOI or publication occurred.

## Failures, intermediate checkpoint and terminal handoff

After atomic repair but before the validation driver existed, ENOSPC blocked
both its creation and an initial small failure-record write. The failure was
reported to ROOT immediately. A later read command used the absent name
`package_03/INPUT_PINS.json`; the correct preserved file is FROZEN_INPUTS.json.
Both facts are in `FAILED_ATTEMPT_01.json` and the log, separate from passes.
No new full control had run at that failure. Read-only preliminary guard checks
did accept the baseline/preserved3.11 result. ROOT subsequently reported safe
byte-preserving storage recovery in its own effort; this worker did not remove
or modify any external source/runtime/preexisting derivative.

The first complete four-suite validation passed. A final prose check then
reconciled two SUPPLEMENT sentences which had still described the old whole02
gate without sufficient historical qualification. Operative code did not change.
The complete genuine first-phase commands/guards/results and four native checks
remain under `initial_phase/`, with the local exact intermediate ZIP and old
interface resolutions. The final archive was atomically refreshed and **all four
complete suites, custody/closed-ZIP checks and four native checks repeated** on
the final current bytes. First-phase evidence is never substituted for the final
results above. Its nine after pins individually resolve to exact current or
retained intermediate bytes; deterministic sidecar/binding reconstructions are
explicitly labeled and checked against actual captured first-phase hashes.

Both owned scratch phases are hashed after commands settle, then only own
derivatives are removed. No third-party source/runtime tree was copied for these controls.
`scratch/` was ignored immediately at effort creation. The complete code/prose
diff includes every changed existing text interface and all four new authored
current prose/status/evidence/exclusion interfaces. Exact copied history and
the binary archive have separate full byte inventories. A separate terminal
SEAL binds OUTPUT_PINS without self-hashing; inventories bind all current,
before/copy/history/input/output files. No further writes are pending at handoff.

Bounded repair completion estimate: **100%**. Mathematical acceptance and the
paper's exact scope remain unchanged: independent standard equal-H fBm, each
fixed H in(1/4,1), canonical iterated area, both complete uniform grids, every
T>0, n>=1 and every L2 grid estimator. Brownian optimum and smooth rate are prior;
Fourier/Gaussian antecedents retain credit. No endpoint, sharp constant, exact
limit, H-uniform, adaptive/nonuniform, unequal-H or correlated extension is
asserted. Historical/method priority, full novelty and worldwide current-open
status remain **UNKNOWN**; no journal-error/firstness/human-review claim is added.

No Git/index/branch, PR/queue/tracker/Zenodo service, external correspondence,
other-worker action or new agent was used. Parent coordination reported the
storage failure and eventual bounded handoff only. **ROOT repair adoption then
a NEW COMPLETE whole04 remain mandatory. All readiness/issues-resolved/
publication flags stay false, with services held after PR1032.**
