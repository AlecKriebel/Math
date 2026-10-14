from pathlib import Path
import subprocess,json,datetime,shutil,concurrent.futures
HERE=Path(__file__).resolve().parent; AUDIT=HERE.parent.parent; PY= AUDIT/'tmp/venv/bin/python'; ROOT=HERE/'tmp/extracted'; PDF=AUDIT/'publication/output/pdf/note.pdf'; anchor='a50792f1c2d55ba4b4d0085369ca08b0d47296d1a3963ea0c2fe820433093832'
def run(optimized):
 args=[str(PY)]+(['-O'] if optimized else [])+[str(ROOT/'verify_package.py'),'--expected-manifest',anchor,'--pdf',str(PDF)]
 p=subprocess.run(args,cwd=ROOT,capture_output=True,text=True,timeout=600)
 label='optimized' if optimized else 'normal'
 (HERE/f'evidence/replay_{label}.stdout').write_text(p.stdout); (HERE/f'evidence/replay_{label}.stderr').write_text(p.stderr)
 result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'optimized_wrapper':optimized,'returncode':p.returncode,'output':json.loads(p.stdout) if p.returncode==0 else p.stdout,'stderr':p.stderr}
 (HERE/f'evidence/replay_{label}.json').write_text(json.dumps(result,indent=2)+'\n')
 if p.returncode:raise RuntimeError(label+' '+p.stderr)
 return {'label':label,'returncode':p.returncode,'status':result['output']['status'],'payloads':result['output']['payload_files']}
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool: print(json.dumps(list(pool.map(run,(False,True))),indent=2))
