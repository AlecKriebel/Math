"""ROOT-only absent closure of the lean current SOURCE package."""
import json,os
from closed_scope_common import F,sha,mode,topology,verify_prepared
def main():
    assert not (F/'MANIFEST.json').exists()
    idx,ready,n=verify_prepared(False);files,dirs=topology()
    rows=[]
    for rel in files:
        p=F/rel;b=p.read_bytes();rows.append({'path':rel,'bytes':len(b),'sha256':sha(b),'mode':mode(p)})
    rows.append({'path':'MANIFEST.json','bytes':None,'sha256':'LITERAL_SELF_REFERENCE_NOT_A_DIGEST','mode':'0444'})
    m={'schema':'pr53-current-closed-manifest/v1','files':sorted(rows,key=lambda x:x['path']),'directories':dirs,'root_approval':False,'scope':'SOURCE custody only; no mathematical acceptance or native transition'}
    b=(json.dumps(m,indent=2)+'\n').encode()
    fd=os.open(str(F/'MANIFEST.json'),os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o444)
    with os.fdopen(fd,'wb') as stream:stream.write(b);stream.flush();os.fchmod(stream.fileno(),0o444);os.fsync(stream.fileno())
    verify_prepared(True)
    print(json.dumps({'status':'PASS_CURRENT_SOURCE_CLOSURE_ONLY','manifest_sha256':sha(b),'payload_files':len(files),'external_whole_body_rows':n,'root_approval':False}))
if __name__=='__main__':main()
