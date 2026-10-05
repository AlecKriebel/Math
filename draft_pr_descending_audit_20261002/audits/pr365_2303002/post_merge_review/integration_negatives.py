#!/usr/bin/env python3
"""Scope/status/mode adversarial controls; no finite theorem claim."""
import copy,json,pathlib
from capture import ROOT
A=ROOT.parent;F=A/'clean_final_adversary';P='unsolved_math_prioritization/attempts/2303002/';Q='unsolved_math_prioritization/QUEUE.md'
live=json.loads((F/'05_prepared_gate.json').read_bytes());bs=live['bindings'];expected={b['path']:b for b in bs}
old=(__import__('gzip').decompress((F/'captures/prepared_v2_base_queue.stdout.gz').read_bytes()))
new=(pathlib.Path('/Users/alec/Documents/Math')/Q).read_bytes()
def valid_queue(a,b):
    x=a.splitlines(keepends=True);y=b.splitlines(keepends=True)
    if len(x)!=1966 or len(x)!=len(y):return False
    if [i for i,(p,q) in enumerate(zip(x,y)) if p!=q]!=[404]:return False
    c=x[404].split(b'|');d=y[404].split(b'|')
    if len(c)!=len(d) or c[2].strip()!=b'2303002 / AMR-022-3002':return False
    if [i for i,(p,q) in enumerate(zip(c,d)) if p!=q]!=[8]:return False
    return c[8].strip()==b'queued' and d[8].strip()==b'already_solved' and c[9].strip()==d[9].strip()==b'0/5'
def valid_scope(rows):
    return len(rows)==19 and len({b['path'] for b in rows})==19 and all(b['path'] in expected and b==expected[b['path']] for b in rows)
controls=[]
def reject(name,c):assert not c,name;controls.append(name)
assert valid_queue(old,new) and valid_scope(bs)
reject('wrong discovery turn cell',valid_queue(old,new.replace(b'| already_solved | 0/5 |',b'| already_solved | 1/5 |')))
reject('wrong status',valid_queue(old,new.replace(b'| already_solved | 0/5 |',b'| researching | 0/5 |')))
reject('wrong target identity',valid_queue(old,new.replace(b'2303002 / AMR-022-3002',b'2303003 / AMR-022-3003')))
reject('second queue line mutation',valid_queue(old,new+b'\n'))
reject('queue unchanged',valid_queue(old,old))
wrong=copy.deepcopy(bs);wrong[1]['mode']='100755';reject('unexpected executable mode',valid_scope(wrong))
wrong=copy.deepcopy(bs);wrong[1]['kind']='commit';wrong[1]['mode']='160000';reject('submodule substitution',valid_scope(wrong))
wrong=copy.deepcopy(bs);wrong[1]['path']=P+'UNREVIEWED.txt';reject('scope transfer to added file',valid_scope(wrong))
wrong=copy.deepcopy(bs);wrong[1]=copy.deepcopy(wrong[0]);reject('duplicate binding hides omitted target',valid_scope(wrong))
wrong=copy.deepcopy(bs);wrong[1]['sha256']='0'*64;reject('mathematical bytes changed',valid_scope(wrong))
reject('extra twentieth file',valid_scope(bs+[copy.deepcopy(bs[0])]))
reject('only eighteen files',valid_scope(bs[:-1]))
print(json.dumps(dict(rejected_integration_overclaims=controls,negative_controls=len(controls),finite_controls_prove_theorem=False),indent=2))
