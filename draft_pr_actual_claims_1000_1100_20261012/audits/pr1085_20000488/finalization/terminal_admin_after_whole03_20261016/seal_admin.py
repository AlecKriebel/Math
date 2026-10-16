"""Check bounded custody and seal the completed terminal administration after whole03; no readiness grant."""
from pathlib import Path
import datetime,difflib,hashlib,io,json,zipfile
F=Path(__file__).resolve().parent;A=F.parents[1];K=A/'preprint_v1_0';P=A.parents[1];REPO=A.parents[2]
def sha(b):return hashlib.sha256(b).hexdigest()
def ident(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':sha(b)}
def pin(p,base):return {'path':str(p.relative_to(base)),**ident(p)}
def load(p):return json.loads(p.read_text())
def dump(p,o):p.write_text(json.dumps(o,indent=2)+'\n')
def need(ok,msg):
 if not ok:raise ValueError(msg)
def rows(o,pointer=''):
 if isinstance(o,dict):
  if isinstance(o.get('sha256'),str) and type(o.get('bytes',o.get('size'))) is int:yield pointer,o
  for k,v in o.items():yield from rows(v,pointer+'/'+str(k))
 elif isinstance(o,list):
  for i,v in enumerate(o):yield from rows(v,pointer+'/'+str(i))
def main():
 need(not (F/'SEAL.json').exists(),'already sealed')
 now=datetime.datetime.now(datetime.timezone.utc).isoformat()
 baseline=load(F/'BASELINE_INPUT_PINS.json')['files'];allowed=set(load(F/'AUTHORIZED_EXISTING_CHANGES.json')['files'])
 protected=[];changes=[]
 for r in baseline:
  expect={k:r[k] for k in ['bytes','sha256']};current=ident(A/r['path'])
  if r['path'] in allowed:
   before=F/'before'/r['path'];need(ident(before)==expect,'saved before changed '+r['path'])
   need(current!=expect,'allowed edit did not change '+r['path']);changes.append({'path':r['path'],'before':expect,'after':current,'before_custody':str(before.relative_to(A))})
  else:need(current==expect,'protected old audit changed '+r['path']);protected.append(r)
 need(len(changes)==6,'exact six edits')
 dump(F/'CHANGE_INVENTORY.json',{'utc':now,'files':changes})
 dump(F/'PROTECTED_UNCHANGED.json',{'utc':now,'all_rehashed':True,'files':protected})
 current=[pin(p,A) for p in sorted(A.rglob('*')) if p.is_file() and F not in p.parents]
 dump(F/'CURRENT_AUDIT_PINS.json',{'utc':now,'scope':'All current regular audit files outside this new post-whole03 terminal effort.','files':current})
 dump(F/'CURRENT_CANDIDATE_PINS.json',{'utc':now,'files':[pin(p,K) for p in sorted(K.rglob('*')) if p.is_file()]})
 external=[REPO/'zenodo_deposit_tool/zenodo.py']
 dump(F/'EXTERNAL_INPUT_PINS.json',{'utc':now,'scope':'Actual repository LOCAL native checker; hash-only. Its check branch returns before any network client.','files':[pin(p,REPO) for p in external]})
 core=['paper.pdf','paper.tex','STATUS.json','TERMINAL_ACCOUNTING.json','SOURCE_METADATA.json','check_math.py','build_pdf.py','build_archive.py','metadata_constants.py','.zenodo.json','metadata.json','zenodo-deposit.json','COPY_MAP.json','EXCLUSIONS.json','PREPARATION_INPUT_PINS.json','PREPARATION_REPORT.md','PREPARATION_SEAL.json','OUTPUT_PINS.json','FINAL_VERIFICATION.json','PROPOSED_PR_FRAMING.md','TERMINAL_INPUT_PINS.json','TERMINAL_COPY_MAP.json','TERMINAL_EXCLUSIONS.json','kit_common.py','CASE_ALIAS_REPAIR_ACCOUNTING.json','CASE_ALIAS_REPAIR_COPY_MAP.json']
 bm={r['path']:r for r in baseline}
 for n in core:need(ident(K/n)=={k:bm['preprint_v1_0/'+n][k] for k in ['bytes','sha256']},'core changed '+n)
 native=load(K/'.zenodo.json');need(native==load(K/'metadata.json')['metadata']==load(K/'zenodo-deposit.json')['metadata']==load(K/'UPLOAD_BINDINGS.json')['metadata']==load(F/'before/preprint_v1_0/UPLOAD_BINDINGS.json')['metadata'],'native metadata changed')
 dump(F/'CORE_PROTECTED_IDENTITIES.json',{'utc':now,'native_metadata_exact':True,'files':[pin(K/n,K) for n in core]})
 copies=[]
 for cmap,bpins,excl in [('COPY_MAP.json','PREPARATION_INPUT_PINS.json','EXCLUSIONS.json'),('TERMINAL_COPY_MAP.json','TERMINAL_INPUT_PINS.json','TERMINAL_EXCLUSIONS.json')]:
  frozen=load(K/bpins)['files'];fm={r['path']:r for r in frozen};selected=load(K/cmap)['files'];excluded=load(K/excl)['files']
  s=[r['source_relative_audit'] for r in selected];e=[r['path'] for r in excluded]
  need(len(fm)==len(frozen) and len(set(s))==len(s) and len(set(e))==len(e) and set(s).isdisjoint(e) and set(s+e)==set(fm),'old partition')
  for r in selected:
   src=A/r.get('source_snapshot_relative_audit',r['source_relative_audit']);dst=K/r['copy'];exp={k:r[k] for k in ['bytes','sha256']}
   need(ident(src)==ident(dst)==exp=={k:fm[r['source_relative_audit']][k] for k in ['bytes','sha256']} and src.read_bytes()==dst.read_bytes(),'old copy mismatch')
   copies.append({'map':cmap,'source_relative_program':str(src.relative_to(P)),'copy':r['copy'],**exp,'bytes_equal':True})
  for r in excluded:need({k:r[k] for k in ['bytes','sha256']}=={k:fm[r['path']][k] for k in ['bytes','sha256']} and bool(r['reason']),'old exclusion')
 for r in load(K/'CASE_ALIAS_REPAIR_COPY_MAP.json')['files']:
  src=P/r['source_relative_program'];dst=K/r['copy'];exp={k:r[k] for k in ['bytes','sha256']}
  need(ident(src)==ident(dst)==exp and src.read_bytes()==dst.read_bytes(),'repair source copy')
  copies.append({'map':'CASE_ALIAS_REPAIR_COPY_MAP.json',**r,'bytes_equal':True})
 for r in load(K/'CURRENT_TERMINAL_COPY_MAP_20261016.json')['files']:
  src=A/r.get('source_snapshot_relative_audit',r['source_relative_audit']);dst=K/r['copy'];exp={k:r[k] for k in ['bytes','sha256']}
  need(ident(src)==ident(dst)==exp and src.read_bytes()==dst.read_bytes(),'current source copy')
  copies.append({'map':'CURRENT_TERMINAL_COPY_MAP_20261016.json',**r,'bytes_equal':True})
 need((F/'CURRENT_TERMINAL_ACCOUNTING.json').read_bytes()==(K/'CURRENT_TERMINAL_ACCOUNTING_20261016.json').read_bytes(),'outer/kit current state differs')
 dump(F/'COPY_EQUALITY_RECHECK.json',{'utc':now,'passed':True,'preparation':{'inputs':192,'copies':66,'exclusions':126},'historical_terminal':{'inputs':375,'copies':52,'exclusions':323},'historical_repair_copies':6,'new_after_whole03_copies':18,'total_copies':len(copies),'files':copies})
 selected={r['source_relative_audit']:r for r in load(K/'CURRENT_TERMINAL_COPY_MAP_20261016.json')['files']};selection=[]
 for r in baseline:
  name=r['path']
  if name in selected:reason='Selected minimal exact authored whole03/root/before interface.';disposition='selected_exact_copy'
  elif name=='preprint_v1_0/pr1085_support_v1_0.zip':reason='Exact old ZIP preserved only in local before custody; excluded from all new public selection.';disposition='local_before_only'
  elif 'private' in name or 'private_sources' in name:reason='Third-party source body/extract/pixels or source retrieval custody: not copied.';disposition='not_selected'
  elif Path(name).suffix in ['.png','.pdf','.zip','.gz','.log']:reason='Existing primary paper already remains current, or body/pixels/runtime/raw operational derivative/historical archive: no duplicate added.';disposition='not_selected'
  elif name.startswith('preprint_v1_0/'):reason='Existing current/historical package material remains exact; no terminal duplication required.';disposition='not_selected'
  elif any(t in Path(name).name for t in ['COMMAND','SCRATCH','STDERR','STDOUT','COMPILE','RECEIPTS']):reason='Raw operational/command/scratch receipt retained locally; selected authored interfaces suffice.';disposition='not_selected'
  else:reason='Earlier exact custody or nonessential operational/reproduction interface retained in original local stage; no duplicate selected.';disposition='not_selected'
  selection.append({**r,'disposition':disposition,'reason':reason,**({'copy':selected[name]['copy']} if name in selected else {})})
 need(len(selection)==len(baseline) and len(selected)==18,'selection ledger partition')
 dump(F/'SELECTION_LEDGER.json',{'utc':now,'scope':'Individual disposition for every immediate baseline input. Public minimal copy map adds18; prior192/375 partitions and six repair copies are untouched.','selected':18,'not_selected_or_local_before_only':len(selection)-18,'files':selection})
 index={}
 for p in sorted(A.rglob('*')):
  if p.is_file() and (F not in p.parents or F/'before' in p.parents):
   i=ident(p);index.setdefault((i['bytes'],i['sha256']),[]).append(p)
 resolved=[];stages=[];retired=[]
 retirement_manifest=A/'reviews/package_03/FINAL_SCRATCH_PINS_BEFORE_CLEANUP.json'
 retirement_rows=load(retirement_manifest)['files'];retirement_index={r['path']:r for r in retirement_rows}
 retirement_receipt=A/'reviews/package_03/OWN_DERIVATIVE_CLEANUP.json';retirement=load(retirement_receipt)
 need(retirement.get('hash_pin_manifest_sha256')==ident(retirement_manifest)['sha256'] and retirement.get('regular_files_removed')==len(retirement_rows)==192 and retirement.get('bytes_removed')==sum(r['bytes'] for r in retirement_rows) and retirement.get('all_hashes_rechecked_before_removal') is True and retirement.get('own_unsealed_derivatives_only') is True and retirement.get('preexisting_files_removed')==0,'whole03 actual retirement provenance')
 stdout_witnesses={}
 for source in ['COMMAND_RECEIPTS.json','SUPPLEMENTAL_RECEIPTS.json','ATTEMPT_01_RECEIPTS.json']:
  for number,record in enumerate(load(A/'reviews/package_03'/source)):
   body=record.get('stdout','').encode();stdout_witnesses.setdefault((len(body),sha(body)),[]).append({'source':'reviews/package_03/'+source,'record_index':number,'field':'stdout','bytes':len(body),'sha256':sha(body)})
 for r in baseline:
  name=Path(r['path']).name
  if 'PINS' not in name and name not in ['MANIFEST.json','SUPPORT_MANIFEST.json','INPUT_FREEZE.json']:continue
  stage=(F/'before'/r['path']) if r['path'] in allowed else A/r['path'];count=0
  for pointer,row in rows(load(stage)):
   size=row.get('bytes',row.get('size'));matches=index.get((size,row['sha256']),[])
   hint=row.get('snapshot_path',row.get('path',row.get('file',pointer.split('/')[-1])))
   if not matches and isinstance(hint,str):
    for candidate in [REPO/hint,P/hint,stage.parent/hint]:
     candidate=candidate.resolve()
     if REPO in candidate.parents and candidate.is_file() and not candidate.is_symlink() and ident(candidate)=={'bytes':size,'sha256':row['sha256']}:
      matches.append(candidate)
   if not matches and r['path'] in ['reviews/package_03/SCRATCH_PINS_BEFORE_CLEANUP.json','reviews/package_03/FINAL_SCRATCH_PINS_BEFORE_CLEANUP.json']:
    need(isinstance(hint,str) and hint.startswith('scratch/') and retirement_index.get(hint)==row,'retired scratch exact original row')
    retired.append({'stage':r['path'],'json_pointer':pointer,'captured_locator':hint,'bytes':size,'sha256':row['sha256'],'disposition':'INTENTIONALLY_RETIRED_OWN_WHOLE03_DERIVATIVE_NOT_EXTANT_FILE_CLAIM','final_cleanup_manifest':'reviews/package_03/FINAL_SCRATCH_PINS_BEFORE_CLEANUP.json','final_cleanup_manifest_identity':ident(retirement_manifest),'actual_cleanup_receipt':'reviews/package_03/OWN_DERIVATIVE_CLEANUP.json','actual_cleanup_receipt_identity':ident(retirement_receipt),'original_row_equals_final_cleanup_row':True,'retained_actual_stdout_exact_witnesses':stdout_witnesses.get((size,row['sha256']),[]),'regenerated':False});count+=1
    continue
   need(bool(matches),'unresolved historical row '+r['path']+pointer+' '+str(row))
   choices=[A/hint,stage.parent/hint,stage.parent/'frozen'/hint]
   chosen=next((p for p in choices if p in matches),matches[0]);need(ident(chosen)=={'bytes':size,'sha256':row['sha256']},'historical rehash')
   resolved.append({'stage':r['path'],'json_pointer':pointer,'captured_locator':hint,'resolved_exact_path':str(chosen.relative_to(A)) if A in chosen.parents else str(chosen),'resolution_scope':'audit_local' if A in chosen.parents else 'individual_explicit_external_repository_locator','bytes':size,'sha256':row['sha256']});count+=1
  stages.append({'stage':r['path'],'stage_bytes':ident(stage),'records':count})
 for r in baseline:
  p=F/'before'/r['path'] if r['path'] in allowed else A/r['path'];need(ident(p)=={k:r[k] for k in ['bytes','sha256']},'baseline exact resolution')
  resolved.append({'stage':'post-whole03 terminal baseline','json_pointer':'/'+r['path'],'captured_locator':r['path'],'resolved_exact_path':str(p.relative_to(A)),**{k:r[k] for k in ['bytes','sha256']}})
 stages.append({'stage':'post-whole03 terminal baseline','records':len(baseline)})
 dump(F/'HISTORICAL_RETIRED_SCRATCH_ROWS.json',{'utc':now,'passed':True,'scope':'Every otherwise unavailable historical whole03 own-scratch row individually accounted by exact pre-cleanup/final-cleanup row equality and actual cleanup provenance. No claim these retired files remain extant. Exact stdout witnesses, where available, are rehashed in memory only; no body regenerated.','rows':retired,'records':len(retired),'distinct_retired_locators':len({r['captured_locator'] for r in retired})})
 dump(F/'HISTORICAL_STAGE_RESOLUTION.json',{'utc':now,'passed':True,'scope':'Every retained-live stage pin/manifest/input-freeze row and immediate terminal baseline resolves to individual exact current/saved-before bytes or explicit exact external locator. The separately inventoried intentional whole03 scratch retirements have actual cleanup provenance; no extant-byte claim for retired bodies. No stale pin rewritten and no omission claimed as replay.','records':len(resolved),'intentionally_retired_scratch_rows':len(retired),'total_accounted_rows':len(resolved)+len(retired),'stages':stages,'rows':resolved})
 seals=[]
 for rel in ['preprint_v1_0/PREPARATION_SEAL.json','reviews/ground_state_01/REVIEW_SEAL.json','reviews/hardy_absence_01/SEAL.json','reviews/priority_01/SEAL.json','reviews/package_01/FINAL_SEAL.json','reviews/package_02/SEAL.json','finalization/terminal_admin_20261016/SEAL.json','repairs/case_alias01/SEAL.json','reviews/package_03/SEAL.json']:
  p=A/rel;o=load(p);actual=sha((p.parent/'OUTPUT_PINS.json').read_bytes());need(o.get('output_pins_sha256',o.get('manifest_sha256'))==actual,'seal binding '+rel)
  seals.append({'seal':rel,'output_pins_sha256':actual,'passed':True})
 dump(F/'HISTORICAL_SEAL_BINDINGS.json',{'passed':True,'six_original_stages_plus_terminal_admin_repair_whole03':True,'seals':seals})
 diff=[]
 for n in ['README.md','verify_package.py','PAYLOAD_MEMBERS.txt','SUPPORT_MANIFEST.json','UPLOAD_BINDINGS.json']:
  diff.extend(difflib.unified_diff((F/'before/preprint_v1_0'/n).read_text().splitlines(keepends=True),(K/n).read_text().splitlines(keepends=True),fromfile='before/preprint_v1_0/'+n,tofile='after/preprint_v1_0/'+n))
 for n in ['CURRENT_TERMINAL_ACCOUNTING_20261016.json','CURRENT_TERMINAL_COPY_MAP_20261016.json']:
  diff.extend(difflib.unified_diff([], (K/n).read_text().splitlines(keepends=True),fromfile='/dev/null',tofile='after/preprint_v1_0/'+n))
 (F/'COMPLETE_CODE_PROSE_DIFF.patch').write_text(''.join(diff))
 controls=load(F/'CONTROL_SUMMARY.json');need(controls['passed'] and controls['commands']>=290 and controls['physical_alias_cases']==64,'controls incomplete')
 body=(K/'pr1085_support_v1_0.zip').read_bytes();manifest=load(K/'SUPPORT_MANIFEST.json')['files'];expected=sorted([r['path'] for r in manifest]+['SUPPORT_MANIFEST.json'])
 with zipfile.ZipFile(io.BytesIO(body)) as z:
  need(z.namelist()==expected and z.testzip() is None,'final ZIP exact order CRC')
  for i in z.infolist():need(z.read(i)==(K/i.filename).read_bytes(),'final ZIP payload')
 current=load(K/'CURRENT_TERMINAL_ACCOUNTING_20261016.json')
 need(current['whole_reviews_completed']==3 and current['latest_complete_whole_review']==3 and current['latest_actionable_P0_P1_P2_P3']==0 and current['root_terminal_integrity_adoption_required'] and not current['root_terminal_integrity_adopted'],'current terminal semantics')
 need(not (F/'scratch').exists() or not any((F/'scratch').iterdir()),'own scratch not settled')
 dump(F/'CURRENT_ARCHIVE_IDENTITY.json',{'utc':now,'closed_members':len(expected),**ident(K/'pr1085_support_v1_0.zip'),'paper_pdf':ident(K/'paper.pdf'),'support_manifest':ident(K/'SUPPORT_MANIFEST.json'),'external_binding':ident(K/'UPLOAD_BINDINGS.json')})
 report=f'''# PR1085 terminal administration after adopted whole03

Completed {now}; PR1085, problem20000488, audited head `5e23f0c801d23976830657d2eef2b32bdc7da05a`.

**Bounded current terminal administration passes. External ROOT final terminal integrity adoption is REQUIRED and unadopted.** Three NEW complete whole-package reviews are complete (minimum two). Root adopted the case-alias repair and the NEW complete whole03 ZERO-actionable P0–P3 result on the repaired candidate. No further complete whole review is currently required. This administration is not a new whole-package or mathematical review. Publication readiness, all-actionable-issues clearance, issues_resolved and published remain false; all services remain held after PR1032. AI assistance and unrefereed status, no human peer review and no formal certificate remain explicit.

## Evidence and substantive boundary

I read the COMPLETE whole03 report, frozen independent derivation, source-read ledger, verdict, review inventory/seal and root whole03 adoption. Root adoption records full proof/report/derivation/source-ledger/new-code reading, 509 input rehashes, 30 output rehashes, 11 primary interfaces and eight actual independent mathematical commands with complete normal/optimized JSON equality and six mutation rejections. Whole03 independently checked universal proof steps, all current interfaces, actually compiled both modes, and actually viewed every one of seven pages. These are retained review facts, not actions or new mathematical review performed by this terminal task.

The unchanged claims are every connected smooth nontrivial compact halfspace perturbation binding at every beta>0 in ambient2,3, weak-beta absence for every compact W1,infinity graph in ambient>=4, and the explicit smooth R4 h/100 graph with spectrum[-1,infinity) at beta1. Ambient/boundary dimension, beta-dependence, all-form H1 bridge, sign conventions, overhangs/holes, no all-coupling absence for one fixed nonzero graph, no higher-dimensional nongraph classification and no embedded-eigenvalue exclusion remain unchanged. Exner-Minakov planar theorem and exponential/Stokes mechanism credit, published HHRV A6 at theta1/4 with distinct older-version qualification, Frank-Laptev and capacity/Hardy credits remain exact. Priority, novelty, independent discovery and current worldwide openness remain UNKNOWN.

Paper PDF is still seven pages,97,501 bytes SHA256 `464de043ac6b723f3bd5c03dddb6efd1c0bfeb05b5209bb532006580b7aedc2d`; paper TeX remains SHA256 `c18a6ed12250dcee413e85f9a6297c525015396f151cdab8d89a6eb76938046d`. No PDF creation/compilation/render or new authoring marker occurred. Mathematical checker, PDF/archive builders, all four output-path guard calls and shared case-alias/physical-ancestor/path guards, metadata constants, source metadata, all four native bibliographic metadata objects and native descriptor remain exact. The operative verifier changes current terminal semantics only. Actual guard tests use an uninvoked compiler sentinel, not compilation.

## Current state and minimal changes

All {len(baseline)} preexisting regular audit inputs were frozen before mutation and all six permitted old targets saved as exact before bytes first. Exactly six old files changed: README, operative verifier, payload member list, support manifest, support ZIP and dependent external ZIP binding. The other {len(protected)} immediate baseline files remain exact. Atomic replacement avoided modifying shared historical inodes. All previous statuses, accounting, reports, review verdicts, manifests/pins and seals retain original bytes and captured-stage meaning; none was rewritten to assert a later outcome.

CURRENT_TERMINAL_ACCOUNTING_20261016.json is byte-identical to the separate outer CURRENT_TERMINAL_ACCOUNTING.json. It records three reviews/minimum two/latest03 ZERO and root adoption, adopted case repair, no further complete review currently required, external ROOT terminal integrity REQUIRED/unadopted and all false readiness/clearance/publication flags. README describes earlier pending records as historical snapshots. The operative verifier validates those captured stages first, then the separate current state, exact selected evidence identities, selected review-output pins, report/verdict/input-freeze seal bindings, frozen derivation, and root adoption semantics. The new summary reports the current three-review stage without treating administration as another review.

The full COMPLETE_CODE_PROSE_DIFF.patch contains every changed operative code/prose/allowlist/manifest/binding and complete new current accounting/map. No abbreviated code diff substitutes for source. CHANGE_INVENTORY, PROTECTED_UNCHANGED, core identities and full current audit/candidate pins substantiate the bounded changes. The initial archive build was followed by stricter copied-evidence historical-scope checks before final-byte controls; the earlier BUILD_RECEIPT/SUMMARY remain captured initial-build records. CURRENT_ARCHIVE_IDENTITY and final controls bind final bytes.

## Copy and stage custody

Original192 preparation inputs still partition into66 exact copies and126 individually hashed exclusions. Original375 terminal inputs still partition into52 exact copies and323 individual exclusions. All six case-repair copies remain exact. This administration adds18 minimal selected authored whole03/root/before interfaces, giving {len(copies)} exact source/copy pairs total. All were read as bytes and independently rehashed on both sides, with exact saved-before locators where old interfaces changed. SELECTION_LEDGER individually records every immediate baseline disposition. Bounded authored finite mathematical result receipts are selected; no public third-party body/source extract, pixel, runtime, general raw command/compiler stream, raw search or old ZIP was newly selected. The exact prior ZIP remains local before custody only. Historical executable copies retain their environment assumptions; no omitted code or original no-executable submission is represented as replayed.

HISTORICAL_STAGE_RESOLUTION resolves {len(resolved)} retained-live size/hash rows across {len(stages)} old pin/manifest/input-freeze stages plus immediate baseline to individual extant exact current/saved-before bytes or individual exact declared external repository locators. HISTORICAL_RETIRED_SCRATCH_ROWS separately accounts for {len(retired)} otherwise unavailable row occurrences ({len({r['captured_locator'] for r in retired})} distinct locators) from two whole03 own-scratch pre-cleanup inventories. Each exact original locator/size/hash equals its final cleanup row, bound by the actual cleanup receipt; these are intentionally retired derivatives, not retained-live obligations. Exact actual-stdout witnesses are hash-checked in memory where available; no old pixels/runtime/body is regenerated and no retired file is falsely called extant. All {len(resolved)+len(retired)} captured rows have an explicit checkable disposition. Explicit alternate identical-copy resolution never silently redirects a historic pin to different successor bytes. All {len(seals)} prior stage-seal/output-inventory bindings, including old terminal, repair and whole03, pass. Separate output inventory and terminal seal avoid a cycle; the archive excludes its own upload descriptors and self-hash-excludes only its manifest.

## Actual final-byte validation

The final suite executed {controls['commands']} actual commands: {controls['successes']} successes and {controls['expected_rejections']} expected nonzero rejections, all with intended outcomes. Full default verifier, shipped mathematical and strict native-binding JSON agree normally and under optimization. Default extraction reports external binding absent; required missing descriptors/bindings, stale attachment hashes and dangling/ordinary descriptor symlinks reject. Both actual archive writer builds match exact final bytes; an independently implemented writer was compared only AFTER its ZipFile closed. All {len(expected)} sorted members, fixed 2026-10-14 headers, Unix regular0644, deflate9, zero flags, empty extras/comments, payload and CRC pass.

Coherent current-accounting faults refresh outer manifests and reach the intended current review-count, identity, adoption/history, forbidden-promotion/stale-hold, ordered-hold, source-scope and paper-identity gates. Copied whole03 root/verdict/derivation mutations refresh copy maps and outer manifests; selected review-output mutations additionally refresh the review output pin, seal and root output binding. They still reject at the intended semantic guard. Copy membership/hash and exact-before-locator faults reject. The unchanged historical case-repair and root-hold semantics remain tested. Duplicate JSON and identical bootstrap member-list/manifest symlinks reject before JSON ingestion. The shipped four finite mathematical mutations reject both modes; these finite diagnostics do not replace analytic proofs.

All64 physical case/Unicode-normalization alias cases cover both spelling directions, fresh and absent intermediate descendants, all four writers and both Python modes with actual samefile/device-inode premises. Every forbidden path leaves inputs exact, directories/outputs absent and compiler sentinel uninvoked. Canonical/direct/hardlink/symlink/linked-parent and supplied-descriptor aliases, every PDF child hardlink and legitimate external noncompiler outputs also pass their intended outcomes. Static filesystem scope, with no concurrent hostile-race claim, is unchanged.

Actual repository zenodo_deposit_tool/zenodo.py check accepted the unchanged native {{metadata,files}} descriptor with exact final PDF/ZIP identities. Its local check branch returns before creating any network client. No credentials, deposit, publish, release, PR/tracker/queue, Git/index/branch mutation, service action, outreach, subagent or other-worker contact occurred. Two custody-sealing attempts failed correctly: the first audit-local index omitted an explicitly declared program-level report locator; the second treated deliberately retired whole03 scratch bodies as retained-live obligations. A third attempt completed custody validation but hit an extra-brace TypeError in report formatting. SEAL_ATTEMPT_01/02/03 preserve all three actual failures. The resolver now checks only individual declared repository candidates for otherwise unresolved live rows, separately validates exact historical scratch rows against actual cleanup provenance and formats their distinct-locator count correctly. No broad external scan, stale-pin rewrite, candidate change, control reclassification, body regeneration or seal occurred in those failed attempts. No new ENOSPC was observed; earlier actual review/repair harness and ENOSPC events remain exact in their historical records. Only this effort owned ignored scratch was cleaned, after individual hash/link inventories and immediate rechecks; no canonical or other worker cleanup occurred.

Final support ZIP: {len(body):,} bytes SHA256 `{sha(body)}`, {len(expected)} members. UPLOAD_BINDINGS selects it with exact unchanged bibliography. Current candidate contains {len([p for p in K.rglob('*') if p.is_file()])} regular files. Output records are sealed only after all commands/writes settled and scratch cleanup completed.

Delegated administrative completion estimate: **100%**. ROOT must independently read, replay and adopt final terminal integrity. Publication readiness and all-issues clearance are not self-promoted; the PR1032 service hold remains.
'''
 (F/'REPORT.md').write_text(report)
 with (F/'RESEARCH_LOG.md').open('a') as log:log.write('\n'+now+f' — Final-byte {controls["commands"]} commands pass including64 physical aliases; all{len(protected)} protected inputs, {len(copies)} copies, {len(resolved)} historical rows and {len(seals)} prior seals rehashed. Own scratch settled. Administrative completion100%; ROOT final integrity adoption remains REQUIRED/unadopted and service hold afterPR1032 remains.\n')
 final={'utc':now,'passed':True,'baseline_old_files':len(baseline),'allowed_existing_edits':6,'protected_unchanged':len(protected),'current_candidate_files':len([p for p in K.rglob('*') if p.is_file()]),'exact_copies':len(copies),'new_exact_copies':18,'historical_retained_live_rows':len(resolved),'historical_intentionally_retired_scratch_rows':len(retired),'historical_total_accounted_rows':len(resolved)+len(retired),'historical_stages':len(stages),'prior_seal_bindings':len(seals),'commands':controls['commands'],'physical_alias_cases':64,'normal_optimized_full_JSON_equal':True,'paper_math_pathguards_native_metadata_unchanged':True,'archive_members':len(expected),'archive_bytes':len(body),'archive_sha256':sha(body),'whole_reviews_completed':3,'minimum_whole_reviews':2,'latest_complete_whole_review':3,'latest_actionable_P0_P1_P2_P3':0,'further_complete_whole_review_currently_required':False,'root_terminal_integrity_adoption_required':True,'root_terminal_integrity_adopted':False,'publication_ready':False,'all_actionable_issues_resolved':False,'issues_resolved':False,'published':False,'services_held_after_pr':1032,'all_commands_writes_settled':True,'own_scratch_cleaned_after_pinning':True}
 dump(F/'FINAL_VERIFICATION.json',final)
 outputs=[pin(p,F) for p in sorted(F.rglob('*')) if p.is_file() and p.name not in ['OUTPUT_PINS.json','SEAL.json']]
 dump(F/'OUTPUT_PINS.json',{'utc':now,'scope':'Every retained post-whole03 terminal administration output including exact before custody and actual receipts; inventory itself and separate seal self-excluded. Scratch empty.','files':outputs})
 for r in outputs:need(ident(F/r['path'])=={k:r[k] for k in ['bytes','sha256']},'output changed during seal')
 dump(F/'SEAL.json',{'utc':now,'terminal':True,'kind':'BOUNDED_TERMINAL_ADMIN_AFTER_ADOPTED_WHOLE03_PASS_PENDING_EXTERNAL_ROOT_FINAL_INTEGRITY','pr':1085,'problem_id':20000488,'audited_head':'5e23f0c801d23976830657d2eef2b32bdc7da05a','output_records':len(outputs),'output_pins_bytes':(F/'OUTPUT_PINS.json').stat().st_size,'output_pins_sha256':sha((F/'OUTPUT_PINS.json').read_bytes()),'report_sha256':sha((F/'REPORT.md').read_bytes()),'complete_code_prose_diff_sha256':sha((F/'COMPLETE_CODE_PROSE_DIFF.patch').read_bytes()),'final_verification_sha256':sha((F/'FINAL_VERIFICATION.json').read_bytes()),'current_terminal_accounting_sha256':sha((F/'CURRENT_TERMINAL_ACCOUNTING.json').read_bytes()),'whole_reviews_completed':3,'minimum_whole_reviews':2,'latest_complete_whole_review':3,'latest_actionable_P0_P1_P2_P3':0,'further_complete_whole_review_currently_required':False,'root_terminal_integrity_adoption_required':True,'root_terminal_integrity_adopted':False,'publication_ready':False,'all_actionable_issues_resolved':False,'issues_resolved':False,'published':False,'services_held_after_pr':1032,'delegated_administrative_completion_percent':100})
 print(json.dumps(final,indent=2))
if __name__=='__main__':main()
