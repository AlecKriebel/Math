#!/usr/bin/env python3
"""Read-only independent native metadata and downloaded-byte comparison."""
import argparse,datetime,hashlib,html,http.client,types,json,sys,urllib.parse,urllib.request
from pathlib import Path
sys.dont_write_bytecode=True
A=Path(__file__).absolute().parent;P=A/'publication';REPO=A.parents[2]
K=REPO/'zenodo_deposit_tool/zenodo.py'
EXPECTED_KIT='a91f961bcabadb15f92bb738c3194f0277cd47f1f87167ac8db8eb7c4fd3b9ca'
def sha(b):return hashlib.sha256(b).hexdigest()
def require(c,m):
 if not c:raise ValueError(m)
def write(p,d):
 with p.open('x') as f:json.dump(d,f,indent=2,ensure_ascii=False);f.write('\n')
def normalize(native):
 m=native['metadata']
 return {'title':m['title'],'upload_type':'publication' if m['resource_type']['id'].startswith('publication-') else None,'publication_type':m['resource_type']['id'].removeprefix('publication-'),'publication_date':m['publication_date'],'version':m['version'],'description':m['description'],'creators':[{'name':x['person_or_org']['name'],'affiliation':x.get('affiliations',[{}])[0].get('name'),'orcid':next((i['identifier'] for i in x['person_or_org'].get('identifiers',[]) if i['scheme']=='orcid'),None)} for x in m['creators']],'access_right':'open' if native['access'].get('record')=='public' and native['access'].get('files')=='public' else None,'license':m['rights'][0]['id'],'keywords':[x['subject'] for x in m['subjects']],'related_identifiers':[{'identifier':x['identifier'],'scheme':x['scheme'],'relation':x['relation_type']['id'].lower()} for x in m['related_identifiers']]}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--phase',choices=['staged','published'],required=True);ap.add_argument('--receipt',required=True);args=ap.parse_args()
 captured_kit=K.read_bytes()
 require(sha(captured_kit)==EXPECTED_KIT,'repository kit changed')
 k=types.ModuleType('readonly_repository_zenodo');k.__file__=str(K)
 exec(compile(captured_kit,str(K),'exec'),k.__dict__)
 manifest=(P/'zenodo-deposit.json').resolve();metadata,files=k.load_manifest(manifest)
 place,state=k.local_state(manifest,'production');require(state is not None,'no known saved deposit identity')
 rid=state['id'];client=k.ZenodoClient('production',k.token_for('production'))
 legacy=client.get(rid);k.validate_record(legacy,rid);normalizations=k.verify(legacy,metadata,files)
 staged=args.phase=='staged';require(legacy['submitted'] is (not staged),'phase differs from actual publication state')
 if staged:native=client.native_get(rid,draft=True)
 else:
  request=urllib.request.Request(f'https://zenodo.org/api/records/{rid}',headers={'Accept':'application/vnd.inveniordm.v1+json','User-Agent':k.USER_AGENT})
  with urllib.request.urlopen(request,timeout=45) as response:
   require(response.status==200,'public native status');native=json.load(response)
 require(str(native['id'])==str(rid),'wrong native identity')
 require(native['is_published'] is (not staged),'native published state differs')
 expected=dict(metadata);expected['related_identifiers']=[dict(x,relation=x['relation'].lower()) for x in metadata['related_identifiers']]
 for norm in normalizations:
  require(norm=={'field':'description','kind':'plain_text_html_entities'},'unreviewed normalization kind')
  expected['description']=html.escape(metadata['description'],quote=False)
 actual=normalize(native);require(actual==expected,'native supplied metadata mapping differs')
 entries=native['files']['entries'];require(set(entries)=={x['name'] for x in files},'native file inventory differs')
 scratch=A/'tmp';scratch.mkdir(exist_ok=True)
 stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
 write(scratch/f'zenodo-{args.phase}-{stamp}.json',native)
 checks={}
 for file in files:
  name=file['name'];entry=entries[name]
  url=f'https://zenodo.org/api/records/{rid}' + ('/draft' if staged else '') + f'/files/{urllib.parse.quote(name)}/content'
  u=urllib.parse.urlsplit(url);require(u.scheme=='https' and u.hostname=='zenodo.org' and u.port in (None,443) and not u.username and not u.password,'unsafe download URL')
  headers={'User-Agent':k.USER_AGENT}
  if staged:headers['Authorization']='Bearer '+client.token
  connection=http.client.HTTPSConnection('zenodo.org',timeout=45)
  try:
   connection.request('GET',u.path+('?' +u.query if u.query else ''),headers=headers);response=connection.getresponse();data=response.read(10_000_001)
   require(response.status==200 and len(data)<=10_000_000,'download failed or oversize')
  finally:connection.close()
  require(data==file['path'].read_bytes() and len(data)==file['size'] and sha(data)==file['sha256'],'download bytes differ')
  md5=hashlib.md5(data).hexdigest();require(entry['size']==len(data) and entry['checksum']=='md5:'+md5,'native size/MD5 differs')
  (scratch/f'{args.phase}-{stamp}-{name}').write_bytes(data)
  checks[name]={'bytes':len(data),'sha256':sha(data),'md5':md5,'HTTP_status':200}
 if not staged:
  require(native['status']=='published' and native['pids']['doi']['identifier']==f'10.5281/zenodo.{rid}','published DOI/state mismatch')
  previous=json.loads((A/'ZENODO_STAGED_NATIVE_READBACK.json').read_text())
  require(previous['native_metadata']==native['metadata'] and previous['native_access']==native['access'],'metadata/access changed since staged inspection')
 result={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_EXACT_METADATA_AND_DOWNLOADED_BYTES' if not normalizations else 'PASS_DOCUMENTED_KIT_NORMALIZATION_REQUIRES_RECONCILIATION','id':rid,'published':not staged,'expected_local_metadata':metadata,'legacy_supplied_metadata_fields':{key:legacy['metadata'].get(key) for key in metadata},'legacy_metadata_normalizations':normalizations,'native_metadata':native['metadata'],'native_access':native['access'],'native_pids':native.get('pids',{}),'files':checks,'all_supplied_metadata_fields_verified':len(metadata),'only_read_requests':True}
 write(A/args.receipt,result);print(json.dumps({'status':result['status'],'id':rid,'normalizations':normalizations,'files':checks},indent=2))
if __name__=='__main__':main()
