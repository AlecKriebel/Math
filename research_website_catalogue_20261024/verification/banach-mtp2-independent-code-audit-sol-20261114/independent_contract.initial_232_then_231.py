#!/usr/bin/env python3
"""Read-only structural/content/overlay audit of exactly two new articles.
Uses an independently built element tree and actual approved section objects.
No old content campaigns or old fixture trees are produced.
"""
from pathlib import Path
from html.parser import HTMLParser
from html import unescape
import copy,hashlib,json,re,subprocess,sys,xml.etree.ElementTree as ET
sys.dont_write_bytecode=True
A=Path(__file__).resolve().parent;P=A.parents[1]
E=P/'verification/local-banach-mtp2-stage-sol-20261025/resume'
L=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public')
Q=A/'new-only-render/public'
rows=[]
def ck(label,value):
 rows.append({'check':label,'passed':bool(value)})
 if not value:raise RuntimeError(label)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def norm(s):return ' '.join(s.split())
class Node:
 def __init__(self,tag,attrs):self.tag=tag;self.attrs=dict(attrs);self.children=[]
 def text(self):return ''.join(x if isinstance(x,str) else x.text() for x in self.children)
 def all(self,tag=None):
  return ([self] if tag is None or tag==self.tag else [])+[y for x in self.children if isinstance(x,Node) for y in x.all(tag)]
class Tree(HTMLParser):
 def __init__(self,s):
  super().__init__(convert_charrefs=True);self.roots=[];self.stack=[];self.feed(s)
  ck('balanced independently parsed tree',not self.stack)
 def handle_starttag(self,t,attrs):
  n=Node(t,attrs);ck('unique attributes',len(n.attrs)==len(attrs))
  (self.stack[-1].children if self.stack else self.roots).append(n)
  if t not in {'meta','link','br','hr'}:self.stack.append(n)
 def handle_endtag(self,t):
  if not self.stack or self.stack[-1].tag!=t:raise RuntimeError('unbalanced tree '+t)
  self.stack.pop()
 def handle_data(self,s):
  if self.stack:self.stack[-1].children.append(s)
  elif s.strip():raise RuntimeError('outside-root text')
 def all(self,t=None):return [y for x in self.roots for y in x.all(t)]
def main():
 if len(sys.argv)!=1:raise ValueError('No arguments accepted')
 baseline=json.loads((E.parent/'BASELINE_ACTUAL_524.json').read_text())
 ck('actual production commit',subprocess.check_output(['git','-C',str(L.parent),'rev-parse','HEAD'],text=True).strip()=='262f0f4f3eafd513e1bd549960020678307d6c67')
 expected={x['path']:(x['bytes'],x['sha256']) for x in baseline['public_files']}
 actual={str(p):(p.stat().st_size,sha(p)) for p in L.rglob('*') if p.is_file()}
 ck('all actual524 baseline public bytes unchanged',len(actual)==524 and actual==expected)
 for x in baseline['actual_installed_core']:ck('baseline core '+Path(x['path']).name,Path(x['path']).stat().st_size==x['bytes'] and sha(Path(x['path']))==x['sha256'])
 additions=[];article_summaries={}
 for rid in ['23217863','23146753']:
  paper=P/'papers'/rid;c=json.loads((paper/'publication.json').read_text());ed=paper/'reviews/editorial'
  sections=json.loads((ed/'public-sections.json').read_text());out=E/'public/research'/c['slug'];independent=Q/'research'/c['slug']
  ck(rid+' exact four public files',set(x.name for x in out.iterdir())=={'index.html','citation.bib',c['pdf_filename'],c['supplement_filename']})
  for x in out.iterdir():ck(rid+' independent full rendering '+x.name,x.read_bytes()==(independent/x.name).read_bytes())
  t=Tree((out/'index.html').read_text());body=t.all('body');head=t.all('head')
  ck(rid+' one actual tree body and head',len(body)==len(head)==1)
  actual_sections={n.attrs['id']:n for n in t.all('section')}
  for key,sid in [('abstract','abstract'),('plain_language','plain-language'),('result','result'),('why_it_works','proof'),('limitations','limits')]:
   accepted=sections[key];accepted=accepted if isinstance(accepted,list) else [accepted]
   configured=c[key] if isinstance(c[key],list) else [c[key]]
   ps=[norm(x.text()) for x in actual_sections[sid].children if isinstance(x,Node) and x.tag=='p']
   ck(rid+' full approved ordered section '+sid,accepted==configured==ps)
  statuses=sections['status'] if isinstance(sections['status'],list) else [sections['status'],sections['ai_disclosure'],sections['edition_note']]
  ps=[norm(x.text()) for x in actual_sections['status'].children if isinstance(x,Node) and x.tag=='p']
  ck(rid+' full approved ordered status edition AI disclosure',ps==statuses)
  accepted=sections['collaboration'];accepted=accepted[0] if isinstance(accepted,list) else accepted
  ck(rid+' passive accepted collaboration',norm(actual_sections['collaborate'].all('p')[0].text())==accepted==c['collaboration'])
  background=actual_sections['background'].all('li')
  ck(rid+' every background credit and exact URL',len(background)==len(sections['background']) and all(norm(n.text())==x['title']+': '+x['note'] and [z.attrs['href'] for z in n.all('a')]==[x['url']] for n,x in zip(background,sections['background'])))
  tex=(paper/c['source_binding']['source_tex_path']).read_text();abstract=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',tex,re.S).group(1)
  ck(rid+' original abstract exact substring',abstract==(ed/'ORIGINAL_ABSTRACT.tex').read_text()==c['source_binding']['abstract_tex'])
  for x,y in ([('Banach--Mazur','Banach–Mazur'),('$*$','*'),('~',' ')] if rid=='23217863' else [('MTP$_2$','MTP₂'),('Conjecture~1','Conjecture 1')]):abstract=abstract.replace(x,y)
  ck(rid+' only authorized abstract typography',norm(abstract)==c['abstract'] and [norm(x.text()) for x in actual_sections['abstract'].all('h2')]==['Original abstract'])
  ck(rid+' original complete asset bytes',all((out/c[key]).read_bytes()==(paper/'sources'/c[key]).read_bytes() for key in ['pdf_filename','supplement_filename']))
  ck(rid+' exact prepared citation',(out/'citation.bib').read_bytes()==c['prepared_bibtex'].encode()==(paper/c['source_binding']['prepared_bibtex_path']).read_bytes())
  metas={x.attrs.get('name',x.attrs.get('property')):x.attrs.get('content') for x in head[0].all('meta')}
  base='https://aleckriebel.com/research/'+c['slug']+'/'
  ck(rid+' exact scholarly head identity',metas['citation_title']==metas['og:title']==c['title'] and metas['citation_doi']==c['doi'] and metas['citation_author']==c['author']=='Alec Kriebel' and metas['citation_author_orcid']=='0009-0001-9320-500X' and metas['citation_publication_date']==c['publication_date'].replace('-','/') and metas['description']==metas['og:description']==c['description'] and metas['og:url']==base and metas['citation_pdf_url']==base+c['pdf_filename'])
  graph=json.loads(head[0].all('script')[0].text())['@graph'];article=graph[1]
  ck(rid+' exact scholarly article dates abstract encoding license',article['abstract']==c['abstract'] and article['datePublished']==c['publication_date'] and article['license']==c['license_url'] and article['encoding']['contentUrl']==base+c['pdf_filename'] and article['author']==[{'@type':'Person','name':'Alec Kriebel','sameAs':c['orcid']}])
  ck(rid+' correct absent versus Zenodo version',('version' not in article if rid=='23217863' else article['version']=='1.0') and c['version_field_present'] is (rid=='23146753'))
  ck(rid+' genuine date not current creation date',t.all('time')[0].attrs=={'datetime':c['publication_date']} and article['datePublished']!=graph[0]['dateCreated'])
  if rid=='23217863':ck(rid+' full approved mixed licenses',[norm(x.text()) for x in actual_sections['licensing'].all('p')]==sections['licensing'])
  ck(rid+' Research and exact self navigation',[(x.attrs['href'],norm(x.text())) for x in t.all('nav')[0].all('a')][0]==('/research/','Research') and t.all('h1')[0].all('a')[0].attrs['href']=='/research/'+c['slug']+'/')
  ck(rid+' one complete local reader',len(t.all('iframe'))==1 and t.all('iframe')[0].attrs['src']==c['pdf_filename']+'#view=FitH')
  additions.append(c);article_summaries[rid]={'h2_labels':[norm(x.text()) for x in t.all('h2')],'html_sha256':sha(out/'index.html'),'publication_date':c['publication_date'],'version':c['version'],'source_status':json.loads((paper/'promotion.json').read_text())['status']}
 before=(L/'research/index.html').read_text();after=(E/'public/research/index.html').read_text()
 ck('independent complete index reproduction',after==(Q/'research/index.html').read_text())
 old_li=re.findall(r'<li>.*?</li>',before,re.S);new_li=re.findall(r'<li>.*?</li>',after,re.S)
 retained=[x for x in new_li if not any('/research/'+c['slug']+'/' in x for c in additions)]
 ck('old70 complete index entries byte-identical',len(old_li)==70 and len(new_li)==72 and retained==old_li)
 get_schema=lambda s:json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',s,re.S).group(1))
 oldjs=get_schema(before);newjs=get_schema(after);tmp=copy.deepcopy(newjs);tmp['mainEntity']['itemListElement']=tmp['mainEntity']['itemListElement'][:-2];tmp['mainEntity']['numberOfItems']-=2
 ck('only two ordered index schema additions',tmp==oldjs and newjs['mainEntity']['numberOfItems']==72 and all(x['url']=='https://aleckriebel.com/research/'+c['slug']+'/' and x['name']==c['title'] for x,c in zip(newjs['mainEntity']['itemListElement'][-2:],additions)))
 sm0=(L/'research/sitemap.xml').read_text();sm1=(E/'public/research/sitemap.xml').read_text()
 ck('independent complete sitemap reproduction',sm1==(Q/'research/sitemap.xml').read_text())
 old_urls=re.findall(r'<url>.*?</url>',sm0,re.S);new_urls=re.findall(r'<url>.*?</url>',sm1,re.S)
 ck('old71 complete sitemap entries byte-identical',len(old_urls)==71 and len(new_urls)==73 and new_urls[:-2]==old_urls)
 names={p.relative_to(L).as_posix() for p in L.rglob('*') if p.is_file()};overlay={p.relative_to(E/'public').as_posix() for p in (E/'public').rglob('*') if p.is_file()}
 ck('eight and only eight new public paths',len(overlay-names)==8 and len(names|overlay)==532 and len(overlay)==10)
 print(json.dumps({'status':'EXACT_TWO_RECORD_CONTRACT_AND_OVERLAY_SUPPORTED','controls':len(rows),'checks':rows,'article_summaries':article_summaries,'baseline_public':524,'resulting_overlay_public':532,'index_entries':72,'sitemap_entries':73,'old69_campaign_repeated':False,'old_article_fixture_trees_created':False},indent=2,ensure_ascii=False))
if __name__=='__main__':main()
