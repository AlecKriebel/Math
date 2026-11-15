"""One-time metadata/opaque custody freeze, no scientific semantic reading/imports."""
from pathlib import Path
from hashlib import sha256,md5
from datetime import datetime,timezone
import json,zipfile,zlib,io
A=Path(__file__).resolve().parent
S=A.parents[2]/'sources'
def now():return datetime.now(timezone.utc).isoformat()
def need(ok,msg):
 if not ok:raise ValueError(msg)
def binding(b):return {'bytes':len(b),'SHA256':sha256(b).hexdigest()}
def save(n,x):
 p=A/n;need(not p.exists(),'refuse overwrite '+n);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
need(not (A/'INPUT_MANIFEST.json').exists(),'new custody freeze only')
# Entire raw folder is ignored before it is created or any original byte is copied.
ignore=A/'.gitignore';need(not ignore.exists(),'new ignore protocol only');ignore.write_text('raw/\n')
ignore_time=now();(A/'raw').mkdir()
paths=sorted(S.rglob('*'));need(not any(p.is_symlink() for p in paths),'no source symlinks')
files=[p for p in paths if p.is_file()];names=[str(p.relative_to(S)) for p in files]
need(len(files)==87,'actual complete87 source namespace')
rows=[]
for p in files:
 b=p.read_bytes();rel=p.relative_to(S);q=A/'raw'/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
 need(q.read_bytes()==b,'fresh raw byte identity')
 rows.append({'original':str(p),'copy':'raw/'+str(rel),**binding(b)})
lookup={r['original']:r for r in rows}
def load_source(p):
 p=Path(p);p=p if p.is_absolute() else S/p
 # Only metadata allowlist paths are parsed; archive payloads/code/opinions are opaque.
 allowed={S/'SOURCE_READY.json',S/'SOURCE_READY_SEAL.json',S/'ALL_TRANSPORT_RECEIPTS.json',S/'NATIVE_SCHEMA_TYPES.json',S/'ARCHIVE_CUSTODY.json',S/'MANUSCRIPT_CUSTODY.json',S/'SOURCE_READY_MANIFEST.json',S/'SOURCE_READY_CLOSURE.json',S/'INPUT_MANIFEST.json',S/'record.response.body',S/'latest.response.body.redirect-01',S/'versions-page001.response.body',S/'files.response.body'}
 if str(p).endswith('.transport.json'):allowed.add(p)
 need(p in allowed,'metadata-only parsing allowlist '+str(p))
 return json.loads((A/lookup[str(p)]['copy']).read_bytes())
r=load_source('SOURCE_READY.json');seal=load_source('SOURCE_READY_SEAL.json')
need(binding((A/'raw/SOURCE_READY.json').read_bytes())['SHA256']=='28a9736d92beaadb1faa37c9146d56191be83fb217116f24b33162bea922e469','source ready pin')
need(binding((A/'raw/SOURCE_READY_SEAL.json').read_bytes())['SHA256']=='c523e830e06555037254c26d9d85c82f4324c841cdd268f99d95664bf02e2150','actual source seal pin')
metadata={'SOURCE_READY_whole_literal':r,'SOURCE_READY_SEAL_whole_literal':seal,'native_API_whole_literal':[load_source(q['path']) for q in r['whole_native_API_objects']],'transport_aggregate_whole_literal':load_source(r['actual_transport_receipts']['path']),'schema_whole_literal':load_source(r['native_schema_types']['path']),'archive_custody_whole_literal':load_source(r['whole_archive_custody']['path']),'manuscript_custody_whole_literal':load_source(r['manuscript_custody']['path']),'source_manifest_whole_literal':load_source('SOURCE_READY_MANIFEST.json'),'source_closure_whole_literal':load_source('SOURCE_READY_CLOSURE.json'),'source_input_manifest_whole_literal':load_source('INPUT_MANIFEST.json')}
receipts=metadata['transport_aggregate_whole_literal'];need(type(receipts) is list and len(receipts)==7,'actual aggregate is list7, not receipts wrapper')
need([q['HTTP_status'] for q in receipts]==[200,301,200,200,200,200,200],'literal transport order')
metadata['seven_transport_objects_whole_literal']=[load_source(q['body_path']+'.transport.json') for q in receipts]
need(type(metadata['schema_whole_literal']) is list,'actual schema is list, not object')
archive=metadata['archive_custody_whole_literal'];occ=archive['regular_payload_occurrences'];need(len(occ)==38 and len(archive['containers'])==1,'actual complete38payload1container')
assets=r['all_native_assets_in_original_order'];need([Path(q['path']).suffix for q in assets]==['.zip','.pdf'],'native ZIP thenPDF order')
ziprow=assets[0];zipbytes=(A/lookup[ziprow['path']]['copy']).read_bytes();checks=[]
with zipfile.ZipFile(io.BytesIO(zipbytes)) as z:
 regular=[q for q in z.infolist() if not q.is_dir()]
 need(len(regular)==38,'actual ZIP38regular entries')
 byname={q.filename:q for q in regular};need(len(byname)==38,'unique literal ZIP names')
 for o in occ:
  info=byname[o['original_member_name']];b=z.read(info)
  extracted=(A/lookup[o['extracted_path']]['copy']).read_bytes()
  need(b==extracted and len(b)==o['bytes'] and sha256(b).hexdigest()==o['SHA256'],'opaque ZIP/extracted identity')
  need(f'{zlib.crc32(b)&0xffffffff:08x}'==o['CRC32'] and info.CRC==(zlib.crc32(b)&0xffffffff),'opaque CRC identity')
  checks.append({'original_member_name':o['original_member_name'],'original_extracted_path':o['extracted_path'],'bytes':len(b),'SHA256':sha256(b).hexdigest(),'CRC32':o['CRC32'],'compressed_bytes':info.compress_size,'compression_method':info.compress_type,'whole_original_external_attr':info.external_attr,'whole_original_flags':info.flag_bits,'whole_original_date_time':list(info.date_time),'opaque_bytes_equal':True})
for a in assets:
 b=(A/lookup[a['path']]['copy']).read_bytes();need(binding(b)=={'bytes':a['bytes'],'SHA256':a['SHA256']},'native asset SHA size')
 need('md5:'+md5(b).hexdigest()==a['original_api_file_object']['checksum'],'native MD5')
need(r['selected_actual_PDF']['pages']==5 and r['controlling_TeX']['opaque_byte_splitlines_count']==342,'actual metadata page/line counts')
tex=(A/lookup[r['controlling_TeX']['extracted_path']]['copy']).read_bytes();need(len(tex.splitlines())==342,'opaque actual342TeXlines')
need(r['completion_percent_at_preseal']==100,'literal historical preseal100')
need(r['printed_title_date_version_inspected'] is False and r['mathematical_PDF_TeX_or_pixels_read'] is False and r['scientific_verdict'] is None and r['publication_authority'] is False,'source unread/null flags literal')
need(sorted(str(p.relative_to(S)) for p in S.rglob('*') if p.is_file())==names,'complete source namespace unchanged acrosscopy')
for row in rows:need((Path(row['original']).read_bytes())==(A/row['copy']).read_bytes(),'source unchanged acrosscopy')
save('INPUT_MANIFEST.json',{'UTC':now(),'source_root':str(S),'source_namespace':names,'original_source_regular_files':87,'raw_entire_folder_ignored_before_creation':True,'ignore_established_UTC':ignore_time,'files':rows,'scientific_content_semantically_read':False,'source_programs_executed':[]})
save('WHOLE_LITERAL_NATIVE.json',metadata)
save('ARCHIVE_OPAQUE_COMPARISONS.json',{'UTC':now(),'containers':1,'regular_payload_occurrences':38,'checks':checks,'scientific_semantic_reading':False,'code_import_or_execution':False})
save('DIAGNOSTIC.json',{'UTC':now(),'actual_readonly_intake_error':'An exploratory metadata shape printer assumed ALL_TRANSPORT_RECEIPTS was an object with receipts; the actual schema is an ordered list. It raised TypeError after printing transport metadata. No source writes or scientific body exposure occurred. The corrected freezer preserves the whole list literally.','native_schema_object_also_actual_list':True,'source_or_opinion_bodies_read':False})
initial_names=['.gitignore','freeze_custody.py','INPUT_MANIFEST.json','WHOLE_LITERAL_NATIVE.json','ARCHIVE_OPAQUE_COMPARISONS.json','DIAGNOSTIC.json']+[row['copy'] for row in rows]
save('INITIAL_SEAL.json',{'UTC':now(),'scope':'Metadata/opaque custody only; no scientific finding or authority','frozen_input_payloads':{n:binding((A/n).read_bytes()) for n in initial_names},'completion_percent_bounded_custody':80,'scientific_gate':'ROOT133CLOSED','canonical_url':None,'AA':None,'follow_up':None})
print(json.dumps({'scope':'neutral metadata-only freeze','initial_seal':binding((A/'INITIAL_SEAL.json').read_bytes()),'completion_percent':80}))
