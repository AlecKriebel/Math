"""Fresh finite fault tests. Invalid fixtures are confined to ignored private_sources."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
BASE = ROOT / 'private_sources/zip_extract/verification'
FIXTURES = ROOT / 'private_sources/invalid_fixtures'

def digest(data):
    return hashlib.sha256(data).hexdigest()

def execute(path, optimized, cwd):
    command = [sys.executable] + (['-O'] if optimized else []) + [str(path)]
    return subprocess.run(command, cwd=cwd, capture_output=True, timeout=300)

def main():
    if FIXTURES.exists():
        shutil.rmtree(FIXTURES)
    FIXTURES.mkdir(exist_ok=True)
    faults = [
        ('retained_missing_face', 'check_exact.py', 'tt = tuple(sorted(t))', 'tt = tuple(sorted(t))\n    s.add(tt)', 'tt not in s'),
        ('zero_parameters', 'check_exact.py', 'row[idx[mv]]=pow(v+1,power,p)', 'row[idx[mv]]=0', "sd['dimension']"),
        ('lost_flores_crossings', 'check_exact.py', 'crossings+=1', 'crossings+=0', 'crossings==2*d+3'),
        ('empty_homological_fill', 'check_independent.py', 'return {pool[j] for j in solve(cols,target)}', 'return set()', 'not bd'),
        ('wrong_complement_homology', 'check_independent.py', 'return [len(vs)-r1-1,len(es)-r1-r2]', 'return [1,len(es)-r1-r2]', 'betti01(complement)'),
        ('lost_transferred_crossings', 'check_independent.py', 'crossings+=tuple(u[::2]) in (s,t)', 'crossings+=0', 'crossings%2==1'),
        ('wrong_dense_rank', 'check_bitmask_controls.py', 'relation_rank = rank(rows,prime)', 'relation_rank = rank(rows,prime)+1', 'Source quotient dimensions'),
        ('wrong_rational_circuit', 'check_bitmask_controls.py', 'Fraction(1,math.prod(x-y for y in points if y!=x))', 'Fraction(2 if x==points[0] else 1,math.prod(x-y for y in points if y!=x))', 'Circuit affine dependence fails'),
        ('empty_triangle_filling', 'check_bitmask_controls.py', 'result={triangles[col] for r,col in pivots if matrix[r][-1]}', 'result=set()', 'Returned filling has wrong boundary'),
    ]
    results=[]
    for name, script, old, new, diagnostic in faults:
        source=(BASE/'checks'/script).read_text()
        if source.count(old)!=1:
            raise RuntimeError('Nonunique mutation anchor: '+name)
        mutant=source.replace(old,new)
        path=FIXTURES/(name+'.py')
        path.write_text(mutant)
        for optimized in [False,True]:
            run=execute(path,optimized,FIXTURES)
            stderr=run.stderr.decode(errors='replace')
            intended=run.returncode!=0 and 'RuntimeError:' in stderr and diagnostic in stderr
            results.append({'fault':name,'script':script,'mode':'optimized' if optimized else 'normal',
                            'source_sha256':digest(source.encode()),'mutant_sha256':digest(mutant.encode()),
                            'exit_code':run.returncode,'intended_RuntimeError':intended,
                            'last_diagnostic':stderr.splitlines()[-1] if stderr else '',
                            'invalid_fixture_distributed':False})
            if not intended:
                raise RuntimeError('Fault was not caught at intended condition: '+name+' '+stderr[-500:])
    driver=[]
    for name in ['changed_program','changed_expected','escaping_path','missing_file','wrong_expected_output','unexpected_stderr','outside_symlink','inside_symlink_probe']:
        case_root=FIXTURES/name
        shutil.copytree(BASE,case_root,dirs_exist_ok=True)
        manifest=json.loads((case_root/'CONTROL_MANIFEST.json').read_text())
        manifest['cases']=manifest['cases'][:1]
        case=manifest['cases'][0]
        script=case_root/case['script']; expected=case_root/case['expected']
        expected_error=None
        if name=='changed_program':
            script.write_text(script.read_text()+'\n# corruption\n'); expected_error='Control file checksum mismatch'
        elif name=='changed_expected':
            expected.write_bytes(expected.read_bytes()+b' '); expected_error='Control file checksum mismatch'
        elif name=='escaping_path':
            case['script']='../outside.py'; expected_error='Control path escapes package'
        elif name=='missing_file':
            script.unlink(); expected_error='Missing regular control file'
        elif name=='wrong_expected_output':
            expected.write_bytes(expected.read_bytes()+b' '); case['expected_sha256']=digest(expected.read_bytes()); expected_error='output differs from recorded bytes'
        elif name=='unexpected_stderr':
            script.write_text(script.read_text()+"\nimport sys\nsys.stderr.write('unexpected diagnostic')\n");case['script_sha256']=digest(script.read_bytes()); expected_error='produced unexpected diagnostic output'
        elif name=='outside_symlink':
            target=FIXTURES/'outside_control.py'; target.write_bytes(script.read_bytes());script.unlink();script.symlink_to(target.resolve());expected_error='Control path escapes package'
        else:
            alias=case_root/'expected/author_alias.json';alias.symlink_to(expected.resolve());case['expected']='expected/author_alias.json'
        (case_root/'CONTROL_MANIFEST.json').write_text(json.dumps(manifest))
        for optimized in [False,True]:
            run=execute(case_root/'reproduce.py',optimized,case_root)
            stderr=run.stderr.decode(errors='replace')
            intended=(run.returncode!=0 and 'RuntimeError:' in stderr and expected_error in stderr) if expected_error else run.returncode==0
            driver.append({'fault':name,'mode':'optimized' if optimized else 'normal','exit_code':run.returncode,
                           'expected_behavior_observed':intended,'expected_rejection':expected_error,
                           'last_diagnostic':stderr.splitlines()[-1] if stderr else '',
                           'note':'Benign in-root symlink is accepted after resolve; optional contract clarity, no byte mismatch.' if not expected_error else ''})
            if not intended:raise RuntimeError('Driver control unexpected: '+name+' '+stderr[-500:])
    output={'utc':datetime.now(timezone.utc).isoformat(),'python':sys.version.split()[0],
            'scope':'Actual finite computational faults and disposable integrity/path tests; no universal mathematical certification.',
            'mathematical_faults':results,'driver_faults':driver,'all_18_mathematical_fault_executions_rejected':all(r['intended_RuntimeError'] for r in results),
            'all_14_intended_driver_rejections_observed':all(r['expected_behavior_observed'] for r in driver if r['expected_rejection']),
            'in_root_symlink_probe':'accepted in both modes, same hash-bound bytes; not counted as a rejected fault'}
    (ROOT/'FRESH_NEGATIVE_CONTROLS.json').write_text(json.dumps(output,indent=2)+'\n')
    print('18 mathematical fault executions rejected; 14 driver rejection executions rejected; in-root symlink behavior recorded.')

if __name__=='__main__':
    main()
