"""Unexecuted SOURCE: ROOT's separate full read-only check after actual V2 closure."""
import argparse,os
from source_package_checks import F,NAME,sha,need,topology,parse,eq,external,captures,science_and_sources,readiness_capture
p=argparse.ArgumentParser();p.add_argument('--expected-manifest-sha256',required=True);a=p.parse_args();body=(F/NAME).read_bytes();need(sha(body)==a.expected_manifest_sha256,'Exact actual returned self manifest SHA');q=parse(body)
K={'schema','status','utc','self_excluded','files_count','files','source_only','proposed_helpers_imported_compiled_executed','future_acceptance_or_ROOT_approval_claimed'}
need(type(q) is dict and set(q)==K and q['schema']=='pr49-acceptance-source-closure/v2' and q['status']=='CLOSED_SOURCE_ONLY' and eq(q['self_excluded'],[NAME]) and q['source_only'] is True and q['proposed_helpers_imported_compiled_executed'] is False and q['future_acceptance_or_ROOT_approval_claimed'] is False,'Exact literal nine-key SOURCE V2 closure')
rows=q['files'];need(type(rows) is list and type(q['files_count']) is int and q['files_count']==len(rows) and len({z['path'] for z in rows})==len(rows) and NAME not in {z['path'] for z in rows},'Typed complete nonduplicate self-only count')
files,dirs=topology();need(set(files)=={z['path'] for z in rows}|{NAME},'No omitted/extra file')
for z in rows:
    need(set(z)=={'path','bytes','sha256'} and type(z['bytes']) is int and z['bytes']>=0,'Exact typed payload row');actual=files[z['path']];need(z['bytes']==actual['bytes'] and z['sha256']==actual['sha256'],'Complete payload bytes')
for z in files.values():need(z['full_mode']==0o444,'Full literal444 every payload/self')
external();captures();science_and_sources();readiness_capture()
print(__import__('json').dumps(dict(status='PASS_CLOSED_SOURCE_READ_ONLY',actual_readback_pid=os.getpid(),files_count=len(rows),directories_count=len(dirs),manifest_sha256=a.expected_manifest_sha256,production_imported_compiled_executed=False,future_acceptance_approved=False)))
