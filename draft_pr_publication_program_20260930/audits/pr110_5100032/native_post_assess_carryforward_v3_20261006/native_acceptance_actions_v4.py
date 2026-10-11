#!/usr/bin/env python3
"""Prepared PR110 actions. Every action requires a fresh, actual root commission.

No action executes at import. Export, acceptance checkpoint, PR readiness, and
exact-tree integration are separate invocations with separate gates/receipts.
Preparation, compile-only checks, and fixtures never authorize a live action.
"""
import sys, os
START_ENV = {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C', 'LANG': 'C', 'TZ': 'UTC'}
if sys.platform == 'darwin':
    START_ENV['__CF_USER_TEXT_ENCODING'] = '0x' + format(os.getuid(), 'X') + ':0x0:0x0'
if __name__ == '__main__' and (dict(os.environ) != START_ENV or not
        (sys.flags.ignore_environment and sys.flags.no_site and sys.flags.dont_write_bytecode
         and getattr(sys.flags, 'safe_path', False))):
    raise SystemExit('Start with the physical pinned Python -E -S -B -P and exact clean environment.')
import base64, configparser, datetime, hashlib, json, pathlib, re, selectors, shutil, signal, stat, subprocess, time

A = pathlib.Path('/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout/draft_pr_publication_program_20260930/audits/pr110_5100032')
C = A.parents[2]
F = A / 'native_post_assess_carryforward_v3_20261006'
ORIGINAL = '3d159f0a00d0bd7ff8d558d6fbc75af5094f7a35'
URL = 'https://github.com/AlecKriebel/Math.git'
PR_URL = 'https://github.com/AlecKriebel/Math/pull/110'
DOI = '10.5281/zenodo.23191247'
RANGE = "'Math Puzzles'!A32:D32"
PREFIX = 'unsolved_math_prioritization/attempts/5100032/'
DERIVED = {'unsolved_math_prioritization/' + x for x in (
    'assessments.json', 'state.json', 'history.jsonl', 'assessment_history.jsonl',
    'catalog.json', 'ranking.csv', 'summary.json', 'QUEUE.md')}
AUTHOR = {'name': 'Alec Kriebel', 'email': 'me@aleckriebel.com'}
SCOPE_CHECKS = {
    'full_actual_candidate_DIFF_and_offer_reviewed',
    'actual_native_PID_resources_and_process_custody_authenticated',
    'all17_originals_and_nonempty_prior_preserved',
    'source_cache_readonly_and_original_2_of_5_no_extra_search_turn',
    'unrelated_scores_order_physical_CSV_history_and_campaign_preserved',
    'accepted_full_mathematical_resolution_and_bounded_priority',
    'actual_publication_tracker_and_clean_whole_package_R1_R2',
    'this_exact_source_and_main_only_exact_tree_integration_reviewed',
}
SPAWN_CRITICAL = False
PENDING_SIGNAL = None

def need(value, message):
    if not value:
        raise RuntimeError(message)

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def timestamp(value):
    t = datetime.datetime.fromisoformat(value)
    need(t.tzinfo is not None, 'UTC timestamp must have a timezone')
    return t.astimezone(datetime.timezone.utc)

def canonical(value):
    return (json.dumps(value, sort_keys=True, ensure_ascii=False, indent=2,
                       allow_nan=False) + '\n').encode()

def pin(body):
    return {'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest()}

def loads(body):
    def pairs(items):
        result = {}
        for key, value in items:
            need(key not in result, 'Duplicate JSON key')
            result[key] = value
        return result
    def invalid(value):
        raise ValueError('Nonfinite JSON value: ' + value)
    return json.loads(body, object_pairs_hook=pairs, parse_constant=invalid)

def relpath(value):
    need(isinstance(value, str), 'Path must be a string')
    p = pathlib.PurePosixPath(value)
    need(value and not p.is_absolute() and '..' not in p.parts and str(p) == value,
         'Canonical nonescaping relative path required')
    return p

def dirfd(path):
    p = pathlib.Path(path)
    need(p.is_absolute() and '..' not in p.parts, 'Canonical absolute directory required')
    fd = os.open('/', os.O_RDONLY | os.O_DIRECTORY)
    try:
        for part in p.parts[1:]:
            nxt = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            os.close(fd)
            fd = nxt
        return fd
    except BaseException:
        os.close(fd)
        raise

def read(path, cap=32*1024*1024, spec=None, retain=True):
    p = pathlib.Path(path)
    fd = dirfd(p.parent)
    child = None
    try:
        child = os.open(p.name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=fd)
        first = os.fstat(child)
        need(stat.S_ISREG(first.st_mode) and first.st_nlink == 1 and first.st_size <= cap,
             'Unique regular bounded input required: ' + str(p))
        h = hashlib.sha256(); count = 0; chunks = []
        while True:
            b = os.read(child, 65536)
            if not b:
                break
            count += len(b); need(count <= cap, 'Input grew beyond cap'); h.update(b)
            if retain:
                chunks.append(b)
        last = os.fstat(child)
        need((first.st_dev, first.st_ino, first.st_size, first.st_mtime_ns) ==
             (last.st_dev, last.st_ino, last.st_size, last.st_mtime_ns), 'Input changed while reading')
        actual = {'bytes': count, 'sha256': h.hexdigest()}
        if spec is not None:
            need(actual == {k: spec[k] for k in ('bytes', 'sha256')}, 'Full input pin mismatch: ' + str(p))
        return b''.join(chunks) if retain else actual
    finally:
        if child is not None:
            os.close(child)
        os.close(fd)

def audit(spec, cap=8*1024*1024):
    need(set(spec) == {'path', 'bytes', 'sha256'}, 'Exact audit pin shape')
    return read(A / relpath(spec['path']), cap, spec)

def mkdirs(path):
    need(path.is_relative_to(C), 'Output outside the dedicated checkout')
    fd = dirfd(C)
    try:
        for part in path.relative_to(C).parts:
            try:
                os.mkdir(part, 0o755, dir_fd=fd)
            except FileExistsError:
                pass
            nxt = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            os.close(fd); fd = nxt
    finally:
        os.close(fd)

def atomic(path, body, expected=None):
    mkdirs(path.parent)
    fd = dirfd(path.parent)
    tmp = path.name + '.pr110-exclusive-tmp'
    created = False
    try:
        if expected is None:
            need(not os.path.lexists(path), 'An absent output appeared: ' + str(path))
        else:
            read(path, spec=expected, retain=False)
        child = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o644, dir_fd=fd)
        created = True
        with os.fdopen(child, 'wb') as stream:
            stream.write(body); stream.flush(); os.fsync(stream.fileno())
        if expected is None:
            os.link(tmp, path.name, src_dir_fd=fd, dst_dir_fd=fd, follow_symlinks=False)
            os.unlink(tmp, dir_fd=fd); created = False
        else:
            read(path, spec=expected, retain=False)
            os.replace(tmp, path.name, src_dir_fd=fd, dst_dir_fd=fd); created = False
        os.fsync(fd)
    finally:
        if created:
            os.unlink(tmp, dir_fd=fd)
        os.close(fd)

def save(path, value):
    previous = read(path) if os.path.lexists(path) else None
    atomic(path, canonical(value), None if previous is None else pin(previous))

def group_absent(pid):
    try:
        os.killpg(pid, 0); return False
    except ProcessLookupError:
        return True
    except PermissionError:
        return False

class Capture:
    """Actual bounded capture, including failures and descendant cleanup.

    Full streams are retained on successful bounded operations. Oversize or
    failed-drain operations are honestly labelled partial. Each launch is
    journaled before waiting so an independent outer supervisor can clean up.
    """
    def __init__(self, root, whole_seconds=300):
        need(not os.path.lexists(root), 'Unique action record directory required')
        mkdirs(root); self.root = root; self.records = []; self.launches = []
        self.begin = time.monotonic(); self.whole_seconds = whole_seconds; self.active = None

    def journal(self):
        save(self.root/'PROCESS_JOURNAL.json', {'actual_operator_PID': os.getpid(), 'records': self.records})
        save(self.root/'PROCESS_LAUNCHES.json', {'actual_operator_PID': os.getpid(), 'launches': self.launches})

    def run(self, argv, cwd, env, deadline=30, stdout_cap=32*1024*1024, allow_failure=False,
            stdout_retention_cap=None, immutable_git_body_source=None):
        global SPAWN_CRITICAL, PENDING_SIGNAL
        need(len(self.records) < 512 and time.monotonic()-self.begin < self.whole_seconds,
             'Action process count or overall deadline')
        limit = min(deadline, self.whole_seconds-(time.monotonic()-self.begin))
        need(limit > 0 and isinstance(argv, list) and all(isinstance(x, str) for x in argv), 'Explicit argv/deadline')
        began = now(); mono = time.monotonic(); p = None; sel = None
        counts = {'stdout': 0, 'stderr': 0}; hashes = {k: hashlib.sha256() for k in counts}
        buffers = {k: bytearray() for k in counts}; caps = {'stdout': stdout_cap, 'stderr': 65536}
        reason = None; stopped = None; killed = False; drained = False; reaped = False; error = None
        def terminate(why):
            nonlocal reason, stopped
            if reason is None:
                reason = why; stopped = time.monotonic()
                try: os.killpg(p.pid, signal.SIGTERM)
                except ProcessLookupError: pass
        try:
            SPAWN_CRITICAL = True
            try:
                p = subprocess.Popen(argv, cwd=cwd, env=env, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE, start_new_session=True)
                self.active = p
                self.launches.append({'PID': p.pid, 'argv': argv, 'cwd': str(cwd),
                    'environment_sha256': pin(canonical(env))['sha256'], 'UTC_start': began,
                    'state': 'launched_not_yet_reaped'})
                self.journal()
            finally:
                SPAWN_CRITICAL = False
            if PENDING_SIGNAL is not None:
                s=PENDING_SIGNAL;PENDING_SIGNAL=None
                raise SystemExit('Deferred operator '+signal.Signals(s).name)
            sel = selectors.DefaultSelector()
            for k, s in [('stdout',p.stdout),('stderr',p.stderr)]:
                os.set_blocking(s.fileno(), False); sel.register(s, selectors.EVENT_READ, k)
            while sel.get_map() or p.poll() is None:
                if time.monotonic()-mono >= limit: terminate('deadline')
                if stopped is not None and time.monotonic()-stopped >= 1 and not killed:
                    try: os.killpg(p.pid, signal.SIGKILL)
                    except ProcessLookupError: pass
                    killed = True
                for key, _ in sel.select(0.1):
                    b = os.read(key.fileobj.fileno(), 65536)
                    if not b: sel.unregister(key.fileobj); continue
                    k=key.data; counts[k]+=len(b); hashes[k].update(b)
                    room=max(0,caps[k]-len(buffers[k])); buffers[k].extend(b[:room])
                    if counts[k] > caps[k]: terminate(k+'_cap')
                if stopped is not None and time.monotonic()-stopped > 4:
                    reason += '+drain_deadline'; break
            drained = not sel.get_map()
        except BaseException as e:
            error = type(e).__name__ + ': ' + str(e)[:240]
            if p is not None:
                try: terminate('operator_exception')
                except PermissionError: reason = 'cleanup_permission_denied'
        finally:
            if p is not None:
                if p.poll() is None or not group_absent(p.pid):
                    try: os.killpg(p.pid, signal.SIGKILL)
                    except ProcessLookupError: pass
                    except PermissionError: reason = (reason or '')+'+cleanup_permission_denied'
                try: p.wait(timeout=3); reaped=True
                except subprocess.TimeoutExpired: reason=(reason or '')+'+reap_deadline'
                if sel is not None:
                    sel.close()
                p.stdout.close(); p.stderr.close()
                absent=group_absent(p.pid)
                if not absent: reason=(reason or '')+'+group_absence_unconfirmed'
                i=len(self.records); streams={}
                for k in counts:
                    retained=bytes(buffers[k])
                    if k=='stdout' and stdout_retention_cap is not None:retained=retained[:stdout_retention_cap]
                    filename=str(i)+'.'+k+'.bin'; atomic(self.root/filename,retained)
                    streams[k]={'observed':{'bytes':counts[k],'sha256':hashes[k].hexdigest()},
                        'retained_file':filename,'retained':pin(retained),
                        'full':drained and counts[k]==len(retained)}
                    if k=='stdout' and immutable_git_body_source is not None:
                        streams[k]['complete_body_retained_in_immutable_Git']=immutable_git_body_source
                record={'argv':argv,'cwd':str(cwd),'environment_sha256':pin(canonical(env))['sha256'],
                    'actual_PID':p.pid,'UTC_start':began,'UTC_end':now(),'exit_code':p.returncode,
                    'reaped':reaped,'process_group_absence_confirmed':absent,
                    'fully_drained':drained,'termination_reason':reason,'error':error,'streams':streams}
                self.records.append(record); self.launches[-1]['state']='reaped' if reaped else 'reap_unconfirmed'
                self.journal(); self.active=None
        need(p is not None and reaped and record['process_group_absence_confirmed'] and drained
             and reason is None and error is None, 'Actual child failed a bound or cleanup; record retained')
        need(allow_failure or p.returncode==0, 'Actual child failed; full failure streams retained')
        return bytes(buffers['stdout'])

def validate_runtime(runtime):
    need(runtime['pin_scope']=='fresh_current_preflight_only' and runtime['historical_binary_bytes_attested'] is False,
         'Current pins cannot attest historical executable bytes')
    need(runtime['python_environment']==START_ENV, 'Exact initial clean environment')
    need(runtime['binaries']['python']['resolved_absolute_path']==sys.executable, 'Physical pinned Python startup')
    for spec in runtime['binaries'].values():
        physical=pathlib.Path(spec['resolved_absolute_path'])
        need(pathlib.Path(spec['invocation_path']).resolve(strict=True)==physical, 'Invocation resolution drift')
        for link in spec['symlink_chain']:
            need(os.readlink(link['path'])==link['target'] and
                 pin(link['target'].encode())['sha256']==link['target_utf8_sha256'], 'Invocation link drift')
        read(physical,64*1024*1024,spec,retain=False)
    for spec in runtime['dependency_files'].values():
        read(spec['absolute_path'],64*1024*1024,spec,retain=False)
    fd=dirfd(C/'.git');os.close(fd)
    need(not os.path.lexists(C/'.git/commondir'), 'Direct independent Git admin directory required')
    ghdir=pathlib.Path(runtime['gh_config_directory']);fd=dirfd(ghdir);os.close(fd)
    required={(str(C/'.git/config'),'git')}
    if os.path.lexists(C/'.git/config.worktree'): required.add((str(C/'.git/config.worktree'),'git'))
    for item in os.scandir(ghdir):
        need(item.name in {'config.yml','hosts.yml','state.yml'} and item.is_file(follow_symlinks=False), 'Unreviewed GH config entry')
        required.add((str(ghdir/item.name),'gh'))
    actual=set()
    for spec in runtime['private_configuration_pins']:
        identity=(spec['absolute_path'],spec['role']);need(identity in required and identity not in actual and spec['body_private'] is True,'Private configuration coverage')
        actual.add(identity);body=read(spec['absolute_path'],128*1024,spec)
        if spec['role']=='git':
            parser=configparser.RawConfigParser();parser.read_string(body.decode())
            for section in parser.sections():
                need(not section.lower().startswith(('include','alias','url ','filter ','diff ','credential')), 'Unreviewed local Git execution/rewrite')
                for k in parser[section]:need(k.lower() not in {'sshcommand','pager','editor','proxy','promisor','partialclonefilter'},'Unreviewed Git runtime command')
        elif pathlib.Path(spec['absolute_path']).name=='config.yml':
            # Only the same conservative plain subset allowed by the commissioned runner.
            seen=set();aliases=False
            for line in body.decode().splitlines():
                if not line.strip() or line.lstrip().startswith('#'):continue
                if line.startswith(' '):
                    need(aliases and line=='    co: pr checkout' and 'alias:co' not in seen,'Unreviewed GH alias');seen.add('alias:co');continue
                need(':' in line and not line.startswith(('\t','-','!','&','*')),'GH plain mapping')
                k,v=line.split(':',1);v=v.strip();need(k not in seen,'Duplicate GH config');seen.add(k);aliases=k=='aliases'
                choices={'git_protocol':{'https'},'editor':{'','null','~'},'pager':{'','null','~'},'browser':{'','null','~'},
                    'http_unix_socket':{'','null','~'},'prompt':{'enabled','disabled'},'prefer_editor':{'enabled','disabled'},
                    'aliases':{'','{}'},'version':{'1','"1"',"'1'"}}
                need(k in choices and v in choices[k],'Unreviewed GH config value')
    need(actual==required and (str(ghdir/'hosts.yml'),'gh') in required, 'All effective local Git/GH private pins required')

def git_env(runtime, authenticated=False):
    env={**START_ENV,'GIT_CONFIG_NOSYSTEM':'1','GIT_CONFIG_GLOBAL':'/dev/null','GIT_CONFIG_SYSTEM':'/dev/null',
         'GIT_OPTIONAL_LOCKS':'0','GIT_NO_REPLACE_OBJECTS':'1','GIT_TERMINAL_PROMPT':'0'}
    if authenticated:env.update(gh_env(runtime))
    return env

def gh_env(runtime):
    return {**START_ENV,'GH_CONFIG_DIR':runtime['gh_config_directory'],'GH_HOST':'github.com','GH_PROMPT_DISABLED':'1',
        'GH_PAGER':'','GH_BROWSER':'/usr/bin/false','GH_EDITOR':'/usr/bin/false','GH_NO_UPDATE_NOTIFIER':'1'}

def git(capture, runtime, *args, authenticated=False, deadline=30, allow_failure=False):
    argv=[runtime['binaries']['git']['resolved_absolute_path'],'-c','core.fsmonitor=false','-c','core.hooksPath=/dev/null',
          '-c','credential.helper=','-c','commit.gpgsign=false','-c','gc.auto=0']
    if authenticated:
        gh=runtime['binaries']['gh']['resolved_absolute_path']
        need(re.fullmatch(r'/[A-Za-z0-9_./@+\-]+',gh), 'Safe declared physical GH credential helper')
        argv+=['-c','credential.helper='+gh+' auth git-credential']
    # The exact committed body already remains in immutable Git; retain its
    # honest stream SHA/count and only a labelled prefix, avoiding duplicate
    # large native catalog snapshots. Dynamic outputs retain their full bodies.
    source=args[1] if len(args)==2 and args[0]=='show' and ':' in args[1] else None
    return capture.run(argv+list(args),C,git_env(runtime,authenticated),deadline=deadline,allow_failure=allow_failure,
        stdout_retention_cap=4096 if source is not None else None,immutable_git_body_source=source)

def gh(capture,runtime,*args):
    return capture.run([runtime['binaries']['gh']['resolved_absolute_path'],*args],C,gh_env(runtime),deadline=60,stdout_cap=1024*1024)

def main_preflight(capture,runtime,parent):
    need(git(capture,runtime,'symbolic-ref','--short','HEAD').strip()==b'main','Stay on main')
    need(git(capture,runtime,'rev-parse','HEAD').decode().strip()==parent,'Own main changed')
    remote=git(capture,runtime,'ls-remote',URL,'refs/heads/main').decode().split()
    need(remote==[parent,'refs/heads/main'],'Remote main changed')
    need(not git(capture,runtime,'diff','--cached','--name-only','-z'),'Foreign staged entries')
    need(git(capture,runtime,'write-tree').strip()==git(capture,runtime,'rev-parse','HEAD^{tree}').strip(),
         'Complete index must equal current main tree')

def live_pr(capture,runtime,state='OPEN',draft=None,body=None,title=None):
    obj=loads(gh(capture,runtime,'pr','view',PR_URL,'--json','number,state,isDraft,headRefOid,headRefName,baseRefName,title,body,mergeCommit,mergedAt,url'))
    need(obj['number']==110 and obj['state']==state and obj['headRefOid']==ORIGINAL and
         obj['headRefName']=='dot/math-5100032' and obj['baseRefName']=='main','Original PR identity/state drift')
    if draft is not None:need(obj['isDraft'] is draft,'Original PR draft/readiness drift')
    if body is not None:need(obj['body']==body,'Actual PR description readback differs')
    if title is not None:need(obj['title']==title,'Actual PR title readback differs')
    return obj


HISTORICAL_MAIN = 'f9f840d21305bdc353d151abe8dd5c51b6a27dd6'
INTEGRATION_MAIN = 'e0a94b93520610553c001f265f210f959b591c2c'

def validate_integration_inputs(spec, original_packet):
    raw=audit(spec);item=loads(raw)
    need(item['schema']=='pr110-current-main-carryforward-inputs/v1'
         and item['actual_receipt'] is True and item['template_only'] is False
         and item.get('fixture',False) is False and item.get('simulated',False) is False,
         'Actual current-main carryforward inputs')
    timestamp(item['UTC'])
    need(item['original_assessed_main_parent']==HISTORICAL_MAIN
         and original_packet['main_parent']==HISTORICAL_MAIN
         and item['main_parent']==item['remote_main']==INTEGRATION_MAIN and item['branch']=='main'
         and item['original_packet_sha256']=='d9eb646c1dd70e891cc44bcaa5de2b62fc0c5a6eabdf2d487a148c3d3cc02281',
         'Explicit historical assessment/current integration distinction')
    need(item['original_worker_not_reassessed'] is True,'Carryforward does not claim a reassessment')
    flags=['all12_current_native_fullbodies_authenticated','eleven_non_QUEUE_native_files_identical',
        'exactly_one_unrelated_QUEUE_row_changed','target_QUEUE_row_unchanged',
        'original_target_source_prior_original17_unchanged','science_priority_publication_tracker_unchanged',
        'main_and_remote_current_verified']
    need(all(item[k] is True for k in flags),'Root actual carryforward full-custody decisions')
    current=item['native_baseline'];old=original_packet['native_baseline']
    need(set(current)==set(old) and len(current)==12,'Full current native baseline')
    for name,pinned in current.items():
        need(set(pinned)=={'path','bytes','sha256'} and pinned['path']==old[name]['path'],
             'Current native baseline canonical path')
        if name!='QUEUE.md':need(pinned==old[name],'Exactly eleven native files remain byte-identical')
    q0=audit(item['original_QUEUE_pin']);q1=audit(item['current_QUEUE_pin'])
    need(pin(q0)=={k:old['QUEUE.md'][k] for k in ('bytes','sha256')}
         and pin(q1)=={k:current['QUEUE.md'][k] for k in ('bytes','sha256')},'Actual historical/current full QUEUE pins')
    before=q0.decode().splitlines(keepends=True);after=q1.decode().splitlines(keepends=True)
    need(len(before)==len(after),'Only a physical row replacement is allowed')
    changed=[i for i,(x,y) in enumerate(zip(before,after)) if x!=y]
    need(len(changed)==1 and item['unrelated_QUEUE_id']=='30005460','Exactly the reviewed unrelated row changes')
    i=changed[0]
    for row in [before[i],after[i]]:
        cells=row.rstrip('\r\n').split('|')
        need(len(cells)==14 and cells[2].strip().split(' / ')[0]=='30005460',
             'Changed physical QUEUE row belongs only to unrelated target')
    need(type(item['changed_physical_row_number']) is int and item['changed_physical_row_number']==i+1
         and before[i].encode()==audit(item['changed_physical_row_before_pin'])
         and after[i].encode()==audit(item['changed_physical_row_after_pin']),'Full changed physical row custody')
    targets=[x for x in before if x.startswith('| ') and x.split('|')[2].strip().startswith('5100032 / ')]
    need(len(targets)==1 and targets==[x for x in after if x.startswith('| ') and x.split('|')[2].strip().startswith('5100032 / ')],
         'Original target QUEUE row unchanged')
    delta=audit(item['Git_delta_pin']);parts=delta.split(b'\0');need(parts[-1]==b'' and len(parts[:-1])%2==0,'Complete name-status NUL delta')
    pairs=[(parts[j].decode(),parts[j+1].decode()) for j in range(0,len(parts)-1,2)]
    need(len(pairs)==64 and len({p for _,p in pairs})==64,'Exactly64 unique changed Git paths')
    need([p for st,p in pairs if st=='M']==['unsolved_math_prioritization/QUEUE.md']
         and sum(st=='A' for st,p in pairs)==63
         and all((st=='M' and p=='unsolved_math_prioritization/QUEUE.md') or
                 (st=='A' and p.startswith('unsolved_math_prioritization/attempts/30005460/')) for st,p in pairs),
         'Only one QUEUE modification and63 unrelated target additions')
    declared=[(x['status'],x['path']) for x in item['changed_paths']]
    need(sorted(pairs)==sorted(declared),'Actual delta matches declared full status/path set')
    for bodypin in item['checked_artifacts']:audit(bodypin)
    return item,q0,q1,delta

def verify_stopped_continuation(spec):
    item=loads(audit(spec));root=A/'native_post_assess_continuation_v1_20261006/workspaces/candidate_d9eb646c1dd70e89'
    need(item['schema']=='pr110-preserved-main-advance-stop-inventory/v1' and item['source_workspace']==str(root)
         and item['actual_stopped_continuation_PID']==43487 and item['file_count']==10,
         'Preserved exact main-advance stop')
    names=set()
    for entry in item['files']:
        relpath(entry['path']);need(entry['path'] not in names,'Unique stopped member');names.add(entry['path'])
        read(root/entry['path'],128*1024,entry,retain=False)
    actual=set()
    for path in root.rglob('*'):
        st=path.lstat();need(stat.S_ISDIR(st.st_mode) or (stat.S_ISREG(st.st_mode) and st.st_nlink==1),'Safe stopped member')
        if stat.S_ISREG(st.st_mode):actual.add(str(path.relative_to(root)))
    need(actual==names and not os.path.lexists(root/'offer') and not os.path.lexists(root/'CANDIDATE_RECEIPT.json'),
         'Stopped continuation remains untouched and nonexportable')
    failure=loads(read(root/'FAILURE.json'))
    need(failure['operator_PID']==43487 and failure['error']=='Remote main changed'
         and failure['reassessment_executed'] is False and failure['native_export_executed'] is False,
         'Actual original main-advance failure preserved')
    return item

def verify_stopped_CPU_continuation(spec):
    item=loads(audit(spec));root=A/'native_post_assess_carryforward_v2_20261006/workspaces/candidate_d9eb646c1dd70e89'
    need(A/relpath(spec['path'])==F/'STOPPED_CPU_CONTINUATION_INVENTORY.json'
         and item['schema']=='pr110-preserved-CPU-limit-stop-inventory/v1'
         and item['source_workspace']==str(root) and item['actual_stopped_continuation_PID']==59213
         and item['actual_outer_operator_PID']==59205 and item['file_count']==129 and item['offer_count']==84
         and item['original_packet_sha256']=='d9eb646c1dd70e891cc44bcaa5de2b62fc0c5a6eabdf2d487a148c3d3cc02281',
         'Exact previous CPU-stop custody')
    names=set();total=0
    for entry in item['files']:
        relpath(entry['path']);need(entry['path'] not in names,'Unique CPU-stop member');names.add(entry['path'])
        measured=read(root/entry['path'],32*1024*1024,entry,retain=False);total+=measured['bytes']
    actual=set()
    for path in root.rglob('*'):
        st=path.lstat();need(stat.S_ISDIR(st.st_mode) or (stat.S_ISREG(st.st_mode) and st.st_nlink==1),'Safe CPU-stop member')
        if stat.S_ISREG(st.st_mode):actual.add(str(path.relative_to(root)))
    need(actual==names and total==item['total_bytes'] and sum(x.startswith('offer/') for x in names)==84
         and all(not os.path.lexists(root/n) for n in ['FAILURE.json','DIFF.txt','CANDIDATE_RECEIPT.json']),
         'All129 stopped bodies unchanged and incomplete')
    need(item['partial_offer_must_not_be_exported'] is True and item['failure_receipt_invented'] is False
         and item['DIFF_present'] is False and item['candidate_receipt_present'] is False and item['FAILURE_present'] is False
         and type(item['native_assess_calls_during_stopped_continuation']) is int
         and item['native_assess_calls_during_stopped_continuation']==0 and item['live_export_executed'] is False,
         'No fabricated failure or completed candidate')
    for entry in item['checked_artifacts']:audit(entry)
    outer=loads(audit(item['outer_execution_pin']));launcher=audit(item['outer_launcher_source_pin'],128*1024)
    need(outer['schema']=='pr110-actual-bounded-native-carryforward-launch/v1'
         and outer['child_PID']==59213 and outer['actual_operator_PID']==59205 and outer['exit_code']==-24
         and outer['reaped'] is True and outer['streams_fully_drained'] is True
         and outer['all_recorded_groups_absence_confirmed'] is True and outer['cleanup_errors']==[]
         and outer['whole_launch_deadline_seconds']==300 and outer['actual_continuation_custody_path']==str(root)
         and outer['outer_source_pin']==pin(launcher),'Actual CPU signal/reap/bounded outer custody')
    journal=loads(read(root/'PROCESS_JOURNAL.json'))
    need(journal['actual_operator_PID']==59213 and len(journal['records'])==21
         and all(x['exit_code']==0 and x['reaped'] is True and x['fully_drained'] is True
                 and x['process_group_absence_confirmed'] is True and x['cwd']==str(C)
                 for x in journal['records']),'Previous21 readonly children complete')
    return item

def load_gate(path,action):
    raw=read(path,512*1024);gate=loads(raw)
    need(path.is_relative_to(A) and raw==canonical(gate),'Canonical root gate inside this effort')
    need(gate['schema']=='pr110-native-action-commission/v1' and gate['action']==action and gate['role']=='root'
         and gate['actual_review'] is True and gate['clearance'] is True and gate['required_findings']==[]
         and all(gate[k] is False for k in ('template_only','fixture','simulated')),'Actual fresh root action clearance')
    need(datetime.timedelta(0)<=timestamp(now())-timestamp(gate['UTC'])<=datetime.timedelta(minutes=30),'Fresh action commission')
    need(gate['original_head']==ORIGINAL and gate['DOI']==DOI and gate['tracker_range']==RANGE,'Publication/original identity')
    need(set(gate['scope_checks'])==SCOPE_CHECKS and all(x is True for x in gate['scope_checks'].values()),'Full actual root scope review')
    need(A/relpath(gate['program_pin']['path'])==pathlib.Path(__file__) and audit(gate['program_pin'],128*1024)==read(__file__,128*1024),'Exact reviewed executing action source')
    packet_raw=audit(gate['packet_pin']);packet=loads(packet_raw)
    need(packet['schema']=='pr110-concrete-native-inputs/v1' and packet['template_only'] is False and
         pin(packet_raw)['sha256']==gate['packet_sha256'],'Exact actual native packet')
    runtime=packet['runtime'];validate_runtime(runtime)
    integration,_,_,_=validate_integration_inputs(gate['integration_inputs_pin'],packet)
    original_packet=packet
    # Only this in-memory integration view changes. The original packet bytes
    # and successful worker control continue to bind the historical assessment.
    packet={**original_packet,'main_parent':integration['main_parent'],'native_baseline':integration['native_baseline']}
    ad_raw=audit(gate['candidate_adversary_pin']);ad=loads(ad_raw)
    need(ad['schema']=='pr110-actual-native-candidate-adversary/v1' and ad['actual_review'] is True and
         ad['clearance'] is True and ad['required_findings']==[] and ad['packet_sha256']==gate['packet_sha256']
         and ad['candidate_receipt_pin']==gate['candidate_receipt_pin'] and ad['action_program_pin']==gate['program_pin']
         and ad['template_only'] is False and ad.get('fixture',False) is False and ad.get('simulated',False) is False
         and timestamp(ad['UTC'])<=timestamp(gate['UTC']),'Actual candidate adversary bound to candidate and execution source')
    W=pathlib.Path(gate['candidate']);need(W.parent==F/'workspaces'
        and W.name=='candidate_'+gate['packet_sha256'][:16],'Exact exclusive candidate directory')
    need(not os.path.lexists(W/'FAILURE.json'),'Continued candidate must have no failure receipt')
    receipt_raw=read(W/'CANDIDATE_RECEIPT.json',128*1024,gate['candidate_receipt_pin']);r=loads(receipt_raw)
    need(r['schema']=='pr110-actual-post-assess-carryforward-candidate/v1' and r['packet_sha256']==gate['packet_sha256']
         and r['main_parent']==packet['main_parent'] and r['original_head']==ORIGINAL and r['native_export_executed'] is False
         and r['native_status']=='claimed_solved' and r['turns_used']==2 and r['new_central_proof_search_turns']==0
         and r['nonempty_prior_preserved'] is True and r['Git_mutations']==0 and r['service_writes']==0,'Actual private candidate facts')
    need(r['DIFF_pin']==gate['DIFF_pin'],'Actual reviewed complete DIFF binding');read(W/'DIFF.txt',1024*1024,gate['DIFF_pin'],retain=False)
    need(r['original_assessed_main_parent']==HISTORICAL_MAIN and r['main_parent']==INTEGRATION_MAIN
         and r['integration_inputs_pin']==gate['integration_inputs_pin']
         and ad['integration_inputs_pin']==gate['integration_inputs_pin'],
         'Actual carryforward integration inputs bound by candidate/adversary/root')
    verify_stopped_continuation(r['stopped_continuation_inventory_pin'])
    need(gate['stopped_CPU_continuation_inventory_pin']==r['stopped_CPU_continuation_inventory_pin']
         and ad['stopped_CPU_continuation_inventory_pin']==r['stopped_CPU_continuation_inventory_pin'],
         'CPU-stop inventory bound by candidate/adversary/root')
    verify_stopped_CPU_continuation(r['stopped_CPU_continuation_inventory_pin'])
    need(gate['linear_diff_program_pin']==r['linear_diff_program_pin']
         and ad['linear_diff_program_pin']==r['linear_diff_program_pin']
         and A/relpath(r['linear_diff_program_pin']['path'])==F/'linear_full_diff.py',
         'Exact linear DIFF source bound by candidate/adversary/root')
    audit(r['linear_diff_program_pin'],128*1024)
    need(r['diff_algorithm']=='linear-single-replacement-hunk-with-three-context-lines'
         and r['original_resource_policy_unchanged'] is True
         and r['parent_limits']['requested']==original_packet['resources']
         and r['parent_limits']['enforced']=={
             'RLIMIT_CPU':[original_packet['resources']['cpu_seconds']]*2,
             'RLIMIT_FSIZE':[original_packet['resources']['file_size_bytes']]*2,
             'RLIMIT_NOFILE':[original_packet['resources']['open_files']]*2},
         'Original worker/continuation resource policy remains unchanged')
    need(type(r['native_assess_calls_during_continuation']) is int and r['native_assess_calls_during_continuation']==0
         and r['holds_cleared'] is False and r['successful_existing_worker_PID']==23360
         and r['native_assess_actual_PID']==23360 and r['failed_original_operator_PID']==23224
         and r['source_workspace']==str(A/'native_execution_programs_v1/workspaces/candidate_d9eb646c1dd70e89')
         and r['empty_clear_holds_generated_metadata_only'] is True
         and r['original_failure_preserved'] is True,'Explicit no-reassessment continuation provenance')
    need(gate['continuation_program_pin']==r['continuation_program_pin']
         and ad['continuation_program_pin']==r['continuation_program_pin'],'Continuation source bound by root and actual candidate adversary')
    audit(r['continuation_program_pin'],128*1024)
    seed=loads(audit(r['seed_inventory_pin']))
    need(seed['schema']=='pr110-failed-successful-worker-seed-inventory/v1'
         and seed['source_workspace']==r['source_workspace'] and seed['file_count']==61
         and seed['original_packet_sha256']==gate['packet_sha256'],'Exact failed workspace seed inventory')
    names=set()
    for entry in seed['files']:
        relpath(entry['path']);need(entry['path'] not in names,'Duplicate preserved seed path');names.add(entry['path'])
        read(pathlib.Path(seed['source_workspace'])/entry['path'],32*1024*1024,entry,retain=False)
    actual=set()
    for path in pathlib.Path(seed['source_workspace']).rglob('*'):
        s=path.lstat()
        need(stat.S_ISDIR(s.st_mode) or (stat.S_ISREG(s.st_mode) and s.st_nlink==1),'Unsafe preserved seed member')
        if stat.S_ISREG(s.st_mode):actual.add(str(path.relative_to(seed['source_workspace'])))
    need(actual==names and len(names)==61,'Full failed workspace inventory preserved')
    oldfail=loads(read(pathlib.Path(seed['source_workspace'])/'FAILURE.json',65536,r['source_failure_pin']))
    need(oldfail['operator_PID']==23224 and oldfail['error']=='Target assessment changed beyond reviewed metadata'
         and oldfail['candidate_must_not_be_exported'] is True,'Original failure stays authentic and nonexportable')
    failed_auth=loads(audit(r['failed_run_root_authentication_pin']))
    need(failed_auth['schema']=='pr110-root-failed-native-run-authentication/v1'
         and failed_auth['actual_worker_PID']==23360 and failed_auth['actual_assess_once_success_authenticated'] is True
         and failed_auth['target_delta_only_reviewed_at_and_empty_clear_holds'] is True
         and failed_auth['all12_actual_output_fullbodies_authenticated'] is True
         and failed_auth['all17_children_reaped_and_groups_absent'] is True,'Root actual failed-run custody prerequisite')
    for entry in failed_auth['checked_artifacts']:audit(entry)
    for spec in packet['input_files']:audit(spec)
    auth=loads(read(A/'ROOT_ACTUAL_PUBLICATION_TRACKER_AUTHENTICATION_20261006.json'))
    need(auth['DOI']==DOI and auth['range']==RANGE and auth['publication_fullbody_and_all33_logical_members'] is True
         and auth['actual_GWS_append_and_two_readbacks'] is True,'Actual service authentication')
    return gate,packet,runtime,W,r,pin(raw)

def verify_offer(W,r,packet,capture,runtime,parent):
    rows=r['affected_paths'];need(1<=len(rows)<=256 and len({x['path'] for x in rows})==len(rows),'Unique bounded offer destinations')
    expected=set();size=0
    for row in rows:
        name=row['path'];relpath(name);need(name in DERIVED or name.startswith(PREFIX),'Exact native target/eight-global scope')
        need(name!=PREFIX+'NATIVE_ACCEPTANCE_RECEIPT.json','Generated export receipt cannot collide with private offer')
        body=read(W/'offer'/name,32*1024*1024,row['after']);size+=len(body);need(size<=160*1024*1024,'Bounded full offered bodies')
        expected.add(name)
        if name in DERIVED:
            base=packet['native_baseline'][pathlib.PurePosixPath(name).name]
            need(row['before']=={k:base[k] for k in ('bytes','sha256')},'Exact native derived preimage pin')
            need(pin(git(capture,runtime,'show',parent+':'+name))==row['before'],'Committed native preimage drift')
            if os.path.lexists(C/name):read(C/name,spec=row['before'],retain=False)
        else:need(row['before'] is None,'New target attempt only')
    found=set()
    def walk(path):
        for e in os.scandir(path):
            s=e.stat(follow_symlinks=False);p=pathlib.Path(e.path)
            if stat.S_ISDIR(s.st_mode):walk(p)
            else:
                need(stat.S_ISREG(s.st_mode) and s.st_nlink==1,'Unsafe unreviewed offer member')
                found.add(str(p.relative_to(W/'offer')))
                need(len(found)<=256,'Offer file count')
    fd=dirfd(W/'offer');os.close(fd);walk(W/'offer');need(found==expected,'Full offer inventory must equal reviewed receipt')
    byname={x['path']:x for x in rows}
    for name,spec in packet['attempt_offer_sources'].items():
        need(name in byname and byname[name]['after']=={k:spec[k] for k in ('bytes','sha256')},
             'Every declared source offer equals its authenticated packet input')
    original=loads(read(A/'original_head_authentication_20261006/ORIGINAL_BLOB_MANIFEST.json'))
    need(original['original_head']==ORIGINAL and len(original['files'])==17,'Original seventeen-file manifest')
    for x in original['files']:
        name=PREFIX+'historical_original/'+x['relative_path'];need(name in found,'Original historical member missing')
        read(W/'offer'/name,spec=x,retain=False)
    for n in ('source_record.json','prior_imported_report.json'):
        x=next(x for x in original['files'] if x['relative_path']==n)
        read(W/'offer'/PREFIX/n,spec=x,retain=False)
    prior=loads(read(W/'offer'/PREFIX/'prior_imported_report.json'))
    need(bool(prior),'Nonempty imported prior cannot be replaced')
    return rows,size

def export_action(gate,packet,runtime,W,r,capture):
    parent=packet['main_parent'];need(gate['main_parent']==parent,'Actual candidate parent')
    main_preflight(capture,runtime,parent);live_pr(capture,runtime,draft=True)
    need(not os.path.lexists(C/PREFIX),'Attempt absent before authorized export')
    need(not git(capture,runtime,'ls-tree','-r','--name-only',parent,'--',PREFIX),'Target absent from current main')
    cache=packet['source_cache'];read(cache['absolute_path'],256*1024*1024,cache['pin'],retain=False)
    for suffix in ('-wal','-shm','-journal'):
        need(not os.path.lexists(cache['absolute_path']+suffix),'Shared SQL sidecar appeared')
    for name,spec in packet['raw_source_pins'].items():
        read(pathlib.Path('/Users/alec/Documents/Math/unsolved_math_prioritization/cache')/name,
             128*1024*1024,spec,retain=False)
    # Check every native input, even those absent from the sparse physical checkout.
    for name,spec in packet['native_baseline'].items():
        need(pin(git(capture,runtime,'show',parent+':'+spec['path']))=={k:spec[k] for k in ('bytes','sha256')},'All native baseline bodies unchanged')
        if os.path.lexists(C/spec['path']):read(C/spec['path'],spec=spec,retain=False)
    rows,size=verify_offer(W,r,packet,capture,runtime,parent)
    need(shutil.disk_usage(C).free>=size+64*1024*1024,'Export space/reserve')
    save(capture.root/'PRE_EXPORT.json',{'UTC':now(),'main_parent':parent,'packet_sha256':gate['packet_sha256'],
         'candidate_receipt_pin':gate['candidate_receipt_pin'],'all_offer_and_native_preimages_checked':True,'exported':False})
    copied=[];started=now()
    for row in rows:
        destination=C/row['path'];body=read(W/'offer'/row['path'],spec=row['after'])
        physical_before=row['before'] if os.path.lexists(destination) else None
        atomic(destination,body,physical_before);read(destination,spec=row['after'],retain=False)
        copied.append(row);save(capture.root/'EXPORT_PROGRESS.json',{'UTC':now(),'actual_operator_PID':os.getpid(),
             'copied':copied,'export_incomplete':len(copied)!=len(rows),'main_parent':parent})
    result={'schema':'pr110-actual-reviewed-native-export/v2','actual_operator_PID':os.getpid(),'UTC_start':started,'UTC_end':now(),
        'main_parent':parent,'original_PR_head':ORIGINAL,'packet_sha256':gate['packet_sha256'],'candidate':str(W),
        'candidate_receipt_pin':gate['candidate_receipt_pin'],'DIFF_pin':gate['DIFF_pin'],'exported_paths':rows,
        'native_export_executed':True,'all_exported_full_bytes_checked':True,'original_status':'claimed_solved','original_budget':'2/5',
        'new_central_proof_search_turns':0,'nonempty_prior_preserved':True,'DOI':DOI,'tracker_range':RANGE,
        'additional_actual_target_receipt':PREFIX+'NATIVE_ACCEPTANCE_RECEIPT.json',
        'Git_staging_executed':False,'merge_executed':False,'actual_process_journal':str(capture.root/'PROCESS_JOURNAL.json')}
    body=canonical(result);atomic(C/result['additional_actual_target_receipt'],body)
    read(C/result['additional_actual_target_receipt'],spec=pin(body),retain=False)
    save(capture.root/'RECEIPT.json',result);return result

def acceptance_commit(gate,packet,runtime,W,r,capture):
    parent=packet['main_parent'];need(gate['main_parent']==parent and gate['commit_identity']==AUTHOR,'Accepted main parent and explicit author')
    main_preflight(capture,runtime,parent);live_pr(capture,runtime,draft=True)
    exported=loads(audit(gate['export_receipt_pin']))
    need(exported['schema']=='pr110-actual-reviewed-native-export/v2' and exported['native_export_executed'] is True
         and exported['main_parent']==parent and exported['candidate_receipt_pin']==gate['candidate_receipt_pin']
         and exported['exported_paths']==r['affected_paths'],'Exact actual export receipt')
    paths={x['path']:x['after'] for x in r['affected_paths']}
    extra=PREFIX+'NATIVE_ACCEPTANCE_RECEIPT.json';body=audit(gate['export_receipt_pin']);paths[extra]=pin(body)
    need(read(C/extra)==body,'Live actual acceptance receipt equals complete export receipt')
    need(isinstance(gate['additional_checkpoint_pins'],list) and len(gate['additional_checkpoint_pins'])<=256,'Bounded explicit extra evidence')
    for spec in gate['additional_checkpoint_pins']:
        name=spec['path'];relpath(name);need(name.startswith(str(A.relative_to(C))+'/') and name not in paths,
             'Extra checkpoint scope stays in PR110 audit, with no collisions')
        paths[name]={'bytes':spec['bytes'],'sha256':spec['sha256']}
    for name,spec in paths.items():read(C/name,spec=spec,retain=False)
    tracked={x.decode() for x in git(capture,runtime,'diff','--name-only','--diff-filter=ACMRTUXB','-z').split(b'\0') if x}
    need(tracked<=set(paths),'Foreign materialized tracked changes; do not stage or erase them')
    sorted_paths=sorted(paths);need(sum(len(x)+1 for x in sorted_paths)<=65536,'Bounded exact staging argv')
    need(gate['commit_message']=='Accept PR110: verified and published focal antipedal invariant','Reviewed exact commit message')
    git(capture,runtime,'add','-f','--',*sorted_paths)
    staged={x.decode() for x in git(capture,runtime,'diff','--cached','--name-only','-z').split(b'\0') if x}
    need(staged and staged<=set(paths),'Scoped staged entries only')
    need(not git(capture,runtime,'diff','--cached','--name-only','--diff-filter=D','-z'),'No staged deletions')
    git(capture,runtime,'-c','user.name='+AUTHOR['name'],'-c','user.email='+AUTHOR['email'],'commit','-m',gate['commit_message'],deadline=60)
    commit=git(capture,runtime,'rev-parse','HEAD').decode().strip()
    need(git(capture,runtime,'show','-s','--format=%P',commit).decode().split()==[parent],'Exact single acceptance parent')
    changed={x.decode() for x in git(capture,runtime,'diff-tree','--no-commit-id','--name-only','-r','-z',commit).split(b'\0') if x}
    need(changed==staged,'Actual commit paths equal exact staged selection')
    for name,spec in paths.items():need(pin(git(capture,runtime,'show',commit+':'+name))==spec,'Full accepted committed bytes')
    tree=git(capture,runtime,'rev-parse',commit+'^{tree}').decode().strip()
    result={'schema':'pr110-actual-main-acceptance-checkpoint/v1','UTC':now(),'actual_operator_PID':os.getpid(),
        'parent':parent,'commit':commit,'tree':tree,'pins':[{'path':n,**paths[n]} for n in sorted_paths],
        'changed_paths':sorted(changed),'main_only':True,'remote_verified':False,'DOI':DOI,'tracker_range':RANGE,
        'packet_sha256':gate['packet_sha256'],'candidate_receipt_pin':gate['candidate_receipt_pin'],'merge_pending':True}
    save(capture.root/'LOCAL_RECEIPT.json',result)
    git(capture,runtime,'push','--force-with-lease=refs/heads/main:'+parent,URL,'HEAD:refs/heads/main',authenticated=True,deadline=60)
    need(git(capture,runtime,'ls-remote',URL,'refs/heads/main').decode().split()==[commit,'refs/heads/main'],'Acceptance remote readback')
    need(not git(capture,runtime,'diff','--cached','--name-only','-z'),'Acceptance index empty')
    result.update({'UTC':now(),'remote_verified':True});save(capture.root/'RECEIPT.json',result);return result

def accepted(gate,packet,runtime,capture):
    r=loads(audit(gate['acceptance_receipt_pin']))
    need(r['schema']=='pr110-actual-main-acceptance-checkpoint/v1' and r['remote_verified'] is True and r['parent']==packet['main_parent']
         and r['packet_sha256']==gate['packet_sha256'] and r['candidate_receipt_pin']==gate['candidate_receipt_pin']
         and r['commit']==gate['accepted_commit'] and r['tree']==gate['accepted_tree'],'Actual accepted checkpoint binding')
    main_preflight(capture,runtime,r['commit'])
    need(not git(capture,runtime,'diff','--name-only','--diff-filter=ACMRTUXB','-z'),'Materialized tracked changes after acceptance')
    for spec in r['pins']:
        read(C/spec['path'],spec=spec,retain=False)
        need(pin(git(capture,runtime,'show',r['commit']+':'+spec['path']))=={k:spec[k] for k in ('bytes','sha256')},'Accepted Git body drift')
    return r

def ready_action(gate,packet,runtime,W,r,capture):
    acc=accepted(gate,packet,runtime,capture)
    title=audit(gate['title_pin']).decode().rstrip('\n');body=audit(gate['body_pin']).decode()
    need(title=='Accept PR110: focal antipedal invariant k603 proved and published' and DOI in body,'Exact reviewed title and published body')
    live_pr(capture,runtime,draft=True)
    gh(capture,runtime,'pr','edit',PR_URL,'--title',title,'--body-file',str(A/relpath(gate['body_pin']['path'])))
    live_pr(capture,runtime,draft=True,title=title,body=body)
    gh(capture,runtime,'pr','ready',PR_URL)
    pr=live_pr(capture,runtime,draft=False,title=title,body=body)
    result={'schema':'pr110-actual-reviewed-ready-PR/v1','UTC':now(),'actual_operator_PID':os.getpid(),
        'accepted_commit':acc['commit'],'accepted_tree':acc['tree'],'original_PR_head':ORIGINAL,
        'exact_title_and_body_readback':True,'PR':pr,'DOI':DOI,'tracker_range':RANGE,'merge_pending':True}
    save(capture.root/'RECEIPT.json',result);return result

def merge_action(gate,packet,runtime,W,r,capture):
    acc=accepted(gate,packet,runtime,capture);head=acc['commit'];tree=acc['tree']
    ready=loads(audit(gate['ready_receipt_pin']))
    need(ready['schema']=='pr110-actual-reviewed-ready-PR/v1' and ready['accepted_commit']==head and ready['accepted_tree']==tree
         and ready['original_PR_head']==ORIGINAL and ready['exact_title_and_body_readback'] is True,'Actual readiness receipt')
    title=audit(gate['title_pin']).decode().rstrip('\n');body=audit(gate['body_pin']).decode()
    live_pr(capture,runtime,draft=False,title=title,body=body)
    absences=git(capture,runtime,'diff','--name-only','--diff-filter=D','-z')
    need(git(capture,runtime,'write-tree').decode().strip()==tree,'Complete accepted index/tree, despite physical sparse absences')
    git(capture,runtime,'cat-file','-e',ORIGINAL+'^{commit}')
    need(shutil.disk_usage(C).free>=64*1024*1024,'Merge reserve')
    save(capture.root/'PRE_MERGE_READBACK.json',{'UTC':now(),'accepted_main':head,'original_PR_head':ORIGINAL,'accepted_tree':tree,
        'physical_sparse_absence_name_stream_pin':pin(absences),'physical_sparse_absences_never_staged':True,
        'complete_index_matches_accepted_tree':True,'full_accepted_bytes_checked':True,'no_materialized_tracked_changes':True})
    git(capture,runtime,'-c','user.name='+AUTHOR['name'],'-c','user.email='+AUTHOR['email'],'merge','-s','ours','--no-ff','--no-edit',
        '-m','Merge PR110: independently verified and published focal antipedal invariant',ORIGINAL,deadline=60)
    commit=git(capture,runtime,'rev-parse','HEAD').decode().strip()
    parents=git(capture,runtime,'show','-s','--format=%P',commit).decode().split()
    merged_tree=git(capture,runtime,'rev-parse',commit+'^{tree}').decode().strip()
    need(parents==[head,ORIGINAL] and merged_tree==tree,'Exact original-head second parent and byte-identical accepted tree')
    need(git(capture,runtime,'write-tree').decode().strip()==tree and not git(capture,runtime,'diff','--cached','--name-only','-z'),
         'Merge index stays identical and unstaged')
    for spec in acc['pins']:read(C/spec['path'],spec=spec,retain=False)
    result={'schema':'pr110-actual-main-only-native-merge/v1','UTC':now(),'actual_operator_PID':os.getpid(),'accepted_commit':head,
        'original_PR_head':ORIGINAL,'merge_commit':commit,'exact_parents':parents,'accepted_tree':tree,'merge_tree':merged_tree,
        'tree_equality_verified':True,'main_only':True,'all_accepted_materialized_pins_preserved':True,
        'local_merge_complete':True,'remote_push_complete':False,'GitHub_MERGED_confirmed':False,'DOI':DOI,'tracker_range':RANGE,
        'primary_checkout_mutated':False,'new_central_proof_search_turns':0,'human_outreach_or_GitHub_release':False}
    save(capture.root/'LOCAL_RECEIPT.json',result)
    git(capture,runtime,'push','--force-with-lease=refs/heads/main:'+head,URL,'HEAD:refs/heads/main',authenticated=True,deadline=60)
    need(git(capture,runtime,'ls-remote',URL,'refs/heads/main').decode().split()==[commit,'refs/heads/main'],'Merge remote readback')
    result.update({'UTC':now(),'remote_push_complete':True});save(capture.root/'REMOTE_RECEIPT.json',result)
    # A pending server transition does not trigger another mutation or invented success.
    pr=loads(gh(capture,runtime,'pr','view',PR_URL,'--json','number,state,headRefOid,mergeCommit,mergedAt,url'))
    save(capture.root/'GITHUB_STATUS_READBACK.json',pr)
    need(pr['number']==110 and pr['headRefOid']==ORIGINAL,'Actual GitHub head identity')
    if pr['state']=='MERGED':
        need(pr['mergeCommit']['oid']==commit and pr['mergedAt'],'Actual GitHub merged OID/time')
        result.update({'UTC':now(),'GitHub_MERGED_confirmed':True,'mergedAt':pr['mergedAt'],'PR_URL':pr['url'],
                       'native_acceptance_and_merge_complete':True})
        save(capture.root/'RECEIPT.json',result)
    else:
        need(pr['state']=='OPEN','Unexpected GitHub post-push state')
        result['native_acceptance_and_merge_complete']=False
        save(capture.root/'SERVER_STATUS_PENDING.json',result)
    return result

def status_action(gate,packet,runtime,W,r,capture):
    merged=loads(audit(gate['remote_merge_receipt_pin']));commit=merged['merge_commit']
    need(merged['schema']=='pr110-actual-main-only-native-merge/v1' and merged['remote_push_complete'] is True
         and merged['tree_equality_verified'] is True and merged['original_PR_head']==ORIGINAL
         and merged['exact_parents']==[gate['accepted_commit'],ORIGINAL],'Actual already-pushed merge receipt')
    main_preflight(capture,runtime,commit)
    pr=live_pr(capture,runtime,state='MERGED')
    need(pr['mergeCommit']['oid']==commit and pr['mergedAt'],'Actual delayed GitHub merged OID/time')
    result={**merged,'UTC':now(),'actual_status_reader_PID':os.getpid(),'GitHub_MERGED_confirmed':True,
        'native_acceptance_and_merge_complete':True,'mergedAt':pr['mergedAt'],'PR_URL':pr['url'],'read_only_followup':True}
    save(capture.root/'RECEIPT.json',result);return result

def main():
    need(len(sys.argv)==3 and sys.argv[1] in {'export','acceptance_commit','ready','merge','status'},'Explicit action and root gate required')
    action=sys.argv[1];path=pathlib.Path(sys.argv[2]);gate,packet,runtime,W,r,gatepin=load_gate(path,action)
    label=gate['operation_label'];need(re.fullmatch(r'[a-z][a-z0-9_]{0,79}',label),'Unique bounded action label')
    capture=Capture(A/'actual_acceptance_actions_20261006'/label)
    def stopped(sig,frame):
        global PENDING_SIGNAL
        if SPAWN_CRITICAL:PENDING_SIGNAL=sig;return
        raise SystemExit('Actual operator '+signal.Signals(sig).name)
    signal.signal(signal.SIGTERM,stopped);signal.signal(signal.SIGINT,stopped)
    save(capture.root/'START.json',{'actual_operator_PID':os.getpid(),'UTC':now(),'action':action,'gate_path':str(path),
        'gate_pin':gatepin,'argv':sys.argv,'cwd':os.getcwd(),'environment_sha256':pin(canonical(dict(os.environ)))['sha256'],
        'executing_program_pin':pin(read(__file__,128*1024))})
    try:
        result={'export':export_action,'acceptance_commit':acceptance_commit,'ready':ready_action,
                'merge':merge_action,'status':status_action}[action](gate,packet,runtime,W,r,capture)
    except BaseException as e:
        save(capture.root/'FAILURE.json',{'UTC':now(),'actual_operator_PID':os.getpid(),'action':action,
             'error':type(e).__name__+': '+str(e)[:400],'live_action_may_be_partial':True,
             'do_not_blindly_repeat_mutations':True,'process_journal':str(capture.root/'PROCESS_JOURNAL.json')})
        raise
    print(json.dumps(result,sort_keys=True))

if __name__=='__main__':
    main()
