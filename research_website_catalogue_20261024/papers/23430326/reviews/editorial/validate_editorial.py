"""Read-only original validation; write only new own editorial evidence."""
from pathlib import Path
from datetime import datetime,timezone
from io import BytesIO
import ast,copy,hashlib,json,re,zipfile
from pypdf import PdfReader
P=Path(__file__).resolve().parents[2];O=P/'reviews/editorial';ROOT=P.parents[1];ID=P.name
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def digest(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_text())
def now():return datetime.now(timezone.utc).isoformat()
def write(p,obj):assert not p.exists(),p;p.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
pins={'23390551':'4c727e1b34afddf6804c9b0954f6706868f45b697bdad9697471d8205eedd16a','23430326':'ca0ea2a7b0ecf7243d8e23b2ed1aa7e18e9890ff28c786e468237e052c118dbf'}
prepare=ROOT/'papers/23390551/reviews/editorial/prepare_configs.py';tree=ast.parse(prepare.read_text());norm_node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='norm_abstract');env={'re':re};exec(compile(ast.Module(body=[norm_node],type_ignores=[]),'<owned abstract typography>','exec'),env);normalize=env['norm_abstract']
pub=load(P/'publication.json');pro=load(P/'promotion.json');binding=pub['source_binding'];clearpath=ROOT/pro['root_clearance_file'];clear=load(clearpath)
checks=[]
def check(ok,label):
 if not ok:raise RuntimeError(label)
 checks.append(label)
def content_checks(c,g):
 failures=[]
 def require(ok,label):
  if not ok:failures.append(label)
 b=c['source_binding'];tex=P/b['source_tex_path'];a=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',tex.read_text(),re.S).group(1).strip()
 require(normalize(ID,a)==c['abstract'] and a==b['abstract_tex'] and digest(a.encode())==b['abstract_tex_sha256'],'complete_original_abstract')
 require(c['abstract_heading']==b['abstract_display_heading']=='Original abstract' and c['abstract_is_original'] is True,'original_abstract_heading')
 require(g['root_clearance_record']==clear and g['approved_scope']==clear['approved_scope'] and g['scope_gate_resolution']==clear['scope_gate_resolution'],'entire_separate_root_authority')
 require(all(v['verdict']==load(P/v['verdict_file']) for v in g['reviews'].values()),'entire_original_custom_verdicts')
 original_receipt=load(P/clear['source_receipt_path'])
 require(b['receipt_path']==clear['source_receipt_path'] and g['source_receipt_record']==original_receipt and g['source_files']==b['files']==original_receipt['files'],'entire_original_receipt_objects')
 if ID=='23390551':
  require(b['receipt_path']=='sources/acquisition_receipt.json' and b['metadata_path']=='sources/zenodo_record.json' and b['asset_root_path']=='sources/cache' and not (P/'sources/receipt.json').exists(),'custom_original_paths_no_alias')
  require(b['archive_recursive_regular_member_occurrences']==323 and b['archive_unique_member_sha256_count']==170 and b['archive_regular_file_count']==187 and b['nested_archive_count']==1 and b['archive_layers']==2 and b['total_distinct_reader_pdf_count']==2,'true_historical_and_nested_archive_metadata')
  result=' '.join(c['result']);limits=' '.join(c['limitations']);proof=' '.join(c['why_it_works'])
  require(all(t in result for t in ['chosen representative','Fix κ∈ℂ throughout the mesh limit','(G): |Ω_h△Ω|→0','every 3×3 diagonal block zero','S_κ=A_κ−I/3','exact closed numerical range','uniformly bounded discrete inverses','total algebraic multiplicity','Both gap directions','h³∑_m|u_m|²','κ=1/10000','existential finite index']),'dipole_full_claim_quantifiers')
  require(all(t in limits for t in ['No spectral correctness inside J_lat','convergence rate','Individual Jordan block sizes','does not classify','Rahola','no firstness']) and 'adjoint resolvents' in proof and 'closed ball' in proof,'dipole_limits_and_mechanism')
 else:
  require(b['receipt_path']=='sources/receipt.json' and 'record_sha256' not in load(P/b['receipt_path']) and b['nested_archive_count']==0 and b['archive_regular_file_count']==37 and b['total_distinct_reader_pdf_count']==1,'original_standard_raw_receipt_shape')
  candidate=load(P/b['frozen_scope_content_path']);require(c['abstract']==candidate['abstract'],'frozen_candidate_full_abstract')
  result=' '.join(c['result']);proof=' '.join(c['why_it_works']);limits=' '.join(c['limitations'])
  require(all(t in result for t in ['F=ℚ₃','unramified quadratic extension','smooth admissible complex','Langlands quotient','entire normalized induction','every nonsingular 15-dimensional Hermitian space','zero rather than two']),'langlands_full_exact_field_quotient_and_orbits')
  require(all(t in proof for t in ['each fixed Hermitian orbit','Two strict-containment swaps','odd cycle','No general equality generating that kernel','partition of the five segment occurrences']) and all(t in limits for t in ['remain UNKNOWN','may overlap, be contained in, or be superseded','No exhaustive literature absence, independent first discovery','unitarizable','spherical']),'langlands_fixed_orbit_odd_cycle_all_partitions_unknown_overlap')
 require(c['follow_up'] is g['follow_up'] is None and g['native_sheet_aa_url'] is None and all(g[k] is False for k in ['rendered_copy_verified','live_verified','browser_verified']),'publication_gates_withheld')
 return failures
check(not content_checks(pub,pro),'all literal content, complete custom authorities, original paths and full original abstract')
check(sha(clearpath)==pro['root_clearance_sha256']==pub['review_metadata']['root_clearance_sha256']==pins[ID],'exact independently supplied root pin')
check(pro['status']==clear['status']=='PASS' and pro['disposition_by']==clear['disposition_by']=='root','later root status only')
check(sha(P/'publication.json')==pro['publication_sha256'],'exact publication binding')
check(sha(P/binding['source_tex_path'])==binding['source_tex_sha256']==binding['abstract_source_sha256'],'exact selected TeX')
check(sha(P/binding['receipt_path'])==binding['receipt_sha256']==binding['source_receipt_sha256']==pro['source_receipt_sha256']==clear['source_receipt_sha256'],'original receipt bytes')
check(sha(P/binding['metadata_path'])==binding['metadata_sha256']==binding['record_sha256']==pro['metadata_sha256']==clear['metadata_sha256'],'original readable metadata bytes')
record=load(P/binding['metadata_path']);metadata=record['metadata']
check(str(record['id'])==ID and all(pub[k]==metadata[k] for k in ['title','publication_date','version','doi']),'exact deposited metadata')
check(record['created']==binding['record_created_utc'] and record['updated']==binding['record_updated_utc'],'exact record timestamps')
check(metadata['creators'][0]['orcid']=='0009-0001-9320-500X' and pub['author']=='Alec Kriebel' and metadata['license']['id']=='cc-by-4.0','author ORCID and CC BY4')
root_custody=load(ROOT/clear['root_custody_receipt']);check(sha(ROOT/clear['root_custody_receipt'])==clear['root_custody_receipt_sha256'],'exact root custody receipt')
check(sha(ROOT/clear['root_review'])==clear['root_review_sha256'],'entire root proof receipt')
for entry in root_custody['final_family_seal_bindings_rehashed']:
 path=ROOT/entry['path'];check(path.stat().st_size==entry['bytes'] and sha(path)==entry['sha256'],'existing family binding '+entry['path'])
for role,v in pro['reviews'].items():
 check(sha(P/v['report'])==v['sha256']==clear['reviews'][role]['report_sha256'],role+' entire report exact')
 check(sha(P/v['verdict_file'])==v['verdict_sha256']==clear['reviews'][role]['verdict_sha256'] and v['verdict']==load(P/v['verdict_file']),role+' entire original custom object exact')
 check(v['root_disposition']==('SCOPE_COMPLETE' if role=='scope' else 'PASS'),role+' root disposition separate')
scope=pro['reviews']['scope']['verdict']
check(scope['mathematical_verdict'] is None,'scope mathematical verdict stays null')
if ID=='23390551':check(scope['publication_recommendation'] is None and pro['reviews']['analytic']['verdict']['publication_clearance'] is False and pro['reviews']['adversarial']['verdict']['publication_authorization_granted'] is False,'dipole original hold/custom fields unchanged')
else:check(scope['mathematical_clearance'] is scope['publication_clearance'] is scope['page_promotion_permission'] is False and pro['reviews']['analytic']['verdict']['publication_authority_granted'] is False,'Langlands original pending false flags unchanged')
candidate=P/binding['frozen_scope_content_path'];check(sha(candidate)==binding['frozen_scope_content_sha256'],'frozen held candidate unchanged')
asset_root=P/binding['asset_root_path']
for asset in binding['files']:
 name=asset.get('filename',asset.get('name'));path=asset_root/name;api=next(x for x in record['files'] if x['key']==name)
 check(path.stat().st_size==asset['bytes']==api['size'] and sha(path)==asset['sha256'] and hashlib.md5(path.read_bytes()).hexdigest()==asset['md5'] and api['checksum']=='md5:'+asset['md5'],'actual deposited asset '+name)
check(sha(asset_root/pub['pdf_filename'])==binding['pdf_sha256']==clear['pdf_sha256'] and sha(asset_root/pub['supplement_filename'])==binding['supplement_sha256']==clear['supplement_sha256'],'selected deposited PDF/ZIP exact root hashes')
reader=PdfReader(asset_root/pub['pdf_filename']);check(len(reader.pages)==pub['pdf_pages'] and all(len(x.extract_text().strip())>100 for x in reader.pages),'full selected PDF searchable pages')
members=[];readers=[]
def walk(data,base,container,layer):
 with zipfile.ZipFile(BytesIO(data)) as z:
  check(z.testzip() is None,'full ZIP CRC '+container)
  for item in z.infolist():
   if item.is_dir():continue
   b=z.read(item);path=base/item.filename
   check(path.read_bytes()==b,'all original extracted bytes '+container+'!'+item.filename)
   members.append({'container':container,'path':item.filename,'bytes':len(b),'sha256':digest(b),'layer':layer})
   if item.filename.lower().endswith('.pdf'):readers.append({'container':container,'path':item.filename,'sha256':digest(b),'pages':len(PdfReader(BytesIO(b)).pages)})
   if zipfile.is_zipfile(BytesIO(b)):walk(b,Path(str(path)+'.expanded'),container+'!'+item.filename,layer+1)
walk((asset_root/pub['supplement_filename']).read_bytes(),P/('sources/cache/extracted' if ID=='23390551' else 'sources/support'),pub['supplement_filename'],1)
check(len(members)==binding['archive_recursive_regular_member_occurrences'],'true recursive archive occurrence count')
check(max(x['layer'] for x in members)==binding['archive_layers'],'true archive layers')
if ID=='23390551':
 check(len({x['sha256'] for x in members})==170 and len(readers)==1 and readers[0]['sha256']==binding['archive_historical_reader_pdfs'][0]['sha256']!=binding['pdf_sha256'] and readers[0]['pages']==11,'true distinct historical reader and170 unique archive hashes')
else:check(len(readers)==1 and readers[0]['sha256']==binding['pdf_sha256'],'sole embedded nine-page reader equals standalone')
sections=load(O/'public-sections.json');copytext=(O/'PUBLIC_COPY.md').read_text();bib=(O/'citation.bib').read_text()
check(sections['bibtex']==bib and all(x in bib for x in [pub['title'],pub['version'],pub['doi'],pub['bibtex_note']]),'exact prepared citation/BibTeX')
check(pub['canonical_url']==sections['canonical_url']=='https://aleckriebel.com/research/'+pub['slug']+'/','exact final canonical specification')
for section in sections['sections']:
 check('## '+section['heading'] in copytext,'full section heading '+section['id'])
 for paragraph in section.get('paragraphs',[]):check(paragraph in copytext,'complete proposed paragraph '+section['id'])
 for link in section.get('links',[]):check(link['url'] in copytext,'complete proposed link '+section['id'])
for ref in pub['background']:check(all(ref[k] in copytext for k in ['title','url','note']),'complete credited reference '+ref['title'])
check(len(sections['sections'])==11 and sections['sections'][0]['paragraphs']==[pub['abstract']],'full original abstract and ordered eleven sections')
paper_section=next(x for x in sections['sections'] if x['id']=='paper');materials=next(x for x in sections['sections'] if x['id']=='materials')
check(paper_section['links'][1]['download'] is True and paper_section['iframe']['src']==pub['pdf_filename']+'#view=FitH' and materials['links'][0]['download'] is True,'explicit local PDF/ZIP downloads, open/original and same iframe specification')
check('AI tools were used extensively' in copytext and 'mutual agreement' in pub['collaboration'] and 'actual research and writing contributions' in pub['collaboration'],'AI and passive authorship disclosures')
check(not any(x in copytext.lower() for x in ['2026-10-25','25 october 2026','sha256','sha-256','root-clearance','custody-recheck','checks passed','replay_receipt','locator precision']),'no public private-audit narrative')
negative=[]
for pos in ['first','middle','final']:
 c=copy.deepcopy(pub);sentences=re.split(r'(?<=\.)\s+',c['abstract']);sentences.pop(0 if pos=='first' else len(sentences)//2 if pos=='middle' else -1);c['abstract']=' '.join(sentences);fail=content_checks(c,copy.deepcopy(pro));check('complete_original_abstract' in fail,'reject '+pos+' abstract truncation');negative.append({'case':pos+'_abstract_truncation','rejected_by':'complete_original_abstract'})
g=copy.deepcopy(pro);g['reviews']['scope']['verdict']['mathematical_verdict']='PASS';check('entire_original_custom_verdicts' in content_checks(pub,g),'reject rewritten original scope verdict');negative.append({'case':'rewritten_scope_status','rejected_by':'entire_original_custom_verdicts'})
g=copy.deepcopy(pro);g['source_receipt_record']['files'][0]['bytes']+=1;check('entire_original_receipt_objects' in content_checks(pub,g),'reject altered complete receipt entry');negative.append({'case':'altered_original_receipt_entry','rejected_by':'entire_original_receipt_objects'})
c=copy.deepcopy(pub)
if ID=='23390551':c['source_binding']['receipt_path']='sources/receipt.json';label='custom_original_paths_no_alias'
else:c['limitations']=[x.replace('remain UNKNOWN','are known to be unrelated') for x in c['limitations']];label='langlands_fixed_orbit_odd_cycle_all_partitions_unknown_overlap'
check(label in content_checks(c,pro),'reject source alias or false overlap clearance');negative.append({'case':'fabricated_receipt_alias' if ID=='23390551' else 'invented_overlap_clearance','rejected_by':label})
baseline=load(O/'frozen-inputs-before.json')['files'];after={path:{'bytes':Path(path).stat().st_size,'sha256':sha(Path(path))} for path in baseline};check(after==baseline,'all frozen original inputs unchanged')
write(O/'editorial-validation-20261025-01.json',{'utc':now(),'status':'PASS','completion_percent':95,'checks_passed':len(checks),'checks':checks,'negative_controls':negative,'archive_members':members,'archive_readers':readers,'mathematical_programs_executed':False,'website_rendered':False,'live_verified':False,'browser_verified':False,'native_sheet_aa_url':None})
write(O/'editorial-validation-20261025-01-custody-after.json',{'utc':now(),'status':'PASS','all_originals_unchanged':True,'frozen_files':after})
print(json.dumps({'record':ID,'status':'PASS','checks':len(checks),'archive_occurrences':len(members),'source_files_unchanged':len(baseline)}))
