#!/usr/bin/env python3
"""Replay the two sealed historical control programs in this audit's own folder."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess,sys
O=Path(__file__).resolve().parent;P=O.parent/'authenticated_sources_01/existing_publication_audit/preprint'
results=[]
for family,program,receipt in [('fresh_review_01','independent_exact_checks.py','INDEPENDENT_EXACT_RESULT.json'),('fresh_review_02','independent_controls.py','INDEPENDENT_CONTROL_RECEIPT.json')]:
 d=O/'historical_control_replay'/family;d.mkdir(parents=True,exist_ok=True)
 src=P/family/program;dst=d/program;dst.write_bytes(src.read_bytes())
 run=subprocess.run([sys.executable,'-I',str(dst)],capture_output=True,text=True,timeout=60)
 (d/'stdout.json').write_text(run.stdout);(d/'stderr.txt').write_text(run.stderr)
 actual=json.loads(run.stdout);expected=json.loads((P/family/receipt).read_text())
 actual.pop('utc',None);expected.pop('utc',None)
 results.append({'family':family,'returncode':run.returncode,'program_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'matches_historical_exact_JSON_excluding_UTC':actual==expected,'assertions':actual.get('assertions',actual.get('new_exact_assertions'))})
result={'UTC':datetime.now(timezone.utc).isoformat(),'scope':'Finite historical-program reproduction; no evidence of historical mental independence or asymptotic truth','all_pass':all(r['returncode']==0 and r['matches_historical_exact_JSON_excluding_UTC'] for r in results),'results':results}
(O/'HISTORICAL_CONTROL_REPLAY.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
