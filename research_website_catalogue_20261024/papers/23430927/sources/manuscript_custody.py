#!/usr/bin/env python3
"""Metadata-only manuscript custody. Never extract PDF text, view pixels or read TeX."""
from pathlib import Path
import datetime,hashlib,json,re,struct,subprocess
R=Path(__file__).resolve().parent
def need(v,m):
 if not v:raise RuntimeError(m)
def load(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def info(p):
 r=subprocess.run(['pdfinfo',str(p)],capture_output=True);need(r.returncode==0,'PDF metadata parser failed')
 match=re.search(rb'^Pages:\s+(\d+)\s*$',r.stdout,re.M);need(match,'Missing PDF page count');return int(match.group(1)),r
def main():
 a=load(R/'ACQUIRED_NATIVE.json');arc=load(R/'ARCHIVE_CUSTODY.json');selection=load(R/'MANUSCRIPT_SELECTION.json') if (R/'MANUSCRIPT_SELECTION.json').exists() else {}
 pdfs=[x for x in a['all_assets_in_original_order'] if Path(x['path']).suffix.lower()=='.pdf'];need(pdfs,'No actual native standalone PDF reader')
 if len(pdfs)==1:primary_key=pdfs[0]['original_api_file_object']['key']
 else:primary_key=selection['primary_native_PDF_key']
 selected_matches=[x for x in pdfs if x['original_api_file_object']['key']==primary_key];need(len(selected_matches)==1,'Actual primary reader selection must be unique')
 readers=[];metadata=[]
 for original in pdfs:
  pc,pi=info(Path(original['path']));reader=dict(original);reader.update({'pages':pc,'text_extracted':False,'pages_visually_or_scientifically_read':False,'actual_standalone_API_asset':True});readers.append(reader);metadata.append({'argv':['pdfinfo',original['path']],'exit_code':pi.returncode,'full_original_stdout_opaque':pi.stdout.decode(errors='replace'),'full_original_stderr':pi.stderr.decode(errors='replace')})
 selected=next(x for x in readers if x['original_api_file_object']['key']==primary_key);pdf=Path(selected['path']);count=selected['pages']
 texs=[dict(x) for x in arc['regular_payload_occurrences'] if x['original_member_name'].lower().endswith('.tex')];native=[x for x in a['all_assets_in_original_order'] if Path(x['path']).suffix.lower()=='.tex']
 need(len(native)<=1,'Ambiguous native standalone TeX')
 if native:
  matches=[x for x in texs if x['SHA256']==native[0]['SHA256']]
  if matches:
   chosen=dict(matches[0]);basis='Actual native standalone TeX is byte identical to '+str(len(matches))+' archived occurrence(s); first original archive-order matching occurrence selected as structural source path. Native PDF/TeX basenames may differ. No body or typeset/build equivalence claimed.'
  else:
   chosen=dict(native[0]);chosen['extracted_path']=chosen['path'];chosen['actual_standalone_API_source_not_extracted']=True;basis='Sole actual native standalone TeX co-deposited with the selected native published PDF. No byte-identical archived TeX was found; all archived source candidates remain preserved, with no source-body/build equivalence inferred.'
 else:
  if len(texs)==1:chosen=dict(texs[0]);basis='Sole archived TeX occurrence co-deposited with the selected native standalone PDF; structural source custody only, no body or typeset/build equivalence certified.'
  else:
   key=selection['controlling_archived_TeX_member'];matches=[x for x in texs if x['original_member_name']==key and x['SHA256']==selection['controlling_archived_TeX_SHA256'] and x['container_id']==selection.get('controlling_archived_TeX_container_id',x['container_id'])];need(len(matches)==1,'Explicit metadata-only archived TeX selector must be unique');chosen=dict(matches[0]);basis=selection['selection_basis']
 tp=Path(chosen['extracted_path']);chosen['opaque_byte_splitlines_count']=len(tp.read_bytes().splitlines());chosen['preamble_or_mathematical_body_read']=False
 embedded=[]
 for x in arc['regular_payload_occurrences']:
  p=Path(x['extracted_path'])
  if p.read_bytes()[:5]==b'%PDF-':
   pc,unused=info(p);embedded.append(dict(x)|{'pages':pc,'identical_to_standalone_published_PDF':x['SHA256']==selected['SHA256'],'body_or_pixels_scientifically_read':False})
 out=R/'rasters';out.mkdir();commands=[];rasters=[]
 for ordinal,reader in enumerate(readers,1):
  sub=out/('reader-%03d'%ordinal);sub.mkdir();cmd=['pdftoppm','-r','145','-png',reader['path'],str(sub/'page')];start=datetime.datetime.now(datetime.timezone.utc).isoformat();r=subprocess.run(cmd,capture_output=True);commands.append({'started_UTC':start,'completed_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'argv':cmd,'exit_code':r.returncode,'stdout':r.stdout.decode(errors='replace'),'stderr':r.stderr.decode(errors='replace'),'native_reader_key':reader['original_api_file_object']['key']})
  need(r.returncode==0,'PDF raster generation failed');found=[]
  for p in sorted(sub.glob('page-*.png')):
   b=p.read_bytes();need(b[:8]==b'\x89PNG\r\n\x1a\n','Raster format');w,h=struct.unpack('>II',b[16:24]);found.append({'path':str(p),'bytes':len(b),'SHA256':sha(b),'width':w,'height':h,'visually_read':False,'native_reader_key':reader['original_api_file_object']['key'],'native_reader_SHA256':reader['SHA256']})
  need(len(found)==reader['pages'],'Actual reader page/raster count mismatch');rasters.extend(found)
 (R/'RENDER_RECEIPT.json').write_text(json.dumps({'commands_in_reader_order':commands,'exit_code':0,'metadata_parser_actual_results':metadata,'images_opened_or_emitted_or_visually_read':False},indent=2)+'\n')
 need(len(rasters)==sum(x['pages'] for x in readers),'All native reader page/raster coverage')
 q=load(R/'QUEUE_BINDING.json');identity_only=q['identity_only']
 need(identity_only['record_id']==a['record_id'] and identity_only['title']==a['title'] and identity_only['doi']==a['doi'],'Existing exact queue and fresh native record identity')
 identity={'identity_source':'existing exact inventory queue plus actual fresh native Zenodo APIs; not a current native Sheet read','queue_identity_only_original':identity_only,'queue_and_fresh_native_record_match':True,'current_native_Sheet_read':False,'current_native_identifier_and_queued_status_match':None,'native_Sheet_identifier_or_eligibility_verified':False,'actual_native_PDF_SHA256_matches_current_sheet':None,'current_sheet_PDF_checksum_field_read':False,'actual_native_PDF_SHA256':selected['SHA256'],'actual_native_PDF_checksum_and_size_verified':selected['native_checksum_verified'],'native_API_version_field_present':a['version_field_present'],'native_API_version_original':a['version_original'],'scientific_assessment_columns_read':False,'target_scientific_body_code_result_or_opinion_exposure':False}
 (R/'NATIVE_IDENTITY_MATCH.json').write_text(json.dumps(identity,indent=2,ensure_ascii=False)+'\n')
 result={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'record_id':a['record_id'],'selected_actual_PDF':selected,'actual_standalone_readers':readers,'controlling_TeX':chosen,'controlling_TeX_selection_basis':basis,'all_TeX_candidates':texs,'actual_standalone_TeX_assets':native,'embedded_PDFs':embedded,'fresh_page_rasters':rasters,'PDF_pages':count,'all_native_reader_total_pages':sum(x['pages'] for x in readers),'metadata_only_selector':selection,'source_byte_line_count':chosen['opaque_byte_splitlines_count'],'printed_title_date_version_inspected':False,'printed_date':None,'printed_version':None,'PDF_text_extracted':False,'mathematical_PDF_TeX_or_pixels_read':False};(R/'MANUSCRIPT_CUSTODY.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
 schema=[]
 def walk(v,path,role):
  item={'role':role,'JSON_pointer':path,'original_type':type(v).__name__}
  if v is None or v=={} or v==[]:item['original_empty_or_null_value']=v
  schema.append(item)
  if isinstance(v,dict):
   for k,w in v.items():walk(w,path+'/'+str(k).replace('~','~0').replace('/','~1'),role)
  elif isinstance(v,list):
   for i,w in enumerate(v):walk(w,path+'/'+str(i),role)
 for obj in a['whole_native_API_objects']:walk(load(Path(obj['path'])),'',obj['role'])
 (R/'NATIVE_SCHEMA_TYPES.json').write_text(json.dumps(schema,indent=2,ensure_ascii=False)+'\n')
 with (R/'SOURCE_LOG.md').open('a') as f:f.write('\n'+result['UTC']+' — 80%: Native PDF page metadata and fresh per-page raster hashes recorded without PDF text extraction or image viewing. Exact native/archive source association and opaque TeX byte-line count recorded. Printed identity and every mathematical body/pixel/program/result/opinion remain unread.\n')
 print(json.dumps({'record_id':a['record_id'],'PDF_pages':count,'TeX_bytes':chosen['bytes'],'TeX_lines':chosen['opaque_byte_splitlines_count'],'all_native_reader_total_pages':sum(x['pages'] for x in readers),'native_standalone_TeX_count':len(native),'archived_TeX_occurrences':len(texs),'fresh_unread_rasters':len(rasters),'source_body_read':False}))
if __name__=='__main__':main()
