#!/usr/bin/env python3
"""Selected published mathematical replays; historical verdict wrappers omitted."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,shutil,subprocess,sys,tempfile
import sympy
HERE=Path(__file__).resolve().parent;PKG=HERE.parents[1]/'sources/published-source/satoh_filtration_verification'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def hashes():return {str(p.relative_to(PKG)):sha(p) for p in sorted(PKG.rglob('*')) if p.is_file()}
def main():
    before=hashes();start=datetime.now(timezone.utc).isoformat()
    native='native/unsolved_math_prioritization/attempts/30003703'
    jobs=[('native',native+'/release/verify.py',native+'/release/verification.json'),
          ('freegroup','reviews/freegroup_01/controls.py','reviews/freegroup_01/controls.normal.json'),
          ('matrix_ideal','reviews/matrix_ideal_01/matrix_controls.py','reviews/matrix_ideal_01/MATRIX_CONTROLS.normal.json')]
    out=[];env=dict(os.environ);env['PYTHONDONTWRITEBYTECODE']='1';env.pop('PYTHONOPTIMIZE',None)
    with tempfile.TemporaryDirectory(dir=HERE/'cache',prefix='satoh-replay-') as temp:
        work=Path(temp)/'source';shutil.copytree(PKG,work)
        for name,script,expected in jobs:
            begin=datetime.now(timezone.utc).isoformat()
            r=subprocess.run([sys.executable,'-B',str(work/script)],cwd=work,env=env,capture_output=True,timeout=240)
            (HERE/f'replay-{name}.stdout.txt').write_bytes(r.stdout);(HERE/f'replay-{name}.stderr.txt').write_bytes(r.stderr)
            assert r.returncode==0,(name,r.stderr.decode())
            assert json.loads(r.stdout)==json.loads((work/expected).read_text()),name
            out.append({'name':name,'script':script,'script_sha256':before[script],'expected_output':expected,
                        'expected_output_sha256':before[expected],'exit_code':r.returncode,'json_exact_match':True,
                        'started_utc':begin,'finished_utc':datetime.now(timezone.utc).isoformat()})
            print(json.dumps(out[-1]),flush=True)
    assert hashes()==before
    result={'started_utc':start,'finished_utc':datetime.now(timezone.utc).isoformat(),'python':sys.version,'sympy':sympy.__version__,
            'runs':out,'source_sha256':before,'source_files':len(before),'all_sources_unchanged':True,
            'full_package_replay_claimed':False,'scope':'Three unmodified mathematical controls only; no historical acceptance/priority wrapper or package builder executed. Source custody uses opaque byte hashes.'}
    (HERE/'replay-results.json').write_text(json.dumps(result,indent=2)+'\n')
if __name__=='__main__':main()
