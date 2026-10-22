"""NEW independent controls; exact frozen candidates, isolated local providers only."""
from pathlib import Path
from datetime import datetime,timezone
import sys,io,json,types,copy,contextlib,traceback,hashlib,subprocess,zipfile,shutil,http.client,importlib.util
D=Path(__file__).resolve().parent;C=D.parent;P=C/'publication';PY='/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
# Historical providers stay unmodified. Only path/source globals and provider behavior
# are substituted. Every candidate module is compiled from the exact frozen bytes.
sys.path.insert(0,str(P/'native_repair_02'))
import legacy_fixture_source as L
b=L.b;b.HERE=D;b.RUNS=D/'fixtures';b.SNAP=D;b.SOURCE={n:(D/n).read_bytes() for n in b.NAMES}
NAMES=b.NAMES;RESULTS=[]
def utc():return datetime.now(timezone.utc).isoformat()
def sha(x):return hashlib.sha256(x).hexdigest()
def dump(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+'\n')
def pin(p,base):return dict(path=p.relative_to(base).as_posix(),bytes=p.stat().st_size,sha256=sha(p.read_bytes()))
def reject(fn):
 try:fn()
 except Exception as e:return dict(type=type(e).__name__,error=str(e))
 raise AssertionError('Expected rejection was accepted')
def quiet(fn):
 with contextlib.redirect_stdout(io.StringIO()):return fn()
def record(label,fn):
 start=utc()
 try:r=dict(label=label,start_utc=start,PASS=True,result=fn())
 except Exception as e:r=dict(label=label,start_utc=start,PASS=False,error=repr(e),traceback=traceback.format_exc())
 r['completed_utc']=utc();RESULTS.append(r);print(json.dumps(r),flush=True);dump(D/'RESULTS.json',RESULTS)
 return r

def compact(label):
 folder=b.RUNS/label
 files={p.relative_to(folder).as_posix():p for p in folder.rglob('*') if p.is_file()}
 zpath=D/('FIXTURE_'+label+'.zip')
 with zipfile.ZipFile(zpath,'x',compression=zipfile.ZIP_DEFLATED) as z:
  for n,p in sorted(files.items()):z.write(p,n)
 with zipfile.ZipFile(zpath) as z:
  assert len(z.namelist())==len(files) and set(z.namelist())==set(files) and z.testzip() is None
  rows=[]
  for n,p in sorted(files.items()):
   raw=p.read_bytes();assert z.read(n)==raw;rows.append(dict(path=n,bytes=len(raw),sha256=sha(raw)))
 dump(D/('FIXTURE_'+label+'_MANIFEST.json'),dict(archive=pin(zpath,D),utc=utc(),exact_members=True,CRC=True,every_body_SHA256_and_original_equality=True,files=rows))
 shutil.rmtree(folder)

class Fixture(L.Fixture):
 def run(self,args,**kw):
  if not ('--method' in args and Path(args[0]).name=='gh'):assert kw.get('text') is False
  result=super().run(args,**kw)
  if args[0].endswith('/gws'):
   params=json.loads(args[args.index('--params')+1]);v=json.loads(result.stdout);grid=1114+self.appends
   if args[1:4]==['sheets','spreadsheets','get']:
    v['sheets'][0]['properties'].update(sheetType='GRID',gridProperties=dict(rowCount=grid,columnCount=43))
   elif args[4]=='append':
    v.update(spreadsheetId=self.rb.SHEET);v['updates']['updatedData'].update(range=v['updates']['updatedRange'],majorDimension='ROWS')
   else:
    v.update(majorDimension='ROWS')
    if params['range']==self.rb.FULL_RANGE:v['range']="'Math Puzzles'!A1:D"+str(grid)
   if getattr(self,'sheet_hook',None):v=self.sheet_hook(args,params,v)
   result.stdout=json.dumps(v).encode()
  if isinstance(result.stdout,str):result.stdout=result.stdout.encode()
  if isinstance(result.stderr,str):result.stderr=result.stderr.encode()
  if len(args)>3 and args[3]=='inspect' and getattr(self,'late_hook',None):
   hook=self.late_hook;self.late_hook=None;hook()
  return result
 def urlopen(self,url,**kw):
  name=url.split('/files/')[1].split('?')[0];mapping=next(m for m in self.maps if m['name']==name)
  self.calls.append(dict(public_url=url,finite_cursor=True))
  return io.BytesIO((self.r/mapping['path']).read_bytes())
L.Fixture=Fixture


def source_and_real_science():
 spec=importlib.util.spec_from_file_location('independent_binding',D/'release_binding.py');rb=importlib.util.module_from_spec(spec);spec.loader.exec_module(rb)
 spec=importlib.util.spec_from_file_location('independent_integrate',D/'integrate_reviewed_pr.py');m=importlib.util.module_from_spec(spec);sys.modules['release_binding']=rb;spec.loader.exec_module(m)
 source=m.frozen_source(C/'preprint');assert len(source)==211
 intake=json.loads((C/'initial_review_20261016/INTAKE.json').read_bytes());assert len(intake['original_source_files'])==23
 original=[]
 for row in intake['original_source_files']:
  path='pr_update/5100015/history/original_submission_20261016/'+row['native_path'].removeprefix(m.PREFIX)
  raw=source[path];assert len(raw)==row['bytes'] and sha(raw)==row['sha256'] and m.blob(raw)==row['native_blob'] and row['native_mode']=='100644';original.append(path)
 inputs=json.loads((C/'release_helpers_adversary_02/ACTUAL_CHAIN_INPUTS.json').read_bytes())
 assert rb.review_chain(C,inputs['entries'],'whole-package',rb.current_core(C/'preprint'))==(2,1)
 dump(D/'ACTUAL_SCIENCE_INPUTS.json',dict(entries=inputs['entries'],core=rb.current_core(C/'preprint'),compiler_log=pin(C/'preprint/manuscript.log',C),source_payload_count=211,originals=original,whole_chain_result=[2,1]))
 # Actual historical helper seals and all 13 dispositions, with a synthetic parser
 # successor only. This is explicitly not the review's own completed assessment.
 folder=D/'parser_successor';folder.mkdir()
 for n in NAMES:(folder/n).write_bytes(b.SOURCE[n])
 rows=[pin(folder/n,folder) for n in NAMES];frozen=utc();dump(folder/'FROZEN_SOURCES.json',dict(frozen_utc=frozen,rows=rows,SYNTHETIC_NO_AUTHORITY=True))
 (folder/'REPORT.md').write_text('SYNTHETIC parser successor only; no review or authority.\n')
 dump(folder/'ASSESSMENT.json',dict(schema='pr209-release-helper-assessment-v1',reviewer='SYNTHETIC_PARSER_SUCCESSOR_03',completed_utc=utc(),frozen_sources=rows,mandatory_findings=[],optional_findings=[],verdict='PASS',SYNTHETIC_NO_AUTHORITY=True))
 dump(folder/'AUTHORED_MANIFEST.json',dict(files=[pin(p,folder) for p in sorted(folder.iterdir())]))
 entries=[]
 for index in [1,2]:
  old=C/('release_helpers_adversary_%02d'%index);entries.append(dict(assessment=pin(old/'ASSESSMENT.json',C),authored_manifest=pin(old/'AUTHORED_MANIFEST.json',C),source_freeze=pin(old/'FROZEN_SOURCES.json',C),resolution=pin(C/('initial_review_20261016/ROOT_RELEASE_HELPER_REVIEW%02d_RESOLUTION.json'%index),C),supplements=[]))
 entries.append(dict(assessment=pin(folder/'ASSESSMENT.json',C),authored_manifest=pin(folder/'AUTHORED_MANIFEST.json',C),source_freeze=pin(folder/'FROZEN_SOURCES.json',C),supplements=[]))
 assert rb.review_chain(C,entries,'release-helper',rows)==(3,1)
 dump(D/'ACTUAL_HELPER_CHAIN_INPUTS.json',dict(entries=entries,result=[3,1],SYNTHETIC_SUCCESSOR_NO_AUTHORITY=True))
 return dict(zip_payloads=211,originals=23,whole_chain=[2,1],actual_prior_helper_seals_and_dispositions=True,helper_parser_chain=[3,1])


def import_process_controls():
 out=[]
 for n in NAMES:
  compile(b.SOURCE[n],str(D/n),'exec')
  r=subprocess.run([PY,'-B','-O',str(D/n)],capture_output=True);print('LOCAL_OPTIMIZED_EXIT',n,r.returncode,flush=True)
  (D/(n+'.optimized.stdout')).write_bytes(r.stdout);(D/(n+'.optimized.stderr')).write_bytes(r.stderr)
  assert r.returncode!=0 and b'optimized' in r.stderr.lower();out.append(dict(source=n,exit=r.returncode))
 script='import sys,subprocess,urllib.request;sys.path.insert(0,'+repr(str(D))+');subprocess.run=lambda *a,**k:(_ for _ in ()).throw(RuntimeError("FORBIDDEN PROVIDER"));urllib.request.urlopen=subprocess.run;import release_binding,append_verified_tracker,integrate_reviewed_pr,publish_preprint,verify_and_merge,verify_published_readonly;print("ALL SIX INERT")'
 r=subprocess.run([PY,'-B','-c',script],capture_output=True);print('LOCAL_IMPORT_EXIT',r.returncode,flush=True);(D/'IMPORT.stdout').write_bytes(r.stdout);(D/'IMPORT.stderr').write_bytes(r.stderr);assert r.returncode==0
 return dict(optimized=out,all_imports_inert=True)


def terminal_and_extra_controls():
 f=Fixture('terminal');quiet(f.prepare);f.unknown_main=True;error=reject(lambda:quiet(f.merge));f.unknown_main=False
 assert 'unknown' in error['error'].lower() and not (f.pub/'PR_MERGED.json').exists()
 assert sum(x['path']=='git/refs/heads/main' for x in f.mutations)==1
 m=f.module('verify_and_merge.py');i=f.module('integrate_reviewed_pr.py');rb=f.rb
 dump(f.base/'TERMINAL_SETUP.json',dict(error=error,mutations=f.mutations,main=f.main_head,PR=f.pr))
 # Reuse terminal state for independent boundary controls; no intent/provider write
 # replay or candidate-global function substitution.
 out={}
 meta=dict(spreadsheetId=rb.SHEET,sheets=[dict(properties=dict(sheetId=rb.SHEET_ID,title='Math Puzzles',sheetType='GRID',gridProperties=dict(rowCount=1115,columnCount=43)))])
 response=dict(range="'Math Puzzles'!A1:D1115",majorDimension='ROWS',values=copy.deepcopy(f.sheet))
 out['canonical_trimmed_rows']=len(rb.tracker_readback(dict(request=dict(spreadsheetId=rb.SHEET,range=rb.FULL_RANGE),response=response),rb.FULL_RANGE,meta))
 for name,value in [('boolean_grid',True),('undersized_grid',1),('negative_grid',-1)]:
  bad=copy.deepcopy(meta);bad['sheets'][0]['properties']['gridProperties']['rowCount']=value
  out[name]=reject(lambda:rb.tracker_readback(dict(request=dict(spreadsheetId=rb.SHEET,range=rb.FULL_RANGE),response=response),rb.FULL_RANGE,bad))
 bad=copy.deepcopy(meta);bad['sheets'].append(copy.deepcopy(bad['sheets'][0]));out['duplicate_gid']=reject(lambda:rb.tracker_properties(bad))
 for name,target in [('leading_zero',"'Math Puzzles'!A02:D02"),('row1',"'Math Puzzles'!A1:D1"),('different_rows',"'Math Puzzles'!A2:D3"),('unquoted','Math Puzzles!A2:D2')]:out[name]=reject(lambda:rb.tracker_row_number(target))
 for bad in [dict(response,values=[['x']*5]),dict(response,values=[[]]*1116),dict(response,majorDimension='COLUMNS'),dict(response,range="'Math Puzzles'!A1:D1114")]:
  out['value_schema_'+str(len(out))]=reject(lambda:rb.tracker_readback(dict(request=dict(spreadsheetId=rb.SHEET,range=rb.FULL_RANGE),response=bad),rb.FULL_RANGE,meta))
 z=rb.publication(f.r,f.pub,f.ctx);t=rb.tracker(f.r,f.pub,f.ctx,z)
 # Both whitespace and one-cell note drift must fail exact canonical metadata.
 for key in ['title','body']:
  old=f.pr[key];f.pr[key]=old+' ';api=i.NativeAPI(f.pub,'independent_metadata_'+key,readonly=True)
  out['canonical_'+key]=reject(lambda:m.current_pr(api,f.pr['head']['sha'],i.expected_pr_metadata(z,t),False,state='closed'));f.pr[key]=old
 # Full tree modes, deletions and unowned additions cannot masquerade as overlay.
 files={i.QUEUE:b'queue',i.PREFIX+'PROOF.md':b'proof'}
 for kind,values in [('mode',{i.QUEUE:b'queue',i.PREFIX+'PROOF.md':(b'proof','100755')}),('extra',{**files,'foreign/change':b'bad'}),('missing',{i.QUEUE:b'queue'})]:
  base=f.tree({'foreign/keep':b'keep'});actual=f.tree({'foreign/keep':b'keep',**values});api=i.NativeAPI(f.pub,'independent_tree_'+kind,readonly=True);trees=i.NativeTrees(api)
  out['tree_'+kind]=reject(lambda:trees.verify_overlay(base,actual,files))
 # Unknown existing main intent keeps BOTH write-capable modes disabled.
 out['normal_after_unknown']=reject(lambda:quiet(f.merge));out['resume_after_unknown']=reject(lambda:quiet(f.resume))
 fixed=len(f.mutations);oldpr=copy.deepcopy(f.pr);oldmain=f.main_head
 for kind in ['body','main','event']:
  def hook(kind=kind):
   if kind=='body':f.pr['body']='SYNTHETIC late bad theorem'
   elif kind=='event':f.pr['merge_commit_sha']=L.OLD
   else:
    f.main_head='unrelated-independent-main';f.commits[f.main_head]=dict(tree={'sha':f.tree({i.QUEUE:b'foreign unrelated'})},parents=[])
  f.late_hook=hook;out['late_'+kind]=reject(lambda:quiet(lambda:f.merge(True)));assert not (f.pub/'PR_MERGED.json').exists() and len(f.mutations)==fixed
  f.pr=copy.deepcopy(oldpr);f.main_head=oldmain
 # Shared lock exclusion is tested on the actual append entrance.
 with rb.acquire(f.pub):out['lock']=reject(f.append)
 # Exact provider raw binary retention, actual local child, no live executable.
 v=f.module('verify_published_readonly.py');folder=f.base/'local_binary';folder.mkdir();rawout=b'out\x00\xff';rawerr=b'err\x00\xfe';realrun=subprocess.run
 def child(cmd,**kw):return realrun([PY,'-B','-c','import os;os.write(1,'+repr(rawout)+');os.write(2,'+repr(rawerr)+')'],**kw)
 oldrun=v.subprocess;v.subprocess=types.SimpleNamespace(run=child)
 try:out['real_binary']=reject(lambda:v.inspect_existing(f.r,f.ctx,z['id'],folder))
 finally:v.subprocess=oldrun
 assert (folder/'inspect-stdout.json').read_bytes()==rawout and (folder/'inspect-stderr.txt').read_bytes()==rawerr
 # A finite stream failure after two successful chunks retains both plus partial.
 folder=f.base/'partial_stream';folder.mkdir();chunks=[b'first\x00',b'second\xff'];partial=b'last\xfe';expected=b''.join(chunks)+partial
 class Broken:
  def __enter__(self):return self
  def __exit__(self,*a):return None
  def read(self,n):
   if chunks:return chunks.pop(0)
   raise http.client.IncompleteRead(partial,100)
 oldurl=v.urllib;v.urllib=types.SimpleNamespace(request=types.SimpleNamespace(Request=lambda *a,**kw:a[0],urlopen=lambda *a,**kw:Broken()))
 try:out['partial_stream']=reject(lambda:v.public_bytes(f.r,f.ctx,z,folder))
 finally:v.urllib=oldurl
 assert (folder/'k303b-outer-center-pedal-areas.pdf').read_bytes()==expected
 # Final recovery, one actual synthetic main write, counts derived exactly once.
 quiet(lambda:f.merge(True));receipt=json.loads((f.pub/'PR_MERGED.json').read_bytes());assert receipt['program_counts']==[45,22,22,0] and len(f.mutations)==fixed
 original=(f.pub/'PR_MERGED.json').read_bytes();quiet(lambda:f.merge(True));assert (f.pub/'PR_MERGED.json').read_bytes()==original and len(f.mutations)==fixed
 out['final_counts']=receipt['program_counts'];out['main_writes']=sum(x['path']=='git/refs/heads/main' for x in f.mutations);out['accepted_readonly_immutable']=True
 f.trace();dump(f.base/'CONTROL_RESULTS.json',out);compact('terminal');return out

if __name__=='__main__':
 deps=[P/'native_repair_02/legacy_fixture_source.py',P/'native_repair_02/binding_fixture_source.py',P/'native_repair_02/archive_completed_group.py']
 dump(D/'PROVIDER_INPUT_PINS.json',dict(files=[pin(p,C) for p in deps],historical_programs_unmodified=True,adapter=pin(Path(__file__),D),candidate_bytes_unchanged=True))
 record('actual_scientific_zip_originals_and_review_chains',source_and_real_science)
 record('all_six_import_and_optimized_process_guards',import_process_controls)
 record('terminal_end_to_end_and_independent_boundaries',terminal_and_extra_controls)
 dump(D/'SUMMARY.json',dict(completed_utc=utc(),groups=len(RESULTS),all_pass=all(x['PASS'] for x in RESULTS),synthetic_providers_only=True,no_release_authority=True,case_completion_percent=65))
 raise SystemExit(0 if all(x['PASS'] for x in RESULTS) else 1)
