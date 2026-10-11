"""Self-only SOURCE closure; ROOT must capture this child externally after its exit."""
import datetime as dt, hashlib, json, os, stat, sys
from pathlib import Path, PurePosixPath
F=Path(__file__).absolute().parent; A=F.parent; R=A.parents[2]
def need(v,m):
    if not v: raise ValueError(m)
def sha(b): return hashlib.sha256(b).hexdigest()
def raw(p):
    need(not p.is_symlink() and all(not q.is_symlink() for q in p.parents) and stat.S_ISREG(p.stat().st_mode),'Regular nonsymlink member'); return p.read_bytes()
def clock(v):
    t=dt.datetime.fromisoformat(v.replace('Z','+00:00')); need(t.tzinfo is not None and t.utcoffset()==dt.timedelta(0),'AwareUTC'); return t
def dump(p,o):
    with p.open('xb') as h: h.write((json.dumps(o,indent=2,sort_keys=True,allow_nan=False)+'\n').encode()); h.flush(); os.fsync(h.fileno())
def checkrow(r):
    p=R/r['path']; b=raw(p); need(len(b)==r['bytes'] and sha(b)==r['sha256'] and stat.S_IMODE(p.stat().st_mode)==r['full_mode'],'Fixed dependency changed')
def main():
    need(not sys.flags.optimize and os.environ.get('PYTHONOPTIMIZE','') in ('','0'),'No optimized checks'); need(F.name=='current_preparation_family' and A.name=='pr47_2849' and R==Path('/Users/alec/Documents/Math'),'Exact SOURCE family'); need(not (F/'PREPARATION_MANIFEST.json').exists(),'Never reclose/replace SOURCE'); need(not (A/'reviewed_candidate').exists() and not (A/'reviewed_candidate').is_symlink(),'No production candidate')
    source=raw(Path(__file__).absolute()); status=json.loads(raw(F/'SOURCE_STATUS.json')); need(status['production_import_compile_or_execution'] is False and status['builder_executed'] is False and status['ROOT_operator_executed'] is False and status['actual_current_freeze'] is False and status['ROOT_approval'] is None and status['current_verdict'] is None,'SOURCE only; no acceptance')
    fixed=json.loads(raw(F/'STATIC_INPUT_BINDINGS.json'))
    for r in fixed['complete_fixed_member_reads']: checkrow(r)
    root=json.loads(raw(F/'ROOT_FIXED_EVIDENCE.json')); checkrow(root['manifest'])
    for r in root['members']+root['separate_actual_closure_members']: checkrow(r)
    snap=json.loads(raw(A/'snapshot_manifest.json'))
    for r in snap['files']:
        b=raw(F/'original_archive'/r['relative_path']); need(len(b)==r['bytes'] and sha(b)==r['sha256'],'All16 original archive bytes')
    for n in ['verify.py','verification.json','source_checksums.json','source_record.json','turns.json','prior_report.json','review/independent_checks.py','review/independent_results.json','review/submitted_verify.py','review/submitted_results.json']: need(raw(F/'operative_proposal'/n)==raw(F/'original_archive'/n),'Immutable operative data')
    for n in ['DRAFT_ROOT_READ_LEDGER.json','DRAFT_ROOT_SCIENCE_CARD.json']:
        o=json.loads(raw(F/n)); need(o['reading_completed'] is False and all(v is False for v in o['root_flags'].values()) and o['created_utc'] is None and o['preparation_manifest_sha256'] is None,'False/null ROOT read drafts')
    for n in ['DRAFT_ROOT_CURRENT_INPUT_PREIMAGES.json','DRAFT_ROOT_EVIDENCE_BINDINGS.json','DRAFT_ROOT_NEW_SOURCE_ADVERSARY_RECORD.json']:
        o=json.loads(raw(F/n)); need(o['approved_by_root'] is False and o['created_utc'] is None,'False/null ROOT approval drafts')
    need('ROOT_SCOPE_ACCEPTED_CORRECTED_UNRESOLVED_ONLY' not in raw(F/'DRAFT_ROOT_CURRENT_SCOPE_CERTIFICATE.md').decode(),'No draft acceptance sentinel')
    controls=json.loads(raw(F/'PRIVATE_CONTRACT_CONTROL_RESULTS_FINAL.json')); need(type(controls['assertions']) is int and controls['assertions']==4200 and controls['production_import_compile_or_execution'] is False and controls['production_builder_text_sha256']==sha(raw(F/'prepare_current_packet.py')) and controls['production_operator_text_sha256']==sha(raw(F/'capture_root_builder_operation.py')),'Current TEXT controls exact, no production run')
    expected={'SOURCE_INPUT_INSPECTION_ACTUAL_CAPTURE':1,'SOURCE_INPUT_INSPECTION_REPAIRED_ACTUAL_CAPTURE':1,'SOURCE_INPUT_INSPECTION_FINAL_ACTUAL_CAPTURE':1,'SOURCE_INPUT_INSPECTION_CORRECTED_ACTUAL_CAPTURE':1,'SOURCE_INPUT_INSPECTION_SUCCESS_ACTUAL_CAPTURE':0,'AUTHORING_ACTUAL_CAPTURE':0,'ROOT_CLOSED_INPUT_INSPECTION_ACTUAL_CAPTURE':0,'SOURCE_PRECISION_REPAIR_ACTUAL_CAPTURE':0,'PRIVATE_EXPECTED_NEGATIVE_ACTUAL_CAPTURE':1,'PRIVATE_CONTROLS_ACTUAL_CAPTURE':0,'PRIVATE_CONTROLS_FINAL_ACTUAL_CAPTURE':0}; actual=[]
    need({p.name for p in F.iterdir() if p.is_dir() and p.name.endswith('ACTUAL_CAPTURE')}==set(expected),'Exact own actual capture inventory')
    for n,exitcode in expected.items():
        d=F/n; need({p.name for p in d.iterdir()}=={'CAPTURE.json','PRELAUNCH.json','PRELAUNCH_SOURCE.py','PRELAUNCH_OPERATOR.py','stdout.bin','stderr.bin'},'Complete own six-member capture'); c=json.loads(raw(d/'CAPTURE.json')); pre=json.loads(raw(d/'PRELAUNCH.json'))
        need(c['schema']=='PR47_SOURCE_PREPARATION_ACTUAL_CAPTURE_v1' and c['actual_execution'] is True and c['completed'] is True and type(c['pid']) is int and c['pid']>0 and type(c['exit_code']) is int and c['exit_code']==exitcode and c['stdin_supplied'] is False and c['source_unchanged'] is True and c['operator_unchanged'] is True and c['production_import_compile_or_execution'] is False,'Genuine own success/failure capture')
        need(clock(c['started_utc'])<=clock(c['finished_utc'])<=dt.datetime.now(dt.timezone.utc) and c['cwd']==str(R) and len(c['argv'])==3 and c['argv'][:2]==['/usr/bin/python3','-B'] and Path(c['argv'][2]).parent==F,'Real capture scope/time/argv')
        need(sha(raw(d/'PRELAUNCH_SOURCE.py'))==c['source_sha256'] and sha(raw(d/'PRELAUNCH_OPERATOR.py'))==c['operator_sha256'],'Own prelaunch source/operator bytes')
        for k,v in pre.items(): need(c[k]==v if k!='schema' else v=='PR47_SOURCE_PREPARATION_PRELAUNCH_v1','Own prelaunch record')
        for ch in ['stdout','stderr']: b=raw(d/c[ch]['path']); need(len(b)==c[ch]['bytes'] and sha(b)==c[ch]['sha256'],'Own complete separate streams')
        need(bool(raw(d/'stderr.bin'))==(exitcode!=0),'Expected negative/failure remains failure'); actual.append({'directory':n,'complete_actual_capture':c,'current_source_matches_prelaunch':raw(F/Path(c['argv'][2]).name)==raw(d/'PRELAUNCH_SOURCE.py')})
    now=dt.datetime.now(dt.timezone.utc).isoformat(); (F/'CLOSURE_PRELAUNCH_SOURCE.py').write_bytes(source)
    with (F/'SOURCE_PREPARATION_RESEARCH_LOG.md').open('a') as h:
        h.write('\n'+now+' — Actual SOURCE-only self closure childPID'+str(os.getpid())+'. Preparation100%; actual freeze0%; new-discovery0%; full KP3.51 discovery0%. Six successful own captures plus four retained initial inspection failures and one intentional private negative; 4200 final private predicates. Builder/operator never imported, compiled or executed. Original301+self/separate5, closed cover143+self, gauge71+self and ROOT219+self unchanged. Original16/archive/operative immutable raw/source/turns/prior/helper/results byte-exact. Known realized degeneracy closes universal vanishing route; actual Floer control/bypass remains. All ROOT drafts false/null. Clean different SOURCE adversary, genuine ROOT post-closure approvals, current freeze, new whole-current review, final ROOT reconciliation and native acceptance pending. ROOT must capture this source-closure child externally only after child exit; no completed outer is invented here. No foreign PDF/text/OCR/pixels/cache/SQL/headers/cookies, Git/native/canonical/remote/outreach/paper/DOI/tracker write.\n'); h.flush(); os.fsync(h.fileno())
    fs=[]; ds=[]
    for p in sorted(F.rglob('*')):
        need(not p.is_symlink(),'No SOURCE symlinks'); n=p.relative_to(F).as_posix()
        if stat.S_ISREG(p.stat().st_mode): fs.append(p)
        else: need(p.is_dir(),'No SOURCE special members'); ds.append(n)
    need(set(ds)=={q.as_posix() for p in fs for q in PurePosixPath(p.relative_to(F).as_posix()).parents if str(q)!='.'},'No extra/empty SOURCE dirs'); rs=[]
    for p in fs: b=raw(p); p.chmod(0o444); need(stat.S_IMODE(p.stat().st_mode)==0o444,'SOURCE FULL0444'); rs.append({'path':p.relative_to(F).as_posix(),'bytes':len(b),'sha256':sha(b)})
    obj={'schema':'PR47_CURRENT_SOURCE_ONLY_CLOSURE_v1','status':'CLOSED_SOURCE_ONLY_CURRENT_PREPARATION','utc':now,'actual_closure_pid':os.getpid(),'self_excluded':['PREPARATION_MANIFEST.json'],'files_count':len(rs),'files':rs,'directories':sorted(ds),'all_full_modes0444':True,'original_scientific_files':16,'original_scoped_preparation301_plus_self_with_separate5':True,'original_turns_object_count':1,'turn_limit':5,'original_prior_literal':'null\n','upstream_prior_key_attributed_presence':'ABSENT','upstream_absent_fallback':{},'new_substantive_attempts':0,'audit_turns':0,'production_builder_sha256':sha(raw(F/'prepare_current_packet.py')),'production_operator_sha256':sha(raw(F/'capture_root_builder_operation.py')),'production_import_compile_or_execution':False,'ROOT_reading_or_approval':None,'actual_current_freeze_or_new_current_verdict':None,'source_preparation_completion_estimate_percent':100,'actual_current_freeze_completion_estimate_percent':0,'target_discovery_completion_estimate_percent':0,'complete_own_actual_captures':actual,'genuine_closed_ROOT_reproduction_manifest_sha256':root['manifest']['sha256'],'genuine_ROOT_current_approval_inferred':False,'foreign_bodies_copied':False,'separate_ROOT_actual_closure_capture_required_AFTER_this_child_exit':True,'new_different_clean_SOURCE_adversary_and_ROOT_full_read_required':True,'new_whole_current_adversary_and_final_ROOT_reconciliation_pending':True,'dated_private_mode_fixtures_frozen0444_after_actual_controls':True}
    dump(F/'PREPARATION_MANIFEST.json',obj); (F/'PREPARATION_MANIFEST.json').chmod(0o444)
    for r in rs: p=F/r['path']; b=raw(p); need(len(b)==r['bytes'] and sha(b)==r['sha256'] and stat.S_IMODE(p.stat().st_mode)==0o444,'Final closed SOURCE readback')
    need(raw(Path(__file__).absolute())==source,'Closer unchanged')
    print(json.dumps({'status':obj['status'],'files_count':len(rs),'directories':len(ds),'manifest_sha256':sha(raw(F/'PREPARATION_MANIFEST.json')),'builder_sha256':obj['production_builder_sha256'],'operator_sha256':obj['production_operator_sha256'],'production_executed':False,'ROOT_approval':None,'actual_current_freeze':False},sort_keys=True))
if __name__=='__main__': main()
