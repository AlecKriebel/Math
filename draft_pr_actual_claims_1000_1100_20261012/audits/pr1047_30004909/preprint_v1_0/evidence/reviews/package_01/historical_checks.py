#!/usr/bin/env python3
"""Validate historical pins against each exact frozen stage, not later revisions."""
from pathlib import Path
import hashlib,json,subprocess,datetime
D=Path(__file__).resolve().parent;C=D/'frozen/candidate';E=C/'evidence'
def require(ok,msg):
    if not ok:raise RuntimeError(msg)
def load(p):return json.loads(p.read_text())
def check(p,row):
    b=p.read_bytes();require(len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],'stage mismatch '+str(p))
out=[]
for folder,manifest,key,namekey in [('basis_family_01','OUTPUT_PINS.json','files','file'),('source_scope_01','AUTHORED_OUTPUT_MANIFEST.json','entries','path'),('priority_01','OUTPUT_PINS.json','files','path')]:
    root=E/'reviews'/folder;rows=load(root/manifest)[key]
    omitted=[]
    for row in rows:
        shipped=root/row[namekey]
        if shipped.exists():check(shipped,row)
        else:
            original=D/'frozen/reviews'/folder/row[namekey];check(original,row)
            omitted.append({'path':row[namekey],'verified_against_frozen_original_stage':True,'in_selected_supportkit':False})
    out.append({'stage':folder,'output_manifest':manifest,'entries_verified':len(rows),'all_match':True,'omitted_stage_outputs':omitted})
P=E/'reviews/priority_01';rows=load(P/'INPUT_PINS_INITIAL.json')['inputs']
for row in rows:check(P/row['own_snapshot'],row)
out.append({'stage':'priority_01','own_frozen_inputs_verified':len(rows)})
S=E/'reviews/source_scope_01';pins=load(S/'frozen/SUBMITTED_PINS.json')
for row in pins['files']:check(S/'frozen'/row['snapshot_path'],row)
out.append({'stage':'source_scope_01','own_frozen_submitted_verified':len(pins['files'])})
for stage in ['layout_initial_20261014','layout_repair1_20261014','package_initial_20261014']:
    p=C/'history'/stage/'STAGE_PINS.json';obj=load(p);rows=obj.get('copies',obj.get('pins'))
    for row in rows:check(C/row.get('snapshot',row.get('copy',row.get('snapshot_path'))),row)
    out.append({'stage':stage,'stage_snapshot_entries_verified':len(rows),'snapshot_not_current_source_used':True})
head=pins['head_oid'];gitrows=load(D/'INPUT_PINS_INITIAL.json')['original_git_objects']
for f in ['INPUT_PINS_INITIAL.json','INPUT_PINS_FINAL.json']:
    X=load(E/'reviews/basis_family_01'/f)
    for row in X['files']:
        original=next(r for r in gitrows if r['repository_path']==row['repository_path'])
        require(row['oid']==original['git_blob_oid'] and row['sha256']==original['actual_sha256'],'actual Git identity mismatch')
        check(E/row['snapshot_path'],row)
    raw=subprocess.check_output(['git','cat-file','commit',head])
    commit_digest=hashlib.sha1(b'commit '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    tree=X['root_tree_oid'];raw_tree=subprocess.check_output(['git','cat-file','tree',tree]);tree_digest=hashlib.sha1(b'tree '+str(len(raw_tree)).encode()+b'\0'+raw_tree).hexdigest()
    fulltree=subprocess.check_output(['git','ls-tree','-r','--full-tree','-z',head])
    require(commit_digest==head==X['actual_commit_object_sha1'],'Git commit digest')
    require(tree_digest==tree==X['actual_root_tree_object_sha1'],'Git root tree digest')
    require(hashlib.sha256(fulltree).hexdigest()==X['fulltree_sha256'] and fulltree.count(b'\0')==X['fulltree_entries'],'Git full recursive tree identity')
    out.append({'stage':'basis_family_01','input_pin_phase':f,'nine_actual_git_objects_verified':True,'commit_header_digest_verified':True,'root_tree_digest_verified':True,'recursive_tree_entries':fulltree.count(b'\0'),'recursive_tree_sha256':hashlib.sha256(fulltree).hexdigest()})
# Readable navigation references are regular files; raw-source references are deliberately excluded.
history=load(C/'REVIEW_HISTORY.json');keys={'inputs','pins','derivation','report','output_pins','frozen_inputs','comparison','record','finite_reproduction','copy_map','fresh_run','portable_adaptation','compiler','export','receipt'}
navigation=[]
for row in history['stages']:
    for key in keys&row.keys():
        p=C/row[key];require(p.exists(),'stage navigation missing '+row[key]);navigation.append({'stage':row['id'],'key':key,'path':row[key],'present':True})
(D/'HISTORICAL_CHECKS.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'historical_pin_checks':out,'stage_navigation':navigation,'status':'PASS','historical_labels_are_not_mathematical_premises':True,'unsupplied_predecessor_events_not_authenticated':True},indent=2)+'\n')
print(json.dumps({'status':'PASS','historical_checks':len(out),'stage_navigation_references':len(navigation)}))
