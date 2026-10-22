"""Whole-packet integrity, semantic comparison and negative guards; no publication."""
from pathlib import Path
import json,hashlib,zipfile,stat,subprocess,sys,importlib.util,datetime,copy
R=Path(__file__).resolve().parent;P=R.parent.parent/'publication';E=R/'tmp/extracted';PREFIX='draft_pr_actual_claims_1100_1200_20261017/audits/pr1141_30006210';A=E/PREFIX

def need(ok,msg):
 if not ok:raise RuntimeError(msg)
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def load(f):return json.loads(f.read_text())
manifest=load(E/'SOURCE_MANIFEST.json');allowed=load(E/'verification/AUDIT_MEMBERS.json')
with zipfile.ZipFile(P/'output/polynomial-compatibility-source-and-verification.zip') as z:
 names=z.namelist();need(len(names)==len(set(names))==111,'source cardinality')
 need(set(names)==set(manifest)|{'SOURCE_MANIFEST.json'},'manifest exact membership')
 for info in z.infolist():
  n=info.filename;need(not Path(n).is_absolute() and '..' not in Path(n).parts and '\\' not in n and not stat.S_ISLNK(info.external_attr>>16),'unsafe ZIP member')
 for n,w in manifest.items():need(pin(z.read(n))==w,'manifest fingerprint '+n)
 need({n[len(PREFIX)+1:] for n in names if n.startswith(PREFIX+'/')}==set(allowed),'audit allowlist membership')
 need(len(allowed)==98,'audit count')
 for n,w in allowed.items():need(pin(z.read(PREFIX+'/'+n))==w,'audit fingerprint '+n)
 need(not any(any(s in n.split('/') for s in ['sources','private','tmp','rendered','__pycache__']) or n.endswith(('.html','.png','.pyc')) for n in names),'excluded member paths')
 for n in names:
  if n in ['SOURCE_MANIFEST.json','PROVENANCE.json']:continue
  live=P.parent/n[len(PREFIX)+1:] if n.startswith(PREFIX+'/') else P/n
  need(z.read(n)==live.read_bytes(),'live/archive identity '+n)
 original=load(A/'inputs/MANIFEST.json');need(set(original['members'])=={f.name for f in (A/'inputs').iterdir()},'ten original members')
 for row in original['entries']:need(pin((A/'inputs'/row['file']).read_bytes())=={'bytes':row['bytes'],'sha256':row['sha256']},'original input pin')
receipt=load(P/'PACKAGE_RECEIPT.json');need(receipt['source_members']==manifest,'package receipt mapping')
with zipfile.ZipFile(P/'output/zenodo-upload-kit.zip') as k:
 need(len(k.namelist())==len(set(k.namelist()))==5,'kit count')
 mapping={'polynomial-compatibility.pdf':P/'output/pdf/polynomial-compatibility.pdf','polynomial-compatibility-source-and-verification.zip':P/'output/polynomial-compatibility-source-and-verification.zip','README.md':P/'README.md','zenodo-metadata.json':P/'zenodo-metadata.json'}
 need(set(k.namelist())==set(mapping)|{'zenodo-deposit.json'},'kit allowlist')
 for n,f in mapping.items():need(k.read(n)==f.read_bytes(),'kit payload '+n)
 dep=json.loads(k.read('zenodo-deposit.json'));local=load(P/'zenodo-deposit.json');meta=load(P/'zenodo-metadata.json')
 need(dep['metadata']==local['metadata']==meta,'all metadata equality');need(dep['files']==[{'path':'polynomial-compatibility.pdf'},{'path':'polynomial-compatibility-source-and-verification.zip'}],'flat kit paths')
 need(set(dep)==set(local)=={'files','metadata'},'deposit keys')
# Every compared mathematical field is retained. Strict type, key, list and leaf tests.
spec=importlib.util.spec_from_file_location('portable',E/'verification/verify_all.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
plan=load(E/'verification/CONTROL_PLAN.json');replay=load(R/'OFFLINE_REPLAY.json');frozen=load(E/'verification/REPLAY_RECEIPT.json')
need(replay['status']=='PASS' and len(replay['runs'])==8 and len(replay['actual_failure_guards'])==40,'complete replay')
semantic_rows=[]
for row in plan['controls']:
 expected=load(A/row['expected']);sem=v.expected_semantics(expected,row)
 for optimized in (False,True):
  rr=next(x for x in replay['runs'] if x['program']==row['program'] and x['optimized'] is optimized)
  v.compare(v.normalize(rr['result'],row,optimized),sem)
  ff=next(x for x in frozen['runs'] if x['program']==row['program'] and x['optimized'] is optimized)
  v.compare(v.expected_semantics(ff['result'],row),sem)
 semantic_rows.append({'program':row['program'],'runtime_kind':row['runtime_kind'],'excluded_runtime_paths':row['drop_paths'],'all_other_fields_exact':True})
need(all(x['exit_code']!=0 and x['expected_diagnostic_present'] for x in replay['actual_failure_guards']),'real failures')
comparison_failures=0
for g,w in [(True,1),({'a':1},{'a':2}),({'a':1,'b':2},{'a':1}),([1],[1,2]),('bad_hash','good_hash')]:
 try:v.compare(g,w)
 except RuntimeError:comparison_failures+=1
 else:raise RuntimeError('comparison accepted corruption')
for row in plan['controls']:
 if row['runtime_kind'] not in ['target','separator']:continue
 actual=next(x['result'] for x in replay['runs'] if x['program']==row['program'] and x['optimized'] is False)
 for field in ['interpreter','mode']:
  bad=copy.deepcopy(actual)
  if row['runtime_kind']=='target':bad['python_version' if field=='interpreter' else 'optimized']='corrupt'
  else:bad['runtime']['python' if field=='interpreter' else 'optimization']='corrupt'
  try:v.normalize(bad,row,False)
  except RuntimeError:comparison_failures+=1
  else:raise RuntimeError('runtime corruption accepted')
# Deliberately alter disposable inputs; guard must stop before the expensive baselines.
guards=[]
def reject(name,f,new,program,diagnostic):
 old=f.read_bytes()
 try:
  f.write_bytes(new);run=subprocess.run([sys.executable,'-B',str(E/program)],cwd='/',capture_output=True,text=True,timeout=30)
  need(run.returncode!=0 and diagnostic in run.stderr+run.stdout,'inactive guard '+name)
  guards.append({'name':name,'exit_code':run.returncode,'diagnostic':diagnostic})
 finally:f.write_bytes(old)
reject('changed original proof',A/'inputs/PROOF.md',(A/'inputs/PROOF.md').read_bytes()+b'\n','verification/verify_all.py','Fingerprint mismatch')
bad=copy.deepcopy(manifest);bad['main.tex']['sha256']='0'*64
reject('changed source manifest',E/'SOURCE_MANIFEST.json',json.dumps(bad).encode(),'verification/verify_all.py','Fingerprint mismatch')
bad=load(E/'zenodo-metadata.json');bad['title']='incorrect altered title'
reject('mismatched metadata',E/'zenodo-metadata.json',json.dumps(bad).encode(),'build_package.py','Metadata mismatch')
reject('changed PDF',E/'output/pdf/polynomial-compatibility.pdf',(E/'output/pdf/polynomial-compatibility.pdf').read_bytes()+b'\n','build_package.py','PDF QA pins')
reject('changed paper source',E/'main.tex',(E/'main.tex').read_bytes()+b'\n','build_package.py','PDF QA pins')
# Check each final repaired heading record against its privately held source line, without redistributing any source strings.
body=load(A/'reviews/priority_classification_01/BODY_SCOPE.json');heading_count=0
for b in body['bodies']:
 lines=Path(b['text_path']).read_text().splitlines()
 need(len(lines)==b['lines'],'scope line count')
 for row in b['result_heading_scan']:
  need('text' not in row and 'heading' not in row,'copied heading retained')
  line=lines[row['line']-1].encode();need(len(line)==row['source_line_utf8_bytes'],'heading line length')
  hkey=next(k for k in row if 'sha256' in k);need(hashlib.sha256(line).hexdigest()==row[hkey],'heading line hash');heading_count+=1
need(heading_count==249,'heading coverage')
# Authenticated receipt crosschecks. Existing absolute paths may include historical states; disclose mismatches rather than silently repin.
checks=[];mismatches=[]
def walk(x,source,key=''):
 if isinstance(x,dict):
  if isinstance(x.get('sha256'),str) and isinstance(x.get('path'),str) and Path(x['path']).is_absolute() and Path(x['path']).is_file():
   f=Path(x['path']);actual=pin(f.read_bytes());want={'bytes':x.get('bytes',actual['bytes']),'sha256':x['sha256']};result={'receipt':source,'path':str(f),'current_matches':actual==want}
   checks.append(result)
   if actual!=want:mismatches.append(dict(result,historical_pin=want,current_pin=actual))
  for k,y in x.items():walk(y,source,key+'.'+k)
 elif isinstance(x,list):
  for y in x:walk(y,source,key)
for f in sorted(A.rglob('*.json')):walk(load(f),str(f.relative_to(A)))
# Only root's old mathematical-decision seal includes a subsequently repaired priority artifact, if any.
for row in mismatches:
 need('priority_classification_01' in row['path'] or 'ROOT_PRIORITY_DECISION.md' in row['path'],'unexplained historical custody mismatch')
need((A/'reviews/priority_classification_01/RECEIPT.sha256').read_text().split()[0]==hashlib.sha256((A/'reviews/priority_classification_01/RECEIPT.json').read_bytes()).hexdigest(),'receipt sidecar')
for n in ['output/polynomial-compatibility-source-and-verification.zip','output/zenodo-upload-kit.zip']:need((E/n).read_bytes()==(P/n).read_bytes(),'exact disposable rebuild')
result={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_members':111,'manifest_entries':110,'allowlisted_audit_members':98,'kit_members':5,'original_input_members':10,'runtime_semantics':semantic_rows,'comparison_or_runtime_corruptions_rejected':comparison_failures,'disposable_input_guard_failures':guards,'repaired_heading_positions_verified_from_source':heading_count,'receipt_fingerprint_checks':len(checks),'historical_pin_mismatches':mismatches,'source_and_kit_rebuild_exact':True,'limits':'Finite and integrity controls supplement universal proof. Historical custody mismatches are not current release-manifest failures.'}
(R/'PACKET_CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
