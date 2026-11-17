"""Fresh private three-page staging builder; standard-library data/copy operations only.
Never imports or executes any producer/helper/source program; no subprocess/Git/network.
Every write is confined to this new owned lane. One invocation; failure leaves all evidence.
"""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import hashlib, html, json, os, re, shutil, stat, struct, xml.etree.ElementTree as ET, zlib
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
V=P/'verification'; W=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com'); M=P.parent
OWN=V/'mink-riesz-k3-stage-sol-20261117'; BASE=OWN/'baseline-public'; CAND=OWN/'candidate-public'
HEAD='217d41c0a9344aed9caacee7aed31d4f23b77e47'; TREE='cb7ae0adb22dc34b9c36b9d1e8efcf94f89f44e3'
INDEX_SHA='25494ed68b5d5612ae64ac01f2897c77b26024a994b66167426203d5620de4b7'
PAGES=[('even-minkowski','23203081'),('riesz-surface','23202994'),('mixed-k3-moduli','23204176')]
ADOPTIONS=[
 ('root-even-minkowski-editorial-adoption-20261117.json','c4662a85ed9471090145d8c6f3a30a04e8808ad016dd7e6b9de8463807dd4c1c'),
 ('root-riesz-surface-editorial-adoption-20261117.json','2f2afb3020fea2772057ce668cbeb48c1e6cf005bb255484f87a663a5d5b9705'),
 ('root-mixed-k3-moduli-editorial-adoption-20261117.json','bcb4431c53f7828a12c233a97890ebd000d433eff2d7e685b85cb89e42aac225')]
RULES=[
 ('verification/even-minkowski-editorial-sol-20261117','MANIFEST.json','FINAL.json','private-editorial-finite-manifest-v1','exact_created_terminal_exclusions'),
 ('verification/even-minkowski-fact-sol-20261117','MANIFEST.json','FINAL.json','finite-private-even-minkowski-fact-manifest-v1','exact_already_created_terminal_recursive_hash_exclusions'),
 ('verification/even-minkowski-legacy-sol-20261117','FINAL_MANIFEST.json','FINAL_SEAL.json',None,'exact_recursive_content_hash_exclusions'),
 ('verification/riesz-surface-editorial-sol-20261117','MANIFEST.json','FINAL.json','finite-private-editorial-manifest-v1','excluded_terminal_controls'),
 ('verification/riesz-surface-fact-sol-20261117','MANIFEST.json','FINAL.json','finite-private-fact-audit-manifest-v1','only_recursive_content_hash_exclusions'),
 ('verification/riesz-surface-legacy-sol-20261117','FINAL_MANIFEST.json','FINAL.json','bounded-legacy-manifest-v1','exact_recursive_hash_exclusions'),
 ('verification/mixed-k3-moduli-editorial-sol-20261117','MANIFEST.json','FINAL.json','finite-private-editorial-manifest-v1','exact_terminal_self_hash_exclusions'),
 ('verification/mixed-k3-moduli-fact-sol-20261117','MANIFEST.json','FINAL.json','finite-private-k3-fact-manifest-v1','only_recursive_content_hash_exclusions'),
 ('verification/mixed-k3-moduli-legacy-sol-20261117','MANIFEST.json','FINAL.json','finite-legacy-identity-manifest-v1','exact_terminal_self_hash_exclusions'),
 ('papers/23203081/sources','SOURCE_MANIFEST.json','SOURCE_FINAL.json','source-custody-finite-manifest-v1','excluded_control_files'),
 ('papers/23202994/sources','SOURCE_MANIFEST.json','SOURCE_FINAL.json','source-custody-manifest-v1','excluded_control_files'),
 ('papers/23204176/sources','SOURCE_MANIFEST.json','SOURCE_FINAL.json','source-custody-manifest-v1','excluded_control_files')]
ROOTS=[P/x[0] for x in RULES]
CONTROLS=[V/x[0] for x in ADOPTIONS]+[V/('root-clearance-'+r+'-20261117.json') for f,r in PAGES]

def utc(): return datetime.now(timezone.utc).isoformat()
def sha(b): return hashlib.sha256(b).hexdigest()
def pairs(rows):
 d={}
 for k,v in rows:
  assert k not in d,('duplicate JSON key',k)
  d[k]=v
 return d
def loads(s):
 return json.loads(s,object_pairs_hook=pairs,parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))
def readj(p): return loads(p.read_bytes().decode('utf-8'))
def pathcheck(r,root=False):
 assert type(r) is str and r and '\\' not in r and '\x00' not in r
 if r=='.' and root: return
 assert not r.startswith('/') and all(x not in ('','.','..') for x in r.split('/'))
 assert PurePosixPath(r).as_posix()==r
def mode(p): return format(stat.S_IMODE(p.lstat().st_mode),'04o')
def pin(p):
 assert stat.S_ISREG(p.lstat().st_mode),str(p)
 b=p.read_bytes(); return {'bytes':len(b),'SHA256':sha(b),'mode':mode(p)}
def validate_pin(x):
 assert type(x) is dict and set(x)=={'bytes','SHA256','mode'}
 assert type(x['bytes']) is int and x['bytes']>=0
 assert type(x['SHA256']) is str and re.fullmatch('[0-9a-f]{64}',x['SHA256'])
 assert type(x['mode']) is str and re.fullmatch('0[0-7]{3}',x['mode'])
def validate(s):
 assert type(s) is dict and set(s)=={'root','files','directories','regular_files','child_directories'}
 assert type(s['root']) is str and Path(s['root']).is_absolute()
 fs,ds=s['files'],s['directories']; assert type(fs) is dict and type(ds) is dict
 assert '.' in ds and not set(fs)&set(ds)
 parents=set()
 for r,x in fs.items():
  pathcheck(r); validate_pin(x); parents.add(PurePosixPath(r).parent.as_posix())
 for r,x in ds.items():
  pathcheck(r,True); assert type(x) is dict and set(x)=={'mode','empty'}
  assert type(x['empty']) is bool and type(x['mode']) is str and re.fullmatch('0[0-7]{3}',x['mode'])
  if r!='.': parents.add(PurePosixPath(r).parent.as_posix())
 assert parents<=set(ds) and all(x['empty']==(r not in parents) for r,x in ds.items())
 assert type(s['regular_files']) is int and s['regular_files']==len(fs)
 assert type(s['child_directories']) is int and s['child_directories']==len(ds)-1
def census(root):
 assert stat.S_ISDIR(root.lstat().st_mode)
 fs,ds={},{}
 for base,dirs,files in os.walk(root,followlinks=False):
  base=Path(base); dirs.sort(); files.sort()
  assert all(not (base/n).is_symlink() for n in dirs+files)
  ds[base.relative_to(root).as_posix()]={'mode':mode(base),'empty':not dirs and not files}
  for n in files: fs[(base/n).relative_to(root).as_posix()]=pin(base/n)
 x={'root':str(root),'files':fs,'directories':ds,'regular_files':len(fs),'child_directories':len(ds)-1}
 validate(x); return x
def native(repo):
 g=repo/'.git'; head=(g/'HEAD').read_text(); assert re.fullmatch(r'ref: refs/heads/[^\n]+\n',head)
 ref=head.removeprefix('ref: ').strip()
 local=[x for x in (g/'packed-refs').read_text().splitlines(keepends=True) if re.fullmatch(r'[0-9a-f]{40} refs/heads/[^\n]+\n?',x)]
 assert len({x.split()[1] for x in local})==len(local)
 vals=[x.split()[0] for x in local if x.split()[1]==ref]
 oid=(g/ref).read_text().strip() if (g/ref).exists() else vals[0]
 assert re.fullmatch('[0-9a-f]{40}',oid)
 return {n:pin(g/n) for n in ('HEAD','index','config')}|{'HEAD_text':head,'local_loose_heads':census(g/'refs/heads'),
  'packed_local_heads':{'file_mode':mode(g/'packed-refs'),'raw_lines':local},'resolved_native_HEAD':oid}
def norm_mode(x):
 assert type(x) is str and re.fullmatch(r'(?:0o)?[0-7]{3,4}',x)
 return format(int(x.removeprefix('0o'),8),'04o')
def write(path,data,replace=False):
 assert path.is_relative_to(OWN) and path!=OWN and not path.is_symlink()
 assert OWN.is_dir() and not OWN.is_symlink() and OWN.resolve()==OWN and path.parent.is_dir() and path.parent.resolve().is_relative_to(OWN)
 if replace: assert path in (CAND/'research/index.html',CAND/'research/sitemap.xml') and path.is_file()
 with path.open('wb' if replace else 'xb') as f: f.write(data)
def writej(name,data): write(OWN/name,(json.dumps(data,indent=2,ensure_ascii=False)+'\n').encode())
def native_full(repo):
 n=native(repo); q=repo/'.git/config.worktree'
 n['optional_worktree_config']=pin(q) if q.exists() else None
 return n
def capture():
 return {'schema':'complete-private-three-stage-protected-dict-snapshots-v1',
  'roots':{str(r):census(r) for r in ROOTS},'controls':{str(r):pin(r) for r in CONTROLS},
  'public':census(W/'public'),'native_M':native_full(M),'native_W':native_full(W)}
def compare_rows(root,s,rows,directories_required=True):
 fs,ds={},{}
 for r,x in rows:
  pathcheck(r,True); assert type(x) is dict
  kind=x['kind']; assert kind in ('file','directory')
  if kind=='directory':
   assert r not in ds and r not in fs and s['directories'][r]['mode']==norm_mode(x.get('mode',x.get('mode_octal')))
   if 'empty' in x: assert type(x['empty']) is bool and s['directories'][r]['empty']==x['empty']
   ds[r]=x
  else:
   assert r!='.' and r not in fs and r not in ds
   expected={'bytes':x['bytes'],'SHA256':x.get('SHA256',x.get('sha256')),'mode':norm_mode(x.get('mode',x.get('mode_octal')))}
   validate_pin(expected); assert s['files'][r]==expected
   fs[r]=x
 assert set(fs)==set(s['files'])
 if directories_required: assert set(ds)==set(s['directories'])
 return {'root':str(root),'files':len(fs),'child_directories':len(s['directories'])-1,'complete_adopted_file_pins_exact':True,'complete_adopted_directory_modes_exact':directories_required}
def authenticate_adoptions(snaps):
 docs=[]
 for name,h in ADOPTIONS:
  p=V/name; assert pin(p)['SHA256']==h; docs.append(readj(p))
 assert docs[0]['schema']=='root-even-minkowski-private-editorial-adoption-v1' and docs[0]['status']=='ACCEPTED_PRIVATE_COPY_ONLY'
 assert docs[1]['schema']=='root-riesz-private-editorial-adoption-v1' and docs[1]['status']=='ACCEPTED_PRIVATE_COPY_ONLY'
 assert 'schema' not in docs[2] and docs[2]['status']=='PRIVATE_EDITORIAL_ACCEPTED_FOR_SEPARATE_STAGING'
 checks=[]
 for x in docs[0]['finite_authentication']:
  root=P/x['root']; ss=snaps[str(root)]; rows=[(y['path'],dict(y,kind='file')) for y in x['file_pins']]
  assert (ss['regular_files'],ss['child_directories'])==(x['files'],x['child_directories'])
  checks.append(compare_rows(root,ss,rows,False))
  assert pin(root/x['manifest'])['SHA256']==x['manifest_SHA256'] and pin(root/x['terminal'])['SHA256']==x['terminal_SHA256']
 for x in docs[1]['finite_authentication']:
  root=P/x['root']; ss=snaps[str(root)]
  assert (ss['regular_files'],ss['child_directories'])==(x['files'],x['child_directories'])
  checks.append(compare_rows(root,ss,list(x['complete_fresh_tree'].items())))
  assert pin(root/x['manifest'])['SHA256']==x['manifest_sha256'] and pin(root/'FINAL.json')['SHA256']==x['final_sha256']
 root=P/'papers/23202994/sources'; checks.append(compare_rows(root,snaps[str(root)],list(docs[1]['source_full_exact'].items())))
 for x in docs[2]['authenticated']:
  root=P/x['root']; ss=snaps[str(root)]
  assert (ss['regular_files'],ss['child_directories'])==(x['files'],x['childdirs'])
  checks.append(compare_rows(root,ss,[(y['path'],y) for y in x['objects']]))
 assert len(checks)==12 and {x['root'] for x in checks}==set(snaps)
 return docs,checks
def manifest_check(rule,s):
 relative,manifest,terminal,schema,exclusion=rule; root=P/relative; d=readj(root/manifest)
 assert d.get('schema')==schema and ('schema' in d)==(schema is not None)
 assert type(d[exclusion]) is list and len(d[exclusion])==2 and set(d[exclusion])=={manifest,terminal}
 assert str(root)==d.get('root',d.get('scope'))
 keys=[k for k in ('entries','files','payload_files') if k in d]; assert len(keys)==1
 key=keys[0]; rows=d[key]; assert type(rows) is list
 files,dirs,terminal_rows=set(),set(),set()
 allowed={'path','kind','mode','mode_octal','bytes','SHA256','sha256','MD5','md5','hidden','hidden_component','empty','terminal_control','content_hash_excluded_terminal_control','recursive_terminal_hash_excluded','mtime_ns','git_blob_oid'}
 for x in rows:
  assert type(x) is dict and set(x)<=allowed; r=x['path']; pathcheck(r,True)
  assert r not in files|dirs
  kind=x.get('kind','file'); assert kind in ('file','directory')
  actual_mode=norm_mode(x.get('mode',x.get('mode_octal')))
  if kind=='directory':
   assert actual_mode==s['directories'][r]['mode']
   if 'empty' in x: assert type(x['empty']) is bool and x['empty']==s['directories'][r]['empty']
   dirs.add(r)
  else:
   assert r!='.' and actual_mode==s['files'][r]['mode']; files.add(r)
   control=any(x.get(k) is True for k in ('terminal_control','content_hash_excluded_terminal_control','recursive_terminal_hash_excluded'))
   if control:
    assert r in (manifest,terminal) and x.get('SHA256',x.get('sha256')) is None
    terminal_rows.add(r)
   else:
    assert r not in (manifest,terminal)
    assert type(x['bytes']) is int and x['bytes']==s['files'][r]['bytes']
    assert x.get('SHA256',x.get('sha256'))==s['files'][r]['SHA256']
    md5=x.get('MD5',x.get('md5'))
    if md5 is not None: assert hashlib.md5((root/r).read_bytes()).hexdigest()==md5
    if 'empty' in x: assert type(x['empty']) is bool and x['empty']==(x['bytes']==0)
   if 'bytes' in x: assert type(x['bytes']) is int and x['bytes']==s['files'][r]['bytes']
  for k in ('hidden','hidden_component'):
   if k in x: assert type(x[k]) is bool and x[k]==any(p.startswith('.') for p in Path(r).parts if p!='.')
  if 'mtime_ns' in x: assert type(x['mtime_ns']) is int and x['mtime_ns']>=0
 if key!='entries':
  assert type(d['directories']) is list
  for x in d['directories']:
   assert set(x)<={'path','mode','empty','hidden'}; r=x['path']; pathcheck(r)
   assert r not in dirs|files and norm_mode(x['mode'])==s['directories'][r]['mode']; dirs.add(r)
   if 'empty' in x: assert x['empty']==s['directories'][r]['empty']
  assert norm_mode(d['root_mode'])==s['directories']['.']['mode']; dirs.add('.')
 assert files|{manifest,terminal}==set(s['files']) and dirs==set(s['directories'])
 assert terminal_rows in (set(),{manifest,terminal})
 for k in ('final_regular_file_count','regular_files','actual_file_count_including_terminal_controls','actual_file_count','actual_files'):
  if k in d: assert type(d[k]) is int and d[k]==s['regular_files']
 for k in ('child_directory_count','child_directories','actual_child_directory_count','actual_childdirs'):
  if k in d: assert type(d[k]) is int and d[k]==s['child_directories']
 if 'payload_file_count' in d: assert type(d['payload_file_count']) is int and d['payload_file_count']==len(files)
 if 'file_count' in d: assert type(d['file_count']) is int and d['file_count']==len(files)
 if 'directory_count' in d: assert type(d['directory_count']) is int and d['directory_count']==len(dirs)
 if 'counts' in d:
  assert type(d['counts']) is dict
  if 'files' in d['counts']: assert type(d['counts']['files']) is int and d['counts']['files']==s['regular_files']
  for k in ('child_directories','childdirs'):
   if k in d['counts']: assert type(d['counts'][k]) is int and d['counts'][k]==s['child_directories']
 for k in ('terminal_controls','terminal_control_topology'):
  if k in d:
   assert type(d[k]) is list and len(d[k])==2 and {x['path'] for x in d[k]}=={manifest,terminal}
   for x in d[k]: assert norm_mode(x.get('mode',x.get('mode_octal')))==s['files'][x['path']]['mode']
 return {'root':str(root),'manifest':manifest,'terminal':terminal,'actual_schema':schema,'row_table':key,'exclusion_key':exclusion,'manifest_pin':pin(root/manifest),'terminal_pin':pin(root/terminal),'all_payload_and_terminal_modes_and_topology_exact':True,'mtime_ns_manifest_provenance_only':True}

class HTML(HTMLParser):
 def __init__(self,s):
  super().__init__(convert_charrefs=True); self.tags=[]; self.data=[]; self.ids=[]
  self.feed(s); self.close(); assert len(self.ids)==len(set(self.ids))
 def handle_starttag(self,t,attrs):
  assert len(attrs)==len({k for k,v in attrs}),('duplicate HTML attribute',t)
  x=dict(attrs); self.tags.append((t,x))
  if 'id' in x: self.ids.append(x['id'])
 def handle_data(self,s): self.data.append(s)
def visible(s): return ' '.join(''.join(HTML(s).data).split())
def one(p,s):
 rows=list(re.finditer(p,s,re.S)); assert len(rows)==1,(p,len(rows)); return rows[0]
def xml_full(x): return {'tag':x.tag,'attributes':x.attrib,'text':x.text,'tail':x.tail,'children':[xml_full(y) for y in x]}
def aggregate(index,xml):
 text=index.decode(); HTML(text)
 script=one(r'<script type="application/ld\+json">(.*?)</script>',text)
 schema=loads(script[1]); item=schema['mainEntity']
 assert schema['@type']=='CollectionPage' and item['@type']=='ItemList'
 pos=one(r'"itemListElement"\s*:\s*\[',script[1]).end(); raw=[]
 decoder=json.JSONDecoder(object_pairs_hook=pairs)
 while True:
  while script[1][pos].isspace(): pos+=1
  if script[1][pos]==']': break
  start=pos; obj,pos=decoder.raw_decode(script[1],pos); raw.append(script[1][start:pos])
  while script[1][pos].isspace(): pos+=1
  assert script[1][pos] in ',]'
  if script[1][pos]==',': pos+=1; assert script[1][pos:].lstrip()[0]!=']'
 typed=item['itemListElement']; assert [loads(x) for x in raw]==typed
 ul=one(r'<ul(?:\s[^>]*)?>(.*?)</ul>',text); units=re.findall(r'<li(?:\s[^>]*)?>.*?</li>',ul[1],re.S)
 assert re.sub(r'<li(?:\s[^>]*)?>.*?</li>','',ul[1],flags=re.S).strip()==''
 assert type(item['numberOfItems']) is int and item['numberOfItems']==len(raw)==len(units)
 for i,(x,r) in enumerate(zip(typed,units),1):
  assert set(x)=={'@type','position','url','name'} and x['@type']=='ListItem' and type(x['position']) is int and x['position']==i
  anchors=[a for t,a in HTML(r).tags if t=='a']; assert anchors and x['url']=='https://aleckriebel.com'+anchors[0]['href']
 assert len({x['url'] for x in typed})==len(typed)
 xmltext=xml.decode(); assert '<!DOCTYPE' not in xmltext and '<!ENTITY' not in xmltext
 tree=ET.fromstring(xml); ns='{http://www.sitemaps.org/schemas/sitemap/0.9}'; assert tree.tag==ns+'urlset'
 locations=[]
 for x in tree:
  assert x.tag==ns+'url' and len(x)==2 and x[0].tag==ns+'loc' and x[1].tag==ns+'lastmod'
  assert not list(x[0]) and not list(x[1]); locations.append(x[0].text)
 rawxml=re.findall(r'<url(?:\s[^>]*)?>.*?</url>',xmltext,re.S); assert len(rawxml)==len(tree)==len(set(locations))
 parsed=[{'tag':x.tag,'attributes':x.attrib,'children':[{'tag':y.tag,'attributes':y.attrib,'text':y.text,'tail':y.tail} for y in x]} for x in tree]
 values={'index_whole_UTF8':text,'sitemap_whole_UTF8':xmltext,'raw_visible_HTML_units':units,'visible_text_units':[visible(x) for x in units],
  'visible_text_rule':'concatenate HTMLParser data events, then whitespace collapse','raw_JSON_units':raw,'typed_ItemList_units':typed,
  'raw_XML_units':rawxml,'parsed_XML_units':parsed,'XML_locations':locations,
  'counts':{'visible_HTML':len(units),'raw_JSON':len(raw),'typed_JSON':len(typed),'XML':len(tree)}}
 return values,{'tree':xml_full(tree),'JSON_end_byte':len(text[:script.start(1)+pos].encode())}
def splice(old,new,rows):
 assert type(rows) is list and rows
 previous=0; cursor=0; parts=[]; reverse=[]; shift=0
 for x in rows:
  assert set(x)=={'start_byte','end_byte','old_UTF8','new_UTF8','reason'}
  a,b=x['start_byte'],x['end_byte']; assert type(a) is int and type(b) is int and previous<=a<=b<=len(old)
  assert all(type(x[k]) is str for k in ('old_UTF8','new_UTF8','reason'))
  removed,added=x['old_UTF8'].encode(),x['new_UTF8'].encode(); assert old[a:b]==removed
  parts.extend((old[cursor:a],added)); cursor=b; previous=b
  reverse.append((a+shift,a+shift+len(added),removed,added)); shift+=len(added)-len(removed)
 parts.append(old[cursor:]); assert b''.join(parts)==new
 restored=new
 for a,b,removed,added in reversed(reverse): assert restored[a:b]==added; restored=restored[:a]+removed+restored[b:]
 assert restored==old
 return {'span_count':len(rows),'whole_forward_exact':True,'whole_reverse_exact':True,'old_bytes':len(old),'new_bytes':len(new),'old_SHA256':sha(old),'new_SHA256':sha(new)}

def edits(old,rows):
 cursor=0; out=[]
 for x in rows:
  a,b=x['start_byte'],x['end_byte']; assert cursor<=a<=b<=len(old) and old[a:b]==x['old_UTF8'].encode()
  out.extend((old[cursor:a],x['new_UTF8'].encode())); cursor=b
 out.append(old[cursor:]); return b''.join(out)
def row(a,b,old,new,reason): return dict(start_byte=a,end_byte=b,old_UTF8=old.decode(),new_UTF8=new.decode(),reason=reason)
def activate(oldhead,canonical):
 sch=loads(one(rb'<script type="application/ld\+json">(.*?)</script>',oldhead)[1].decode())
 assert sch['@type']=='ScholarlyArticle' and '@graph' not in sch and all(k not in sch for k in ('@id','url','mainEntityOfPage'))
 rows=[]
 for name in ('robots','googlebot'):
  x=('<meta name="'+name+'" content="noindex, nofollow">\n').encode(); assert oldhead.count(x)==1; a=oldhead.index(x)
  rows.append(row(a,a+len(x),x,b'','remove exact private '+name))
 x=b'<meta name="citation_pdf_url" content="assets/paper.pdf">'; assert oldhead.count(x)==1; a=oldhead.index(x)
 rows.append(row(a,a+len(x),x,('<meta name="citation_pdf_url" content="'+canonical+'assets/paper.pdf">').encode(),'absolute citation PDF'))
 for enc in sch['encoding']:
  assert enc['contentUrl']=='assets/'+enc['name']
  x=('"contentUrl": "'+enc['contentUrl']+'"').encode(); assert oldhead.count(x)==1; a=oldhead.index(x)
  rows.append(row(a,a+len(x),x,('"contentUrl": "'+canonical+enc['contentUrl']+'"').encode(),'absolute native encoding '+enc['name']))
 x=b'<link rel="stylesheet" href="/research/research.css">\n'; assert oldhead.count(x)==1; a=oldhead.index(x)
 rows.append(row(a,a,b'',('<link rel="canonical" href="'+canonical+'">\n<meta property="og:url" content="'+canonical+'">\n').encode(),'canonical and OG URL'))
 a=one(rb'<script type="application/ld\+json">(.*?)</script>',oldhead).end(1)-1
 rows.append(row(a,a,b'',(', "@id": '+json.dumps(canonical)+', "url": '+json.dumps(canonical)+', "mainEntityOfPage": '+json.dumps(canonical)).encode(),'three canonical string identities'))
 rows.sort(key=lambda x:(x['start_byte'],x['end_byte'])); newhead=edits(oldhead,rows); proof=splice(oldhead,newhead,rows)
 expected=loads(json.dumps(sch)); expected.update({k:canonical for k in ('@id','url','mainEntityOfPage')})
 for x in expected['encoding']: x['contentUrl']=canonical+x['contentUrl']
 new=loads(one(rb'<script type="application/ld\+json">(.*?)</script>',newhead)[1].decode()); assert new==expected
 return newhead,rows,proof,sch,new
def local_checks(page,canonical):
 text=page.read_text(); parsed=HTML(text); ids=set(parsed.ids)
 for tag,attrs in parsed.tags:
  for k in ('aria-labelledby','aria-describedby'):
   if k in attrs: assert set(attrs[k].split())<=ids
  for k in ('href','src'):
   if k not in attrs: continue
   u=urlsplit(attrs[k]); value=unquote(u.path)
   if u.scheme or u.netloc:
    if u.scheme!='https' or u.netloc!='aleckriebel.com': continue
    if value=='/': continue
   if not value: target=page
   elif value.startswith('/'): target=CAND/value.lstrip('/')
   else: target=page.parent/value
   assert target.resolve().is_relative_to(CAND.resolve())
   if target.is_dir(): target=target/'index.html'
   assert target.is_file(),str(target)
   if u.fragment and target.suffix=='.html': assert unquote(u.fragment) in HTML(target.read_text()).ids
 return {'ids':len(ids),'local_paths_and_fragments_and_ARIA_exact':True}
def object_check(oid,kind):
 raw=zlib.decompress((W/'.git/objects'/oid[:2]/oid[2:]).read_bytes()); head,body=raw.split(b'\x00',1)
 assert head==kind.encode()+b' '+str(len(body)).encode() and hashlib.sha1(raw).hexdigest()==oid
 return body

started=utc(); before=capture(); writej('GUARDS_BEFORE.json',before)
try:
 assert before['native_M']['resolved_native_HEAD']=='a4ce3c37dad209339e490d18dcced6c48cf912d2'
 assert before['native_M']['index']['SHA256']=='91b10d938f7d737226662bbff3b07016dcc0e501376a045811ab4e930c6fbb11'
 assert before['native_W']['resolved_native_HEAD']==HEAD and before['native_W']['HEAD_text']=='ref: refs/heads/master\n'
 assert before['native_W']['index']=={'bytes':9060430,'SHA256':INDEX_SHA,'mode':'0644'}
 index=(W/'.git/index').read_bytes(); assert index[:4]==b'DIRC' and struct.unpack('!II',index[4:12])==(2,58730) and hashlib.sha1(index[:-20]).digest()==index[-20:]
 assert object_check(HEAD,'commit').split(b'\n',1)[0]==b'tree '+TREE.encode(); object_check(TREE,'tree')
 baseline=before['public']; assert (baseline['regular_files'],baseline['child_directories'])==(790,381) and baseline['directories']['.']['mode']=='0750'
 assert sum(Path(x).name=='.DS_Store' for x in baseline['files'])==17
 docs,adoption_checks=authenticate_adoptions(before['roots']); manifest_checks=[manifest_check(rule,before['roots'][str(P/rule[0])]) for rule in RULES]
 assert sum(before['roots'][str(P/r[0])]['regular_files'] for r in RULES[9:])==133
 assert sum(before['roots'][str(P/r[0])]['child_directories'] for r in RULES[9:])==34
 assert sum(before['roots'][str(P/r[0])]['regular_files'] for r in RULES[:9])==378
 assert sum(before['roots'][str(P/r[0])]['child_directories'] for r in RULES[:9])==25
 writej('INPUT_AUTHENTICATION.json',{'schema':'three-page-private-stage-input-authentication-v1','root_adoptions':[{'path':str(V/n),'pin':pin(V/n),'actual_schema':d.get('schema'),'actual_status':d['status']} for (n,h),d in zip(ADOPTIONS,docs)],'complete_adoption_custody_checks':adoption_checks,'actual_manifests':manifest_checks,'source_files_childdirs':[133,34],'private_files_childdirs':[378,25],'scientific_clearance_inherited':True,'new_scientific_copy_review':False})
 assert not BASE.exists() and not CAND.exists()
 shutil.copytree(W/'public',BASE,copy_function=shutil.copy2); shutil.copytree(BASE,CAND,copy_function=shutil.copy2)
 base=census(BASE); assert base['files']==baseline['files'] and base['directories']==baseline['directories']
 oi=(BASE/'research/index.html').read_bytes(); ox=(BASE/'research/sitemap.xml').read_bytes()
 write(OWN/'ORIGINAL_RESEARCH_INDEX.html',oi); write(OWN/'ORIGINAL_RESEARCH_SITEMAP.xml',ox)
 old,oe=aggregate(oi,ox); assert old['counts']=={'visible_HTML':130,'raw_JSON':130,'typed_JSON':130,'XML':131}
 models=[]; bindings=[]; heads=[]; units=[]; items=[]; xmlunits=[]; adds=[]; newdirs=[]
 for number,(family,record) in enumerate(PAGES,131):
  writer=V/(family+'-editorial-sol-20261117'); model=readj(writer/'page-model.json'); models.append(model)
  assert model['schema']=='private-editorial-page-model-v1' and model['record_id']==record and model['follow_up'] is None and model['publication_authority'] is False
  proposal=model['deployment_proposal']; slug=proposal['slug']; path=proposal['path']; canonical=proposal['proposed_canonical_url']
  assert re.fullmatch('[a-z0-9]+(?:-[a-z0-9]+)*',slug) and path=='/research/'+slug+'/' and canonical=='https://aleckriebel.com'+path
  assert canonical not in old['XML_locations'] and canonical not in [x['url'] for x in old['typed_ItemList_units']]
  dest=CAND/'research'/slug; assert not dest.exists()
  for directory in (dest,dest/'assets'): directory.mkdir(mode=0o755); os.chmod(directory,0o755); newdirs.append(directory.relative_to(CAND).as_posix())
  article=(writer/'article.html').read_bytes(); oldhead=(writer/'head.html').read_bytes(); hm=one(rb'(<head>.*?</head>\n)',article)
  assert hm[1]==oldhead and one(rb'(<main id="main">.*?</main>\n)',article)[1]==(writer/'main.html').read_bytes()
  newhead,spans,hproof,oldsch,newsch=activate(oldhead,canonical)
  assert oldsch['abstract']==model['abstract'] and oldsch['datePublished']==model['publication_date']=='2026-10-06'
  assert [x['name'] for x in oldsch['encoding']]==[x['name'] for x in model['native_asset_order']]
  if model['native_version'] is None: assert 'version' not in oldsch
  else: assert oldsch['version']==model['native_version']=='1.0.0'
  newarticle=article[:hm.start(1)]+newhead+article[hm.end(1):]
  assert one(rb'(<body>.*?</body>\n)',article)[1]==one(rb'(<body>.*?</body>\n)',newarticle)[1]
  write(dest/'index.html',newarticle); os.chmod(dest/'index.html',int(pin(writer/'article.html')['mode'],8))
  payloads=['index.html',model['citation_bib']]+[x['local_path'] for x in model['native_asset_order']]
  assert payloads==proposal['future_payloads']
  for r in payloads: pathcheck(r); adds.append((dest/r).relative_to(CAND).as_posix())
  bib=(writer/model['citation_bib']).read_bytes(); write(dest/model['citation_bib'],bib); os.chmod(dest/model['citation_bib'],int(pin(writer/model['citation_bib'])['mode'],8))
  assets=[]
  for x in model['native_asset_order']:
   r=x['local_path']; assert r=='assets/'+x['name']; native_path=P/'papers'/record/'sources/zenodo-files'/x['name']
   raw=(writer/r).read_bytes(); assert raw==native_path.read_bytes()
   assert len(raw)==x['bytes'] and sha(raw)==x['SHA256'] and hashlib.md5(raw).hexdigest()==x['MD5']
   assert pin(writer/r)['mode']==norm_mode(x['mode'])==pin(native_path)['mode']=='0644'
   write(dest/r,raw); os.chmod(dest/r,0o644); assets.append({'relative_path':r,'native_source_path':str(native_path),'pin':pin(dest/r),'native_name':x['name']})
  parsed=HTML(newarticle.decode()); metas=[x for t,x in parsed.tags if t=='meta']
  assert [x['content'] for x in metas if x.get('name')=='DC.description']==[model['abstract']]
  assert html.unescape(one(r'<p id="abstract-text">(.*?)</p>',newarticle.decode())[1])==model['abstract']==newsch['abstract']
  assert not any(x.get('name') in ('robots','googlebot') for x in metas)
  assert [x['href'] for t,x in parsed.tags if t=='link' and x.get('rel')=='canonical']==[canonical]
  assert [x['content'] for x in metas if x.get('property')=='og:url']==[canonical]
  assert [x['href'] for t,x in parsed.tags if t=='link' and x.get('rel')=='stylesheet']==['/research/research.css']
  assert [x['content'] for x in metas if x.get('name')=='citation_pdf_url']==[canonical+'assets/paper.pdf']
  metadata=one(r'<p class="entry-meta">(.*?)</p>',(writer/'main.html').read_text())[1].split('</a> · ',1)[1]
  unit='<li><a href="'+path+'">'+html.escape(model['title'])+'</a><br><span class="entry-meta">'+metadata+'</span><p>'+html.escape(model['meta_description'])+'</p><p><a href="'+path+'assets/paper.pdf">PDF</a> · <a href="'+model['doi_url']+'">Zenodo</a></p></li>'
  assert len(re.findall(r'<p>(.*?)</p>',unit,re.S))==2
  assert visible(unit)==' '.join((model['title']+visible(metadata)+model['meta_description']+'PDF · Zenodo').split())
  units.append(unit); items.append({'@type':'ListItem','position':number,'url':canonical,'name':model['title']})
  xmlunits.append('<url><loc>'+canonical+'</loc><lastmod>2026-11-17</lastmod></url>')
  body=one(rb'(<body>.*?</body>)',article)[1]
  bindings.append({'family':family,'record_id':record,'slug':slug,'canonical':canonical,'model':pin(writer/'page-model.json'),'accepted_article':pin(writer/'article.html'),'accepted_HEAD':pin(writer/'head.html'),'accepted_MAIN':pin(writer/'main.html'),'BODY':{'bytes':len(body),'SHA256':sha(body),'trailing_LF_included':False},'abstract':model['abstract'],'native_version':model['native_version'],'native_encoding_names':[x['name'] for x in oldsch['encoding']],'Bib':pin(dest/model['citation_bib']),'assets':assets,'candidate_article':pin(dest/'index.html'),'local_paths':local_checks(dest/'index.html',canonical)})
  heads.append({'family':family,'canonical':canonical,'accepted_head_SHA256':sha(oldhead),'candidate_head_SHA256':sha(newhead),'spans':spans,'forward_reverse':hproof,'whole_BODY_MAIN_article_outside_HEAD_exact':True})
 assert len(adds)==13 and len(set(adds))==13 and len(newdirs)==len(set(newdirs))==6 and len(units)==3
 count=one(rb'"numberOfItems"\s*:\s*(130)(?=\s*[,}])',oi)
 indexrows=[row(count.start(1),count.end(1),b'130',b'133','JSON count130to133'),row(oe['JSON_end_byte'],oe['JSON_end_byte'],b'',(', '+', '.join(json.dumps(x,ensure_ascii=False) for x in items)).encode(),'append whole raw ListItems131–133'),row(oi.index(b'</ul>'),oi.index(b'</ul>'),b'',('\n'.join(units)+'\n').encode(),'append three whole li units')]
 xmlrows=[row(ox.index(b'</urlset>'),ox.index(b'</urlset>'),b'',('\n'.join(xmlunits)+'\n').encode(),'append three canonical XML nodes')]
 ni,nx=edits(oi,indexrows),edits(ox,xmlrows)
 aggproof={'index':splice(oi,ni,indexrows),'XML':splice(ox,nx,xmlrows)}
 write(CAND/'research/index.html',ni,True); write(CAND/'research/sitemap.xml',nx,True)
 new,ne=aggregate(ni,nx); assert new['counts']=={'visible_HTML':133,'raw_JSON':133,'typed_JSON':133,'XML':134}
 for k in ('raw_visible_HTML_units','visible_text_units','raw_JSON_units','typed_ItemList_units','raw_XML_units','parsed_XML_units','XML_locations'): assert new[k][:len(old[k])]==old[k],k
 assert new['raw_visible_HTML_units'][130:]==units and new['typed_ItemList_units'][130:]==items and new['raw_XML_units'][131:]==xmlunits
 assert ne['tree']['attributes']==oe['tree']['attributes'] and ne['tree']['text']==oe['tree']['text'] and ne['tree']['children'][:131]==oe['tree']['children']
 candidate=census(CAND); modifications=['research/index.html','research/sitemap.xml']; gitpaths=['public/'+x for x in adds+modifications]
 assert len(gitpaths)==len(set(gitpaths))==15 and sorted(set(candidate['files'])-set(base['files']))==sorted(adds)
 assert not set(base['files'])-set(candidate['files'])
 assert sorted(x for x in base['files'] if base['files'][x]!=candidate['files'][x])==sorted(modifications)
 assert sorted(set(candidate['directories'])-set(base['directories']))==sorted(newdirs)
 assert all(candidate['files'][r]==x for r,x in base['files'].items() if r not in modifications)
 assert sum(r not in modifications for r in base['files'])==788
 assert all(candidate['directories'][r]==x for r,x in base['directories'].items())
 assert all(candidate['directories'][r]=={'mode':'0755','empty':False} for r in newdirs)
 assert all(candidate['files'][r]['mode']=='0644' for r in adds)
 assert (candidate['regular_files'],candidate['child_directories'])==(803,387)
 assert candidate['files']['research/research.css']==base['files']['research/research.css'] and sum(Path(r).name=='.DS_Store' for r in candidate['files'])==17
 writej('INPUT_BINDINGS.json',{'schema':'accepted-three-private-stage-input-bindings-v1','pages':bindings,'all_whole_BODY_MAIN_abstracts_Bibs_seven_assets_exact':True,'follow_up':None,'scientific_clearance_inherited':True})
 writej('BASELINE_MANIFEST.json',base); writej('CANDIDATE_MANIFEST.json',candidate)
 writej('BASELINE_AGGREGATE_UNITS.json',old); writej('CANDIDATE_AGGREGATE_UNITS.json',new)
 writej('HEAD_ACTIVATION.json',{'schema':'three-page-exact-private-stage-head-activation-v1','pages':heads,'only_closed_canonical_OG_scholarly_assetURL_private_robots_changes':True,'all_original_dates_versions_BODY_MAIN_abstracts_rights_AI_collaboration_exact':True})
 writej('AGGREGATE_FIDELITY.json',{'schema':'three-page-whole-buffer-reversible-aggregate-fidelity-v1','baseline_index':pin(BASE/'research/index.html'),'candidate_index':pin(CAND/'research/index.html'),'baseline_XML':pin(BASE/'research/sitemap.xml'),'candidate_XML':pin(CAND/'research/sitemap.xml'),'index_spans':indexrows,'XML_spans':xmlrows,'whole_forward_reverse':aggproof,'whole_old130_rawHTML_concat_visible_rawJSON_typed_and131_raw_fullparsedXML_prefix_exact':True,'new_visible_units':units,'new_typed_units':items,'new_XML_units':xmlunits,'no_old_aggregate_reserialization':True,'XML_lastmod_scope':'2026-11-17 sitemap file-update metadata only; no article/publication/audit date substitution'})
 writej('TARGETS.json',{'schema':'explicit-three-private-stage-targets-v1','append_order':[r for f,r in PAGES],'additions_public_relative':adds,'modifications_public_relative':modifications,'new_directories_public_relative':newdirs,'Git_relative_targets':gitpaths,'expected':{'additions':13,'modifications':2,'Git_targets':15,'new_directories':6,'candidate_files':803,'candidate_child_directories':387,'index_units':133,'sitemap_nodes':134},'private_stage_only':True,'publication_authority':False})
 writej('PROJECTION.json',{'schema':'three-private-stage-exact-projection-v1','additions_public_relative':sorted(adds),'modifications_public_relative':sorted(modifications),'new_directories_public_relative':sorted(newdirs),'Git_relative_targets':gitpaths,'whole_baseline_files_childdirs':[790,381],'whole_candidate_files_childdirs':[803,387],'untouched_old_files':788,'old_directory_rows':381,'DS_Store':17,'public_prefix_exactly_once':True,'whole_candidate_not_the_target_projection':True})
finally:
 after=capture(); writej('GUARDS_AFTER.json',after); assert after==before,'Protected source/private/root/native/public state changed'
writej('BUILD_RESULT.json',{'schema':'three-private-stage-build-result-v1','status':'PRIVATE_STAGE_COMPLETE_AWAITING_ROOT_AND_INDEPENDENT_AUDIT','UTC_start':started,'UTC_end':utc(),'invocations':1,'counts':[803,387,133,134],'projection':'13A2M/15paths/6dirs','guards_beforeafter_byte_identical':True,'completion_percent_staging_only':100,'follow_up':None,'publication_or_futureaction_authority':False})
