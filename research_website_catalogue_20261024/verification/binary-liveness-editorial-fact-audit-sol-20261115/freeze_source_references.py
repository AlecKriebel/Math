"""New initial source/root reference custody. No editorial, network or science execution."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,stat
D=Path(__file__).resolve().parent
B=D.parent.parent
P=B/'papers/23202966'
def need(ok,label):
 if not ok:raise RuntimeError(label)
def read(p):
 p=Path(p);need(p.resolve()==p and stat.S_ISREG(p.lstat().st_mode),'ordinary source reference');return p.read_bytes()
def pin(b):return {'bytes':len(b),'SHA256':hashlib.sha256(b).hexdigest()}
def new(name,obj):
 with (D/name).open('x') as f:json.dump(obj,f,ensure_ascii=False,indent=2);f.write('\n')
def extent(root):
 need(root.resolve()==root and stat.S_ISDIR(root.lstat().st_mode),'ordinary root')
 fs={};ds=[]
 for q in root.rglob('*'):
  rel=q.relative_to(root).as_posix();m=q.lstat().st_mode
  if stat.S_ISDIR(m):ds.append(rel)
  else:need(stat.S_ISREG(m),'ordinary entry');need(rel not in fs,'duplicate');fs[rel]=pin(read(q))
 return {'root':str(root),'files':dict(sorted(fs.items())),'directories':sorted(ds)}
need(D==B/'verification/binary-liveness-editorial-fact-audit-sol-20261115','exact own namespace')
need(not (D/'INITIAL_SEAL.json').exists(),'initial not yet sealed')
ready_path=P/'sources/SOURCE_READY.json';ready_raw=read(ready_path)
need(pin(ready_raw)['SHA256']=='86264fb9c694c35abcdcae60fd15aaa617627204ceb8e0cd95b09947e4d893dc','source READY pin')
authority=B/'verification/root-clearance-23202966-20261115.json';ar=read(authority)
need(pin(ar)['SHA256']=='3310703ec448b133b4f1cf5cfdd4b12845cf588e2a4920609345b5d0ee737237','full root authority pin')
proof=P/'reviews/root/ROOT_REVIEW_20261115.md';pr=read(proof)
need(pin(pr)['SHA256']=='a0e755680cc1c210d96c2ea2930aab47d2bb92ab2a7da82e63f116f677105370','root full proof pin')
roots=[P/'sources',P/'reviews/scope',P/'reviews/adversarial',P/'reviews/root']
refs=[extent(r) for r in roots]
need([(len(x['files']),len(x['directories'])) for x in refs]==[(82,9),(272,45),(133,21),(35,3)],'exact source/science/root extents')
new('SOURCE_ROOT_REFERENCES.json',{'UTC':datetime.now(timezone.utc).isoformat(),'namespaces':refs,'separate_root_authority':{'path':str(authority),**pin(ar)},'raw_copyrighted_corpora_recopied':False,'new_editorial_listed_read_or_executed':False})
ready=json.loads(ready_raw);record=json.loads(read(P/'sources/record.response.body'));files=json.loads(read(P/'sources/files.response.body'));tex=read(P/'sources/assets/main.tex').decode()
abstract=tex.split('\\begin{abstract}',1)[1].split('\\end{abstract}',1)[0]
metadata={'record_id':23202966,'whole_original_native_metadata':record['metadata'],'whole_original_native_record_asset_array':record['files'],'whole_original_native_files_object':files,'whole_source_READY_native_asset_entries':ready['all_native_assets_in_original_order'],'whole_printed_abstract_TeX':abstract,'native_description_is_distinct_from_printed_abstract':True,'API_version_field_present':'version' in record['metadata'],'API_version_original_value':record['metadata'].get('version'),'printed_version_present':False,'printed_version':None,'declared_publication_date':record['metadata']['publication_date'],'created':record['created'],'modified':record['modified'],'whole_authored_license_and_disclosure_README':read(P/'sources/assets/README.md').decode(),'whole_source_ready_reference':{'path':str(ready_path),**pin(ready_raw)}}
new('EXPECTED_NATIVE_METADATA.json',metadata)
own_rasters=[]
for i in range(1,7):
 q=D/'rasters'/('page-%d.png'%i);own_rasters.append({'page':i,'path':q.relative_to(D).as_posix(),**pin(read(q)),'fresh_own_native_PDF_render':True,'individually_visually_read':True})
new('OWN_PDF_READING.json',{'native_PDF':{'path':str(P/'sources/assets/paper.pdf'),**pin(read(P/'sources/assets/paper.pdf'))},'full_PDF_pages_personally_read':6,'native_TeX':{'path':str(P/'sources/assets/main.tex'),**pin(tex.encode()),'all_lines_personally_read':376},'renderer':'/opt/homebrew/bin/pdftoppm','arguments':['-r','140','-png'],'actual_render_tool_chunk':'38e790','actual_render_exit':0,'render_stdout':pin(read(D/'PDF_RENDER.stdout')),'render_stderr':pin(read(D/'PDF_RENDER.stderr')),'all_six_fresh_own_rasters':own_rasters,'existing_native_or_upstream_build_scientific_program_executed':False})
print(json.dumps({'status':'SOURCE_ROOT_REFERENCE_INITIAL_CAPTURED','original_namespaces':[[len(x['files']),len(x['directories'])] for x in refs],'original_native_assets':len(record['files']),'fresh_own_rasters':6,'raw_corpora_recopied':False,'new_editorial_exposure':False,'scientific_native_network_or_outside_writes':False}))
