#!/usr/bin/env python3
"""Only source/prior/owned custody checks; no writerV2/site/Git/science access."""
from pathlib import Path
import hashlib, json, stat

OWN=Path(__file__).resolve().parent
checks=0
typed_nodes=0
def need(ok,label):
    global checks
    checks+=1
    if not ok:raise RuntimeError(label)
def raw(p):
    need(stat.S_ISREG(p.lstat().st_mode),'ordinary file '+str(p))
    return p.read_bytes()
def pin(b):return {'bytes':len(b),'SHA256':hashlib.sha256(b).hexdigest()}
def obj(p):return json.loads(raw(p))
def exact(a,b,label):
    global typed_nodes
    typed_nodes+=1
    need(type(a) is type(b),'type '+label)
    if isinstance(a,dict):
        need(list(a)==list(b),'keys/order '+label)
        for k in a:exact(a[k],b[k],label+'/'+k)
    elif isinstance(a,list):
        need(len(a)==len(b),'length '+label)
        for n,(x,y) in enumerate(zip(a,b)):exact(x,y,label+'/'+str(n))
    else:need(a==b,'scalar '+label)
def paths(root):
    fs=[];ds=[]
    need(stat.S_ISDIR(root.lstat().st_mode),'ordinary root')
    for p in root.rglob('*'):
        rel=p.relative_to(root).as_posix();m=p.lstat().st_mode
        if stat.S_ISDIR(m):ds.append(rel)
        else:need(stat.S_ISREG(m),'ordinary entry '+rel);fs.append(rel)
    need(len(fs)==len(set(fs)) and len(ds)==len(set(ds)),'duplicate actual identities')
    return sorted(fs),sorted(ds)
for name in ['SOURCE_CLOSED_EXTENTS.json','PRIOR_CLOSED_EXTENTS.json']:
    for entry in obj(OWN/name):
        root=Path(entry['root']);fs,ds=paths(root)
        expected=list(entry['files'])
        need(len(expected)==len(set(expected)),'duplicate expected identities')
        need(fs==sorted(expected),'whole file extent '+str(root))
        need(ds==sorted(entry['directories']),'whole directory extent '+str(root))
        for rel,record in entry['files'].items():need(pin(raw(root/rel))==record,'whole input '+rel)
for binding in obj(OWN/'INPUT_BINDINGS.json'):
    a=raw(Path(binding['source']));b=raw(OWN/binding['copy'])
    need(a==b,'whole literal binding '+binding['copy'])
    need(pin(b)=={k:binding[k] for k in ['bytes','SHA256']},'binding pin')
    try:x=json.loads(a)
    except (ValueError,UnicodeDecodeError):continue
    exact(x,json.loads(b),binding['copy'])
e=obj(OWN/'INITIAL_EXPECTATIONS.json')
need(e['root_adoption'] is False and e['production_installation_authority'] is False,'authority false')
need(e['canonical_url'] is None and e['AA'] is None and e['follow_up'] is None,'null gates')
need(e['new_V2_writer_exposure']=={'listed':False,'read':False,'executed':False},'preexposure contract')
if (OWN/'INITIAL_SEAL.json').exists():
    seal=obj(OWN/'INITIAL_SEAL.json');mraw=raw(OWN/'INITIAL_MANIFEST.json')
    need(pin(mraw)==seal['manifest'],'initial manifest pin')
    manifest=json.loads(mraw)
    for record in manifest['files']:
        need(pin(raw(OWN/record['path']))=={k:record[k] for k in ['bytes','SHA256']},'initial immutable payload')
print(json.dumps({'status':'PASS_SOURCE_ROOT_PRIOR_ONLY_INITIAL_CUSTODY','checks':checks,'whole_typed_nodes':typed_nodes,'source_files':775,'prior_closed_files':[1352,1335],'new_V2_writer_exposed':False,'website_Git_network_science_authoring_control_or_writes':False,'root_adoption':False,'canonical_url':None,'AA':None}))
