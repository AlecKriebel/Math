"""Prepared guards for PR311. Importing this file grants no publishing clearance."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, stat, subprocess, zipfile

A = Path(__file__).resolve().parent
P = A.parents[1]
R = P.parent
Q = A/'preprint_package_v02'
O = A/'submission_v02'
QUEUE = 'unsolved_math_prioritization/QUEUE.md'
PREFIX = 'unsolved_math_prioritization/attempts/30005303/'
RELEASE = PREFIX+'README.md'
ORIGINAL_HEAD = '895f2ba037e71bac054b58f1a4be7bb4d5dbd53a'
BRANCH = 'math/30005303-reviewed-mtp2'
FORMAL = ('mtp2-edge-closure-note.tex','mtp2-edge-closure-note.pdf',
          'mtp2-edge-closure-verification.zip','zenodo-deposit.json','SUBMISSION_MANIFEST.json')
utc = lambda: datetime.now(timezone.utc).isoformat()
sha = lambda b: hashlib.sha256(b).hexdigest()
load = lambda p: json.loads(p.read_bytes())

def pin(p):
    assert p.is_file() and not p.is_symlink(), p
    b = p.read_bytes()
    return {'bytes':len(b), 'sha256':sha(b), 'mode':format(stat.S_IMODE(p.stat().st_mode),'04o')}

def window():
    assert not load(P/'SHARED_GIT_WINDOW_STATUS.json')['shared_git_writes_paused']

class Capture:
    def __init__(self, purpose):
        self.directory = A/'root_integration_private'/(purpose+'_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f'))
        self.directory.mkdir(parents=True, exist_ok=False)
        self.entries = []
    def run(self, label, argv, input=None, ok=(0,), cwd=R):
        argv = [str(x) for x in argv]
        assert not (self.directory/(label+'.json')).exists()
        prep = {'started_utc':utc(), 'argv':argv, 'cwd':str(cwd),
                'program_pins':{x:pin(Path(x)) for x in argv if x.endswith('.py') and Path(x).is_file()}}
        (self.directory/(label+'.preexecution.json')).write_text(json.dumps(prep,indent=2)+'\n')
        run = subprocess.run(argv,cwd=cwd,input=input,capture_output=True,
            env=dict(os.environ,GIT_OPTIONAL_LOCKS='0',GIT_NO_LAZY_FETCH='1',PYTHONDONTWRITEBYTECODE='1'))
        streams = {}
        for name,b in [('stdout',run.stdout),('stderr',run.stderr)]:
            p = self.directory/(label+'.'+name)
            p.write_bytes(b)
            streams[name] = {'path':str(p), **pin(p)}
        rec = {**prep,'ended_utc':utc(),'exit_code':run.returncode,'streams':streams}
        self.entries.append(rec)
        (self.directory/(label+'.json')).write_text(json.dumps(rec,indent=2)+'\n')
        assert run.returncode in ok, (label,run.returncode,run.stderr.decode(errors='replace'))
        return run
    def git(self,*args,input=None,ok=(0,)):
        return self.run('git_'+str(len(self.entries)),['/usr/bin/git',*args],input=input,ok=ok).stdout
    def persist_foreign_snapshot(self,label,excluded=()):
        """Retain the actual baseline even if a later observation guard fails."""
        directory = self.directory/(label+'_foreign_baseline')
        directory.mkdir(exist_ok=False)
        args = ['ls-files','--stage','-z','--','.']+[':(exclude)'+n for n in sorted(excluded)]
        index = self.git(*args)
        (directory/'index.bin').write_bytes(index)
        bodies = dirty_tracked(self,excluded)
        entries = {}
        for n,(exists,body,mode) in bodies.items():
            entry = {'exists':exists,'mode':mode,'body_file':None,'bytes':None,'sha256':None}
            if body is not None:
                name = sha(n.encode())+'.body'
                (directory/name).write_bytes(body)
                entry.update(body_file=name,bytes=len(body),sha256=sha(body))
            entries[n] = entry
        (directory/'manifest.json').write_text(json.dumps({'recorded_utc':utc(),'excluded_paths':sorted(excluded),
            'index_bytes':len(index),'index_sha256':sha(index),'dirty_tracked_bodies':entries},indent=2)+'\n')
        return index,bodies

def current_clearance():
    # Written only after ROOT reads and independently adjudicates a NEW clean
    # whole-package review; an absent file is a hard gate, not inferred approval.
    c = load(A/'PUBLISHING_CLEARANCE.json')
    assert c['status'] == 'READY_AFTER_GLOBAL_REPAIRS_AND_NEW_FULL_PREPRINT_REVIEW'
    assert c['original_head'] == ORIGINAL_HEAD and c['original_status'] == 'claimed_solved'
    assert c['original_author_turn_count'] == '2/5'
    assert c['final_clean_review'] >= 2 and c['unresolved_findings'] == 0
    assert c['historical_review01_findings_retained'] and not c['historical_first_priority_certified']
    assert c['unrefereed'] and c['extensive_AI_use'] and not c['human_peer_review_claimed']
    assert set(c['formal_submission_files']) == set(FORMAL)
    assert {n:pin(O/n) for n in FORMAL} == c['formal_submission_files']
    assert pin(Q/'MANIFEST.json')['sha256'] == 'e08af5edc9c4aed6ccb4b92b3b2e8ea0505a02e762b27c31efbacf00d7b8f683'
    assert pin(O/'SUBMISSION_MANIFEST.json')['sha256'] == '043de76e326db5b5ba1af7fe2c7442bef1eed2d04de36654605045ce61f40383'
    assert {str(p.relative_to(Q)):pin(p) for p in Q.rglob('*') if p.is_file()} == c['package_files']
    for n,e in c['immutable_root_artifacts'].items():
        assert pin(A/n) == e, n
    for n,e in c['closed_scientific_files'].items():
        assert pin(A/n) == e, n
    f = load(A/c['final_review_closure'])
    assert f['status'] == 'PASS_ROOT_CLOSED_CLEAN_FULL_PREPRINT_REVIEW'
    assert f['unresolved_findings'] == 0 and f['complete_report_read']
    assert f['source_gate_unchanged'] and f['all_released_inputs_unchanged']
    assert f['sealed_review_authenticated'] and f['independent_reproduction_verified']
    original = load(A/'snapshot_manifest.json')
    assert original['head'] == ORIGINAL_HEAD and len(original['files']) == 30
    for e in original['files']:
        b = (A/'snapshot'/e['path']).read_bytes()
        assert len(b) == e['bytes'] and sha(b) == e['sha256']
    assert load(A/'ROOT_MATHEMATICAL_ACCEPTANCE.json')['status'] == 'PASS_BOTH_EXACT_SOURCE_MATHEMATICAL_ANSWERS_ACCEPTED'
    assert load(A/'ROOT_PRIORITY_DECISION_03.json')['status'] == 'PASS_BOUNDED_PRIORITY_AUDIT_QUALIFIED_RESEARCH_NOTE_PREPARATION'
    with zipfile.ZipFile(O/'mtp2-edge-closure-verification.zip') as z:
        assert len(z.namelist()) == 13 and set(z.namelist()) == set(c['package_files'])
        for n,e in c['package_files'].items():
            assert sha(z.read(n)) == e['sha256'] and z.read(n) == (Q/n).read_bytes()
            assert stat.S_IMODE(z.getinfo(n).external_attr >> 16) == 0o644
    return c

def dirty_tracked(cap, excluded=()):
    result = {}
    for n in cap.git('diff','--name-only','-z').split(b'\0'):
        if n and n.decode() not in excluded:
            p = R/n.decode()
            result[n.decode()] = (p.exists(),p.read_bytes() if p.is_file() else None,
                                  stat.S_IMODE(p.stat().st_mode) if p.exists() else None)
    return result

def ownrow(lines):
    found = [i for i,b in enumerate(lines) if len(b.split(b'|')) > 11 and b.split(b'|')[2].strip().split(b' / ')[0] == b'30005303']
    assert len(found) == 1
    return found[0]

def queue_binding(cap,base,tree):
    old = cap.git('show',base+':'+QUEUE).splitlines(keepends=True)
    new = cap.git('show',tree+':'+QUEUE).splitlines(keepends=True)
    assert len(old) == len(new)
    changed = [i for i,(a,b) in enumerate(zip(old,new)) if a != b]
    assert changed == [ownrow(old)]
    i = changed[0]
    a,b = old[i].split(b'|'),new[i].split(b'|')
    assert [a[j].strip() for j in (8,9)] == [b'queued',b'0/5']
    assert [b[j].strip() for j in (8,9)] == [b'claimed_solved',b'2/5']
    assert [j for j,(x,y) in enumerate(zip(a,b)) if x != y] == [8,9,11]
    r = load(A/'queue_repair_receipt.json')
    assert old[i].decode() == r['old_row'] and new[i].decode() == r['new_row']
    return {'queue_physical_line':i+1,'queue_only_pipe_cells':[8,9,11],
            'all_other_queue_bytes_equal':True,'base_row':old[i].decode(),'accepted_row':new[i].decode()}

def tree_binding(cap,base,tree):
    c = current_clearance()
    original = load(A/'snapshot_manifest.json')
    m = load(A/'repaired_snapshot_manifest.json')
    expected = {e['path'] for e in original['files']} | {RELEASE}
    assert len(expected) == 31 and {e['path'] for e in m['files']} == expected
    assert set(cap.git('diff','--name-only',base,tree).decode().splitlines()) == expected
    for e in m['files']:
        body = cap.git('show',tree+':'+e['path'])
        assert len(body) == e['bytes'] and sha(body) == e['sha256']
        assert cap.git('ls-tree',tree,'--',e['path']).split(b'\t',1)[0].split() == [b'100644',b'blob',e['git_blob_sha'].encode()]
    for e in original['files']:
        if e['path'] != QUEUE:
            body = cap.git('show',tree+':'+e['path'])
            assert len(body) == e['bytes'] and sha(body) == e['sha256']
    for n,e in c['formal_submission_files'].items():
        p = str((O/n).relative_to(R))
        body = cap.git('show',tree+':'+p)
        assert body == (O/n).read_bytes() and cap.git('show',base+':'+p) == body
    return {'all_expected_changed_paths_exact':31,'original_attempt_files_unchanged':29,
            'five_preexisting_formal_submission_files_exact':True,**queue_binding(cap,base,tree)}
