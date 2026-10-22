#!/usr/bin/env python3
"""Authenticate portable authored evidence and replay scoped finite diagnostics."""
from pathlib import Path,PurePosixPath
import hashlib,json,os,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parent
MINIMUM_FREEZES={
 'reviews/analytic_adversary/FINAL_AUTHORED_FREEZE.json':('reviews/analytic_adversary','entries','file'),
 'reviews/source_question_family/FREEZE_MANIFEST.json':('reviews/source_question_family','authored_files','path'),
 'reviews/convex_core_adversary/FREEZE_MANIFEST.json':('reviews/convex_core_adversary','authored_files','path'),
 'priority/independent/FREEZE_MANIFEST.json':('priority/independent','all_authored_content_files','path_relative_to_authored_root'),
 'priority/adversary/FREEZE_MANIFEST.json':('priority/adversary','authored_files','path'),
}
def need(c,m):
 if not c:raise ValueError(m)
def safe(raw):
 need(isinstance(raw,str) and bool(raw),'invalid member');rel=PurePosixPath(raw)
 need(not rel.is_absolute() and '..' not in rel.parts and str(rel)==raw and raw!='.','unsafe member');return raw
def member(root,raw):
 p=root/safe(raw);need(not p.is_symlink(),'symlink member '+raw)
 try:p.resolve().relative_to(root.resolve())
 except ValueError:raise ValueError('member escapes root '+raw)
 return p
def check_binding(p,e):
 b=p.read_bytes();need(type(e.get('bytes')) is int and len(b)==e['bytes'],'size '+str(p));need(hashlib.sha256(b).hexdigest()==e['sha256'],'digest '+str(p))
def authenticate_nested_manifests(root,registry=None,require_complete=True):
 """Explicit schemas/bases only; omitted-source/raw inventories are receipts."""
 if registry is None:
  context=json.loads((root/'provenance/CURRENT_PR1241_CONTEXT.json').read_text());registry=context['authored_freezes']
 need(isinstance(registry,list),'invalid explicit registry')
 listed={};checked=[]
 for item in registry:
  need(set(item)=={'path','base','entries_key','path_key','sha256'},'invalid registry schema')
  raw=safe(item['path']);safe(item['base']);need(raw not in listed,'duplicate registered freeze');listed[raw]=item
  need(raw.startswith(('reviews/','priority/')),'freeze outside authored family trees')
  need(item['entries_key'] in {'entries','files','authored_files','all_authored_content_files','new_authored_files'} and item['path_key'] in {'file','path','path_relative_to_authored_root','path_relative_to_family_root'},'unsupported freeze schema')
  path=member(root,raw);need(hashlib.sha256(path.read_bytes()).hexdigest()==item['sha256'],'freeze anchor '+raw)
 if require_complete:
  for raw,shape in MINIMUM_FREEZES.items():
   item=listed.get(raw);need(item is not None and tuple(item[k] for k in ['base','entries_key','path_key'])==shape,'required freeze/schema '+raw)
  need(any(raw.startswith('priority/adversary/') for raw in listed),'general-theory priority freeze absent')
  # Recognized authored freeze files cannot silently disappear from the registry.
  detected={p.relative_to(root).as_posix() for family in ['reviews','priority'] for p in (root/family).rglob('*.json') if p.name in {'MANIFEST.json','FINAL_AUTHORED_FREEZE.json'} or p.name.endswith(('_MANIFEST.json','_FREEZE.json'))}
  need(detected==set(listed),'unregistered/missing authored freeze')
 all_specs=list(registry)
 if require_complete:
  all_specs += [{'path':d+'/MANIFEST.json','base':d,'entries_key':'entries','path_key':'file'} for d in ['original_submitted','current_edition']]
 for item in all_specs:
  path=member(root,item['path']);obj=json.loads(path.read_text());entries=obj.get(item['entries_key']);need(isinstance(entries,list) and bool(entries),'invalid nested entries '+item['path']);base=member(root,item['base']);seen=set()
  for e in entries:
   raw=safe(e.get(item['path_key']));need(raw not in seen,'duplicate nested member');seen.add(raw);check_binding(member(base,raw),e)
  checked.append({'path':item['path'],'base':item['base'],'entries':len(entries),'schema_keys':[item['entries_key'],item['path_key']]})
 return checked

def replay_diagnostics(root):
 env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1'
 checks=[]
 root_program=root/'diagnostics/root_horowitz_checks.py';expected=json.loads((root/'diagnostics/ROOT_EXACT_DIAGNOSTICS.json').read_text());receipt=json.loads((root/'diagnostics/ROOT_REPLAY_RECEIPT.json').read_text())
 need(receipt['program_sha256']==hashlib.sha256(root_program.read_bytes()).hexdigest(),'root replay program receipt differs')
 need(receipt['result_sha256']==hashlib.sha256((root/'diagnostics/ROOT_EXACT_DIAGNOSTICS.json').read_bytes()).hexdigest(),'root replay result receipt differs')
 with tempfile.TemporaryDirectory(prefix='johnson-finite-replay-') as temp:
  tmp=Path(temp);script=tmp/root_program.name;shutil.copyfile(root_program,script)
  for flags in [[],['-O'],['-OO']]:
   run=subprocess.run([sys.executable,'-B',*flags,str(script)],env=env,cwd=tmp,capture_output=True,text=True,timeout=180)
   need(run.returncode==0,'root finite replay failed '+run.stderr);need(json.loads(run.stdout)==expected,'root finite replay differs')
  checks.append({'program':'diagnostics/root_horowitz_checks.py','modes':['normal','-O','-OO'],'all_results_match':True,'scope':'Exact finite free-word/SL2 checks only; no infinite/ambient theorem certificate.'})
  for family,program,result in [('source_question_family','verification.py','verification_results.json'),('convex_core_adversary','adversarial_checks.py','adversarial_results.json')]:
   folder=tmp/family;folder.mkdir();source=root/'reviews'/family/program;shutil.copyfile(source,folder/program)
   # Assertions are essential here: explicitly run a fresh normal interpreter,
   # regardless of the optimization mode of this outer integrity verifier.
   run=subprocess.run([sys.executable,'-B',str(folder/program)],env=env,cwd=folder,capture_output=True,text=True,timeout=180)
   need(run.returncode==0,'normal assertion-based replay failed '+family+' '+run.stderr)
   need((folder/result).read_bytes()==(root/'reviews'/family/result).read_bytes(),'normal finite replay result differs '+family)
   checks.append({'program':'reviews/'+family+'/'+program,'modes':['normal only, assertions enabled'],'result_bytes_match':True,'frozen_originals_mutated':False,'scope':'Finite consistency/boundary controls on a temporary copy; not the infinite geometric proof.'})
 return checks

def main():
 manifest=json.loads((ROOT/'MANIFEST.json').read_text());seen=set()
 need(manifest.get('schema')=='johnson-filtration-multiplicity-verification-v1','wrong root manifest target/schema')
 for e in manifest['files']:
  raw=safe(e['path']);need(raw not in seen,'duplicate root member');seen.add(raw);check_binding(member(ROOT,raw),e)
 actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
 need(actual==seen|{'MANIFEST.json'},'unlisted/missing archive member')
 nested=authenticate_nested_manifests(ROOT)
 original=json.loads((ROOT/'provenance/SUBMITTED_SNAPSHOT.json').read_text())
 need(original['pr']==1241 and original['problem_id']==11000082 and original['head']=='493a764dec034b7b645be76a284c4e6edc0583eb','wrong original snapshot identity')
 names={'ACCEPTANCE.json','ACCEPTANCE.md','AUDIT.md','MANIFEST.json','PROOF.md','README.md','SOURCES.json','VERIFICATION.json'}
 need(len(original['files'])==8 and {e['path'] for e in original['files']}=={'unsolved_math_prioritization/attempts/11000082/'+n for n in names},'wrong submitted scope')
 for e in original['files']:
  b=(ROOT/'original_submitted'/Path(e['path']).name).read_bytes();need(len(b)==e['bytes'],'submitted size');need(hashlib.sha256(b).hexdigest()==e['sha256'],'submitted digest');need(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==e['blob'],'submitted Git object identity')
 diagnostics=replay_diagnostics(ROOT)
 # Executing copied diagnostics cannot excuse mutations of any frozen member.
 for e in manifest['files']:check_binding(member(ROOT,e['path']),e)
 print(json.dumps({'status':'PASS','authenticated_members':len(seen),'submitted_files':8,'all_nested_manifests':nested,'finite_diagnostic_replays':diagnostics,'limits':'Byte bindings and scoped finite exact checks only. Infinite geometric and ambient-conjugacy conclusions and independence/priority rest on written arguments and documented acts. Omitted third-party source bodies and unavailable historical execution bodies are not reauthenticated; their inventories are receipts only.'},indent=2))
if __name__=='__main__':main()
