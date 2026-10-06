#!/usr/bin/env python3
"""Fresh review subprocess custody; copies sealed inputs and confines all scratch."""
from pathlib import Path
import datetime,hashlib,json,os,shutil,subprocess,sys
O=Path(__file__).resolve().parent
A=O.parent
D=A/'publication_ready_package_v2'
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def digest(b):return hashlib.sha256(b).hexdigest()
def run(tag,argv,cwd=None,expect=0):
    (O/'receipts').mkdir(exist_ok=True)
    start=utc(); env=os.environ.copy(); env['PYTHONDONTWRITEBYTECODE']='1';env['TMPDIR']=str(O/'scratch'/'tmp')
    proc=subprocess.Popen(argv,cwd=cwd or O,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=proc.communicate();end=utc()
    (O/'receipts').mkdir(exist_ok=True)
    (O/'receipts'/f'{tag}.stdout.bin').write_bytes(out);(O/'receipts'/f'{tag}.stderr.bin').write_bytes(err)
    rec=dict(tag=tag,argv=argv,cwd=str(cwd or O),actual_PID=proc.pid,start_UTC=start,end_UTC=end,actual_exit=proc.returncode,expected_exit=expect,stdout_bytes=len(out),stderr_bytes=len(err),stdout_sha256=digest(out),stderr_sha256=digest(err),environment_overrides={'TMPDIR':env['TMPDIR'],'PYTHONDONTWRITEBYTECODE':'1'})
    (O/'receipts'/f'{tag}.json').write_text(json.dumps(rec,indent=2)+'\n')
    if proc.returncode!=expect:raise RuntimeError(rec)
    print(json.dumps(rec))
    return out
if __name__=='__main__':
    (O/'scratch'/'tmp').mkdir(parents=True,exist_ok=True)
    if sys.argv[1]=='runner':
      source=O/'scratch'/'source'
      if not source.exists():shutil.copytree(D/'source_preparation',source)
      for label,opt in [('runner_normal',[]),('runner_optimized',['-O'])]:
        run(label,[sys.executable,*opt,'-B',str(source/'run_checks.py'),'--include-historical','--output',str(O/'receipts'/f'{label}_internal.json')],source)
    elif sys.argv[1]=='provenance':
      run('provenance_diagnostics',[sys.executable,'-B',str(O/'provenance_diagnostics.py')],O)
    elif sys.argv[1]=='pdf':
      run('pdfinfo',['/opt/homebrew/bin/pdfinfo','-meta',str(D/'root_dependent_spanning_trees.pdf')],O)
      run('pdfinfo_general',['/opt/homebrew/bin/pdfinfo',str(D/'root_dependent_spanning_trees.pdf')],O)
      run('pdffonts',['/opt/homebrew/bin/pdffonts',str(D/'root_dependent_spanning_trees.pdf')],O)
    elif sys.argv[1]=='original':
      checkout=A.parents[2]
      run('original_head_source_record',['git','show','3526d46bf143b08e5055ffa7728c6278e9f958ea:unsolved_math_prioritization/attempts/30003996/source_record.json'],checkout)
      run('original_head_queue',['git','show','3526d46bf143b08e5055ffa7728c6278e9f958ea:unsolved_math_prioritization/QUEUE.md'],checkout)
      run('checkout_branch',['git','branch','--show-current'],checkout)
    elif sys.argv[1]=='diagnostics':
      for label,opt in [('fresh_diagnostics_normal',[]),('fresh_diagnostics_optimized',['-O'])]:
        run(label,[sys.executable,*opt,'-B',str(O/'independent_diagnostics.py')],O)
