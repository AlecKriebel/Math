#!/usr/bin/env python3
"""Bounded local installation after all exact historical inputs are preserved."""
from pathlib import Path
import datetime as dt,difflib,hashlib,json,os
from controls_support import HERE,AUDIT,NAMES
OLD_SHA='53aeb70604d4f28f4986cf2e30f5cb90ccd900de7fff96a2d60bb31c03be886f'

def sha(b):return hashlib.sha256(b).hexdigest()
def bind(root,name):
    p=root/name;b=p.read_bytes();return {'path':name,'bytes':len(b),'sha256':sha(b)}
def verify(root,entries):
    for e in entries:
        p=root/e['path']
        if p.is_symlink() or bind(root,e['path'])!=e:raise RuntimeError('Preservation changed '+str(p))

def main():
    O=HERE/'pre_record_url_binding';old=AUDIT/'ops_identity_repair_20261021/MANIFEST.json'
    if sha(old.read_bytes())!=OLD_SHA or old.read_bytes()!=(O/'ops_identity_repair_20261021/MANIFEST.json').read_bytes():raise RuntimeError('Old156 seal changed')
    entries=json.loads(old.read_bytes())['files'];verify(O,entries);verify(AUDIT,entries)
    extra=json.loads((HERE/'SUPPLEMENTAL_PRESERVATION.json').read_bytes())['files'];verify(AUDIT,extra);verify(O,extra)
    changes=[];diff=[]
    for n in NAMES:
        name=n+'.py';before=(O/name).read_bytes();after=(HERE/'proposed_helpers'/name).read_bytes()
        compile(after,str(AUDIT/name),'exec')
        changes.append({'path':name,'before':bind(O,name),'after':bind(HERE/'proposed_helpers',name),'changed':before!=after})
        diff.extend(difflib.unified_diff(before.decode().splitlines(keepends=True),after.decode().splitlines(keepends=True),fromfile='preserved156/'+name,tofile='canonical399/'+name))
    if {e['path'] for e in changes if e['changed']}!={'ops_binding.py','record_publication_ledger.py'}:raise RuntimeError('Unexpected install inventory')
    # One local helper replacement at a time; no provider, Git, lifecycle or
    # publication action occurs. All before bytes already preserved above.
    for e in changes:
        if not e['changed']:continue
        path=AUDIT/e['path'];temp=HERE/(e['path']+'.install.tmp')
        with temp.open('xb') as stream:
            stream.write((HERE/'proposed_helpers'/e['path']).read_bytes());stream.flush();os.fsync(stream.fileno())
        os.replace(temp,path)
    verify(O,entries);verify(AUDIT,[e for e in entries if e['path'] not in {n+'.py' for n in NAMES}]);verify(AUDIT,extra)
    receipt={'timestamp_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'historical156_manifest_sha256':OLD_SHA,'all156_preserved_before_install':True,'supplemental64_preserved_before_install':len(extra),'canonical_files':changes,'actual_provider_attempts':0,'git_mutations':0,'publication_ready':False}
    (HERE/'CANONICAL_INSTALLATION.json').write_text(json.dumps(receipt,indent=2)+'\n');(HERE/'REPAIR.diff').write_text(''.join(diff));print(json.dumps({'installed_changed_helpers':2,'preserved156':156,'supplemental':len(extra),'publication_ready':False}))
if __name__=='__main__':main()
