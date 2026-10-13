"""ROOT-only absent-manifest closure. Inspect source before invoking."""
import json,os
from closed_scope_common import F,sha,mode,regular_paths,verify_prepared
def main():
    assert not (F/'MANIFEST.json').exists()
    idx,ready,count=verify_prepared(False)
    files,dirs=regular_paths()
    rows=[]
    for rel in files:
        p=F/rel;b=p.read_bytes()
        rows.append({'path':rel,'bytes':len(b),'sha256':sha(b),'mode':mode(p)})
    rows.append({'path':'MANIFEST.json','bytes':None,'sha256':'LITERAL_SELF_REFERENCE_NOT_A_DIGEST','mode':'0444'})
    obj={'schema':'pr53-original-closed-manifest/v1','scope':'original preparation only; no ROOT mathematical approval','files':sorted(rows,key=lambda x:x['path']),'directories':dirs,'root_approval':False}
    body=(json.dumps(obj,indent=2)+'\n').encode()
    fd=os.open(str(F/'MANIFEST.json'),os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o444)
    try:
        with os.fdopen(fd,'wb') as out:out.write(body);out.flush();os.fchmod(out.fileno(),0o444);os.fsync(out.fileno())
    except BaseException:raise
    verify_prepared(True)
    print(json.dumps({'status':'PASS_ORIGINAL_CUSTODY_ONLY','manifest_sha256':sha(body),'prepared_payload_files':len(files),'closed_files_including_literal_self':len(rows),'complete_actual_capture_objects':count,'root_approval':False}))
if __name__=='__main__':main()
