"""Root hashes/recorded-results adoption; does not repeat scientific campaigns."""
from pathlib import Path,PurePosixPath
import hashlib,json,subprocess,sys
sys.dont_write_bytecode=True
O=Path(__file__).resolve().parent;R=O.parent;P=R.parent;S=P/'sources'
H=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
load=lambda f:json.loads(f.read_bytes())
def need(ok,msg):
    if not ok:raise RuntimeError(msg)
def rows_bind(rows,root):
    for row in rows:
        f=root/row['path'];need(f.is_file() and not f.is_symlink() and f.stat().st_size==row['bytes'] and H(f)==row['sha256'],'binding '+str(f))
spec=[('scope/resume_20261114_sol','MANIFEST.json','SEAL.json','manifest_sha256','5ca9c063bdbcca8b8d23f4287de7f53071c37bb276490e3601f12b2a3b27d331'),('analytic/resume_20261114','PACKET_MANIFEST.json','PACKET_SEAL.json','manifest_sha256','af115cd2d82157bd66570ce7bc2aef51b349028490b777695d18cedaf4f0e3bb')]
packets=[]
for lane,mf,sf,field,pin in spec:
    d=R/lane;need(H(d/sf)==pin,'exact seal '+lane);seal=load(d/sf);need(H(d/mf)==seal[field],'manifest seal '+lane)
    m=load(d/mf);names=set()
    for row in m['files']:
        n=row['path'];q=PurePosixPath(n);need(not q.is_absolute() and '..' not in q.parts and n not in names,'safe owned path');names.add(n)
    rows_bind(m['files'],d)
    need({str(f.relative_to(d)) for f in d.rglob('*') if f.is_file()}==names|{mf,sf},'exact owned set '+lane)
    packets.append({'lane':lane,'owned_files':len(names),'seal_sha256':pin})
D=R/'scope/resume_20261114_sol';bindings=load(D/'SOURCE_BINDINGS.json')['files'];rows_bind(bindings,Path('/'))
A=R/'analytic/resume_20261114';inputs=load(A/'INPUT_BINDINGS.json')['files']
for name,row in inputs.items():
    f=P/name;need(f.is_file() and f.stat().st_size==row['bytes'] and H(f)==row['sha256'],'analytic external '+name)
old=R/'analytic';early=load(old/'EARLY_MANIFEST.json');rows_bind(early['files'],old)
need(H(S/'SOURCE_READY.json')=='1e18c3ce5d1b7556f97ee9c90f4d8ed21fa6a4d19e54cee8b730210a15795eaa','exact native ready')
supplied=load(A/'SUPPLIED_REPLAY.json');need(supplied['finite_checks']==147619 and supplied['all_odd_prime_checks']==46298,'actual stored native scopes')
independent=load(A/'INDEPENDENT_CHECKS.json');need(independent['total_controls']==103033,'recorded independent scope')
adv=R/'adversarial';need(H(adv/'FINAL_SEAL.json')=='46b0688cd819b9218d6a2dbe531508723f2863263895972b07b02d8ac89c49cb','adversarial final seal')
args=[sys.executable,'-B',str(adv/'verify_packet.py')];run=subprocess.run(args,capture_output=True,text=True,timeout=60)
need(run.returncode==0 and not run.stderr,'adversarial actual read-only custody')
print(json.dumps({'status':'PASS_ROOT_THREE_SEALS_SOURCE_AND_RECORDED_RESULTS_WITHOUT_SCIENTIFIC_REPLAY','direct_hash_only_packets':packets,'scope_source_and_predecessor_bindings':len(bindings),'analytic_external_bindings':len(inputs),'analytic_predecessor_files':len(early['files']),'actual_read_only_adversarial_execution':{'args':args,'returncode':run.returncode,'stdout':run.stdout,'stderr':run.stderr,'script_sha256':H(adv/'verify_packet.py')},'whole_native_replay_original':supplied,'recorded_independent_analytic_controls':103033,'scientific_programs_or_campaigns_reexecuted':False,'originals_or_existing_reviews_rewritten':False,'mathematical_proof_replaced_by_hashes_or_counts':False},indent=2))
