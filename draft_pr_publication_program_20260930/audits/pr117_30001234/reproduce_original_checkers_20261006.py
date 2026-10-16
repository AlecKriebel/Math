"""Reproduce immutable checkers in root-owned copies; keep originals unchanged."""
from pathlib import Path
import datetime,hashlib,json,os,shutil,subprocess
A=Path(__file__).resolve().parent
O=A/'original_head_authentication_20261006/original_attempt'
D=A/'root_original_reproduction_20261006'
PY='/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/bin/python3.14'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def require(value,label):
    if not value:raise RuntimeError(label)
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
require(not D.exists(),'Existing original replay: inspect before retry')
D.mkdir()
author=D/'author';independent=D/'independent'
author.mkdir();independent.mkdir()
for name in ['CANDIDATE.md','verify.py']:shutil.copyfile(O/name,author/name)
shutil.copyfile(O/'review/independent_checks.py',independent/'independent_checks.py')
(independent/'author_replay').mkdir()
shutil.copyfile(O/'CANDIDATE.md',independent/'author_replay/CANDIDATE.md')
events=[]
for name,folder,code,resultfile,expected in [
    ('author',author,'verify.py','verification.json',O/'verification.json'),
    ('independent',independent,'independent_checks.py','independent_results.json',O/'review/independent_results.json')]:
    argv=[PY,'-E','-S','-B','-P',str(folder/code)]
    started=now();child=subprocess.Popen(argv,cwd=folder,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
        env={'PATH':'/usr/bin:/bin','LANG':'C','LC_ALL':'C','TZ':'UTC','__CF_USER_TEXT_ENCODING':'0x1F5:0x0:0x0'})
    out,err=child.communicate()
    (folder/'stdout.log').write_bytes(out)
    require(child.returncode==0 and not err,'Original normal checker failed')
    require((folder/resultfile).read_bytes()==expected.read_bytes(),'Original result differs')
    events.append({'name':name,'argv':argv,'PID':child.pid,'start_UTC':started,'end_UTC':now(),'exit_code':child.returncode,
        'stdout_bytes':len(out),'stdout_sha256':hashlib.sha256(out).hexdigest(),'stderr_bytes':len(err),
        'full_result_reproduced_byte_for_byte':True,'result_sha256':sha(folder/resultfile),
        'original_checker_sha256':sha(folder/code),'assertions':json.loads((folder/resultfile).read_text())['assertions']})
    (D/'PROCESS_JOURNAL.json').write_text(json.dumps({'actual_operator_PID':os.getpid(),'events':events},indent=2)+'\n')
auth=json.loads((A/'original_head_authentication_20261006/ORIGINAL_AUTHENTICATION.json').read_text())
for item in auth['original_files']:require(sha(O/item['path'])==item['sha256'],'Original altered')
record={'schema':'pr117-root-original-normal-reproduction/v1','UTC':now(),'actual_operator_PID':os.getpid(),
    'events':events,'all20_originals_unchanged':True,'normal_run_only':True,
    'optimized_mode_clearance':False,'guard_limitation':'Both original checkers use assertions, which Python -O strips. Normal reproduction is valid; an effective verification package requires exception-based guards and negative controls.',
    'new_central_proof_search_turns':0,'mathematical_clearance':False,'priority_clearance':False}
(A/'ROOT_ORIGINAL_CHECKER_REPRODUCTION_20261006.json').write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
print(json.dumps(record,sort_keys=True))
