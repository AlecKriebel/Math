"""SOURCE ONLY: ROOT's separate whole closed review readback, without writes."""
import argparse,json,os,stat
from closure_common import F,NAME,need,sha,parse,topology,check_external,check_captures
p=argparse.ArgumentParser();p.add_argument('--expected-manifest-sha256',required=True);a=p.parse_args()
body=(F/NAME).read_bytes();need(sha(body)==a.expected_manifest_sha256,'actual returned root-close hash');mf=parse(body)
need(type(mf) is dict and mf['schema']=='pr49-fresh-acceptance-source-adversary-closure/v1' and mf['self_excluded']==[NAME] and type(mf['files_count']) is int and mf['files_count']==len(mf['files']),'literal source-review closure')
files,dirs=topology();names={z['path'] for z in mf['files']};need(len(names)==len(mf['files']) and set(files)==names|{NAME} and sorted(dirs)==mf['directories'],'complete exact topology')
for z in mf['files']:
    need(set(z)=={'path','bytes','sha256'} and type(z['bytes']) is int and z['bytes']>=0,'exact typed member')
    actual=files[z['path']];need(actual['bytes']==z['bytes'] and actual['sha256']==z['sha256'] and actual['full_mode']==0o444,'complete frozen body/mode')
need(files[NAME]['full_mode']==0o444 and stat.S_IMODE(F.stat().st_mode)==0o555,'self444 root555')
for d in dirs:need(stat.S_IMODE((F/d).stat().st_mode)==0o555,'all review directories555')
count=check_external();caps=check_captures()
print(json.dumps(dict(status='PASS_COMPLETE_CLOSED_REVIEW_READ_ONLY',actual_readback_pid=os.getpid(),files_count=len(names),directories_count=len(dirs),external_rows=count,complete_actual_captures=caps,manifest_sha256=a.expected_manifest_sha256,production_imported_compiled_executed=False,future_acceptance_approved=False)))
