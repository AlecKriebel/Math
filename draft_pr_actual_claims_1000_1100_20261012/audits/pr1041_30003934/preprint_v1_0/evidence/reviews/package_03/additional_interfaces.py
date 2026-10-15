#!/usr/bin/env python3
from pathlib import Path
import subprocess,os,sys,tarfile,json,datetime,hashlib,shutil
HERE=Path(__file__).resolve().parent;CAND=HERE.parent.parent/'preprint_v1_0';env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');records=[]
def run(tag,args,cwd,ok=True):
 p=subprocess.run(args,cwd=cwd,env=env,capture_output=True,text=True);(HERE/(tag+'_STDOUT.txt')).write_text(p.stdout);(HERE/(tag+'_STDERR.txt')).write_text(p.stderr)
 if (p.returncode==0)!=ok:raise RuntimeError(tag+p.stderr)
 r={'tag':tag,'args':args,'returncode':p.returncode,'expected_pass':ok,'stdout_sha256':hashlib.sha256(p.stdout.encode()).hexdigest(),'stderr_sha256':hashlib.sha256(p.stderr.encode()).hexdigest()};records.append(r);return p
opt=HERE/'private/clean_opt';opt.mkdir()
with tarfile.open(CAND/'supportkit-v1.0.tar.gz','r:gz') as t:t.extractall(opt,filter='data')
kit=opt/'rank_one_uniqueness_v1_0'
run('OPT_CLEAN_VERIFY_BEFORE',[sys.executable,'-O','verify_package.py'],kit)
run('OPT_CLEAN_REQUIRE_ABSENT_BEFORE',[sys.executable,'-O','verify_package.py','--require-deposit'],kit,False)
run('OPT_CLEAN_BUILD',[sys.executable,'-O','build_archive.py'],kit)
run('OPT_CLEAN_VERIFY_AFTER',[sys.executable,'-O','verify_package.py'],kit)
run('OPT_CLEAN_REQUIRE_ABSENT_AFTER',[sys.executable,'-O','verify_package.py','--require-deposit'],kit,False)
original=(CAND/'supportkit-v1.0.tar.gz').read_bytes()
if (kit/'supportkit-v1.0.tar.gz').read_bytes()!=original:raise RuntimeError('Optimized archive mismatch')
# Inject source/ignored/intermediate files outside and inside excluded folders.
probes={'raw/source.pdf':b'%PDF-source','rawprivate/source.txt':b'private body','private/secret.json':b'{"private":true}','fullsource.txt':b'extracted source body','source.pdf':b'%PDF-source','source.png':b'\x89PNG\r\n\x1a\n','render/page.png':b'pixels','replay/output.json':b'{}','cache/temp.md':b'cache','sources/CITATION_DISCOVERY.json':b'{"response":"raw"}','__pycache__/x.pyc':b'code'}
for name,data in probes.items():p=kit/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
run('OPT_EXCLUSION_BUILD',[sys.executable,'-O','build_archive.py'],kit)
run('OPT_EXCLUSION_VERIFY',[sys.executable,'-O','verify_package.py'],kit)
if (kit/'supportkit-v1.0.tar.gz').read_bytes()!=original:raise RuntimeError('Excluded material changed archive')
shutil.copy2(CAND/'zenodo-deposit.json',kit/'zenodo-deposit.json');run('OPT_CLEAN_REQUIRE_PRESENT',[sys.executable,'-O','verify_package.py','--require-deposit'],kit)
# Sentinel intentionally false guards remain active in both modes.
for mode in [False,True]:
 for file,guard in [('private/replay_flow/flow_check.py','demand'),('math_checks.py','need')]:
  cmd="import runpy; f=runpy.run_path("+repr(str(HERE/file))+"); f["+repr(guard)+"](False,'review03_false_guard')"
  run('GUARD_'+guard+('_optimized' if mode else '_normal'),[sys.executable]+(['-O'] if mode else [])+['-c',cmd],HERE,False)
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','records':records,'optimized_clean_sequence_byte_identical':True,'excluded_probe_count':len(probes),'excluded_material_changes_archive':False,'explicit_guard_failures_in_both_modes':True}
(HERE/'ADDITIONAL_INTERFACES.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2))
