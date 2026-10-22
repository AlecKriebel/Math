"""Exercise full public/tracker helpers and read-only-kit code with local adapters."""
from pathlib import Path
import argparse,contextlib,copy,datetime,hashlib,importlib.util,io,json,shutil,types
H=Path(__file__).resolve().parent;SOURCE=H/'_local/copy';LAB=H/'_local/external_probes';LAB.mkdir(exist_ok=True);RESULT=[]
def load(p,n):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def save(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2)+'\n')
def silent(fn):
 with contextlib.redirect_stdout(io.StringIO()) as out:r=fn()
 return r,out.getvalue()
def reject(fn):
 try:fn()
 except (RuntimeError,ValueError,KeyError,StopIteration) as e:return str(e)
 raise RuntimeError('altered fixture accepted')
def test(n,f):
 try:RESULT.append({'name':n,'status':'PASS','detail':f()})
 except Exception as e:RESULT.append({'name':n,'status':'FAIL','error':repr(e)})
def fixture(n):
 root=LAB/n
 if root.exists():shutil.rmtree(root)
 shutil.copytree(SOURCE/'publication',root/'publication');p=root/'publication';meta=json.loads((p/'zenodo-deposit.json').read_text())['metadata'];b=json.loads((p/'BUILD_RECEIPT.json').read_text());pub={'environment':'production','state':'published','metadata_normalizations':[],'id':321,'doi':'10.5281/zenodo.321','doi_url':'https://doi.org/10.5281/zenodo.321','record_url':'https://zenodo.org/records/321','url':'https://doi.org/10.5281/zenodo.321','title':meta['title'],'files':[{'name':b[k]['path'],'size':b[k]['bytes'],'sha256':b[k]['sha256']} for k in ['pdf','verification_zip']]};save(p/'PUBLICATION_RECEIPT.json',pub);return root,p,meta,b,pub

def public():
 root,p,meta,b,pub=fixture('public');m=load(p/'check_public_downloads.py','public_probe');actualmeta=copy.deepcopy(meta);actualmeta['resource_type']={'type':actualmeta.pop('upload_type'),'subtype':actualmeta.pop('publication_type')};actualmeta['license']={'id':actualmeta['license']};actualmeta['doi']=pub['doi']
 actual={'id':321,'doi':pub['doi'],'metadata':actualmeta,'files':[{'key':b[k]['path'],'links':{'self':'https://zenodo.org/api/records/321/files/'+b[k]['path']+'/content'}} for k in ['pdf','verification_zip']]};current=copy.deepcopy(actual);calls=[];corrupt=False
 def fetch(url,limit):
  calls.append(url)
  if url=='https://zenodo.org/api/records/321':return json.dumps(current).encode()
  item=next((f for f in current['files'] if f['links']['self']==url),None)
  if item is None:raise RuntimeError('unexpected URL')
  return (p/item['key']).read_bytes()+(b'corrupted' if corrupt else b'')
 m.fetch=fetch;silent(m.main);receipt=json.loads((p/'PUBLIC_DOWNLOAD_VERIFICATION.json').read_text());assert len(calls)==3 and receipt['id']==321 and len(receipt['files'])==2 and receipt['metadata_fields_verified']==sorted(meta)
 rejected={}
 for key in meta:
  current=copy.deepcopy(actual)
  if key=='upload_type':current['metadata']['resource_type']['type']='dataset'
  elif key=='publication_type':current['metadata']['resource_type']['subtype']='article'
  elif key=='license':current['metadata']['license']['id']='wrong'
  else:current['metadata'][key]=None
  rejected[key]=reject(lambda:silent(m.main))
 for key in ['record_id','record_doi','metadata_doi','missing_file','duplicate_file','corrupt_file']:
  current=copy.deepcopy(actual);corrupt=False
  if key=='record_id':current['id']=322
  elif key=='record_doi':current['doi']='10.5281/zenodo.322'
  elif key=='metadata_doi':current['metadata']['doi']='10.5281/zenodo.322'
  elif key=='missing_file':current['files'].pop()
  elif key=='duplicate_file':current['files'][1]=current['files'][0]
  else:corrupt=True
  rejected[key]=reject(lambda:silent(m.main))
 return {'full_main_exact_same_record_two_downloads':True,'all11_fields_corruption_and_identity_inventory_bytes_controls':rejected,'network_calls':0}

def tracker(kind):
 root,p,meta,b,pub=fixture('tracker_'+kind);m=load(p/'append_tracker.py','track_probe_'+kind);row=m.expected_row(pub,meta['title']);rows=[['Original Problem','Solution Chat URL','DOI','Notes']];calls=[];appends=0
 if kind=='duplicate':rows += [row,row]
 if kind=='conflict':rows += [[row[0],'outside',pub['doi_url'],'outside']]
 if kind=='wrongheader':rows[0][1]='Wrong'
 if kind=='uncertain_absent':save(p/'tracker/INTENT.json',{'prior':'uncertain'})
 def call(parts,params,body=None):
  nonlocal appends
  calls.append({'parts':parts,'params':params,'body':body})
  if parts==['spreadsheets','get']:return {'sheets':[{'properties':{'sheetId':m.GID,'title':'Renamed' if kind=='renamed' else 'Math Puzzles'}}]}
  if parts==['spreadsheets','values','append']:
   appends+=1;assert body['values']==[row] and row[1]=='' and params['valueInputOption']=='RAW' and params['insertDataOption']=='INSERT_ROWS';rows.append(row)
   if kind=='lost_response' and appends==1:raise RuntimeError('lost append response')
   return {'updates':{'updatedRange':"'Math Puzzles'!A2:D2",'updatedRows':1,'updatedColumns':4}}
  if parts==['spreadsheets','values','get']:
   return {'values':rows if params['range']=="'Math Puzzles'!A:D" else [rows[1]]}
  raise RuntimeError('unexpected app call')
 m.call=call
 if kind in ['duplicate','conflict','wrongheader','uncertain_absent','renamed']:
  msg=reject(lambda:silent(m.main));assert appends==0;return {'refused_before_append':msg,'appends':0}
 if kind=='lost_response':reject(lambda:silent(m.main));assert appends==1 and (p/'tracker/INTENT.json').exists() and not (p/'tracker/TRACKER_RECEIPT.json').exists()
 silent(m.main);silent(m.main);r=json.loads((p/'tracker/TRACKER_RECEIPT.json').read_text());assert appends==1 and r['row']==row and r['row'][1]=='' and r['readback_verified'];m.validate_tracker_receipt(r,pub,meta['title'])
 return {'appends':appends,'full_four_cells_exact_blankB':True,'range':r['updatedRange'],'retry_recovered_exact_row':r['recovered_existing_exact_row'],'application_calls':0}

def kit():
 root,p,meta,b,pub=fixture('kit');m=load(Path('/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py'),'kit_probe');m.STATE_DIR=root/'state';m.doi_status=lambda doi:{'status':'resolved','url':'https://doi.org/'+doi,'fixture':True}
 class Fake:
  def __init__(self):self.creates=0;self.uploads=0;self.publishes=0;self.updates=0;self.lost=True;self.d={'id':321,'submitted':False,'metadata':copy.deepcopy(meta),'files':[],'links':{'bucket':'https://zenodo.org/api/files/offline','html':'https://zenodo.org/deposit/321'},'doi':pub['doi']}
  def create(self,metadata):self.creates+=1;return copy.deepcopy(self.d)
  def get(self,id):assert id==321;return copy.deepcopy(self.d)
  def upload(self,bucket,e):self.uploads+=1;self.d['files'].append({'filename':e['name'],'filesize':e['size'],'checksum':e['md5']});return {}
  def update(self,id,metadata):assert id==321;self.updates+=1;self.d['metadata']=copy.deepcopy(metadata);return copy.deepcopy(self.d)
  def publish(self,id):
   assert id==321;self.publishes+=1;self.d['submitted']=True
   if self.lost:self.lost=False;raise m.DepositError('lost publication response')
   return copy.deepcopy(self.d)
 c=Fake();a=argparse.Namespace(command='check',manifest=p/'zenodo-deposit.json',sandbox=False,confirm_id=None,check_doi=False);check=m.run(a,c);assert len(check['files'])==2
 a.command='stage';st=m.run(a,c);assert st['id']==321 and st['metadata_normalizations']==[];m.run(a,c);assert c.creates==1 and c.uploads==2
 a.command='inspect';ins=m.run(a,c);assert ins['id']==321 and ins['metadata_normalizations']==[]
 a.command='publish';a.confirm_id=322
 try:m.run(a,c)
 except m.DepositError as e:wrong=str(e)
 else:raise RuntimeError('wrong confirm accepted')
 assert c.publishes==0;a.confirm_id=321;out=m.run(a,c);assert out['recovered_after_publish_error'] and out['state']=='published' and out['metadata_normalizations']==[];again=m.run(a,c);assert again['already_published'] and c.publishes==1
 a.command='inspect';again=m.run(a,c);assert again['id']==321 and again['state']=='published' and c.creates==1
 # The generic kit reports its narrow allowed normalization; this PR requires [] and its identity helper rejects it.
 c.d['metadata']['description']=meta['description'].replace('\u2019',"'");normalized=m.run(a,c);assert normalized['metadata_normalizations']
 t=load(p/'append_tracker.py','kit_strict_tracker');strict=reject(lambda:t.validate_publication_identity(normalized,meta['title']))
 return {'creates':c.creates,'uploads':c.uploads,'publication_posts':c.publishes,'wrong_confirm_refused':wrong,'lost_response_recovered_known_id':True,'inspect_exact_metadata_normalizations':ins['metadata_normalizations'],'reported_normalization_rejected_by_PR_contract':strict,'kit_unchanged_and_no_real_client_created':True,'limits':'A local fake supplies all API and DOI responses; kit state writes are private scratch only. Coordinator still must check inspect[] before actual publish.'}

test('public_helper_full_main',public)
for k in ['normal','lost_response','duplicate','conflict','wrongheader','uncertain_absent','renamed']:test('tracker_'+k,lambda k=k:tracker(k))
test('read_only_kit_offline_lifecycle',kit)
save(H/'EXTERNAL_ADAPTER_RESULTS.json',{'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'results':RESULT,'all_pass':all(x['status']=='PASS' for x in RESULT),'scope':'Full production helpers/kit with local fake API/DOI/GWS adapters; no credentials, network, external mutations or live integration.'});print(json.dumps(RESULT,indent=2))
