"""Actually replay the unchanged first whole controls privately, preserving the defect."""
from pathlib import Path
import hashlib,json,shutil,subprocess,sys
H=Path(__file__).resolve().parent;P=Path('/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr34_7000004')
D=H/'tmp/historical_whole';F=P/'current_whole_adversary';T=D/'reviewer';T.mkdir(parents=True,exist_ok=True)
shutil.copyfile(F/'independent_controls.py',T/'independent_controls.py')
shutil.copytree(P/'reviewed_candidate',D/'reviewed_candidate',dirs_exist_ok=True)
shutil.copyfile(P/'ROOT_NI2026_RETRIEVAL.json',D/'ROOT_NI2026_RETRIEVAL.json')
r=subprocess.run([sys.executable,str(T/'independent_controls.py')],capture_output=True)
(H/'historical_controls.stdout.txt').write_bytes(r.stdout);(H/'historical_controls.stderr.txt').write_bytes(r.stderr)
assert r.returncode==0 and not r.stderr
actual=json.loads((T/'INDEPENDENT_CONTROLS.json').read_bytes());expected=json.loads((F/'INDEPENDENT_CONTROLS.json').read_bytes())
for k in expected:
 if k=='actual_mutations':assert [{q:v for q,v in z.items() if q!='stderr_sha256'} for z in expected[k]]==[{q:v for q,v in z.items() if q!='stderr_sha256'} for z in actual[k]]
 else:assert expected[k]==actual[k],k
assert actual['mandatory_administrative_failure']['mandatory'] is True
shutil.copyfile(T/'INDEPENDENT_CONTROLS.json',H/'HISTORICAL_ACTUAL_CONTROLS.json')
shutil.copytree(T/'actual_mutations',H/'historical_actual_mutations',dirs_exist_ok=True)
rec={'returncode':r.returncode,'implementation_sha256':hashlib.sha256((T/'independent_controls.py').read_bytes()).hexdigest(),'implementation_exact':(T/'independent_controls.py').read_bytes()==(F/'independent_controls.py').read_bytes(),'historical44checks12mutants5actualvariants_equal_except_private_traceback_hashes':True,'historical_metadata_failure_reproduced_as_failure':True}
(H/'FIRST_WHOLE_CONTROLS_REPLAY.json').write_text(json.dumps(rec,indent=2)+'\n');print(json.dumps(rec))
