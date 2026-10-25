"""Read-only six-work legacy correspondence preflight. Writes only beside itself."""
from pathlib import Path
from datetime import datetime, timezone
from html.parser import HTMLParser
from html import unescape
import hashlib, json, re, subprocess, unicodedata, urllib.request

OUT = Path(__file__).resolve().parent
PROGRAM = OUT.parents[1]
REPO = PROGRAM.parent
DOCS = REPO / 'docs'
IDS = ['23393596', '23358014', '23356964', '23306332', '23203100', '22089807']
API = 'https://api.github.com/repos/AlecKriebel/Math'
BASE = 'https://aleckriebel.github.io/Math/'
MARKERS = {
 '23393596': {'braid': r'\bbraids?\b', 'mechanism': r'quasimorph|Gambaudo|Toffoli|Burau|derived.{0,35}braid|braid.{0,35}derived'},
 '23358014': {'critical_wave': r'critical[\s-]+wave|quintic|defocusing', 'sparse_control': r'sparse[\s-]+control|strong[\s-]+quadratic|critical[\s-]+cone|Kunisch|Meinlschmidt'},
 '23356964': {'cantor_hyperfinite': r'Cantor|hyperfin|Borel[\s-]+asympt', 'height_group': r'profinite|wreath|Tucker[\s–-]*Drob|\bIyer\b|\bShinko\b'},
 '23306332': {'stability': r'nearest.{0,30}stable|stable.{0,30}quadratic|spectral[\s-]+abscissa|Hurwitz', 'prox_regular': r'prox[\s-]*regular|proxregular|nonunique.{0,30}quadratic'},
 '23203100': {'bosonic': r'bosonic|pure[\s-]+loss|EPnI|photon', 'secrecy': r'consumed[\s-]+key|generated[\s-]+secret|secret[\s-]+key|dynamic[\s-]+capacit'},
 '22089807': {'amplification': r'amplif|Moran|fixation', 'specific_hybrid': r'pair[\s–-]+pendant|R.?hyb|1[.]502856|beyond.{0,45}(?:three[\s-]+halves|3\s*/\s*2)|simultaneous.{0,30}amplif'},
}

def utc(): return datetime.now(timezone.utc).isoformat()
def sha(b): return hashlib.sha256(b).hexdigest()
def blob(b): return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def info(p):
 b=p.read_bytes()
 return {'path':str(p), 'bytes':len(b), 'sha256':sha(b), 'git_blob_sha1':blob(b)}
def dump(name, obj):
 p=OUT/name;p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def git(*args): return subprocess.check_output(['git',*args],cwd=REPO,text=True).strip()
def acquire(name, url):
 request=urllib.request.Request(url,headers={'User-Agent':'AlecKriebel-read-only-correspondence-preflight','Accept':'application/vnd.github+json'})
 with urllib.request.urlopen(request,timeout=30) as r:
  body=r.read(); receipt={'requested_url':url,'resolved_url':r.url,'status':r.status,'utc':utc(),'bytes':len(body),'sha256':sha(body),'etag':r.headers.get('ETag'),'last_modified':r.headers.get('Last-Modified')}
 p=OUT/'remote'/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(body)
 receipt['saved_path']=str(p);return json.loads(body),receipt
def norm(s): return re.sub(r'[^a-z0-9]+','',unicodedata.normalize('NFKC',unescape(s)).lower())
class HTML(HTMLParser):
 def __init__(self,s):
  super().__init__(convert_charrefs=True);self.text=[];self.title=[];self.h1=[];self.links=[];self.meta=[];self.canonical=[];self.t=False;self.h=False;self.ignore=0;self.feed(s)
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if t in ['script','style']:self.ignore+=1
  if t=='title':self.t=True
  if t=='h1':self.h=True
  if t in ['a','iframe','object','embed']:self.links.append({'tag':t,'url':a.get('href') or a.get('src') or a.get('data')})
  if t=='meta':self.meta.append(a)
  if t=='link' and 'canonical' in a.get('rel','').split():self.canonical.append(a.get('href'))
 def handle_endtag(self,t):
  if t in ['script','style']:self.ignore=max(0,self.ignore-1)
  if t=='title':self.t=False
  if t=='h1':self.h=False
 def handle_data(self,s):
  if self.t:self.title.append(s)
  if self.h:self.h1.append(s)
  if not self.ignore:self.text.append(s)
def screen(text, targets):
 n=norm(text);text=unicodedata.normalize('NFKC',text);text=re.sub(r'(?<=\w)-\s*\n\s*(?=\w)','',text);hits={}
 for rid,t in targets.items():
  exact=[label for label,value in t['identity_queries'].items() if value and norm(value) in n]
  markers={}
  for label,pattern in MARKERS[rid].items():
   matches=list(re.finditer(pattern,text,re.I|re.S))
   if matches:markers[label]={'count':len(matches),'contexts':[' '.join(text[max(0,m.start()-120):m.end()+180].split()) for m in matches[:20]]}
  if exact or markers:hits[rid]={'exact_identity_hits':exact,'mechanism_hits':markers}
 return hits

def main():
 assert OUT.name=='preflight-prepared-six-sol-20261025'
 started=utc();tracked=[];targets={}
 initial={'utc':started,'branch':git('branch','--show-current'),'head':git('rev-parse','HEAD'),'local_origin_main':git('rev-parse','origin/main'),'remote_url':git('remote','get-url','origin')}
 assert initial['branch']=='main'
 for f in ['AGENTS.md', '.git/HEAD', '.git/index', '.git/config']:
  p=REPO/f
  if p.is_file():tracked.append(p)
 tracked += [PROGRAM/'MODEL_POLICY.md',Path('/Users/alec/.codex/attachments/97d02095-52a0-400f-a038-cbc727c7c885/goal-objective.md')]
 tracked += [p for p in DOCS.rglob('*') if p.is_file()]
 for rid in IDS:
  paper=PROGRAM/'papers'/rid
  c=json.loads((paper/'publication.json').read_text());g=json.loads((paper/'promotion.json').read_text());sb=c['source_binding'];root=PROGRAM/c['review_metadata']['root_clearance_file'];clearance=json.loads(root.read_text())
  possible=[paper/'sources'/c['pdf_filename']]
  possible += [paper/a['source_relative_path'] for a in sb.get('files',[]) if (a.get('filename') or a.get('name'))==c['pdf_filename'] and a.get('source_relative_path')]
  possible += [paper/'sources'/'assets'/c['pdf_filename']]
  pdf=next(p for p in possible if p.is_file());pinfo=info(pdf)
  assert pinfo['sha256']==sb['pdf_sha256']==clearance['pdf_sha256']==g['pdf_sha256']
  assert info(root)['sha256']==c['review_metadata']['root_clearance_sha256']==g['root_clearance_sha256']
  assert info(paper/'publication.json')['sha256']==g['publication_sha256']
  paths=[paper/'publication.json',paper/'promotion.json',root,pdf]
  for suffix in ['receipt.json','record.json','metadata.json','record-raw.json','record/zenodo_record.json','record/RECORD_IDENTITY.json','record/transport_receipts.json']:
   p=paper/'sources'/suffix
   if p.is_file():paths.append(p)
  for p in paths:
   tracked.append(p)
   if p.suffix=='.json':
    dest=OUT/'input-snapshots'/rid/p.relative_to(paper).as_posix() if p.is_relative_to(paper) else OUT/'input-snapshots'/rid/p.name
    dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(p.read_bytes())
  text=subprocess.check_output(['pdftotext','-layout',str(pdf),'-']).decode()
  dest=OUT/'target-pdf-text'/f'{rid}.txt';dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(text)
  concept=sb.get('concept_doi') or ('10.5281/zenodo.'+str(sb['concept_record_id']))
  queries={'title':c['title'],'doi':c['doi'],'concept_doi':concept}
  if rid=='22089807':queries['earlier_named_release_doi']='10.5281/zenodo.21852072'
  targets[rid]={'record_id':rid,'title':c['title'],'doi':c['doi'],'concept_doi':concept,'version':c.get('version'),'edition_label':c.get('edition_label'),'publication_date':c['publication_date'],'canonical_candidate':c['canonical_url'],'slug':c['slug'],'identity_queries':queries,'published_pdf':pinfo,'full_pdf_text':info(dest),'first_page':text.split('\f')[0],'root_clearance':info(root),'root_status':clearance['status'],'publication_binding':info(paper/'publication.json'),'promotion_binding':info(paper/'promotion.json'),'live_browser_status':'NOT_ASSESSED; root live and browser gate remains pending for this assignment'}
 tracked += [PROGRAM/'redirects'/f for f in ['publish_verified_article_redirects.py','publish_jc_incorporated_article.py','braid-wave-cantor-correspondence-preflight-20261025.json','jc-incorporated-article-root-final-disposition-20261025.json']]
 tracked=sorted(set(p for p in tracked if p.is_file()))
 baseline={str(p):info(p) for p in tracked};dump('protected-input-baseline.json',{'utc':utc(),'git':initial,'files':baseline})
 log=OUT/'RESEARCH_LOG.md'
 log.write_text(f'# Six prepared papers: legacy correspondence preflight\n\n- {started}: Initialized read-only six-work scope. Dedicated evidence directory only; no original docs, website, configs, sources, reviews, shared helpers, Git state, Sheet, redirects, deployment or release changes. Completion estimate: 15% of this preflight, not the 203-work programme.\n- {utc()}: Verified exact configured PDFs, promotion bindings and six root clearance hashes. Captured protected-input baseline. Completion estimate: 30%.\n')
 ref,r1=acquire('main-ref-start.json',API+'/git/refs/heads/main');commit=ref['object']['sha']
 commitdata,r2=acquire('main-commit-start.json',API+'/git/commits/'+commit)
 roottree,r3=acquire('root-tree-start.json',API+'/git/trees/'+commitdata['tree']['sha'])
 docssha=next(x['sha'] for x in roottree['tree'] if x['path']=='docs')
 tree,r4=acquire('docs-tree-start.json',API+'/git/trees/'+docssha+'?recursive=1');assert tree['truncated'] is False
 receipts=[r1,r2,r3,r4];entries={x['path']:x for x in tree['tree'] if x['type']=='blob'}
 relevant={p:e for p,e in entries.items() if p.endswith(('.html','.pdf')) or p in ['sitemap.xml','robots.txt','CNAME','_config.yml']}
 old=[];mismatches=[]
 for path,e in sorted(relevant.items()):
  p=DOCS/path;b=p.read_bytes() if p.is_file() else b'';local_match=p.is_file() and blob(b)==e['sha'] and len(b)==e['size']
  if not local_match:
   url='https://raw.githubusercontent.com/AlecKriebel/Math/'+commit+'/docs/'+path
   with urllib.request.urlopen(url,timeout=30) as r:b=r.read();receipts.append({'requested_url':url,'resolved_url':r.url,'status':r.status,'utc':utc(),'bytes':len(b),'sha256':sha(b)})
   mismatches.append(path)
  assert blob(b)==e['sha'] and len(b)==e['size']
  record={'path':'docs/'+path,'url':BASE+path,'git_commit':commit,'git_blob_sha1':e['sha'],'bytes':len(b),'sha256':sha(b),'local_bytes_match_remote':local_match}
  if path.endswith('.pdf'):
   if not local_match:
    pp=OUT/'remote-pdf'/path;pp.parent.mkdir(parents=True,exist_ok=True);pp.write_bytes(b)
   else:pp=p
   text=subprocess.check_output(['pdftotext','-layout',str(pp),'-']).decode();dest=OUT/'old-pdf-text'/(path.replace('/','__')+'.txt');dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(text)
   pi=subprocess.check_output(['pdfinfo',str(pp)],text=True)
   record.update({'kind':'pdf','full_text':info(dest),'first_page':text.split('\f')[0],'pdfinfo':pi,'doi_strings':sorted(set(re.findall(r'10\.[0-9]{4,9}/[a-zA-Z0-9._;()/:-]+',text))),'identity_screen':screen(text,targets)})
  elif path.endswith('.html'):
   html=b.decode();h=HTML(html);text=' '.join(h.text);dest=OUT/'old-html'/path;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(b)
   td=OUT/'old-html-text'/(path.replace('/','__')+'.txt');td.parent.mkdir(parents=True,exist_ok=True);td.write_text(text)
   record.update({'kind':'html','title':' '.join(h.title),'h1':' '.join(h.h1),'canonical':h.canonical,'meta':h.meta,'links':h.links,'full_html':info(dest),'full_text':info(td),'doi_strings':sorted(set(re.findall(r'10\.[0-9]{4,9}/[a-zA-Z0-9._;()/:-]+',html))),'identity_screen':screen(text+' '+html,targets)})
  else:
   text=b.decode();dest=OUT/'old-index'/path;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(b)
   record.update({'kind':'auxiliary','snapshot':info(dest),'identity_screen':screen(text,targets)})
  if path.endswith('/index.html'):record['reader_url']=BASE+path[:-len('index.html')]
  old.append(record)
 local_paths={str(p.relative_to(DOCS)) for p in DOCS.rglob('*') if p.is_file() and (p.suffix in ['.pdf','.html'] or p.name in ['sitemap.xml','robots.txt','CNAME','_config.yml'])}
 dump('screen.json',{'utc':utc(),'completion_percent':65,'remote_commit':commit,'docs_tree_sha':docssha,'tree_truncated':False,'scoped_paths_equal':set(relevant)==local_paths,'remote_only_paths':sorted(set(relevant)-local_paths),'local_only_paths':sorted(local_paths-set(relevant)),'local_remote_mismatch_paths':mismatches,'targets':targets,'old_documents':old})
 dump('acquisition-receipts.json',receipts)
 with log.open('a') as f:f.write(f'- {utc()}: Pinned current public main commit {commit}, docs tree {docssha}. Parsed all {sum(x["kind"]=="html" for x in old)} HTML documents and extracted all {sum(x["kind"]=="pdf" for x in old)} complete PDF texts; checked index/sitemap and exact object identity. Completion estimate: 65%; human interpretation of candidate identity remains.\n')
 final={str(p):info(p) for p in tracked}
 dump('protected-input-after-scan.json',{'utc':utc(),'files':final,'changed':[p for p in baseline if baseline[p]!=final[p]]})
 print(json.dumps({'remote_commit':commit,'docs_tree_sha':docssha,'old_html':sum(x['kind']=='html' for x in old),'old_pdfs':sum(x['kind']=='pdf' for x in old),'mismatch_paths':mismatches,'protected_changes':[p for p in baseline if baseline[p]!=final[p]],'hits':{rid:[{'path':o['path'],'exact':o['identity_screen'][rid]['exact_identity_hits'],'markers':list(o['identity_screen'][rid]['mechanism_hits'])} for o in old if rid in o['identity_screen']] for rid in IDS}},ensure_ascii=False))

if __name__=='__main__':main()
