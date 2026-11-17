from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,stat
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
D=P/'verification/checkpoint-haf-retract-publish-graminitial-20261117'
O=P/'verification/root-checkpoint-a426-adoption-20261117.json'
assert not O.exists()
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
pins={'FINAL.json':'eb981912416d96a52bd0fb10621894c7733a8dae32339ffa5c7c2d4f93cd9eab','MANIFEST.json':'a1ce73377276e3926aba788e4f4ae59c910105bb8fac0a992d7fea2bcfc66c9b'}
for n,pin in pins.items():assert sha(D/n)==pin
m=json.loads((D/'MANIFEST.json').read_text())
expected={e['path']:dict(e,kind='file') for e in m['payload_files']}
expected.update({e['path']:dict(e,kind='directory') for e in m['directories']})
expected.update({e['path']:dict(e,kind='file') for e in m['terminal_controls']})
actual={str(f.relative_to(D)):f for f in D.rglob('*')}
assert set(expected)==set(actual) and len(actual)==49
assert stat.S_IMODE(D.stat().st_mode)==int(m['root_mode'],8)
rows=[]
for n,f in sorted(actual.items()):
 e=expected[n];assert not f.is_symlink() and f.is_dir()==(e['kind']=='directory')
 assert stat.S_IMODE(f.stat().st_mode)==int(e['mode'],8)
 if f.is_file():
  b=f.read_bytes();digest=hashlib.sha256(b).hexdigest()
  if n in pins:assert digest==pins[n]
  else:assert digest==e['SHA256'] and len(b)==e['bytes']
  rows.append({'path':n,'bytes':len(b),'SHA256':digest})
assert len(rows)==48
checks=json.loads((D/'FINAL_CHECKS.json').read_text());post=json.loads((D/'POST_TREE_AUDIT.json').read_text())
assert checks['dry_push_exits']==[0,0] and all(r['exit_code']==0 for r in checks['all_wrapper_runs'])
assert checks['all_159_untargeted_root_siblings_and_docs_exact'] and checks['all_changed_blob_whole_bytes_and_git_modes_verified']
assert checks['key_actual_file_identities']==40 and checks['complete_durable_packet_source_closures']==19
assert checks['changed_paths']==404 and checks['status_counts']=={'M':4,'A':400}
assert post['fresh_actual_remote_main'].split()[0]=='a4267dc5366bb693dd565421271276677a060320'
assert post['parent']=='15482acd0ef864af280a864758b2ac6aa24dfbe8' and post['tree']=='0b68ff45d05e310d7bc959ff48060fe91a08316c'
before=json.loads((D/'GUARDS_BEFORE.json').read_text());after=json.loads((D/'GUARDS_AFTER.json').read_text())
for k in ['repositories','public','helper','protected_boundary']:assert before[k]==after[k],k
assert before['repositories']==checks['native_protected_repositories_exact']
result={'UTC':datetime.now(timezone.utc).isoformat(),'status':'SCOPED_CHECKPOINT_ACCEPTED','commit':checks['commit'],'parent':checks['parent'],'tree':checks['tree'],'changed_paths':404,'siblings_exact':159,'key_actual_files':40,'durable_closures':19,'original_INITIALs':6,'files_authenticated':48,'childdirs':1,'payload':rows,'root_reading':['Actual entire FINAL and REPORT','Actual FINAL_CHECKS claims and native guard identities','Actual POST_TREE_AUDIT summary/remote/parent/drydelta/cache boundaries','Complete actual manifest schema and all finite payload identities'],'native_repository_public_helper_boundary_before_after_exact':True,'dry_push_exits':[0,0],'completion_percent':100,'overall_scientific_review_percent':141/203*100,'goal_active_incomplete':True,'scientific_clearance':False,'future_publication_authority':False}
O.write_text(json.dumps(result,indent=2)+'\n')
f=P/'PROGRESS.json';x=json.loads(f.read_text());x['latest_math_checkpoint']=checks['commit'];x['latest_math_checkpoint_root_adoption']=str(O.relative_to(P));x['latest_math_checkpoint_root_adoption_SHA256']=sha(O);x['updated_utc']=result['UTC'];f.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':result['status'],'commit':checks['commit'],'files_authenticated':48,'receipt_SHA256':sha(O)}))
