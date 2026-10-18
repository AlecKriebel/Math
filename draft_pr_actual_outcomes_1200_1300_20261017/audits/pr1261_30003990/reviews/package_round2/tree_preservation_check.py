#!/usr/bin/env python3
"""Exercise actual recursive tree writer against an in-memory Git object model."""
from pathlib import Path
import hashlib, importlib.util, json

HERE=Path(__file__).resolve().parent
ACTUAL=HERE.parents[1]/'publication/update_pr_publication.py'
def need(x,m):
    if not x:raise RuntimeError(m)
spec=importlib.util.spec_from_file_location('actual_pr_tree',ACTUAL);u=importlib.util.module_from_spec(spec);spec.loader.exec_module(u)
objects={};calls=[]
def object_id(kind,data):return hashlib.sha1(kind.encode()+b' '+str(len(data)).encode()+b'\0'+data).hexdigest()
def make(entries):
    data=b'\0'.join(sorted(entries,key=lambda e:e.split(b'\t',1)[1]))+b'\0';oid=object_id('tree-model',data);objects[oid]=data;return oid
def git(*args,data=None):
    calls.append(args[0])
    if args[0]=='ls-tree':return objects[args[-1]]
    if args==('mktree','-z'):return (make([s for s in data.split(b'\0') if s])+'\n').encode()
    raise RuntimeError('Unmocked Git call '+repr(args))
u.git=git
def flatten(oid,prefix=''):
    out={}
    for entry in objects[oid].split(b'\0'):
        if not entry:continue
        left,name=entry.split(b'\t',1);mode,kind,child=left.decode().split();name=prefix+name.decode()
        if kind=='tree':out.update(flatten(child,name+'/'))
        else:out[name]=(mode,kind,child)
    return out
empty=make([]);root=empty
initial={
    'QUEUE.md':('100644','blob','1'*40),
    'foreign/folder/file with space.txt':('100644','blob','2'*40),
    'foreign/executable':('100755','blob','3'*40),
    'foreign/link':('120000','blob','4'*40),
    'foreign/submodule':('160000','commit','5'*40),
    u.BASE+'/unrelated-extra.txt':('100644','blob','6'*40),
}
for name,(mode,kind,oid) in initial.items():root=u.put(root,name.split('/'),oid,kind,mode)
for name in u.current_context()['edition_text']:
    root=u.put(root,(u.BASE+'/'+name).split('/'),'7'*40)
before=flatten(root);objects[u.ORIGINAL]=objects[root];root=u.ORIGINAL
names=['ACCEPTANCE.json','AUDIT.md','MOMENT_FORMULATION.md','PROOF.md','PUBLIC_MANIFEST.json','RESULT.md','SOURCE_VERIFICATION.json']
targets=[u.BASE+'/'+name for name in names]+[u.BASE+'/publication_20261017/'+name for name in ['Convex_Body_SOS_Density_Note_v1.0.pdf','Convex_Body_SOS_Density_Verification_v1.0.zip','zenodo-deposit.json','PUBLICATION_RECEIPT.json','README.md']]
desired={name:object_id('blob',('synthetic '+name).encode()) for name in targets}
for name,oid in desired.items():root=u.put(root,name.split('/'),oid)
after=flatten(root)
need(len(desired)==12,'twelve target paths')
need(all(after[name]==('100644','blob',oid) for name,oid in desired.items()),'target writer mismatch')
need({k:v for k,v in before.items() if k not in desired}=={k:v for k,v in after.items() if k not in desired},'unrelated entry changed')
result={'status':'PASS','actual_function':'update_pr_publication.put','twelve_target_paths_checked':12,'unrelated_entries_and_modes_preserved':len(initial),'only_emulated_operations':sorted(set(calls)),'scope':'Actual recursion exercised with an in-memory tree-entry model. No native Git object/index/ref/push operation, service call, or mutation of shared inputs occurred. Native Git serialization and branch integration remain later live checks.'}
(HERE/'TREE_PRESERVATION_RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
