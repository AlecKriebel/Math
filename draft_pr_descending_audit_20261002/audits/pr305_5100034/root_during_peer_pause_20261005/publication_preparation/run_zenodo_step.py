"""One production operation using the repository Zenodo kit; no automatic retry."""
from submission_gate import *
from public_identity import identity,resolution_binding
import sys
step=sys.argv[1];assert step in {'stage','inspect_draft','publish','inspect_published'}
lock=acquire();clear=current_clearance();kit=R/'zenodo_deposit_tool/zenodo.py'
assert pin(kit)['sha256']=='26f264df93b657137b343acc05ae87a3e8e60d46cbbb8b822bc327d77b89c277'
manifest=O/'zenodo-deposit.json';local=load(manifest);assert len(local['metadata'])==11 and len(local['files'])==2
argv=['/opt/homebrew/bin/python3','-E','-B',str(kit),{'stage':'stage','inspect_draft':'inspect','publish':'publish','inspect_published':'inspect'}[step],str(manifest)]
if step!='stage':
 staged=load(OUT/'stage_receipt.json');assert staged['environment']=='production' and type(staged['id']) is int
 if step=='publish':
  draft=load(OUT/'inspect_draft_receipt.json');assert draft['id']==staged['id'] and draft['state']=='ready_to_publish';argv+=['--confirm-id',str(staged['id'])]
 if step=='inspect_published':argv+=['--check-doi']
current_clearance();window();record=execute(step,argv)
identity(record,required=step in {'publish','inspect_published'})
assert record['environment']=='production' and record['title']==local['metadata']['title']
assert len(record['files'])==2 and {x['name'] for x in record['files']}=={x['path'] for x in local['files']}
for x in record['files']:
 b=(O/x['name']).read_bytes();assert len(b)==x['size'] and sha(b)==x['sha256']
if step in {'publish','inspect_published'}:
 assert record['state']=='published' and record['id']==staged['id']
 if step=='inspect_published':resolution_binding(record['doi_resolution'],record['id'])
else:assert record['state']=='ready_to_publish'
current_clearance();(OUT/(step+'_receipt.json')).write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record,indent=2))
