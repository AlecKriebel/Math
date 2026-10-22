"""Read-only authentication of the complete immutable candidate inventory."""
from pathlib import Path
import datetime, hashlib, json, os, stat, subprocess, sys

HERE = Path(__file__).resolve().parent.parent
AUDIT = HERE.parent.parent
REPO = Path('/Users/alec/Documents/Math')
HEAD = 'b356dec5cb01e5f536b9cfeece56ad08844c03cb'
RECORD_SHA = '610351fbb778f78ce53cda03ea715f38615abb5710690987c214f8093bda13ae'

def main():
    records_bytes = (AUDIT / 'ORIGINAL_FILE_RECORDS.json').read_bytes()
    if hashlib.sha256(records_bytes).hexdigest() != RECORD_SHA:
        raise RuntimeError('External records anchor mismatch')
    records = json.loads(records_bytes)
    if records['head'] != HEAD or len(records['files']) != 26:
        raise RuntimeError('Inventory shape mismatch')
    commands = []
    def git(*args):
        cmd = ['git', '-C', str(REPO), *args]
        start = datetime.datetime.now(datetime.timezone.utc).isoformat()
        p = subprocess.run(cmd, capture_output=True, check=False)
        commands.append({'argv': cmd, 'launch_utc': start, 'returncode': p.returncode,
                         'stdout_sha256': hashlib.sha256(p.stdout).hexdigest(),
                         'stdout_bytes': len(p.stdout), 'stderr': p.stderr.decode(errors='replace')})
        if p.returncode:
            raise RuntimeError(p.stderr.decode(errors='replace'))
        return p.stdout
    actual_paths = sorted(str(p.relative_to(AUDIT / 'original')) for p in (AUDIT / 'original').rglob('*') if p.is_file() or p.is_symlink())
    if actual_paths != sorted(records['files']):
        raise RuntimeError('Extra/missing snapshot paths')
    observed = {}
    for rel, expected in records['files'].items():
        p = AUDIT / 'original' / rel
        st = p.lstat()
        if not stat.S_ISREG(st.st_mode):
            raise RuntimeError('Nonregular snapshot entry: ' + rel)
        disk = p.read_bytes()
        tree = git('ls-tree', HEAD, '--', rel).decode().strip()
        mode, typ, tail = tree.split(' ', 2)
        blob, name = tail.split('\t', 1)
        committed = git('cat-file', 'blob', blob)
        got = {'bytes': len(disk), 'sha256': hashlib.sha256(disk).hexdigest(),
               'git_blob': blob, 'git_mode': mode, 'disk_mode': format(stat.S_IMODE(st.st_mode), '04o')}
        if name != rel or typ != 'blob' or got != expected or disk != committed:
            raise RuntimeError('Authentication failed: ' + rel)
        observed[rel] = got
    result = {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'head': HEAD, 'record_sha256': RECORD_SHA, 'files': observed,
              'file_count': len(observed), 'total_bytes': sum(x['bytes'] for x in observed.values()),
              'exact_git_disk_bytes_and_modes': True, 'read_only_git_commands': commands}
    destination = HERE / 'receipts' / sys.argv[1]
    destination.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('files', 'read_only_git_commands')}, indent=2))

if __name__ == '__main__':
    main()
