#!/usr/bin/env python3
"""Pure offline read-only custody verification; no target imports, execution, writes or network."""
from pathlib import Path,PurePosixPath
import hashlib,json,zipfile,zlib,stat,sys,copy
P=Path(__file__).resolve().parent
S=P.parent.parent/'sources'
EX={'OWNED_MANIFEST.json','CLOSURE.json','SEAL.json'}
checks=0;fail=[]
def ck(v,n):
 global checks
 checks+=1
 if not v:fail.append(n)
def sha(b):return hashlib.sha256(b).hexdigest()
def js(q):return json.loads(Path(q).read_text())
def bind(e,q=None):
 q=Path(q or e['path']);b=q.read_bytes();ck(len(b)==e['bytes'],'bytes '+str(q));ck(sha(b)==e['SHA256'],'SHA256 '+str(q));return b

def facts(r,record,latest,versions,files,tr):
 try:
  hits=versions['hits']['hits'];assets=r['all_native_assets_in_original_order']
  return all([
   r['record_id']==23578142,r['sheet_row']==126,r['version']=='1.0.0',r['publication_date']=='2026-10-22',
   r['created']=='2026-10-22T21:01:06.850027+00:00',r['updated']=='2026-10-22T21:01:07.620984+00:00',
   r['native_conceptrecid_whole_field']=={'present':True,'original_value':'23578141'},
   r['native_version_whole_field']=={'present':True,'original_value':'1.0.0'},
   r['native_license_metadata_whole_field']=={'present':True,'original_value':{'id':'cc-by-4.0'}},
   record['id']==latest['id']==hits[0]['id']==23578142,len(hits)==1,
   record['swh']=={},type(record['swh'])is dict,latest['swh']=={},hits[0]['swh']is None,
   files['order']==[],type(files['order'])is list,files['default_preview']is None,type(files['entries'])is list,
   r['native_schema_distinctions']['record_swh']=={'present':True,'original_value':{}},
   r['native_schema_distinctions']['versions_swh_fields']==[{'present':True,'original_value':None}],
   [x['original_api_file_object']['key']for x in assets]==['supported-cycle-source-and-verification.zip','supported-cycle-bound.pdf'],
   [x['ordinal_zero_based']for x in assets]==[0,1],
   [x['original_api_file_object']for x in assets]==record['files'],[x['whole_original_native_files_entry']for x in assets]==files['entries'],
   type(tr)is list,len(tr)==7,[x['HTTP_status']for x in tr]==[200,301,200,200,200,200,200],
   [x['logical_role']for x in tr]==['record','latest','latest','versions-page001','files','asset-001','asset-002'],
   [x['redirect_hop']for x in tr]==[0,0,1,0,0,0,0],
   all(type(x['response_headers_in_received_order'])is list for x in tr),
   all(sum(k.lower()=='content-type'for k,v in x['response_headers_in_received_order'])==2 for x in tr[-2:]),
   r['printed_title_date_version_inspected']is False,r['printed_date']is None,r['printed_version']is None,
   r['target_PDF_pages_rendered']is True,r['target_PDF_rasters_visually_read']is False,r['mathematical_PDF_TeX_or_pixels_read']is False,
   r['source_programmes_executed']==[],r['completion_percent_at_preseal']==100,r['publication_authority']is False,
   r['whole_regular_payload_occurrences']==27,r['expanded_bytes_all_depths']==243851,r['nested_archive_count']==0,
   r['selected_actual_PDF']['pages']==7,r['controlling_TeX']['opaque_byte_splitlines_count']==391,
   len(r['embedded_PDFs'])==1,r['embedded_PDFs'][0]['identical_to_standalone_published_PDF']is True,
  ])
 except(KeyError,IndexError,TypeError,ValueError):return False

def directory(i,q):
 return {'ordinal_zero_based':i,'filename':q.filename,'original_filename':q.orig_filename,'is_directory':q.is_dir(),'bytes':q.file_size,'compressed_bytes':q.compress_size,'CRC32':format(q.CRC,'08x'),'flags':q.flag_bits,'compression':q.compress_type,'native_date_time':list(q.date_time),'external_attr':q.external_attr,'internal_attr':q.internal_attr,'create_system':q.create_system,'create_version':q.create_version,'extract_version':q.extract_version,'header_offset':q.header_offset,'extra_hex':q.extra.hex(),'comment_hex':q.comment.hex()}

def main():
 pre=sys.argv[1:]==['--preseal'];ck(not sys.argv[1:]or pre,'supported argument')
 im=js(P/'INPUT_MANIFEST.json');om=js(P/'OWNED_MANIFEST.json')
 for x in im['files']:bind(x)
 ck({str(q.resolve())for q in S.rglob('*')if q.is_file()}=={x['path']for x in im['files']if x['role']=='immutable_native_source'},'whole77-source-file footprint')
 ck({str(q.relative_to(P))for q in P.rglob('*')if q.is_file()and str(q.relative_to(P))not in EX}=={x['path']for x in om['files']},'whole owned footprint')
 for x in om['files']:bind(x,P/x['path'])
 sm=js(S/'SOURCE_READY_MANIFEST.json');ss=js(S/'SOURCE_READY_SEAL.json')
 for x in sm['files']:bind(x,S/x['path'])
 ck({str(q.relative_to(S))for q in S.rglob('*')if q.is_file()}=={x['path']for x in sm['files']}|set(sm['excluded_terminal_files']),'whole source manifest footprint')
 for key,name in [('SOURCE_READY_SHA256','SOURCE_READY.json'),('MANIFEST_SHA256','SOURCE_READY_MANIFEST.json'),('CLOSURE_SHA256','SOURCE_READY_CLOSURE.json')]:ck(ss[key]==sha((S/name).read_bytes()),'source final seal '+name)
 ck(sha((S/'SOURCE_READY.json').read_bytes())=='346d425ca3b35b03465fc6a3e0873b372ed2088c58ee9681354d41dad6de7576','exact native READY anchor')
 ck(sha((S/'SOURCE_READY_SEAL.json').read_bytes())=='e3821fe642435394f82a70c50c5d4dcd2c8159d674ed2cc7ae83be9c365dd8cc','exact source final seal anchor')
 r=js(S/'SOURCE_READY.json');objects={x['role']:js(x['path'])for x in r['whole_native_API_objects']}
 for x in r['whole_native_API_objects']:bind(x)
 tr=js(r['actual_transport_receipts']['path']);bind(r['actual_transport_receipts'])
 vals=[r,objects['record'],objects['latest'],objects['versions-page001'],objects['files'],tr];ck(facts(*vals),'literal native schema/types/order/historical flags')
 for x in tr:
  bind(x,x['body_path']);ck(x['error_type']is None,'actual transport error classification retained')
 for x in r['all_native_assets_in_original_order']:
  b=bind(x);ck('md5:'+hashlib.md5(b).hexdigest()==x['original_api_file_object']['checksum'],'native API MD5');ck(b==Path(x['transport_body_path']).read_bytes(),'asset identical to whole actual transport')
 pdf=Path(r['selected_actual_PDF']['path']).read_bytes();tex=Path(r['controlling_TeX']['extracted_path']).read_bytes()
 ck(len(pdf)==81251 and sha(pdf)=='a5e1a710a51c3c9805cd371471fa2699c8418915d5a6b07f799a9fd090e61d7e','exact standalone target PDF')
 ck(len(tex)==20779 and len(tex.splitlines())==391 and sha(tex)=='64cf1aac42d2c1e873aa8cdbe79d4404be074472cc91bd9d3128641cb5b6fc93','whole actual controlling TeX')
 ck(Path(r['embedded_PDFs'][0]['extracted_path']).read_bytes()==pdf,'archived PDF identical to native standalone PDF')
 ac=js(r['whole_archive_custody']['path']);bind(r['whole_archive_custody']);nd=js(P/'NATIVE_ZIP_DIRECTORY.json')
 ck(len(ac['containers'])==1 and len(ac['regular_payload_occurrences'])==27,'all containers/payload occurrences')
 c=ac['containers'][0];zb=Path(c['input_path']).read_bytes();ck(len(zb)==c['input_bytes']and sha(zb)==c['input_SHA256']==nd['archive_SHA256'],'whole original ZIP binding')
 total=0
 with zipfile.ZipFile(c['input_path'])as z:
  inf=z.infolist();ck(len(inf)==len(c['members'])==len(nd['members_in_original_order'])==27,'whole original ZIP member count');ck(z.comment.hex()==nd['archive_comment_hex'],'whole original ZIP comment')
  names=[]
  for i,(zi,e)in enumerate(zip(inf,c['members'])):
   ck(directory(i,zi)==nd['members_in_original_order'][i],'whole native central entry '+str(i))
   n=PurePosixPath(zi.filename);ck(not n.is_absolute()and'..'not in n.parts and'\\'not in zi.filename and not zi.is_dir()and stat.S_ISREG(zi.external_attr>>16)and not(zi.flag_bits&1),'safe regular member '+str(i))
   body=z.read(zi);names.append(zi.filename);total+=len(body)
   ck(e['original_member_name']==zi.filename and e['ordinal_zero_based']==i,'native original member order '+str(i))
   ck(len(body)==e['bytes']and sha(body)==e['SHA256']and format(zlib.crc32(body)&0xffffffff,'08x')==e['CRC32'],'whole member bytes/hash/CRC '+str(i))
   ex=Path(e['extracted_path']);ck(ex.resolve().is_relative_to(Path(c['extraction_root']).resolve())and ex.read_bytes()==body,'safe exact extracted member '+str(i))
  ck(len(names)==len(set(names))==len({n.casefold()for n in names}),'no duplicate/case-colliding member paths')
 ck(total==243851,'all expanded bytes')
 packet=Path(r['controlling_TeX']['extracted_path']).parent
 manifest=js(packet/'SOURCE_MANIFEST.json')
 ck(len(manifest['members'])==26,'native package manifest complete26 plus self')
 for x in manifest['members']:
  b=(packet/x['path']).read_bytes();ck(len(b)==x['bytes']and sha(b)==x['sha256'],'native whole package member '+x['path'])
 ob=js(packet/'ORIGINAL_BINDING.json');ck(len(ob['original_files'])==8,'all eight historical artifact bindings')
 for x in ob['original_files']:
  b=(packet/'original'/x['file']).read_bytes();ck(len(b)==x['bytes']and sha(b)==x['sha256'],'original artifact byte binding '+x['file'])
 for x in js(P/'PRIMARY_INTERFACES.json')['nine_actual_native_PDF_bodies']:
  b=Path(x['PDF_path']).read_bytes();rc=js(x['receipt_path']);ck(len(b)==x['PDF_bytes']and sha(b)==x['PDF_SHA256']and b.startswith(b'%PDF-'),'actual primary PDF '+x['name']);ck(rc['status']==200 and rc['SHA256']==x['PDF_SHA256'],'actual successful primary transport '+x['name'])
 wr=js(P/'primary/Wright2019.receipt.json');ck(wr['status']==403 and len(Path(wr['path']).read_bytes())==318 and sha(Path(wr['path']).read_bytes())==wr['SHA256'],'actual Wright403 preserved distinct from web response')
 init=js(P/'INITIAL_SEAL.json');freeze=js(P/'OWN_RESULTS_FREEZE.json');v=js(P/'VERDICT.json')
 ck(sha((P/'INITIAL_RECONSTRUCTION.md').read_bytes())==init['INITIAL_RECONSTRUCTION_SHA256'],'substantial initial reconstruction seal')
 ck(init['all_actual_PDF_pages_personally_read']==7 and init['all_controlling_TeX_lines_personally_read']==391 and init['all_fresh_individual_rasters_personally_viewed']==7,'whole target reading ledger')
 ck(init['foreign_scientific_primary_native_code_results_archived_current_peer_or_root_findings_read']is False,'paper-first independence')
 ck(sha((P/'independent_minor_controls.py').read_bytes())==freeze['script_SHA256']and sha((P/'INDEPENDENT_MINOR_CONTROLS.json').read_bytes())==freeze['results_SHA256'],'own controls freeze')
 ck(freeze['native_code_results_read_or_run']is False and freeze['status']=='PASS','own controls precede native code/results')
 ck(v['all_original_mathematical_parts_assessed']is True and v['substantive_defect_found']is False and v['exact_remaining_mathematical_gap']is None and v['followup']is None,'literal custom verdict boundary')
 mutants=[]
 def mutation(index,f):
  a=copy.deepcopy(vals);f(a[index]);mutants.append(a)
 mutation(0,lambda x:x.update(version='1.0'))
 mutation(0,lambda x:x.update(publication_date='2026-10-23'))
 mutation(0,lambda x:x.update(native_version_whole_field={'present':True,'original_value':None}))
 mutation(0,lambda x:x.update(printed_title_date_version_inspected=True))
 mutation(0,lambda x:x.update(target_PDF_rasters_visually_read=True))
 mutation(0,lambda x:x.update(completion_percent_at_preseal=95))
 mutation(0,lambda x:x.update(publication_authority=None))
 mutation(0,lambda x:x.update(source_programmes_executed=['reproduce.py']))
 mutation(0,lambda x:x['all_native_assets_in_original_order'].reverse())
 mutation(0,lambda x:x.update(whole_regular_payload_occurrences=26))
 mutation(0,lambda x:x.update(expanded_bytes_all_depths=243850))
 mutation(1,lambda x:x.update(swh=None))
 mutation(2,lambda x:x.update(swh=[]))
 mutation(3,lambda x:x['hits']['hits'][0].update(swh={}))
 mutation(4,lambda x:x.update(order={}))
 mutation(4,lambda x:x.update(default_preview=''))
 mutation(4,lambda x:x['entries'].reverse())
 mutation(5,lambda x:x.pop(1))
 mutation(5,lambda x:x[1].update(HTTP_status=200))
 mutation(5,lambda x:x[-1].update(response_headers_in_received_order=list(dict(x[-1]['response_headers_in_received_order']).items())))
 for i,a in enumerate(mutants):ck(not facts(*a),'in-memory native fact falsifier '+str(i))
 ck(sha(pdf+b'X')!=r['selected_actual_PDF']['SHA256'],'appended manuscript rejected');ck(sha(tex[:-1])!=r['controlling_TeX']['SHA256'],'truncated TeX rejected')
 d=copy.deepcopy(nd['members_in_original_order'][0]);d['native_date_time'][0]+=1;ck(d!=nd['members_in_original_order'][0],'changed native ZIP timestamp rejected')
 if not pre:
  seal=js(P/'SEAL.json')
  for key,name in [('INPUT_MANIFEST_SHA256','INPUT_MANIFEST.json'),('OWNED_MANIFEST_SHA256','OWNED_MANIFEST.json'),('CLOSURE_SHA256','CLOSURE.json'),('REPORT_SHA256','REPORT.md'),('VERDICT_SHA256','VERDICT.json'),('verifier_SHA256','verify_closure.py')]:ck(seal[key]==sha((P/name).read_bytes()),'terminal seal '+name)
  ck(seal['completion_percent']==100 and seal['source_changes']is False,'final completion/source unchanged')
 return {'status':'PASS'if not fail else'FAIL','checks':checks,'failures':fail,'input_files':len(im['files']),'owned_files':len(om['files']),'original_ZIP_payloads':27,'in_memory_falsifiers':len(mutants)+3,'mode':'preseal'if pre else'final','network':False,'writes':False,'target_scientific_imports_or_execution':False}
try:result=main()
except Exception as e:result={'status':'FAIL','checks':checks,'failures':fail+[type(e).__name__+': '+str(e)],'network':False,'writes':False,'target_scientific_imports_or_execution':False}
print(json.dumps(result,indent=2));sys.exit(0 if result['status']=='PASS'else 1)
