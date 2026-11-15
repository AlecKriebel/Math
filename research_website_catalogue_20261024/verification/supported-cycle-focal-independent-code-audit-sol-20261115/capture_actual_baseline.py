"""Root-authorized independent fresh623 read-only baseline; no writer or mutations."""
from pathlib import Path
from html.parser import HTMLParser
import datetime,hashlib,json,os,re,stat,struct,subprocess,xml.etree.ElementTree as ET
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024');D=Path(__file__).resolve().parent;W=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com');WRITER=P/'verification/supported-cycle-focal-private-stage-sol-20261115'
H=lambda b:hashlib.sha256(b).hexdigest();COMMANDS=[]

def need(ok,label):
 if not ok:raise RuntimeError(label)
def read(p):
 p=Path(p);need(p!=WRITER and WRITER not in p.parents,'writer remains blind before any inspection')
 need(p.resolve()==p and stat.S_ISREG(p.lstat().st_mode),'ordinary real captured file '+str(p));return p.read_bytes()
def pin(p):
 b=read(p);return {'path':str(p),'bytes':len(b),'SHA256':H(b)}
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def write(name,value):
 with open(D/name,'x') as f:json.dump(value,f,indent=2,ensure_ascii=False);f.write('\n')
def extent(root):
 need(root.resolve()==root and stat.S_ISDIR(root.lstat().st_mode),'ordinary root')
 files=[];dirs=[]
 for p in root.rglob('*'):
  mode=p.lstat().st_mode;need(p.resolve()==p and (stat.S_ISREG(mode) or stat.S_ISDIR(mode)),'no symlink or special baseline entry')
  (files if stat.S_ISREG(mode) else dirs).append(p.relative_to(root).as_posix())
 return sorted(files),sorted(dirs)
def git(*args):
 env={k:v for k,v in os.environ.items() if not k.startswith('GIT_')};env['GIT_OPTIONAL_LOCKS']='0'
 need(args[0] in ['rev-parse','symbolic-ref','ls-files','remote','ls-remote','diff'],'read-only targeted Git allowlist')
 argv=['git','-c','gc.auto=0','-c','core.hooksPath=/dev/null','-c','core.fsmonitor=false']+list(args)
 r=subprocess.run(argv,cwd=W,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=60)
 COMMANDS.append({'arguments':list(args) if args[0]!='ls-remote' else ['ls-remote','--refs','EXPLICIT_PUSH_URL_SHA256:'+H(args[2].encode()),'refs/heads/master'],'exit_code':r.returncode,'stdout_bytes':len(r.stdout),'stdout_SHA256':H(r.stdout),'stderr_bytes':len(r.stderr),'stderr_SHA256':H(r.stderr)})
 need(r.returncode==0,'read-only targeted Git failed: '+args[0]);return r.stdout

def parse_index(raw,targets):
 need(raw[:4]==b'DIRC' and len(raw)>=32,'whole native index');version,count=struct.unpack('>II',raw[4:12]);need(version==2 and hashlib.sha1(raw[:-20]).digest()==raw[-20:],'v2 index checksum')
 offset=12;records=[];protected=[];tuples=[];protected_tuples=[];paths=[]
 for _ in range(count):
  start=offset;need(offset+62<len(raw)-20,'whole native header');flags=struct.unpack('>H',raw[start+60:start+62])[0];need(flags&0xF000==0,'native stage0 flags')
  end=raw.find(b'\0',start+62,len(raw)-20);need(end>=0,'native pathname terminator');path=raw[start+62:end];need(path and flags&0xFFF==min(len(path),0xFFF),'native pathname length')
  offset=start+((end+1-start+7)//8)*8;need(raw[end:offset]==b'\0'*(offset-end),'native padding');mode=struct.unpack('>I',raw[start+24:start+28])[0];need(mode in [0o100644,0o100755,0o120000,0o160000],'ordinary native index mode')
  record=raw[start:offset];oid=raw[start+40:start+60].hex();value=('%06o'%mode).encode()+b' '+oid.encode()+b' 0\t'+path;paths.append(path);tuples.append(value);records.append((path,record,mode,oid))
  if path not in targets:protected.append((path,record));protected_tuples.append(value)
 need(paths==sorted(paths) and len(paths)==len(set(paths)),'unique sorted whole index entries');extensions=[]
 while offset<len(raw)-20:
  need(offset+8<=len(raw)-20,'whole extension header');key=raw[offset:offset+4];length=struct.unpack('>I',raw[offset+4:offset+8])[0];offset+=8
  need(key==b'TREE' and offset+length<=len(raw)-20,'only audited complete TREE extension');extensions.append({'type':key.decode(),'bytes':length,'SHA256':H(raw[offset:offset+length])});offset+=length
 need(offset==len(raw)-20 and len(extensions)<=1,'exact native index extent')
 raw_protected=b'\0'.join(p+b'\t'+r.hex().encode() for p,r in protected)+b'\0'
 return {'version':version,'count':count,'records':records,'protected':protected,'tuple_stream':b'\0'.join(tuples)+b'\0','protected_tuple_stream':b'\0'.join(protected_tuples)+b'\0','protected_raw_stream':raw_protected,'extensions':extensions}

class FirstAnchor(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.href=None
 def handle_starttag(self,tag,attrs):
  if tag=='a' and self.href is None:self.href=dict(attrs).get('href')

def node(x):return {'tag':x.tag,'attributes_in_original_order':list(x.attrib.items()),'text':x.text,'tail':x.tail,'children':[node(c) for c in x]}

def main():
 start=now();go_path=P/'verification/root-supported-cycle-focal-actual623-baseline-GO-20261115.json';gb=read(go_path);need(H(gb)=='0d7371f227e608c79d7f79135cb78cecd2fee4e190c7952bebb3afa7c0c639c2','actual separate root623GO');go=json.loads(gb);need(go['independentFreshBaselineCaptureAuthorized'] is True and go['installationOrCanonicalAAAuthority'] is False,'read-only baseline only')
 with open(D/'BASELINE_ACTUAL_GO.json','xb') as f:f.write(gb)
 initial=read(D/'INITIAL_SEAL.json');need(H(initial)=='709ceeaf5c386f2ffd24682a919fd100d51224b4207e43f68c361ab8e4c8b21b','source-only initial remains exact')
 rawroot=D/'inputs/baseline623';rawroot.mkdir();blobs=rawroot/'blobs';blobs.mkdir()
 def snapshot(path,body=None):
  b=read(path) if body is None else body;h=H(b);q=blobs/h
  if not q.exists():
   with open(q,'xb') as f:f.write(b)
  else:need(read(q)==b,'exact reused blob')
  return {'path':str(path),'bytes':len(b),'SHA256':h,'snapshot':{'path':str(q),'bytes':len(b),'SHA256':h}}
 need(git('rev-parse','--show-toplevel').decode().strip()==str(W),'exact website repository');need(git('rev-parse','--show-object-format').strip()==b'sha1','actual SHA1 object format')
 branch=git('symbolic-ref','HEAD').decode().strip();head=git('rev-parse','HEAD').decode().strip();master=git('rev-parse','refs/heads/master').decode().strip();tree=git('rev-parse','HEAD^{tree}').decode().strip()
 need(branch=='refs/heads/master' and head==master==go['actualWebsiteHEAD'] and tree==go['actualWebsiteTree'],'actual local baseline authority identity');need(git('rev-parse','--absolute-git-dir').decode().strip()==str(W/'.git'),'ordinary real website Gitdir')
 gitdir=W/'.git';need(gitdir.resolve()==gitdir and stat.S_ISDIR(gitdir.lstat().st_mode),'actual Gitdir not a link')
 try:(gitdir/'index.lock').lstat()
 except FileNotFoundError:pass
 else:raise RuntimeError('existing index lock: no stable capture')
 raw=read(gitdir/'index');need(H(raw)==go['actualIndexSHA256'],'actual current native index equals root623 GO')
 exp=json.loads(read(D/'EXPECTED_SOURCE_OBJECTS.json'));future=[p for r in exp['records'] for p in r['expected_four_article_root_leaf_paths']]+['research/index.html','research/sitemap.xml'];targets={('public/'+p).encode() for p in future};index=parse_index(raw,targets)
 selected={p for p,r,m,o in index['records'] if p in targets};need(selected=={b'public/research/index.html',b'public/research/sitemap.xml'},'exact current two aggregate targets only; eight new leaves absent')
 ls=git('ls-files','--stage','-z');need(ls==index['tuple_stream'],'full native index agrees with actual stage tuples')
 urls=git('remote','get-url','--push','--all','origin').splitlines();need(len(urls)==1 and urls[0] and b'\0' not in urls[0],'one explicit origin push URL');remote=git('ls-remote','--refs',urls[0].decode(),'refs/heads/master');need(remote.split()==[head.encode(),b'refs/heads/master'],'actual explicit push destination advertisement')
 deletion=git('diff','--cached','--name-only','--diff-filter=D','-z',head)
 git_files=[snapshot(gitdir/n) for n in ['HEAD','refs/heads/master','config']];git_files.append(snapshot(gitdir/'index',raw))
 for n,b in [('native-index.before',raw),('native-index-stage-tuples.z',ls),('protected-native-index.raw-records',index['protected_raw_stream']),('protected-index-stage-tuples.z',index['protected_tuple_stream']),('actual-staged-deletions.z',deletion),('remote-advertisement.stdout',remote)]:
  with open(rawroot/n,'xb') as f:f.write(b)
 public_root=W/'public';files,dirs=extent(public_root);need(len(files)==623,'actual623 whole public namespace');rows=[snapshot(public_root/n) for n in files]
 for r,n in zip(rows,files):r['public_relative_path']=n
 configrows=[snapshot(W/n) for n in ['.firebaserc','firebase.json']]
 html=read(public_root/'research/index.html');scripts=re.findall(rb'<script type="application/ld\+json">\s*(.*?)\s*</script>',html,re.S);need(len(scripts)==1,'one actual index graph');graph=json.loads(scripts[0]);listing=graph['mainEntity'];items=listing['itemListElement'];need(type(listing['numberOfItems']) is int and listing['numberOfItems']==len(items)==94,'actual94 typed index items');need([x['position'] for x in items]==list(range(1,95)),'actual old ordered typed positions')
 cards=re.findall(rb'<li(?:\s[^>]*)?>.*?</li>',html,re.S);need(len(cards)==94,'actual94 whole visible records');visible=[]
 for item,card in zip(items,cards):
  parser=FirstAnchor();parser.feed(card.decode());url=('https://aleckriebel.com'+parser.href) if parser.href and parser.href.startswith('/') else parser.href;need(url==item['url'],'typed/visible whole old record order');visible.append({'first_url':url,'whole_raw_HTML':card.decode()})
 xml=read(public_root/'research/sitemap.xml');xmlroot=ET.fromstring(xml);need(len(xmlroot)==95,'actual95 whole XML nodes');locs=[c.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text for c in xmlroot];need(len(locs)==len(set(locs))==95,'distinct whole old sitemap locations')
 oldset=set(files);need(oldset&set(future)=={'research/index.html','research/sitemap.xml'} and len(oldset-set(future))==621 and len(oldset|set(future))==631,'actual conditional future eight new leaves two aggregates')
 protected=json.loads(read(D/'inputs/23578142/editorial/PROTECTED_INPUTS.json'));expected_core={r['path']:r for r in protected['files'] if r['path'] in protected['core_files']};need(len(expected_core)==18,'qualified18 current core descriptors')
 corerows=[]
 for name in protected['core_files']:
  row=expected_core[name];body=read(name);need(len(body)==row['bytes'] and H(body)==row['SHA256'],'qualified core full bytes');corerows.append(snapshot(Path(name),body))
 checkpoint=next(r for r in corerows if r['path'].endswith('/checkpoint_subtree.py'));need(checkpoint['SHA256']=='405b0357fd20a2e14893ce6c3c1a0f81910894ccd8ffaddac4e25014138fb9c0','sole authorized405b checkpoint')
 scripts_ns=sorted(str(p) for p in (P/'scripts').glob('*.py'));need(scripts_ns==sorted(p for p in protected['core_files'] if str(Path(p).parent)==str(P/'scripts')),'exact current17-script namespace')
 need(extent(public_root)==(files,dirs),'public namespace unchanged during capture')
 for r in rows+configrows+git_files+corerows:need(read(r['path'])==read(r['snapshot']['path']),'complete baseline bytes unchanged across capture window')
 need(git('rev-parse','HEAD').decode().strip()==head and git('rev-parse','refs/heads/master').decode().strip()==head and git('symbolic-ref','HEAD').decode().strip()==branch,'local reference unchanged during capture');remote_end=git('ls-remote','--refs',urls[0].decode(),'refs/heads/master');need(remote_end==remote,'explicit remote advertisement unchanged across capture')
 write('ACTUAL623_PUBLIC_BASELINE.json',{'schema':'independent-fresh-actual623-public-config-baseline-v1','capture_start_UTC':start,'capture_end_UTC':now(),'root_GO_SHA256':H(gb),'source_only_INITIAL_SHA256':H(initial),'HEAD':head,'tree':tree,'branch':'master','counts':[623,94,95],'public_namespace':files,'public_directories':dirs,'public_files':rows,'site_configs':configrows,'expected_future_paths':future,'conditional_proposal_counts':[631,96,97],'unrelated_public_paths':621,'actual_baseline_verified_before_writer_exposure':True,'writer_exposed':False,'publication_authority':False})
 write('ACTUAL623_AGGREGATE_OBJECTS.json',{'schema':'independent-actual623-whole-ordered-aggregate-objects-v1','whole_index_JSON_graph':graph,'whole_visible_records_in_original_order':visible,'whole_XML_root':node(xmlroot),'whole_XML_nodes_in_original_order':[node(c) for c in xmlroot],'whole_XML_location_order':locs,'complete_raw_aggregates_snapshotted_in_public_baseline':True,'counts':[94,95]})
 write('ACTUAL623_GIT_OBSERVATIONS.json',{'schema':'independent-fresh-actual623-full-native-index-Git-observation-v1','UTC':now(),'website_root':str(W),'HEAD':head,'master':master,'tree':tree,'branch':'master','Git_control_files':git_files,'actual_whole_index_SHA256':H(raw),'actual_whole_index_bytes':len(raw),'all_native_index_record_count':index['count'],'fresh_exact_future10_target_set':sorted(p.decode() for p in targets),'fresh_protected_raw_native_record_count':len(index['protected']),'fresh_protected_raw_native_stream':pin(rawroot/'protected-native-index.raw-records'),'whole_native_index_snapshot':pin(rawroot/'native-index.before'),'actual_stage_tuple_stream':pin(rawroot/'native-index-stage-tuples.z'),'protected_stage_tuple_stream':pin(rawroot/'protected-index-stage-tuples.z'),'actual_native_extensions':index['extensions'],'origin_push_URL_SHA256':H(urls[0]),'actual_remote_master':head,'actual_remote_advertisement':remote.decode(),'actual_cached_deletion_count':len([x for x in deletion.split(b'\0') if x]),'actual_cached_deletions':pin(rawroot/'actual-staged-deletions.z'),'actual_read_only_commands':COMMANDS,'all_complete_raw_record_bytes_including_stat_flags_mode_OID_path_padding_protected':True,'Git_or_remote_mutations':False,'global_status_or_add_reset_clean_checkout_run':False})
 write('ACTUAL623_QUALIFIED_CORE.json',{'schema':'independent-actual-qualified17-plus405b-core-v1','UTC':now(),'original17_plus_sole_authorized405b_checkpoint':True,'all18_original_unchanged_claim':False,'qualification':protected['core_qualification'],'files':corerows,'actual_complete_scripts_namespace':scripts_ns,'actual_checkpoint_SHA256':checkpoint['SHA256'],'source_or_core_programmes_executed':False})
 print(json.dumps({'status':'PASS_FRESH_INDEPENDENT_ACTUAL623_BASELINE_BEFORE_WRITER_EXPOSURE','HEAD':head,'tree':tree,'counts':[623,94,95],'conditional_proposal':[631,96,97],'unrelated_public_paths':621,'actual_native_index_records':index['count'],'fresh_protected_full_native_records':len(index['protected']),'actual_index_SHA256':H(raw),'actual_cached_deletion_count':len([x for x in deletion.split(b'\0') if x]),'qualified_original17_plus405b':True,'actual_read_only_Git_commands':len(COMMANDS),'writer_exposed':False,'production_or_publication_authority':False},indent=2))
if __name__=='__main__':main()
