"""Independent pure source adversary controls, not operational approval.
No high-level helper entry point, transport, lock, current-file writer or Git is invoked.
Fixtures are in-memory objects only; stdout is the sole output of this script.
"""
import sys
assert sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode and sys.flags.safe_path and not sys.flags.optimize
import ast,copy,datetime,hashlib,itertools,json,os,stat,types
from pathlib import Path
HERE=Path(__file__).absolute().parent
CASE=HERE.parent
L=CASE/'logical_capture_preparation_02'
E=CASE/'operational_source_preparation_01'
EXPECTED={'bytes':42168,'sha256':'313a9fdfeb37407f94a5950ab91120e52850b85acb178d1f7a83e5bef8851a3b'}
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def load(name,p):
 raw=p.read_bytes();m=types.ModuleType(name);m.__file__=str(p);exec(compile(raw,str(p),'exec'),m.__dict__);return m
source=(L/'capture_logical_packet.py').read_bytes()
assert pin(source)==EXPECTED
cap=load('independent_source_subject',L/'capture_logical_packet.py')
h=load('independent_frozen_model',E/'native239_model.py')
c=load('independent_frozen_tree_core',E/'native_trees_readonly.py')
results=[]
def good(name,fn):
 v=fn()
 assert v is not False,name
 results.append({'name':name,'result':'PASS'})
def bad(name,fn):
 try:fn()
 except (RuntimeError,ValueError,TypeError,KeyError,IndexError,UnicodeError,AttributeError,OverflowError) as error:
  results.append({'name':name,'result':'EXPECTED_REFUSAL','exception':type(error).__name__});return
 raise AssertionError('Unexpected acceptance: '+name)
def trap(*args,**kwargs):raise AssertionError('Forbidden high-level/effect entry point called')
for n in ('capture','finalize','source_guard','Output','GET','helpers','main'):
 setattr(cap,n,trap)
for base,schema,count in ((L,'pr239-logical-capture-source-manifest-v1',10),(E,'pr239-completion-source-manifest-v1',19)):
 manifest=(base/'SOURCE_MANIFEST.json').read_bytes();value=json.loads(manifest)
 good('source closure schema/count '+base.name,lambda:value['schema']==schema and len(value['files'])==count)
 total=0
 for row in value['files']:
  p=base/row['path'];b=p.read_bytes();total+=len(b)
  good('source closure readonly canonical pin '+base.name+'/'+row['path'],lambda p=p,b=b,row=row:p.resolve()==p and stat.S_ISREG(p.stat().st_mode) and stat.S_IMODE(p.stat().st_mode)==0o444 and pin(b)=={k:row[k] for k in ('bytes','sha256')})
 good('source closure exact total '+base.name,lambda:total==value['total_bytes'])
seal=json.loads((L/'EXTERNAL_SEAL.json').read_bytes())
good('helper manifest externally sealed',lambda:seal['source_manifest']=={'path':'SOURCE_MANIFEST.json',**pin((L/'SOURCE_MANIFEST.json').read_bytes())})
# Fresh opaque state. The sentinel child is not in saved at all.
def make_tree(flat):
 saved={}
 trie={}
 for path,entry in flat.items():
  node=trie;parts=path.split('/')
  for name in parts[:-1]:node=node.setdefault(name,{})
  node[parts[-1]]=entry
 def walk(node):
  entries={name:(('040000','tree',walk(value)) if type(value) is dict else value) for name,value in node.items()}
  oid=c.tree_hash([(name,*value) for name,value in entries.items()]);saved[oid]=entries;return oid
 return walk(trie),saved
def replay(saved):
 ts=cap.authenticated_tree_replay(h,c,saved);calls=[];inner=ts.api
 def observe(method,route,body=None):
  calls.append((method,route));return inner(method,route,body)
 ts.api=observe;return ts,calls
opaque='a'*40
root,saved=make_tree({h.ATTEMPT:('040000','tree',opaque),'foreign':('040000','tree','f'*40)})
ts,calls=replay(saved)
good('F01 no opaque child fixture exists',lambda:opaque not in saved)
good('F01 fresh empty overlay returns opaque tuple',lambda:cap.projected_attempt(h,c,ts,root,{}, {})==('040000','tree',opaque))
good('F01 only three ancestor envelopes requested',lambda:len(calls)==3 and all(route!='git/trees/'+opaque for method,route in calls))
before=(len(calls),dict(ts.cache),ts.inspected)
good('F01 repeat return unchanged without extra reads',lambda:cap.projected_attempt(h,c,ts,root,{'own_unrelated.json':b'x'}, {})==('040000','tree',opaque) and (len(calls),dict(ts.cache),ts.inspected)==before)
good('F01 unknown foreign child also opaque',lambda:'f'*40 not in ts.cache)
aroot,asaved=make_tree({'foreign':('040000','tree','f'*40)})
ats,acalls=replay(asaved)
good('F01 absent empty attempt remains None',lambda:cap.projected_attempt(h,c,ats,aroot,{}, {}) is None)
broot,bsaved=make_tree({h.ATTEMPT:('100644','blob','b'*40)})
bad('F01 file in place of attempt tree refused',lambda:cap.projected_attempt(h,c,replay(bsaved)[0],broot,{}, {}))
# Positive nonempty overlay still rebuilds and checks own native preimages.
for present in (False,True):
 flat={h.ATTEMPT+'/old.txt':('100644','blob',cap.native('blob',b'old\n'))} if present else {'foreign':('040000','tree','f'*40)}
 oldroot,oldsave=make_tree(flat);obs,obs_calls=replay(oldsave)
 p=h.ATTEMPT+'/new/deep/note.txt';payload={p:b'new note\n'};pre={p:None}
 projected=cap.projected_attempt(h,c,obs,oldroot,payload,pre)
 desired,dest=make_tree({**flat,p:('100644','blob',cap.native('blob',payload[p]))})
 expected=replay(dest)[0].lookup(desired,h.ATTEMPT)
 good('nonempty own projection correct '+str(present),lambda:projected==expected)
 good('nonempty projection never descends foreign '+str(present),lambda:'f'*40 not in obs.cache)
bad('nonempty projection wrong exact preimage',lambda:cap.projected_attempt(h,c,replay(oldsave)[0],oldroot,{h.ATTEMPT+'/old.txt':b'bad'}, {h.ATTEMPT+'/old.txt':None}))
# Read the ACTUAL carry validator with a wholly in-memory, explicitly synthetic gate.
required=cap.required_carry(h)
extra=h.OLD_CASE+'extra_public_metadata.json'
text=b'synthetic reviewed public note\n'
gate={'schema':'pr239-root-prior-operational-carry-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','PR':239,'accepted':True,
 'prior_terminal_pin':h.PRIOR_TERMINAL_PIN,'finite_positive_public_selection_reviewed':True,'ordered239_intake_and_additive234_skip_preserved':True,
 'files':[{'path':p,**v} for p,v in required.items()]}
original_root_ref=h.root_ref
try:
 h.root_ref=lambda ref:copy.deepcopy(ref['SYNTHETIC_IN_MEMORY_VALUE'])
 carry=h.carry_inventory({'SYNTHETIC_IN_MEMORY_VALUE':gate})
 gate_extra=copy.deepcopy(gate);gate_extra['files'].append({'path':extra,**pin(text)})
 extra_carry=h.carry_inventory({'SYNTHETIC_IN_MEMORY_VALUE':gate_extra})
 bad('actual carry validator excludes arbitrary foreign target',lambda:h.carry_inventory({'SYNTHETIC_IN_MEMORY_VALUE':{**gate,'files':gate['files']+[{'path':'foreign/new.json',**pin(text)}]}}))
finally:h.root_ref=original_root_ref
good('actual carry validator retains required24',lambda:carry==required and len(carry)==24)
# Each pure final-predicate invocation uses a small relevant accepted-carry subset.
# Missing required24 is checked above by actual carry_inventory; the payload here is synthetic.
for phase in ('merge95','completion100'):
 bad('F02 extra old case outside actual carry '+phase,lambda phase=phase:cap.final_target_admissibility(h,{extra:text},{},[],phase))
 good('F02 same extra accepted when actual carry-listed '+phase,lambda phase=phase:cap.final_target_admissibility(h,{extra:text},{extra:extra_carry[extra]},[],phase))
 bad('F02 accepted carry byte mismatch '+phase,lambda phase=phase:cap.final_target_admissibility(h,{extra:text},{extra:pin(b'other')},[],phase))
 bad('F02 accepted carry missing from payload '+phase,lambda phase=phase:cap.final_target_admissibility(h,{}, {extra:pin(text)},[],phase))
 for suffix in ('report.json','note.tex','nested/check.py'):
  good('public target allowed '+phase+'/'+suffix,lambda phase=phase,suffix=suffix:cap.final_target_admissibility(h,{h.CASE+suffix:text},{},[],phase))
 for path in ('foreign/report.json',h.CASE+'private/x.json',h.CASE+'nested/RAW_STDOUT.json',h.CASE+'main.pdf',h.CASE+'verify.zip',h.SHARED+'/note.json'):
  bad('unlisted scope rejected '+phase+'/'+path,lambda phase=phase,path=path:cap.final_target_admissibility(h,{path:text},{},[],phase))
 science_path=h.ATTEMPT+'/research_note.txt';science=[{'path':science_path,**pin(text)}]
 bad('science absent from explicit list '+phase,lambda phase=phase:cap.final_target_admissibility(h,{science_path:text},{},[],phase))
 if phase=='merge95':
  good('science explicit exact body accepted95',lambda:cap.final_target_admissibility(h,{science_path:text},{},science,'merge95'))
  bad('science explicit wrong body rejected95',lambda:cap.final_target_admissibility(h,{science_path:text+b'changed'},{},science,'merge95'))
  good('QUEUE allowed only95',lambda:cap.final_target_admissibility(h,{h.QUEUE:text},{},[],'merge95'))
 else:
  bad('science explicit still forbidden100',lambda:cap.final_target_admissibility(h,{science_path:text},{},science,'completion100'))
  bad('QUEUE forbidden100',lambda:cap.final_target_admissibility(h,{h.QUEUE:text},{},[],'completion100'))
for malformed in ([{'path':science_path,**pin(text)},{'path':science_path,**pin(text)}],[{'path':science_path,**pin(text),'extra':True}],[{'path':h.CASE+'not_science.json',**pin(text)}]):
 bad('malformed or duplicate science list '+str(len(results)),lambda malformed=malformed:cap.final_target_admissibility(h,{science_path:text},{},malformed,'merge95'))
# Strict preliminary selection metadata; explicit known origin does not imply body classification.
def row(path,p,oid):
 return {'path':path,'origin':str(HERE/'IN_MEMORY_ONLY_NOT_READ.json'),**p,'git_blob':oid,'observed_source_mode':292,'role':'SYNTHETIC_METADATA','selection_basis':'No source body read'}
base=[row(p,v,'1'*40) for p,v in required.items()]+[row(p,{k:r[k] for k in ('bytes','sha256')},r['native_blob']) for p,r in h.original_archives().items()]
science_rows=[row(r['repository_path'],{k:r[k] for k in ('bytes','sha256')},r['native_blob']) for r in h.submitted_inventory()]
def plan(rows):
 return {'schema':'pr239-root-positive-public-selection-v1','PR':239,'operational_authority':False,'files':rows,'total_files':len(rows),'total_bytes':sum(r['bytes'] for r in rows)}
p95=plan(base+science_rows);p100=plan(base)
good('selection95 exact required88',lambda:len(cap.selection(h,p95,'merge95'))==88)
good('selection100 exact required56',lambda:len(cap.selection(h,p100,'completion100'))==56)
good('F02 preliminary selection intentionally permits reserved old case',lambda:extra in cap.selection(h,plan(base+[row(extra,pin(text),cap.native('blob',text))]),'completion100',True))
for key,value in (('PR',239.0),('PR',True),('schema','other'),('operational_authority',1),('operational_authority',True),('total_files',56.0),('total_bytes',True)):
 bad('selection typed header '+key+repr(value),lambda key=key,value=value:cap.selection(h,{**p100,key:value},'completion100'))
bad('selection extra key',lambda:cap.selection(h,{**p100,'extra':False},'completion100'))
bad('selection missing original archive',lambda:cap.selection(h,plan(base[:-1]),'completion100'))
bad('selection missing required carry',lambda:cap.selection(h,plan(base[1:]),'completion100'))
bad('selection duplicate target',lambda:cap.selection(h,plan(base+[base[0]]),'completion100'))
bad('selection science forbidden100',lambda:cap.selection(h,p95,'completion100'))
for key,value in (('observed_source_mode',True),('observed_source_mode','0444'),('observed_source_mode',0o644),('git_blob','F'*40),('sha256','g'*64),('bytes',True),('bytes',-1),('role',''),('selection_basis',''),('origin','relative.json'),('origin','/tmp/not_owned.json')):
 mutated=copy.deepcopy(p100);mutated['files'][0][key]=value
 bad('selection malformed row '+key+repr(value),lambda mutated=mutated:cap.selection(h,mutated,'completion100'))
for path in (h.VIEWS[0],h.QUEUE,h.CASE+'../escape.json',h.CASE+'nested//x.json',h.CASE+'x\\y.json',h.CASE+'x\x00.json',h.CASE+'x\n.json',h.CASE+'x.pdf',h.CASE+'x.zip',h.CASE+'ROOT_COMPLETE_capture/file.json',h.CASE+'nested/api_receipt.txt'):
 bad('selection unsafe/generated destination '+repr(path),lambda path=path:cap.selection(h,plan(base+[row(path,pin(text),cap.native('blob',text))]),'completion100'))
empty_pin=pin(b'')
large=base+[row(h.CASE+'bounded/'+str(i)+'.txt',empty_pin,cap.native('blob',b'')) for i in range(539)]
good('selection595 metadata bound accepted',lambda:len(cap.selection(h,plan(large),'completion100'))==595)
bad('selection596 metadata bound refused',lambda:cap.selection(h,plan(large+[row(h.CASE+'bounded/overflow.txt',empty_pin,cap.native('blob',b''))]),'completion100'))
oversize=base+[row(h.CASE+'size'+str(i)+'.txt',{'bytes':4_000_000,'sha256':'a'*64},'a'*40) for i in range(2)]
bad('selection aggregate8MB bound',lambda:cap.selection(h,plan(oversize),'completion100'))
# selected_bodies logical checks with an in-memory descriptor stand-in, never actual file access.
reader=cap.read_regular
try:
 store={}
 cap.read_regular=lambda p:(store[str(p)],None)
 p=h.CASE+'check.txt';origin=str(HERE/'SYNTHETIC.txt')
 for b in (b'hello\n','unicode π\n'.encode(),b''):
  store[origin]=b;r={'origin':origin,**pin(b),'git_blob':cap.native('blob',b)}
  good('selected body full hash logical '+str(len(b)),lambda r=r,b=b:cap.selected_bodies(h,{p:r})[p]==b)
  bad('selected body SHA1 mismatch '+str(len(b)),lambda r=r:cap.selected_bodies(h,{p:{**r,'git_blob':'a'*40}}))
 for b in (b'x\0y',b'\xff'):
  store[origin]=b;r={'origin':origin,**pin(b),'git_blob':cap.native('blob',b)}
  bad('selected body NUL/invalidUTF8 '+repr(b),lambda r=r:cap.selected_bodies(h,{p:r}))
finally:cap.read_regular=reader
# Signed commits: exact continuation folding, parent order and all bytes are identity-bearing.
root_id='2'*40
for parents in (['1'*40],['1'*40,'3'*40]):
 for ending in ('','\n','\n\n','\r\n'):
  payload='tree '+root_id+'\n'+''.join('parent '+p+'\n' for p in parents)+'author Test <x@example.invalid> 0 +0000\ncommitter Test <x@example.invalid> 0 +0000\n\nπ\nmessage\n'
  signature='-----BEGIN PGP SIGNATURE-----\nTEST\n-----END PGP SIGNATURE-----'+ending
  hdr,body=payload.encode().split(b'\n\n',1)
  raw=hdr+b'\ngpgsig '+b'\n '.join(signature.encode().split(b'\n'))+b'\n\n'+body
  j={'sha':cap.native('commit',raw),'tree':{'sha':root_id},'parents':[{'sha':p} for p in parents],'verification':{'payload':payload,'signature':signature}}
  good('signed exact folding '+str(len(parents))+'/'+repr(ending),lambda j=j,raw=raw:cap.raw_commit(j)==raw)
  bad('signed changed signature refused '+str(len(results)),lambda j=j:cap.raw_commit({**j,'verification':{**j['verification'],'signature':j['verification']['signature']+'x'}}))
  bad('signed changed native SHA refused '+str(len(results)),lambda j=j:cap.raw_commit({**j,'sha':'a'*40}))
  if len(parents)==2:
   bad('signed reversed parent metadata refused '+repr(ending),lambda j=j:cap.raw_commit({**j,'parents':list(reversed(j['parents']))}))
for a,z in ((0,0),(-420,-420),(345,345),(0,60)):
 def who(offset):
  sign='+' if offset>=0 else '-';n=abs(offset);return 'Test <x@example.invalid> 0 '+sign+str(n//60).zfill(2)+str(n%60).zfill(2)
 raw=('tree '+root_id+'\nparent '+'1'*40+'\nauthor '+who(a)+'\ncommitter '+who(z)+'\n\nunsigned\n').encode()
 meta={'name':'Test','email':'x@example.invalid','date':'1970-01-01T00:00:00Z'}
 j={'sha':cap.native('commit',raw),'tree':{'sha':root_id},'parents':[{'sha':'1'*40}],'author':meta,'committer':meta,'message':'unsigned','verification':{'reason':'unsigned','payload':None,'signature':None}}
 good('unsigned exact offset SHA-only recovery '+str((a,z)),lambda j=j,raw=raw:cap.raw_commit(j)==raw)
bad('unsupported unsigned/signed encoding refuses',lambda:cap.raw_commit({**j,'verification':{'reason':'unknown','payload':None,'signature':None}}))
bad('zero-parent native commit unsupported fail-stop',lambda:cap.raw_commit({**j,'parents':[]}))
bad('three-parent native commit unsupported fail-stop',lambda:cap.raw_commit({**j,'parents':[{'sha':'1'*40}]*3}))
# Offline tree replay must authenticate content before its tuples become usable.
r,sv=make_tree({'owned/a.txt':('100644','blob',cap.native('blob',b'a')), 'foreign':('040000','tree','f'*40),'executable':('100755','blob','e'*40)})
obs,rcalls=replay(sv)
good('canonical replay own association',lambda:obs.lookup(r,'owned/a.txt')==('100644','blob',cap.native('blob',b'a')))
good('equal foreign subtree never requested',lambda:'f'*40 not in obs.cache)
corrupt=copy.deepcopy(sv);corrupt[r]['executable']=('100755','blob','d'*40)
bad('corrupt saved tuple hash rejected',lambda:replay(corrupt)[0].lookup(r,'owned/a.txt'))
bad('missing saved envelope rejected without fallback',lambda:replay({})[0].lookup(r,'owned/a.txt'))
corrupt=copy.deepcopy(sv);corrupt[r]['executable']=('100644','tree','e'*40)
bad('mode/type mismatch rejected',lambda:replay(corrupt)[0].lookup(r,'owned/a.txt'))
corrupt=copy.deepcopy(sv);corrupt[r]['unsafe/name']=corrupt[r].pop('executable')
bad('immediate tree slash name rejected',lambda:replay(corrupt)[0].lookup(r,'owned/a.txt'))
overlay={'owned/new/deep.txt':b'new'};pre={p:obs.lookup(r,p) for p in overlay}
projected,changed,newdirs=h.expected(c,obs,r,overlay,pre)
rr,ss=make_tree({'owned/a.txt':('100644','blob',cap.native('blob',b'a')),'owned/new/deep.txt':('100644','blob',cap.native('blob',b'new')),'foreign':('040000','tree','f'*40),'executable':('100755','blob','e'*40)})
good('whole tree rebuild preserves foreign tuple and mode',lambda:projected==rr and changed=={'owned/new/deep.txt'} and newdirs=={'owned/new'} and 'f'*40 not in obs.cache)
bad('whole tree exact preimage mismatch refuses',lambda:h.expected(c,obs,r,{'owned/a.txt':b'changed'},{'owned/a.txt':None}))
bad('overlay leaf/ancestor collision refuses',lambda:h.expected(c,obs,r,{'owned':b'file','owned/sub.txt':b'x'},{'owned':None,'owned/sub.txt':None}))
# Whole QUEUE replacement; foreign line endings/order must remain exact.
own=b'|239|30001321 / OWR-4081-005|a|b|c|d|e|claimed_solved|3/5|f|g|h|'
for ending in (b'\n',b'\r\n',b''):
 pre_row=own.replace(b'claimed_solved|3/5',b'queued|0/5')+ending
 prefix=b'FOREIGN\r\n';before=prefix+pre_row
 after,prior,post=cap.queue_postimage(h,before,own+ending,'merge95')
 good('QUEUE preserves foreign prefix and exact endings '+repr(ending),lambda:after==prefix+own+ending and prior==pre_row and post==own+ending)
 good('QUEUE100 whole exact no-op '+repr(ending),lambda:cap.queue_postimage(h,after,None,'completion100')==(after,own+ending,own+ending))
bad('QUEUE wrong3of5 required',lambda:cap.queue_postimage(h,before,own.replace(b'3/5',b'1/5'),'merge95'))
bad('QUEUE duplicate own rows rejected',lambda:cap.queue_postimage(h,before+b'\n'+own+b'\n',own+b'\n','merge95'))
bad('QUEUE indented own ambiguity rejected',lambda:cap.queue_postimage(h,before+b'\n '+own+b'\n',own+b'\n','merge95'))
bad('QUEUE foreign payload hidden in supplied ownrow rejected',lambda:cap.queue_postimage(h,before,own+b'\nFOREIGN\n','merge95'))
bad('QUEUE supplied completion100 ownrow rejected',lambda:cap.queue_postimage(h,before,own,'completion100'))
# In-memory publication validator exercised through actual model, then phase proposals.
pubref={'SYNTHETIC_KEY':'publication'};trackref={'SYNTHETIC_KEY':'tracker'}
pub={'schema':'pr239-root-actual-publication-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','PR':239,'accepted':True,'published':True,
 'actual_submitted_record_verified_by_top_level_kit':True,'public_body_downloads_SHA256_verified':True,'new_publication':True,'unknown_outcome':False,'record_id':1,'doi':'10.5281/zenodo.1',
 'files':[{'name':'synthetic.pdf','size':1,'sha256':'a'*64},{'name':'synthetic.zip','size':1,'sha256':'b'*64}]}
track={'schema':'pr239-root-actual-tracker-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','PR':239,'accepted':True,'appended_once':True,'native_readback_verified':True,'fresh_duplicate_check_accepted':True,
 'publication_receipt':pubref,'spreadsheet_id':h.SPREADSHEET,'tab':'Math Puzzles','row':['30001321','', 'https://doi.org/10.5281/zenodo.1','https://github.com/AlecKriebel/Math/pull/239'],'range':"'Math Puzzles'!A1:D1"}
evidence={'publication':pubref,'tracker':trackref}
try:
 h.root_ref=lambda ref:copy.deepcopy({'publication':pub,'tracker':track}[ref['SYNTHETIC_KEY']])
 good('actual publication validator on labelled in-memory fixture',lambda:h.publication_identity({'evidence_references':evidence})['doi']=='10.5281/zenodo.1')
 native={p:None for p in h.VIEWS};local=dict(native)
 baseline={**h.baseline_facts('merge95'),**h.source_baseline(),'dated_eligible_total':99}
 native[h.VIEWS[2]]=local[h.VIEWS[2]]=cap.enc(baseline)
 native[h.VIEWS[4]]=b'older program history\n';local[h.VIEWS[4]]=b'older program history\nlocal addition\n';local[h.VIEWS[1]]=b'older case history\n'
 v95=cap.postimages(h,evidence,'merge95',native,local,'2026-10-18T00:00:00Z')
 good('95 keeps actual55/39 membership baseline',lambda:h.decode(v95[h.VIEWS[2]])['published_count']==39 and all(h.decode(v95[h.VIEWS[2]])[k]==a for k,a in h.source_baseline().items()))
 good('95 prefix preserves both native/local logs',lambda:all(v95[p].startswith(local[p] or b'') and v95[p].startswith(native[p] or b'') for p in (h.VIEWS[1],h.VIEWS[4])))
 v100=cap.postimages(h,evidence,'completion100',v95,v95,'2026-10-18T00:01:00Z')
 good('100 conditional56/40 only239 membership addition',lambda:h.decode(v100[h.VIEWS[2]])['published_count']==40 and all(h.decode(v100[h.VIEWS[2]])[k]==a+[239] for k,a in h.source_baseline().items()))
 good('100 conditional proposal never actual intake authority',lambda:h.decode(v100[h.VIEWS[0]])['completed'] is True and h.decode(v100[h.VIEWS[0]])['conditional_proposal_only'] is True and h.decode(v100[h.VIEWS[0]])['advance_to_next_PR_authorized_now'] is False)
 good('100 old prefix and exact95to100 log order',lambda:all(v100[p].startswith(v95[p]) for p in (h.VIEWS[1],h.VIEWS[4])))
 bad('95 duplicate marker refused',lambda:cap.postimages(h,evidence,'merge95',v95,v95,'2026-10-18T00:02:00Z'))
 bad('100 missing95 markers refused',lambda:cap.postimages(h,evidence,'completion100',native,local,'2026-10-18T00:02:00Z'))
 bad_local=dict(local);bad_local[h.VIEWS[4]]=b'divergent branch\n'
 bad('divergent log histories refused',lambda:cap.postimages(h,evidence,'merge95',native,bad_local,'2026-10-18T00:02:00Z'))
 for key,value in (('published_count',40),('published_count',39.0),('dated_eligible_total','99'),('dated_eligible_total',100),('fully_completed_count',True)):
  nv=dict(native);nv[h.VIEWS[2]]=cap.enc({**baseline,key:value})
  bad('mutable global progress mismatch '+key+repr(value),lambda nv=nv:cap.postimages(h,evidence,'merge95',nv,local,'2026-10-18T00:02:00Z'))
finally:h.root_ref=original_root_ref
# Static full call and order boundaries: these do not execute high-level operations.
tree=ast.parse(source);nodes={n.name:n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
segments={name:ast.get_source_segment(source.decode(),node) for name,node in nodes.items()}
final=segments['finalize'];capture=segments['capture'];guard=segments['source_guard']
good('F02 admissibility is before first stage Output',lambda:final.index('final_target_admissibility(')<final.index('out=Output('))
good('fresh guard and selected bytes before stage Output',lambda:final.index("guard();need(selected_bodies(")<final.index('out=Output('))
good('finalize has no live GET transport constructor',lambda:not any(t in final for t in ('GET(','e.API(','Seed(','Runtime(','WriterLock(','api(')))
good('capture cannot synthesize Root acceptance schema',lambda:"'evidence_scope':'ACTUAL_ROOT_RECEIPT'" not in capture and "'accepted':True" not in capture)
good('finalize construction explicitly denies actual logical authority',lambda:"'actual_Root_logical_acceptance_or_checkpoint_or_numeric_advance':False" in final and "'pr239-root-completion-logical-packet-acceptance-v1'" not in final)
good('source guard checks pinned config selection and acceptance',lambda:all(t in guard for t in ('config_ref,config_raw','selection_ref,selection_raw','acceptance_ref,acceptance_raw','independent_source_review_accepted','capture_source_pin')))
good('source guard covers both finite source manifests',lambda:"(HERE,own_raw" in guard and "(ENGINE,engine_raw" in guard and "for row in rows:" in guard)
good('main obtains source guard before either high-level action',lambda:segments['main'].index('source_guard(')<segments['main'].index("result=capture("))
good('Output writes exclusively new owned files',lambda:'os.O_EXCL|os.O_NOFOLLOW' in segments['Output'] and 'not path.exists() and not path.is_symlink()' in segments['Output'])
good('descriptor reader never follows any path component symlink',lambda:sum(isinstance(n,ast.Attribute) and n.attr=='O_NOFOLLOW' for n in ast.walk(nodes['read_regular']))>=3)
old_source=(CASE/'logical_capture_preparation_01/capture_logical_packet.py').read_text()
old_nodes={n.name:n for n in ast.parse(old_source).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
changes=[]
for name,n in nodes.items():
 if name not in old_nodes:changes.append('ADDED:'+name)
 elif ast.dump(n,include_attributes=False)!=ast.dump(old_nodes[name],include_attributes=False):changes.append('CHANGED:'+name)
good('revision02 changes only promised three functions',lambda:sorted(changes)==['ADDED:final_target_admissibility','CHANGED:finalize','CHANGED:projected_attempt'])
print(json.dumps({'schema':'pr239-independent-capture-source-controls-v1','PR':239,'revision':2,'source_pin':EXPECTED,'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'passed':len(results),'results':results,'execution_scope':'INERT_IMPORTS_PINNED_SOURCE_READS_AND_PURE_SYNTHETIC_CALLBACKS_ONLY','high_level_capture_finalize_source_guard_Output_GET_helpers_main_forbidden_by_in_memory_traps':True,'no_API_Seed_Runtime_lock_native_provider_tracker_PR_current_five_Git_or_network':True,'no_filesystem_writes_from_controls':True,'synthetic_receipts_are_in_memory_values_not_Root_operational_gates':True},sort_keys=True,indent=2))
