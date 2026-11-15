"""Read-only exact14 fences plus narrowly scoped primitives used only after root authority."""
from pathlib import Path,PurePosixPath
from datetime import datetime,timezone
import hashlib,json,os,re,struct,subprocess,xml.etree.ElementTree as ET
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
W=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
S=P/'verification/nash-quotient-robinson-private-stage-sol-20261115'
O=Path(__file__).resolve().parent
BASE='e2e064c48755452a56c2a31207fb12d7e55074fb'
STAGE_SEAL='e0bb4ec8ae90cf48e0d71f9e66b723f65403d743610d5477916f7dda6a6a00e9'
CHECKPOINT='405b0357fd20a2e14893ce6c3c1a0f81910894ccd8ffaddac4e25014138fb9c0'
AUDIT=P/'verification/nash-quotient-robinson-independent-code-audit-sol-20261115/SEAL.json'
AUDIT_SEAL='d0e0c037b29c5bef4b0466079f2667cfa7a17fffdee2ed4092aedcf0bad62f5e'
ADOPTION=P/'verification/root-nash-quotient-robinson-stage-adoption-20261115.json'
COMMIT_APPROVAL=P/'verification/root-nash-quotient-robinson-commit-approval-20261115.json'
AGGREGATES={'research/index.html','research/sitemap.xml'}
CODE_FILES=['exact14_lib.py','preflight.py','install_exact.py','hooks/pre-push']
def need(ok,why):
 if not ok:raise RuntimeError(why)
def now():return datetime.now(timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):
 p=Path(p);need(p.is_file()and not p.is_symlink(),'regular nonsymlink '+str(p));return p.read_bytes()
def obj(p):return json.loads(read(p))
def pin(p,row):
 b=read(p);need(len(b)==row['bytes']and sha(b)==row['SHA256'],'whole-byte pin '+str(p));return b
def safe_rel(s):
 p=PurePosixPath(s);need(not p.is_absolute()and '..'not in p.parts and str(p)==s and '\\'not in s,'safe relative path');return p
def namespace(root):
 paths=list(root.rglob('*'));need(not root.is_symlink()and not any(p.is_symlink()for p in paths),'namespace nonsymlink '+str(root));return sorted(p.relative_to(root).as_posix()for p in paths if p.is_file())
def git(*args,index=None,data=None,mutating=False,guard_commit=None,guard_remote_sha=None):
 # Strip inherited Git environment routing/config injection. No optional shared-index refresh.
 env={k:v for k,v in os.environ.items()if not k.startswith('GIT_')}
 env.update(GIT_OPTIONAL_LOCKS='0')
 if index is not None:env['GIT_INDEX_FILE']=str(index)
 if guard_commit is not None:
  need(args and args[0]=='push'and re.fullmatch('[0-9a-f]{40}',guard_commit)and re.fullmatch('[0-9a-f]{64}',guard_remote_sha or''),'approved push-guard parameters')
  need(namespace(O/'hooks')==['pre-push'],'sole controlled pre-push hook')
  hook=O/'hooks/pre-push';read(hook);need(hook.stat().st_mode&0o7777==0o555 and os.access(hook,os.X_OK),'required executable read-only0555 push guard')
  env['EXACT14_APPROVED_COMMIT']=guard_commit;env['EXACT14_APPROVED_PUSH_URL_SHA256']=guard_remote_sha
 command=['git','-c','gc.auto=0','-c','core.hooksPath=/dev/null','-c','core.fsmonitor=false','-c','commit.gpgsign=false','-c','push.followTags=false','-c','remote.origin.mirror=false']
 if guard_commit is not None:command+=['-c','core.hooksPath='+str(O/'hooks')]
 command+=list(args)
 allowed_read={'rev-parse','symbolic-ref','ls-files','ls-remote','remote','diff','diff-tree','cat-file','ls-tree','config'}
 need(mutating or(args and args[0]in allowed_read),'Git write requires explicit mutated-phase primitive')
 r=subprocess.run(command,cwd=W,env=env,input=data,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=90)
 need(r.returncode==0,'Git '+args[0]+' failed: '+r.stderr.decode('utf-8','replace')[-1500:]);return r.stdout

def parse_index(raw,targets):
 need(raw[:4]==b'DIRC'and len(raw)>=32,'DIRC index')
 version,count=struct.unpack('>II',raw[4:12]);need(version==2,'Only audited v2 index is supported')
 need(hashlib.sha1(raw[:-20]).digest()==raw[-20:],'whole index SHA1 checksum')
 offset=12;entries=[];protected=[];paths=[]
 for _ in range(count):
  start=offset;need(offset+62<len(raw)-20,'whole v2 entry header');flags=struct.unpack('>H',raw[offset+60:offset+62])[0]
  need(flags&0xF000==0,'No extended/assume-valid/unmerged index flags')
  end=raw.find(b'\0',offset+62,len(raw)-20);need(end>=0,'whole path terminator');path=raw[offset+62:end]
  need(path and (flags&0xFFF)==min(len(path),0xFFF),'actual v2 pathname length')
  length=((end+1-start+7)//8)*8;offset=start+length;need(raw[end:offset]==b'\0'*(offset-end),'native zero v2 entry padding')
  mode=struct.unpack('>I',raw[start+24:start+28])[0];need(mode in[0o100644,0o100755,0o120000,0o160000],'audited native index mode')
  record=raw[start:offset];entries.append((path,record,mode,raw[start+40:start+60].hex()));paths.append(path)
  if path not in targets:protected.append((path,record))
 need(paths==sorted(paths)and len(paths)==len(set(paths)),'unique byte-sorted v2 stage0 paths')
 extensions=[]
 while offset<len(raw)-20:
  need(offset+8<=len(raw)-20,'whole index extension header');key=raw[offset:offset+4];length=struct.unpack('>I',raw[offset+4:offset+8])[0];offset+=8
  need(offset+length<=len(raw)-20,'whole index extension payload');body=raw[offset:offset+length];offset+=length
  need(key==b'TREE','Only actual audited TREE cache extension is supported')
  extensions.append((key,body))
 need(offset==len(raw)-20 and len(extensions)<=1,'exact v2 extent and sole TREE extension')
 records=b'\0'.join(path+b'\t'+record.hex().encode()for path,record in protected)+b'\0'
 return{'version':version,'count':count,'entries':entries,'protected':protected,'protected_record_count':len(protected),'protected_raw_records_SHA256':sha(records),'whole_index_SHA256':sha(raw),'extensions':[(k.decode(),len(b),sha(b))for k,b in extensions]}

def stage_fences(mode):
 need(mode in['baseline','installed'],'bounded website state')
 need(sha(read(S/'FINAL_SEAL.json'))==STAGE_SEAL,'exact sealed writer stage')
 seal=obj(S/'FINAL_SEAL.json');need(sha(read(S/'OWNED_MANIFEST.json'))==seal['owned_manifest_SHA256'],'stage owned manifest seal')
 owned=obj(S/'OWNED_MANIFEST.json');rows=owned['files'];names=[r['path']for r in rows]
 need(set(owned['exact_root_terminal_exclusions_only'])=={'OWNED_MANIFEST.json','FINAL_SEAL.json'},'stage exact terminal exclusions')
 need(len(names)==len(set(names))==seal['owned_payload_count']==1599,'stage complete1599 owned payloads')
 need(set(namespace(S))-{'OWNED_MANIFEST.json','FINAL_SEAL.json'}==set(names),'whole sealed stage namespace')
 for row in rows:pin(S/safe_rel(row['path']),row)
 for name,h in seal['critical_files_SHA256'].items():need(sha(read(S/safe_rel(name)))==h,'stage critical pin '+name)
 contract=obj(S/'STAGE_CONTRACT.json');overlay=obj(S/'OVERLAY_MANIFEST.json')['files'];paths=[r['path']for r in overlay]
 need(len(paths)==len(set(paths))==14 and paths==contract['overlay_paths'],'exact14 ordered overlay')
 need(contract['GO_website_commit']==BASE and contract['baseline_counts']==[593,87,88]and contract['virtual_counts']==[605,90,91],'stage actual baseline and candidate counts')
 need({r['path']for r in overlay if r['action']=='replace_aggregate_only'}==AGGREGATES and sum(r['action']=='add_new_leaf'for r in overlay)==12,'only12new and2aggregate changes')
 need(all(safe_rel(p).as_posix().startswith('research/')for p in paths),'public research-only scope')
 for row in overlay:
  b=pin(S/'candidate-a/public'/row['path'],row);need(b==pin(S/'candidate-b/public'/row['path'],row),'whole paired stage payload')
 for candidate in ['candidate-a','candidate-b']:need(namespace(S/candidate/'public')==paths,'exact14 candidate namespace')
 plan=obj(S/'INSTALLATION_PLAN.json');need([r['path']for r in plan['files']]==paths,'exact installation plan order')
 for a,b in zip(overlay,plan['files']):need(all(a[k]==b[k]for k in ['path','bytes','SHA256','action'])and b['destination']==str(W/'public'/a['path']),'installation row exact destination')
 external=obj(S/'INPUT_MANIFEST.json')['files'];allowed_changed={str(W/'public'/p)for p in paths}if mode=='installed'else set()
 for row in external:
  raw=pin(S/safe_rel(row['blob']),row)
  if row['path']not in allowed_changed:need(read(Path(row['path']))==raw,'whole current external input '+row['path'])
 source=obj(S/'SOURCE_INPUTS.json')
 for n in source['namespaces']:need([str(Path(n['root'])/p)for p in namespace(Path(n['root']))]==n['files']and len(n['files'])==n['count'],'entire preserved source/review namespace')
 core=obj(S/'CORE_INPUTS.json');need(len(core['files'])==18 and core['original17_files_unchanged']==17 and core['historical_qualification_preserved']is True and core['claim_all18_unchanged_from_original_baseline']is False,'qualified17original plus1authorized core')
 need(core['current_checkpoint_SHA256']==CHECKPOINT and core['authorized_changed_checkpoint_whole_supplement']['authorized_current_SHA256']==CHECKPOINT,'exact authorized405b supplement')
 old={r['path']:r for r in core['original_core_file_bindings']};need(len(old)==18,'complete original core fence')
 for row in core['files']:
  pin(Path(row['path']),row)
  if row['path']==str(P/'scripts/checkpoint_subtree.py'):need(row['SHA256']==CHECKPOINT and row['bytes']==6213,'only qualified checkpoint')
  else:need(row['SHA256']==old[row['path']]['SHA256']and row['bytes']==old[row['path']]['bytes'],'original17 exact')
 need(sorted(str(p)for p in(P/'scripts').glob('*.py'))==core['scripts_namespace'],'complete17-script namespace')
 base=obj(S/'WEBSITE_BASELINE.json');need(base['root_GO_commit']==BASE and [base['public_count'],base['index_count'],base['sitemap_count']]==[593,87,88],'actual sealed website baseline')
 for row in base['site_configs']:pin(Path(row['path']),row)
 oldpaths={str(Path(r['path']).relative_to(W/'public'))for r in base['public_files']};need(len(oldpaths)==593 and oldpaths&set(paths)==AGGREGATES,'complete593 baseline and2 existing targets')
 expected=oldpaths if mode=='baseline'else oldpaths|set(paths);need(set(namespace(W/'public'))==expected,'whole actual public namespace')
 for row in base['public_files']:
  rel=str(Path(row['path']).relative_to(W/'public'))
  if mode=='baseline'or rel not in paths:pin(Path(row['path']),row)
 if mode=='baseline':
  for row in overlay:
   if row['action']=='add_new_leaf':need(not(W/'public'/row['path']).exists(),'new leaf absent')
 else:
  for row in overlay:pin(W/'public'/row['path'],row)
 index_text=read(W/'public/research/index.html').decode();matches=re.findall(r'<script type="application/ld\+json">\s*(.*?)\s*</script>',index_text,re.S);need(len(matches)==1,'actual single research index graph')
 listing=json.loads(matches[0])['mainEntity'];index_count=87 if mode=='baseline'else 90;sitemap_count=88 if mode=='baseline'else 91
 need(listing['numberOfItems']==len(listing['itemListElement'])==index_count,'actual ordered research index count')
 need(len(ET.fromstring(read(W/'public/research/sitemap.xml')))==sitemap_count,'actual research sitemap count')
 virtual_old=oldpaths|set(paths);need(len(virtual_old)==605,'exact605 union')
 candidate=json.loads(re.findall(r'<script type="application/ld\+json">\s*(.*?)\s*</script>',read(S/'candidate-a/public/research/index.html').decode(),re.S)[0])['mainEntity']
 need(candidate['numberOfItems']==len(candidate['itemListElement'])==90 and len(ET.fromstring(read(S/'candidate-a/public/research/sitemap.xml')))==91,'actual candidate90/91')
 return overlay,{'stage_owned':len(rows),'external_input_bindings':len(external),'core_original':17,'core_qualified':1,'public':len(expected),'index':index_count,'sitemap':sitemap_count,'candidate_counts':[605,90,91]}

def website_git_state(overlay,head=BASE,remote=True):
 need(git('rev-parse','--show-toplevel').decode().strip()==str(W),'exact website repository root')
 need(git('rev-parse','--show-object-format').strip()==b'sha1','audited SHA1 repository')
 need(git('symbolic-ref','HEAD').strip()==b'refs/heads/master'and git('rev-parse','HEAD').decode().strip()==head,'existing master and exact parent')
 gitdir=Path(git('rev-parse','--absolute-git-dir').decode().strip());need(gitdir==W/'.git'and gitdir.is_dir()and not gitdir.is_symlink(),'audited ordinary local Gitdir')
 need(not(gitdir/'index.lock').exists(),'no index lock exists')
 # Index parser itself rejects sparse/split index extensions and every nonzero high entry flag.
 targets={('public/'+r['path']).encode()for r in overlay};raw=read(gitdir/'index');index=parse_index(raw,targets)
 stage=git('ls-files','--stage','-z');records=[r for r in stage.split(b'\0')if r];need(len(records)==index['count'],'whole ls-files/native index coverage')
 parsed=[]
 for path,record,mode,oid in index['entries']:parsed.append(('%06o'%mode).encode()+b' '+oid.encode()+b' 0\t'+path)
 need(records==parsed,'complete raw index/ls-files identity')
 protected=[r for r in records if r.split(b'\t',1)[1]not in targets];index['protected_stage_tuple_SHA256']=sha(b'\0'.join(protected)+b'\0')
 urls=git('remote','get-url','--push','--all','origin').splitlines();need(len(urls)==1,'one explicit origin push URL only')
 if remote:
  refs=git('ls-remote','origin','refs/heads/master').splitlines();need(len(refs)==1 and refs[0].split()==[BASE.encode(),b'refs/heads/master'],'actual remote parent baseline')
 return raw,index,{'HEAD':head,'branch':'master','gitdir':str(gitdir),'index_SHA256':index['whole_index_SHA256'],'index_record_count':index['count'],'protected_record_count':index['protected_record_count'],'protected_raw_records_SHA256':index['protected_raw_records_SHA256'],'protected_stage_tuple_SHA256':index['protected_stage_tuple_SHA256'],'index_extensions':index['extensions'],'origin_push_URL_SHA256':sha(urls[0]),'remote_master_checked':remote,'remote_master':BASE if remote else None}

def verify_preparation():
 seal=obj(O/'PREPARATION_SEAL.json');need(sha(read(O/'PREPARATION_MANIFEST.json'))==seal['MANIFEST_SHA256'],'preparation manifest seal')
 manifest=obj(O/'PREPARATION_MANIFEST.json');excluded={'PREPARATION_MANIFEST.json','PREPARATION_SEAL.json','PREPARATION_CLOSURE.json'}
 actual={p for p in namespace(O)if not p.startswith('run-state/')and p not in excluded};need(actual=={r['path']for r in manifest['files']},'complete sealed preparation namespace')
 for row in manifest['files']:pin(O/safe_rel(row['path']),row)
 return seal

def root_adoption(expected_sha):
 # This function performs reads only and is always called before any mutation.
 need(re.fullmatch('[0-9a-f]{64}',expected_sha or'')is not None,'explicit root receipt SHA256 is required')
 need(ADOPTION.exists(),'ROOT_ADOPTION_MISSING: no mutation permitted')
 adoption_bytes=read(ADOPTION);need(sha(adoption_bytes)==expected_sha,'exact root adoption receipt hash')
 a=json.loads(adoption_bytes);need(a.get('root_stage_adopted')is True,'root explicit stage adoption')
 message=a.get('commit_message');need(isinstance(message,str)and 0<len(message)<=300 and '\x00'not in message,'root explicit bounded commit message before any mutation')
 need(a['schema']=='root_exact14_production_adoption_v1'and a['authority']=='root','root explicit adoption schema')
 need(a['stage_root']==str(S)and a['stage_final_seal_SHA256']==STAGE_SEAL,'root adopted exact writer stage')
 need(a['independent_code_audit_adopted']is True and a['complete_current_helper_and_rendered_output_adopted']is True and a['production_install_authorized']is True,'root adoption and separate installation authority')
 need(a['website_root']==str(W)and a['website_HEAD']==BASE and a['website_branch']=='master'and a['baseline_counts']==[593,87,88]and a['candidate_counts']==[605,90,91],'root exact actual baseline adoption')
 need(a['preparation_final_seal_SHA256']==sha(read(O/'PREPARATION_SEAL.json')),'root adopted exact preparation seal')
 verify_preparation()
 for name in CODE_FILES:need(a['code_files_SHA256'][name]==sha(read(O/name)),'root full code-body adoption '+name)
 audit=Path(a['independent_audit_final_seal_path']);need(audit==AUDIT and a['independent_audit_final_seal_SHA256']==AUDIT_SEAL and sha(read(audit))==AUDIT_SEAL,'exact actual independent audit SEAL.json and d0e0 pin adopted')
 need(a['hook_mode_octal']=='0555'and (O/'hooks/pre-push').stat().st_mode&0o7777==0o555,'root adopted executable read-only0555 guard mode')
 need(a['public_relative_paths']==[r['path']for r in obj(S/'OVERLAY_MANIFEST.json')['files']],'root exact14 path order')
 capture=obj(O/'PREFLIGHT_CAPTURE.json');need(a['preflight_capture_SHA256']==sha(read(O/'PREFLIGHT_CAPTURE.json'))and a['index_SHA256']==capture['Git']['index_SHA256']and a['protected_raw_records_SHA256']==capture['Git']['protected_raw_records_SHA256'],'root exact fresh shared-index protection adoption')
 return a
