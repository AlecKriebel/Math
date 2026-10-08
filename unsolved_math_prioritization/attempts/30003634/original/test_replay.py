#!/usr/bin/env python3
"""Adversarial subprocess replay; only the system temporary directory is written."""
import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

class TestFailure(Exception):
    pass

def check(value, message):
    if not value:
        raise TestFailure(message)

def run():
    root = Path(__file__).resolve().parent
    original = json.loads((root/'certificate.json').read_text())
    cases = {}
    for name, key, value in [('signature_zero','signature',0), ('wrong_derived','derived_level',2),
                              ('wrong_n','n',0), ('wrong_m','m',4), ('wrong_inertia','goeritz_inertia',[24,24,0]),
                              ('wrong_linking','pairwise_linking',[1,0,0]), ('wrong_correction','goeritz_correction',1),
                              ('wrong_determinant','goeritz_determinant',0), ('boolean_integer','n',True),
                              ('float_integer','signature',-2.0)]:
        x=copy.deepcopy(original);x[key]=value;cases[name]=json.dumps(x)
    for name,key,index in [('bad_word','word',0),('bad_meyer','meyer_terms',1),('bad_burau','burau_matrix',0),('bad_syllable','syllables',0)]:
        x=copy.deepcopy(original);x[key][index]+=1;cases[name]=json.dumps(x)
    x=copy.deepcopy(original);x['goeritz'][0][0]+=1;cases['bad_matrix']=json.dumps(x)
    x=copy.deepcopy(original);x['goeritz_pivots'][0]='3';cases['bad_pivot']=json.dumps(x)
    x=copy.deepcopy(original);x['extra']='not allowed';cases['unknown_field']=json.dumps(x)
    x=copy.deepcopy(original);del x['word'];cases['missing_field']=json.dumps(x)
    cases['duplicate_key']='{"n":1,'+json.dumps(original)[1:]
    cases['malformed_json']='{"n":'
    cases['wrong_root']='[]'
    cases['nonfinite']='{"n":NaN}'
    modes=[('normal',[],{}),('O',['-O'],{}),('OO',['-OO'],{}),('env_2',[],{'PYTHONOPTIMIZE':'2'})]
    accepted=[];rejected=[];outputs=[]
    with tempfile.TemporaryDirectory(prefix='pure_braid_replay_') as tmp:
        tmp=Path(tmp);rel=tmp/'relocated';rel.mkdir()
        for name in ['verify.py','certificate.json']:
            shutil.copy2(root/name,rel/name);(rel/name).chmod(0o444)
        rel.chmod(0o555)
        before={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in rel.iterdir()}
        for name,data in cases.items():(tmp/(name+'.json')).write_text(data)
        for label,flags,extra in modes:
            env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env.update(extra);env['PYTHONDONTWRITEBYTECODE']='1'
            args=[sys.executable,'-B',*flags,str(rel/'verify.py')]
            good=subprocess.run(args,cwd=tmp,env=env,capture_output=True,text=True,timeout=90)
            check(good.returncode==0 and good.stderr=='',label+' valid replay failed: '+good.stderr)
            result=json.loads(good.stdout)
            check(result['status']=='PASS_EXACT_CERTIFICATE' and result['signature']==-2,label+' false valid result')
            outputs.append(good.stdout);accepted.append(label)
            for name in cases:
                bad=subprocess.run(args+[str(tmp/(name+'.json'))],cwd=tmp,env=env,capture_output=True,text=True,timeout=90)
                check(bad.returncode!=0 and 'REJECT:' in bad.stderr and 'PASS_EXACT_CERTIFICATE' not in bad.stdout,label+' accepted '+name)
                rejected.append(label+':'+name)
        after={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in rel.iterdir()}
        check(before==after,'read-only relocation changed files')
        rel.chmod(0o755)
    check(len(set(outputs))==1,'optimization-dependent result')
    return {'status':'PASS_ADVERSARIAL_REPLAY','valid_modes':accepted,'rejected_cases':len(rejected),
            'mutation_names':list(cases),'read_only_permission_relocation':True,'relocated_bytes_unchanged':True,
            'output_sha256':hashlib.sha256(outputs[0].encode()).hexdigest()}

if __name__=='__main__':
    try:
        print(json.dumps(run(),sort_keys=True,indent=2))
    except (TestFailure,ValueError,OSError,subprocess.SubprocessError) as error:
        print('FAIL: '+str(error),file=sys.stderr);sys.exit(1)
