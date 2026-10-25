"""Build narrow three-record production proposals and explicit private copies."""
from pathlib import Path
import json,hashlib,difflib,datetime,ast,warnings
O=Path(__file__).resolve().parent;R=O.parents[1];LIVE=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public');S=O/'public';IDS=['23204952','22983138','23409904']
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
def save(n,v):
 p=O/n;p.parent.mkdir(exist_ok=True,parents=True);p.write_text(v if isinstance(v,str) else json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def diff(n,a,b,an,bn):save(n,''.join(difflib.unified_diff(a.splitlines(True),b.splitlines(True),fromfile=an,tofile=bn)))
configs={rid:json.loads((R/'papers'/rid/'publication.json').read_text()) for rid in IDS};pins={}
for rid,c in configs.items():
 p=R/'papers'/rid;g=json.loads((p/'promotion.json').read_text());b=c['source_binding']
 pins[rid]={k:sha(f) for k,f in [('publication',p/'publication.json'),('promotion',p/'promotion.json'),('science',R/g['root_clearance_file']),('editorial',R/f'verification/root-editorial-{rid}-20261025.json'),('receipt',p/b['receipt_path']),('metadata',p/b['metadata_path']),('record',p/b['record_path']),('tex',p/b['source_tex_path']),('seal',p/'reviews/editorial/SEAL.json')]}
 pins[rid].update(metadata_path=b['metadata_path'],record_path=b['record_path'],created=b['record_created_utc'],pages=c['pdf_pages'])
 if rid=='23204952':pins[rid]['raw_api']=sha(p/'sources/record/api.raw.json')
helper=(O/'cfh_source.py').read_text();marker='PINS = {}  # Replaced by the private proposal builder with exact frozen pins.'
if marker in helper:helper=helper.replace(marker,'PINS = '+repr(pins));save('cfh_source.py',helper)
else:assert ast.literal_eval(next(x.value for x in ast.parse(helper).body if isinstance(x,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='PINS' for t in x.targets)))==pins
diff('proposed-cfh-source.diff','',helper,'/dev/null','b/scripts/cfh_source.py')
changes=[]
def rep(s,a,b,count=1):
 assert s.count(a)==count,(a,s.count(a),count);changes.append((a,b,count));return s.replace(a,b)
old=(O/'inputs/render_page.py').read_text();render=rep(old,'from dipole_source import dipole_source_view','from dipole_source import dipole_source_view\nfrom cfh_source import CFH_IDS, cfh_source_view')
render=rep(render,"if paper.name == '23390551':","if paper.name in CFH_IDS:\n    raw_receipt, receipt, asset_root = cfh_source_view(paper, c, gate)\nelif paper.name == '23390551':")
for tup,count in [("('23444606','23440119','23224103','23390551','23430326')",3),("('23383961','23430906','23444606','23440119','23224103','23390551','23430326')",2)]:render=rep(render,tup,tup[:-1]+",'23204952','22983138','23409904')",count)
line=next(x for x in render.splitlines() if x.startswith('pdf_download='));render=rep(render,line,line.replace(" else ''"," or paper.name in CFH_IDS else ''"))
render=rep(render,"'23430326':'Read the complete 9-page paper in the on-page PDF reader.'","'23430326':'Read the complete 9-page paper in the on-page PDF reader.','23204952':'Read the complete 8-page paper in the on-page PDF reader.','22983138':'Read the complete 4-page paper in the on-page PDF reader.','23409904':'Read the complete 6-page paper in the on-page PDF reader.'")
render=rep(render,"pdf_reader_word='complete' if paper.name in ('23390551','23430326') else 'full'","pdf_reader_word='complete' if paper.name in ('23390551','23430326') or paper.name in CFH_IDS else 'full'\noriginal_pdf_download=' download' if paper.name in CFH_IDS else ''")
render=rep(render,'files/{h(c["pdf_filename"])}">Download the original','files/{h(c["pdf_filename"])}"{original_pdf_download}>Download the original')
material_condition="if paper.name in ('23383961','23430906','23444606','23440119','23224103','23390551','23430326','23204952','22983138','23409904'):"
new_material='''if paper.name in CFH_IDS:
    checksum_link='<li><a href="https://zenodo.org/records/22983138/files/SHA256SUMS">Zenodo original published checksum file (SHA256SUMS)</a></li>' if paper.name == '22983138' else ''
    sections+=f'<section id="materials"><h2>Supporting materials</h2><ul><li><a href="{h(c["supplement_filename"])}" download>{h(c["supplement_label"])}</a> · <a href="https://zenodo.org/records/{record_id}/files/{h(c["supplement_filename"])}">Zenodo original ZIP</a></li>{checksum_link}</ul></section>'
el'''+material_condition
render=rep(render,material_condition,new_material)
save('render_page.proposed.py',render);diff('proposed-shared-renderer.diff',old,render,'a/scripts/render_page.py','b/scripts/render_page.py');render_changes=changes[:];changes=[]
oldcheck=(O/'inputs/final-content-check.py').read_text();check=rep(oldcheck,'from dipole_source import dipole_source_view','from dipole_source import dipole_source_view\nfrom cfh_source import cfh_source_view, normalized_cfh_abstract')
check=rep(check,'DIPOLE_LANGLANDS_IDS=',"CFH_IDS={'23204952','22983138','23409904'}\nCFH_PINS="+repr(pins)+'\nDIPOLE_LANGLANDS_IDS=')
maps=''.join(' '+repr(rid)+':'+repr(configs[rid]['source_binding']['source_tex_path'].removeprefix('sources/'))+',\n' for rid in IDS)
check=rep(check," '23390551':'cache/",maps+" '23390551':'cache/")
check=rep(check,'def abstract_tokens(tex,record_id=None):\n','def abstract_tokens(tex,record_id=None):\n if record_id in CFH_IDS:return wt(normalized_cfh_abstract(record_id,tex))\n')
check=rep(check," if rid=='23390551':\n  gate=json.loads((p/'promotion.json').read_text());raw_receipt,receipt,asset_root=dipole_source_view(p,c,gate);receipt_file=p/c['source_binding']['receipt_path']"," if rid in CFH_IDS:\n  gate=json.loads((p/'promotion.json').read_text());raw_receipt,receipt,asset_root=cfh_source_view(p,c,gate)\n elif rid=='23390551':\n  gate=json.loads((p/'promotion.json').read_text());raw_receipt,receipt,asset_root=dipole_source_view(p,c,gate);receipt_file=p/c['source_binding']['receipt_path']")
check=rep(check,"'zenodo_record.json' if rid=='23390551' else", "c['source_binding']['record_path'].removeprefix('sources/') if rid in CFH_IDS else 'zenodo_record.json' if rid=='23390551' else")
check=rep(check,"if rid in SURREAL_CONE_BROWNIAN_IDS or rid in DIPOLE_LANGLANDS_IDS else c['author']","if rid in SURREAL_CONE_BROWNIAN_IDS or rid in DIPOLE_LANGLANDS_IDS or rid in CFH_IDS else c['author']")
check=rep(check,'unescape(h) if rid in SURREAL_CONE_BROWNIAN_IDS or rid in DIPOLE_LANGLANDS_IDS else h','unescape(h) if rid in SURREAL_CONE_BROWNIAN_IDS or rid in DIPOLE_LANGLANDS_IDS or rid in CFH_IDS else h')
check=rep(check,'and rid not in DIPOLE_LANGLANDS_IDS:','and rid not in DIPOLE_LANGLANDS_IDS and rid not in CFH_IDS:')
block=''' if rid in CFH_IDS:
  binding=c['source_binding'];pinned=CFH_PINS[rid];body=' '.join(unescape(re.sub(r'<[^>]+>',' ',re.search(r'<body>(.*?)</body>',h,re.S).group(1))).split())
  science=json.loads((R/gate['root_clearance_file']).read_text());editorial=json.loads((R/('verification/root-editorial-'+rid+'-20261025.json')).read_text())
  test('exact_approved_config_source_authority',sha(p/'publication.json')==pinned['publication']==gate['publication_sha256'] and sha(p/'promotion.json')==pinned['promotion'] and gate['root_clearance_record']==science and sha(R/gate['root_clearance_file'])==pinned['science'] and sha(R/('verification/root-editorial-'+rid+'-20261025.json'))==pinned['editorial'] and editorial['publication_sha256']==pinned['publication'] and editorial['promotion_sha256']==pinned['promotion'])
  test('complete_original_custom_verdicts',all(v['verdict']==json.loads((p/v['verdict_file']).read_text()) and sha(p/v['report'])==v['sha256']==science['reviews'][role]['report_sha256'] and sha(p/v['verdict_file'])==v['verdict_sha256']==science['reviews'][role]['verdict_sha256'] and v['root_authority_entry']==science['reviews'][role] for role,v in gate['reviews'].items()))
  test('complete_original_receipt_and_source_assets',raw_receipt==gate['source_receipt_record'] and binding['files']==gate['source_files']==raw_receipt['files'] and sha(receipt_file)==pinned['receipt'])
  test('exact_source_tex_path_and_bytes',textpath==p/binding['source_tex_path'] and sha(textpath)==binding['source_tex_sha256']==pinned['tex'])
  test('complete_original_abstract',a.strip()==binding['abstract_tex'] and normalized_cfh_abstract(rid,a)==c['abstract'] and c['abstract_is_original'] is True and len(c['abstract'].split('\\n\\n'))==1)
  test('original_abstract_heading',re.search(r'<section id="abstract"><h2>(.*?)</h2>',h).group(1)==c['abstract_heading']=='Original abstract')
  prepared=json.loads((p/'reviews/editorial/public-sections.json').read_text())
  test('all_approved_public_paragraphs',all(re.search(r'<section id="'+x['id']+r'"><h2>(.*?)</h2>',h).group(1)==x['heading'] and all(paragraph in body for paragraph in x.get('paragraphs',[]) if x['id']!='cite') for x in prepared['sections']))
  test('exact_prepared_bibtex_and_license',bib==(p/'reviews/editorial/citation.bib').read_text()==prepared['bibtex'] and art['license']=='https://creativecommons.org/licenses/by/4.0/' and any(t=='a' and x.get('href')==art['license'] for t,x in d.a))
  test('two_explicit_local_original_pdf_downloads',len([x for t,x in d.a if t=='a' and x.get('href')==c['pdf_filename'] and 'download' in x])==1 and len([x for t,x in d.a if t=='a' and x.get('href')=='https://zenodo.org/records/'+rid+'/files/'+c['pdf_filename'] and 'download' in x])==1 and any(t=='a' and x.get('href')==c['pdf_filename'] and 'download' not in x for t,x in d.a))
  test('one_selected_unchanged_reader_and_complete_zip',len(frames)==1 and len(texts)==c['pdf_pages']==pinned['pages'] and sha(f.parent/c['pdf_filename'])==binding['pdf_sha256']==science['pdf_sha256'] and sha(f.parent/c['supplement_filename'])==binding['supplement_sha256']==science['supplement_sha256'] and {x.name for x in f.parent.iterdir() if x.is_file()}=={'index.html','citation.bib',c['pdf_filename'],c['supplement_filename']} and c['additional_assets']==[])
  test('complete_local_original_zip_links',all(any(t=='a' and x.get('href')==url for t,x in d.a) for url in [c['supplement_filename'],'https://zenodo.org/records/'+rid+'/files/'+c['supplement_filename']]))
  test('edition_chronology',record['version']==c['version']==science['reviewed_zenodo_version'] and c['publication_date']==science['publication_date'] and c['source_binding']['record_created_utc']==pinned['created'] and c['edition_note'] in body and 'Manuscript and declared publication date <time' in h)
  test('no_manufactured_publication_gates_or_followup',gate['rendered_copy_verified'] is gate['live_verified'] is gate['browser_verified'] is False and gate['native_sheet_aa_url'] is None and gate['follow_up'] is c['follow_up'] is science['follow_up'] is None and all(x in body for x in ['used extensively','human or journal peer review','formal proof-assistant certification','actual research and writing contributions','mutual agreement']))
  with zipfile.ZipFile(asset_root/c['supplement_filename']) as archive:
   members=[x for x in archive.infolist() if not x.is_dir()];readers=[x for x in members if x.filename.lower().endswith('.pdf')]
   test('all_original_archive_members',len(members)==binding['archive_regular_file_count'] and all((p/'sources/published-source'/x.filename).read_bytes()==archive.read(x) for x in members) and not any(x.filename.lower().endswith(('.zip','.tar','.gz')) for x in members))
   test('archive_reader_identity',not readers if rid=='23204952' else len(readers)==1 and archive.read(readers[0])==(asset_root/c['pdf_filename']).read_bytes())
  if rid=='23204952':
   test('cubic_full_declared_scope_and_dependencies',all(x in body for x in ['every irreducible normal finite quasi-étale cover','I=±J','n≥5','every dimension 2≤k≤n','G_n(ℂ)/⟨σ⟩','including across their singular loci','principal external inputs','complete proofs are not freshly recertified','full chapter proof has not been accessed','stronger result of Kong, Shen, Zhao and Zhao']))
   test('cubic_original_null_scope_history',gate['reviews']['scope']['verdict']['mathematical_verdict'] is None and gate['reviews']['scope']['verdict']['promotion_decision'] is None)
  elif rid=='22983138':
   test('fps_full_universal_equality_and_prior_credit',all(x in body for x in ['n≥1 and r>0','‖v‖₂≥r for every actual extreme point','C₂(K)≥[r²+(n+1)‖g_K‖₂²]/(n+2)','need not be regular','centroid need not be the origin','finite body-dependent strictness witness','FPS already proved the inequality, simplex moments, finite vertex decomposition and common-centroid rigidity for polytopes']))
   checksum=p/'sources/SHA256SUMS';test('fps_third_published_checksum_original_link',checksum.stat().st_size==170 and sha(checksum)==binding['published_checksum_sha256']==science['additional_public_checksum_file_sha256'] and any(t=='a' and x.get('href')=='https://zenodo.org/records/22983138/files/SHA256SUMS' for t,x in d.a) and len(receipt['files'])==3 and not (f.parent/'SHA256SUMS').exists())
  else:
   test('hessian_full_proper_positive_ordered_torsion_scope',all(x in body for x in ['one fixed finite dimension n≥1','N=binomial(2n+4,3)>n','one smooth Ψ:U→ℝ with positive ordinary Hessian','proper smooth embedding f:M→U','exactly ∇ and ∇*, in that order','if and only if both prescribed torsions vanish','nonconvex and incomplete','dual affine coordinates are local','no fixed finite probability model','final Lê 2006','final Lê 2007','separate Lauritzen Lancaster','Abe article']))
   test('hessian_full_four_receipts_two_actual_assets',len(raw_receipt['files'])==4 and len(receipt['files'])==2 and sum(x['actual_file_object'] is None for x in raw_receipt['files'])==2 and not (p/'sources/record.json').exists())
'''
save('new-record-checks.block.txt',block);check=rep(check," result['papers'][rid]={'checks':checks,",block+" result['papers'][rid]={'checks':checks,")
save('final-content-check.proposed.py',check);diff('proposed-shared-checker.diff',oldcheck,check,'a/verification/final-content-check.py','b/verification/final-content-check.py')
save('reversible-proposal-edits.json',dict(renderer=render_changes,checker=changes))
for name,base,proposal,edits in [('renderer',old,render,render_changes),('checker',oldcheck,check,changes)]:
 restored=proposal
 for a,b,n in reversed(edits):assert restored.count(b)==n;restored=restored.replace(b,a)
 assert restored==base
stage=render.replace('ROOT = Path(__file__).resolve().parents[1]','ROOT = Path('+repr(str(R))+')').replace("SITE = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public/research')",'SITE = Path('+repr(str(S/'research'))+')')
save('render_page.stage.py',stage);diff('renderer-staging-overrides.diff',render,stage,'production proposal','private ROOT/SITE overrides')
stage=check.replace("sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))",'sys.path.insert(0, '+repr(str(O))+')\nsys.path.append('+repr(str(R/'scripts'))+')').replace('R=Path(__file__).resolve().parents[1]','R=Path('+repr(str(R))+')')
save('final-content-check.stage.py',stage);diff('checker-staging-overrides.diff',check,stage,'production proposal','private ROOT/import overrides')
for rel in ['research/index.html','research/sitemap.xml','research/research.css','robots.txt','index.html','blog/index.html','favicon.ico']:
 f=S/rel;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes((LIVE/rel).read_bytes())
for name in ['cfh_source.py','render_page.proposed.py','render_page.stage.py','final-content-check.proposed.py','final-content-check.stage.py']:
 with warnings.catch_warnings(record=True) as caught:warnings.simplefilter('always');compile((O/name).read_text(),name,'exec')
 assert not caught,[str(x.message) for x in caught]
save('proposal-static-checks.json',dict(status='PASS',exact_current_script_recovered_by_reversing_changes=True,new_helper_restricted_records=IDS,production_private_path_free=all(str(O) not in (O/n).read_text() for n in ['cfh_source.py','render_page.proposed.py','final-content-check.proposed.py']),unchanged_existing_helpers={n:sha(R/'scripts'/n) for n in ['published_assets.py','bosonic_source.py','dipole_source.py']}))
with (O/'RESEARCH_LOG.md').open('a') as f:f.write(datetime.datetime.now(datetime.timezone.utc).isoformat()+' — 40%: Complete narrow production helper/renderer/checker proposals and explicit private execution overrides built. Exact edit reversal recovers both actual current consumers. No shared mutation.\n')
print('Three-record proposals built')
