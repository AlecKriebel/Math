"""Run the public exact verification checks into a NEW output directory."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,os,subprocess,sys
if sys.flags.optimize:
    raise SystemExit('Assertions must be enabled; remove -O/PYTHONOPTIMIZE.')
P=Path(__file__).resolve().parent;sha=lambda b:hashlib.sha256(b).hexdigest();utc=lambda:datetime.now(timezone.utc).isoformat()
parser=argparse.ArgumentParser();parser.add_argument('--out-dir',type=Path,required=True);args=parser.parse_args()
O=args.out_dir.resolve();O.mkdir(parents=True,exist_ok=False)
env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None)
jobs=[]
for label,cmd in [('boundary',[sys.executable,str(P/'verify_boundary.py')]),
 ('priority_laws',[sys.executable,str(P/'verify_priority_examples.py'),'--output',str(O/'priority_laws.json')])]:
    j=dict(argv=cmd,cwd=str(P),started_utc=utc(),source_sha256=sha(Path(cmd[1]).read_bytes()))
    (O/(label+'_spec.json')).write_text(json.dumps(j,indent=2)+'\n')
    r=subprocess.run(cmd,cwd=P,env=env,capture_output=True)
    for k,b in [('stdout',r.stdout),('stderr',r.stderr)]: (O/(label+'.'+k)).write_bytes(b)
    j.update(ended_utc=utc(),exit_code=r.returncode,stdout_sha256=sha(r.stdout),stderr_sha256=sha(r.stderr))
    (O/(label+'_execution.json')).write_text(json.dumps(j,indent=2)+'\n');jobs.append(j)
    assert r.returncode==0 and not r.stderr, (label,'failed')
    if label=='boundary':
        assert json.loads(r.stdout)==json.loads((P/'expected/boundary.json').read_bytes())
    else:
        assert (O/'priority_laws.json').read_bytes()==(P/'expected/priority_laws.json').read_bytes()
receipt=dict(actual_utc=utc(),status='PASS_EXACT_PUBLIC_REPRODUCTION',jobs=jobs,
 limitations='Finite examples and residual-network checks supplement the all-graph prose proof. No formal proof-assistant certification or historical absence certificate.')
(O/'REPRODUCTION_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(dict(status=receipt['status'],output_directory=str(O)),indent=2))
