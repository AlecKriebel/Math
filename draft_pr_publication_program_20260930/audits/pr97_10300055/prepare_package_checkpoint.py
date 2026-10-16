from pathlib import Path
import json, datetime

A=Path(__file__).resolve().parent; C=A.parents[2]; P=A.parents[1]
progress=P/'CURRENT_PROGRESS.json'; r=json.loads(progress.read_text())
r['current_PR_workflow_percent']=40
r['current_package_preparation_percent']=100
r['current_priority_checkpoint_commit']='ca1424cad13c72ed34f83b2c2a344108e06f986e'
r['current_priority_checkpoint_remote_verified']=True
r['updated_UTC']=datetime.datetime.now(datetime.timezone.utc).isoformat()
progress.write_text(json.dumps(r,indent=2)+'\n')
paths=[]
def add(p):
    if not p.is_file() or p.is_symlink(): raise RuntimeError('Invalid selection: '+str(p))
    paths.append(p.relative_to(C).as_posix())
for p in sorted((A/'contingent_credited_note_v1').rglob('*')):
    if not p.is_file(): continue
    rel=p.relative_to(A/'contingent_credited_note_v1').as_posix()
    if rel.startswith(('tmp/','private/source_visuals/')): continue
    add(p)
for name in ['authenticate_prepared_package.py','ROOT_PREPARED_PACKAGE_AUTHENTICATION_20261006.json','ROOT_NATIVE_COMPILER_VISUAL_CHECK_20261006.json','record_storage_recovery.py','ROOT_OWNED_STORAGE_RECOVERY_20261006.json','ROOT_PRIVATE_GIT_PACKING_20261006.json','RESEARCH_LOG.md','prepare_package_checkpoint.py']:
    add(A/name)
for label in ['authenticate_prepared_package','record_storage_recovery','repack_private_git','checkpoint_priority_adjudication']:
    for p in sorted((A/'actual_operations'/label).rglob('*')):
        if p.is_file(): add(p)
for name in ['RECEIPT.json','PROCESS_JOURNAL.json']:
    add(A/'actual_checkpoints/priority_adjudication'/name)
add(progress)
selection=A/'PREPARED_PACKAGE_CHECKPOINT_SELECTION.json'
paths.append(selection.relative_to(C).as_posix())
selection.write_text(json.dumps({'schema':'explicit-pr97-prepared-package-checkpoint-selection/v1','scope':'Concrete credited package and actual provenance, storage-recovery summaries and fresh-review handoff; third-party source pixels/bodies, active reviewer folder and compressed private checkpoint streams excluded.','paths':sorted(set(paths))},indent=2)+'\n')
print(json.dumps({'paths':len(set(paths)),'bytes':sum((C/p).stat().st_size for p in set(paths)),'third_party_source_pixels_included':False,'publication_authorized':False}))
