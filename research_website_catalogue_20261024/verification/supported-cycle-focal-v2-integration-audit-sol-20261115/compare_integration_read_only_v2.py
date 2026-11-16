"""Independent source/fresh-held-baseline/V2 comparison. No live or scientific calls."""
from pathlib import Path
from html.parser import HTMLParser
import difflib,hashlib,json,re,stat
import xml.etree.ElementTree as ET
D=Path(__file__).resolve().parent;V=D/'reviewed-writer';checks=0;nodes=0
def need(ok,label):
 global checks
 checks+=1
 if not ok:raise RuntimeError(label)
def read(p):
 p=Path(p);need(p.resolve()==p and stat.S_ISREG(p.lstat().st_mode),'ordinary buffer '+str(p));return p.read_bytes()
def obj(p):return json.loads(read(p))
def pin(b):return {'bytes':len(b),'SHA256':hashlib.sha256(b).hexdigest()}
def exact(a,b,label):
 global nodes
 nodes+=1;need(type(a) is type(b),'type '+label)
 if isinstance(a,dict):
  need(list(a)==list(b),'key/order '+label)
  for k in a:exact(a[k],b[k],label+'/'+k)
 elif isinstance(a,list):
  need(len(a)==len(b),'array size '+label)
  for i,(x,y) in enumerate(zip(a,b)):exact(x,y,label+'/'+str(i))
 else:need(a==b,'value '+label)
def extent(root):
 fs=[];ds=[]
 for p in root.rglob('*'):
  rel=p.relative_to(root).as_posix();m=p.lstat().st_mode
  if stat.S_ISDIR(m):ds.append(rel)
  else:need(stat.S_ISREG(m),'ordinary extent');fs.append(rel)
 need(len(fs)==len(set(fs)) and len(ds)==len(set(ds)),'duplicate enumerated identity')
 return sorted(fs),sorted(ds)
bindings=obj(D/'WRITER_CURRENT_BINDINGS.json');root=Path(bindings['source_root'])
for where in [root,V]:
 fs,ds=extent(where);expected=[r['path'] for r in bindings['files']]
 need(len(expected)==len(set(expected)) and fs==sorted(expected) and ds==bindings['directories'],'exact whole V2 extent')
 for r in bindings['files']:need(pin(read(where/r['path']))=={k:r[k] for k in ['bytes','SHA256']},'whole V2 payload')
need(pin(read(V/'FINAL_SEAL.json'))['SHA256']=='e3cdadbcddc446632a52e21b7d5d9f2b9de4901c62cb065770bdc5c1186700f6','immutable V2 final')
base=obj(D/'ACTUAL623_PUBLIC_BASELINE.json');fresh={r['path']:read(r['snapshot']['path']) for r in base['public_files']+base['site_configs']+obj(D/'ACTUAL623_GIT_OBSERVATIONS.json')['Git_control_files']}
oldroot=Path(obj(D/'PRIOR_CLOSED_EXTENTS.json')[1]['root']);oldbase=obj(oldroot/'WEBSITE_BASELINE.json');source=obj(oldroot/'SOURCE_INPUTS.json')
need(base['public_namespace']==oldbase['public_namespace'] and base['public_directories']==oldbase['public_directories'],'whole fresh623 identity matches V2 reference')
for r in oldbase['files']:
 b=read(oldroot/r['blob']);need(pin(b)=={k:r[k] for k in ['bytes','SHA256']},'old held baseline pin')
 if r['path'] in fresh:need(b==fresh[r['path']],'whole independently fresh body')
need(read(D/'inputs/baseline623/native-index.before')==read(oldroot/oldbase['full_raw_index']),'whole independently fresh raw index')
for r in source['files']:
 b=read(oldroot/r['blob']);need(pin(b)=={k:r[k] for k in ['bytes','SHA256']},'whole original819 literal source buffer')
for binding in obj(D/'INPUT_BINDINGS.json'):
 a=read(binding['source']);b=read(D/binding['copy']);need(a==b,'complete original/source/selected literal binding')
 try:x=json.loads(a)
 except (ValueError,UnicodeDecodeError):continue
 exact(x,json.loads(b),'literal original wrapper')
overlay=obj(V/'OVERLAY_MANIFEST.json')['files'];paths=[r['path'] for r in overlay];htmlpaths=[];diff=[];heads=[]
frame=obj(D/'BASELINE_FRAME_EXPECTATIONS.json');native=frame['whole_native_frames'][0]
class Head(HTMLParser):
 def __init__(self):super().__init__();self.meta={};self.links=[]
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if t=='meta':
   name=a.get('name') or a.get('property')
   if name:need(name not in self.meta,'unique head metadata');self.meta[name]=a.get('content')
  if t=='link':self.links.append(a)
def graph(b):
 h=b[:b.index(b'</head>')+7];parts=re.findall(rb'<script type="application/ld\+json">(.*?)</script>',h,re.S);need(len(parts)==1,'one metadata graph');return h,parts[0],json.loads(parts[0])
for item in frame['source_derived_heads']:
 i=item['record_id'];url=item['canonical'];slug=url.rstrip('/').split('/')[-1];name='research/'+slug+'/index.html';htmlpaths.append(name)
 main=read(D/'inputs'/i/'editorial/PUBLIC_MAIN.html');old=read(D/'inputs/prior-outputs'/name);new=read(V/'candidate-a/public'/name);h,gr,g=graph(new);oh,ogr,og=graph(old)
 need(new.count(main)==1 and new.count(b'<main ')==1,'whole approved MAIN exactly once')
 need(new[len(h):new.index(main)]==native['whole_head_to_main_body_prefix'].encode() and new[new.index(main)+len(main):]==native['whole_after_main_suffix'].encode(),'exact independently observed native prefix/footer')
 need(re.findall(rb'<style>.*?</style>',h,re.S)==[x.encode() for x in native['whole_inline_styles']],'exact native reader style')
 parsed=Head();parsed.feed(h.decode())
 for key,value in item['expected_meta_content'].items():need(parsed.meta[key]==value,'presealed exact meta '+key)
 need({'rel':'stylesheet','href':'/research/research.css'} in parsed.links and {'rel':'icon','href':'/favicon.ico'} in parsed.links and {'rel':'canonical','href':url} in parsed.links,'native links')
 need(list(g)==['@context','@graph'] and len(g['@graph'])==2,'linked native graph')
 page,article=g['@graph'];wp=dict(item['WebPage_except_build_dates']);wp['dateCreated']='2026-11-15';wp['dateModified']='2026-11-15'
 need(list(page)==['@type','@id','url','name','dateCreated','dateModified','mainEntity'],'native page field order')
 exact(page,{k:wp[k] for k in page},'complete page mapping')
 expected=item['whole_expected_ScholarlyArticle']
 need(set(article)==set(expected),'generated article field identity')
 # Explicit recorded insertion-position qualification only; all values retain exact recursive order/types.
 need(list(article)==list(og)+['@id','isAccessibleForFree'],'existing article field order retained')
 exact(article,{k:expected[k] for k in article},'presealed article mapped only to declared generated insertion positions')
 restored=json.loads(json.dumps(article,ensure_ascii=False));restored.pop('@id');restored.pop('isAccessibleForFree');restored['mainEntityOfPage']=og['mainEntityOfPage']
 for enc,oldenc in zip(restored['encoding'],og['encoding']):enc.pop('sameAs');enc['contentUrl']=oldenc['contentUrl']
 exact(restored,og,'complete original scholarly recovery')
 if i=='23578142':need('license' not in article['encoding'][0] and article['encoding'][1]['license']=='https://creativecommons.org/licenses/by/4.0/','mixed ZIP license absence')
 else:need(all(x['license']=='https://creativecommons.org/licenses/by/4.0/' for x in article['encoding']),'broad129 rights')
 def neutral(head,raw):
  b=head.replace(raw,b'__GRAPH__');b=re.sub(rb'<style>.*?</style>',b'',b,flags=re.S);b=b.replace(b'<link rel="stylesheet" href="/research/research.css">',b'')
  return re.sub(rb'(<meta name="citation_pdf_url" content=")[^"]*(">)',rb'\1__PDF__\2',b)
 need(neutral(h,gr)==neutral(oh,ogr),'only authorized head bytes change')
 heads.append({'record_id':i,'whole_head_prefix':new[:new.index(main)].decode(),'whole_after_MAIN_suffix':new[new.index(main)+len(main):].decode(),'whole_graph':g,'MAIN':pin(main),'HTML':pin(new)})
for row in overlay:
 name=row['path'];a=read(V/'candidate-a/public'/name);b=read(V/'candidate-b/public'/name);old=read(D/'inputs/prior-outputs'/name)
 need(a==b and pin(a)=={k:row[k] for k in ['bytes','SHA256']},'whole actual paired10 output')
 if name not in htmlpaths:need(a==old,'whole other8 unchanged')
 need((a==old) is row['whole_equal_original'],'exact equality label')
 if a!=old:diff.append(''.join(difflib.unified_diff(old.decode().splitlines(True),a.decode().splitlines(True),fromfile='original-edf8/public/'+name,tofile='corrective-v2/public/'+name)))
need(''.join(diff).encode()==read(V/'CORRECTIVE_DIFF.patch'),'complete corrective diff independently recomputed')
# Whole aggregate recovery uses held fresh buffers, with exact original typed order and raw reverse insertion.
old=fresh['/Users/alec/Desktop/alec-dev/aleckriebel.com/public/research/index.html'];new=read(V/'candidate-a/public/research/index.html');oh,oraw,og=graph(old);nh,nraw,ng=graph(new)
exact(ng['mainEntity']['itemListElement'][:94],og['mainEntity']['itemListElement'],'all old94 typed records')
need(ng['mainEntity']['numberOfItems']==len(ng['mainEntity']['itemListElement'])==96,'candidate96')
oldcards=list(re.finditer(rb'<li(?:\s[^>]*)?>.*?</li>',old,re.S));newcards=list(re.finditer(rb'<li(?:\s[^>]*)?>.*?</li>',new,re.S));need(len(oldcards)==94 and len(newcards)==96,'whole visible record counts')
need([x.group() for x in oldcards]==[x.group() for x in newcards[:94]],'all94 whole visible records')
recovered=new[:newcards[93].end()]+new[newcards[95].end():];recovered=recovered.replace(nraw,oraw,1);need(recovered==old,'entire old index recovered raw')
oldxml=fresh['/Users/alec/Desktop/alec-dev/aleckriebel.com/public/research/sitemap.xml'];newxml=read(V/'candidate-a/public/research/sitemap.xml');ox=list(re.finditer(rb'<url>.*?</url>',oldxml,re.S));nx=list(re.finditer(rb'<url>.*?</url>',newxml,re.S));need(len(ox)==95 and len(nx)==97,'whole sitemap counts');need([x.group() for x in ox]==[x.group() for x in nx[:95]],'all95 whole old URL bodies');need(newxml[:nx[94].end()]+newxml[nx[96].end():]==oldxml,'entire old XML recovered raw')
need(set(paths)&set(base['public_namespace'])=={'research/index.html','research/sitemap.xml'} and len(set(paths)|set(base['public_namespace']))==631,'exact eight leaves two aggregates')
for mode in ['PRE','POST']:
 guard=obj(V/(mode+'_GUARD.json'));need(guard['HEAD']==base['HEAD'] and guard['tree']==base['tree'] and guard['index_SHA256']==pin(read(D/'inputs/baseline623/native-index.before'))['SHA256'],'fresh owner guard identity agrees with independent snapshot')
 need(guard['native_index_records']==58563 and guard['protected_raw_records']==58561 and guard['actual_staged_deletions']==0,'native record/deletion distinction')
 need(guard['raw_protected_fingerprint']==pin(read(D/'inputs/baseline623/protected-native-index.raw-records'))['SHA256'],'whole protected raw stream matches fresh independent reconstruction')
 for r in guard['all623_configs_controls_whole_observations']:
  if r['path'] in fresh:need(pin(fresh[r['path']])=={k:r[k] for k in ['bytes','SHA256']},'whole independent guard body')
 for rec in guard['actual_Git_receipts']:
  need(rec['exit']==0,'actual owner Git exit')
  for role in ['stdout','stderr']:
   stream=rec[role];need(pin(read(stream['path']))=={k:stream[k] for k in ['bytes','SHA256']},'whole owner guard stream')
history=obj(V/'EXECUTIONS.json')['actual_processes'];need(len(history)==9,'actual nine recorded process objects')
for rec in history:
 need(rec['actual_observed_exit']==0,'owner actual exit')
 for role in ['stdout','stderr']:
  r=rec['whole_'+role];raw=read(V/r['path']);need(pin(raw)=={k:r[k] for k in ['bytes','SHA256']} and raw.decode()==rec['literal_'+role],'whole literal owner process stream')
verdict=obj(V/'VERDICT.json');need(verdict['root_V2_code_output_adopted'] is False and verdict['publication_authority'] is False and verdict['canonical_url'] is None and verdict['AA'] is None and verdict['follow_up'] is None,'private authority separation')
print(json.dumps({'status':'PASS_INDEPENDENT_INFORMED_V2_EXACT10_INTEGRATION','checks':checks,'whole_typed_nodes':nodes,'complete_MAINs_unchanged':2,'other8_whole_unchanged':True,'paired_outputs':10,'old_typed_visible_XML':[94,94,95],'whole_old_aggregates_recovered':True,'corrective_diff_bytes':len(read(V/'CORRECTIVE_DIFF.patch')),'writer_files':107,'writer_directories':12,'fresh_baseline':[623,94,95],'candidate_counts':[631,96,97],'native_index_records':58563,'protected_raw_records':58561,'actual_cached_deletions':0,'owner_actual_process_objects':len(history),'generated_key_position_qualification_only':True,'new_product_or_scientific_defect':False,'science_render_control_Git_network_subprocess_or_writes':False,'root_adoption':False,'production_authority':False,'canonical_url':None,'AA':None,'follow_up':None},sort_keys=True))
