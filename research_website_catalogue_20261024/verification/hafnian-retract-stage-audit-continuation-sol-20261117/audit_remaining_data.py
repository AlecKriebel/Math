"""One passive data-only continuation. No project imports, subprocess or network.
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
N=V/'hafnian-retract-stage-audit-continuation-sol-20261117'
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
 B/'INPUT_BINDINGS.json':'c7ddeb3e335b317bba3864912807083fe4df423f0392be004de6df376c1b8a40'}

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
 return {'protected':protected,'whole_corrected_stage':census(S),'prior_failed_audit':census(A)}
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

started=utc(); expected=readj(A/'GUARDS_BEFORE.json')
assert set(expected)=={'protected','whole_corrected_stage'}
validate(expected['whole_corrected_stage'])
template=expected['protected']; before=capture(template); save_guard('GUARDS_BEFORE.json',before)
try:
 for p,h in PINS.items(): assert pin(p)['SHA256']==h,str(p)
 assert (A/'GUARDS_BEFORE.json').read_bytes()==(A/'GUARDS_AFTER.json').read_bytes()
 assert before['protected']==template and before['whole_corrected_stage']==expected['whole_corrected_stage']
 failed=before['prior_failed_audit']; assert (failed['regular_files'],failed['child_directories'])==(12,0)
 manifest=readj(A/'OWNED_MANIFEST.json'); assert manifest['schema']=='finite-hafnian-retract-corrected-stage-audit-manifest-v1'
 assert manifest['regular_files_after_terminal_creation']==12 and manifest['child_directories']==0
 assert manifest['root_mode']==failed['directories']['.']['mode']=='0755' and manifest['directories']==[]
 assert manifest['other_exclusions']==[] and set(manifest['exact_already_created_terminal_recursive_hash_exclusions'])=={str(A/'FINAL.json'),str(A/'OWNED_MANIFEST.json')}
 seen=set()
 for x in manifest['payload_files']:
  assert set(x)=={'path','bytes','SHA256','mode'}; r=x['path']; pathcheck(r); assert r not in seen; seen.add(r)
  validate_pin({k:x[k] for k in ('bytes','SHA256','mode')}); assert failed['files'][r]=={k:x[k] for k in ('bytes','SHA256','mode')}
 assert seen==set(failed['files'])-{'FINAL.json','OWNED_MANIFEST.json'} and len(seen)==10
 assert readj(A/'FINAL.json')['status']=='AUDIT_INCOMPLETE_READER_SCHEMA_ERROR'
 binding=readj(B/'INPUT_BINDINGS.json')
 oi=(BASE/'research/index.html').read_bytes(); ni=(CAND/'research/index.html').read_bytes()
 ox=(BASE/'research/sitemap.xml').read_bytes(); nx=(CAND/'research/sitemap.xml').read_bytes()
 old,oe=aggregate(oi,ox); new,ne=aggregate(ni,nx)
 assert old==binding['aggregate_baseline']==readj(S/'BASELINE_AGGREGATE_UNITS.json')
 assert new==readj(S/'CANDIDATE_AGGREGATE_UNITS.json')
 assert old['counts']=={'visible_HTML':128,'raw_JSON':128,'typed_JSON':128,'XML':129}
 assert new['counts']=={'visible_HTML':130,'raw_JSON':130,'typed_JSON':130,'XML':131}
 for k in ('raw_visible_HTML_units','visible_text_units','raw_JSON_units','typed_ItemList_units','raw_XML_units','parsed_XML_units','XML_locations'): assert new[k][:len(old[k])]==old[k],k
 assert ne['tree']['attributes']==oe['tree']['attributes'] and ne['tree']['text']==oe['tree']['text'] and ne['tree']['children'][:129]==oe['tree']['children']
 entries=[]; wanted=[]; canonicals=[]
 for i,accepted in enumerate(binding['pages'],128):
  writer=V/(accepted['family']+'-editorial-sol-20261117'); model=readj(writer/'page-model.json')
  path=model['deployment_proposal']['path']; canonical='https://aleckriebel.com'+path; canonicals.append(canonical)
  unit=new['raw_visible_HTML_units'][i]; parsed=HTML(unit); anchors=[x for t,x in parsed.tags if t=='a']
  assert [x['href'] for x in anchors]==[path,path+'assets/paper.pdf',model['doi_url']]
  paragraphs=re.findall(r'<p>(.*?)</p>',unit,re.S); assert len(paragraphs)==2
  assert html.unescape(paragraphs[0])==model['meta_description']
  expected_links='<a href="'+path+'assets/paper.pdf">PDF</a> · <a href="'+model['doi_url']+'">Zenodo</a>'
  assert paragraphs[1]==expected_links
  assert html.unescape(one(r'<li><a[^>]*>(.*?)</a>',unit)[1])==model['title']
  metadata=one(r'<span class="entry-meta">(.*?)</span>',unit)[1]
  native_entry=one(r'<p class="entry-meta">(.*?)</p>',(writer/'main.html').read_text())[1].split('</a> · ',1)[1]
  assert metadata==native_entry and one(r'<time datetime="(.*?)">(.*?)</time>',metadata)[1]=='2026-10-06'
  expected_unit='<li><a href="'+path+'">'+html.escape(model['title'])+'</a><br><span class="entry-meta">'+metadata+'</span><p>'+html.escape(model['meta_description'])+'</p><p>'+expected_links+'</p></li>'
  assert unit==expected_unit and visible(unit)==' '.join((model['title']+visible(metadata)+model['meta_description']+'PDF · Zenodo').split())
  if accepted['family']=='hafnian': assert 'Version 1.0.0' in metadata and model['native_version']=='1.0.0'
  else: assert 'Zenodo display edition: v1' in metadata and model['native_version'] is None
  item={'@type':'ListItem','position':i+1,'url':canonical,'name':model['title']}; wanted.append(item)
  entries.append({'family':accepted['family'],'paragraphs':2,'description_first_links_second':True,'accepted_metadata_and_full_visible_unit_exact':True,'canonical':canonical,'unit_SHA256':sha(unit.encode())})
 assert new['typed_ItemList_units'][128:]==wanted and new['XML_locations'][129:]==canonicals
 assert all(x['children'][1]['text']=='2026-11-17' for x in ne['tree']['children'][129:])
 fidelity=readj(S/'AGGREGATE_FIDELITY.json'); assert fidelity['schema']=='whole-buffer-reversible-aggregate-fidelity-v1'
 count=one(rb'"numberOfItems"\s*:\s*(128)(?=\s*[,}])',oi)
 edits=[(count.start(1),count.end(1),'128','130'),(oe['JSON_end_byte'],oe['JSON_end_byte'],'',', '+', '.join(new['raw_JSON_units'][128:])),(oi.index(b'</ul>'),oi.index(b'</ul>'),'','\n'.join(new['raw_visible_HTML_units'][128:])+'\n')]
 assert [(x['start_byte'],x['end_byte'],x['old_UTF8'],x['new_UTF8']) for x in fidelity['index_spans']]==edits
 assert [(x['start_byte'],x['end_byte'],x['old_UTF8'],x['new_UTF8']) for x in fidelity['XML_spans']]==[(ox.index(b'</urlset>'),ox.index(b'</urlset>'),'','\n'.join(new['raw_XML_units'][129:])+'\n')]
 proofs={'index':splice(oi,ni,fidelity['index_spans']),'XML':splice(ox,nx,fidelity['XML_spans'])}
 assert (S/'ORIGINAL_RESEARCH_INDEX.html').read_bytes()==oi and (S/'ORIGINAL_RESEARCH_SITEMAP.xml').read_bytes()==ox
 for k,p in (('baseline_index',BASE/'research/index.html'),('candidate_index',CAND/'research/index.html'),('baseline_XML',BASE/'research/sitemap.xml'),('candidate_XML',CAND/'research/sitemap.xml')): assert fidelity[k]==pin(p)
 index=(W/'.git/index').read_bytes(); assert len(index)==9059206 and index[:4]==b'DIRC'
 assert struct.unpack('!II',index[4:12])==(2,58721) and hashlib.sha1(index[:-20]).digest()==index[-20:]
 assert sha(index)=='592a25281b63a357fbe4fe2580e2c9764ba2b4836650d8751ac573ff8117c365'
 objects=[]
 for oid,kind,body in ((binding['guards_before']['native_W']['resolved_native_HEAD'],'commit',binding['native_W_commit_body'].encode()),(binding['native_W_commit_tree'],'tree',bytes.fromhex(binding['native_W_tree_body_hex']))):
  obj=zlib.decompress((W/'.git/objects'/oid[:2]/oid[2:]).read_bytes()); assert obj==kind.encode()+b' '+str(len(body)).encode()+b'\x00'+body and hashlib.sha1(obj).hexdigest()==oid
  objects.append({'kind':kind,'oid':oid,'whole_body_equal_to_binding':True})
 out={'schema':'independent-hafnian-retract-stage-audit-continuation-data-v1','status':'PASS_REMAINING_FIXED_ARTIFACT_CHECKS','UTC_start':started,
  'new_entries':entries,'whole_aggregate_forward_reverse':proofs,'all_old128_HTML_visible_rawJSON_typed_and129_full_XML_prefixes_exact':True,
  'actual_two_paragraph_schema_validated':True,'native_W_raw_index_checksum_and_header_exact':True,'native_W_existing_objects':objects,
  'whole_protected_stage_inputs_and_prior_failed_audit_exact':True,'prior_own_attempt_exit_remains':1,'producer_exits_remain':[1,0],
  'producer_source_helper_execution':False,'Git_network_W_source_otherpacket_mutation':False,'production_authority':False}
finally:
 after=capture(template); save_guard('GUARDS_AFTER.json',after)
 assert after==before,'Protected state changed during continuation'
out['UTC_end']=utc(); out['whole_before_after_guards_equal']=True
print(json.dumps(out,indent=2,ensure_ascii=False))
