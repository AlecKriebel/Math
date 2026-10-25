from pathlib import Path
from html import unescape
from html.parser import HTMLParser
import hashlib,json,re,datetime,subprocess,zipfile
p=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/22729545');q=p/'reviews/publication-qa';site=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public/research')
c=json.loads((p/'publication.json').read_text());scope=json.loads((p/'reviews/scope/content.json').read_text());out=site/c['slug'];html=(out/'index.html').read_text();visible=unescape(re.sub('<[^>]+>',' ',html));source=(p/'sources/published-source/NMSC_Paper_B_Source/manuscript/main.tex').read_text();receipt=json.loads((p/'sources/receipt.json').read_text());record=json.loads((p/'sources/record.json').read_text())['metadata'];checks={}
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
def ws(t):return ' '.join(t.split())
def check(k,v):checks[k]=bool(v)
class Doc(HTMLParser):
 def __init__(self,t):super().__init__();self.tags=[];self.feed(t)
 def handle_starttag(self,t,a):self.tags.append((t,dict(a)))
d=Doc(html);links=[a.get('href') for t,a in d.tags if t=='a']
abstract=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',source,re.S).group(1).strip();segment=re.search(r'<section id="abstract">(.*?)</section>',html,re.S).group(1);paras=[unescape(x) for x in re.findall('<p>(.*?)</p>',segment,re.S)]
check('complete_actual_source_abstract',abstract==c['abstract']==scope['abstract'])
check('four_abstract_paragraphs',paras==abstract.split('\n\n') and len(paras)==4)
check('source_binding_preserved',c['source_binding']==scope['source_binding'])
check('approved_narrative_preserved',all(c[k]==scope[k] for k in ('title','description','plain_language','why_it_works','limitations','background','ai_disclosure')))
check('result_preserved_with_one_qualified_addition',[x.replace('eight specified equivalence moves, Q1–Q8.', 'eight specified equivalence moves.') for x in c['result'][:-1]]==scope['result'] and len(c['result'])==len(scope['result'])+1)
check('companion_finite_determination_qualified',all(x in c['result'][-1] for x in ('companion','finite determining locus length','fixed finite union','compact semianalytic normalized finite-presentation charts','no effective practical sequence-length bound')))
check('finite_determination_matches_section11',all(x in source for x in ('fixed finite union $K$ of compact semianalytic normalized finite-presentation charts','No effective practical sequence-length bound is claimed here.')))
check('publication_metadata',all(c[k]==record[k] for k in ('title','doi','version','publication_date')) and c['publication_date']=='2026-09-12')
check('manuscript_date_separate',r'\date{September 5, 2026}' in source and c['source_binding']['manuscript_date']=='2026-09-05' and 'Published <time datetime="2026-09-12">12 September 2026</time>' in html)
check('strong_tree_child_explicit','tree-child under every admissible rooting' in visible and 'stronger than checking the supplied rooting alone' in visible)
check('level_two_per_blob','limits each blob to two reticulations' in visible and 'does not limit the entire network to two reticulations' in visible)
check('positive_complete_sampling_temporal_hypotheses',all(x in visible for x in ('Samples are contemporaneous','known sampling map is surjective','piecewise-constant Kingman pair rates are positive','strictly between zero and one','distinct internal biological events have distinct ages','distinct parents')))
check('quotient_not_every_raw_parameter',all(x in visible for x in ('eight specified equivalence moves','entire exposed donor rate history transferred','not unique recovery of every raw event and parameter','two-outlet routing fans')))
check('all_indexed_small_marginals',all(x in visible for x in ('every labelled genealogy marginal on at most three sampled lineages','all relevant labelled pairs and triples','one triple, three nucleotide sites or three observed genealogies')))
check('companion_model_limits',all(x in visible for x in ('companion preprint','known boundaries','shared irreducible stationary reversible','common scale ambiguity','Unknown locus boundaries, recombination, nonreversible substitution and arbitrary demographic mixtures')))
check('exact_law_no_practical_inference_claim',all(x in visible for x in ('exact rooted metric-genealogy probability laws','No sample-size guarantee, noise-stability bound or efficient practical estimator','do not prove the universal theorem')))
check('prior_credit_preserved',all(x['url'] in links and x['title'] in visible and x['note'] in visible for x in scope['background']))
check('no_followups',c.get('follow_up') is None and 'id="further-research"' not in html)
check('unrefereed_ai_disclosure','Unrefereed preprint' in visible and c['ai_disclosure'] in visible)
check('authorship_single_statement',html.count('Authorship and responsibilities would be discussed in relation to the substantive contributions made.')==1 and 'Any authorship would reflect substantive contributions.' not in html)
check('collaboration_edit_only_duplicate',c['collaboration']==scope['collaboration'].replace(' Any authorship would reflect substantive contributions.','') and c['collaboration'] in visible)
expected='https://aleckriebel.com/research/'+c['slug']+'/'
check('canonical',[a.get('href') for t,a in d.tags if t=='link' and a.get('rel')=='canonical']==[expected])
check('pdf_embed',any(t=='iframe' and a.get('src')==c['pdf_filename']+'#view=FitH' for t,a in d.tags))
assets=[c['pdf_filename'],c['supplement_filename']]+[x['filename'] for x in c['additional_assets']]
check('four_expected_assets',set(assets)=={'NMSC_Paper_B_Main.pdf','NMSC_Paper_B_Supplement.pdf','NMSC_Paper_B_Source.zip','NMSC_Paper_B_Reproducibility.zip'})
for name in assets:
 check('immutable_'+name,sha(out/name)==sha(p/'sources'/name)==next(x['sha256'] for x in receipt['files'] if x['name']==name) and name in links)
 if name.endswith('.zip'):
  with zipfile.ZipFile(out/name) as z:check('zip_integrity_'+name,z.testzip() is None)
for name,pages in [('NMSC_Paper_B_Main.pdf',21),('NMSC_Paper_B_Supplement.pdf',11)]:
 text=subprocess.check_output(['pdftotext','-layout',str(out/name),'-'],text=True);check('pages_'+name,text.count('\f')==pages and 'PDF, '+str(pages)+' pages' in html)
check('source_zip_label','LaTeX source (ZIP)' in visible or 'Source (ZIP)' in visible or 'Source archive (ZIP)' in visible)
check('index_once',(site/'index.html').read_text().count('href="/research/'+c['slug']+'/"')==1)
check('sitemap_once',(site/'sitemap.xml').read_text().count('<loc>'+expected+'</loc>')==1)
gate=json.loads((p/'promotion.json').read_text());check('promotion_review_hashes',gate['status']=='PASS' and all(sha(p/x['report'])==x['sha256'] for x in gate['reviews'].values()))
imp=gate['companion_import'];check('companion_promotion_binding',imp['record_id']=='22729537' and imp['status']=='PASS' and sha(p/imp['promotion_file'])==imp['promotion_sha256'])
result={'record_id':'22729545','time_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS' if all(checks.values()) else 'ISSUES_FOUND','checks':checks,'hashes':{name:sha(path) for name,path in [('page',out/'index.html'),('publication',p/'publication.json'),('receipt',p/'sources/receipt.json'),('source_main_tex',p/'sources/published-source/NMSC_Paper_B_Source/manuscript/main.tex'),('citation',out/'citation.bib'),('promotion',p/'promotion.json')]},'scope':'Independent source/content/immutable-assets QA only. No mathematical rereview, no browser/live HTTP/deploy/outreach; no other paper inspected.'}
(q/'qa.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n');print(result['status'],len(checks),'checks',[(k,v) for k,v in checks.items() if not v])
