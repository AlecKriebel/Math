#!/usr/bin/env python3
"""One bounded native-first audit of the already published fourteen paths.

Only this lane receives writes. No helper is imported or executed. Git commands
are restricted to local read-only object/ref inspection; there is no network.
Both prior failures are preserved. Complete public and original-asset checks
are inherited exactly from v2, which stopped at an erroneous HTML tag counter.
This fresh continuation checks native indexes, commits, cache trees and guards.
"""
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import struct
import subprocess
import sys
import traceback

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
W = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
M = Path('/Users/alec/Documents/Math')
OWN = P / 'verification/stage3-post-publication-native-audit-sol-v3-20261117'
PROD = P / 'verification/wreath-dyadic-stress-production-root-v3-20261117'
STAGE = P / 'verification/wreath-dyadic-stress-stage-sol-20261116'
OLDIDX = P / 'verification/wreath-dyadic-stress-runtime-root-v3-20261117/install/63e3fc9e7a3ec74f92eb0124f171bc90725519976119663ca5dfb6fb450a5a91/native-backups/index.before'
GUARDS = P / 'verification/checkpoint-v3-installed-sources188189-initials-20261117/NATIVE_GUARDS_BEFORE.json'
OLD = 'b767102567ad89aff909f9f11c0e8b7d72b75c40'
NEW = '96f04aa5544df69daba07a9ed4d6212172e9984a'
TREE = '7260c2f004d311ab06dd8556de6e17a2196d1d28'
CHECKS = []
CHECK_GROUPS = {}
DETAILS = {}
START = datetime.datetime.now(datetime.timezone.utc).isoformat()

def need(ok, name, details=None):
    if name not in CHECK_GROUPS:
        group = {'check': name, 'PASS': True, 'observations': 0, 'details': details}
        CHECK_GROUPS[name] = group
        CHECKS.append(group)
    group = CHECK_GROUPS[name]
    group['observations'] += 1
    if not ok:
        group['PASS'] = False
        group['details'] = details
        raise AssertionError(name + ': ' + repr(details))

def sha(data):
    return hashlib.sha256(data).hexdigest()

def mode(path):
    return format(stat.S_IMODE(path.lstat().st_mode), '04o')

def filedata(path):
    need(stat.S_ISREG(path.lstat().st_mode), 'regular input', str(path))
    raw = path.read_bytes()
    return {'bytes': len(raw), 'SHA256': sha(raw), 'mode': mode(path)}

def pin(path, expected):
    actual = filedata(path)
    need(actual == {k: expected[k] for k in actual}, 'whole-file pin', {'path': str(path), 'actual': actual})
    return actual

def load(path):
    return json.loads(path.read_bytes())

def git(repo, *args, data=None):
    allowed = {'rev-parse', 'for-each-ref', 'ls-tree', 'cat-file'}
    need(bool(args) and args[0] in allowed, 'read-only Git allowlist', list(args))
    env = dict(os.environ)
    for key in list(env):
        if key.startswith('GIT_'):
            del env[key]
    env.update({'GIT_OPTIONAL_LOCKS': '0', 'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': '/dev/null', 'GIT_NO_REPLACE_OBJECTS': '1', 'LC_ALL': 'C'})
    cmd = ['/usr/bin/git', '--no-optional-locks', '-c', 'core.hooksPath=/dev/null', '-c', 'core.fsmonitor=false', '-C', str(repo), *args]
    run = subprocess.run(cmd, input=data, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, timeout=120)
    need(run.returncode == 0 and run.stderr == b'', 'read-only Git result', {'args': list(args), 'code': run.returncode, 'stderr': run.stderr.decode(errors='backslashreplace')})
    return run.stdout

def parse_index(path, expected_count):
    raw = path.read_bytes()
    need(raw[:4] == b'DIRC' and len(raw) >= 32, 'native index signature', str(path))
    version, count = struct.unpack('>II', raw[4:12])
    need(version == 2 and count == expected_count, 'native v2 record count', [str(path), version, count])
    need(hashlib.sha1(raw[:-20]).digest() == raw[-20:], 'native index trailing checksum', str(path))
    records, offset, previous = {}, 12, None
    for number in range(count):
        start = offset
        need(offset + 62 <= len(raw) - 20, 'index fixed record bounds', number)
        words = struct.unpack('>10I', raw[offset:offset + 40])
        oid = raw[offset + 40:offset + 60].hex()
        flags = struct.unpack('>H', raw[offset + 60:offset + 62])[0]
        need(not (flags & 0x4000), 'v2 no extended entry', number)
        end = raw.index(b'\0', offset + 62, len(raw) - 20)
        name = raw[offset + 62:end]
        offset = end + 1
        offset += (-(offset - start)) % 8
        need(offset <= len(raw) - 20 and raw[end:offset] == b'\0' * (offset - end), 'whole raw record zero padding', number)
        need(name and not name.startswith(b'/') and all(x not in (b'', b'.', b'..') for x in name.split(b'/')), 'valid index path bytes', repr(name))
        need((flags & 0xfff) == min(len(name), 0xfff), 'record name length flag', repr(name))
        stage = (flags >> 12) & 3
        key = (name, stage)
        need(previous is None or previous < key, 'strict index ordering', repr(key))
        need(words[6] in (0o100644, 0o100755, 0o120000, 0o160000), 'index mode', [repr(name), oct(words[6])])
        records[key] = {'raw': raw[start:offset], 'mode': format(words[6], 'o'), 'oid': oid, 'stage': stage}
        previous = key
    extensions = []
    while offset < len(raw) - 20:
        need(offset + 8 <= len(raw) - 20, 'index extension header bounds')
        sig, size = raw[offset:offset + 4], struct.unpack('>I', raw[offset + 4:offset + 8])[0]
        offset += 8
        need(offset + size <= len(raw) - 20, 'index extension payload bounds')
        need(sig == b'TREE' and not extensions, 'known single TREE extension only', repr(sig))
        extensions.append((sig, raw[offset:offset + size]))
        offset += size
    need(offset == len(raw) - 20, 'exact index end')
    return raw, records, extensions

def leaves(commit):
    out = git(W, 'ls-tree', '-r', '-z', '--full-tree', commit)
    result = {}
    for row in out.split(b'\0'):
        if not row:
            continue
        meta, name = row.split(b'\t', 1)
        mod, kind, oid = meta.split(b' ')
        need(name not in result, 'unique commit leaf', repr(name))
        result[name] = (mod.decode(), kind.decode(), oid.decode())
    return result

def index_semantics(records):
    return {key: (rec['mode'], rec['oid']) for key, rec in records.items()}

def staging_delta(records, head):
    semantics = index_semantics(records)
    result = {}
    for name in set(head) | {key[0] for key in records}:
        indexed = tuple((stage, *semantics[(name, stage)]) for stage in range(4) if (name, stage) in semantics)
        expected = ((0, head[name][0], head[name][2]),) if name in head else ()
        if indexed != expected:
            result[name] = (expected, indexed)
    return result

def native_trees(records):
    root = {}
    for (name, stage), rec in records.items():
        need(stage == 0, 'native TREE semantics require resolved stage zero', repr(name))
        parts, node = name.split(b'/'), root
        for part in parts[:-1]:
            need(part not in node or isinstance(node[part], dict), 'native directory/file conflict', repr(name))
            node = node.setdefault(part, {})
        need(parts[-1] not in node, 'native duplicate tree leaf', repr(name))
        node[parts[-1]] = rec
    trees = {}
    def build(node, path):
        entries, count = [], 0
        for name, item in node.items():
            if 'raw' in item and 'oid' in item:
                entries.append((name, item['mode'].encode(), bytes.fromhex(item['oid']), False))
                count += 1
            else:
                oid, subcount = build(item, path + (b'/' if path else b'') + name)
                entries.append((name, b'40000', bytes.fromhex(oid), True))
                count += subcount
        entries.sort(key=lambda e: e[0] + (b'/' if e[3] else b''))
        body = b''.join(mod + b' ' + name + b'\0' + oid for name, mod, oid, isdir in entries)
        oid = hashlib.sha1(b'tree ' + str(len(body)).encode() + b'\0' + body).hexdigest()
        trees[path] = {'oid': oid, 'count': count, 'body': body}
        return oid, count
    build(root, b'')
    return trees

def validate_cache(payload, records, label):
    trees, pos, nodes = native_trees(records), 0, []
    def parse(parent, root=False):
        nonlocal pos
        end = payload.index(b'\0', pos)
        name = payload[pos:end]
        need((root and name == b'') or (not root and name and b'/' not in name and name not in (b'.', b'..')), 'TREE node name', [label, repr(name)])
        lineend = payload.index(b'\n', end + 1)
        text = payload[end + 1:lineend]
        need(re.fullmatch(rb'-?[0-9]+ [0-9]+', text) is not None, 'TREE numeric syntax', [label, repr(text)])
        count, children = map(int, text.split(b' '))
        need(count >= -1 and children <= len(records), 'TREE counts bounded', [label, count, children])
        pos = lineend + 1
        oid = None
        if count >= 0:
            need(pos + 20 <= len(payload), 'TREE object bounds', label)
            oid = payload[pos:pos + 20].hex()
            pos += 20
        path = parent + (b'/' if parent else b'') + name if not root else b''
        need(path in trees and all(n['path'] != path for n in nodes), 'TREE unique actual native directory', [label, repr(path)])
        entry = {'path': path, 'entry_count': count, 'subtrees': children, 'oid': oid}
        nodes.append(entry)
        if count >= 0:
            need(count == trees[path]['count'] and oid == trees[path]['oid'], 'valid TREE native count and oid', [label, repr(path), count, oid, trees[path]['count'], trees[path]['oid']])
        for child in range(children):
            parse(path)
    parse(b'', True)
    need(pos == len(payload), 'whole TREE extension consumed', label)
    valid = [n for n in nodes if n['entry_count'] >= 0]
    request = b''.join(n['oid'].encode() + b'\n' for n in valid)
    response = git(W, 'cat-file', '--batch', data=request)
    pos = 0
    for n in valid:
        lineend = response.index(b'\n', pos)
        header = response[pos:lineend].split(b' ')
        need(len(header) == 3 and header[0].decode() == n['oid'] and header[1] == b'tree', 'cached tree object header', [label, repr(n['path']), repr(header)])
        size = int(header[2]); pos = lineend + 1
        body = response[pos:pos + size]; pos += size
        need(response[pos:pos + 1] == b'\n' and body == trees[n['path']]['body'], 'cached tree exact object bytes', [label, repr(n['path']), size])
        pos += 1
    need(pos == len(response), 'exact tree batch response consumed', label)
    return {'nodes': len(nodes), 'valid_nodes_verified': len(valid), 'valid_nodes': [{'path': os.fsdecode(n['path']), 'entry_count': n['entry_count'], 'subtrees': n['subtrees'], 'oid': n['oid']} for n in valid], 'invalidated_nodes': [{'path': os.fsdecode(n['path']), 'entry_count': n['entry_count'], 'subtrees': n['subtrees']} for n in nodes if n['entry_count'] < 0], 'native_root_tree': trees[b'']['oid']}

def main():
    prior = load(OWN / 'PRIOR_PACKETS.json')
    for packet in prior['packets']:
        root = Path(packet['root'])
        need(sorted(str(x) for x in root.iterdir()) == sorted(x['path'] for x in packet['files']) and mode(root) == packet['root_mode'], 'prior failed packet exact finite root extent', str(root))
        for item in packet['files']:
            pin(Path(item['path']), item)
    DETAILS['prior_failed_packets'] = prior
    v2root = Path(prior['packets'][1]['root'])
    v2 = load(v2root / 'AUDIT_RESULT.json')
    required_inherited = ['entire live public namespace equals actual accepted stage with only explicit root rebasing', 'public exact counts and root mode', 'all seventeen DS_Store leaves retained', 'all old 368 directory modes preserved', 'exact five new directories mode 0755', 'all 758 untouched old public leaves exact', 'exact twelve added public leaves', 'all fourteen actual target pins and modes', 'original/stage/live asset byte equality', 'six original assets authenticated']
    need(v2['schema'] == 'independent-post-publication-native-public-audit-v2' and v2['status'] == 'FAIL_STOP' and [x['check'] for x in v2['checks'] if not x['PASS']] == ['actual article and sitemap counts'], 'literal v2 failure correctly disclosed')
    for name in required_inherited:
        need(any(x['check'] == name and x['PASS'] for x in v2['checks']), 'exact successful inherited public check', name)
    DETAILS['inherited_public_evidence'] = {'source': str(v2root / 'AUDIT_RESULT.json'), 'source_literal_status': v2['status'], 'observed_started_UTC': v2['started_UTC'], 'observed_completed_UTC': v2['completed_UTC'], 'successful_check_names': required_inherited, 'public_namespace': v2['details']['public_namespace'], 'six_original_assets': v2['details']['assets'], 'ordering_diagnosis': v2['details']['v1_failure_diagnosis'], 'scope_limit': 'Inherited observed v2 local public/asset snapshot; no fresh v3 public census, no article-count claim from the failed tag counter, and no HTTP/browser/PDF claim.'}
    pin(PROD / 'PLAN.json', {'bytes': 18077, 'SHA256': 'b16e72c5c1d8e100b5234263b0be33e48176ccdac7071388aa9e024ae8fde713', 'mode': '0644'})
    pin(PROD / 'release_three.py', {'bytes': 76195, 'SHA256': '878df1fff183a407371f4b298c45d5560e6349d4b4f2dfd6bdc3a1ea1eb53cc7', 'mode': '0644'})
    plan = load(PROD / 'PLAN.json')
    for label, expected in plan['controls'].items():
        pin(Path(expected['path']), expected)
    adoption = load(Path(plan['controls']['root_stage_adoption']['path']))
    need(adoption['schema'] == 'root-private-three-stage-adoption-v1' and adoption['status'] == 'ROOT_STAGE_ACCEPTED_WITH_AUDIT_EXPECTATION_CORRECTION', 'actual root adoption schema and status')
    targets = load(STAGE / 'PUBLIC_PAYLOADS.json')['targets']
    targetmap = {os.fsencode(t['path']): t for t in targets}
    need(len(targetmap) == 14 and sorted(t['path'] for t in targets) == plan['scope_paths'], 'exact fourteen target paths')
    pin(OLDIDX, {'bytes': 9056134, 'SHA256': '6e57311ffb524aabe230dec4962ebfa6983085674882606f5b8594aa1d4cee18', 'mode': '0644'})
    oldraw, oldindex, oldext = parse_index(OLDIDX, 58700)
    newraw, newindex, newext = parse_index(W / '.git/index', 58712)
    need(len(newraw) == 9057886 and sha(newraw) == 'e6285d49b7249ae2c88a1f624ca98c1dcf480424db272c4fe111ca91dbdafb5e' and mode(W / '.git/index') == '0644', 'exact published successor native index')
    oldprotected = {k: v['raw'] for k, v in oldindex.items() if k[0] not in targetmap}
    newprotected = {k: v['raw'] for k, v in newindex.items() if k[0] not in targetmap}
    need(len(oldprotected) == 58698 and oldprotected == newprotected, 'all 58698 untargeted whole raw records byte identical including stats flags padding')
    DETAILS['native_index_before'] = {'bytes': len(oldraw), 'SHA256': sha(oldraw), 'records': len(oldindex)}
    DETAILS['native_index_after'] = {'bytes': len(newraw), 'SHA256': sha(newraw), 'records': len(newindex)}
    expectedoids = {}
    for name, t in targetmap.items():
        assetpath = STAGE / 'candidate' / t['path']
        pin(assetpath, t['candidate'])
        blob = assetpath.read_bytes()
        oid = hashlib.sha1(b'blob ' + str(len(blob)).encode() + b'\0' + blob).hexdigest()
        expectedoids[name] = oid
        need([(k, v['mode'], v['oid']) for k, v in newindex.items() if k[0] == name] == [((name, 0), '100644', oid)], 'exact new target index mode and blob oid', t['path'])
    need(git(W, 'rev-parse', 'HEAD').strip().decode() == NEW, 'current website HEAD exact published commit')
    commit = git(W, 'cat-file', 'commit', NEW)
    headers = commit.split(b'\n\n', 1)[0].split(b'\n')
    need([h for h in headers if h.startswith(b'parent ')] == [('parent ' + OLD).encode()] and headers[0] == ('tree ' + TREE).encode(), 'exact single parent and root tree')
    oldhead, newhead = leaves(OLD), leaves(NEW)
    delta = {name: {'old': oldhead.get(name), 'new': newhead.get(name)} for name in set(oldhead) | set(newhead) if oldhead.get(name) != newhead.get(name)}
    need(set(delta) == set(targetmap), 'full commit leaf delta exact fourteen paths')
    need(sum(v['old'] is None for v in delta.values()) == 12 and sum(v['old'] is not None and v['new'] is not None for v in delta.values()) == 2, 'commit exact 12 additions 2 modifications')
    need(all((name not in oldhead) == (t['action'] == 'A') for name, t in targetmap.items()), 'each commit action matches exact target plan')
    need(all(newhead[name] == ('100644', 'blob', expectedoids[name]) for name in targetmap), 'all fourteen commit target modes types and blob oids exact')
    need({k: v for k, v in oldhead.items() if k not in targetmap} == {k: v for k, v in newhead.items() if k not in targetmap}, 'all untargeted commit path mode type oid leaves exact')
    oldforeign, newforeign = staging_delta(oldindex, oldhead), staging_delta(newindex, newhead)
    need(oldforeign == newforeign, 'all foreign staging preserved relative to respective HEADs')
    DETAILS.update({'old_commit_leaves': len(oldhead), 'new_commit_leaves': len(newhead), 'foreign_staging_paths': len(oldforeign), 'foreign_staging': [{'path': os.fsdecode(name), 'old_and_new': value} for name, value in sorted(oldforeign.items())], 'commit_delta': [{'path': os.fsdecode(name), **v} for name, v in sorted(delta.items())]})
    need(len(oldext) == 1 and len(newext) == 1 and len(oldext[0][1]) == 35878 and sha(oldext[0][1]) == 'f12d2a0b795034ce5cab45ad6fa5da31b4d7ad6f4b22a5999ce27841b41350b3', 'known baseline TREE cache exact')
    need(oldext == newext, 'whole old/new TREE extension byte identity')
    DETAILS['TREE_before'] = validate_cache(oldext[0][1], oldindex, 'baseline')
    DETAILS['TREE_after'] = validate_cache(newext[0][1], newindex, 'published')
    guards = load(GUARDS)
    for label, repo in [('Math', M), ('Website', W)]:
        guard = guards[label]
        for leaf, key in [('config', 'config'), ('HEAD', 'raw_HEAD')]:
            expectedpin = {k: guard[key][k] for k in ('bytes', 'SHA256')}
            expectedpin['mode'] = format(int(guard[key]['mode'], 8), '04o')
            pin(repo / '.git' / leaf, expectedpin)
        if label == 'Math':
            expectedpin = {k: guard['index'][k] for k in ('bytes', 'SHA256')}
            expectedpin['mode'] = format(int(guard['index']['mode'], 8), '04o')
            pin(repo / '.git/index', expectedpin)
            need(git(repo, 'rev-parse', 'HEAD').strip().decode() == guard['HEAD'], 'Math native HEAD unchanged')
        refs = git(repo, 'for-each-ref', '--format=%(refname) %(objectname)', 'refs/heads').decode().strip().splitlines()
        expectedrefs = guard['local_heads'].splitlines()
        if label == 'Website':
            refs = [x for x in refs if not x.startswith('refs/heads/master ')]
            expectedrefs = [x for x in expectedrefs if not x.startswith('refs/heads/master ')]
        need(refs == expectedrefs, 'local heads unchanged except website master', label)
    for config in plan['configuration_guards']:
        pin(Path(config['path']), config)

if __name__ == '__main__':
    error = None
    try:
        main()
    except BaseException:
        error = traceback.format_exc()
    end = datetime.datetime.now(datetime.timezone.utc).isoformat()
    status = 'PASS' if error is None else 'FAIL_STOP'
    result = {'schema': 'independent-post-publication-native-audit-v3', 'status': status, 'started_UTC': START, 'completed_UTC': end, 'published_commit': NEW, 'checks': CHECKS, 'assertion_observations': sum(x['observations'] for x in CHECKS), 'details': DETAILS, 'literal_error': error, 'utility_invocations': 1, 'helper_invocations': 0, 'network_actions': 0, 'writes_outside_own_lane': 0, 'completion_percent': 100 if error is None else 65, 'limits': ['Observed local snapshots only; no claim of future persistence or concurrent-process exclusion.', 'No fresh scientific proof review, priority determination, live deployment, browser/mobile layout, PDF rendering, live download or network verification.', 'No helper execution, index refresh, write-tree, object/ref/index mutation, source-program execution, Sheet or AA changes, redirect work or external contact.']}
    (OWN / 'AUDIT_RESULT.json').write_text(json.dumps(result, indent=2) + '\n')
    (OWN / 'REPORT.md').write_text('# Independent native-first post-publication audit\n\n' + status + ': commit `' + NEW + '`.\n\n' + str(len(CHECKS)) + ' recorded check groups and ' + str(result['assertion_observations']) + ' assertion observations; literal error: ' + ('none' if error is None else 'retained in AUDIT_RESULT.json') + '.\n\nFresh scope: raw native index records, TREE cache semantics and local object bytes, old/new commit leaves, foreign staging and native repository guards. Complete public772/373 and six-original-asset checks are inherited from pinned v2 successful check groups; v1 and v2 literal FAIL_STOP results remain unchanged. V3 makes no article-count assertion.\n\nCompletion estimate: ' + str(result['completion_percent']) + '%.\n\n' + '\n'.join('- ' + s for s in result['limits']) + '\n')
    with (OWN / 'RESEARCH_LOG.md').open('a') as log:
        log.write('\n' + end + ' — Sole audit invocation completed with ' + status + '; ' + str(len(CHECKS)) + ' recorded checks. Completion estimate ' + str(result['completion_percent']) + '%. Literal errors retained without retry.\n')
    print(json.dumps({'schema': result['schema'], 'status': status, 'checks': len(CHECKS), 'literal_error': error, 'completion_percent': result['completion_percent']}))
    sys.exit(0 if error is None else 1)
