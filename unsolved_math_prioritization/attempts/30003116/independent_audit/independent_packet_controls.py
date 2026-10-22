"""Read-only, malformed-packet and scope-boundary controls. Works on temporary copies only."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

class ControlFailure(Exception):pass

def require(x,label):
    if not x:raise ControlFailure(label)

def identity(root):
    return {p.name:{'bytes':p.stat().st_size,'sha256':sha256(p.read_bytes()).hexdigest(),'mode':oct(p.stat().st_mode & 0o777)} for p in sorted(root.iterdir())}

def rewrite_manifest(root,m):
    raw=(json.dumps(m,sort_keys=True,indent=2)+'\n').encode();(root/'MANIFEST.json').write_bytes(raw)
    return sha256(raw).hexdigest()

def rebind(root,name):
    m=json.loads((root/'MANIFEST.json').read_text());p=root/name;raw=p.read_bytes()
    m['files'][name]={'bytes':len(raw),'sha256':sha256(raw).hexdigest(),'mode':format(p.stat().st_mode & 0o777,'04o')}
    return rewrite_manifest(root,m)

def invoke(root,pin,mode,integrity=False):
    args=[sys.executable,'-B']+mode+[str(root/'verify_public.py'),'--expected-manifest',pin]
    if integrity:args+=['--integrity-only']
    cp=subprocess.run(args,cwd=root,capture_output=True,text=True,timeout=120)
    return {'returncode':cp.returncode,'stdout':cp.stdout.strip(),'stderr_last_line':cp.stderr.strip().splitlines()[-1] if cp.stderr.strip() else ''}

def run(source,pin,hardened):
    source=source.resolve();hardened=hardened.resolve();before=identity(source)
    require(sha256((source/'MANIFEST.json').read_bytes()).hexdigest()==pin,'source pin mismatch')
    rows=[]
    for variant in ('original','hardened_candidate'):
      for mode in ([],['-O'],['-OO']):
        label='normal' if not mode else mode[0]
        cases=['clean_full','invalid_external_pin','manifest_list','manifest_null','manifest_bad_json','manifest_duplicate_key',
          'manifest_wrong_target','manifest_wrong_format','unsafe_path','file_record_list','negative_byte_count','boolean_byte_count',
          'invalid_digest','invalid_mode','scope_list','scope_duplicate_key','scope_wrong_target','scope_wrong_rank','scope_wrong_status',
          'checker_syntax','checker_assert','rebound_false_result','mode_drift','extra_directory','extra_file','symlink','manifest_symlink',
          'rebound_false_proof_demonstrates_scope','readonly_full']
        for case in cases:
          with tempfile.TemporaryDirectory(prefix='rational-orbit-audit-') as td:
            root=Path(td)/'packet';shutil.copytree(source,root)
            usepin=pin
            if variant=='hardened_candidate':
                (root/'verify_public.py').write_bytes(hardened.read_bytes());usepin=rebind(root,'verify_public.py')
            m=json.loads((root/'MANIFEST.json').read_text())
            full=case in ('clean_full','scope_list','scope_duplicate_key','scope_wrong_target','scope_wrong_rank','scope_wrong_status','rebound_false_result','rebound_false_proof_demonstrates_scope','readonly_full')
            if case=='invalid_external_pin':usepin='invalid'
            elif case=='manifest_list':usepin=rewrite_manifest(root,[])
            elif case=='manifest_null':usepin=rewrite_manifest(root,None)
            elif case=='manifest_bad_json':
                raw=b'{invalid';(root/'MANIFEST.json').write_bytes(raw);usepin=sha256(raw).hexdigest()
            elif case=='manifest_duplicate_key':
                raw=(root/'MANIFEST.json').read_bytes().replace(b'{',b'{"problem_id": 0,',1)
                (root/'MANIFEST.json').write_bytes(raw);usepin=sha256(raw).hexdigest()
            elif case=='manifest_wrong_target':m['problem_id']=0;usepin=rewrite_manifest(root,m)
            elif case=='manifest_wrong_format':m['format']='other';usepin=rewrite_manifest(root,m)
            elif case=='unsafe_path':m['files']['../outside']={};usepin=rewrite_manifest(root,m)
            elif case=='file_record_list':m['files']['README.md']=[];usepin=rewrite_manifest(root,m)
            elif case=='negative_byte_count':m['files']['README.md']['bytes']=-1;usepin=rewrite_manifest(root,m)
            elif case=='boolean_byte_count':m['files']['README.md']['bytes']=True;usepin=rewrite_manifest(root,m)
            elif case=='invalid_digest':m['files']['README.md']['sha256']='invalid';usepin=rewrite_manifest(root,m)
            elif case=='invalid_mode':m['files']['README.md']['mode']='invalid';usepin=rewrite_manifest(root,m)
            elif case.startswith('scope_'):
                p=root/'source_scope.json';o=json.loads(p.read_text())
                if case=='scope_list':raw=b'[]'
                elif case=='scope_duplicate_key':raw=p.read_bytes().replace(b'{',b'{"problem_id": 0,',1)
                else:
                    key={'scope_wrong_target':'problem_id','scope_wrong_rank':'rank','scope_wrong_status':'disposition'}[case]
                    o[key]='solved' if key=='disposition' else 0;raw=json.dumps(o).encode()
                p.write_bytes(raw);usepin=rebind(root,p.name)
            elif case=='checker_syntax':(root/'check_math.py').write_text('def !\n');usepin=rebind(root,'check_math.py')
            elif case=='checker_assert':
                p=root/'check_math.py';p.write_text(p.read_text()+'\nassert False\n');usepin=rebind(root,p.name)
            elif case=='rebound_false_result':
                p=root/'checks.json';o=json.loads(p.read_text());o['checks']+=1;p.write_text(json.dumps(o));usepin=rebind(root,p.name)
            elif case=='mode_drift':(root/'README.md').chmod(0o600)
            elif case=='extra_directory':(root/'extra').mkdir()
            elif case=='extra_file':(root/'extra').write_text('x')
            elif case=='symlink':p=root/'README.md';p.unlink();p.symlink_to(root/'01_congruence.md')
            elif case=='manifest_symlink':
                p=root/'MANIFEST.json';target=Path(td)/'manifest';target.write_bytes(p.read_bytes());p.unlink();p.symlink_to(target)
            elif case=='rebound_false_proof_demonstrates_scope':
                p=root/'03_difference_amplification.md';p.write_text(p.read_text().replace('sqrt(log log s)','(log s)^100'));usepin=rebind(root,p.name)
            elif case=='readonly_full':
                for name,entry in m['files'].items():entry['mode']='0444'
                usepin=rewrite_manifest(root,m)
                for p in root.iterdir():p.chmod(0o444)
                root.chmod(0o555)
                blocked=False
                try:
                    with (root/'README.md').open('ab'):pass
                except PermissionError:blocked=True
                require(blocked,'read-only copy writable')
                snapshot=identity(root)
            result=invoke(root,usepin,mode,integrity=not full)
            if case=='readonly_full':
                require(identity(root)==snapshot,'read-only copy changed')
                root.chmod(0o755)
                for p in root.iterdir():p.chmod(0o644)
            accepts=case in ('clean_full','readonly_full','rebound_false_proof_demonstrates_scope') or (case=='manifest_wrong_target' and variant=='original')
            expected=0 if accepts else 2
            if variant=='original' and case in ('manifest_list','manifest_null','checker_syntax'):expected=1
            require(result['returncode']==expected,variant+'/'+label+'/'+case+': '+str(result))
            if expected==2:require(result['stdout'].startswith('REJECTED:'),'rejection label absent')
            rows.append({'variant':variant,'mode':label,'case':case,**result})
    require(identity(source)==before,'frozen source changed')
    return {'status':'PASS','source_manifest_sha256':pin,'source_unchanged':True,'cases':len(rows),'results':rows,
      'scope':'Original malformed payloads fail closed; three inputs raise uncaught exceptions. Original ignores manifest top-level target under an independently changed pin. Optional hardening rejects these cleanly. A deliberately false re-pinned proof is accepted by both: this is an integrity/finite-control checker, not a theorem prover. Read-only copies rebind only file modes and, for the candidate, validator bytes; frozen original bytes and modes are unchanged.'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--packet',type=Path,required=True);p.add_argument('--expected-manifest',required=True);p.add_argument('--hardened',type=Path,required=True);a=p.parse_args()
    try:print(json.dumps(run(a.packet,a.expected_manifest,a.hardened),indent=2,sort_keys=True))
    except ControlFailure as exc:
        print('FAILED: '+str(exc));raise SystemExit(2)
