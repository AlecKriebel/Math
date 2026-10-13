#!/usr/bin/env python3
"""Replay in three optimization modes, reject real mutations, then relocate read-only."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parent
MODES=[[],['-O'],['-OO']]
ENV=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')

class ControlError(Exception):
    pass

def require(ok,msg):
    if not ok:
        raise ControlError(msg)

def call(root,mode,args=(),cwd=None):
    r=subprocess.run([sys.executable,*mode,str(root/'check.py'),*map(str,args)],cwd=cwd or root,env=ENV,text=True,capture_output=True)
    try:
        data=json.loads(r.stdout)
    except ValueError as exc:
        raise ControlError(f'Unparseable checker output: {r.stdout} {r.stderr}') from exc
    return r.returncode,data

def snapshot(root):
    return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file()}

def main():
    results={'schema':1,'status':'PASS','normal_optimized_valid':[],'negative_controls':[],'relocation':[]}
    baseline=None
    with tempfile.TemporaryDirectory(prefix='weighted-affine-controls-') as td:
        tmp=Path(td)
        for mode in MODES:
            code,data=call(ROOT,mode,cwd=tmp)
            require(code==0 and data.get('status')=='PASS',f'Valid run failed {mode}: {data}')
            if baseline is None:
                baseline=data
            require(data==baseline,'Optimization changed output')
            results['normal_optimized_valid'].append({'mode':mode or ['normal'],'status':'PASS'})
        claims=json.loads((ROOT/'claims.json').read_text())
        probes=json.loads((ROOT/'probes.json').read_text())
        negatives=[]
        for label,key,value in [
            ('false_global_solution','global_endpoint_proved',True),
            ('wrong_slope_scope','nonzero_slope_required',False),
            ('fake_finite_proof','finite_checks_are_proof',True),
            ('bool_for_turn_count','author_approaches',True)]:
            d=dict(claims);d[key]=value
            negatives.append((label,'--claims',json.dumps(d)))
        extra=dict(claims);extra['unexpected']='field'
        negatives.append(('extra_claim_field','--claims',json.dumps(extra)))
        negatives.append(('malformed_json','--claims','{"schema":'))
        for label,idx,key,value in [
            ('wrong_projective_identity',1,'v','3'),
            ('false_rank_one',0,'claimed_max_rank',1),
            ('wrong_cf_recurrence',2,'q_next',6),
            ('malformed_rank_vector',0,'vectors',[[1,0]])]:
            p=json.loads(json.dumps(probes));p[idx][key]=value
            negatives.append((label,'--probes',json.dumps(p)))
        for label,flag,body in negatives:
            path=tmp/(label+'.json');path.write_text(body)
            for mode in MODES:
                code,data=call(ROOT,mode,[flag,path],cwd=tmp)
                require(code!=0 and data.get('status')=='FAIL',f'Negative accepted: {label} {mode}')
            results['negative_controls'].append({'control':label,'rejected_in':['normal','-O','-OO']})
        # A content mutation must be rejected by the actual integrity checker.
        damaged=tmp/'damaged';shutil.copytree(ROOT,damaged)
        damaged.chmod(0o755)
        for p in damaged.rglob('*'):
            p.chmod(0o755 if p.is_dir() else 0o644)
        with (damaged/'PROOF.md').open('a') as fh:
            fh.write('\nUnauthorized altered proof claim.\n')
        for mode in MODES:
            code,data=call(damaged,mode,cwd=tmp)
            require(code!=0 and data.get('status')=='FAIL','Proof integrity mutation accepted')
        results['negative_controls'].append({'control':'proof_byte_drift','rejected_in':['normal','-O','-OO']})
        # Only public files are copied; run from a separate unrelated directory.
        relocated=tmp/'read_only_release';shutil.copytree(ROOT,relocated)
        for p in relocated.rglob('*'):
            p.chmod(0o555 if p.is_dir() else 0o444)
        relocated.chmod(0o555)
        before=snapshot(relocated)
        probe="from pathlib import Path\nimport sys\ntry:\n Path(sys.argv[1]).write_text('forbidden')\nexcept PermissionError:\n sys.exit(0)\nsys.exit(3)\n"
        write_test=subprocess.run([sys.executable,'-c',probe,str(relocated/'FORBIDDEN_WRITE')],env=ENV,capture_output=True,text=True)
        require(write_test.returncode==0,'Relocation is not actually write-protected for this process')
        for mode in MODES:
            code,data=call(relocated,mode,cwd=tmp)
            require(code==0 and data==baseline,f'Read-only relocated replay failed {mode}: {data}')
            results['relocation'].append({'mode':mode or ['normal'],'status':'PASS','unrelated_cwd':True,'source_files_absent':True})
        require(snapshot(relocated)==before,'Relocation altered release bytes')
        results['read_only_write_attempt_rejected']=True
        results['read_only_files_unchanged']=True
        results['checker_output']=baseline
        # Restore modes only so TemporaryDirectory can clean up its private copies.
        for p in relocated.rglob('*'):
            p.chmod(0o755 if p.is_dir() else 0o644)
        relocated.chmod(0o755)
    print(json.dumps(results,indent=2,sort_keys=True))

if __name__=='__main__':
    try:
        main()
    except (ControlError,OSError,ValueError) as exc:
        print(json.dumps({'status':'FAIL','reason':str(exc)},sort_keys=True))
        sys.exit(1)
