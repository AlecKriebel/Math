"""Own adjacent source author/control capture; never runs a proposed helper."""
from pathlib import Path
import subprocess,sys,datetime,json,hashlib,os,stat
H=Path(__file__).resolve().parent
allowed={'AUTHORING_ACTUAL_CAPTURE':'author_adjacent_repair.py','CONTROLS_ACTUAL_CAPTURE':'independent_repair_controls.py','CLOSURE_ACTUAL_CAPTURE':'close_owned_source.py'}
name,member=sys.argv[1:3]
if name not in allowed or member!=allowed[name]:raise ValueError('Own sources only')
source=H/member
if source.is_symlink() or not source.is_file():raise ValueError('Regular own source')
C=H/name;C.mkdir(exist_ok=False);raw=source.read_bytes()
(C/'PRELAUNCH_SOURCE.py').write_bytes(raw);(C/'PRELAUNCH_OPERATOR.py').write_bytes(Path(__file__).read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest();stamp=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
argv=[sys.executable,'-B',str(source)];start=stamp()
with (C/'stdout.bin').open('xb') as out,(C/'stderr.bin').open('xb') as err:
    child=subprocess.Popen(argv,cwd=H,stdin=subprocess.DEVNULL,stdout=out,stderr=err);code=child.wait()
end=stamp();streams=[]
for n in ['stdout.bin','stderr.bin']:
    b=(C/n).read_bytes();streams.append({'path':n,'bytes':len(b),'sha256':sha(b)})
rec={'schema':'pr43-own-adjacent-source-operation-capture/v2','actual_execution':True,'completed':True,'parent_pid':os.getpid(),'pid':child.pid,'argv':argv,'cwd':str(H),'started_utc':start,'finished_utc':end,'exit_code':code,'status':'PASS' if code==0 else 'FAIL','stdin_supplied':False,'source_sha256':sha(raw),'source_unchanged':source.read_bytes()==raw,'prelaunch_operator_sha256':sha((C/'PRELAUNCH_OPERATOR.py').read_bytes()),'stdout':streams[0],'stderr':streams[1],'proposed_acceptance_helpers_imported_compiled_executed':False,'science_helpers_executed':False,'native_Git_remote_people_mutations':False}
(C/'CAPTURE.json').write_text(json.dumps(rec,indent=2)+'\n')
if member=='close_owned_source.py' and code==0:
    files=[]
    for p in sorted(H.rglob('*')):
        if p.is_symlink() or not (p.is_file() or p.is_dir()):raise ValueError('Unsafe own closure')
        if p.is_file():
            if p.parent==H and p.name=='PREPARATION_MANIFEST.json':raise ValueError('Existing closure')
            p.chmod(0o444);b=p.read_bytes();files.append({'path':p.relative_to(H).as_posix(),'bytes':len(b),'sha256':sha(b)})
    mf=H/'PREPARATION_MANIFEST.json';obj={'schema':'pr43-acceptance-source-closure/v1','status':'CLOSED_SOURCE_ONLY','utc':stamp(),'self_excluded':['PREPARATION_MANIFEST.json'],'files_count':len(files),'files':files,'source_only':True,'proposed_helpers_imported_compiled_executed':False,'future_acceptance_or_ROOT_approval_claimed':False}
    with mf.open('x') as f:json.dump(obj,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
    mf.chmod(0o444);print(json.dumps({'status':'CLOSED_SOURCE_ONLY','actual_closure_parent_pid':os.getpid(),'actual_closure_child_pid':child.pid,'files_count':len(files),'manifest_sha256':sha(mf.read_bytes()),'future_ROOT_or_acceptance_approval':False}))
else:print(json.dumps(rec))
sys.exit(code)
