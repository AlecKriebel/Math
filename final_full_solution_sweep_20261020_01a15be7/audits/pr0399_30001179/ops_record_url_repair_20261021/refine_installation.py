#!/usr/bin/env python3
"""Install final bounded malformed bare-authority coverage, local files only."""
from pathlib import Path
import datetime as dt,difflib,hashlib,json,os
from controls_support import HERE,AUDIT,NAMES

def sha(b):return hashlib.sha256(b).hexdigest()
def main():
    target=AUDIT/'ops_binding.py';before=target.read_bytes()
    if sha(before)!='54671025b7d21bc69d931449ed83c9c75b21a5ee33121b4764bec597bff54bb5':raise RuntimeError('Initial local installation changed')
    after=(HERE/'proposed_helpers/ops_binding.py').read_bytes();compile(after,str(target),'exec')
    temp=HERE/'ops_binding.py.refine.tmp'
    with temp.open('xb') as stream:stream.write(after);stream.flush();os.fsync(stream.fileno())
    os.replace(temp,target)
    receipt={'timestamp_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'path':'ops_binding.py','before_sha256':sha(before),'after_sha256':sha(after),'reason':'Full malformed bare userinfo/backslash controls plus bounded URI lexical prefixes; no provider or other file mutations.','publication_ready':False}
    (HERE/'INSTALLATION_REFINEMENT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    entries=[];diff=[]
    for n in NAMES:
        name=n+'.py';body=(AUDIT/name).read_bytes();old=(HERE/'pre_record_url_binding'/name).read_bytes()
        entries.append({'path':name,'bytes':len(body),'sha256':sha(body)})
        if body!=(HERE/'proposed_helpers'/name).read_bytes():raise RuntimeError('Proposal/current mismatch '+name)
        diff.extend(difflib.unified_diff(old.decode().splitlines(keepends=True),body.decode().splitlines(keepends=True),fromfile='preserved156/'+name,tofile='canonical399/'+name))
    (HERE/'CURRENT_HELPER_BINDING.json').write_text(json.dumps({'timestamp_utc':receipt['timestamp_utc'],'files':entries,'publication_ready':False},indent=2)+'\n');(HERE/'REPAIR.diff').write_text(''.join(diff));print(json.dumps(receipt))
if __name__=='__main__':main()
