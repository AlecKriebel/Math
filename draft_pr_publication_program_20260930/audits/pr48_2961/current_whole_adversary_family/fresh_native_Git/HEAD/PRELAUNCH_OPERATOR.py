from pathlib import Path,PurePosixPath
import datetime as dt,hashlib,json,math,os,stat,subprocess
F=Path(__file__).absolute().parent;A=F.parent;R=A.parents[2];C=A/'reviewed_candidate';B=A.parent/'pr45_9900007';rows=[]
sha=lambda b:hashlib.sha256(b).hexdigest()
def raw(p):
 assert p.is_file()and not p.is_symlink()and all(not q.is_symlink()for q in p.parents);b=p.read_bytes();rows.append(dict(path=str(p),bytes=len(b),sha256=sha(b),full_mode=stat.S_IMODE(p.stat().st_mode)));return b

def load(p):
 def unique(items):
  d={}
  for k,v in items:assert k not in d;d[k]=v
  return d
 return json.loads(raw(p),object_pairs_hook=unique,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
def eq(a,b):
 if type(a)is not type(b):return False
 if type(a)is dict:return a.keys()==b.keys()and all(eq(a[k],b[k])for k in a)
 if type(a)is list:return len(a)==len(b)and all(eq(x,y)for x,y in zip(a,b))
 return a==b

def time(v):z=dt.datetime.fromisoformat(v.replace('Z','+00:00'));assert z.tzinfo and z.utcoffset()==dt.timedelta(0);return z
caps={}
for p in sorted(B.glob('root_pr48*capture/CAPTURE.json')):
 d=p.parent;c=load(p);assert {q.name for q in d.iterdir()}=={'CAPTURE.json','prelaunch_operator.py','stdout.bin','stderr.bin'}
 assert c['schema']=='root-explicit-command-capture/v1'and c['actual_execution']is True and c['completed']is True and type(c['pid'])is int and type(c['exit_code'])is int and c['stdin_supplied']is False and c['operator_unchanged']is True
 assert (c['exit_code']==c['expected_exit_code'])==(c['status']=='PASS');assert time(c['started_utc'])<=time(c['finished_utc'])<=dt.datetime.now(dt.timezone.utc)
 assert sha(raw(d/'prelaunch_operator.py'))==c['operator_sha256']
 for k in ['stdout','stderr']:
  b=raw(d/c[k]['path']);assert len(b)==c[k]['bytes']and sha(b)==c[k]['sha256']
 caps[d.name]=c
assert len(caps)==16
for cl,ver,folder,selfn,field,pid,vpid in [('current_source','current_source_closed_readback','current_preparation_family','PREPARATION_MANIFEST.json','created_utc',50088,50493),('current_source_adversary','current_source_adversary_closed_readback','current_source_adversary_family','MANIFEST.json','utc',86310,86540),('reproduction','closed_reproduction_readback','root_original_actual_reproduction_v2','MANIFEST.json','created_utc',19105,19580),('algebra_cocycle','algebra_cocycle_closed_readback','algebra_cocycle_family','MANIFEST.json','created_utc',20740,20855),('smooth_geometry','smooth_geometry_closed_readback','smooth_geometry_family','MANIFEST.json','created_utc',15467,16307)]:
 cc=caps['root_pr48_'+cl+'_closure_actual_capture'];vv=caps['root_pr48_'+ver+'_actual_capture'];m=load(A/folder/selfn)
 assert cc['pid']==pid and vv['pid']==vpid and time(cc['started_utc'])<=time(m[field])<=time(cc['finished_utc'])<time(vv['started_utc'])
# Original closure has a different six-file actual capture and source, verified separately.
d=A/'original_preparation_closure_actual_capture';original=load(d/'CAPTURE.json');assert original['pid']==87065 and original['exit_code']==0
for p in sorted(d.iterdir()):raw(p)
# ROOT complete derived SOURCE bindings and true five prerequisite records.
adv=load(A/'ROOT_NEW_SOURCE_ADVERSARY_RECORD.json');prep=load(A/'current_preparation_family/PREPARATION_MANIFEST.json');sourceclose=caps['root_pr48_current_source_closure_actual_capture'];adverclose=caps['root_pr48_current_source_adversary_closure_actual_capture'];author=caps['root_pr48_current_prerequisites_authoring_actual_capture']
assert author['pid']==91962 and time(caps['root_pr48_current_source_adversary_closed_readback_actual_capture']['finished_utc'])<time(author['started_utc'])
assert len(adv['individual_complete_external_bindings'])==1698
for r in adv['individual_complete_external_bindings']:
 b=raw(R/r['path']);assert len(b)==r['bytes']and sha(b)==r['sha256']and stat.S_IMODE((R/r['path']).stat().st_mode)==r['full_mode']
assert eq(adv['members'],[{k:r[k]for k in ['path','bytes','sha256']}for r in adv['normalized_complete_owned_body_mode_rows']])
for z in adv['complete_actual_SOURCE_and_adversary_closure_readback_captures']:
 c=z['complete_capture'];name=next(k for k,v in caps.items()if eq(v,c));assert eq(load(B/name/'stdout.bin'),z['complete_stdout_object'])
qualsha=sha(raw(C/'SOURCE_PRECISION_QUALIFICATIONS.md'));prepsha=sha(raw(A/'current_preparation_family/PREPARATION_MANIFEST.json'))
scope=raw(A/'ROOT_CURRENT_PARTIAL_SCOPE_CERTIFICATE.md');evidence=load(A/'ROOT_EVIDENCE_BINDINGS.json');ledger=load(A/'ROOT_PRIMARY_READ_LEDGER.json');science=load(A/'ROOT_SCIENCE_CARD.json');native=load(A/'ROOT_CURRENT_INPUT_PREIMAGES.json')
for n in ['ROOT_CURRENT_PARTIAL_SCOPE_CERTIFICATE.md','ROOT_EVIDENCE_BINDINGS.json','ROOT_PRIMARY_READ_LEDGER.json','ROOT_SCIENCE_CARD.json','ROOT_CURRENT_INPUT_PREIMAGES.json']:assert raw(A/n)==raw(C/'root_approval'/n)
for z in [evidence,ledger,science]:
 assert z['approved_by_root']is True and z['preparation_manifest_sha256']==prepsha and z['source_qualification_sha256']==qualsha and time(sourceclose['finished_utc'])<time(z['created_utc'])<=time(author['finished_utc'])
for z in [ledger,science]:assert z['scope_certificate_sha256']==sha(scope)and z['evidence_bindings_sha256']==sha(raw(A/'ROOT_EVIDENCE_BINDINGS.json'))
assert ledger['reading_completed']is True and len(ledger['root_flags'])==8 and all(v is True for v in ledger['root_flags'].values())
assert type(science['duplicate_id'])is int and science['duplicate_id']==30004403
for k in ['manifest','summary','proof_notes','raw_audit','source_adversary']:
 r=evidence[k];b=raw(R/r['path']);assert len(b)==r['bytes']and sha(b)==r['sha256']
# Exact current52 argv independently reconstructed from builder's explicit operations.
head='e2e5c8c3e5ad218f867fa753c465bb96b3687bda';base='c6975ca76f9f667f1250ba403d0e6da2aafe14d0';mb='60292bed09f59236aa192cb17aa138f7b4750e1a';snap=load(A/'snapshot_manifest.json');files=snap['files'];native4=['unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl','draft_pr_publication_program_20260930/inventory.json']
exact=[['git','branch','--show-current']]
for r in files:exact.extend([['git','show',head+':'+r['path']],['git','ls-tree',head,'--',r['path']]])
exact.extend([['git','merge-base',head,base],['git','diff','--no-ext-diff','--no-textconv','--binary',mb,head,'--'],['git','diff','--name-only',mb,head],['git','branch','--show-current'],['git','rev-parse','HEAD']])
for n in native4:exact.extend([['git','show',native['current_head']+':'+n],['git','ls-tree',native['current_head'],'--',n]])
exact.extend([['git','branch','--show-current'],['git','rev-parse','HEAD']]*2)
e=load(C/'CURRENT_EXECUTION_REFERENCE.json');inner=A/e['audit_relative_inner_attempt'];commands=load(inner/'GIT_COMMANDS.json');assert len(exact)==52 and eq([c['argv']for c in commands],exact)
for i,r in enumerate(files):
 assert raw(inner/commands[1+2*i]['stdout']['path'])==raw(A/'source_snapshot'/r['relative_path'])
 assert raw(inner/commands[2+2*i]['stdout']['path']).decode().strip()=='100644 blob '+r['git_object']+'\t'+r['path']
# Exact ROOT38 argv, sources and complete helper results.
rr=load(A/'root_original_actual_reproduction_v2/ROOT_REPRODUCTION_RESULT.json');expected=[]
for r in files:expected.extend([['git','show',head+':'+r['path']],['git','ls-tree',head,'--',r['path']]])
expected.extend([['git','merge-base',head,base],['git','diff','--no-ext-diff','--no-textconv','--binary',mb,head,'--'],['git','ls-tree','-r','-z',head,'--','unsolved_math_prioritization/attempts/2961/'],['git','show','2c32c34e6ddfa52ce067805afd3e2157dc32a130:unsolved_math_prioritization/attempts/2961/PARTIAL.md']]);assert eq([c['argv']for c in rr['complete_actual_Git_captures']],expected)
for c,name in zip(rr['complete_actual_helper_captures'],['author_historical','identical_submitted_historical','author_final','independent']):
 output=json.loads(raw(R/c['stdout']['path']));expected=rr['entire_historical_independent_result']if name=='independent'else rr['entire_historical_and_final_replayed_results'][name];assert eq(output,expected)
# ROOT author8 actual readonly children and five printed bindings.
for i in range(8):
 d=A/'root_current_prerequisite_Git_actual_captures'/str(i);c=load(d/'CAPTURE.json');p=load(d/'PRELAUNCH.json');assert c['operator_pid']==p['operator_pid']==91962 and c['source']is None and c['source_unchanged']is None and c['actual_execution']is True and c['completed']is True and c['exit_code']==0 and c['argv']==p['argv'];assert time(author['started_utc'])<=time(c['started_utc'])<=time(c['finished_utc'])<=time(author['finished_utc'])
 for k in ['stdout','stderr']:b=raw(d/c[k]['path']);assert sha(b)==c[k]['sha256']and len(b)==c[k]['bytes']
 if i in [1,7]:assert raw(d/'stdout.bin').decode().strip()==native['current_head']
 if 2<=i<=5:assert raw(d/'stdout.bin')==raw(C/'native4_proposal/preimage'/native4[i-2].replace('/','__'))
out=load(B/'root_pr48_current_prerequisites_authoring_actual_capture/stdout.bin');assert len(out['five_actual_prerequisites'])==5 and out['actual_pid']==91962
for r in out['five_actual_prerequisites']:b=raw(R/r['path']);assert len(b)==r['bytes']and sha(b)==r['sha256']
# Current first-party native/HEAD read only, with real fresh child captures; no new authority.
def git(name,argv):
 d=F/'fresh_native_Git'/name;d.mkdir(parents=True,exist_ok=False);s=Path(__file__).read_bytes();(d/'PRELAUNCH_OPERATOR.py').write_bytes(s);p=dict(argv=argv,cwd=str(R),operator_pid=os.getpid(),started_utc=dt.datetime.now(dt.timezone.utc).isoformat(),source=None,source_sha256=None);(d/'PRELAUNCH.json').write_text(json.dumps(p,indent=2)+'\n');c=dict(p,actual_execution=False,pid=None,completed=False,exit_code=None,stdin_supplied=False)
 try:
  with (d/'stdout.bin').open('xb')as so,(d/'stderr.bin').open('xb')as se:
   ch=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=so,stderr=se,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'));c.update(actual_execution=True,pid=ch.pid);c['exit_code']=ch.wait(timeout=60);c['completed']=True
 finally:
  c['finished_utc']=dt.datetime.now(dt.timezone.utc).isoformat()
  for k in ['stdout','stderr']:b=raw(d/(k+'.bin'));c[k]=dict(path=k+'.bin',bytes=len(b),sha256=sha(b))
  (d/'CAPTURE.json').write_text(json.dumps(c,indent=2)+'\n')
 assert c['exit_code']==0;return raw(d/'stdout.bin')
assert git('main',['git','branch','--show-current'])==b'main\n';livehead=git('HEAD',['git','rev-parse','HEAD']).decode().strip();livequeue=raw(R/'unsolved_math_prioritization/QUEUE.md');datedqueue=raw(C/'native4_proposal/preimage/unsolved_math_prioritization__QUEUE.md')
changed=[(a.decode(),b.decode())for a,b in zip(datedqueue.splitlines(),livequeue.splitlines())if a!=b]if len(datedqueue.splitlines())==len(livequeue.splitlines())else 'ROW_COUNT_CHANGED'
result=dict(schema='pr48-independent-complete-supplemental-readback/v1',status='PASS_ALL_ACTUAL_CAPTURES_ROOT_CROSSPINS_EXACT_COMMANDS_AND_NATIVE_DATING',actual_pid=os.getpid(),UTC=dt.datetime.now(dt.timezone.utc).isoformat(),all16_external_root_captures=caps,source_review13_directories_includes_root=True,current52_exact_argv=True,historicalROOT38_exact_argv=True,ROOT4_complete_printed_results_equal=True,ROOT8_prerequisite_Git_children_checked=True,five_actual_ROOT_records_reconciled=True,current_main_head_observed=livehead,dated_head=native['current_head'],current_queue_differs=livequeue!=datedqueue,complete_first_party_queue_changed_lines=changed,read_bindings=rows,future_acceptance_approved=False)
(F/'SUPPLEMENTAL_READBACK_RESULT.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n');print(json.dumps({k:v for k,v in result.items()if k not in {'read_bindings','all16_external_root_captures','complete_first_party_queue_changed_lines'}},indent=2))
