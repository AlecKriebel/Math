"""Unexecuted ROOT-only checkpoint SOURCE; copy unchanged after personal review."""
from pathlib import Path, PurePosixPath
import datetime as dt, hashlib, json, os, shutil, stat, subprocess, sys
P=Path('/Users/alec/Documents/Math/draft_pr_publication_program_20260930');R=P.parent;T=P/'checkpoints/checkpoint_20261003_1023_preparation'
A={n:P/'audits'/s for n,s in [(45,'pr45_9900007'),(47,'pr47_2849'),(48,'pr48_2961'),(49,'pr49_30000703'),(50,'pr50_10600042'),(51,'pr51_30000166')]}
SELF=Path(__file__).absolute();C=P/'checkpoints/CHECKPOINT_20261003_1023_V2.json';names=set();closures=[];caps=[];LIMIT=400*1024*1024
def sha(b):return hashlib.sha256(b).hexdigest()
def duplicate_free(pairs):
 d={}
 for k,v in pairs:assert k not in d;d[k]=v
 return d
def load(p):return json.loads(p.read_bytes(),object_pairs_hook=duplicate_free)
def git(*args):return subprocess.check_output(['git',*args],cwd=R)
def mode(p):return stat.S_IMODE(p.lstat().st_mode)
def safe(p):
 assert p.is_relative_to(R) and not p.is_symlink() and all(not q.is_symlink() for q in p.parents)
 assert stat.S_ISREG(p.lstat().st_mode)
def row(p):
 safe(p);s=p.stat();h=hashlib.sha256();g=hashlib.sha1();g.update(('blob '+str(s.st_size)+'\0').encode())
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b);g.update(b)
 assert p.stat().st_size==s.st_size and mode(p)==stat.S_IMODE(s.st_mode)
 return dict(path=p.relative_to(R).as_posix(),bytes=s.st_size,sha256=h.hexdigest(),full_mode=mode(p),git_mode='100755' if mode(p)&0o111 else '100644',git_blob_sha1=g.hexdigest())
ART={str(A[50]/'publication_package_v1/even_strand_markov.pdf'):(58971,'ea3e6f6b647de0acd71219a2840ee515fe6548f7d4dbba828558b7fb0e01624e'),str(A[50]/'publication_package_v1/even-strand-markov-verification-v1.zip'):(19128,'2b519b4ba59ccd2e5ed9c88a79aa96d273481b45bb18b6a1ecc6fcbd0381a48d')}
def add(p):
 safe(p);assert p.stat().st_size<100*1024*1024
 if str(p) in ART:
  z=row(p);assert (z['bytes'],z['sha256'])==ART[str(p)]
 else:assert p.suffix.lower() not in {'.pdf','.zip','.db','.sqlite','.png','.jpg','.jpeg','.gif','.webp','.pyc'}
 names.add(p.relative_to(R).as_posix())
def tree(d,exclude=()):
 assert d.is_dir() and not d.is_symlink()
 for p in d.rglob('*'):
  rel=p.relative_to(d)
  if any(s in rel.parts for s in exclude):continue
  assert not p.is_symlink()
  if p.is_file():add(p)
def norm_mode(v):return int(v,8) if isinstance(v,str) else v
def closed(n,folder,mf,h,schema,count):
 d=(R/'unsolved_math_prioritization/attempts/2849') if n==0 else A[n]/folder;p=d/mf
 assert sha(p.read_bytes())==h;m=load(p);assert m['schema']==schema;rows=m['files']
 assert len(rows)==count==m.get('files_count',m.get('payload_file_count'));seen=set()
 for z in rows:
  s=z['path'];pp=PurePosixPath(s);assert s==pp.as_posix() and not pp.is_absolute() and '..' not in pp.parts and s not in seen and s!=mf;seen.add(s)
  q=d/s;a=row(q);assert type(z['bytes']) is int and (a['bytes'],a['sha256'])==(z['bytes'],z['sha256'])
  assert a['full_mode']==norm_mode(z.get('full_mode',z.get('mode',0o444)))==0o444
 assert {q.relative_to(d).as_posix() for q in d.rglob('*') if q.is_file()}==seen|{mf}
 assert mode(p)==0o444 and not any(q.is_symlink() for q in d.rglob('*'))
 dirs={'.'}|{q.relative_to(d).as_posix() for q in d.rglob('*') if q.is_dir()};dm={s:mode(d/s) for s in dirs}
 default=0o555 if (n,folder) in {(50,'preprint_v1_adversary_family'),(51,'eta_algebra_adversary_family'),(51,'modular_geometry_adversary_family')} else 0o755
 expected_dm={s:default for s in dirs}
 if (n,folder)==(48,'acceptance_source_adversary_family_v2_fresh'):
  for s in ('fixed_custody_actual_capture','fixed_custody_v2_actual_capture','fixed_custody_v3_actual_capture','private_controls_actual_capture'):expected_dm[s]=0o700
 assert dm==expected_dm
 declared=m.get('directories',m.get('relative_directories'))
 if declared is not None:
  ds={('.' if (z.get('path','.') if isinstance(z,dict) else z) in ('','.') else (z['path'] if isinstance(z,dict) else z)) for z in declared};assert ds in (dirs,dirs-{'.'})
  for z in declared:
   if isinstance(z,dict):assert norm_mode(z.get('full_mode',z.get('mode',dm[z['path'] or '.'])))==dm[z['path'] or '.']
 if 'directory_full_modes' in m:assert {z['path']:norm_mode(z['full_mode']) for z in m['directory_full_modes']}==dm
 excluded=m.get('self_excluded',m.get('manifest_excludes_only_itself'))
 assert excluded in (mf,[mf]) or (type(excluded) is int and excluded==1 and n==49) or (excluded is None and m.get('self_excluded_count')==1) or (excluded==[dict(path=mf,mode='0o444')] and n==51 and folder=='eta_algebra_adversary_family')
 closures.append(dict(path=p.relative_to(R).as_posix(),sha256=h,payload_files=count,files_full_mode='0444',complete_directory_full_modes=dm));tree(d)
def cap(d):
 assert {p.name for p in d.iterdir()}=={'CAPTURE.json','prelaunch_operator.py','stdout.bin','stderr.bin'}
 c=load(d/'CAPTURE.json');assert c['schema']=='root-explicit-command-capture/v1' and c['actual_execution'] is True and c['completed'] is True and c['operator_unchanged'] is True
 assert type(c['pid']) is int and c['pid']>0 and type(c['exit_code']) is int and c['cwd']==str(R) and isinstance(c['argv'],list) and all(isinstance(s,str) for s in c['argv'])
 assert type(c['expected_exit_code']) is int and c['status'] in ('PASS','FAIL') and (c['status']=='PASS')==(c['exit_code']==c['expected_exit_code'])
 start=dt.datetime.fromisoformat(c['started_utc']);end=dt.datetime.fromisoformat(c['finished_utc']);assert start.utcoffset()==end.utcoffset()==dt.timedelta(0) and start<=end<=dt.datetime.now(dt.timezone.utc)
 assert c['operator_sha256']==sha((d/'prelaunch_operator.py').read_bytes())=='c1ae969ccbbc48ed6fb486e96184da94329291a46b27d2b891ecb87185c909ec'
 for k in ('stdout','stderr'):
  z=c[k];assert z['path']==k+'.bin' and type(z['bytes']) is int;b=(d/z['path']).read_bytes();assert (len(b),sha(b))==(z['bytes'],z['sha256'])
 caps.append(dict(path=(d/'CAPTURE.json').relative_to(R).as_posix(),sha256=sha((d/'CAPTURE.json').read_bytes()),actual_pid=c['pid'],exit_code=c['exit_code'],status=c['status'],started_utc=c['started_utc'],finished_utc=c['finished_utc']));tree(d);return c
def index(raw):
 out={}
 for z in raw.split(b'\0'):
  if not z:continue
  m,p=z.split(b'\t',1);gm,oid,stage=m.decode().split();n=p.decode();assert stage=='0' and n not in out;out[n]=(gm,oid)
 return out
def foreign_modes(table):
 out={}
 for n in table:
  if n in names:continue
  q=R/n
  try:s=q.lstat();out[n]=dict(full_mode=stat.S_IMODE(s.st_mode),kind=stat.S_IFMT(s.st_mode),link=os.readlink(q) if stat.S_ISLNK(s.st_mode) else None)
  except FileNotFoundError:out[n]=None
 return out
def foreign_dirty():
 out=[]
 for n in git('diff','--name-only','-z').decode().split('\0'):
  if not n or n in names:continue
  q=R/n
  if not q.exists() and not q.is_symlink():out.append(dict(path=n,absent=True));continue
  s=q.lstat();b=os.fsencode(os.readlink(q)) if stat.S_ISLNK(s.st_mode) else q.read_bytes();out.append(dict(path=n,bytes=len(b),sha256=sha(b),full_mode=stat.S_IMODE(s.st_mode),kind=stat.S_IFMT(s.st_mode)))
 return sorted(out,key=lambda z:z['path'])
def selected_queue_row(b):
 matches=[line for line in b.splitlines(keepends=True) if len(line.split(b'|'))>2 and line.split(b'|')[2].strip().split(b'/')[0].strip()==b'2849']
 assert len(matches)==1;return matches[0]
def check_current_queue():
 assert row(R/queue)==fresh_queue and git('rev-parse','HEAD').decode().strip()==head and git('show','HEAD:'+queue)==(R/queue).read_bytes()==fresh_queue_bytes
assert __debug__ and SELF==P/'checkpoints/checkpoint_20261003_1023_v2.py' and SELF.read_bytes()==(T/'checkpoint_20261003_1023_v2.py').read_bytes() and len(sys.argv)==1
failed_path=A[45]/'root_completed_findings_checkpoint_1023_actual_capture/CAPTURE.json'
assert sha(failed_path.read_bytes())=='9a9b4abaf7be1a10d21087dcfe4e1ebf60cc016cd8e2d12fc5903b1934e4cdd2';failed=load(failed_path);assert failed['pid']==4763 and failed['status']=='FAIL' and failed['exit_code']==1 and failed['stdout']['bytes']==0 and failed['stderr']['bytes']==318
assert sha((P/'checkpoints/checkpoint_20261003_1023.py').read_bytes())=='7eed2fbb8be0af59af79dba03fa3f123f484e4cd36ccaf00415e86b1a3cbc76a'
assert git('branch','--show-current')==b'main\n' and not git('diff','--cached','--name-only') and not C.exists();os.umask(0o022)
head=git('rev-parse','HEAD').decode().strip();initial_raw=git('ls-files','--stage','-z');before=index(initial_raw);head_tree=git('ls-tree','-r','-z','HEAD')
postp=A[47]/'ROOT_ACTUAL_POST_INSPECTION.json';assert sha(postp.read_bytes())=='89924d5de705c8465ab75f872201b1b8a004c4ebc3c092f3c95bfc17f97777ab';post=load(postp)
assert len(post)==22 and post['schema']=='pr47-root-complete-actual-post-inspection/v1' and post['status']=='PASS' and post['completed_primary_prs']==37 and post['original_attempts']==1 and post['audit_turns']==post['new_substantive_attempts']==0 and post['full_problem_solved'] is False
assert sha((A[47]/'root_complete_actual_post_inspection_capture/CAPTURE.json').read_bytes())=='8df3d6fcf7cc57697096cefca0cd5b838501c69f527cf2f5e539baa63f0c7143';pc=cap(A[47]/'root_complete_actual_post_inspection_capture');assert pc['pid']==74925 and pc['exit_code']==0
assert len(post['current13'])==13 and len({z['path'] for z in post['current13']})==13
queue='unsolved_math_prioritization/QUEUE.md';dated_queue=git('show',post['entire_post']['merge_commit']+':'+queue)
assert sha(dated_queue)=='04187ab3fc4c1be7ec56635f760658be1709cb1bfa28f7a7a59f3924c8a9670c'
for z in post['current13']:
 q=R/z['path'];a=row(q);assert a['full_mode']==z['worktree_mode']==0o644
 if z['path']==queue:assert (len(dated_queue),sha(dated_queue))==(z['bytes'],z['sha256'])
 else:assert (a['bytes'],a['sha256'])==(z['bytes'],z['sha256'])
fresh_queue_bytes=(R/queue).read_bytes();fresh_queue=row(R/queue);assert selected_queue_row(dated_queue)==selected_queue_row(fresh_queue_bytes)
check_current_queue();assert subprocess.run(['git','merge-base','--is-ancestor',post['entire_post']['merge_commit'],head],cwd=R).returncode==0
assert load(P/'inventory.json')['completed_count']==37
for args in [
 (0,'','MANIFEST.json','94bec9448f41dcb1b2421d4f60f11087051871802cac11bd2e277684b204ef3c','pr47-accepted-strict-self-excluding-closure/v1',1339),
 (47,'acceptance_preparation_family','PREPARATION_MANIFEST.json','1a10442d9962db99c608412f53fef754870bfadf24fd76e7e899112fc38ebef1','pr47-acceptance-source-closure/v1',126),
 (47,'acceptance_source_adversary_family','SELF_MANIFEST.json','a4c15b8bc831c71b61e0b6d830904813519eab147d1c7bd1d96987b2e98c0222','pr47-acceptance-source-adversary-self-only-closure/v1',85),
 (47,'reviewed_candidate','MANIFEST.json','a7d1acc9dbbf8cd5435d0bebd8f6b1a540ecb0f2aea8d0c616c46bc5bf6b4ea5','PR47_STRICT_CURRENT_PACKET_v1',1328),
 (47,'current_whole_adversary_family','MANIFEST.json','658133399198e8528aa2a45b89c87a19f3b69edd6998b86b7e8227c850f5fd78','pr47-whole-current-independent-self-only-closure/v1',385),
 (48,'acceptance_preparation_family_v2','PREPARATION_MANIFEST.json','48ddcccb22eb898c42598278fa4914d84fa0da640e098973a1e70d7c60577662','pr48-acceptance-source-closure/v2',70),
 (48,'acceptance_source_adversary_family_v2_fresh','SELF_MANIFEST.json','9f9e9d0226f4cf1bb4439e46cf7ecfa7469ca1d4da52785569b96767eb2298a3','pr48-v2-fresh-source-adversary-closure/v1',60),
 (49,'current_whole_adversary_family','SELF_MANIFEST.json','b3d91982e7a2cfbda0ffce7fe0e45141dabafcb374aecd52078ad3d66a1e9736','pr49-current-whole-adversary-self-only-closure/v2',127),
 (50,'preprint_v1_adversary_family','SELF_MANIFEST.json','80dfd0470f135332a245535dbdfdff0090b753eb6008a0ab9fa4fc9331fdc4bd','pr50-preprint-v1-adversary-self-only-closure/v1',21),
 (50,'preprint_v1_second_adversary_family','SELF_MANIFEST.json','99adb0dd1cd09e46316521a214c5b1b96f0c11c1c78ff8c5700265c1156f4cb0','pr50-second-adversary-self-only-closure/v1',30),
 (51,'original_preparation_family','SELF_MANIFEST.json','d358945982e92b1e3fc121cbdf54664304f6ae6118375f3fb1da8c590d75e57d','pr51-original-preparation-self-only-manifest/v1',188),
 (51,'eta_algebra_adversary_family','SELF_MANIFEST.json','dc8d2d207850534823110c9eff6055ad30d0b21fc0ec84d82a74f27b4475453b','pr51-eta-algebra-adversary-self-only-closure/v1',23),
 (51,'modular_geometry_adversary_family','SELF_MANIFEST.json','29a9e737671999b864e02364a6a3f47f584f2b4d5c13cb41b230f14632e05ac6','pr51-modular-geometry-adversary-self-only-closure/v1',35),
 (51,'current_preparation_family','SELF_MANIFEST.json','7ece84cf8366514b959b867aa95b690931a94ae3e8e1ce1ef14089a399f70844','pr51-current-preparation-self-only-manifest/v1',58)]:closed(*args)
tree(A[47]);tree(A[49],('acceptance_preparation_family','acceptance_preparation_family_v2','acceptance_source_adversary_family_v2_fresh','__pycache__'))
for folder in ('original','captures','priority_adversary_family','classical_markov_adversary_family','virtual_markov_priority_adversary_family','preprint_v1','publication_package_v1','publication_operations'):tree(A[50]/folder,('__pycache__',))
for n in (50,51):
 for p in A[n].iterdir():
  if p.is_file():add(p)
for d in A[45].glob('root*'):
 if d.is_dir() and (d/'CAPTURE.json').is_file():
  c=load(d/'CAPTURE.json')
  if c.get('schema')=='root-explicit-command-capture/v1' and c.get('started_utc','')>='2026-10-03T09:42:00':cap(d)
for p in [SELF,T/'checkpoint_20261003_1023_v2.py',T/'REPORT_V2.md',P/'checkpoints/checkpoint_20261003_1023.py',T/'checkpoint_completed_findings.py',T/'REPORT.md',P/'inventory.json',R/'unsolved_math_prioritization/state.json',R/'unsolved_math_prioritization/history.jsonl']:add(p)
logs=[P/'RESEARCH_LOG.md',*[A[n]/'ROOT_RESEARCH_LOG.md' for n in (47,48,49,50,51)]]
for p in logs:
 if p.exists():safe(p);assert mode(p)==0o644;add(p)
 else:assert p==A[51]/'ROOT_RESEARCH_LOG.md';names.add(p.relative_to(R).as_posix())
assert queue not in names and not any('/audits/pr52_' in n or '/acceptance_preparation_family_v3/' in n or '/submission_final_adversary_family/' in n or any('/pr49_30000703/'+s+'/' in n for s in ('acceptance_preparation_family','acceptance_preparation_family_v2','acceptance_source_adversary_family_v2_fresh')) for n in names) and all(p.relative_to(R).as_posix() not in names for p in T.glob('historical_source_v*.py'))
foreign=foreign_dirty();fm=foreign_modes(before);assert len([z for z in foreign if z['path'].startswith('paper_ii_simultaneous_amplification_referee_audit_2026-08-22/logs/')])==2
check_current_queue();assert shutil.disk_usage(P).free>=LIMIT and git('rev-parse','HEAD').decode().strip()==head and not git('diff','--cached','--name-only')
utc=dt.datetime.now(dt.timezone.utc).isoformat();old_logs=[dict(path=p.relative_to(R).as_posix(),bytes=p.stat().st_size if p.exists() else 0,sha256=sha(p.read_bytes()) if p.exists() else sha(b''),absent_before=not p.exists()) for p in logs]
note=('\n'+utc+' — ROOT checkpoint V2: failed original4763 2026-10-03T10:57:35.884706–10:57:36.710664 UTC exit1 before logs/staging, full318-byte stderr retained. Dated ROOT review at main d1df0d99d5ffe56f771cac3819774896474dcdea found only legitimate foreignPR372 row9700034 Status/Turns queued0/5->unsolved5/5 after accepted47 merge; runtime permits committed foreign queue updates only while accepted2849 row remains byte-exact and the entire current QUEUE matches fresh HEAD, all other12 dated native bodies/modes exact. Scientific/preparation status below is the dated2026-10-03T10:55:17 UTC snapshot; live runtime gates and native37 remain separately checked. ROOT checkpoint37/180=20.555555555555557%, next48. PR47 UNSOLVED1/5, new0/audit0; accepted partial only, no paper. Actual six acceptance phases passed and complete ROOT post74925 PASS10:20:31–10:21:00, exact22-key89924d5d...; other12 native files match the dated post; full0644 current QUEUE and accepted2849 row are separately qualified against dated source and fresh HEAD. PR48 closed V2 SOURCE70+self and new independent adverse60+self actual76512/77465 retained: M2 correction remains operationally pending, V3 SOURCE53+self ROOT97743 closed (MF9c525f7b540068af07477e8f794e21596d93e69e49e8dbc52972d3196eb9fda4), excluded while fresh source adversary is pending; scientific shared2/5 partial unchanged. PR49 credited2007 theorem already_solved0/5, no paper; current WHOLE127+self and ROOT42814 reconciliation completed, both acceptance SOURCE preparations and fresh source adversary excluded. PR50 two actually closed clean preprint reviews21/30+self retained; third final review75+self actually ROOT closed87623/read97362 (MF1d3b52bef763bf0e9c8f2c6e8ae63f22e37149030226c30e8765184b8287a336), retained outside this checkpoint scope; final4-page PDF58971 and verificationZIP19128 exact hashes checked, local submission/tool validation ready, checkpoint confers no publication authority; no DOI/upload/tracker claim. PR51 credited prior all-N result already_solved; two independent scientific families23/35+self actually closed clean, original188+self and current58+self ROOT81014/81691 closed/readback completed; current is SOURCE only, no native acceptance/production approval. PR52 original194+self now ROOT closed/read back but omitted here; both new independent mathematical reviews actually ROOT closed/read back10:54:44–10:55:17 UTC exit0: divergence27+self2468/2863 MF5bcf514d64da5d3de4bd8b21247f8258ed406584db71b8105655e60639170886 and nilpotent25+self2475/2865 MF64e5170cf0692357c61fb98f3c494d2e07cd6bba9fa859a637bd595b4db1faa8; whole52 remains excluded. No original budgets/turns changed, new0/audit0; no invented source-response count. Dated ROOT report: bad-slash outer helper invocation failed before any child launch; no actual child CAP exists for that invocation and no PID is manufactured. Actual ROOT regenerable npm download-cache purge84994 10:33:16–10:33:18 retained in its full CAP4; no research/installed packages removed, free space separately checked at runtime. Dated ROOT tool-history report: verified regular regenerable Homebrew download-cache cleanup discarded365789966 bytes, observed489828352 bytes free after; no installed packages/research deletion, no certified deleted-file count, no CAP/PID inferred for rejected prelaunch attempts. Foreign descending-program work and two unrelated paper logs preserved. Goal active; acceptance20.5556%, PR47workflow100%, PR48operationalrepair pending, PR49current100%, PR50publication0%, PR51source100%. No release or external outreach.\n')
for p in logs:
 with p.open('a',encoding='utf-8') as f:f.write(note);f.flush();os.fsync(f.fileno())
 assert mode(p)==0o644
rows=[row(R/n) for n in sorted(names)];changes={z['path'] for z in rows if before.get(z['path'])!=(z['git_mode'],z['git_blob_sha1'])};assert sum(z['bytes'] for z in rows if z['path'] in changes)<LIMIT
record=dict(schema='ROOT_completed_owned_checkpoint/v6',utc=utc,actual_pid=os.getpid(),source_sha256=sha(SELF.read_bytes()),main_before=head,completed37of180_percent=37/180*100,current_pr=48,actual47_post_sha256=sha(postp.read_bytes()),dated_shared_QUEUE_qualification=True,dated_QUEUE=dict(path=queue,git_commit=post['entire_post']['merge_commit'],bytes=len(dated_queue),sha256=sha(dated_queue)),entire_current_QUEUE=dict(**fresh_queue,git_commit=head,selected2849_row_utf8=selected_queue_row(fresh_queue_bytes).decode(),selected2849_row_sha256=sha(selected_queue_row(fresh_queue_bytes))),retained_failed_checkpoint_CAP4=dict(path=failed_path.relative_to(R).as_posix(),sha256=sha(failed_path.read_bytes()),actual_pid=4763,started_utc=failed['started_utc'],finished_utc=failed['finished_utc'],exit_code=1,before_logs_and_staging=True),completed_closures=closures,completed_ROOT_CAP4=caps,owned_files_excluding_receipt=rows,foreign_tracked_dirty=foreign,foreign_index_path_count=len(fm),foreign_full_mode_snapshot_sha256=sha(json.dumps(fm,sort_keys=True).encode()),initial_entire_index_sha256=sha(initial_raw),initial_HEAD_tree_sha256=sha(head_tree),log_prefixes_before=old_logs,QUEUE_staged_by_this_checkpoint=False,active_families_included=False,publication_approved=False,staging_success_claimed_in_this_pre_stage_record=False,new_changed_payload_bytes=sum(z['bytes'] for z in rows if z['path'] in changes),payload_bound_is_not_physical_Git_space_estimate=True)
with C.open('x',encoding='utf-8') as f:json.dump(record,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
add(C);cr=row(C);rows.append(cr);changes.add(cr['path']);check_current_queue();assert shutil.disk_usage(P).free>=LIMIT and git('rev-parse','HEAD').decode().strip()==head and not git('diff','--cached','--name-only')
check_current_queue();assert foreign_dirty()==foreign and foreign_modes(before)==fm
subprocess.run(['git','add','-f','--pathspec-from-file=-','--pathspec-file-nul'],cwd=R,input=b''.join(n.encode()+b'\0' for n in sorted(changes)),check=True)
after_raw=git('ls-files','--stage','-z');after=index(after_raw);expected=dict(before)
for z in rows:expected[z['path']]=(z['git_mode'],z['git_blob_sha1']);assert row(R/z['path'])==z
assert after==expected and {n for n in git('diff','--cached','--name-only','-z').decode().split('\0') if n}==changes
check_current_queue();assert queue not in changes and foreign_dirty()==foreign and foreign_modes(after)==fm and git('rev-parse','HEAD').decode().strip()==head and git('ls-tree','-r','-z','HEAD')==head_tree and git('branch','--show-current')==b'main\n'
print(json.dumps(dict(status='PASS_EXACT_COMPLETED_OWNED_STAGE',actual_pid=os.getpid(),source_sha256=sha(SELF.read_bytes()),main_before=head,owned_files=len(names),staged_changed_files=len(changes),changed_paths_sha256=sha(b''.join(n.encode()+b'\0' for n in sorted(changes))),entire_post_stage_index_sha256=sha(after_raw),foreign_tracked_dirty_preserved=len(foreign),foreign_HEAD_index_worktree_modes_preserved=len(fm),completed_count=37,completion_percent=37/180*100,dated_shared_QUEUE_qualified=True,current_QUEUE_sha256=fresh_queue['sha256'],QUEUE_staged=False,publication_approved=False)))
