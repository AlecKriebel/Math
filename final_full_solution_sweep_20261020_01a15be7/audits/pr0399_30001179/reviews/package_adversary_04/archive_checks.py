#!/usr/bin/env python3
from pathlib import Path
import argparse,copy,hashlib,json,os,shutil,subprocess,sys,zipfile
R=Path(__file__).resolve().parent;A=R.parents[1];P=A.parents[1]/'private/pr0399_package04';bundle=P/'archive/free-product-tensor-core-verification'
parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path);args=parser.parse_args();OUTPUT=R
if args.output is not None:
 if not args.output.is_absolute() or not args.output.is_relative_to(A.parents[1]/'private'):raise RuntimeError('New private output required')
 args.output.mkdir(parents=True,exist_ok=False);P=args.output;OUTPUT=P
 with zipfile.ZipFile(A/'preprint/publication/free-product-tensor-core-verification.zip') as z:z.extractall(P/'archive')
 bundle=P/'archive/free-product-tensor-core-verification'
def sha(b):return hashlib.sha256(b).hexdigest()
def run(args,expected=0):
 r=subprocess.run(args,capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','PYTHONOPTIMIZE':'2'})
 if (r.returncode==0)!=(expected==0):raise RuntimeError('unexpected outcome '+r.stderr[:200])
 return {'command':args,'returncode':r.returncode,'stdout_sha256':sha(r.stdout.encode()),'stdout':r.stdout if expected==0 else None,'stderr':r.stderr if expected else None}
results=[]
for flags in [[],['-O']]:
 results.append(run([sys.executable,*flags,'-B',str(bundle/'tools/reproduce.py'),str(bundle)]))
 results.append(run([sys.executable,*flags,'-B',str(bundle/'tools/test_integrity_controls.py'),str(P/('negative_'+str(len(flags))))]))
# Rehash all layers after injecting a false historical nested assertion.
for mode in [0,1]:
 dest=P/('semantic_assert_mutant_'+str(mode));shutil.copytree(bundle,dest)
 p=dest/'original/check_density_chain.py';p.write_text(p.read_text()+"\nassert False, 'PACKAGE04_NESTED_SENTINEL'\n")
 old=dest/'original/PUBLIC_PACKET_MANIFEST.json';v=json.loads(old.read_text());v['files']['check_density_chain.py']={'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())};old.write_text(json.dumps(v,indent=2)+'\n')
 manifest=dest/'FILES.json';v=json.loads(manifest.read_text())
 for e in v['files']:
  body=(dest/e['path']).read_bytes();e['bytes']=len(body);e['sha256']=sha(body)
 manifest.write_text(json.dumps(v,indent=2)+'\n')
 integrity=run([sys.executable,'-B',str(dest/'tools/integrity.py'),str(dest)])
 replay=run([sys.executable,*(['-O'] if mode else []),'-B',str(dest/'tools/reproduce.py'),str(dest)],1)
 if 'PACKAGE04_NESTED_SENTINEL' not in replay['stderr']:raise RuntimeError('nested sentinel not reached')
 results.append({'mutant':'false nested assertion after manifests rehashed','outer_optimization':mode,'integrity':integrity,'replay':replay})
(OUTPUT/'ARCHIVE_CHECKS.json').write_text(json.dumps({'inherited_PYTHONOPTIMIZE':'2','runs':results},indent=2)+'\n')
print(json.dumps({'baseline_replays':2,'integrity_suites':2,'semantic_mutants_rejected':2,'baseline_stdout_equal':results[0]['stdout_sha256']==results[2]['stdout_sha256']},indent=2))
