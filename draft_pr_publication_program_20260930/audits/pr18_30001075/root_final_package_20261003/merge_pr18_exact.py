"""Merge the exact PR18 head on main, preserving all foreign work and queue rows."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

if sys.flags.optimize or sys.argv[1:] != ['--exclusive-window-confirmed']:
    raise RuntimeError('Requires the confirmed exclusive shared writer window')
own = Path(__file__).resolve().parent
a18 = own.parent
program = a18.parents[1]
repo = program.parent
run_dir = own/'integration_step1'
run_dir.mkdir()
seq = 0
def run(argv, allowed=(0,)):
    global seq
    seq += 1
    start = dt.datetime.now(dt.timezone.utc).isoformat()
    child = subprocess.Popen(argv,cwd=repo,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.DEVNULL)
    out,err = child.communicate()
    prefix = run_dir/f'{seq:03d}'
    prefix.with_suffix('.stdout').write_bytes(out)
    prefix.with_suffix('.stderr').write_bytes(err)
    prefix.with_suffix('.json').write_text(json.dumps({'argv':argv,'started_utc':start,
        'finished_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_pid':child.pid,
        'exit_code':child.returncode,'stdout_sha256':sha(out),'stderr_sha256':sha(err)},indent=2)+'\n')
    if child.returncode not in allowed:
        raise RuntimeError(f'Command {seq} failed; preserved complete output: '+err.decode(errors='replace'))
    return out,child.returncode
def sha(body):
    return hashlib.sha256(body).hexdigest()
def git(*args):
    return run(['git',*args])[0]
def must(condition, message):
    if not condition:
        raise RuntimeError(message)
head = '99e403e85d38d92b021198c4a57bbad3cd8775ba'
queue = 'unsolved_math_prioritization/QUEUE.md'
canonical = 'unsolved_math_prioritization/attempts/30001075'
current = canonical+'/CURRENT_RESULT.md'
plan = json.loads((a18/'native_acceptance_plan_20261003/PLAN.json').read_bytes())
originals = plan['original_scientific_files_to_preserve_exactly']
paths = {item['canonical_path'] for item in originals}|{queue,current}
must(git('branch','--show-current').strip()==b'main','Requires main')
must(not git('diff','--cached','--name-only').strip(),'Preserve foreign staging; real index must be clean')
must(not (repo/'.git/MERGE_HEAD').exists(),'Existing merge must be handled by its owner')
base = git('rev-parse','HEAD').decode().strip()
must(git('ls-remote','--heads','origin','main').decode().split()[0]==base,'Main remote changed')
pr = json.loads(run(['gh','pr','view','18','--repo','AlecKriebel/Math','--json','number,state,isDraft,headRefOid,baseRefName,title,body,url'])[0])
(run_dir/'PR_BEFORE.json').write_text(json.dumps(pr,indent=2)+'\n')
must(pr['state']=='OPEN' and pr['headRefOid']==head and pr['baseRefName']=='main','PR head or state changed')
pr_queue = git('show',head+':'+queue).decode()
pr_rows = [line for line in pr_queue.splitlines() if '| 30001075 /' in line]
must(len(pr_rows)==1 and pr_rows[0].split('|')[8].strip()=='claimed_solved' and pr_rows[0].split('|')[9].strip()=='1/5','Not an eligible claimed_solved head')
common = git('merge-base',base,head).decode().strip()
incoming = set(git('diff','--name-only','-z',common,head).decode().split('\0'))-{''}
must(incoming==paths-{current},'Unexpected incoming PR scope')
for item in originals:
    must(not (repo/item['canonical_path']).exists(),'Canonical original already exists')
    must(sha(git('show',head+':'+item['canonical_path']))==item['sha256'],'Original head blob differs')
must(not (repo/current).exists(),'Current result already exists')
before_queue = (repo/queue).read_bytes()
must(before_queue==git('show',base+':'+queue),'Queue has foreign worktree edits')
lines = before_queue.decode().splitlines(keepends=True)
targets = [i for i,line in enumerate(lines) if '| 30001075 /' in line]
must(len(targets)==1,'Exactly one native queue row required')
i = targets[0]
cells = lines[i].split('|')
must(len(cells)==14 and cells[8].strip()=='queued' and cells[9].strip()=='0/5','Unexpected native status or row shape')
cells[8] = ' preprint_published '
cells[9] = ' 1/5 '
cells[11] = ' Conjecture 4 spatial outer-nullness accepted for arbitrary convex sets; two fresh package reviews; AI-assisted, unrefereed; tracker pending '
cells[12] = ' 10.5281/zenodo.23127955 '
lines[i] = '|'.join(cells)
accepted_queue = ''.join(lines).encode()
publication = json.loads((a18/'publication/PUBLICATION_VERIFICATION.json').read_bytes())
must(publication['published'] is True and publication['all_public_bytes_identical'] is True and publication['DOI']=='10.5281/zenodo.23127955','Publication is unverified')
decision = json.loads((own/'ROOT_FINAL_SUBMISSION_DECISION.json').read_bytes())
for name,pin in decision['publication_pins'].items():
    must(sha((a18/'preprint_v1'/name).read_bytes())==pin,'Published package drift')
for folder,key in [('preprint_round1_adversary_family','first_fresh_review_verdict_sha256'),('preprint_round2_adversary_family','second_NEW_fresh_review_verdict_sha256')]:
    must(sha((a18/folder/'VERDICT.json').read_bytes())==decision[key],'Fresh review drift')
def foreign_index():
    return b'\0'.join(e for e in git('ls-files','--stage','-z').split(b'\0') if e and e.split(b'\t',1)[1].decode() not in paths)
foreign = foreign_index()
merge_out,merge_exit = run(['git','merge','--no-ff','--no-commit',head],allowed=(0,1))
unmerged = set(git('diff','--name-only','--diff-filter=U','-z').decode().split('\0'))-{''}
must(unmerged <= {queue},'Unexpected conflicts; stop without resetting foreign work')
must((repo/'.git/MERGE_HEAD').read_text().strip()==head,'Merge parent mismatch')
must(foreign_index()==foreign,'Foreign index drift during merge')
(repo/queue).write_bytes(accepted_queue)
for item in originals:
    must(sha((repo/item['canonical_path']).read_bytes())==item['sha256'],'Original imported blob changed')
root_url = 'https://github.com/AlecKriebel/Math/blob/main/'+a18.relative_to(repo).as_posix()
body = f'''# Accepted current result — PR18 / OWR-2090-028

The accepted proof is the published research note **The spatial locus of common tangents to three disjoint convex sets is null**, by Alec Kriebel: [DOI 10.5281/zenodo.23127955](https://doi.org/10.5281/zenodo.23127955).

It resolves literal Conjecture 4 in OWR44/2008: the spatial union of complete common tangent lines to any three pairwise disjoint convex subsets of R³ has Lebesgue outer measure zero. Tangency requires actual contact and containment in a supporting plane. Nonclosed, unbounded and lower-dimensional sets are covered. This result does not establish the stronger Conjecture 3.

The operative [manuscript]({root_url}/preprint_v1/paper.tex) has SHA256 `2522ac0138de5e21067af8c16e6749b3a9d3cd01f12bdb929cca87cb6baeabb6`. The [published PDF and verification package](https://zenodo.org/records/23127955) match the exact files checked by [two fresh whole-package reviews]({root_url}/preprint_round2_adversary_family/REPORT.md). The [bounded priority assessment]({root_url}/ROOT_CURRENT_PRIORITY_ASSESSMENT_20261003.md) includes the complete 2024 geometric-transversals article supplied by the human user and does not claim exhaustive global priority.

The 15 original research files in this directory are preserved byte-for-byte from head `{head}` as dated inputs. Their candidate, readiness and review hashes describe that historical draft, not the corrected final manuscript. This current-result record and acceptance.json govern present acceptance. Original central attempts remain 1/5; review and publication added no new central discovery attempts.

AI tools were used extensively in solving, drafting and verification. The preprint is unrefereed and has not undergone conventional external human peer review or formal proof certification. Exact finite controls support reproducibility and do not replace the analytic proof.

Publication and public file readbacks are complete. The Google tracker row remains pending credential reconnection. A present-day acceptance mirror will bind the actual merge commit after it is known; no historical lifecycle transitions are reconstructed.
'''
(repo/current).write_text(body)
git('add','--',queue,current)
must(not git('diff','--name-only','--diff-filter=U').strip(),'Unresolved merge remains')
staged = set(git('diff','--cached','--name-only','-z').decode().split('\0'))-{''}
must(staged==paths,'Staged merge scope differs from the 15 originals, queue and current-result record')
must(foreign_index()==foreign,'Foreign index changed before commit')
git('commit','-m','Accept PR18 published resolution of spatial common-tangent nullness')
commit = git('rev-parse','HEAD').decode().strip()
must(git('show','-s','--format=%P',commit).decode().strip().split()==[base,head],'Exact two-parent merge failed')
must((repo/queue).read_bytes()==accepted_queue,'Queue drift')
for item in originals:
    must(sha(git('show',commit+':'+item['canonical_path']))==item['sha256'],'Committed original differs')
must(foreign_index()==foreign,'Foreign index changed')
git('push','origin','main')
remote = git('ls-remote','--heads','origin','main').decode().split()[0]
must(remote==commit,'Remote main readback mismatch')
record = {'schema':'pr18-exact-native-merge/v1','UTC':dt.datetime.now(dt.timezone.utc).isoformat(),
    'actual_pid':os.getpid(),'base':base,'submitted_head':head,'merge_commit':commit,'remote_main':remote,
    'merge_exit_code':merge_exit,'conflicts':sorted(unmerged),'foreign_index_unchanged':True,
    'all_15_original_blobs_unchanged':True,'QUEUE_only_target_four_cells_changed':True,
    'DOI':publication['DOI'],'tracker_row_written':False,'workflow_percent':97,
    'native_state_followup_pending':True,'new_central_attempts':0}
(own/'NATIVE_MERGE_RESULT.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
