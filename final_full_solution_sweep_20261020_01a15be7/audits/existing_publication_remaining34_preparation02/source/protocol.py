"""Remaining34 real one-attempt protocol; inherited01 guards, real authority/provider bridge."""
from pathlib import Path
import json,hashlib,copy
from ops_core import require,GateError,typed_equal,canonical,sha,strict_json
from journal import Journal
import numeric
COMPLETE_MAX_AGE=180
NATIVE_MAX_AGE=60
INTENT_MAX_AGE=600
PRODUCTION_ADAPTER_INCLUDED=True
VERIFY_SOURCE_CLOSURE=None

def row_hash(row):return sha(canonical(row+['']*(43-len(row))))
def validate(plan):
 require(type(plan['new_rows'])is int and plan['new_rows']==34 and type(plan['new_publications'])is int and plan['new_publications']==0,'Exact34 existing-publication scope')
 require(plan['preparation_readiness']is False and plan['action_authority']is False,'Preparation never grants authority')
 items=plan['items'];require(len(items)==34 and len({i['pr']for i in items})==34 and sum(len(i['associated_prs'])for i in items)==35,'Exact family inventory')
 closed=strict_json((Path(__file__).resolve().parent.parent/'CLOSED_PRIOR_INPUT.json').read_bytes());adopted=strict_json((Path(closed['root'])/'PROPOSAL.json').read_bytes());literal={i['pr']:i['row']for i in adopted['items']}
 require(set(literal)=={i['pr']for i in items}and all(typed_equal(i['row'],literal[i['pr']])for i in items),'Exact root-adopted34 literal vectors required')
 for i in items:
  require(type(i['pr'])is int and type(i['row'])is list and len(i['row'])==4 and all(type(c)is str for c in i['row'])and i['row'][1]=='','Exact4 strings/blankB')
  require(sha(canonical(i['row']))==i['row_sha256'],'Literal row byte binding')
  require(i['associated_prs']==([1270,1277]if i['pr']==1270 else[i['pr']]),'One joint1270/77 family')
  require(i['row'][2]==''if i['pr']in[1292,1310,1312]else i['row'][2].startswith('https://doi.org/10.'),'Intentional blankC/source role')
  if i['pr']!=1263:require(typed_equal(i['row'],i['original_root_adopted_row']),'Unreviewed literal revision')
 require(1277 not in[i['pr']for i in items]and 1224 not in[i['pr']for i in items],'Joint or separately excluded eleven scope drift')
 require(next(i for i in items if i['pr']==1330)['original_problem_ids']==['30003185'],'GL/GU original scope')
 return items

def known_reply(response,book):
 if response is None:return False,False
 try:j=json.loads(response['stdout'],object_pairs_hook=_unique_pairs)
 except (ValueError,TypeError):return False,False
 two={'spreadsheetId':book,'replies':[{}]};three={**two,'commentUpdateState':'NO_UPDATES_REQUESTED'}
 exact=typed_equal(j,two)or typed_equal(j,three)
 return response.get('returncode')==0 and exact,not exact

def _unique_pairs(pairs):
 out={}
 for key,value in pairs:
  if key in out:raise ValueError('Duplicate JSON reply key')
  out[key]=value
 return out

def exact_after(before,after,rows):
 require(typed_equal(before['metadata'],after['metadata']),'Full metadata changed')
 n=len(before['values']);count=len(rows)
 for key in ['values','formulas']:
  require(len(after[key])==n+count and typed_equal(after[key][:n],before[key])and typed_equal(after[key][n:],rows),'Exact full43 typed prefix plus one ordered batch')
 for raw,key in [('value_raw','values'),('formula_raw','formulas')]:
  expected=copy.deepcopy(before[raw]);expected['valueRanges'][0]['valueRange']['values']=before[key]+rows
  require(typed_equal(after[raw],expected),'Unknown full raw response/range key changed')

def own_positions(observed,rows):
 positions=[]
 for row in rows:
  hits=[n for n,v in enumerate(observed['values'],1)if typed_equal(row,v)]
  require(len(hits)<=1,'Duplicate existing literal row');positions.append(hits[0]if hits else None)
 if not any(positions):return []
 require(all(positions),'Partial existing batch: HOLD, never append remainder')
 require(positions==list(range(positions[0],positions[0]+len(rows))),'Existing exact batch order/contiguity changed')
 return positions

def local_check(provider,plan,plan_bytes,source_hash,approvals,keys,revision_hash,journal=None):
 require(callable(VERIFY_SOURCE_CLOSURE),'Caller-pinned bootstrap required');VERIFY_SOURCE_CLOSURE()
 require(typed_equal(plan,strict_json(plan_bytes)),'Captured complete plan changed')
 provider.check_integrity(plan_bytes,source_hash,journal);VERIFY_SOURCE_CLOSURE()

def fresh(provider,plan,plan_bytes,source_hash,approvals,keys,revision_hash,semantic_gate,source_gate,expected=None,journal=None):
 local_check(provider,plan,plan_bytes,source_hash,approvals,keys,revision_hash,journal)
 started=provider.now();account=provider.complete_owned_and_local();provider.preserve_observation('complete_owned_local',account)
 require(type(account)is dict and type(account.get('passes'))is list and len(account['passes'])==2,'Two complete account passes required')
 for collection in account['passes']:
  require(type(collection)is dict and type(collection.get('records'))is dict and bool(collection['records'])and type(collection.get('terminal_empty_page'))is int and collection['terminal_empty_page']>=1,'Complete owned terminal/records')
  for identifier,record in collection['records'].items():
   require(type(record)is dict and type(record.get('id'))is int and record['id']>0 and identifier==str(record['id'])and type(record.get('metadata'))is dict and type(record.get('files'))is list,'Strict full native owned shape/ID')
  pages=collection.get('raw_pages');statuses=collection.get('http_statuses')
  require(type(pages)is list and 1<=len(pages)<=10000 and collection['terminal_empty_page']==len(pages),'Complete raw pages through empty terminal required')
  require(type(statuses)is list and len(statuses)==len(pages)and all(type(x)is int and x==200 for x in statuses),'Every raw owned page exact HTTP200')
  aggregate={}
  for index,raw in enumerate(pages):
   require(type(raw)is str,'Raw owned page text required');values=strict_json(raw)
   require(type(values)is list and len(values)<=25 and (bool(values)if index<len(pages)-1 else values==[]),'Nonempty pages followed by exactly empty terminal')
   for record in values:
    require(type(record)is dict and type(record.get('id'))is int and record['id']>0 and type(record.get('metadata'))is dict and type(record.get('files'))is list,'Raw native record full typed shape')
    identifier=str(record['id']);require(identifier not in aggregate,'Repeated owned record across pages');aggregate[identifier]=record
  require(typed_equal(aggregate,collection['records']),'Full raw pages do not reconstruct complete record map')
 require(typed_equal(account['passes'][0]['records'],account['passes'][1]['records']),'Full typed owned passes drift')
 require(type(account.get('local'))is list,'Complete local scientific carrier list required')
 account_at=provider.now();observed=numeric.observe(provider,expected);provider.preserve_observation('numeric_full_raw',observed);native=provider.complete_publication_source_observations();provider.preserve_observation('complete_publication_source',native);native_at=provider.public_started
 require(type(native)is dict and native.get('all_required_roles_observed')is True,'Missing DOI/source/native/PR role observations')
 source_gate(native) # Exact version/DOI/authorship/PR/source-body contracts, no429-as-absence or metadata-as-payload claim.
 semantic_gate(observed,account,native)
 local_check(provider,plan,plan_bytes,source_hash,approvals,keys,revision_hash,journal)
 age={'started':started,'account_at':account_at,'native_at':native_at}
 edge(provider,age,plan,plan_bytes,source_hash,approvals,keys,revision_hash,journal)
 return observed,age

def edge(provider,age,plan,plan_bytes,source_hash,approvals,keys,revision_hash,journal=None):
 local_check(provider,plan,plan_bytes,source_hash,approvals,keys,revision_hash,journal)
 now=provider.now();require(0<=now-age['started']<=COMPLETE_MAX_AGE and 0<=now-age['account_at']<=COMPLETE_MAX_AGE,'Complete guard expired at actual edge')
 require(0<=now-age['native_at']<=NATIVE_MAX_AGE,'Native/source guard expired at actual edge')
 if'intent_at'in age:require(0<=now-age['intent_at']<=INTENT_MAX_AGE,'Durable intent expired')

def run_reviewed_protocol(provider,plan,source_hash,approvals,keys,revision_hash,journal_path,semantic_gate,source_gate):
 """Real authority checked at every local gate; one fixed durable action journal."""
 require(Path(journal_path)==provider.bound_case_path,'Alternate CASE path forbidden')
 items=validate(plan);raw=provider.plan_bytes;rows=[i['row']for i in items]
 local_check(provider,plan,raw,source_hash,approvals,keys,revision_hash)
 require(not Path(journal_path).exists(),'Existing SAMECASE: GET-only reconciliation, never retry or alternate case')
 attempted=False;fact=None;journal=None;before=None
 try:
  before,age=fresh(provider,plan,raw,source_hash,approvals,keys,revision_hash,semantic_gate,source_gate)
  own=own_positions(before,rows)
  if own:return {'status':'EXACT_EXISTING_BATCH_NOOP','positions':own,'writes':0,'action_authority':False}
  require(numeric.target(before['metadata'])['gridProperties']['rowCount']>=len(before['values'])+len(rows),'Allocated grid capacity insufficient')
  request={'requests':[{'appendCells':{'sheetId':plan['sheet_gid'],'rows':[{'values':[{'userEnteredValue':{'stringValue':c}}for c in r]}for r in rows],'fields':'userEnteredValue'}}]}
  journal=provider.new_journal(journal_path,Journal);provider.journal=journal
  journal.save('HEADER.json',{'plan_sha256':sha(raw),'source_sha256':source_hash,'previous_rows':len(before['values']),'write_attempt_limit':1,'schema':'remaining34-real-bridge-v2','gate_sha256':provider.gate_sha256,'authority_raw_sha256':provider.authority.pins})
  journal.save('BEFORE.json',before);intent_at=provider.now();journal.save('INTENT.json',{'request':request,'at':provider.stamp(),'attempt_limit':1})
  local_check(provider,plan,raw,source_hash,approvals,keys,revision_hash,journal)
  journal.save('WRITE_ATTEMPTED.json',{'attempt':1,'request_sha256':sha(canonical(request))})
  # Actual marker fsync precedes the long fresh observation and BOTH direct edge checks.
  local_check(provider,plan,raw,source_hash,approvals,keys,revision_hash,journal)
  last,age=fresh(provider,plan,raw,source_hash,approvals,keys,revision_hash,semantic_gate,source_gate,before,journal);age['intent_at']=intent_at
  edge(provider,age,plan,raw,source_hash,approvals,keys,revision_hash,journal)
  edge(provider,age,plan,raw,source_hash,approvals,keys,revision_hash,journal)
  provider.direct_guard=lambda:edge(provider,age,plan,raw,source_hash,approvals,keys,revision_hash,journal)
  attempted=True;response=None;error=None
  try:response=provider.append_once(request)
  except Exception as e:error=repr(e)
  journal.save('TRANSPORT.json',{'response':response,'error':error})
  known,contradictory=known_reply(response,plan['spreadsheet_id']);after=numeric.observe(provider);journal.save('AFTER.json',after)
  exact_after(before,after,rows);fact={'exact_prefix_plus_batch_observed':True,'known_response':known,'contradictory_response':contradictory,'attempts':1};journal.save('SERVICE_OUTCOME.json',fact)
  require(not contradictory,'Contradictory parsed reply: preserve service fact, certification HOLD')
  post,age=fresh(provider,plan,raw,source_hash,approvals,keys,revision_hash,semantic_gate,source_gate,after,journal);age['intent_at']=intent_at
  edge(provider,age,plan,raw,source_hash,approvals,keys,revision_hash,journal)
  receipt={'status':'VERIFIED_EXACT_ONE_ATOMIC_EXISTING_PUBLICATION_BATCH','new_rows':len(rows),'new_publications':0,'attempts':1,'old43_rows_preserved':len(before['values']),'after_rows':len(post['values']),'unknown_reply_get_reconciled':not known,'action_authority':False}
  journal.save('VERIFIED.json',{'status':'CANDIDATE_REQUIRES_FINAL_POST_FSYNC_CHECK','candidate':receipt})
  edge(provider,age,plan,raw,source_hash,approvals,keys,revision_hash,journal)
  return receipt
 except BaseException as e:
  failure={'status':'UNKNOWN'if attempted else'HOLD','attempted':attempted,'error':repr(e),'service_fact':fact,'certification_complete':False,'no_retry_or_alternate_case':True}
  if journal is not None:
   try:journal.save('FAILURE.json',failure)
   except BaseException as pe:failure['failure_preservation_error']=repr(pe)
  provider.preserve_failure(failure)
  raise


def reconcile_get_only(provider,plan,journal_path):
 require(Path(journal_path)==provider.bound_case_path,'GET-only original SAMECASE required')
 root=Path(journal_path);require(root.is_dir(),'Original durable CASE absent')
 before=json.loads((root/'BEFORE.json').read_bytes());observed=numeric.observe(provider)
 result={'status':'GET_ONLY_ORIGINAL_OUTCOME_RECONCILIATION','writes':0,'approval_inferred':False,'can_retry':False,'exact_own_positions':own_positions(observed,[i['row']for i in plan['items']])}
 if result['exact_own_positions']:exact_after(before,observed,[i['row']for i in plan['items']]);result['service_fact']='EXACT_PREFIX_PLUS_ORIGINAL_BATCH'
 else:result['service_fact']='NO_EXACT_COMPLETE_BATCH_OBSERVED'
 return result
