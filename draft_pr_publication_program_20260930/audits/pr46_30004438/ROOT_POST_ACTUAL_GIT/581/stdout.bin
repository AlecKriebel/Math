"""Export PR46 evidence literally; never execute submitted helpers or write native inputs."""
from pathlib import Path, PurePosixPath
import datetime as dt
import hashlib
import json
import os
import stat
import subprocess

A = Path(__file__).resolve().parent
R = A.parents[2]
ID = '30004438'
HEAD = 'a39d178b10f75fb127058b08e0d0002b3ae97f8a'
BASE = 'c6975ca76f9f667f1250ba403d0e6da2aafe14d0'
PREFIX = 'unsolved_math_prioritization/attempts/' + ID + '/'

def sha(b): return hashlib.sha256(b).hexdigest()
def now(): return dt.datetime.now(dt.timezone.utc).isoformat()
def write(p, b):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('xb') as f:
        f.write(b); f.flush(); os.fsync(f.fileno())
def js(p, x): write(p, (json.dumps(x, indent=2, sort_keys=True) + '\n').encode())
def cmd(label, argv):
    d = A / 'original_git_commands' / label
    d.mkdir(parents=True)
    src = Path(__file__).read_bytes()
    write(d / 'prelaunch_operator.py', src)
    rec = dict(schema='pr46-original-git-command/v1', argv=argv, cwd=str(R),
               operator_sha256=sha(src), started_utc=now(), actual_execution=False,
               completed=False, pid=None, exit_code=None, stdin_supplied=False)
    js(d / 'PRELAUNCH.json', rec)
    p = subprocess.Popen(argv, cwd=R, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    rec.update(actual_execution=True, completed=True, pid=p.pid, exit_code=p.returncode, finished_utc=now())
    for name, b in [('stdout', out), ('stderr', err)]:
        write(d / (name + '.bin'), b)
        rec[name] = dict(path=name + '.bin', bytes=len(b), sha256=sha(b))
    rec['operator_unchanged'] = Path(__file__).read_bytes() == src
    js(d / 'CAPTURE.json', rec)
    assert p.returncode == 0, (label, p.returncode)
    return out
def gitbody(label, path):
    tree = cmd(label + '_tree', ['git', 'ls-tree', '-z', HEAD, '--', path])
    assert tree.endswith(b'\0') and tree.count(b'\0') == 1
    meta, literal = tree[:-1].split(b'\t')
    mode, kind, oid = meta.decode().split(' ')
    assert kind == 'blob' and literal.decode() == path
    b = cmd(label + '_body', ['git', 'cat-file', 'blob', oid])
    return b, dict(path=path, git_mode=mode, git_object=oid, bytes=len(b), sha256=sha(b))
def filebinding(p):
    st = p.stat(); h = hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda: f.read(1024*1024), b''): h.update(b)
    st2 = p.stat()
    assert (st.st_size, st.st_mtime_ns) == (st2.st_size, st2.st_mtime_ns)
    return dict(path=p.relative_to(R).as_posix(), bytes=st.st_size, sha256=h.hexdigest(),
                full_mode=stat.S_IMODE(st.st_mode), mtime_ns=st.st_mtime_ns,
                individually_bound=True, copied_into_owned_topology=False)
def selected(obj):
    if isinstance(obj, dict):
        if ID in obj: return obj[ID]
        return {k: selected(v) for k,v in obj.items() if ID in json.dumps(v)}
    if isinstance(obj, list):
        return [x for x in obj if (isinstance(x, dict) and str(x.get('id')) == ID) or ID in json.dumps(x)]
    return obj
def main():
    src = Path(__file__).read_bytes(); write(A / 'EXPORT_PRELAUNCH_SOURCE.py', src)
    m = json.loads((A / 'github_metadata_v2_actual_capture/stdout.bin').read_bytes())
    api = sum(json.loads((A / 'github_changed_files_actual_capture/stdout.bin').read_bytes()), [])
    assert m['number'] == 46 and m['state'] == 'open' and m['draft'] is True
    assert m['head']['sha'] == HEAD and m['base']['sha'] == BASE
    assert cmd('current_branch', ['git','branch','--show-current']) == b'main\n'
    mb = cmd('merge_base', ['git','merge-base',BASE,HEAD]).decode().strip()
    names = cmd('changed_paths', ['git','diff','--name-status','-z',mb,HEAD]).split(b'\0')
    assert names.pop() == b'' and len(names) % 2 == 0
    changes = [dict(status=names[i].decode(),path=names[i+1].decode()) for i in range(0,len(names),2)]
    assert len(changes) == m['changed_files'] == len(api) == 14
    assert {x['path'] for x in changes} == {x['filename'] for x in api}
    diff = cmd('whole_diff',['git','diff','--no-ext-diff','--no-textconv','--binary',mb,HEAD,'--'])
    write(A / 'original_diff.patch',diff)
    files=[]; foreign=[]
    for i,r in enumerate(changes):
        assert r['status'] in ('A','M')
        path=r['path']
        assert path == 'unsolved_math_prioritization/QUEUE.md' or path.startswith(PREFIX)
        b,row=gitbody('changed_%02d'%i,path)
        assert len(b)<100*1024*1024
        assert Path(path).suffix.lower() not in ('.pdf','.sqlite','.db','.png','.jpg','.jpeg','.webp')
        if path.startswith(PREFIX):
            rel=path[len(PREFIX):]; pp=PurePosixPath(rel)
            assert not pp.is_absolute() and '..' not in pp.parts
            p=A/'source_snapshot'/rel;write(p,b);os.chmod(p,0o444)
            row.update(relative_path=rel,snapshot_mode='0444');files.append(row)
        else:
            write(A/'original_queue_in_head.md',b);queue=b;queuebinding=row
    matches=[x for x in queue.decode().splitlines() if ('| '+ID+' / ') in x]
    assert len(matches)==1
    cells=[x.strip() for x in matches[0].strip('|').split('|')]
    original_status=cells[7];original_turns=cells[8]
    native=[]
    nativepaths=['catalog.json','assessments.json','state.json','history.jsonl','assessment_history.jsonl',
                 'manifest.json','review_v2/related_target_groups.json']
    for i,name in enumerate(nativepaths):
        path='unsolved_math_prioritization/'+name
        b,row=gitbody('head_native_%02d'%i,path)
        if name.endswith('.jsonl'):obj=[json.loads(x) for x in b.splitlines() if x.strip()]
        else:obj=json.loads(b)
        chosen=selected(obj)
        out='original_native_selected/'+name.replace('/','__')
        js(A/out,dict(original_path=path,original_git_binding=row,selected_problem_id=ID,
                      complete_selected_objects=chosen,selection_only=True,priority_or_claim_verification=False))
        row['selected_objects_path']=out;native.append(row)
    working=[]
    for name in nativepaths+['QUEUE.md','README.md','AGENTS.md']:
        p=R/'unsolved_math_prioritization'/name
        working.append(filebinding(p))
    for p in sorted((R/'unsolved_math_prioritization/cache').glob('*')):
        if p.is_file():
            foreign.append(filebinding(p))
    js(A/'original_native_input_bindings.json',dict(schema='pr46-original-native-individual-bindings/v1',
       captured_utc=now(),actual_pid=os.getpid(),head_native_individual_inputs=native,
       working_native_individual_inputs=working,foreign_cached_inputs_individually_bound=foreign,
       foreign_cached_bytes_never_copied=True,native_input_writes=False))
    js(A/'original_pr_metadata.json',dict(schema='pr46-original-github-and-git-metadata/v1',number=46,
       problem_id=ID,title=m['title'],body=m['body'],head=HEAD,github_base=BASE,merge_base=mb,
       github_state=m['state'],github_draft=m['draft'],all_changed_paths=changes,changed_files=len(changes),
       original_queue_row=matches[0],original_declared_status=original_status,original_declared_turns=original_turns,
       original_queue_git_binding=queuebinding,full_diff=dict(path='original_diff.patch',bytes=len(diff),sha256=sha(diff)),
       captured_utc=now(),actual_pid=os.getpid(),acceptance_verdict=None,mathematical_reproduction_performed=False))
    js(A/'snapshot_manifest.json',dict(schema='pr46-original-source-snapshot/v1',head=HEAD,github_base=BASE,
       merge_base=mb,files=files,original_files=len(files),whole_repository_diff_files=len(changes),
       created_utc=now(),actual_pid=os.getpid(),helper_execution_performed=False,acceptance_verdict=None))
    assert Path(__file__).read_bytes()==src
    print(json.dumps(dict(status='ORIGINAL_EXPORT_COMPLETED_ONLY',head=HEAD,github_base=BASE,merge_base=mb,
       original_files=len(files),diff_files=len(changes),diff_bytes=len(diff),diff_sha256=sha(diff),
       original_queue_row=matches[0],foreign_cache_inputs_bound=len(foreign)),sort_keys=True))
if __name__=='__main__':main()
