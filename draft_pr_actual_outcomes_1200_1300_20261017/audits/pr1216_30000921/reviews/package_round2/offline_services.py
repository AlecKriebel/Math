from pathlib import Path
import copy,datetime,hashlib,importlib.util,json,shutil
R=Path(__file__).resolve().parent;P=R.parent.parent/'publication';C=R/'_local/controls/services';C.mkdir(parents=True,exist_ok=True)
def load(n):
 s=importlib.util.spec_from_file_location('service_'+n,P/(n+'.py'));m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def put(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d))
headers=['Original Problem','Solution Chat URL','DOI','Notes'];results=[]
def tracker(name,scenario):
 root=C/name
 if root.exists():shutil.rmtree(root)
 root.mkdir(exist_ok=True);m=load('append_tracker');m.ROOT=root
 put(root/'PUBLICATION_RECEIPT.json',{'state':'published','doi_url':'https://doi.org/10.5281/zenodo.123'})
 shutil.copyfile(P/'zenodo-deposit.json',root/'zenodo-deposit.json')
 state={'rows':[headers.copy()],'appends':0,'lost':False,'badread':False,'header':False}
 def call(parts,params,body=None):
  if parts==['spreadsheets','get']:return {'sheets':[{'properties':{'sheetId':m.GID,'title':'Math Puzzles'}}]}
  if parts==['spreadsheets','values','get']:
   if params['range'].endswith('A:D'):return {'values':copy.deepcopy(state['rows'])}
   return {'values':[['wrong']] if state['badread'] else [copy.deepcopy(state['rows'][-1])]}
  if parts==['spreadsheets','values','append']:
   state['appends']+=1;state['rows']+=copy.deepcopy(body['values'])
   if state['lost']:state['lost']=False;raise RuntimeError('simulated lost response after accepted append')
   return {'updates':{'updatedRange':"'Math Puzzles'!A2:D2",'updatedRows':1,'updatedColumns':4}}
  raise RuntimeError('Unmocked GWS operation')
 m.call=call
 errors=[]
 def run():
  try:m.main();return True
  except Exception as e:errors.append(str(e));return False
 if scenario=='normal':ok=run() and run() and state['appends']==1
 elif scenario=='lost':
  state['lost']=True;first=run();ok=not first and run() and state['appends']==1
 elif scenario=='prior_intent':
  put(root/'tracker/INTENT.json',{'old':'intent'});ok=not run() and state['appends']==0
 elif scenario=='headers':
  state['rows'][0][2]='wrong';ok=not run() and state['appends']==0
 elif scenario=='duplicate':
  run();state['rows'].append(state['rows'][1].copy());ok=not run() and state['appends']==1
 elif scenario=='conflict':
  state['rows'].append(['30000921','','wrong DOI','unrelated']);ok=not run() and state['appends']==0
 elif scenario=='readback':
  state['badread']=True;ok=not run() and state['appends']==1 and not (root/'tracker/TRACKER_RECEIPT.json').exists()
 results.append({'case':'tracker_'+name,'pass':ok,'appends':state['appends'],'errors':errors})
for name in ['normal','lost','prior_intent','headers','duplicate','conflict','readback']:tracker(name,name)
meta=json.loads((P/'zenodo-deposit.json').read_text())['metadata'];build=json.loads((P/'BUILD_RECEIPT.json').read_text());wanted=copy.deepcopy(meta)
def public(name,mutator=None):
 root=C/('public_'+name)
 if root.exists():shutil.rmtree(root)
 root.mkdir(exist_ok=True);m=load('check_public_downloads');m.ROOT=root
 shutil.copyfile(P/'zenodo-deposit.json',root/'zenodo-deposit.json');shutil.copyfile(P/'BUILD_RECEIPT.json',root/'BUILD_RECEIPT.json')
 put(root/'PUBLICATION_RECEIPT.json',{'state':'published','metadata_normalizations':[],'id':123,'doi':'10.5281/zenodo.123'})
 actualmeta=copy.deepcopy(meta);actualmeta['resource_type']={'type':actualmeta.pop('upload_type'),'subtype':actualmeta.pop('publication_type')};actualmeta['license']={'id':actualmeta['license']};actualmeta['doi']='10.5281/zenodo.123'
 data={'id':123,'doi':'10.5281/zenodo.123','metadata':actualmeta,'files':[{'key':build[k]['path'],'links':{'self':'https://mock/'+k}} for k in ['pdf','verification_zip']]}
 bytefiles={k:(P/build[k]['path']).read_bytes() for k in ['pdf','verification_zip']}
 if mutator:mutator(data,bytefiles)
 calls=[]
 def fetch(url,limit):
  calls.append(url)
  if url=='https://zenodo.org/api/records/123':return json.dumps(data).encode()
  if url.startswith('https://mock/'):return bytefiles[url.split('/')[-1]]
  raise RuntimeError('Unmocked Zenodo operation')
 m.fetch=fetch
 try:m.main();outcome='accepted';err=None
 except Exception as e:outcome='rejected';err=str(e)
 expected='accepted' if mutator is None else 'rejected'
 results.append({'case':'public_'+name,'pass':outcome==expected,'outcome':outcome,'error':err,'fetches':len(calls)})
public('valid')
for key in meta:
 def corrupt(d,b,key=key):
  if key=='upload_type':d['metadata']['resource_type']['type']='wrong'
  elif key=='publication_type':d['metadata']['resource_type']['subtype']='wrong'
  elif key=='license':d['metadata']['license']['id']='wrong'
  else:d['metadata'][key]=None
 public('field_'+key,corrupt)
public('wrong_id',lambda d,b:d.update(id=124))
public('wrong_doi',lambda d,b:d.update(doi='10.5281/zenodo.999'))
public('wrong_metadata_doi',lambda d,b:d['metadata'].update(doi='wrong'))
public('missing_file',lambda d,b:d['files'].pop())
public('duplicate_file',lambda d,b:d['files'].append(copy.deepcopy(d['files'][0])))
public('corrupt_pdf',lambda d,b:b.update(pdf=b['pdf'][:-1]+bytes([b['pdf'][-1]^1])))
public('corrupt_zip',lambda d,b:b.update(verification_zip=b['verification_zip'][:-1]))
(R/'OFFLINE_SERVICE_RECEIPT.json').write_text(json.dumps({'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'all_passed':all(x['pass'] for x in results),'results':results,'scope':'Main entry points with fully mocked GWS and Zenodo calls; no external mutation.'},indent=2)+'\n')
print(json.dumps({'all_passed':all(x['pass'] for x in results),'cases':len(results)}))
