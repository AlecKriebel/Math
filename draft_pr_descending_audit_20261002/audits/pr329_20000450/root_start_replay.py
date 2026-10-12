from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess
A=Path(__file__).resolve().parent
D=A/'root_replays_private/author001';D.mkdir(parents=True,exist_ok=False)
utc=lambda:datetime.now(timezone.utc).isoformat()
sha=lambda b:hashlib.sha256(b).hexdigest()
p=A/'ROOT_FIRST_CANDIDATE_ASSESSMENT.md'
freeze={'utc':utc(),'assessment_path':str(p),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes()),
    'stage':'FIRST_ROOT_CANDIDATE_ASSESSMENT_BEFORE_INHERITED_PR_VERDICTS','workflow_percent':15,'mathematical_verification_percent':20}
(A/'ROOT_FIRST_ASSESSMENT_FREEZE.json').write_text(json.dumps(freeze,indent=2)+'\n')
with (A/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+freeze['utc']+' — First candidate assessment frozen before inherited PR verdicts. Full submitted mathematical claim/source/code read, no mathematical acceptance. Workflow15%, mathematical verification20%.\n')
runtime=A/'geometry/.runtime/bin/python'
program=A/'snapshot/unsolved_math_prioritization/attempts/20000450/verify_turn1.py'
assert runtime.exists() and program.exists()
args=[str(runtime),str(program)]
spec={'argv':args,'cwd':str(A),'started_utc':utc(),'program_sha256':sha(program.read_bytes()),'hypothesis':'Submitted verifier reproduces; acceptance not inferred.'}
(D/'execution_spec.json').write_text(json.dumps(spec,indent=2)+'\n')
with (D/'stdout.bin').open('wb') as out,(D/'stderr.bin').open('wb') as err:
    r=subprocess.run(args,cwd=A,stdout=out,stderr=err)
record={**spec,'ended_utc':utc(),'exit_code':r.returncode}
for k in ['stdout','stderr']:
    b=(D/(k+'.bin')).read_bytes();record[k+'_bytes']=len(b);record[k+'_sha256']=sha(b)
(D/'execution.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2));print((D/'stdout.bin').read_text());print((D/'stderr.bin').read_text())
assert r.returncode==0
