"""ROOT-only self-only SOURCE closer. No production imports/native/Git/remote writes."""
import argparse, datetime as dt, hashlib, json, os, stat
from pathlib import Path, PurePosixPath
H=Path(__file__).absolute().parent;R=H.parents[3];NAME='PREPARATION_MANIFEST.json'
def need(v,m):
    if not v:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def parse(b):
    def pairs(v):
        d={}
        for k,x in v:need(k not in d,'Duplicate JSON key');d[k]=x
        return d
    return json.loads(b,object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
def name(n):
    need(type(n) is str and n and '\\' not in n and '\0' not in n,'Path');p=PurePosixPath(n);need(not p.is_absolute() and p.as_posix()==n and n!='.' and not {'.','..','.git','__pycache__'}.intersection(p.parts),'Canonical path');return n
def read(p):
    need(not p.is_symlink() and all(not x.is_symlink() for x in p.parents) and stat.S_ISREG(p.stat().st_mode),'Regular nonsymlink');return p.read_bytes()
def check(base,z,mode=False):
    p=base/name(z['path']);b=read(p);need(type(z['bytes']) is int and z['bytes']>=0 and len(b)==z['bytes'] and sha(b)==z['sha256'],'Whole body binding '+str(p))
    if mode:need(type(z['full_mode']) is int and stat.S_IMODE(p.stat().st_mode)==z['full_mode'],'Full external mode')
def tree():
    need(H.is_dir() and not H.is_symlink(),'Owned family');files={};dirs=set()
    for p in H.rglob('*'):
        n=name(p.relative_to(H).as_posix());need(not p.is_symlink() and (p.is_file() or p.is_dir()),'No special/symlink member');(files if p.is_file() else {}).update({n:p}) if p.is_file() else dirs.add(n)
    expected={p.as_posix() for n in files for p in PurePosixPath(n).parents if p.as_posix()!='.'};need(dirs==expected,'No unbound/empty directory');return files,dirs
def own_capture(folder,expected):
    need({p.name for p in folder.iterdir()}=={'CAPTURE.json','PRELAUNCH.json','PRELAUNCH_SOURCE.py','PRELAUNCH_OPERATOR.py','stdout.bin','stderr.bin'},'Exact private six-member capture');c=parse(read(folder/'CAPTURE.json'));pre=parse(read(folder/'PRELAUNCH.json'))
    need(c['schema']=='pr47-acceptance-source-preparation-private-actual-capture/v1' and c['production_import_compile_or_execution'] is False and c['actual_execution'] is True and c['completed'] is True and type(c['pid']) is int and c['pid']>0 and type(c['operator_pid']) is int and c['operator_pid']>0 and type(c['exit_code']) is int and c['exit_code']==expected and c['source_unchanged'] is True and c['operator_unchanged'] is True and c['stdin_supplied'] is False,'Complete actual private capture')
    need(c['argv']==pre['argv'] and c['cwd']==pre['cwd']==str(R) and c['argv'][:2]==['/usr/bin/python3','-B'] and len(c['argv'])==3,'Actual private argv/cwd');need(sha(read(folder/'PRELAUNCH_SOURCE.py'))==c['source_sha256']==pre['source_sha256'] and sha(read(folder/'PRELAUNCH_OPERATOR.py'))==c['operator_sha256']==pre['operator_sha256'],'Whole prelaunch sources')
    for channel in ['stdout','stderr']:need(set(c[channel])=={'path','bytes','sha256'} and c[channel]['path']==channel+'.bin','Exact complete stream');check(folder,c[channel])
    start=dt.datetime.fromisoformat(c['started_utc']);finish=dt.datetime.fromisoformat(c['finished_utc']);need(start.tzinfo is not None and start.utcoffset()==dt.timedelta(0) and finish.tzinfo is not None and finish.utcoffset()==dt.timedelta(0) and start<=finish<=dt.datetime.now(dt.timezone.utc),'Actual capture chronology')
    if expected==0:need(read(folder/'stderr.bin')==b'','Entire successful stderr')
    else:need(read(folder/'stderr.bin')!=b'','Retain real negative stderr')
def main():
    p=argparse.ArgumentParser();p.add_argument('--expected-report-sha256',required=True);a=p.parse_args();need(not (H/NAME).exists() and not (H/NAME).is_symlink(),'No existing closure');need(sha(read(H/'REPORT.md'))==a.expected_report_sha256,'ROOT supplied exact report pin')
    inputs=parse(read(H/'INPUT_BINDINGS.json'));need(inputs['actual_predecessor_PR46_completed'] is False and inputs['previous_mirror'] is None and inputs['previous_post'] is None and inputs['previous_root_post'] is None and inputs['future_native13_and_main_required'] is True,'Pending actual predecessor retained')
    for z in list(inputs['pins'].values())+inputs['external_input_rows']:check(R,z,True)
    need(len(inputs['external_input_rows'])==2933 and len({z['path'] for z in inputs['external_input_rows']})==2933,'Every external body individually bound')
    # The unfinished design reference is attributed and hash-bound, never accepted.
    check(R,inputs['unfinished_design_reference'],False)
    expected={'inspect_inputs_v1_actual_capture':0,'author_sources_v1_actual_capture':0,'private_controls_v1_actual_capture':1,'repair_sources_v2_actual_capture':0,'private_controls_v2_actual_capture':0,'expected_negative_actual_capture':1,'harden_sources_v3_actual_capture':0,'precision_sources_v4_actual_capture':0,'final_readback_v4_actual_capture':0}
    for n,code in expected.items():own_capture(H/n,code)
    result=parse(read(H/'PRIVATE_CONTROLS_RESULT.json'));need(result['assertions']==17361 and result['actual_full_modes']==4096 and result['genuine_null_Git_positive']==33 and result['genuine_typed_helper_positive']==3 and result['production_imported_compiled_executed'] is False,'Actual private controls, no production PASS')
    final=parse(read(H/'FINAL_READY_CHECK.json'));need(final['status']=='READY_SOURCE_ONLY_WAIT_ROOT_CLOSURE_AND_NEW_ADVERSARY' and final['production_imported_compiled_executed'] is False and final['actual_PR46_predecessor_completed'] is False,'Final SOURCE-only readback')
    files,dirs=tree();need(NAME not in files,'Literal self excluded');payload=[]
    for n,path in sorted(files.items()):b=read(path);payload.append({'path':n,'bytes':len(b),'sha256':sha(b)})
    for row in payload:check(H,row)
    again,dd=tree();need(set(again)==set(files) and dd==dirs,'Own topology changed before closure')
    body=(json.dumps({'schema':'pr47-acceptance-source-closure/v1','status':'CLOSED_SOURCE_ONLY','utc':dt.datetime.now(dt.timezone.utc).isoformat(),'self_excluded':[NAME],'files_count':len(payload),'files':payload,'source_only':True,'proposed_helpers_imported_compiled_executed':False,'future_acceptance_or_ROOT_approval_claimed':False},sort_keys=True,indent=2)+'\n').encode()
    for path in files.values():path.chmod(0o444)
    for row in payload:check(H,row);need(stat.S_IMODE((H/row['path']).stat().st_mode)==0o444,'Own full0444 including special bits')
    stage=H/'.PREPARATION_MANIFEST.staging'
    with stage.open('xb') as f:f.write(body);f.flush();os.fsync(f.fileno())
    stage.chmod(0o444);os.link(stage,H/NAME,follow_symlinks=False);stage.unlink();fd=os.open(H,os.O_RDONLY)
    try:os.fsync(fd)
    finally:os.close(fd)
    # All original/fixed foreign bytes and modes must remain exact after closure.
    for z in list(inputs['pins'].values())+inputs['external_input_rows']:check(R,z,True)
    check(R,inputs['unfinished_design_reference'],False)
    closed,dd=tree();need(set(closed)==set(files)|{NAME} and dd==dirs,'Exact self-only closed topology');need(stat.S_IMODE((H/NAME).stat().st_mode)==0o444,'Manifest full0444')
    print(json.dumps({'status':'CLOSED_SOURCE_ONLY','actual_closing_pid':os.getpid(),'files_count':len(payload),'directories_count':len(dirs),'manifest_sha256':sha(read(H/NAME)),'production_imported_compiled_executed':False,'future_acceptance_approved':False},sort_keys=True))
if __name__=='__main__':main()
