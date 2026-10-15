"""Separate ROOT readback; requires the genuine closure-returned digest."""
import json,sys
from closed_scope_common import F,sha,mode,topology,verify_prepared,check
def main():
    assert len(sys.argv)==2 and len(sys.argv[1])==64
    b=(F/'MANIFEST.json').read_bytes();assert sha(b)==sys.argv[1]
    m=json.loads(b);assert m['schema']=='pr55-priority-closed-manifest/v1' and m['root_acceptance'] is False and m['priority_cleared'] is False
    idx,ready,n=verify_prepared(True);files,dirs=topology()
    assert m['directories']==dirs and {r['path'] for r in m['files']}==set(files) and len(m['files'])==len(files)
    assert [r for r in m['files'] if r['path']=='MANIFEST.json']==[{'path':'MANIFEST.json','bytes':None,'sha256':'LITERAL_SELF_REFERENCE_NOT_A_DIGEST','mode':'0444'}]
    for row in m['files']:
        if row['path']!='MANIFEST.json':check(row)
    assert mode(F/'MANIFEST.json')=='0444'
    print(json.dumps({'status':'PASS_SEPARATE_PRIORITY_SOURCE_READBACK_ONLY','manifest_sha256':sys.argv[1],'closed_files':len(files),'external_files_verified':n,'root_acceptance':False,'priority_cleared':False,'native_git_writes':False}))
if __name__=='__main__':main()
