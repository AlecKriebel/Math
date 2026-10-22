"""Exact-source actual-B export and actual sequential-review applicability controls."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,traceback,importlib.util
HERE=Path(__file__).resolve().parent
CASE=HERE.parent.parent.parent
PUB=CASE/'publication'
RUNS=HERE/'probe_runs'
SNAP=HERE/'source_snapshot'
NAMES=['release_binding.py','append_verified_tracker.py','publish_preprint.py','verify_published_readonly.py']
SOURCE={n:(PUB/n).read_bytes() for n in NAMES}
def sha(raw):return hashlib.sha256(raw).hexdigest()
def pin(p,base):return {'path':p.relative_to(base).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())}
def dump(path,value):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(value,indent=2)+'\n')
def module(raw,name):
    ns={'__name__':'isolated_'+name,'__file__':str(SNAP/name)};exec(compile(raw,str(SNAP/name),'exec'),ns);return ns
rb=module(SOURCE['release_binding.py'],'release_binding.py')
old=module((HERE.parent/'source_snapshot_03/release_binding.py').read_bytes(),'old_release_binding.py')
def reject(fn):
    try:fn()
    except Exception as e:return {'error_type':type(e).__name__,'error':str(e)}
    raise AssertionError('Negative control accepted')
def make(label,log=True,extra=None):
    case=RUNS/label;r=case/'preprint';pub=case/'publication';r.mkdir(parents=True);pub.mkdir()
    for path in sorted((CASE/'preprint').iterdir()):
        if path.is_file():
            assert not path.is_symlink()
            (r/path.name).write_bytes(path.read_bytes())
    files=[pin(r/'manuscript.pdf',case)]
    if log:files.append(pin(r/'manuscript.log',case))
    if extra:
        target=case/extra;target.write_text('SYNTHETIC UNREVIEWED MARKER\n');files.append(pin(target,case))
    dump(pub/'PUBLIC_EXPORT_MANIFEST.json',{'schema':'pr209-public-export-manifest-v1','files':files})
    return case,r,pub,{'clear':{'public_export_manifest':pin(pub/'PUBLIC_EXPORT_MANIFEST.json',case)}}
RESULTS=[]
def test(label,fn):
    try:r={'label':label,'status':'PASS','detail':fn()}
    except Exception as e:r={'label':label,'status':'FAIL','error':repr(e),'traceback':traceback.format_exc()}
    RESULTS.append(r);dump(HERE/'PROBE_RESULTS.json',RESULTS);print(json.dumps(r),flush=True)
def actual_membership():
    freeze=json.loads((CASE/'whole_package_adversary_02/FROZEN_INPUTS.json').read_text())
    files=freeze['all_candidate_files']
    for row in files:assert pin(CASE/'preprint'/row['path'],CASE/'preprint')==row
    case,r,pub,ctx=make('actual_B')
    old_rejection=reject(lambda:old['public_exports'](r,pub,ctx))
    exports=rb['public_exports'](r,pub,ctx)
    log=next(x for x in files if x['path']=='manuscript.log')
    assert pin(r/'manuscript.log',r)==log and exports['preprint/manuscript.log']==(CASE/'preprint/manuscript.log').read_bytes()
    top=[pin(path,r) for path in sorted(r.iterdir()) if path.is_file()]
    dump(HERE/'ACTUAL_B_MEMBERSHIP.json',{'actual_frozen_files_verified':len(files),'actual_top_files':top,
        'compiler_log_frozen_pin':log,'old_exact_source_rejection':old_rejection,'new_exact_source_acceptance':True,
        'actual_freeze_pin':pin(CASE/'whole_package_adversary_02/FROZEN_INPUTS.json',CASE)})
    return {'all_actual_frozen_files_unchanged':len(files),'actual_top_file_count':len(top),'explicit_log_bytes':log['bytes'],'old_rejection_preserved':old_rejection}
def missing_log_pin():
    case,r,pub,ctx=make('missing_log_pin',False)
    return reject(lambda:rb['public_exports'](r,pub,ctx))
def extras():
    out={}
    for label,path in [('unreviewed','preprint/UNREVIEWED.txt'),('env','publication/.env')]:
        case,r,pub,ctx=make(label,True,path)
        out[label]=reject(lambda:rb['public_exports'](r,pub,ctx))
    return out
def changed_log():
    case,r,pub,ctx=make('changed_log');(r/'manuscript.log').write_bytes((r/'manuscript.log').read_bytes()+b'changed')
    return reject(lambda:rb['public_exports'](r,pub,ctx))
def symlink_log():
    case,r,pub,ctx=make('symlink_log');target=case/'saved_log';target.write_bytes((r/'manuscript.log').read_bytes());(r/'manuscript.log').unlink();(r/'manuscript.log').symlink_to(target)
    return reject(lambda:rb['public_exports'](r,pub,ctx))
def actual_review_chain():
    entries=[]
    for n in ['whole_package_adversary_01','whole_package_adversary_02']:
        folder=CASE/n;e={'assessment':pin(folder/'ASSESSMENT.json',CASE),'authored_manifest':pin(folder/'AUTHORED_MANIFEST.json',CASE),'supplements':[]}
        if n.endswith('_01'):
            e['supplements']=[pin(folder/'AUTHORED_MANIFEST_SUPPLEMENT_REPORT_CORRECTION.json',CASE)]
            e['resolution']=pin(CASE/'initial_review_20261016/ROOT_REVIEW01_RESOLUTION.json',CASE)
        entries.append(e)
    result=rb['review_chain'](CASE,entries,'whole-package',rb['current_core'](CASE/'preprint'))
    assert result==(2,1)
    dump(HERE/'ACTUAL_REVIEW_CHAIN.json',{'actual_entries':entries,'derived_reviews':result[0],'derived_exact_current_clean_reviews':result[1],
        'scope':'Pure parser validation of actual sealed reviews; no clearance or release action'})
    return {'actual_sequential_reviews':2,'actual_final_clean_current':1,'both_frozen_core_forms_validated':True}
def existing_workflow():
    spec=importlib.util.spec_from_file_location('owned_fixture',HERE.parent/'probes_01.py');p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
    p.RUNS=HERE/'workflow_run';p.SOURCE={n:(PUB/n).read_bytes() for n in p.NAMES};p.SNAP=SNAP
    f=p.Fixture('baseline');z=f.publish();t=f.append()
    f.module('verify_published_readonly.py').verify_publication_live(f.r,f.pub,f.ctx)
    f.module('append_verified_tracker.py').verify_tracker_live(f.r,f.pub,f.ctx,z)
    assert f.stages==f.publishes==f.appends==1;f.trace()
    return {'stage_calls':1,'publish_calls':1,'append_calls':1,'live_readbacks':True}
if __name__=='__main__':
    SNAP.mkdir()
    for n,raw in SOURCE.items():(SNAP/n).write_bytes(raw)
    dump(HERE/'EXACT_SOURCE_INPUTS.json',{'utc':datetime.now(timezone.utc).isoformat(),'case_completion_percent':65,'files':[pin(SNAP/n,HERE) for n in NAMES]})
    for label,fn in [('actual_B_top_membership',actual_membership),('missing_log_export_pin',missing_log_pin),
        ('UNREVIEWED_and_env_rejected',extras),('changed_log_rejected',changed_log),('symlink_log_rejected',symlink_log),
        ('actual_whole01_whole02_chain',actual_review_chain),('publication_tracker_workflow',existing_workflow)]:
        test(label,fn)
    raise SystemExit(0 if all(x['status']=='PASS' for x in RESULTS) else 1)
