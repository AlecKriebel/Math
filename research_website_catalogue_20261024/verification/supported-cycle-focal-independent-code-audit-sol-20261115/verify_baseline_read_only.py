"""Standalone held baseline custody; no live/site/Git/writer/source descriptor imports or writes."""
from pathlib import Path,PurePosixPath
import hashlib,json,re,stat,struct,sys,xml.etree.ElementTree as ET
D=Path(__file__).resolve().parent;N=0

def need(ok,label):
 global N
 N+=1
 if not ok:raise RuntimeError(label)
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):
 p=Path(p);need(D in p.parents and p.resolve()==p and stat.S_ISREG(p.lstat().st_mode),'only own ordinary held file')
 return p.read_bytes()
def obj(p):return json.loads(read(p))
def pin(p,r):
 b=read(p);need(len(b)==r['bytes'] and sha(b)==r['SHA256'],'full held byte pin');return b
def snap(row):return pin(row['snapshot']['path'],row['snapshot'])
def equal(a,b):
 need(type(a) is type(b),'exact held type')
 if isinstance(a,dict):
  need(list(a)==list(b),'whole ordered keys')
  for k in a:equal(a[k],b[k])
 elif isinstance(a,list):
  need(len(a)==len(b),'whole ordered array extent')
  for x,y in zip(a,b):equal(x,y)
 else:need(a==b,'whole held scalar/null')
def namespace(root):
 need(root==D,'only own root namespace')
 files=[];dirs=[]
 for p in root.rglob('*'):
  mode=p.lstat().st_mode;need(p.resolve()==p and (stat.S_ISREG(mode) or stat.S_ISDIR(mode)),'ordinary exact held extent')
  (files if stat.S_ISREG(mode) else dirs).append(p.relative_to(root).as_posix())
 return sorted(files),sorted(dirs)
def native(raw,targets):
 need(raw[:4]==b'DIRC' and len(raw)>=32 and hashlib.sha1(raw[:-20]).digest()==raw[-20:],'whole native checksum');version,count=struct.unpack('>II',raw[4:12]);need(version==2,'native v2')
 offset=12;paths=[];tuples=[];protected=[];ptuples=[]
 for _ in range(count):
  start=offset;need(start+62<len(raw)-20,'native complete header');flags=struct.unpack('>H',raw[start+60:start+62])[0];need(flags&0xF000==0,'stage0 native flags');end=raw.find(b'\0',start+62,len(raw)-20);need(end>=0,'native terminator');p=raw[start+62:end];need(p and flags&0xFFF==min(len(p),0xFFF),'native name length');offset=start+((end+1-start+7)//8)*8;need(raw[end:offset]==b'\0'*(offset-end),'native padding');mode=struct.unpack('>I',raw[start+24:start+28])[0];need(mode in [0o100644,0o100755,0o120000,0o160000],'native mode');oid=raw[start+40:start+60].hex();t=('%06o'%mode).encode()+b' '+oid.encode()+b' 0\t'+p;paths.append(p);tuples.append(t)
  if p not in targets:protected.append((p,raw[start:offset]));ptuples.append(t)
 need(paths==sorted(paths) and len(paths)==len(set(paths)),'unique ordered whole native records');extensions=0
 while offset<len(raw)-20:
  need(offset+8<=len(raw)-20,'whole extension');key=raw[offset:offset+4];length=struct.unpack('>I',raw[offset+4:offset+8])[0];offset+=8;need(key==b'TREE' and offset+length<=len(raw)-20,'audited TREE extension');offset+=length;extensions+=1
 need(offset==len(raw)-20 and extensions<=1,'whole native extent')
 return count,paths,b'\0'.join(tuples)+b'\0',protected,b'\0'.join(p+b'\t'+r.hex().encode() for p,r in protected)+b'\0',b'\0'.join(ptuples)+b'\0'
def node(x):return {'tag':x.tag,'attributes_in_original_order':list(x.attrib.items()),'text':x.text,'tail':x.tail,'children':[node(c) for c in x]}
def main():
 need(sys.argv[1:] in [[],['--preseal']],'only held modes');preseal=bool(sys.argv[1:])
 sb=read(D/'INITIAL_SEAL.json');need(sha(sb)=='709ceeaf5c386f2ffd24682a919fd100d51224b4207e43f68c361ab8e4c8b21b','source-only initial immutable');initial=json.loads(sb);mb=read(D/'INITIAL_MANIFEST.json');need(sha(mb)==initial['MANIFEST_SHA256'],'whole initial manifest')
 for r in json.loads(mb)['files']:pin(D/r['path'],r)
 gb=read(D/'BASELINE_ACTUAL_GO.json');need(sha(gb)=='0d7371f227e608c79d7f79135cb78cecd2fee4e190c7952bebb3afa7c0c639c2','separate actual623 GO');go=json.loads(gb)
 b=obj(D/'ACTUAL623_PUBLIC_BASELINE.json');need(b['HEAD']==go['actualWebsiteHEAD']=='0880af3e389248dbcd098ac275a880d93e09ea99' and b['tree']==go['actualWebsiteTree'],'actual captured HEAD/tree')
 need(b['counts']==[623,94,95] and b['writer_exposed'] is False,'fresh before writer exposure')
 public={}
 for r in b['public_files']:
  body=snap(r);need(len(body)==r['bytes'] and sha(body)==r['SHA256'],'whole623 original descriptor');public[r['public_relative_path']]=body
 need(sorted(public)==b['public_namespace'] and len(public)==623,'all623 distinct held public files')
 for r in b['site_configs']:snap(r)
 need(len(b['site_configs'])==2,'two actual site configs')
 a=obj(D/'ACTUAL623_AGGREGATE_OBJECTS.json');graphs=re.findall(rb'<script type="application/ld\+json">\s*(.*?)\s*</script>',public['research/index.html'],re.S);need(len(graphs)==1,'one held graph');equal(json.loads(graphs[0]),a['whole_index_JSON_graph']);cards=re.findall(rb'<li(?:\s[^>]*)?>.*?</li>',public['research/index.html'],re.S);need([c.decode() for c in cards]==[x['whole_raw_HTML'] for x in a['whole_visible_records_in_original_order']] and len(cards)==94,'whole ordered94 visible records')
 x=ET.fromstring(public['research/sitemap.xml']);equal(node(x),a['whole_XML_root']);equal([node(c) for c in x],a['whole_XML_nodes_in_original_order']);need(len(x)==95,'whole95 XML nodes')
 g=obj(D/'ACTUAL623_GIT_OBSERVATIONS.json');raw=pin(g['whole_native_index_snapshot']['path'],g['whole_native_index_snapshot']);need(sha(raw)==go['actualIndexSHA256']==g['actual_whole_index_SHA256'],'whole fresh actual index')
 targets={p.encode() for p in g['fresh_exact_future10_target_set']};count,paths,tuples,prot,stream,ptuples=native(raw,targets)
 need(count==g['all_native_index_record_count']==58563 and len(prot)==g['fresh_protected_raw_native_record_count']==58561,'actual derived new-scope counts')
 need(set(paths)&targets=={b'public/research/index.html',b'public/research/sitemap.xml'},'exact two existing aggregates')
 need(tuples==pin(g['actual_stage_tuple_stream']['path'],g['actual_stage_tuple_stream']) and stream==pin(g['fresh_protected_raw_native_stream']['path'],g['fresh_protected_raw_native_stream']) and ptuples==pin(g['protected_stage_tuple_stream']['path'],g['protected_stage_tuple_stream']),'every full raw record and whole actual tuple stream')
 for r in g['Git_control_files']:snap(r)
 deletion=pin(g['actual_cached_deletions']['path'],g['actual_cached_deletions']);need(g['actual_cached_deletion_count']==len([r for r in deletion.split(b'\0') if r])==0,'actual deletion observation not assumed')
 core=obj(D/'ACTUAL623_QUALIFIED_CORE.json');need(len(core['files'])==18 and core['all18_original_unchanged_claim'] is False and core['actual_checkpoint_SHA256']=='405b0357fd20a2e14893ce6c3c1a0f81910894ccd8ffaddac4e25014138fb9c0','qualified17 plus405b core')
 for r in core['files']:snap(r)
 source=obj(D/'SOURCE_FULL_SNAPSHOTS.json');originals=obj(D/'SOURCE_ROOT_BINDINGS.json')['whole_distinct_original_bindings'];equal([r['original'] for r in source['rows']],originals)
 for r in source['rows']:body=pin(r['snapshot']['path'],r['snapshot']);need(len(body)==r['original']['bytes'] and sha(body)==r['original']['SHA256'],'all775 whole original buffers')
 need(len(source['rows'])==775,'775 complete source/editorial held snapshots')
 frame=obj(D/'BASELINE_FRAME_EXPECTATIONS.json');need(frame['derived_before_any_writer_exposure'] is True and frame['actual_HEAD']==b['HEAD'],'independent actual frame before writer exposure')
 for r in frame['whole_observed_frames']:snap(r['whole_baseline_file'])
 if not preseal:
  seal=obj(D/'BASELINE_SEAL.json');manifest_body=read(D/'BASELINE_MANIFEST.json');need(sha(manifest_body)==seal['MANIFEST_SHA256'],'same baseline manifest buffer');m=json.loads(manifest_body);names=[]
  for r in m['files']:pin(D/r['path'],r);names.append(r['path'])
  files,dirs=namespace(D);need(files==sorted(names+['BASELINE_MANIFEST.json','BASELINE_SEAL.json']) and dirs==m['directories'],'complete prewriter baseline extent')
  need(m['exact_root_terminal_exclusions']==['BASELINE_MANIFEST.json','BASELINE_SEAL.json'] and m['future_subtree_exclusions']==[],'exact baseline root terminals only')
 print(json.dumps({'status':'PASS_INDEPENDENT_PREWRITER_ACTUAL623_HELD_BASELINE_CUSTODY','mode':'preseal' if preseal else 'sealed-baseline','checks':N,'HEAD':b['HEAD'],'counts':[623,94,95],'conditional_proposal':[631,96,97],'whole_native_index_records':count,'fresh_protected_full_native_records':len(prot),'whole_original_source_editorial_buffers':775,'writer_or_live_site_Git_source_programmes_network_subprocess_or_writes':False,'publication_authority':False},sort_keys=True))
if __name__=='__main__':main()
