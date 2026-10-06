#!/usr/bin/env python3
"""Independent read-only SOURCE/control audit; production sources are only parsed as text."""
import ast, copy, ctypes, datetime as dt, hashlib, json, math, os, re, stat, subprocess
from pathlib import Path, PurePosixPath
R=Path('/Users/alec/Documents/Math'); A=R/'draft_pr_publication_program_20260930/audits/pr47_2849'; F=A/'current_source_adversary_family_v2'; S=A/'current_preparation_family_v2'
HEAD='487327b2412c436ae69e8c52bf353a9a1fb7594e'; BASE='c6975ca76f9f667f1250ba403d0e6da2aafe14d0'
assert __debug__
count=0; reads={}; mutations=[]; git_commands=[]
def ck(v,m):
 global count
 assert v,m
 count+=1
def sha(b): return hashlib.sha256(b).hexdigest()
def eq(a,b):
 if type(a) is not type(b): return False
 if type(a) is dict: return set(a)==set(b) and all(eq(a[k],b[k]) for k in a)
 if type(a) is list: return len(a)==len(b) and all(eq(x,y) for x,y in zip(a,b))
 return a==b
def load(b):
 def pairs(v):
  o={}
  for k,x in v:
   ck(k not in o,'duplicate JSON key'); o[k]=x
  return o
 def floating(v):
  x=float(v); ck(math.isfinite(x),'nonfinite number'); return x
 def constant(v): raise ValueError(v)
 return json.loads(b,object_pairs_hook=pairs,parse_constant=constant,parse_float=floating)
def rel(n):
 assert type(n) is str and n and '\\' not in n and '\0' not in n
 p=PurePosixPath(n); assert not p.is_absolute() and str(p)==n and not {'.','..','.git','__pycache__'}.intersection(p.parts)
 return n
def read(p,expected=None):
 p=Path(p); ck(not p.is_symlink() and all(not q.is_symlink() for q in p.parents) and stat.S_ISREG(p.stat().st_mode),'regular read')
 b=p.read_bytes(); mode=stat.S_IMODE(p.stat().st_mode); row={'path':p.relative_to(R).as_posix(),'bytes':len(b),'sha256':sha(b),'full_mode':mode}
 if expected:
  for k in ['bytes','sha256']: ck(row[k]==expected[k], 'exact body '+str(p))
  if 'full_mode' in expected: ck(mode==(int(expected['full_mode'],8) if type(expected['full_mode']) is str else expected['full_mode']),'exact declared mode')
 ck(row['path'] not in reads or eq(reads[row['path']],row),'repeated immutable read'); reads[row['path']]=row
 return b
def checked(row):
 assert type(row) is dict and set(row) in [{'path','bytes','sha256'},{'path','bytes','sha256','full_mode'}]
 rel(row['path']); assert type(row['bytes']) is int and row['bytes']>=0 and type(row['sha256']) is str and re.fullmatch('[0-9a-f]{64}',row['sha256'])
 if 'full_mode' in row: assert type(row['full_mode']) is int and 0<=row['full_mode']<4096
 return read(R/row['path'],row)
def tree(root):
 fs=set(); ds=set()
 ck(root.is_dir() and not root.is_symlink(),'root directory')
 for p in root.rglob('*'):
  ck(not p.is_symlink(),'nonsymlink topology'); n=rel(p.relative_to(root).as_posix())
  if stat.S_ISREG(p.stat().st_mode): fs.add(n)
  else: ck(stat.S_ISDIR(p.stat().st_mode),'no special member'); ds.add(n)
 return fs,ds
def closure(root,mname,expected_sha,count_expected,dirs_expected=None):
 mb=read(root/mname); ck(sha(mb)==expected_sha,'literal closure hash'); m=load(mb)
 if root.name=='cover_algebra_family': ck(m['sole_self_excluded_from_members']==mname and len(m['files'])==count_expected,'cover distinct schema')
 elif root.name=='gauge_geometry_family': ck(m['self_excluded']==mname and type(m['file_count_excluding_self']) is int and m['file_count_excluding_self']==len(m['files'])==count_expected,'gauge distinct schema')
 else: ck(m['self_excluded']==[mname] and type(m['files_count']) is int and m['files_count']==len(m['files'])==count_expected,'self-only count')
 ck(len({r['path'] for r in m['files']})==len(m['files']),'unique closure rows')
 for row in m['files']:
  read(root/rel(row['path']),row); ck(stat.S_IMODE((root/row['path']).stat().st_mode)==0o444,'full member0444')
 ck(stat.S_IMODE((root/mname).stat().st_mode)==0o444,'full self0444')
 if mname!='ORIGINAL_PREPARATION_MANIFEST.json':
  fs,ds=tree(root); ck(fs=={r['path'] for r in m['files']}|{mname},'no extra member')
  declared={x['path'] if type(x) is dict else x for x in m['directories']}; declared.discard('.')
  ck(ds==declared,'exact directory names')
  if dirs_expected is not None: ck(len(ds)==dirs_expected,'directory count')
 else:
  fs=set(m['authorship_root_files']); ds=set()
  for n in m['authorship_directory_roots']:
   subf,subd=tree(root/n); fs|={n+'/'+x for x in subf}; ds|={n}|{n+'/'+x for x in subd}
  ck(fs=={r['path'] for r in m['files']},'original scoped ownership')
  ck(ds==set(m['owned_directories']) and len(ds)==55,'original55 directories')
 return m
def time(v):
 assert type(v) is str
 x=dt.datetime.fromisoformat(v.replace('Z','+00:00')); assert x.tzinfo is not None and x.utcoffset()==dt.timedelta(0)
 return x
def completed(c,kind,argv,source,op):
 # Independently transcribed predicate; no extraction/import/compile/exec of production.
 assert type(c) is dict and set(c)=={'schema','argv','cwd','started_utc','actual_operator_pid','stdin_supplied','source','actual_execution','pid','completed','exit_code','finished_utc','stdout','stderr','source_unchanged'}
 assert c['schema']=='pr47-root-literal-operation-capture/v1' and kind in {'helper','git'}
 assert type(c['argv']) is list and all(type(x) is str for x in c['argv']) and eq(c['argv'],argv) and c['cwd']==str(R)
 assert type(op) is int and op>0 and type(c['actual_operator_pid']) is int and c['actual_operator_pid']==op
 assert c['actual_execution'] is True and c['completed'] is True and type(c['pid']) is int and c['pid']>0 and type(c['exit_code']) is int and c['exit_code']==0 and c['stdin_supplied'] is False
 assert time(c['started_utc'])<=time(c['finished_utc'])<=dt.datetime.now(dt.timezone.utc)
 streams={k:checked(c[k]) for k in ['stdout','stderr']}; assert streams['stderr']==b''
 if kind=='helper':
  assert type(c['source']) is dict and eq(c['source'],source) and c['source_unchanged'] is True; checked(c['source'])
 else: assert source is None and c['source'] is None and c['source_unchanged'] is None
 return streams
def reject(c,kind,argv,source,op,label):
 try: completed(c,kind,argv,source,op)
 except (AssertionError,ValueError,TypeError,KeyError,OSError): mutations.append(label); ck(True,label); return
 raise AssertionError('accepted malformed '+label)

prep=closure(S,'PREPARATION_MANIFEST.json','da314f40d628606f8e80cc198c3ab4a94b71554e929f70c63fce31cc195def10',139,16)
builder=read(S/'prepare_current_packet.py'); operator=read(S/'capture_root_builder_operation.py')
ck(sha(builder)=='5d0f9c7206043e0503acf1212832ae05d85d670f2d37d9894ab3af3b1071c6c3','exact builder')
ck(len(builder.splitlines())==269,'all269 builder lines')
parsed=ast.parse(builder)
ck({n.name for n in parsed.body if isinstance(n,ast.FunctionDef)}=={'need','sha','enc','utc','clock','equal','hex64','load','relative','raw','topology','rows','write','publish_absent','validate_completed_original_capture','build','main'},'source AST reviewed functions')
ck(b'compile(' not in builder and b'exec(' not in builder and b'importlib' not in builder,'no dynamic production source execution')
ck(b'caps=summary[\'complete_actual_helper_captures\']; gitcaps=summary[\'complete_actual_Git_captures\']' in builder,'explicit class lists')
pins=load(read(S/'STATIC_INPUT_BINDINGS.json')); fixed=load(read(S/'ROOT_FIXED_EVIDENCE.json')); repair=load(read(S/'SOURCE_V1_REPAIR_BINDINGS.json'))
for group,info in pins['groups'].items():
 checked(info['manifest'])
 for row in info['members']: checked(row)
 root=(R/info['manifest']['path']).parent
 for row in info['directories']: ck(stat.S_IMODE((root/row['path']).stat().st_mode)==row['full_mode'],'directory full mode')
for row in pins['separate_original_and_ROOT_actual_captures']: checked(row)
closure(A,'ORIGINAL_PREPARATION_MANIFEST.json',pins['groups']['original']['manifest']['sha256'],301)
closure(A/'cover_algebra_family','SELF_MANIFEST.json',pins['groups']['cover_algebra_family']['manifest']['sha256'],143,23)
closure(A/'gauge_geometry_family','SELF_MANIFEST.json',pins['groups']['gauge_geometry_family']['manifest']['sha256'],71,15)
closure(A/'root_original_actual_reproduction','MANIFEST.json',fixed['manifest']['sha256'],219,46)
for row in fixed['members']+fixed['separate_actual_closure_members']: checked(row)
for group,info in repair['closed_groups'].items():
 checked(info['manifest']); closure((R/info['manifest']['path']).parent,Path(info['manifest']['path']).name,info['manifest']['sha256'],len(info['members']) if 'members' in info else load(checked(info['manifest']))['files_count'])
for row in repair['complete_fixed_member_reads']+repair['external_ROOT_closure_and_readback_members']: checked(row)
for row in repair['qualified_current_packet_exports']: checked(row)
summary=load(read(A/'root_original_actual_reproduction/ROOT_REPRODUCTION_RESULT.json')); snapshot=load(read(A/'snapshot_manifest.json'))
author=load(read(A/'source_snapshot/verification.json')); independent=load(read(A/'source_snapshot/review/independent_results.json')); ledger=load(read(A/'source_snapshot/turns.json'))
ck(author['assertions']==114 and len(author['checks'])==114 and len(set(author['checks']))==114,'complete author labels114')
ck(independent['passed']==100 and independent['failed']==0 and len(independent['checks'])==100 and all(v=='PASS' for v in independent['checks'].values()),'complete independent100')
ck(eq(summary['entire_author_result'],author) and eq(summary['entire_identical_submitted_copy_result'],author) and eq(summary['entire_historical_independent_result'],independent),'every result scalar/type')
ck(summary['duplicate114_counted_independent'] is False and summary['full_Floer_problem_solved'] is False and summary['future_acceptance_approved'] is False,'honest scope')
ck(type(ledger) is dict and type(ledger['count']) is int and ledger['count']==1 and len(ledger['attempts'])==1 and eq(summary['complete_original_turns'],ledger),'one object attempt')
ck(read(A/'source_snapshot/prior_report.json')==b'null\n','literal prior null retained')
original={}
for row in snapshot['files']:
 n=row['relative_path']; original[n]=read(A/'source_snapshot'/n,row)
 ck(read(S/'original_archive'/n)==original[n],'V2 archival16 exact')
for n in ['verify.py','verification.json','source_checksums.json','source_record.json','turns.json','prior_report.json','review/independent_checks.py','review/independent_results.json','review/submitted_verify.py','review/submitted_results.json']:
 ck(read(S/'operative_proposal'/n)==original[n],'operative immutable exact')
ck(original['verify.py']==original['review/submitted_verify.py'] and original['verification.json']==original['review/submitted_results.json'],'duplicate114 equality')
gitargv=[]
for row in snapshot['files']: gitargv.extend([['git','show',HEAD+':'+row['path']],['git','ls-tree',HEAD,'--',row['path']]])
gitargv.append(['git','diff','--no-ext-diff','--no-textconv','--binary',BASE,HEAD,'--'])
specs=[('author/verify.py','verify.py'),('submitted_copy/submitted_verify.py','review/submitted_verify.py'),('historical_independent/independent_checks.py','review/independent_checks.py')]
cases=[]
for c,(private,orig) in zip(summary['complete_actual_helper_captures'],specs):
 source={'path':(A/'source_snapshot'/orig).relative_to(R).as_posix(),'bytes':len(original[orig]),'sha256':sha(original[orig])}; argv=['/usr/bin/python3','-B',str(A/'root_original_actual_reproduction'/private)]
 completed(c,'helper',argv,source,summary['actual_operator_pid']); ck(read(A/'root_original_actual_reproduction'/private)==original[orig],'actual private helper exact original')
 cases.append((c,'helper',argv,source))
for c,argv in zip(summary['complete_actual_Git_captures'],gitargv): completed(c,'git',argv,None,summary['actual_operator_pid']); cases.append((c,'git',argv,None))
ck(len(cases)==36 and len({c['pid'] for c,_,_,_ in cases})==36,'all36 real child identities')
for index,(c,kind,argv,source) in enumerate(cases):
 for key in c:
  bad=copy.deepcopy(c); del bad[key]; reject(bad,kind,argv,source,summary['actual_operator_pid'],f'{index}:missing:{key}')
 bad=copy.deepcopy(c); bad['extra']=True; reject(bad,kind,argv,source,summary['actual_operator_pid'],f'{index}:extra')
 for key,vs in {'schema':['other',None,True], 'argv':[None,'git',[],argv+['--mutated'],[True]],'cwd':[None,'/tmp'], 'actual_operator_pid':[True,0,-1,22446.0], 'pid':[True,0,-1,'1'], 'exit_code':[True,False,1,'0'], 'completed':[1,False,None], 'actual_execution':[1,False,None], 'stdin_supplied':[0,True,None], 'started_utc':[None,'2026-10-03T00:00:00','9999-01-01T00:00:00+00:00'], 'finished_utc':['2000-01-01T00:00:00+00:00','9999-01-01T00:00:00+00:00']}.items():
  for j,v in enumerate(vs):
   bad=copy.deepcopy(c); bad[key]=v; reject(bad,kind,argv,source,summary['actual_operator_pid'],f'{index}:bad:{key}:{j}')
 for key,vs in [('source',[None,{},source,True] if kind=='helper' else [{},cases[0][3],False]),('source_unchanged',[None,1,False] if kind=='helper' else [True,False,0])]:
  for j,v in enumerate(vs):
   if eq(v,c[key]): continue
   bad=copy.deepcopy(c); bad[key]=v; reject(bad,kind,argv,source,summary['actual_operator_pid'],f'{index}:class:{key}:{j}')
 for stream in ['stdout','stderr']:
  for key,v in [('bytes',True),('bytes',-1),('sha256','f'*64),('path','../bad'),('path','/etc/passwd'),('extra',0)]:
   bad=copy.deepcopy(c); bad[stream][key]=v; reject(bad,kind,argv,source,summary['actual_operator_pid'],f'{index}:{stream}:{key}:{v}')
rawaudit=load(read(A/'ROOT_COMPLETE_RAW_SQL_AUDIT.json'))
ck(rawaudit['full_raw_and_prior_bytes']==149266659 and rawaudit['all_SQL_rows']==15458 and len(rawaudit['complete_row_bindings'])==15458,'full derived rawSQL certificate')
ck(rawaudit['selected_prior_key_present'] is False and eq(rawaudit['selected_prior_fallback'],{}) and rawaudit['raw_null_present'] is False and rawaudit['literal_original_prior_file_value'] is None,'null not ABSENT{}')
ck(all(r['complete_payload_recursive_type_equal'] is True and r['complete_report_recursive_type_equal'] is True and r['ambiguous_code'] is False for r in rawaudit['complete_row_bindings']),'all15458 derived rows')
ck(len({r['key'] for r in rawaudit['complete_row_bindings']})==15458,'derivedrow uniqueness')
# New real read-only Git children: reproduce original bodies/modes/diff. No mathematical helper execution.
G=F/'READONLY_GIT_CHILDREN'; G.mkdir(exist_ok=False)
for i,(c,kind,argv,source) in enumerate(cases[3:]):
 D=G/str(i); D.mkdir(); rec={'argv':argv,'cwd':str(R),'operator_pid':os.getpid(),'started_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'stdin_supplied':False}
 with (D/'stdout.bin').open('xb') as out,(D/'stderr.bin').open('xb') as err:
  child=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=out,stderr=err,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0')); rec['pid']=child.pid; rec['exit_code']=child.wait(timeout=30)
 rec['finished_utc']=dt.datetime.now(dt.timezone.utc).isoformat(); rec['completed']=True
 for k in ['stdout','stderr']:
  b=(D/(k+'.bin')).read_bytes(); rec[k]={'path':(D/(k+'.bin')).relative_to(F).as_posix(),'bytes':len(b),'sha256':sha(b)}
 ck(rec['exit_code']==0 and (D/'stderr.bin').read_bytes()==b'','readonly Git actual success')
 ck((D/'stdout.bin').read_bytes()==checked(c['stdout']),'new readonly Git exact complete historical stream')
 (D/'CAPTURE.json').write_text(json.dumps(rec,indent=2)+'\n'); git_commands.append(rec)
# Full4096 permission predicate and actual private chmod control, including set-ID/sticky bits.
fixture=F/'private_mode_fixture'; fixture.write_bytes(b'own mode control\n')
for mode in range(4096):
 fixture.chmod(mode); observed=stat.S_IMODE(fixture.stat().st_mode)
 ck(observed==mode,'actual full mode survives chmod'); ck((observed==0o444)==(mode==0o444),'exact full0444 predicate')
fixture.chmod(0o644)
for mode in [True,False,-1,4096,'0444',None,292.0]: ck(not(type(mode) is int and 0<=mode<4096),'malformed fullmode')
for n in ['', '.', '..', './a', 'a/../b', '/a', 'a//b', 'a/', 'a\\b','a\0b','.git/x','__pycache__/a']:
 try: rel(n)
 except (AssertionError,ValueError): ck(True,'badpath'); continue
 raise AssertionError('bad path accepted '+repr(n))
T=F/'PRIVATE_TOPOLOGY'; T.mkdir(); (T/'file').write_bytes(b'own')
ck(tree(T)==({'file'},set()),'simple private topology'); (T/'empty').mkdir(); ck(tree(T)[1]=={'empty'},'extra empty detected'); (T/'empty').rmdir()
(T/'link').symlink_to('file')
try: tree(T)
except AssertionError: ck(True,'symlink rejected')
else: raise AssertionError('symlink accepted')
(T/'link').unlink(); os.mkfifo(T/'fifo')
try: tree(T)
except AssertionError: ck(True,'special rejected')
else: raise AssertionError('fifo accepted')
(T/'fifo').unlink()
# Actual macOS absent-only publication, including existing empty directory and symlink cases.
lib=ctypes.CDLL(None,use_errno=True); rename=lib.renamex_np; rename.argtypes=[ctypes.c_char_p,ctypes.c_char_p,ctypes.c_uint]; rename.restype=ctypes.c_int
E=F/'PRIVATE_RENAME'; E.mkdir(); src=E/'source'; src.mkdir(); (src/'file').write_bytes(b'own'); dest=E/'published'
ck(rename(os.fsencode(src),os.fsencode(dest),4)==0 and (dest/'file').read_bytes()==b'own' and not src.exists(),'absent-only publish success')
for name,kind in [('empty','dir'),('occupied','dir'),('file','file'),('symlink','symlink')]:
 target=E/name
 if kind=='dir': target.mkdir(); (target/'member').write_bytes(b'original') if name=='occupied' else None
 elif kind=='file': target.write_bytes(b'original')
 else: target.symlink_to('published')
 source=E/('source_'+name); source.mkdir(); (source/'member').write_bytes(b'own')
 ck(rename(os.fsencode(source),os.fsencode(target),4)==-1 and source.exists(),'RENAME_EXCL preserves existing destination')
 if kind=='symlink': target.unlink()
 elif kind=='file': target.unlink()
 elif name=='empty': target.rmdir()
 # occupied kept as own first-party fixture
for n in ['DRAFT_ROOT_READ_LEDGER.json','DRAFT_ROOT_SCIENCE_CARD.json','DRAFT_ROOT_CURRENT_INPUT_PREIMAGES.json','DRAFT_ROOT_EVIDENCE_BINDINGS.json','DRAFT_ROOT_NEW_SOURCE_ADVERSARY_RECORD.json']:
 o=load(read(S/n)); ck(o.get('approved_by_root',False) is False and o.get('reading_completed',False) is False,'draft not approval')
 if 'root_flags' in o: ck(all(v is False for v in o['root_flags'].values()),'allROOTflagsfalse')
ck(not (A/'reviewed_candidate').exists(),'actual candidate not fabricated')
for key in ['ROOT_reading_or_approval','actual_current_freeze_or_new_current_verdict','future_acceptance_approved','full_problem_solved','novelty_claimed','production_import_compile_or_execution','foreign_bodies_copied','old_SOURCE_V1_promoted','ADVERSE_promoted_to_clean_PASS']: ck(prep[key] is False,'closedSOURCEfuturegatefalse')
ck(prep['original_substantive_attempts']==1 and prep['turn_limit']==5 and prep['new_substantive_attempts']==0 and prep['audit_turns']==0,'typed source accounting')
# Preserve complete rows, never foreign raw or PDF/OCR bodies.
out={'schema':'pr47-source-v2-independent-private-controls/v1','created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_pid':os.getpid(),'assertions':count,'full_unique_reads':sorted(reads.values(),key=lambda r:r['path']),'unique_read_files':len(reads),'unique_read_bytes':sum(r['bytes'] for r in reads.values()),'malformed_capture_rejections':mutations,'genuine_helpers':3,'genuine_readonly_Git':33,'new_real_readonly_Git_children':git_commands,'all4096_logical_and_actual_modes':True,'production_import_compile_execution':False,'historical_math_helper_execution':False,'foreign_raw_SQL_PDF_OCR_body_copy':False,'future_acceptance_approved':False,'full_problem_solved':False}
(F/'PRIVATE_CONTROL_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['full_unique_reads','malformed_capture_rejections','new_real_readonly_Git_children']},indent=2))
