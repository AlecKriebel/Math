#!/usr/bin/env python3
"""Independent orchestrator fault injection; all mutations confined to temp copies."""
from pathlib import Path
import importlib.util,hashlib,json,shutil,sys,tempfile,types,contextlib,io,zipfile,argparse
HERE=Path(__file__).resolve().parent
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--archive',type=Path,default=HERE.parent.parent/'publication/verification_package.zip')
args=parser.parse_args()
assert hashlib.sha256(args.archive.read_bytes()).hexdigest()=='3b9f38102723c3d1c62a762417f31c147d52569827edd23d0052254e0939d54b','This review requires its initial frozen ZIP; supply --archive PATH to that version.'
with zipfile.ZipFile(args.archive) as z:
 ORIGINAL={name.removeprefix('weighted_centers_verification/'):z.read(name) for name in z.namelist()}
(HERE/'.cache').mkdir(exist_ok=True)

def digest(b):return hashlib.sha256(b).hexdigest()
def encode(j):return (json.dumps(j,indent=2)+'\n').encode()
def reseal(p):
 for name in json.loads((p/'SEALS.json').read_bytes()):
  seal=p/name;lines=[]
  for line in seal.read_text().splitlines():
   _,rel=line.split('  ',1);lines.append(digest((seal.parent/rel).read_bytes())+'  '+rel)
  seal.write_text('\n'.join(lines)+'\n')
 m=json.loads((p/'MANIFEST.json').read_bytes())
 m['files']={name:{'bytes':len((p/name).read_bytes()),'sha256':digest((p/name).read_bytes())} for name in m['files'] if (p/name).exists()}
 (p/'MANIFEST.json').write_bytes(encode(m))

def invoke(p,actual_override=None):
 spec=importlib.util.spec_from_file_location('integrity',p/'integrity.py');integ=importlib.util.module_from_spec(spec);spec.loader.exec_module(integ);sys.modules['integrity']=integ
 spec=importlib.util.spec_from_file_location('candidate_replay',p/'run_all.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);mod.ROOT=p
 # Isolate JSON comparison/control-flow logic; full real jobs are independently replayed separately.
 def fake_run(args,**kw):
  script=Path(args[1])
  jobs=json.loads(ORIGINAL['JOBS.json'])
  key=next(j['script'] for j in jobs if script.as_posix().endswith(j['script']))
  job=next(j for j in jobs if j['script']==key);actual=json.loads(ORIGINAL[job['record']])
  if actual_override:actual_override(key,actual)
  return types.SimpleNamespace(returncode=0,stdout=json.dumps(actual),stderr='')
 mod.subprocess=types.SimpleNamespace(run=fake_run)
 try:
  with contextlib.redirect_stdout(io.StringIO()):mod.main()
 except Exception as e:return {'accepted':False,'error':str(e)}
 return {'accepted':True}

def main():
 results=[]
 cases=['bad_payload','extra_file','missing_nested_file_after_outer_reseal','missing_nested_seal_after_outer_reseal','bad_nested_digest_after_outer_reseal','wrong_expected_math_after_all_reseals','unsupported_clock_normalization_after_reseal','clock_normalization_on_wrong_job','mathematical_actual_field_changed','nested_clock_named_math_changed','allowed_three_clocks_only']
 for name in cases:
  with tempfile.TemporaryDirectory(dir=HERE/'.cache',prefix='negative-') as tmp:
   p=Path(tmp)
   for key,b in ORIGINAL.items():(p/key).parent.mkdir(parents=True,exist_ok=True);(p/key).write_bytes(b)
   override=None
   if name=='bad_payload':(p/'README.md').write_bytes(b'bad')
   elif name=='extra_file':(p/'UNREGISTERED.json').write_bytes(b'{}')
   elif name=='missing_nested_file_after_outer_reseal':(p/'reviews/priority02/REPORT.md').unlink();m=json.loads((p/'MANIFEST.json').read_bytes());m['files'].pop('reviews/priority02/REPORT.md');(p/'MANIFEST.json').write_bytes(encode(m))
   elif name=='missing_nested_seal_after_outer_reseal':(p/'reviews/priority02/SHA256SUMS').unlink();m=json.loads((p/'MANIFEST.json').read_bytes());m['files'].pop('reviews/priority02/SHA256SUMS');(p/'MANIFEST.json').write_bytes(encode(m))
   elif name=='bad_nested_digest_after_outer_reseal':
    seal=p/'reviews/priority02/SHA256SUMS';s=seal.read_text();seal.write_text(('0' if s[0]!='0' else '1')+s[1:]);m=json.loads((p/'MANIFEST.json').read_bytes());m['files']['reviews/priority02/SHA256SUMS']={'bytes':seal.stat().st_size,'sha256':digest(seal.read_bytes())};(p/'MANIFEST.json').write_bytes(encode(m))
   elif name=='wrong_expected_math_after_all_reseals':
    record=p/'reviews/oracle01/CONTROL_RESULTS.json';j=json.loads(record.read_bytes());j['fault_injected_mathematical_result']=999;record.write_bytes(encode(j));reseal(p)
   elif name in ('unsupported_clock_normalization_after_reseal','clock_normalization_on_wrong_job'):
    record=p/'JOBS.json';j=json.loads(record.read_bytes())
    if name=='unsupported_clock_normalization_after_reseal':j[2]['ignored_clock_fields'].append('counts')
    else:j[0]['ignored_clock_fields']=['started_at_utc','completed_at_utc','elapsed_seconds']
    record.write_bytes(encode(j));reseal(p)
   elif name=='mathematical_actual_field_changed':
    def override(key,j):
     if key=='reviews/oracle01/controls.py':j['fault_injected_mathematical_result']=999
   elif name=='nested_clock_named_math_changed':
    def override(key,j):
     if key=='reviews/oracle01/controls.py':j['fault_injected_nested']={'started_at_utc':999}
   elif name=='allowed_three_clocks_only':
    def override(key,j):
     if key=='reviews/oracle01/controls.py':
      for field in ('started_at_utc','completed_at_utc','elapsed_seconds'):j[field]='INTENTIONAL_EXECUTION_CLOCK_DIFFERENCE'
   result=invoke(p,override);want=name=='allowed_three_clocks_only';assert result['accepted']==want,(name,result);results.append({'case':name,'expected_acceptance':want,**result})
 # Producer absolute-ancestor rejection reproducer uses an unmodified copied audit structure.
 with tempfile.TemporaryDirectory(dir=HERE/'.cache',prefix='producer-checkout-') as tmp:
  prod=Path(tmp)
  for key,b in ORIGINAL.items():(prod/key).parent.mkdir(parents=True,exist_ok=True);(prod/key).write_bytes(b)
  pub=prod/'publication';pub.mkdir()
  for key in ('make_package.py','integrity.py','weighted_centers.tex'):(pub/key).write_bytes(ORIGINAL[key])
  proc=__import__('subprocess').run([sys.executable,str(pub/'make_package.py')],capture_output=True,text=True)
 assert proc.returncode!=0 and 'Excluded source: weighted_centers.tex' in proc.stderr
 results.append({'case':'producer_valid_checkout_below_cache','exit_code':proc.returncode,'error':'Excluded source: weighted_centers.tex','finding':'Unrelated absolute checkout ancestry triggers payload-source exclusion.'})
 print(json.dumps({'status':'PASS','method':'Copied archive payloads, integrity validation and full main orchestration; mocked subprocess output only for precise differential comparison tests. Separate real offline replay checks all five actual scripts.','controls':results},indent=2))

if __name__=='__main__':main()
