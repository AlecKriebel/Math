"""Proposed separate readback: no writes, imports only this closed review's reader."""
from review_common import *
import argparse
p=argparse.ArgumentParser();p.add_argument('--manifest-sha256',required=True);a=p.parse_args()
mp=F/'SELF_MANIFEST.json';assert ref(mp)['sha256']==a.manifest_sha256 and ref(mp)['full_mode']==0o444
m=load(mp);assert m['schema']=='pr49-current-whole-adversary-self-only-closure/v1' and m['self_excluded']==1
files,dirs,dm=topology()
assert files==sorted([v['path'] for v in m['files']]+[mp.name]) and dirs==m['directories'] and dm==m['directory_full_modes']
assert len(m['files'])==m['files_count'] and len({v['path'] for v in m['files']})==m['files_count']
for v in m['files']:
    assert v['full_mode']==0o444;body(F/v['path'],v)
for v in m['external_body_mode_bindings']:body(R/v['path'],v)
q=inspect_complete();assert q['external_rows']==m['external_body_mode_bindings']
assert ref(F/'REPORT.md')['sha256']==m['report_sha256']
assert m['future_acceptance_approved'] is False and m['ROOT_approval_created'] is False
print(json.dumps(dict(status='PASS_SEPARATE_CLOSED_WHOLE_READ_ONLY',actual_readback_pid=os.getpid(),manifest_sha256=a.manifest_sha256,files_count=m['files_count'],external_rows=len(q['external_rows']),future_acceptance_approved=False)))
