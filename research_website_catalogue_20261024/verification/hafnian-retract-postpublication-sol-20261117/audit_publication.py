"""One passive fixed postpublication audit. No project imports, subprocess or network.
Only two exclusive guard files in this new lane are written; all other paths read.
"""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
from html.parser import HTMLParser
import hashlib
import html
import json
import os
import re
import stat
import struct
import xml.etree.ElementTree as ET
import zlib

P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
V=P/'verification'
S=V/'hafnian-retract-stage-corrected-sol-20261117'
A=V/'hafnian-retract-stage-corrected-audit-sol-20261117'
N=V/'hafnian-retract-postpublication-sol-20261117'
C=V/'hafnian-retract-stage-audit-continuation-sol-20261117'
PREP=V/'hafnian-retract-production-prepare-sol-20261117'
R=V/'hafnian-retract-runtime-sol-20261117'
E=V/'hafnian-retract-production-root-executions-20261117'
T=R/'publish/23a8cf5c60cb5f6d9a7c8cdca34f79c819b5e9d55fb3a0953f0adfa5b469a985'
COMMIT='217d41c0a9344aed9caacee7aed31d4f23b77e47'
PARENT='7d5ac8ea5dc8d6cddee457da7a5b40042d36d344'
TREE='cb7ae0adb22dc34b9c36b9d1e8efcf94f89f44e3'
B=V/'hafnian-retract-stage-initial-bindings-sol-20261117'
F=V/'hafnian-retract-stage-sol-20261117'
D=V/'hafnian-retract-stage-failure-diagnosis-sol-20261117'
W=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
M=Path('/Users/alec/Documents/Math')
BASE,CAND=S/'baseline-public',S/'candidate-public'
PINS={
 S/'FINAL.json':'4282c414493774f4d562af7f6b0364a8f3efb90d026b7116936f17f01ef792e5',
 S/'OWNED_MANIFEST.json':'e2a0e565f7849c11af60c774b1cec4903ceae4a7b22f2ac61dcc3ea0002c6318',
 S/'build_private.py':'bbe547b27bd2c5fa32875d6717078b70c595ed3aba5cd6815a0b6b633d1c306b',
 S/'PRODUCER.diff':'232f3b3cdc5f2160088df38ad9eba8d652f8224663a2290a82c9c13c1f7f6f5b',
 S/'GUARDS_BEFORE.json':'9c883e92611eed08cea271bcb3a3e957ce20bcda3a495b3859434a22ffdad145',
 S/'GUARDS_AFTER.json':'9c883e92611eed08cea271bcb3a3e957ce20bcda3a495b3859434a22ffdad145',
 A/'FINAL.json':'9bca1054938f93d5f5ade1a590c435fe673c083126b27f38c7216fece9ddd864',
 A/'OWNED_MANIFEST.json':'31fa54b5e3dcdf33396276ccdeba666849eea0c365f16d41e1811bc10bb2526e',
 A/'GUARDS_BEFORE.json':'7c77a9f4b510c0fcede2203e2ce17ca01febecae49230eb3d43d3fa3bf1eac66',
 A/'GUARDS_AFTER.json':'7c77a9f4b510c0fcede2203e2ce17ca01febecae49230eb3d43d3fa3bf1eac66',
 B/'INPUT_BINDINGS.json':'c7ddeb3e335b317bba3864912807083fe4df423f0392be004de6df376c1b8a40',
 C/'FINAL.json':'32f304fa1ef31a62897d384ba0785b39a3b357e6931cb99a9668fa99c43465dc',
 C/'OWNED_MANIFEST.json':'9aefd0049fc758708dd61972944e87a3369832eae28586ea2c4573597769e845',
 PREP/'FINAL.json':'0cda3ae3168b12b510ac54f6afa284f6535ff19c6dad730bc50a03f574592a58',
 PREP/'OWNED_MANIFEST.json':'1cba4b1f682f93a439ce1918d9306c0b6ccbdf23cdee3c30eb2d67c1518a70ff',
 E/'publish-python314.stdout.json':'78250e5e345c993e0b71f0ed99952c57fb45f8ec4f13889068dbf51074fd1627',
 E/'install-python314.stdout.json':'3ed47ba44be03cdaf59228f91b3c366fd760d16e4d22c4839aa13a09a0e902f1',
 T/'native-index-proof.json':'9484d66c29402f4e172eb78674a0c92a1d32787e9fc0ddfa692384701aa60f67'}
ROOT_CONTROLS=[V/x for x in ('root-hafnian-retract-corrected-stage-adoption-20261117.json','root-hafnian-retract-newhelper-reading-20261117.json','root-hafnian-retract-python-runtime-disposition-20261117.json')]

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
def validate_protected(t):
 assert set(t)=={'roots','controls','public','native_M','native_W','old_failed_lane','frozen_diagnostic_lane','binding_lane','stage_control_pins'}
 for r,s in t['roots'].items(): validate(s); assert s['root']==r
 for k in ('controls','stage_control_pins'):
  for r,x in t[k].items(): assert Path(r).is_absolute(); validate_pin(x)
 for k in ('public','old_failed_lane','frozen_diagnostic_lane','binding_lane'): validate(t[k])
 for k in ('native_M','native_W'):
  n=t[k]; assert set(n)=={'HEAD','index','config','HEAD_text','local_loose_heads','packed_local_heads','resolved_native_HEAD'}
  for q in ('HEAD','index','config'): validate_pin(n[q])
  validate(n['local_loose_heads'])
  assert re.fullmatch(r'ref: refs/heads/[^\n]+\n',n['HEAD_text'])
  assert re.fullmatch('[0-9a-f]{40}',n['resolved_native_HEAD'])
  p=n['packed_local_heads']; assert set(p)=={'file_mode','raw_lines'}
  assert re.fullmatch('0[0-7]{3}',p['file_mode']) and type(p['raw_lines']) is list
  assert all(re.fullmatch(r'[0-9a-f]{40} refs/heads/[^\n]+\n?',x) for x in p['raw_lines'])
  assert len(p['raw_lines'])==len({x.split()[1] for x in p['raw_lines']})
def capture(t):
 validate_protected(t)
 protected={'roots':{r:census(Path(r)) for r in t['roots']},'controls':{r:pin(Path(r)) for r in t['controls']},
  'public':census(W/'public'),'native_M':native(M),'native_W':native(W),'old_failed_lane':census(F),
  'frozen_diagnostic_lane':census(D),'binding_lane':census(B),'stage_control_pins':{r:pin(Path(r)) for r in t['stage_control_pins']}}
 validate_protected(protected)
 return {'protected':protected,'whole_corrected_stage':census(S),'prior_failed_audit':census(A),
  'completed_stage_audit':census(C),'preparation':census(PREP),'runtime':census(R),
  'execution_receipts':census(E),'production_static_audit':census(V/'hafnian-retract-production-audit-sol-20261117'),
  'root_controls':{str(p):pin(p) for p in ROOT_CONTROLS}}
def save_guard(name,x):
 assert name in ('GUARDS_BEFORE.json','GUARDS_AFTER.json')
 with (N/name).open('x',encoding='utf-8') as f: f.write(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
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

def git_oid(kind,body):
 return hashlib.sha1(kind.encode()+b' '+str(len(body)).encode()+b'\x00'+body).hexdigest()
def object_bytes(oid,kind):
 raw=zlib.decompress((W/'.git/objects'/oid[:2]/oid[2:]).read_bytes())
 header,body=raw.split(b'\x00',1)
 assert header==kind.encode()+b' '+str(len(body)).encode() and hashlib.sha1(raw).hexdigest()==oid
 return body
def index_parse(raw):
 assert raw[:4]==b'DIRC' and hashlib.sha1(raw[:-20]).digest()==raw[-20:]
 version,count=struct.unpack('!II',raw[4:12]); assert version==2
 pos=12; records={}; semantics={}; names=[]
 for _ in range(count):
  start=pos; fields=struct.unpack('!10I',raw[pos:pos+40]); oid=raw[pos+40:pos+60].hex()
  flags=struct.unpack('!H',raw[pos+60:pos+62])[0]; assert not flags&0x4000 and not flags&0x3000
  zero=raw.index(b'\x00',pos+62); name=raw[pos+62:zero]
  assert name and not name.startswith(b'/') and all(x not in (b'',b'.',b'..') for x in name.split(b'/'))
  assert flags&0xFFF==min(len(name),0xFFF) and name not in records
  end=start+((zero+1-start+7)//8)*8; assert raw[zero:end]==b'\x00'*(end-zero)
  records[name]=raw[start:end]; names.append(name)
  assert fields[6] in (0o100644,0o100755,0o120000,0o160000)
  semantics[name]=(format(fields[6],'06o'),'commit' if fields[6]==0o160000 else 'blob',oid)
  pos=end
 assert names==sorted(names) and len(records)==count
 extensions=[]
 while pos<len(raw)-20:
  sig=raw[pos:pos+4]; length=struct.unpack('!I',raw[pos+4:pos+8])[0]; end=pos+8+length
  assert len(sig)==4 and all(65<=x<=90 or 97<=x<=122 for x in sig) and end<=len(raw)-20
  assert sig not in [x[0] for x in extensions]; extensions.append((sig,raw[pos:end])); pos=end
 assert pos==len(raw)-20
 return records,semantics,extensions
def semantic_map(rows):
 assert type(rows) is list; result={}
 for x in rows:
  assert type(x) is dict and set(x)=={'header_ascii','path_hex'} and type(x['path_hex']) is str
  name=bytes.fromhex(x['path_hex']); assert name.hex()==x['path_hex'] and name and b'\x00' not in name
  assert not name.startswith(b'/') and all(y not in (b'',b'.',b'..') for y in name.split(b'/')) and name not in result
  assert type(x['header_ascii']) is str and re.fullmatch(r'(100644|100755|120000|160000) (blob|commit) [0-9a-f]{40}',x['header_ascii'])
  m,k,o=x['header_ascii'].split(); assert (m=='160000')==(k=='commit'); result[name]=(m,k,o)
 return result
def semantic_trees(mapping):
 root={}; table={}; bodies={}
 for name,value in mapping.items():
  bits=name.split(b'/'); node=root
  for bit in bits[:-1]:
   if bit not in node: node[bit]={}
   assert type(node[bit]) is dict; node=node[bit]
  assert bits[-1] not in node; node[bits[-1]]=value
 def visit(node,path):
  chunks=[]; count=0; dirs=0
  for name in sorted(node,key=lambda n:n+(b'/' if type(node[n]) is dict else b'')):
   value=node[name]
   if type(value) is dict:
    child,count_child=visit(value,path+b'/'+name if path else name); count+=count_child; dirs+=1
    chunks.append(b'40000 '+name+b'\x00'+bytes.fromhex(child))
   else:
    m,k,oid=value; count+=1; chunks.append(m.encode()+b' '+name+b'\x00'+bytes.fromhex(oid))
  body=b''.join(chunks); oid=git_oid('tree',body); table[path]=(oid,count,dirs); bodies[path]=body
  return oid,count
 oid,count=visit(root,b''); assert count==len(mapping); return oid,table,bodies
def cache_check(chunk,table,wanted):
 assert chunk[:4]==b'TREE' and struct.unpack('!I',chunk[4:8])[0]==len(chunk)-8
 payload=chunk[8:]; pos=0; nodes=[]; valid=[]; invalid=[]
 def visit(parent=None):
  nonlocal pos
  zero=payload.index(b'\x00',pos); name=payload[pos:zero]; pos=zero+1
  if parent is None: assert name==b''; path=b''
  else:
   assert name and b'/' not in name and name not in (b'.',b'..')
   path=parent+b'/'+name if parent else name
  end=payload.index(b'\n',pos); header=payload[pos:end]; pos=end+1
  assert re.fullmatch(rb'(-1|0|[1-9][0-9]*) (0|[1-9][0-9]*)',header)
  entries,children=map(int,header.split()); assert path in table and path not in nodes; nodes.append(path)
  if entries>=0:
   oid=payload[pos:pos+20].hex(); assert len(payload[pos:pos+20])==20; pos+=20
   assert table[path]==(oid,entries,children)
   valid.append({'OID':oid,'entries':entries,'path_hex':path.hex(),'subtrees':children})
  else: invalid.append(path.decode())
  for _ in range(children): visit(path)
 visit(); assert pos==len(payload) and len(nodes)==983 and len(valid)==977
 assert invalid==['','public','public/research','public/research/binary-relation-liveness','public/research/rational-point-undecidability','public/research/focal-distance-period-criterion']
 assert set(wanted)=={'invalidated_paths_no_OID','native_root_tree','nodes','payload','valid_cached_nodes','valid_nodes','whole_extension'}
 assert wanted['nodes']==len(nodes) and wanted['valid_nodes']==len(valid) and wanted['valid_cached_nodes']==valid and wanted['invalidated_paths_no_OID']==invalid
 assert wanted['whole_extension']=={'bytes':len(chunk),'SHA256':sha(chunk)} and wanted['payload']=={'bytes':len(payload),'SHA256':sha(payload)}
 assert wanted['native_root_tree']==table[b''][0]
 return {'nodes':len(nodes),'valid':len(valid),'preexisting_invalid_paths':invalid,'whole_extension':wanted['whole_extension'],'payload':wanted['payload']}
started=utc(); expected=readj(A/'GUARDS_BEFORE.json'); template=expected['protected']
before=capture(template); save_guard('GUARDS_BEFORE.json',before)
try:
 for p,h in PINS.items(): assert pin(p)['SHA256']==h,str(p)
 for k in ('roots','controls','native_M','old_failed_lane','frozen_diagnostic_lane','binding_lane','stage_control_pins'): assert before['protected'][k]==template[k],k
 assert before['whole_corrected_stage']==expected['whole_corrected_stage']
 nw,ow=before['protected']['native_W'],template['native_W']
 assert nw['HEAD']==ow['HEAD'] and nw['config']==ow['config'] and nw['HEAD_text']==ow['HEAD_text']
 assert nw['packed_local_heads']==ow['packed_local_heads'] and nw['resolved_native_HEAD']==COMMIT
 assert nw['index']=={'bytes':9060430,'SHA256':'25494ed68b5d5612ae64ac01f2897c77b26024a994b66167426203d5620de4b7','mode':'0644'}
 assert nw['local_loose_heads']['directories']==ow['local_loose_heads']['directories']
 assert set(nw['local_loose_heads']['files'])==set(ow['local_loose_heads']['files'])
 assert all(v==nw['local_loose_heads']['files'][k] for k,v in ow['local_loose_heads']['files'].items() if k!='master')
 assert nw['local_loose_heads']['files']['master']=={'bytes':41,'SHA256':sha((COMMIT+'\n').encode()),'mode':ow['local_loose_heads']['files']['master']['mode']}
 binding=readj(B/'INPUT_BINDINGS.json'); target=readj(S/'TARGETS.json')
 base,candidate=census(BASE),census(CAND); published=before['protected']['public']
 for s in (base,candidate,published): validate(s)
 assert base['files']==template['public']['files'] and base['directories']==template['public']['directories']
 assert candidate['files']==published['files'] and candidate['directories']==published['directories']
 assert (base['regular_files'],base['child_directories'],published['regular_files'],published['child_directories'])==(781,377,790,381)
 adds=sorted(set(published['files'])-set(base['files'])); changes=sorted(k for k in base['files'] if published['files'][k]!=base['files'][k])
 assert adds==sorted(target['additions_public_relative']) and changes==sorted(target['modifications_public_relative']) and len(adds)==9 and len(changes)==2
 assert set(published['files'])==set(base['files'])|set(adds)
 assert sorted(set(published['directories'])-set(base['directories']))==sorted(target['new_directories_public_relative'])
 assert all(published['files'][k]==v for k,v in base['files'].items() if k not in changes)
 assert sum(k not in changes for k in base['files'])==779 and all(published['directories'][k]==v for k,v in base['directories'].items())
 assert published['directories']['.']['mode']=='0750' and sum(Path(k).name=='.DS_Store' for k in published['files'])==17
 scope=sorted(target['Git_relative_targets']); assert len(scope)==11 and scope==sorted('public/'+x for x in adds+changes)
 heads=readj(S/'HEAD_ACTIVATION.json'); pageproofs=[]
 for accepted in binding['pages']:
  family=accepted['family']; writer=V/(family+'-editorial-sol-20261117'); model=readj(writer/'page-model.json')
  old=(writer/'article.html').read_bytes(); oldhead=(writer/'head.html').read_bytes()
  page=W/'public/research'/accepted['slug']/'index.html'; new=page.read_bytes()
  om=one(rb'(<head>.*?</head>\n)',old); nm=one(rb'(<head>.*?</head>\n)',new); newhead=nm[1]
  assert om[1]==oldhead and old[:om.start(1)]==new[:nm.start(1)] and old[om.end(1):]==new[nm.end(1):]
  assert one(rb'(<body>.*?</body>\n)',old)[1]==one(rb'(<body>.*?</body>\n)',new)[1]
  assert one(rb'(<main id="main">.*?</main>\n)',new)[1]==(writer/'main.html').read_bytes()
  body=one(rb'(<body>.*?</body>)',new)[1]; assert (len(body),sha(body))==(accepted['BODY']['bytes'],accepted['BODY']['SHA256'])
  canonical=model['deployment_proposal']['proposed_canonical_url']
  osch=loads(one(rb'<script type="application/ld\+json">(.*?)</script>',oldhead)[1].decode())
  nsch=loads(one(rb'<script type="application/ld\+json">(.*?)</script>',newhead)[1].decode())
  expected_sch=loads(json.dumps(osch)); expected_sch.update({k:canonical for k in ('@id','url','mainEntityOfPage')})
  for x in expected_sch['encoding']: x['contentUrl']=canonical+x['contentUrl']
  assert osch==accepted['schema_object'] and nsch==expected_sch and nsch['@type']=='ScholarlyArticle' and '@graph' not in nsch
  receipt=next(x for x in heads['pages'] if x['family']==family)
  assert receipt['accepted_head_SHA256']==sha(oldhead) and receipt['candidate_head_SHA256']==sha(newhead)
  assert len(receipt['spans'])==(8 if family=='hafnian' else 7)
  hp=splice(oldhead,newhead,receipt['spans']); parsed=HTML(new.decode()); metas=[x for t,x in parsed.tags if t=='meta']
  assert not any(x.get('name') in ('robots','googlebot') for x in metas)
  assert [x['href'] for t,x in parsed.tags if t=='link' and x.get('rel')=='canonical']==[canonical]
  assert [x['content'] for x in metas if x.get('property')=='og:url']==[canonical]
  assert [x['href'] for t,x in parsed.tags if t=='link' and x.get('rel')=='stylesheet']==['/research/research.css']
  assert [x['content'] for x in metas if x.get('name')=='citation_pdf_url']==[canonical+'assets/paper.pdf']
  assert [x['content'] for x in metas if x.get('name')=='DC.description']==[model['abstract']]
  assert html.unescape(one(r'<p id="abstract-text">(.*?)</p>',new.decode())[1])==nsch['abstract']==model['abstract']==accepted['abstract']
  assert pin(page.parent/'citation.bib')==pin(writer/'citation.bib')==accepted['Bib']
  for a in accepted['assets']:
   assert pin(page.parent/a['relative_path'])=={k:a[k] for k in ('bytes','SHA256','mode')}==pin(writer/a['relative_path'])
   for r in a['native_source_matches']: assert pin(P/'papers'/model['record_id']/'sources'/r)==pin(page.parent/a['relative_path'])
  assert [x['name'] for x in nsch['encoding']]==accepted['native_encoding_names']
  pageproofs.append({'family':family,'canonical':canonical,'article':pin(page),'HEAD_forward_reverse':hp,'BODY_MAIN_abstract_Bib_native_assets_exact':True})
 oi=(BASE/'research/index.html').read_bytes(); ox=(BASE/'research/sitemap.xml').read_bytes()
 ni=(W/'public/research/index.html').read_bytes(); nx=(W/'public/research/sitemap.xml').read_bytes()
 old,oe=aggregate(oi,ox); new,ne=aggregate(ni,nx)
 assert old==binding['aggregate_baseline']==readj(S/'BASELINE_AGGREGATE_UNITS.json') and new==readj(S/'CANDIDATE_AGGREGATE_UNITS.json')
 assert old['counts']=={'visible_HTML':128,'raw_JSON':128,'typed_JSON':128,'XML':129} and new['counts']=={'visible_HTML':130,'raw_JSON':130,'typed_JSON':130,'XML':131}
 for k in ('raw_visible_HTML_units','visible_text_units','raw_JSON_units','typed_ItemList_units','raw_XML_units','parsed_XML_units','XML_locations'): assert new[k][:len(old[k])]==old[k],k
 assert ne['tree']['attributes']==oe['tree']['attributes'] and ne['tree']['text']==oe['tree']['text'] and ne['tree']['children'][:129]==oe['tree']['children']
 fidelity=readj(S/'AGGREGATE_FIDELITY.json'); count=one(rb'"numberOfItems"\s*:\s*(128)(?=\s*[,}])',oi)
 edits=[(count.start(1),count.end(1),'128','130'),(oe['JSON_end_byte'],oe['JSON_end_byte'],'',', '+', '.join(new['raw_JSON_units'][128:])),(oi.index(b'</ul>'),oi.index(b'</ul>'),'','\n'.join(new['raw_visible_HTML_units'][128:])+'\n')]
 assert [(x['start_byte'],x['end_byte'],x['old_UTF8'],x['new_UTF8']) for x in fidelity['index_spans']]==edits
 assert [(x['start_byte'],x['end_byte'],x['old_UTF8'],x['new_UTF8']) for x in fidelity['XML_spans']]==[(ox.index(b'</urlset>'),ox.index(b'</urlset>'),'','\n'.join(new['raw_XML_units'][129:])+'\n')]
 aggregateproofs={'index':splice(oi,ni,fidelity['index_spans']),'XML':splice(ox,nx,fidelity['XML_spans'])}
 publish=readj(E/'publish-python314.stdout.json'); installed=readj(E/'install-python314.stdout.json')
 assert publish['schema']=='hafnian-retract-publication-success-v1' and publish['status']=='SCOPED11_COMMIT_AND_PUSH_VERIFIED_SNAPSHOT'
 assert publish['commit']==COMMIT and publish['parent']==PARENT and publish['tree']==TREE and publish['bindings']['scope_paths']==scope
 assert installed['counts']==[790,381,130,131] and installed['targets']==scope and installed['status']=='FILESYSTEM_INSTALL_VERIFIED_SNAPSHOT'
 it=Path(installed['transaction'])
 assert (it/'aggregate-backups/public/research/index.html').read_bytes()==oi and (it/'aggregate-backups/public/research/sitemap.xml').read_bytes()==ox
 assert readj(T/'SUCCESS.json')==publish and readj(it/'SUCCESS.json')==installed
 attempts=[]
 for stem,exitcode in [('preflight',1),('preflight-python314',0),('install-python314',0),('verify-installed-python314',0),('publish-python314',0)]:
  x=readj(E/(stem+'.execution.json')); out=(E/(stem+'.stdout.json')).read_bytes(); err=(E/(stem+'.stderr.bin')).read_bytes()
  assert x['exit_code']==exitcode and x['stdout_bytes']==len(out) and x['stderr_bytes']==len(err)
  assert x['stdout_SHA256']==sha(out) and x['stderr_SHA256']==sha(err) and x['helper_SHA256']==publish['bindings']['helper']['SHA256']
  if exitcode: assert not out and len(err)==1741 and b"zip() takes no keyword arguments" in err
  else: assert not err
  attempts.append({'stem':stem,'exit':exitcode,'stdout_bytes':len(out),'stderr_bytes':len(err)})
 disposition=readj(ROOT_CONTROLS[2]); assert disposition['exit']==1 and disposition['installation_or_publication_authorized_by_this_note'] is False
 rawold=(T/'native-backups/index.before').read_bytes(); rawnew=(W/'.git/index').read_bytes()
 assert len(rawold)==9059206 and sha(rawold)=='592a25281b63a357fbe4fe2580e2c9764ba2b4836650d8751ac573ff8117c365'
 assert len(rawnew)==9060430 and sha(rawnew)=='25494ed68b5d5612ae64ac01f2897c77b26024a994b66167426203d5620de4b7'
 assert rawnew==(T/'native-successor.index').read_bytes()
 oldrecords,oldmap,oldext=index_parse(rawold); newrecords,newmap,newext=index_parse(rawnew)
 targets={x.encode() for x in scope}; assert len(oldrecords)==58721 and len(newrecords)==58730
 assert set(newrecords)==set(oldrecords)|targets and len(set(oldrecords)-targets)==58719
 assert {k:v for k,v in oldrecords.items() if k not in targets}=={k:v for k,v in newrecords.items() if k not in targets}
 assert oldext==newext
 targetproof=[]
 for name in sorted(targets):
  data=(W/name.decode()).read_bytes(); oid=git_oid('blob',data)
  record=struct.pack('!10I',0,0,0,0,0,0,0o100644,0,0,0)+bytes.fromhex(oid)+struct.pack('!H',min(len(name),0xFFF))+name+b'\x00'
  record+=b'\x00'*((-len(record))%8); assert newrecords[name]==record and newmap[name]==('100644','blob',oid)
  assert object_bytes(oid,'blob')==data
  targetproof.append({'path':name.decode(),'blob_OID':oid,'whole_zero_stat_record_exact':True,'record_bytes':len(record)})
 rebuilt=b'DIRC'+struct.pack('!II',2,58730)+b''.join(newrecords[k] for k in sorted(newrecords))+b''.join(x[1] for x in oldext)
 rebuilt+=hashlib.sha1(rebuilt).digest(); assert rebuilt==rawnew
 maps=[semantic_map(readj(T/n)) for n in ('before-native-semantics.json','after-native-semantics.json','parent-HEAD-tree.json','successor-commit-tree.json')]
 assert maps[0]==maps[2]==oldmap and maps[1]==maps[3]==newmap
 foreign_before={k:(oldmap.get(k),maps[2].get(k)) for k in set(oldmap)|set(maps[2]) if oldmap.get(k)!=maps[2].get(k) and k not in targets}
 foreign_after={k:(newmap.get(k),maps[3].get(k)) for k in set(newmap)|set(maps[3]) if newmap.get(k)!=maps[3].get(k) and k not in targets}
 assert foreign_before==foreign_after=={} and readj(T/'foreign-staging.before.json')==readj(T/'foreign-staging.after.json')==[]
 oldtree,oldtable,oldbodies=semantic_trees(oldmap); newtree,newtable,newbodies=semantic_trees(newmap)
 assert oldtree=='c59d0d0a542f20bceb3556b1e936e86b22626434' and newtree==TREE
 assert object_bytes(oldtree,'tree')==oldbodies[b''] and object_bytes(TREE,'tree')==newbodies[b'']
 proof=readj(T/'native-index-proof.json'); assert proof['schema']=='hafnian-retract-native-index-proof-v1'
 assert proof['protected_whole_raw_records']==58719 and proof['selected_zero_stat_records']==11 and proof['after_records']==58730 and proof['before_records']==58721
 oc=next(x[1] for x in oldext if x[0]==b'TREE'); nc=next(x[1] for x in newext if x[0]==b'TREE')
 assert oc==nc and len(nc)==35878 and sha(nc)=='f12d2a0b795034ce5cab45ad6fa5da31b4d7ad6f4b22a5999ce27841b41350b3'
 cache_before=cache_check(oc,oldtable,proof['before_TREE_semantics']); cache_after=cache_check(nc,newtable,proof['after_TREE_semantics'])
 commit=object_bytes(COMMIT,'commit'); assert commit==(T/'commit-object.txt').read_bytes()
 header=commit.decode().split('\n\n',1)[0].splitlines()
 assert header[0]=='tree '+TREE and [x for x in header if x.startswith('parent ')]==['parent '+PARENT]
 assert any(x.startswith('author Alec Kriebel <me@aleckriebel.com> ') for x in header) and any(x.startswith('committer Alec Kriebel <me@aleckriebel.com> ') for x in header)
 assert object_bytes(PARENT,'commit').split(b'\n',1)[0]==b'tree '+oldtree.encode()
 delta=[]
 for name in sorted(set(oldmap)|set(newmap)):
  if oldmap.get(name)==newmap.get(name): continue
  assert name in targets
  oldvalue=oldmap.get(name,('000000','blob','0'*40)); newvalue=newmap[name]; status='M' if name in oldmap else 'A'
  delta.extend(((':'+oldvalue[0]+' '+newvalue[0]+' '+oldvalue[2]+' '+newvalue[2]+' '+status).encode(),name))
 assert b'\x00'.join(delta)+b'\x00'==(T/'commit-delta.raw').read_bytes() and len(delta)==22
 assert (T/'native-backups/HEAD.before').read_bytes()==(W/'.git/HEAD').read_bytes()
 assert (T/'native-backups/config.before').read_bytes()==(W/'.git/config').read_bytes()
 assert (T/'native-backups/loose-master.before').read_bytes()==(PARENT+'\n').encode()
 out={'schema':'independent-hafnian-retract-postpublication-data-audit-v1','status':'PASS_FIXED_LOCAL_POSTPUBLICATION_AUDIT',
  'UTC_start':started,'commit':COMMIT,'parent':PARENT,'tree':TREE,'public_extent':[790,381,130,131],'projection':'9A2M/11paths/4dirs',
  'published_all_candidate_bytes_modes_topology_exact':True,'untouched_old_files':779,'old_directory_modes':377,'DS_Store':17,
  'page_fidelity':pageproofs,'whole_old128_HTML_concat_visible_rawJSON_typed_and129_full_XML_prefixes_exact':True,
  'aggregate_whole_forward_reverse':aggregateproofs,'protected_untargeted_whole_raw_index_records':58719,
  'selected_zero_stat_records':targetproof,'whole_successor_index_exact_reconstructed':True,'all_extension_chunks_exact':True,
  'TREE_before':cache_before,'TREE_after':cache_after,'semantic_before_tree':oldtree,'semantic_after_tree':newtree,
  'foreign_staging_actual_count':0,'actual_commit_object_and_single_parent_and11path_delta_exact':True,'literal_execution_history':attempts,
  'all_source_private_stage_audit_runtime_root_receipts_and_native_guards_exact':True,'producer_helper_Git_network_source_W_mutation':False,
  'actual_UI_scientific_copy_live_deploy_certificate':False}
finally:
 after=capture(template); save_guard('GUARDS_AFTER.json',after)
 assert after==before,'Protected state changed during passive publication audit'
out['UTC_end']=utc(); out['whole_before_after_guards_equal']=True
print(json.dumps(out,indent=2,ensure_ascii=False))
