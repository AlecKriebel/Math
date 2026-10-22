"""Record actual verified publication/tracker/native merge; no provider actions."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json

PUB=Path(__file__).resolve().parent;D=PUB.parent/'initial_review_20261015'
R=PUB.parent/'preprint';P=PUB.parent.parent.parent;F=PUB/'native_current_source'
m=json.loads((PUB/'PR_MERGED.json').read_text())
z=json.loads((PUB/'ZENODO_VERIFIED_PUBLICATION.json').read_text())
t=json.loads((PUB/'TRACKER_VERIFIED_APPEND.json').read_text())
assert m['merged'] and m['doi_url']==z['doi_url']==t['doi_url']
assert z['submitted'] and z['metadata_and_files_verified'] and t['verified'] and t['append_count']==1
assert not (F/'MERGE_RECEIPT.json').exists(),'Already recorded; reconcile read-only'
now=datetime.now(timezone.utc).isoformat()
(F/'MERGE_RECEIPT.json').write_text(json.dumps(m,indent=2)+'\n')
for name in ['README.md','PUBLICATION_STATUS.md','FINAL_DISPOSITION.md']:
    with (F/name).open('a') as f:f.write('\nNative merge subsequently verified at '+m['merge_commit']+'. MERGE_RECEIPT.json records the actual accepted head, DOI/tracker and merge event. This current native outcome supersedes dated preparation-stage records.\n')
with (F/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+now+' — case100%: actual native science/original archive/PDF/ZIP readbacks and merge verified. DOI '+z['doi_url']+', exact GWS row '+t['updated_range']+'. Entire descending goal remains active/incomplete.\n')
for name in ['metadata.json','FINAL_ACCEPTANCE.json']:
    p=F/name;o=json.loads(p.read_text());o.update(native_merge_verified=m,case_completion_percent=100)
    if name=='metadata.json':o['status']='claimed_solved_audited_published_merged'
    p.write_text(json.dumps(o,indent=2)+'\n')
subset=[]
for p in sorted(F.iterdir()):
    if p.is_file() and p.name not in {'MANIFEST.json','PUBLICATION_MANIFEST.json','CURRENT_PACKET_MANIFEST.json'}:
        raw=p.read_bytes();subset.append(dict(path=p.name,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
for name in ['MANIFEST.json','PUBLICATION_MANIFEST.json']:
    (F/name).write_text(json.dumps(dict(scope='Current accepted published merged administrative outcome; historical originals retained byte-exact',files=subset),indent=2)+'\n')
rows=[]
for p in sorted(F.rglob('*')):
    if p.is_file() and p.name!='CURRENT_PACKET_MANIFEST.json':
        raw=p.read_bytes();rows.append(dict(path=p.relative_to(F).as_posix(),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
(F/'CURRENT_PACKET_MANIFEST.json').write_text(json.dumps(dict(schema='pr211-reconciled-packet-v1',self_excluded=True,status='claimed_solved_audited_published_merged',source_head='9d7b623203b525386da3d9d91548c79e7445a11c',files=rows),indent=2)+'\n')
U=R/'pr_update/5100063'
assert (F/'PROOF.md').read_bytes()==(U/'PROOF.md').read_bytes()
for p in (U/'history/original_submission_20261015').rglob('*'):
    if p.is_file():assert p.read_bytes()==(F/p.relative_to(U)).read_bytes()
prepared=json.loads((PUB/'PR_PREPARED.json').read_text())
q=next(x for x in prepared['included_owned_pins'] if x['path']=='unsolved_math_prioritization/QUEUE.md')
state=json.loads((D/'CURRENT_AUDIT_STATE.json').read_text())
state.update(utc=now,stage='verified_publication_tracker_native_merge_complete',completion_percent=100,
    original_head='9d7b623203b525386da3d9d91548c79e7445a11c',head=m['reviewed_head'],
    DOI=z['doi'],tracker_range=t['updated_range'],merged_head=m['reviewed_head'],merge_commit=m['merge_commit'],
    counts=[43,20,20,0],preprint_upload_cleared=True)
(D/'CURRENT_AUDIT_STATE.json').write_text(json.dumps(state,indent=2)+'\n')
g=json.loads((P/'CURRENT_GOAL_SELECTION_20261013.json').read_text())
g.update(utc=now,current_stage='PR211_verified_publication_tracker_native_merge_complete',case_completion_percent=100,
    current_PR_head=m['reviewed_head'],current_DOI=z['doi'],current_tracker_range=t['updated_range'],
    last_native_merge=m['merge_commit'],previous_completed_PR=211,previous_completed_DOI=z['doi'],
    program_counts=[43,20,20,0],previous_completion_counts=[43,20,20,0],preprint_upload_cleared=True,
    overall_goal_active_incomplete=True)
(P/'CURRENT_GOAL_SELECTION_20261013.json').write_text(json.dumps(g,indent=2)+'\n')
line='\n## '+now+' — PR211 checkpoint100%\n\nExact pinned k904,a odd outer original-focus inverse-area product accepted within strict nondegenerate confocal-ellipse domain, all odd leastperiods/stars/N3/repetitions. Three new math/source families, two extensive bounded priority families and two fresh sequential whole-package adversaries with global repairs completed; final new reviewer found no mandatory/optional concerns. All19 originals/proofmathsections preserved. Researchnote and portable archive published ONCE at '+z['doi_url']+', exact metadata/bothactualpublicdownloads verified and DOI resolved; GWS appendedONCE/all4cellsreadback '+t['updated_range']+'. Native full selectedtree identities and actualscience/originalarchive/PDF/ZIP/Queuebytes verified; PR211 actually merged at '+m['merge_commit']+' from acceptedhead '+m['reviewed_head']+'. Historical novelty remains undetermined and source-access limits/classical credit retained; extensiveAI/unrefereed/no independenthumanreview/formalization. Counts43completed/20preprints/20merges/0pendingtracker. Full descending goal active/incomplete; final factual main checkpoint and nextlower exactclaimed_solved selection remain.\n'
for p in [D/'RESEARCH_LOG.md',P/'RESEARCH_LOG.md',R/'RESEARCH_LOG.md']:
    with p.open('a') as f:f.write(line)
print(json.dumps(dict(case_completion_percent=100,DOI=z['doi'],tracker_range=t['updated_range'],merge_commit=m['merge_commit'],counts=[43,20,20,0],full_goal_active_incomplete=True),indent=2))
