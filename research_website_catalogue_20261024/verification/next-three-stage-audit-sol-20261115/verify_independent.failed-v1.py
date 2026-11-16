#!/usr/bin/env python3
"""Independent read-only private stage audit; adverse inputs live only in RAM."""
from pathlib import Path, PurePosixPath
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote, urljoin
import hashlib, json, stat, re, unicodedata, datetime, xml.etree.ElementTree as ET
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024'); W=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
O=P/'verification/next-three-stage-audit-sol-20261115'; S=P/'verification/next-three-private-stage-sol-20261115'; C=S/'candidate'
I=json.loads((O/'INITIAL.json').read_bytes()); EXPECTED=set(I['expected_stage_paths']); CHECKS=0
BIB={23331331:'papers/23331331/reviews/editorial/candidate/citation.bib',23203732:'papers/23203732/reviews/editorial/normal/citation.bib',23204591:'papers/23204591/reviews/editorial/citation.bib'}
def sha(b): return hashlib.sha256(b).hexdigest()
def require(condition,message):
 global CHECKS
 CHECKS+=1
 if not condition: raise ValueError(message)
def pin(p):
 b=p.read_bytes(); return {'bytes':len(b),'SHA256':sha(b),'mode':oct(stat.S_IMODE(p.lstat().st_mode))}
class H(HTMLParser):
 def __init__(self,text):
  super().__init__(convert_charrefs=True);self.tags=[];self.meta={};self.dupes=[];self.feed(text)
 def handle_starttag(self,t,attrs):
  a=dict(attrs);self.tags.append((t,a))
  if t=='meta' and ('name'in a or 'property'in a):
   k=a.get('name',a.get('property'))
   if k in self.meta:self.dupes.append(k)
   self.meta[k]=a.get('content')
def ld(text):
 blocks=re.findall(r'<script\b[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',text,re.S)
 require(len(blocks)==1,'One JSONLD object required');return json.loads(blocks[0])
def adopted(rid):
 if rid==23204591:
  m=json.loads((P/'papers/23204591/reviews/editorial/METADATA.json').read_bytes());pm=json.loads((P/'papers/23204591/reviews/editorial/PAGE_MODEL.json').read_bytes());return m['scholarly'],pm['page_title'],pm['meta_description'],m['full_printed_abstract']
 name='papers/23331331/reviews/editorial/candidate/PUBLIC_HEAD.html' if rid==23331331 else 'papers/23203732/reviews/editorial/normal/HEAD.html'
 head=(P/name).read_text();h=H(head);a=ld(head);return a,re.search(r'<title>(.*?)</title>',head,re.S)[1],h.meta['description'],a['abstract']
def links_ok(path,text,files):
 h=H(text);ids=[a['id'] for t,a in h.tags if 'id'in a]
 require(len(ids)==len(set(ids)),'Duplicate HTML IDs')
 for t,a in h.tags:
  for attr in ['href','src']:
   if attr not in a:continue
   v=a[attr];u=urlsplit(v)
   require(u.scheme in ('','https'),'Non-HTTPS or executable link')
   if u.scheme or u.netloc:continue
   raw=unquote(u.path);require('..'not in PurePosixPath(raw).parts and '\\'not in raw,'Traversal link')
   resolved=urlsplit(urljoin('https://aleckriebel.com/'+path.removeprefix('public/'),v))
   target='public'+resolved.path
   if target.endswith('/'):target+='index.html'
   require(target in files or target in I['W_public'],'Missing local link '+v)
   if resolved.fragment and target.endswith('.html'):
    content=files.get(target,(W/target).read_bytes() if target in I['W_public'] else b'').decode()
    require(unquote(resolved.fragment) in [a['id'] for t,a in H(content).tags if 'id'in a],'Missing fragment '+v)
 return h

def check(files):
 require(set(files)==EXPECTED,'Exact16-path namespace')
 norms=[unicodedata.normalize('NFC',p).casefold() for p in files]
 require(len(norms)==len(set(norms)),'Case/Unicode path aliases')
 oldnames={unicodedata.normalize('NFC',x).casefold() for x in I['W_public']}
 for x in EXPECTED-{'public/research/index.html','public/research/sitemap.xml'}:
  require(unicodedata.normalize('NFC',x).casefold() not in oldnames,'Existing public namespace collision')
 rows=[];descriptions=[]
 for ridstr,r in I['records'].items():
  rid=int(ridstr);route='public/research/'+r['slug']+'/';path=route+'index.html';body=files[path];text=body.decode();main=(P/r['MAIN']['path']).read_bytes();a,title,description,abstract=adopted(rid);h=links_ok(path,text,files);meta=h.meta;graph=ld(text)['@graph'];arts=[x for x in graph if x.get('@type')=='ScholarlyArticle'];pages=[x for x in graph if x.get('@type')=='WebPage']
  require(not h.dupes,'Duplicate metadata')
  require(body.count(main)==1,'Approved whole MAIN bytes absent or duplicated')
  require(len([1 for t,a in h.tags if t=='h1'])==1,'Exactly one H1')
  require([a.get('id')for t,a in h.tags if t=='main']==['main'],'Actual main ID')
  require(any(t=='a'and a.get('class')=='skip-link'and a.get('href')=='#main'for t,a in h.tags),'Skip target')
  require(re.search(r'<title>(.*?)</title>',text,re.S)[1]==title,'Adopted title')
  require(meta['description']==description and len(description)>60,'Adopted unique description')
  descriptions.append(description)
  url='https://aleckriebel.com/'+route.removeprefix('public/');native=r['metadata'];doi=native['doi']
  require([a.get('href')for t,a in h.tags if t=='link'and a.get('rel')=='canonical']==[url],'Canonical fidelity')
  require(meta['og:url']==url and meta['robots']=='index,follow','Release metadata only')
  require(meta['citation_title']==native['title'],'Native citation title')
  require(meta['citation_author']=='Kriebel, Alec'and meta['citation_author_orcid']=='https://orcid.org/0009-0001-9320-500X','Author and ORCID')
  require(meta['citation_doi']==doi and meta['citation_publication_date']==native['publication_date'].replace('-','/'),'Native date/DOI')
  require(meta.get('citation_version')==native.get('version'),'No invented native version')
  require(meta['article:published_time']==native['publication_date'],'Original date retained')
  require(meta['DC.description']==abstract and meta['DC.rights']=='CC BY 4.0','Full scholarly abstract/DC rights')
  require(len(arts)==len(pages)==1,'Scholarly/WebPage graph')
  art,page=arts[0],pages[0]
  for k in ['name','headline','author','datePublished','identifier']:
   require(art[k]==a[k],'Adopted scholarly '+k)
  require(art['abstract']==abstract and art['description']==description,'Complete abstract and unique synopsis')
  require(art.get('version')==native.get('version'),'Structured native version')
  require(art['license']=='https://creativecommons.org/licenses/by/4.0/'and art['creativeWorkStatus']=='Unrefereed preprint','Rights/status')
  require(art['@id']==url+'#article'and art['url']==url and art['mainEntityOfPage']=={'@id':url+'#page'},'Article graph wiring')
  require(page['@id']==url+'#page'and page['mainEntity']=={'@id':url+'#article'},'WebPage graph wiring')
  require(page['dateCreated']==page['dateModified']=='2026-11-16','Assembly dates separate from paper dates')
  expected_enc=[]; pdf=None
  for asset in r['assets_in_native_order']:
   key=asset['native_key'];local=('assets/'if rid==23204591 else '')+key
   require(files[route+local]==(P/asset['path']).read_bytes(),'Unchanged native asset '+key)
   require(sha(files[route+local])==asset['SHA256'],'Native original source pin')
   expected_enc.append((key,url+local,'https://zenodo.org/api/records/'+ridstr+'/files/'+key+'/content'))
   if key.endswith('.pdf'):pdf=local
  require([(x['name'],x['contentUrl'],x['sameAs'])for x in art['encoding']]==expected_enc,'All native encoding entries in original order')
  require(meta['citation_pdf_url']==url+pdf,'Searchable local PDF citation URL')
  frames=[a for t,a in h.tags if t=='iframe'];require(len(frames)==1 and frames[0]['src']==pdf+'#view=FitH'and frames[0].get('title'),'One labelled unchanged local reader')
  require(files[route+'citation.bib']==(P/BIB[rid]).read_bytes(),'Adopted whole BibTeX')
  if rid==23203732:require(b'version ='not in files[route+'citation.bib'],'No invented Bib version')
  require([a['href']for t,a in h.tags if t=='link'and a.get('rel')=='stylesheet']==['/research/research.css'],'Existing stylesheet reused')
  require(len([1 for t,a in h.tags if t=='script'])==1 and not any(t in ('form','button')for t,a in h.tags),'No active scripts/actions')
  require('main iframe{display:block;width:100%;height:80vh;'in text and 'main pre,main code,main .math{white-space:pre-wrap;'in text,'Wrapper raw-reader and pre styling')
  # Whole MAIN equality separately establishes original abstract/nativeDescription/disclosures/contribution text fidelity.
  aside=re.search(r'<aside\b.*?</aside>',text,re.S)[0]
  require([a['href']for t,a in H(aside).tags if t=='a'and a.get('href')!='citation.bib']==[x[1].removeprefix(url)for x in expected_enc],'Local download list in native order')
  rows.append({'rid':rid,'route':route,'url':url,'headline':art['headline'],'description':description,'PDF':pdf,'MAIN_SHA256':sha(main)})
 require(len(set(descriptions))==3,'Three distinct meta descriptions')
 # Preserve every original visible entry byte-for-byte and every original JSONLD item object.
 ix=files['public/research/index.html'].decode();old=(W/'public/research/index.html').read_text();oldli=re.findall(r'<li>.*?</li>',old,re.S);newli=re.findall(r'<li>.*?</li>',ix,re.S)
 require(len(oldli)==99 and len(newli)==102 and newli[:99]==oldli,'Original99 visible entries preserved exactly')
 oldld=ld(old);newld=ld(ix);oi=oldld['mainEntity']['itemListElement'];ni=newld['mainEntity']['itemListElement']
 require(newld['mainEntity']['numberOfItems']==102 and len(ni)==102 and ni[:99]==oi,'Original99 JSONLD entries preserved exactly')
 oldrest=dict(oldld);newrest=dict(newld);oldrest.pop('mainEntity');newrest.pop('mainEntity');require(oldrest==newrest,'Collection metadata preserved')
 for j,row in enumerate(rows,99):
  require(ni[j]=={'@type':'ListItem','position':j+1,'url':row['url'],'name':row['headline']},'New ItemList mapping')
  require('href="/'+row['route'].removeprefix('public/')+'"'in newli[j],'New visible canonical route')
  require(row['PDF']in newli[j]and row['description'].replace('’','’')in HText(newli[j]),'New visible summary/PDF')
 # Remove only the verified appended entries and replace only JSONLD to reconstruct entire original index bytes.
 reconstructed=ix
 for entry in newli[99:]:reconstructed=reconstructed.replace('      '+entry+'\n','',1)
 om=re.search(r'(<script\b[^>]*type="application/ld\+json"[^>]*>)(.*?)(</script>)',old,re.S)
 nm=re.search(r'(<script\b[^>]*type="application/ld\+json"[^>]*>)(.*?)(</script>)',reconstructed,re.S)
 reconstructed=reconstructed[:nm.start(2)]+om[2]+reconstructed[nm.end(2):]
 require(reconstructed==old,'No unrelated index byte changes')
 sm=files['public/research/sitemap.xml'];oldsm=(W/'public/research/sitemap.xml').read_bytes();ot=ET.fromstring(oldsm);nt=ET.fromstring(sm);ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
 require(len(nt)==103 and [ET.tostring(x)for x in nt[:100]]==[ET.tostring(x)for x in ot],'Original100 sitemap entries preserved')
 require([x.find('s:loc',ns).text for x in nt[100:]]==[r['url']for r in rows],'Only exact three new sitemap URLs')
 require(sm.startswith(oldsm[:oldsm.rfind(b'</urlset>')]) and sm.endswith(b'</urlset>\n'),'Sitemap original prefix/footer retained')
 return rows
class Text(HTMLParser):
 def __init__(self,s):super().__init__(convert_charrefs=True);self.parts=[];self.feed(s)
 def handle_data(self,s):self.parts.append(s)
def HText(s):return ''.join(Text(s).parts)
def baseline():
 files={str(p.relative_to(W)):pin(p)for p in (W/'public').rglob('*')if p.is_file()}
 require(files==I['W_public'],'Entire647file W public baseline')
 dirs=sorted(str(p.relative_to(W))for p in (W/'public').rglob('*')if p.is_dir());require(dirs==I['W_public_dirs'],'W public directory namespace')
 require(pin(W/'.git/index')=={k:I['W_native_index'][k]for k in ['bytes','SHA256','mode']},'Native W index unchanged')
 for r in I['records'].values():
  for p in [r['root'],r['MAIN'],r['native'],*r['assets_in_native_order']]:require(pin(P/p['path'])=={k:p[k]for k in ['bytes','SHA256','mode']},'Initial source pin drift')

def main():
 nodes=list(C.rglob('*'));require(not any(p.is_symlink()for p in nodes),'No stage symlink')
 require(all(stat.S_ISREG(p.lstat().st_mode)or stat.S_ISDIR(p.lstat().st_mode)for p in nodes),'Only regular files/directories')
 files={str(p.relative_to(C)):p.read_bytes()for p in nodes if p.is_file()}
 require(sorted(str(p.relative_to(C))for p in nodes if p.is_dir())==['public','public/research','public/research/bilinear-ergodic-hilbert-variation','public/research/bilinear-ergodic-hilbert-variation/assets','public/research/cost-betti-rank-100-amalgam','public/research/outer-pedal-area-centroid'],'Exact six stage directories')
 require(all(stat.S_IMODE(p.stat().st_mode)==0o644 and p.stat().st_nlink==1 for p in nodes if p.is_file()),'Stage modes/no hardlinks')
 baseline();rows=check(files);manifest=json.loads((S/'VERIFY.stdout.json').read_bytes())
 require(manifest['candidate_pins']==[{'path':k,'bytes':len(v),'SHA256':sha(v)}for k,v in sorted(files.items())],'Fixed handoff manifest')
 positives=CHECKS;cases=[]
 # Independent verifier sensitivity, with no filesystem fixtures or candidate writes.
 cases_in=[('foreign extra namespace',lambda f:f.update({'public/research/foreign/index.html':b'x'})),('native PDF byte drift',lambda f:f.update({rows[0]['route']+rows[0]['PDF']:b'broken PDF'})),('canonical hijack',lambda f:f.update({rows[0]['route']+'index.html':f[rows[0]['route']+'index.html'].replace(b'rel="canonical" href="https://aleckriebel.com',b'rel="canonical" href="https://foreign.example',1)})),('main ID drift',lambda f:f.update({rows[0]['route']+'index.html':f[rows[0]['route']+'index.html'].replace(b'<main id="main">',b'<main id="wrong">',1)})),('local link traversal',lambda f:f.update({rows[0]['route']+'index.html':f[rows[0]['route']+'index.html'].replace(b'href="citation.bib"',b'href="../foreign/citation.bib"',1)})),('structured abstract omission',lambda f:f.update({rows[1]['route']+'index.html':f[rows[1]['route']+'index.html'].replace(b'"abstract":',b'"abstract_removed":',1)})),('old index entry edit',lambda f:f.update({'public/research/index.html':f['public/research/index.html'].replace(b'Free spanning-forest degree can decrease under squaring',b'Changed old entry',2)})),('old sitemap removal',lambda f:f.update({'public/research/sitemap.xml':re.sub(rb'  <url>.*?</url>\n',b'',f['public/research/sitemap.xml'],count=1)})),('BibTeX drift',lambda f:f.update({rows[2]['route']+'citation.bib':b'@misc{changed}'}))]
 for name,mutate in cases_in:
  f=dict(files);mutate(f)
  try:check(f)
  except (ValueError,KeyError)as e:cases.append({'case':name,'rejected':True,'reason':str(e)})
  else:raise ValueError('Adversarial case survived: '+name)
 baseline();out={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_INDEPENDENT_PRIVATE_STAGE_MECHANICAL','positive_checks':positives,'in_memory_negative_cases':cases,'negative_cases_rejected':len(cases),'stage_files':len(files),'stage_dirs':6,'old_index_entries_exact':99,'new_index_entries':102,'old_sitemap_entries_exact':100,'new_sitemap_entries':103,'whole_original_index_reconstructed_exact':True,'records':rows,'candidate_pins':[{'path':k,'bytes':len(v),'SHA256':sha(v)}for k,v in sorted(files.items())],'baseline_public647_and_native_index_unchanged':True,'AA':None,'follow_up':None,'scientific_review_replayed':False,'limits':'Mechanical source/copy/metadata integration only. Owner DEFAULT read-order lapse retained separately. No browser/PDF display,external URL liveness,installation,deployment,Sheet or publication claim.'}
 print(json.dumps(out,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
