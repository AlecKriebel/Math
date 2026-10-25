"""Verify rendered research content. Supported source layouts are listed in TEX_PATHS.
Uses Python standard library plus an existing pdftotext executable; installs nothing.
"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,urljoin,unquote
import json,hashlib,re,datetime,subprocess,zipfile,gzip,tarfile,zlib,unicodedata,argparse,sys
from html import unescape
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
from published_assets import PublishedAssets, asset_name
parser=argparse.ArgumentParser(description='Read-only generated research-page checks; only QA reports are written.')
parser.add_argument('record_ids',nargs='*',default=['23539283','23577484'])
parser.add_argument('--site',type=Path,default=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public'))
parser.add_argument('--output-stem',default='final-content-check')
args=parser.parse_args()
if not re.fullmatch(r'[a-zA-Z0-9_-]+',args.output_stem):parser.error('output-stem must be a simple filename stem')
R=Path(__file__).resolve().parents[1]
S=args.site
TEX_PATHS={
 '23539283':'published-source/free-product-tensor-core-verification/manuscript/main.tex',
 '23577484':'published-source/main.tex',
 '23310484':'published-source/manuscript.tex',
 '23331395':'published-source/paper.tex',
 '22770864':'published-source/kourovka_16_63/report/kourovka_16_63.tex',
 '22729537':'published-source/NMSC_Paper_A_Source/manuscript/main.tex',
 '21699161':'related-records/21699181/published-source/main.tex',
 '22089551':'published-source/bimolecular_positive_recurrence_submission_v1_2_4/manuscript/paper_content.tex',
 '22729545':'published-source/NMSC_Paper_B_Source/manuscript/main.tex',
 '23441523':'published-source/main.tex',
 '23356680':'published-source/note.tex',
 '23445342':'published-source/main.tex',
 '23387753':'published-source/note.tex',
 '23352246':'published-source/rational_mixed_integer_bipartite_covers_v1/research_note.tex',
 '23414025':'published-source/note.tex',
 '23390181':'published-source/note.tex',
 '23410944':'published-source/paper.tex',
 '23422055':'published-source/paper/note.tex',
 '23203334':'published-source/source-and-verification/main.tex',
 '22929486':'published-source/kourovka_16_45/proof.tex',
 '23088066':'published-source/paper.tex',
 '23353160':'published-source/grassmann_calibrations_v1/research_note.tex',
 '23147866':'w4_locc_dense_coding.tex',
 '23157237':'published-source/spectral-tensor-consistency/spectral_tensor_consistency.tex',
 '22729355':'published-source/Exact_Diffusion_Design_Source_v1.0.11/main.tex',
 '22136869':'published-source/k2p-k3p-theta-collision-19cf11f65ed4/combined-paper-clarified.tex',
 '23180194':'published-source/mass_stationarity_verification/paper.tex',
 '23127646':'published-source/biconstrained-asymmetry-verification/biconstrained-asymmetry-verification/biconstrained_asymmetry.tex',
 '23191301':'published-source/odd_power_sos_verification/paper.tex',
 '23127955':'published-source/paper.tex',
 '23430642':'published-source/rank_one_uniqueness_v1_0/paper.tex',
 '23387814':'published-source/seshadri_counterexample_verification/seshadri_counterexample.tex',
}
GAME_SESHADRI_IDS={'23430642','23387814'}
def normalized_game_seshadri_abstract(rid,body):
 if rid=='23430642':
  body=body.replace(r'\rank(A+B)=1','rank(A + B) = 1').replace('\\PART\\','Partition').replace('$','')
 elif rid=='23387814':
  replacements={r'$\eps(S,L;x)\ge (2+|K_S^2|^{1/4})^{-1}$':'ε(S,L;x) ≥ (2+|K_S²|^(1/4))⁻¹',r'$d\ge7$':'d ≥ 7',r'$K_S^2=6(d-1)(d-3)$':'K_S² = 6(d−1)(d−3)','$L$':'L','$L^2=6$':'L² = 6',r'$\eps(S,L;x)\le1/(d-1)$':'ε(S,L;x) ≤ 1/(d−1)','$d=7$':'d = 7'}
  for old,new in replacements.items():body=body.replace(old,new)
 return ' '.join(body.split())
def tar_gz_integrity(path):
 """Read the complete gzip stream and tar members without extracting files."""
 try:
  with gzip.open(path,'rb') as stream:
   while stream.read(1024*1024):pass
  with tarfile.open(path,'r:gz') as archive:
   for member in archive:
    if member.isfile():
     with archive.extractfile(member) as stream:
      while stream.read(1024*1024):pass
  return True
 except (OSError,EOFError,tarfile.TarError,zlib.error):return False
OCTOBER_EDITOR_IDS={'23127646','23191301'}
def normalized_october_abstract(rid,body):
 body=body.replace('$','')
 if rid=='23127646':
  for old,new in [(r'\psi','ψ'),(r'\theta','θ'),(r'\geq','≥')]:body=body.replace(old,new)
  body=body.replace('ψ(x,y)','ψ(x, y)').replace('|ψ(13/27,14/27)-ψ(14/27,13/27)|≥','|ψ(13/27, 14/27) − ψ(14/27, 13/27)| ≥').replace('ψ(1-θ,θ)=1-θ/d(θ)','ψ(1 − θ, θ) = 1 − θ/d(θ)')
 elif rid=='23191301':
  body=body.replace('q=3','q = 3').replace(r'3\cdot10^{62}','3 · 10^62').replace(r'q\ge3','q ≥ 3').replace(r'220\times220','220 × 220')
 return ' '.join(body.split())
ADDED_IDS={'23203334','22929486','23088066','23353160','23147866','23157237','22729355'}
def decode_added_abstract(tex):
 tex=tex.replace(r'Rei\ss{}','Reiß').replace('$L^2$','L²')
 for old,new in {r'\ge':'≥',r'\sum':'∑',r'\chi':'χ',r'\Theta':'Θ',r'\sqrt n':'√n','n-1':'n−1','n-2':'n−2','n-3':'n−3'}.items():tex=tex.replace(old,new)
 for old,new in {r'\mup':'μ′',r'\Sep':'Sep',r'\mathbb R^{12}':'R¹²',r'K\"ahler':'Kähler','Bru\\ss\\':'Bruß',r'\hbin':'h₂',r'\ldots':'…','C_{4,12}':'C₄,₁₂',r'C_b^\infty\cap L^2':'C_b^∞ ∩ L²',r'e_a e_b/m_a':'eₐe_b/mₐ'}.items():tex=tex.replace(old,new)
 return tex.replace(r'\[','').replace(r'\]','').replace('$','').replace('--','–').replace("'",'’')
LATEX_WORDS={r'\omega':'ω',r'\delta':'δ',r'\log':'log',r'\geq':'≥',r'\simeq':'≃',r'\PP':'P',r'\dim':'dim',r'\Aut':'Aut',r'\qquad':' ',r'\emph':'',r'\CCR':'CCR',r"V\'ertesi":'Vértesi',r'\times':'×'}
def abstract_tokens(tex,record_id=None):
 if record_id in GAME_SESHADRI_IDS:return wt(normalized_game_seshadri_abstract(record_id,tex))
 if record_id in ADDED_IDS:tex=decode_added_abstract(tex)
 if record_id in OCTOBER_EDITOR_IDS:tex=normalized_october_abstract(record_id,tex)
 if record_id=='23180194':tex=tex.replace(r'\xi','ξ').replace('$','').replace('--','–')
 if record_id=='23127955':tex=tex.replace(r'\R^3','ℝ³').replace('$','').replace('~',' ')
 tex=tex.replace(r"Krej\v{c}\'i\v{r}\'ik",'Krejčířík')
 tex=tex.replace('K_4','K₄').replace(r'\sqrt','√')
 tex=tex.replace(r'\Z^d','Zᵈ').replace(r'\ZZ','Z').replace(r'\Z','Z').replace(r'\textbf','').replace(r'H\"aggstr\"om','Häggström')
 tex=re.sub(r'\\ge(?![A-Za-z])','≥',tex)
 tex=re.sub(r'\\(g|n|to)(?![A-Za-z])',lambda m:{'g':'g','n':'n','to':'→'}[m.group(1)],tex).replace('j_1','j₁').replace('j_2','j₂')
 for old,new in LATEX_WORDS.items():tex=tex.replace(old,new)
 commands=re.findall(r'\\[A-Za-z]+',tex)
 if commands:raise ValueError('Unrecognized abstract TeX commands: '+repr(commands))
 return wt(tex)
def normalized_kimura_abstract(tex):
 return '\n\n'.join(' '.join(p.split()) for p in re.split(r'\n\s*\n',tex.replace('$','').replace('~',' ').replace('--','–').strip()))
class Doc(HTMLParser):
 def __init__(self,p):
  super().__init__();self.a=[];self.text=[];self.feed(p.read_text())
 def handle_starttag(self,t,a):self.a.append((t,dict(a)))
 def handle_data(self,t):self.text.append(t)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def wt(t):return re.findall('[A-Za-z0-9]+|[\u0370-\u03ff]',unicodedata.normalize('NFKC',t))
result={'time':datetime.datetime.now(datetime.timezone.utc).isoformat(),'papers':{},'issues':[]}
index=(S/'research/index.html').read_text(); sitemap=(S/'research/sitemap.xml').read_text()
for rid in args.record_ids:
 p=R/'papers'/rid;c=json.loads((p/'publication.json').read_text());f=S/'research'/c['slug']/'index.html';h=f.read_text();d=Doc(f);base='https://aleckriebel.com/research/'+c['slug']+'/';checks={}
 def test(k,v):
  checks[k]=bool(v)
  if not v:result['issues'].append(rid+': '+k)
 meta={a.get('name',a.get('property')):a.get('content') for t,a in d.a if t=='meta'}
 test('title',unescape(re.search('<title>(.*?)</title>',h).group(1))==c['title']+' | Alec Kriebel')
 for k,v in {'description':c['description'],'citation_title':c['title'],'citation_author':c['author'],'citation_publication_date':c['publication_date'].replace('-','/'),'citation_doi':c['doi'],'citation_pdf_url':base+c['pdf_filename'],'citation_author_orcid':'0009-0001-9320-500X','og:title':c['title'],'og:description':c['description'],'og:url':base,'article:published_time':c['publication_date']}.items():test(k,meta[k]==v)
 test('canonical',[a['href'] for t,a in d.a if t=='link' and a.get('rel')=='canonical']==[base])
 schemas=[json.loads(x) for x in re.findall('<script type="application/ld\\+json">(.*?)</script>',h,re.S)]
 art=next(x for x in schemas[0]['@graph'] if x['@type']=='ScholarlyArticle')
 test('jsonld',all(art[k]==c[k] for k in ['description','abstract','version']) and art['name']==c['title'] and art['datePublished']==c['publication_date'] and art['sameAs']=='https://doi.org/'+c['doi'] and art['encoding']['contentUrl']==base+c['pdf_filename'] and art['author'][0]['name']==c['author'] and art['identifier']['value']==c['doi'])
 for sec,key in [('abstract','abstract'),('plain-language','plain_language'),('result','result'),('proof','why_it_works'),('limits','limitations')]:
  segment=re.search('<section id="'+sec+'">(.*?)</section>',h,re.S).group(1)
  paras=[unescape(x) for x in re.findall('<p>(.*?)</p>',segment,re.S)]
  expected=c[key] if isinstance(c[key],list) else c[key].split('\n\n')
  test(sec,paras==expected)
 textpath=p/'sources'/TEX_PATHS[rid]
 source=textpath.read_text()
 abstract_source=source
 if rid=='22089551':
  branch=re.search(r'\\ifdefined\\japsubmission(.*?)\\else(.*?)\\fi',source,re.S)
  main_source=(textpath.parent/'main_arxiv.tex').read_text()
  test('non_jap_abstract_source_selected',branch is not None and r'\input{paper_content}' in main_source and 'japsubmission' not in main_source)
  abstract_source=branch.group(2)
 a=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',abstract_source,re.S).group(1)
 test('abstract_full_source_words',abstract_tokens(a,rid)==wt(c['abstract']))
 if rid in GAME_SESHADRI_IDS:
  test('abstract_full_source_text',normalized_game_seshadri_abstract(rid,a)==c['abstract'])
  test('abstract_full_source_word_count',len(c['abstract'].split())=={'23430642':140,'23387814':97}[rid])
  test('abstract_source_paragraphs',len(re.split(r'\n\s*\n',a.strip()))==len(c['abstract'].split('\n\n')))
 if rid=='22136869':
  test('abstract_full_source_text',normalized_kimura_abstract(a)==c['abstract'])
  test('abstract_source_paragraphs',len(re.split(r'\n\s*\n',a.strip()))==len(c['abstract'].split('\n\n')))
 if rid=='23180194':
  normalized_abstract=' '.join(a.replace(r'\xi','ξ').replace('$','').replace('--','–').split())
  test('abstract_full_source_text',normalized_abstract==c['abstract'])
  test('abstract_full_113_words',len(c['abstract'].split())==113)
  test('abstract_source_paragraphs',len(re.split(r'\n\s*\n',a.strip()))==len(c['abstract'].split('\n\n')))
 if rid in OCTOBER_EDITOR_IDS:
  test('abstract_full_source_text',normalized_october_abstract(rid,a)==c['abstract'])
  test('abstract_full_source_word_count',len(c['abstract'].split())=={'23127646':109,'23191301':123}[rid])
  test('abstract_source_paragraphs',len(re.split(r'\n\s*\n',a.strip()))==len(c['abstract'].split('\n\n')))
 if rid=='23127955':
  normalized_abstract=' '.join(a.replace(r'\R^3','ℝ³').replace('$','').replace('~',' ').split())
  test('abstract_full_source_text',normalized_abstract==c['abstract'])
  test('abstract_full_122_words',len(c['abstract'].split())==122)
  test('abstract_source_paragraphs',len(re.split(r'\n\s*\n',a.strip()))==len(c['abstract'].split('\n\n')))
 if rid in ADDED_IDS:
  compact=lambda text: re.sub(r'\s+','',unicodedata.normalize('NFKC',text))
  test('abstract_full_source_text',compact(decode_added_abstract(a))==compact(c['abstract']))
  test('abstract_source_paragraphs',len(re.split(r'\n\s*\n',a.strip()))==len(c['abstract'].split('\n\n')))
 if rid in ('23441523','23356680'):
  normalized_abstract=a.replace('$K_4$','K₄').replace('$3$','3').replace(r'$4+\sqrt{17}$','4 + √17').replace('--','–').replace('~',' ')
  test('abstract_full_source_text',' '.join(normalized_abstract.split())==' '.join(c['abstract'].split()))
  test('abstract_source_paragraphs',len(re.split(r'\n\s*\n',a.strip()))==len(c['abstract'].split('\n\n')))
 if rid in ('23445342','23387753','23352246'):
  normalized_abstract=a.replace(r'$\ZZ$','Z').replace(r'$\Z^d$','Zᵈ').replace(r'$d\ge2$','d ≥ 2').replace('$p<1$','p < 1').replace(r'\textbf{Priority qualification:}','Priority qualification:').replace(r'H\"aggstr\"om','Häggström').replace(r'\ ',' ').replace('$','').replace('~',' ').replace('--','–').replace("'",'’')
  test('abstract_full_source_text',' '.join(normalized_abstract.split())==' '.join(c['abstract'].split()))
  test('abstract_source_paragraphs',len(re.split(r'\n\s*\n',a.strip()))==len(c['abstract'].split('\n\n')))
 if rid=='23414025':
  normalized_abstract=a.replace(r'\(\g\)','g').replace(r'\(\n\)','n').replace(r'\(j_1,j_2:\g\to\n\)','j₁, j₂ : g → n')
  test('abstract_full_source_text',' '.join(normalized_abstract.split())==' '.join(c['abstract'].split()))
  test('abstract_source_paragraphs',len(re.split(r'\n\s*\n',a.strip()))==len(c['abstract'].split('\n\n')))
 if rid in ('23390181','23410944','23422055'):
  normalized_abstract=a.replace('$1/3<d<1$','1/3 < d < 1').replace("Kazhdan's","Kazhdan’s").replace(r"Krej\v{c}\'i\v{r}\'ik",'Krejčířík').replace('--','–')
  test('abstract_full_source_text',' '.join(normalized_abstract.split())==' '.join(c['abstract'].split()))
  test('abstract_source_paragraphs',len(re.split(r'\n\s*\n',a.strip()))==len(c['abstract'].split('\n\n')))
  printed_date=re.search(r'\\date\{([^}]+)\}',source).group(1)
  expected_dates={'23390181':r'October 15, 2026\quad (version 1.0.0)','23410944':r'15 October 2026\\ \small Research note, version 1.0','23422055':r'October 16, 2026 \quad Version 1.0'}
  test('printed_version_date',printed_date==expected_dates[rid] and c['source_binding']['manuscript_version']==c['version']==c['source_binding']['zenodo_version'])
 test('no_noindex','noindex' not in meta.get('robots',''))
 visible_text=''.join(d.text).lower()
 novelty_checked_text=visible_text.replace('does not certify worldwide first priority','').replace('does not establish worldwide first priority','')
 test('no_audit_replay',not any(x in novelty_checked_text for x in ['24 october 2026','october 24','audit completed','checks passed','worldwide first','first-ever']))
 test('no_followup',c['follow_up'] is None and 'id="further-research"' not in h)
 test('authorship_once',h.count('Authorship and responsibilities would be discussed in relation to the substantive contributions made.')==1)
 test('ai_disclosure',c.get('ai_disclosure','') in unescape(h))
 test('collaboration',c['collaboration'] in unescape(h))
 ids=[a['id'] for t,a in d.a if 'id' in a];test('unique_ids',len(ids)==len(set(ids)))
 local=[]
 for tag,attrs in d.a:
  for key in ['href','src']:
   if key not in attrs:continue
   u=urlsplit(urljoin(base,attrs[key]))
   if u.netloc!='aleckriebel.com':continue
   q=S/unquote(u.path).lstrip('/')
   if q.is_dir():q=q/'index.html'
   good=q.is_file()
   if good and q.suffix=='.html' and u.fragment:good=unquote(u.fragment) in [b['id'] for _,b in Doc(q).a if 'id' in b]
   local.append(good)
 test('local_links_anchors',all(local))
 receipt=json.loads((p/'sources/receipt.json').read_text()); hashes={'html':sha(f),'publication':sha(p/'publication.json')}
 resolver=PublishedAssets(p/'sources',receipt,c.get('source_binding',{}).get('embedded_assets',[]))
 assets=[(key,c[key]) for key in ['pdf_filename','supplement_filename'] if c.get(key)]
 assets += [('additional_asset_'+asset['filename'],asset['filename']) for asset in c.get('additional_assets',[])]
 for key,name in assets:
  original=resolver.resolve(name)
  actual=sha(f.parent/name);hashes[name]=actual
  test(key,actual==original.sha256 and name in [a.get('href') for t,a in d.a if t=='a'])
  if name.endswith('.zip'):
   with zipfile.ZipFile(f.parent/name) as z:test('zip_integrity_'+name,z.testzip() is None)
  if name.endswith('.tar.gz'):
   test('tar_gz_integrity_'+name,tar_gz_integrity(f.parent/name))
  if key.startswith('additional_asset_') and name.endswith('.pdf'):
   extra_text=subprocess.check_output(['/opt/homebrew/bin/pdftotext',str(f.parent/name),'-'],text=True).split('\f')
   if not extra_text[-1].strip():extra_text.pop()
   test('supplement_pdf_searchable_'+name,all(len(t.strip())>100 for t in extra_text))
   test('supplement_pdf_page_label_'+name,f'PDF, {len(extra_text)} pages' in h)
   if original.pages is not None:
    test('embedded_pdf_page_count_'+name,len(extra_text)==original.pages)
    label=next(x['label'] for x in c['additional_assets'] if x['filename']==name)
    test('embedded_pdf_individual_page_label_'+name,f'PDF, {len(extra_text)} pages' in label)
 texts=subprocess.check_output(['/opt/homebrew/bin/pdftotext',str(f.parent/c['pdf_filename']),'-'],text=True).split('\f')
 if not texts[-1].strip():texts.pop()
 test('pdf_searchable',all(len(t.strip())>100 for t in texts));test('page_count',f'PDF, {len(texts)} pages' in h)
 frames=[a for t,a in d.a if t=='iframe'];test('iframe',len(frames)==1 and frames[0]['src']==c['pdf_filename']+'#view=FitH' and bool(frames[0].get('title')))
 test('index_entry',f'href="/research/{c["slug"]}/"' in index and c['description'] in unescape(index))
 ix=json.loads(re.search('<script type="application/ld\\+json">(.*?)</script>',index,re.S).group(1));items=ix['mainEntity']['itemListElement'];test('index_jsonld',len([x for x in items if x['url']==base and x['name']==c['title']])==1 and ix['mainEntity']['numberOfItems']==len(items))
 test('sitemap',sitemap.count('<loc>'+base+'</loc>')==1)
 bib=(f.parent/'citation.bib').read_text();test('bibtex',all(x in bib for x in [c['title'],c['author'],c['doi'],c.get('bibtex_note','Unrefereed preprint, version '+c['version'])]))
 test('background_links',all(x['url'] in h and x['title'] in unescape(h) and x['note'] in unescape(h) for x in c['background']))
 record=json.loads((p/'sources/record.json').read_text())['metadata'];test('record_metadata',all(c[k]==record[k] for k in ['title','doi','publication_date']) and (c['version']==record['version'] if 'version' in record else rid in ('21699161','23203334') and c['source_binding']['zenodo_version'] is None))
 if c.get('edition_label'):test('edition_label',c['edition_label'] in unescape(h) and c['citation_edition_label'] in unescape(h) and c['edition_note'] in unescape(h))
 if c.get('related_resources'):
  materials=re.search('<section id="materials">(.*?)</section>',h,re.S).group(1)
  test('supporting_materials_links',all(x['url'] in materials and x['label'] in unescape(materials) and x.get('doi','') in unescape(materials) for x in c['related_resources']))
  related_bound=True
  for related in c['source_binding'].get('related_records',[]):
   rp=p/'sources/related-records'/related['record_id'];rr=json.loads((rp/'receipt.json').read_text())
   related_bound=related_bound and rr['record_id']==related['record_id'] and rr['files']==related['files']
   related_bound=related_bound and all(sha(rp/asset_name(x))==x['sha256'] for x in rr['files'])
  test('related_resource_source_bindings',related_bound)
 if (p/'promotion.json').exists():
  gate=json.loads((p/'promotion.json').read_text())
  test('promotion_pdf_binding',gate['status']=='PASS' and gate['pdf_sha256']==sha(p/'sources'/c['pdf_filename']))
  if gate.get('publication_sha256'):test('promotion_publication_binding',gate['publication_sha256']==sha(p/'publication.json'))
  if rid in ('23441523','23356680','23445342','23387753','23352246','23414025','23390181','23410944','23422055','23180194','23127955') or rid in ADDED_IDS or rid in OCTOBER_EDITOR_IDS:
   test('promotion_source_receipt_binding',gate['source_receipt_sha256']==sha(p/'sources/receipt.json'))
   test('promotion_review_bindings',all(v['sha256']==sha(p/v['report']) and v['verdict_sha256']==sha(p/v['verdict_file']) and v['verdict']==json.loads((p/v['verdict_file']).read_text()) for v in gate['reviews'].values()) and set(gate['reviews'])=={'analytic','adversarial','scope'})
  if rid in ADDED_IDS or rid in ('23180194','23127955') or rid in OCTOBER_EDITOR_IDS:
   test('all_published_source_assets_bound',gate['source_files']==receipt['files'] and all(sha(p/'sources'/asset_name(x))==x['sha256'] for x in receipt['files']))
 if rid=='23577484':test('commuting_fixed','elements that commute with the starting involution' in h and 'produces commuting elements' not in h);test('scope_complete',all(x in unescape(h) for x in ['[d/3, 2d/3]','independent, exactly uniform','sufficiently large','separately','0 < δ < 1']))
 if rid=='23310484':test('scope_complete',all(x in unescape(h) for x in ['finite simplicial complex','actual vertex set','Nevo and Wagner’s result for PL spheres already excludes arbitrary topological embeddings','d = 0']))
 if rid=='23331395':test('scope_complete',all(x in unescape(h) for x in ['smooth integral projective variety','arbitrary characteristic','one closed point','mult_x(ρ_*Γ)','inseparable degree']))
 if rid=='22770864':test('scope_complete',all(x in unescape(h) for x in ['full automorphism group','1009^52359','i ≥ 7','Lie-ring automorphism','awaiting confirmation by mathematicians','Omirov and Ruan','does not claim that G and Aut(G) are isomorphic']))
 if rid=='22729537':test('scope_complete',all(x in unescape(h) for x in ['population alignment laws indexed by locus length','stationary reversible','not a canonical species graph','incidence-separated','scalar-separator faithfulness','compact semianalytic','no practical numerical bound','L + 1']))
 if rid=='21699161':
  printed_date=re.search(r'\\date\{([^}]+)\}',source).group(1)
  test('printed_edition_archive_distinction',printed_date==c['version']==c['source_binding']['manuscript_date']=='July 2026' and c['archive_version_label']=='1.1.0' and 'version' not in record and 'Version July 2026' not in h and c['supplement_filename'] is None and len(c['related_resources'])==4)
  test('scope_complete',all(x in unescape(h) for x in ['shared-randomness convex hulls','dimension at most two','finite, input-dependent output alphabets','zero projectors','same-state simulation','Neither is claimed to be the exact global optimum','Vértesi and Bene established that phenomenon in 2010']))
 if rid=='22089551':test('scope_complete',all(x in unescape(h) for x in ['strictly positive rate constants','one linkage class','at most two molecules','unique on each reachable class','no closed-form or product-form formula','pure-species condition','supplementary-note-v1.2.4.pdf']))
 if rid=='22729545':
  test('scope_complete',all(x in unescape(h) for x in ['tree-child under every admissible rooting','surjective onto the terminal taxa','inheritance weights lie strictly between zero and one','distinct internal biological events have distinct ages','does not limit the entire network to two reticulations','Q1–Q8','not unique recovery of every raw event and parameter','one triple, three nucleotide sites or three observed genealogies','no effective practical sequence-length bound','compact semianalytic normalized finite-presentation charts','relies on the companion preprint']))
  test('abstract_verbatim_source',' '.join(a.split())==' '.join(c['abstract'].split()))
  companion=R/'papers/22729537/promotion.json'
  test('companion_gate_binding',gate['companion_import']['status']=='PASS' and gate['companion_import']['promotion_sha256']==sha(companion) and json.loads(companion.read_text())['status']=='PASS')
  test('all_four_published_materials',all(name in [x.get('href') for t,x in d.a if t=='a'] for name in ['NMSC_Paper_B_Main.pdf','NMSC_Paper_B_Supplement.pdf','NMSC_Paper_B_Source.zip','NMSC_Paper_B_Reproducibility.zip']))
 if rid=='23441523':
  test('scope_complete',all(x in unescape(h) for x in ['every nonempty input size','sequence of positive rational ε','total sample-plus-adjacency cost','complete positive rational weight vector','unordered changed vertex pairs','not a sample-only bound','does not imply polynomial running time','established two-sided triangle-testing lower bound of Alon and Shapira']))
  test('heavy_apex_distance_direction','new graph’s distance from P is exactly one quarter of the tail’s triangle-free distance' in unescape(h))
 if rid=='23356680':
  test('scope_complete',all(x in unescape(h) for x in ['every Lipschitz domain Ω compactly contained in U','Competitors need not be continuous','positive area','not Korevaar–Schoen harmonic','not a global minimizer','complete metric target','4 + √17','2√2 + √6','revised journal body was not available','neither unchanged final wording nor continued open status','First priority and optimal constants are not claimed']))
  test('pinned_question_history',any(x['url']=='https://arxiv.org/abs/2503.08553v1' for x in c['background']))
 if rid=='23445342':
  test('scope_complete',all(x in unescape(h) for x in ['fixed iid space-time environment law','every deterministic real sequence M_N','uniformly in each deterministic alignment','twice the usual total variation distance','may diverge nonmonotonically and arbitrarily slowly','not a simultaneous assertion for partitions selected after observing the environment','Novelty and historical priority remain unresolved','four relevant older original full texts could not be accessed']))
  test('credited_methods',all(x in unescape(h) for x in ['Dunlap–Gu','Barraquand–Rychnovsky','auxiliary polynomial rate']))
 if rid=='23387753':
  test('scope_complete',all(x in unescape(h) for x in ['ordinary finite energy','every integer d ≥ 2','Finite components are allowed','quenched: X is fixed','internal site thresholds','maximum finite-side size','connected one-ended spanning tree','not the induced bond graph','factor-of-iid','No first-priority claim']))
  test('credited_planar_antecedent',all(x in unescape(h) for x in ['planar perturbation mechanism is due to Häggström and Mester','additional bounded-cutset deduction']))
 if rid=='23352246':
  test('scope_complete',all(x in unescape(h) for x in ['Variables have unrestricted signs','total binary encoding','Dimension, integer-coordinate count and denominators may all vary','integral improving recession direction','actual convex hull conv(S) is a closed rational polyhedron','including boundary points','width at most 2n','at most 2n|I| nodes','two integer coordinates','separate subtree-hull Conjecture 2 remains unaddressed','not claim an algorithm for arbitrary unencoded real data','not implement the full polynomial-time']))
  test('credited_classical_methods',all(x in unescape(h) for x in ['Classical mixed proximity','hybrid partial minimization','ring-family submodular minimization','exact optimization–separation']))
 if rid=='23414025':
  test('scope_complete',all(x in unescape(h) for x in ['same finite dimension','tr(ad_g x) = 0','n is semisimple','invertible linear difference','zero-dimensional case is included','Remark 4 supplies','merely reductive target is not covered','not asserted to be a group homomorphism','nilpotent targets are outside','original body of Onishchik’s 1969 decomposition paper was not accessible']))
  test('credited_classical_methods',all(x in unescape(h) for x in ['predecessor in Baues’s work','established pair j₁ = R + I and j₂ = R','holomorphic identity theorem','stabilizer is closed and discrete']))
 if rid=='23390181':
  test('scope_complete',all(x in unescape(h) for x in ['n ≥ 3','nonempty finite inverse-closed generating sets','Words are not identified under rotation or inversion','independent uniform elements of Sℓ with replacement','through all integers','factors, alphabets and density remain fixed','at most two','distinct sampling law','d = 1/3','not infinitude or factor embeddings','earlier collapse theorem already covers d > one-half']))
  test('credited_established_program',all(x in unescape(h) for x in ['Montee and Steenbock','almost-equal blocks','common-suffix finite-index','triangular-link criterion','Tropp','independent whole-relator Laplacians']))
 if rid=='23410944':
  test('scope_complete',all(x in unescape(h) for x in ['every integer d ≥ 2','connected open quasi-conical set','H₀¹(Ω)','closure of the point spectrum','Both cube widths and window widths are chosen inductively','zero-thickness interface screens','without explicit numerical bounds','not asserted to equal the whole half-line','It does not mean an isolated sequence of eigenvalues or compact resolvent']))
  test('credited_spectral_antecedents',all(x in unescape(h) for x in ['Krejčířík and Lotoreichik','Hempel, Seco and Simon','not a new general principle','does not certify historical first priority']))
 if rid=='23422055':
  test('scope_complete',all(x in unescape(h) for x in ['at least three independent','one fixed coordinate ball','Three fixed, linearly independent classes','h⁻_Jε ≥ 3','not an exact dimension','unrestricted compact-four-manifold integrability conjecture','real dimension two','no common positive compatible metric','not closed']))
  test('credited_geometry_antecedents',all(x in unescape(h) for x in ['prior work of Tan–Wang–Zhang–Zhu','pluricanonical sections','different invariant','bounded comparison does not certify exhaustive novelty']))
 if rid=='23203334':
  test('scope_complete',all(x in unescape(h) for x in ['Fix a finite number of species in three space dimensions','positive mass and a real charge, including zero charge','compact support in position and momentum','every spatial derivative is bounded','Maxwell divergence constraints','smooth on every finite time interval','No smallness, symmetry or neutrality condition','No uniform infinite-species or zero-mass limit','pinned OpenAI family 362','no independently reproduced proof-assistant certificate'.capitalize()]))
  test('no_invented_numbered_version','version' not in record and c['source_binding']['manuscript_version'] is None and 'Version 6 October' not in h and c['edition_label']=='Manuscript dated 6 October 2026')
  extra=gate['additional_reviews']['primary_adversarial'];gap=gate['gap_resolution'];old=gate['reviews']['adversarial']['verdict']
  test('additional_primary_review_binding',extra['sha256']==sha(p/extra['report']) and extra['verdict_sha256']==sha(p/extra['verdict_file']) and extra['verdict']==json.loads((p/extra['verdict_file']).read_text()) and extra['verdict']['status']=='PASS')
  test('conditional_review_preserved',old['status']=='conditional_multispecies_transfer_supported_upstream_global_verification_incomplete' and old['disposition']=='verification_coverage_dependency_hold' and old['unconditional_global_theorem_independently_verified'] is False)
  test('root_gap_resolution_binding',gate['disposition_by']=='root' and gap['additional_review_key']=='additional_reviews.primary_adversarial' and gap['additional_report_sha256']==extra['sha256'] and gap['additional_verdict_sha256']==extra['verdict_sha256'] and gap['upstream_pdf_sha256']==extra['verdict']['upstream']['pdf_sha256'] and gap['upstream_commit']==extra['verdict']['upstream']['commit'])
 if rid=='22929486':
  test('scope_complete',all(x in unescape(h) for x in ['G = F₂₉² ⋊ H','100920','b_f(G) = b(G) = 3 and μ′(G) = 4','inclusion-minimal','faithful and nonfaithful','not claimed to have the smallest','characteristic-11','not a journal acceptance']))
  test('notebook_confirmation_scoped',all(x in unescape(h) for x in ['reports confirmation by P. J. Cameron','distinct from journal publication']) and c['external_status']['doi_cited']==c['doi'] and c['external_status']['url'] in h)
 if rid=='23088066':
  test('scope_complete',all(x in unescape(h) for x in ['e_PL(K) = 3','e_lin(K) = 5','first barycentric subdivision','need not be arithmetic barycenters','including nongeneric placements','n = 2²⁵⁶','not a displayed small model','no explicit list of facets','need not be a surface or manifold']))
  test('credited_embedding_antecedents',all(x in unescape(h) for x in ['Brehm–Sarkaria','Newman','Lee–Nevo','withdrawn odd-dimensional claim']))
 if rid=='23353160':
  test('scope_complete',all(x in unescape(h) for x in ['C₄,₁₂','including both orientations','normalized complex Sep(3,3)','arbitrary auxiliary variables and affine equalities','affine-linear polynomials modulo the full real vanishing ideal','coefficients of the unnormalized ℓ can be rational','No coefficient list, exact comass','No claim is made that this is the least dimension']))
  test('credited_nonrepresentability_antecedents',all(x in unescape(h) for x in ['Fawzi’s established result','prior tensor-to-wedge lemma','Question 6.5','not the failing form']))
 if rid=='23147866':
  test('scope_complete',all(x in unescape(h) for x in ['independent uniformly distributed messages','R₁ < 3/2, R₂ < 3/2','vanishing uniform average decoding error','A₁B₁ : A₂B₂','R₁ = R₂ = 9/8','lower bound on the optimal LOCC capacity','not a one-copy advantage','Zero-error and maximal-error coding are not established','no extra shared entanglement']))
  test('eight_files_no_invented_zip',len(receipt['files'])==8 and all(not asset_name(x).endswith('.zip') for x in receipt['files']) and c['supplement_filename'] is None and 'Source and verification (ZIP)' not in h)
  links=[a['href'] for t,a in d.a if t=='a' and 'href' in a]
  test('all_eight_original_files_linked',all(any(link==asset_name(x) or '/files/'+asset_name(x) in link for link in links) for x in receipt['files']))
 if rid=='23157237':
  test('scope_complete',all(x in unescape(h) for x in ['known bounded connected C∞ domain','d ≥ 2','L = μ⁻¹ div(S∇)','conormal reflection n·S∇u = 0','stationary exact positions','every positive empirical eigenpair','Fourth powers of the transition eigenvalues','Any strictly positive deterministic ridge sequence tending to zero','separately fitted vector','density estimate converges in C² on the closure','globally in L²(D)','not a claim about differentiating the estimated tensor']))
  test('scope_limits_preserved',all(x in unescape(h) for x in ['Ordinary normal reflection is not an interchangeable','No convergence rate, finite-sample guarantee','different estimator obtained from classical variational regularization','does not prove consistency of the main spectral fit']))
  test('metadata_printed_version_distinction',record['version']==c['version']=='1.0' and c['source_binding']['manuscript_version'] is None and r'\date{October 5, 2026}' in source and c['edition_label']=='Zenodo version 1.0')
 if rid=='22729355':
  test('scope_complete',all(x in unescape(h) for x in ['For every n ≥ 4','every positive-equilibrium realization','d_Z > 8h_Z ∑_{j=2}^{n−2} d_j/h_j','strictly positive diffusion coefficients','not attained','χ_Dχ_H > 8(n−3)','one-dimensional Neumann interval','locally exponentially stable in H¹','fixed-integrated-mass class defined by the semipositive conservation law','Both contrasts are Θ(√n)']))
  test('scope_limits_preserved',all(x in unescape(h) for x in ['networks are synthetic','stationary zero-eigenvalue crossings','conserved quantity has zero weight on X₁','do not give global attraction','exponent-optimal only within this topology','does not claim intrinsic finite wavelength selection']))
  test('printed_month_edition_date_distinction',record['version']==c['version']=='1.0.11' and record['publication_date']=='2026-09-12' and c['source_binding']['manuscript_date']=='August 2026' and r'\date{August 2026}' in source and c['edition_label']=='Zenodo version 1.0.11')
  test('both_reader_pdfs_labelled',len(texts)==19 and 'Mathematical supplement (PDF, 19 pages)' in unescape(h))
  links=[a['href'] for t,a in d.a if t=='a' and 'href' in a]
  test('all_eight_published_assets_linked',len(receipt['files'])==8 and all(any(link==asset_name(x) or '/files/'+asset_name(x) in link for link in links) for x in receipt['files']))
  test('companion_software_doi_distinct','https://doi.org/10.5281/zenodo.22625980' in links and c['doi']=='10.5281/zenodo.22729355')
 if rid=='22136869':
  test('scope_complete',all(x in unescape(h) for x in ['proper lower-dimensional subset','generic choice of parameters on the network is not tree-equivalent','theta admits no tree-child rooting','network multispecies coalescent','Jukes–Cantor tree–network theorem','no clock or global timing','one chosen vertex','fixed theta maps have ambient ranks 9 under K2P and 15 under K3P']))
  test('record_manuscript_edition_distinction',record['version']==c['version']=='1.2.6' and record['publication_date']==c['publication_date']=='2026-08-28' and c['source_binding']['manuscript_version']=='1.2.7' and c['source_binding']['manuscript_date']=='August 2026' and r'\date{August 2026}' in source and 'v1.2.7' in source and '1.2.6' in c.get('edition_note','') and '1.2.7' in c.get('edition_note',''))
  test('reader_pdf_provenance',len(c['source_binding']['embedded_assets'])==2 and all(x['archive_filename']==c['supplement_filename'] and x['pages']==2 for x in c['source_binding']['embedded_assets']))
  test('all_published_source_assets_bound',gate['source_files']==receipt['files'] and all(sha(p/'sources'/asset_name(x))==x['sha256'] for x in receipt['files']))
  test('promotion_source_receipt_binding',gate['source_receipt_sha256']==sha(p/'sources/receipt.json'))
  test('promotion_review_bindings',set(gate['reviews'])=={'analytic','adversarial','scope'} and all(v['sha256']==sha(p/v['report']) and v['verdict_sha256']==sha(p/v['verdict_file']) and v['verdict']==json.loads((p/v['verdict_file']).read_text()) for v in gate['reviews'].values()))
  gap=gate['gap_resolution']
  test('root_gap_resolution_file_binding',gate['disposition_by']=='root' and gap['disposition_by']=='root' and gap['status']=='RESOLVED_WITH_CONTEXTUAL_SCOPE' and gate['gap_resolution_sha256']==sha(p/gate['gap_resolution_file']) and gap==json.loads((p/gate['gap_resolution_file']).read_text()))
  test('frozen_scope_hold_preserved',gate['reviews']['scope']['verdict']['publication_hold'] is True and all(x['sha256']==sha(p/x['path']) for x in [gap['frozen_scope_content'],gap['frozen_scope_report'],gap['frozen_scope_verdict']]) and json.loads((p/gap['frozen_scope_content']['path']).read_text())['publication_hold']==gap['original_scope_hold'] and gap['original_scope_hold']['active'] is True and not c.get('publication_hold',{}).get('active',False))
  test('gap_independent_evidence_bindings',all(x['sha256']==sha(p/x['path']) for x in gap['analytic_evidence']+gap['adversarial_evidence']) and any(x['path']=='reviews/analytic/INTERPRETIVE_NOTE.md' for x in gap['analytic_evidence']) and any(x['path']=='reviews/analytic/counterexample_ratio_results.json' for x in gap['analytic_evidence']) and any(x['path']=='reviews/adversarial/structural_control_results.json' for x in gap['adversarial_evidence']) and any(x['path']=='reviews/adversarial/counterexample_results.json' for x in gap['adversarial_evidence']))
  test('gap_original_context_binding',gap['source']['sha256']==sha(textpath) and gap['main_pdf_sha256']==sha(p/'sources'/c['pdf_filename']) and gap['equation_17_source'] in source and gap['construction_paragraph_source'] in source and gap['public_scope_note'] in unescape(h) and gap['broad_reading_counterexample_preserved'] is True and gap['no_source_repair'] is True)
  test('main_mathematical_disposition_scoped',gate['reviews']['analytic']['verdict']['status']=='PASS' and gate['reviews']['adversarial']['verdict']['main_claims_supported_at_stated_hypotheses'] is True and gate['reviews']['adversarial']['verdict']['substantive_main_theorem_defect_identified'] is False)
  links=[attrs['href'] for tag,attrs in d.a if tag=='a' and 'href' in attrs]
  test('all_original_materials_linked',all(asset_name(x) in links for x in receipt['files']) and all(x['filename'] in links for x in c['source_binding']['embedded_assets']))
  test('no_false_top_level_zenodo_reader_links',all(not any('/files/'+x['filename'] in link for link in links) for x in c['source_binding']['embedded_assets']))
 if rid=='23180194':
  test('scope_complete',all(x in unescape(h) for x in ['locally compact second countable Hausdorff Abelian group','acting jointly measurably on an arbitrary measurable space Ω','sigma-finite measure on Ω','covariant, locally finite Radon random measure','nonzero Q-almost everywhere','every invariant, pointwise ξ-preserving, ξ-measurable Markov transport kernel','each row has mass one','every nonnegative measurable function f on Ω','every nonnegative measurable g on Ω × G','joint Mecke identity, or Campbell reversal']))
  test('scope_limits_preserved',all(x in unescape(h) for x in ['no assumption that the marginal law of ξ is sigma-finite','Invariance of the law of ξ alone is not a substitute','deterministic transports','Cox allocations','does not cover non-Abelian groups or the zero random measure','Standard Borel structure is used for the space of Radon measures; it is not imposed on Ω']))
  test('credited_classical_imports',all(x in unescape(h) for x in ['classical Mecke/Palm and Palm/mass-stationarity equivalences','known converse transport invariance','Problem 7.3 from 2009','complete final journal body was unavailable','complete final journal body was not checked']))
  test('printed_edition_date_binding',record['version']==c['version']=='1.0' and record['publication_date']==c['publication_date']=='2026-10-06' and c['source_binding']['manuscript_version'] is None and r'\date{6 October 2026\quad---\quad Unrefereed research note}' in source)
  test('two_original_assets_only',len(receipt['files'])==2 and len(texts)==7 and c.get('additional_assets',[])==[] and c['source_binding'].get('embedded_assets',[])==[] and {asset_name(x) for x in receipt['files']}=={c['pdf_filename'],c['supplement_filename']})
  test('abstract_source_binding',c['source_binding']['abstract_source']=='sources/'+TEX_PATHS[rid] and c['source_binding']['abstract_source_sha256']==sha(textpath) and c['source_binding']['abstract_word_count']==113)
  test('frozen_scope_candidate_binding',c['source_binding']['frozen_scope_content_path']=='reviews/scope/candidate-content.json' and c['source_binding']['frozen_scope_content_sha256']==sha(p/c['source_binding']['frozen_scope_content_path']))
  test('root_disposition_at_stated_scope',gate['disposition_by']=='root' and gate['source_repair'] is False and gate['human_peer_review'] is False and gate['reviews']['analytic']['verdict']['status']=='SUPPORTED_AT_STATED_SCOPE' and gate['reviews']['adversarial']['verdict']['status']=='PASS' and gate['reviews']['scope']['verdict']['verdict']=='PASS_SCOPE_ONLY')
  test('frozen_scope_chronology_preserved',gate['reviews']['scope']['verdict']['mathematical_clearance'] is False and bool(gate['scope_gate_resolution']))
 if rid in OCTOBER_EDITOR_IDS:
  expected_date={'23127646':'2026-10-03','23191301':'2026-10-06'}[rid]
  printed_date={'23127646':r'\date{October 3, 2026}','23191301':r'\date{6 October 2026}'}[rid]
  candidate_path={'23127646':'reviews/scope/candidate-content.json','23191301':'reviews/scope/content.json'}[rid]
  test('printed_edition_date_binding',record['version']==c['version']==c['source_binding']['zenodo_version']=='1.0' and record['publication_date']==c['publication_date']==expected_date and c['source_binding']['manuscript_version'] is None and printed_date in source)
  test('two_original_assets_only',len(receipt['files'])==2 and len(texts)=={'23127646':4,'23191301':6}[rid] and c.get('additional_assets',[])==[] and c['source_binding'].get('embedded_assets',[])==[] and {asset_name(x) for x in receipt['files']}=={c['pdf_filename'],c['supplement_filename']})
  test('abstract_source_binding',c['source_binding']['abstract_source']=='sources/'+TEX_PATHS[rid] and c['source_binding']['abstract_source_sha256']==sha(textpath) and c['source_binding']['abstract_word_count']==len(c['abstract'].split()))
  test('frozen_scope_candidate_binding',c['source_binding']['frozen_scope_content_path']==candidate_path and c['source_binding']['frozen_scope_content_sha256']==sha(p/candidate_path))
  av=gate['reviews']['adversarial']['verdict'];sv=gate['reviews']['scope']['verdict']
  test('root_disposition_at_stated_scope',gate['disposition_by']=='root' and gate['source_repair'] is False and gate['human_peer_review'] is False and gate['reviews']['analytic']['verdict']['status']=='PASS' and av.get('status',av.get('verdict'))=='PASS')
  test('frozen_scope_chronology_preserved',(sv['mathematical_clearance'] is False if rid=='23127646' else sv['mathematical_gate'] is False) and bool(gate['scope_gate_resolution']))
 if rid=='23127646':
  test('scope_complete',all(x in unescape(h) for x in ['finite and simple','nonempty stable parts A, B and C','no A–C edges','all four conditions','x|B| neighbors in B','x|A| neighbors in A and y|C| neighbors in C','y|B| neighbors in B','Each reached A vertex is counted once','infimum of this maximum over all eligible finite graphs','every rational θ with 0 < θ < 1','ψ(1−θ,θ) = 1−θ/d(θ)','attained by a finite ordinary graph','minimum unweighted maximum row degree','distinct columns and strictly positive rational probability vectors b and q','Mq = θ1 and Mᵀb = θ1']))
  test('quantitative_gap_and_limits',all(x in unescape(h) for x in ['|ψ(13/27,14/27) − ψ(14/27,13/27)| ≥ 1/108','Neither exact value nor their ordering is asserted','two integer minima','upper bounds only','not claimed to attain the infima','not claimed to be the exact gap','no claim about irrational boundary parameters','The inherited seven-type example is credited prior work']))
  test('universal_proof_not_examples_only',all(x in unescape(h) for x in ['lower bound valid for every finite graph','minimum connection requirement in both directions','finite ordinary graph','d(13/27) ≤ 4 and d(14/27) ≤ 4','known symmetry of the related one-direction function φ is a different result']))
 if rid=='23191301':
  test('scope_complete',all(x in unescape(h) for x in ['real homogeneous forms','squares of real polynomials','Here n counts variables','N = 10^62','C(3 · 10^62,6,3) is nonconvex','every fixed odd q ≥ 3','finite n(q)','different separating functional','coefficient-1 modified Motzkin sextic','220 monomials','eight parity blocks']))
  test('quantifiers_and_limits',all(x in unescape(h) for x in ['not prove nonconvexity for three variables','one common dimension that works for all odd exponents','not a classification','no claim of optimality','no stubbornness claim','It is not integration against a positive measure','not materialized numerically']))
  test('credited_classical_ingredients',all(x in unescape(h) for x in ['The classical polynomial and its sum-of-squares cube come from earlier work','separation, product positivity and distinct-index counting have earlier sources','application to a fixed-exponent obstruction','larger odd power after the polynomials are added']))
 if rid=='23127955':
  test('scope_complete',all(x in unescape(h) for x in ['every three pairwise disjoint convex subsets','union of all complete affine lines','three-dimensional Lebesgue outer measure zero','Tangency requires actual intersection with the set and containment of the line in a supporting plane','contact may be an entire segment','their closures may intersect','If any set is empty','sets need not be closed, bounded, full dimensional, strictly convex or smooth']))
  test('scope_limits_preserved',all(x in unescape(h) for x in ['does not prove containment in countably many 2-manifolds','Hausdorff-dimension bound of two','union of tangent lines need not itself be closed','Contact with a closure alone is not enough','not an algorithm for enumerating tangents','not a certification of first priority']))
  test('proof_and_credited_inputs',all(x in unescape(h) for x in ['countably many disjoint compact caps','At almost every parameter','three distinct contacts give it three distinct roots','Separate cases handle points, segments and planar sets','Conjecture 4 in Oberwolfach Report 44/2008','standard density theorem, Rademacher’s theorem and area formula']))
  test('printed_edition_date_binding',record['version']==c['version']==c['source_binding']['zenodo_version']=='1.0' and record['publication_date']==c['publication_date']=='2026-10-03' and c['source_binding']['manuscript_version'] is None and r'\date{3 October 2026\\\small Unrefereed preprint}' in source)
  test('two_original_assets_one_reader',len(receipt['files'])==2 and len(texts)==8 and c.get('additional_assets',[])==[] and c['source_binding'].get('embedded_assets',[])==[] and {asset_name(x) for x in receipt['files']}=={c['pdf_filename'],c['supplement_filename']} and sha(p/'sources/published-source/common_tangent_nullness.pdf')==sha(p/'sources'/c['pdf_filename']))
  test('abstract_source_binding',c['source_binding']['abstract_source']=='sources/'+TEX_PATHS[rid] and c['source_binding']['abstract_source_sha256']==sha(textpath) and c['source_binding']['abstract_word_count']==122)
  test('frozen_scope_candidate_binding',c['source_binding']['frozen_scope_content_path']=='reviews/scope/content.json' and c['source_binding']['frozen_scope_content_sha256']==sha(p/'reviews/scope/content.json'))
  test('root_disposition_at_stated_scope',gate['disposition_by']=='root' and gate['source_repair'] is False and gate['human_peer_review'] is False and gate['reviews']['analytic']['verdict']['status']=='PASS' and gate['reviews']['adversarial']['verdict']['status']=='PASS' and gate['reviews']['scope']['verdict']['status']=='PASS_SCOPE_ONLY' and gate['reviews']['scope']['verdict']['completion_percent']==100 and bool(gate['scope_gate_resolution']))
  test('proof_wording_precision_preserved',bool(gate['nonblocking_proof_wording']) and 'globally smooth' not in unescape(h))
 if rid in GAME_SESHADRI_IDS:
  test('promotion_source_receipt_binding',gate['source_receipt_sha256']==sha(p/'sources/receipt.json'))
  test('promotion_review_bindings',set(gate['reviews'])=={'analytic','adversarial','scope'} and all(v['sha256']==sha(p/v['report']) and v['verdict_sha256']==sha(p/v['verdict_file']) and v['verdict']==json.loads((p/v['verdict_file']).read_text()) for v in gate['reviews'].values()))
  test('all_published_source_assets_bound',gate['source_files']==receipt['files']==c['source_binding']['files'] and all(sha(p/'sources'/asset_name(x))==x['sha256'] for x in receipt['files']))
  clearance_path=R/gate['root_clearance_file'];clearance=json.loads(clearance_path.read_text())
  decision=next(x for x in clearance['papers'] if x['record_id']==rid)
  test('root_clearance_binding',clearance['status']==decision['status']=='PASS' and clearance['disposition_by']==gate['disposition_by']=='root' and gate['root_clearance_sha256']==sha(clearance_path) and gate['root_clearance_record']==decision and gate['approved_scope']==decision['approved_scope'] and gate['source_repair'] is False and gate['human_peer_review'] is False)
  test('root_clearance_source_review_identity',decision['pdf_sha256']==gate['pdf_sha256'] and decision['supplement_sha256']==gate['supplement_sha256'] and decision['source_receipt_sha256']==gate['source_receipt_sha256'] and all(decision['reviews'][k]['report_sha256']==v['sha256'] and decision['reviews'][k]['verdict_sha256']==v['verdict_sha256'] for k,v in gate['reviews'].items()))
  test('abstract_source_binding',c['source_binding']['abstract_source']=='sources/'+TEX_PATHS[rid] and c['source_binding']['abstract_source_sha256']==sha(textpath) and c['source_binding']['abstract_word_count']==len(c['abstract'].split()))
  test('two_original_assets_one_reader',len(receipt['files'])==2 and len(texts)=={'23430642':9,'23387814':5}[rid] and c.get('additional_assets',[])==[] and c['source_binding'].get('embedded_assets',[])==[] and {asset_name(x) for x in receipt['files']}=={c['pdf_filename'],c['supplement_filename']})
 if rid=='23430642':
  test('scope_complete',all(x in unescape(h) for x in ['one equilibrium to be found in polynomial time','deciding uniqueness is coNP-complete','exact rank(A + B) = 1','variable positive dimensions','entire mixed-strategy equilibrium pair','known strict pure equilibrium','Arbitrary degeneracy','positive-dimensional equilibrium sets','(8n + 9) rows and (16n + 22) columns','rank-invalid inputs belong to neither']))
  test('complexity_limits_and_credit',all(x in unescape(h) for x in ['Unless P = NP','does not establish strong hardness','fixed dimensions','nondegeneracy promise','uniqueness of equilibrium payoffs','does not run the potentially exponential sequence','Disser and Skutella','Adsul and coauthors','worldwide priority']))
  test('tar_gz_label_and_identity',c['supplement_filename']=='supportkit-v1.0.tar.gz' and 'Source and verification (tar.gz)' in h and 'Source and verification (ZIP)' not in h and all(not asset_name(x).endswith('.zip') for x in receipt['files']))
  test('printed_edition_date_binding',r'\date{13 October 2026\quad Version 1.0}' in source and record['version']==c['version']==c['source_binding']['manuscript_version']=='1.0' and record['publication_date']==c['publication_date']=='2026-10-13')
  test('archive_main_pdf_identity',sha(p/'sources/published-source/rank_one_uniqueness_v1_0/output/pdf/paper.pdf')==sha(p/'sources/paper.pdf'))
 if rid=='23387814':
  test('scope_complete',all(x in unescape(h) for x in ['For every integer d ≥ 7','smooth integral complex projective surface','ample canonical bundle','ample integral line bundle','K_S² = 6(d−1)(d−3)','L² = 6','ε(S,L;x) ≤ 1/(d−1) < 1/(2+(K_S²)^(1/4))','The additive 2 is outside the fourth root','The surfaces vary with d and x is a special point']))
  test('scope_limits_and_credit',all(x in unescape(h) for x in ['does not determine its exact value','very-general-point','Picard-rank-one','canonical or adjoint polarization bounds','Miranda’s classical pencil construction','does not list explicit coefficients','Historical priority']))
  test('printed_edition_date_binding',r'\date{October 14, 2026}' in source and c['source_binding']['manuscript_version'] is None and record['version']==c['version']=='1.0' and record['publication_date']==c['publication_date']=='2026-10-14' and c['edition_label']=='Zenodo version 1.0')
  test('frozen_scope_candidate_binding',c['source_binding']['frozen_scope_content_path']=='reviews/scope/candidate-content.json' and c['source_binding']['frozen_scope_content_sha256']==sha(p/'reviews/scope/candidate-content.json'))
 result['papers'][rid]={'checks':checks,'hashes':hashes,'local_links_checked':len(local),'pdf_pages':len(texts),'pdf_chars_per_page':[len(t) for t in texts]}
result['shared']={'index_sha256':sha(S/'research/index.html'),'sitemap_sha256':sha(S/'research/sitemap.xml'),'robots_sitemap':'Sitemap: https://aleckriebel.com/research/sitemap.xml' in (S/'robots.txt').read_text()}
result['status']='PASS' if not result['issues'] and result['shared']['robots_sitemap'] else 'ISSUES_FOUND'
try:
 target=R/'verification'/args.output_stem
 target.with_suffix('.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
 lines=['# Final content QA','',result['time'],'','Status: '+result['status'],'','Completion: 100% of requested checks executed.','',
 'Read-only checks of generated content against approved publication data and published source. Browser rendering and external HTTP checks are separate.','']
 for rid,item in result['papers'].items():
  lines += [rid+': '+str(sum(item['checks'].values()))+'/'+str(len(item['checks']))+' checks passed; '+str(item['local_links_checked'])+' local links/anchors; '+str(item['pdf_pages'])+' searchable PDF pages.','']
 lines += ['Issues: '+('; '.join(result['issues']) or 'None.'),'','SHA-256 bindings and individual checks are recorded in the accompanying JSON.']
 target.with_suffix('.md').write_text('\n'.join(lines)+'\n')
 result['saved']=True
except OSError as error:result['saved']=False;result['save_error']=str(error)
print(json.dumps(result,ensure_ascii=False))
raise SystemExit(0 if result['status']=='PASS' and result['saved'] else 1)
