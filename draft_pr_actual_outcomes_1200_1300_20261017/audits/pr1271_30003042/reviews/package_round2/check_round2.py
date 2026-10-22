#!/usr/bin/env python3
"""Fresh adversarial execution of authenticated current code, own ignored scratch only.
All service/Git operations are explicitly mocked. Prior reviewer code is not imported.
"""
from pathlib import Path, PurePosixPath
import ast,contextlib,copy,hashlib,importlib.util,io,json,os,shutil,subprocess,sys,tempfile,types,zipfile
R=Path(__file__).resolve().parent;A=R.parents[1];P=A/'publication';T=A.parents[1];L=R/'_local';L.mkdir(exist_ok=True)
os.environ['PYTHONDONTWRITEBYTECODE']='1';os.environ['TMPDIR']=str(L);tempfile.tempdir=str(L)
def need(x,m):
 if not x:raise RuntimeError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2)+'\n')
def load(p):
 s=importlib.util.spec_from_file_location('round2_'+p.stem+str(id(p)),p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def capture(f):
 with contextlib.redirect_stdout(io.StringIO()):return f()
def rejected(f,label):
 try:f()
 except (RuntimeError,ValueError,KeyError,FileNotFoundError,IsADirectoryError) as e:return {'case':label,'exception':type(e).__name__,'reason':str(e)}
 raise RuntimeError('Corruption accepted: '+label)
def portable():
 root=L/('portable_'+str(sys.flags.optimize));shutil.rmtree(root,ignore_errors=True);root.mkdir()
 with zipfile.ZipFile(P/'Gamma_Filtration_Counterexample_Verification_v1.0.zip') as z:
  names=z.namelist();need(len(names)==169 and len(names)==len(set(names))==len({n.casefold() for n in names}),'ZIP duplicate/case/inventory')
  for n in names:
   q=PurePosixPath(n);need(not q.is_absolute() and '..' not in q.parts and str(q)==n and '\\' not in n,'unsafe zip path');need((z.getinfo(n).external_attr>>16)&0o170000!=0o120000,'zip symlink')
  z.extractall(root)
 v=load(root/'verify.py');an=json.loads((P/'BUILD_RECEIPT.json').read_text())['verification_anchors'];run=lambda manifest=an['manifest']:v.verify(root,manifest,an['context'],an['snapshot'])
 result=run();need(result['authenticated_members']==168 and len(result['nested_manifests'])==13,'actual inventory differs')
 names_on_disk={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()};need(set(names)==names_on_disk,'actual extraction differs')
 outer=root/'MANIFEST.json';raw=outer.read_bytes();matrix=[]
 def refresh():
  obj=json.loads(raw)
  for e in obj['files']:
   p=root/e['path'];e.update(bytes=p.stat().st_size,sha256=sha(p))
  save(outer,obj);return sha(outer)
 payload=root/'reviews/finite_computation_adversary/REPORT.md';old=payload.read_bytes()
 try:
  payload.write_bytes(old+b'\nchanged nested evidence\n');matrix.append(rejected(run,'changed_nested_payload'))
  anchor=refresh();matrix.append(rejected(lambda:run(anchor),'nested_payload_and_outer_rewritten'))
 finally:payload.write_bytes(old);outer.write_bytes(raw)
 context=root/'provenance/CURRENT_PR1271_CONTEXT.json';cb=context.read_bytes();ctx=json.loads(cb)
 reg=ctx['authored_freezes'][0];nested=root/reg['path'];nb=nested.read_bytes()
 try:
  obj=json.loads(nb);obj[reg['entries_key']][0]['sha256']='1'*64;save(nested,obj);anchor=refresh();matrix.append(rejected(lambda:run(anchor),'nested_manifest_outer_rewritten'))
 finally:nested.write_bytes(nb);outer.write_bytes(raw)
 try:
  changed=copy.deepcopy(ctx);changed['tracker']['notes']='forged';save(context,changed);anchor=refresh();matrix.append(rejected(lambda:run(anchor),'context_outer_coupled_outside_anchor'))
 finally:context.write_bytes(cb);outer.write_bytes(raw)
 for label,change in [('parent_path',lambda o:o['files'][0].update(path='../escape')),('absolute_path',lambda o:o['files'][0].update(path='/escape')),('case_mismatch',lambda o:o['files'][0].update(path=o['files'][0]['path'].swapcase())),('duplicate_member',lambda o:o['files'].append(copy.deepcopy(o['files'][0]))),('self_reference',lambda o:o['files'][0].update(path='MANIFEST.json')),('path_alias',lambda o:o['files'][0].update(path='./'+o['files'][0]['path']))]:
  try:
   obj=json.loads(raw);change(obj);save(outer,obj);anchor=sha(outer);matrix.append(rejected(lambda:run(anchor),label))
  finally:outer.write_bytes(raw)
 extra=root/'unlisted.txt'
 try:extra.write_text('unlisted');matrix.append(rejected(run,'unlisted_regular_file'))
 finally:extra.unlink()
 target=root/'PORTABLE_README.md';data=target.read_bytes();outside=L/('outside_'+str(sys.flags.optimize)+'.md');outside.write_bytes(data)
 try:
  target.unlink();target.symlink_to(outside);matrix.append(rejected(run,'same_bytes_symlink_member'))
 finally:target.unlink();target.write_bytes(data)
 folder=root/'reviews/finite_computation_adversary';moved=L/('symlink_family_'+str(sys.flags.optimize));shutil.rmtree(moved,ignore_errors=True)
 try:
  folder.rename(moved);folder.symlink_to(moved,target_is_directory=True);matrix.append(rejected(run,'same_bytes_symlink_parent'))
 finally:folder.unlink();moved.rename(folder)
 matrix.append(rejected(lambda:v.need(False,'explicit false guard'),'explicit_false_guard'))
 return {'optimization':sys.flags.optimize,'actual_archive_verification':result,'archive_members':len(names),'negative_controls':matrix,'outside_anchors':an,'all_source_and_published_candidates_read_only':True}
def merged_matrix(w):
 with tempfile.TemporaryDirectory(prefix='new_merge_matrix_',dir=L) as d:
  f=w.fixture(Path(d)/'base');pub=f['pub'];audit=f['audit'];program=audit.parents[1];p,t,_=w.publication_and_tracker_controls(f);w.update_controls(f,p,t)
  u=load(pub/'update_pr_publication.py');tracker=load(pub/'append_tracker.py');m=load(program/'publication_coordinators/verify_pr1271_merge.py')
  need(sha(pub/'update_pr_publication.py')==sha(P/'update_pr_publication.py') and sha(program/'publication_coordinators/verify_pr1271_merge.py')==sha(T/'publication_coordinators/verify_pr1271_merge.py'),'deployed source differs')
  p['doi_resolution']={'status':'resolved','http_status':200};save(pub/'PUBLICATION_RECEIPT.json',p);files,_,_=u.desired_files(f['build'],p,t,f['snapshot']);need(len(files)==13,'expected13');head='a'*40;merge='c'*40
  body=(pub/'PR_BODY_FINAL.md').read_text();wanted=u.expected_identity(p,t,files,body);save(pub/'PR_BRANCH_RECEIPT.json',{**wanted,'commit':head,'body_readback_verified':True,'remote_readback_verified':True})
  live={'state':'MERGED','headRefOid':head,'headRefName':u.BRANCH,'mergeCommit':{'oid':merge},'mergedAt':'2026-10-18T01:00:00Z','body':body,'url':'https://github.com/AlecKriebel/Math/pull/1271'}
  state={'current_pr':1271,'completed_prs':copy.deepcopy(m.COMPLETED_BEFORE),'publications':[{'pr':n} for n in m.COMPLETED_BEFORE],'eligible_prs':copy.deepcopy(m.ELIGIBLE),'eligible_count':12};statepath=program/'PROGRAM_STATE.json';active={'path':None};events=[]
  def git(*args,data=None):
   events.append(['git',*args])
   if args==('branch','--show-current'):return b'main\n'
   if args[0]=='rev-list':return ((merge+' '+'d'*40+' '+head if args[-1]==merge else head+' '+u.ORIGINAL)+'\n').encode()
   if args[0]=='diff-tree':return ('\n'.join(sorted(files))+'\n').encode()
   if args[0]=='show':
    c,n=args[1].split(':',1);return files[n]+b'\nSINGLE_CORRUPTION' if c==merge and n==active['path'] else files[n]
   if args[0] in {'fetch','update-ref'}:return b''
   raise RuntimeError('Unmocked Git request '+repr(args))
  u.git=git
  def call(parts,params,body=None):
   events.append(['gws',*parts])
   if parts==['spreadsheets','get']:return {'sheets':[{'properties':{'sheetId':tracker.GID,'title':'Math Puzzles'}}]}
   if parts==['spreadsheets','values','get']:return {'values':[['Original Problem','Solution Chat URL','DOI','Notes'],copy.deepcopy(t['row'])]}
   raise RuntimeError('External mutation forbidden')
  tracker.call=call
  def route(path):
   if Path(path).name=='update_pr_publication.py':return u.__dict__
   if Path(path).name=='append_tracker.py':return tracker.__dict__
   raise RuntimeError('Unmocked source '+str(path))
  m.runpy=types.SimpleNamespace(run_path=route);m.subprocess=types.SimpleNamespace(check_output=lambda *a,**k:json.dumps(live));save(statepath,state);capture(m.main);after=json.loads(statepath.read_text());need(after['completed_prs']==state['completed_prs']+[1271] and after['current_pr']==1274 and len(after['publications'])==9,'wrong advancement')
  outcomes=[]
  for name in sorted(files):
   active['path']=name;save(statepath,state);before=statepath.read_bytes();bad=rejected(m.main,'each_merged_blob:'+name);need('Merged bytes differ '+name in bad['reason'] and statepath.read_bytes()==before,'corrupt merge did not reject at blob or advanced');bad['state_unchanged']=True;outcomes.append(bad)
  active['path']=None
  for label,key,value in [('wrong_eligible_count','eligible_count',13),('duplicate_prior_completion','completed_prs',state['completed_prs']+[1268])]:
   changed=copy.deepcopy(state);changed[key]=value;save(statepath,changed);before=statepath.read_bytes();bad=rejected(m.main,label);need('Program state' in bad['reason'] and statepath.read_bytes()==before,'bad program state advanced');outcomes.append(bad)
  return {'positive_complete_main_8_to_9_then_1274':True,'thirteen_individual_merged_blob_rejections':outcomes[:13],'two_new_program_state_rejections':outcomes[13:],'all_network_and_Git_mocked':True}
def actual_metadata_kit():
 c=load(T/'publication_coordinators/pr1271.py');kit=c.load_exact_kit();source=json.loads((P/'zenodo-deposit.json').read_text());out=[]
 with tempfile.TemporaryDirectory(prefix='actual_metadata_kit_',dir=L) as d:
  folder=Path(d);manifest=folder/'manifest.json';save(manifest,source)
  for e in source['files']:shutil.copyfile(P/e['path'],folder/e['path'])
  for changed in [None,*sorted(source['metadata'])]:
   kit.STATE_DIR=folder/('state_'+str(changed));path=manifest.resolve();place=kit.state_path(path,'production');kit.save_state(place,{'manifest':str(path),'environment':'production','id':123})
   meta,files=kit.load_manifest(path);events=[]
   class Client:
    def get(self,n):
     need(n==123,'wrong known ID');events.append('GET');r={'id':123,'submitted':False,'metadata':copy.deepcopy(meta),'files':[{'filename':e['name'],'filesize':e['size'],'checksum':'md5:'+e['md5']} for e in files]}
     if changed is not None:r['metadata'][changed]=None
     if 'POST' in events:r.update(submitted=True,doi='10.5281/zenodo.123')
     return r
    def publish(self,n):need(n==123,'wrong publish ID');events.append('POST')
   kit.doi_status=lambda d:{'status':'resolved','http_status':200}
   args=types.SimpleNamespace(command='publish',manifest=manifest,sandbox=False,confirm_id=123,check_doi=True)
   if changed is None:
    result=kit.run(args,client=Client());need(result['state']=='published' and result['metadata_normalizations']==[] and events.count('POST')==1,'baseline exact kit failed');out.append({'field':'baseline','events':events,'published':True})
   else:
    try:kit.run(args,client=Client())
    except kit.DepositError as e:need('POST' not in events,'field corruption reached POST');out.append({'field':changed,'events':events,'rejection':str(e)})
    else:raise RuntimeError('Actual current metadata corrupted field accepted '+changed)
 return {'actual_manifest_sha256':sha(P/'zenodo-deposit.json'),'actual_pdf_zip_sha256':[sha(P/e['path']) for e in source['files']],'read_only_shared_kit_sha256':sha(Path('/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py')),'cases':out,'all_network_methods_mocked':True}
def workflow():
 w=load(P/'workflow_regression.py');w.REPORT_ROOT=R
 return {'optimization':sys.flags.optimize,'operative_regression':w.worker(),'fresh_merged_matrix':merged_matrix(w),'actual_current_metadata_and_two_artifacts_shared_kit':actual_metadata_kit()}
def finite():
 context=json.loads((A/'CURRENT_PR1271_CONTEXT.json').read_text());out=[]
 for spec in context['diagnostic_replays']:
  p=A/spec['program'];tree=ast.parse(p.read_text(), optimize=0);need(not any(isinstance(n,ast.Assert) for n in ast.walk(tree)),'assert in actual mathematical checker')
  # Existing archive verifier already replays all four programs in three modes.
  # Here mutate the program's actual decisive guard, in a separate copy only.
  guards=[n for n in ast.walk(tree) if isinstance(n,ast.If) and any(isinstance(t,ast.Raise) for t in ast.walk(n))]
  need(bool(guards),'checker has no hard guard')
  guard=next((g for g in guards if isinstance(g.test,ast.UnaryOp) and isinstance(g.test.op,ast.Not)),guards[0]);guard.test=ast.Constant(value=True)
  # Force the first actually executed hard guard to fail, including the
  # source-only program whose guards are top-level statements.
  ast.fix_missing_locations(tree)
  copy_path=L/('false_'+p.name);copy_path.write_text(ast.unparse(tree)+'\n')
  flags=[] if sys.flags.optimize==0 else ['-O' if sys.flags.optimize==1 else '-OO']
  r=subprocess.run([sys.executable,'-B',*flags,str(copy_path)],capture_output=True,text=True,cwd=L,timeout=180)
  need(r.returncode!=0,'deliberately false checker guard accepted');out.append({'program':spec['program'],'original_sha256':sha(p),'false_copy_sha256':sha(copy_path),'returncode':r.returncode,'stderr_tail':r.stderr[-800:],'AST_assert_count':0})
 return {'optimization':sys.flags.optimize,'actual_programs':out,'scope':'Actual programs reproduced by portable verification; here each real guard is forced to reject in an isolated altered copy. Original bytes untouched.'}
if __name__=='__main__':
 mode=sys.argv[1];result={'portable':portable,'workflow':workflow,'finite':finite}[mode]();save(R/(mode+'_mode'+str(sys.flags.optimize)+'.json'),result);print(json.dumps({'status':'PASS','mode':mode,'optimization':sys.flags.optimize}))
