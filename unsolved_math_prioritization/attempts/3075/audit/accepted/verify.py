#!/usr/bin/env python3
"""Verify integrity and the complete authored finite certificate."""
import hashlib,json,pathlib,sys,types
ROOT=pathlib.Path(__file__).resolve().parent
EXPECTED_FILES={'REPORT.md','VERIFYING.md','arrangement.py','verify_planar.py','verify.py',
                'verify_inputs.py','witness.json','SOURCE_PINS.json','IDENTITY.json','AUTHOR_CHECKS.json'}

def need(x,msg):
    if not x:raise ValueError(msg)

def main():
    manifest=json.loads((ROOT/'MANIFEST.json').read_text())
    need(set(manifest)==EXPECTED_FILES,'Manifest file set differs')
    verified={}
    for name,pin in manifest.items():
        b=(ROOT/name).read_bytes()
        need(len(b)==pin['bytes'],'Size mismatch: '+name)
        need(hashlib.sha256(b).hexdigest()==pin['sha256'],'SHA-256 mismatch: '+name)
        verified[name]=b
    # Compile the already hash-checked bytes, independent of sys.path and .pyc caches.
    def verified_module(name):
        module=types.ModuleType('_verified_'+name)
        module.__file__=str(ROOT/(name+'.py'))
        exec(compile(verified[name+'.py'],module.__file__,'exec'),module.__dict__)
        return module
    enumerate_arrangement=verified_module('arrangement').enumerate_arrangement
    inspect=verified_module('verify_planar').inspect
    x=json.loads((ROOT/'witness.json').read_text())
    rows=[[1,1,5],[1,2,-1],[1,4,2],[1,5,-2],[1,7,2],[1,8,-5],[1,9,-1],[1,10,-2]]
    need(x['hyperplanes']==rows and x['delete_zero_based']==5,'Witness identity mismatch')
    need(x['equation_convention']=='a*x+b*y=c','Wrong equation convention')
    outputs={}
    for label,rs in [('full',rows),('deletion',rows[:5]+rows[6:])]:
        a=enumerate_arrangement(rs,True);b=inspect(rs)
        a['polygons']=b['cells']
        need(a==x[label],'Full certificate mismatch: '+label)
        graph={tuple(c['signs']):(c['facets'],c['diameter']) for c in a['cells']}
        polygon={tuple(c['signs']):(c['sides'],c['diameter']) for c in b['cells']}
        need(graph==polygon,'Independent chamber certificates differ')
        for k in ('bounded_cells','diameter_sum','facet_histogram'):
            need(a[k]==b[k],'Independent aggregate differs: '+k)
        outputs[label]={k:a[k] for k in ('bounded_cells','diameter_sum','average','defect','facet_histogram')}
    need(outputs['full']['diameter_sum']==36 and outputs['deletion']['diameter_sum']==23,'Unexpected sums')
    need(36-23>2*(21-15),'Claimed obstruction absent')
    deletion_defects=[enumerate_arrangement(rows[:j]+rows[j+1:])['defect'] for j in range(8)]
    need(deletion_defects==[6,5,5,6,6,7,6,6],'Other deletion defects differ')
    # Exact sanity tests in dimensions 2, 3, 4; no exhaustive-class claim.
    for d in (2,3,4):
        for n in (d+1,d+2):
            rs=[[t**k for k in range(d)]+[t**d] for t in range(1,n+1)]
            z=enumerate_arrangement(rs)
            need(z['diameter_sum']==(1 if n==d+1 else 2*d),'Simplex/small-arrangement sanity failure')
    print(json.dumps({'result':'PASS','scope':'packet integrity and exact finite witness; not the general conjecture',
                      'computed':outputs,'all_deletion_defects':deletion_defects},sort_keys=True))
if __name__=='__main__':
    try:main()
    except Exception as e:
        print('FAIL: '+str(e),file=sys.stderr);sys.exit(1)
