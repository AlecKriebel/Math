#!/usr/bin/env python3
"""Fixed ten-path private assembly. Default is read-only; --build creates once.
No Git subprocesses, source/science imports, rendering, browser or network access.
Only the fixed candidate inside this owned folder is writable in explicit build.
"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin,urlsplit,unquote
from datetime import date
import argparse,hashlib,html,json,mimetypes,re,stat,xml.etree.ElementTree as ET
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
W=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
O=P/'verification/coefficient-boundary-private-stage-sol-20261116';C=O/'candidate'
INITIAL_SHA='34a63c3cb4ce1be6076ff214c4e37b2f1e01ff18be47a4bbe4d2772589395882'
def need(x,why):
 if not x:raise ValueError(why)
def sha(b):return hashlib.sha256(b).hexdigest()
def pinned(row,root=P):
 p=root/row['path'];need(not any(q.is_symlink()for q in [p,*p.parents]),'No symlink source');s=p.lstat();need(stat.S_ISREG(s.st_mode),'Regular source');b=p.read_bytes();need(len(b)==row['bytes']and sha(b)==row['SHA256'],'Whole source pin '+str(p));return b
def filepin(p):
 s=p.lstat();need(stat.S_ISREG(s.st_mode),'Regular file');b=p.read_bytes();return {'bytes':len(b),'SHA256':sha(b),'mode':oct(stat.S_IMODE(s.st_mode))}
class Tags(HTMLParser):
 def __init__(self,s):
  super().__init__(convert_charrefs=True);self.tags=[];self.meta={};self.feed(s)
 def handle_starttag(self,t,attrs):
  a=dict(attrs);self.tags.append((t,a))
  if t=='meta'and('name'in a or'property'in a):
   k=a.get('name',a.get('property'));need(k not in self.meta,'Duplicate metadata');self.meta[k]=a.get('content')
class Text(HTMLParser):
 def __init__(self,s):super().__init__(convert_charrefs=True);self.parts=[];self.feed(s)
 def handle_data(self,s):self.parts.append(s)
def text(s):return ''.join(Text(s).parts).strip()
def ld(s):
 matches=re.findall(r'<script type="application/ld\+json">(.*?)</script>',s,re.S);need(len(matches)==1,'One JSONLD object');return json.loads(matches[0])
def escaped(s):return html.escape(str(s),quote=True)
def dumps(x):return json.dumps(x,ensure_ascii=False).replace('<','\\u003c')
def actual_abstract(main):
 s=main.decode();m=re.search(r'<p id="original-abstract">(.*?)</p>',s,re.S)
 if m:return text(m[1])
 section=re.search(r'<section id="original-abstract"[^>]*>(.*?)</section>',s,re.S);need(section is not None,'Actual original-abstract section');paragraphs=re.findall(r'<p>(.*?)</p>',section[1],re.S);need(len(paragraphs)==1,'One whole abstract paragraph');return text(paragraphs[0])
def intake():
 raw=(O/'INITIAL.json').read_bytes();need(sha(raw)==INITIAL_SHA,'Initial frozen');i=json.loads(raw);b=json.loads(pinned(i['baseline'],O))
 need((W/'.git/HEAD').read_text()=='ref: refs/heads/master\n'and(W/'.git/refs/heads/master').read_text().strip()==b['HEAD'],'Current W master unchanged');need(filepin(W/'.git/index')==b['index'],'Native index exact')
 files={};dirs={}
 for p in sorted((W/'public').rglob('*')):
  s=p.lstat();need(not p.is_symlink(),'No W symlink')
  if stat.S_ISREG(s.st_mode):files[p.relative_to(W).as_posix()]=filepin(p)
  else:need(stat.S_ISDIR(s.st_mode),'Ordinary W directory');dirs[p.relative_to(W).as_posix()]=oct(stat.S_IMODE(s.st_mode))
 need((files,dirs)==(b['files'],b['directories']),'Whole674file W bytes/modes/topology')
 return i,b

def compose(i):
 files={};rows=[]
 for r in i['records']:
  authority=json.loads(pinned(r['authority']));preview=pinned(r['preview']).decode();model=json.loads(pinned(r['model']));native=json.loads(pinned(r['native']));meta=native['metadata'];need(meta==r['native_metadata']==model.get('native_metadata_original',model.get('native_metadata')),'Original metadata whole equal')
  main=re.search(rb'<main\b.*?</main>',preview.encode(),re.S)[0];need(len(main)==r['MAIN']['bytes']and sha(main)==r['MAIN']['SHA256']==authority['approved_whole_MAIN']['SHA256'],'Whole approved MAIN exact');need(authority['proposed_slug'].strip('/').removeprefix('research/')==r['slug'],'Root slug')
  head=preview.split('<head>',1)[1].split('</head>',1)[0];ht=Tags(head);article=ld(head);article.pop('@context',None);abstract=actual_abstract(main)
  if 'abstract'in article:need(article['abstract']==abstract,'Existing full abstract exact')
  article['abstract']=abstract
  title=html.unescape(re.search(r'<title>(.*?)</title>',head,re.S)[1]);description=ht.meta['description'];route='/research/'+r['slug']+'/';url=i['site_base']+route;stem='public'+route;need(not(W/stem).exists(),'No current route collision')
  assets={a['name']:pinned(a)for a in r['assets_in_native_order']};pdf=next(n for n in assets if n.endswith('.pdf'))
  article.update({'@id':url+'#article','url':url,'mainEntityOfPage':{'@id':url+'#page'}});article['encoding']=[{'@type':'MediaObject','name':name,'encodingFormat':mimetypes.guess_type(name)[0]or'application/octet-stream','contentUrl':url+name,'sameAs':'https://zenodo.org/api/records/'+str(r['record_id'])+'/files/'+name+'/content'}for name in assets]
  page={'@type':'WebPage','@id':url+'#page','url':url,'name':article['headline'],'dateCreated':i['assembly_day_UTC'],'dateModified':i['assembly_day_UTC'],'mainEntity':{'@id':url+'#article'}}
  public={k:v for k,v in ht.meta.items()if k not in ['viewport','robots','research_preview_status','editorial-status']};public.update({'author':'Alec Kriebel','robots':'index,follow','citation_pdf_url':url+pdf,'og:url':url,'og:site_name':'Alec Kriebel','DC.description':abstract,'DC.identifier':'doi:'+meta['doi'],'DC.rights':'CC BY 4.0','twitter:card':'summary','twitter:title':article['headline'],'twitter:description':description})
  metatags='\n'.join('<meta '+('property'if k.startswith(('og:','article:'))else'name')+'="'+escaped(k)+'" content="'+escaped(v)+'">'for k,v in public.items())
  prefix='<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<title>'+escaped(title)+'</title>\n'+metatags+'\n<link rel="canonical" href="'+url+'">\n<link rel="icon" href="/favicon.ico">\n<link rel="stylesheet" href="/research/research.css">\n<style>main p,main li,main td,main th{overflow-wrap:anywhere}main pre{white-space:pre-wrap;overflow-wrap:anywhere}sup{white-space:nowrap}</style>\n<script type="application/ld+json">'+dumps({'@context':'https://schema.org','@graph':[page,article]})+'</script>\n</head>\n<body>\n<a class="skip-link" href="#main">Skip to content</a>\n<header><p class="site-title"><a href="/">Alec Kriebel</a></p><nav aria-label="Main navigation"><a href="/research/">Research</a> | <a href="/blog/">Blog</a> | <a href="https://orcid.org/0009-0001-9320-500X">ORCID</a></nav></header>\n'
  suffix='\n<footer><hr><p><a href="/research/">Research home</a></p><p class="copyright">© 2013–2026 Kriebel LLC.</p></footer>\n</body>\n</html>\n';files[stem+'index.html']=prefix.encode()+main+suffix.encode();files[stem+'citation.bib']=pinned(r['Bib']);files.update({stem+name:data for name,data in assets.items()})
  rows.append({'route':route,'url':url,'title':meta['title'],'headline':article['headline'],'description':description,'PDF':pdf,'date':meta['publication_date'],'doi':meta['doi'],'status':article['creativeWorkStatus'],'abstract':abstract,'MAIN_SHA256':sha(main)})
 old=(W/'public/research/index.html').read_text();m=re.search(r'(<script type="application/ld\+json">)(.*?)(</script>)',old,re.S);obj=json.loads(m[2]);need(len(obj['mainEntity']['itemListElement'])==obj['mainEntity']['numberOfItems']==105,'Old105index')
 js=m[2];need(js.count('"numberOfItems": 105')==1 and js.endswith(']}}'),'Known static index representation');js=js.replace('"numberOfItems": 105','"numberOfItems": 107');add=[{'@type':'ListItem','position':106+n,'url':r['url'],'name':r['title']}for n,r in enumerate(rows)];js=js[:-3]+', '+', '.join(dumps(a)for a in add)+js[-3:];index=old[:m.start(2)]+js+old[m.end(2):]
 marker='    </ul>\n    <p>I’m gradually';need(index.count(marker)==1,'Unique visible append point');newli=''.join('      <li><a href="'+r['route']+'">'+escaped(r['title'])+'</a><br><span class="entry-meta">'+date.fromisoformat(r['date']).strftime('%-d %B %Y')+' · '+escaped(r['status'])+'</span><p>'+escaped(r['description'])+'</p><p><a href="'+r['route']+r['PDF']+'">PDF</a> · <a href="https://doi.org/'+r['doi']+'">Zenodo</a></p></li>\n'for r in rows);files['public/research/index.html']=index.replace(marker,newli+marker).encode()
 sm=(W/'public/research/sitemap.xml').read_text();need(len(ET.fromstring(sm))==106 and sm.count('</urlset>')==1,'Old106sitemap');extra=''.join('  <url><loc>'+r['url']+'</loc><lastmod>'+i['assembly_day_UTC']+'</lastmod></url>\n'for r in rows);files['public/research/sitemap.xml']=sm.replace('</urlset>',extra+'</urlset>').encode();need(set(files)==set(i['expected_paths'])and len(files)==10,'Exact10paths');return files,rows

def verify(i,b,files,rows):
 nodes=list(C.rglob('*'));need(not any(p.is_symlink()for p in nodes),'No candidate symlinks');actual={p.relative_to(C).as_posix():p for p in nodes if p.is_file()};need(set(actual)==set(files),'Exact10file namespace');dirs={q.relative_to(C).as_posix()for n in files for q in(C/n).parents if q!=C and C in q.parents};need({p.relative_to(C).as_posix()for p in nodes if p.is_dir()}==dirs,'Exact candidate directory namespace')
 for n,data in files.items():need(actual[n].read_bytes()==data and stat.S_IMODE(actual[n].stat().st_mode)==0o644,'Candidate whole bytes/mode')
 for r,row in zip(i['records'],rows):
  body=files['public'+row['route']+'index.html'];s=body.decode();h=Tags(s);ids=[a['id']for t,a in h.tags if'id'in a];need(len(ids)==len(set(ids))and[a.get('id')for t,a in h.tags if t=='main']==['main']and sum(t=='h1'for t,a in h.tags)==1,'Main/H1/IDs')
  main=re.search(rb'<main\b.*?</main>',body,re.S)[0];need(sha(main)==r['MAIN']['SHA256'],'Approved MAIN untouched');graph=ld(s)['@graph'];article=next(a for a in graph if a['@type']=='ScholarlyArticle');need(article['abstract']==actual_abstract(main)==row['abstract']==h.meta['DC.description'],'Full actual abstract in MAIN/JSONLD/DC')
  need(h.meta['robots']=='index,follow'and not{'research_preview_status','editorial-status'}&set(h.meta),'Release metadata no private markers');need(h.meta['citation_title']==r['native_metadata']['title']and h.meta['citation_publication_date']==row['date'].replace('-','/')and h.meta.get('citation_version')==r['native_metadata'].get('version'),'Original native title/date/version')
  need([a.get('href')for t,a in h.tags if t=='link'and a.get('rel')=='canonical']==[row['url']]and h.meta['og:url']==row['url']and h.meta['citation_pdf_url']==row['url']+row['PDF'],'Canonical/OG/local PDF metadata')
  need([a['name']for a in article['encoding']]==[a['name']for a in r['assets_in_native_order']],'Native encoding order')
  for t,a in h.tags:
   for k in ('src','href'):
    if k not in a:continue
    u=urlsplit(a[k]);need(u.scheme in ('','https'),'Safe link scheme')
    if u.scheme or u.netloc:continue
    need('..'not in Path(unquote(u.path)).parts,'No local traversal');url=urlsplit(urljoin(row['url'],a[k]));name='public'+unquote(url.path);name+='index.html'if name.endswith('/')else'';need(name in files or name in b['files'],'Local link exists '+a[k])
    if url.fragment and name.endswith('.html'):
     other=Tags((files[name]if name in files else(W/name).read_bytes()).decode());need(unquote(url.fragment)in[a['id']for t,a in other.tags if'id'in a],'Fragment exists')
 old=(W/'public/research/index.html').read_text();new=files['public/research/index.html'].decode();oldli=re.findall(r'<li>.*?</li>',old,re.S);newli=re.findall(r'<li>.*?</li>',new,re.S);need(len(oldli)==105 and len(newli)==107 and newli[:105]==oldli,'All105old visible entries exact');oldld=ld(old);newld=ld(new);need(newld['mainEntity']['itemListElement'][:105]==oldld['mainEntity']['itemListElement']and newld['mainEntity']['numberOfItems']==107,'All105old JSONLD items exact');need([a['name']for a in newld['mainEntity']['itemListElement'][105:]]==[r['native_metadata']['title']for r in i['records']],'New index uses full native titles')
 restored=new
 for li in newli[105:]:restored=restored.replace('      '+li+'\n','',1)
 om=re.search(r'<script type="application/ld\+json">(.*?)</script>',old,re.S);nm=re.search(r'<script type="application/ld\+json">(.*?)</script>',restored,re.S);restored=restored[:nm.start(1)]+om[1]+restored[nm.end(1):];need(restored==old,'No other index byte changes');oldsm=(W/'public/research/sitemap.xml').read_bytes();sm=files['public/research/sitemap.xml'];need(sm.startswith(oldsm[:oldsm.rfind(b'</urlset>')])and len(ET.fromstring(sm))==108,'All106old sitemap entries/prefix preserved');intake()
 return {'status':'PASS_FIXED_TWO_PAGE_PRIVATE10_PATH_STAGE','candidate_files':10,'candidate_directories':sorted(dirs),'new_leaves':8,'aggregate_replacements':2,'projected_counts':[682,107,108],'old_visible_JSONLD_items_preserved':105,'old_sitemap_entries_preserved':106,'whole2MAINs_4native_assets_2Bibs_exact':True,'boundary_JSONLD_abstract_source':'Actual complete approved MAIN section#original-abstract paragraph','index_full_native_titles':[r['native_metadata']['title']for r in i['records']],'candidate_pins':[{'path':n,'bytes':len(v),'SHA256':sha(v)}for n,v in sorted(files.items())],'helper_SHA256':sha(Path(__file__).read_bytes()),'proposed_canonicals':[r['url']for r in rows],'AA':None,'follow_up':None,'publication_authority':False,'W_baseline_unchanged':True,'render_browser_loopback_executions':False}
def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--build',action='store_true');args=parser.parse_args();i,b=intake();files,rows=compose(i)
 if args.build:
  need(not C.exists(),'Single exclusive private build')
  for name,data in files.items():
   p=C/name;need(C in p.parents and'..'not in p.parts,'Owned candidate boundary');p.parent.mkdir(parents=True,exist_ok=True)
   with p.open('xb')as f:f.write(data)
   p.chmod(0o644)
 result=verify(i,b,files,rows);print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
