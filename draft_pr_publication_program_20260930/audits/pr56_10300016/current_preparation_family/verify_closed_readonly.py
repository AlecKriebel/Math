"""Separate ROOT readback requiring genuine current closure digest; no file writes."""
import json,sys,os
from closed_scope_common import F,sha,mode,topology,verify_prepared,check
def main():
    assert len(sys.argv)==3 and sys.argv[1]=='--root-only-read-after-close' and len(sys.argv[2])==64
    b=(F/'MANIFEST.json').read_bytes();assert sha(b)==sys.argv[2]
    m=json.loads(b);assert m['schema']=='pr56-current-closed-manifest/v1' and m['root_approval'] is False and m['native_acceptance'] is False
    idx,ready,n=verify_prepared(True);files,dirs=topology()
    assert m['directories']==dirs and {r['path'] for r in m['files']}==set(files) and len(m['files'])==len(files)
    assert [r for r in m['files'] if r['path']=='MANIFEST.json']==[{'path':'MANIFEST.json','bytes':None,'sha256':'LITERAL_SELF_REFERENCE_NOT_A_DIGEST','mode':'0444'}]
    for row in m['files']:
        if row['path']!='MANIFEST.json':check(row)
    assert mode(F/'MANIFEST.json')=='0444'
    print(json.dumps({'status':'PASS_SEPARATE_CURRENT_SOURCE_READBACK_ONLY','actual_reader_pid':os.getpid(),'actual_closer_pid':m['actual_closer_pid'],'manifest_sha256':sys.argv[2],'closed_files':len(files),'external_whole_body_rows':n,'root_approval':False,'native_git_writes':False}))
if __name__=='__main__':main()
