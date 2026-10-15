"""Separate ROOT readback, requiring the actual closure-returned manifest hash."""
import json,sys
from closed_scope_common import F,sha,mode,verify_prepared,check_row,regular_paths
def main():
    assert len(sys.argv)==2 and len(sys.argv[1])==64
    body=(F/'MANIFEST.json').read_bytes();assert sha(body)==sys.argv[1]
    m=json.loads(body)
    assert m['schema']=='pr53-original-closed-manifest/v1' and m['root_approval'] is False
    idx,ready,count=verify_prepared(True)
    files,dirs=regular_paths()
    assert len(m['files'])==len(files) and {r['path'] for r in m['files']}==set(files)
    assert m['directories']==dirs
    selfrow=[r for r in m['files'] if r['path']=='MANIFEST.json']
    assert selfrow==[{'path':'MANIFEST.json','bytes':None,'sha256':'LITERAL_SELF_REFERENCE_NOT_A_DIGEST','mode':'0444'}]
    for row in m['files']:
        if row['path']!='MANIFEST.json':check_row(row)
    assert mode(F/'MANIFEST.json')=='0444'
    print(json.dumps({'status':'PASS_SEPARATE_ORIGINAL_READBACK_ONLY','actual_manifest_sha256':sys.argv[1],'closed_files':len(files),'complete_actual_capture_objects':count,'root_approval':False,'native_state_or_git_writes':False}))
if __name__=='__main__':main()
