#!/usr/bin/env python3
"""Private editorial copy/state/native-object check; no scientific replay/writes."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib,json,re,sys,subprocess
sys.dont_write_bytecode=True
E=Path(__file__).resolve().parent;PAPER=E.parents[1];Q=PAPER/'publication/promotion'
EXCLUDED={'OWNED_MANIFEST.json','SEAL.json'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def need(ok,why):
 if not ok:raise RuntimeError(why)
def flat(t):return ' '.join(t.split())
def compact(t):return re.sub(r'\s+','',t)
class Document(HTMLParser):
 def __init__(self):
  super().__init__(convert_charrefs=True);self.stack=[];self.nodes=[];self.roots=[];self.decl=0
 def handle_decl(self,d):need(d.lower()=='doctype html' and self.decl==0 and not self.stack,'doctype');self.decl+=1
 def handle_comment(self,d):raise RuntimeError('document comments not allowed')
 def handle_starttag(self,tag,attrs):
  parents={'html':{None},'head':{'html'},'body':{'html'},'meta':{'head'},'title':{'head'},'script':{'head'},'style':{'head'},'main':{'body'},'nav':{'main'},'article':{'main'},'h1':{'article'},'h2':{'article'},'p':{'article','footer'},'div':{'article'},'iframe':{'article'},'footer':{'article'},'a':{'nav','p'},'time':{'p'},'cite':{'p'},'sup':{'p','div'},'sub':{'p','div'},'br':{'p','div'}}
  parent=self.stack[-1]['tag'] if self.stack else None
  need(tag in parents and parent in parents[tag],'document parent grammar '+tag)
  allowed={'html':{'lang'},'meta':{'charset','name','content','property'},'script':{'type'},'nav':{'aria-label'},'h2':{'id'},'p':{'class','id'},'div':{'class','role','aria-label'},'iframe':{'id','title','src','loading'},'a':{'href','target','rel','download'},'time':{'datetime'}}.get(tag,set())
  need(len(dict(attrs))==len(attrs) and all(k in allowed for k,v in attrs),'unexpected/hidden element attribute '+tag)
  node={'tag':tag,'attrs':dict(attrs),'children':[]}
  (self.stack[-1]['children'] if self.stack else self.roots).append(node);self.nodes.append(node)
  if tag not in {'meta','br'}:self.stack.append(node)
 def handle_endtag(self,tag):
  need(self.stack and self.stack[-1]['tag']==tag,'balanced actual nesting '+tag);self.stack.pop()
 def handle_data(self,data):
  if not self.stack:need(not data.strip(),'text outside document');return
  if self.stack[-1]['tag'] in {'html','head','body','main','article','footer'}:need(not data.strip(),'unknown document/body text')
  self.stack[-1]['children'].append(data)
 def finish(self):
  self.close();need(not self.stack and self.decl==1,'complete balanced document')
  need([n['tag'] for n in self.roots]==['html'],'single html document')
  need([x['tag'] for x in self.roots[0]['children'] if isinstance(x,dict)]==['head','body'],'ordered head and body')
 def find(self,tag):return [n for n in self.nodes if n['tag']==tag]
def text(n):return ''.join(text(c) if isinstance(c,dict) else c for c in n['children'])
def semantic(html,cfg,snap):
 d=Document();d.feed(html);d.finish()
 need(len(d.find('article'))==1 and len(d.find('main'))==1 and len(d.find('h1'))==1,'one visible article and title')
 body=flat(text(d.find('article')[0]));small=body.casefold();raw=compact(body)
 title='Loss of total-space positivity for the normalized relative Kähler–Ricci flow'
 need(text(d.find('h1')[0])==title,'full exact title')
 need(len(body)>7500,'substantive accessible article')
 style=d.find('style');need(len(style)==1 and text(style[0])==load(E/'STYLE_CONTRACT.json')['exact_approved_CSS'],'approved visible white Arial stylesheet')
 abstract=(E/'ORIGINAL_ABSTRACT.txt').read_text().strip();pars=[p for p in d.find('p') if p['attrs'].get('id')=='original-abstract']
 need(len(pars)==1 and flat(text(pars[0]))==flat(abstract),'full original abstract in body')
 need((Q/'abstract.txt').read_text().strip()==abstract,'whole standalone abstract')
 required=[
  'every finite t ≥ 0','all four coordinate charts','every complex tangent direction everywhere on the compact X',
  'square-root metric, with weight φ₀/2','negative curvature on the actual tangent vector ∂/∂s',
  'Both fiber measures in the defining equation are probabilities','evolving fiber integral I(s,t)',
  'reaction coefficient is one for this weight and time','defining equation (13)',
  'displayed equation (14) with the same weight and time','Dropping the evolving log I term instead changes the flow',
  'exact derivative identity for the nonlinear solution','Classical smooth finite-time parabolic existence and parameter regularity',
  'does not prove that analytic existence theorem','No regularity or horizontal convergence of an infinite-time limit is required',
  'Naumann constructed the relative flow','Remark 4.11 already gives normalized anticanonical negativity',
  'effectively parametrized Fano families','rule out a broad claim of first positivity loss',
  '4 June 2025','Its text was not recovered','its overlap is unknown',
  'does not settle the Griffiths conjecture','bundle itself already has Griffiths-positive metrics',
  'searchable four-page PDF','Python assertions enabled','Authorship would be discussed in relation to actual contributions',
  'AI tools were used extensively','unrefereed preprint','Internal AI reviews are not human peer review',
  'no formal proof-assistant certification is claimed','CC BY 4.0']
 for term in required:need(term.casefold() in small,'required scientific/credit/status phrase '+term)
 for formula in ['φ₀=2log(1+u)+(2−ε)/(1+u)+2log(1+v)+δpx².',
   'φₛₛ̄(0,0,t)=1/96−(1−e−2t)/24.',
   'Att*=(log2)/2thiscoefficientis−1/96.',
   'AB−Q≥1/64+(159/32)p>0.',
   '∂ₜw=Δ_Fw+w−∫ℙ¹wμ_F,',
   'w(x,t)=ε+δ/3+(δ/2)P₁(x)+(δ/6)e−2tP₂(x).']:
  need(formula in raw,'exact quantitative counterexample '+formula)
 need(not re.search(r'\bMIT\b',body),'no invented separate MIT license')
 need(not re.search(r'has (?:received|undergone) human peer review|human peer reviewed|has been formally certified',small),'no human/formal review promotion')
 need(not any(w in small for w in ['first-ever','we are the first','this is the first','proves the griffiths conjecture','disproves the griffiths conjecture']),'no inflated firstness or Griffiths claim')
 need(not any(w in small for w in ['semantic_faults','owned_manifest','checkpoint','66 checks','441 grid','57 checks']),'internal audit details excluded')
 need(not any('follow-up' in text(n).casefold() or 'open question' in text(n).casefold() for n in d.find('h2')),'no unsupported follow-up section')
 meta={n['attrs'].get('name',n['attrs'].get('property',n['attrs'].get('charset'))):n['attrs'].get('content') for n in d.find('meta')}
 need(meta.get('robots')=='noindex,nofollow','private robots')
 need(meta.get('citation_title')==title and meta.get('citation_doi')=='10.5281/zenodo.23331080','scholarly source identity')
 need(meta.get('citation_author')=='Alec Kriebel' and meta.get('citation_publication_date')=='2026/10/12','scholarly author and original date')
 need(meta.get('citation_pdf_url')=='https://zenodo.org/records/23331080/files/positivity_loss.pdf','unchanged scholarly PDF link')
 need('relative Kähler–Ricci flow' in meta['description'] and len(meta['description'])>100,'descriptive scientific SEO')
 need(len(d.find('title'))==1 and 'Positivity Loss' in text(d.find('title')[0]),'descriptive SEO title')
 scripts=d.find('script');need(len(scripts)==1 and scripts[0]['attrs']=={'type':'application/ld+json'},'one nonexecuting scholarly data object')
 ld=json.loads(text(scripts[0]));need(ld['@type']=='ScholarlyArticle' and ld['abstract']==abstract,'full scholarly abstract')
 need(ld['datePublished']=='2026-10-12' and ld['version']=='1.0' and ld['creativeWorkStatus']=='Unrefereed preprint','structured date/version/status')
 need(ld['author']['sameAs']=='https://orcid.org/0009-0001-9320-500X' and ld['license']=='https://creativecommons.org/licenses/by/4.0/','structured author/license')
 need(not any(k in ld for k in ['url','@id','mainEntityOfPage']),'canonical assignment absent')
 need(d.find('time')[0]['attrs']=={'datetime':'2026-10-12'},'original date machine time')
 links=[n['attrs']['href'] for n in d.find('a')];need('https://aleckriebel.com/research/' in links,'research index navigation')
 need([x for x in links if x.startswith('assets/')]==['assets/positivity_loss.pdf','assets/positivity_loss.pdf','assets/verification_package.zip'],'actual public source order and open/download links')
 need('citation.bib' in links and 'https://doi.org/10.5281/zenodo.23331080' in links,'citation and DOI navigation')
 for href in links:need(href.startswith(('https://','assets/','#')) or href=='citation.bib','ordinary non-outreach links only')
 ids=[n['attrs']['id'] for n in d.nodes if 'id' in n['attrs']];need(len(ids)==len(set(ids)),'unique navigation identifiers')
 for href in links:
  if href.startswith('#'):need(href[1:] in ids,'local navigation target')
 frame=d.find('iframe');need(len(frame)==1 and frame[0]['attrs']['src']=='assets/positivity_loss.pdf#view=FitH&navpanes=0','full unchanged PDF embed')
 need(frame[0]['attrs'].get('title','').startswith('Complete published paper:'),'PDF accessible title')
 state=cfg['state'];need(state['private_editorial_complete'] is True and state['root_editorial_adoption'] is None,'root editorial adoption pending')
 for k in ['public_promotion_authority','production_config_authority','production_config_created','site_created','site_deployed','live_page_verified','browser_publication_gate','native_service_gate','tracker_gate','redirect_gate','git_gate','release_gate']:need(state[k] is False,'all public flags false '+k)
 need(state['canonical_url'] is None and state['AA'] is None,'canonical and native AA null')
 need(cfg['proposed']['slug']=='normalized-relative-kahler-ricci-flow-positivity-loss' and cfg['proposed']['page_url'].endswith('/'+cfg['proposed']['slug']+'/'),'separate proposed slug only')
 src=cfg['source'];need(src['PDF']['pages']==4 and src['ZIP']['original_regular_payloads']==40 and src['ZIP']['embedded_PDFs']==0,'actual four-page PDF and40payload ZIP/no embedded PDF')
 need(src['native_public_asset_order']==['positivity_loss.pdf','verification_package.zip'],'native original file order')
 need(src['license_original']=={'id':'cc-by-4.0'} and src['separate_code_license'] is None,'exact source license without invention')
 need(src['declared_publication_date']=='2026-10-12' and src['version']=='1.0' and src['DOI']=='10.5281/zenodo.23331080','native publication identity')
 science=cfg['science'];c=science['full_counterexample']
 need(science['root_clearance_SHA256']=='df67490c786bef3bcb1623cfb4a25f5b8948a74d49c039b199543a7cf21da315' and sha(E/'inputs/root-clearance.json')==science['root_clearance_SHA256'],'actual root scientific clearance')
 need(c['all_finite_t_geq_zero']=='phi_(s sbar)(0,0,t)=1/96-(1-exp(-2t))/24' and c['negative_actual_tangent_coefficient']=='-1/96 on d/ds','full all-finite-time coefficient and actual direction')
 need(c['global_initial_smooth_strict_positive_all_four_charts'] is True and c['nonlinear_jet_exact_not_approximate'] is True and c['vertical_curvature_remains_positive'] is True,'whole nonlinear geometric claim')
 need(science['follow_up'] is None and science['mathematical_gap'] is None and science['source_equation13_vs_literal_equation14_distinction_retained'],'exact root-cleared scope')
 need(not cfg['credit']['specific_2025_Naumann_habilitation_body_recovered'] and cfg['credit']['specific_2025_Naumann_habilitation_overlap']=='UNKNOWN','specific priority gap preserved')
 need(not cfg['credit']['worldwide_firstness_claimed'] and not cfg['credit']['Griffiths_refutation_claimed'],'no invented stronger claim')
 need(not cfg['copy']['human_peer_review_claimed'] and not cfg['copy']['formal_proof_assistant_certification_claimed'],'review type not promoted')
 need(cfg['source_programs_or_scientific_campaigns_replayed'] is False,'no source science replay in editorial task')
 originals={'source_ready_original':'SOURCE_READY.json','source_manifest_original':'SOURCE_READY_MANIFEST.json','source_seal_original':'SOURCE_READY_SEAL.json','native_record_original':'record.raw.json','native_latest_original':'latest.raw.json','native_versions_original':'versions.raw.json','native_normalized_metadata_original':'normalized-metadata.json','five_whole_transport_objects_in_native_order':'api-receipts.json','native_archive_custody_original':'archive-members.json'}
 for key,name in originals.items():need(snap[key]==load(E/'inputs'/name),'whole original native object '+key)
 need('schema' not in snap['source_ready_original'] and len(snap['five_whole_transport_objects_in_native_order'])==5,'actual absent schema and FIVE mixed endpoints')
 need(cfg['whole_native_transport_objects_preserved']==5 and cfg['all_three_custom_verdicts_preserved_whole'] is True and cfg['historical_flags_preserved'] is True and src['readiness_schema_tag_present'] is False,'literal native preservation fields')
 for lane in ['scope','analytic','adversarial']:need(snap['literal_three_custom_verdicts'][lane]==load(E/'inputs'/f'{lane}-VERDICT.json'),'whole literal custom verdict '+lane)
 need(snap['acquisition_verdict_original']==load(E/'inputs/acquisition-VERDICT.json') and snap['historical_flags_preserved_without_current_state_reinterpretation'],'old flags not rewritten')
 for key in ['PDF','ZIP']:
  a=src[key];f=Q/a['file'];need(f.stat().st_size==a['bytes'] and sha(f)==a['SHA256'],'unchanged promoted native asset '+key)
  original=snap['source_ready_original']['all_assets_in_original_order'][0 if key=='PDF' else 1]
  need(a['SHA256']==original['sha256'] and a['bytes']==original['bytes'],'exact private asset against original native identity '+key)
 return {'literal_status':'PRIVATE_FULL_COUNTEREXAMPLE_COPY_STATE_NATIVE_OBJECTS_AND_ASSETS_SUPPORTED','paragraph_characters':len(body),'native_transport_objects':5,'whole_custom_verdicts':3,'PDF_pages':4,'ZIP_payloads':40}
def main():
 need(len(sys.argv)==1,'no overrides');cfg=load(Q/'promotion.json');snap=load(E/'LITERAL_INPUT_SNAPSHOT.json')
 result=semantic((Q/'page.html').read_text(),cfg,snap)
 for r in load(E/'INPUT_MANIFEST.json')['files']:
  f=Path(r['path']);need(f.stat().st_size==r['bytes'] and sha(f)==r['sha256'],'all immutable source/scientific input bytes '+str(f))
 if (E/'SEAL.json').exists():
  seal=load(E/'SEAL.json');need(sha(E/'OWNED_MANIFEST.json')==seal['owned_manifest_sha256'],'owned manifest sealed')
  rows=load(E/'OWNED_MANIFEST.json')['files'];expected={r['path']:(r['bytes'],r['sha256']) for r in rows}
  actual={str(f.resolve()):(f.stat().st_size,sha(f)) for base in [E,Q] for f in base.rglob('*') if f.is_file() and not(base==E and str(f.relative_to(E)) in EXCLUDED)}
  need(actual==expected,'entire final editorial/promotion owned set')
  for opt,name in [(False,'FALSIFIERS_NORMAL.json'),(True,'FALSIFIERS_OPTIMIZED.json')]:
   a=subprocess.run([sys.executable,'-E','-B']+(['-O'] if opt else [])+[str(E/'falsifiers.py')],capture_output=True,timeout=30)
   need(a.returncode==0 and not a.stderr and a.stdout==(E/name).read_bytes(),'read-only semantic fault controls '+name)
  after={str(f.resolve()):(f.stat().st_size,sha(f)) for base in [E,Q] for f in base.rglob('*') if f.is_file() and not(base==E and str(f.relative_to(E)) in EXCLUDED)}
  need(after==actual==expected,'owned bytes unchanged after semantic controls')
  result.update(editorial_semantic_faults_each_mode=32,editorial_semantic_fault_executions=64,owned_files_verified=len(expected))
 result.update(input_files_unchanged=len(load(E/'INPUT_MANIFEST.json')['files']),scientific_programs_replayed=False,network_or_file_writes=False,publication_authority=False)
 print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
