#!/usr/bin/env python3
"""Exact repository kit controls with all HTTP/DOI/state transports isolated."""
import copy,hashlib,html,io,json,shutil,sys,types
from pathlib import Path
import http.client as real_http
R=Path(__file__).absolute().parent;A=R.parent.parent;REPO=A.parents[2]
K=REPO/'zenodo_deposit_tool/zenodo.py';SOURCE=K.read_bytes();SHA=hashlib.sha256(SOURCE).hexdigest()
T=R/'tmp'/('kit-optimized'if sys.flags.optimize else'kit-normal')
if T.exists():shutil.rmtree(T)
T.mkdir(parents=True,exist_ok=True)
k=types.ModuleType('round3_exact_kit');k.__file__=str(K);exec(compile(SOURCE,str(K),'exec'),k.__dict__)
k.STATE_DIR=T/'state';k.token_for=lambda *a:(_ for _ in ()).throw(RuntimeError('REAL TOKEN ACCESS BLOCKED'))
RESULTS=[];NORM=[{'field':'description','kind':'plain_text_html_entities'}];RID=999999991
DOI=f'10.5281/zenodo.{RID}'
def need(c,m):
 if not c:raise ValueError(m)
def check(name,f):f();RESULTS.append({'name':name,'status':'PASS'})
def reject(name,f):
 try:f()
 except (k.DepositError,ValueError):RESULTS.append({'name':name,'status':'REJECTED'});return
 raise ValueError(name+' accepted')
meta,files=k.load_manifest(A/'publication/zenodo-deposit.json')
def deposit(metadata=None,published=False):
 m=copy.deepcopy(meta if metadata is None else metadata);m['description']=html.escape(m['description'],quote=False)
 return {'id':RID,'submitted':published,'metadata':m,'doi':DOI if published else None,
 'links':{'html':f'https://zenodo.org/deposit/{RID}','bucket':f'https://zenodo.org/api/files/fixture'},
 'files':[{'filename':f['name'],'filesize':f['size'],'checksum':'md5:'+f['md5']}for f in files]}
base=deposit();check('actual_metadata_exact_escape_normalization',lambda:need(k.verify(base,meta,files)==NORM,'norm'))
raw=copy.deepcopy(base);raw['metadata']=copy.deepcopy(meta);check('actual_metadata_unchanged_remote_positive',lambda:need(k.verify(raw,meta,files)==[],'raw'))
for field in meta:
 d=copy.deepcopy(base);d['metadata'].pop(field);reject('missing_supplied_metadata_'+field,lambda:k.verify(d,meta,files))
for name,change in [('edited_description',lambda d:d['metadata'].update(description=d['metadata']['description']+' altered')),('wrong_file_checksum',lambda d:d['files'][0].update(checksum='md5:'+'0'*32)),('duplicate_file',lambda d:d['files'].append(copy.deepcopy(d['files'][0]))),('extra_file',lambda d:d['files'].append({'filename':'extra'})),('missing_file',lambda d:d['files'].pop()),('wrong_size',lambda d:d['files'][0].update(filesize=d['files'][0]['filesize']+1)),('creator_reordered_or_edited',lambda d:d['metadata']['creators'][0].update(name='Other'))]:
 d=copy.deepcopy(base);change(d);reject(name,lambda:k.verify(d,meta,files))
for name,desc in [('HTML','<p>'+meta['description']+'</p>'),('preescaped',meta['description']+'&amp;'),('numeric_entity',meta['description']+'&#62;'),('comment',meta['description']+'<!--x-->')]:
 m=copy.deepcopy(meta);m['description']=desc;d=deposit(m);reject('escaped_'+name+'_not_plain_text',lambda:k.verify(d,m,files))
# no-change representation must produce [], and the helper separately rejects a
# claimed one-item normalization with no change.
m=copy.deepcopy(meta);m['description']=m['description'].replace('>','greater than')
check('no_representation_change_emits_empty_list',lambda:need(k.verify(deposit(m),m,files)==[],'nochange'))
# Fake all network calls while retaining exact kit stage/publish/inspect logic.
class Client:
 def __init__(self):self.d=deposit();self.d['files']=[];self.calls=[];self.mode='ok'
 def create(self,m):self.calls.append('CREATE_FAKE');return copy.deepcopy(self.d)
 def get(self,i):
  need(i==RID,'wrong id');self.calls.append('GET_FAKE')
  if self.mode=='lost_get'and self.d['submitted']:raise k.DepositError('fake readback lost')
  return copy.deepcopy(self.d)
 def upload(self,bucket,entry):self.calls.append('UPLOAD_FAKE');self.d['files'].append({'filename':entry['name'],'filesize':entry['size'],'checksum':'md5:'+entry['md5']});return {}
 def update(self,i,m):need(i==RID,'update id');self.calls.append('UPDATE_FAKE');self.d['metadata']=copy.deepcopy(m);self.d['metadata']['description']=html.escape(m['description'],quote=False);return copy.deepcopy(self.d)
 def publish(self,i):
  need(i==RID,'publish id');self.calls.append('PUBLISH_FAKE')
  if self.mode!='unpublished':self.d['submitted']=True;self.d['doi']=DOI
  if self.mode=='lost':raise k.DepositError('fake POST response lost')
  return copy.deepcopy(self.d)

def resolver(doi):need(doi==DOI,'wrong fake DOI');return {'status':'resolved','http_status':200,'url':'https://doi.org/'+DOI,'resolved_url':f'https://zenodo.org/records/{RID}'}
k.doi_status=resolver
args=types.SimpleNamespace(command='stage',manifest=A/'publication/zenodo-deposit.json',sandbox=False,confirm_id=RID,check_doi=True)
for case in ['ok','lost','lost_get','unpublished']:
 k.STATE_DIR=T/case;k.STATE_DIR.mkdir(exist_ok=True);client=Client();args.command='stage';out=k.run(args,client)
 check('stage_exact_current_kit_'+case,lambda:need(out['state']=='ready_to_publish'and out['metadata_normalizations']==NORM and client.calls.count('CREATE_FAKE')==1 and client.calls.count('UPLOAD_FAKE')==2,'stage'))
 k.run(args,client);check('stage_saved_id_reused_no_create_'+case,lambda:need(client.calls.count('CREATE_FAKE')==1 and client.calls.count('UPLOAD_FAKE')==2,'duplicate create/upload'))
 client.mode=case;args.command='publish'
 if case in ['lost_get','unpublished']:reject('publish_unconfirmed_no_automatic_second_POST_'+case,lambda:k.run(args,client));need(client.calls.count('PUBLISH_FAKE')==1,'automatic retry')
 else:
  out=k.run(args,client);check('publish_exact_verified_receipt_'+case,lambda:need(out['state']=='published'and out['receipt_saved']and out['metadata_normalizations']==NORM and out['doi_resolution']['status']=='resolved','publish receipt'))
  args.command='inspect';out=k.run(args,client);check('independent_inspect_same_fake_record_'+case,lambda:need(out['id']==RID and out['state']=='published'and client.calls.count('PUBLISH_FAKE')==1,'inspect'))
  args.command='publish';out=k.run(args,client);check('already_published_no_second_POST_'+case,lambda:need(out['already_published']and client.calls.count('PUBLISH_FAKE')==1,'repeat POST'))
# Low-level HTTPS transport test has no real socket and a fake token only.
wire=[]
class Conn:
 def __init__(self,host,timeout):wire.append(['CONNECT_FAKE',host,timeout]);self.headers={}
 def putrequest(self,method,target):wire.append([method,target])
 def putheader(self,key,value):self.headers[key]=value
 def endheaders(self):need(self.headers.get('Authorization')=='Bearer FAKE-NOT-REAL','fake auth')
 def send(self,data):wire.append(['BODY_BYTES',len(data)])
 def getresponse(self):return types.SimpleNamespace(status=200,read=lambda n:b'{"ok":true}')
 def close(self):wire.append(['CLOSE_FAKE'])
k.http=types.SimpleNamespace(client=types.SimpleNamespace(HTTPSConnection=Conn,HTTPException=real_http.HTTPException))
c=k.ZenodoClient('production','FAKE-NOT-REAL');check('low_level_request_fake_HTTPS_only',lambda:need(c.request('POST','https://zenodo.org/api/fake',{'safe':True})=={'ok':True},'wire'))
for url in ['http://zenodo.org/api/x','https://zenodo.org.evil/api/x','https://sandbox.zenodo.org/api/x','https://user@zenodo.org/api/x','https://zenodo.org:444/api/x']:
 reject('reject_unselected_or_unsafe_host_'+url,lambda:c.request('GET',url))
# Independent reconstruction of staged legacy/native metadata and downloaded
# two-file evidence; this does not make a fresh external publication claim.
r=json.loads((A/'ZENODO_STAGED_NATIVE_READBACK.json').read_bytes());stage=json.loads((A/'ZENODO_STAGE.stdout').read_bytes());native=r['native_metadata'];local=copy.deepcopy(meta)
check('observed_stage_unpublished_id_exact',lambda:need(stage['id']==r['id']==23387442 and stage['state']=='ready_to_publish' and r['published']is False and r['native_pids']=={},'staged state'))
check('observed_stage_local_metadata_unchanged',lambda:need(r['expected_local_metadata']==meta and stage['metadata_normalizations']==r['legacy_metadata_normalizations']==NORM,'stage local'))
expected=copy.deepcopy(meta);expected['description']=html.escape(meta['description'],quote=False)
check('observed_legacy_all11_metadata_exact',lambda:need(r['legacy_supplied_metadata_fields']==expected and r['all_supplied_metadata_fields_verified']==11,'legacy metadata'))
reconstructed={'title':native['title'],'upload_type':'publication','publication_type':native['resource_type']['id'].removeprefix('publication-'),'publication_date':native['publication_date'],'version':native['version'],'description':native['description'],'creators':[{'name':x['person_or_org']['name'],'affiliation':x['affiliations'][0]['name'],'orcid':next(j['identifier']for j in x['person_or_org']['identifiers']if j['scheme']=='orcid')}for x in native['creators']],'access_right':'open'if r['native_access']['record']=='public'and r['native_access']['files']=='public'else None,'license':native['rights'][0]['id'],'keywords':[x['subject']for x in native['subjects']],'related_identifiers':[{'identifier':x['identifier'],'scheme':x['scheme'],'relation':x['relation_type']['id']}for x in native['related_identifiers']]}
expected['related_identifiers']=[dict(x,relation=x['relation'].lower())for x in expected['related_identifiers']]
check('observed_native_all11_metadata_independent_mapping',lambda:need(reconstructed==expected,'native mapping'))
for f in files:
 name=f['name'];matches=list((A/'tmp').glob('staged-*-'+name));need(len(matches)>=1 and all(x.read_bytes()==f['path'].read_bytes()for x in matches),'actual downloads unchanged');b=matches[0].read_bytes()
 check('observed_download_byte_SHA_MD5_size_'+name,lambda:need(b==f['path'].read_bytes()and hashlib.sha256(b).hexdigest()==r['files'][name]['sha256']and hashlib.md5(b).hexdigest()==r['files'][name]['md5']and len(b)==r['files'][name]['bytes']==f['size'],'actual download'))
print(json.dumps({'schema':'pr681-round3-exact-kit-controls-v1','status':'PASS','mode':'optimized'if sys.flags.optimize else'normal','kit_sha256':SHA,'check_count':len(RESULTS),'controls':RESULTS,'HTTP_wire_mocked':wire,'fake_fixtures_only':True,'real_HTTP_or_cloud_mutations':0,'actual_staged_published':False,'remote_description_sha256':hashlib.sha256(html.escape(meta['description'],quote=False).encode()).hexdigest()},indent=2,sort_keys=True))
