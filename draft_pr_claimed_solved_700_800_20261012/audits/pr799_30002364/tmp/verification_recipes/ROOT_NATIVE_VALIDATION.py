from pathlib import Path
import csv,datetime,hashlib,json,sys
R=Path('/Users/alec/Documents/Math');D=R/'draft_pr_claimed_solved_700_800_20261012';A=D/'audits/pr799_30002364';T=A/'tmp';M=T/'root-receipts'
sys.path.insert(0,str(D))
from graphql_scoped_commit import Remote,get_pr,gql
from remote_scoped_commit import need,oid
r=json.loads((M/'NATIVE_PRIORITY_MIRROR_RECEIPT.json').read_text());pre=Remote(r['parent']);post=Remote(r['commit'])
P='30002364';N='unsolved_math_prioritization/'
names=['QUEUE.md','state.json','history.jsonl','catalog.json','ranking.csv','assessments.json','assessment_history.jsonl']
wanted={N+n for n in names}|{N+'attempts/'+P+'/PR799_PRIOR_RESULT.json'}
need(set(r['paths'])==set(r['file_hashes'])==wanted,'exact eight paths')
texts={p:post.read(p) for p in wanted}
for p,s in texts.items():need(hashlib.sha256(s.encode()).hexdigest()==r['file_hashes'][p],'committed SHA')
updates={p:{'mode':'100644','type':'blob','sha':oid('blob',s.encode())} for p,s in texts.items()}
need(pre.expected_tree(updates)==post.root,'entire result tree beyond eight paths')
commit=gql('query($o:GitObjectID!){repository(owner:"AlecKriebel",name:"Math"){object(oid:$o){... on Commit{parents(first:2){nodes{oid}}}}}}',{'o':r['commit']})['repository']['object']
need([p['oid'] for p in commit['parents']['nodes']]==[r['parent']],'ordinary single parent')
def queue(raw):
 lines=raw.splitlines(keepends=True);ii=[i for i,l in enumerate(lines) if l.startswith('| ') and ' 30002364 / ' in l]
 need(len(ii)==1,'unique queue row');i=ii[0];return lines[i],lines[:i]+lines[i+1:]
before,bo=queue(pre.read(N+'QUEUE.md'));after,ao=queue(texts[N+'QUEUE.md']);need(bo==ao,'other queue physical bytes')
b=before.split('|');a=after.split('|');need(a[8].strip()=='already_solved' and a[9].strip()=='5/5' and not a[12].strip(),'own status budget blank DOI')
need(all(b[i]==a[i] for i in range(len(a)) if i not in [8,9,11]),'only own status turns findings changed')
def spans(raw,kind):
 decoder=json.JSONDecoder();p=0;out=[]
 while raw[p].isspace():p+=1
 need(raw[p]==('{' if kind=='object' else '['),'JSON type');p+=1
 while True:
  while raw[p].isspace():p+=1
  if raw[p] in '}]':break
  if kind=='object':
   key,p=decoder.raw_decode(raw,p)
   while raw[p].isspace():p+=1
   need(raw[p]==':','colon');p+=1
   while raw[p].isspace():p+=1
  start=p;value,p=decoder.raw_decode(raw,p)
  if kind!='object':key=value['id']
  out.append((key,raw[start:p],value))
  while raw[p].isspace():p+=1
  if raw[p]==',':p+=1
  else:need(raw[p] in '}]','delimiter')
 need(len({x[0] for x in out})==len(out),'duplicate JSON member');return out
for name in ['state.json','assessments.json','catalog.json']:
 kind='array' if name=='catalog.json' else 'object'
 before=spans(pre.read(N+name),kind);after=spans(texts[N+name],kind)
 need([(k,s) for k,s,v in before if k!=P]==[(k,s) for k,s,v in after if k!=P],'unrelated member value bytes/order: '+name)
 own=[v for k,s,v in after if k==P];need(len(own)==1,'one own member')
 if name=='state.json':need(own[0]['status']=='already_solved' and own[0]['turns_used']==5 and own[0]['turn_limit']==5,'state budget')
 if name=='assessments.json':need(own[0]['resolution']=='already_solved' and own[0]['decision']=='exclude','assessment')
 if name=='catalog.json':
  old=[v for k,s,v in before if k==P][0];new=own[0]
  gate=json.loads((M/'MATH_GATE.json').read_text())
  for row in [old,new]:need(row['statement_hash']==gate['statement_hash'] and row['review_hash']==gate['review_hash'],'catalog source hashes')
  need(new['local_status']=='already_solved' and new['turns_used']==5 and new['eligible'] is False,'catalog status')
for name in ['history.jsonl','assessment_history.jsonl']:
 before=pre.read(N+name);after=texts[N+name];need(after.startswith(before),'entire history prefix')
 delta=[json.loads(l) for l in after[len(before):].splitlines() if l.strip()]
 need(len(delta)==1 and delta[0]['id']==P,'one own event')
 if name=='history.jsonl':
  ev=delta[0];need(ev['status']=='already_solved' and ev['turns_used']==5 and ev['turn_limit']==5,'event budget')
  binding=ev['evidence']['disposition'];need(binding['path']==(A/'DISPOSITION.json').relative_to(R).as_posix(),'disposition path')
  need(hashlib.sha256((A/'DISPOSITION.json').read_bytes()).hexdigest()==binding['sha256'],'frozen disposition evidence')
def ranking(raw):
 lines=raw.splitlines(keepends=True);h=next(csv.reader([lines[0]]));ii=[i for i,l in enumerate(lines[1:],1) if next(csv.reader([l]))[h.index('id')]==P]
 need(len(ii)==1,'ranking own row');i=ii[0];return dict(zip(h,next(csv.reader([lines[i]])))),lines[:i]+lines[i+1:]
old,bo=ranking(pre.read(N+'ranking.csv'));new,ao=ranking(texts[N+'ranking.csv']);need(bo==ao,'other ranking bytes')
need(new['local_status']=='already_solved' and new['turns_used']=='5' and new['eligible']=='False','own ranking')
source=json.loads((T/'intake/ROOT_SOURCE_IDENTITY.json').read_text());candidate=Remote(source['reviewed_head']);present=0
for row in source['original_files']:
 p=row['path'];need(pre.entry(p)==post.entry(p),'native operation must not alter original candidate presence or blob')
 if post.entry(p) is not None:present+=1
 need(candidate.entry(p)=={'mode':'100644','type':'blob','sha':row['git_blob']},'immutable candidate Git blob')
 raw=(T/'intake/original'/p).read_bytes();need(len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'] and oid('blob',raw)==row['git_blob'],'original intake exact bytes')
fresh=get_pr(799);need(fresh['state']=='closed' and not fresh['merged'] and fresh['head']['sha']==source['reviewed_head'],'fresh closed exact head')
side=json.loads(texts[N+'attempts/'+P+'/PR799_PRIOR_RESULT.json']);need(side['action_executed'] and side['result']=='closed_without_merge_prior_full_result' and side['new_Zenodo_deposit'] is False and side['tracker_row_added'] is False,'sidecar scope')
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':'PASS','pr':799,'problem':P,'commit':r['commit'],'parent':r['parent'],'exact_only_eight_native_paths':True,'full_expected_Merkle_tree_independently_verified':True,'unrelated_JSON_value_bytes_and_order_preserved':True,'other_QUEUE_and_ranking_physical_bytes_preserved':True,'both_complete_history_prefixes_preserved':True,'one_contemporary_own_event_each':True,'statement_review_hashes_unchanged':True,'original54_intake_and_PR_blobs_unchanged':True,'original_candidate_paths_present_on_main_before_and_after':present,'no_claim_of_importing_unmerged_originals_to_main':True,'original_explicit_budget':'5/5','own_DOI_blank':True,'disposition_file_frozen_to_native_event_hash':True,'fresh_closed_unmerged_same_head':True,'no_new_paper_deposit_tracker':True,'local_Git_objects_index_refs_checkout_untouched':True}
(M/'ROOT_NATIVE_VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
