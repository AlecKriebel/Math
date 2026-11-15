"""Independent frozen-candidate semantic/asset/fence checks and private probes.

Uses pre-candidate editorial expectations. Candidate builder is reproduced only
in memory after full code reading; no disk builder, campaign or source program.
"""
from pathlib import Path
import json,hashlib,re,copy,sys,xml.etree.ElementTree as ET
from urllib.parse import urljoin
from html import escape
from datetime import date
import dom_oracle as O
E=Path(__file__).resolve().parent;P=E.parents[1];W=P/'verification/six-paper-private-stage-sol-20261114';T=W/'final-build-a/public';U=W/'final-build-b/public';PUBLIC=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public')
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def need(ok,s):
 if not ok:raise ValueError(s)
def parse(html):
 p=O.Parse();p.feed(html);p.close();return p
def subtree(n,tag):return [x for x in n.all() if x.tag==tag and O.active(x)]
def anchor(n,href,base):return any(urljoin(base,x.attrs.get('href',''))==href for x in subtree(n,'a'))
def scientific_blocks(spec):
 # Frozen-source roles, rather than builder's text/hash. Metadata headers,
 # link groups, bibliography joins and citation style have explicit mappings.
 out=[]
 for b in spec['blocks']:
  raw=b['raw'];text=b['text'];kind=None
  if b['kind']=='verbatim_citation':kind='exact_downloaded_BibTeX_not_displayed'
  elif b['ordinal'] in [1,2]:kind='header_metadata_reformatted'
  elif re.fullmatch(r'Zenodo DOI',text):kind='DOI_link_label_reformatted'
  elif raw.startswith('[') and re.search(r'\]\([^)]*\)\. ',raw):kind='background_title_and_note_colon_join'
  elif raw.startswith('['):kind='asset_link_group_reformatted'
  elif text.startswith(('Paper and prose: CC BY','Authored paper and accompanying materials: CC BY')):kind='more_complete_visible_rights_notice'
  elif text.startswith('Alec Kriebel'):kind='visible_citation_reformatted'
  out.append((b,kind))
 return out
def semantic_page(spec,html,files):
 d=parse(html);nodes=list(d.root.all());mains=[n for n in nodes if n.tag=='main' and O.active(n)];need(len(mains)==1,'one active main')
 arts=subtree(mains[0],'article');need(len(arts)==1,'one active article');art=arts[0];body=O.norm(O.text(art));base=spec['canonical_for_private_render_only'];covered=[]
 # Every substantive paragraph matches whole, with no dropped words/math.
 for b,kind in scientific_blocks(spec):
  if kind is None:need(O.norm(b['text']) in body,'complete original paragraph '+str(spec['row'])+'/'+str(b['ordinal']));method='whole_exact_visible_paragraph'
  elif kind=='background_title_and_note_colon_join':
   m=re.match(r'^\[([^\]]+)\]\(([^)]+)\)\. (.*)$',b['raw'],re.S);need(m is not None,'background parse');label,href,note=m.groups();lis=subtree(art,'li')
   need(any(O.norm(label) in O.norm(O.text(n)) and O.norm(note) in O.norm(O.text(n)) and anchor(n,urljoin(base,href),base) for n in lis),'whole visible primary title/note/link');method=kind
  elif kind=='exact_downloaded_BibTeX_not_displayed':need(files['citation.bib']==spec['complete_bibtex'].encode(),'exact source BibTeX asset');method=kind
  else:method=kind
  covered.append({'ordinal':b['ordinal'],'method':method})
 need(body.count(O.norm(spec['abstract']))==1,'one complete visible abstract')
 h1=subtree(art,'h1');need(len(h1)==1 and O.norm(O.text(h1[0]))==spec['title'] and anchor(h1[0],base,base),'exact visible h1 self link')
 need(spec['author'] in body,'visible author');need(anchor(d.root,spec['orcid'],base),'actual ORCID link')
 dt=date.fromisoformat(spec['publication_date']);day=f'{dt.day} {dt.strftime("%B %Y")}';need(day in body and spec['version'] in body,'visible original date/edition')
 if spec['row'] in [106,107]:need('Zenodo version '+spec['version'] in body,'API version distinguished from unprinted manuscript version')
 need('CC BY 4.0' in body and anchor(art,spec['license_url'],base),'visible actual paper license')
 need(('Python scripts and website code: MIT.' in body) if spec['row']==111 else 'MIT' not in body,'record-specific code rights')
 links=subtree(art,'a')
 for wanted in spec['visible_links']:
  href=wanted['resolved_href'];pool=subtree(d.root,'a') if wanted['semantic_role']=='navigation' or 'orcid.org' in href else links
  need(any(urljoin(base,x.attrs.get('href',''))==href for x in pool),'approved destination '+href)
 # Exact descriptions/citation/DOI/date and scholarly meaning from independent
 # preflight values, not builder-generated expected output.
 head=next(n for n in nodes if n.tag=='head');meta={};count=0
 for n in head.all():
  if n.tag=='meta' and ('name' in n.attrs or 'property' in n.attrs):
   k=n.attrs.get('name',n.attrs.get('property'));need(k not in meta,'unique head meta '+k);meta[k]=n.attrs.get('content');count+=1
 for k,v in {'description':spec['description'],'author':spec['author'],'citation_title':spec['title'],'citation_author':spec['author'],'citation_author_orcid':'0009-0001-9320-500X','citation_publication_date':spec['publication_date'].replace('-','/'),'citation_doi':spec['doi'],'citation_pdf_url':base+spec['pdf_filename'],'og:title':spec['title'],'og:description':spec['description'],'og:url':base}.items():need(meta.get(k)==v,'independent metadata '+k)
 need(not any('noindex' in str(v).lower() for k,v in meta.items() if 'robots' in k),'indexable robots')
 canonical=[n.attrs.get('href') for n in head.all() if n.tag=='link' and n.attrs.get('rel')=='canonical'];need(canonical==[base],'single self canonical')
 scripts=[n for n in head.all() if n.tag=='script'];need(len(scripts)==1 and scripts[0].attrs=={'type':'application/ld+json'},'one nonexecuting scholarly schema')
 def unique_pairs(rows):
  out={}
  for k,v in rows:need(k not in out,'unique JSON key');out[k]=v
  return out
 schema=json.loads(''.join(x for x in scripts[0].children if isinstance(x,str)),object_pairs_hook=unique_pairs);articles=[x for x in schema['@graph'] if x.get('@type')=='ScholarlyArticle'];need(len(articles)==1,'one scholarly article');s=articles[0]
 for k,v in {'url':base,'headline':spec['title'],'description':spec['description'],'abstract':spec['abstract'],'datePublished':spec['publication_date'],'version':spec['version'],'license':spec['license_url']}.items():need(s.get(k)==v,'independent scholarly '+k)
 need(s['encoding']['contentUrl']==base+spec['pdf_filename'] and s['identifier']['value']==spec['doi'],'actual scholarly PDF/DOI');need('Unrefereed' in s['creativeWorkStatus'],'unrefereed scholarly status')
 need(all(x not in body for x in spec['forbidden_private_tokens']),'no private audit narrative');need(not any(t in json.dumps(schema) for t in ['/Users/alec/','SOURCE_READY','root-clearance-','PRIVATE_EDITORIAL']),'no private schema leakage')
 iframes=subtree(art,'iframe');need(len(iframes)==1 and iframes[0].attrs.get('src').split('#')[0]==spec['pdf_filename'] and bool(iframes[0].attrs.get('title')),'one complete accessible reader')
 need(anchor(art,base+spec['pdf_filename'],base),'local direct PDF open')
 for name in [spec['pdf_filename'],spec['zip_filename'],'citation.bib']:
  need(any(urljoin(base,x.attrs.get('href',''))==base+name and 'download' in x.attrs for x in links),'explicit local download '+name)
 need(files['citation.bib']==spec['complete_bibtex'].encode(),'exact prepared citation bytes')
 return {'row':spec['row'],'record_id':spec['record_id'],'status':'PASS_SEMANTIC_MAPPING_WITH_EXPLICIT_PRESENTATION_DIFFERENCES','all_frozen_blocks_accounted_for':len(covered),'mapping':covered,'headings_as_rendered':[O.norm(O.text(n)) for n in subtree(art,'h2')],'source_h2_count':len(spec['h2_headings']),'rendered_h2_count':len(subtree(art,'h2')),'strict_preflight_unchanged':True}
def execute():
 pins={'CANDIDATE_READY.json':'4fc89dc274a53c7bad55d4571f1b2e174f43d13218a662ee3c4302cd67de0e73','FINAL_SEAL.json':'8796f52a8dfa86cabf08507aff8120d39149b5e8ca8a2c2d01015dc68723fc93','OWNED_MANIFEST.json':'239bf60a4b7590c33389b75b64dba30d22f9080f3edefd5994958c05cec03912','CANDIDATE_CODE_MANIFEST.json':'97ce5b02ee63493e6dedfaee97e727d20b795b9de32b9de8b2745b937a6e66af'}
 for n,v in pins.items():need(sha(W/n)==v,'exact candidate '+n)
 manifest=load(W/'OWNED_MANIFEST.json');actual={str(p.relative_to(W)) for p in W.rglob('*') if p.is_file()};need(actual=={x['path'] for x in manifest['files']}|{'OWNED_MANIFEST.json','FINAL_SEAL.json'},'closed owned inventory')
 for x in manifest['files']:p=W/x['path'];need(p.stat().st_size==x['bytes'] and sha(p)==x['sha256'],'frozen candidate payload')
 expected=load(E/'EXPECTED_PAGES.json')['pages'];results=[];faults=[]
 for spec in expected:
  folder=T/'research'/spec['slug'];files={p.name:p.read_bytes() for p in folder.iterdir() if p.is_file()};html=files['index.html'].decode();results.append(semantic_page(spec,html,files))
  # Independent deliberate defects against the approved scientific prose.
  target=next(b['text'] for b,k in reversed(scientific_blocks(spec)) if k is None and len(b['text'])>100)
  mutations={'lost_nonleading_complete_paragraph':html.replace(escape(target),'Qualification omitted.',1),'hidden_article':html.replace('<article>','<article hidden>',1),'inert_article':html.replace('<article>','<article inert>',1),'template_only_body':html.replace('<article>','<article><template>',1).replace('</article>','</template></article>',1),'noscript_only_body':html.replace('<article>','<article><noscript>',1).replace('</article>','</noscript></article>',1),'wrong_original_date':html.replace('content="'+spec['publication_date'].replace('-','/')+'"','content="2099/01/01"',1),'wrong_article_license':html.replace(spec['license_url'],'https://example.org/wrong-license',1),'wrong_DOI_meta':html.replace('name="citation_doi" content="'+spec['doi']+'"','name="citation_doi" content="10.5281/zenodo.1"',1),'wrong_canonical':html.replace('rel="canonical" href="'+spec['canonical_for_private_render_only']+'"','rel="canonical" href="https://example.org/wrong/"',1)}
  prefixes={106:'For every literal positive word',107:'There is no prorepresentable recipient',108:'Let g₀ be the unit round metric',110:'Theorem 1(iii).',111:'For every t ∈ [0,1]',112:'For every test ψ in the stated class'}
  mathblock=next(x['text'] for x in spec['blocks'] if x['text'].startswith(prefixes[spec['row']]))
  if spec['row']==106:changed=mathblock.replace('20, 30 or 40','20 or 40',1)
  elif spec['row']==107:changed=mathblock.replace('every tangent dimension','one tangent dimension',1)
  elif spec['row']==108:changed=mathblock.replace('1106714561/1700054750','1106714561/1700054751',1)
  elif spec['row']==110:changed=mathblock.replace('For every A⊆S','For some A⊆S',1)
  elif spec['row']==111:changed=mathblock.replace('[0,1]','[0,1)',1)
  else:changed=mathblock.replace('−(2/a²)','+(2/a²)',1)
  need(changed!=mathblock,'real mathematical fault anchor')
  mutations['lost_specific_mathematical_quantifier_constant_or_endpoint']=html.replace(escape(mathblock),escape(changed),1)
  for name,mutant in mutations.items():
   need(mutant!=html,'actual independent mutation '+name)
   try:semantic_page(spec,mutant,files)
   except (ValueError,KeyError,IndexError):faults.append({'row':spec['row'],'name':name,'rejected':True,'mutant_sha256':hashlib.sha256(mutant.encode()).hexdigest()})
   else:raise ValueError('independent defect accepted '+name)
  ready=load(P/'papers'/spec['record_id']/'sources/SOURCE_READY.json');ak='assets' if spec['row']==106 else 'all_native_assets_in_original_order' if spec['row']==111 else 'all_assets_in_original_order';obj='native_file_object' if spec['row']==106 else 'original_api_file_object';S=P/'papers'/spec['record_id']/'sources'
  for x in ready[ak]:
   name=x[obj]['key'];p=Path(x['path']);p=p if p.is_absolute() else S/p;digest=x.get('sha256',x.get('SHA256'));need(sha(p)==digest and hashlib.sha256(files[name]).hexdigest()==digest and files[name]==p.read_bytes(),'actual complete native PDF/ZIP')
 # Actual current base, separate from source/candidate outputs.
 baseline=load(W/'FRESH_BASELINE.json');old={x['path']:x for x in baseline['public_files']};present={str(p.relative_to(PUBLIC)) for p in PUBLIC.rglob('*') if p.is_file()};need(present==set(old) and len(present)==532,'current exact production base inventory')
 for x in baseline['public_files']:
  p=PUBLIC/x['path'];need(p.stat().st_size==x['bytes'] and sha(p)==x['sha256'],'all current old public bytes')
 for x in baseline['installed_core_files']:
  p=Path(x['path']);need(p.stat().st_size==x['bytes'] and sha(p)==x['sha256'],'all installed core bytes')
 need({str(p) for p in [*(P/'scripts').glob('*.py'),P/'verification/final-content-check.py']}=={x['path'] for x in baseline['installed_core_files']},'exact current installed core inventory')
 a={str(p.relative_to(T)):p.read_bytes() for p in T.rglob('*') if p.is_file()};b={str(p.relative_to(U)):p.read_bytes() for p in U.rglob('*') if p.is_file()};need(a==b and len(a)==26,'exact paired 26 output bytes')
 wanted={x.lstrip('/') for x in load(E/'EXPECTED_OVERLAY.json')['exact_overlay_paths']};need(wanted-set(a)=={'sitemap.xml'} and set(a)-wanted=={'research/sitemap.xml'},'only explicit preflight sitemap-location correction')
 need(set(a)&set(old)=={'research/index.html','research/sitemap.xml'} and len(set(old)|set(a))==556,'24 new files/two old replacements')
 ix=parse(a['research/index.html'].decode());oldix=parse((PUBLIC/'research/index.html').read_text());oldli=[O.norm(O.text(n)) for n in oldix.root.all() if n.tag=='li'];newli=[O.norm(O.text(n)) for n in ix.root.all() if n.tag=='li'];need(len(oldli)==72 and len(newli)==78 and oldli==newli[:72],'old72 plus exact six index entries')
 for spec in expected:
  dt=date.fromisoformat(spec['publication_date']);day=f'{dt.day} {dt.strftime("%B %Y")}';need(any(spec['title'] in x and day in x for x in newli[72:]),'correct new index title/date')
 rawold=(PUBLIC/'research/index.html').read_text();rawnew=a['research/index.html'].decode();rx=r'<li>.*?</li>';oldentries=re.findall(rx,rawold,re.S);newentries=re.findall(rx,rawnew,re.S);need(len(oldentries)==72 and newentries[:72]==oldentries,'all old index-entry bytes preserved')
 jm=r'(<script type="application/ld\+json">\s*)(.*?)(\s*</script>)';jo=re.search(jm,rawold,re.S);jn=re.search(jm,rawnew,re.S);oldj=json.loads(jo.group(2));newj=json.loads(jn.group(2));need(newj['mainEntity']['numberOfItems']==78 and newj['mainEntity']['itemListElement'][:72]==oldj['mainEntity']['itemListElement'],'old index schema plus78 count')
 need([x['url'] for x in newj['mainEntity']['itemListElement'][72:]]==[x['canonical_for_private_render_only'] for x in expected],'exact six index schema URLs')
 restored=rawnew[:jn.start(2)]+jo.group(2)+rawnew[jn.end(2):]
 for entry in newentries[72:]:restored=restored.replace('      '+entry+'\n','',1)
 need(restored==rawold,'all unrelated index bytes preserved')
 before=ET.fromstring((PUBLIC/'research/sitemap.xml').read_bytes());after=ET.fromstring(a['research/sitemap.xml']);oldloc=[n.text for n in before.findall('{*}url/{*}loc')];newloc=[n.text for n in after.findall('{*}url/{*}loc')];need(len(oldloc)==73 and newloc==oldloc+[x['canonical_for_private_render_only'] for x in expected] and len(set(newloc))==79,'old73 plus exact six sitemap URLs')
 restored=a['research/sitemap.xml'].decode()
 for spec in expected:restored=restored.replace('  <url><loc>'+spec['canonical_for_private_render_only']+'</loc><lastmod>2026-11-15</lastmod></url>\n','',1)
 need(restored==(PUBLIC/'research/sitemap.xml').read_text(),'all unrelated sitemap bytes preserved')
 for x in load(E/'ALL_PREFLIGHT_BINDINGS.json')['files']:
  p=Path(x['path']);need(p.stat().st_size==x['bytes'] and sha(p)==x['sha256'],'all original preflight inputs still literal')
 return {'status':'PASS_INDEPENDENT_SEMANTIC_ASSET_CURRENT_BASE_AUDIT_WITH_EXPLICIT_PRESENTATION_RECONCILIATION','pages':results,'independent_private_faults':faults,'all_preflight_blocks_accounted_for':sum(x['all_frozen_blocks_accounted_for'] for x in results),'rendered_section_headings':sum(x['rendered_h2_count'] for x in results),'paired_complete_overlay_files':26,'all_current_production_files_unchanged':532,'old_nonoverlay_public_fence':530,'installed_core_files_unchanged':18,'source_and_editorial_input_bindings_unchanged':73,'conditional_union_counts':[556,78,79],'explicit_preflight_path_correction':'Actual existing sitemap is research/sitemap.xml, not the preflight shorthand sitemap.xml. Frozen original expectation is preserved.','candidate_code_or_stage_edited':False,'production_or_AA_clearance':False}
if __name__=='__main__':print(json.dumps(execute(),indent=2,ensure_ascii=False))
