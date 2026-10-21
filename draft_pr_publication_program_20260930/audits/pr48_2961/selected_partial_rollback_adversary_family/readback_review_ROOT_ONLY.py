"""UNEXECUTED SOURCE: separate readback of closed own review, no mutation."""
import json
import os
import sys
sys.dont_write_bytecode=True
from review_custody import H,need,row,sha,validate
need(__debug__,'Optimized Python refused')
ready,files,dirs=validate(True)
mf=(H/'SELF_MANIFEST.json').read_bytes(); m=json.loads(mf)
need(m['schema']=='pr48-independent-rollback-SOURCE-review-closure/v1' and m['self_excluded']==['SELF_MANIFEST.json'],'Exact review manifest schema/self')
need(m['files_count']==len(m['files']) and m['files']==[z for z in files if z['path']!='SELF_MANIFEST.json'] and m['directories']==dirs,'Complete closed review body/mode domain')
need(row(H/'SELF_MANIFEST.json')['full_mode']==0o444 and m['ROOT_execution_approval_claimed'] is False and m['math_review_credit']==0,'Custody only')
print(json.dumps({'status':'PASS_SEPARATE_CLOSED_SOURCE_REVIEW_READBACK','actual_pid':os.getpid(),'total_files':len(files),'manifest_sha256':sha(mf),'native_or_Git_mutation':False}))
