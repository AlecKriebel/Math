"""Independent actual PR1131 public+row read-only reconciliation; preserves failed ledger actor."""
from pathlib import Path
import json,hashlib,base64,datetime,io,zipfile,copy
R=Path('/Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7');A=R/'audits';P=A/'pr1131_30005455';W=A/'final_reconciliation_new_independent_adversary01'
def load(p,h):
 b=p.read_bytes();assert hashlib.sha256(b).hexdigest()==h
 n={'__file__':str(p),'__name__':'_independent_actual1131_'+p.stem};exec(compile(b,str(p),'exec',optimize=0),n);return n
I=load(W/'independent_checks.py','63f9f0d1cd4d8e8d87b3c087ce8db2535ef526db3f359e2df7f4c13ce550aa8a')
H=I['H'];C=I['C'];typed=I['typed'];strict=I['strict'];PINS={}
def read(p,h=None):
 b=p.read_bytes();assert h is None or H(b)==h;pin={'path':str(p),'bytes':len(b),'sha256':H(b)};PINS[str(p)]=pin;return I['objpin'](pin)
def raw(p,h=None):
 b=p.read_bytes();assert h is None or H(b)==h;PINS[str(p)]={'path':str(p),'bytes':len(b),'sha256':H(b)};return b
def utc(x):
 t=datetime.datetime.fromisoformat(x.replace('Z','+00:00'));assert t.tzinfo is not None and t.utcoffset()==datetime.timedelta(0);return t
def sheet(s):
 return {'metadata':s['metadata_before'],'value_raw':s['numeric_response'],'formula_raw':s['numeric_formula_response'],'values':s['values'],'formulas':s['numeric_formula_response']['valueRanges'][0]['valueRange']['values']}
def source19_validation_view(s):
 # Pinned Source19 uses row-unbounded full columns, unlike strict final indexed inputs.
 # Replace only this explicitly checked representation in a derived validation copy.
 original=[{'gridRange':{'sheetId':1254632077,'startColumnIndex':0,'endColumnIndex':43}}]
 d=copy.deepcopy(s)
 targets=[x for x in s['metadata']['sheets']if type(x['properties']['sheetId'])is int and x['properties']['sheetId']==1254632077]
 assert len(targets)==1;rows=targets[0]['properties']['gridProperties']['rowCount']
 assert type(rows)is int and rows>0
 indexed=[{'gridRange':{'sheetId':1254632077,'startRowIndex':0,'endRowIndex':rows,'startColumnIndex':0,'endColumnIndex':43}}]
 for name in['value_raw','formula_raw']:
  assert type(d[name]['valueRanges'])is list and len(d[name]['valueRanges'])==1
  assert typed(d[name]['valueRanges'][0]['dataFilters'],original)
  d[name]['valueRanges'][0]['dataFilters']=indexed
 return d
def source19_sheet(s):
 d=I['strict_sheet'](source19_validation_view(s))
 d['source19_filter']=[{'gridRange':{'sheetId':1254632077,'startColumnIndex':0,'endColumnIndex':43}}]
 return d
def http(folder,name,h,url):
 e=read(folder/name,h);assert e['method']=='GET'and e['url']==url and type(e['status'])is int and e['status']==200 and e['transport_error']is None and e['service_mutations']==0 and e['original_wire_saved_before_parse']is True
 b=base64.b64decode(e['raw_body_base64'],validate=True);assert len(b)==e['raw_body_bytes']and H(b)==e['raw_body_sha256']
 assert utc(e['before'])<=utc(e['after'])<=datetime.datetime.now(datetime.timezone.utc)
 return e,b
def main():
 RT=P/'operations19/runtime';D=P/'root_actual21_known23592692_actions01';ACT=P/'root_actual21_known23592692_activation01';E=P/'known23592692_operations21_preparation01'
 ID=23592692;doi='10.5281/zenodo.23592692';HEAD='9601e1e768c94522bc8ad105db4dfae4770bad75'
 contract=read(P/'known23592692_operations21_authority01/ROOT_EXECUTION_ADOPTION21.json','bb7a8af3131f7244a9b5c7b68b1e0b870ccb10336e95642d12959e9f048bdd09')
 assert contract['id']==ID and contract['known_create_only']is True and contract['future_create_allowance_zero']is True
 source=read(E/'source21/SOURCE_MANIFEST21.json','c64fae35c2ea0ebd7213e0791559f3cb5eba9f87a5b6fa8a0fc2038af2da9670')
 for name,spec in source.items():b=raw(E/'source21'/name,spec['sha256']);assert len(b)==spec['bytes']
 entry=raw(E/'entry21.py','694fb1692a0d30c5f4d7ea3e782887a88070ec3a980869717a8f5f025d8663ea')
 raw(E/'native_step21.py','ca513166da9a72098891b90d44175d2a547c1a530e68595222e5ba8f426b9f7f')
 data=read(E/'source21/DATA_CONTRACT21.json',source['DATA_CONTRACT21.json']['sha256'])
 for name,pin in data['historical_runtime'].items():b=raw(RT/name,pin['sha256']);assert len(b)==pin['bytes']
 fp=data['first_response'];first=raw(Path(fp['path']),fp['sha256']);assert len(first)==fp['bytes']and fp['sha256']=='509e46d778614c1cf7ec0709cd75b571333ee5814927b53a123f2eaa596eddff'
 cp=P/'operations19/source/custody18.py'
 cb=raw(cp,'a0890e56df45eb963a29b031d1f360a5cf16df86b1cd0f3a4a33fc245c12069c');cn={'__file__':str(cp),'__name__':'_actual1131_custody','_OPS18_VERIFIED':True};exec(compile(cb,str(cp),'exec',optimize=0),cn);create=cn['loads'](first)
 assert create['kind']=='create'and create['requested_or_known_id']==ID and create['response']['id']==ID and create['response']['conceptrecid']=='23592691'and create['response']['owner']==1789874 and create['response']['submitted']is False
 phases=[];previous=None
 for action in['stage-known','publish','verify-public','ledger']:
  outer=read(ACT/('ROOT_'+action+'_ORIGINAL_PARENT_NATIVE.json'));ex=read(D/(action+'.exit.json'));intent=read(D/(action+'.intent.json'))
  ob=raw(D/(action+'.stdout.bin'));eb=raw(D/(action+'.stderr.bin'))
  assert ex['stdout']=={'bytes':len(ob),'sha256':H(ob)}and ex['stderr']=={'bytes':len(eb),'sha256':H(eb)}
  assert ex['complete_native_return']is True and ex['error']is None and outer['complete_native_return']is True and outer['error']is None
  assert outer['ROOT_contract_sha256']==intent['ROOT_execution_sha256']==H(raw(P/'known23592692_operations21_authority01/ROOT_EXECUTION_ADOPTION21.json'))
  assert outer['helper_sha256']==contract['native_controller21_sha256']=='ca513166da9a72098891b90d44175d2a547c1a530e68595222e5ba8f426b9f7f'
  av=[action,'--expected-pr-head',HEAD,'--deposit-id',str(ID),'--clearance-sha256',contract['ROOT19_sha256'],'--root21-clearance-sha256',contract['ROOT21_sha256'],'--compat20-clearance-sha256',contract['compatibility20_authority_sha256']]
  inner='from pathlib import Path;import hashlib;p=Path('+repr(str(E/'entry21.py'))+');b=p.read_bytes();\nif hashlib.sha256(b).hexdigest()!='+repr(contract['entry21_sha256'])+':raise RuntimeError("entry21 changed")\nn={"__file__":str(p),"__name__":"checked_actual_known21"};exec(compile(b,str(p),"exec",dont_inherit=True,optimize=0),n);n["main"]('+repr(av)+')'
  outprog="from pathlib import Path;import hashlib;p=Path("+repr(str(E/'native_step21.py'))+");b=p.read_bytes();assert hashlib.sha256(b).hexdigest()=="+repr(contract['native_controller21_sha256'])+";n={'__file__':str(p),'__name__':'ROOT_checked_actual_known21_helper'};exec(compile(b,str(p),'exec',dont_inherit=True,optimize=0),n);n['main'](['--action',"+repr(action)+",'--root-contract-sha256',"+repr('bb7a8af3131f7244a9b5c7b68b1e0b870ccb10336e95642d12959e9f048bdd09')+"])"
  assert ex['native_command']==intent['native_command']==['/opt/homebrew/bin/python3','-I','-S','-B','-c',inner]and intent['argv']==av
  assert outer['argv']==['/opt/homebrew/bin/python3','-I','-S','-B','-c',outprog]
  for role in['stdout','stderr']:
   x=outer['physical_streams'][role];b=raw(Path(x['path']),x['sha256_at_snapshot']);assert len(b)==x['bytes_at_snapshot']and b==base64.b64decode(outer[role+'_base64'],validate=True)
  start=utc(outer['before']);end=utc(outer['after']);assert start<=utc(ex['started_at'])<=utc(ex['finished_at'])<=end and(previous is None or previous<=start);previous=end
  if action!='ledger':
   assert type(ex['returncode'])is int and ex['returncode']==outer['returncode']==0 and eb==b''and outer['successful_native_return']is True
   result=strict(ob);assert typed(result,read(D/(action+'.parsed.json')));assert result.get('id',result.get('record'))==ID
  else:
   assert ex['returncode']==outer['returncode']==1 and ob==b''and outer['successful_native_return']is False and outer['stream_snapshot_may_be_incomplete_and_descendant_may_continue']is True
   assert H(eb)=='62fc7edfd53e20b89eb2befe3b6e33f8d9519d4b0271d1a3ed58d880321314fd'and b'Expired/future observation'in eb and b"final_facts(args,'ledger'"in eb
   assert not (D/'ledger.parsed.json').exists()and not (RT/'LEDGER_VERIFIED.json').exists()
  phases.append({'action':action,'child_returncode':ex['returncode'],'outer_returncode':outer['returncode'],'before':outer['before'],'after':outer['after']})
 intent=read(RT/'LEDGER_APPEND_INTENT.json','fa72b5f4b46faaf7ce707046ec184d9626247c1d9952d6afba42e3c5b159f1d2')
 response=read(RT/'LEDGER_APPEND_RESPONSE.json','36de7b610cf3ff13493cb6311dea41cf83a9ca71502e176db6bb08a14e6ee28a')
 ack=read(RT/'LEDGER_APPEND_ACKNOWLEDGED.json','f8c9dad35e72dfa3b302619a0570a74feb666cd26e24c45bc6dd34c0b982b76a')
 assert intent['record']==ack['record']==ID and intent['before_rows']==286 and ack['request_sha256']==H(C(intent['request']))and ack['response_sha256']==H(C(response))
 assert response['spreadsheetId']==I['BOOK']and response['replies']==[{}]
 row=intent['values'];request={'requests':[{'appendCells':{'sheetId':1254632077,'rows':[{'values':[{'userEnteredValue':{'stringValue':c}}for c in row]}],'fields':'userEnteredValue'}}],'includeSpreadsheetInResponse':True,'responseIncludeGridData':False}
 assert typed(request,intent['request'])and intent['head']==HEAD and intent['sheet_id']==1254632077 and intent['sheet_title']=='Math Puzzles'
 before=sheet(intent['before_snapshot']);source19_sheet(before);assert len(before['values'])==286 and H(C(before['values']))==intent['before_sha256']
 prior=read(R/'EXISTING_PUBLICATION_REMAINING34_RECONCILIATION.json','3679737af83a029468e82aa4ef91d2ab030b22db88c47d69049d5f5872f0035a');prior286=I['objpin'](prior['after_snapshot']);assert typed(source19_validation_view(before),prior286)
 sd=P/'ROOT_ACTUAL287_SOURCE19_GET_ONLY_POSTAPPEND01';snap=read(sd/'ACTUAL_FULL287_SOURCE19_SNAPSHOT.json','35f2ffa2c3a156d9b2ab9b27c62c29e12af3768162cad8db7c87e7586ed7b065')
 after=sheet(snap);details=source19_sheet(after);assert len(after['values'])==287 and typed(after['values'],before['values']+[row])and typed(after['formulas'],before['formulas']+[row])
 assert typed(after['metadata'],before['metadata'])and typed(snap['metadata_after'],after['metadata'])
 roles=['metadata_before','values','formulas','metadata_after'];derived={};last=utc(phases[-1]['after']);events=[]
 for i,role in enumerate(roles):
  e=read(sd/('ORIGINAL_NATIVE_'+str(i).zfill(2)+'.json'));derived[role]=I['raw_cli'](e,role,{**details,'full_filter':details['source19_filter']})
  assert e['binary_sha256']==I['GWS_SHA']if 'GWS_SHA'in I else e['binary_sha256']=='0f27b8b0815bf09cdf95da48d3c604f05ceb8f16bf5c9f0ba355b1f957cdd47e'
  assert e['transport_error']is None and last<=utc(e['before'])<=utc(e['after']);last=utc(e['after']);events.append({'role':role,'before':e['before'],'after':e['after']})
 assert typed(derived['metadata_before'],derived['metadata_after'])and typed(derived['metadata_before'],after['metadata'])and typed(derived['values'],after['value_raw'])and typed(derived['formulas'],after['formula_raw'])
 assert last<=utc(snap['observed_at'])
 doirows=[i for i,x in enumerate(after['values'],1)if len(x)>2 and x[2].lower().replace('https://doi.org/','')==doi];assert doirows==[287]
 familyrows=[i for i,x in enumerate(after['values'],1)if any('10.5281/zenodo.23592692'in str(y).lower()or'10.5281/zenodo.23592691'in str(y).lower()for y in x)];assert familyrows==[287]
 nonempty=[str(x[2]).lower().replace('https://doi.org/','').strip()for x in after['values'][1:]if len(x)>2 and x[2]];assert len(nonempty)==len(set(nonempty))==272
 folder=P/'known23592692_readonly_reconciliation06_postappend_public'
 le,lb=http(folder,'legacy_ORIGINAL_HTTP.json','87a0ceab105006a14c16adca9dae8b548755a0a7751b7a25e35ac85774290a72','https://zenodo.org/api/deposit/depositions/'+str(ID))
 ne,nb=http(folder,'native_record_ORIGINAL_HTTP.json','2c6917b36d4919ef54b3bc7a30623ade65cb5fa32ab675902d5b3927bb67562a','https://zenodo.org/api/records/'+str(ID))
 fe,fb=http(folder,'native_files_ORIGINAL_HTTP.json','3c8061c37e55fa003ae311bd7687ace786e429d9f4f36303ddd535e00dd8d083','https://zenodo.org/api/records/'+str(ID)+'/files')
 legacy=strict(lb);native=strict(nb);files=strict(fb)
 assert legacy['id']==ID and legacy['conceptrecid']=='23592691'and legacy['owner']==1789874 and legacy['submitted']is True and legacy['state']=='done'and legacy['doi']==doi
 assert native['id']==str(ID)and native['is_draft']is False and native['is_published']is True and native['status']=='published'
 assert native['parent']['id']=='23592691'and native['parent']['access']['owned_by']['user']=='1789874'and native['pids']['doi']['identifier']==doi
 manifest=read(P/'operations/proposed/preprint/zenodo-deposit.json','0ca12e07eee0ed88da4f94b82a2404eed4341aaa1f08f9100ecb630014fed6fe')
 assert all(k in legacy['metadata']and typed(legacy['metadata'][k],v)for k,v in manifest['metadata'].items())
 expected=[('finite-warm-thresholds.pdf',91613,'42c5c632de7e942df6b7c407fb95d877a165281f215e4aa7d1dfa862b08b2157','845715d7fffb5aba43baddb039692933','fbfaf3bff6b15ace8bb1750e5bdadf97243e712feb19e2649a2869b17bdd59a2'),('finite-warm-thresholds-source-and-verification.zip',211840,'e92f6fa13245686525a0dd8fc4c5327bd03e58a1f02ae7dcae918668c16c5fee','513e0c50bc16dfe669473fb83695dbca','f599de207557b26e32ab5f73e9721b1682e48c6cdd45670326d88da1cf47600d')]
 entries={x['key']:x for x in files['entries']};assert len(entries)==2 and set(entries)=={x[0]for x in expected}
 for name,size,sha,md5,eh in expected:
  ee,b=http(folder,name+'_PUBLIC_ORIGINAL_HTTP.json',eh,'https://zenodo.org/records/'+str(ID)+'/files/'+name+'?download=1')
  assert len(b)==size and H(b)==sha and hashlib.md5(b).hexdigest()==md5 and b==raw(P/'operations/proposed/preprint'/name,sha)
  f=entries[name];assert f['size']==size and f['checksum']=='md5:'+md5 and f['status']=='completed'and f['access']['hidden']is False
  if name.endswith('.zip'):
   with zipfile.ZipFile(io.BytesIO(b))as z:assert len(z.namelist())==45 and z.testzip()is None
 de,db=http(folder,'DOI_PUBLIC_ORIGINAL_HTTP.json','81a715dfe1a0dbdb9d4b09b6fa6e705ae44819451c618ac823aafdf826381e90','https://doi.org/'+doi)
 assert de['destination']=='https://zenodo.org/records/'+str(ID)and last<=utc(le['before'])<=utc(de['after'])
 return {'status':'PASS_INDEPENDENT_EXTERNAL_GET_ONLY_PR1131_PUBLICATION_AND_ROW_WITH_FAILED_LEDGER_ACTOR_PRESERVED','record':ID,'doi':doi,'sheet_row':287,'sheet_rows':287,'published_record_and_metadata_exact':True,'both_complete_public_payloads_equal_local':True,'downloaded_source_ZIP_45_CRCs':True,'full286_typed_prefix_preserved':True,'all272_nonempty_data_C_values_unique':True,'actual_append_acknowledged':True,'successful_actor_actions':3,'failed_actor_action':'ledger','base_LEDGER_VERIFIED_exists':False,'actor_ledger_parsed_exists':False,'ledger_actor_returncode':1,'append_retried':False,'phase_originals':phases,'full287_original_native_observations':events,'source19_original_filter':details['source19_filter'],'representation_qualification':'Source19 original row-unbounded full43-column requests and full A1:AQ1178 replies checked explicitly; derived validation copy changes only that checked filter representation. Strict final indexed original ingress remains separately required.','preserved_first_strict_schema_refusal_sha256':'c131888514b4d3d3a9e6226cb3ab6dc23df0b5d0beebec2800eb4dc4c6857c16','latest_public_original_after':de['after'],'external_inputs':list(PINS.values()),'no_new_actor_or_service_calls':True,'root_completion_adoption_pending':True,'final_clearance':False,'remaining_gap':'Authentic root completion receipt/adoption and final global inventory/numeric43/canonical QUEUE-parent reconciliation'}
if __name__=='__main__':print(json.dumps(main(),sort_keys=True,ensure_ascii=False,indent=2,allow_nan=False))
