#!/usr/bin/env python3
"""Read-only input binding and unchanged original replay, isolated in tmp."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
import subprocess
import sys

HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent
REPO=HERE.parents[3]
HEAD='90a81313f3f65a7914fb6d5a9950fa087ea7467e'
BASE='c6975ca76f9f667f1250ba403d0e6da2aafe14d0'
PREFIX='unsolved_math_prioritization/attempts/7000019/'
manifest=json.loads((AUDIT/'snapshot_manifest.json').read_text())
source=AUDIT/'source_snapshot'
tmp=HERE/'tmp'/'original_replay'
tmp.mkdir(parents=True,exist_ok=True)
def run(args):
    return subprocess.run(args,cwd=REPO,capture_output=True,check=True).stdout
def digest(b):return hashlib.sha256(b).hexdigest()

files=[]
for item in manifest['files']:
    name=item['path'];b=(source/name).read_bytes()
    # Fully decode/read each body. Human inspected prose/scripts; repetitive
    # receipt arrays are additionally parsed and compared in full.
    content=b.decode()
    if name.endswith('.json'):json.loads(content)
    git=run(['git','show',HEAD+':'+PREFIX+name])
    blob=run(['git','rev-parse',HEAD+':'+PREFIX+name]).decode().strip()
    assert b==git and digest(b)==item['sha256'] and blob==item['git_blob_sha1']
    files.append({'path':name,'bytes':len(b),'sha256':digest(b),'git_blob_sha1':blob,
                  'full_body_read':True,'matches_exact_head':True})
paths=run(['git','diff','--no-ext-diff','--name-only',BASE,HEAD]).decode().splitlines()
assert paths==manifest['changed_paths'] and len(paths)==18 and len(files)==17
diff=run(['git','diff','--no-ext-diff',BASE,HEAD])
(tmp/'all18paths.diff').write_bytes(diff)
queue=run(['git','diff','--no-ext-diff',BASE,HEAD,'--','unsolved_math_prioritization/QUEUE.md']).decode()
queue_lines=[line for line in queue.splitlines() if '| 48 | 7000019' in line]
assert len(queue_lines)==2 and '| unsolved | 2/5 |' in queue_lines[1]

replays=[]
for name in ['verify.py','review/submitted_verify.py','review/independent_checks.py']:
    destination=tmp/name
    destination.parent.mkdir(parents=True,exist_ok=True)
    original=(source/name).read_bytes();destination.write_bytes(original)
    command=[sys.executable,str(destination)]
    result=subprocess.run(command,cwd=tmp,capture_output=True,text=True)
    assert result.returncode==0,(name,result.stderr)
    if name.endswith('independent_checks.py'):
        output=json.loads(destination.with_name('independent_results.json').read_text())
        recorded=json.loads((source/'review/independent_results.json').read_text())
        assert output==recorded and output['passed']==266
    else:
        output=json.loads(result.stdout)
        recorded=json.loads((source/('review/verification.json' if name.startswith('review/') else 'verification.json')).read_text())
        assert output==recorded and output['total_assertions']==1056
    assert digest(destination.read_bytes())==digest(original)
    replays.append({'script':name,'script_sha256':digest(original),'copied_unchanged':True,
                    'exit_code':result.returncode,'stdout':result.stdout,
                    'complete_receipt_equal':True,'receipt':output})

sources=[]
for name,url,inspected in [
 ('ghomi-op.pdf','https://people.math.gatech.edu/~ghomi/Papers/op.pdf','printed p12 pixels and surrounding text'),
 ('reichel.pdf','https://ems.press/content/serial-article-files/34877','printed p622 pixels; §§2,4, Theorem1 and proof pp624–630'),
 ('ghomi2017.html','https://mathoverflow.net/questions/283109/converse-of-the-archimedean-property-of-the-sphere','full question body, definition, and visible comments'),
 ('kim-kim.pdf','https://arxiv.org/pdf/1208.5361','pp1–4 definitions; Proposition2, Theorem3, Lemma8 and proof pp5–7')]:
    b=(HERE/'tmp'/name).read_bytes()
    assert run(['git','check-ignore',str(HERE/'tmp'/name)]).decode().strip()
    sources.append({'url':url,'ignored_local_path':str(HERE/'tmp'/name),
                    'sha256':digest(b),'bytes':len(b),'inspected':inspected})
provenance=json.loads((source/'source_provenance.json').read_text())
for original_name,local_name in [('ghomi-op.pdf','ghomi-op.pdf'),('reichel1996.pdf','reichel.pdf'),('kim-kim-II.pdf','kim-kim.pdf')]:
    expected=next(x for x in provenance['sources'] if x['local_basename']==original_name)
    assert digest((HERE/'tmp'/local_name).read_bytes())==expected['sha256']
import sympy
receipt={'utc':datetime.now(timezone.utc).isoformat(),'head':HEAD,'base':BASE,
         'all17files_exact':True,'all18diff_paths_exact':True,'files':files,
         'changed_paths':paths,'full_diff_sha256':digest(diff),'queue_transition':queue_lines,
         'attempts_used_original':json.loads((source/'attempt.json').read_text())['substantive_attempts_used'],
         'original_replays':replays,'original_files_unchanged':True,
         'runtime':{'executable':sys.executable,'python':sys.version,
                    'sympy':sympy.__version__,'sympy_path':sympy.__file__,'installation_performed':False},
         'primary_sources':sources}
(HERE/'INPUT_AND_REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'all17files_exact':True,'all18diff_paths_exact':True,
                  'replays':'1056 + 1056 + 266 passed; complete receipts equal','foreign_sources_ignored':True}))
