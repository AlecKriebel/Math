"""Ordinary exact-ten-path website commit/push, preserving unrelated index entries."""
from pathlib import Path
import datetime,hashlib,json,subprocess
O=Path(__file__).resolve().parent;W=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com');PUB=W/'public'
def need(x,m):
    if not x:raise RuntimeError(m)
def git(*args):return subprocess.check_output(['git',*args],cwd=W)
def H(b):return hashlib.sha256(b).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
installation=json.loads((O/'installation.json').read_text())
rows=[r for r in installation['copies'] if Path(r['destination']).is_relative_to(PUB)]
paths=sorted(str(Path(r['destination']).relative_to(W)) for r in rows)
need(len(paths)==len(set(paths))==10,'exact ten public paths')
parent='0171f8e3234e44aa7e57b1f5a5050c80465aeb74'
need(not (O/'website-commit.json').exists(),'commit already recorded; resume push separately')
need(git('rev-parse','HEAD').decode().strip()==parent and git('branch','--show-current').decode().strip()=='master','base/master')
remote_before=git('ls-remote','--heads','origin','master').decode().split()
need(remote_before and remote_before[0]==parent,'remote base changed')
def other_entries():
    return b'\0'.join(r for r in git('ls-files','--stage','-z').split(b'\0') if r and r.split(b'\t',1)[1].decode() not in paths)
index_before=other_entries()
pre={'utc':now(),'parent':parent,'paths':paths,'unrelated_index_entries_sha256':H(index_before)}
(O/'website-git-preflight.json').write_text(json.dumps(pre,indent=2)+'\n')
git('add','--',*paths)
commit_output=git('commit','--only','-m','Publish research notes on odd-ear prefixes and shortest-path blocking','--',*paths).decode()
commit=git('rev-parse','HEAD').decode().strip()
need(git('rev-parse','HEAD^').decode().strip()==parent,'commit parent')
changed=git('diff-tree','--no-commit-id','--name-only','-r','--no-renames',commit).decode().splitlines()
need(sorted(changed)==paths,'exact commit path list')
for row in rows:
    rel=str(Path(row['destination']).relative_to(W));need(H(git('show',commit+':'+rel))==row['sha256'],'committed bytes '+rel)
need(other_entries()==index_before,'unrelated index entries unchanged')
commit_receipt={'utc':now(),'commit':commit,'parent':parent,'paths':paths,'commit_output':commit_output,'all_committed_bytes_exact':True,'unrelated_index_entries_sha256_before_after':H(index_before)}
(O/'website-commit.json').write_text(json.dumps(commit_receipt,indent=2)+'\n')
push=subprocess.run(['git','push','origin','master'],cwd=W,capture_output=True,text=True)
(O/'website-push-execution.json').write_text(json.dumps({'utc':now(),'returncode':push.returncode,'stdout':push.stdout,'stderr':push.stderr},indent=2)+'\n')
need(push.returncode==0,'ordinary push failed; committed state preserved')
need(git('ls-remote','--heads','origin','master').decode().split()[0]==commit,'actual remote head')
need(other_entries()==index_before,'unrelated index after push')
receipt={**commit_receipt,'utc':now(),'status':'PASS_EXACT10_PATHS_ORDINARY_WEBSITE_MASTER_PUSH','ordinary_nonforce_push_remote_exact':True,'unrelated_index_entries_unchanged':True,'old_unmodified_public_files':514,'unrelated_public_homepage_sha256':H((PUB/'index.html').read_bytes()),'all203_complete':False}
(O/'website-git.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({'status':receipt['status'],'commit':commit,'paths':len(paths)}))
