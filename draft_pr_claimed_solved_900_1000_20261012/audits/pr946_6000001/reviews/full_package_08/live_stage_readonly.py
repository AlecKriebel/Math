"""Read only exact existing ID via the authenticated original kit token factory."""
import sys
if not(sys.flags.isolated and sys.flags.no_site and not sys.flags.optimize and sys.dont_write_bytecode):raise RuntimeError('Use -I -S -B')
from pathlib import Path
import hashlib,json,datetime
R=Path('/Users/alec/Documents/Math');A=R/'draft_pr_claimed_solved_900_1000_20261012/audits/pr946_6000001';O=Path(__file__).resolve().parent
raw=(R/'zenodo_deposit_tool/zenodo.py').read_bytes()
if hashlib.sha256(raw).hexdigest()!='a91f961bcabadb15f92bb738c3194f0277cd47f1f87167ac8db8eb7c4fd3b9ca':raise RuntimeError('kit external pin')
N={'__name__':'_readonly_captured_kit_','__file__':str(R/'zenodo_deposit_tool/zenodo.py')};exec(compile(raw,N['__file__'],'exec',dont_inherit=True,optimize=0),N)
meta,files=N['load_manifest']((A/'operations_runtime/zenodo-deposit.json').resolve());_,state=N['local_state']((A/'operations_runtime/zenodo-deposit.json').resolve(),'production')
if type(state['id'])is not int or state['id']!=23409904:raise RuntimeError('exact private state')
d=N['ZenodoClient']('production',N['token_for']('production')).get(23409904);N['validate_record'](d,23409904)
operator=(A/'publication_operator.py').read_bytes()
if hashlib.sha256(operator).hexdigest()!='d085ec080ee6c2f1239f49f724e7a71ef6d86b3d994fbe9b4039371181a61aef':raise RuntimeError('operator external pin')
M={'__name__':'_readonly_notes_normalizer_','__file__':str(A/'publication_operator.py')};exec(compile(operator,M['__file__'],'exec',dont_inherit=True,optimize=0),M)
logical,changed=M['normalize_notes'](d,meta['notes']);normalizations=N['verify'](logical,meta,files)
if d['submitted'] is not False:raise RuntimeError('Expected unchanged unpublished existing draft')
receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_READONLY_EXISTING_DRAFT','id':d['id'],'submitted':d['submitted'],'exact_single_observed_notes_escape':changed,'all_other_expected_metadata_verified':True,'original_kit_normalizations':normalizations,'remote_files':[{k:v for k,v in f.items() if k in ['filename','filesize','checksum']} for f in d['files']],'expected_files':[{'name':f['name'],'bytes':f['size'],'sha256':f['sha256'],'md5':f['md5']} for f in files],'external_GET_count':1,'POST_create_update_upload_count':0,'credentials_output':False}
(O/'LIVE_STAGE_READONLY.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({k:receipt[k] for k in ['status','id','submitted','exact_single_observed_notes_escape','external_GET_count','POST_create_update_upload_count']}))
