#!/usr/bin/env python3
"""Fresh isolated intended mathematical/domain mutation controls; no geometric proof."""
import hashlib,json,os,subprocess,sys,tempfile
from pathlib import Path
MUTATIONS = [{'name': 'wrong_discriminant_sign', 'old': 'discriminant = c*c-alpha*integral', 'new': 'discriminant = c*c+alpha*integral'}, {'name': 'wrong_quadratic_root', 'old': 'return integral/(c+rational_sqrt(discriminant))', 'new': 'return integral/(c-rational_sqrt(discriminant))'}, {'name': 'area_half_factor', 'old': 'return integral/(c+rational_sqrt(discriminant))', 'new': 'return integral/(2*(c+rational_sqrt(discriminant)))'}, {'name': 'radius_product_multiply', 'old': 'product = s/q', 'new': 'product = s*q'}, {'name': 'radius_root_wrong_factor', 'old': 'return ((s-root)/2, (s+root)/2)', 'new': 'return ((s-root)/4, (s+root)/4)'}, {'name': 'unscaled_degree_one_subtraction', 'old': 'return (scaled_g-scale*g)/(alpha*scale*(scale-1))', 'new': 'return (scaled_g-g)/(alpha*scale*(scale-1))'}, {'name': 'wrong_scale_determinant', 'old': 'return (scaled_g-scale*g)/(alpha*scale*(scale-1))', 'new': 'return (scaled_g-scale*g)/(alpha*scale*(scale+1))'}, {'name': 'mixed_area_missing_half', 'old': '-area(a)-area(b))/2', 'new': '-area(a)-area(b))'}, {'name': 'boolean_admitted', 'old': 'if isinstance(value, bool) or not isinstance(value, (int, Fraction)):', 'new': 'if not isinstance(value, (int, Fraction)):'}, {'name': 'negative_alpha_admitted', 'old': 'if c <= 0 or integral <= 0 or alpha < 0:', 'new': 'if c <= 0 or integral <= 0:'}, {'name': 'negative_scale_admitted', 'old': 'if scale <= 0 or scale == 1 or alpha <= 0:', 'new': 'if scale == 0 or scale == 1 or alpha <= 0:'}, {'name': 'disk_lens_missing_two', 'old': 'lens_perimeter=4*radius*acos', 'new': 'lens_perimeter=2*radius*acos'}]
EXPECTED_ERRORS = {'area_half_factor': ['RuntimeError', 'area recovery identity'], 'boolean_admitted': ['RuntimeError', 'meaningful negative was accepted'], 'disk_lens_missing_two': ['RuntimeError', 'disk asymptotic convergence'], 'mixed_area_missing_half': ['RuntimeError', 'same triangle mixed area'], 'negative_alpha_admitted': ['RuntimeError', 'independent invalid fixture accepted'], 'negative_scale_admitted': ['RuntimeError', 'meaningful negative was accepted'], 'radius_product_multiply': ['ValueError', 'inconsistent positive radius data'], 'radius_root_wrong_factor': ['RuntimeError', 'opposite curvature recovery'], 'unscaled_degree_one_subtraction': ['RuntimeError', 'two-scale separation'], 'wrong_discriminant_sign': ['ValueError', 'fixture requires an exact rational square root'], 'wrong_quadratic_root': ['ZeroDivisionError', 'Fraction(1, 0)'], 'wrong_scale_determinant': ['RuntimeError', 'two-scale separation']}
INPUT_PINS = {'audit/ACCEPTANCE.json': {'bytes': 3172, 'sha256': 'b610a347a9814166c8924ff5b0c51351fac38929adb6673e6dc8da2fbe522132'}, 'audit/AUDIT_REPORT.md': {'bytes': 23880, 'sha256': '6e8b26144bf56c4ca63caf954224b117ec51b43a886e77423485dafa03417dc9'}, 'audit/REVIEWED.patch': {'bytes': 8554, 'sha256': '57c7bcb9173135dfa228349a24c4e8d26c6dcd7c9816ae306871aa3ae8fc4cf0'}, 'audit/independent_checks.py': {'bytes': 6308, 'sha256': 'abc87ac20648ec2984a9ff621c9234b18cb89191341debb9c0736c68abdd978e'}, 'current/MANIFEST.json': {'bytes': 1264, 'sha256': 'e1f2171d6b7c00deeaa8fb343755699f821de8a61c22721a89920a690f8182ec'}, 'current/REPORT.md': {'bytes': 28553, 'sha256': '51eb0a2c80d1b46b959fe6aab793e088d7c4d14f0af639e0c0ab92485505813e'}, 'current/ROUTES.md': {'bytes': 5148, 'sha256': 'fd4f5625770bbd08d7f3001fff4af15c8bf2d08cec3e226add9261e9e4bd5672'}, 'current/SOURCE_INTERFACES.md': {'bytes': 5542, 'sha256': '363422c5971937339792b7a757a521a012291916c745fc066e5588bb2a7bc35c'}, 'current/TEST_RESULTS.json': {'bytes': 2161, 'sha256': '826113f911e6b6ac808391b13dabe487bce99fe2f5088164e4cc2222155a063e'}, 'current/check_covariogram_lemmas.py': {'bytes': 6686, 'sha256': '7169a26fab2cbc3a59cea1139b69357b6bc0fd49d5439862b84eacbb60ab037e'}, 'historical/FINAL_READ_ONLY_REPLAY.json': {'bytes': 17495, 'sha256': '63593535a95f9f2e8f04f05ddaadde2753e9f46ef826f62ec1cfc72d02c1ab9a'}, 'historical/FROZEN_EVIDENCE.json': {'bytes': 1080, 'sha256': '179228b2702078182f36ef309b70640022f31b87710c01443eb080a45176cada'}, 'historical/MUTATION_DEFINITIONS.json': {'bytes': 1807, 'sha256': 'd144ad8296c48b17b1a67c61664187d191895ce374facb288b7e1fed612fa231'}, 'historical/PATCH_REPLAY.json': {'bytes': 334, 'sha256': 'd3537f5ab2a6342dc5cbc375b96cee0a1a17c6b0fd482aa50ecadeb3b3d2b77a'}, 'historical/SOURCE_CHECK.json': {'bytes': 2606, 'sha256': 'dd3d426ff809f9b95aa084091618900e4f4a46b48303f92a5536f1822b95b574'}}
DOMAIN = {'boolean_admitted','negative_alpha_admitted','negative_scale_admitted'}
RUNNER = "import json,sys\nfrom pathlib import Path\nns={'__name__':'audited_independent','__file__':sys.argv[1]}\nexec(compile(Path(sys.argv[1]).read_bytes(),'audit/independent_checks.py','exec'),ns)\ntry:\n result=ns['check_source'](sys.argv[2],True)\nexcept Exception as exc:\n print(json.dumps(dict(error_type=type(exc).__name__,error=str(exc)),sort_keys=True))\n sys.exit(1)\nprint(json.dumps(result,sort_keys=True))\n"
sha=lambda b:hashlib.sha256(b).hexdigest()
def need(ok,message):
 if not ok:raise ValueError(message)
def same(a,b):
 if type(a) is not type(b):return False
 if type(b) is dict:return set(a)==set(b) and all(same(a[k],v) for k,v in b.items())
 if type(b) is list:return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
 return a==b
def main():
 root=Path(__file__).resolve().parent
 need(os.getuid()==os.geteuid()==1000,'UID=EUID=1000');need(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,'-I -S -B')
 def snapshot():return {n:dict(bytes=len(b),sha256=sha(b)) for n in INPUT_PINS for b in [(root/n).read_bytes()]}
 before=snapshot();need(same(before,INPUT_PINS),'exact 15 accepted input identities and hashes')
 source=(root/'current/check_covariogram_lemmas.py').read_text();physical=[];runs=[]
 def probe(p,label,create):
  need((p.stat().st_mode&0o777)==(0o555 if create else 0o444) and not os.access(p,os.W_OK),'read-only mode')
  try:fd=os.open(p/'DENIED' if create else p,os.O_WRONLY|(os.O_CREAT|os.O_EXCL if create else os.O_APPEND),0o600)
  except PermissionError as exc:need(exc.errno==13,'EACCES required');physical.append(dict(path=label,operation='create' if create else 'append_open',errno=13,denied=True))
  else:os.close(fd);raise ValueError('physical denial missing')
 probe(root/'current','current',True);probe(root/'current/check_covariogram_lemmas.py','current/check_covariogram_lemmas.py',False)
 mode=[] if sys.flags.optimize==0 else ['-'+'O'*sys.flags.optimize];env=dict(PATH=os.defpath,HOME='/tmp',TMPDIR='/tmp',LC_ALL='C')
 with tempfile.TemporaryDirectory(prefix='covariogram-mutations-') as td:
  td=Path(td);paths=[]
  try:
   for row in MUTATIONS:
    name,old,new=row['name'],row['old'],row['new'];need(source.count(old)==1,'unique mutation target '+name)
    d=td/name;d.mkdir();candidate=d/'candidate.py';candidate.write_text(source.replace(old,new));candidate.chmod(0o444);d.chmod(0o555);paths.append(d)
   td.chmod(0o555)
   def variants_snapshot():return {str(p.relative_to(td)):dict(bytes=len(b),sha256=sha(b),mode=oct(p.stat().st_mode&0o777)) for p in sorted(td.rglob('*')) if p.is_file() for b in [p.read_bytes()]}
   variant_before=variants_snapshot()
   for row in MUTATIONS:
    name=row['name'];d=td/name;candidate=d/'candidate.py';probe(d,name,True);probe(candidate,name+'/candidate.py',False)
    r=subprocess.run([sys.executable,'-I','-S','-B',*mode,'-c',RUNNER,str(root/'audit/independent_checks.py'),str(candidate)],cwd=root,env=env,capture_output=True,timeout=30)
    error_type,error=EXPECTED_ERRORS[name];expected=dict(error_type=error_type,error=error);raw=(json.dumps(expected,sort_keys=True)+'\n').encode()
    need(type(r.returncode) is int and r.returncode==1 and r.stdout==raw and r.stderr==b'' and same(json.loads(r.stdout),expected),'wrong intended rejection '+name)
    runs.append(dict(control=name,category='input_domain' if name in DOMAIN else 'finite_mathematics',exit_code=r.returncode,stdout=r.stdout.decode(),stderr=r.stderr.decode(),intended_error_type=error_type,intended_error=error,intended_rejection_verified=True,full_raw_output_equal=True,recursive_exact_json_equal=True))
   variant_after=variants_snapshot();need(variant_before==variant_after,'read-only variants changed')
  finally:
   td.chmod(0o755)
   for d in paths:
    d.chmod(0o755)
    for p in d.iterdir():p.chmod(0o644)
 need([r['control'] for r in runs]==[r['name'] for r in MUTATIONS] and len(runs)==12,'exact semantic identities and count')
 need(sum(r['category']=='finite_mathematics' for r in runs)==9 and sum(r['category']=='input_domain' for r in runs)==3,'exact mutation categories')
 after=snapshot();need(after==before,'protected accepted inputs changed')
 print(json.dumps(dict(schema=1,problem_id=30000630,status='PASS',uid=os.getuid(),euid=os.geteuid(),optimization=sys.flags.optimize,semantic_mutants=12,finite_mathematics_mutants=9,input_domain_mutants=3,physical_denials=physical,runs=runs,before=before,after=after,variant_before=variant_before,variant_after=variant_after,whole_mathematics_unchanged=True,limitations='Finite algebra/constants and input-domain regressions only; geometric proofs and classical dependencies require written review.'),sort_keys=True))
if __name__=='__main__':
 try:main()
 except (ValueError,OSError,TypeError,KeyError,subprocess.TimeoutExpired) as exc:print('REJECT: semantic controls failed: '+str(exc),file=sys.stderr);sys.exit(1)
