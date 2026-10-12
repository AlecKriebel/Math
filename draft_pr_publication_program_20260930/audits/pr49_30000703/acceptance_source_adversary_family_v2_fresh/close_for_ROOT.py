"""SOURCE ONLY: ROOT's actual absent-only close, after complete independent handoff."""
import argparse,datetime as dt,json,os,stat
from closure_common import F,NAME,need,sha,parse,topology,check_external,check_captures
p=argparse.ArgumentParser();p.add_argument('--expected-report-sha256',required=True);a=p.parse_args()
need(not (F/NAME).exists() and not (F/NAME).is_symlink(),'literal self manifest absent')
need(sha((F/'REPORT.md').read_bytes())==a.expected_report_sha256,'personally ROOT-read exact report')
ready=parse((F/'READY.json').read_bytes());verdict=parse((F/'VERDICT.json').read_bytes());custody=parse((F/'CUSTODY_RESULT.json').read_bytes())
need(ready['status']=='READY_UNCLOSED_FOR_ROOT' and ready['ROOT_approval_created'] is False,'actual reviewer handoff only')
need(verdict['schema']=='pr49-acceptance-source-adversary-verdict/v1' and verdict['verdict']=='PASS_SOURCE_ONLY_SCOPED' and verdict['mandatory_corrections']==[],'exact clean SOURCE verdict')
need(custody['status']=='PASS' and verdict['preparation_manifest_sha256']==custody['preparation_manifest_sha256'],'actual reviewed fixed source')
count=check_external();caps=check_captures();files,dirs=topology();need(NAME not in files,'self absent-only')
rows=[dict(path=n,bytes=z['bytes'],sha256=z['sha256']) for n,z in sorted(files.items())]
body=(json.dumps(dict(schema='pr49-fresh-acceptance-source-adversary-closure/v1',utc=dt.datetime.now(dt.timezone.utc).isoformat(),self_excluded=[NAME],files_count=len(rows),files=rows,directories=sorted(dirs),source_only=True,production_imported_compiled_executed=False,future_acceptance_approved=False),sort_keys=True,indent=2)+'\n').encode()
for n in files:(F/n).chmod(0o444)
stage=F/'.SELF_MANIFEST.staging'
with stage.open('xb') as stream:stream.write(body);stream.flush();os.fchmod(stream.fileno(),0o444);os.fsync(stream.fileno())
os.link(stage,F/NAME,follow_symlinks=False);stage.unlink()
fd=os.open(F,os.O_RDONLY)
try:os.fsync(fd)
finally:os.close(fd)
after,after_dirs=topology();need(set(after)==set(files)|{NAME} and after_dirs==dirs,'complete literal self-only closure')
for n,z in files.items():need(after[n]['bytes']==z['bytes'] and after[n]['sha256']==z['sha256'] and after[n]['full_mode']==0o444,'full closed payload')
need(after[NAME]['full_mode']==0o444,'literal self mode444')
for d in sorted(dirs,key=lambda n:len(n),reverse=True):(F/d).chmod(0o555)
F.chmod(0o555)
print(json.dumps(dict(status='CLOSED_SOURCE_REVIEW_ONLY',actual_closing_pid=os.getpid(),files_count=len(rows),directories_count=len(dirs),external_rows=count,complete_actual_captures=caps,manifest_sha256=sha(body),production_imported_compiled_executed=False,future_acceptance_approved=False)))
