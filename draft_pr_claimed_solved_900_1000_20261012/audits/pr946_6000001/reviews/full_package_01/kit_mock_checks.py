import sys
if not sys.flags.safe_path:raise SystemExit('safe startup')
import pathlib,json,hashlib,copy,types,datetime
R=pathlib.Path('/Users/alec/Documents/Math');A=R/'draft_pr_claimed_solved_900_1000_20261012/audits/pr946_6000001';W=A/'reviews/full_package_01';source=R/'zenodo_deposit_tool/zenodo.py';raw=source.read_bytes()
if hashlib.sha256(raw).hexdigest()!='a91f961bcabadb15f92bb738c3194f0277cd47f1f87167ac8db8eb7c4fd3b9ca':raise ValueError('external kit pin')
N={'__name__':'_captured_mock_kit_','__file__':str(source)};exec(compile(raw,str(source),'exec'),N)
fix=W/'private/kit_fixture';fix.mkdir();N['STATE_DIR']=fix/'state';N['doi_status']=lambda doi:{'status':'resolved','synthetic':True}
# Actual frozen two-file descriptor and payload bytes, authenticated earlier.
for name in ['zenodo-deposit.json','research_note.pdf','global_hessian_verification.zip']:(fix/name).write_bytes((A/'preprint'/name).read_bytes())
calls=[]
class Client:
 def __init__(self):self.data=None
 def create(self,meta):
  calls.append('create');self.data={'id':17,'submitted':False,'metadata':copy.deepcopy(meta),'files':[],'links':{'bucket':'https://zenodo.org/api/files/mock','html':'https://zenodo.org/deposit/17'}};return copy.deepcopy(self.data)
 def get(self,ident):
  if ident!=17:raise RuntimeError('wrong mock ID')
  calls.append('get');return copy.deepcopy(self.data)
 def upload(self,bucket,entry):
  calls.append('upload:'+entry['name']);self.data['files'].append({'filename':entry['name'],'filesize':entry['size'],'checksum':entry['md5']});return {}
 def update(self,ident,metadata):calls.append('update');self.data['metadata']=copy.deepcopy(metadata);return {}
 def publish(self,ident):
  if ident!=17:raise RuntimeError('wrong publish ID')
  calls.append('publish');self.data['submitted']=True;self.data['doi']='10.5281/zenodo.17';return {}
client=Client()
def args(command,ident=None):return types.SimpleNamespace(command=command,manifest=fix/'zenodo-deposit.json',sandbox=False,confirm_id=ident,check_doi=True)
stage=N['run'](args('stage'),client)
if stage['state']!='ready_to_publish' or stage['id']!=17 or len(stage['files'])!=2:raise RuntimeError('stage')
wrong=False
try:N['run'](args('publish',16),client)
except N['DepositError']:wrong=True
if not wrong or 'publish' in calls:raise RuntimeError('wrong ID accepted')
pub=N['run'](args('publish',17),client);inspect=N['run'](args('inspect'),client)
if pub['state']!='published' or inspect['state']!='published' or pub['files']!=stage['files'] or inspect['files']!=stage['files'] or pub['doi']!='10.5281/zenodo.17' or calls.count('publish')!=1:raise RuntimeError('publication linkage')
old=client.data['metadata']['title'];client.data['metadata']['title']='unreviewed title';bad=False
try:N['run'](args('inspect'),client)
except N['DepositError']:bad=True
if not bad:raise RuntimeError('metadata mismatch accepted')
client.data['metadata']['title']=old;client.data['files'].append({'filename':'extra.txt','filesize':1,'checksum':'0'*32});badfile=False
try:N['run'](args('inspect'),client)
except N['DepositError']:badfile=True
if not badfile:raise RuntimeError('extra file accepted')
result={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_kit_sha256':hashlib.sha256(raw).hexdigest(),'frozen_two_file_descriptor_used':True,'stage_publish_inspect_files_equal':True,'wrong_confirm_id_rejected_before_publish':wrong,'metadata_title_mismatch_rejected':bad,'extra_remote_file_rejected':badfile,'mock_publish_calls':calls.count('publish'),'actual_external_actions':0,'network_client':'injected synthetic in-memory client; public DOI resolver mocked','files':stage['files']}
(W/'KIT_MOCK_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'PASS','actual_external_actions':0,'mock_publish_calls':1}))
