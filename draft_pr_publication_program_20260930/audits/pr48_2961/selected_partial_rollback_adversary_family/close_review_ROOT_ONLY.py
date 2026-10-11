"""UNEXECUTED SOURCE: ROOT closes this review only, never native/Git/rollback."""
import datetime as dt
import json
import os
import sys
sys.dont_write_bytecode=True
from review_custody import H,need,row,sha,validate
need(__debug__ and '--personally-read-complete-review' in sys.argv,'ROOT complete personal review required')
need(not (H/'SELF_MANIFEST.json').exists() and not (H/'SELF_MANIFEST.json').is_symlink(),'Absent review manifest only')
ready,files,dirs=validate()
for z in files: os.chmod(H/z['path'],0o444)
files=[row(H/z['path']) for z in files]
manifest={'schema':'pr48-independent-rollback-SOURCE-review-closure/v1','status':'CLOSED_SOURCE_REVIEW_ONLY','utc':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_closer_pid':os.getpid(),'self_excluded':['SELF_MANIFEST.json'],'files_count':len(files),'files':files,'directories':dirs,'source_only':True,'ROOT_execution_approval_claimed':False,'math_review_credit':0}
body=(json.dumps(manifest,sort_keys=True,indent=2)+'\n').encode()
with (H/'SELF_MANIFEST.json').open('xb') as f:
    f.write(body); f.flush(); os.fchmod(f.fileno(),0o444); os.fsync(f.fileno())
validate(True)
print(json.dumps({'status':'CLOSED_SOURCE_REVIEW_ONLY','actual_pid':os.getpid(),'prepared_plus_self':len(files)+1,'manifest_sha256':sha(body)}))
