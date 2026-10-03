# Adjacent source-only permission repair

The original source adversary found one narrow mandatory guard failure: the
old `st_mode & 0o777` verification accepts permission04444 while the publication
contract requires the complete permission0444. The stage producer's chmod0444
was correct; no existing candidate or mathematical defect was found.

This adjacent revision imports `stat` and uses `stat.S_IMODE(st_mode) == 0o444`
for every staged file and the manifest. All six literal preparation anchors
point consistently to `current_preparation_family_v2`. The exact original
preparation21+self and adversary193+self (including four intentional empty
control directories) are byte-bound dependencies left at their closed audit
locations. Their full source/capture/failure history is preserved without
recopying large forensic logs. SOURCE_REPAIR_DELTA.patch identifies every
builder change; REPAIR_INPUT_PINS.json binds both old closures and the new
source/delta. No new file was placed inside either closed parent.

Own separate finite controls retain genuine PID22572, exit0, complete source,
argv/cwd/UTC/stdout/stderr, and four actual filesystem objects. Full permissions
04444,02444,01444 are rejected and0444 is accepted. These are own predicate
diagnostics, not candidate execution or a whole-current PASS. Their special
bits remain in this source-preparation folder as concrete finite evidence;
future candidate copies receive chmod0444 and full permission verification.
Authoring-only inspection/copying ran genuinely as PID22454, exit0. Neither
run imported, compiled or executed the proposed builder or scientific helper.

Original SOURCE_PRECISION_QUALIFICATIONS SHA256
3529898445960cde70381bf99ea8287ec88a1003d8ca1cb4c3e0d088abdee570, INPUT_PINS,
overview and false/null ROOT drafts remain byte-exact. The science, eight flags,
four external genuine ROOT prerequisite schemas, original2/5,new0/audit0,
runtime/verdict nulls, source reading limits and full EP-653 UNSOLVED status
are unchanged. The original14 auxiliary bindings, including RESEARCH_LOG,
remain in force; separate ROOT_RESEARCH_LOG is outside these old pins. Native13
preparation observations remain dated. Fresh ROOT actual13 and current HEAD
must be issued after intervening publications are inspected.

A NEW different source adversary must review this exact closed revision before
ROOT executes it. A genuine future freeze and NEW whole-current source-first
review remain PENDING. No paper/DOI/tracker, native/canonical/shared/Git/remote
mutation, release or human outreach occurred.

Tool-only preparation failures/limits are disclosed separately from genuine
captures. An initial read guessed REPORT.md and VERDICT.json, which do not
exist; the read-only tool returned exit1 (chunkc1a8ac). The actual report and
verdict were then fully read as SOURCE_AUDIT_REPORT.md and FAMILY_VERDICT.json.
No PID/UTC was exposed for that failed read and none is invented. A subsequent
manifest-summary display accidentally included its large external dependency
array and was truncated; it was treated as truncated, not a complete displayed
manifest read. The authoring-only actual inspection parsed the full manifest
and individually checked all193 file bindings and exact directory membership.
