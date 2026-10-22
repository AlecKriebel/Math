"""Read-only replay of this closed held review; never calls services or writes files."""
from pathlib import Path
import collections,decimal,hashlib,json,stat,sys,tarfile
V=Path(__file__).resolve().parent
A=V.parent/'existing_publication_batch_b1_plus1198_v03'
EXPECTED_INPUT='a1797b910a865607887faa9ef5e28ad8798be616393c867a3bbaf47baf1d8944'
def ck(ok,msg):
 if not ok:raise RuntimeError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def typed(a,b):
 if type(a) is not type(b):return False
 if type(a) is dict:return a.keys()==b.keys() and all(typed(a[k],b[k]) for k in a)
 if type(a) is list:return len(a)==len(b) and all(typed(x,y) for x,y in zip(a,b))
 if type(a) is float:return a.hex()==b.hex()
 return a==b
def rsha(x):return sha(canon(x+['']*(43-len(x))))
def load(p):return json.loads(p.read_bytes())
def main():
 ck(len(sys.argv)==2,'Pass expected manifest SHA256 from the review handoff')
 raw=(V/'MANIFEST.json').read_bytes();ck(sha(raw)==sys.argv[1],'Review manifest drift');m=json.loads(raw)
 expected={e['path']:e for e in m['files']};ck(len(expected)==len(m['files']),'Manifest duplicate')
 names=set();inodes=collections.defaultdict(list)
 for p in V.rglob('*'):
  ck(not p.is_symlink(),'Symlink');s=p.stat();inodes[(s.st_dev,s.st_ino)].append(p)
  if p.is_file() and '__pycache__' not in p.parts and p not in [V/'MANIFEST.json',V/'MANIFEST.sha256']:
   name=str(p.relative_to(V));names.add(name);ck(name in expected,'Unsealed file '+name);e=expected[name];b=p.read_bytes();ck(len(b)==e['bytes'] and sha(b)==e['sha256'],'Pin '+name)
 ck(names==set(expected),'Closed membership drift')
 for paths in inodes.values():
  if paths[0].is_file():ck(paths[0].stat().st_nlink==len(paths),'Outside hardlink')
 ck(sha((V/'INPUT_MANIFEST_VERSION03.json').read_bytes())==EXPECTED_INPUT,'Input snapshot manifest drift')
 ck(sha((A/'MANIFEST.json').read_bytes())==EXPECTED_INPUT,'Original input manifest drift')
 orig=load(A/'MANIFEST.json')
 for e in orig['files']:
  p=A/e['path'];ck(not p.is_symlink(),'Input symlink');b=p.read_bytes();ck(len(b)==e['bytes'] and sha(b)==e['sha256'],'Protected input drift '+e['path'])
 C=V/'private/packet_copy';pins=load(V/'INDEPENDENT_COPY_PINS.json')
 for e in pins['files']:
  b=(C/e['path']).read_bytes();ck(len(b)==e['bytes'] and sha(b)==e['sha256'],'Independent source-copy drift')
 plan=load(C/'PROPOSAL.json');sem=load(V/'SEMANTIC_DECISIONS.json');action=load(V/'ACTION_REVIEW.json')
 ck(action['action_review_accepted'] is False and action['verdict']=='HOLD_KNOWN_PR_REFERENCE_DUPLICATE_GUARD_GAP','HOLD changed')
 for key,name in [('plan_sha256','PROPOSAL.json'),('runner_sha256','append_reviewed_rows.py'),('core_sha256','ops_core.py'),('numeric_helper_sha256','frozen/reconcile_existing_row.py')]:ck(action[key]==sha((C/name).read_bytes()),'Action source binding')
 for item,e in zip(plan['items'],action['exact_rows']):
  ck(item['pr']==e['pr'] and rsha(item['row'])==e['row_sha256_43_columns'],'Literal row hash')
  ck(len(item['row'])==4 and all(type(x) is str for x in item['row']) and item['row'][1]=='','Four literal cells')
 ck(action['approved_semantic_clearance_keys']==[e['semantic_clearance_key'] for e in sem['existing_row_decisions']],'Semantic keys')
 ck(action['approved_intrabatch_clearance_keys']==[e['intrabatch_clearance_key'] for e in sem['within_batch_decisions']],'Pair keys')
 ck(len(sem['existing_row_decisions'])==29 and len(sem['within_batch_decisions'])==3,'Scientific decision count')
 baseline=load(C/'private_readonly/ledger_preparation02/02.stdout')['valueRanges'][0]['valueRange']['values']
 for e in sem['existing_row_decisions']:
  ck(rsha(baseline[e['row']-1])==e['row_sha256_43_columns'],'Semantic row binding')
  ck(sha(canon([e['pr'],e['row'],e['row_sha256_43_columns'],e['matched']]))==e['semantic_clearance_key'],'Semantic key binding')
 for e in sem['within_batch_decisions']:ck(sha(canon([e['pr'],e['other_pr'],e['other_row_sha256_43_columns'],e['matched']]))==e['intrabatch_clearance_key'],'Pair key binding')
 outcomes=[];general=[];bad=0;good=0
 for mode in ['normal','O','OO']:
  f=load(V/('FRESH_CONTROLS_'+mode+'.json'));r=load(V/('PR_REFERENCE_CONTROLS_'+mode+'.json'));ck(len(f['results'])==48 and len(r['results'])==4,'Mode count')
  for i,e in enumerate(r['results']):
   ck(e['all_publication_logic_executed'] and e['get_calls']==54 and e['pr_calls']==17,'PR test execution scope')
   if i<3:
    ck(e['write_attempts']==1 and e['receipt_exists'] and e['error'] is None,'Counterexample not reproduced');bad+=1
    receipt=load(C/'private_tests'/('fresh_pr_reference_world_'+mode)/'private_action'/e['name']/'RECONCILIATION.json')
    ck(receipt['status']=='verified' and receipt['previous_rows_preserved_all43columns']==192 and receipt['after_rows']==208 and receipt['items'][0]['row']==193,'Actual false receipt')
   else:ck(e['write_attempts']==0 and not e['case_exists'] and not e['receipt_exists'],'URL control failed');good+=1
  def project(e):return {k:e.get(k) for k in ['name','issue','mode','error','get_calls','pr_calls','gws_calls','write_attempts','case_exists','receipt_exists','all_publication_logic_executed','independent_fixture','existing_row_pr_reference']}
  outcomes.append([project(e) for e in r['results']]);general.append([project(e) for e in f['results']])
 ck(outcomes[0]==outcomes[1]==outcomes[2] and general[0]==general[1]==general[2],'Optimization outcome drift')
 retained=load(C/'CONTROLS_FINAL_normal.json');ck(len(retained['full_actual_runner_cases'])==305,'Retained normal case count')
 cold_members=0
 for mode in ['normal','O','OO']:
  D=V/'private'/('cold_fresh_'+mode);idx=load(D/'INDEX.json');path=D/'histories.tar.xz';ck(sha(path.read_bytes())==idx['archive_sha256'],'Cold archive drift')
  es={e['path']:e for e in idx['files']+idx['directories']};seen=[]
  with tarfile.open(path,'r:xz') as ar:
   for t in ar:
    ck(t.name in es,'Cold unindexed entry');seen.append(t.name);e=es[t.name]
    ck(t.mode==e['mode'] and int(decimal.Decimal(t.pax_headers['mtime'])*10**9)==e['mtime_ns'] and t.uid==e['uid'] and t.gid==e['gid'],'Cold metadata')
    if 'bytes' in e:
     b=ar.extractfile(t).read();ck(len(b)==e['bytes'] and sha(b)==e['sha256'],'Cold bytes');cold_members+=1
  ck(len(seen)==len(es) and set(seen)==set(es),'Cold membership')
 live=load(V/'LIVE_PREFLIGHT_REVIEW.json');L=V/live['raw_private_capture'];readfiles=sorted(L.glob('gws_read_*.stdout'));ck(len(readfiles)==7,'Live read count')
 docs=[load(p) for p in readfiles];ck(typed(docs[0],docs[3]) and typed(docs[0],docs[6]),'Live metadata drift')
 vals=[docs[i]['valueRanges'][0]['valueRange'] for i in [1,2,4,5]]
 ck(all(x['range']=="'Math Puzzles'!A1:AQ1178" and x['majorDimension']=='ROWS' for x in vals),'Live extent')
 ck(all(typed(vals[0]['values'],x['values']) for x in vals[1:]) and typed(vals[0]['values'],baseline),'Live full value/FORMULA drift')
 ck(live['old_rows']==191 and live['publication_gets']==54 and live['pr_bindings']==17 and live['writes']==0,'Live scope')
 ck(not(A/'private_action/action01').exists() and load(A/'READINESS.json')['ready_for_execution'] is False,'Production guard changed')
 print(json.dumps({'status':'PASS_CLOSED_REVIEW_HOLD_REPLAY','review_manifest_sha256':sys.argv[1],'review_files':len(expected),'protected_input_files':len(orig['files']),'independent_copy_pins':len(pins['files']),'scientific_clearances':32,'retained_normal_cases':305,'fresh_three_mode_cases':144,'PR_reference_cases':12,'incorrect_fake_verified_receipts':bad,'URL_controls_rejected':good,'cold_history_files':cold_members,'live_old_rows':191,'live_publication_GETs':54,'live_PR_bindings':17,'read_only_no_writes':True,'action_review_accepted':False},sort_keys=True))
if __name__=='__main__':main()
