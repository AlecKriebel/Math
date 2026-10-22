#!/usr/bin/env python3
"""Authenticate and copy this driver and BOOTSTRAP.py outside the tested packet."""
import argparse,hashlib,json,os,shutil,stat,subprocess,sys,tempfile
from pathlib import Path
CASES=['stale_payload','missing_file','extra_file','empty_directory','file_symlink','directory_symlink','fifo','executable_mode','writable_directory','duplicate_manifest','nonfinite_manifest','truncated_manifest','bool_schema','float_problem','false_status','false_turns','false_source_scope','wrong_frozen_pin','bool_bytes','negative_bytes','upper_digest','duplicate_inventory','unsafe_path','wrong_mode_schema','unknown_manifest_key','rebound_inner_claim','rebound_ledger_bool','rebound_audit_acceptance','rebound_patch','replaced_verifier','replaced_bootstrap']
MODES=[('normal',[]),('-O',['-O']),('-OO',['-OO'])]
def need(ok,msg):
    if not ok: raise ValueError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def regular(p):return stat.S_ISREG(p.lstat().st_mode)
def jread(p):return json.loads(p.read_text())
def write(p,obj):p.write_text(json.dumps(obj,sort_keys=True,indent=2)+'\n')
def rebind_top(p):
    m=jread(p/'PUBLICATION_MANIFEST.json')
    for item in m['files']:
        f=p/item['path']
        if f.exists() and regular(f):
            raw=f.read_bytes();item['bytes']=len(raw);item['sha256']=sha(raw)
    write(p/'PUBLICATION_MANIFEST.json',m)
def rebind_inner(p,directory,name):
    manifest='AUDIT_MANIFEST.json' if directory=='independent_audit' else 'MANIFEST.json'
    m=jread(p/directory/manifest);raw=(p/directory/name).read_bytes();m['files'][name]={'bytes':len(raw),'sha256':sha(raw)};write(p/directory/manifest,m)
def mutate(p,case):
    f=p/'PUBLICATION_MANIFEST.json';m=jread(f)
    if case=='stale_payload':(p/'corrected/PROOFS.md').write_text('corrupt');return
    if case=='missing_file':(p/'corrected/PROOFS.md').unlink();return
    if case=='extra_file':(p/'extra.txt').write_text('unexpected');return
    if case=='empty_directory':(p/'extra').mkdir();return
    if case=='file_symlink':(p/'README.md').unlink();(p/'README.md').symlink_to('PUBLICATION_ACCEPTANCE.md');return
    if case=='directory_symlink':shutil.rmtree(p/'corrected');(p/'corrected').symlink_to('original',target_is_directory=True);return
    if case=='fifo':(p/'README.md').unlink();os.mkfifo(p/'README.md');return
    if case=='executable_mode':(p/'README.md').chmod(0o755);return
    if case=='writable_directory':(p/'corrected').chmod(0o777);return
    if case=='duplicate_manifest':f.write_text('{"schema":1,"schema":1}');return
    if case=='nonfinite_manifest':f.write_text('{"schema":NaN}');return
    if case=='truncated_manifest':f.write_text('{');return
    if case=='bool_schema':m['schema']=True
    elif case=='float_problem':m['problem_id']=30003533.0
    elif case=='false_status':m['status']='claimed_solved'
    elif case=='false_turns':m['turns']='0/5'
    elif case=='false_source_scope':m['source_files_redistributed']=True
    elif case=='wrong_frozen_pin':m['frozen_manifest_anchors']['original']='0'*64
    elif case=='bool_bytes':m['files'][0]['bytes']=True
    elif case=='negative_bytes':m['files'][0]['bytes']=-1
    elif case=='upper_digest':m['files'][0]['sha256']=m['files'][0]['sha256'].upper()
    elif case=='duplicate_inventory':m['files'].append(dict(m['files'][0]))
    elif case=='unsafe_path':m['files'][0]['path']='../outside.md'
    elif case=='wrong_mode_schema':m['files'][0]['mode']=644
    elif case=='unknown_manifest_key':m['extra']=False
    elif case.startswith('rebound_'):
        if case=='rebound_inner_claim':
            d,n='corrected','CLAIMS.json';x=jread(p/d/n);x['original_target_resolved']=True;write(p/d/n,x);rebind_inner(p,d,n)
        elif case=='rebound_ledger_bool':
            d,n='corrected','LEDGER.json';x=jread(p/d/n);x['attempts'][0]['turn']=True;write(p/d/n,x);rebind_inner(p,d,n)
        elif case=='rebound_audit_acceptance':
            d,n='independent_audit','ACCEPTANCE.json';x=jread(p/d/n);x['pde_target_resolved']=True;write(p/d/n,x);rebind_inner(p,d,n)
        elif case=='rebound_patch':
            d,n='independent_audit','CORRECTIONS.patch';(p/d/n).write_text((p/d/n).read_text().replace('sufficient, not necessary','necessary, not sufficient'));rebind_inner(p,d,n)
        rebind_top(p);return
    elif case=='replaced_verifier':(p/'VERIFY_PUBLICATION.py').write_text('raise SystemExit("MUTATED_WRAPPER_EXECUTED")\n');rebind_top(p);return
    elif case=='replaced_bootstrap':(p/'BOOTSTRAP.py').write_text('raise SystemExit("MUTATED_WRAPPER_EXECUTED")\n');rebind_top(p);return
    else:raise ValueError(case)
    write(f,m)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--packet',type=Path,required=True);ap.add_argument('--bootstrap',type=Path,required=True);ap.add_argument('--expected-manifest',required=True);a=ap.parse_args()
    root=a.packet.resolve();bootstrap=a.bootstrap.resolve()
    need(root not in bootstrap.parents,'Bootstrap must be outside tested packet')
    need(root not in Path(__file__).resolve().parents,'Driver must be outside tested packet')
    need(sha((root/'PUBLICATION_MANIFEST.json').read_bytes())==a.expected_manifest,'Input pin mismatch')
    env={k:v for k,v in os.environ.items()if not k.startswith('PYTHON')};env['PYTHONDONTWRITEBYTECODE']='1'
    def invoke(packet,pin,flags):return subprocess.run([sys.executable,'-I','-B',*flags,str(bootstrap),'--packet',str(packet),'--expected-manifest',pin,'--check-only'],cwd='/tmp',env=env,capture_output=True,text=True,timeout=30)
    for label,flags in MODES:
        r=invoke(root,a.expected_manifest,flags);need(r.returncode==0,'Baseline failure '+label+': '+r.stderr)
    rejected=0
    with tempfile.TemporaryDirectory(prefix='coercivity-publication-mutations-')as tmp:
        for case in CASES:
            p=Path(tmp)/case;shutil.copytree(root,p)
            for x in [p,*p.rglob('*')]:x.chmod(0o755 if x.is_dir() else 0o644)
            mutate(p,case)
            # A fresh top-level anchor is intentional: schema and frozen inner pins
            # must reject hostile fixtures even when top-level hashes are rebound.
            pin=sha((p/'PUBLICATION_MANIFEST.json').read_bytes())
            for label,flags in MODES:
                r=invoke(p,pin,flags);need(r.returncode!=0,'Mutation accepted: '+case+' '+label)
                need('MUTATED_WRAPPER_EXECUTED' not in r.stdout+r.stderr,'Unauthenticated executable ran')
                rejected+=1
    print(json.dumps({'status':'PASS_EXTERNAL_BOOTSTRAP_MUTATIONS','problem_id':30003533,'modes':['normal','-O','-OO'],'cases':CASES,'mutation_cases':len(CASES),'rejections':rejected,'baseline_identity_passes':3,'top_level_hashes_rebound':True,'nested_frozen_pins_retained':True,'replaced_wrapper_not_executed':True},sort_keys=True,indent=2))
if __name__=='__main__':
    try:main()
    except (ValueError,OSError,subprocess.SubprocessError)as exc:print('MUTATION_TEST_FAILED: '+str(exc),file=sys.stderr);sys.exit(1)
