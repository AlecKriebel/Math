"""PR205 stage/inspect/publish/inspect-doi/finalize, each explicitly invoked."""
import sys
sys.dont_write_bytecode=True
import argparse,json,os,pathlib,subprocess,urllib.parse,urllib.request
_common=sys.modules.get('operations_common')
if _common is None:raise RuntimeError('Root authenticated-buffer loader must preload operations_common')
globals().update({k:v for k,v in vars(_common).items() if not k.startswith('_')})

class KitProcess:
 def run(self,argv,env):return subprocess.run(argv,env=env,capture_output=True,text=True,check=False)
class PublicHTTP:
 def get(self,url,limit):
  parsed=urllib.parse.urlsplit(url);require(parsed.scheme=='https' and parsed.hostname in ('zenodo.org','doi.org'),'Unexpected public URL')
  request=urllib.request.Request(url,headers={'User-Agent':'PR205-Public-File-Verification/1.0'})
  with urllib.request.urlopen(request,timeout=45) as response:
   require(urllib.parse.urlsplit(response.url).scheme=='https','Non-HTTPS redirect')
   return response.status,response.read(limit+1) if limit else b'',response.url

def locate_kit(base):
 for parent in [base]+list(base.parents):
  p=parent/'zenodo_deposit_tool/zenodo.py'
  if p.is_file():return p.resolve()
 raise RuntimeError('Repository Zenodo kit not found; pass --kit explicitly')

def summary(context,j,expected_id=None,expected_state=None):
 require(isinstance(j,dict) and j.get('environment')=='production','Wrong kit environment')
 require(type(j.get('id')) is int and j['id']>0,'Missing actual positive deposition ID')
 if expected_id is not None:require(j['id']==expected_id,'Different actual deposition ID')
 if expected_state:require(j.get('state')==expected_state,'Unexpected actual publication state')
 require(j.get('title')==context['gate']['metadata']['title'] and j.get('metadata_normalizations')==[],'Metadata verification mismatch/normalization')
 files=j.get('files',[]);require(len(files)==3 and len({x['name'] for x in files})==3 and {x['name']:{'bytes':x['size'],'sha256':x['sha256']} for x in files}==context['gate']['intended_upload_files'],'Kit file set/size/hash differs')
 if j.get('state')=='published':
  require(j.get('record_url')=='https://zenodo.org/records/'+str(j['id']),'Published record URL differs')
  if j.get('doi') is not None:require(j['doi']=='10.5281/zenodo.'+str(j['id']) and j.get('doi_url')=='https://doi.org/'+j['doi'],'Actual DOI/id mismatch')

class Publisher:
 def __init__(self,base,kit=None,transport=None,public=None):
  self.base=pathlib.Path(base).resolve();self.directory=self.base/'private_operations/zenodo'
  self.kit=pathlib.Path(kit).resolve() if kit else None
  self.transport=transport if transport is not None else KitProcess()
  self.public=public if public is not None else PublicHTTP()
 def facts(self):
  c=load_context(self.base);kit=self.kit or locate_kit(self.base)
  require(pin(kit)['sha256']==KIT_SHA,'Repository kit code changed; no kit edits authorized')
  return c,kit
 def record(self,path,context):
  r=read(path);require(r['context']==context_pin(context) and r.get('kit_sha256')==KIT_SHA,'Operational receipt belongs to different gate/ready/package/kit')
  raw=self.directory/r['raw_file'];require(pin(raw)==r['raw_pin'],'Raw kit response changed');body=read(raw)
  require(body['exit']==0 and json.loads(body['stdout'])==r['response'],'Kit response binding failed')
  return r['response']
 def inspection_index(self,path,mode):
  tail=path.name[len(mode)+1:];tail=tail.removesuffix('.raw.json').removesuffix('.json')
  require(tail.isdecimal(),'Unexpected inspection receipt filename');return int(tail)
 def inspect_records(self,mode):return sorted((p for p in self.directory.glob(mode+'_*.json') if not p.name.endswith('.raw.json')),key=lambda p:self.inspection_index(p,mode))
 def next_inspection(self,mode):
  indices=[self.inspection_index(p,mode) for p in self.directory.glob(mode+'_*.json')]
  return self.directory/(mode+'_'+str(max(indices,default=0)+1).zfill(4)+'.json')
 def expected_id(self,c,explicit=None):
  require(explicit is None or type(explicit) is int and explicit>0,'Invalid explicit confirmation ID')
  ids=[]
  p=self.directory/'stage.json'
  if p.exists():ids.append(self.record(p,c)['id'])
  for name in ['inspect','inspect-doi']:
   for p in self.inspect_records(name):ids.append(self.record(p,c)['id'])
  require(not ids or len(set(ids))==1,'Stored operation IDs disagree')
  if explicit is not None:
   require(not ids or explicit==ids[0],'Explicit ID differs from known record');return explicit
  require(ids,'Unknown outcome requires a known --confirm-id and read-only inspect')
  return ids[0]
 def invoke(self,mode,confirm_id=None):
  require(mode in ('stage','inspect','publish','inspect-doi'),'Unsupported mode')
  c,kit=self.facts();cp=context_pin(c)
  if mode in ('stage','publish'):require(not (self.base/'ROOT_PUBLICATION_RECEIPT.json').exists(),'Publication already finalized')
  private_directory(self.directory)
  expected=None
  if mode!='stage':
   marker=self.directory/'STAGE_INFLIGHT.json';require(marker.exists(),'No original stage attempt to inspect/publish')
   require(read(marker)['context']==cp,'Original stage context changed')
   expected=self.expected_id(c,confirm_id)
  if mode=='publish':
   require(confirm_id is not None,'Publish requires explicit --confirm-id')
   ready=[]
   if (self.directory/'stage.json').exists():ready.append(self.record(self.directory/'stage.json',c))
   ready.extend(self.record(p,c) for p in self.inspect_records('inspect'))
   require(any(x.get('id')==expected and x.get('state')=='ready_to_publish' for x in ready),'No verified ready inspection/stage for confirmed ID')
  if mode in ('stage','publish'):
   target=self.directory/(mode+'.json');marker=self.directory/(mode.upper()+'_INFLIGHT.json')
   require(not target.exists() and not marker.exists(),'Mutation was already attempted; inspect read-only, never repeat')
   durable_json(marker,dict(UTC=utc(),mode=mode,context=cp,known_id=expected,intended_upload_files=c['gate']['intended_upload_files'],mutation_not_yet_launched=True,semantics='Exclusive file and directory fsynced before child; existence prohibits every automatic mutation retry, including unknown outcomes.'))
  else:target=self.next_inspection(mode)
  same_context(self.base,cp)
  command=[sys.executable,'-E','-S','-B','-P',str(kit),('inspect' if mode=='inspect-doi' else mode),str(c['manifest'])]
  if mode=='inspect-doi':command+=['--check-doi']
  if mode=='publish':command+=['--confirm-id',str(expected)]
  env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');rawpath=target.with_name(target.stem+'.raw.json')
  try:proc=self.transport.run(command,env)
  except Exception as error:
   durable_json(rawpath,dict(UTC=utc(),context=cp,argv=command,launch_exception_type=type(error).__name__,outcome_unconfirmed=True))
   raise RuntimeError('Kit outcome unknown; durable inflight retained; inspect read-only') from None
  durable_json(rawpath,dict(UTC=utc(),context=cp,argv=command,exit=proc.returncode,stdout=proc.stdout,stderr=proc.stderr))
  require(proc.returncode==0,'Kit outcome unconfirmed; inspect private raw receipt, do not repeat mutation')
  j=json.loads(proc.stdout,parse_constant=reject_constant)
  summary(c,j,expected,'ready_to_publish' if mode=='stage' else 'published' if mode=='publish' else None)
  require(j.get('state') in ('ready_to_publish','published'),'Unknown kit state')
  same_context(self.base,cp)
  durable_json(target,dict(UTC=utc(),context=cp,response=j,raw_file=rawpath.name,raw_pin=pin(rawpath),kit_sha256=KIT_SHA))
  return j
 def finalize(self):
  require(self.directory.resolve()==self.directory and self.directory.is_dir() and not self.directory.is_symlink(),'Missing/symlinked private publication directory')
  c,kit=self.facts();cp=context_pin(c);target=self.base/'ROOT_PUBLICATION_RECEIPT.json';require(not target.exists(),'Publication receipt already exists')
  marker=self.directory/'PUBLISH_INFLIGHT.json';require(marker.exists(),'No preserved publish intent')
  intent=read(marker);require(intent['context']==cp and type(intent['known_id']) is int,'Publish context/id missing')
  inspections=self.inspect_records('inspect-doi');require(inspections,'Fresh inspect-doi receipt required')
  j=self.record(inspections[-1],c);summary(c,j,intent['known_id'],'published')
  require(j.get('doi') is not None and j.get('doi_url')=='https://doi.org/'+j['doi'],'No actual assigned DOI; never invent one')
  require(j.get('doi_resolution',{}).get('http_status')==200 and j['doi_resolution'].get('status')=='resolved','Kit DOI resolver not verified')
  checked=[]
  for name,wanted in sorted(c['gate']['intended_upload_files'].items()):
   url='https://zenodo.org/api/records/'+str(j['id'])+'/files/'+urllib.parse.quote(name,safe='')+'/content'
   status,raw,finalurl=self.public.get(url,wanted['bytes'])
   require(status==200 and len(raw)==wanted['bytes'] and digest(raw)==wanted['sha256'],'Public download size/SHA mismatch')
   checked.append(dict(name=name,url=url,final_url=finalurl,bytes=len(raw),sha256=digest(raw)))
  status,unused,finalurl=self.public.get(j['doi_url'],0)
  parsed=urllib.parse.urlsplit(finalurl)
  require(status==200 and parsed.scheme=='https' and parsed.hostname=='zenodo.org' and parsed.path.rstrip('/') in ('/records/'+str(j['id']),'/record/'+str(j['id'])),'Independent actual DOI resolver mismatch')
  same_context(self.base,cp)
  receipt=dict(UTC=utc(),PR=PR,actual_publication_verified=True,metadata_exact_verified=True,metadata_normalizations=[],metadata_exact_evidence='Pinned repository kit verifies every manifest metadata field; no normalization accepted.',metadata_sha256=digest(encoded(c['gate']['metadata'])),all_three_public_download_SHA256_verified=True,verified_public_download_names=[x['name'] for x in checked],public_downloads=checked,id=j['id'],state='published',doi=j['doi'],doi_url=j['doi_url'],record_url=j['record_url'],doi_resolution=dict(status='resolved',http_status=status,final_url=finalurl),files=j['files'],gate_sha256=c['gate_pin']['sha256'],publication_gate='ROOT_PUBLICATION_GATE_01.json',package=c['gate']['package'],context=cp,inspect_doi_receipt=pin(inspections[-1]),historical_firstness_independence_established=False,private_kit_receipts='private_operations/zenodo/')
  durable_json(target,receipt,readonly=True);return receipt

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('mode',choices=['stage','inspect','publish','inspect-doi','finalize']);p.add_argument('--base',type=pathlib.Path,default=pathlib.Path(__file__).resolve().parent.parent);p.add_argument('--kit',type=pathlib.Path);p.add_argument('--confirm-id',type=int);p.add_argument('--adoption',required=True);p.add_argument('--adoption-bytes',required=True,type=int);p.add_argument('--adoption-sha256',required=True);args=p.parse_args()
 configure_authority(args.adoption,dict(bytes=args.adoption_bytes,sha256=args.adoption_sha256))
 publisher=Publisher(args.base,args.kit)
 result=publisher.finalize() if args.mode=='finalize' else publisher.invoke(args.mode,args.confirm_id)
 print(json.dumps(result,sort_keys=True))
if __name__=='__main__':raise RuntimeError('Live operations require the Root authenticated-buffer dispatcher; direct script execution refused')
