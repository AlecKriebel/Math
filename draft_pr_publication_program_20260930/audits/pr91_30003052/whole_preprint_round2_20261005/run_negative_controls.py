from pathlib import Path
import datetime, hashlib, json, os, shutil, subprocess, time
O=Path(__file__).resolve().parent
R=O/'extracted_root'
base=O/'negative_controls'; base.mkdir()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
env={k:v for k,v in os.environ.items() if not k.startswith('PYTHON')}
def execute(label,argv,cwd,sources):
 d=base/label;d.mkdir()
 rec={'label':label,'argv':argv,'cwd':str(cwd),'recorder_pid':os.getpid(),'started_utc':now(),'sources':[{"path":str(p),"sha256":sha(p),"bytes":p.stat().st_size} for p in sources]}
 t=time.monotonic()
 with (d/'stdout.bin').open('wb') as so,(d/'stderr.bin').open('wb') as se:
  p=subprocess.Popen(argv,cwd=cwd,env=env,stdout=so,stderr=se);rec['pid']=p.pid
  (d/'execution.json').write_text(json.dumps(rec,indent=2)+'\n');rec['exit_code']=p.wait()
 rec.update({'ended_utc':now(),'elapsed_seconds':time.monotonic()-t,'streams':{n:{'sha256':sha(d/n),'bytes':(d/n).stat().st_size} for n in ['stdout.bin','stderr.bin']}})
 (d/'execution.json').write_text(json.dumps(rec,indent=2)+'\n')
 return d,rec
outcomes=[]
for name,marker in [('verify.py','def zero(M)'),('independent_checks.py','def zero(M)'),('boundary_checks.py','def M(rows)')]:
 src=R/'verification'/name; text=src.read_text()
 if marker not in text:raise RuntimeError('marker not found')
 false=base/('false_'+name);false.write_text(text.replace(marker,'ck("round2_deliberately_false", False)\n'+marker,1))
 for optimized in [False,True]:
  label=name.removesuffix('.py')+('_optimized' if optimized else '_ordinary')
  requested=base/(label+'_forbidden_success_receipt.json')
  argv=['/usr/bin/python3','-E','-B']+(['-O'] if optimized else [])+[str(false),'--output',str(requested)]
  if name!='boundary_checks.py':argv+=['--artifact',str(R/'pr91_note.tex')]
  d,rec=execute(label,argv,R,[src,false,R/'pr91_note.tex'])
  stderr=(d/'stderr.bin').read_text()
  valid=rec['exit_code']!=0 and 'round2_deliberately_false' in stderr and not requested.exists() and (d/'stdout.bin').stat().st_size==0
  outcomes.append({'label':label,'expected_failure_observed':valid,'exit_code':rec['exit_code'],'receipt_absent':not requested.exists()})
  if not valid:raise RuntimeError('false control failed open: '+label)
clone=base/'tampered_extracted_root';shutil.copytree(R,clone)
p=clone/'verification/verify.py';p.write_text(p.read_text()+'\n# Private round-two source-tamper test.\n')
argv=['/usr/bin/python3','-E','-B','verification/run_all.py','--output-dir',str(base/'tampered_output')]
d,rec=execute('wrapper_tampered_source',argv,clone,[clone/'verification/run_all.py',p,clone/'verification/SOURCE_PROVENANCE.json'])
valid=rec['exit_code']!=0 and 'source hash mismatch: verify.py' in (d/'stderr.bin').read_text() and not (base/'tampered_output').exists()
outcomes.append({'label':'wrapper_tampered_source','expected_failure_observed':valid,'exit_code':rec['exit_code']})
if not valid:raise RuntimeError('tampered wrapper failed open')
argv=['/usr/bin/python3','-E','-B','verification/run_all.py','--output-dir',str(O/'portable_reproduction')]
d,rec=execute('wrapper_nonempty_output',argv,R,[R/'verification/run_all.py',R/'verification/SOURCE_PROVENANCE.json'])
valid=rec['exit_code']!=0 and '--output-dir must be empty' in (d/'stderr.bin').read_text()
outcomes.append({'label':'wrapper_nonempty_output','expected_failure_observed':valid,'exit_code':rec['exit_code']})
if not valid:raise RuntimeError('nonempty output failed open')
(O/'NEGATIVE_CONTROLS_SUMMARY.json').write_text(json.dumps({'all_expected_failures_observed':all(x['expected_failure_observed'] for x in outcomes),'outcomes':outcomes,'note':'All alterations are private clones; supplied package bytes were not edited.'},indent=2)+'\n')
print(json.dumps(outcomes,indent=2))
