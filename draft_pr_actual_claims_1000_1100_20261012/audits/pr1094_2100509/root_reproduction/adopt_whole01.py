from pathlib import Path
import hashlib,json,subprocess,tempfile,os,datetime
A=Path(__file__).resolve().parents[1];R=A/'reviews/package_01';P=A/'preprint_v1_0'
def load(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def require(v,m):
    if not v:raise RuntimeError(m)
def check(p,r):
    b=p.read_bytes();require(len(b)==r['bytes'] and sha(b)==r['sha256'],str(p))
seal=load(R/'SEALED.json');require(sha((R/'OUTPUT_PINS.json').read_bytes())==seal['output_pins_sha256'],'output seal')
counts={}
for filename,base in [('INPUT_PINS.json',A),('OUTPUT_PINS.json',R)]:
    rows=load(R/filename)['entries']
    for row in rows:check(base/row['path'],row)
    counts[filename]=len(rows)
for r in load(R/'SOURCE_READ_LEDGER.json')['sources']:check(A/r['path'],r)
controls=[]
for optimized in [False,True]:
    argv=['python3','-B']+(['-O'] if optimized else [])+[str(R/'independent_controls.py')]
    p=subprocess.run(argv,capture_output=True);require(p.returncode==0,p.stderr.decode(errors='replace'))
    result=json.loads(p.stdout);require(result==load(R/'INDEPENDENT_NORMAL.json')==load(R/'INDEPENDENT_OPTIMIZED.json'),'full independent math JSON differs')
    controls.append({'optimized':optimized,'exit_code':p.returncode,'full_JSON_equals_review':True,'stdout_sha256':sha(p.stdout)})
reproduced=[]
with tempfile.TemporaryDirectory(prefix='root1094-finding-',dir='/private/tmp') as td:
    td=Path(td);link=td/'lexical-link';os.symlink(P/'kit',link)
    for optimized in [False,True]:
        mode='optimized' if optimized else 'normal';target=link/'..'/('lexical-'+mode+'.zip')
        argv=['python3','-B']+(['-O'] if optimized else [])+[str(P/'kit/scripts/build_support.py'),'--out',str(target)]
        p=subprocess.run(argv,capture_output=True);normalized=td/('lexical-'+mode+'.zip')
        require(p.returncode==0 and normalized.read_bytes()==(P/'pr1094_supportkit_v1.0.zip').read_bytes(),'advertised-contract mismatch did not reproduce')
        reproduced.append({'optimized':optimized,'literal_argument':str(target),'normalized_target':str(normalized),'writer_exit':p.returncode,'fresh_archive_byte_equal':True,'impact':'Advertised lexical-link rejection absent; no protected overwrite or mathematical defect.'})
for row in load(R/'INPUT_PINS.json')['entries']:check(A/row['path'],row)
record={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'ADOPT_COMPLETE_WHOLE01_ONE_P3_PENDING_BOUNDED_REPAIR_AND_NEW_WHOLE02','full_REPORT_INDEPENDENT_DERIVATION_VERDICT_SOURCE_LEDGER_read':True,'counts_rehashed':counts,'primary_source_files_rehashed':5,'independent_math_root_replays':controls,'root_actual_P3_reproduction':reproduced,'whole_reviews_completed':1,'minimum_whole_reviews':2,'findings':{'P0':0,'P1':0,'P2':0,'P3':1},'accepted_math':'Complete real-spectrum compact-support classification all n in commutingframe; scope/credit/UNKNOWNpriority unchanged.','required_repair':'Inspect lexical path symlink components before collapsing dot-dot, preserving documented safe sibling ../ outputs, or consistently narrow every current advertised contract. Refresh exact dependent custody/manifest/ZIP/bindings; preserve manuscript/PDF/native metadata and all captured historical stages. New complete independent whole02 required.','publication_ready':False,'published':False,'services_held_after_pr':1032,'output_pins_sha256':seal['output_pins_sha256']}
(A/'ROOT_WHOLE_PACKAGE_REVIEW_01.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({'status':'PASS_ADOPT_ONE_P3','counts':counts,'actual_fault_reproductions':2,'ready':False}))
