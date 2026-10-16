import sys,json,hashlib,csv,io,datetime
from pathlib import Path
R=Path('/Users/alec/Documents/Math'); D=R/'draft_pr_claimed_solved_700_800_20261012'; A=D/'audits/pr789_30001478/tmp'; M=A/'root-receipts'
sys.path.insert(0,str(D)); from graphql_scoped_commit import Remote,gql
from remote_scoped_commit import need,oid
receipt=json.loads((M/'NATIVE_ACCEPTANCE_RECEIPT.json').read_text()); post=Remote(receipt['commit']); pre=Remote(receipt['parent']); problem='30001478'; N='unsolved_math_prioritization/'
wanted={N+x for x in ['QUEUE.md','state.json','history.jsonl','catalog.json','ranking.csv']}|{N+'attempts/'+problem+'/acceptance.json',N+'attempts/'+problem+'/PREPRINT_PUBLICATION.md'}
need(set(receipt['paths'])==wanted and set(receipt['file_hashes'])==wanted,'Native path set')
rows={}; texts={}
for path in sorted(wanted):
 raw=post.read(path); need(hashlib.sha256(raw.encode()).hexdigest()==receipt['file_hashes'][path],'Committed native SHA mismatch')
 texts[path]=raw; rows[path]={'mode':'100644','type':'blob','sha':oid('blob',raw.encode())}
need(pre.expected_tree(rows)==post.root,'Native full tree differs beyond seven paths')
def queue_rows(raw):
 lines=raw.splitlines(keepends=True); own=[i for i,l in enumerate(lines) if l.startswith('| ') and ' 30001478 / ' in l]; need(len(own)==1,'Queue own row'); i=own[0]; return lines[i],lines[:i]+lines[i+1:]
oldqueue=pre.read(N+'QUEUE.md'); oldrow,otherold=queue_rows(oldqueue); newrow,othernew=queue_rows(texts[N+'QUEUE.md']); need(otherold==othernew,'Unrelated queue bytes')
beforecells=oldrow.split('|'); aftercells=newrow.split('|'); need(beforecells[8].strip()=='claimed_solved' and aftercells[8].strip()=='preprint_published' and beforecells[9]==aftercells[9] and aftercells[9].strip()=='1/5' and aftercells[12].strip()==receipt['doi'],'Own queue fields')
def root_spans(raw):
 d=json.JSONDecoder(); p=0
 while raw[p].isspace(): p+=1
 need(raw[p]=='{','Root JSON object'); p+=1; result=[]
 while True:
  while raw[p].isspace(): p+=1
  if raw[p]=='}': break
  k,e=d.raw_decode(raw,p); p=e
  while raw[p].isspace(): p+=1
  need(raw[p]==':','JSON colon'); p+=1
  while raw[p].isspace(): p+=1
  start=p; v,p=d.raw_decode(raw,p); result.append((k,raw[start:p],v))
  while raw[p].isspace(): p+=1
  if raw[p]==',': p+=1
  else: need(raw[p]=='}','JSON delimiter')
 need(len({x[0] for x in result})==len(result),'Duplicate JSON keys'); return result
beforestate=root_spans(pre.read(N+'state.json')); afterstate=root_spans(texts[N+'state.json'])
need([(k,v) for k,v,_ in beforestate if k!=problem]==[(k,v) for k,v,_ in afterstate if k!=problem],'Unrelated state JSON bytes/order')
need(len([x for x in afterstate if x[0]==problem])==1,'Own state entry')
ownstate=[v for k,_,v in afterstate if k==problem][0]
need(ownstate['status']=='preprint_published' and ownstate['turns_used']==1 and ownstate['turn_limit']==5 and ownstate['doi']==receipt['doi'],'Own state promotion and budget')
def array_spans(raw):
 d=json.JSONDecoder(); p=0
 while raw[p].isspace(): p+=1
 need(raw[p]=='[','Catalog array'); p+=1; result=[]
 while True:
  while raw[p].isspace(): p+=1
  if raw[p]==']': break
  start=p; v,p=d.raw_decode(raw,p); result.append((v['id'],raw[start:p],v))
  while raw[p].isspace(): p+=1
  if raw[p]==',': p+=1
  else: need(raw[p]==']','Array delimiter')
 need(len({x[0] for x in result})==len(result),'Duplicate catalog IDs'); return result
oldcat=array_spans(pre.read(N+'catalog.json')); newcat=array_spans(texts[N+'catalog.json'])
need([(k,v) for k,v,_ in oldcat if k!=problem]==[(k,v) for k,v,_ in newcat if k!=problem],'Unrelated catalog JSON bytes/order')
oldown=[v for k,_,v in oldcat if k==problem]; newown=[v for k,_,v in newcat if k==problem]; need(len(oldown)==len(newown)==1,'Catalog own cardinality')
gate=json.loads((A/'FINAL_READINESS.json').read_text())
for row in [oldown[0],newown[0]]:
 need(row['statement_hash']==gate['statement_hash'] and row['review_hash']==gate['review_hash'],'Catalog source hashes')
need(newown[0]['local_status']=='preprint_published' and newown[0]['turns_used']==1 and newown[0]['eligible'] is False,'Catalog promotion')
oldhist=pre.read(N+'history.jsonl'); newhist=texts[N+'history.jsonl']; need(newhist.startswith(oldhist),'Old history byte prefix')
events=[json.loads(l) for l in newhist[len(oldhist):].splitlines() if l.strip()]; need(len(events)==1 and events[0]['id']==problem and events[0]['doi']==receipt['doi'],'One contemporary event')
def rank(raw):
 lines=raw.splitlines(keepends=True); header=next(csv.reader([lines[0]])); idx=header.index('id'); own=[i for i,line in enumerate(lines[1:],1) if next(csv.reader([line]))[idx]==problem]; need(len(own)==1,'Ranking own row'); p=own[0]; return lines[p],lines[:p]+lines[p+1:]
_,oldrank=rank(pre.read(N+'ranking.csv')); _,newrank=rank(texts[N+'ranking.csv']); need(oldrank==newrank,'Unrelated ranking row bytes')
source=json.loads((A/'intake/ROOT_SOURCE_IDENTITY.json').read_text())
need(len(source['original_files'])==58 and source['reviewed_head']=='aa44dec3baf8c1cd179cf8b55f32be95c74ee81a','Exact original scientific identity')
need(hashlib.sha256((A/'intake/ROOT_SOURCE_IDENTITY.json').read_bytes()).hexdigest()=='92c0b6666f23bcab7624a7801d79247d8dc9a3d01333da8a300d2328da75db70','Original identity receipt pin')
for row in source['original_files']:
 need(post.entry(row['path'])=={'mode':'100644','type':'blob','sha':row['git_blob']},'Original candidate blob changed')
acceptance=json.loads(texts[N+'attempts/'+problem+'/acceptance.json']); need(acceptance['result']==gate['acceptance_result'] and acceptance['accepted_scope']==gate['accepted_scope'] and acceptance['reviewed_head']==gate['reviewed_head'],'Qualified acceptance')
for row in gate['publication_files']:
 b=(A/'preprint'/row['path']).read_bytes(); need(len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],'Frozen six drift')
# Independently bind actual parent, frozen readiness, publication and tracker.
actual=gql('query($o:GitObjectID!){repository(owner:"AlecKriebel",name:"Math"){object(oid:$o){...on Commit{oid parents(first:2){nodes{oid}}}}}}',{'o':receipt['commit']})['repository']['object']
need([p['oid']for p in actual['parents']['nodes']]==[receipt['parent']],'Actual native parent differs')
for field,path in [('final_readiness',A/'FINAL_READINESS.json'),('publication',A/'publication/PUBLISH_RECEIPT.json'),('tracker',A/'publication/SHEET_VERIFICATION.json')]:
 need(acceptance[field]['path']==path.relative_to(R).as_posix()and acceptance[field]['sha256']==hashlib.sha256(path.read_bytes()).hexdigest(),'Native immutable administration binding differs')
need(acceptance['turns_used']==1 and acceptance['turn_limit']==5 and acceptance['doi']==receipt['doi'],'Acceptance budget/DOI')
need(acceptance['priority_summary']==gate['priority_summary']and 'Nevins' in acceptance['priority_summary']and 'Campbell' in acceptance['priority_summary']and 'UNRESOLVED' in acceptance['priority_summary'],'Exact-algebra priority context lost')
need(acceptance['statement_hash']==gate['statement_hash']and acceptance['review_hash']==gate['review_hash'],'Acceptance source identity')
need(acceptance['publication_files']==gate['publication_files'],'Acceptance exact six binding')
need(hashlib.sha256((A/'preprint/source/MANIFEST.json').read_bytes()).hexdigest()==gate['source_manifest_sha256']=='50baca75de83bb4959f52b88762b020a65181428d200dffc4f343db8e026f9de','Source pin drift')
result={'verified_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':'PASS','pr':789,'problem':problem,'native_commit':receipt['commit'],'parent':receipt['parent'],'doi':receipt['doi'],'unrelated_JSON_value_bytes_and_order_preserved':True,'unrelated_QUEUE_and_ranking_row_bytes_preserved':True,'complete_old_history_byte_prefix_preserved':True,'new_contemporary_acceptance_events':1,'original_candidate_blobs_preserved':58,'explicit_budget':'1/5','source_hashes_preserved':True,'exact_six_relation_quotient_scope_and_NS_Campbell_characteristic_boundaries_preserved':True,'same_reviewed_six_published':True,'exact_native_paths':sorted(wanted),'all_seven_committed_file_hashes_match':True,'full_expected_Merkle_tree_independently_verified':True}
(M/'ROOT_NATIVE_VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n')
try: (A/'ROOT_NATIVE_VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n')
except OSError: pass
print(json.dumps(result),flush=True)
