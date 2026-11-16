"""Source/root-only reference capture. No editorial, science, build or network access."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,stat
D=Path(__file__).resolve().parent;B=D.parent.parent;P=B/'papers/23205305'
def need(ok,label):
 if not ok:raise RuntimeError(label)
def read(p):
 p=Path(p);need(p.resolve()==p and stat.S_ISREG(p.lstat().st_mode),'ordinary pinned file');return p.read_bytes()
def pin(b):return {'bytes':len(b),'SHA256':hashlib.sha256(b).hexdigest()}
def new(n,x):
 with (D/n).open('x') as f:json.dump(x,f,indent=2,ensure_ascii=False);f.write('\n')
def extent(root):
 need(root.resolve()==root and stat.S_ISDIR(root.lstat().st_mode),'ordinary root')
 fs={};ds=[]
 for q in root.rglob('*'):
  rel=q.relative_to(root).as_posix();m=q.lstat().st_mode
  if stat.S_ISDIR(m):ds.append(rel)
  else:need(stat.S_ISREG(m) and rel not in fs,'ordinary unique entry');fs[rel]=pin(read(q))
 return {'root':str(root),'files':dict(sorted(fs.items())),'directories':sorted(ds)}
need(D==B/'verification/rational-point-editorial-fact-audit-sol-20261115','exact own root')
need(not (D/'INITIAL_SEAL.json').exists(),'not yet initial sealed')
authority=B/'verification/root-clearance-23205305-20261115.json';ar=read(authority)
need(pin(ar)=={'bytes':5711,'SHA256':'cf6d07993f0a174bb0552c9e4484a854add3b804a56b8a4e394699c234c15895'},'root authority pin')
proof=P/'reviews/root/ROOT_PROOF_20261115.md';need(pin(read(proof))=={'bytes':18285,'SHA256':'c20eed98a18ecabfe61c268ccdd043d681f63f8884eb556bd081443187be1393'},'full root proof pin')
ready_path=P/'sources/SOURCE_READY.json';rr=read(ready_path);ready=json.loads(rr)
need(pin(rr)['SHA256']=='d5e1575052e0db802b6d8ff47309660b50213d91594856eb4df141943bf0db91','READY pin')
need(pin(read(P/'sources/SOURCE_READY_SEAL.json'))['SHA256']=='6540b1c94839ae033e0747843452bd6c33d29c3734680332c8cbc119e79fdcc8','source FINAL pin')
need(pin(read(P/'reviews/root/FINAL_SEAL.json'))['SHA256']=='123c2ab1b3d584cad5fa66d3d01a18f5a75917b661bd866902bb464561e7f74c','root FINAL pin')
for family in json.loads(ar)['current_independent_families'].values():
 r=family['FINAL'];need(pin(read(r['path']))=={k:r[k] for k in ['bytes','SHA256']},'root-authorized original family FINAL pin')
namespaces=[extent(P/n) for n in ['sources','reviews/scope','reviews/adversarial','reviews/root']]
need([(len(x['files']),len(x['directories'])) for x in namespaces]==[(126,17),(424,7),(292,7),(33,2)],'exact frozen source/science/root extents')
prior=B/'verification/binary-liveness-editorial-fact-audit-sol-20261115/EDITORIAL_REFERENCE_EXTENT.json'
core=json.loads(read(prior))['qualified_core_references'];need(len(core)==18,'qualified17 plus405b core descriptors')
for r in core:need(pin(read(r['path']))=={k:r[k] for k in ['bytes','SHA256']},'qualified current core bytes')
need(any(r['SHA256']=='405b0357fd20a2e14893ce6c3c1a0f81910894ccd8ffaddac4e25014138fb9c0' for r in core),'sole authorized405b checkpoint')
new('SOURCE_ROOT_REFERENCES.json',{'UTC':datetime.now(timezone.utc).isoformat(),'namespaces':namespaces,'authority':{'path':str(authority),**pin(ar)},'qualified_core17_plus_sole405b':core,'core_descriptor_prior_immutable_context':{'path':str(prior),**pin(read(prior))},'core_qualification':'17original sources plus sole separately authorized405b; no generated-cache/GitHEAD/index freeze','current_editorial_folder_listed_or_read':False,'original_science_or_primary_corpora_recopied':False})
record=json.loads(read(P/'sources/record.response.body'));files=json.loads(read(P/'sources/files.response.body'))
manuscripts=[]
for key,desc,pages,prefix in [('paper.pdf',ready['controlling_TeX'],6,'main'),('height-repair.pdf',ready['additional_controlling_TeX_sources'][0],4,'companion')]:
 tex=read(desc['extracted_path']).decode();abstract=tex.split('\\begin{abstract}',1)[1].split('\\end{abstract}',1)[0]
 title=tex.split('\\title{',1)[1].split('}\n\\author',1)[0]
 rasters=[]
 for i in range(1,pages+1):
  q=D/'rasters'/('%s-%d.png'%(prefix,i));rasters.append({'page':i,'path':q.relative_to(D).as_posix(),**pin(read(q)),'fresh_own_individually_visually_read':True})
 manuscripts.append({'native_PDF_key':key,'native_PDF':{'path':str(P/'sources/assets'/key),**pin(read(P/'sources/assets'/key))},'PDF_pages_personally_read':pages,'TeX_reference':{'path':desc['extracted_path'],**pin(tex.encode()),'lines_personally_read':len(tex.splitlines())},'full_original_title_TeX':title,'full_original_abstract_TeX':abstract,'fresh_own_individual_rasters':rasters})
licenses=[]
for n in ['asset-001/LICENSES.md','asset-002/LICENSES.md']:
 q=P/'sources/published-source'/n;licenses.append({'path':str(q),**pin(read(q)),'whole_original_license_text':read(q).decode()})
new('EXPECTED_NATIVE_METADATA.json',{'record_id':23205305,'whole_original_record_metadata':record['metadata'],'whole_original_record_asset_array':record['files'],'whole_original_files_API_object':files,'whole_original_SOURCE_READY_asset_custody':ready['all_native_assets_in_original_order'],'both_complete_original_manuscripts':manuscripts,'native_full_description_distinct_from_both_printed_abstracts':record['metadata']['description'],'whole_original_LICENSES':licenses,'printed_and_API_version_present':False,'native_version_original_value':None,'native_date':record['metadata']['publication_date'],'native_creation_UTC':record['created'],'native_modified_UTC':record['modified'],'prose':'CC BY4.0','authored_code':'MIT','mixed_ZIP_encoding_blanket_license':'ABSENT in generated metadata, original native license fields remain literal','full_companion_conditional_title_and_abstract_must_remain_explicit':True})
print(json.dumps({'status':'SOURCE_ROOT_ONLY_RATIONAL_POINT_INITIAL_REFERENCES_CAPTURED','original_namespaces':[[126,17],[424,7],[292,7],[33,2]],'original_native_assets':4,'complete_PDF_pages':[6,4],'complete_TeX_lines':[371,325],'fresh_own_rasters':10,'qualified_core':'17original_plus405b','current_editorial_exposure':False,'scientific_native_foreign_network_or_outside_writes':False,'raw_corpora_recopied':False}))
