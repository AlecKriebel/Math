"""Private five-target constants and import-safe primitives; no source writes."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import hashlib,json,re
OWN=Path(__file__).resolve().parent
PROGRAMME=OWN.parents[1]
PUBLIC=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public')
IDS=('23441890','23174283','23430498','23149775','23331080')
CLEARANCES={
 '23441890':('root-clearance-23441890-20261114.json','c09a3b765eabc0b98f61dd2f4bafe1f831ccefb0d6b5dc848e109ffa33dfa7c5'),
 '23174283':('root-clearance-23174283-20261114.json','c22dcb687d2065e49b1186b66701687ece05c74468bdf78ae85422432fcd3298'),
 '23430498':('root-clearance-23430498-20261115.json','9791b6178d1a0dc8bd9b32b5f0f56f1812f72e5d0dc1fafc03e806cdc80d8d2d'),
 '23149775':('root-clearance-23149775-20261114.json','b1ae0e007d98f9ece4c712556239c0a9802befd93154972a3d5af39ea9c583b7'),
 '23331080':('root-clearance-23331080-20261114.json','df67490c786bef3bcb1623cfb4a25f5b8948a74d49c039b199543a7cf21da315')}
OLD_DLAB='https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/10/21tkt-1.pdf'
NEW_DLAB='https://kourovkanotebookorg.wordpress.com/'
def need(ok,label):
 if not ok:raise ValueError('five_stage:'+label)
def sha(data):return hashlib.sha256(data).hexdigest()
def bind(path):
 b=Path(path).read_bytes();return {'bytes':len(b),'sha256':sha(b)}
def strict_json(text):
 def pairs(rows):
  d={}
  for k,v in rows:need(k not in d,'duplicate_JSON_key:'+k);d[k]=v
  return d
 return json.loads(text,object_pairs_hook=pairs)
def load(path):return strict_json(Path(path).read_bytes())
def same(a,b):
 if type(a) is not type(b):return False
 if type(a) is dict:return list(a)==list(b) and all(same(a[k],b[k]) for k in a)
 if type(a) is list:return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
 return a==b
def safe_name(name):
 need(type(name) is str and re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]*',name) and name not in {'.','..'},'safe_native_basename')
 return name
def contained(root,path):
 root=Path(root).resolve();p=Path(path);p=p if p.is_absolute() else root/p
 need(p.is_file() and not p.is_symlink() and p.resolve().is_relative_to(root),'contained_regular_input:'+str(path))
 need(all(not q.is_symlink() for q in p.parents if q.is_relative_to(root)),'no_input_symlink_parent')
 return p
def safe_output(path):
 p=Path(path).absolute();need(p.resolve().is_relative_to(OWN) and p.resolve()!=OWN,'only_new_private_stage_output')
 need(all(not q.is_symlink() for q in [p,*p.parents] if q.is_relative_to(OWN)),'no_output_symlinks')
 return p
def authorize_dlab():
 a=load(OWN/'SUPPLEMENTAL_DLAB_AUTHORITY.json');p=Path(a['root_authority_path'])
 need(bind(p)['sha256']==a['root_authority_sha256']=='43e4f6133b8b0cdee7fc686e8d9352d58417873909712b9cf2d407ebe84dab67','exact_additive_root_Dlab_link_authority')
 r=load(p);need(same(r,a['whole_root_authority_original']),'whole_additive_Dlab_authority')
 need(r['old_href']==OLD_DLAB and r['new_href']==NEW_DLAB and r['display_text']=='Kourovka Notebook','exact_single_Dlab_link_delta')
 need(r['status']=='ROOT_ADOPTED_EXACT_ONE_HREF_BACKGROUND_OVERRIDE_FOR_PRIVATE_RENDERING' and r['scientific_sentence_delta'] is None,'Dlab_link_only_scope')
 need(r['historical_source_or_sealed_editorial_mutation_authorized'] is False and r['publication_adoption_or_live_verification'] is False,'Dlab_no_source_or_public_authority')
 proposal=PROGRAMME/'verification/dlab-notebook-link-resolution-sol-20261114/FINAL_SEAL.json'
 need(bind(proposal)['sha256']==r['source_proposal_seal_sha256'],'exact_Dlab_proposal_source')
 return r
def authorize_editorials():
 a=load(OWN/'SUPPLEMENTAL_EDITORIAL_AUTHORITY.json');p=Path(a['root_authority_path'])
 need(bind(p)['sha256']==a['root_authority_sha256']=='4af1b271c9f678899b17504dc2b6678fba2ae11f0a6609da719a543dcc73b4f4','exact_additive_root_five_copy_authority')
 r=load(p);need(same(r,a['whole_root_authority_original']),'whole_five_editorial_authority')
 need(r['status']=='ROOT_FIVE_EDITORIAL_COPY_ADOPTED_PRIVATE_STAGE_CODE_AND_LIVE_GATES_PENDING' and r['followups_all_null'] is True,'full_five_copy_private_adoption_scope')
 need([x['record_id'] for x in r['records']]==list(IDS),'exact_five_root_copy_records')
 for row in r['records']:
  need(row['decision']=='ROOT_ADOPTED_FULL_PUBLIC_COPY_AND_UNIQUE_CONFIGURATION_PROSE_FOR_PRIVATE_STAGING','specific_full_copy_decision')
  for b in row['bindings']:need(bind(contained(PROGRAMME,b['path']))=={k:b[k] for k in ['bytes','sha256']},'root_bound_complete_editorial_input')
 for key in ['production_installation_authorized_by_this_record','live_or_browser_verified_by_this_record','native_canonical_URL_assignment_authorized_by_this_record','source_or_frozen_packet_repair']:need(r[key] is False,'root_no_install_live_native_or_source_repair:'+key)
 return r
