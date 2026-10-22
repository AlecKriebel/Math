#!/usr/bin/env python3
"""Reproduce the support proposal and exercise semantic failure controls.

Runs only local programs. Creates a NEW run directory inside this script's
directory, never replaces existing files, and never imports stored PASS results.
"""
import argparse
import ast
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys


def require(condition,message):
    if condition is not True:
        raise RuntimeError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def replace_once(text,old,new):
    require(text.count(old)==1,'mutation anchor is not unique: '+old)
    return text.replace(old,new,1)


def inventory(directory):
    return {str(path.relative_to(directory)):sha(path.read_bytes())
            for path in directory.rglob('*') if path.is_file()}


def execute(run_dir,name,script,optimized=False,args=()):
    command=[sys.executable,'-E','-B','-P']
    if optimized:
        command.append('-O')
    command += [str(script),*args]
    completed=subprocess.run(command,capture_output=True,timeout=120,check=False)
    stdout_path=run_dir/(name+'.stdout.json')
    stderr_path=run_dir/(name+'.stderr.txt')
    stdout_path.write_bytes(completed.stdout)
    stderr_path.write_bytes(completed.stderr)
    return {'name':name,'optimized':optimized,'returncode':completed.returncode,
            'stdout':stdout_path.name,'stdout_sha256':sha(completed.stdout),
            'stderr':stderr_path.name,'stderr_sha256':sha(completed.stderr),
            'json':json.loads(completed.stdout) if completed.returncode==0 else None,
            'error_json':json.loads(completed.stderr) if completed.stderr else None}


def run(name):
    base=Path(__file__).resolve().parent
    require(Path(name).name==name and name not in ('','.','..'),
            'run directory must be a single new name')
    destination=base/name
    destination.mkdir(exist_ok=False)
    exact=base/'verify_exact.py'
    geometry=base/'diagnose_geometry.py'
    exact_source=exact.read_text()
    geometry_source=geometry.read_text()
    originals={path.name:sha(path.read_bytes()) for path in (exact,geometry)}
    for path in (exact,geometry):
        require(not any(isinstance(node,ast.Assert) for node in ast.walk(ast.parse(path.read_text()))),
                path.name+' contains an assertion-only check')
    cases=[]
    for optimized in (False,True):
        result=execute(destination,'exact_'+('optimized' if optimized else 'ordinary'),exact,optimized)
        require(result['returncode']==0,'exact checker failed')
        require(result['json']['optimization_level']==int(optimized),'unexpected optimization level')
        require(result['json']['exact_checks']==len(result['json']['checks'])>0,
                'missing exact check records')
        require(all(record['residual']=='0' for record in result['json']['checks']),
                'nonzero recorded exact residual')
        require(result['json']['code_sha256']==originals[exact.name],'wrong exact code pin')
        cases.append(result)
    ordinary=[case for case in cases if case['name']=='exact_ordinary'][0]['json']
    optimized=[case for case in cases if case['name']=='exact_optimized'][0]['json']
    require(ordinary['checks']==optimized['checks'],'optimization changed exact checks')

    result=execute(destination,'geometry_optimized',geometry,True)
    require(result['returncode']==0,'optimized geometric diagnostic failed')
    require(result['json']['optimization_level']==1,'geometry not actually optimized')
    require(len(result['json']['target_families'])==8,'missing selected default families')
    require(result['json']['code_sha256']==originals[geometry.name],'wrong geometry code pin')
    cases.append(result)

    mutations=[
        ('wrong_focal_area_factor',exact_source,
         'edge = translated_det/(2*distance_product**2)',
         'edge = translated_det/(distance_product**2)',
         'inverted_edge_shoelace_contribution_divided_by_b'),
        ('wrong_local_decomposition',exact_source,
         'L = (1 - k**2 * t * x)',
         'L = (1 - 2*k**2 * t * x)',
         'generic_local_rational_decomposition'),
        ('wrong_boundary_focus_sign',exact_source,
         "zero('boundary_inverse_minus_P', Im-(8*root2+root3)/80)",
         "zero('boundary_inverse_minus_P', Im-(8*root2-root3)/80)",
         'boundary_inverse_minus_P'),
        ('nonfinite_geometric_vertex',geometry_source,
         'A=area(points)',
         'points[0]=(mp.nan,points[0][1])\n        A=area(points)',
         'nonfinite scalar')]
    mutation_pins=[]
    for label,source,old,new,expected_error in mutations:
        script=destination/(label+'.py')
        content=replace_once(source,old,new).encode()
        with script.open('xb') as stream:
            stream.write(content)
        mutation_pins.append({'name':script.name,'sha256':sha(content)})
        result=execute(destination,label,script,True)
        require(result['returncode']==1,label+' did not exit with verification failure')
        require(not result['json'],label+' emitted an accepted result')
        require(result['error_json']['status']=='FAIL',label+' emitted no failure status')
        require(expected_error in result['error_json']['error'],label+' failed for the wrong reason')
        cases.append(result)

    # Exercise true overwrite protection on a fresh sentinel in this run directory.
    protected=destination/'protected_existing_file.txt'
    with protected.open('x') as stream:
        stream.write('This preexisting file must remain byte-for-byte unchanged.\n')
    sentinel=protected.read_bytes()
    for label,script in [('exact',exact),('geometry',geometry)]:
        result=execute(destination,label+'_output_exists',script,True,('--output',str(protected)))
        require(result['returncode']==1,label+' silently accepted existing output')
        require(result['error_json']['error_type']=='FileExistsError',label+' failed for the wrong reason')
        require(protected.read_bytes()==sentinel,label+' overwrote protected output')
        cases.append(result)

    # Invalid physical/control inputs must fail before pretending to check a theorem.
    result=execute(destination,'insufficient_stress_precision',geometry,True,('--stress','--dps','90'))
    require(result['returncode']==1,'insufficient stress precision accepted')
    require('requires --dps at least 130' in result['error_json']['error'],
            'stress precision failed for the wrong reason')
    cases.append(result)
    domain_script=destination/'invalid_physical_inputs.py'
    domain_source='''import json,runpy
from pathlib import Path
ns=runpy.run_path(str(Path(__file__).resolve().parent.parent/'diagnose_geometry.py'),run_name='verification_import')
mp=ns['mp']
tests=[('nan_modulus',lambda:ns['geometry'](mp.nan,8,1),'nonfinite scalar'),
       ('degenerate_modulus',lambda:ns['geometry'](mp.mpf(1),8,1),'strictly between'),
       ('repeated_label',lambda:ns['geometry'](mp.mpf('0.8'),12,2),'least period'),
       ('wrong_parity_as_target',lambda:ns['family'](mp.mpf('0.8'),6,1,['0'],mp.mpf('1e-20'),True),'divisible by four')]
records=[]
for name,call,message in tests:
    try:
        call()
    except ns['VerificationError'] as error:
        if message not in str(error):
            raise RuntimeError(name+': wrong rejection')
        records.append(name)
    else:
        raise RuntimeError(name+': invalid physical input accepted')
print(json.dumps({'status':'PASS','rejected_cases':records}))
'''
    with domain_script.open('x') as stream:
        stream.write(domain_source)
    result=execute(destination,'invalid_physical_inputs',domain_script,True)
    require(result['returncode']==0 and len(result['json']['rejected_cases'])==4,
            'physical input rejection controls failed')
    cases.append(result)
    require({path.name:sha(path.read_bytes()) for path in (exact,geometry)}==originals,
            'original proposal programs changed during execution')
    # Each checker defaults to stdout; execute() captures this explicitly.
    # The exact checker and diagnostic themselves never write sidecar results.
    compact=[]
    for case in cases:
        compact.append({key:value for key,value in case.items()
                        if key not in ('json','error_json')})
    result={'schema':'pr207-portable-fail-closed-validation-v1','status':'PASS',
            'created_utc':datetime.now(timezone.utc).isoformat(),
            'python':sys.version,'source_pins':originals,'cases':compact,
            'harness_sha256':sha(Path(__file__).read_bytes()),
            'semantic_mutation_pins':mutation_pins,
            'checks':'Three damaged exact mathematical formulas fail under -O; '
                     'an injected NaN vertex fails under -O; ordinary and optimized '
                     'exact check inventories agree; both programs reject existing '
                     'output without changing its bytes; stress runs reject '
                     'insufficient precision. No assertion nodes occur in either '
                     'verification program.'}
    # The manifest covers every file already created in this new directory.
    result['generated_artifacts']=inventory(destination)
    with (destination/'VALIDATION_RESULT.json').open('x') as stream:
        stream.write(json.dumps(result,indent=2,allow_nan=False)+'\n')
    return {'status':'PASS','run_directory':str(destination),
            'cases':len(cases),'exact_checks':ordinary['exact_checks'],
            'validation_sha256':sha((destination/'VALIDATION_RESULT.json').read_bytes())}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-directory',default='validation_run_01',metavar='NEW_NAME')
    args=parser.parse_args()
    try:
        print(json.dumps(run(args.run_directory),indent=2,allow_nan=False))
    except Exception as error:
        sys.stderr.write(json.dumps({'status':'FAIL','error_type':type(error).__name__,
                                     'error':str(error)},allow_nan=False)+'\n')
        return 1
    return 0


if __name__=='__main__':
    sys.exit(main())
