import pathlib, json, hashlib, stat, datetime, subprocess, os, sqlite3, collections
assert __debug__
r=pathlib.Path(__file__).resolve().parent;a=r.parent;repo=a.parents[2]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def pairs(v):
 d={}
 for k,x in v:
  assert k not in d, ('duplicate key',k)
  d[k]=x
 return d
def parse(b):return json.loads(b,object_pairs_hook=pairs,parse_constant=lambda v: (_ for _ in ()).throw(ValueError(v)))
def typed(x,y):
 assert type(x) is type(y), (type(x),type(y))
 if isinstance(x,dict):
  assert x.keys()==y.keys()
  for k in x:typed(x[k],y[k])
 elif isinstance(x,list):
  assert len(x)==len(y)
  for u,v in zip(x,y):typed(u,v)
 else:assert x==y,(x,y)
def full(p):
 s=p.lstat();assert stat.S_ISREG(s.st_mode) and not p.is_symlink();b=p.read_bytes();t=p.lstat();assert (s.st_mode,s.st_size,s.st_mtime_ns)==(t.st_mode,t.st_size,t.st_mtime_ns)
 return b,dict(path=str(p),bytes=len(b),sha256=sha(b),full_mode=stat.S_IMODE(s.st_mode))
def write(name,v):
 with (r/name).open('x') as f:json.dump(v,f,indent=2);f.write('\n')
source=pathlib.Path(__file__).read_bytes();gitrows=[]
def git(name,args):
 d=r/'readonly_git'/name;d.mkdir(parents=True,exist_ok=False)
 argv=['git']+args;start=now()
 (d/'PRELAUNCH.json').write_text(json.dumps(dict(argv=argv,cwd=str(repo),started_utc=start,pid=None,completed=False),indent=2)+'\n')
 (d/'prelaunch_operator.py').write_bytes(source)
 p=subprocess.Popen(argv,cwd=str(repo),stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=p.communicate();finish=now()
 (d/'stdout.bin').write_bytes(out);(d/'stderr.bin').write_bytes(err)
 rec=dict(argv=argv,cwd=str(repo),started_utc=start,finished_utc=finish,pid=p.pid,exit_code=p.returncode,operator_sha256=sha(source),stdout=dict(bytes=len(out),sha256=sha(out)),stderr=dict(bytes=len(err),sha256=sha(err)))
 (d/'CAPTURE.json').write_text(json.dumps(rec,indent=2)+'\n');gitrows.append(rec)
 assert p.returncode==0,(name,p.returncode,err)
 return out
mb,mref=full(a/'ORIGINAL_PREPARATION_MANIFEST.json');assert sha(mb)=='278e4fd39b5a13c7a181e3f7d494420c41ea4082fa8ab9add34229671a1be3b4';m=parse(mb)
assert m['files_count']==len(m['files'])==574 and m['self_excluded']==['ORIGINAL_PREPARATION_MANIFEST.json'] and mref['full_mode']==0o444
reads=[];objs={}
for row in m['files']:
 b,ref=full(a/row['path']);assert len(b)==row['bytes'] and sha(b)==row['sha256'] and ref['full_mode']==row['full_mode']==0o444
 reads.append(ref)
 if row['path'].endswith('.json'):objs[row['path']]=parse(b)
 elif row['path'].endswith('.jsonl'):
  for line in b.splitlines():
   if line.strip():parse(line)
actualdirs=[];actualfiles=[]
for name in m['authorship_directory_roots']:
 for p in (a/name).rglob('*'):
  assert not p.is_symlink(),p
  if p.is_dir():actualdirs.append(p.relative_to(a).as_posix())
  elif p.is_file():actualfiles.append(p.relative_to(a).as_posix())
  else:assert False,p
 actualdirs.append(name)
assert sorted(actualdirs)==m['owned_directories'] and len(actualdirs)==110
assert set(actualfiles)|set(m['authorship_root_files'])=={x['path'] for x in m['files']}
for row in m['owned_directory_bindings']:assert stat.S_IMODE((a/row['path']).lstat().st_mode)==row['full_mode']
capchecks=[]
for row in m['complete_prior_actual_captures']:
 c=objs[row['path']];d=(a/row['path']).parent
 assert c['pid']==row['pid'] and c['exit_code']==row['exit_code'] and c['argv']==row['argv']
 assert datetime.datetime.fromisoformat(c['started_utc'])<=datetime.datetime.fromisoformat(c['finished_utc'])
 for key in ['stdout','stderr']:
  b=(d/(key+'.bin')).read_bytes();assert len(b)==c[key]['bytes'] and sha(b)==c[key]['sha256']
 capchecks.append({'path':row['path'],'pid':c['pid'],'exit_code':c['exit_code'],'full_streams_verified':True})
assert len(capchecks)==103
outer=[]
for p in sorted((a/'original_preparation_closure_actual_capture').iterdir()):
 b,ref=full(p);assert ref['full_mode']==0o444;outer.append(ref)
assert len(outer)==6
cap=parse((a/'original_preparation_closure_actual_capture/CAPTURE.json').read_bytes());assert cap['operator_pid']==87064 and cap['pid']==87065 and cap['exit_code']==0
for key in ['stdout','stderr']:
 b=(a/'original_preparation_closure_actual_capture'/cap[key]['path']).read_bytes();assert len(b)==cap[key]['bytes'] and sha(b)==cap[key]['sha256']
assert sha((a/'original_preparation_closure_actual_capture/prelaunch_target.py').read_bytes())==cap['target_source']['sha256']==sha((a/'close_original_preparation.py').read_bytes())
assert sha((a/'original_preparation_closure_actual_capture/prelaunch_operator.py').read_bytes())==cap['operator_sha256']
snap=parse((a/'snapshot_manifest.json').read_bytes());head=snap['head'];base=snap['merge_base']
assert base=='60292bed09f59236aa192cb17aa138f7b4750e1a' and head=='e2e5c8c3e5ad218f867fa753c465bb96b3687bda'
science=[]
for i,row in enumerate(snap['files']):
 b,ref=full(a/'source_snapshot'/row['relative_path']);assert len(b)==row['bytes'] and sha(b)==row['sha256']
 actual=git('science_%02d_body'%i,['show',head+':'+row['path']]);assert actual==b
 tree=git('science_%02d_tree'%i,['ls-tree',head,'--',row['path']]).decode().strip().split();assert tree[:3]==[row['git_mode'],'blob',row['git_object']]
 science.append(ref)
diff=git('full_diff',['diff','--binary','--no-ext-diff',base,head,'--']);assert diff==(a/'original_diff.patch').read_bytes() and len(diff)==80679 and sha(diff)=='994b4bbd4993227d1100cbd9d7493de776c6619c9daa379dca7f4ef3b3a26698'
chunks=diff.split(b'diff --git ')[1:];assert len(chunks)==18
for c in chunks[1:]:
 ls=c.splitlines(keepends=True);path=ls[0].decode().strip().split(' b/',1)[1];rel=path.split('/attempts/2961/')[1];j=next(i for i,v in enumerate(ls) if v.startswith(b'@@ '));assert b''.join(v[1:] for v in ls[j+1:])==(a/'source_snapshot'/rel).read_bytes()
ledger=[parse(x) for x in (a/'source_snapshot/turns.jsonl').read_bytes().splitlines()];assert len(ledger)==2 and [x['turn'] for x in ledger]==[1,2]
# Independent raw/SQLite type audit, in place; never copies foreign bodies.
c=repo/'unsolved_math_prioritization';rawrefs=[]
for p in [c/'cache/problems.json',c/'cache/research_results.json',c/'cache/catalog.sqlite']:
 b,ref=full(p);rawrefs.append(ref)
 if p.name=='problems.json':problems=parse(b)
 elif p.name=='research_results.json':reports=parse(b)
rawmap={str(p['id']):p for p in problems};assert len(rawmap)==len(problems)==15458
assert all(type(p['id']) is int and type(p['problem_number']) is str for p in problems)
counts=collections.Counter(p['problem_number'] for p in problems)
db=sqlite3.connect((c/'cache/catalog.sqlite').as_uri()+'?mode=ro&immutable=1',uri=True)
sqlrows=[]
for key,payload,report in db.execute('SELECT key,payload,report FROM records ORDER BY key'):
 p=parse(payload);expected=dict(rawmap[key]);code=p['problem_number']
 ambiguous=counts[code]>1 and code in reports
 if ambiguous:expected['_ambiguous_report']=True
 typed(p,expected);v=parse(report);typed(v,{} if ambiguous else reports.get(code,{}))
 sqlrows.append({'key':key,'payload_bytes':len(payload.encode()),'payload_sha256':sha(payload.encode()),'report_bytes':len(report.encode()),'report_sha256':sha(report.encode()),'recursive_type_identity_verified':True})
revision=db.execute('SELECT revision FROM metadata').fetchall();db.close();assert len(sqlrows)==15458
selected=[]
for key,code,name in [('2961','KP-4.85','source_record.json'),('30004403','OWR-17471-009','related_source_record.json')]:
 p=parse((a/'source_snapshot'/name).read_bytes());typed(p,rawmap[key]);assert p['id']==int(key) and code not in reports
 selected.append({'key':key,'integer_source_id':p['id'],'plain_original_problem_typed_equal_raw':True,'raw_report_key_present':False,'raw_report_null_present':False,'sqlite_report_literal':'{}','original_prior_report_file_exists':False})
fresh=parse((r/'FRESH_PRIMARY_SOURCE_BINDINGS.json').read_bytes())['sources'];old=parse((a/'source_snapshot/source_checksums.json').read_bytes());assert [(x['url'],x['sha256'],x['bytes']) for x in fresh]==[(x['url'],x['sha256'],x['bytes']) for x in old]
write('ORIGINAL_COMPLETE_INDEPENDENT_AUDIT.json',dict(schema='pr48-smooth-geometry-complete-original-independent-audit/v1',created_utc=now(),actual_pid=os.getpid(),original_manifest=mref,closed_original_payload_reads=reads,closed_original_files_count=575,exact_directory_topology_verified=True,directories=110,full_prior_captures_verified=capchecks,external_actual_original_closure_reads=outer,external_actual_original_closure=cap,science_full_reads=science,readonly_git_commands=gitrows,full_diff_bytes=80679,full_diff_sha256=sha(diff),diff_paths=18,all17science_hunks_equal=True,original_substantive_turns=2,turn_limit=5,new_substantive_turns=0,audit_turn_charge=0,raw_in_place_full_reads=rawrefs,sqlite_rows_type_checked=sqlrows,sqlite_revision=revision,selected_raw_semantics=selected,five_primary_body_hashes_freshly_authenticated=True,old_runtime_and_review_attributions_remain_dated=True,current_mathematical_acceptance=False,foreign_raw_copies=False))
assert pathlib.Path(__file__).read_bytes()==source
print(json.dumps({'status':'PASS_COMPLETE_READ_REPROVENANCE_ONLY','original_payloads':574,'external_closure_files':6,'science':17,'readonly_git_children':len(gitrows),'sql_rows':15458,'original_turns':'2/5','five_fresh_primary_hashes_match':True,'math_acceptance':False}))
