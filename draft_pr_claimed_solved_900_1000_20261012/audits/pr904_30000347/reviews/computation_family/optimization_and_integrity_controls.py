#!/usr/bin/env python3
"""Adversarial package controls; source packet is never modified."""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys,tempfile

HERE=Path(__file__).resolve().parent
ROOT=HERE/'submitted_working_copy'

def require(condition,message):
    if not condition: raise RuntimeError(message)

def run(command,cwd=None,env=None):
    child=subprocess.run(command,cwd=cwd,env=env,capture_output=True,text=True,timeout=60)
    return {'command':command,'returncode':child.returncode,'stdout':child.stdout,'stderr':child.stderr}

results=[]
with tempfile.TemporaryDirectory(prefix='pr904-controls-',dir=HERE) as temporary:
    tmp=Path(temporary)
    # Demonstrate the raw checker assertion boundary. Its documented gate compensates.
    checker=tmp/'checker'; checker.mkdir()
    source=(ROOT/'frozen_packet/checks/check_reduction.py').read_text()
    require(source.count('if not constraints:return 0')==1,'unexpected source text')
    (checker/'check_reduction.py').write_text(source.replace('if not constraints:return 0','return 0  # deliberately wrong hitting-set solver'))
    for optimized in (False,True):
        outcome=run([sys.executable]+(['-O'] if optimized else [])+[str(checker/'check_reduction.py')])
        results.append({'case':'raw_checker_wrong_solver','optimized':optimized,**outcome})
        require((outcome['returncode']==0)==optimized,'raw assertion control did not distinguish modes')
        if optimized:
            require(json.loads((checker/'check_results.json').read_text())['result']=='PASS','raw optimized checker did not report PASS')
    # A math-output edit and public-manifest update must still fail against the frozen anchors.
    packet=tmp/'packet'; shutil.copytree(ROOT,packet)
    manifest=packet/'PUBLIC_MANIFEST.json'; saved_manifest=manifest.read_bytes()
    target=packet/'frozen_packet/checks/check_results.json'; saved=target.read_bytes()
    result=json.loads(saved); result['checks']['tripartite_222_graphs_exact_optimum_checks']=3374
    target.write_text(json.dumps(result))
    m=json.loads(saved_manifest); data=target.read_bytes()
    m['files']['frozen_packet/checks/check_results.json']={'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
    manifest.write_text(json.dumps(m))
    for optimized in (False,True):
        outcome=run([sys.executable,'-I']+(['-O'] if optimized else [])+[str(packet/'verify_publication.py'),'--integrity-only'])
        require(outcome['returncode']!=0,'coordinated result/public-manifest tamper escaped')
        results.append({'case':'math_result_and_public_manifest_rewrite','optimized':optimized,**outcome})
    target.write_bytes(saved); manifest.write_bytes(saved_manifest)
    # A directory extra, omitted result, and symlinked payload are distinct file-boundary cases.
    target=packet/'frozen_packet/PROOF.md'; saved=target.read_bytes(); other=tmp/'other-proof'; other.write_bytes(saved)
    target.unlink(); target.symlink_to(other)
    for optimized in (False,True):
        outcome=run([sys.executable,'-I']+(['-O'] if optimized else [])+[str(packet/'verify_publication.py'),'--integrity-only'])
        require(outcome['returncode']!=0,'symlink payload was accepted')
        results.append({'case':'identical_byte_symlink_payload','optimized':optimized,**outcome})
    target.unlink(); target.write_bytes(saved)
    # Verify the precise isolation command used by replay defeats environment optimization.
    env=dict(os.environ,PYTHONOPTIMIZE='2')
    outcome=run([sys.executable,'-I','-c','import sys; print(sys.flags.optimize); assert False, "assertion sentinel"'],env=env)
    require(outcome['stdout'].strip()=='0' and outcome['returncode']!=0 and 'assertion sentinel' in outcome['stderr'],'-I did not retain assertions')
    results.append({'case':'child_isolation_under_PYTHONOPTIMIZE_2',**outcome})

out={'status':'PASS','cases':results,'interpretation':'Raw assertion-based scripts can report PASS under -O despite a deliberately wrong solver. Supported verify_publication.py compensates by explicit guards, byte/anchor checks, and replaying suites with -I and no -O. Integrity is against accidental/local mutations and the trusted verifier, not authenticity against coordinated replacement of verifier and all anchors.'}
(HERE/'optimization_and_integrity_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'cases':len(results),'raw_assert_erasure_demonstrated':True,'supported_gate_compensation_checked':True},indent=2))
