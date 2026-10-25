#!/usr/bin/env python3
"""Run selected unmodified published mathematical controls in an isolated copy.

Historical assessment bodies are not interpreted. The complete-package launcher
is deliberately not used: its historical verdict-dependent wrappers are not
needed for this review's mathematical replay. Byte hashing is not opinion reading.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, shutil, subprocess, sys, tempfile

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parents[1]/'sources/published-source/dfc_stability_verification/dfc_stability_verification'
def hashes(root):
    return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob('*')) if p.is_file()}
def main():
    started=datetime.now(timezone.utc).isoformat()
    before=hashes(SOURCE)
    manifest=json.loads((SOURCE/'MANIFEST.json').read_text())
    assert set(before)=={row['path'] for row in manifest['files']}|{'MANIFEST.json'}
    for row in manifest['files']:
        p=SOURCE/row['path']
        assert p.stat().st_size==row['bytes'] and before[row['path']]==row['sha256']
    tasks=[
        ('turn4','original/checks/turn4_checks.py','original/checks/turn4_output.json',[]),
        ('tridiagonal','reviews/foster_recheck_02/exact_falsification.py','reviews/foster_recheck_02/exact_falsification_output.json',[]),
        ('protocol_identity','reviews/priority_recheck_02/identity_controls.py','reviews/priority_recheck_02/identity_controls.stdout',[]),
        ('function_transfer','reviews/priority_recheck_02/theorem_transfer_control.py','reviews/priority_recheck_02/theorem_transfer_control.stdout',[]),
        ('false_protocol_identity','reviews/priority_recheck_02/identity_controls.py',None,['--false-identity']),
    ]
    rows=[]
    env=dict(os.environ); env['PYTHONDONTWRITEBYTECODE']='1'; env.pop('PYTHONOPTIMIZE',None)
    with tempfile.TemporaryDirectory(dir=HERE/'cache',prefix='isolated-') as tmp:
        work=Path(tmp)/'package'; shutil.copytree(SOURCE,work)
        for label,script,expected,args in tasks:
            begin=datetime.now(timezone.utc).isoformat()
            r=subprocess.run([sys.executable,str(work/script),*args],cwd=work,env=env,capture_output=True,text=True,timeout=240)
            (HERE/f'replay-{label}.stdout.txt').write_text(r.stdout)
            (HERE/f'replay-{label}.stderr.txt').write_text(r.stderr)
            if expected:
                assert r.returncode==0,(label,r.stderr)
                result=json.loads(r.stdout); frozen=json.loads((work/expected).read_text())
                result.pop('utc',None); frozen.pop('utc',None)
                assert result==frozen,label
            else:
                assert r.returncode!=0 and 'EXPECTED_REJECTION: Common Chunk is not DFC' in r.stderr
            rows.append({'label':label,'script':script,'script_sha256':before[script],
                         'started_utc':begin,'completed_utc':datetime.now(timezone.utc).isoformat(),
                         'exit_code':r.returncode,'matched_published_expected_output':expected is not None,
                         'intentional_rejection':expected is None})
            print(json.dumps(rows[-1]),flush=True)
    after=hashes(SOURCE); assert before==after
    result={'started_utc':started,'finished_utc':datetime.now(timezone.utc).isoformat(),
            'python':sys.version,'source':str(SOURCE),'manifest_payloads_verified':len(manifest['files']),
            'original_source_file_count':len(before),'all_original_source_hashes_unchanged':True,
            'source_sha256':before,'runs':rows,'complete_package_reproduction_claimed':False,
            'scope':'Selected unmodified mathematical controls, exact expected-output comparisons, one intentional rejection. Float transfer diagnostic is not an analytic proof. No old verdict bodies used.'}
    (HERE/'replay-results.json').write_text(json.dumps(result,indent=2)+'\n')
if __name__=='__main__': main()
