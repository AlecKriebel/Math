"""Unexecuted SOURCE: ROOT's absent-only closure of this fully personally inspected V2 family."""
from pathlib import Path
import argparse,datetime as dt,json,os,stat
from source_package_checks import F,NAME,sha,need,topology,inspect,readiness_capture
p=argparse.ArgumentParser();p.add_argument('--expected-report-sha256',required=True);a=p.parse_args()
need(not (F/NAME).exists() and not (F/NAME).is_symlink(),'Absent-only literal self manifest')
need(sha((F/'REPORT.md').read_bytes())==a.expected_report_sha256,'Exact personally ROOT-read report SHA')
readiness_capture();q=inspect();need(q['status']=='READY_SOURCE_ONLY_FOR_ROOT_CLOSURE','Complete source-only readiness')
files,dirs=topology();rows=[dict(path=n,bytes=z['bytes'],sha256=z['sha256']) for n,z in sorted(files.items())]
body=(json.dumps(dict(schema='pr49-acceptance-source-closure/v2',status='CLOSED_SOURCE_ONLY',utc=dt.datetime.now(dt.timezone.utc).isoformat(),self_excluded=[NAME],files_count=len(rows),files=rows,source_only=True,proposed_helpers_imported_compiled_executed=False,future_acceptance_or_ROOT_approval_claimed=False),sort_keys=True,indent=2)+'\n').encode()
for n in files:(F/n).chmod(0o444)
stage=F/'.PREPARATION_MANIFEST.staging'
with stage.open('xb') as f:f.write(body);f.flush();os.fchmod(f.fileno(),0o444);os.fsync(f.fileno())
os.link(stage,F/NAME,follow_symlinks=False);stage.unlink();fd=os.open(F,os.O_RDONLY)
try:os.fsync(fd)
finally:os.close(fd)
closed,ds=topology();need(set(closed)==set(files)|{NAME} and ds==dirs,'Complete self-only closure')
for n,z in files.items():need(closed[n]['bytes']==z['bytes'] and closed[n]['sha256']==z['sha256'] and closed[n]['full_mode']==0o444,'Full closed payload bytes/permission mode')
need(stat.S_IMODE((F/NAME).stat().st_mode)==0o444,'Literal self full444')
print(json.dumps(dict(status='CLOSED_SOURCE_ONLY',actual_closing_pid=os.getpid(),files_count=len(rows),directories_count=len(dirs),manifest_sha256=sha(body),production_imported_compiled_executed=False,future_acceptance_approved=False)))
