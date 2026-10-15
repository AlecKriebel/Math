from pathlib import Path
import json,hashlib,subprocess,sqlite3,re,collections,datetime
HERE=Path(__file__).resolve().parent;A=HERE.parent;ROOT=A.parents[2]
HEAD='aa99d4a36eff79cbb7aae55ce3ffe4a0eb31af95';PREFIX='unsolved_math_prioritization/attempts/2800102/'
checks=[]
def sha(b):return hashlib.sha256(b).hexdigest()
def ck(name,value,detail=None):
 checks.append({'name':name,'pass':bool(value),'detail':detail})
 if not value:raise AssertionError(name)
def command(*x):return subprocess.check_output(x,cwd=ROOT).decode()
MANIFESTS=[('source_snapshot',A/'snapshot_manifest.json'),('reviewed_candidate',A/'reviewed_candidate/MANIFEST.json')]+[(d,A/d/'MANIFEST.json') for d in ['primary_scope_family','complex_family','real_family','real_dependency_falsifier']]
summary=[]
for name,p in MANIFESTS:
 m=json.loads(p.read_text());entries=m['files'];fp=0
 for f in entries:
  data=(A/name/f['path']).read_bytes();ck(name+':bytes:'+f['path'],len(data)==f['bytes']);ck(name+':hash:'+f['path'],sha(data)==f['sha256']);fp+=not f.get('ignored_runtime_or_foreign',False)
 summary.append({'name':name,'entries':len(entries),'first_party_entries':fp,'manifest_sha256':sha(p.read_bytes())})
ck('exact23manifest',len(json.loads((A/'reviewed_candidate/MANIFEST.json').read_text())['files'])==23)
ck('given_candidate_manifest_sha',sha((A/'reviewed_candidate/MANIFEST.json').read_bytes())=='daeb6f57f65bea40d5392eaec732ba4e024af36653530458b6d1805396f408a1')
ck('given_current_source_sha',sha((A/'reviewed_candidate/SOURCE_AUDIT.md').read_bytes())=='cf775d9ed6ac85cecfb37a8b1f09e253b4eb5fd21681cf579bf987630f2a6569')
sm=json.loads((A/'snapshot_manifest.json').read_text())
for f in sm['files']:
 data=(A/'source_snapshot'/f['path']).read_bytes();g=subprocess.check_output(['git','show',HEAD+':'+PREFIX+f['path']],cwd=ROOT)
 ck('original_head:'+f['path'],data==g)
 ck('original_git_blob:'+f['path'],hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==f['git_blob_sha1'])
 current=A/'reviewed_candidate'/f['path'];archive=A/'reviewed_candidate'/('ORIGINAL_'+f['path'])
 ck('original_current_or_archive:'+f['path'],(archive if archive.exists() else current).read_bytes()==data)
for d,file,sealf,k in [('primary_scope_family','SEALED_CRITERION.md','SEAL.json','criterion_sha256'),('real_family','SEALED_RECONSTRUCTION.md','SEAL.json','sha256')]:
 s=json.loads((A/d/sealf).read_text());ck('seal:'+d,sha((A/d/file).read_bytes())==s[k])
s=json.loads((A/'ROOT_RECONSTRUCTION_SEAL.json').read_text());ck('seal:root',sha((A/'ROOT_RECONSTRUCTION.md').read_bytes())==s['sha256'])
ck('seal:real_dependency_falsifier',sha((A/'real_dependency_falsifier/EARLY_SEAL_v1.md').read_bytes())==(A/'real_dependency_falsifier/EARLY_SEAL_v1.sha256').read_text().split()[0])
ck('seal:complex_family_recorded_digest',sha((A/'complex_family/INDEPENDENCE_SEAL.md').read_bytes())=='acc2fcd45beb69e1883f3b38f5b2b416acd5a7a23d3b54267b6386e2fafbd22d')
deps=json.loads((A/'reviewed_candidate/CURRENT_PROOF_DEPENDENCIES.json').read_text())
for f in deps['supporting_first_party_files']:
 data=(ROOT/f['path']).read_bytes();ck('dependency:'+f['path'],len(data)==f['bytes'] and sha(data)==f['sha256'])
manifest=json.loads((ROOT/'unsolved_math_prioritization/manifest.json').read_text());corpus={}
for name,f in manifest['files'].items():
 data=(ROOT/'unsolved_math_prioritization/cache'/name).read_bytes();ck('full_corpus:'+name,len(data)==f['bytes'] and sha(data)==f['sha256']);corpus[name]=json.loads(data)
problems=corpus['problems.json'];reports=corpus['research_results.json'];ck('15458records',len(problems)==manifest['records']==15458)
counts=collections.Counter(x['problem_number'] for x in problems)
record=json.loads((A/'source_snapshot/source_record.json').read_text());report=json.loads((A/'source_snapshot/prior_report.json').read_text())
selected=[p for p in problems if p['id']==2800102];ck('numeric_exactidentity',len(selected)==1 and selected[0]==record)
ck('code_exactidentity',[p['id'] for p in problems if p['problem_number']=='AMR-027-0102']==[2800102]);ck('prior_payload_exact',reports['AMR-027-0102']==report)
dbfile=ROOT/'unsolved_math_prioritization/cache/catalog.sqlite';db=sqlite3.connect('file:'+str(dbfile)+'?mode=ro',uri=True)
ck('sqlite_revision',db.execute('SELECT revision FROM metadata').fetchall()==[(manifest['revision'],)])
rows=db.execute('SELECT key,payload,report FROM records').fetchall();ck('sqlite15458',len(rows)==15458)
raw={str(p['id']):p for p in problems};mismatch=[]
for key,payload,rep in rows:
 p=dict(raw[key]);ambiguous=counts[p['problem_number']]>1 and p['problem_number'] in reports
 if ambiguous:p['_ambiguous_report']=True
 want={} if ambiguous else reports.get(p['problem_number'],{})
 if json.loads(payload)!=p or json.loads(rep)!=want:mismatch.append(key)
ck('full_sqlite_payload_prior_join',not mismatch,mismatch);db.close()
normalize=lambda s:re.sub(r'\s+',' ',s).strip().casefold()
identical=[p['id'] for p in problems if normalize(p.get('statement',''))==normalize(record['statement'])];ck('normalized_statement_unique',identical==[2800102],identical)
related=[{'id':p['id'],'number':p.get('problem_number'),'title':p.get('title'),'statement':p.get('statement')} for p in problems if re.search(r'singular.value|1606.00494|monotonicity of singular',p.get('title','')+' '+p.get('statement','')+' '+p.get('background',''),re.I)]
(HERE/'tmp/related_full_payloads.json').write_text(json.dumps(related,indent=2)+'\n')
ck('related_group_absent','2800102' not in (ROOT/'unsolved_math_prioritization/review_v2/related_target_groups.json').read_text())
changed=command('git','diff','--name-only',sm['actual_merge_base'],HEAD).splitlines();ck('actual17changed',set(changed)==set(sm['changed_paths']) and len(changed)==17)
qdiff=command('git','diff','--unified=0',sm['actual_merge_base'],HEAD,'--','unsolved_math_prioritization/QUEUE.md');(HERE/'tmp/original_queue.diff').write_text(qdiff)
changed_rows=[s for s in qdiff.splitlines() if s.startswith(('+|','-|'))];ck('only_selected_queue_row',len(changed_rows)==2 and all('2800102 / AMR-027-0102' in s for s in changed_rows))
pr=json.loads(command('gh','pr','view','25','--json','number,url,title,state,isDraft,headRefOid,headRefName,baseRefOid,body,files'))
(HERE/'tmp/fresh_live_pr.json').write_text(json.dumps(pr,indent=2)+'\n')
ck('remote_original_exacthead',pr['headRefOid']==HEAD);ck('remote_open_draft',pr['state']=='OPEN' and pr['isDraft']);ck('remote_original17files',{x['path'] for x in pr['files']}==set(changed))
ck('current_body_matches_live',pr['body']==(A/'current_pr_body.md').read_text());ck('candidate_body_matches_live',pr['body']==(A/'reviewed_candidate/pr_body.md').read_text())
prsearch=[]
for query in ['2800102','AMR-027-0102','Gaussian monotonicity']:
 prs=json.loads(command('gh','pr','list','--state','all','--limit','100','--search',query,'--json','number,title,url,state,headRefName'))
 prsearch.append({'query':query,'limit':100,'results':prs});ck('bounded_remote_duplicate_search:'+query,all(x['number']==25 for x in prs))
(HERE/'tmp/bounded_pr_searches.json').write_text(json.dumps(prsearch,indent=2)+'\n')
ck('no_original_attempt_merge_base',not command('git','ls-tree','--name-only',sm['actual_merge_base'],PREFIX).strip())
history=command('git','log','--format=%H %cI %s',HEAD,'--',PREFIX);(HERE/'tmp/original_attempt_git_history.txt').write_text(history);ck('original_single_attempt_commit',len(history.strip().splitlines())==1 and history.startswith('94641588dc23568e01b4dc8304d95de4ba7b034d'))
revision='37e53eabe540fb458758e198be61634bd02ee008'
absent=[]
local_tree=subprocess.run(['git','cat-file','-e',revision+'^{tree}'],cwd=ROOT,capture_output=True,text=True)
ck('source_revision_is_not_local_repository_tree',local_tree.returncode!=0)
# Dataset revision pins raw corpus. It cannot reconstruct the research
# repository's later QUEUE/related-group or historical remote search.
for path in ['unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/review_v2/related_target_groups.json']:
 first=command('git','log','--reverse','--format=%H %cI',HEAD,'--',path).splitlines()
 absent.append({'path':path,'repository_first_addition':first[0] if first else None,'dataset_revision_is_repository_baseline':False})
ck('source_revision_not_replaybaseline',all(not x['dataset_revision_is_repository_baseline'] for x in absent))
statepath=ROOT/'unsolved_math_prioritization/state.json';hpath=ROOT/'unsolved_math_prioritization/history.jsonl';assessmentpath=ROOT/'unsolved_math_prioritization/assessments.json'
state=json.loads(statepath.read_text());historyevents=[json.loads(s) for s in hpath.read_text().splitlines() if s.strip()]
ck('current_no25canonical_state','2800102' not in state);ck('current_no25canonical_history',not any(str(x.get('id'))=='2800102' for x in historyevents))
original_state=json.loads(command('git','show',HEAD+':unsolved_math_prioritization/state.json'));ck('original_no25canonical_state','2800102' not in original_state)
original_history=command('git','show',HEAD+':unsolved_math_prioritization/history.jsonl');ck('original_no25canonical_history',not any(str(json.loads(x).get('id'))=='2800102' for x in original_history.splitlines() if x.strip()))
a=json.loads((A/'reviewed_candidate/attempt.json').read_text());old=json.loads((A/'source_snapshot/attempt.json').read_text())
ck('preserved0of5',a['substantive_attempts_used']==old['substantive_attempts_used']==0 and a['substantive_attempt_limit']==old['substantive_attempt_limit']==5);ck('no_campaign_credit',not a['novel_result_claimed'] and not a['campaign_solution_credit'] and not a['full_resolution_claimed_by_this_attempt']);ck('current_gate_pending',json.loads((A/'reviewed_candidate/current_status.json').read_text())['current_complete_gate']=='pending')
accepted=[{'id':key,'record':value} for key,value in state.items() if value.get('accepted_pr') or value.get('acceptance') or value.get('program_acceptance')]
# Preserve full current state/history rather than relying on an incomplete field-name guess.
(HERE/'tmp/current_canonical_state.json').write_bytes(statepath.read_bytes());(HERE/'tmp/current_canonical_history.jsonl').write_bytes(hpath.read_bytes())
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'passed':len(checks),'failed':0,'checks':checks,'manifests':summary,'families_total_entries':sum(x['entries'] for x in summary[2:]),'families_first_party_entries':sum(x['first_party_entries'] for x in summary[2:]),'dependencies_verified':len(deps['supporting_first_party_files']),'selected_review_hash':sha(json.dumps([record,report],sort_keys=True).encode()),'selected_statement_hash':sha(record['statement'].encode()),'full_sqlite_rows_verified':len(rows),'sqlite_sha256':sha(dbfile.read_bytes()),'related_count':len(related),'source_revision_missing_paths':absent,'current_remote':{'head':pr['headRefOid'],'state':pr['state'],'isDraft':pr['isDraft'],'body_sha256':sha(pr['body'].encode())},'canonical_baseline':{'state_sha256':sha(statepath.read_bytes()),'history_sha256':sha(hpath.read_bytes()),'state_entry_count':len(state),'history_event_count':len(historyevents),'selected_effective_assessment':json.loads(assessmentpath.read_text()).get('2800102'),'selected_state_absent':True,'selected_history_absent':True},'limits':'Bounded present duplicate searches; absent raw historical global-search receipt remains historical attribution. Parent owns remote integration/final exact administrative binding and later present accepted mirror. No mutation.'}
(HERE/'INTEGRITY_RECEIPTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['checks','canonical_baseline']},indent=2))
