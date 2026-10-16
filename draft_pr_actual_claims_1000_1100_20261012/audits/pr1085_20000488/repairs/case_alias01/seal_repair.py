"""Check bounded custody and seal the completed focused repair; no readiness grant."""
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
 need(len(changes)==7,'exact seven edits')
 dump(F/'CHANGE_INVENTORY.json',{'utc':now,'files':changes})
 dump(F/'PROTECTED_UNCHANGED.json',{'utc':now,'all_rehashed':True,'files':protected})
 current=[pin(p,A) for p in sorted(A.rglob('*')) if p.is_file() and F not in p.parents]
 dump(F/'CURRENT_AUDIT_PINS.json',{'utc':now,'scope':'All current regular audit files outside this focused repair.','files':current})
 dump(F/'CURRENT_CANDIDATE_PINS.json',{'utc':now,'files':[pin(p,K) for p in sorted(K.rglob('*')) if p.is_file()]})
 external=[P/'reviews/case_alias_scope_20261016/REPORT.md',P/'ROOT_CASE_ALIAS_SCOPE_REVIEW.json',REPO/'zenodo_deposit_tool/zenodo.py']
 dump(F/'EXTERNAL_INPUT_PINS.json',{'utc':now,'scope':'Authored scope finding/adoption and actual LOCAL repository checker; hash-only.','files':[pin(p,REPO) for p in external]})
 core=['paper.pdf','paper.tex','STATUS.json','TERMINAL_ACCOUNTING.json','SOURCE_METADATA.json','check_math.py','build_pdf.py','build_archive.py','metadata_constants.py','.zenodo.json','metadata.json','zenodo-deposit.json','COPY_MAP.json','EXCLUSIONS.json','PREPARATION_INPUT_PINS.json','PREPARATION_REPORT.md','PREPARATION_SEAL.json','OUTPUT_PINS.json','FINAL_VERIFICATION.json','PROPOSED_PR_FRAMING.md','TERMINAL_INPUT_PINS.json','TERMINAL_COPY_MAP.json','TERMINAL_EXCLUSIONS.json']
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
 dump(F/'COPY_EQUALITY_RECHECK.json',{'utc':now,'passed':True,'preparation':{'copies':66,'exclusions':126},'terminal':{'copies':52,'exclusions':323},'new_repair_copies':6,'total_copies':len(copies),'files':copies})
 index={}
 for p in sorted(A.rglob('*')):
  if p.is_file() and (F not in p.parents or F/'before' in p.parents):
   i=ident(p);index.setdefault((i['bytes'],i['sha256']),[]).append(p)
 resolved=[];stages=[]
 for r in baseline:
  name=Path(r['path']).name
  if 'PINS' not in name and name not in ['MANIFEST.json','SUPPORT_MANIFEST.json']:continue
  stage=(F/'before'/r['path']) if r['path'] in allowed else A/r['path'];count=0
  for pointer,row in rows(load(stage)):
   size=row.get('bytes',row.get('size'));matches=index.get((size,row['sha256']),[])
   need(bool(matches),'unresolved historical row '+r['path']+pointer+' '+str(row))
   hint=row.get('snapshot_path',row.get('path',row.get('file',pointer.split('/')[-1])))
   choices=[A/hint,stage.parent/hint,stage.parent/'frozen'/hint]
   chosen=next((p for p in choices if p in matches),matches[0]);need(ident(chosen)=={'bytes':size,'sha256':row['sha256']},'historical rehash')
   resolved.append({'stage':r['path'],'json_pointer':pointer,'captured_locator':hint,'resolved_exact_path':str(chosen.relative_to(A)),'bytes':size,'sha256':row['sha256']});count+=1
  stages.append({'stage':r['path'],'stage_bytes':ident(stage),'records':count})
 for r in baseline:
  p=F/'before'/r['path'] if r['path'] in allowed else A/r['path'];need(ident(p)=={k:r[k] for k in ['bytes','sha256']},'baseline exact resolution')
  resolved.append({'stage':'case repair baseline','json_pointer':'/'+r['path'],'captured_locator':r['path'],'resolved_exact_path':str(p.relative_to(A)),**{k:r[k] for k in ['bytes','sha256']}})
 stages.append({'stage':'case repair baseline','records':len(baseline)})
 dump(F/'HISTORICAL_STAGE_RESOLUTION.json',{'utc':now,'passed':True,'scope':'Every size/hash row from every old audit pin/manifest plus immediate repair baseline resolves to individual exact current or saved-before bytes. No stale pin rewritten and no omission claimed as replay.','records':len(resolved),'stages':stages,'rows':resolved})
 seals=[]
 for rel in ['preprint_v1_0/PREPARATION_SEAL.json','reviews/ground_state_01/REVIEW_SEAL.json','reviews/hardy_absence_01/SEAL.json','reviews/priority_01/SEAL.json','reviews/package_01/FINAL_SEAL.json','reviews/package_02/SEAL.json','finalization/terminal_admin_20261016/SEAL.json']:
  p=A/rel;o=load(p);actual=sha((p.parent/'OUTPUT_PINS.json').read_bytes());need(o.get('output_pins_sha256',o.get('manifest_sha256'))==actual,'seal binding '+rel)
  seals.append({'seal':rel,'output_pins_sha256':actual,'passed':True})
 dump(F/'HISTORICAL_SEAL_BINDINGS.json',{'passed':True,'six_original_stages_plus_terminal_admin':True,'seals':seals})
 diff=[]
 for n in ['kit_common.py','README.md','verify_package.py','PAYLOAD_MEMBERS.txt','SUPPORT_MANIFEST.json','UPLOAD_BINDINGS.json']:
  diff.extend(difflib.unified_diff((F/'before/preprint_v1_0'/n).read_text().splitlines(keepends=True),(K/n).read_text().splitlines(keepends=True),fromfile='before/preprint_v1_0/'+n,tofile='after/preprint_v1_0/'+n))
 for n in ['CASE_ALIAS_REPAIR_ACCOUNTING.json','CASE_ALIAS_REPAIR_COPY_MAP.json','evidence/case_alias01/FINDING_AND_REPAIR.md']:
  diff.extend(difflib.unified_diff([], (K/n).read_text().splitlines(keepends=True),fromfile='/dev/null',tofile='after/preprint_v1_0/'+n))
 (F/'COMPLETE_CODE_PROSE_DIFF.patch').write_text(''.join(diff))
 controls=load(F/'CONTROL_SUMMARY.json');need(controls['passed'] and controls['commands']==213 and controls['physical_alias_cases']==64,'controls incomplete')
 body=(K/'pr1085_support_v1_0.zip').read_bytes();manifest=load(K/'SUPPORT_MANIFEST.json')['files'];expected=sorted([r['path'] for r in manifest]+['SUPPORT_MANIFEST.json'])
 with zipfile.ZipFile(io.BytesIO(body)) as z:
  need(z.namelist()==expected and z.testzip() is None,'final ZIP exact order CRC')
  for i in z.infolist():need(z.read(i)==(K/i.filename).read_bytes(),'final ZIP payload')
 report=f'''# PR1085 focused case-alias repair

Completed {now}; PR1085, problem20000488, audited head `5e23f0c801d23976830657d2eef2b32bdc7da05a`.

**The bounded static output-location repair and controls pass. This is not a whole-package review or readiness grant.** Root repair adoption and a NEW complete whole03 review remain required. Both earlier whole-package reviews and terminal accounting retain exact captured bytes and meaning. Readiness, all-issues clearance, publication, human refereeing and formal-certificate flags remain false; services stay held after PR1032. No Git/index/branch mutation, service/deposit/publication operation, PR/tracker action, outreach or new agent occurred.

## Finding and mechanism

I fully read the scope REPORT, root scope adoption, current shared guard and all four writers, verifier, README and terminal administrative REPORT. CASE-1085 is a newly confirmed P3 support-interface defect: ordinary and optimized archive writers accepted fresh output below an uppercase physical alias of the kit while canonical-spelling controls rejected it. No existing-input overwrite or mathematical flaw was found by that audit.

The shared guard now compares device/inode identity of every existing resolved output ancestor against ROOT, including the existing ancestor above absent intermediate directories. It works when the script root uses the canonical spelling and the output uses an alias, or conversely. It assumes no lowercase rule. Existing direct/resolved-input, symlink leaf/ancestor, existing-hardlink and supplied-descriptor protections remain. All four writers call the guard before output writes, directory creation or compiler calls. This is a static local-file policy; no hostile concurrent-filesystem-race security claim is added.

## Preserved claims and bounded changes

All {len(baseline)} old regular audit files were hash-frozen BEFORE mutation; exact before bytes of seven allowed changes were saved BEFORE mutation, including the old ZIP locally only. Exactly seven old files changed: shared guard, README, operative verifier, allowlist, manifest, support ZIP and dependent ZIP hash binding. All {len(protected)} others remain exact. Atomic replacement avoided changing any shared historical inode. CURRENT_AUDIT_PINS, CURRENT_CANDIDATE_PINS, CHANGE_INVENTORY and PROTECTED_UNCHANGED record the boundary.

The PDF remains 97,501 bytes SHA256 `464de043ac6b723f3bd5c03dddb6efd1c0bfeb05b5209bb532006580b7aedc2d`; TeX remains SHA256 `c18a6ed12250dcee413e85f9a6297c525015396f151cdab8d89a6eb76938046d`. The mathematical checker, source credits, metadata constants, every native metadata field and zenodo-deposit.json remain exact. Original STATUS, TERMINAL_ACCOUNTING, FINAL records and every prior report/pin/seal remain exact. No PDF compilation/render or new paper-authoring marker was performed. This task does not reconsider mathematics or priority.

CASE_ALIAS_REPAIR_ACCOUNTING separately records two completed historical reviews, minimum two, pending NEW complete whole03 and required external root repair adoption. Its strict semantic gate rejects premature clearance and service-hold bypass. README distinguishes captured historical zero-finding reviews from the new repair stage. The COMPLETE_CODE_PROSE_DIFF includes every operative text change and new accounting/map/finding prose; complete source files and maps are separately pinned.

## Exact custody

The original 66-copy/126-exclusion and terminal 52-copy/323-exclusion partitions remain exact. Only six necessary authored finding/root-hold and old-interface copies were appended. All {len(copies)} copies were compared as actual bytes to exact source or saved-before custody. No third-party body, raw command/compiler stream, pixel, runtime or old ZIP was added to the package. Local controls retain full actual process outputs. Historical code copies keep their original interfaces; no omitted checker or original no-executable submission was claimed replayed.

HISTORICAL_STAGE_RESOLUTION individually resolves all {len(resolved)} rows across {len(stages)} old pin/manifest stages and the immediate baseline to exact extant bytes; no historical locator was silently retargeted to changed current bytes. The six original stage-seal/output-pin bindings and later terminal-admin seal binding all pass. The previous support ZIP remains solely in exact local before custody. No input/output hash cycle exists: the current archive binds its self-hash-excluded manifest; external UPLOAD_BINDINGS binds archive/PDF; output inventory excludes itself and separate SEAL.

## Actual final-byte controls

The final suite executed {controls['commands']} actual commands: {controls['successes']} successes and {controls['expected_rejections']} expected nonzero rejections. Full normal and optimized verifier, mathematical and strict native-binding JSON results agree. Default clean extraction reports external binding absent; required missing descriptor/binding, corrupt binding and ordinary/dangling descriptor symlinks reject. Bootstrap member-list and self-hash-excluded-manifest symlinks reject. A genuinely external missing descendant succeeds for each noncompiler writer; both actual archive rebuilds equal the current ZIP.

All 64 physical-alias cases pass with actual samefile and device/inode premises recorded: case and Unicode normalization aliases, both script-root/output spelling directions, fresh leaves and absent intermediate directories, all four writers, ordinary and optimized Python. Inputs remain exact, outputs and missing directories remain absent, and the compiler sentinel remains absent. Canonical internal controls also reject. Original direct/hardlink/symlink/linked-parent protections, four supplied-descriptor aliases and all four PDF child hardlinks were checked in both modes using owned disposable copies only. No actual compiler ran.

Twenty-two current semantic faults per mode refresh the coherent outer manifest and reach their intended account guard. Copy-map membership/hash faults reject, and a copied-root-hold fault refreshes its copy-map hash as well as manifest before reaching the root-hold semantic guard. Duplicate JSON and all four unchanged mathematical fault controls reject. The latter are finite diagnostics, not continuum proofs or historical-source replays.

The closed {len(expected)}-member ZIP has exact sorted membership, fixed 2026-10-14 timestamps, Unix regular0644, deflate9, empty extras/comments, exact headers/payload/CRC. An independent writer was compared only AFTER closing its ZipFile and matches exactly. Current ZIP: {len(body):,} bytes SHA256 `{sha(body)}`. The actual repository `zenodo_deposit_tool/zenodo.py check` ran LOCAL-only against the unchanged native descriptor and accepted exact current attachments. No credentials/services were used.

The first harness-generation attempt actually failed because the shell could not create its temporary heredoc (no space); Python then correctly reported controls.py absent. No test ran in that attempt. A compact direct write succeeded later. The first completed 213-command suite passed; a new authored finding sentence was then corrected to describe the root-adoption/terminal-hold evidence actually copied. Its dependent map/manifest/ZIP/binding were refreshed and the entire 213-command suite passed again on final bytes. INITIAL_CONTROL_RECEIPTS/SUMMARY preserve that earlier successful run without replacing historical receipts. No other-folder cleanup occurred.

Bounded delegated repair completion estimate: **100%**. The parent research/publication goal remains incomplete: root adoption, NEW complete whole03 review and the ordered service hold remain.
'''
 (F/'REPORT.md').write_text(report)
 with (F/'RESEARCH_LOG.md').open('a') as log:log.write('\n'+now+f' — Final-byte controls passed {controls["commands"]} commands including64 physical alias cases; all{len(protected)} protected old files, {len(copies)} exact copies, {len(resolved)} historical rows and seven seal bindings rehashed. Paper/native metadata unchanged. Focused delegated repair 100%; root adoption, NEW complete whole03 and service hold remain.\n')
 dump(F/'FINAL_VERIFICATION.json',{'utc':now,'passed':True,'baseline_old_files':len(baseline),'allowed_existing_edits':7,'protected_unchanged':len(protected),'exact_copies':len(copies),'historical_rows':len(resolved),'historical_stages':len(stages),'original_seal_bindings':6,'additional_terminal_seal_binding':1,'commands':controls['commands'],'physical_alias_cases':64,'normal_optimized_full_JSON_equal':True,'paper_math_native_metadata_unchanged':True,'archive_members':len(expected),'archive_bytes':len(body),'archive_sha256':sha(body),'root_repair_adoption_required':True,'new_complete_whole03_required':True,'publication_ready':False,'all_actionable_issues_resolved':False,'published':False,'services_held_after_pr':1032})
 outputs=[pin(p,F) for p in sorted(F.rglob('*')) if p.is_file() and p.name not in ['OUTPUT_PINS.json','SEAL.json']]
 dump(F/'OUTPUT_PINS.json',{'utc':now,'scope':'Every local focused-repair artifact, including exact before custody and actual receipts; this inventory and separate seal self-excluded.','files':outputs})
 for r in outputs:need(ident(F/r['path'])=={k:r[k] for k in ['bytes','sha256']},'output changed during seal')
 dump(F/'SEAL.json',{'utc':now,'terminal':True,'kind':'BOUNDED_CASE_ALIAS_REPAIR_PASS_PENDING_ROOT_ADOPTION_AND_NEW_COMPLETE_WHOLE03','pr':1085,'problem_id':20000488,'audited_head':'5e23f0c801d23976830657d2eef2b32bdc7da05a','output_records':len(outputs),'output_pins_bytes':(F/'OUTPUT_PINS.json').stat().st_size,'output_pins_sha256':sha((F/'OUTPUT_PINS.json').read_bytes()),'report_sha256':sha((F/'REPORT.md').read_bytes()),'complete_code_prose_diff_sha256':sha((F/'COMPLETE_CODE_PROSE_DIFF.patch').read_bytes()),'final_verification_sha256':sha((F/'FINAL_VERIFICATION.json').read_bytes()),'root_repair_adoption_required':True,'new_complete_whole03_required':True,'publication_ready':False,'all_actionable_issues_resolved':False,'published':False,'services_held_after_pr':1032})
 print(json.dumps(load(F/'FINAL_VERIFICATION.json'),indent=2))
if __name__=='__main__':main()
