from pathlib import Path
import ast,copy,types,json,hashlib,datetime as dt,subprocess,argparse,re,uuid,io,contextlib,sys
home=Path(__file__).resolve().parent; bound=home/'bound_ops';work=home/'ops_fixtures_v4';work.mkdir(exist_ok=False)
def load_defs(name,names,env):
 p=bound/name;t=ast.parse(p.read_text());items=[n for n in t.body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name in names];exec(compile(ast.Module(body=items,type_ignores=[]),str(p),'exec'),env);return env
sha=lambda b:hashlib.sha256(b).hexdigest()
def atomic_json(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+'\n')
def zenodo_dois(v):return set(re.findall(r'10\.5281/zenodo\.\d+',str(v)))
baseenv={'Path':Path,'json':json,'hashlib':hashlib,'dt':dt,'subprocess':subprocess,'atomic_json':atomic_json,'zenodo_dois':zenodo_dois,'sys':sys}
e=load_defs('publication_live_gates.py',{'digest','identity_projection','require_release_clearance','collect'},dict(baseenv))
rows=[]
def expect(label,fn,ok=False):
 try:v=fn()
 except Exception as ex:
  rows.append({'case':label,'expected':'accept' if ok else 'reject','actual':'reject','exception':type(ex).__name__,'reason':str(ex)});assert not ok,(label,str(ex));return
 rows.append({'case':label,'expected':'accept' if ok else 'reject','actual':'accept'});assert ok,label
# Clearance must bind exact five artifact bytes and current release entries.
a=work/'clearance';pub=a/'preprint/publication';pub.mkdir(parents=True)
files=[]
for p in (home/'bound_release').iterdir():
 data=p.read_bytes();(pub/p.name).write_bytes(data);files.append({'path':p.name,'bytes':len(data),'sha256':sha(data)})
release={'files':files};clearance={'publication_ready':True,'unresolved_material_findings':[],'sequential_new_reviewers':['reviewer2','reviewer3'],'files':files}
e['AUDIT']=a
atomic_json(pub/'RELEASE_FILES.json',release)
def ccheck(change):
 d=copy.deepcopy(clearance);change(d);atomic_json(a/'ROOT_PUBLICATION_CLEARANCE.json',d);return e['require_release_clearance']()
expect('trusted_exact_root_clearance',lambda:ccheck(lambda d:None),True)
expect('clearance_false',lambda:ccheck(lambda d:d.update(publication_ready=False)))
expect('unresolved_finding',lambda:ccheck(lambda d:d.update(unresolved_material_findings=['x'])))
expect('only_one_new_reviewer',lambda:ccheck(lambda d:d.update(sequential_new_reviewers=['r'])))
expect('missing_new_reviewers',lambda:ccheck(lambda d:d.pop('sequential_new_reviewers')))
expect('mismatching_released_hash',lambda:ccheck(lambda d:d['files'][0].update(sha256='0'*64)))
(p0:=pub/files[0]['path']).write_bytes(b'changed')
expect('cleared_artifact_bytes_changed',lambda:ccheck(lambda d:None));p0.write_bytes((home/'bound_release'/p0.name).read_bytes())
# Full account pagination is exercised through production account_search AST.
from urllib.parse import urlencode
pe=load_defs('prepublication_check.py',{'account_search'},{'urlencode':urlencode})
class Client:
 base='https://synthetic.invalid'
 def __init__(self,pages):self.pages=iter(pages)
 def request(self,method,url):assert method=='GET';return next(self.pages)
def page(total,hits,next=None):return {'hits':{'total':total,'hits':[{'id':x} for x in hits]},'links':({'next':next} if next else {})}
expect('pagination_two_complete_pages',lambda:pe['account_search'](Client([page(2,[1],'next'),page(2,[2])]),''),True)
for label,pages in [
 ('inexact_total',[page({'value':1,'relation':'gte'},[1])]),('missing_records',[page(2,[1])]),('changing_total',[page(2,[1],'next'),page(3,[2])]),('duplicate_record',[page(2,[1],'next'),page(2,[1])]),('pagination_loop',[page(2,[1],'next'),page(2,[2],'next')]),('boolean_total',[page(True,[1])]),('negative_total',[page(-1,[])]),('missing_id',[{'hits':{'total':1,'hits':[{}]},'links':{}}])]:expect(label,lambda pages=pages:pe['account_search'](Client(pages),''))
# Production collect with synthetic read-only provider output: no real credentials/services.
a=work/'gate';a.mkdir();root=a;raw=root/'raw';raw.mkdir();e['AUDIT']=a;e['ROOT']=root
record={'id':101,'metadata':{'title':'Synthetic unrelated model','description':'different mathematical object'},'files':[{'key':'other.pdf','checksum':'md5:abc','size':1}]};record2={'id':102,'metadata':{'title':'Synthetic other result'},'files':[]}
priorrow=['unrelated','', 'https://doi.org/10.5281/zenodo.101','synthetic']
recon={'all_broad_Aldous_leads_cleared_as_distinct':[{'record':v['id'],'metadata_sha256':e['digest'](v['metadata']),'metadata_and_files_sha256':e['digest'](e['identity_projection'](v))} for v in [record,record2]],'ledger_leads':[{'values_sha256':sha(json.dumps(priorrow,ensure_ascii=False).encode())}]}
atomic_json(a/'ROOT_PREPUBLICATION_LEAD_RECONCILIATION.json',recon)
gatebase={'raw_receipts':'raw','receipt':str(a/'gate.json'),'unexpected_account_matches':[{'id':101},{'id':102}],'ledger_matches':[{'row':2,'values':priorrow}],'local_deposit_state_matches':[],'operation':'fixture'}
e['subprocess']=types.SimpleNamespace(run=lambda *args,**kw:types.SimpleNamespace(stdout=json.dumps(e['_gate'])))
def gcheck(label,mutate,ok=False,expected=None,allow=False):
 recs=copy.deepcopy([record,record2]);gate=copy.deepcopy(gatebase);mutate(recs,gate);atomic_json(raw/'account_complete.json',{'records':recs});atomic_json(a/'gate.json',gate);e['_gate']=gate;expect(label,lambda:e['collect']('before_publish','a'*40,expected,allow),ok)
gcheck('unchanged_known_metadata_complete_files',lambda r,g:None,True)
gcheck('new_account_lead',lambda r,g:g['unexpected_account_matches'].append({'id':103}))
gcheck('known_file_key_change',lambda r,g:r[0]['files'][0].update(key='congestion.pdf'))
gcheck('known_file_checksum_change',lambda r,g:r[0]['files'][0].update(checksum='md5:changed'))
gcheck('known_file_size_change',lambda r,g:r[0]['files'][0].update(size=2))
gcheck('known_complete_file_list_addition',lambda r,g:r[0]['files'].append({'key':'congestion.pdf'}))
gcheck('known_complete_file_list_removal',lambda r,g:r[0].update(files=[]))
gcheck('known_metadata_change',lambda r,g:r[0]['metadata'].update(description='different'))
gcheck('known_files_schema_change',lambda r,g:r[0].update(files={}))
gcheck('known_metadata_schema_change',lambda r,g:r[0].update(metadata=[]))
gcheck('known_record_missing',lambda r,g:r.pop(0))
gcheck('new_ledger_lead',lambda r,g:g['ledger_matches'].append({'row':3,'values':['9700002','', '', 'new']}))
gcheck('changed_cleared_ledger_lead',lambda r,g:g['ledger_matches'][0]['values'].append('changed'))
gcheck('local_unexpected_target_state',lambda r,g:g['local_deposit_state_matches'].append({'deposit_id':998}))
gcheck('local_other_expected_state',lambda r,g:g['local_deposit_state_matches'].append({'deposit_id':998}),expected=999)
gcheck('exact_expected_local_state',lambda r,g:g['local_deposit_state_matches'].append({'deposit_id':999}),True,expected=999)
gcheck('new_target_ledger_row_without_allowance',lambda r,g:g['ledger_matches'].append({'row':3,'values':['9700002','','https://doi.org/10.5281/zenodo.999','']}),expected=999)
gcheck('target_row_allowed_for_idempotent_ledger_check',lambda r,g:g['ledger_matches'].append({'row':3,'values':['9700002','','https://doi.org/10.5281/zenodo.999','']}),True,expected=999,allow=True)
# The actual ledger main is isolated with synthetic receipts/read/append functions.
le=load_defs('record_publication_ledger.py',{'desired_row','matches','main'},{**baseenv,'argparse':argparse,'uuid':uuid,'re':re,'SHEET':'synthetic','RANGE':'synthetic'})
a=work/'ledger';a.mkdir();le['AUDIT']=a;le['ROOT']=a;le['require_release_clearance']=lambda:True;le['collect']=lambda *args,**kwargs:({'receipt':str(a/'gate.json')},{});le['_append_calls']=0
identifier=999; desired=le['desired_row'](identifier)
publicbase={'record':identifier,'all_public_file_bytes_match_reviewed':True,'doi_resolution':{'status':200}}
def setup_ledger(before,after,intent=False,publicchange=None):
 for n in ['LEDGER_APPEND_INTENT.json','LEDGER_APPEND_RESPONSE.json','LEDGER_PUBLICATION_VERIFICATION.json']:
  if (a/n).exists():(a/n).unlink()
 if intent:atomic_json(a/'LEDGER_APPEND_INTENT.json',{'earlier_intent':True})
 atomic_json(a/'ZENODO_PUBLISH.json',{'id':999,'state':'published','doi':'10.5281/zenodo.999'})
 atomic_json(a/'ZENODO_PUBLISHED_INSPECTION.json',{'id':999,'state':'published','doi_url':'https://doi.org/10.5281/zenodo.999','doi_resolution':{'http_status':200}})
 pub=copy.deepcopy(publicbase)
 if publicchange:publicchange(pub)
 atomic_json(a/'ZENODO_PUBLIC_FILE_VERIFICATION.json',pub)
 reads=iter([before,after]);le['read']=lambda *args:next(reads);le['_append_calls']=0
 def fake_gws(action,*args,**kwargs):
  assert action=='append';le['_append_calls']+=1;return {'updates':{'updatedRows':1,'updatedColumns':4,'updatedData':{'values':[desired]}}}
 le['gws']=fake_gws
 def invoke():
  import sys
  old=sys.argv;sys.argv=['record_publication_ledger.py','--expected-pr-head','a'*40,'--deposit-id','999']
  try:
   with contextlib.redirect_stdout(io.StringIO()):le['main']()
  finally:sys.argv=old
 return invoke
header=['Original Problem','Solution Chat URL','DOI','Notes']
expect('ledger_existing_exact_is_idempotent',setup_ledger([header,desired],[header,desired]),True);assert le['_append_calls']==0
expect('ledger_existing_exact_after_uncertain_intent',setup_ledger([header,desired],[header,desired],True),True);assert le['_append_calls']==0
expect('ledger_prior_uncertain_intent_no_visible_row',setup_ledger([header],[header],True));assert le['_append_calls']==0
alter=desired[:];alter[3]+='changed'
expect('ledger_same_DOI_changed_row_no_append',setup_ledger([header,alter],[header,alter]));assert le['_append_calls']==0
expect('ledger_duplicate_target_no_append',setup_ledger([header,desired,desired],[header,desired,desired]));assert le['_append_calls']==0
expect('ledger_public_files_unverified_no_append',setup_ledger([header],[header],publicchange=lambda p:p.update(all_public_file_bytes_match_reviewed=False)));assert le['_append_calls']==0
expect('ledger_new_single_synthetic_append',setup_ledger([header],[header,desired]),True);assert le['_append_calls']==1
expect('ledger_bad_readback_stops_without_retry',setup_ledger([header],[header]));assert le['_append_calls']==1
out={'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'all_assertions_passed':True,'controls':len(rows),'accepted':sum(r['actual']=='accept' for r in rows),'rejected':sum(r['actual']=='reject' for r in rows),'cases':rows,'scope':'Production AST function bodies with purely synthetic read-only/provider stubs and assigned-directory files. No live main, GitHub, Zenodo, GWS, index or ref mutation. Root clearance is a trusted authored assertion, not cryptographic independent-review authentication.'}
(home/'OPERATIONAL_CONTROLS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='cases'}))
