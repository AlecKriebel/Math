#!/usr/bin/env python3
"""Fixed private fifteen-path stage. Default verifies without writes.
Only --build creates new private payloads; --serve verifies then binds loopback.
No project imports, Git commands, scientific programs, outside requests or W writes.
"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,urljoin,unquote
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from datetime import date
import argparse,hashlib,html,json,mimetypes,re,stat,xml.etree.ElementTree as ET
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
W=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
O=P/'verification/tsp-qss-fine-wilf-private-stage-sol-20261116';C=O/'candidate'
INITIAL_SHA='51345c929a993fee845bd27e3c234913f8bb91cc3256c62f98341e705c25a61c'
def need(x,why):
 if not x:raise ValueError(why)
def sha(b):return hashlib.sha256(b).hexdigest()
def pins(p):
 s=p.lstat();need(stat.S_ISREG(s.st_mode),'Regular file required');b=p.read_bytes();return {'bytes':len(b),'SHA256':sha(b),'mode':oct(stat.S_IMODE(s.st_mode))}
def readpin(row,root=P):
 p=root/row['path'];need(not any(x.is_symlink()for x in [p,*p.parents]),'Source symlink');b=p.read_bytes();need(len(b)==row['bytes']and sha(b)==row['SHA256'],'Source bytes changed '+str(p));return b
class Tags(HTMLParser):
 def __init__(self,text):
  super().__init__(convert_charrefs=True);self.tags=[];self.meta={};self.feed(text)
 def handle_starttag(self,t,attrs):
  a=dict(attrs);self.tags.append((t,a))
  if t=='meta'and('name'in a or'property'in a):
   k=a.get('name',a.get('property'));need(k not in self.meta,'Duplicate meta');self.meta[k]=a.get('content')
def ld(text):
 blocks=re.findall(r'<script type="application/ld\+json">(.*?)</script>',text,re.S);need(len(blocks)==1,'One JSONLD object');return json.loads(blocks[0])
def j(x):return json.dumps(x,ensure_ascii=False).replace('<','\\u003c')
def e(x):return html.escape(str(x),quote=True)
def intake():
 raw=(O/'INITIAL.json').read_bytes();need(sha(raw)==INITIAL_SHA,'Initial changed');i=json.loads(raw);b=json.loads(readpin(i['baseline'],O))
 need((W/'.git/HEAD').read_text()=='ref: refs/heads/master\n'and(W/'.git/refs/heads/master').read_text().strip()==b['HEAD'],'W HEAD unchanged')
 need(pins(W/'.git/index')==b['native_index'],'Native W index unchanged')
 files={};dirs={}
 for p in sorted((W/'public').rglob('*')):
  s=p.lstat();need(not p.is_symlink(),'W symlink')
  if stat.S_ISREG(s.st_mode):files[p.relative_to(W).as_posix()]=pins(p)
  else:need(stat.S_ISDIR(s.st_mode),'W special node');dirs[p.relative_to(W).as_posix()]=oct(stat.S_IMODE(s.st_mode))
 need((files,dirs)==(b['files'],b['directories']),'Whole W661 topology/bytes/modes unchanged')
 return i,b

def compose(i):
 files={};rows=[]
 for r in i['records']:
  authority=json.loads(readpin(r['root_authority']));preview=readpin(r['preview']).decode();model=json.loads(readpin(r['model']));native=json.loads(readpin(r['native_record']))
  need(native['metadata']==r['native_metadata']==model['native_metadata_original'],'Native metadata exact')
  main=readpin(r['MAIN'])if r['MAIN']['path']else re.search(rb'<main\b.*?</main>',preview.encode(),re.S)[0]
  need(len(main)==r['MAIN']['bytes']and sha(main)==r['MAIN']['SHA256'],'Approved whole MAIN')
  need(authority['approved_whole_MAIN']['SHA256']==sha(main)and authority['proposed_slug'].strip('/').removeprefix('research/')==r['slug'],'Root MAIN/slug authority')
  head=preview.split('<head>',1)[1].split('</head>',1)[0];original=Tags(head);article=ld(head);article.pop('@context',None)
  title=html.unescape(re.search(r'<title>(.*?)</title>',head,re.S)[1]);description=original.meta['description'];url=i['site_base']+'/research/'+r['slug']+'/';route='public/research/'+r['slug']+'/'
  need(not(W/'public/research'/r['slug']).exists(),'Existing route collision')
  assets={a['name']:readpin(a)for a in r['assets_in_native_order']};pdf=next(n for n in assets if n.endswith('.pdf'))
  article.update({'@id':url+'#article','url':url,'mainEntityOfPage':{'@id':url+'#page'}})
  article['encoding']=[{'@type':'MediaObject','name':name,'encodingFormat':mimetypes.guess_type(name)[0]or'application/octet-stream','contentUrl':url+name,'sameAs':'https://zenodo.org/api/records/'+str(r['record_id'])+'/files/'+name+'/content'}for name in assets]
  page={'@type':'WebPage','@id':url+'#page','url':url,'name':article['headline'],'dateCreated':i['assembly_day_UTC'],'dateModified':i['assembly_day_UTC'],'mainEntity':{'@id':url+'#article'}}
  meta={k:v for k,v in original.meta.items()if k not in ['robots','research_preview_status','viewport']};meta.update({'robots':'index,follow','citation_pdf_url':url+pdf,'og:url':url,'DC.description':article['abstract'],'DC.identifier':'doi:'+native['metadata']['doi'],'DC.rights':'CC BY 4.0','twitter:title':article['headline'],'twitter:description':description})
  tags='\n'.join('<meta '+('property'if k.startswith('og:')or k.startswith('article:')else'name')+'="'+e(k)+'" content="'+e(v)+'">'for k,v in meta.items())
  prefix='<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<title>'+e(title)+'</title>\n'+tags+'\n<link rel="canonical" href="'+url+'">\n<link rel="icon" href="/favicon.ico">\n<link rel="stylesheet" href="/research/research.css">\n<style>main p,main li,main td,main th{overflow-wrap:anywhere}main pre{white-space:pre-wrap;overflow-wrap:anywhere}sup{white-space:nowrap}</style>\n<script type="application/ld+json">'+j({'@context':'https://schema.org','@graph':[page,article]})+'</script>\n</head>\n<body>\n<a class="skip-link" href="#main">Skip to content</a>\n<header><p class="site-title"><a href="/">Alec Kriebel</a></p><nav aria-label="Main navigation"><a href="/research/">Research</a> | <a href="/blog/">Blog</a> | <a href="https://orcid.org/0009-0001-9320-500X">ORCID</a></nav></header>\n'
  suffix='\n<footer><hr><p><a href="/research/">Research home</a></p><p class="copyright">© 2013–2026 Kriebel LLC.</p></footer>\n</body>\n</html>\n'
  files[route+'index.html']=prefix.encode()+main+suffix.encode();files[route+'citation.bib']=readpin(r['Bib']);files.update({route+name:data for name,data in assets.items()})
  rows.append({'route':'/research/'+r['slug']+'/','url':url,'title':article['headline'],'description':description,'pdf':pdf,'date':native['metadata']['publication_date'],'doi':native['metadata']['doi'],'status':article['creativeWorkStatus'],'MAIN_SHA256':sha(main)})
 old=(W/'public/research/index.html').read_text();m=re.search(r'(<script type="application/ld\+json">)(.*?)(</script>)',old,re.S);obj=json.loads(m[2]);items=obj['mainEntity']['itemListElement'];need(len(items)==obj['mainEntity']['numberOfItems']==102,'Old102index')
 text=m[2];need(text.count('"numberOfItems": 102')==1 and text.endswith(']}}'),'Known aggregate representation');text=text.replace('"numberOfItems": 102','"numberOfItems": 105');added=[{'@type':'ListItem','position':103+n,'url':r['url'],'name':r['title']}for n,r in enumerate(rows)];text=text[:-3]+', '+', '.join(j(x)for x in added)+text[-3:]
 index=old[:m.start(2)]+text+old[m.end(2):];marker='    </ul>\n    <p>I’m gradually';need(index.count(marker)==1,'Unique append point')
 additions=''.join('      <li><a href="'+r['route']+'">'+e(r['title'])+'</a><br><span class="entry-meta">'+date.fromisoformat(r['date']).strftime('%-d %B %Y')+' · '+e(r['status'])+'</span><p>'+e(r['description'])+'</p><p><a href="'+r['route']+r['pdf']+'">PDF</a> · <a href="https://doi.org/'+r['doi']+'">Zenodo</a></p></li>\n'for r in rows)
 files['public/research/index.html']=index.replace(marker,additions+marker).encode();sm=(W/'public/research/sitemap.xml').read_text();need(len(ET.fromstring(sm))==103 and sm.count('</urlset>')==1,'Old103sitemap')
 files['public/research/sitemap.xml']=sm.replace('</urlset>',''.join('  <url><loc>'+r['url']+'</loc><lastmod>'+i['assembly_day_UTC']+'</lastmod></url>\n'for r in rows)+'</urlset>').encode();need(set(files)==set(i['expected_paths'])and len(files)==15,'Exact15paths');return files,rows

def verify(i,b,files,rows):
 nodes=list(C.rglob('*'));need(not any(p.is_symlink()for p in nodes),'No candidate symlinks');actual={p.relative_to(C).as_posix():p for p in nodes if p.is_file()};need(set(actual)==set(files),'Exact candidate file namespace')
 dirs={q.relative_to(C).as_posix()for n in files for q in(C/n).parents if q!=C and C in q.parents};need({p.relative_to(C).as_posix()for p in nodes if p.is_dir()}==dirs,'Exact candidate directory namespace')
 for n,data in files.items():need(actual[n].read_bytes()==data and stat.S_IMODE(actual[n].stat().st_mode)==0o644,'Whole candidate buffer/mode')
 for r,row in zip(i['records'],rows):
  path='public'+row['route']+'index.html';text=files[path].decode();tags=Tags(text);ids=[a['id']for t,a in tags.tags if'id'in a];need(len(ids)==len(set(ids))and[a.get('id')for t,a in tags.tags if t=='main']==['main']and sum(t=='h1'for t,a in tags.tags)==1,'Actual main/H1/IDs')
  main=re.search(rb'<main\b.*?</main>',files[path],re.S)[0];need(sha(main)==r['MAIN']['SHA256'],'Whole approved MAIN remains unchanged');need('research_preview_status'not in tags.meta and tags.meta['robots']=='index,follow','Public metadata no private markers')
  need(tags.meta['citation_publication_date']==row['date'].replace('-','/')and tags.meta.get('citation_version')==r['native_metadata'].get('version'),'Native date/version absence')
  for t,a in tags.tags:
   for k in ('src','href'):
    if k not in a:continue
    u=urlsplit(a[k]);need(u.scheme in ('','https'),'Safe link scheme')
    if u.scheme or u.netloc:continue
    need('..'not in Path(unquote(u.path)).parts,'No traversal link');target=urlsplit(urljoin(row['url'],a[k]));name='public'+unquote(target.path);name+='index.html'if name.endswith('/')else'';need(name in files or name in b['files'],'Local link resolves '+a[k])
    if target.fragment and name.endswith('.html'):
     other=Tags((files[name]if name in files else(W/name).read_bytes()).decode());need(unquote(target.fragment)in[a['id']for t,a in other.tags if'id'in a],'Fragment resolves')
 old=(W/'public/research/index.html').read_text();new=files['public/research/index.html'].decode();oldli=re.findall(r'<li>.*?</li>',old,re.S);newli=re.findall(r'<li>.*?</li>',new,re.S);need(len(oldli)==102 and len(newli)==105 and newli[:102]==oldli,'All102old visible entries exact');need(ld(new)['mainEntity']['itemListElement'][:102]==ld(old)['mainEntity']['itemListElement'],'All102old JSONLD items exact')
 restored=new
 for entry in newli[102:]:restored=restored.replace('      '+entry+'\n','',1)
 om=re.search(r'<script type="application/ld\+json">(.*?)</script>',old,re.S);nm=re.search(r'<script type="application/ld\+json">(.*?)</script>',restored,re.S);restored=restored[:nm.start(1)]+om[1]+restored[nm.end(1):];need(restored==old,'No unrelated index byte changes')
 sm=files['public/research/sitemap.xml'];oldsm=(W/'public/research/sitemap.xml').read_bytes();need(sm.startswith(oldsm[:oldsm.rfind(b'</urlset>')])and len(ET.fromstring(sm))==106,'All103old sitemap entries/prefix retained');intake()
 return {'status':'PASS_FIXED_PRIVATE15_PATH_STAGE','candidate_files':15,'candidate_directories':sorted(dirs),'new_leaves':13,'replacements':2,'projected_counts':[674,105,106],'old_visible_JSONLD_entries_preserved':102,'old_sitemap_entries_preserved':103,'whole3MAINs_7native_assets_3Bibs_exact':True,'candidate_pins':[{'path':n,'bytes':len(v),'SHA256':sha(v)}for n,v in sorted(files.items())],'helper_SHA256':sha(Path(__file__).read_bytes()),'canonical_candidates':[r['url']for r in rows],'AA':None,'follow_up':None,'production_authority':False,'W_baseline_unchanged':True}

def serve(files,b):
 class Handler(BaseHTTPRequestHandler):
  def do_GET(self):self.respond(False)
  def do_HEAD(self):self.respond(True)
  def respond(self,head):
   name='public/'+unquote(urlsplit(self.path).path).lstrip('/');name+='index.html'if name.endswith('/')else''
   if '..'in Path(name).parts or name not in set(files)|set(b['files']):self.send_error(404);return
   data=files[name]if name in files else(W/name).read_bytes();self.send_response(200);self.send_header('Content-Type',mimetypes.guess_type(name)[0]or'application/octet-stream');self.send_header('Content-Length',str(len(data)));self.send_header('Cache-Control','no-store');self.send_header('X-Robots-Tag','noindex,nofollow,noarchive');self.send_header('Content-Security-Policy',"default-src 'self'; style-src 'self' 'unsafe-inline'; frame-src 'self'; object-src 'self'; img-src 'self' data:; connect-src 'none'; base-uri 'none'; form-action 'none'");self.end_headers()
   if not head:self.wfile.write(data)
 server=ThreadingHTTPServer(('127.0.0.1',0),Handler);print(json.dumps({'private_loopback_URL':'http://127.0.0.1:'+str(server.server_port)}),flush=True)
 try:server.serve_forever()
 except KeyboardInterrupt:pass
 finally:server.server_close()
def main():
 parser=argparse.ArgumentParser(description=__doc__);g=parser.add_mutually_exclusive_group();g.add_argument('--build',action='store_true');g.add_argument('--serve',action='store_true');args=parser.parse_args();i,b=intake();files,rows=compose(i)
 if args.build:
  need(not C.exists(),'Exclusive first private build only')
  for name,data in files.items():
   p=C/name;need(C in p.parents and'..'not in p.parts,'Owned candidate boundary');p.parent.mkdir(parents=True,exist_ok=True)
   with p.open('xb')as f:f.write(data)
   p.chmod(0o644)
 result=verify(i,b,files,rows);print(json.dumps(result,ensure_ascii=False,indent=2),flush=True)
 if args.serve:serve(files,b)
if __name__=='__main__':main()
