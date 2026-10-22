import pathlib,sys,hashlib,json,subprocess,shutil,datetime
W=pathlib.Path('/Users/alec/Documents/Math');P=W/'draft_pr_claimed_solved_900_1000_20261012';A=P/'audits/pr967_2616';R=A/'reviews/closure_package_adversary_02';T=R/'private/engineering/program';O=T/'audits/pr967_2616/closure_engineering_02';O.mkdir(parents=True,exist_ok=True)
def sha(b):return hashlib.sha256(b).hexdigest()
def checked(p,h):
 b=p.read_bytes()
 if sha(b)!=h:raise RuntimeError('initial source pin '+str(p))
 return b
cp='4a9a273e37d43b7d987dea29319aaa4ca70f14432e6bafb568ee5f6af9130c88';wp='59f46a1f29140fc2018f9bb10ea3f2989dbaf0313ab33acf32f02ba05b787533';tp='d183e3a5c25c26dc55ab4aba68fb4b624566606b516a0d5bd991ca3317e47fe5';fp='1a8225a4e40c1ce509f7c48390fb30e10934b982fab60b3345269d1cfe90f118'
for n,h in [('close_pr967.py',cp),('finalize_pr967_and_gate_next.py',wp)]: (T/n).write_bytes(checked(P/n,h))
for n,h in [('test_offline.py',tp),('test_finite_json.py',fp)]: (O/n).write_bytes(checked(A/'closure_engineering_02'/n,h))
shutil.copytree(A/'original',O.parent/'original',dirs_exist_ok=True)
for n in ['ORIGINAL_FILE_RECORDS.json','source_record_private.txt']:shutil.copy2(A/n,O.parent/n)
loader='import pathlib,hashlib,sys; p=pathlib.Path(sys.argv.pop(1)); expected=sys.argv.pop(1); raw=p.read_bytes();\nif hashlib.sha256(raw).hexdigest()!=expected: raise RuntimeError("external initial source authentication failed")\nsys.argv[0]=str(p); exec(compile(raw,str(p),"exec",dont_inherit=True,optimize=sys.flags.optimize),{"__name__":"__main__","__file__":str(p)})'
rows=[]
for mode,flags in [('normal',[]),('O',['-O']),('OO',['-OO'])]:
 for name,h,args in [('OFFLINE',tp,['--core-sha256',cp,'--wrapper-sha256',wp]),('FINITE',fp,['--core',str(T/'close_pr967.py'),'--core-sha256',cp,'--wrapper',str(T/'finalize_pr967_and_gate_next.py'),'--wrapper-sha256',wp,'--test-sha256',fp])]:
  path=O/('test_offline.py'if name=='OFFLINE'else'test_finite_json.py');cmd=[sys.executable,'-I','-S','-B',*flags,'-c',loader,str(path),h,*args];start=datetime.datetime.now(datetime.timezone.utc).isoformat();p=subprocess.run(cmd,capture_output=True,timeout=180)
  base=name+'_'+mode
  for ext,b in [('stdout.raw',p.stdout),('stderr.raw',p.stderr)]: (R/(base+'.'+ext)).write_bytes(b)
  row={'mode':mode,'suite':name,'started_utc':start,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'returncode':p.returncode,'initial_authentication':'unconditional trusted loader before compile, actual outer optimization','source_sha256':h,'helper_sha256':[cp,wp],'stdout':{'bytes':len(p.stdout),'sha256':sha(p.stdout)},'stderr':{'bytes':len(p.stderr),'sha256':sha(p.stderr)}}
  if p.returncode==0:
   o=json.loads(p.stdout);row.update(event_count=o['event_count'],status=o['status'],actual_optimization=o['outer_optimization'])
  (R/(base+'.launch.json')).write_text(json.dumps(row,indent=2)+'\n');rows.append(row);print(json.dumps(row),flush=True)
(R/'ENGINEERING_REPRODUCTIONS.json').write_text(json.dumps(rows,indent=2)+'\n')
