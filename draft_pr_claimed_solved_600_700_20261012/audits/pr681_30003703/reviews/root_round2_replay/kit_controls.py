"""Pinned repository kit through a wholly fake client/state/DOI resolver.
No token lookup or real HTTP transport is reachable. Operator-owned durable
stage/publish intents are modeled explicitly outside the unchanged kit.
"""
import copy,hashlib,json,sys,types
from pathlib import Path
R=Path(__file__).absolute().parent;A=R.parent.parent
source=A.parents[2]/'zenodo_deposit_tool/zenodo.py';m=types.ModuleType('round2_exact_kit');m.__file__=str(source)
exec(compile(source.read_bytes(),str(source),'exec'),m.__dict__)
tmp=R/'tmp'/('FAKE_FIXTURE_KIT_OPT'if sys.flags.optimize else'FAKE_FIXTURE_KIT_NORMAL');tmp.mkdir(parents=True,exist_ok=True)
m.STATE_DIR=tmp/'state';m.SECRETS=tmp/'NO_SECRETS_EXIST'
def impossible(*a,**k):raise RuntimeError('LIVE TRANSPORT OR TOKEN PATH REACHED')
m.token_for=impossible;m.http.client.HTTPSConnection=impossible
ID=999999995;DOI='10.5281/zenodo.'+str(ID)
m.doi_status=lambda doi:{'status':'resolved','http_status':200,'url':'https://doi.org/'+doi,'resolved_url':'https://zenodo.org/records/'+str(ID),'FAKE_FIXTURE':True}
checks=[]
def need(v,label):
 if not v:raise RuntimeError(label)
 checks.append({'case':label,'outcome':'PASS'})
def reject(label,fn):
 try:fn()
 except m.DepositError:checks.append({'case':label,'outcome':'REJECTED'});return
 raise RuntimeError('hostile accepted '+label)
manifest=A/'publication/zenodo-deposit.json'
meta,files=m.load_manifest(manifest)
class Fake:
 def __init__(self):
  self.creates=self.uploads=self.publishes=0;self.fail_publish=False
  self.record={'id':ID,'submitted':False,'metadata':{},'files':[],'doi':DOI,'links':{'bucket':'https://zenodo.org/api/files/FAKE','html':'https://zenodo.org/deposit/'+str(ID)}}
 def create(self,metadata):
  if not(tmp/'STAGE_INTENT_FAKE.json').exists():raise RuntimeError('stage without operator intent')
  self.creates+=1;self.record['metadata']=copy.deepcopy(metadata);return copy.deepcopy(self.record)
 def get(self,record_id):
  if record_id!=ID:raise RuntimeError('wrong id')
  return copy.deepcopy(self.record)
 def upload(self,bucket,entry):
  self.uploads+=1
  if hashlib.sha256(entry['path'].read_bytes()).hexdigest()!=entry['sha256']:raise RuntimeError('input changed')
  self.record['files'].append({'filename':entry['name'],'filesize':entry['size'],'checksum':'md5:'+entry['md5']});return{'FAKE':True}
 def update(self,record_id,metadata):self.record['metadata']=copy.deepcopy(metadata);return copy.deepcopy(self.record)
 def publish(self,record_id):
  if not(tmp/'PUBLISH_INTENT_FAKE.json').exists():raise RuntimeError('publish without operator intent')
  self.publishes+=1;self.record['submitted']=True
  if self.fail_publish:raise m.DepositError('FAKE publication response lost after accepted dispatch')
  return copy.deepcopy(self.record)
def args(command,confirm=None):return types.SimpleNamespace(command=command,manifest=manifest,sandbox=False,confirm_id=confirm,check_doi=True)
# State paths can refer to the live manifest, but all state is under FAKE_KIT tmp.
place=m.state_path(manifest.absolute(),'production')
if place.exists():place.unlink()
client=Fake();(tmp/'STAGE_INTENT_FAKE.json').write_text(json.dumps({'FAKE_FIXTURE':True,'input_metadata_sha256':hashlib.sha256(manifest.read_bytes()).hexdigest()}))
staged=m.run(args('stage'),client)
need(client.creates==1 and client.uploads==2 and staged['state']=='ready_to_publish'and staged['metadata_normalizations']==[],'stage_once_exact_manifest_two_files')
staged2=m.run(args('stage'),client)
need(client.creates==1 and client.uploads==2 and staged2==staged,'saved_draft_stage_resumes_without_duplicate_or_reupload')
inspection=m.run(args('inspect'),client)
need(inspection['id']==ID and inspection['state']=='ready_to_publish'and inspection['metadata_normalizations']==[],'exact_staged_inspection_of_same_id_metadata_files')
reject('wrong_confirm_id_cannot_publish',lambda:m.run(args('publish',ID+1),client));need(client.publishes==0,'wrong_id_sent_no_publish')
(tmp/'PUBLISH_INTENT_FAKE.json').write_text(json.dumps({'FAKE_FIXTURE':True,'id':ID,'staged':staged}))
client.fail_publish=True;published=m.run(args('publish',ID),client)
need(client.publishes==1 and published['state']=='published'and published['recovered_after_publish_error']and published['receipt_saved'],'lost_publish_response_recovers_by_get_without_repost')
need(published['doi']==DOI and published['doi_resolution']['resolved_url']=='https://zenodo.org/records/'+str(ID),'exact_public_doi_identity_fake_resolver')
need(published['files']==[{'name':x['name'],'size':x['size'],'sha256':x['sha256']}for x in files],'receipt_binary_sha256_from_exact_prepared_files')
second=m.run(args('inspect'),client)
need(second['state']=='published'and second['metadata_normalizations']==[]and client.publishes==1,'second_metadata_file_doi_inspection_has_no_publish_dispatch')
again=m.run(args('publish',ID),client)
need(again['already_published']and client.publishes==1,'already_published_exact_id_is_read_only')
client.record['metadata']['creators'][0]['orcid']='0000-0000-0000-0000'
reject('changed_remote_ORCID_rejected_at_inspection',lambda:m.run(args('inspect'),client));client.record['metadata']=copy.deepcopy(meta)
client.record['files'][0]['checksum']='md5:'+'0'*32
reject('changed_remote_binary_checksum_rejected',lambda:m.run(args('inspect'),client))
# Transport URL validation must fail before even constructing a connection.
c=m.ZenodoClient('production','FAKE_TOKEN_NOT_A_SECRET')
for url in ['https://sandbox.zenodo.org/api/deposit/depositions','https://evil.invalid/api','http://zenodo.org/api','https://user@zenodo.org/api','https://zenodo.org:444/api']:
 reject('API_environment_host_boundary_'+url,lambda url=url:c.request('GET',url))
print(json.dumps({'schema':'pr681-round2-repository-kit-controls-v1','status':'PASS','count':len(checks),'checks':checks,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'FAKE_FIXTURE_ROOT':str(tmp),'token_lookups':0,'real_HTTP_requests':0,'fake_client':{'create':client.creates,'upload':client.uploads,'publish':client.publishes},'limitation':'Actual staged/public metadata and independently downloaded binaries remain required; fake receipts cannot satisfy live gates.'},indent=2,sort_keys=True))
