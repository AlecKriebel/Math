#!/usr/bin/env python3
"""Run seven unchanged exact controls in temporary mirrors; Python3.10+ stdlib.

The analytic proofs establish universal claims. These checks corroborate them.
No networking, package installation, or mutation of supplied material occurs.
"""
import argparse,ast,concurrent.futures,hashlib,json
from pathlib import Path
import subprocess,sys,tempfile

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
AUDIT=ROOT/'audit' if (ROOT/'audit').is_dir() else ROOT.parent

def digest(raw):return hashlib.sha256(raw).hexdigest()
def pinned(path,pin):
 raw=path.read_bytes()
 if len(raw)!=pin['bytes'] or digest(raw)!=pin['sha256']:
  raise RuntimeError('Fingerprint mismatch: '+str(path))
 return raw

def run(job):
 spec,optimized,inputs=job
 code=pinned(AUDIT/spec['file'],spec['pin'])
 if any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(code))):
  raise RuntimeError('Optimization-sensitive assertion: '+spec['file'])
 expected=json.loads(pinned(AUDIT/spec['expected'],spec['expected_pin']))
 if spec['expected_key']:expected=expected[spec['expected_key']]
 with tempfile.TemporaryDirectory(prefix='lattice-verification-') as tmp:
  mirror=Path(tmp)/'audit';source=mirror/spec['file'];source.parent.mkdir(parents=True)
  source.write_bytes(code)
  (mirror/'inputs').mkdir()
  for name,pin in inputs.items():
   (mirror/'inputs'/name).write_bytes(pinned(AUDIT/'inputs'/name,pin))
  for name,pin in spec['auxiliary'].items():
   p=mirror/name;p.parent.mkdir(parents=True,exist_ok=True)
   p.write_bytes(pinned(AUDIT/name,pin))
  args=[sys.executable,'-B']+(['-O'] if optimized else [])+[str(source)]
  result=subprocess.run(args,capture_output=True,text=True)
  if result.returncode:raise RuntimeError(spec['file']+': '+result.stderr[-3000:])
  actual=json.loads(result.stdout)
  if actual!=expected:raise RuntimeError('Result mismatch: '+spec['file'])
  guard_exit=None
  if spec['guard']:
   failed=subprocess.run(args+[spec['guard']],capture_output=True,text=True)
   guard_exit=failed.returncode
   if guard_exit==0 or not failed.stderr:raise RuntimeError('Failure guard inactive')
 return {'checker':spec['file'],'optimized':optimized,'sha256':spec['pin']['sha256'],
         'complete_result_equal':True,'negative_guard_exit':guard_exit}

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--mode',choices=['both','ordinary','optimized'],default='both')
 args=p.parse_args();plan=json.loads((HERE/'CONTROL_PLAN.json').read_text())
 modes=[False,True] if args.mode=='both' else [args.mode=='optimized']
 jobs=[(s,o,plan['inputs']) for s in plan['controls'] for o in modes]
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(run,jobs))
 print(json.dumps({'status':'PASS','controls':len(plan['controls']),'runs':results,
                   'inputs_authenticated':len(plan['inputs']),'finite_checks_supplement_written_proofs':True},indent=2,sort_keys=True))

if __name__=='__main__':main()
