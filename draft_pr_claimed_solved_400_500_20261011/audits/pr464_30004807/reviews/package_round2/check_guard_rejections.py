#!/usr/bin/env python3
"""Independent negative probes, with all altered payloads in private temporaries."""
from pathlib import Path
import copy
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile

OUT=Path(__file__).resolve().parent
AUDIT=OUT.parent.parent
SOURCE=AUDIT/'package/verification'
spec=importlib.util.spec_from_file_location('round2_reviewed_driver',SOURCE/'run_verification.py')
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
records=[]

def need(ok,label):
    if not ok:raise RuntimeError(label)

def rejects(label,call):
    try:call()
    except module.VerificationError:
        records.append({'case':label,'intended_VerificationError':True,'unexpected_crash':False})
    else:raise RuntimeError('accepted '+label)

valid={'all_passed':True,'exact_check_count':3,'checks':{'x':True,'y':True,'z':True}}
module.check_bool_result(valid,valid,3,'exact_check_count')
records.append({'case':'valid_three_named_booleans_control','accepted':True})
for key,value in [('all_passed',False),('all_passed',1),('all_passed','true'),('exact_check_count',True),('exact_check_count',3.0),('exact_check_count','3'),('exact_check_count',2),('exact_check_count',4)]:
    item=copy.deepcopy(valid);item[key]=value
    rejects(key+'_'+repr(value),lambda item=item:module.check_bool_result(item,valid,3,'exact_check_count'))
for field in ['all_passed','checks','exact_check_count']:
    item=copy.deepcopy(valid);del item[field]
    rejects('missing_'+field,lambda item=item:module.check_bool_result(item,valid,3,'exact_check_count'))
for value in [False,1,0,None,'true',[],{}]:
    item=copy.deepcopy(valid);item['checks']['y']=value
    rejects('non_true_boolean_'+repr(value),lambda item=item:module.check_bool_result(item,valid,3,'exact_check_count'))
for checks in [{'x':True,'y':True},{'x':True,'y':True,'different':True},{'x':True,'y':True,'z':True,'extra':True},[]]:
    item=copy.deepcopy(valid);item['checks']=checks
    rejects('name_inventory_'+repr(checks),lambda item=item:module.check_bool_result(item,valid,3,'exact_check_count'))
rejects('duplicate_outer_JSON_key',lambda:module.parse_json('{"all_passed":true,"all_passed":false}'))
rejects('duplicate_nested_JSON_key',lambda:module.parse_json('{"checks":{"x":true,"x":false}}'))

with tempfile.TemporaryDirectory(prefix='round2 private guard ',dir=OUT/'private_sources') as tmp:
    base=Path(tmp).resolve();root=base/'path_root';root.mkdir()
    (root/'valid.txt').write_text('valid payload\n')
    module.ROOT=root
    need(module.safe_path('valid.txt')==root/'valid.txt','canonical path control')
    records.append({'case':'canonical_existing_path_control','accepted':True})
    for name in ['../valid.txt','/valid.txt','a/./b','a//b','private_sources/a','private_cases/a','mutation_fixtures/a','.venv/a','.secrets/a','__pycache__/a','']:
        rejects('unsafe_path_'+name,lambda name=name:module.safe_path(name))
    outside=base/'outside';outside.mkdir();(outside/'valid.txt').write_text('outside\n')
    (root/'leaf_link').symlink_to(outside/'valid.txt')
    (root/'ancestor').symlink_to(outside,target_is_directory=True)
    rejects('symlink_leaf',lambda:module.safe_path('leaf_link'))
    rejects('symlink_ancestor',lambda:module.safe_path('ancestor/valid.txt'))

    # Exercise the actual CLI dispatch, rather than treating an arbitrary crash
    # as evidence. Every change is restricted to a disposable private copy.
    for case in ['payload_changed','payload_missing','payload_symlink','manifest_duplicate_path','manifest_wrong_byte_boolean','manifest_noncanonical_path','manifest_forbidden_venv','manifest_duplicate_json_key']:
        folder=base/case
        shutil.copytree(SOURCE,folder)
        manifest=folder/'VERIFICATION_MANIFEST.json'
        data=json.loads(manifest.read_bytes())
        target=folder/'controls/check_geometry.py'
        if case=='payload_changed':target.write_bytes(target.read_bytes()+b'\n')
        elif case=='payload_missing':target.unlink()
        elif case=='payload_symlink':
            target.unlink();target.symlink_to(SOURCE/'controls/check_geometry.py')
        elif case=='manifest_duplicate_path':data['files'][1]['path']=data['files'][0]['path']
        elif case=='manifest_wrong_byte_boolean':data['files'][0]['bytes']=True
        elif case=='manifest_noncanonical_path':data['files'][0]['path']='a/./b'
        elif case=='manifest_forbidden_venv':data['files'][0]['path']='venv/valid.txt'
        elif case=='manifest_duplicate_json_key':
            original=manifest.read_text()
            manifest.write_text(original.replace('"manifest_self_hash_excluded": true','"manifest_self_hash_excluded": true, "manifest_self_hash_excluded": false'))
        if case.startswith('manifest_') and case!='manifest_duplicate_json_key':manifest.write_text(json.dumps(data))
        proc=subprocess.run([sys.executable]+(['-O'] if sys.flags.optimize else [])+[str(folder/'run_verification.py')],capture_output=True,cwd=folder,timeout=30)
        need(proc.returncode==2 and proc.stdout==b'' and proc.stderr.startswith(b'VerificationError: '),case+' actual CLI intended rejection')
        records.append({'case':'actual_cli_'+case,'exit_code':proc.returncode,'intended_VerificationError':True,'unexpected_crash':False})

print(json.dumps({'verdict':'PASS','probe_count':len(records),'actual_cli_rejections':8,'all_inputs_private_and_removed':True,'external_calls':False,'records':records},indent=2,sort_keys=True))
