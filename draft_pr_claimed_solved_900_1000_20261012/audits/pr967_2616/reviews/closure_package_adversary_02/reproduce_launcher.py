import pathlib,hashlib,subprocess,sys,json,os,shutil,datetime,ast
W=pathlib.Path('/Users/alec/Documents/Math');P=W/'draft_pr_claimed_solved_900_1000_20261012';A=P/'audits/pr967_2616';R=A/'reviews/closure_package_adversary_02';S=R/'private/launcher';S.mkdir(parents=True,exist_ok=True)
def sha(b):return hashlib.sha256(b).hexdigest()
def need(ok,m):
 if not ok:raise RuntimeError(m)
source=(A/'ROOT_TRUSTED_CLOSURE_LAUNCHER.py').read_bytes();need(sha(source)=='69fc93f82639e7c01d570115bb0bd92873966e81cbe93822a5fabdbe4c62757e','external launcher pin')
pins={'close_pr967.py':'4a9a273e37d43b7d987dea29319aaa4ca70f14432e6bafb568ee5f6af9130c88','finalize_pr967_and_gate_next.py':'59f46a1f29140fc2018f9bb10ea3f2989dbaf0313ab33acf32f02ba05b787533','audits/pr967_2616/CLOSURE_OPERATIONS_INVENTORY.json':'1aec2d70a27a8ef251c8478932d1cd578c0a259e075fec591edc345c19d8745a'};raw={n:(P/n).read_bytes()for n in pins}
for n,b in raw.items():need(sha(b)==pins[n],'external input '+n)
# Exact authenticated entry() functions are identical; actual captured worker
# controls below exercise each copy independently against explicit synthetic core.
entry_sources={}
for n in ['close_pr967.py','finalize_pr967_and_gate_next.py']:
 tree=ast.parse(raw[n]);entry_sources[n]=next(ast.get_source_segment(raw[n].decode(),x)for x in tree.body if isinstance(x,ast.FunctionDef)and x.name=='entry')
need(entry_sources['close_pr967.py']==entry_sources['finalize_pr967_and_gate_next.py'],'entry implementations differ')
rows=[];sentinel=S/'UNAUTHENTICATED_EXECUTED'
for mode,flags in [('normal',[]),('O',['-O']),('OO',['-OO'])]:
 for case in ['positive_close','positive_finalize','missing_action','invalid_action',*[(n,kind)for n in pins for kind in ['same_size_sentinel','append','symlink','hardlink','FIFO','directory','missing']],'no_I','no_S','no_B']:
  label=case if isinstance(case,str)else case[0].replace('/','_')+'_'+case[1];root=S/(mode+'_'+label);program=root/P.name;audit=program/'audits/pr967_2616';audit.mkdir(parents=True)
  for n,b in raw.items():(program/n).write_bytes(b)
  if isinstance(case,tuple):
   n,kind=case;path=program/n
   if kind=='same_size_sentinel':
    bad=('from pathlib import Path\nPath('+repr(str(sentinel))+').write_text("EXECUTED")\n').encode();path.write_bytes(bad+b'#'*(len(raw[n])-len(bad)))
   elif kind=='append':path.write_bytes(raw[n]+b'X')
   elif kind=='symlink':path.unlink();path.symlink_to(P/n)
   elif kind=='hardlink':path.unlink();os.link(P/n,path)
   elif kind=='FIFO':path.unlink();os.mkfifo(path)
   elif kind=='directory':path.unlink();path.mkdir()
   else:path.unlink()
  old=b'root=Path("/Users/alec/Documents/Math")';replacement=('root=Path('+repr(str(root))+')').encode();need(source.count(old)==1,'root occurrence');code=source.replace(old,replacement).decode();launchflags=['-I','-S','-B',*flags]
  if case=='no_I':launchflags.remove('-I')
  if case=='no_S':launchflags.remove('-S')
  if case=='no_B':launchflags.remove('-B')
  args=[]if case=='missing_action'else ['bad']if case=='invalid_action'else ['finalize'if case=='positive_finalize'else'close','--help'];start=datetime.datetime.now(datetime.timezone.utc).isoformat();p=subprocess.run([sys.executable,*launchflags,'-c',code,*args],cwd=root,capture_output=True,timeout=10);positive=case in ('positive_close','positive_finalize');need((p.returncode==0)==positive,'unexpected result '+label);need(not sentinel.exists(),'malicious sentinel executed')
  rows.append({'mode':mode,'case':label,'started_utc':start,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'returncode':p.returncode,'expected_success':positive,'stdout':p.stdout.decode(),'stderr':p.stderr.decode(),'only_launcher_substitution':{'old':old.decode(),'new':replacement.decode()},'substituted_launcher_sha256':sha(code.encode()),'sentinel_absent':True})
 # Test captured entry's actual child controls independently for both helpers.
 for name,action in [('close_pr967.py','close'),('finalize_pr967_and_gate_next.py','finalize')]:
  root=S/(mode+'_worker_'+action);program=root/P.name;audit=program/'audits/pr967_2616';audit.mkdir(parents=True)
  synthetic=b'import sys,json\ndef operation(action,args,context):\n print(json.dumps({"action":action,"optimization":sys.flags.optimize,"isolated":sys.flags.isolated,"no_site":sys.flags.no_site,"no_bytecode":sys.dont_write_bytecode,"synthetic_only":True}))\n';(program/'close_pr967.py').write_bytes(synthetic);(program/'finalize_pr967_and_gate_next.py').write_bytes(raw['finalize_pr967_and_gate_next.py'])
  inv={'schema':'pr967-closure-operations-v1','pr':967,'problem_id':'2616','original_pr_head':'b356dec5cb01e5f536b9cfeece56ad08844c03cb','files':{str((program/n).relative_to(root)):{'bytes':len((program/n).read_bytes()),'sha256':sha((program/n).read_bytes())}for n in ['close_pr967.py','finalize_pr967_and_gate_next.py']}};ib=(json.dumps(inv,sort_keys=True)+'\n').encode();(audit/'CLOSURE_OPERATIONS_INVENTORY.json').write_bytes(ib)
  # Trusted test loads full actual initial helper under a non-main name after
  # unconditional external source authentication; only path globals are rebound.
  loader='import sys,pathlib,hashlib; p=pathlib.Path(sys.argv.pop(1)); h=sys.argv.pop(1); root=pathlib.Path(sys.argv.pop(1)); raw=p.read_bytes();\nif hashlib.sha256(raw).hexdigest()!=h: raise RuntimeError("initial source mismatch")\nn={"__name__":"_independent_worker_probe","__file__":str(p)}; exec(compile(raw,str(p),"exec",dont_inherit=True,optimize=sys.flags.optimize),n); n.update(ROOT=root,P=root/"'+P.name+'",A=root/"'+P.name+'/audits/pr967_2616"); sys.argv=[str(p),*sys.argv[1:]]; n["entry"]("'+action+'")'
  p=subprocess.run([sys.executable,'-I','-S','-B',*flags,'-c',loader,str(P/name),pins[name],str(root),'--operations-sha256',sha(ib),'--disposition-sha256','0'*64],capture_output=True,timeout=10,cwd=root);need(p.returncode==0 and not p.stderr,'worker failed '+action);v=json.loads(p.stdout);need(v=={'action':action,'optimization':0,'isolated':1,'no_site':1,'no_bytecode':True,'synthetic_only':True},'worker flags '+action);rows.append({'mode':mode,'case':'actual_'+action+'_entry_optimization0_child','returncode':p.returncode,'stdout':v,'initial_source_authentication_unconditional':True,'fixture_dependency_only':True})
(R/'TRUSTED_LAUNCHER_REPRODUCTIONS.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'trusted_launcher_sha256':sha(source),'controls':rows,'count':len(rows),'actual_service_or_Git_mutations':0,'actual_operations_called':False,'entry_functions_exactly_identical':True},indent=2)+'\n');print(json.dumps({'count':len(rows),'status':'PASS','sentinel_absent':not sentinel.exists()}))
