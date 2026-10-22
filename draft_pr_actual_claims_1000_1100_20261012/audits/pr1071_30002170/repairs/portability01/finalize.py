"""Final package refresh, own scratch cleanup and noncircular terminal seal."""
import difflib,hashlib,json,os,shutil,sys,zipfile
sys.dont_write_bytecode=True
from datetime import datetime,timezone
from pathlib import Path
D=Path(__file__).resolve().parent;A=D.parents[1];P=A/'NEWpreprint_v1_0';S=D/'scratch';ZIP='PR1071_preprint_v1_0_support.zip'
def now():return datetime.now(timezone.utc).isoformat()
def need(ok,msg):
    if not ok:raise RuntimeError(msg)
def read(p):return json.loads(p.read_text())
def pin(p,n):
    b=p.read_bytes();return {'path':str(n),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def atomic(p,data):
    temp=p.with_name(p.name+'.finalize-tmp');need(not temp.exists(),'Existing temp');temp.write_bytes(data if isinstance(data,bytes) else data.encode());os.replace(temp,p)
def dump(p,obj):atomic(p,json.dumps(obj,indent=2)+'\n')
def cleanup(dest):
    rows=[];links=[]
    for p in sorted(S.rglob('*')):
        if p.is_symlink():links.append({'path':str(p.relative_to(S)),'link_target':os.readlink(p)})
        elif p.is_file():rows.append(pin(p,p.relative_to(S)))
    dump(dest,{'utc':now(),'scope':'Own derivative scratch only; all settled regular bytes hashed and own links recorded before cleanup. No canonical/preexisting path removed.','regular_files':rows,'symlinks':links})
    shutil.rmtree(S)
def refresh():
    initial=D/'initial_phase';need(not initial.exists(),'Refresh already performed');initial.mkdir()
    atomic(initial/'INTERMEDIATE_SUPPORT.zip',(P/ZIP).read_bytes())
    # Retain the genuine complete first-phase controls, not just an all-pass count.
    names=[p for p in D.iterdir() if p.name.startswith(('COMMANDS_','CONTROLS_','GUARDS_','RESULT_')) or p.name in ['FINAL_VERIFICATION.json','INDEPENDENT_CLOSED_ZIP.json','NATIVE_REPOSITORY_LOCAL_CHECK.json','CHANGE_INVENTORY.json','BUILD_SUMMARY.json']]
    for p in names:os.replace(p,initial/p.name)
    cleanup(initial/'SCRATCH_FINAL_PINS.json')
    m=read(P/'PACKAGE_MANIFEST.json');m['members']=[pin(P/r['path'],r['path']) for r in m['members']];dump(P/'PACKAGE_MANIFEST.json',m)
    temp=P/(ZIP+'.finalize-tmp')
    with zipfile.ZipFile(temp,'w',compression=zipfile.ZIP_STORED,allowZip64=False) as z:
        for name in sorted([r['path'] for r in m['members']]+['PACKAGE_MANIFEST.json']):
            i=zipfile.ZipInfo(name,(2026,10,14,0,0,0));i.create_system=3;i.external_attr=0o100644<<16;z.writestr(i,(P/name).read_bytes())
    os.replace(temp,P/ZIP);archive=pin(P/ZIP,ZIP)
    atomic(P/(ZIP+'.sha256'),archive['sha256']+'  '+ZIP+'\n')
    b=read(P/'UPLOAD_BINDINGS.json');b['archive']['bytes']=archive['bytes'];b['archive']['sha256']=archive['sha256'];b['manifest_sha256']=pin(P/'PACKAGE_MANIFEST.json','')['sha256'];dump(P/'UPLOAD_BINDINGS.json',b)
    dump(D/'BUILD_SUMMARY.json',{'utc':now(),'archive':archive,'members':len(m['members'])+1,'copy_rows':len(read(P/'INPUT_COPY_MAP.json')['copies']),'final_prose_reconciliation':'Replaced two unqualified old whole02/current-gate sentences in SUPPLEMENT with truthful dated-history/current-whole04 wording. Operative code unchanged. Complete first-pass controls retained separately in initial_phase.','no_old_archive_redistribution':True})
    S.mkdir()
    with zipfile.ZipFile(P/ZIP) as z:z.extractall(S/'CleanPackage')
    with (D/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+now()+' — 90%: final SUPPLEMENT reconciled two formerly unqualified whole02/gate sentences. All genuine initial full controls and intermediate ZIP kept locally in initial_phase; initial scratch hashed and only own derivatives removed. Code unchanged; final archive refreshed atomically. Full current-archive suites will repeat before sealing.\n')
    print(json.dumps(archive))
def seal():
    need(not (D/'SEAL.json').exists(),'Already sealed')
    v=read(D/'FINAL_VERIFICATION.json');need(v['status']=='PASS','Final controls incomplete')
    cleanup(D/'SCRATCH_FINAL_PINS.json')
    dump(D/'CLEANUP_RECEIPT.json',{'utc':now(),'removed_only':str(S),'scratch_pins':pin(D/'SCRATCH_FINAL_PINS.json','SCRATCH_FINAL_PINS.json'),'removed':not S.exists(),'canonical_or_preexisting_deletion':False})
    inventory=read(D/'CHANGE_INVENTORY.json');patch=[]
    for row in inventory['authorized_existing_changes']:
        if row['path'].endswith('.zip'):continue
        before=A/row['before_bytes_path_relative_to_audit'];after=A/row['path']
        patch.extend(difflib.unified_diff(before.read_text().splitlines(keepends=True),after.read_text().splitlines(keepends=True),fromfile='before/'+row['path'],tofile='after/'+row['path']))
    for n in ['PORTABILITY_REPAIR_STATUS.json','PORTABILITY_REPAIR_NOTES.md','PORTABILITY_SOURCE_EVIDENCE.json','PORTABILITY_COPY_EXCLUSIONS.json']:
        patch.extend(difflib.unified_diff([], (P/n).read_text().splitlines(keepends=True),fromfile='/dev/null',tofile='after/NEWpreprint_v1_0/'+n))
    atomic(D/'COMPLETE_CODE_AND_PROSE_CHANGES.patch',''.join(patch))
    candidate=[pin(p,p.relative_to(P)) for p in sorted(P.rglob('*')) if p.is_file() and not p.is_symlink()]
    audit=[pin(p,p.relative_to(A)) for p in sorted(A.rglob('*')) if p.is_file() and not p.is_symlink() and D not in p.parents]
    dump(D/'CURRENT_CANDIDATE_PINS.json',{'utc':now(),'records':candidate})
    dump(D/'CURRENT_AUDIT_PINS.json',{'utc':now(),'records':audit})
    need(len(audit)==763+16,'Current audit path count')
    with (D/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+now()+' — 100%: final current-archive four-suite validation, exact historical/copy/native/ZIP rehash, complete code/prose diff, own scratch hash/cleanup, full current inventories and bounded report complete. Separate terminal seal follows; root repair adoption then NEW COMPLETE whole04 remain mandatory. Readiness/issues-resolved/published false, hold1032, priority UNKNOWN.\n')
    need((D/'REPORT.md').is_file(),'Full report required before seal')
    outputs=[pin(p,p.relative_to(D)) for p in sorted(D.rglob('*')) if p.is_file() and not p.is_symlink() and p not in {D/'OUTPUT_PINS.json',D/'SEAL.json'}]
    # Exclude only the top-level manifest and seal, not similarly named history.
    need(all((D/r['path']).is_file() for r in outputs),'Output missing')
    stamp=now();dump(D/'OUTPUT_PINS.json',{'utc':stamp,'scope':'Every settled non-scratch regular effort output including full report, drivers, exact before bytes, local intermediate archive, both complete actual execution phases, failure record, history/copy/current inventories, and full operative code/prose diff. Only this top-level self-manifest and its separate terminal seal excluded.','records':outputs})
    seal={'utc':stamp,'status':'BOUNDED_WHOLE03_P3_01_PORTABILITY_REPAIR_PASS_PENDING_ROOT_ADOPTION_AND_NEW_COMPLETE_WHOLE04','pr':1071,'head':'fc37aa5169a0fe6adae0a254c9ee6c1531a2911f','output_pins':pin(D/'OUTPUT_PINS.json','OUTPUT_PINS.json'),'output_records':len(outputs),'current_candidate_records':len(candidate),'current_audit_records':len(audit),'baseline_inputs':763,'existing_changes':9,'protected_unchanged':754,'historical_rows':4346,'newer_prior_input_output_pin_rows':3158,'copy_pairs':140,'original128_rows_unchanged_ordered':True,'individual_omissions':72,'archive':pin(P/ZIP,ZIP),'paper':v['paper'],'tex':v['tex'],'final_current_support_commands':356,'final_current_native_local_commands':4,'final_guard_controls':5724,'initial_phase_support_commands_retained':356,'initial_phase_native_checks_retained':4,'three_complete_whole_reviews_finished':True,'minimum_whole_reviews':2,'whole03_finding_counts':{'P0':0,'P1':0,'P2':0,'P3':1},'bounded_repair_applied':['WHOLE03-P3-01'],'root_repair_adoption_required':True,'new_complete_whole_review_required':4,'new_complete_whole_review_completed':False,'root_terminal_adoption_required':True,'old_statuses_counters_ROOT_seals_exact':True,'publication_ready':False,'issues_resolved':False,'published':False,'services_held_after_pr':1032,'bounded_completion_percent':100,'no_actual_compile_render_PDF_marker':True,'no_external_contact_Git_index_branch_service_PR_queue_tracker_or_new_agent':True,'no_self_hash':True}
    dump(D/'SEAL.json',seal)
    for base,rr in [(D,outputs),(P,candidate),(A,audit)]:
        for r in rr:need(pin(base/r['path'],r['path'])==r,'Terminal identity drift '+r['path'])
    need(pin(D/'OUTPUT_PINS.json','OUTPUT_PINS.json')==seal['output_pins'],'Separate seal binding')
    print(json.dumps(seal,indent=2))
if __name__=='__main__':{'refresh':refresh,'seal':seal}[sys.argv[1]]()
