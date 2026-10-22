"""Read-only actual-input integration check. Writes only its own preparation receipt."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from datetime import datetime,timezone
import hashlib,importlib.util,json,os,stat
P=Path(__file__).resolve().parent
SOURCE_PIN={'bytes':44120,'sha256':'47e01e759f67e96db7151fe738bf18e21a1dc25dcaf624e5628abea59d49d1e9'}
GATE_PIN={'path':'ROOT_PUBLICATION_GATE_01.json','bytes':68666,'sha256':'e9f94fee3fa66b47f44fee38c7c30701790d4a477de330146a11279f1b4d628b'}
def check(ok,msg):
    if not ok:raise RuntimeError(msg)
def bp(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
check(bp((P/'make_native.py').read_bytes())==SOURCE_PIN,'Constructor pin differs')
spec=importlib.util.spec_from_file_location('native02_actual_preflight',P/'make_native.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
A=P.parent
gate=m.json_bytes(m.read_pin(A,GATE_PIN),'actual final gate')
originals=m.originals()
baseline=m.check_canonical_gate(A,gate,{'publication_ready_gate':GATE_PIN},False)
seal_pin={'path':gate['package']+'/'+gate.get('package_seal_file','PACKAGE_SEAL.json'),**gate['package_seal']}
package,seal,files,paper,driver=m.verify_package(A,seal_pin,gate,False)
reviews=m.canonical_reviews(A,gate,seal_pin,False)
check(len(files)==181 and len(gate['other_safe_files'])==88 and len(reviews)==2 and len(baseline)==4,'Pinned final integration extent differs')
protected={'ORIGINAL_SUBMISSION_CUSTODY.json',m.GATE_NAME}
protected.update('original_submitted_head/'+n for n in originals)
protected.update(package+'/'+n for n in files)
protected.update(gate['other_safe_files'])
for e in reviews:
    protected.add(e['Root_acceptance_file'])
    protected.update(e['directory']+'/'+n for n in e['safe_files'])
native01=A/'native_publication_preparation_01'
for q in native01.rglob('*'):
    check(not q.is_symlink(),'Native01 symlink')
    if q.is_file():protected.add(q.relative_to(A).as_posix())
def snapshot():
    out={}
    for name in sorted(protected):
        q=m.safe_file(A,name);b=q.read_bytes();s=q.stat()
        out[name]={**bp(b),'mtime_ns':s.st_mtime_ns,'ctime_ns':s.st_ctime_ns,'mode':stat.S_IMODE(s.st_mode)}
    return out
now=snapshot()
B=P/'PROTECTED_INPUT_BASELINE.json'
phase=sys.argv[1] if len(sys.argv)>1 else 'verify'
if phase=='baseline':
    check(not B.exists(),'Protected baseline already exists')
    record={'schema':'pr204-native02-protected-input-baseline-v1','UTC':datetime.now(timezone.utc).isoformat(),'files':now}
    target=B
else:
    old=json.loads(B.read_bytes())
    check(now==old['files'],'Protected inputs byte/time/mode drift')
    target=P/('ACTUAL_PREFLIGHT_OPTIMIZED.json' if sys.flags.optimize else 'ACTUAL_PREFLIGHT_NORMAL.json')
    record={'schema':'pr204-native02-actual-readonly-integration-v1','evidence_scope':'READ_ONLY_ACTUAL_INPUTS_NOT_PUBLICATION_OR_ADOPTION','UTC':datetime.now(timezone.utc).isoformat(),'status':'PASS','python_optimization':sys.flags.optimize,'constructor':SOURCE_PIN,'gate':GATE_PIN,'package':package,'package_files_verified':len(files),'other_safe_paths_verified':len(gate['other_safe_files']),'actual_Root_review_events_verified':len(reviews),'preparation_receipts_verified':len(baseline),'original_archive_files_verified':len(originals),'protected_regular_files_unchanged':len(now),'protected_input_bytes_times_modes_unchanged':True,'sealed_native01_unchanged':True,'paper':{'path':package+'/'+paper,**files[paper]},'portable_entrypoint':{'path':package+'/'+driver,**files[driver]},'actual_constructor_payload_constructed':False,'actual_ready_publication_tracker_or_merge_facts_supplied':False,'actual_API_or_external_action':False}
data=m.enc(record);tmp=target.with_name('.'+target.name+'.tmp')
with open(tmp,'xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
check(tmp.read_bytes()==data,'Receipt readback differs')
os.replace(tmp,target);fd=os.open(P,os.O_RDONLY);os.fsync(fd);os.close(fd)
print(json.dumps({'status':'PASS','phase':phase,'optimization':sys.flags.optimize,'protected_files':len(now),'receipt':target.name,**bp(data)},sort_keys=True))
