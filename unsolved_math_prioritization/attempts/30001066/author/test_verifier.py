#!/usr/bin/env python3
"""Exact geometry, semantic rejection, -O behavior and relocation tests."""
import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import verify
ROOT=Path(__file__).resolve().parent

def need(ok,msg):
    if not ok:raise RuntimeError(msg)

def run(args,expected,cwd=None):
    p=subprocess.run(args,cwd=cwd,text=True,capture_output=True)
    need((p.returncode==0)==expected,'unexpected exit '+str(args)+': '+p.stdout+p.stderr)
    if expected:need('"status": "PASS"' in p.stdout,'missing positive receipt')

def main():
    base=verify.load(ROOT/'certificate.json');dimensions=[2,3,4,5,8,12,20]
    for d in dimensions:verify.verify(verify.generated(d))
    mutations=[]
    def add(name,fn):
        d=copy.deepcopy(base);fn(d);mutations.append((name,json.dumps(d)))
    add('overclaimed_full_solution',lambda d:d.__setitem__('classification','resolved'))
    add('wrong_size',lambda d:d.__setitem__('claimed_minimal_size',5))
    add('boolean_dimension',lambda d:d.__setitem__('dimension',True))
    add('touching_slabs',lambda d:d['boxes'][1]['bounds'][-1].__setitem__(0,'1'))
    add('wrong_alternation',lambda d:d['boxes'][1]['bounds'].__setitem__(0,['0','1']))
    add('axis_excluded',lambda d:d['boxes'][0]['bounds'].__setitem__(1,['1','2']))
    add('flat_box',lambda d:d['boxes'][0]['bounds'].__setitem__(1,['0','0']))
    add('deleted_witness',lambda d:d['deletion_witnesses'].pop())
    add('stationary_motion',lambda d:(d['deletion_witnesses'][0].__setitem__('intercepts',['0','0']),d['deletion_witnesses'][0].__setitem__('slopes',['0','0'])))
    add('motion_too_large',lambda d:d['deletion_witnesses'][0].__setitem__('epsilon_max','100'))
    add('zero_motion_interval',lambda d:d['deletion_witnesses'][0].__setitem__('epsilon_max','0'))
    add('negative_motion_interval',lambda d:d['deletion_witnesses'][0].__setitem__('epsilon_max','-1'))
    add('missing_retained_hit',lambda d:d['deletion_witnesses'][0]['hits'].pop())
    add('wrong_hit_parameter',lambda d:d['deletion_witnesses'][0]['hits'][0].__setitem__('t','1000'))
    add('reversed_motion',lambda d:d['deletion_witnesses'][0].__setitem__('slopes',['-1','0']))
    add('zero_denominator',lambda d:d['deletion_witnesses'][0].__setitem__('epsilon_max','1/0'))
    add('noncanonical_fraction',lambda d:d['deletion_witnesses'][0].__setitem__('epsilon_max','2/28'))
    add('float_in_geometry',lambda d:d['boxes'][0]['bounds'][0].__setitem__(0,0.0))
    add('unknown_field',lambda d:d.__setitem__('trust_me',True))
    mutations.append(('duplicate_json_key',json.dumps(base)[:-1]+',"dimension":3}'))
    mutations.append(('malformed_json','{'))
    with tempfile.TemporaryDirectory(prefix='pinning_replay_') as td:
        td=Path(td);shutil.copy(ROOT/'verify.py',td/'verify.py');shutil.copy(ROOT/'certificate.json',td/'certificate.json')
        for flags in ([],['-O']):
            run([sys.executable,*flags,str(td/'verify.py')],True,cwd='/tmp')
            for name,payload in mutations:
                p=td/(name+'.json');p.write_text(payload)
                run([sys.executable,*flags,str(td/'verify.py'),str(p)],False,cwd='/tmp')
    print(json.dumps({'status':'PASS','tested_dimensions':dimensions,'semantic_or_input_mutations_rejected':len(mutations),
                      'modes':['normal','-O'],'relocation':'PASS','continuous_intervals_not_samples':True},sort_keys=True))
if __name__=='__main__':main()
