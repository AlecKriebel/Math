#!/usr/bin/env python3
"""Adversarial replay checks in disposable directories, including optimized Python."""
import sys
sys.dont_write_bytecode=True
import hashlib,json,os,shutil,subprocess,tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parent
MODES=[[],['-O'],['-OO']]

def invoke(p,mode):
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
    return subprocess.run([sys.executable,'-B']+mode+[str(p/'verify.py')],cwd=p.parent,env=env,text=True,capture_output=True)

def need(ok,msg):
    if not ok: raise RuntimeError(msg)

def rebind(p,name):
    m=json.loads((p/'MANIFEST.json').read_text());b=(p/name).read_bytes()
    m['files'][name]={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
    (p/'MANIFEST.json').write_text(json.dumps(m,sort_keys=True,indent=2)+'\n')

def mutate(p,case):
    if case=='altered_proof': (p/'PROOFS.md').write_text((p/'PROOFS.md').read_text()+'\ncorruption\n');return
    if case=='extra_file': (p/'extra.txt').write_text('unexpected');return
    if case=='missing_file': (p/'SOURCES.md').unlink();return
    if case=='symlink':
        (p/'RESULT.md').unlink();(p/'RESULT.md').symlink_to('PROOFS.md');return
    name='CLAIMS.json';d=json.loads((p/name).read_text())
    if case=='false_solved':d['status']='solved';d['original_target_resolved']=True
    elif case=='false_smooth_counterexample':d['smooth_counterexample_proved']=True
    elif case=='false_curvature':d['geometric_controls']['curvature_at_pi_over_3']='8/3'
    elif case=='bool_for_integer':d['schema_version']=True
    elif case=='unknown_claim':d['unproved_claim']=True
    elif case=='duplicate_key':
        (p/name).write_text('{"status":"unsolved","status":"solved"}');rebind(p,name);return
    elif case=='nonfinite':
        (p/name).write_text('{"x":NaN}');rebind(p,name);return
    elif case=='truncated_json':
        (p/name).write_text('{');rebind(p,name);return
    else:raise ValueError(case)
    (p/name).write_text(json.dumps(d,indent=2)+'\n');rebind(p,name)

def main():
    positive=0;negative=0
    baseline=None
    for mode in MODES:
        r=invoke(ROOT,mode);need(r.returncode==0,'baseline failed: '+r.stderr)
        baseline=baseline or r.stdout;need(r.stdout==baseline,'mode output mismatch');positive+=1
    cases=['altered_proof','extra_file','missing_file','symlink','false_solved','false_smooth_counterexample','false_curvature','bool_for_integer','unknown_claim','duplicate_key','nonfinite','truncated_json']
    with tempfile.TemporaryDirectory(prefix='coercivity_packet_test_') as temp:
        temp=Path(temp)
        for case in cases:
            p=temp/case;shutil.copytree(ROOT,p);mutate(p,case)
            for mode in MODES:
                r=invoke(p,mode);need(r.returncode!=0,'mutation accepted: '+case+str(mode));negative+=1
        p=temp/'readonly_relocated';shutil.copytree(ROOT,p)
        for f in p.iterdir():f.chmod(0o444)
        p.chmod(0o555)
        before={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in p.iterdir()}
        try:
            for mode in MODES:
                r=invoke(p,mode);need(r.returncode==0 and r.stdout==baseline,'readonly relocated failure: '+r.stderr);positive+=1
            after={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in p.iterdir()}
            need(before==after,'readonly payload changed')
        finally:
            p.chmod(0o755)
            for f in p.iterdir():f.chmod(0o644)
    print(json.dumps({'status':'PASS','normal_optimized_double_optimized':True,'successful_replays':positive,'mutation_cases':len(cases),'rejected_mutations':negative,'readonly_relocation':True},sort_keys=True,separators=(',',':')))

if __name__=='__main__': main()
