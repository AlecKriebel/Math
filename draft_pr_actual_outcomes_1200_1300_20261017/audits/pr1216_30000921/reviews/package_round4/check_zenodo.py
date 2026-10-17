#!/usr/bin/env python3
"""Offline exact-manifest exercise of the repository generic deposit kit."""
from pathlib import Path
import argparse,copy,hashlib,importlib.util,json,shutil,socket,sys,datetime
HERE=Path(__file__).resolve().parent
SOURCE=Path('/Users/alec/Documents/Math/zenodo_deposit_tool')
ROOT=HERE/'fixtures/generic_zenodo'
ROOT.mkdir(exist_ok=True)
def no_network(*a,**k):raise RuntimeError('Unmocked network denied by round4 review')
socket.create_connection=no_network
spec=importlib.util.spec_from_file_location('round4_zenodo',SOURCE/'zenodo.py');z=importlib.util.module_from_spec(spec);spec.loader.exec_module(z)
z.STATE_DIR=ROOT/'state';z.doi_status=lambda _: {'status':'resolved','mock':True}
manifest=ROOT/'zenodo-deposit.json'
publication=HERE.parents[1]/'publication'
for n in ['zenodo-deposit.json','Polynomial_Multipliers_Note_v1.0.pdf','Polynomial_Multipliers_Verification_v1.0.zip']:shutil.copyfile(publication/n,ROOT/n)
class Client:
    def __init__(self):self.actions=[];self.record=None;self.lost=False
    def create(self,metadata):
        self.actions.append('create');self.record={'id':123456,'metadata':copy.deepcopy(metadata),'files':[],'submitted':False,'links':{'bucket':'mock://bucket','html':'mock://draft'}};return copy.deepcopy(self.record)
    def get(self,i):
        if i!=123456:raise RuntimeError('unknown mock id')
        return copy.deepcopy(self.record)
    def upload(self,bucket,f):self.actions.append('upload');self.record['files'].append({'filename':f['name'],'filesize':f['size'],'checksum':'md5:'+f['md5']})
    def update(self,i,metadata):self.actions.append('update');self.record['metadata']=copy.deepcopy(metadata)
    def publish(self,i):
        self.actions.append('publish');self.record.update(submitted=True,doi='10.5281/zenodo.123456')
        if self.lost:raise z.DepositError('simulated lost publication response')
def args(command,confirm_id=None):return argparse.Namespace(command=command,manifest=manifest,sandbox=False,confirm_id=confirm_id,check_doi=True)
def need(c,m):
    if not c:raise RuntimeError(m)
client=Client();check=z.run(args('check'),client);need(not client.actions,'local check mutates')
stage=z.run(args('stage'),client);z.run(args('stage'),client);need(client.actions.count('create')==1,'duplicate create');need(client.actions.count('upload')==2,'duplicate upload')
inspection=z.run(args('inspect'),client);need(inspection['metadata_normalizations']==[],'unexpected normalization of exact package')
try:z.run(args('publish',999),client)
except z.DepositError:pass
else:raise RuntimeError('Wrong confirm id accepted')
need(client.actions.count('publish')==0,'wrong-id publication called')
old=copy.deepcopy(client.record['metadata']);client.record['metadata']['description']='stale'
try:z.run(args('publish',123456),client)
except z.DepositError:pass
else:raise RuntimeError('stale metadata accepted')
need(client.actions.count('publish')==0,'stale publication called');client.record['metadata']=old
client.lost=True;receipt=z.run(args('publish',123456),client);need(receipt.get('recovered_after_publish_error'),'lost response not recovered');z.run(args('publish',123456),client);need(client.actions.count('publish')==1,'publication repeated')
result={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'generic_tool_sha256':hashlib.sha256((SOURCE/'zenodo.py').read_bytes()).hexdigest(),'exact_package_check_stage_inspect':True,'create_once_upload_each_once':True,'wrong_confirm_id_and_stale_metadata_refused_before_publish':True,'lost_publish_response_recovered_and_retry_no_second_post':True,'metadata_normalizations':receipt['metadata_normalizations'],'actions':client.actions,'scope':'Actual generic run entrypoint with exact current manifest/artifacts and fake client/DOI resolver. No credentials, live HTTP, record creation or publication. Mathematical gate belongs to coordinator under WORKFLOW.md.'}
(HERE/'ZENODO_MOCK_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
