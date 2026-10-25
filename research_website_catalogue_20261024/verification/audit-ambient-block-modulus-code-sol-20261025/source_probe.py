"""Independent, in-memory schema and custody probes; never executes supplied maths."""
from pathlib import Path
from copy import deepcopy
import sys,json,hashlib,datetime
E=Path(__file__).resolve().parent;P=E.parents[1];S=P/'verification/local-ambient-block-modulus-stage-sol-20261025';sys.path[:0]=[str(S),str(P/'scripts')]
import ambient_block_modulus_source as m
rb,rt=Path.read_bytes,Path.read_text;dg=m.digest;rows=[]
def run(rid,name,layer,expect,fn):
 try:
  value=fn();observed='accepted';reason='';detail=value if isinstance(value,dict) else None
 except Exception as e:observed='rejected';reason=type(e).__name__+':'+str(e);detail=None
 rows.append({'record_id':rid,'case':name,'layer':layer,'expected':expect,'observed':observed,'expectation_met':expect==observed,'reason':reason,'detail':detail})
def call(p,c,g):return m.ambient_block_modulus_source_view(p,c,g)
def altered_actual(p,c,g,path,payload,name):
 Path.read_bytes=lambda q:payload if q==path else rb(q)
 Path.read_text=lambda q,*a,**k:Path.read_bytes(q).decode(k.get('encoding') or 'utf-8')
 try:run(p.name,name,'unmodified full consumer; actual read altered only','rejected',lambda:call(p,c,g))
 finally:Path.read_bytes=rb;Path.read_text=rt
for rid in sorted(m.ABM_IDS):
 p=P/'papers'/rid;c=json.loads(rb(p/'publication.json'));g=json.loads(rb(p/'promotion.json'));b=c['source_binding'];raw=json.loads(rb(p/b['source_receipt_path']));api=json.loads(rb(p/b['raw_record_path']));snap=json.dumps([c,g,raw,api],sort_keys=True)
 run(rid,'pristine_full_consumer','unmodified full consumer','accepted',lambda:call(p,c,g))
 for name in ['completion_int_to_float','version_string_to_number','root_status_to_generic_PASS','whole_custom_verdict_drop_field','transport_drop_entry','source_receipt_add_files_alias','premature_AA','whole_defect_drop_effect']:
  cc,gg=deepcopy(c),deepcopy(g)
  if name=='completion_int_to_float':cc['review_metadata']['completion_percent']=100.0
  elif name=='version_string_to_number':cc['version']=1.0
  elif name=='root_status_to_generic_PASS':gg['status']='PASS_ANY_SUFFIX'
  elif name=='whole_custom_verdict_drop_field':gg['reviews']['analytic']['verdict'].pop(next(iter(gg['reviews']['analytic']['verdict'])))
  elif name=='transport_drop_entry':cc['source_binding']['transport_receipt_original'].pop()
  elif name=='source_receipt_add_files_alias':cc['source_binding']['source_receipt_original']['files']=[]
  elif name=='premature_AA':cc['AA']='https://aleckriebel.com/research/unauthorized/'
  elif name=='whole_defect_drop_effect':
   if rid!='23441617':continue
   gg['root_clearance_record']['noncentral_bibliographic_defect'].pop('effect')
  run(rid,name,'unmodified full consumer; caller objects altered only','rejected',lambda:call(p,cc,gg))
 for rel in ['publication.json','promotion.json',b['source_receipt_path'],b['metadata_path'],b['raw_record_path'],b['transport_receipt_path'],'sources/archive-members.json']:
  path=p/rel;data=rb(path);altered_actual(p,c,g,path,data+b' ', 'actual_file_byte_change:'+rel)
 key,objkey=m.SCHEMAS[rid]
 for name in ['bytes_float','bytes_string','bytes_boolean','API_size_float','SHA_uppercase','MD5_uppercase','API_checksum_mismatch','wrong_asset_schema','array_tuple','asset_array_reorder','asset_unknown_field','asset_path_escape']:
  rr,aa=deepcopy(raw),deepcopy(api)
  if name=='bytes_float':rr[key][0]['bytes']=float(rr[key][0]['bytes'])
  elif name=='bytes_string':rr[key][0]['bytes']=str(rr[key][0]['bytes'])
  elif name=='bytes_boolean':rr[key][0]['bytes']=True
  elif name=='API_size_float':rr[key][0][objkey]['size']=float(rr[key][0][objkey]['size']);aa['files'][0]['size']=float(aa['files'][0]['size'])
  elif name=='SHA_uppercase':rr[key][0]['sha256']=rr[key][0]['sha256'].upper()
  elif name=='MD5_uppercase':rr[key][0]['md5']=rr[key][0]['md5'].upper()
  elif name=='API_checksum_mismatch':rr[key][0][objkey]['checksum']='md5:'+'0'*32;aa['files'][0]['checksum']='md5:'+'0'*32
  elif name=='wrong_asset_schema':rr['all_assets' if key=='all_actual_assets' else 'all_actual_assets']=rr.pop(key)
  elif name=='array_tuple':rr[key]=tuple(rr[key])
  elif name=='asset_array_reorder':rr[key].reverse()
  elif name=='asset_unknown_field':rr[key][0]['http_status']=200
  elif name=='asset_path_escape':rr[key][0]['path']=str(p.parent/'escape')
  run(rid,name,'standalone validate_abm_assets; actual authority not bypassed','rejected',lambda:m.validate_abm_assets(p,rid,rr,aa))
 inv=json.loads(rb(p/'sources/archive-members.json'));arc=p/'sources'/c['supplement_filename']
 run(rid,'pristine_complete_recursive_archive','standalone archive CRC/read/extraction','accepted',lambda:m.verify_abm_archive(p,rid,arc,inv))
 for name in ['wrong_member_crc','wrong_member_sha','member_count_drop','duplicate_member_remove_other','member_bytes_float']:
  ii=deepcopy(inv)
  if name=='wrong_member_crc':ii['members'][0]['CRC32']='00000000'
  elif name=='wrong_member_sha':ii['members'][0]['sha256']='0'*64
  elif name=='member_count_drop':ii['members'].pop()
  elif name=='duplicate_member_remove_other':ii['members'][-1]=deepcopy(ii['members'][0])
  elif name=='member_bytes_float':ii['members'][0]['bytes']=float(ii['members'][0]['bytes'])
  run(rid,name,'standalone archive utility; inventory not authenticated in this direct call','accepted' if name=='member_bytes_float' else 'rejected',lambda:m.verify_abm_archive(p,rid,arc,ii))
 if rid=='23416806':
  for name in ['drop_nested_container_rows','collapse_nested_qualification','escape_extraction_root','duplicate_container_declaration','container_depth_float']:
   ii=deepcopy(inv)
   if name=='drop_nested_container_rows':ii['members']=[x for x in ii['members'] if x['container']==arc.name]
   elif name=='collapse_nested_qualification':ii['archive_containers'][1]['container']=arc.name
   elif name=='escape_extraction_root':ii['archive_containers'][1]['extraction_root']=str(p.parent)
   elif name=='duplicate_container_declaration':ii['archive_containers'].append(deepcopy(ii['archive_containers'][0]))
   elif name=='container_depth_float':ii['archive_containers'][1]['depth']=1.0
   run(rid,name,'standalone archive utility; inventory not authenticated in this direct call','accepted' if name in ['duplicate_container_declaration','container_depth_float'] else 'rejected',lambda:m.verify_abm_archive(p,rid,arc,ii))
 if rid=='23441617':
  # Neutralize only byte digests of explicitly changed JSON for independent deeper guards.
  # This diagnostic is deliberately outside production custody assumptions.
  for name in ['deep_exact_generic_PASS','deep_exact_prefix_status','deep_missing_root_defect','deep_manuscript_printed_version','deep_public_180_regression']:
   cc,gg=deepcopy(c),deepcopy(g);sc=json.loads(rb(P/g['root_clearance_file']));changed={}
   if name in ['deep_exact_generic_PASS','deep_exact_prefix_status']:
    val='PASS' if name=='deep_exact_generic_PASS' else 'PASS_WITH_NONCENTRAL_BIBLIOGRAPHIC_DEFECT_extra';gg['status']=sc['status']=val;gg['root_clearance_record']['status']=val;cc['review_metadata']['scientific_clearance_status']=val;changed[P/g['root_clearance_file']]=json.dumps(sc).encode()
   elif name=='deep_missing_root_defect':gg['root_clearance_record']['noncentral_bibliographic_defect'].pop('effect');sc['noncentral_bibliographic_defect'].pop('effect');changed[P/g['root_clearance_file']]=json.dumps(sc).encode()
   elif name=='deep_manuscript_printed_version':cc['source_binding']['manuscript_version']='1.0';cc['source_binding']['manuscript_version_printed']=True
   elif name=='deep_public_180_regression':
    for x in cc['background']:
     if 'Heinonen' in x['title']:x['title']=x['title'].replace('181','180')
   changed[p/'publication.json']=json.dumps(cc).encode();changed[p/'promotion.json']=json.dumps(gg).encode()
   Path.read_bytes=lambda q:changed[q] if q in changed else rb(q)
   Path.read_text=lambda q,*a,**k:Path.read_bytes(q).decode(k.get('encoding') or 'utf-8')
   m.digest=lambda q:hashlib.sha256(rb(q)).hexdigest() if q in changed else dg(q)
   try:run(rid,name,'explicit diagnostic with changed-file digests neutralized, no bytes written','rejected',lambda:call(p,cc,gg))
   finally:Path.read_bytes=rb;Path.read_text=rt;m.digest=dg
 if snap!=json.dumps([c,g,raw,api],sort_keys=True):raise RuntimeError('original_arguments_changed')
run('UNSUPPORTED','exclude_outside_exact_IDs','unmodified full consumer','rejected',lambda:call(P/'papers/23441976',{},{}))
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'optimize':sys.flags.optimize,'rows':rows,'all_expectations_met':all(x['expectation_met'] for x in rows),'original_arguments_unchanged':True,'all_changes_in_memory':True,'archive_execution_or_extraction':False}
(E/('SOURCE_PROBES_'+('optimized' if sys.flags.optimize else 'normal')+'.json')).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'runs':len(rows),'all_expectations_met':result['all_expectations_met'],'unexpected':[x for x in rows if not x['expectation_met']],'accepted_utility_diagnostics':[(x['record_id'],x['case']) for x in rows if x['observed']=='accepted' and x['case'] not in ['pristine_full_consumer','pristine_complete_recursive_archive']]}))
