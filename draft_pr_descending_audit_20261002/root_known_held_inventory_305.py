"""Save a public-safe current inventory for a possible later peer write window.

This is not a writer ACK. The snapshot must be refreshed and bound to an exact
future plan before a window is granted. No file bodies are copied or published.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,os,stat,subprocess
P=Path(__file__).resolve().parent;R=P.parent;A=P/'audits/pr305_5100034';B=P/'audits/pr311_30005303'
utc=lambda:datetime.now(timezone.utc).isoformat()
sha=lambda b:hashlib.sha256(b).hexdigest()
def pin(p):
    assert p.is_file() and not p.is_symlink(),p
    b=p.read_bytes();return {'bytes':len(b),'sha256':sha(b),'mode':format(stat.S_IMODE(p.stat().st_mode),'04o')}
output=P/'KNOWN_HELD_FILES_FOR_FUTURE_PEER_WINDOW_305.json'
coord=P/'SHARED_GIT_WINDOW_STATUS.json'
tracked=subprocess.check_output(['/usr/bin/git','ls-files','-z','--',str(P.relative_to(R))],cwd=R,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'))
paths={R/p.decode() for p in tracked.split(b'\0') if p}
paths.update(p for p in A.rglob('*') if p.is_file())
for filename in ['PUBLISHING_CLEARANCE.json','OPERATIONAL_PUBLISHING_CLEARANCE.json']:
    c=json.loads((B/filename).read_bytes());paths.add(B/filename)
    for field in ['immutable_root_artifacts','closed_scientific_files','final_review_artifacts']:
        paths.update(B/n for n in c.get(field,{}))
    paths.update(R/n for n in c.get('operator_files',{}))
    if 'root_adjudication_path' in c:paths.add(B/c['root_adjudication_path'])
paths.update(p for folder in ['preprint_package_v02','submission_v02'] for p in (B/folder).rglob('*') if p.is_file())
paths.discard(coord);paths.discard(output)
paths.add(Path(__file__).resolve())
known={str(p.relative_to(R)):pin(p) for p in sorted(paths)}
assert all(pin(R/n)==e for n,e in known.items()),'A body changed while this dated inventory was measured'
state=json.loads(coord.read_bytes())
assert state['descending_active_pr']==state['descending_acceptance_pr']==305
assert state['descending_shared_write_lease']['token']=='dd8a3816-588a-4873-a0c5-daf812b24b07'
j={'utc':utc(),'purpose':'Authoritative known held file snapshot requested for a later, separately authorized peer integration window',
   'writer_window_granted':False,'current_descending_lease_released':False,
   'files':known,'file_count':len(known),'all_paths_repository_relative':True,'file_bodies_included':False,
   'covers':'Every tracked descending-program file currently on disk; every current PR305 file including untracked/private custody; PR311 publishing and operational clearance inputs and both final submission/package directories.',
   'excluded_mutable_coordination_path':str(coord.relative_to(R)),
   'excludes_self_reference':str(output.relative_to(R)),
   'current_research_still_writing':'PR305 preparation and ROOT research continue under the current descending lease. This dated list is not a hold or an ACK; a fresh stable inventory and full ordinary/flagged foreign-index/body/mode check are required at a later exact window.',
   'private_research_continuing_outside_held_set':'No known required current PR305 evidence is intentionally outside this inventory. New files/captures created after this UTC must be included at any actual later pause.',
   'external_messages_sent':False}
output.write_text(json.dumps(j,indent=2)+'\n')
state.update(utc=utc(),descending_known_held_inventory_for_future_peer_window={'path':str(output.relative_to(R)),**pin(output)},
             descending_known_held_inventory_snapshot_only=True,ascending_pr80_publication_window_granted=False,
             descending_known_held_inventory_note='Inventory only; current PR305 writer lease remains active. Fresh exact plan, stable refreshed inventory and actual-window gate required before any peer integration ACK.')
coord.write_text(json.dumps(state,indent=2)+'\n')
print(json.dumps({'utc':j['utc'],'inventory_path':str(output),'inventory':pin(output),'file_count':len(known),'writer_window_granted':False,'current_lease_released':False},indent=2))
