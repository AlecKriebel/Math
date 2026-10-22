"""Dated individual exact-body rebindings and explicit cross-result proposals, never approvals."""
from pathlib import Path
import json,gzip,hashlib,types,sys,datetime
O=Path(__file__).resolve().parent;OLD=O.with_name('existing_publication_remaining34_preparation01');D=O.with_name('existing_publication_remaining_rows_inventory01');R=O.parent.parent
def gz(p):return json.loads(gzip.decompress(p.read_bytes()))
def sha(b):return hashlib.sha256(b).hexdigest()
def jb(v):return (json.dumps(v,sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode()
p=O/'source/ops_core.py';C=types.ModuleType('ops_core');exec(compile(p.read_bytes(),str(p),'exec',optimize=0),C.__dict__)
plan=json.loads((O/'PROPOSAL.json').read_bytes());items={i['pr']:i for i in plan['items']};scopes=json.loads((O/'EXACT_TARGET_AND_ELEVEN_SCOPE_CONTEXT.json').read_bytes());target={int(k):v for k,v in scopes['target34'].items()};other11={int(k):v for k,v in scopes['separate11'].items()}
obs=json.loads((O/'INITIAL_READONLY_COLLECTION.json').read_bytes());numeric=gz(O/obs['numeric']['path']);owned=gz(O/obs['owned_complete'][0]['path'])['records'];local=gz(O/obs['local']['path']);public=gz(O/'private/PUBLIC_INITIAL_COMPLETE.json.gz')['results'];follow=gz(O/'private/PUBLIC_1253_FOLLOWUP.json.gz');assert follow['error']is None and follow['result']['status']==200;public['1253_registry_0']=follow['result']
requests=json.loads((O/'PUBLIC_REQUESTS_DISCOVERY.json').read_bytes())['requests'];assert set(public)=={r['key']for r in requests}
for r in requests:
 v=public[r['key']];r.update({k:v[k]for k in ['status','final_url','bytes','sha256']});r['qualification']='Exact dated complete body/route; original source/proof/DOI qualifications retained, not current proof verification.'
 if'body'in v:r['canonical_body_sha256']=sha(C.canonical(v['body']))
 if v['status']!=200:r['qualification']='Observed HTTP'+str(v['status'])+' access limit for this exact route. Independent registered/source identity remains inherited; no successful publisher-body retrieval or absence claim.'
prior_owned=gz(D/'private/terminal_owned_complete_pass1.json.gz')['records'];prior_local={x['state_path']:x for x in gz(D/'private/terminal_LOCAL_SCIENTIFIC_CARRIERS.json.gz')['items']};prior_index=gz(OLD/'private/FULL_CARRIER_REFERENCE_INDEX.json.gz')['carriers'];old_dec=gz(OLD/'private/CF_TYPED_MATCHER_SEMANTICS02.json.gz')['decisions'];bykey={}
for d in old_dec:bykey.setdefault((d['pr'],d['carrier_key']),[]).append(d)
oldlocals=gz(D/'private/terminal_LOCAL_SCIENTIFIC_CARRIERS.json.gz')['items'];local_key_by_path={x['state_path']:'local:'+str(n)for n,x in enumerate(oldlocals)}
def diff(a,b,path=''):
 if type(a)is not type(b):return[{'path':path,'old':a,'new':b}]
 if type(a)is dict:
  out=[]
  for k in sorted(a.keys()|b.keys()):out+=([{'path':path+'/'+str(k),'old_present':k in a,'new_present':k in b,'old':a.get(k),'new':b.get(k)}]if k not in a or k not in b else diff(a[k],b[k],path+'/'+str(k)))
  return out
 if type(a)is list:
  if len(a)!=len(b):return[{'path':path,'old':a,'new':b}]
  return sum((diff(x,y,path+'/'+str(n))for n,(x,y)in enumerate(zip(a,b))),[])
 return []if C.typed_equal(a,b)else[{'path':path,'old':a,'new':b}]
rebinds=[];carriers=[];newclaims={1372:'Variable-threshold NP-completeness of the INITIAL consecutive ODD prefix of OPEN ear decompositions on finite simple2-connected cones over connected bipartite bases; initial circuit and1-edge ears count, first even ear terminates the prefix. Not maximum total odd ears, closed ears or fixed-threshold hardness.',1330:'For oddq and sufficiently large naturaln, each separately specified eigenspace of an actual prescribed strong involution in Sp/O/SO/Omega receives a strong even-Bray restriction with c/logn probability, and O(logn(1+log1/delta)) samples contain the actual centralizer second derived subgroup. Not GL/GU/SL/SU prior results, characteristic2/projective/similitude/simultaneous/runtime/all-dimension extensions.'}
for n,row in enumerate(numeric['values'][1:],2):carriers.append({'kind':'sheet','key':'sheet:'+str(n),'body':row,'old_key':'sheet:'+str(n),'new_pr':1372 if n==238 else 1330 if n==239 else None})
for k,v in owned.items():
 old=prior_owned.get(k)
 if old is not None:
  assert C.typed_equal(old['metadata'],v['metadata']);rebinds.append({'kind':'owned','id':int(k),'scientific_metadata_full_typed_exact':True,'all_other_full_field_differences':diff(old,v),'new_full_body_sha256':sha(C.canonical(v))})
 carriers.append({'kind':'owned','key':'owned:'+k,'body':v,'old_key':'owned:'+k,'new_pr':1372 if k=='23576280'else 1330 if k=='23577484'else None})
for n,v in enumerate(local):
 path=v['state']['path'];old=prior_local.get(path)
 if old is not None:
  assert C.typed_equal(old['state'],v['state']['value'])and C.typed_equal(old.get('manifest'),v['scientific_manifest']['value']if v['scientific_manifest']else None)
  rebinds.append({'kind':'local','path':path,'entire_state_and_scientific_manifest_full_typed_exact':True,'old_state_sha256':old['state_sha256'],'new_state_sha256':v['state']['sha256'],'new_full_body_sha256':sha(C.canonical(v))})
 rid=v['state']['value'].get('id');carriers.append({'kind':'local','key':'local:'+str(n),'body':v,'old_key':local_key_by_path.get(path),'new_pr':1372 if rid==23576280 else 1330 if rid==23577484 else None})
for r in requests:
 v=public[r['key']]
 if'body'in v:carriers.append({'kind':'public','key':r['key'],'body':v['body'],'source_pr':r['target_prs'][0],'role':r['role'],'new_pr':r['target_prs'][0]if r['role']=='new_native'or(r['role']=='pr'and r['target_prs'][0]==1330)else None})
decisions=[];unknown=[];seen={}
for c in carriers:
 digest=sha(C.canonical(c['body']))
 for pr,item in items.items():
  hits=C.recursive_identity_hits(c['body'],item)
  if not hits:continue
  key=(pr,c['kind'],digest)
  if key in seen:seen[key]['complete_carrier_references'].append(c['key']);continue
  role='DISTINCT_EXACT_RESULT';reason=None;provenance={}
  if c.get('new_pr'):
   n=c['new_pr'];reason=newclaims[n]+' The distinct accounting target is: '+target[pr]
   if n==1330 and pr==1330:reason='The common problem identifier and cited linear/unitary DOIs require explicit scope separation: '+newclaims[n]+' The proposed row covers exclusively '+target[pr]
   provenance={'new_publication_pr':n,'all_five_carrier_scopes_separately_recorded':True}
  elif c['kind']=='public':
   n=c['source_pr'];assert n in items
   if n==pr:
    role='SAME_AUDITED_CANDIDATE_SOURCE_NOT_LEDGER_COVERAGE'if c['role']=='pr'else'SAME_SELECTED_EXISTING_PUBLICATION_NOT_LEDGER_COVERAGE';reason='This full '+c['role']+' object is bound to the exact existing source/candidate adopted for this target: '+target[pr]+'. It is source/PR evidence, not an already recorded ledger row, and grants no priority or project authorship.'
   else:reason='The complete '+c['role']+' carrier belongs to the separately authenticated source family of PR'+str(n)+': '+target[n]+' The target under comparison is '+target[pr]+'. Citation, editor/byline or term overlap does not identify these mathematical objects or conclusions.'
   provenance={'request_key':c['key'],'authenticated_source_pr':n,'qualified_source_contract_sha256':sha(C.canonical(items[n]['full_root_source_identity_contract']))}
  else:
   prior=bykey.get((pr,c.get('old_key')),[])
   if not prior:
    # Digest/namespace spelling is not used as a reason. Find the exact old
    # local/owned source index and its prior individually read mathematical scope.
    if c['kind']=='local':
     path=c['body']['state']['path'];poss=[x for x in prior_index if x['kind']=='local'and x['source'].get('items_index')==next((i for i,v in enumerate(oldlocals)if v['state_path']==path),-1)]
     prior=sum((bykey.get((pr,x['key']),[])for x in poss),[])
   if prior:
    d=prior[0];reason=d['scientific_reason']+' Current complete scientific metadata (owned) or the entire state+manifest (local), or the exact full prior ledger row, was checked unchanged. This is a NEW exact full-body proposal, not a generic projection or runtime change allowance.';provenance={'prior_carrier_key':d['carrier_key'],'prior_individual_decision_sha256':sha(C.canonical(d)),'prior_full_scope_witness':d['scope_witness']}
    if d['classification'].startswith('SAME_SELECTED'):role='SAME_SELECTED_EXISTING_PUBLICATION_NOT_LEDGER_COVERAGE'
   else:unknown.append({'pr':pr,'key':c['key'],'kind':c['kind'],'matched':hits,'body_sha256':digest});continue
  d={'pr':pr,'kind':c['kind'],'body_sha256':digest,'matched':hits,'target_four_cells_sha256':item['row_sha256'],'classification':role,'scientific_reason':reason,'root_adopted':False,'complete_carrier_references':[c['key']],'provenance':provenance};decisions.append(d);seen[key]=d
intra=[]
for a,i in items.items():
 for b,j in items.items():
  if a==b:continue
  intra.append({'pr':a,'other_pr':b,'target_four_cells_sha256':i['row_sha256'],'other_row_sha256':j['row_sha256'],'classification':'DISTINCT_EXACT_RESULT','scientific_reason':'Exact target scope: '+target[a]+' Other exact qualified scope: '+target[b]+'. Their mathematical objects, hypotheses and required conclusions are the stated distinct targets; shared provenance terms are not duplicate results.','root_adopted':False})
cross=[]
for a,i in items.items():
 for j in plan['separate_eleven_context']:
  b=j['pr'];cross.append({'pr':a,'other_pr':b,'target_four_cells_sha256':i['row_sha256'],'other_row_sha256':j['row_sha256'],'classification':'DISTINCT_EXACT_RESULT','scientific_reason':'Target: '+target[a]+' Separately proposed source-only target: '+other11[b]+'. These exact object classes and conclusions differ; the separate row is neither appended nor treated as ledger coverage in this batch.','root_adopted':False})
gate={'schema':'remaining34-external-reviewed-gate-v2','plan_sha256':sha((O/'PROPOSAL.json').read_bytes()),'plan_canonical_sha256':sha(C.canonical(plan)),'semantic_decisions':decisions,'intrabatch':intra,'cross_batch_eleven':cross,'separate_eleven_prs':[x['pr']for x in plan['separate_eleven_context']],'public_requests':requests,'root_action_adopted':False,'action_authority':False,'unresolved':unknown,'dated_observation':obs['finished'],'limits':'Proposed individual exact objects and inherited qualified scientific contracts. Root/independent approval must bind complete raw gate bytes; no metadata/source status is a new proof or priority audit.'}
raw=jb(gate);(O/'private/REVIEWED_GATE_PROPOSED.json.gz').write_bytes(gzip.compress(raw,mtime=0));(O/'private/CURRENT_CARRIER_REBINDS.json.gz').write_bytes(gzip.compress(jb({'rebindings':rebinds,'automatic_runtime_waivers':False}),mtime=0));index=[{k:v for k,v in c.items()if k!='body'}|{'body_sha256':sha(C.canonical(c['body']))}for c in carriers];(O/'private/CURRENT_CARRIER_REFERENCE_INDEX.json.gz').write_bytes(gzip.compress(jb(index),mtime=0));out={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'gate_raw_sha256':sha(raw),'gate_raw_bytes':len(raw),'carrier_count':len(carriers),'all_pairs':len(carriers)*34,'positive_decisions':len(decisions),'intrabatch':len(intra),'cross_eleven':len(cross),'individual_rebindings':len(rebinds),'unknown':unknown,'action_authority':False};(O/'GATE_PROPOSAL_RECEIPT.json').write_bytes(jb(out));print(json.dumps(out,ensure_ascii=False))
