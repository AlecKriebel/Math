#!/usr/bin/env python3
"""Inert private-stage tools. CLI writes only this new stage. Source preparation
never reads the website. Website freeze and rendering require a later real GO.
No native/scientific code, network, dependency installation or subprocesses.
"""
from pathlib import Path
import copy
import datetime
import hashlib
import html
import json
import re
import sys

A=Path(__file__).resolve().parent
P=A.parent.parent
W=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
IDS=('23392409','23440943')
ROOTS={'23392409':(13689,'e493881b10b281ea2a1bc6aa66d15063374073df2f6a9b99edc5ef5587dc61bf'),
       '23440943':(12638,'e516ebd05ef8243a47f5b40bac31182a75751dcced857cb89ec5dbe9875b1ed6')}
CC='https://creativecommons.org/licenses/by/4.0/'
CSS='main p,main li,main td,main th{overflow-wrap:anywhere}main .math{white-space:pre-wrap;overflow-wrap:anywhere}main pre{white-space:pre-wrap;overflow-wrap:anywhere}main iframe{display:block;width:100%;height:80vh;min-height:500px;max-height:1000px;border:1px solid #ccc;box-sizing:border-box}'
HEADER='<a class="skip-link" href="#main">Skip to content</a>\n<header>\n<p class="site-title"><a href="/">Alec Kriebel</a></p>\n<nav aria-label="Main navigation"><a href="/research/">Research</a> | <a href="/blog/">Blog</a> | <a href="https://orcid.org/0009-0001-9320-500X">ORCID</a></nav>\n</header>\n'
FOOTER='\n<footer>\n<hr>\n<p><a href="/research/">Research home</a></p>\n<p class="copyright">© 2013–2026 Kriebel LLC.</p>\n</footer>\n</body>\n</html>\n'
def need(ok,label):
 if not ok:raise ValueError(label)
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 b=p.read_bytes();return {'bytes':len(b),'SHA256':sha(b)}
def obj(p):return json.loads(p.read_bytes())
def paths(p):return sorted(str(x.relative_to(p)) for x in p.rglob('*') if x.is_file())
def directories(p):return sorted(str(x.relative_to(p)) for x in p.rglob('*') if x.is_dir())
def write(p,b):
 need(p.is_relative_to(A),'write outside stage');need(not p.exists(),'refuse overwrite '+str(p));p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
def dump(n,o):write(A/n,(json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode())
def bound(p,r):need(pin(p)=={'bytes':r['bytes'],'SHA256':r['SHA256']},'whole bytes '+str(p))
def same(a,b):
 if type(a) is not type(b):return False
 if isinstance(a,dict):return list(a)==list(b) and all(same(a[k],b[k]) for k in a)
 if isinstance(a,list):return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
 return a==b

def freeze_sources():
 need(not (A/'SOURCE_INPUTS.json').exists(),'source freeze already exists')
 originals=set();namespaces=[]
 for rid in IDS:
  for tail,count in [('sources',121 if rid==IDS[0] else 81),('reviews/editorial',69 if rid==IDS[0] else 59)]:
   d=P/'papers'/rid/tail;ns=paths(d);need(len(ns)==count,'whole original namespace count')
   namespaces.append({'path':str(d),'files':ns,'directories':directories(d)})
   originals.update(d/n for n in ns)
  q=P/'verification'/('root-editorial-'+rid+'-20261115.json');bound(q,dict(zip(['bytes','SHA256'],ROOTS[rid])));originals.add(q)
  adoption=obj(q)
  # Exact root adoption references, and every actual whole owner wrapper original.
  def refs(v):
   if isinstance(v,dict):
    if all(k in v for k in ['path','bytes','SHA256']):
     need(not Path(v['path']).is_relative_to(W),'website descriptor forbidden before GO');bound(Path(v['path']),v);originals.add(Path(v['path']))
    for b in v.values():refs(b)
   elif isinstance(v,list):
    for b in v:refs(b)
  refs(adoption)
  protocol=obj(P/'papers'/rid/'reviews/editorial/SOURCE_PROTOCOL_BINDINGS.json')
  def wrappers(v):
   if isinstance(v,dict):
    if 'whole_literal_object' in v and 'original' in v:
     q=v['original'];originals.add(Path(q['path'] if isinstance(q,dict) else q))
    for b in v.values():wrappers(b)
   elif isinstance(v,list):
    for b in v:wrappers(b)
  wrappers(protocol)
 rows=[]
 for p in sorted(originals,key=str):
  need(not p.is_relative_to(W),'website input forbidden before GO')
  b=p.read_bytes();digest=sha(b);dest=A/'blobs'/digest
  if not dest.exists():write(dest,b)
  rows.append({'path':str(p),'bytes':len(b),'SHA256':digest,'blob':'blobs/'+digest})
 dump('SOURCE_INPUTS.json',{'UTC':now(),'phase':'SOURCE_ONLY_NO_WEBSITE_READ','files':rows,'complete_original_namespaces':namespaces,'raw_ignored_before_creation':True,'original_native_order':[['five_centers.pdf','five_centers.tex','verification-package.zip'],['totally-mixed-face-posets-source-and-verification.zip','totally-mixed-face-posets.pdf']],'whole_types_order_absence_null_history_preserved':True,'website_read_or_rendered':False})
 guard_sources()

def source_bytes(path):
 rows={r['path']:r for r in obj(A/'SOURCE_INPUTS.json')['files']};r=rows[str(path)];bound(A/r['blob'],r);return (A/r['blob']).read_bytes()
def frozen_obj(path):return json.loads(source_bytes(path))
def guard_sources():
 if (A/'SOURCE_SEAL.json').exists():
  seal=obj(A/'SOURCE_SEAL.json');bound(A/'SOURCE_MANIFEST.json',seal['manifest'])
  for n,r in obj(A/'SOURCE_MANIFEST.json')['payloads'].items():bound(A/n,r)
 s=obj(A/'SOURCE_INPUTS.json')
 for d in s['complete_original_namespaces']:
  p=Path(d['path']);need(paths(p)==d['files'] and directories(p)==d['directories'],'strict original namespace '+str(p))
 for r in s['files']:
  bound(Path(r['path']),r);bound(A/r['blob'],r)
  need(Path(r['path']).read_bytes()==(A/r['blob']).read_bytes(),'whole copied original')
 return s

def records():
 result=[]
 for rid in IDS:
  e=P/'papers'/rid/'reviews/editorial';root=frozen_obj(P/'verification'/('root-editorial-'+rid+'-20261115.json'));p=frozen_obj(e/'publication.json');ready=frozen_obj(P/'papers'/rid/'sources/SOURCE_READY.json');scholarly=frozen_obj(e/'SCHOLARLY_METADATA.json');main=source_bytes(e/'PUBLIC_MAIN.html').decode()
  need(main.endswith('\n') and main[:-1].startswith('<main>') and main[:-1].endswith('</main>'),'exact original main grammar')
  rule=root['future_exact_reader_only_transform_authorized'];need(main.count(rule['from'])==1 and rule['to'].startswith('<iframe '),'exact root reader permission')
  need(p['abstract']==root['original_full_abstract']==scholarly['abstract'],'whole original abstract')
  need(p['version_field_present']==root['native_version_field_present'],'native version presence')
  need(p['publication_date']==scholarly['datePublished']==root['original_publication_date'] and p['slug']==root['future_proposed_slug'],'original dates and exact adopted slug')
  need(root['root_editorial_adopted'] and root['private_stage_preparation_authorized'] and not root['production_installation_authorized'],'actual limited root authority')
  need(same(ready['all_native_assets_in_original_order'],root['native_assets_in_original_order']),'whole typed native root objects')
  need([x['original_api_file_object']['key'] for x in ready['all_native_assets_in_original_order']]==root['actual_native_order'],'literal native order')
  need(p['code_license'] is None and p['follow_up'] is None and p['canonical_url'] is None and p['AA'] is None,'unchanged private nulls')
  result.append({'id':rid,'publication':p,'ready':ready,'scholarly':scholarly,'root':root,'main':main[:-1],'bib':source_bytes(e/'citation.bib')})
 return result

def go():
 # Reading this private file is the first step; no website operation precedes it.
 p=A/'ROOT_WEBSITE_GO.json';need(p.is_file(),'separate actual root website GO has not arrived')
 g=obj(p);need(g['schema']=='five-centers-mixed-face-actual-root-website-GO-v1','GO schema')
 need(g['writer_custody_transcription_of_actual_root_message'] is True and bool(g['actual_root_message']),'actual message custody, not invented authority')
 need(g['source_seal_SHA256']==sha((A/'SOURCE_SEAL.json').read_bytes()),'same immutable source preparation')
 need(g['website_root']==str(W) and g['stage_directory']==str(A),'exact GO target')
 need(g['baseline_counts']==[614,92,93] and g['proposed_counts']==[623,94,95],'new measured baseline planning boundary')
 commit=g['installed_commit'];need(re.fullmatch('[0-9a-f]{40}',commit) and commit!='27cd946786754d66b44cbb309dae76da238b133e','new preceding-pair installed commit')
 need(g['root_stage_code_adopted'] is False and g['production_installation_authorized'] is False,'GO is only freeze/render permission')
 for key in ['prior_installation_receipt','prior_stage_adoption','prior_commit_approval']:
  r=g[key];need(not Path(r['path']).is_relative_to(W),'authority receipt outside website');bound(Path(r['path']),r)
 need(obj(Path(g['prior_installation_receipt']['path']))['commit']==obj(Path(g['prior_commit_approval']['path']))['commit']==commit,'exact installed and root-approved prior commit')
 need(obj(Path(g['prior_commit_approval']['path']))['publication_authorized'] is True,'actual preceding-pair root commit approval')
 need(re.fullmatch(r'\d{4}-\d{2}-\d{2}',g['build_date']),'frozen build date')
 return g

def git_ref(gitdir,ref):
 p=gitdir/ref
 if p.is_file():return p.read_text().strip()
 for line in (gitdir/'packed-refs').read_text().splitlines():
  if line and not line.startswith(('#','^')):
   value,name=line.split(' ',1)
   if name==ref:return value
 raise ValueError('missing authorized Git reference '+ref)
def freeze_website():
 g=go();guard_sources();need(not (A/'WEBSITE_BASELINE.json').exists(),'fresh baseline already frozen')
 gd=W/'.git'
 if gd.is_file():gd=(W/gd.read_text().strip().split(': ',1)[1]).resolve()
 head=(gd/'HEAD').read_text().strip();head=git_ref(gd,head[5:]) if head.startswith('ref: ') else head
 need(head==git_ref(gd,'refs/remotes/origin/master')==g['installed_commit'],'fresh local HEAD and tracking ref match actual GO')
 ns=paths(W/'public');need(len(ns)==614,'actual fresh614 public files')
 allpaths=[W/'public'/n for n in ns]+[W/'firebase.json',W/'.firebaserc',A/'ROOT_WEBSITE_GO.json',Path(g['prior_installation_receipt']['path']),Path(g['prior_stage_adoption']['path']),Path(g['prior_commit_approval']['path'])]
 rows=[]
 for p in sorted(allpaths,key=str):
  b=p.read_bytes();digest=sha(b);q=A/'blobs'/digest
  if not q.exists():write(q,b)
  rows.append({'path':str(p),'bytes':len(b),'SHA256':digest,'blob':'blobs/'+digest})
 index=(W/'public/research/index.html').read_text();graph,raw=json_script(index);xml=(W/'public/research/sitemap.xml').read_text()
 need(graph['mainEntity']['numberOfItems']==len(graph['mainEntity']['itemListElement'])==len(re.findall(r'<li\b[^>]*>.*?</li>',index,re.S))==92,'actual fresh92index')
 need(len(re.findall(r'<url>.*?</url>',xml,re.S))==93,'actual fresh93sitemap')
 for r in records():need(not any(n.startswith('research/'+r['root']['future_proposed_slug']+'/') for n in ns),'new target absent')
 dump('WEBSITE_BASELINE.json',{'UTC':now(),'root_GO_SHA256':sha((A/'ROOT_WEBSITE_GO.json').read_bytes()),'files':rows,'public_namespace':ns,'public_directories':directories(W/'public'),'whole_old_index_schema':graph,'baseline_counts':[614,92,93],'proposed_counts':[623,94,95],'local_HEAD_and_origin_master_tracking':head,'remote_server_ref_queried':False})
 guard_baseline(True)

def guard_baseline(live=False):
 g=go();b=obj(A/'WEBSITE_BASELINE.json');need(b['root_GO_SHA256']==sha((A/'ROOT_WEBSITE_GO.json').read_bytes()),'same actual GO')
 extra={str(W/'firebase.json'),str(W/'.firebaserc'),str(A/'ROOT_WEBSITE_GO.json'),g['prior_installation_receipt']['path'],g['prior_stage_adoption']['path'],g['prior_commit_approval']['path']}
 expected={str(W/'public'/n) for n in b['public_namespace']}|extra
 need(len(b['public_namespace'])==len(set(b['public_namespace']))==614 and len(b['files'])==len(expected)==620 and {r['path'] for r in b['files']}==expected,'exact614public plus6external baseline rows')
 buffers={}
 for r in b['files']:
  bound(A/r['blob'],r);bb=(A/r['blob']).read_bytes()
  if live:need(Path(r['path']).read_bytes()==bb,'all live baseline unchanged before render')
  if Path(r['path']).is_relative_to(W/'public'):buffers[str(Path(r['path']).relative_to(W/'public'))]=bb
 if live:need(paths(W/'public')==b['public_namespace'] and directories(W/'public')==b['public_directories'],'live full namespace before render')
 return g,b,buffers

def json_script(t):
 x=re.findall(r'<script\b[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',t,re.S);need(len(x)==1,'one scholarly script');return json.loads(x[0]),x[0]
def replace_script(t,value):return re.sub(r'(<script\b[^>]*type="application/ld\+json"[^>]*>).*?(</script>)',lambda m:m[1]+value+m[2],t,count=1,flags=re.S)
def production_article(r,g):
 p=r['publication'];canonical=r['root']['future_proposed_canonical_url'];article=copy.deepcopy(r['scholarly'])
 article.update({'@id':canonical+'#article','url':canonical,'mainEntityOfPage':{'@id':canonical+'#page'},'inLanguage':'en','isAccessibleForFree':True})
 if not p['version_field_present']:article.pop('version',None)
 article['encoding']=[{'@type':'MediaObject','encodingFormat':n['whole_original_native_files_entry']['mimetype'],'contentUrl':canonical+n['original_api_file_object']['key'],'sameAs':n['original_api_file_object']['links']['self'],'license':CC} for n in r['ready']['all_native_assets_in_original_order']]
 page={'@type':'WebPage','@id':canonical+'#page','url':canonical,'name':p['title'],'dateCreated':g['build_date'],'dateModified':g['build_date'],'mainEntity':{'@id':canonical+'#article'}}
 graph={'@context':'https://schema.org','@graph':[page,article]}
 meta={'description':p['description'],'author':p['author'],'robots':'index,follow','citation_title':p['title'],'citation_author':p['author'],'citation_author_orcid':p['orcid'],'citation_publication_date':p['publication_date'].replace('-','/'),'citation_doi':p['doi'],'citation_pdf_url':canonical+p['pdf_filename'],'citation_language':'en','twitter:card':'summary'}
 if p['version_field_present']:meta['citation_version']=p['version']
 lines=['<!DOCTYPE html>','<html lang="en">','<head>','<meta charset="utf-8">','<meta name="viewport" content="width=device-width, initial-scale=1">','<title>'+html.escape(p['title'])+' | Alec Kriebel</title>']
 lines += ['<meta name="'+k+'" content="'+html.escape(v,quote=True)+'">' for k,v in meta.items()]
 lines += ['<link rel="canonical" href="'+canonical+'">','<link rel="icon" href="/favicon.ico">','<link rel="stylesheet" href="/research/research.css">']
 for k,v in {'og:type':'article','og:title':p['title'],'og:description':p['description'],'og:url':canonical,'og:site_name':'Alec Kriebel','article:published_time':p['publication_date']}.items():lines.append('<meta property="'+k+'" content="'+html.escape(v,quote=True)+'">')
 lines += ['<script type="application/ld+json">'+json.dumps(graph,ensure_ascii=False)+'</script>','<style>'+CSS+'</style>','</head>','<body>']
 rule=r['root']['future_exact_reader_only_transform_authorized'];main=r['main'].replace('<main>','<main id="main">',1).replace(rule['from'],rule['to'],1)
 return ('\n'.join(lines)+'\n'+HEADER+main+FOOTER).encode()
def render_buffers():
 # Gate even in-memory rendering; this function is never called source-only.
 g,b,old=guard_baseline(True);guard_sources();rs=records();out={};lis='';nodes='';graph,raw=json_script(old['research/index.html'].decode())
 for j,r in enumerate(rs):
  p=r['publication'];slug=r['root']['future_proposed_slug'];base='research/'+slug+'/';canonical=r['root']['future_proposed_canonical_url']
  out[base+'index.html']=production_article(r,g)
  for n in r['ready']['all_native_assets_in_original_order']:out[base+n['original_api_file_object']['key']]=source_bytes(Path(n['path']))
  out[base+'citation.bib']=r['bib']
  graph['mainEntity']['itemListElement'].append({'@type':'ListItem','position':93+j,'url':canonical,'name':p['title']})
  lis+='      <li><a href="/'+base+'">'+html.escape(p['title'])+'</a><br><span class="entry-meta">'+p['publication_date_label']+' · Unrefereed preprint</span><p>'+html.escape(p['description'])+'</p><p><a href="/'+base+p['pdf_filename']+'">PDF</a> · <a href="https://doi.org/'+p['doi']+'">Zenodo</a></p></li>\n'
  nodes+='  <url><loc>'+canonical+'</loc><lastmod>'+g['build_date']+'</lastmod></url>\n'
 graph['mainEntity']['numberOfItems']=94
 index=old['research/index.html'].decode();need(index.count('    </ul>')==1,'one exact current list insertion point')
 out['research/index.html']=replace_script(index.replace('    </ul>',lis+'    </ul>',1),json.dumps(graph,ensure_ascii=False)).encode()
 xml=old['research/sitemap.xml'].decode();need(xml.count('</urlset>')==1,'one sitemap insertion point');out['research/sitemap.xml']=xml.replace('</urlset>',nodes+'</urlset>',1).encode()
 need(len(out)==11 and len(set(out)-set(old))==9 and len(set(old)|set(out))==623,'exact11overlay nine new leaves623union')
 return out

def main():
 need(len(sys.argv)>=2,'explicit phase required')
 if sys.argv[1]=='freeze-sources':freeze_sources();print(json.dumps({'phase':'SOURCE_ONLY_FROZEN','website_read_or_rendered':False,'source_files':len(obj(A/'SOURCE_INPUTS.json')['files'])}))
 elif sys.argv[1]=='freeze-website':freeze_website();print(json.dumps({'phase':'ACTUAL_FRESH_AUTHORIZED_WEBSITE_FROZEN','baseline':[614,92,93],'proposed':[623,94,95]}))
 elif sys.argv[1]=='render':
  need(len(sys.argv)==3 and sys.argv[2] in ['candidate-a','candidate-b'],'explicit new candidate name');name=sys.argv[2];need(not (A/name).exists(),'candidate already exists');buffers=render_buffers()
  for n,b in buffers.items():write(A/name/'public'/n,b)
  print(json.dumps({'candidate':name,'actual_all_eleven_buffers_written':True,'optimization_level':sys.flags.optimize,'overlay_files':11,'native_files':5,'BibTeX_files':2,'baseline':[614,92,93],'proposed':[623,94,95],'production_installation_authorized':False}))
 else:raise ValueError('unknown phase')
if __name__=='__main__':main()
