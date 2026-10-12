#!/usr/bin/env python3
"""Independently decode all ROOT69 whole reexecution streams and exact deltas."""
import gzip,hashlib,json,pathlib
A=pathlib.Path(__file__).resolve().parent.parent
sha=lambda b:hashlib.sha256(b).hexdigest()
root=json.loads((A/'root_family_verification_receipt.json').read_bytes())
assert len(root['checks'])==1620 and len(root['commands'])==69
old_poisson={r['name']:r for r in json.loads((A/'poisson_components_review/receipts/commands.json').read_bytes())}
permitted={('head','repo',k) for k in ['open_issues_count','open_issues','pushed_at','updated_at']}|{('base','repo',k) for k in ['open_issues_count','open_issues','pushed_at','updated_at']}
diffs=[]
def compare(a,b,path=()):
    if isinstance(a,dict) and isinstance(b,dict):
        assert a.keys()==b.keys()
        for k in a:compare(a[k],b[k],path+(k,))
    elif isinstance(a,list) and isinstance(b,list):
        assert len(a)==len(b)
        for i,(x,y) in enumerate(zip(a,b)):compare(x,y,path+(i,))
    elif a!=b:
        assert path in permitted and type(a) is type(b)
        diffs.append(dict(path=list(path),before=a,after=b))
streams=0
for r in root['commands']:
    values={}
    for name,s in r['streams'].items():
        stored=(A/s['path']).read_bytes();data=gzip.decompress(stored)
        assert len(stored)==s['stored_bytes'] and sha(stored)==s['stored_sha256']
        assert len(data)==s['bytes'] and sha(data)==s['sha256']
        values[name]=data;streams+=1
    label=r['label']
    if label.startswith('geometry_') and label!='geometry_final_verifier':
        name=label.removeprefix('geometry_');old=json.loads((A/'path_geometry_review/captures'/(name+'.receipt.json')).read_bytes())
        assert r['exit']==old['exit_code']
        for s in ['stdout','stderr']:assert values[s]==gzip.decompress((A/'path_geometry_review'/old[s]['path']).read_bytes())
    elif label.startswith('poisson_') and label not in ['poisson_final_verifier','poisson_corrections_verifier']:
        name=label.removeprefix('poisson_');old=old_poisson[name]
        assert r['exit']==old['exit']
        for s in ['stdout','stderr']:
            prior=gzip.decompress((A/'poisson_components_review'/old['streams'][s]['path']).read_bytes())
            if name=='api_pr' and s=='stdout':compare(json.loads(prior),json.loads(values[s]))
            else:assert values[s]==prior
    else:assert r['exit']==0 and not values['stderr']
assert len(diffs)==8 and diffs==root['allowed_repository_metadata_differences']
for directory,(mf,msha,sseal) in root['pins'].items():
    if msha:assert sha((A/directory/mf).read_bytes())==msha
    assert sha((A/directory/'FINAL_SEAL.json').read_bytes())==sseal
print(json.dumps(dict(whole_root_reexecution_streams_verified=streams,readonly_commands=69,root_checks_inspected=1620,
    exact_allowed_typed_repository_metadata_differences=8,immutable_family_pins_verified=True,writes=0),indent=2))
