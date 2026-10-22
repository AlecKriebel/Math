from pathlib import Path
import collections,datetime,hashlib,json,shutil,subprocess,sys
R=Path('/Users/alec/Documents/Math');D=R/'draft_pr_claimed_solved_700_800_20261012';T=D/'audits/pr799_30002364/tmp';M=T/'root-receipts'
sys.path.insert(0,str(D));from graphql_scoped_commit import gql,Remote
def need(ok,msg):
 if not ok:raise RuntimeError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
S=D/'final_screen_20261016';P=S/'packet'
MP='18a9c5af827deeffbb20b947db499023ac6ca3030662cd62801651757d989c80'
CP='8cbfc42ea0fb21a9e6e123067bfe664de9895082a13b1e7a1d180e4aeb8256fe'
need(sha(P/'MANIFEST.json')==MP and sha(P/'verify_certificate.py')==CP,'screen external pins')
cert=json.loads((P/'CERTIFICATE.json').read_text());old={r['number']:r for r in cert['rows']}
r=subprocess.run([sys.executable,'-I','-S','-B',str(P/'verify_certificate.py'),str(P),MP,CP,str(R),'--replay-blobs'],cwd='/',capture_output=True,text=True,timeout=120)
need(r.returncode==0 and not r.stderr,'original final screen source replay')
replay=json.loads(r.stdout);need(replay['source_blobs_replayed']==90,'source replay count')
runner=S/'run_controls.py';need(sha(runner)=='049da90741a6852f39d37fb1a328759f7e3641a5e4cc2e543d865600e8900cf5','external control runner pin')
copy=T/'root-final-screen-controls';need(not copy.exists(),'never overwrite root control copy');copy.mkdir()
shutil.copytree(P,copy/'packet');shutil.copyfile(runner,copy/runner.name)
r=subprocess.run([sys.executable,'-I','-S','-B',str(copy/runner.name)],cwd='/',capture_output=True,text=True,timeout=120)
need(r.returncode==0 and not r.stderr,'screen controls')
controls=json.loads((copy/'CONTROL_RESULTS.json').read_text());need(controls['status']=='PASS' and controls['control_count']==8,'eight screen controls')
(M/'ROOT_FINAL_SCREEN_CONTROLS.json').write_text(json.dumps(controls,indent=2)+'\n')
started=datetime.datetime.now(datetime.timezone.utc).isoformat()
fields='number title state isDraft merged headRefOid headRefName closedAt url mergeCommit { oid }'
def capture():
 result=[]
 for start in range(700,801,25):
  ns=list(range(start,min(start+25,801)))
  aliases=' '.join(f'p{n}:pullRequest(number:{n}){{{fields}}}' for n in ns)
  q='query { repository(owner:"AlecKriebel",name:"Math") { '+aliases+' } }'
  data=gql(q)['repository'];need(set(data)=={f'p{n}' for n in ns},'complete direct-number aliases')
  result.extend(data['p'+str(n)] for n in ns)
 need([r['number'] for r in result]==list(range(700,801)),'all101 integers')
 return result
before=capture();rows=[]
for meta in before:
 n=meta['number'];row={**meta,'queue_inspected':False}
 if meta['state']=='OPEN' and meta['isDraft']:
  previous=old[n];problem=previous['problem_id']
  need(problem in meta['headRefName'],'unambiguous unchanged problem identity')
  if meta['headRefOid']==previous['headRefOid'] and previous['queue_inspected']:
   own=previous['own_row'];status=previous['queue_status'];turns=previous['queue_turns']
   source={'method':'same immutable head/blob as independently replayed certificate','blob_oid':previous['queue_blob_oid'],'blob_sha256':previous['queue_blob_sha256']}
  else:
   raw=Remote(meta['headRefOid']).read('unsolved_math_prioritization/QUEUE.md')
   ownrows=[l for l in raw.splitlines() if l.startswith('| ') and (' '+problem+' / ') in l]
   need(len(ownrows)==1,'unique exact-head own row');own=ownrows[0];cells=own.split('|');need(len(cells)==14,'12column schema')
   status=cells[8].strip();turns=cells[9].strip()
   source={'method':'fresh immutable-head QUEUE only','blob_sha256':hashlib.sha256(raw.encode()).hexdigest()}
  row.update(queue_inspected=True,problem=problem,own_row=own,queue_status=status,turns=turns,source=source,
             decision='eligible' if status=='claimed_solved' else 'skip_without_processing')
 rows.append(row)
after=capture();need(before==after,'metadata changed during fresh final screen')
eligible=[r['number'] for r in rows if r.get('decision')=='eligible']
merged=[r['number'] for r in rows if r['merged']]
closed=[r['number'] for r in rows if r['state']=='CLOSED' and not r['merged']]
expected_merged=[718,742,764,765,778,781,786,788,789];expected_closed=[734,767,799]
need(merged==expected_merged and closed==expected_closed,'processed outcome metadata drift')
need(eligible==[],'new eligible PRs remain; resume ascending processing')
need([r['number'] for r in rows if r['state']=='OPEN' and r['isDraft']]==[r['number'] for r in rows if r.get('decision')=='skip_without_processing'],'every remaining draft exact-other-status')
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'started_utc':started,'result':'PASS','all101numbers_queried_twice':True,'metadata_stable':True,'complete_rows':rows,'merged':merged,'closed_unmerged':closed,'open_draft_status_counts':dict(collections.Counter(r['queue_status'] for r in rows if r['queue_inspected'])),'remaining_exact_claimed_solved':eligible,'no_skipped_mathematics_read_or_mutated':True,'source_certificate_manifest':MP,'source_certificate_checker':CP,'root_prior_certificate90blob_replay':replay,'root_screen_controls':8,'fresh_PR799_closed_same_head':next(r for r in rows if r['number']==799)['headRefOid']=='cc45ec9dc93515593c3b2a228def86c3a562e13f'}
(M/'ROOT_FINAL_RECONCILIATION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['complete_rows','root_prior_certificate90blob_replay']}))
