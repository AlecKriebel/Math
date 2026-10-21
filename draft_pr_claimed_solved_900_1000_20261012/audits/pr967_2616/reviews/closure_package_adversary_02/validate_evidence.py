import pathlib,json,hashlib,datetime,stat
W=pathlib.Path('/Users/alec/Documents/Math');P=W/'draft_pr_claimed_solved_900_1000_20261012';A=P/'audits/pr967_2616';R=A/'reviews/closure_package_adversary_02'
def sha(b):return hashlib.sha256(b).hexdigest()
def need(ok,m):
 if not ok:raise RuntimeError(m)
rows=[]
for mode,opt in [('normal',0),('O',1),('OO',2)]:
 for kind,count,status in [('REPAIR01',200,'PASS_OFFLINE_CONTROLS_ONLY'),('REPAIRED_FINITE',46,'PASS_FINITE_FLOAT_AND_OVERFLOW_CONTROLS'),('BASELINE_FINITE',46,'LEGACY_DEFECT_REPRODUCED_NO_CLEAN_CREDIT')]:
  folder=A/'closure_engineering_02';base=kind+'_'+mode;b=(folder/(base+'.stdout.raw')).read_bytes();err=(folder/(base+'.stderr.raw')).read_bytes();launch=json.loads((folder/(base+'.launch.json')).read_bytes());o=json.loads(b)
  need(not err and launch['returncode']==0 and o['outer_optimization']==opt and o['event_count']==count and len(o['events'])==count and o['status']==status,'old actual raw '+base)
  names=[(x.get('helper'),x['test'])for x in o['events']];need(len(names)==len(set(names)),'event duplicates '+base)
  allowed={'PASS','REJECTED_EXPECTED'}if count==200 else {'PASS_FINITE','REJECTED_EXPECTED','KNOWN_LEGACY_DEFECT_ACCEPTED_NONFINITE'}if kind=='BASELINE_FINITE'else{'PASS_FINITE','REJECTED_EXPECTED'};need(all(x['status']in allowed for x in o['events']),'event status')
  if kind!='BASELINE_FINITE':
   own=json.loads((R/(('OFFLINE'if count==200 else'FINITE')+'_'+mode+'.stdout.raw')).read_bytes());need(own==o,'cold current mismatch '+base)
  rows.append({'kind':kind,'mode':mode,'count':count,'actual_optimization':opt,'status':status,'stdout_sha256':sha(b),'all_events_reviewed':True,'statuses':{s:sum(x['status']==s for x in o['events'])for s in allowed},'event_names':[x['test']for x in o['events']]})
# Exact repair delta for each entire helper, excluding any unrelated change.
deltas=[]
for n in ['close_pr967.py','finalize_pr967_and_gate_next.py']:
 old=(A/'closure_engineering_02'/('BASE_'+n)).read_bytes();new=(P/n).read_bytes();expected=old.replace(b'hashlib,json,os,re,',b'hashlib,json,math,os,re,',1);token=b"    return json.loads(raw,object_pairs_hook=pairs,parse_constant=bad)";replacement=b"    def finite_float(text):\n        value=float(text)\n        need(math.isfinite(value),'nonfinite JSON float')\n        return value\n    return json.loads(raw,object_pairs_hook=pairs,parse_constant=bad,parse_float=finite_float)";need(old.count(token)==1 and expected.replace(token,replacement)==new,'unadvertised helper delta '+n);deltas.append({'file':n,'base_sha256':sha(old),'current_sha256':sha(new),'only_math_import_and_finite_float_callback':True})
dis=json.loads((A/'ROOT_INDIVIDUAL_FAMILY_FINDING_DISPOSITIONS.json').read_bytes());counts={k:len(v)for k,v in dis['families'].items()};need(sum(counts.values())==35,'all35');ids=[x['id']for v in dis['families'].values()for x in v];need(len(set(ids))==35,'unique35')
# Preserve and validate actual prior failed review, with no inherited clean credit.
old=json.loads((A/'reviews/closure_package_adversary_01/RESULT.json').read_bytes());need(old['clean_for_closure']is False and old['required_issues']==[]and len(old['optional_issues'])==1 and old['optional_issues'][0]['id']=='O-C01','old adverse altered')
prioractual=json.loads((A/'reviews/closure_package_adversary_01/ACTUAL_READONLY_GATES.json').read_bytes());priorlaunch=json.loads((A/'reviews/closure_package_adversary_01/TRUSTED_LAUNCHER_REPRODUCTIONS.json').read_bytes())
# All53 evidence bodies are decoded/parsed in full after their external authentication.
evidence=json.loads((A/'PRIORITY_DISPOSITION.json').read_bytes())['evidence_files'];parsed=[]
for name,e in evidence.items():
 b=(W/name).read_bytes();need(sha(b)==e['sha256']and len(b)==e['bytes'],'53drift')
 if name.endswith('.json'):obj=json.loads(b);parsed.append({'path':name,'top_level':list(obj)if isinstance(obj,dict)else str(type(obj)),'bytes':len(b)})
(R/'EVIDENCE_VALIDATION.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'engineering_raw_current_and_baseline':rows,'helper_deltas':deltas,'all35_disposition_counts':counts,'all35_ids':ids,'old01_remains_nonclean':True,'prior_actual_readonly_record_read':True,'prior_actual_launcher_record_read':True,'all53_evidence_authentic':True,'json_evidence_full_parse':parsed},indent=2)+'\n');print(json.dumps({'status':'PASS','current_raw_controls_per_mode':[200,46],'historical_baseline_per_mode':46,'all35counts':counts,'all53':len(evidence),'old_review_nonclean':True}))
