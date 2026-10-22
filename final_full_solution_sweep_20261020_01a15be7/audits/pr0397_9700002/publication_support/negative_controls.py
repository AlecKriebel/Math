#!/usr/bin/env python3
"""Targeted controls of production replay guards; no scientific theorem is inferred."""
import argparse
import copy
import datetime as dt
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('pr397_replay', HERE/'replay.py')
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--candidate', type=Path, default=HERE/'candidate')
    parser.add_argument('--output', type=Path, required=True, help='New output directory, outside candidate')
    args = parser.parse_args()
    candidate = args.candidate.absolute()
    output = args.output.absolute()
    r.require(not output.resolve().is_relative_to(candidate.resolve()), 'Output must be outside candidate')
    output.mkdir(parents=True, exist_ok=False)
    binding, policy = r.load_controls(HERE)
    r.verify_candidate(candidate, binding)
    versions = {'python':'3.9.6', 'numpy':'2.0.2', 'scipy':'1.13.1'}
    expected = {name:r.strict_json((candidate/path).read_bytes()) for name,script,path,generated in r.COMPONENTS}
    base = copy.deepcopy(expected)
    base['portable'].update(versions)
    base['portable']['checks'][0] = copy.deepcopy(policy['portable_metadata']['public_projection'])
    results = []
    def positive(name, function):
        function()
        results.append({'name':name,'expected':'accept','observed':'accept','pass':True})
    def negative(name, function):
        try:
            function()
        except Exception as error:
            results.append({'name':name,'expected':'reject','observed':'reject','error_type':type(error).__name__,'reason':str(error),'pass':True})
        else:
            raise AssertionError('Substantive mutation incorrectly accepted: ' + name)
    def compare(comp, value):
        return r.compare_records(expected[comp], value, comp, policy, versions)
    def set_path(obj, path, value):
        keys = path.strip('/').split('/')
        parent = obj
        for key in keys[:-1]:
            parent = parent[int(key)] if type(parent) is list else parent[key]
        if type(parent) is list:
            parent[int(keys[-1])] = value
        else:
            parent[keys[-1]] = value
    for comp in ['turn1','turn2','portable']:
        positive('unchanged structured record: ' + comp, lambda comp=comp:compare(comp, base[comp]))
    for comp, rules in policy['float_tolerances'].items():
        for path, rule in rules.items():
            value = copy.deepcopy(base[comp])
            set_path(value, path, rule['historical_value'] + rule['absolute_tolerance']/2)
            positive('enumerated diagnostic within tolerance: ' + comp + path, lambda comp=comp,value=value:compare(comp,value))
            value = copy.deepcopy(base[comp])
            set_path(value, path, rule['historical_value'] + rule['absolute_tolerance']*4)
            negative('enumerated diagnostic outside tolerance: ' + comp + path, lambda comp=comp,value=value:compare(comp,value))
            value = copy.deepcopy(base[comp])
            set_path(value, path, True)
            negative('bool at numeric diagnostic: ' + comp + path, lambda comp=comp,value=value:compare(comp,value))
    for comp, path, value, label in [
        ('turn1','/all_assertions_passed',False,'top failure boolean'),
        ('turn1','/all_assertions_passed',1,'integer masquerading as pass boolean'),
        ('turn1','/seed',True,'bool masquerading as integer seed'),
        ('turn1','/seed',9700003,'changed deterministic seed'),
        ('turn1','/checks/0/cases',76,'changed integer case count'),
        ('turn1','/checks/0/pass',False,'nested failure boolean'),
        ('turn1','/checks/0/max_objective_error',1e-12,'unlisted float diagnostic'),
        ('turn1','/critical_window_profiles/0/m',101,'changed model size'),
        ('turn1','/critical_window_profiles/0/x',-1.9999999999999998,'changed model parameter'),
        ('portable','/checks/0/files',9,'wrong public input count'),
        ('portable','/checks/0/name','Different projection','wrong projection label'),
        ('portable','/checks/0/pass',1,'projection boolean changed to int'),
        ('portable','/numpy','999.0.0','reported environment differs from imported runtime'),
        ('portable','/checks/3/throughput','157/5','changed exact mixed-cut witness'),
        ('portable','/checks/7/k',1024,'changed first admissible family member'),
        ('turn2','/all_assertions_passed',False,'turn2 failure flag'),
    ]:
        actual = copy.deepcopy(base[comp]);set_path(actual,path,value)
        negative(label, lambda comp=comp,actual=actual:compare(comp,actual))
    for name, mutate in [
        ('missing top key',lambda v:v.pop('seed')),
        ('extra top key',lambda v:v.update(extra='unreviewed')),
        ('missing nested key',lambda v:v['checks'][0].pop('pass')),
        ('extra nested key',lambda v:v['checks'][0].update(extra=True)),
        ('shorter list',lambda v:v['checks'].pop()),
        ('longer list',lambda v:v['checks'].append({'pass':True})),
        ('list replaced by mapping',lambda v:v.update(checks={})),
    ]:
        actual = copy.deepcopy(base['turn1']);mutate(actual)
        negative(name, lambda actual=actual:compare('turn1',actual))
    for value in [float('nan'),float('inf'),-float('inf')]:
        actual = copy.deepcopy(base['turn1']);actual['checks'][2]['max_integral_error'] = value
        negative('nonfinite diagnostic ' + repr(value), lambda actual=actual:compare('turn1',actual))
    for data in ['{"x":NaN}', '{"x":Infinity}', '{"x":-Infinity}', '{"x":1e999}', '{"x":1,"x":2}']:
        negative('strict JSON ' + data, lambda data=data:r.strict_json(data))
    for value in ['../escape','/absolute','a/../escape','a//b','./a']:
        negative('unsafe binding path ' + value, lambda value=value:r.safe_relative(value))
    turn2_data = (candidate/'turns/turn_02/CHECKS.json').read_bytes()
    positive('turn2 exact raw bytes', lambda:r.compare_component(turn2_data,turn2_data,'turn2',policy,versions))
    negative('turn2 semantically same extra newline rejected', lambda:r.compare_component(turn2_data,turn2_data+b'\n','turn2',policy,versions))
    with tempfile.TemporaryDirectory(prefix='fixtures-',dir=output) as td:
        fixtures = Path(td)
        for label, mutation in [
            ('missing_file',lambda c:(c/'SOURCE_GATE.md').unlink()),
            ('extra_file',lambda c:(c/'extra.txt').write_text('unreviewed')),
            ('changed_proof',lambda c:(c/'turns/turn_02/CANDIDATE.md').write_text('changed theorem')),
            ('changed_frozen_output',lambda c:(c/'turns/turn_02/CHECKS.json').write_bytes(turn2_data+b'\n')),
            ('symlink_file',lambda c:((c/'SOURCE_GATE.md').unlink(),(c/'SOURCE_GATE.md').symlink_to(candidate/'SOURCE_GATE.md'))),
            ('extra_empty_directory',lambda c:(c/'extra_dir').mkdir()),
        ]:
            current = fixtures/label
            shutil.copytree(candidate,current)
            mutation(current)
            negative('candidate guard: '+label, lambda current=current:r.verify_candidate(current,binding))
            if label in ['missing_file','changed_proof']:
                evidence = output/('integration_'+label)
                run = subprocess.run([sys.executable,'-B',str(HERE/'replay.py'),'--candidate',str(current),'--output',str(evidence)],capture_output=True,text=True)
                (output/(label+'.stdout')).write_text(run.stdout)
                (output/(label+'.stderr')).write_text(run.stderr)
                receipt = r.strict_json((evidence/'receipt.json').read_bytes())
                r.require(run.returncode != 0 and receipt['status']=='failed' and receipt['components']==[], 'Integration did not fail before execution')
                results.append({'name':'integration retained failed-run evidence: '+label,'expected':'reject before execution','observed':'reject before execution','pass':True})
        control_home = fixtures/'controls'
        control_home.mkdir()
        shutil.copyfile(HERE/'candidate-binding.json',control_home/'candidate-binding.json')
        shutil.copyfile(HERE/'comparison-policy.json',control_home/'comparison-policy.json')
        (control_home/'comparison-policy.json').write_bytes((control_home/'comparison-policy.json').read_bytes()+b'\n')
        negative('immutable policy byte binding',lambda:r.load_controls(control_home))
        shutil.copyfile(HERE/'comparison-policy.json',control_home/'comparison-policy.json')
        (control_home/'candidate-binding.json').write_bytes((control_home/'candidate-binding.json').read_bytes()+b'\n')
        negative('immutable candidate binding byte guard',lambda:r.load_controls(control_home))
    result = {'timestamp':dt.datetime.now(dt.timezone.utc).isoformat(),'all_assertions_passed':True,'controls':len(results),'accepted_controls':sum(x['expected']=='accept' for x in results),'rejected_controls':sum(x['expected']!='accept' for x in results),'fixture_runtime_metadata':versions,'policy_sha256':r.POLICY_SHA256,'binding_sha256':r.BINDING_SHA256,'results':results,'scope':'Tests production replay guards and exact enumerated exceptions; not a mathematical or priority certificate. All candidate mutations were disposable copies.'}
    (output/'NEGATIVE_CONTROLS.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('results',)}))

if __name__ == '__main__':
    main()
