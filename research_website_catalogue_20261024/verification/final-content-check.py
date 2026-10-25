"""Verify rendered research content. Supported source layouts are listed in TEX_PATHS.
Uses Python standard library plus an existing pdftotext executable; installs nothing.
"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,urljoin,unquote
import json,hashlib,re,datetime,subprocess,zipfile,unicodedata,argparse
from html import unescape
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
}
LATEX_WORDS={r'\omega':'ω',r'\delta':'δ',r'\log':'log',r'\geq':'≥',r'\simeq':'≃',r'\PP':'P',r'\dim':'dim',r'\Aut':'Aut',r'\qquad':' ',r'\emph':'',r'\CCR':'CCR',r"V\'ertesi":'Vértesi',r'\times':'×'}
def abstract_tokens(tex):
 for old,new in LATEX_WORDS.items():tex=tex.replace(old,new)
 commands=re.findall(r'\\[A-Za-z]+',tex)
 if commands:raise ValueError('Unrecognized abstract TeX commands: '+repr(commands))
 return wt(tex)
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
 test('abstract_full_source_words',abstract_tokens(a)==wt(c['abstract']))
 test('no_noindex','noindex' not in meta.get('robots',''))
 test('no_audit_replay',not any(x in ''.join(d.text).lower() for x in ['24 october 2026','october 24','audit completed','checks passed','worldwide first','first-ever']))
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
 assets=[(key,c[key]) for key in ['pdf_filename','supplement_filename'] if c.get(key)]
 assets += [('additional_asset_'+asset['filename'],asset['filename']) for asset in c.get('additional_assets',[])]
 for key,name in assets:
  actual=sha(f.parent/name);hashes[name]=actual
  test(key,actual==sha(p/'sources'/name)==next(x['sha256'] for x in receipt['files'] if x['name']==name) and name in [a.get('href') for t,a in d.a if t=='a'])
  if name.endswith('.zip'):
   with zipfile.ZipFile(f.parent/name) as z:test('zip_integrity_'+name,z.testzip() is None)
  if key.startswith('additional_asset_') and name.endswith('.pdf'):
   extra_text=subprocess.check_output(['/opt/homebrew/bin/pdftotext',str(f.parent/name),'-'],text=True).split('\f')
   if not extra_text[-1].strip():extra_text.pop()
   test('supplement_pdf_searchable',all(len(t.strip())>100 for t in extra_text))
   test('supplement_pdf_page_label',f'PDF, {len(extra_text)} pages' in h)
 texts=subprocess.check_output(['/opt/homebrew/bin/pdftotext',str(f.parent/c['pdf_filename']),'-'],text=True).split('\f')
 if not texts[-1].strip():texts.pop()
 test('pdf_searchable',all(len(t.strip())>100 for t in texts));test('page_count',f'PDF, {len(texts)} pages' in h)
 frames=[a for t,a in d.a if t=='iframe'];test('iframe',len(frames)==1 and frames[0]['src']==c['pdf_filename']+'#view=FitH' and bool(frames[0].get('title')))
 test('index_entry',f'href="/research/{c["slug"]}/"' in index and c['description'] in unescape(index))
 ix=json.loads(re.search('<script type="application/ld\\+json">(.*?)</script>',index,re.S).group(1));items=ix['mainEntity']['itemListElement'];test('index_jsonld',len([x for x in items if x['url']==base and x['name']==c['title']])==1 and ix['mainEntity']['numberOfItems']==len(items))
 test('sitemap',sitemap.count('<loc>'+base+'</loc>')==1)
 bib=(f.parent/'citation.bib').read_text();test('bibtex',all(x in bib for x in [c['title'],c['author'],c['doi'],c.get('bibtex_note','Unrefereed preprint, version '+c['version'])]))
 test('background_links',all(x['url'] in h and x['title'] in unescape(h) and x['note'] in unescape(h) for x in c['background']))
 record=json.loads((p/'sources/record.json').read_text())['metadata'];test('record_metadata',all(c[k]==record[k] for k in ['title','doi','publication_date']) and (c['version']==record['version'] if 'version' in record else rid=='21699161' and c['source_binding']['zenodo_version'] is None))
 if c.get('edition_label'):test('edition_label',c['edition_label'] in unescape(h) and c['citation_edition_label'] in unescape(h) and c['edition_note'] in unescape(h))
 if c.get('related_resources'):
  materials=re.search('<section id="materials">(.*?)</section>',h,re.S).group(1)
  test('supporting_materials_links',all(x['url'] in materials and x['label'] in unescape(materials) and x.get('doi','') in unescape(materials) for x in c['related_resources']))
  related_bound=True
  for related in c['source_binding'].get('related_records',[]):
   rp=p/'sources/related-records'/related['record_id'];rr=json.loads((rp/'receipt.json').read_text())
   related_bound=related_bound and rr['record_id']==related['record_id'] and rr['files']==related['files']
   related_bound=related_bound and all(sha(rp/x['name'])==x['sha256'] for x in rr['files'])
  test('related_resource_source_bindings',related_bound)
 if (p/'promotion.json').exists():
  gate=json.loads((p/'promotion.json').read_text())
  test('promotion_pdf_binding',gate['status']=='PASS' and gate['pdf_sha256']==sha(p/'sources'/c['pdf_filename']))
  if gate.get('publication_sha256'):test('promotion_publication_binding',gate['publication_sha256']==sha(p/'publication.json'))
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
