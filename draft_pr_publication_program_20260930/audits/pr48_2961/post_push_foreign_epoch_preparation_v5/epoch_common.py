"""SOURCE ONLY. Explicit per-phase foreign-epoch adapter; no original source is edited.

ROOT runtime loads this exact verified byte object. Every substitution is declared
and limited to declared current foreign identities, their authority path, the live
QUEUE assertion, and the actual derived finalizer source identity.
"""
from pathlib import Path, PurePosixPath
import argparse, datetime as dt, hashlib, json, math, os, re, stat, subprocess, sys, types

P = Path(__file__).absolute().parent
A = P.parent
R = A.parents[2]
H = A / 'acceptance_preparation_family_v3'
PREP = '9c525f7b540068af07477e8f794e21596d93e69e49e8dbc52972d3196eb9fda4'
MERGE = '209581a4627b01745974837fe7adab62ab8c0af7'
OLD_OPERATOR = '331cb4cb479113a8dbedc758e328b30a11bc93bcd052535953a4da9fd705095c'
ROOT_OPERATOR = 'c1ae969ccbbc48ed6fb486e96184da94329291a46b27d2b891ecb87185c909ec'
PHASES = ['finalize', 'mirror', 'post']
OWNED_LOGS = ['draft_pr_publication_program_20260930/audits/pr48_2961/ROOT_RESEARCH_LOG.md',
              'draft_pr_publication_program_20260930/RESEARCH_LOG.md']
SOURCE_NAMES = ['epoch_common.py', 'author_post_push_foreign_epoch_v5.py', 'execute_post_push_foreign_epoch_phase_v5.py', 'run_post_push_foreign_epoch_phase_v5.py', 'inspect_complete_actual_post_epoch_v5.py', 'integrate_reviewed_partial_epoch_v5.py', 'state_mirror_reconciliation_epoch_v5.py', 'CONTRACT.json', 'REPORT.md', 'NATIVE_SOURCE_DATE_SURVEY.json', 'private_mode_controls.py', 'PRIVATE_MODE_CONTROL_RESULTS.json', 'close_SOURCE_family.py', 'verify_closed_SOURCE_family.py', 'RESEARCH_LOG.md', 'REPAIR_PLAN.md', 'ACTUAL_REJECTED_V1_SOURCE_BINDINGS.json','M2_AND_SUPERSEDED_V2_BINDINGS.json','M3_AND_SUPERSEDED_V3_BINDINGS.json','M4_AND_SUPERSEDED_V4_BINDINGS.json']

def need(v, m):
    if not v: raise ValueError(m)
def sha(b): return hashlib.sha256(b).hexdigest()
def stamp(): return dt.datetime.now(dt.timezone.utc).isoformat()
def safe(n):
    need(type(n) is str and n and '\\' not in n and '\0' not in n, 'Literal relative path')
    p = PurePosixPath(n)
    need(not p.is_absolute() and p.as_posix() == n and not {'.', '..', '.git', '__pycache__'}.intersection(p.parts), 'Canonical relative path')
    return n
def regular(p):
    need(not p.is_symlink() and all(not q.is_symlink() for q in p.parents) and p.is_file(), 'Regular nonsymlink input')
    return p
def raw(p): return regular(p).read_bytes()
def parse(b):
    def pairs(items):
        d = {}
        for k, v in items: need(k not in d, 'Duplicate JSON key'); d[k] = v
        return d
    def fl(s):
        v = float(s); need(math.isfinite(v), 'Finite JSON number'); return v
    return json.loads(b, object_pairs_hook=pairs, parse_float=fl,
                      parse_constant=lambda s: (_ for _ in ()).throw(ValueError(s)))
def load(p): return parse(raw(p))
def eq(a, b):
    return type(a) is type(b) and (a.keys() == b.keys() and all(eq(a[k], b[k]) for k in a) if type(a) is dict else len(a) == len(b) and all(eq(x, y) for x, y in zip(a, b)) if type(a) is list else a == b)
def clock(s):
    need(type(s) is str and s == s.strip(), 'UTC literal')
    v = dt.datetime.fromisoformat(s[:-1] + '+00:00' if s.endswith('Z') else s)
    need(v.tzinfo is not None and v.utcoffset() == dt.timedelta(0), 'Aware UTC'); return v
def encode(v): return (json.dumps(v, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + '\n').encode()
def streamed(p):
    regular(p); before=p.stat(); h=hashlib.sha256(); size=0
    with p.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk); size+=len(chunk)
    after=p.stat()
    need((before.st_dev,before.st_ino,before.st_size,before.st_mtime_ns,before.st_mode)==(after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns,after.st_mode) and size==after.st_size,'Stable complete streamed body/mode')
    return dict(path=safe(p.relative_to(R).as_posix()),bytes=size,sha256=h.hexdigest(),worktree_mode=stat.S_IMODE(after.st_mode))
def ref(p): return {k:v for k,v in streamed(p).items() if k!='worktree_mode'}
def mode_ref(p): return streamed(p)
def check(z):
    need(type(z) is dict and set(z) == {'path', 'bytes', 'sha256'} and type(z['bytes']) is int and z['bytes'] >= 0 and type(z['sha256']) is str and re.fullmatch('[0-9a-f]{64}', z['sha256']), 'Typed triple')
    b = raw(R / safe(z['path'])); need(len(b) == z['bytes'] and sha(b) == z['sha256'], 'Entire referenced body'); return b
def put(p, b):
    need(not p.exists() and not p.is_symlink() and all(not q.is_symlink() for q in p.parents), 'Absent regular output')
    with p.open('xb') as f: f.write(b); f.flush(); os.fsync(f.fileno())
    need(stat.S_IMODE(p.stat().st_mode) == 0o644, 'Operational output full0644')

MODE_CONTRACT='pr48-source-operator-dependency-full07777/v5'
ADJACENT_NAMES=['author_post_push_foreign_epoch_v5.py','execute_post_push_foreign_epoch_phase_v5.py','run_post_push_foreign_epoch_phase_v5.py','inspect_complete_actual_post_epoch_v5.py']
ORIGINAL_RUNTIME_NAMES=['pr48_guards.py','integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py']
NEW_RUNTIME_NAMES=['epoch_common.py','integrate_reviewed_partial_epoch_v5.py','state_mirror_reconciliation_epoch_v5.py']
def source_read(p,expected):
    need(type(expected) is int and 0<=expected<=0o7777,'Typed expected source fullmode');regular(p);before=p.stat();need(stat.S_IMODE(before.st_mode)==expected,'Expected full07777 source mode at read')
    with p.open('rb') as f:
        opened=os.fstat(f.fileno());need((opened.st_dev,opened.st_ino,opened.st_mode)==(before.st_dev,before.st_ino,before.st_mode),'Exact regular opened source identity/mode');b=f.read();end=os.fstat(f.fileno())
    after=p.stat();need((before.st_dev,before.st_ino,before.st_size,before.st_mtime_ns,before.st_ctime_ns,before.st_mode)==(end.st_dev,end.st_ino,end.st_size,end.st_mtime_ns,end.st_ctime_ns,end.st_mode)==(after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns,after.st_ctime_ns,after.st_mode),'Source bytes/fullmode stable during read')
    return b,dict(path=safe(p.relative_to(R).as_posix()),bytes=len(b),sha256=sha(b),full_mode=expected)
def source_binding(p,expected):return source_read(p,expected)[1]
def source_binding_check(z,expected):
    need(type(z) is dict and set(z)=={'path','bytes','sha256','full_mode'} and type(z['full_mode']) is int and z['full_mode']==expected,'Typed separate source mode descriptor');b,current=source_read(R/safe(z['path']),expected);need(eq(current,z),'Entire source body/fullmode matches separate descriptor');return b
def directory_binding(p,expected=0o755):
    need(type(expected) is int and expected in (0o700,0o755),'Typed exact role directory fullmode');need(p.is_dir() and not p.is_symlink() and all(not q.is_symlink() for q in p.parents) and stat.S_IMODE(p.stat().st_mode)==expected,'Exact role-specific nonsymlink directory fullmode');return dict(path=safe(p.relative_to(R).as_posix()),full_mode=expected)
def directory_bindings(paths,expected=0o755):return [directory_binding(q,expected) for q in sorted(set(paths))]
def current_runtime_source_modes():
    adjacent=[]
    for n in ADJACENT_NAMES:
        b,z=source_read(A/n,0o644);original,_=source_read(P/n,0o444);need(b==original,'Actual adjacent source exactly closed prepared body and full0644');adjacent.append(z)
    native=source_binding(R/'draft_pr_publication_program_20260930/infrastructure/accepted_state_sync/revision2/accepted_state_sync_v2.py',0o644);need(native['sha256']=='ca7576ece5bc37a6e569a62764541de773243d38bffa811f4d1174f25635667f','Original native mirror body authority unchanged')
    return dict(adjacent=adjacent,prepared=[source_binding(P/n,0o444) for n in NEW_RUNTIME_NAMES],original=[source_binding(H/n,0o444) for n in ORIGINAL_RUNTIME_NAMES],native_mirror=native,directories=directory_bindings([A,P,H,(R/native['path']).parent]))
def actual_outer_parent(directory):
    need(directory.is_absolute() and directory.parent==A and directory.is_dir() and not directory.is_symlink() and all(not q.is_symlink() for q in directory.parents) and directory.resolve(strict=True)==directory and A.resolve(strict=True)==A,'Actual ROOT outer must have exact canonical nonsymlink A48 parent');return directory_binding(A)
def operator_binding(directory):
    actual_outer_parent(directory);z=source_binding(directory/'prelaunch_operator.py',0o644);need(z['sha256']==ROOT_OPERATOR,'Exact genuine ROOT outer operator body/fullmode');directory_binding(directory,0o700);return z
def live_operator_binding(directory):
    actual_outer_parent(directory);live,z=source_read(A/'capture_root_command.py',0o644);snapshot,_=source_read(directory/'prelaunch_operator.py',0o644);need(sha(live)==ROOT_OPERATOR and live==snapshot,'Actual live ROOT operator entire c1ae body/full0644 equals retained genuine snapshot');return dict(source=z,parent=directory_binding(A))
def retained_source_modes(directory,phase):
    rows=[source_binding(directory/'PRELAUNCH_SOURCE.py',0o644),source_binding(directory/'PRELAUNCH_OPERATOR.py',0o644)]
    dirs=[directory]
    for sub,names in [('ORIGINAL_DEPENDENCIES',dependency_names(phase)),('NEW_DEPENDENCIES',NEW_RUNTIME_NAMES)]:
        dirs.append(directory/sub);rows += [source_binding(directory/sub/n,0o644) for n in names]
    return dict(files=rows,directories=directory_bindings(dirs))
def author_source_modes(outer,directory):
    return dict(runtime=current_runtime_source_modes(),outer_operator=operator_binding(outer),actual_live_ROOT_operator=live_operator_binding(outer),prelaunch_source=source_binding(directory/'PRELAUNCH_SOURCE.py',0o644),directories=directory_bindings([directory])+directory_bindings([outer],0o700))
def caller_source_modes(outer,directory,phase):return dict(runtime=current_runtime_source_modes(),outer_operator=operator_binding(outer),actual_live_ROOT_operator=live_operator_binding(outer),retained=retained_source_modes(directory,phase),directories=directory_bindings([outer],0o700))
def artifact_modes(directory,names):
    out=[]
    for n in names:
        q=regular(directory/n);need(stat.S_IMODE(q.stat().st_mode)==0o644,'Actual epoch/capture artifact full0644');out.append(dict(path=safe(q.relative_to(R).as_posix()),full_mode=0o644))
    return out

def rejected_v1_binding():
    v=load(P/'ACTUAL_REJECTED_V1_SOURCE_BINDINGS.json');need(v['actual_closed_review_only'] is True and v['candidate_V1_ROOT_closed'] is False and v['repaired_candidate_ROOT_approved'] is False,'Rejected-only actual adverse binding')
    for name in ['verdict','report','adverse_SELF']:source_binding_check(v[name],0o444)
    need(v['adverse_SELF']['sha256']=='5493fc07f4a9e8911f18c828b296e1eeb6357a24d59eb9b5ee5c0027030c5a4a','Genuine closed rejected review');return v

def packet(ready_sha):
    need(__debug__ and sys.flags.optimize == 0 and os.environ.get('PYTHONOPTIMIZE', '') in ('', '0'), 'Nonoptimized SOURCE')
    need(sha(source_read(P / 'SOURCE_READY.json',0o444)[0]) == ready_sha, 'ROOT-supplied SOURCE READY hash')
    v = load(P / 'SOURCE_READY.json')
    need(v['schema'] == 'pr48-post-push-epoch-SOURCE-readiness/v5' and v['source_only'] is True and v['proposed_code_executed'] is False and v['actual_epoch_or_acceptance_approved'] is False, 'SOURCE-only packet')
    need([Path(z['path']).name for z in v['source_files']] == SOURCE_NAMES, 'Exact packet dependency list')
    bodies = {}
    for z in v['source_files']:
        name = Path(z['path']).name
        need(z['path'] == (P / name).relative_to(R).as_posix(), 'Exact own SOURCE path')
        bodies[name],mode=source_read(P/name,0o444);need(eq({k:mode[k] for k in ['path','bytes','sha256']},z),'Unchanged old triple schema plus explicit prepared source fullmode')
    return v, bodies

def original_sources():
    b,_ = source_read(H / 'PREPARATION_MANIFEST.json',0o444); need(sha(b) == PREP and stat.S_IMODE((H / 'PREPARATION_MANIFEST.json').stat().st_mode) == 0o444, 'Exact original closed self')
    v = parse(b); need(v['schema'] == 'pr48-acceptance-source-closure/v3' and v['self_excluded'] == ['PREPARATION_MANIFEST.json'] and type(v['files_count']) is int and v['files_count'] == len(v['files']) == 53, 'Original53 SOURCE')
    names = {safe(z['path']) for z in v['files']}; need(len(names) == 53, 'Distinct original files')
    dirs = {p.as_posix() for n in names for p in PurePosixPath(n).parents if p.as_posix() != '.'}
    need({p.relative_to(H).as_posix() for p in H.rglob('*') if p.is_file()} == names | {'PREPARATION_MANIFEST.json'} and {p.relative_to(H).as_posix() for p in H.rglob('*') if p.is_dir()} == dirs and all(not p.is_symlink() and (p.is_file() or p.is_dir()) for p in H.rglob('*')), 'Exact original topology without bytecode')
    result = {}
    for z in v['files']:
        p = H / z['path']; x,_ = source_read(p,0o444); need(len(x) == z['bytes'] and sha(x) == z['sha256'] and stat.S_IMODE(p.stat().st_mode) == 0o444, 'Original complete payload/mode'); result[z['path']] = x
    directory_bindings([H]+[q for q in H.rglob('*') if q.is_dir()]);return result

def module(name, body, path):
    need(name not in sys.modules, 'No preexisting injected production module')
    actual,mode=source_read(path,0o444);need(actual==body,'Exact cached verified source object/fullmode before compile');directory_binding(path.parent)
    m = types.ModuleType(name); m.__file__ = str(path); sys.modules[name] = m
    exec(compile(body, str(path), 'exec'), m.__dict__)
    need(eq(source_binding(path,0o444),mode),'Source bytes/fullmode unchanged through cached object execution');return m

def pins():
    pre = load(A / 'integration_preflight.json')
    names = ['preparation_manifest_sha256']
    for n in ['final_plan', 'final_receipt', 'final_manifest', 'reconciliation_capture', 'previous_mirror', 'previous_post', 'fresh_preimage', 'root_bindings']: names += [n, n + '_sha256']
    result = {n: pre[n] for n in names}; need(result['preparation_manifest_sha256'] == PREP, 'Original17 pins')
    for n in names[1::2]: need(sha(raw(R / safe(result[n]))) == result[n + '_sha256'], 'Unchanged original reference')
    return result

def literal_helper_argv(phase, values):
    name = {'mirror': 'state_mirror_reconciliation.py', 'post': 'verify_post_acceptance.py'}.get(phase, 'integrate_reviewed_partial.py')
    a = ['/usr/bin/python3', '-B', str(H / name), '--execute', '--preparation-manifest-sha256', PREP]
    for n in ['final_plan', 'final_receipt', 'final_manifest', 'reconciliation_capture', 'previous_mirror', 'previous_post', 'fresh_preimage', 'root_bindings']:
        a += ['--' + n.replace('_', '-'), values[n], '--' + n.replace('_', '-') + '-sha256', values[n + '_sha256']]
    if phase not in ['mirror', 'post']: a += [phase]
    if phase == 'overlay': a += ['--merge-queue-preimage-sha256', load(A / 'integration_check.json')['automatic_merge_queue_preimage_sha256']]
    return a

def cap4(path):
    c = load(path); need({p.name for p in path.parent.iterdir()} == {'CAPTURE.json', 'prelaunch_operator.py', 'stdout.bin', 'stderr.bin'}, 'ROOT CAP4 complete')
    need(c['schema'] == 'root-explicit-command-capture/v1' and c['actual_execution'] is True and c['completed'] is True and type(c['pid']) is int and c['pid'] > 0 and type(c['exit_code']) is int and c['exit_code'] == 0 and c['status'] == 'PASS' and c['operator_unchanged'] is True and c['stdin_supplied'] is False and c['cwd'] == str(R), 'Genuine completed successful ROOT child')
    need(sha(raw(path.parent / 'prelaunch_operator.py')) == c['operator_sha256'] == ROOT_OPERATOR, 'Actual ROOT operator')
    for k in ['stdout', 'stderr']:
        z = c[k]; need(z['path'] == k + '.bin', 'Literal complete stream'); b = raw(path.parent / z['path']); need(len(b) == z['bytes'] and sha(b) == z['sha256'], 'Whole ROOT streams')
    need(clock(c['started_utc']) <= clock(c['finished_utc']) <= dt.datetime.now(dt.timezone.utc), 'Actual ROOT times')
    return c

def original_prefix(values):
    rows = []; last = None; old_foreign = load(A / 'integration_preflight.json')['foreign_logs']
    for phase in ['preflight', 'overlay', 'prepush']:
        d = A / ('root_' + phase + '_actual_capture'); c = load(d / 'CAPTURE.json'); pre = load(d / 'PRELAUNCH.json')
        need({q.name for q in d.iterdir()} == {'CAPTURE.json', 'PRELAUNCH.json', 'PRELAUNCH_SOURCE.py', 'PRELAUNCH_OPERATOR.py', 'stdout.bin', 'stderr.bin'}, 'Original actual CAP6')
        need(c['schema'] == 'ROOT_actual_reviewed_acceptance_phase_capture_v1' and c['phase'] == phase and c['actual_execution'] is True and c['completed'] is True and type(c['pid']) is int and c['pid'] > 0 and type(c['exit_code']) is int and c['exit_code'] == 0 and c['status'] == 'PASS' and c['source_unchanged'] is True and c['operator_unchanged'] is True and c['complete_final_references_unchanged'] is True and c['protected_foreign_full_bodies_modes_unchanged'] is True, 'Genuine dated first3 successes')
        need(eq(c['argv'], literal_helper_argv(phase, values)) and all(eq(c[k], v) for k, v in pre.items() if k != 'schema') and sha(raw(d / 'PRELAUNCH_OPERATOR.py')) == c['operator_sha256'] == OLD_OPERATOR and sha(raw(d / 'PRELAUNCH_SOURCE.py')) == c['source_sha256'] == sha(raw(H / 'integrate_reviewed_partial.py')), 'Exact original role/source/operator/argv')
        foreign = [{k: z[k] for k in ['path', 'bytes', 'sha256', 'worktree_mode']} for z in old_foreign]
        need(eq(c['protected_foreign_before'], foreign) and eq(c['protected_foreign_after'], foreign), 'Original foreign equality belongs to original epoch')
        for k in ['stdout', 'stderr']:
            z = c[k]; need(z['path'] == k + '.bin', 'Literal phase stream'); b = raw(d / z['path']); need(len(b) == z['bytes'] and sha(b) == z['sha256'], 'Whole original streams')
        need(raw(d / 'stderr.bin') == b'' and clock(c['prepared_utc']) <= clock(c['started_utc']) <= clock(c['finished_utc']) and (last is None or last <= clock(c['started_utc'])), 'Original chronological roles')
        last = clock(c['finished_utc']); rows.append(ref(d / 'CAPTURE.json'))
    return rows

def git_index(g):
    name=g.git('rev-parse','--git-path','index'); p=Path(name); p=p if p.is_absolute() else R/p
    regular(p); before=p.stat(); b=p.read_bytes(); after=p.stat()
    need((before.st_ino,before.st_size,before.st_mtime_ns,before.st_mode)==(after.st_ino,after.st_size,after.st_mtime_ns,after.st_mode),'Stable whole actual index')
    return dict(absolute_path=str(p.absolute()),bytes=len(b),sha256=sha(b),full_mode=stat.S_IMODE(after.st_mode))
def tracked_foreign(g):
    need(g.git('branch','--show-current')=='main' and g.git_bytes('diff','--cached','--name-only','-z')==b'','Main and globally clean index')
    dirty=g.git_bytes('diff','--name-only','-z').decode().split('\0'); need(dirty[-1]=='','Complete NUL dirty domain')
    names=sorted({safe(n) for n in dirty if n and not g.owned_mutation_path(n)})
    # Both old unrelated paper logs remain protected even if temporarily clean.
    old=load(A/'integration_preflight.json')['foreign_logs']
    papers=[z for z in old if z['path'].startswith('paper_ii_simultaneous_amplification_referee_audit_2026-08-22/logs/')]
    need(len(papers)==2,'Exact dated unrelated paper pair')
    names=sorted(set(names)|{z['path'] for z in papers}); out=[]
    for n in names:
        v=mode_ref(R/n); e=g.git_bytes('ls-tree','-z','HEAD','--',n).decode().rstrip('\0'); i=g.git_bytes('ls-files','--stage','-z','--',n).decode().rstrip('\0')
        fields,literal=e.split('\t'); mode,kind,oid=fields.split(); need(literal==n and mode in {'100644','100755'} and kind=='blob' and i==mode+' '+oid+' 0\t'+n,'Exact regular tracked HEAD/index row')
        hb=g.git_bytes('show','HEAD:'+n); ib=g.git_bytes('show',':'+n);need(hb==ib,'Entire current HEAD/index body equality')
        out.append(dict(v,head_sha256=sha(hb),head_entry=e,index_entry=i))
    for z in papers: need(eq(next(v for v in out if v['path']==z['path']),z),'Both unrelated paper logs retain exact dated body/mode/HEAD/index')
    return out

def queue_check(g,epoch,after):
    current=raw(g.Q); z=epoch['current_queue']; need(eq(mode_ref(g.Q),z),'Current entire queue/mode bound to this epoch')
    need(g.selected(current)==g.selected(after),'Only original accepted PR48 row is own disposition authority');g.alias_QUEUE_absent(current)
    need(current==g.git_bytes('show',epoch['current_head']+':'+g.Q.relative_to(R).as_posix())==g.git_bytes('show',':'+g.Q.relative_to(R).as_posix()),'Current unrelated queue rows authenticated by whole HEAD/index body')
    return current

def native_and_logs(g, phase, current_queue=None):
    fresh = load(A / 'ROOT_FRESH_ACCEPTANCE_INPUT_PREIMAGES.json'); pre = load(A / 'integration_preflight.json'); rows = []
    need(len(fresh['files']) == 13 and {z['path'] for z in fresh['files']} == g.NATIVE, 'Exact native13 domain')
    mutable = {'unsolved_math_prioritization/QUEUE.md': (current_queue or mode_ref(g.Q))['sha256']}
    if phase in ['mirror', 'post']:
        final = load(A / 'integration_finalization.json'); remote = load(A / 'remote_merge_receipt.json'); inv = g.derive_inventory(load(A / 'integration_inventory_before.json'), remote, final['utc']); need(eq(load(g.B / 'inventory.json'), inv), 'Exact derived inventory before later epoch')
        mutable[(g.B / 'inventory.json').relative_to(R).as_posix()] = sha(raw(g.B / 'inventory.json'))
    if phase == 'post':
        plan = load(A / 'state_mirror_plan.json'); need(raw(R / 'unsolved_math_prioritization/state.json') == plan['state_after_bytes'].encode() and raw(R / 'unsolved_math_prioritization/history.jsonl') == raw(A / 'integration_history_before.jsonl') + plan['history_append_bytes'].encode(), 'Exact mirror outputs before post epoch')
        mutable.update({'unsolved_math_prioritization/state.json': sha(plan['state_after_bytes'].encode()), 'unsolved_math_prioritization/history.jsonl': plan['history_after_sha256']})
    for z in fresh['files']:
        v = mode_ref(R / z['path']); need(type(z['worktree_mode']) is int and v['worktree_mode'] == z['worktree_mode'] and v['sha256'] == mutable.get(z['path'], z['sha256']), 'Only exact phase-authorized native changes'); rows.append(v)
    original_logs = load(A / 'ROOT_SOURCE_ACCEPTANCE_REVIEW.json')['exact_owned_operational_log_preimages']; logs = []
    for n in OWNED_LOGS:
        z = next(z for z in original_logs if z['path'] == n); v = mode_ref(R / n); expected = z['preimage']['full_mode'] if z['present'] else 0o644; need(v['worktree_mode'] == expected, 'Original full owned-log mode')
        if phase in ['mirror', 'post']:
            receipt = load(A / 'integration_log_append_receipt.json'); after = next(z['after'] for z in receipt['logs'] if z['log'] == n); need(eq({k: v[k] for k in ['path', 'bytes', 'sha256']}, after), 'Both prior finalization append bodies remain exact')
        logs.append(v)
    return rows, logs

def absent_outputs(phase):
    names = {'finalize': [A / n for n in ['remote_merge_receipt.json', 'integration_finalization.json', 'acceptance.json', 'integration_log_append_receipt.json', 'integration_log_preimages']] + [R / 'unsolved_math_prioritization/attempts/2961' / n for n in ['acceptance.json', 'ACCEPTANCE.md', 'MANIFEST.json']],
             'mirror': [A / n for n in ['state_mirror_bindings.json', 'state_mirror_plan.json', 'state_mirror_intent.json', 'state_mirror_receipt.json']],
             'post': [A / 'post_acceptance_verification.json']}[phase]
    present = [p.relative_to(R).as_posix() for p in names if p.exists() or p.is_symlink()]
    need(not present, 'Partial/completed outputs prohibit blind retry; ROOT recovery required: ' + repr(present))

EPOCH_KEYS={'schema','phase','status','approved_by_ROOT','utc','actual_ROOT_author_pid','science_or_original_approval_changed','original_dated_foreign_live_equality_asserted','source_ready','source_manifest','independent_SOURCE_review','original_preflight','original_preparation_manifest_sha256','merge_commit','current_head','whole_index','dated_original_foreign_rows','protected_foreign_tracked_paths','current_foreign_rows','current_queue','native13_before','owned_logs_before','original17_pins','genuine_push_capture','genuine_commit_capture','original_successful_prefix','readonly_ledger','declared_delegations','mode_contract','source_modes_before','source_modes_after','source_custody_modes'}
DELEGATIONS=['foreign_check: foreign_logs and fresh_preimage only within predicate','live queue: exact current whole body plus original accepted2961 row and absent30004403','finalization: actual derived integration source_sha256 only', 'native mirror loader: same SHA-bound bytes and ledger predicates, direct byte execution without .pyc']
def source_review(z,ready_sha):
    v=parse(check(z));need(v['schema']=='pr48-post-push-epoch-independent-SOURCE-verdict/v1' and v['status']=='PASS_SOURCE_ONLY' and v['source_ready_sha256']==ready_sha and v['mandatory_findings']==[] and v['production_executed'] is False and v['future_acceptance_approved'] is False and stat.S_IMODE((R/z['path']).stat().st_mode)==0o444,'Actual independent verdict exact source pin/no future authority')
    return v

def validated_epoch(path,expected_sha,phase,author_cap,ready_sha,manifest_sha):
    b=raw(path);need(sha(b)==expected_sha,'Explicit actual epoch hash');e=parse(b)
    need(type(e) is dict and set(e)==EPOCH_KEYS and e['schema']=='pr48-ROOT-post-push-per-phase-foreign-epoch/v5' and e['phase']==phase and e['status']=='ROOT_APPROVED_CURRENT_FOREIGN_EPOCH_ONLY' and e['approved_by_ROOT'] is True and e['mode_contract']==MODE_CONTRACT and e['science_or_original_approval_changed'] is False and e['original_dated_foreign_live_equality_asserted'] is False,'Exact typed actual ROOT epoch')
    c=cap4(author_cap);need(type(e['actual_ROOT_author_pid']) is int and e['actual_ROOT_author_pid']==c['pid'] and clock(c['started_utc'])<=clock(e['utc'])<=clock(c['finished_utc']),'Actual epoch author interval/PID')
    need(c['argv']==author_argv(phase,ready_sha,manifest_sha,e['independent_SOURCE_review'],path.name,e['genuine_commit_capture']['path'],e['genuine_push_capture']['path'],author_cap.parent.relative_to(R).as_posix()),'Exact actual epoch author argv')
    stdout=load(author_cap.parent/'stdout.bin');need(eq(stdout,dict(status='PASS_ACTUAL_ROOT_FOREIGN_EPOCH_ONLY',epoch=ref(path),actual_pid=c['pid'])),'Whole actual author stdout')
    need(eq(e['source_ready'],ref(P/'SOURCE_READY.json')) and e['source_ready']['sha256']==ready_sha and eq(e['source_manifest'],ref(P/'SOURCE_MANIFEST.json')) and e['source_manifest']['sha256']==manifest_sha,'Own actual closed source authority');source_review(e['independent_SOURCE_review'],ready_sha)
    pre=load(A/'integration_preflight.json');need(eq(e['original_preflight'],ref(A/'integration_preflight.json')) and eq(e['dated_original_foreign_rows'],pre['foreign_logs']) and e['merge_commit']==MERGE and e['original_preparation_manifest_sha256']==PREP and eq(e['original17_pins'],pins()) and e['declared_delegations']==DELEGATIONS,'Original dated authority and explicit delegation only')
    need(type(e['current_head']) is str and re.fullmatch('[0-9a-f]{40}',e['current_head']) and e['protected_foreign_tracked_paths']==sorted(set(e['protected_foreign_tracked_paths'])) and [z['path'] for z in e['current_foreign_rows']]==e['protected_foreign_tracked_paths'],'Typed distinct current foreign domain')
    for z in e['current_foreign_rows']:
        need(set(z)=={'path','bytes','sha256','worktree_mode','head_sha256','head_entry','index_entry'} and type(z['bytes']) is int and type(z['worktree_mode']) is int and 0<=z['worktree_mode']<=0o7777 and re.fullmatch('[0-9a-f]{64}',z['sha256']) and re.fullmatch('[0-9a-f]{64}',z['head_sha256']),'Complete typed current row')
    ledger=parse(check(e['readonly_ledger']));need(type(ledger) is list and ledger,'Complete actual readonly source-mode ledger')
    digest=sha(encode(e['source_modes_before']))
    for row in ledger:need(row['schema']=='pr48-epoch-actual-memory-readonly/v5' and row['mode_contract']==MODE_CONTRACT and row['source_mode_bindings_before_sha256']==row['source_mode_bindings_after_sha256']==digest and row['source_fullmodes_unchanged'] is True and row['status']=='PASS' and type(row['pid']) is int and row['pid']>0 and row['actual_execution'] is True and row['completed'] is True and type(row['exit_code']) is int and row['exit_code']==0 and row['source'] is None and row['source_unchanged'] is None,'Every genuine readonly child carries actual complete fullmode boundary digest')
    need(eq(e['source_modes_before'],e['source_modes_after']),'Actual author source/operator/prelaunch/dependency bytes and fullmodes before/after')
    need(eq(author_source_modes(author_cap.parent,(R/e['readonly_ledger']['path']).parent),e['source_modes_before']),'Current actual author mode custody matches complete before/after descriptors')
    custody=e['source_custody_modes'];need(eq(custody['readonly_ledger'],source_binding(R/e['readonly_ledger']['path'],0o644)) and eq(custody['epoch'],dict(path=safe(path.relative_to(R).as_posix()),full_mode=0o644)) and stat.S_IMODE(path.stat().st_mode)==0o644,'Actual epoch and readonly ledger fullmode')
    artifact_modes(author_cap.parent,['prelaunch_operator.py','stdout.bin','stderr.bin','CAPTURE.json']);return e

def activate(epoch,phase,original_bodies,new_bodies,readonly_git=None):
    g=module('pr48_guards',original_bodies['pr48_guards.py'],H/'pr48_guards.py')
    if readonly_git is not None:g.git_bytes=readonly_git
    original_predicate=g.foreign_check;original_pre=load(A/'integration_preflight.json')
    def current_foreign(pre):
        need(eq(pre,original_pre),'No original preflight field is rewritten')
        need(g.git('rev-parse','HEAD')==epoch['current_head'] and eq(git_index(g),epoch['whole_index']),'Own epoch whole HEAD/index unchanged')
        need([z['path'] for z in tracked_foreign(g)]==epoch['protected_foreign_tracked_paths'],'Complete current tracked dirty foreign domain remains exact')
        effective=dict(pre,foreign_logs=epoch['current_foreign_rows'],fresh_preimage=epoch['_actual_path'])
        original_predicate(effective)
    g.foreign_check=current_foreign
    g.current_epoch_queue_check=lambda after:queue_check(g,epoch,after)
    def finalization(pins,pre):
        record=g.load(A/'integration_finalization.json');remote=g.load(A/'remote_merge_receipt.json')
        g.keyset(remote,{'number','url','state','isDraft','headRefOid','headRefName','baseRefName','mergeCommit','mergedAt','body'},'Complete actual retained remote schema')
        g.require(type(record) is dict and 'utc' in record,'Actual finalization required')
        expected={'schema':'pr48-actual-integration-finalization/v1','utc':record['utc'],**pins,'pr':48,'before_inventory_sha256':pre['inventory_before_sha256'],'remote_merge_receipt':g.pin(A/'remote_merge_receipt.json'),'merge_commit':remote['mergeCommit']['oid'],'merge_tree':g.git('show','-s','--format=%T',remote['mergeCommit']['oid']),'source_sha256':sha(new_bodies['integrate_reviewed_partial_epoch_v5.py'])}
        g.exact_reference(record['remote_merge_receipt']);g.require(g.equal(record,expected),'Entire typed finalization uses actual derived source SHA only')
        final_clock=g.utc_clock(record['utc'],'Actual finalization UTC');clocks=[g.utc_clock(g.load(A/n)['utc'],'Actual prior role UTC') for n in ['integration_preflight.json','integration_check.json','integration_prepush.json']]+[final_clock]
        g.require(clocks==sorted(clocks) and final_clock<=dt.datetime.now(dt.timezone.utc) and g.utc_clock(remote['mergedAt'],'Merged UTC')<=final_clock,'Actual chronological finalization')
        before=raw(A/'integration_inventory_before.json');g.require(sha(before)==pre['inventory_before_sha256'],'Whole prior inventory');g.derive_inventory(parse(before),remote,record['utc']);return record,remote
    g.finalization=finalization
    def mirror_module_without_bytecode(proposal):
        p=g.BASE/'revision2/accepted_state_sync_v2.py';body,mode=source_read(p,0o644);g.require(sha(body)==g.MIRROR_SHA,'Reviewed native mirror source changed')
        # The only loader change: execute this verified byte object, never .pyc.
        m=types.ModuleType('pr48_bound_native_mirror');m.__file__=str(p);exec(compile(body,str(p),'exec'),m.__dict__)
        budgets=[]
        for e in proposal['entries']:
            b=e['budget'];g.require(type(b['used']) is int and type(b['limit']) is int and 0<=b['used']<=b['limit'],'Typed preserved prior budget')
            whole=g.regular(R,b['ledger']['path']).read_bytes();g.require(sha(whole)==b['ledger']['sha256'],'Full original prior ledger changed');budgets.append((b['kind'],b['used'],b['limit'],whole))
        def ledger(whole,kind,used,limit):
            m.require(type(used) is int and type(limit) is int and any(kind==k and used==u and limit==l and whole==d for k,u,l,d in budgets),'Exact complete accepted ledger/budget required; no inference')
        m.ledger_budget=ledger
        def strict_bound(repo,reference):
            g.require(Path(repo).resolve()==R.resolve(),'Exact native mirror repository required');whole=g.regular(R,reference['path']).read_bytes();g.require(sha(whole)==g.digest(reference['sha256']),'Strict native mirror binding changed');return whole
        m.bound=strict_bound;need(eq(source_binding(p,0o644),mode),'Native source fullmode unchanged through verified byte execution');return m
    g.mirror_module=mirror_module_without_bytecode
    module('integrate_reviewed_partial',new_bodies['integrate_reviewed_partial_epoch_v5.py'],P/'integrate_reviewed_partial_epoch_v5.py')
    module('state_mirror_reconciliation',new_bodies['state_mirror_reconciliation_epoch_v5.py'],P/'state_mirror_reconciliation_epoch_v5.py')
    module('verify_post_acceptance',original_bodies['verify_post_acceptance.py'],H/'verify_post_acceptance.py')
    g.foreign_check(original_pre);return g

class Readonly:
    """Actual ROOT runtime: whole responses consumed; no large stdout corpus saved."""
    def __init__(self,source,mode_scope):self.source=source;self.mode_scope=mode_scope;self.records=[]
    def run(self,argv):
        need((argv[0]=='git' and argv[1] in ['branch','rev-parse','show','ls-tree','ls-files','diff','diff-tree','merge-base']) or argv==remote_argv(),'Readonly literal argv')
        c=dict(schema='pr48-epoch-actual-memory-readonly/v5',argv=argv,cwd=str(R),source=None,source_unchanged=None,operator_sha256=sha(self.source),operator_pid=os.getpid(),started_utc=stamp(),stdin_supplied=False,actual_execution=False,completed=False,pid=None,exit_code=None);out=err=b'';child=None
        try:
            modes=self.mode_scope();c['source_mode_bindings_before_sha256']=sha(encode(modes));c['mode_contract']=MODE_CONTRACT
            env=dict(os.environ,GIT_OPTIONAL_LOCKS='0',GIT_LITERAL_PATHSPECS='1')
            for k in ['GIT_DIR','GIT_WORK_TREE','GIT_INDEX_FILE','GIT_OBJECT_DIRECTORY','GIT_ALTERNATE_OBJECT_DIRECTORIES']:env.pop(k,None)
            child=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=env);c.update(actual_execution=True,pid=child.pid);out,err=child.communicate();c.update(completed=True,exit_code=child.returncode);after=self.mode_scope();c.update(source_mode_bindings_after_sha256=sha(encode(after)),source_fullmodes_unchanged=eq(modes,after));need(c['source_fullmodes_unchanged'] is True,'Source/operator fullmode changed across actual readonly child')
        except BaseException as exc:
            c['operator_error']=repr(exc)
            if child is not None:out,err=child.communicate();c.update(completed=True,exit_code=child.returncode)
        c.update(finished_utc=stamp(),stdout=dict(bytes=len(out),sha256=sha(out),retained_on_disk=False,complete_body_consumed_in_memory=True),stderr=dict(bytes=len(err),sha256=sha(err),retained_on_disk=False,complete_body_consumed_in_memory=True))
        c['status']='PASS' if c['actual_execution'] is True and c['completed'] is True and type(c['pid']) is int and c['pid']>0 and type(c['exit_code']) is int and c['exit_code']==0 and err==b'' and c.get('source_fullmodes_unchanged') is True and 'operator_error' not in c else 'FAIL';self.records.append(c);need(c['status']=='PASS','Actual readonly child failure retained in outer/source ledger');return out
    def git(self,*args):return self.run(['git',*args])

def remote_argv():
    return ['gh', 'pr', 'view', '48', '--repo', 'AlecKriebel/Math', '--json', 'number,url,state,isDraft,headRefOid,headRefName,baseRefName,mergeCommit,mergedAt,body']

def epoch_args(p):
    p.add_argument('--source-ready-sha256', required=True)
    p.add_argument('--source-manifest-sha256', required=True)
    p.add_argument('--phase', choices=PHASES, required=True)
    p.add_argument('--foreign-epoch', required=True)
    p.add_argument('--foreign-epoch-sha256', required=True)
    p.add_argument('--epoch-author-capture', required=True)

def adapter_argv(phase, ready_sha, manifest_sha, epoch_ref, author_capture):
    return ['/usr/bin/python3', '-B', str(A / 'execute_post_push_foreign_epoch_phase_v5.py'), '--source-ready-sha256', ready_sha, '--source-manifest-sha256', manifest_sha, '--phase', phase, '--foreign-epoch', epoch_ref['path'], '--foreign-epoch-sha256', epoch_ref['sha256'], '--epoch-author-capture', author_capture]

def dependency_names(phase):
    result = ['pr48_guards.py', 'integrate_reviewed_partial.py']
    if phase in ['mirror', 'post']: result.append('state_mirror_reconciliation.py')
    if phase == 'post': result.append('verify_post_acceptance.py')
    return result

def phase_capture(phase, ready_sha, manifest_sha):
    d = A / ('root_' + phase + '_actual_capture'); c = load(d / 'CAPTURE.json'); pre = load(d / 'PRELAUNCH.json')
    need({p.name for p in d.iterdir()} == {'CAPTURE.json', 'PRELAUNCH.json', 'PRELAUNCH_SOURCE.py', 'PRELAUNCH_OPERATOR.py', 'stdout.bin', 'stderr.bin', 'ORIGINAL_DEPENDENCIES', 'NEW_DEPENDENCIES'}, 'New transparent adapter capture topology')
    need(c['schema'] == 'ROOT_actual_explicit_post_push_epoch_phase_capture_v5' and c['phase'] == phase and c['actual_execution'] is True and c['completed'] is True and type(c['pid']) is int and c['pid'] > 0 and type(c['exit_code']) is int and c['exit_code'] == 0 and c['status'] == 'PASS' and c['source_unchanged'] is True and c['operator_unchanged'] is True and c['original_dependencies_unchanged'] is True and c['new_dependencies_unchanged'] is True and c['complete_final_references_unchanged'] is True and c['protected_foreign_unchanged_during_this_phase'] is True and c['native_modes_and_owned_logs_scope_checked'] is True and c['source_fullmodes_unchanged'] is True, 'Genuine new phase success, never old helper relabel')
    need(all(eq(c[k], v) for k, v in pre.items() if k != 'schema') and c['source_ready_sha256'] == ready_sha and sha(raw(d / 'PRELAUNCH_SOURCE.py')) == c['source_sha256'] == sha(raw(P / 'execute_post_push_foreign_epoch_phase_v5.py')) and sha(raw(d / 'PRELAUNCH_OPERATOR.py')) == c['operator_sha256'] == sha(raw(P / 'run_post_push_foreign_epoch_phase_v5.py')), 'Entire new source/operator/prelaunch binding')
    need(c['mode_contract']==MODE_CONTRACT and eq(c['source_modes_before'],c['source_modes_after']),'Entire actual new role source/dependency fullmode preservation')
    e = validated_epoch(R / c['foreign_epoch']['path'], c['foreign_epoch']['sha256'], phase, R / c['epoch_author_capture']['path'], ready_sha, manifest_sha)
    need(eq(c['argv'], adapter_argv(phase, ready_sha, manifest_sha, c['foreign_epoch'], c['epoch_author_capture']['path'])) and eq(c['original17_pins'], pins()) and eq(c['delegated_original_helper_argv'], literal_helper_argv(phase, pins())), 'Literal actual adapter argv distinct from delegated helper argv')
    outer=R/safe(c['outer_capture_directory']);need(eq(caller_source_modes(outer,d,phase),c['source_modes_before']),'Current actual caller source/operator/prelaunch/dependency modes equal genuine before/after rows')
    need(eq(c['artifact_mode_bindings'],artifact_modes(d,['PRELAUNCH.json','PRELAUNCH_SOURCE.py','PRELAUNCH_OPERATOR.py','stdout.bin','stderr.bin','CAPTURE.json'])),'Actual complete new phase artifact modes')
    outercap=cap4(outer/'CAPTURE.json');need(outercap['pid']==c['operator_pid'] and eq(outercap['argv'],caller_argv(phase,ready_sha,manifest_sha,c['foreign_epoch'],c['epoch_author_capture']['path'],c['outer_capture_directory'])),'Genuine actual caller PID/argv/outer operator custody');artifact_modes(outer,['prelaunch_operator.py','stdout.bin','stderr.bin','CAPTURE.json'])
    current = [{k: z[k] for k in ['path', 'bytes', 'sha256', 'worktree_mode']} for z in e['current_foreign_rows']]
    need(eq(c['protected_foreign_before'], current) and eq(c['protected_foreign_after'], current) and c['original_dated_foreign_live_equality_asserted'] is False, 'Current equality bounded to own epoch')
    dep = d / 'ORIGINAL_DEPENDENCIES'; need({p.name for p in dep.iterdir()} == set(dependency_names(phase)) and len(c['original_dependency_refs']) == len(dependency_names(phase)), 'Complete retained original dependency sources')
    for z in c['original_dependency_refs']:
        b = check(z); need(b == raw(H / Path(z['path']).name), 'Original dependency body preserved exactly')
    new = d / 'NEW_DEPENDENCIES'; need({p.name for p in new.iterdir()} == {'epoch_common.py', 'integrate_reviewed_partial_epoch_v5.py', 'state_mirror_reconciliation_epoch_v5.py'}, 'Exact transparent new dependencies')
    need(len(c['new_dependency_refs']) == 3, 'All new dependency refs')
    for z in c['new_dependency_refs']: need(check(z) == raw(P / Path(z['path']).name), 'New actual cached source body')
    need(eq(c['native13_before'], e['native13_before']) and eq(c['owned_mutable_logs_before'], e['owned_logs_before']) and eq(c['HEAD_before'], c['HEAD_after']) and eq(c['whole_index_before'], c['whole_index_after']), 'Actual own epoch envelope')
    need(c['source_manifest_sha256']==manifest_sha and c['declared_delegations']==DELEGATIONS and c['HEAD_before']==e['current_head'] and eq(c['whole_index_before'],e['whole_index']), 'Exact own epoch HEAD/index and declared source authority')
    expected={z['path']:z for z in e['native13_before']};fresh=load(A/'ROOT_FRESH_ACCEPTANCE_INPUT_PREIMAGES.json');mode_by={z['path']:z['worktree_mode'] for z in fresh['files']}
    allowed={'finalize':['draft_pr_publication_program_20260930/inventory.json'],'mirror':['unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl'],'post':[]}[phase]
    for n in allowed:expected[n]=mode_ref(R/n)
    need(type(c['native13_after']) is list and len(c['native13_after'])==13 and {z['path'] for z in c['native13_after']}==set(expected) and all(set(z)=={'path','bytes','sha256','worktree_mode'} and type(z['bytes']) is int and type(z['worktree_mode']) is int and z['worktree_mode']==mode_by[z['path']] and eq(z,expected[z['path']]) for z in c['native13_after']),'Only actual authorized per-phase native bodies; every fullmode exact')
    beforelogs={z['path']:z for z in c['owned_mutable_logs_before']};afterlogs={z['path']:z for z in c['owned_mutable_logs_after']};need(set(beforelogs)==set(afterlogs)==set(OWNED_LOGS) and all(type(z['worktree_mode']) is int for z in list(beforelogs.values())+list(afterlogs.values())),'Exact two typed owned logs')
    if phase=='finalize':
        receipt=load(A/'integration_log_append_receipt.json')
        for z in receipt['logs']:
            n=z['log'];need(eq(z['before'],{k:beforelogs[n][k] for k in ['path','bytes','sha256']}) and eq(z['after'],{k:afterlogs[n][k] for k in ['path','bytes','sha256']}) and type(z['before_worktree_mode']) is int and z['before_worktree_mode']==z['after_worktree_mode']==beforelogs[n]['worktree_mode']==afterlogs[n]['worktree_mode'],'Actual captured two complete owned log appends and fullmodes')
    else:need(eq(beforelogs,afterlogs),'No own log body change in mirror/post')

    for k in ['stdout', 'stderr']:
        z = c[k]; need(z['path'] == k + '.bin', 'Literal new streams'); b = raw(d / z['path']); need(len(b) == z['bytes'] and sha(b) == z['sha256'], 'Whole new streams')
    need(raw(d / 'stderr.bin') == b'' and clock(e['utc']) <= clock(c['prepared_utc']) <= clock(c['started_utc']) <= clock(c['finished_utc']), 'Genuine own-epoch launch chronology')
    return c, e

def validated_prefix(phase, ready_sha, manifest_sha):
    values = pins(); rows = original_prefix(values); last = clock(load(R / rows[-1]['path'])['finished_utc'])
    for prior in PHASES[:PHASES.index(phase)]:
        c, e = phase_capture(prior, ready_sha, manifest_sha); need(last <= clock(e['utc']) <= clock(c['started_utc']), 'Distinct ordered mixed six roles'); last = clock(c['finished_utc']); rows.append(ref(A / ('root_' + prior + '_actual_capture') / 'CAPTURE.json'))
    return rows, last

def author_argv(phase,ready,manifest,review,name,commit,push,outer_directory):
    return ['/usr/bin/python3','-B',str(A/'author_post_push_foreign_epoch_v5.py'),'--execute','--personally-read-complete-source','--source-ready-sha256',ready,'--source-manifest-sha256',manifest,'--phase',phase,'--independent-source-verdict',review['path'],'--independent-source-verdict-sha256',review['sha256'],'--output',name,'--root-commit-capture',commit,'--root-push-capture',push,'--outer-capture-directory',outer_directory]

def closed_packet(ready_sha,manifest_sha):
    v,bodies=packet(ready_sha);p=P/'SOURCE_MANIFEST.json';need(sha(source_read(p,0o444)[0])==manifest_sha,'Exact ROOT-closed source family');m=load(p)
    need(set(m)=={'schema','source_only','self_excluded','files_count','files','file_modes','directory_modes'} and m['schema']=='pr48-post-push-epoch-source-closure/v5' and m['source_only'] is True and m['self_excluded']==['SOURCE_MANIFEST.json'] and type(m['files_count']) is int and m['files_count']==len(m['files']),'Typed SOURCE closure')
    names={safe(z['path']) for z in m['files']};need(len(names)==m['files_count'] and {q.relative_to(P).as_posix() for q in P.rglob('*') if q.is_file()}==names|{'SOURCE_MANIFEST.json'} and {q.relative_to(P).as_posix() for q in P.rglob('*') if q.is_dir()}=={r.as_posix() for n in names for r in PurePosixPath(n).parents if r.as_posix()!='.'} and all(not q.is_symlink() and (q.is_file() or q.is_dir()) for q in P.rglob('*')),'Exact closed SOURCE topology')
    for z in m['files']:
        b=raw(P/z['path']);need(len(b)==z['bytes'] and sha(b)==z['sha256'] and stat.S_IMODE((P/z['path']).stat().st_mode)==0o444,'Whole closed SOURCE body/fullmode')
    need(stat.S_IMODE(p.stat().st_mode)==0o444,'Closed self fullmode');need(eq(m['file_modes'],[dict(path=n,full_mode=0o444) for n in sorted(names|{'SOURCE_MANIFEST.json'})]),'Separate complete closed payload/self mode rows')
    dirs={r.as_posix() for n in names for r in PurePosixPath(n).parents if r.as_posix()!='.'};need(eq(m['directory_modes'],[dict(path=n,full_mode=0o755) for n in sorted(dirs|{'.'})]),'Separate exact source directory0755 rows')
    for n in dirs|{'.'}:directory_binding(P/n)
    rejected_v1_binding();return v,bodies

def caller_argv(phase,ready,manifest,epoch,author_capture,outer_directory):
    return ['/usr/bin/python3','-B',str(A/'run_post_push_foreign_epoch_phase_v5.py'),'--source-ready-sha256',ready,'--source-manifest-sha256',manifest,'--phase',phase,'--foreign-epoch',epoch['path'],'--foreign-epoch-sha256',epoch['sha256'],'--epoch-author-capture',author_capture,'--outer-capture-directory',outer_directory]
