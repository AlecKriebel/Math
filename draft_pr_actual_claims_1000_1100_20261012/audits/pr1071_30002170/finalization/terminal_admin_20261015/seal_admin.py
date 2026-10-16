#!/usr/bin/env python3
"""Seal bounded terminal administrative evidence without self-reference."""
import difflib, hashlib, json, sys
sys.dont_write_bytecode = True
from datetime import datetime, timezone
from pathlib import Path
D=Path(__file__).resolve().parent
A=D.parents[1]
P=A/'NEWpreprint_v1_0'
ARCHIVE='PR1071_preprint_v1_0_support.zip'
def read(p):return json.loads(p.read_text())
def write(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
def pin(p,rel):
    b=p.read_bytes();return {'path':str(rel),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def need(ok,msg):
    if not ok:raise RuntimeError(msg)
def main():
    need(not (D/'SEAL.json').exists(),'Already sealed; inspect instead of overwriting')
    result=read(D/'FINAL_VERIFICATION.json');need(result['status']=='PASS','Verification not passed')
    # Full semantic code/prose diff; record arrays are separately rehashed/inventoried row by row.
    patch=[]
    for name in ['README.md','SUPPLEMENT.md','scripts/verify_package.py','UPLOAD_BINDINGS.json']:
        patch.extend(difflib.unified_diff((D/'before/NEWpreprint_v1_0'/name).read_text().splitlines(keepends=True),(P/name).read_text().splitlines(keepends=True),fromfile='before/NEWpreprint_v1_0/'+name,tofile='after/NEWpreprint_v1_0/'+name))
    for name in ['TERMINAL_STATUS.json','FINAL_ACCEPTANCE.md','WHOLE02_COPY_EXCLUSIONS.json']:
        patch.extend(difflib.unified_diff([], (P/name).read_text().splitlines(keepends=True),fromfile='/dev/null',tofile='after/NEWpreprint_v1_0/'+name))
    (D/'COMPLETE_SEMANTIC_CHANGES.patch').write_text(''.join(patch))
    current=[pin(f,f.relative_to(P)) for f in sorted(P.rglob('*')) if f.is_file() and not f.is_symlink()]
    write(D/'CURRENT_CANDIDATE_PINS.json',{'scope':'All current candidate regular files, including existing excluded preparation derivatives. Explicit PACKAGE_MANIFEST defines the distribution subset. Historical pin files are not rewritten.', 'records':current})
    audit=[pin(f,f.relative_to(A)) for f in sorted(A.rglob('*')) if f.is_file() and not f.is_symlink() and not f.is_relative_to(D)]
    write(D/'CURRENT_AUDIT_PINS.json',{'scope':'Every current regular audit file outside this terminal effort, with no duplicated source tree. Terminal effort files are independently sealed in OUTPUT_PINS.', 'records':audit})
    now=datetime.now(timezone.utc).isoformat()
    with (D/'RESEARCH_LOG.md').open('a') as f:
        f.write('\n'+now+': all actual clean controls, 2,788 historical rows, 116 source-equal copies, all protected outputs and local native uploader checks passed. Administrative execution completion estimate 100%. Root terminal adoption remains required; publication/disposition held after PR1032; priority UNKNOWN. No service or Git action occurred.\n')
    pdf=pin(P/'paper.pdf','paper.pdf');tex=pin(P/'paper.tex','paper.tex');archive=pin(P/ARCHIVE,ARCHIVE)
    report=f'''# PR1071 terminal administrative reconciliation

Completed {now}. Candidate: literal `NEWpreprint_v1_0`; PR head `fc37aa5169a0fe6adae0a254c9ee6c1531a2911f`, problem 30002170 / OWR-12013-003. This is **administrative reconciliation only**, after the root's adoption of a NEW complete clean whole02 review. It is AI-assisted and unrefereed. It is not a new mathematical review, human referee report, formal certificate or publication approval.

**Terminal administrative checks pass, with root integrity adoption required.** `TERMINAL_STATUS.json` records `READY_FOR_SUBMISSION_UNPUBLISHED_HELD_AFTER_1032`, two NEW whole reviews completed (minimum two), latest zero actionable P0, P1, P2 or P3 findings, and a mandatory external root terminal adoption. `publication_ready=false`, `issues_resolved=false` and `published=false` remain explicit: this worker does not confer release readiness or bypass the ordered service hold after PR1032.

The unchanged seven-page PDF is {pdf['bytes']:,} bytes, SHA256 `{pdf['sha256']}`. The unchanged paper source SHA256 is `{tex['sha256']}`. The current support ZIP is {archive['bytes']:,} bytes, 150 regular members, SHA256 `{archive['sha256']}`.

## Prior evidence read and preserved

Before candidate mutation I read the COMPLETE whole02 REPORT and VERDICT, `ROOT_WHOLE_PACKAGE_REVIEW_02.json`, the COMPLETE bounded repair report, current README/supplement/status/repair notes, all current support modules relevant to output and integrity, the native upload manifest/interface, and all copy/history/manifest/binding interfaces. Whole02 is a complete new mathematical/source/reproducibility/PDF/metadata/custody review, not a repetition of a hash-only check. The root adoption explicitly records the full report read, rehashing of 569 frozen inputs and 25 outputs, and independent mathematical-control replays with full normal/optimized JSON agreement.

The two-review history is preserved accurately. Whole01 found three P3 support defects; the bounded repair fixed writer output aliases, bootstrap regular-file checking and invalid active CFF citation. Fresh whole02 reconstructed the exact all-H lower-bound theorem, audited primary-source interfaces and priority qualifications, ran its new independent controls, actually compiled in both modes, and actually viewed all seven pages. It found zero actionable concerns. The root adopted that full evidence. This worker neither repeats nor expands those scientific claims.

Historical theorem and method priority, full novelty and worldwide current-open status remain UNKNOWN. The paper remains an attributed localized Gaussian-witness proof; Brownian optimum, smooth rate and established Fourier/Gaussian antecedents remain credited. Its canonical-source version qualifications, extensive-AI disclosure, unrefereed status and lack of formal certification are unchanged.

## Exact bounded changes and historical status accounting

`BASELINE_INPUT_PINS.json` hash-froze **597 immediate regular inputs** before mutation, without duplicating source bodies or runtimes. Exact before bytes of every permitted existing change were saved first. Exactly **eight existing files changed**: README, SUPPLEMENT, `scripts/verify_package.py`, INPUT_COPY_MAP, PACKAGE_MANIFEST, support ZIP, ZIP sidecar and UPLOAD_BINDINGS. All **589 other immediate inputs remain byte-exact**. `CHANGE_INVENTORY.json` gives complete before/after identities and new paths; `PROTECTED_UNCHANGED.json` rehashes every unaffected baseline record.

The paper TeX/PDF, all three native bibliographic objects, original finite checker and baseline, citation, path policy, archive/check/PDF entry scripts, submitted originals and every earlier report/seal/status retain exact bytes. The external native `publication/zenodo-deposit.json` also remains byte-exact. Its object equals the three reviewed metadata objects exactly, and its paths continue to select precisely the same paper PDF and same-named current ZIP. No invented DOI or publication claim is added.

`STATUS.json`, `CURRENT_STATUS.json`, REPAIR_NOTES and every dated preparation/repair report are preserved exactly. Their earlier pending-review fields are historical snapshots, explicitly superseded for current workflow accounting by the new TERMINAL_STATUS and FINAL_ACCEPTANCE records. The operative verifier still validates those old stage identities, then separately requires two completed reviews, latest zero findings, the exact root whole02 adoption and its selected output-manifest hash. It rejects administrative readiness promotion and bypass of the ordered hold. The external root's later integrity seal governs actual release readiness; this task cannot set that seal.

The only operative code addition is these explicit terminal-accounting guards in `verify_package.py`. The mathematics, canonical finite checker, writer policy and citation parser are unchanged. `COMPLETE_SEMANTIC_CHANGES.patch` contains the COMPLETE code/prose diff, new terminal records, individual exclusions and scalar binding changes. Large map/manifest arrays are separately fully inventoried and every row actually rehashed; they are not omitted from verification. The binding changes only current ZIP size/hash and manifest hash, preserving the PDF binding and existing descriptive fields.

## Distribution and exact captured-stage custody

The original **83 copy rows retain exact values and ordering**. Thirty-three source-equal copies were appended: six exact whole02-reviewed authored interface snapshots; twenty safe whole02 authored outputs; its OUTPUT_PINS and SEAL; root whole02 and bounded-repair adoptions; and the bounded-repair report/output manifest/seal. The 116 total source/copy pairs were independently rehashed and compared as bytes. Every changed historical locator uses its explicit exact `source_snapshot`, never a mutated current original.

`WHOLE02_COPY_EXCLUSIONS.json` individually identifies five unselected whole02 files: four raw compiler stdout/stderr streams and the private scratch configuration. The render directory is empty and has no image bytes. No full third-party source body, extracted publication text, pixel, runtime, private copied tree or old ZIP was selected. Whole02 source read/image hashes remain metadata only. Original whole01 exclusions remain unchanged and rehashed. The previous support ZIP and sidecar are retained locally in exact before custody, not redistributed. No omitted historical program/environment is claimed newly replayed.

`HISTORICAL_STAGE_RESOLUTION.json` resolves **all 2,788 captured rows** to exact current or saved before bytes: 597 immediate inputs; 204 original preparation inputs plus separately checked AGENTS; 92 preparation outputs; 492 pre-repair inputs; 34 repair outputs; 270 repaired current candidate rows; 480 repair-unchanged rows; 25 whole01 outputs; 25 whole02 outputs; and all 569 whole02-frozen inputs. No old pin record or seal is silently rewritten or relabeled. `COPY_EQUALITY_RECHECK.json`, CURRENT_CANDIDATE_PINS and CURRENT_AUDIT_PINS provide independent current inventories; terminal effort outputs have a separate external seal to avoid cycles.

## Actual clean reproduction and adverse administrative controls

The complete suite ran **99 actual commands**: 15 expected successes and 84 expected rejections, all with correct outcomes. One disposable clean extraction was used and automatically removed. Normal and optimized Python both passed documented default verification, checker replay, default temporary checker operation, deterministic archive rebuilding, strict present bindings and repeat verification. The unchanged original mathematical checker is replayed by the unchanged explicit full-result wrapper, ignoring only utc. Optimized original assertions are disabled; no claim that they remain active is made.

Strict controls reject required missing bindings, malformed JSON, corrupt PDF/ZIP/manifest hashes and missing archives in both modes. Citation controls with coherently updated outer manifests reject title drift, duplicate author and false software classification. Identical and malformed bootstrap-manifest symlinks reject before JSON parsing or archive writes. Terminal semantic controls with coherent outer manifest hashes reject fewer reviews, premature readiness, bypassed service hold, a nonzero latest finding and missing root adoption; all ten such mode/case combinations reject.

The unchanged fresh-output API was exercised on **749 protected targets per mode**: every current archived member, byte-exact disposable copies of all 597 immediate historical inputs, and both external binding/native-manifest interfaces. Direct existing destinations, hardlinks and symlinks yield **2,247 explicit pre-write rejections per mode**, 4,494 total. Canonical audit inodes were never used as destructive alias targets. All three actual writer entry points additionally reject current terminal/root/citation/manifest destinations, absent descendants of the frozen root, missing parents, linked parents and dangling leaves. PDF rejection cases name a nonexistent compiler and prove rejection before compiler invocation. The static path policy still makes no concurrent filesystem mutation or arbitrary malicious executable guarantee.

The ZIP has 150 regular entries, lexicographic order, ZIP_STORED compression, fixed 2026-10-14 timestamp and Unix mode 0644. Every header, payload and CRC was checked. A separately implemented ZIP was compared **after its ZipFile closed**, and matches exactly; both documented rebuilds match too. All 150 extracted files are unchanged after successful commands and restored negative controls. The actual repository uploader's entirely local `check` succeeds on the real native manifest, selecting exact current file identities. No network deposit operation was invoked.

No new actual PDF compilation, rendering or PDF marker occurred here because the paper source/PDF are unchanged and fresh whole02 already actually compiled both modes byte-exact and viewed every current page. No mathematical or bibliographic meaning changed. The complete raw per-command administrative outputs are in CONTROL_RECEIPTS; separate all-protected and semantic receipts summarize the interface controls. All current physical records were rehashed again after the suite.

Administrative execution completion estimate: **100%**. Root terminal integrity adoption remains required. The service/disposition cursor stays after PR1032. No Git/index/branch operation, Zenodo stage/publication, DOI, spreadsheet write, PR action, external communication or new subagent was performed.
'''
    (D/'REPORT.md').write_text(report)
    outputs=[pin(f,f.relative_to(D)) for f in sorted(D.rglob('*')) if f.is_file() and not f.is_symlink() and not f.is_relative_to(D/'_scratch') and f.name not in {'OUTPUT_PINS.json','SEAL.json'}]
    # Exclusions above apply only to this effort's own top-level seal names; before bytes may include namesake manifests.
    outputs=[pin(f,f.relative_to(D)) for f in sorted(D.rglob('*')) if f.is_file() and not f.is_symlink() and not f.is_relative_to(D/'_scratch') and f not in {D/'OUTPUT_PINS.json',D/'SEAL.json'}]
    write(D/'OUTPUT_PINS.json',{'utc':now,'scope':'Every terminal effort regular non-scratch file except this self-excluded manifest and separate seal; includes all exact before bytes, complete semantic patch, drivers, reports and actual receipts.', 'records':outputs})
    write(D/'SEAL.json',{'utc':now,'status':'TERMINAL_ADMIN_PASS_PENDING_ROOT_INTEGRITY_ADOPTION','output_pins':pin(D/'OUTPUT_PINS.json','OUTPUT_PINS.json'),'output_records':len(outputs),'current_candidate_records':len(current),'current_audit_records_outside_effort':len(audit),'archive':archive,'paper':pdf,'tex':tex,'whole_reviews_completed':2,'minimum_whole_reviews':2,'latest_actionable_P0_P1_P2_P3':0,'root_terminal_adoption_required':True,'publication_ready':False,'issues_resolved':False,'published':False,'services_held_after_pr':1032,'administrative_execution_completion_percent':100,'no_git_services_or_contact':True})
    # Rehash every sealed file after final output-manifest creation.
    for r in outputs:need(pin(D/r['path'],r['path'])==r,'Post-seal output drift')
    print(json.dumps(read(D/'SEAL.json'),indent=2))
if __name__=='__main__':main()
