#!/usr/bin/env python3
"""Replay copied candidate scripts only inside ignored scratch and compare outputs."""
from pathlib import Path
import hashlib,json,shutil,subprocess,sys,datetime
root=Path(__file__).resolve().parent
candidate=root.parent/'reviewed_candidate'
scratch=root/'tmp'/'candidate_replay'; scratch.mkdir(parents=True,exist_ok=True)
receipts=[]
for source_name,out_name in [('verify.py','verification.json'),('independent_symbolic_check.py','independent_symbolic_check.json')]:
    source=candidate/source_name; before=hashlib.sha256(source.read_bytes()).hexdigest()
    shutil.copy2(source,scratch/source_name)
    p=subprocess.run([sys.executable,str(scratch/source_name)],capture_output=True,text=True,timeout=120)
    (scratch/(source_name+'.stdout')).write_text(p.stdout); (scratch/(source_name+'.stderr')).write_text(p.stderr)
    assert p.returncode==0,(source_name,p.stderr)
    fresh=json.loads((scratch/out_name).read_text()); frozen=json.loads((candidate/out_name).read_text())
    assert fresh==frozen,(source_name,'receipt differs')
    assert (scratch/out_name).read_bytes()==(candidate/out_name).read_bytes(),(source_name,'receipt bytes differ')
    assert hashlib.sha256(source.read_bytes()).hexdigest()==before
    receipts.append({'script':source_name,'script_sha256':before,'returncode':p.returncode,'receipt':out_name,
                     'exact_receipt_matches':True,'receipt_byte_identical':True,'immutable_input_unchanged':True,
                     'case_count':fresh.get('case_count'),'checks':fresh.get('equality_and_rank_checks',fresh.get('symbolic_check_count'))})
result={'status':'passed','created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'replays':receipts,
        'execution_root':'ignored tmp/candidate_replay','interpreter':sys.executable}
(root/'replay_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
