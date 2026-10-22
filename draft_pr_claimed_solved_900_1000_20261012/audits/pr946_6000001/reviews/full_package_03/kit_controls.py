import sys
if not sys.flags.isolated:raise RuntimeError('Use -I')
from pathlib import Path
import copy,datetime,hashlib,json,types
R=Path('/Users/alec/Documents/Math');A=R/'draft_pr_claimed_solved_900_1000_20261012/audits/pr946_6000001';O=A/'reviews/full_package_03';p=R/'zenodo_deposit_tool/zenodo.py';b=p.read_bytes()
if hashlib.sha256(b).hexdigest()!='a91f961bcabadb15f92bb738c3194f0277cd47f1f87167ac8db8eb7c4fd3b9ca':raise RuntimeError('kit pin')
N={'__name__':'_captured_fake_kit_','__file__':str(R/'zenodo_deposit_tool/zenodo.py')};exec(compile(b,N['__file__'],'exec'),N);N['STATE_DIR']=O/'private/kit_state';N['doi_status']=lambda doi:{'status':'resolved','fake_service':True}
# No credentials or network are accessed: a client is supplied for every operation.
runtime=O/'private/kit_runtime';runtime.mkdir()
freeze=json.loads((A/'preprint/FREEZE.json').read_bytes())
for name in ['zenodo-deposit.json','research_note.pdf','global_hessian_verification.zip']:
 raw=(A/'preprint'/name).read_bytes();pin=freeze['files'][name]
 if len(raw)!=pin['bytes'] or hashlib.sha256(raw).hexdigest()!=pin['sha256']:raise RuntimeError('asset pin')
 (runtime/name).write_bytes(raw)
manifest=runtime/'zenodo-deposit.json';meta,files=N['load_manifest'](manifest)
class Fake:
 def __init__(self):self.posts=0;self.uploads=[];self.publishes=0;self.d={'id':123,'submitted':False,'metadata':copy.deepcopy(meta),'files':[],'links':{'bucket':'https://zenodo.org/fake','html':'https://zenodo.org/fake'}}
 def create(self,m):self.posts+=1;return copy.deepcopy(self.d)
 def get(self,i):return copy.deepcopy(self.d)
 def upload(self,bucket,f):self.uploads.append(f['name']);self.d['files'].append({'filename':f['name'],'filesize':f['size'],'checksum':'md5:'+f['md5']})
 def update(self,i,m):self.d['metadata']=copy.deepcopy(m)
 def publish(self,i):self.publishes+=1;self.d.update(submitted=True,doi='10.5281/zenodo.123');raise N['DepositError']('simulated lost POST response')
f=Fake();out=[]
def args(command,ident=None):return types.SimpleNamespace(command=command,manifest=manifest,sandbox=False,confirm_id=ident,check_doi=True)
r=N['run'](args('stage'),f)
if r['state']!='ready_to_publish' or f.posts!=1 or len(f.uploads)!=2:raise RuntimeError('stage')
out.append({'case':'actual_kit_stage_two_exact_files_metadata','pass':True,'create_count':f.posts,'uploads':list(f.uploads)})
try:N['run'](args('publish',124),f)
except N['DepositError']:out.append({'case':'wrong_confirm_ID','rejected':True,'publish_count':f.publishes})
else:raise RuntimeError('wrong confirm accepted')
r=N['run'](args('publish',123),f)
if not r.get('recovered_after_publish_error') or r['id']!=123 or f.publishes!=1:raise RuntimeError('lost POST recovery')
out.append({'case':'lost_publish_POST_readback_once','pass':True,'publish_count':f.publishes,'doi':r['doi']})
r=N['run'](args('inspect'),f)
if r['state']!='published' or r['doi']!='10.5281/zenodo.123' or f.publishes!=1:raise RuntimeError('inspect')
out.append({'case':'inspect_exact_record_no_repeat_publish','pass':True})
for label,mut in [('wrong_title',lambda d:d['metadata'].update(title='bad')),('wrong_checksum',lambda d:d['files'][0].update(checksum='md5:'+'0'*32)),('extra_file',lambda d:d['files'].append({'filename':'extra','filesize':0,'checksum':'md5:'+'0'*32}))]:
 original=copy.deepcopy(f.d);mut(f.d)
 try:N['run'](args('inspect'),f)
 except N['DepositError']:out.append({'case':label,'rejected':True})
 else:raise RuntimeError('mutated readback accepted')
 f.d=original
result={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'kit_sha256':hashlib.sha256(b).hexdigest(),'exact_frozen_descriptor_sha256':hashlib.sha256(manifest.read_bytes()).hexdigest(),'controls':out,'external_calls':0,'all_services_fake':True};(O/'KIT_CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'PASS','controls':len(out),'external_calls':0}))
