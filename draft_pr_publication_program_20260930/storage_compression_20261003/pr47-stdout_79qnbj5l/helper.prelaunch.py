#!/usr/bin/python3
"""UNEXECUTED SOURCE: ROOT only; completed, quiescent allowlisted files only."""
import argparse, base64, datetime, fcntl, hashlib, json, os, stat, subprocess, sys, tempfile
from pathlib import Path
PROGRAM = Path('/Users/alec/Documents/Math/draft_pr_publication_program_20260930')
BASE = PROGRAM / 'storage_compression_20261003'
HISTORY = PROGRAM / 'checkpoints/checkpoint_20261003_1215_preparation/actual_run_20261003_1305'
ALLOW = {'pilot': HISTORY / 'PRIVATE_CHECKPOINT_INDEX', 'reconciled': HISTORY / 'RECONCILED_REAL_INDEX',
         'pr47-stdout': PROGRAM / 'audits/pr47_2849/ROOT_POST_ACTUAL_READONLY_COMMANDS/67/stdout.bin'}
PIN = 'd8906de0095a0ac86d1afd15e2f351814fb91b3c2db3e60e70d8aa35764091aa'
COMPRESSED = stat.UF_COMPRESSED
FIELDS = ('st_dev', 'st_ino', 'st_mode', 'st_nlink', 'st_uid', 'st_gid', 'st_size', 'st_rdev',
          'st_atime_ns', 'st_mtime_ns', 'st_ctime_ns', 'st_flags', 'st_blocks', 'st_blksize', 'st_birthtime')
commands = []
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def require(condition, message):
    if not condition: raise RuntimeError(message)
def safe(path):
    for part in (path,) + tuple(path.parents): require(not part.is_symlink(), 'symlink path: ' + str(part))
def values(s): return {k: getattr(s, k) for k in FIELDS}
def digest(path):
    h = hashlib.sha256()
    with os.fdopen(os.open(path, os.O_RDONLY | os.O_NOFOLLOW), 'rb') as f:
        for block in iter(lambda: f.read(1048576), b''): h.update(block)
    return h.hexdigest()
def command(argv, stdout=None, stderr=None):
    env = {k: v for k, v in os.environ.items() if not k.startswith('DITTO')}
    start = utc()
    p = subprocess.Popen(argv, stdout=stdout or subprocess.PIPE, stderr=stderr or subprocess.PIPE, env=env)
    out, err = p.communicate()
    rec = {'argv': argv, 'pid': p.pid, 'start_utc': start, 'end_utc': utc(), 'exit': p.returncode}
    if stdout is None:
        rec.update(stdout_base64=base64.b64encode(out).decode(), stderr_base64=base64.b64encode(err).decode())
    commands.append(rec)
    require(p.returncode == 0, 'native command failed; complete streams retained')
    return out
def stable(s): return {k: v for k, v in s.items() if k != "st_atime_ns"}
def attribute(path, name, compact):
    argv = ["/usr/bin/xattr", "-px", name, str(path)]; start = utc()
    raw = hashlib.sha256(); logical = hashlib.sha256(); count = 0; output = []; value = bytearray(); failure = None
    with tempfile.TemporaryFile(dir=BASE) as errors:
        p = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=errors)
        try:
            while True:
                line = p.stdout.readline(8193)
                if not line: break
                require(len(line) <= 8192, "xattr hex line exceeds bound")
                data = bytes.fromhex(line.decode("ascii")); count += len(data)
                require(count <= (67108864 if compact else 65536), "xattr value exceeds bound")
                raw.update(line); logical.update(data)
                if not compact: output.append(line); value.extend(data)
        except BaseException as exc:
            failure = repr(exc); p.kill()
        finally:
            p.stdout.close(); p.wait(); errors.seek(0); err = errors.read()
            rec = {"argv": argv, "pid": p.pid, "start_utc": start, "end_utc": utc(), "exit": p.returncode,
                   "stderr_base64": base64.b64encode(err).decode(), "parse_failure": failure}
            rec.update(stdout_retention="compression bookkeeping hash only", stdout_sha256=raw.hexdigest()) if compact else rec.update(stdout_base64=base64.b64encode(b"".join(output)).decode())
            commands.append(rec)
    require(failure is None and p.returncode == 0, "xattr read or bounded hex parse failed")
    return {"bytes": count, "sha256": logical.hexdigest()} if compact else base64.b64encode(value).decode()
def snapshot(path, original_names=None):
    safe(path)
    before = values(os.lstat(path))
    require(stat.S_ISREG(before['st_mode']) and before['st_nlink'] == 1, 'not a singly linked regular file')
    body = digest(path)
    after = values(os.lstat(path))
    require(all(before[k] == after[k] for k in FIELDS if k != 'st_atime_ns'), 'file changed during read')
    names_raw = command(["/usr/bin/xattr", str(path)]); require(len(names_raw) <= 16384, "xattr names exceed bound")
    names = names_raw.decode("utf-8").splitlines(); require(len(names) <= 64 and len(names) == len(set(names)), "invalid xattr name inventory")
    if original_names is not None: require(set(names) - set(original_names) <= {"com.apple.decmpfs", "com.apple.ResourceFork"}, "unexpected added xattr")
    attrs = {k: attribute(path, k, original_names is not None and k not in original_names) for k in names}
    acl = command(['/bin/ls', '-lde', str(path)]).splitlines()[1:]
    postmeta = values(os.lstat(path)); require(stable(postmeta) == stable(after), 'file changed during metadata read')
    return {'stat': postmeta, 'pre_read_stat': before, 'post_body_stat': after, 'sha256': body, 'xattrs': attrs,
            'acl_base64': [base64.b64encode(line).decode() for line in acl]}
def identity(s): return {"stat": stable(s["stat"]), **{k: s[k] for k in ("sha256", "xattrs", "acl_base64")}}
def save(path, record):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(record, f, indent=2, sort_keys=True)
        f.write('\n'); f.flush(); os.fsync(f.fileno())
def main():
    ap = argparse.ArgumentParser(description=__doc__); ap.add_argument('target', choices=ALLOW); ap.add_argument('--confirm-completed-quiescent', action='store_true', required=True)
    ap.add_argument('--positive-pilot-receipt', type=Path)
    args = ap.parse_args(); safe(BASE); safe(Path(__file__).absolute())
    require(Path(__file__).absolute() == BASE / 'compress_completed_v2.py', 'run canonical helper source only')
    helper = Path(__file__).read_bytes(); helper_sha = hashlib.sha256(helper).hexdigest()
    safe(BASE / 'operation.lock')
    lock = os.fdopen(os.open(BASE / 'operation.lock', os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600), 'r+b')
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    if args.target != 'pilot':
        receipt = args.positive_pilot_receipt
        require(receipt is not None and receipt.name == 'receipt.json' and receipt.parent.parent == BASE, 'pilot receipt required')
        safe(receipt)
        pilot = json.loads(receipt.read_text())
        require(pilot.get('status') == 'COMPRESSED' and pilot.get('target') == str(ALLOW['pilot'])
                and pilot.get('helper_sha256') == helper_sha and pilot.get('saved_allocated_bytes', 0) > 0, 'no matching positive pilot')
        require(identity(snapshot(ALLOW['pilot'], pilot['before']['xattrs'])) == identity(pilot['after']), 'pilot has changed since successful receipt')
    else:
        require(args.positive_pilot_receipt is None, 'pilot takes no prior receipt')
    source = ALLOW[args.target]; safe(source)
    fd = os.open(source, os.O_RDONLY | os.O_NOFOLLOW); fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    run = Path(tempfile.mkdtemp(prefix=args.target + '_', dir=BASE))
    (run / 'helper.prelaunch.py').write_bytes(helper); record = {'status': 'PRELAUNCH', 'source_replaced': False, 'target': str(source), 'helper_sha256': helper_sha,
              'operator_pid': os.getpid(), 'operator_executable': sys.executable, 'operator_argv': sys.argv,
              'python_flags': repr(sys.flags), 'cwd': os.getcwd(), 'start_utc': utc(), 'commands': commands}
    committed = False
    try:
        original = snapshot(source); record['before'] = original
        require(stable(values(os.fstat(fd))) == stable(original['stat']), 'opened source identity changed')
        s = original['stat']
        require(not (s['st_flags'] & COMPRESSED), 'source already compressed')
        if args.target == 'pilot':
            require(original['sha256'] == PIN and s['st_size'] == 21767721 and stat.S_IMODE(s['st_mode']) == 0o644
                    and s['st_blocks'] * 512 == 21770240 and s['st_flags'] == 0
                    and set(original['xattrs']) == {'com.apple.provenance'}, 'pilot source pin mismatch')
        stage = run / source.name
        argv = ['/usr/bin/ditto', '--hfsCompression', '--noclone', '--nocache', '--rsrc', '--extattr', '--acl', '--qtn', str(source), str(stage)]
        record['ditto_argv'] = argv; save(run / 'prelaunch.json', record)
        with open(run / 'ditto.stdout.bin', 'wb') as out, open(run / 'ditto.stderr.bin', 'wb') as err:
            command(argv, out, err)
        staged = snapshot(stage, original['xattrs']); record['staged'] = staged; t = staged['stat']
        require(original['sha256'] == staged['sha256'], 'logical-byte hash mismatch')
        require(all(s[k] == t[k] for k in ('st_dev', 'st_size', 'st_mode', 'st_mtime_ns', 'st_uid', 'st_gid')), 'required metadata mismatch')
        require(staged['acl_base64'] == original['acl_base64'], 'ACL mismatch')
        require(all(staged['xattrs'].get(k) == v for k, v in original['xattrs'].items()), 'existing xattr mismatch')
        require(set(staged['xattrs']) - set(original['xattrs']) <= {'com.apple.decmpfs', 'com.apple.ResourceFork'}, 'unexpected added xattr')
        require(t['st_flags'] == (s['st_flags'] | COMPRESSED), 'unexpected flag transformation')
        saving = (s['st_blocks'] - t['st_blocks']) * 512; require(saving > 0, 'no allocated-block saving')
        record.update(status='VERIFIED_BEFORE_REPLACE', saved_allocated_bytes=saving, permitted_changes=['inode', 'ctime', 'birthtime', 'UF_COMPRESSED', 'compression bookkeeping xattrs', 'read access time'])
        save(run / 'prepared.json', record)
        require(identity(snapshot(source)) == identity(original) and stable(values(os.fstat(fd))) == stable(original['stat']), 'source changed before replace')
        require(stable(values(os.lstat(source))) == stable(original['stat']), 'source final stat changed')
        os.replace(stage, source); committed = True
        after = snapshot(source, original['xattrs']); record['after'] = after
        require(after['sha256'] == original['sha256'] and all(after['stat'][k] == t[k]
                for k in ('st_dev', 'st_ino', 'st_mode', 'st_mtime_ns', 'st_uid', 'st_gid', 'st_size', 'st_flags')), 'postreplace identity mismatch')
        record.update(status='COMPRESSED', source_replaced=True, end_utc=utc())
        save(run / 'receipt.json', record)
        print(json.dumps({'receipt': str(run / 'receipt.json'), 'saved_allocated_bytes': saving, 'source_replaced': True}))
    except BaseException as exc:
        record.update(status='POSTCOMMIT_RECORD_FAILURE' if committed else 'ABORTED_ORIGINAL_PATH_UNREPLACED', source_replaced=committed, error=repr(exc), end_utc=utc())
        try:
            save(run / 'failure.json', record)
        finally:
            print(json.dumps(record), file=sys.stderr)
        raise
    finally:
        os.close(fd); lock.close()
if __name__ == '__main__': main()
