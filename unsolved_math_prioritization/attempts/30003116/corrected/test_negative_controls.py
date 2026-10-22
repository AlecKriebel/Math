"""Actual corruption and false-mathematics rejection in all Python optimization modes."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

class TestFailure(Exception):
    pass

def require(x,msg):
    if not x:raise TestFailure(msg)

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def repin(root,name):
    p=root/'MANIFEST.json';m=json.loads(p.read_text());b=(root/name).read_bytes()
    m['files'][name]['bytes']=len(b);m['files'][name]['sha256']=hashlib.sha256(b).hexdigest()
    p.write_text(json.dumps(m,sort_keys=True,indent=2)+'\n');return digest(p)

def invoke(root,pin,mode,full=False):
    cmd=[sys.executable,'-B']+mode+[str(root/'verify_public.py'),'--expected-manifest',pin]
    if not full:cmd+=['--integrity-only']
    return subprocess.run(cmd,capture_output=True,text=True,timeout=180)

def run(root,pin):
    require(digest(root/'MANIFEST.json')==pin,'initial manifest pin mismatch')
    results=[]
    mathematical=['nonunit_injectivity','dependent_injectivity','energy_without_diagonal','composite_permutation','false_sparse_period','zero_boundary','false_cover']
    for mode in ([],['-O'],['-OO']):
        label='normal' if not mode else mode[0]
        clean=invoke(root,pin,mode,full=True)
        require(clean.returncode==0,'clean replay failed in '+label+': '+clean.stdout+clean.stderr)
        results.append({'mode':label,'test':'clean_full_replay','returncode':0,'result':json.loads(clean.stdout)})
        for n in mathematical:
            x=subprocess.run([sys.executable,'-B']+mode+[str(root/'check_math.py'),'--negative',n],capture_output=True,text=True,timeout=30)
            require(x.returncode==2 and x.stdout.startswith('REJECTED:'),'false mathematics survived: '+label+'/'+n)
            results.append({'mode':label,'test':n,'returncode':x.returncode,'output':x.stdout.strip()})
        mutations=['proof_drift','missing_file','extra_file','extra_directory','symlink','manifest_rebinding','checker_drift','result_drift','rebound_false_result','rebound_wrong_status']
        for name in mutations:
            with tempfile.TemporaryDirectory(prefix='orbit-entropy-negative-') as temp:
                dest=Path(temp)/'packet';shutil.copytree(root,dest)
                usepin=pin;full=False
                if name=='proof_drift':
                    p=dest/'03_difference_amplification.md';p.write_bytes(p.read_bytes()+b'\nChanged.\n')
                elif name=='missing_file':(dest/'02_logarithmic_seed.md').unlink()
                elif name=='extra_file':(dest/'unlisted.txt').write_text('unlisted')
                elif name=='extra_directory':(dest/'unlisted').mkdir()
                elif name=='symlink':
                    p=dest/'01_congruence.md';p.unlink();p.symlink_to(dest/'README.md')
                elif name=='manifest_rebinding':
                    p=dest/'README.md';p.write_bytes(p.read_bytes()+b'\nRebound.\n');repin(dest,'README.md')
                elif name=='checker_drift':
                    p=dest/'check_math.py';p.write_bytes(p.read_bytes()+b'\n# drift\n')
                elif name=='result_drift':
                    p=dest/'checks.json';x=json.loads(p.read_text());x['checks']+=1;p.write_text(json.dumps(x)+'\n')
                elif name=='rebound_false_result':
                    p=dest/'checks.json';x=json.loads(p.read_text());x['checks']+=1;p.write_text(json.dumps(x)+'\n');usepin=repin(dest,'checks.json');full=True
                elif name=='rebound_wrong_status':
                    p=dest/'source_scope.json';x=json.loads(p.read_text());x['disposition']='solved';p.write_text(json.dumps(x)+'\n');usepin=repin(dest,'source_scope.json');full=True
                x=invoke(dest,usepin,mode,full=full)
                require(x.returncode==2 and x.stdout.startswith('REJECTED:'),'packet corruption survived: '+label+'/'+name+': '+x.stdout+x.stderr)
                results.append({'mode':label,'test':name,'returncode':x.returncode,'output':x.stdout.strip()})
    return {'status':'PASS','clean_full_replays':3,'mathematical_negative_rejections':21,'packet_negative_rejections':30,'manifest_sha256':pin,'results':results,
      'limits':'Controlled accidental-drift tests, not a security proof against arbitrary hostile validator replacement; no claim of formal mathematical verification.'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--expected-manifest',required=True);a=p.parse_args()
    try:print(json.dumps(run(Path(__file__).resolve().parent,a.expected_manifest),sort_keys=True,indent=2))
    except TestFailure as exc:
        print('FAILED: '+str(exc));raise SystemExit(2)
