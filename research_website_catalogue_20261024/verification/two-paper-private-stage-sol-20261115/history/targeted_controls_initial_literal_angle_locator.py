"""24 bounded new-two faults, only in-memory copies; no old campaigns."""
from two_common import *
from two_source import load_bundles,view_record
from two_dom import Tree,nodes,text,serialize
from two_contract import check_page
from verify_stage_read_only import check_overlays
import copy,sys
DATE='2026-11-15'
def run_controls():
 bs=load_bundles();root=OWN/'candidate-a/public';pages={};files={};rows=[]
 for b in bs:
  folder=root/'research'/b['slug'];files[b['rid']]={p.name:p.read_bytes() for p in folder.iterdir()};pages[b['rid']]=files[b['rid']]['index.html'];check_page(b,pages[b['rid']],files[b['rid']],DATE)
 index=(root/'research/index.html').read_bytes();sitemap=(root/'research/sitemap.xml').read_bytes();check_overlays(bs,index,sitemap,DATE)
 def rejects(label,call):
  try:call()
  except ValueError as e:rows.append({'fault':label,'literal_outcome':'DELIBERATE_NEW_TARGET_FAULT_REJECTED','rejection':str(e)});return
  raise RuntimeError('ACCEPTED_MUTATION:'+label)
 def pagecase(b,label,changed,assets=None):
  need(changed!=pages[b['rid']] or assets is not None,'nonvacuous_fault:'+label);rejects(label,lambda:check_page(b,changed,files[b['rid']] if assets is None else assets,DATE))
 def nodecase(b,label,n,q):
  before=serialize(n).encode();need(pages[b['rid']].count(before)==1,'unique_actual_fault_node');pagecase(b,label,pages[b['rid']].replace(before,serialize(q).encode(),1))
 for b in bs:
  t=Tree(pages[b['rid']].decode());p=next(p for p in t.find('p') if text(p)==b['abstract']);q=copy.deepcopy(p);q['children']=['Truncated original abstract.'];nodecase(b,b['rid']+':full_original_abstract_truncated',p,q)
 b=bs[0];raw=pages[b['rid']];need(b'O(B+log n)' in raw,'118_explicit_bit_model_locator');pagecase(b,'118:bit_cost_qualification_removed',raw.replace(b'O(B+log n)',b'O(1)',1));pagecase(b,'118:wrong_API_version_in_scholarly_metadata',raw.replace(b'"version": "1.0"',b'"version": "1.0.1"',1));pagecase(b,'118:wrong_native_reader_source',raw.replace(b'<iframe src="weighted_centers.pdf"',b'<iframe src="excerpt.pdf"',1))
 b=bs[1];raw=pages[b['rid']];pagecase(b,'119:missing_second_moment_square',raw.replace('Then M₁² − M₂² >'.encode(),'Then M₁² − M₂ >'.encode(),1));pagecase(b,'119:existing_skip_link_CSS_hides_paragraph',raw.replace(b'<p>For a membrane',b'<p class="skip-link">For a membrane',1));pagecase(b,'119:actual_MIT_scope_erased',raw.replace(b'Software and website code are MIT licensed.',b'Software has no separate license.',1));pagecase(b,'119:creation_date_substituted_for_publication',raw.replace(b'content="2026/09/23"',b'content="2026/09/26"',1));pagecase(b,'119:PDF_download_attribute_removed',raw.replace(b'download="paper.pdf"',b'',1));pagecase(b,'119:wrong_proposed_canonical',raw.replace(b'rel="canonical" href="https://aleckriebel.com/research/strict-dirichlet-gap/"',b'rel="canonical" href="https://example.invalid/"',1))
 for b,name,label in [(bs[1],'SHA256SUMS.txt','119:damaged_original_checksum_file'),(bs[0],bs[0]['zip']['name'],'118:truncated_complete_ZIP'),(bs[1],bs[1]['pdf']['name'],'119:truncated_complete_PDF')]:
  bad=dict(files[b['rid']]);bad[name]=bad[name][:-1];pagecase(b,label,pages[b['rid']],bad)
 for b,tag in [(bs[0],'template'),(bs[1],'noscript')]:pagecase(b,b['rid']+':outer_'+tag+'_hides_article',pages[b['rid']].replace(b'<body>',('<body><'+tag+'>').encode(),1).replace(b'</body>',('</'+tag+'></body>').encode(),1))
 b=bs[1];a1=b['assets'][0]['original_native_asset']['original_api_file_object']['links']['self'].encode();a2=b['assets'][1]['original_native_asset']['original_api_file_object']['links']['self'].encode();raw=pages[b['rid']];pagecase(b,'119:original_native_API_asset_order_swapped',raw.replace(a1,b'TEMP_FIRST',1).replace(a2,a1,1).replace(b'TEMP_FIRST',a2,1))
 f=load(OWN/'SOURCE_INPUTS.json')['records'];bad=copy.deepcopy(f[bs[0]['rid']]);bad['whole_native_transport_aggregate_original']['receipts'].pop(0);rejects('118:first_failed403_transport_erased',lambda:view_record('23385145',bad))
 bad=copy.deepcopy(f[bs[1]['rid']]);bad['whole_native_API_objects_original']['versions_page_001_failed_HTTP400']['whole_original_object']={};rejects('119:failed_versions400_body_erased',lambda:view_record('22983513',bad))
 bad=copy.deepcopy(f['22983513']);bad['whole_native_API_objects_original']['files']['whole_original_object']['entries'][2]['metadata']=None;rejects('119:original_empty_metadata_object_coerced_to_null',lambda:view_record('22983513',bad))
 bad=copy.deepcopy(f['23385145']);bad['whole_scientific_root_authority_original']['whole_literal_peer_verdicts_and_seals'][0]['whole_literal_verdict']={'status':'PASS'};rejects('118:whole_qualified_custom_verdict_coerced_to_generic_PASS',lambda:view_record('23385145',bad))
 rejects('index:old_visible_entry_changed',lambda:check_overlays(bs,index.replace(b'<li>',b'<li>UNAPPROVED ',1),sitemap,DATE));rejects('sitemap:wrong_new_publication_build_date',lambda:check_overlays(bs,index,sitemap.replace(b'<lastmod>2026-11-15</lastmod>',b'<lastmod>2026-11-14</lastmod>',1),DATE));rejects('output:production_folder_fence',lambda:safe_output(PUBLIC))
 return {'literal_custom_status':'TWO_PRISTINE_COMPLETE_CANDIDATES_AND_ALL_BOUNDED_NEW_FAULTS_VALIDATED','optimization':sys.flags.optimize,'pristine_records':2,'pristine_overlay':True,'faults_rejected':len(rows),'results':rows,'network_or_file_writes':False,'science_or_old_campaign_replay':False}
if __name__=='__main__':print(json.dumps(run_controls(),indent=2))
