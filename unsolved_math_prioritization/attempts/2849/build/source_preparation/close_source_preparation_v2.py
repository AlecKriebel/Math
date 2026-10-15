"""ROOT-launchable self-only SOURCE V2 closure; no production execution."""
import argparse, datetime as dt, hashlib, json, os, stat, sys
from pathlib import Path, PurePosixPath
F=Path(__file__).absolute().parent; A=F.parent; R=A.parents[2]
def need(v,m):
    if not v: raise ValueError(m)
def sha(b): return hashlib.sha256(b).hexdigest()
def raw(p):
    need(not p.is_symlink() and all(not q.is_symlink() for q in p.parents) and stat.S_ISREG(p.stat().st_mode),'Regular nonsymlink member'); return p.read_bytes()
def clock(v):
    need(type(v) is str,'Typed time'); t=dt.datetime.fromisoformat(v.replace('Z','+00:00')); need(t.tzinfo is not None and t.utcoffset()==dt.timedelta(0),'AwareUTC'); return t
def dump(p,o):
    with p.open('xb') as h: h.write((json.dumps(o,indent=2,sort_keys=True,ensure_ascii=False,allow_nan=False)+'\n').encode()); h.flush(); os.fsync(h.fileno())
def checkrow(r):
    need(type(r) is dict and set(r)=={'path','bytes','sha256','full_mode'} and type(r['bytes']) is int and type(r['full_mode']) is int,'Typed pinned full-mode row')
    p=R/r['path']; b=raw(p); need(len(b)==r['bytes'] and sha(b)==r['sha256'] and stat.S_IMODE(p.stat().st_mode)==r['full_mode'],'Fixed dependency body/mode changed')
def scan():
    files={}; dirs=set()
    for p in sorted(F.rglob('*')):
        need(not p.is_symlink(),'No SOURCE symlinks'); n=p.relative_to(F).as_posix()
        if stat.S_ISREG(p.stat().st_mode): files[n]=p
        else: need(stat.S_ISDIR(p.stat().st_mode),'No SOURCE special members'); dirs.add(n)
    need(dirs=={q.as_posix() for n in files for q in PurePosixPath(n).parents if str(q)!='.'},'No extra/empty SOURCE directories'); return files,dirs
def main():
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--expected-report-sha256',required=True); args=parser.parse_args()
    need(__debug__ and not sys.flags.optimize and os.environ.get('PYTHONOPTIMIZE','') in ('','0'),'No optimized guards'); need(F.name=='current_preparation_family_v2' and A.name=='pr47_2849' and R==Path('/Users/alec/Documents/Math'),'Exact distinct V2 anchor'); need(sha(raw(F/'REPORT.md'))==args.expected_report_sha256,'ROOT read exact report'); need(not (F/'PREPARATION_MANIFEST.json').exists() and not (F/'PREPARATION_MANIFEST.json').is_symlink(),'Never reclose or replace SOURCE'); need(not (A/'reviewed_candidate').exists() and not (A/'reviewed_candidate').is_symlink(),'No production current candidate')
    source=raw(Path(__file__).absolute()); status=json.loads(raw(F/'SOURCE_STATUS.json')); need(status['operative_preparation_directory']==F.name and status['production_import_compile_or_execution'] is False and status['builder_executed'] is False and status['ROOT_operator_executed'] is False and status['actual_current_freeze'] is False and status['ROOT_approval'] is None and status['current_verdict'] is None,'SOURCE only false/null')
    fixed=json.loads(raw(F/'STATIC_INPUT_BINDINGS.json'))
    for r in fixed['complete_fixed_member_reads']: checkrow(r)
    root=json.loads(raw(F/'ROOT_FIXED_EVIDENCE.json')); checkrow(root['manifest'])
    for r in root['members']+root['separate_actual_closure_members']: checkrow(r)
    repair=json.loads(raw(F/'SOURCE_V1_REPAIR_BINDINGS.json'))
    for r in repair['complete_fixed_member_reads']+repair['external_ROOT_closure_and_readback_members']: checkrow(r)
    need(repair['old_SOURCE_V1_promoted'] is False and repair['ADVERSE_promoted_to_clean_PASS'] is False and repair['future_acceptance_approved'] is False,'ADVERSE and failed V1 unpromoted')
    snap=json.loads(raw(A/'snapshot_manifest.json'))
    for r in snap['files']:
        b=raw(F/'original_archive'/r['relative_path']); need(len(b)==r['bytes'] and sha(b)==r['sha256'],'All16 original archive bytes exact')
    for n in ['verify.py','verification.json','source_checksums.json','source_record.json','turns.json','prior_report.json','review/independent_checks.py','review/independent_results.json','review/submitted_verify.py','review/submitted_results.json']: need(raw(F/'operative_proposal'/n)==raw(F/'original_archive'/n),'Immutable operative data exact')
    for n in ['DRAFT_ROOT_READ_LEDGER.json','DRAFT_ROOT_SCIENCE_CARD.json']:
        o=json.loads(raw(F/n)); need(o['operative_preparation_directory']==F.name and o['reading_completed'] is False and all(v is False for v in o['root_flags'].values()) and o['created_utc'] is None and o['preparation_manifest_sha256'] is None,'False/null ROOT reading drafts')
    for n in ['DRAFT_ROOT_CURRENT_INPUT_PREIMAGES.json','DRAFT_ROOT_EVIDENCE_BINDINGS.json','DRAFT_ROOT_NEW_SOURCE_ADVERSARY_RECORD.json']:
        o=json.loads(raw(F/n)); need(o['approved_by_root'] is False and o['created_utc'] is None,'False/null ROOT approval drafts')
    need('ROOT_SCOPE_ACCEPTED_CORRECTED_UNRESOLVED_ONLY' not in raw(F/'DRAFT_ROOT_CURRENT_SCOPE_CERTIFICATE.md').decode(),'No draft ROOT scope acceptance sentinel')
    controls=json.loads(raw(F/'PRIVATE_CAPTURE_CLASS_CONTROL_RESULTS_FINAL.json')); need(type(controls['assertions']) is int and controls['assertions']==8006 and controls['genuine_helper_positives']==3 and controls['genuine_null_source_Git_positives']==33 and controls['capture_class_malformed_rejection_cases']==3542 and controls['all4096_actual_full_modes_checked'] is True and controls['production_import_compile_or_execution'] is False and controls['production_builder_text_sha256']==sha(raw(F/'prepare_current_packet.py')) and controls['production_operator_text_sha256']==sha(raw(F/'capture_root_builder_operation.py')),'Final private predicates bound to final production text only')
    expected={'AUTHORING_ACTUAL_CAPTURE':(17487,0),'PRIVATE_CONTROLS_ACTUAL_CAPTURE':(19224,0),'PRIVATE_EXPECTED_NEGATIVE_ACTUAL_CAPTURE':(19709,1),'FINAL_QUALIFICATION_ACTUAL_CAPTURE':(20983,0),'PRIVATE_CONTROLS_FINAL_ACTUAL_CAPTURE':(21205,1),'PRIVATE_CONTROLS_FINAL_V2_ACTUAL_CAPTURE':(21786,0),'READY_INPUT_INSPECTION_ACTUAL_CAPTURE':(27480,0),'FINAL_LINK_QUALIFICATION_ACTUAL_CAPTURE':(29286,0)}; actual=[]
    need({p.name for p in F.iterdir() if p.is_dir() and p.name.endswith('ACTUAL_CAPTURE')}==set(expected),'Exact own actual capture inventory')
    for n,(pid,exitcode) in expected.items():
        d=F/n; need({p.name for p in d.iterdir()}=={'CAPTURE.json','PRELAUNCH.json','PRELAUNCH_SOURCE.py','PRELAUNCH_OPERATOR.py','stdout.bin','stderr.bin'},'Complete own six-member actual capture'); c=json.loads(raw(d/'CAPTURE.json')); pre=json.loads(raw(d/'PRELAUNCH.json'))
        need(c['schema']=='PR47_SOURCE_V2_PREPARATION_ACTUAL_CAPTURE_v1' and c['actual_execution'] is True and c['completed'] is True and type(c['pid']) is int and c['pid']==pid and type(c['exit_code']) is int and c['exit_code']==exitcode and c['stdin_supplied'] is False and c['source_unchanged'] is True and c['operator_unchanged'] is True and c['production_import_compile_or_execution'] is False,'Genuine own completed success or retained failure')
        need(clock(c['started_utc'])<=clock(c['finished_utc'])<=dt.datetime.now(dt.timezone.utc) and c['cwd']==str(R) and len(c['argv'])==3 and c['argv'][:2]==['/usr/bin/python3','-B'] and Path(c['argv'][2]).parent==F,'Real actual capture argv/cwd/time')
        need(sha(raw(d/'PRELAUNCH_SOURCE.py'))==c['source_sha256'] and sha(raw(d/'PRELAUNCH_OPERATOR.py'))==c['operator_sha256'],'Literal own prelaunch source/operator')
        for k,v in pre.items(): need(c[k]==v if k!='schema' else v=='PR47_SOURCE_V2_PREPARATION_PRELAUNCH_v1','Prelaunch and post-exit record equality')
        for ch in ['stdout','stderr']:
            b=raw(d/c[ch]['path']); need(len(b)==c[ch]['bytes'] and sha(b)==c[ch]['sha256'],'Full own complete stdout/stderr')
        need(bool(raw(d/'stderr.bin'))==(exitcode!=0),'Expected negative and fixture-reuse failure remain failures'); actual.append({'directory':n,'complete_actual_capture':c,'current_private_source_matches_its_prelaunch':raw(Path(c['argv'][2]))==raw(d/'PRELAUNCH_SOURCE.py')})
    need(raw(F/'PRIVATE_CONTROLS_FINAL_V2_ACTUAL_CAPTURE/stderr.bin')==b'' and b'PermissionError' in raw(F/'PRIVATE_CONTROLS_FINAL_ACTUAL_CAPTURE/stderr.bin'),'Distinct corrected final fixture succeeds; failed fixture reuse preserved')
    with (F/'CLOSURE_PRELAUNCH_SOURCE.py').open('xb') as h:h.write(source);h.flush();os.fsync(h.fileno())
    now=dt.datetime.now(dt.timezone.utc).isoformat()
    with (F/'SOURCE_PREPARATION_RESEARCH_LOG.md').open('a') as h:
        h.write('\n'+now+' — Actual SOURCE V2 closing childPID '+str(os.getpid())+'. Assigned SOURCE preparation100%; actual current freeze0%; target discovery0%.8006 final independent private predicates, all33 genuine null Git/3 typed helper positives,3542 malformed/class/argv rejections,4096 actual full modes. Six successful own actual children; one intentional private negative and one genuine final fixture-reuse failure retained. Closed SOURCE V1 and closed ADVERSE unmodified and unpromoted. All16 original archive and immutable operative bytes exact; original1/5,new0,audit0. Production never imported, compiled or executed; ROOT drafts false/null. New different clean SOURCE adversary, genuine ROOT prerequisites, actual current freeze, whole-current audit, fresh13/currentHEAD reconciliation and native acceptance PENDING. ROOT must capture this closing child externally after actual exit and perform another separately captured full readback. No future completion/acceptance invented; no foreign bodies, outside communications, native/canonical/Git/remote/paper/DOI/tracker writes.\n');h.flush();os.fsync(h.fileno())
    files,dirs=scan(); rows=[]
    for n,p in sorted(files.items()):
        b=raw(p); p.chmod(0o444); need(stat.S_IMODE(p.stat().st_mode)==0o444,'Full0444 SOURCE files'); rows.append({'path':n,'bytes':len(b),'sha256':sha(b)})
    manifest={'schema':'PR47_CURRENT_SOURCE_ONLY_CLOSURE_v2','status':'CLOSED_SOURCE_ONLY_CURRENT_PREPARATION','operative_preparation_directory':F.name,'source_preparation_version':2,'utc':now,'actual_closure_pid':os.getpid(),'self_excluded':['PREPARATION_MANIFEST.json'],'files_count':len(rows),'files':rows,'directories':sorted(dirs),'all_full_modes0444':True,'production_builder_sha256':sha(raw(F/'prepare_current_packet.py')),'production_operator_sha256':sha(raw(F/'capture_root_builder_operation.py')),'closed_prior_SOURCE_V1_manifest_sha256':'cc29dc830448d8ddf232f3fc080e457c6a8a015428104bba2d4fc15f62f56631','closed_ADVERSE_SOURCE_manifest_sha256':'ed0aba6a7a42e752012399daed24d460e25108afd7b66c89ee1907473eb76a85','old_SOURCE_V1_promoted':False,'ADVERSE_promoted_to_clean_PASS':False,'complete_own_actual_captures':actual,'final_private_assertions':8006,'original_scientific_files':16,'original_substantive_attempts':1,'turn_limit':5,'new_substantive_attempts':0,'audit_turns':0,'full_problem_solved':False,'novelty_claimed':False,'production_import_compile_or_execution':False,'ROOT_reading_or_approval':None,'actual_current_freeze_or_new_current_verdict':None,'future_acceptance_approved':False,'source_preparation_completion_estimate_percent':100,'actual_current_freeze_completion_estimate_percent':0,'target_discovery_completion_estimate_percent':0,'new_different_clean_SOURCE_adversary_and_ROOT_full_read_required':True,'new_whole_current_adversary_and_final_ROOT_reconciliation_pending':True,'foreign_bodies_copied':False,'separate_ROOT_actual_closure_capture_required_AFTER_this_child_exit':True,'private_read_mode_rows_are_dated_preclosure_not_final_mode_authority':True}
    dump(F/'PREPARATION_MANIFEST.json',manifest); (F/'PREPARATION_MANIFEST.json').chmod(0o444)
    final_files,final_dirs=scan(); need(set(final_files)=={r['path'] for r in rows}|{'PREPARATION_MANIFEST.json'} and final_dirs==dirs,'Exact final self-only topology')
    for rr in rows:
        p=F/rr['path']; b=raw(p); need(len(b)==rr['bytes'] and sha(b)==rr['sha256'] and stat.S_IMODE(p.stat().st_mode)==0o444,'Every final SOURCE body and full mode')
    need(raw(Path(__file__).absolute())==source,'Closer unchanged'); print(json.dumps({'status':manifest['status'],'files_count':len(rows),'directories':len(dirs),'manifest_sha256':sha(raw(F/'PREPARATION_MANIFEST.json')),'builder_sha256':manifest['production_builder_sha256'],'operator_sha256':manifest['production_operator_sha256'],'production_executed':False,'ROOT_approval':None,'actual_current_freeze':False},sort_keys=True))
if __name__=='__main__': main()
