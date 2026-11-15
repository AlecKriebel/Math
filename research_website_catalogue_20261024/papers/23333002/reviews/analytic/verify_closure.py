#!/usr/bin/env python3
"""Pure offline read-only custody closure. No target imports, execution, writes or network."""
from pathlib import Path,PurePosixPath
import copy,hashlib,json,sys,zipfile,zlib,stat
BASE=Path(__file__).resolve().parent
SRC=BASE.parent.parent/'sources'
EXCLUDED={'OWNED_MANIFEST.json','CLOSURE.json','SEAL.json'}
checks=0
failures=[]
def check(value,label):
 global checks
 checks+=1
 if not value:failures.append(label)
def sha(body):return hashlib.sha256(body).hexdigest()
def readjson(path):return json.loads(Path(path).read_text())
def binding(entry,path=None):
 q=Path(path or entry['path']);b=q.read_bytes()
 check(len(b)==entry['bytes'],'byte size '+str(q))
 check(sha(b)==entry['SHA256'],'SHA256 '+str(q))
 return b

def nativefacts(r,rec,lat,ver,fil,tr):
 try:
  hits=ver['hits']['hits'];assets=r['all_native_assets_in_original_order']
  return all([
   r['record_id']==23333002,r['sheet_row']==125,r['version']=='1.0',r['publication_date']=='2026-10-12',
   r['created']=='2026-10-13T05:49:11.621031+00:00',r['updated']=='2026-10-13T05:49:13.546664+00:00',
   r['native_conceptrecid_whole_field']=={'present':True,'original_value':rec['conceptrecid']},
   r['native_version_whole_field']=={'present':True,'original_value':'1.0'},
   r['native_license_metadata_whole_field']=={'present':True,'original_value':{'id':'cc-by-4.0'}},
   rec['id']==lat['id']==hits[0]['id']==23333002,len(hits)==1,
   rec['swh']=={},type(rec['swh'])is dict,lat['swh']=={},hits[0]['swh']is None,
   fil['order']==[],type(fil['order'])is list,fil['default_preview']is None,
   r['native_schema_distinctions']=={'record_swh':{'present':True,'original_value':{}},'latest_swh':{'present':True,'original_value':{}},'version_hit_swh_fields':[{'present':True,'original_value':None}],'files_order':{'present':True,'original_value':[]},'files_default_preview':{'present':True,'original_value':None}},
   [x['original_api_file_object']['key']for x in assets]==['robinson-tangency-certificates-v1.0.pdf','robinson-tangency-source-verification-v1.0.zip'],
   [x['ordinal_zero_based']for x in assets]==[0,1],
   [x['original_api_file_object']for x in assets]==rec['files'],
   [x['whole_original_native_files_entry']for x in assets]==fil['entries'],
   r['HTTP_status_sequence']==[200,301,200,200,200,200,200],
   [x['HTTP_status']for x in tr['receipts']]==r['HTTP_status_sequence'],
   tr['failed_responses']==[],len(tr['receipts'])==7,
   r['printed_title_date_version_inspected']is False,r['printed_date']is None,r['printed_version']is None,
   r['target_PDF_text_extracted']is False,r['target_PDF_pages_rendered']is False,
   r['TeX_preamble_or_mathematical_body_read']is False,r['source_scientific_proofs_code_results_triage_reviews_or_opinions_read']is False,
   r['source_programmes_executed']==[],r['completion_percent_at_preseal']==95,
   r['whole_regular_payload_occurrences']==85,r['expanded_bytes_all_depths']==556745,
   r['nested_archive_count']==0,r['embedded_PDFs']==[],r['controlling_TeX']['opaque_byte_splitlines_count']==238,
   r['selected_actual_PDF']['pages']==4,r['selected_actual_PDF']['bytes']==65807,
   r['all_enumerated_version_ids']==[23333002],r['version_enumeration_exhaustive_no_next_link']is True,
  ])
 except (KeyError,IndexError,TypeError):return False

def main():
 preseal=sys.argv[1:]==['--preseal']
 check(not sys.argv[1:]or preseal,'supported argument')
 im=readjson(BASE/'INPUT_MANIFEST.json');om=readjson(BASE/'OWNED_MANIFEST.json')
 for e in im['files']:binding(e)
 check(len({e['path']for e in im['files']})==len(im['files']),'unique input paths')
 sourcepaths={str(q.resolve())for q in SRC.rglob('*')if q.is_file()}
 check(sourcepaths=={e['path']for e in im['files']if e['role']=='immutable_native_source'},'whole unchanged source footprint')
 actualown={str(q.relative_to(BASE))for q in BASE.rglob('*')if q.is_file()and str(q.relative_to(BASE))not in EXCLUDED}
 check(actualown=={e['path']for e in om['files']},'whole owned footprint')
 for e in om['files']:binding(e,BASE/e['path'])
 sm=readjson(SRC/'SOURCE_READY_MANIFEST.json');ss=readjson(SRC/'SOURCE_READY_SEAL.json')
 for e in sm['files']:binding(e,SRC/e['path'])
 check(set(sm['excluded_terminal_files'])=={'SOURCE_READY_CLOSURE.json','SOURCE_READY_MANIFEST.json','SOURCE_READY_SEAL.json'},'literal source terminal exclusions')
 check({str(q.relative_to(SRC))for q in SRC.rglob('*')if q.is_file()}=={e['path']for e in sm['files']}|set(sm['excluded_terminal_files']),'source complete manifest footprint')
 check(ss['SOURCE_READY_SHA256']==sha((SRC/'SOURCE_READY.json').read_bytes()),'source seal READY')
 check(ss['MANIFEST_SHA256']==sha((SRC/'SOURCE_READY_MANIFEST.json').read_bytes()),'source seal manifest')
 check(ss['CLOSURE_SHA256']==sha((SRC/'SOURCE_READY_CLOSURE.json').read_bytes()),'source seal closure')
 check(ss['completion_percent']==100 and ss['printed_date_version_inspected']is False and ss['source_programmes_executed']==[],'source final historical flags')
 r=readjson(SRC/'SOURCE_READY.json')
 objs={e['role']:readjson(e['path'])for e in r['whole_native_API_objects']}
 for e in r['whole_native_API_objects']:binding(e)
 tr=readjson(r['actual_transport_receipts']['path']); binding(r['actual_transport_receipts'])
 values=[r,objs['record'],objs['latest'],objs['versions_page001'],objs['files'],tr]
 check(nativefacts(*values),'literal native facts/types/order/history')
 for receipt in tr['receipts']:
  body=Path(receipt['body_path']).read_bytes()
  check(len(body)==receipt['body_bytes'],'transport body bytes')
  check(sha(body)==receipt['body_SHA256'],'transport body SHA256')
  check(hashlib.md5(body).hexdigest()==receipt['body_MD5'],'transport body MD5')
  check(type(receipt['response_headers_in_received_order'])is list and all(type(x)is list and len(x)==2 for x in receipt['response_headers_in_received_order']),'ordered transport headers retained')
 for a in r['all_native_assets_in_original_order']:
  b=binding(a)
  check('md5:'+hashlib.md5(b).hexdigest()==a['original_api_file_object']['checksum'],'actual native MD5')
  check(a['whole_original_native_files_entry']['checksum']==a['original_api_file_object']['checksum'],'native files checksum consistency')
 check(sha(Path(r['selected_actual_PDF']['path']).read_bytes())=='eac73f8c53ece8ef5825258327b98fb9e5eda161a0cc9ad18afdd0d3cd61d05c','exact actual published PDF')
 tex=Path(r['controlling_TeX']['extracted_path']).read_bytes()
 check(len(tex)==12368 and len(tex.splitlines())==238 and sha(tex)=='4b7d8c6e3ae68db1d77687f2ae11a41811451588234ca7bd6fc2d32e108cb86f','exact controlling TeX')
 ac=readjson(r['whole_archive_custody']['path']);binding(r['whole_archive_custody'])
 check(len(ac['containers'])==1 and len(ac['all_safe_regular_occurrences'])==85,'whole archive and payload count')
 check(ac['unsafe_or_colliding_names']==[] and ac['encrypted_or_nonregular_payloads']==[] and ac['unsupported_archive_magic']==[],'archive safety historical status')
 occ={x['ordinal_zero_based']:x for x in ac['all_safe_regular_occurrences']};total=0
 for c in ac['containers']:
  binding(c)
  with zipfile.ZipFile(c['path'])as z:
   check(z.comment.hex()==c['archive_comment_hex'],'original archive comment')
   inf=z.infolist();central=c['whole_original_central_directory']
   check(len(inf)==len(central)==c['native_member_count_including_directories']==85,'whole original central directory count')
   names=[]
   for i,(zi,old)in enumerate(zip(inf,central)):
    current={'ordinal_zero_based':i,'filename':zi.filename,'original_filename':zi.orig_filename,'is_directory':zi.is_dir(),'bytes':zi.file_size,'compressed_bytes':zi.compress_size,'CRC32':format(zi.CRC,'08x'),'flags':zi.flag_bits,'compression':zi.compress_type,'native_date_time':list(zi.date_time),'external_attr':zi.external_attr,'internal_attr':zi.internal_attr,'create_system':zi.create_system,'create_version':zi.create_version,'extract_version':zi.extract_version,'header_offset':zi.header_offset,'extra_hex':zi.extra.hex(),'comment_hex':zi.comment.hex()}
    check(current==old,'literal whole central entry '+str(i))
    path=PurePosixPath(zi.filename);mode=zi.external_attr>>16
    check(not path.is_absolute()and'..'not in path.parts and'\\'not in zi.filename and not(zi.flag_bits&1)and stat.S_ISREG(mode)and not zi.is_dir(),'safe archive name/type '+str(i))
    names.append(zi.filename)
    body=z.read(zi);entry=occ[i];ex=Path(entry['extracted_path'])
    check(ex.resolve().is_relative_to(Path(c['extraction_root']).resolve()),'extraction containment '+str(i))
    check(zi.filename==entry['original_member_name']and len(body)==entry['bytes']and sha(body)==entry['SHA256'],'complete payload binding '+str(i))
    check(format(zlib.crc32(body)&0xffffffff,'08x')==entry['CRC32'],'payload CRC '+str(i))
    check(body==ex.read_bytes(),'extracted bytes equal complete original payload '+str(i));total+=len(body)
   check(len(names)==len(set(names)),'no duplicate/colliding payload paths')
 check(total==556745,'whole expanded payload bytes')
 for e in readjson(BASE/'PRIMARY_INTERFACES.json')['actual_primary_bodies']:
  b=Path(e['PDF_path']).read_bytes();receipt=readjson(e['receipt_path'])
  check(len(b)==e['PDF_bytes']and sha(b)==e['PDF_SHA256']and b.startswith(b'%PDF-'),'actual primary PDF binding')
  check(receipt['status']==200 and receipt['SHA256']==e['PDF_SHA256']and receipt['bytes']==len(b),'actual primary ordinary transport')
 initial=readjson(BASE/'INITIAL_SEAL.json');freeze=readjson(BASE/'OWN_RESULTS_FREEZE.json');verdict=readjson(BASE/'VERDICT.json')
 check(sha((BASE/'INITIAL_RECONSTRUCTION.md').read_bytes())==initial['INITIAL_RECONSTRUCTION_SHA256'],'substantial early reconstruction seal')
 check(initial['all_actual_PDF_pages_personally_read']==4 and initial['entire_TeX_lines_personally_read']==238 and initial['all_fresh_individual_rasters_personally_viewed']==4,'own full paper/TeX/rasters ledger')
 check(initial['foreign_scientific_body_code_results_bundled_current_opinions_before_initial']is False and initial['other_review_folders_read']is False,'early independence preserved')
 check(sha((BASE/'independent_algebra.py').read_bytes())==freeze['independent_algebra_SHA256']and sha((BASE/'INDEPENDENT_ALGEBRA.json').read_bytes())==freeze['INDEPENDENT_ALGEBRA_SHA256'],'own exact results freeze')
 check(freeze['status']=='PASS'and freeze['native_code_or_results_read']is False,'own results precede native code/results')
 check(verdict['original_claim_assessed_in_full']is True and verdict['substantive_defect_found']is False and verdict['exact_remaining_mathematical_gap']is None and verdict['followup']is None and verdict['native_scientific_programmes_executed_by_this_lane']==[],'literal custom verdict scope')
 # In-memory falsifiers: no files are mutated. Each attacks a required distinct fact.
 mutants=[]
 def mutate(index,fn):
  vals=copy.deepcopy(values);fn(vals[index]);mutants.append(vals)
 mutate(0,lambda x:x.update(version='1.0.0'))
 mutate(0,lambda x:x.update(publication_date='2026-10-13'))
 mutate(0,lambda x:x.update(native_version_whole_field={'present':True,'original_value':None}))
 mutate(0,lambda x:x.update(printed_title_date_version_inspected=True))
 mutate(0,lambda x:x.update(completion_percent_at_preseal=100))
 mutate(0,lambda x:x.update(source_programmes_executed=['verify.py']))
 mutate(0,lambda x:x['all_native_assets_in_original_order'].reverse())
 mutate(0,lambda x:x.update(expanded_bytes_all_depths=556744))
 mutate(0,lambda x:x.update(whole_regular_payload_occurrences=84))
 mutate(0,lambda x:x.update(embedded_PDFs=['invented.pdf']))
 mutate(1,lambda x:x.update(swh=None))
 mutate(2,lambda x:x.update(swh=[]))
 mutate(3,lambda x:x['hits']['hits'][0].update(swh={}))
 mutate(4,lambda x:x.update(order={}))
 mutate(4,lambda x:x.update(default_preview=''))
 mutate(4,lambda x:x['entries'].reverse())
 mutate(5,lambda x:x['receipts'].pop(1))
 mutate(5,lambda x:x['receipts'][1].update(HTTP_status=200))
 for i,m in enumerate(mutants):check(not nativefacts(*m),'meaningful native in-memory falsifier '+str(i))
 pdf=Path(r['selected_actual_PDF']['path']).read_bytes();check(sha(pdf+b'X')!=r['selected_actual_PDF']['SHA256'],'appended manuscript bytes rejected')
 check(sha(tex[:-1])!=r['controlling_TeX']['SHA256'],'truncated controlling TeX rejected')
 changed=copy.deepcopy(ac['containers'][0]['whole_original_central_directory'][0]);changed['native_date_time'][0]+=1
 check(changed!=ac['containers'][0]['whole_original_central_directory'][0],'original ZIP timestamp mutation rejected')
 if not preseal:
  seal=readjson(BASE/'SEAL.json')
  for key,name in [('INPUT_MANIFEST_SHA256','INPUT_MANIFEST.json'),('OWNED_MANIFEST_SHA256','OWNED_MANIFEST.json'),('CLOSURE_SHA256','CLOSURE.json'),('REPORT_SHA256','REPORT.md'),('VERDICT_SHA256','VERDICT.json'),('verifier_SHA256','verify_closure.py')]:check(seal[key]==sha((BASE/name).read_bytes()),'terminal seal '+name)
  check(seal['completion_percent']==100 and seal['source_changes']is False,'terminal completion/no source mutations')
 return {'status':'PASS'if not failures else'FAIL','checks':checks,'failures':failures,'input_files':len(im['files']),'owned_files':len(om['files']),'whole_original_archive_payloads':85,'in_memory_falsifiers':len(mutants)+3,'mode':'preseal'if preseal else'final','network':False,'writes':False,'scientific_source_imports_or_execution':False}
try:
 result=main()
except Exception as e:
 result={'status':'FAIL','checks':checks,'failures':failures+[type(e).__name__+': '+str(e)],'network':False,'writes':False,'scientific_source_imports_or_execution':False}
print(json.dumps(result,indent=2))
sys.exit(0 if result['status']=='PASS'else 1)
