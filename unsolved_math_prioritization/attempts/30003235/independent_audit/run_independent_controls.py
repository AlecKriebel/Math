#!/usr/bin/env python3
"""Source-free replay and actual adversarial controls for the independent checker."""
import argparse, copy, hashlib, json, os
from pathlib import Path
import shutil, subprocess, sys, tempfile
ROOT=Path(__file__).resolve().parent
ENV=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
MODES=[[],['-O'],['-OO']]
class Failure(Exception): pass
def demand(ok,msg):
    if not ok: raise Failure(msg)
def call(script,root,probe,mode,cwd):
    p=subprocess.run([sys.executable,*mode,str(script),'--root',str(root),'--probe',str(probe)],cwd=cwd,env=ENV,text=True,capture_output=True)
    try: d=json.loads(p.stdout)
    except ValueError: raise Failure('Unstructured output: '+p.stdout+p.stderr)
    return p.returncode,d
def snapshot(root):
    return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file()}
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--root',type=Path,required=True); arg=ap.parse_args(); frozen=arg.root.resolve()
    report={'schema':1,'status':'PASS','scope':'finite_controls_only','valid_modes':[],'negative_controls':[],'read_only_modes':[]}
    probe=json.loads((ROOT/'probe.json').read_text()); script=ROOT/'independent_check.py'
    initial=snapshot(frozen)
    with tempfile.TemporaryDirectory(prefix='independent-weighted-affine-') as td:
        tmp=Path(td); baseline=None
        for mode in MODES:
            code,out=call(script,frozen,ROOT/'probe.json',mode,tmp)
            demand(code==0 and out['status']=='PASS','Valid control failed')
            if baseline is None: baseline=out
            demand(out==baseline,'Optimization dependence')
            report['valid_modes'].append(mode or ['normal'])
        mutations=[]
        def changed(label,key,value):
            p=copy.deepcopy(probe);p[key]=value;mutations.append((label,json.dumps(p)))
        changed('zero_weight','weights',['1','0'])
        changed('negative_weight','weights',['4/3','-1/3'])
        changed('nonnormalized_weights','weights',['2/3','2/3'])
        changed('wrong_weight_order','weights',['1/3','2/3'])
        changed('wrong_inversion','image',['-3/2','15/14'])
        changed('inversion_pole','point',['0','5/7'])
        changed('wrong_rank','rank_bound',1)
        changed('rank_three','rank_rows',[[1,0,0],[0,1,0],[0,0,1]])
        changed('boolean_schema','schema',True)
        changed('boolean_rank_bound','rank_bound',True)
        changed('boolean_rank_coefficient','rank_rows',[[True,0,0]])
        changed('malformed_rank_row','rank_rows',[[1,0]])
        changed('numeric_rational_field','point',[2,'3'])
        changed('zero_rational_denominator','point',['1/0','3'])
        changed('false_global_solution','global_endpoint_proved',True)
        p=copy.deepcopy(probe);p['extra']=1;mutations.append(('extra_field',json.dumps(p)))
        p=copy.deepcopy(probe);del p['schema'];mutations.append(('missing_field',json.dumps(p)))
        mutations.extend([('malformed_json','{"schema":'),('array_root','[]'),('duplicate_key',json.dumps(probe)[:-1]+',"schema":1}'),('nonfinite_json',json.dumps(probe).replace('"schema": 1','"schema": NaN'))])
        for label,body in mutations:
            f=tmp/(label+'.json');f.write_text(body)
            for mode in MODES:
                code,out=call(script,frozen,f,mode,tmp)
                demand(code==1 and out['status']=='FAIL','Negative accepted: '+label)
            report['negative_controls'].append({'name':label,'rejected_in':['normal','-O','-OO']})
        for label in ['proof_byte_drift','manifest_self_rewrite','extra_payload']:
            damaged=tmp/label;shutil.copytree(frozen,damaged)
            for p in [damaged,*damaged.rglob('*')]:p.chmod(0o755 if p.is_dir() else 0o644)
            if label=='proof_byte_drift':
                with (damaged/'PROOF.md').open('a') as f:f.write('\nChanged.\n')
            elif label=='manifest_self_rewrite':
                m=json.loads((damaged/'MANIFEST.json').read_text());m['files'][0]['bytes']+=1;(damaged/'MANIFEST.json').write_text(json.dumps(m))
            else:(damaged/'extra.txt').write_text('extra')
            for mode in MODES:
                code,out=call(script,damaged,ROOT/'probe.json',mode,tmp)
                demand(code==1 and out['status']=='FAIL','Integrity negative accepted: '+label)
            report['negative_controls'].append({'name':label,'rejected_in':['normal','-O','-OO']})
        release=tmp/'readonly';release.mkdir();shutil.copytree(frozen,release/'frozen');shutil.copy2(script,release/'independent_check.py');shutil.copy2(ROOT/'probe.json',release/'probe.json')
        for p in [*release.rglob('*'),release]:p.chmod(0o555 if p.is_dir() else 0o444)
        before=snapshot(release)
        test=subprocess.run([sys.executable,'-c',"import sys;from pathlib import Path\ntry: Path(sys.argv[1]).write_text('x')\nexcept PermissionError:sys.exit(0)\nsys.exit(5)",str(release/'forbidden')],env=ENV,capture_output=True)
        demand(test.returncode==0,'Write protection not effective')
        for mode in MODES:
            code,out=call(release/'independent_check.py',release/'frozen',release/'probe.json',mode,tmp)
            demand(code==0 and out==baseline,'Read-only relocated replay failed')
            report['read_only_modes'].append(mode or ['normal'])
        demand(before==snapshot(release),'Read-only package changed')
        report['actual_write_attempt_rejected']=True;report['read_only_files_unchanged']=True;report['unrelated_cwd']=True;report['source_documents_absent']=True
        for p in [release,*release.rglob('*')]:p.chmod(0o755 if p.is_dir() else 0o644)
    demand(initial==snapshot(frozen),'Frozen original changed')
    report['frozen_original_unchanged']=True;report['baseline']=baseline
    print(json.dumps(report,indent=2,sort_keys=True))
if __name__=='__main__':
    try:main()
    except (Failure,OSError,ValueError,KeyError) as e:
        print(json.dumps({'status':'FAIL','reason':str(e)},sort_keys=True));sys.exit(1)
