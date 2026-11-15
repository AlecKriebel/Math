"""Local immutable source/rights binding only; no acquisition or native code run."""
from pathlib import Path
from hashlib import sha256,md5
from datetime import datetime,timezone
import json,shutil,zipfile
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024');Q=P/'papers/23439582';E=Q/'reviews/editorial';S=Q/'source-resume-20261115';OLD=Q/'sources'
def load(p):
 def pairs(xs):
  d={}
  for k,v in xs:
   assert k not in d,'duplicate JSON key';d[k]=v
  return d
 return json.loads(Path(p).read_text(),object_pairs_hook=pairs)
def h(p):return sha256(Path(p).read_bytes()).hexdigest()
def typed(v):
 if isinstance(v,dict):return('dict',tuple((k,typed(x))for k,x in v.items()))
 if isinstance(v,list):return('list',tuple(typed(x)for x in v))
 return(type(v).__name__,v)
def binding(p,role=None):
 p=Path(p);b=p.read_bytes();r={'path':str(p),'bytes':len(b),'SHA256':sha256(b).hexdigest(),'whole_literal_object':load(p)}
 if role:r['role']=role
 return r
def textbinding(p):
 p=Path(p);return{'path':str(p),'bytes':p.stat().st_size,'SHA256':h(p),'whole_literal_text':p.read_text()}
def dump(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
ready=load(S/'SOURCE_READY.json');rootpath=P/'verification/root-clearance-23439582-20261115.json';root=load(rootpath);aggregate=load(Path(ready['actual_transport_receipts']['path']));new=aggregate['new_resumption_receipts_in_chronological_order'];old=aggregate['prior_sealed_failed_transport_receipts_unchanged'];assert len(new)==6 and len(old)==3
candidates=[]
for p in S.rglob('*.json'):
 if p.is_relative_to(S/'published-source'):continue
 try:candidates.append((p,load(p)))
 except (json.JSONDecodeError,UnicodeDecodeError):pass
trans=[]
for i,x in enumerate(new):
 matches=[p for p,v in candidates if typed(v)==typed(x)];assert len(matches)==1,(i,matches)
 trans.append(binding(matches[0],'actual_new_HTTP_exchange_'+str(i+1)))
oldtrans=[];bodies=[]
for x in old:
 p=Path(x['receipt_identity']['path']);assert h(p)==x['receipt_identity']['SHA256'];v=binding(p,'historical_403');assert typed(v['whole_literal_object'])==typed(x['whole_literal_original_receipt']);oldtrans.append(v);bodies.append(Path(v['whole_literal_object']['body_path']))
api=[{**binding(x['path'],x['role']),'whole_source_ready_reference':x}for x in ready['whole_native_API_objects']];record=api[0]['whole_literal_object'];assets=ready['all_native_assets_in_original_order'];assert typed(record['files'])==typed([a['original_api_file_object']for a in assets]);assert record['metadata']['license']=={'id':'cc-by-4.0'}
for a in assets:
 p=Path(a['path']);data=p.read_bytes();assert len(data)==a['bytes']==a['original_api_file_object']['size'];assert sha256(data).hexdigest()==a['SHA256'];assert md5(data).hexdigest()==a['MD5'];assert 'md5:'+md5(data).hexdigest()==a['original_api_file_object']['checksum']
zipasset=assets[0];pdf=assets[1];assert zipasset['acquisition_mechanism']=='authenticated_existing_cache_exact_native_MD5_and_size'and zipasset['native_GET_claimed']is False;assert ready['cached_ZIP_native_GET_claimed']is False
assert not any(x['whole_literal_object']['requested_url']==zipasset['original_api_file_object']['links']['self']for x in trans)
cache=binding(S/'CACHE_ASSOCIATION.json');cachebody=cache['whole_literal_object'];origin=Path(cachebody['candidate_original_path']);assert origin.read_bytes()==Path(zipasset['path']).read_bytes();assert cachebody['exact_native_MD5_size_match_before_copy_or_extraction']is True and cachebody['native_GET_of_cached_ZIP_claimed']is False
members=[]
with zipfile.ZipFile(zipasset['path'])as z:
 assert len(z.infolist())==20 and z.testzip()is None
 for i,info in enumerate(z.infolist()):
  assert not info.is_dir();assert not Path(info.filename).is_absolute()and '..'not in Path(info.filename).parts
  p=S/'published-source'/info.filename;data=z.read(info);assert p.read_bytes()==data
  members.append({'ordinal_zero_based':i,'original_member_name':info.filename,'path':str(p),'bytes':len(data),'SHA256':sha256(data).hexdigest(),'CRC32':format(info.CRC,'08x'),'compressed_bytes':info.compress_size,'compression_method':info.compress_type,'native_external_attr':info.external_attr,'native_internal_attr':info.internal_attr,'flags':info.flag_bits,'native_date_time':list(info.date_time),'native_extra_hex':info.extra.hex(),'native_comment_hex':info.comment.hex()})
embedded=ready['all_embedded_PDFs'];assert len(embedded)==1 and Path(embedded[0]['path']).read_bytes()==Path(pdf['path']).read_bytes()
verdicts=[];seals=[];derivations=[]
for row in root['independent_review_packets']:
 v=binding(P/row['verdict_path'],row['lane']);assert v['SHA256']==row['verdict_sha256']and typed(v['whole_literal_object'])==typed(row['whole_literal_custom_verdict']);verdicts.append(v)
 seals.append(binding(P/row['seal']['path'],row['lane']))
 for p in sorted((Q/'reviews'/row['lane']).glob('DERIVATION*.md')):derivations.append(textbinding(p))
for p in sorted((Q/'reviews/root').glob('INITIAL_RECONSTRUCTION*.md')):derivations.append(textbinding(p))
assert len(verdicts)==2
terminal=[binding(S/n)for n in ['SOURCE_READY_SEAL.json','SOURCE_READY_MANIFEST.json','SOURCE_READY_CLOSURE.json','INPUT_MANIFEST.json','PRESEAL_VALIDATION_HISTORY.json','ASSET_IDENTITIES.json','START.json']]
history=[binding(OLD/n)for n in ['ACQUISITION_INCOMPLETE_SEAL.json','ACQUISITION_INCOMPLETE_MANIFEST.json','ACQUISITION_INCOMPLETE_CLOSURE.json','ACQUISITION_STATUS.json','CACHE_CANDIDATE.json']]+[binding(S/'PRIOR_SOURCE_BASELINE.json')]
license_doc=textbinding(S/'published-source/LICENSE.txt');readme=textbinding(S/'published-source/README.md');assert 'materials and code'in license_doc['whole_literal_text']and 'CC BY 4.0'in license_doc['whole_literal_text']
now=datetime.now(timezone.utc).isoformat();proto={'UTC':now,'role':'Same informed editorial lane metadata/custody binding, not an independent extra review.','current_SOURCE_READY':binding(S/'SOURCE_READY.json'),'root_authority':binding(rootpath),'source_terminal_objects':terminal,'older_incomplete_history_objects':history,'changed_access_authorization_whole':ready['changed_access_authorization'],'native_API_objects':api,'actual_transport_aggregate':binding(S/'ALL_TRANSPORT_RECEIPTS.json'),'six_actual_new_transport_objects':trans,'three_actual_old_403_transport_objects':oldtrans,'cache_association':cache,'authenticated_cached_ZIP_original':{'path':str(origin),'bytes':origin.stat().st_size,'SHA256':h(origin),'MD5':md5(origin.read_bytes()).hexdigest(),'native_GET_claimed':False},'native_assets_in_original_order':assets,'whole_archive_custody':binding(Path(ready['whole_archive_custody']['path'])),'all20_original_member_checks':members,'embedded_PDFs_whole_original':embedded,'native_schema_types':binding(Path(ready['native_schema_types']['path'])),'printed_identity':binding(Path(ready['printed_identity']['path'])),'actual_license_and_requirements':[license_doc,readme],'whole_two_original_scientific_custom_verdicts':verdicts,'scientific_review_seals':seals,'whole_bound_scientific_derivations':derivations,'source_reports_preserved':[textbinding(S/'SOURCE_READY_REPORT.md'),textbinding(OLD/'ACQUISITION_INCOMPLETE_REPORT.md')],'literal_ready_completion':ready['completion_percent'],'literal_final_source_completion':load(S/'SOURCE_READY_SEAL.json')['completion_percent'],'historical_unread_pending_and_old_failure_fields_preserved_literally':True,'current_manuscript_unavailability_inferred_from_old403':False,'fresh_ZIP_GET_invented':False,'network_scientific_native_or_legacy_code_run':False,'publication_or_native_AA_authority':False}
# Raw copies of all exact metadata/verdict/transport bodies, not transformed JSON.
rawpaths={rootpath,S/'SOURCE_READY.json'}
for key in ['current_SOURCE_READY','root_authority','actual_transport_aggregate','cache_association','whole_archive_custody','native_schema_types','printed_identity']:rawpaths.add(Path(proto[key]['path']))
for key in ['source_terminal_objects','older_incomplete_history_objects','native_API_objects','six_actual_new_transport_objects','three_actual_old_403_transport_objects','whole_two_original_scientific_custom_verdicts','scientific_review_seals']:
 for x in proto[key]:rawpaths.add(Path(x['path']))
for x in trans:
 v=x['whole_literal_object']
 if 'body_path'in v:rawpaths.add(Path(v['body_path']))
rawpaths.update(bodies);copies=[]
for p in sorted(rawpaths):
 dest=E/'inputs/raw-native'/p.relative_to(P);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest);copies.append({'original_path':str(p),'copy_relative_to_editorial':str(dest.relative_to(E)),'bytes':p.stat().st_size,'SHA256':h(p)})
proto['raw_byte_copies']=copies;dump(E/'SOURCE_PROTOCOL_BINDINGS.json',proto)
rights={'UTC':now,'record_id':23439582,'title':ready['title'],'DOI':ready['DOI'],'printed_version':'1.0.0','native_version':'1.0.0','declared_and_printed_date':'2026-10-17','actual_native_created':ready['created'],'actual_native_updated':ready['updated'],'date_fields_preserved_separately':True,'native_license_object':record['metadata']['license'],'paper_source_authored_verification_and_code_license':'CC BY 4.0','explicit_code_license':'CC BY 4.0','actual_LICENSE':license_doc,'actual_README':readme,'MIT_default_invented':False,'requirements':'Python3.10 or later; standard library convention tests require assertions, optimized Python -O explicitly rejected. No programme replay in this editorial task. Rebuild instructions are preserved but no PDF rebuild performed.','whole_native_assets_in_original_order':assets,'actual_pdf_pages':4,'complete_original_ZIP_members':20,'embedded_PDF_identical_to_native_reader':True,'native_ZIP_GET_claimed':False,'new_transport_count':6,'old_403_history_count':3,'SOURCE_READY95_and_finalsource100_preserved':True,'actual_scientific_review_cardinality':2,'publication_or_native_AA_authority':False};dump(E/'RIGHTS_AND_IDENTITY.json',rights)
print(json.dumps({'actual_new_transport_files':[x['path']for x in trans],'actual_old403_files':[x['path']for x in oldtrans],'raw_byte_copies':len(copies),'complete_original_members':len(members),'scientific_derivations_bound':len(derivations),'rights':'CC BY4.0 explicitly includes authored code; noMIT','SOURCE_PROTOCOL_BINDINGS_SHA256':h(E/'SOURCE_PROTOCOL_BINDINGS.json'),'RIGHTS_AND_IDENTITY_SHA256':h(E/'RIGHTS_AND_IDENTITY.json')},indent=2))
