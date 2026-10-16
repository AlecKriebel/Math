"""Additional fresh bad-certificate and defective-source algorithm controls."""
from pathlib import Path
from copy import deepcopy
import datetime, hashlib, json, subprocess, sys
R=Path(__file__).resolve().parent
P=R/'extracted/grassmann_calibrations_v1'
H=R/'hostile'; H.mkdir(exist_ok=True)
source=(P/'checks/audit_exact_embedding.py').read_text()
original=json.loads((P/'checks/EMBEDDING_CERTIFICATE.json').read_text())

def require(ok,message):
    if not ok: raise RuntimeError(message)

cases=[]
for label,modify,error in [
    ('boolean_exterior_index',lambda c:c['columns'][0]['entries'][0][0].__setitem__(0,False),'ENTRY_INDEX'),
    ('boolean_coefficient',lambda c:c['columns'][0]['entries'][0].__setitem__(1,True),'ENTRY_VALUE_TYPE'),
    ('noncanonical_fraction',lambda c:c['columns'][0]['entries'][0].__setitem__(1,'2/2'),'ENTRY_VALUE_CANONICAL'),
    ('new_zero_entry',lambda c:c['columns'][0]['entries'][0].__setitem__(1,'0'),'ENTRY_VALUE_CANONICAL'),
    ('wrong_exact_denominator',lambda c:c['columns'][0]['entries'][0].__setitem__(1,'1/3'),'ENTRY_DENOMINATOR'),
]:
    obj=deepcopy(original);modify(obj);path=H/(label+'.json');path.write_text(json.dumps(obj,sort_keys=True)+'\n')
    cases.append((label,P/'checks/audit_exact_embedding.py',path,error))
for label,before,after,error in [
    ('projector_expected_sign','{key: 4*value for key, value in plane[quad].items()}','{key: -4*value for key, value in plane[quad].items()}','GENERAL_PROJECTOR_IDENTITY: (0, 1, 2, 3)'),
    ('trace_expected_scale','phi(col) == (4 if kind == "diag" else 0)','phi(col) == (8 if kind == "diag" else 0)','PHI_TRACE'),
    ('pure_trace_expected_scale','phi(col, pure=True) == (4 if kind == "diag" and','phi(col, pure=True) == (8 if kind == "diag" and','Q_PURE_TRACE'),
    ('mixed_expected_sign','tuple(sorted((3*a+c-3, 3*b+d-3))), -2)','tuple(sorted((3*a+c-3, 3*b+d-3))), 2)','MIXED_PLUCKER_MINORS'),
]:
    require(source.count(before)==1,'source mutation location'+label)
    path=H/(label+'.py');path.write_text(source.replace(before,after))
    cases.append((label,path,P/'checks/EMBEDDING_CERTIFICATE.json',error))
rows=[]
for mode in [0,1,2]:
    for label,checker,certificate,error in cases:
        command=[sys.executable,'-I','-S','-B']
        if mode:command+=['-'+'O'*mode]
        command += [str(checker),'--certificate',str(certificate)]
        q=subprocess.run(command,capture_output=True,timeout=120)
        data=json.loads(q.stdout)
        require(q.returncode==1 and q.stderr==b'' and data=={'status':'FAIL','error':error},'exact expected failure'+label)
        rows.append({'mode':mode,'case':label,'exit_code':q.returncode,'stdout':q.stdout.decode(),'stderr':q.stderr.decode(),
                     'checker_sha256':hashlib.sha256(checker.read_bytes()).hexdigest(),
                     'certificate_sha256':hashlib.sha256(certificate.read_bytes()).hexdigest(),'intended_error':error})
receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','actual_runs':len(rows),
         'certificate_families':5,'algorithm_mutations':4,'runs':rows,
         'scope':'Fresh controls extend checks to coefficient/index types, canonical fractions, projector identity, two trace identities and mixed minor signs. They do not enlarge the package portable48run claim.'}
(R/'receipts/HOSTILE_CONTROLS.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k!='runs'},indent=2))
