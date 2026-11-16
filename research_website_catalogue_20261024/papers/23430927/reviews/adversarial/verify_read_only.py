"""Final bounded custody only, never a scientific/native replay.

Reads this exact owned extent, frozen701-file source, explicitly handed raw
references and qualified core pins. No subprocess, project import, network/write.
"""
from pathlib import Path
import hashlib,json,stat,sys
D=Path(__file__).resolve().parent
B=D.parents[3]
S=D.parent.parent/'sources'
COUNT=0;TYPED=0
EXTERNAL=set()
def need(ok,label):
 global COUNT
 COUNT+=1
 if not ok:raise RuntimeError(label)
def read(p):
 p=Path(p)
 need(p.is_absolute() and p.resolve()==p,'ordinary absolute path')
 need(p.is_relative_to(D) or p.is_relative_to(S) or str(p) in EXTERNAL,'bounded input path')
 need(stat.S_ISREG(p.lstat().st_mode),'ordinary file no symlink/special')
 return p.read_bytes()
def pairs(rows):
 r={}
 for k,v in rows:need(k not in r,'duplicate JSON key');r[k]=v
 return r
def obj(p):return json.loads(read(p),object_pairs_hook=pairs)
def pin(b):return {'bytes':len(b),'SHA256':hashlib.sha256(b).hexdigest()}
def match(p,r):need(pin(read(p))=={k:r[k] for k in ['bytes','SHA256']},'whole unchanged buffer '+str(p))
def lex(xs):need(len(xs)==len(set(xs)),'duplicate full relative identities');return sorted(xs)
def extent(root):
 root=Path(root);need(root.resolve()==root and stat.S_ISDIR(root.lstat().st_mode),'ordinary extent root')
 fs=[];ds=[]
 for p in root.rglob('*'):
  n=p.relative_to(root).as_posix();need(p.resolve()==p,'no escaped entry')
  if stat.S_ISDIR(p.lstat().st_mode):ds.append(n)
  else:need(stat.S_ISREG(p.lstat().st_mode),'ordinary extent entry');fs.append(n)
 return lex(fs),lex(ds)
def exact(root,files,dirs):
 fs,ds=extent(root)
 need(fs==lex(list(files)) and ds==lex(dirs),'full exact file/directory identity')
 for n,r in files.items():match(Path(root)/n,r)
 return fs,ds
def typed(a,b):
 global TYPED
 TYPED+=1;need(type(a) is type(b),'recursive exact type')
 if isinstance(a,dict):
  need(list(a)==list(b),'whole ordered key interface')
  for k in a:typed(a[k],b[k])
 elif isinstance(a,list):
  need(len(a)==len(b),'whole ordered list interface')
  for x,y in zip(a,b):typed(x,y)
 else:need(a==b,'whole scalar interface')

need(D==B/'papers/23430927/reviews/adversarial','fixed own root')
need(sys.argv[1:] in [[],['--preseal']],'safe exact invocation')
initial=obj(D/'INITIAL_SEAL.json')
match(D/'INITIAL_SEAL.json',{'bytes':1965,'SHA256':'3420befb7a6cf6e351adf4da6bd4f61de2859aa287b9598ca41551414b8d1c58'})
match(D/'INITIAL_MANIFEST.json',initial['manifest'])
im=obj(D/'INITIAL_MANIFEST.json')
need(im['exact_root_terminal_exclusions']==['INITIAL_MANIFEST.json','INITIAL_SEAL.json'] and im['future_subtree_exclusions']==[],'initial exact finite terminals')
for n,r in im['files'].items():match(D/n,r)
results=obj(D/'OWN_PROOF_CONTROL_SEAL.json')
match(D/'OWN_PROOF_CONTROL_SEAL.json',{'bytes':1358,'SHA256':'2fbe9ab77f928d2e1b44b5867109daa886360c14b4b2558e5fa9e4ab03811840'})
match(D/'OWN_PROOF_CONTROL_MANIFEST.json',results['manifest'])
rm=obj(D/'OWN_PROOF_CONTROL_MANIFEST.json')
need(rm['exact_root_terminal_exclusions']==['OWN_PROOF_CONTROL_MANIFEST.json','OWN_PROOF_CONTROL_SEAL.json'] and rm['future_subtree_exclusions']==[],'results exact finite terminals')
for n,r in rm['files'].items():match(D/n,r)
need(results['no_supporting_code_results_README_archived_opinions_current_peer_bodies_new_foreign_math'] is True,'pre-exposure results chronology')
ref=obj(D/'SOURCE_REFERENCE_EXTENT.json');need(ref['root']==str(S),'fixed source root')
sf,sd=exact(S,ref['files'],ref['directories'])
need([len(sf),len(sd)]==[701,119],'original701files119dirs')
match(S/'SOURCE_READY_SEAL.json',ref['source_FINAL'])
ready=obj(S/'SOURCE_READY.json');source_seal=obj(S/'SOURCE_READY_SEAL.json')
need(pin(read(S/'SOURCE_READY.json'))['SHA256']==source_seal['SOURCE_READY_SHA256'],'whole original READY binding')
need(ready['source_scientific_proofs_code_results_triage_reviews_or_opinions_read'] is False and ready['scientific_verdict'] is None and ready['publication_authority'] is False,'original historical unread null/false flags')
need(ready['version_field_present'] is True and ready['version']=='1.0','actual original edition')
need(len(ref['five_separately_preserved_TeX_occurrences'])==5,'five distinct current/historical occurrences')
for r in ref['five_separately_preserved_TeX_occurrences']:match(r['extracted_path'],r)
core=obj(S/'QUALIFIED_CORE_BINDINGS.json')
need(core['original17_plus_sole_authorized405b'] is True and core['all18_original_unchanged_claim'] is False and core['global_cache_Git_HEAD_index_constraints'] is False,'qualified17 plus sole405b, no broad freeze')
need(len(core['files'])==18 and len(set(x['path'] for x in core['files']))==18,'exact18 qualified paths')
for r in [core['reference'],*core['files']]:EXTERNAL.add(r['path']);match(r['path'],r)
need(sum(r['SHA256']=='405b0357fd20a2e14893ce6c3c1a0f81910894ccd8ffaddac4e25014138fb9c0' for r in core['files'])==1,'sole authorized405b')

h=obj(D/'RAW_PRIMARY_HANDOFF_01.copy.json')
match(D/'RAW_PRIMARY_HANDOFF_01.copy.json',{'bytes':16170,'SHA256':'d611b86b851385d9f05523b0acb126b335f935ae6fdce0fb0dd001c4bd674236'})
handoff=D.parent/'scope/RAW_PRIMARY_HANDOFF_01.json';EXTERNAL.add(str(handoff))
need(read(handoff)==read(D/'RAW_PRIMARY_HANDOFF_01.copy.json'),'whole literal raw-only original handoff')
authority=B/'verification/root-primary-acquisition-23430927-20261115.json'
need(h['root_authority']['path']==str(authority),'fixed raw authority path');EXTERNAL.add(str(authority));match(authority,h['root_authority'])
typed(obj(authority),h['whole_literal_root_authority'])
need(len(h['records'])==9 and h['new_GETs']==0 and h['root_gate']=='CLOSED','raw-only cached nine bodies')
for r in h['records']:
 need(r['fresh_GET'] is False,'no new raw acquisition here')
 for name in ['whole_original_raw_body','available_legacy_transport_container']:
  x=r[name];EXTERNAL.add(x['path']);match(x['path'],x)
for r in h['legacy_access_limits']:
 need(r['whole_failed_response_body'] is None and r['current_access_claim'] is None and r['fresh_GET'] is False,'literal legacy access limits')

native=obj(D/'NATIVE_PRIVATE_COPY_MANIFEST.json')
need(native['source_root']==str(S/'published-source/asset-002/verification_kit') and native['private_root']==str(D/'native/verification_kit'),'fixed current native copy roots')
nf,nd=exact(D/'native/verification_kit',native['files'],native['directories'])
need([len(nf),len(nd)]==[299,56],'private whole299file56dirkit')
for n,r in native['files'].items():match(Path(native['source_root'])/n,r)
need(extent(D/'native/scratch')==([],[]),'native owned scratch removed')
expected=read(D/'NATIVE_EXPECTED.stdout.json')
for m in ['normal','optimized']:
 raw=read(D/('NATIVE_'+m+'.stdout.json'))
 need(raw==expected and read(D/('NATIVE_'+m+'.stderr'))==b'','whole literal expected normal/O streams')
 typed(json.loads(raw,object_pairs_hook=pairs),json.loads(expected,object_pairs_hook=pairs))
tool=obj(D/'NATIVE_TOOL_RESULTS.json')
need(tool['normal']['exit_code']==0 and tool['optimized']['exit_code']==0,'both actual native exits')
v=obj(D/'VERDICT.json')
need(v['root144_gate']=='CLOSED' and v['root_adoption'] is False and v['production_authority'] is False and v['follow_up'] is None,'no adoption/publication/followup authority')

fs,ds=extent(D)
if sys.argv[1:]:
 pre=obj(D/'PRESEAL_NAMESPACE.json')
 need(fs==lex(pre['files']) and ds==lex(pre['directories']),'exact preseal own file/directory identities')
else:
 seal=obj(D/'FINAL_SEAL.json');manifest=obj(D/'FINAL_MANIFEST.json')
 match(D/'FINAL_MANIFEST.json',seal['manifest'])
 terminals=['FINAL_MANIFEST.json','FINAL_SEAL.json']
 need(seal['exact_root_terminal_exclusions']==terminals and seal['future_subtree_exclusions']==[],'two exact root final exclusions only')
 need(fs==lex(list(manifest['files'])+terminals) and ds==lex(manifest['directories']),'strict final entire owned finite extent')
 for n,r in manifest['files'].items():match(D/n,r)
 need(len(fs)==seal['actual_files'] and len(ds)==seal['directory_count'],'literal actual final counts')
print(json.dumps({'status':'PASS_BOUNDED_ADVERSARIAL_CUSTODY_ONLY','checks':COUNT,'recursive_typed_nodes':TYPED,'source_files':701,'source_directories':119,'private_native_files':299,'private_native_directories':56,'raw_PDF_references':9,'initial_results_unchanged':True,'literal_native_normal_O_whole_expected_equal':True,'root144_gate':'CLOSED','root_adoption':False,'production_authority':False,'follow_up':None,'scientific_native_network_subprocess_execution':False,'writes':0,'mode':'preseal' if sys.argv[1:] else 'strict_default'}))
