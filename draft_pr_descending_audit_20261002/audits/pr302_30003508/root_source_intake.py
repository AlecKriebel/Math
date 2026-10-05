"""Whole original PR302 source intake through immutable Git blob reads only."""
from pathlib import Path
from datetime import datetime,timezone
from concurrent.futures import ThreadPoolExecutor
import subprocess,json,hashlib,base64,stat,sys
if sys.flags.optimize:raise RuntimeError('Unoptimized original source intake required.')
A=Path(__file__).resolve().parent;R=A.parent.parent.parent
HEAD='eb6e0e999521d84a65f9857d338cad76b84d30db';PREFIX='unsolved_math_prioritization/attempts/30003508/'
S=A/'snapshot';O=A/'source_intake_private';assert not S.exists() and not O.exists();S.mkdir();O.mkdir()
sha=lambda b:hashlib.sha256(b).hexdigest();utc=lambda:datetime.now(timezone.utc).isoformat()
def api(label,endpoint):
    argv=['/opt/homebrew/bin/gh','api',endpoint];stamp=utc()
    proc=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    j=dict(argv=argv,cwd=str(R),actual_PID=proc.pid,start_UTC=stamp,source_sha256=sha(Path(__file__).read_bytes()))
    (O/(label+'_started.json')).write_text(json.dumps(j,indent=2)+'\n')
    b,err=proc.communicate(timeout=55)
    for k,x in [('stdout',b),('stderr',err)]:
        (O/(label+'_'+k+'.bin')).write_bytes(x);j[k+'_bytes']=len(x);j[k+'_sha256']=sha(x)
    j.update(end_UTC=utc(),exit_code=proc.returncode);(O/(label+'_execution.json')).write_text(json.dumps(j,indent=2)+'\n')
    assert proc.returncode==0,(label,proc.returncode);return json.loads(b)
pr=api('before','repos/AlecKriebel/Math/pulls/302');assert pr['head']['sha']==HEAD and pr['state']=='open' and pr['draft']
files=api('files','repos/AlecKriebel/Math/pulls/302/files?per_page=100');assert 0<len(files)<100
assert all(e['status'] in ['added','modified'] and (e['filename'].startswith(PREFIX) or e['filename']=='unsolved_math_prioritization/QUEUE.md') for e in files)
def fetch(pair):
    n,e=pair;rel=e['filename'];assert not Path(rel).is_absolute() and '..' not in Path(rel).parts
    j=api('blob_'+str(n),'repos/AlecKriebel/Math/git/blobs/'+e['sha']);assert j['sha']==e['sha'] and j['encoding']=='base64'
    b=base64.b64decode(j['content']);assert len(b)==j['size']
    assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==e['sha']
    p=S/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b);p.chmod(0o444)
    return dict(path=rel,bytes=len(b),sha256=sha(b),git_blob_sha=e['sha'],submitted_Git_mode='100644',frozen_filesystem_mode='0444',status=e['status'])
with ThreadPoolExecutor(max_workers=4) as pool:rows=list(pool.map(fetch,enumerate(files,1)))
fresh=api('after','repos/AlecKriebel/Math/pulls/302');assert fresh['head']['sha']==HEAD and fresh['state']=='open' and fresh['draft']
q=(S/'unsolved_math_prioritization/QUEUE.md').read_bytes();target=[x for x in q.splitlines(keepends=True) if len(x.split(b'|'))==14 and x.split(b'|')[2].strip().startswith(b'30003508 /')];assert len(target)==1
cells=target[0].split(b'|');assert cells[8].strip()==b'claimed_solved' and cells[9].strip()==b'2/5'
old=R/'draft_pr_descending_audit_20261002/intake_after_pr305_20261005/eligible_original_QUEUE.md';assert old.read_bytes()==q
for p in sorted((p for p in S.rglob('*') if p.is_dir()),key=lambda p:len(p.parts),reverse=True):p.chmod(0o555)
S.chmod(0o555)
manifest=dict(status='PASS_ORIGINAL_PR302_WHOLE_BLOB_SOURCE_INTAKE',UTC=utc(),pr=302,head=HEAD,
    original_submitted_status='claimed_solved',original_author_turn_count='2/5',original_target_row=target[0].decode(),
    files=rows,source_file_count=len(rows),whole_source_bytes=sum(e['bytes'] for e in rows),
    actual_native_READONLY_API_captures=len(rows)+3,source= dict(bytes=Path(__file__).stat().st_size,sha256=sha(Path(__file__).read_bytes())),
    snapshot_readonly=True,no_Git_or_shared_index_or_config_or_service_mutation=True,
    no_mathematical_or_priority_acceptance_yet=True,math_percent=0,priority_percent=0,workflow_percent=5,
    live_original_head_stable_before_and_after=True,PR305_completed_before_this_intake=True,peer55_path_window_respected=True)
(A/'snapshot_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
(A/'RESEARCH_LOG.md').write_text(utc()+' — Original PR302 claimed_solved2/5 head '+HEAD+' authenticated from'+str(len(rows))+' complete immutable Git blobs with before/after head equality and full native API process custody. Snapshot frozen; no proof/priority acceptance yet. Mathematics0%,priority0%,workflow5%. Start materially distinct independent adversaries before convergence. No shared/index/config write during peer55path scope.\n')
print(json.dumps({k:v for k,v in manifest.items() if k not in ['files','original_target_row']},indent=2))
