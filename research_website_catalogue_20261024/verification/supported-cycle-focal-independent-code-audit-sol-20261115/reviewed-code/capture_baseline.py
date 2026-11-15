"""Explicit root-GO read-only capture; writes only new owner caches, never website/Git."""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import re
import stat
import struct
import subprocess
import xml.etree.ElementTree as ET

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
W = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
O = Path(__file__).resolve().parent
GO = P / 'verification/root-supported-cycle-focal-actual623-baseline-GO-20261115.json'
GO_SHA = '0d7371f227e608c79d7f79135cb78cecd2fee4e190c7952bebb3afa7c0c639c2'
BASE = '0880af3e389248dbcd098ac275a880d93e09ea99'


def need(ok, why):
    if not ok:
        raise RuntimeError(why)


def sha(body):
    return hashlib.sha256(body).hexdigest()


def read(path):
    need(stat.S_ISREG(path.lstat().st_mode) and path.resolve() == path, 'real ordinary baseline input')
    return path.read_bytes()


def extent(root):
    need(stat.S_ISDIR(root.lstat().st_mode) and root.resolve() == root, 'real directory')
    files, directories = [], []
    def walk(directory):
        with os.scandir(directory) as entries:
            for entry in entries:
                path = Path(entry.path); mode = entry.stat(follow_symlinks=False).st_mode
                relative = path.relative_to(root).as_posix()
                if stat.S_ISDIR(mode):
                    directories.append(relative); walk(path)
                else:
                    need(stat.S_ISREG(mode), 'no namespace links/specials')
                    files.append(relative)
    walk(root)
    return sorted(files), sorted(directories)


def parse_index(raw, targets):
    need(raw[:4] == b'DIRC' and len(raw) >= 32, 'whole native index')
    version, count = struct.unpack('>II', raw[4:12])
    need(version == 2 and hashlib.sha1(raw[:-20]).digest() == raw[-20:], 'native v2 and checksum')
    offset = 12; entries = []; protected = []
    for _ in range(count):
        start = offset
        need(offset + 62 < len(raw) - 20, 'whole native header')
        flags = struct.unpack('>H', raw[offset + 60:offset + 62])[0]
        end = raw.find(b'\0', offset + 62, len(raw) - 20)
        need(end >= 0 and flags & 0xF000 == 0, 'stage0 ordinary native flags')
        path = raw[offset + 62:end]
        offset = start + ((end + 1 - start + 7) // 8) * 8
        need(path and flags & 0xFFF == min(len(path), 0xFFF)
             and raw[end:offset] == b'\0' * (offset - end), 'native path/padding')
        mode = struct.unpack('>I', raw[start + 24:start + 28])[0]
        oid = raw[start + 40:start + 60].hex()
        need(mode in [0o100644, 0o100755, 0o120000, 0o160000], 'native mode')
        record = raw[start:offset]; entries.append((path, record, mode, oid))
        if path not in targets:
            protected.append((path, record))
    paths = [e[0] for e in entries]
    need(paths == sorted(set(paths)), 'complete unique native path order')
    extensions = []
    while offset < len(raw) - 20:
        need(offset + 8 <= len(raw) - 20, 'whole extension header')
        key = raw[offset:offset + 4]; length = struct.unpack('>I', raw[offset + 4:offset + 8])[0]; offset += 8
        need(key == b'TREE' and offset + length <= len(raw) - 20, 'only supported TREE extension')
        extensions.append({'name': 'TREE', 'bytes': length, 'SHA256': sha(raw[offset:offset + length])}); offset += length
    need(offset == len(raw) - 20 and len(extensions) <= 1, 'whole native extension extent')
    records = b'\0'.join(path + b'\t' + record.hex().encode() for path, record in protected) + b'\0'
    return entries, {'version': version, 'records': count, 'protected_records': len(protected),
                     'protected_native_raw_records_SHA256': sha(records), 'extensions': extensions}


def main():
    need(sys.argv[1:] == ['--root-go-sha256', GO_SHA], 'explicit actual root GO hash before live access')
    go_body = read(GO); need(sha(go_body) == GO_SHA, 'whole actual root GO')
    go = json.loads(go_body)
    need(go['authority'] == 'root' and go['writerFreshBaselineCaptureAuthorized'] is True
         and go['installationOrCanonicalAAAuthority'] is False and go['actualWebsiteHEAD'] == BASE
         and go['actualObservedCounts'] == [623, 94, 95], 'fresh623 capture only, no install authority')
    need(not (O / 'FINAL_SEAL.json').exists() and not (O / 'WEBSITE_BASELINE.json').exists(), 'write-once pre-FINAL actual baseline')
    (O / 'ACTUAL_BASELINE_GO.json').write_bytes(go_body)
    (O / 'baseline-blobs').mkdir(); (O / 'private').mkdir(exist_ok=True)
    receipts = []
    def git(*args):
        need(args[0] in {'rev-parse', 'symbolic-ref', 'ls-files', 'ls-remote', 'remote', 'diff'}, 'read-only Git allowlist')
        env = {k:v for k,v in os.environ.items() if not k.startswith('GIT_')}; env['GIT_OPTIONAL_LOCKS'] = '0'
        result = subprocess.run(['git', '-c', 'core.fsmonitor=false', '-c', 'core.hooksPath=/dev/null'] + list(args),
                                cwd=W, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
        ordinal = len(receipts) + 1
        out = O / 'private' / ('git-%02d.stdout' % ordinal); err = O / 'private' / ('git-%02d.stderr' % ordinal)
        out.write_bytes(result.stdout); err.write_bytes(result.stderr)
        receipts.append({'ordinal': ordinal, 'operation': args[0], 'arguments_except_private_remote_URL':
                         [a if not (a.startswith('http') or a.startswith('git@')) else '<explicit captured push URL>' for a in args],
                         'exit': result.returncode, 'stdout': out.relative_to(O).as_posix(), 'stderr': err.relative_to(O).as_posix(),
                         'stdout_bytes': len(result.stdout), 'stdout_SHA256': sha(result.stdout),
                         'stderr_bytes': len(result.stderr), 'stderr_SHA256': sha(result.stderr)})
        need(result.returncode == 0, 'read-only Git operation failed')
        return result.stdout
    def state():
        need(git('rev-parse', '--show-toplevel').decode().strip() == str(W), 'exact actual website repository')
        need(git('symbolic-ref', 'HEAD').strip() == b'refs/heads/master', 'existing master branch')
        head = git('rev-parse', 'HEAD').decode().strip(); master = git('rev-parse', 'refs/heads/master').decode().strip()
        tree = git('rev-parse', 'HEAD^{tree}').decode().strip()
        need(head == master == BASE and tree == go['actualWebsiteTree'], 'actual current623 commit/tree')
        raw = read(W / '.git/index'); need(sha(raw) == go['actualIndexSHA256'], 'fresh actual raw index matches root GO')
        urls = git('remote', 'get-url', '--push', '--all', 'origin').splitlines()
        need(len(urls) == 1 and urls[0], 'one actual explicit push destination')
        remote = git('ls-remote', '--refs', urls[0].decode(), 'refs/heads/master')
        need(remote.split() == [BASE.encode(), b'refs/heads/master'], 'actual explicit remote master identity')
        controls = {name: read(W / '.git' / name) for name in ['HEAD', 'refs/heads/master', 'config']}
        need(not (W / '.git/index.lock').exists() and not (W / '.git/index.lock').is_symlink(), 'no index lock')
        return raw, {'HEAD': head, 'master': master, 'tree': tree, 'branch': 'master',
                     'index_SHA256': sha(raw), 'origin_push_URL_SHA256': sha(urls[0]),
                     'actual_remote_advertisement': remote.decode(),
                     'control_bytes_SHA256': {n:sha(b) for n,b in controls.items()}}, controls
    raw, before, controls = state()
    requirements = json.loads(read(O / 'ADAPTER_REQUIREMENTS.json'))
    targets = {('public/' + p).encode() for p in requirements['eight_article_root_leaves'] + requirements['only_aggregate_paths']}
    entries, native = parse_index(raw, targets)
    tuples = b'\0'.join(('%06o' % mode).encode() + b' ' + oid.encode() + b' 0\t' + path for path,record,mode,oid in entries) + b'\0'
    need(git('ls-files', '--stage', '-z') == tuples, 'whole actual native index and stage tuples agree')
    need({p for p,record,mode,oid in entries if p in targets} ==
         {b'public/research/index.html', b'public/research/sitemap.xml'}, 'only2 indexed aggregate overlaps,8 new leaves absent')
    (O / 'private/shared-index.before').write_bytes(raw)
    staged = git('diff', '--cached', '--name-only', '--diff-filter=D', '-z', BASE)
    (O / 'private/staged-deletions.z').write_bytes(staged)
    files, directories = extent(W / 'public'); need(len(files) == 623, 'actual complete623 public files')
    rows = []
    def freeze(path, role):
        body = read(path); key = sha(body); destination = O / 'baseline-blobs' / key
        if not destination.exists(): destination.write_bytes(body)
        need(read(destination) == body, 'whole baseline buffer retained')
        row = {'path': str(path), 'role': role, 'bytes': len(body), 'SHA256': key,
               'blob': 'baseline-blobs/' + key}; rows.append(row); return body
    for name in files: freeze(W / 'public' / name, 'public')
    for name in ['.firebaserc', 'firebase.json', '.gitignore', 'README.md', 'deploy.sh', 'preview.sh']:
        freeze(W / name, 'site_config')
    for name in controls: freeze(W / '.git' / name, 'Git_control')
    index_body = read(W / 'public/research/index.html')
    graphs = re.findall(rb'<script type="application/ld\+json">\s*(.*?)\s*</script>', index_body, re.S)
    need(len(graphs) == 1, 'one actual current index graph')
    listing = json.loads(graphs[0])['mainEntity']
    need(listing['numberOfItems'] == len(listing['itemListElement']) == 94
         and len(ET.fromstring(read(W / 'public/research/sitemap.xml'))) == 95, 'actual94 index/95 XML')
    old = set(files); need(old & set(requirements['eight_article_root_leaves']) == set()
         and len(old - set(requirements['only_aggregate_paths'])) == 621, 'exact8 new/2 aggregates and621 unrelated public paths')
    inputs = json.loads(read(O / 'SOURCE_INPUTS.json')); original_rows = {r['path']:r for r in inputs['files']}
    for rid in ['23578142', '23306203']:
        editorial = P / 'papers' / rid / 'reviews/editorial'
        descriptor = original_rows[str(editorial / 'PROTECTED_INPUTS.json')]
        protected = json.loads(read(O / descriptor['blob']))
        for item in protected['files']:
            body = read(Path(item['path']))
            need(len(body) == item['bytes'] and sha(body) == item['SHA256'], 'actual current original source/core equals approved input')
    for row in rows: need(read(Path(row['path'])) == read(O / row['blob']), 'whole website/config/control remains unchanged')
    need(extent(W / 'public') == (files, directories), 'whole public directory/file extent unchanged')
    raw_after, after, after_controls = state()
    need(raw_after == raw and after == before and after_controls == controls, 'whole before/after index HEAD master controls remote identity')
    result = {'schema': 'fresh-root-authorized-actual623-readonly-baseline-v1', 'UTC': datetime.now(timezone.utc).isoformat(),
              'root_GO_SHA256': GO_SHA, 'root_actual_GO': go, 'Git': before, 'native_index': native,
              'public_namespace': files, 'public_directories': directories, 'files': rows,
              'baseline_counts': [623,94,95], 'proposed_counts': [631,96,97], 'unrelated_public_paths': 621,
              'actual_staged_deletions': {'count': len([x for x in staged.split(b'\0') if x]), 'bytes': len(staged), 'SHA256': sha(staged)},
              'full_raw_index': 'private/shared-index.before', 'actual_readonly_Git_receipts': receipts,
              'actual_source_core_fences_checked': True, 'all_before_after_fences_unchanged': True,
              'programme_repository_HEAD_index_refs_not_frozen_or_touched': True,
              'website_Git_index_ref_public_remote_source_Sheet_or_deploy_mutation': False,
              'production_installation_authorized': False, 'canonical_url': None, 'AA': None}
    (O / 'WEBSITE_BASELINE.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'PASS_FRESH_ACTUAL623_READONLY_BASELINE','counts':[623,94,95], 'proposal':[631,96,97],
                      'Git': before, 'native_index': native, 'site_configs':6, 'unrelated_public_paths':621,
                      'staged_deletion_count':result['actual_staged_deletions']['count'], 'read_only_Git_operations':len(receipts),
                      'actual_production_mutations':False},indent=2))

def postcheck():
    need(sys.argv[1:] == ['--postcheck', '--root-go-sha256', GO_SHA], 'explicit actual root GO for post-authoring reads')
    need(not (O / 'FINAL_SEAL.json').exists() and not (O / 'POST_AUTHORING_GUARD.json').exists(), 'one pre-FINAL postcheck only')
    need(sha(read(GO)) == GO_SHA, 'same actual root GO remains unchanged')
    baseline = json.loads(read(O / 'WEBSITE_BASELINE.json'))
    receipts = []
    def git(*args):
        need(args[0] in {'rev-parse','symbolic-ref','remote','ls-remote'}, 'postcheck read-only Git')
        env = {k:v for k,v in os.environ.items() if not k.startswith('GIT_')}; env['GIT_OPTIONAL_LOCKS'] = '0'
        r = subprocess.run(['git','-c','core.fsmonitor=false','-c','core.hooksPath=/dev/null']+list(args),
                           cwd=W,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=60)
        ordinal = len(receipts)+1
        out = O / 'private' / ('post-git-%02d.stdout' % ordinal); err = O / 'private' / ('post-git-%02d.stderr' % ordinal)
        need(not out.exists() and not err.exists(), 'fresh exact postcheck stream files')
        out.write_bytes(r.stdout); err.write_bytes(r.stderr)
        receipts.append({'ordinal':ordinal,'operation':args[0],'exit':r.returncode,
                         'stdout':out.relative_to(O).as_posix(),'stderr':err.relative_to(O).as_posix(),
                         'stdout_bytes':len(r.stdout),'stdout_SHA256':sha(r.stdout),
                         'stderr_bytes':len(r.stderr),'stderr_SHA256':sha(r.stderr)})
        need(r.returncode == 0, 'postcheck Git exit'); return r.stdout
    for row in baseline['files']:
        need(read(Path(row['path'])) == read(O / row['blob']), 'post-authoring complete public/config/control byte fence')
    need(extent(W / 'public') == (baseline['public_namespace'],baseline['public_directories']), 'post-authoring exact public extent')
    need(read(W / '.git/index') == read(O / baseline['full_raw_index']), 'post-authoring complete shared raw index')
    need(git('symbolic-ref','HEAD').strip() == b'refs/heads/master'
         and git('rev-parse','HEAD').decode().strip() == git('rev-parse','refs/heads/master').decode().strip() == BASE
         and git('rev-parse','HEAD^{tree}').decode().strip() == baseline['Git']['tree'], 'post-authoring actual existing master/tree')
    url = git('remote','get-url','--push','--all','origin').splitlines()
    need(len(url) == 1 and sha(url[0]) == baseline['Git']['origin_push_URL_SHA256'], 'same explicit actual push destination')
    remote = git('ls-remote','--refs',url[0].decode(),'refs/heads/master')
    need(remote.decode() == baseline['Git']['actual_remote_advertisement'], 'post-authoring actual remote master')
    inputs = json.loads(read(O / 'SOURCE_INPUTS.json'))
    for row in inputs['files']:
        need(read(Path(row['path'])) == read(O / row['blob']), 'all original source/editorial/fact/root bytes unchanged')
    for namespace in inputs['complete_original_namespaces']:
        need(extent(Path(namespace['path'])) == (namespace['files'],namespace['directories']), 'whole source namespace unchanged')
    mapping = {r['path']:r for r in inputs['files']}
    for rid in ['23578142','23306203']:
        e = P / 'papers' / rid / 'reviews/editorial'; row = mapping[str(e / 'PROTECTED_INPUTS.json')]
        protected = json.loads(read(O / row['blob']))
        for descriptor in protected['files']:
            body = read(Path(descriptor['path']))
            need(len(body) == descriptor['bytes'] and sha(body) == descriptor['SHA256'], 'complete original scientific/source/qualified core protection')
    need(read(W / '.git/index') == read(O / baseline['full_raw_index']), 'shared raw index unchanged after postcheck')
    result = {'schema':'private-stage-actual-post-authoring-readonly-guard-v1','UTC':datetime.now(timezone.utc).isoformat(),
              'status':'PASS_ALL_ACTUAL_SOURCE_WEBSITE_CONFIG_CORE_RAW_INDEX_HEAD_MASTER_REMOTE_UNCHANGED',
              'actual_counts':[623,94,95],'actual_master':BASE,'actual_tree':baseline['Git']['tree'],
              'actual_remote_advertisement':remote.decode(),'protected_native_records':baseline['native_index']['protected_records'],
              'all_original_source_input_files':819,'actual_readonly_Git_receipts':receipts,
              'production_source_Sheet_Git_deploy_or_remote_mutations':False}
    (O / 'POST_AUTHORING_GUARD.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'actual_counts':[623,94,95],'protected_native_records':58561,
                      'actual_readonly_Git_operations':len(receipts),'mutations':False},indent=2))


if __name__ == '__main__':
    if sys.argv[1:2] == ['--postcheck']:
        postcheck()
    else:
        main()
