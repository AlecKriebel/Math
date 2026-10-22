#!/usr/bin/env python3
import os,sys
sys.dont_write_bytecode=True
from pathlib import Path
R=Path(__file__).resolve().parent;A=R.parents[1];S=R/'ignored_scratch/strict_actual';S.mkdir(parents=True,exist_ok=True)
os.environ['TMPDIR']=str(R/'ignored_scratch/tmp');os.environ['PYTHONDONTWRITEBYTECODE']='1'
import argparse,copy,datetime,hashlib,importlib.util,json,shutil,types

def need(v,m):
 if not v:raise RuntimeError(m)
def load(p):
 sp=importlib.util.spec_from_file_location('r3actual_'+p.stem+str(id(p)),p);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
def cp(s,d):d.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(s,d)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for n in ['zenodo-deposit.json','Prime_Difference_Counterexample_Note_v1.0.pdf','Prime_Difference_Counterexample_Verification_v1.0.zip','check_public_downloads.py']:cp(A/'publication'/n,S/n)
cp(Path('/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py'),S/'zenodo.py')
cp(A.parents[1]/'publication_coordinators/pr1268.py',S/'pr1268.py')
c=load(S/'pr1268.py');kit=c.install_exact_verifier(load(S/'zenodo.py'));kit.STATE_DIR=S/'state';kit.doi_status=lambda d:{'status':'resolved','http_status':200}
meta,files=kit.load_manifest(S/'zenodo-deposit.json');record={'id':784512,'submitted':False,'metadata':copy.deepcopy(meta),'files':[{'filename':f['name'],'filesize':f['size'],'checksum':'md5:'+f['md5']}for f in files]}
m=load(S/'check_public_downloads.py');public=copy.deepcopy(meta);public['resource_type']={'type':public.pop('upload_type'),'subtype':public.pop('publication_type')};public['license']={'id':public['license']};need(len(m.verify_public_metadata(public,meta))==11,'public11 baseline')
results=[]
mutations=[]
for k in meta:
 def mutate(d,key=k):
  d['metadata'][key]=None
 mutations.append(('metadata_'+k,mutate))
for i,f in enumerate(files):
 mutations.extend([(f['name']+'_checksum',lambda d,j=i:d['files'][j].update(checksum='md5:'+'0'*32)),(f['name']+'_size',lambda d,j=i:d['files'][j].update(filesize=1)),(f['name']+'_name',lambda d,j=i:d['files'][j].update(filename='wrong'))])
mutations.extend([('different_id',lambda d:d.update(id=784513)),('nonboolean_state',lambda d:d.update(submitted=1)),('extra_file',lambda d:d['files'].append({'filename':'extra','filesize':0,'checksum':'md5:'+'0'*32}))])
for label,mutate in [('baseline',lambda d:None),*mutations]:
 events=[];state=copy.deepcopy(record);mutate(state)
 class Client:
  def get(self,n):events.append('GET');return copy.deepcopy(state)
  def publish(self,n):events.append('POST');state.update(submitted=True,doi='10.5281/zenodo.784512')
 place=kit.state_path((S/'zenodo-deposit.json').resolve(),'production');kit.save_state(place,{'manifest':str((S/'zenodo-deposit.json').resolve()),'environment':'production','id':784512})
 try:
  out=kit.run(argparse.Namespace(command='publish',manifest=S/'zenodo-deposit.json',sandbox=False,confirm_id=784512,check_doi=False),client=Client());accepted=True;error=None
 except kit.DepositError as e:accepted=False;error=str(e)
 need(accepted==(label=='baseline'),'strict kit outcome '+label);need(events.count('POST')==(1 if label=='baseline'else 0),'bad kit POST '+label)
 results.append({'case':label,'accepted':accepted,'events':events,'error':error})
# Independent public projection: change every supplied field via its actual projected locus.
public_results=[]
for k in meta:
 d=copy.deepcopy(public)
 if k=='upload_type':d['resource_type']['type']='wrong'
 elif k=='publication_type':d['resource_type']['subtype']='wrong'
 elif k=='license':d['license']['id']='wrong'
 else:d[k]=None
 try:m.verify_public_metadata(d,meta)
 except RuntimeError as e:public_results.append({'field':k,'rejected':True,'error':str(e)})
 else:raise RuntimeError('public field accepted '+k)
(R/('STRICT_ACTUAL_'+str(sys.flags.optimize)+'.json')).write_text(json.dumps({'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'optimization':sys.flags.optimize,'manifest_sha256':sha(S/'zenodo-deposit.json'),'actual_artifacts':[{'name':f['name'],'bytes':f['size'],'sha256':f['sha256']}for f in files],'strict_genuine_kit_cases':results,'public11_projection_cases':public_results,'all_network_client_methods_mocked':True,'scope':'Actual supplied eleven metadata fields and actual artifact bytes. Strict coordinator wrapper plus genuine unchanged shared-kit run; no authentication credentials or real network.'},indent=2)+'\n')
print(json.dumps({'strict_kit_cases':len(results),'public_field_faults':len(public_results),'optimization':sys.flags.optimize}))
