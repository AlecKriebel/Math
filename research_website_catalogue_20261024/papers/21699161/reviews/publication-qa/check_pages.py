from pathlib import Path
from html import unescape
from html.parser import HTMLParser
import hashlib,json,re,datetime,subprocess
root=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers')
site=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public/research')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def whitespace(t):return ' '.join(t.split())
def paragraphs(html):return [unescape(re.sub('<[^>]+>','',x)) for x in re.findall(r'<p>(.*?)</p>',html,re.S)]
class Doc(HTMLParser):
 def __init__(self,text):super().__init__();self.tags=[];self.feed(text)
 def handle_starttag(self,tag,attrs):self.tags.append((tag,dict(attrs)))
summary={}
for rid in ('21699161','22089551'):
 p=root/rid;scope=json.loads((p/'reviews/scope/content.json').read_text());c=json.loads((p/'publication.json').read_text());out=site/c['slug'];html=(out/'index.html').read_text();d=Doc(html);checks={}
 def check(key,val):checks[key]=bool(val)
 check('scope_source_bindings_preserved',c['source_binding']==scope['source_binding'])
 check('scope_narrative_preserved',all(c.get(k)==scope.get(k) for k in ('title','description','plain_language','result','limitations','why_it_works','background','ai_disclosure','collaboration','related_resources','additional_assets','supplement_filename')))
 check('abstract_complete_unchanged_words',whitespace(c['abstract'])==whitespace(scope['abstract']))
 abstract=re.search(r'<section id="abstract">(.*?)</section>',html,re.S).group(1);paras=paragraphs(abstract)
 check('abstract_visible_complete',whitespace(' '.join(paras))==whitespace(scope['abstract']))
 check('abstract_readable_paragraphs',len(paras)>=2)
 check('no_followups',c.get('follow_up') is None and 'id="further-research"' not in html)
 check('unrefereed_ai_disclosure','Unrefereed preprint' in html and c['ai_disclosure'] in unescape(html))
 check('professional_collaboration',c['collaboration'] in unescape(html) and html.count('Authorship and responsibilities would be discussed in relation to the substantive contributions made.')==1)
 expected='https://aleckriebel.com/research/'+c['slug']+'/'
 check('canonical',[(a.get('href')) for t,a in d.tags if t=='link' and a.get('rel')=='canonical']==[expected])
 check('pdf_iframe',any(t=='iframe' and a.get('src')==c['pdf_filename']+'#view=FitH' for t,a in d.tags))
 receipt=json.loads((p/'sources/receipt.json').read_text());assets=[c['pdf_filename']]+([c['supplement_filename']] if c.get('supplement_filename') else [])+[x['filename'] for x in c.get('additional_assets',[])]
 links=[a.get('href') for t,a in d.tags if t=='a']
 for name in assets:
  check('immutable_asset_'+name,sha(out/name)==sha(p/'sources'/name)==next(x['sha256'] for x in receipt['files'] if x['name']==name) and name in links)
 if rid=='21699161':
  metadata=json.loads((p/'sources/record.json').read_text())['metadata'];source=(p/'sources/related-records/21699181/published-source/main.tex').read_text()
  check('primary_record_no_numbered_version','version' not in metadata and c['version']=='July 2026' and r'\date{July 2026}' in source)
  check('archive_label_clear','Archive label v1.1.0' in unescape(html) and 'Version July 2026' not in unescape(html))
  check('edition_explanation','July 2026' in unescape(html) and re.search(r'Zenodo.{0,100}(?:no numbered version|does not specify a numbered version|does not supply a numbered version|does not list a numbered version|has no numbered version)',unescape(html),re.S) is not None)
  check('separate_companion_links',len(c['related_resources'])==4 and all(x['url'] in links and x['doi'] in unescape(html) for x in scope['related_resources']))
  check('no_invented_primary_supplement',c['supplement_filename'] is None and not any('/records/21699161/files/' in x and not c['pdf_filename'] in x for x in links if x))
  bib=(out/'citation.bib').read_text();check('citation_printed_and_archive_editions','July 2026' in bib and '1.1.0' in bib and 'July 2026' in re.search(r'<section id="cite">(.*?)</section>',html,re.S).group(1))
 else:
  source=(p/'sources/published-source/bimolecular_positive_recurrence_submission_v1_2_4/manuscript/paper_content.tex').read_text()
  nonjap=re.search(r'\\else\s*\\begin\{abstract\}(.*?)\\end\{abstract\}',source,re.S).group(1)
  check('actual_nonjap_abstract',whitespace(nonjap)==whitespace(scope['abstract']))
  extra=out/'supplementary-note-v1.2.4.pdf';text=subprocess.check_output(['pdftotext','-layout',str(extra),'-'],text=True)
  check('two_page_supplement_visible',text.count('\f')==2 and 'Supplementary note (PDF, 2 pages)' in unescape(html))
 check('index_once',(site/'index.html').read_text().count('href="/research/'+c['slug']+'/"')==1)
 check('sitemap_once',(site/'sitemap.xml').read_text().count('<loc>'+expected+'</loc>')==1)
 result={'record_id':rid,'time_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS' if all(checks.values()) else 'ISSUES_FOUND','checks':checks,'hashes':{x:sha(y) for x,y in [('page',out/'index.html'),('publication',p/'publication.json'),('primary_receipt',p/'sources/receipt.json'),('citation',out/'citation.bib')]},'scope':'Independent source/content/assets crosscheck; no browser or mathematical rereview. Parent/root handles browser, external HTTP and deployment.'}
 (p/'reviews/publication-qa/qa.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n');summary[rid]=result
 print(rid,result['status'],[k for k,v in checks.items() if not v])
