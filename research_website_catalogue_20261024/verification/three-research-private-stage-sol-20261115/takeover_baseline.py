#!/usr/bin/env python3
"""Fresh read-only baseline, referring to the prior attempt's raw buffers.

The default reports scope without reading the live site. Explicit ``capture``
does read-only Git and whole stable public/control/index reads. Only a new
receipt in this owned directory can be written. No imports from prior helpers.
"""
from pathlib import Path
import datetime, hashlib, json, os, re, stat, struct, subprocess, sys
import xml.etree.ElementTree as ET

N = Path(__file__).absolute().parent
P = N.parent.parent
W = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
CONTROLS = ['.firebaserc', 'firebase.json', '.gitignore', 'README.md', 'deploy.sh', 'preview.sh', '.git/HEAD', '.git/refs/heads/master', '.git/config']

def need(ok, message):
    if not ok:
        raise ValueError(message)

def pin(data):
    return {'bytes': len(data), 'SHA256': hashlib.sha256(data).hexdigest()}

def read(path):
    need(path.is_relative_to(W) or path.is_relative_to(N), 'bounded read')
    first = path.lstat()
    need(stat.S_ISREG(first.st_mode), 'regular file ' + str(path))
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        opened = os.fstat(fd)
        need((first.st_dev, first.st_ino) == (opened.st_dev, opened.st_ino), 'open identity')
        chunks = []
        while True:
            block = os.read(fd, 1048576)
            if not block:
                break
            chunks.append(block)
        after = os.fstat(fd)
        final = path.lstat()
        need((opened.st_size, opened.st_mtime_ns, opened.st_ctime_ns) == (after.st_size, after.st_mtime_ns, after.st_ctime_ns), 'held buffer stable')
        need((final.st_dev, final.st_ino) == (opened.st_dev, opened.st_ino), 'path stable')
        data = b''.join(chunks)
        need(len(data) == opened.st_size, 'whole read')
        return data
    finally:
        os.close(fd)

def public():
    files, directories = [], []
    def visit(directory):
        first = directory.lstat()
        need(stat.S_ISDIR(first.st_mode), 'regular directory')
        for path in sorted(directory.iterdir()):
            name = path.relative_to(W / 'public').as_posix()
            mode = path.lstat().st_mode
            if stat.S_ISDIR(mode):
                directories.append(name)
                visit(path)
            elif stat.S_ISREG(mode):
                files.append({'path': name, **pin(read(path))})
            else:
                raise ValueError('special public entry ' + name)
        last = directory.lstat()
        need((first.st_dev, first.st_ino, first.st_mtime_ns, first.st_ctime_ns) == (last.st_dev, last.st_ino, last.st_mtime_ns, last.st_ctime_ns), 'directory stable')
    visit(W / 'public')
    return sorted(files, key=lambda row: row['path']), sorted(directories)

def controls():
    return [{'path': str(W / name), 'relative_path': name, **pin(read(W / name)), 'role': 'Git_control' if name.startswith('.git/') else 'site_config'} for name in CONTROLS]

def main():
    need(sys.argv[1:] in [[], ['capture']], 'finite explicit mode')
    if not sys.argv[1:]:
        print(json.dumps({'status': 'EXPLICIT_CAPTURE_REQUIRED', 'live_reads': False, 'writes': 0, 'network_requests': 0}))
        return
    out = N / 'TAKEOVER_BASELINE.json'
    need(not out.exists(), 'exclusive receipt; retain failed attempts')
    old_initial = read(N / 'INITIAL.json')
    old_base_raw = read(N / 'WEBSITE_BASELINE.json')
    need(pin(old_initial) == {'bytes': 5313, 'SHA256': 'b86cbeb69d7ff15ee2d7ac24aaaf16ec4443419d895366a488dc33611d891471'}, 'immutable prior INITIAL')
    need(pin(old_base_raw) == {'bytes': 149218, 'SHA256': 'b1abde53ec6456e8291af5cfd62184c0b82840c8947cd6ff2714acb50a7aa2bf'}, 'immutable prior baseline')
    old = json.loads(old_base_raw)
    receipts = []
    def git(root, args):
        need(root in (W, P.parent), 'exact repository')
        need(args[0] in ['rev-parse', 'symbolic-ref', 'ls-files', 'diff'], 'read-only builtins')
        argv = ['git', '--no-optional-locks', '-c', 'core.fsmonitor=false', '-c', 'core.hooksPath=/dev/null', '-C', str(root), *args]
        result = subprocess.run(argv, capture_output=True, timeout=45)
        receipts.append({'argv': argv, 'exit_code': result.returncode, 'stdout': pin(result.stdout), 'stderr': pin(result.stderr)})
        need(result.returncode == 0 and not result.stderr, 'actual read-only Git failure')
        return result.stdout
    need(git(P.parent, ['symbolic-ref', 'HEAD']).strip() == b'refs/heads/main', 'Math main retained')
    def state():
        need(git(W, ['rev-parse', '--show-toplevel']).decode().strip() == str(W), 'exact W')
        need(git(W, ['symbolic-ref', 'HEAD']).strip() == b'refs/heads/master', 'W master retained')
        refs = git(W, ['rev-parse', 'HEAD', 'refs/heads/master', 'HEAD^{tree}']).decode().splitlines()
        need(len(refs) == 3 and refs[0] == refs[1], 'HEAD/master equality')
        need(not os.path.lexists(W / '.git/index.lock'), 'no current index lock')
        index = read(W / '.git/index')
        need(index[:4] == b'DIRC' and hashlib.sha1(index[:-20]).digest() == index[-20:], 'whole native index checksum')
        return {'HEAD': refs[0], 'master': refs[1], 'tree': refs[2], 'raw_index': pin(index), 'native_index_version': struct.unpack('>I', index[4:8])[0], 'native_index_records': struct.unpack('>I', index[8:12])[0]}, index
    before, index = state()
    stage = git(W, ['ls-files', '--stage', '-z'])
    deletes = git(W, ['diff', '--cached', '--name-only', '--diff-filter=D', '-z', 'HEAD'])
    old_stage = next(row['stdout'] for row in old['actual_readonly_Git_receipts'] if row['argv'][-3:] == ['ls-files', '--stage', '-z'])
    need(index == read(N / 'raw/shared-index.before'), 'whole current native index equals prior opaque buffer')
    need(stage == read(Path(old_stage['path'])), 'whole current stage equals prior opaque buffer')
    need(stage.endswith(b'\0') and stage.count(b'\0') == before['native_index_records'], 'stage/native count')
    files, directories = public()
    ctl = controls()
    raw_index_html = read(W / 'public/research/index.html')
    graphs = [json.loads(part) for part in re.findall(rb'<script type="application/ld\+json">\s*(.*?)\s*</script>', raw_index_html, re.S)]
    inventory = [graph['mainEntity'] for graph in graphs if type(graph.get('mainEntity')) is dict and 'itemListElement' in graph['mainEntity']]
    need(len(inventory) == 1 and inventory[0]['numberOfItems'] == len(inventory[0]['itemListElement']), 'one counted native inventory')
    counts = [len(files), len(inventory[0]['itemListElement']), len(ET.fromstring(read(W / 'public/research/sitemap.xml')))]
    need(counts == [631, 96, 97], 'fresh baseline631/96/97')
    need(not any(Path(row['path']).name == 'README.md' for row in files), 'current public README absence')
    after, index_after = state()
    files_after, directories_after = public()
    need(before == after == old['Git'] and index == index_after, 'stable exact Git/index baseline')
    need(files == files_after == old['public_files'] and directories == directories_after == old['public_directories'], 'stable exact whole public baseline')
    need(ctl == controls() == old['site_and_Git_controls'], 'stable exact controls')
    need(pin(deletes) == old['staged_deletions_raw'], 'staged deletion preservation')
    need(git(P.parent, ['symbolic-ref', 'HEAD']).strip() == b'refs/heads/main', 'Math main retained after')
    result = {'UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'status': 'TAKEOVER_FRESH_READONLY_BASELINE_MATCHES_PRIOR_IMMUTABLE_CAPTURE', 'Git': before, 'baseline_counts': counts, 'all631_current_public_files_read_twice_and_compared': True, 'all_current_public_directories_and_controls_compared': True, 'Math_main_and_W_master_unchanged': True, 'raw_native_index_by_reference': {'path': str(N / 'raw/shared-index.before'), **pin(index)}, 'raw_whole_stage_by_reference': old_stage, 'old_baseline_by_reference': {'path': str(N / 'WEBSITE_BASELINE.json'), **pin(old_base_raw)}, 'old_INITIAL_by_reference': {'path': str(N / 'INITIAL.json'), **pin(old_initial)}, 'all58571_native_records_unchanged': True, 'eventual_protected_native_records_expectation': 58569, 'current_public_README_files': 0, 'actual_readonly_Git_receipts': receipts, 'site_or_Git_writes': 0, 'network_requests': 0, 'publication_authority': False, 'canonical_url': None, 'AA': None, 'follow_up': None}
    data = (json.dumps(result, indent=2) + '\n').encode()
    with out.open('xb') as target:
        need(target.write(data) == len(data), 'whole receipt')
    print(json.dumps({'status': result['status'], 'receipt': str(out), **pin(data), 'counts': counts, 'HEAD': before['HEAD'], 'index': before['raw_index']}))

if __name__ == '__main__':
    main()
