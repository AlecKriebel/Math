"""Validate only the fresh held baseline/initial buffers; no actual site/Git access."""
from pathlib import Path
import hashlib,json,re,stat,struct
import xml.etree.ElementTree as ET
D=Path(__file__).resolve().parent
checks=0
def need(ok,label):
 global checks
 checks+=1
 if not ok:raise RuntimeError(label)
def read(p):
 p=Path(p);need(p.resolve()==p and D in p.parents and stat.S_ISREG(p.lstat().st_mode),'owned ordinary file');return p.read_bytes()
def obj(p):return json.loads(read(p))
def pin(b):return {'bytes':len(b),'SHA256':hashlib.sha256(b).hexdigest()}
def exact(a,b,label):
 need(type(a) is type(b),'type '+label)
 if isinstance(a,dict):
  need(list(a)==list(b),'ordered keys '+label)
  for k in a:exact(a[k],b[k],label+'/'+k)
 elif isinstance(a,list):
  need(len(a)==len(b),'length '+label)
  for i,(x,y) in enumerate(zip(a,b)):exact(x,y,label+'/'+str(i))
 else:need(a==b,'scalar '+label)
baseline=obj(D/'ACTUAL623_PUBLIC_BASELINE.json');git=obj(D/'ACTUAL623_GIT_OBSERVATIONS.json');core=obj(D/'ACTUAL623_QUALIFIED_CORE.json')
need(baseline['counts']==[623,94,95] and baseline['writer_exposed'] is False,'fresh preexposure baseline')
rows=baseline['public_files']+baseline['site_configs']+git['Git_control_files']+core['files']
for r in rows:
 b=read(r['snapshot']['path']);need(pin(b)=={k:r[k] for k in ['bytes','SHA256']},'whole held snapshot')
pub={r['public_relative_path']:read(r['snapshot']['path']) for r in baseline['public_files']}
need(len(pub)==623 and sorted(pub)==baseline['public_namespace'],'complete public snapshot')
index=read(D/'inputs/baseline623/native-index.before');need(hashlib.sha1(index[:-20]).digest()==index[-20:],'native SHA1 checksum')
need(pin(index)['SHA256']=='35181f4046df6e197ba5c5c6e34c348b2b46783c0cc073a5b7f066692ba332b6','whole index SHA256')
need(index[:4]==b'DIRC' and struct.unpack('>II',index[4:12])==(2,58563),'native version/count')
targets={('public/'+x).encode() for x in baseline['expected_future_paths']};offset=12;paths=[];tuples=[];protected=[];protected_tuples=[]
for _ in range(58563):
 start=offset;flags=struct.unpack('>H',index[start+60:start+62])[0];end=index.find(b'\0',start+62,len(index)-20)
 need(end>=0 and flags&0xf000==0,'native stage/flags/path')
 path=index[start+62:end];offset=start+((end+1-start+7)//8)*8;record=index[start:offset]
 need(index[end:offset]==bytes(offset-end) and flags&0xfff==min(len(path),0xfff),'native padding/length')
 mode=struct.unpack('>I',index[start+24:start+28])[0];oid=index[start+40:start+60].hex()
 item=('%06o'%mode).encode()+b' '+oid.encode()+b' 0\t'+path;tuples.append(item);paths.append(path)
 if path not in targets:protected.append(path+b'\t'+record.hex().encode());protected_tuples.append(item)
need(paths==sorted(paths) and len(paths)==len(set(paths)),'index identity/order')
need(len(protected)==58561,'fresh protected records')
for name,expected in [('native-index-stage-tuples.z',tuples),('protected-index-stage-tuples.z',protected_tuples),('protected-native-index.raw-records',protected)]:
 need(read(D/'inputs/baseline623'/name)==b'\0'.join(expected)+b'\0','whole native stream '+name)
need(read(D/'inputs/baseline623/actual-staged-deletions.z')==b'','zero actual cached deletion stream')
for command in git['actual_read_only_commands']:
 need(command['exit_code']==0,'actual targeted Git exit')
 for role in ['stdout','stderr']:
  b=read(D/command[role+'_file']);need(len(b)==command[role+'_bytes'] and hashlib.sha256(b).hexdigest()==command[role+'_SHA256'],'whole command stream')
need(len(git['actual_read_only_commands'])==15,'actual targeted command history')
aggregates=obj(D/'ACTUAL623_AGGREGATE_OBJECTS.json');html=pub['research/index.html'];graph=json.loads(re.search(rb'<script type="application/ld\+json">\s*(.*?)\s*</script>',html,re.S).group(1));exact(graph,aggregates['whole_index_JSON_graph'],'complete old graph')
cards=re.findall(rb'<li(?:\s[^>]*)?>.*?</li>',html,re.S);need(len(cards)==94,'old cards')
for a,b in zip(cards,aggregates['whole_visible_records_in_original_order']):need(a.decode()==b['whole_raw_HTML'],'old whole visible card')
def node(x):return {'tag':x.tag,'attributes_in_original_order':list(x.attrib.items()),'text':x.text,'tail':x.tail,'children':[node(c) for c in x]}
exact(node(ET.fromstring(pub['research/sitemap.xml'])),aggregates['whole_XML_root'],'complete old XML')
need(core['original17_plus_sole_authorized405b_checkpoint'] is True and core['all18_original_unchanged_claim'] is False,'qualified core')
need(core['actual_checkpoint_SHA256']=='405b0357fd20a2e14893ce6c3c1a0f81910894ccd8ffaddac4e25014138fb9c0','qualified checkpoint')
frames=obj(D/'BASELINE_FRAME_EXPECTATIONS.json')
for f in frames['whole_native_frames']:
 s=pub[f['fresh_snapshot']['public_relative_path']].decode();need(f['whole_head'] in s and f['whole_head_to_main_body_prefix'] in s and s.endswith(f['whole_after_main_suffix']),'whole observed frame')
for rec in obj(D/'INITIAL_MANIFEST.json')['files']:need(pin(read(D/rec['path']))=={k:rec[k] for k in ['bytes','SHA256']},'immutable initial payload')
print(json.dumps({'status':'PASS_HELD_FRESH623_PREWRITER_BASELINE_CUSTODY','checks':checks,'actual_counts':[623,94,95],'index_records':58563,'protected_native_records':58561,'actual_cached_deletions':0,'core':'17original_plus405b','new_V2_writer_exposure':False,'actual_site_Git_network_science_render_control_subprocess_or_writes':False,'production_authority':False}))
