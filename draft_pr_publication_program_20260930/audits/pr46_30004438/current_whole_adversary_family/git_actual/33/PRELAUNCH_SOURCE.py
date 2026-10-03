"""Independent whole packet and raw importer reconstruction; read-only outside F."""
from pathlib import Path, PurePosixPath
import collections, datetime as dt, hashlib, json, math, os, re, sqlite3, stat, subprocess, sys
F=Path(__file__).absolute().parent; A=F.parent; R=A.parents[2]; C=A/'reviewed_candidate'
assert __debug__ and not sys.flags.optimize and os.environ.get('PYTHONOPTIMIZE','') in ('','0')
reads={}; checks=[]; git_commands=[]
def sha(b): return hashlib.sha256(b).hexdigest()
def encode(x): return (json.dumps(x,indent=2,allow_nan=False)+'\n').encode()
def ck(name, value):
 if value is not True: raise AssertionError(name)
 checks.append(name)
def read(p):
 p=Path(p); ck('regular '+str(p),not p.is_symlink() and all(not q.is_symlink() for q in p.parents) and stat.S_ISREG(p.stat().st_mode))
 b=p.read_bytes(); row={'path':str(p),'bytes':len(b),'sha256':sha(b),'full_mode':stat.S_IMODE(p.stat().st_mode)}
 ck('repeat unchanged '+str(p),str(p) not in reads or reads[str(p)]==row); reads[str(p)]=row
 return b
def unique(items):
 result={}
 for k,v in items:
  if k in result: raise ValueError('Duplicate key '+k)
  result[k]=v
 return result
def parse(b):
 return json.loads(b,object_pairs_hook=unique,parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))
def obj(p): return parse(read(p))
def typed_equal(a,b):
 if type(a) is not type(b): return False
 if type(a) is dict: return a.keys()==b.keys() and all(typed_equal(a[k],b[k]) for k in a)
 if type(a) is list: return len(a)==len(b) and all(typed_equal(x,y) for x,y in zip(a,b))
 return a==b
def path_name(n):
 ck('safe path '+str(n),type(n) is str and bool(n) and n!='.' and '\\' not in n and '\0' not in n and
  not PurePosixPath(n).is_absolute() and PurePosixPath(n).as_posix()==n and not {'.','..','.git','__pycache__'}.intersection(PurePosixPath(n).parts))
 return n
def topology(root,expected):
 fs=set();ds=set()
 ck('root directory '+str(root),root.is_dir() and not root.is_symlink())
 for p in root.rglob('*'):
  ck('no special topology '+str(p),not p.is_symlink() and (p.is_file() or p.is_dir()))
  n=path_name(p.relative_to(root).as_posix())
  (fs if p.is_file() else ds).add(n)
 inferred={q.as_posix() for n in fs for q in PurePosixPath(n).parents if q.as_posix()!='.'}
 ck('exact files '+str(root),fs==expected);ck('no empty extra dirs '+str(root),ds==inferred)
 return sorted(ds)
def check_rows(root,rs,mode=None):
 names=set()
 for row in rs:
  ck('typed manifest row',type(row) is dict and type(row['bytes']) is int and row['bytes']>=0 and type(row['sha256']) is str and re.fullmatch('[0-9a-f]{64}',row['sha256']) is not None)
  n=path_name(row['path']);ck('unique row '+n,n not in names);names.add(n)
  p=root/n;b=read(p);ck('complete row bytes '+str(p),len(b)==row['bytes'] and sha(b)==row['sha256'])
  if mode is not None: ck('full mode '+str(p),stat.S_IMODE(p.stat().st_mode)==mode)
 return names
def git(*args):
 assert args[0] in ('show','ls-tree','diff','rev-parse','branch')
 if args[0]=='branch':assert args==('branch','--show-current')
 d=F/'git_actual'/str(len(git_commands));d.mkdir(parents=True,exist_ok=False)
 rec={'argv':['git',*args],'cwd':str(R),'started_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
  'actual_execution':False,'pid':None,'completed':False,'exit_code':None,'stdin_supplied':False}
 (d/'PRELAUNCH.json').write_bytes(encode(rec));(d/'PRELAUNCH_SOURCE.py').write_bytes(read(Path(__file__)))
 with (d/'stdout.bin').open('xb') as so,(d/'stderr.bin').open('xb') as se:
  child=subprocess.Popen(rec['argv'],cwd=R,stdin=subprocess.DEVNULL,stdout=so,stderr=se,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'))
  rec.update(actual_execution=True,pid=child.pid);rec['exit_code']=child.wait(timeout=60);rec['completed']=True
 rec['finished_utc']=dt.datetime.now(dt.timezone.utc).isoformat()
 for channel in ['stdout','stderr']:
  b=read(d/(channel+'.bin'));rec[channel]={'path':str(d/(channel+'.bin')),'bytes':len(b),'sha256':sha(b)}
 (d/'CAPTURE.json').write_bytes(encode(rec));git_commands.append(rec)
 (F/'GIT_COMMANDS.json').write_bytes(encode(git_commands))
 ck('actual Git completed',rec['exit_code']==0 and read(d/'stderr.bin')==b'')
 return read(d/'stdout.bin')

mraw=read(C/'MANIFEST.json');m=parse(mraw)
ck('fixed candidate manifest',sha(mraw)=='66239699390b279235c4064208e63134049a5804884818de9176d377476a189d')
ck('candidate exact self closure',m['schema']=='PR46_STRICT_CURRENT_PACKET_v1' and m['self_excluded']==['MANIFEST.json'] and type(m['files_count']) is int and m['files_count']==len(m['files'])==946)
names=check_rows(C,m['files'],0o444);dirs=topology(C,names|{'MANIFEST.json'})
ck('manifest actual full0444',stat.S_IMODE((C/'MANIFEST.json').stat().st_mode)==0o444)
dep=obj(C/'CURRENT_DEPENDENCIES.json');ck('dependency true anchor',R/dep['anchor_repository_relative']==A and len(dep['files'])==826)
check_rows(A,dep['files'])
prep=obj(A/'current_preparation_family_v2/PREPARATION_MANIFEST.json')
ck('source V2 pin',sha(read(A/'current_preparation_family_v2/PREPARATION_MANIFEST.json'))=='5ba87a43d1e5da841c8d6f47b6c398c5de55047a447468e1576d2b0cbbd7439e')
pn=check_rows(A/'current_preparation_family_v2',prep['files'],0o444);topology(A/'current_preparation_family_v2',pn|{'PREPARATION_MANIFEST.json'})
ck('source123 actual',prep['files_count']==122 and prep['self_excluded']==['PREPARATION_MANIFEST.json'])
pins=obj(A/'current_preparation_family_v2/STATIC_INPUT_BINDINGS.json')
om=obj(A/pins['original_preparation_manifest']['path'])
on=check_rows(A,pins['original_preparation_members'],0o444)
ck('original318 scoped member equality',len(on)==318 and on=={x['path'] for x in om['files']})
scoped=set(om['authorship_root_files'])
for root in om['authorship_directory_roots']:
 scoped.update(root+'/'+p.relative_to(A/root).as_posix() for p in (A/root).rglob('*') if p.is_file())
ck('original authorship exact scoped topology',scoped==on)
for family,info in pins['families'].items():
 member_names=check_rows(A/family,info['members']+info['separate_excluded_closure'],0o444)
 manifest_relative=info['manifest']['path'];topology(A/family,member_names|{manifest_relative})
 fm=obj(A/family/manifest_relative)
 ck('family exact exclusions '+family,fm['self_excluded']==info['manifest_self_excluded'])
 ck('family member count '+family,fm['files_count']==len(info['members']) and {x['path'] for x in fm['files']}=={x['path'] for x in info['members']})
 for n,mode in info['directory_modes'].items():ck('family directory mode '+family+'/'+n,stat.S_IMODE((A/family/n).stat().st_mode)==mode)
root_reproduction=obj(A/'root_original_actual_reproduction_v2/MANIFEST.json')
rn=check_rows(A/'root_original_actual_reproduction_v2',root_reproduction['files'],0o444)
topology(A/'root_original_actual_reproduction_v2',rn|{'MANIFEST.json'})
ck('ROOT exact37 self-only',len(rn)==37 and root_reproduction['self_excluded']==['MANIFEST.json'])
sm=obj(A/'current_source_adversary_family_v2/MANIFEST.json')
ck('source adversary pin',sha(read(A/'current_source_adversary_family_v2/MANIFEST.json'))=='f41b95e4f2cb3bf32943434ec758718112eb922582865e7b4dca016d5a7beb86')
sn=check_rows(A/'current_source_adversary_family_v2',sm['files'],0o444);topology(A/'current_source_adversary_family_v2',sn|{'MANIFEST.json'})
ck('new source190 actual',len(sn)==189 and sm['self_excluded']==['MANIFEST.json'])
snapshot=obj(C/'original_snapshot_manifest.json'); originals={}
head='a39d178b10f75fb127058b08e0d0002b3ae97f8a';base='c6975ca76f9f667f1250ba403d0e6da2aafe14d0'
for row in snapshot['files']:
 n=row['relative_path'];b=read(C/'original_archive'/n);originals[n]=b
 ck('full original source '+n,len(b)==row['bytes'] and sha(b)==row['sha256'] and b==read(A/'source_snapshot'/n))
 ck('original Git whole body '+n,git('show',head+':'+row['path'])==b)
 ck('original Git blob/mode '+n,git('ls-tree',head,'--',row['path']).decode().strip()=='100644 blob '+row['git_object']+'\t'+row['path'])
ck('full original13',len(originals)==13)
full_diff=git('diff','--no-ext-diff','--no-textconv','--binary',base,head,'--')
ck('full14path diff bytes',full_diff==read(C/'original_diff.patch') and len(full_diff)==89103 and sha(full_diff)=='944d6ac424b3e6fa6d4ccf163e6b381352072589528a3a5a29b146454e458209')
paths=git('diff','--name-only',base,head).decode().splitlines();ck('full14 scope',len(paths)==14 and set(paths)=={snapshot['files'][i]['path'] for i in range(13)}|{'unsolved_math_prioritization/QUEUE.md'})
for n in ['SOURCE_STATUS.md','verification.json','verify.py','source_record.json','turns.json','provenance.json','independent_review/independent_checks.py','independent_review/independent_results.json']:
 ck('operative immutable exact '+n,read(C/n)==originals[n])
ledger=parse(originals['turns.json']);ck('object ledger original0/5 source1',type(ledger) is dict and type(ledger['substantive_turns_used']) is int and ledger['substantive_turns_used']==0 and type(ledger['source_verification_responses']) is int and ledger['source_verification_responses']==1 and type(ledger['turn_limit']) is int and ledger['turn_limit']==5)
for n,count in [('verification.json',51),('independent_review/independent_results.json',848)]:
 r=parse(originals[n]);ck('complete receipt exact count '+n,type(r['passed']) is int and r['passed']==count and type(r['failed']) is int and r['failed']==0 and type(r['checks']) is dict and len(r['checks'])==count and all(x=='PASS' for x in r['checks'].values()))
 for key,val in r['checks'].items():ck('entire receipt label '+key,type(key) is str and val=='PASS')
state=obj(C/'status.json')
for n in ['readiness.json','independent_review/verdict.json','independent_review/review_summary.json']:ck('global current metadata '+n,typed_equal(obj(C/n),state))
ck('exact current known result status',state['status']=='already_solved' and state['full_problem_solved'] is True and state['project_solved'] is False and state['novelty_claimed'] is False and state['exact_mathematical_gap_remaining'] is None)
for key in ['current_model','current_reasoning_effort','current_deadline_utc','current_verdict']:ck('explicit null '+key,state[key] is None)
for key in ['paper_created','new_DOI_created','tracker_row_created','historical_verdict_transferred','journal_publication_certified','fresh_PDF_bytes_or_pixels_authenticated']:ck('explicit false '+key,state[key] is False)
qualification=read(C/'SOURCE_PRECISION_QUALIFICATIONS.md')
for n in ['README.md','PR_DRAFT.md','pr_body.md','CURRENT_CONTEXT.md','CURRENT_SOURCE_STATUS_CONTEXT.md','independent_review/REVIEW.md']:ck('whole operative qualification '+n,qualification in read(C/n))

# Actual final original inner commands after real child exit, not its frozen prefix.
execution=obj(C/'CURRENT_EXECUTION_REFERENCE.json');outer=A/execution['audit_relative_outer_capture'];inner=A/execution['audit_relative_inner_attempt']
capture=obj(outer/'CAPTURE.json');pre=obj(outer/'OPERATION_PRELAUNCH.json');inv=obj(inner/'INVOCATION.json')
ck('actual outer operator child identities',capture['operator_pid']==85727 and capture['pid']==85728 and inv['pid']==85728 and inv['parent_pid']==85727)
ck('complete actual outer exit',capture['actual_execution'] is True and capture['completed'] is True and type(capture['exit_code']) is int and capture['exit_code']==0 and capture['current_whole_verdict'] is None and capture['new_whole_current_gate']=='PENDING')
ck('captured actual chronology',dt.datetime.fromisoformat(capture['started_utc'])<dt.datetime.fromisoformat(capture['finished_utc'])<dt.datetime.now(dt.timezone.utc))
for channel in ['stdout','stderr']:
 b=read(outer/capture[channel]['path']);ck('outer full '+channel,len(b)==capture[channel]['bytes'] and sha(b)==capture[channel]['sha256'])
ck('builder stdout full manifest',parse(read(outer/'stdout.bin'))['manifest_sha256']==sha(mraw) and read(outer/'stderr.bin')==b'')
ck('outer prelaunch full exact',capture['argv']==pre['argv'] and pre['operator_pid']==inv['parent_pid'] and capture['builder_sha256']==sha(read(outer/'PRELAUNCH_BUILDER_SOURCE.py')) and capture['operator_sha256']==sha(read(outer/'PRELAUNCH_OPERATOR.py')))
actual=obj(inner/'GIT_COMMANDS.json');prefix=obj(C/'build/actual_attempt_prepublication_prefix/GIT_COMMANDS.json')
ck('honest strict prefix',len(prefix)<len(actual) and typed_equal(prefix,actual[:len(prefix)]))
for i,rec in enumerate(actual):
 ck('final inner actual child '+str(i),rec['actual_execution'] is True and rec['completed'] is True and type(rec['pid']) is int and rec['pid']>0 and type(rec['exit_code']) is int and rec['exit_code']==0 and rec['stdin_supplied'] is False)
 start=dt.datetime.fromisoformat(rec['started_utc']);end=dt.datetime.fromisoformat(rec['finished_utc'])
 ck('inner actual UTC '+str(i),start<=end<=dt.datetime.fromisoformat(capture['finished_utc']))
 ck('inner readonly argv '+str(i),rec['argv'][0]=='git' and rec['argv'][1] in ('branch','rev-parse','show','ls-tree','diff'))
 for channel in ['stdout','stderr']:
  b=read(inner/rec[channel]['path']);ck('complete original final stream '+str(i)+' '+channel,len(b)==rec[channel]['bytes'] and sha(b)==rec[channel]['sha256'])
 ck('inner stderr empty '+str(i),read(inner/rec['stderr']['path'])==b'')
ck('truthful final command attribution',execution['final_inner_GIT_COMMANDS_written_incrementally_by_builder_before_exit'] is True and execution['frozen_inner_command_copy_is_prepublication_prefix'] is True and execution['outer_operator_does_not_write_inner_GIT_COMMANDS'] is True and execution['already_complete_outer_receipt_or_whole_PASS_certified'] is False)
retained=obj(C/'build/RETAINED_ACTUAL_ATTEMPT_TREES.json')
for tree in retained:
 t=A/tree['audit_relative_directory']
 if tree['current_attempt_listing_is_prepublication_prefix'] is True:
  for row in tree['files']:check_rows(C/'build/actual_attempt_prepublication_prefix',[row])
 else:
  for row in tree['files']:check_rows(t,[row])
 ck('retained honest prefix flag',tree['positive_packet_claimed'] is False)

# Frozen past native4 complete bodies and exact one-row proposed change.
native4={'unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl','draft_pr_publication_program_20260930/inventory.json'}
for row in dep['current_native13']:
 if row['path'] in native4:
  b=read(C/'native4_proposal/preimage'/row['path'].replace('/','__'))
  ck('frozen native4 past '+row['path'],len(b)==row['bytes'] and sha(b)==row['sha256'] and git('show',dep['current_main_head']+':'+row['path'])==b)
  if not row['path'].endswith('/QUEUE.md'):ck('prospective native4 unchanged '+row['path'],read(C/'native4_proposal/prospective'/row['path'].replace('/','__'))==b)
 else:
  b=read(R/row['path']);ck('stable9 wholelive bytes/fullmode '+row['path'],len(b)==row['bytes'] and sha(b)==row['sha256'] and stat.S_IMODE((R/row['path']).stat().st_mode)==row['full_mode'])
before=read(C/'queue_proposal/QUEUE_PREIMAGE.md');after=read(C/'queue_proposal/QUEUE_PROSPECTIVE.md')
bl=before.splitlines(keepends=True);al=after.splitlines(keepends=True);ck('wholequeue line count',len(bl)==len(al))
changed=[(x,y) for x,y in zip(bl,al) if x!=y];ck('one queue row',len(changed)==1)
b,a=changed[0];bf=b.decode().split('|');af=a.decode().split('|');ck('exact selected target',bf[2].strip()==af[2].strip()=='30004438 / OWR-17475-003')
header=[x.strip() for x in next(x for x in bl if x.startswith(b'| Rank |')).decode().split('|')[1:-1]]
allowed={header.index(x)+1 for x in ['Status','Turns','Findings']}
ck('only named target cells',all(x==y for i,(x,y) in enumerate(zip(bf,af)) if i not in allowed) and len(bf)==len(af))
ck('queued to existingknown',bf[header.index('Status')+1].strip()=='queued' and af[header.index('Status')+1].strip()=='already_solved' and bf[header.index('Turns')+1].strip()==af[header.index('Turns')+1].strip()=='0/5')
for n in ['preimage','prospective']:ck('queue copies whole '+n,read(C/'native4_proposal'/n/'unsolved_math_prioritization__QUEUE.md')==(before if n=='preimage' else after))
proposal=obj(C/'native4_proposal/PROPOSAL_SCOPE.json');ck('future native authority required',proposal['native_acceptance_requires_later_ROOT_saved_full_plan_and_fresh13_currentHEAD'] is True and proposal['state_history_inventory_prospective']=='UNCHANGED_BYTE_EXACT')
observed_head=git('rev-parse','HEAD').decode().strip();ck('main branch',git('branch','--show-current').strip()==b'main')

# Independent complete foreign raw/prior/SQL reconstruction, retaining hashes only.
rb=read(R/'unsolved_math_prioritization/cache/problems.json');pb=read(R/'unsolved_math_prioritization/cache/research_results.json')
raw=parse(rb);prior=parse(pb);ck('complete raw/prior lengths',len(rb)+len(pb)==149266659 and len(raw)==15458 and len(prior)==6701)
byid={str(x['id']):x for x in raw};code_counts=collections.Counter(x['problem_number'] for x in raw)
ck('raw ids unique',len(byid)==len(raw));saved_audit=obj(C/'root_evidence/ROOT_COMPLETE_RAW_SQL_AUDIT.json');saved_rows=saved_audit['complete_row_bindings']
connection=sqlite3.connect('file:'+str(R/'unsolved_math_prioritization/cache/catalog.sqlite')+'?mode=ro&immutable=1',uri=True)
connection.execute('PRAGMA query_only=ON');ck('SQL query only',connection.execute('PRAGMA query_only').fetchone()==(1,))
new_rows=[]
for key,payload,report in connection.execute('SELECT key,payload,report FROM records ORDER BY key'):
 expected=dict(byid[key]);code=expected['problem_number'];ambiguous=code_counts[code]>1 and code in prior
 if ambiguous:expected['_ambiguous_report']=True
 expected_prior={} if ambiguous else prior.get(code,{})
 ck('whole SQL payload '+key,typed_equal(parse(payload),expected));ck('whole SQL report '+key,typed_equal(parse(report),expected_prior))
 new_rows.append({'key':key,'payload_sha256':sha(payload.encode()),'report_sha256':sha(report.encode()),'complete_payload_recursive_type_equal':True,'complete_report_recursive_type_equal':True,'prior_key_present':code in prior,'ambiguous_code':ambiguous})
connection.close();ck('all SQL saved row bindings',len(new_rows)==15458 and typed_equal(new_rows,saved_rows))
selected=byid['30004438'];ck('plain saved source full typed identity',typed_equal(selected,parse(originals['source_record.json'])) and type(selected['id']) is int and 'problem' not in selected)
ck('prior absent distinguished',selected['problem_number'] not in prior and saved_audit['selected_prior_key_present'] is False and type(saved_audit['selected_prior_fallback']) is dict and saved_audit['selected_prior_fallback']=={} and saved_audit['raw_null_present'] is False)
(F/'INDEPENDENT_RAW_SQL_ROW_BINDINGS.json').write_bytes(encode({'schema':'pr46-whole-independent-complete-raw-sql/v1','raw_prior_bytes':len(rb)+len(pb),'SQL_rows':new_rows,'foreign_bodies_saved':False,'selected_prior_present':False,'selected_fallback':{},'future_acceptance_approved':False}))
summary=obj(C/'root_evidence/root_original_actual_reproduction_v2/ROOT_CURRENT_REPRODUCTION_SUMMARY.json')
ck('entire ROOT author result',typed_equal(summary['entire_author_result'],parse(originals['verification.json'])))
ck('entire ROOT independent result',typed_equal(summary['entire_historical_independent_result'],parse(originals['independent_review/independent_results.json'])))
ck('entire ROOT turns',typed_equal(summary['complete_original_turns'],ledger))
for cap in summary['complete_helper_captures']:
 ck('real unchanged helper actual capture',cap['actual_execution'] is True and cap['completed'] is True and type(cap['pid']) is int and cap['pid'] in (62515,62516) and type(cap['exit_code']) is int and cap['exit_code']==0 and cap['source_unchanged'] is True)
 for k in ['source','copied_source','stdout','stderr']:check_rows(R,[cap[k]])
ck('helper source whole bytes same',read(A/'root_original_actual_reproduction_v2/author/verify.py')==originals['verify.py'] and read(A/'root_original_actual_reproduction_v2/historical_independent/independent_checks.py')==originals['independent_review/independent_checks.py'])
for cap in summary.get('complete_outer_captures',[]):
 # Complete outer records are additionally pinned/read by the packet closure.
 ck('outer capture dictionary',type(cap) is dict)
result={'schema':'pr46-whole-independent-complete-readback/v1','status':'PASS_COMPLETE_CURRENT_PACKET_AND_ACTUAL_EVIDENCE',
 'created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_pid':os.getpid(),'checks_passed':len(checks),'checks':checks,
 'packet_manifest_sha256':sha(mraw),'packet_payload_files':946,'packet_relative_directories':dirs,
 'dependencies_count':826,'all_unique_reads':sorted(reads.values(),key=lambda x:x['path']),
 'all_unique_read_bytes':sum(x['bytes'] for x in reads.values()),'original13_Git_and_full14diff_checked':True,
 'final_original_inner_command_count':len(actual),'frozen_prefix_command_count':len(prefix),
 'entire_original_final_inner_commands':actual,'entire_original_outer_capture':capture,
 'frozen_native4_head':dep['current_main_head'],'observed_live_main_head':observed_head,'stable9_live_checked':True,
 'raw_prior_bytes_independently_reconstructed':149266659,'all_SQL_rows_independently_reconstructed':15458,
 'genuine_readonly_Git_children':git_commands,'source_adversary_PASS_transferred':False,
 'new_whole_review_mandatory_corrections':[],'production_builder_or_operator_run':False,'future_acceptance_approved':False}
(F/'READBACK_RESULT.json').write_bytes(encode(result))
print(json.dumps({k:result[k] for k in ['status','actual_pid','checks_passed','packet_payload_files','dependencies_count','all_unique_read_bytes','final_original_inner_command_count','frozen_prefix_command_count','frozen_native4_head','observed_live_main_head','raw_prior_bytes_independently_reconstructed','all_SQL_rows_independently_reconstructed']},indent=2))
