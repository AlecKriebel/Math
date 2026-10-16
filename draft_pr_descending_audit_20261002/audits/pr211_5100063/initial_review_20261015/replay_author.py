from pathlib import Path
import shutil,subprocess,json,hashlib,datetime
D=Path(__file__).resolve().parent;S=D/'submitted/unsolved_math_prioritization/attempts/5100063';R=D/'root_reproduction/author';R.mkdir(parents=True)
for name in ['verify.py','PROOF.md']:shutil.copyfile(S/name,R/name)
py='/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr256_5100017/initial_review_20261013/reproduction_environment/bin/python'
p=subprocess.run([py,str(R/'verify.py')],capture_output=True,text=True,timeout=600);(R/'stdout.txt').write_text(p.stdout);(R/'stderr.txt').write_text(p.stderr);assert p.returncode==0,p.stderr
actual=json.loads((R/'verification.json').read_text());expected=json.loads((S/'verification.json').read_text());assert actual==expected,(actual,expected)
r=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='PASS',semantic_exact_replay=True,byte_identical=(R/'verification.json').read_bytes()==(S/'verification.json').read_bytes(),exact_assertions=actual['exact_assertions'],uncertified_numerical_diagnostics=actual['numerical_diagnostics'],proof_sha256=hashlib.sha256((S/'PROOF.md').read_bytes()).hexdigest(),receipt_sha256=hashlib.sha256((R/'verification.json').read_bytes()).hexdigest(),no_original_file_modified=True)
(D/'ROOT_AUTHOR_REPLAY_ACCEPTANCE.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
