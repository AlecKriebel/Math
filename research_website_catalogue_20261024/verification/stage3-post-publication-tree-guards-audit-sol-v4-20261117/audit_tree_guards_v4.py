#!/usr/bin/env python3
"""Fresh read-only TREE/native-guards audit; no prior auditor/helper is run.

Earlier literal failures stay immutable. Inherit successful v2 public and v3
native-core checks only after authenticating every file in their finite packets.
The TREE whole extension includes its eight-byte header; parse only its payload.
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
OWN = P / 'verification/stage3-post-publication-tree-guards-audit-sol-v4-20261117'
OLDIDX = P / 'verification/wreath-dyadic-stress-runtime-root-v3-20261117/install/63e3fc9e7a3ec74f92eb0124f171bc90725519976119663ca5dfb6fb450a5a91/native-backups/index.before'
GUARDS = P / 'verification/checkpoint-v3-installed-sources188189-initials-20261117/NATIVE_GUARDS_BEFORE.json'
OLD = 'b767102567ad89aff909f9f11c0e8b7d72b75c40'
NEW = '96f04aa5544df69daba07a9ed4d6212172e9984a'
CHECKS, DETAILS = [], {}
GROUPS = {}
START = datetime.datetime.now(datetime.timezone.utc).isoformat()

def need(ok, name, details=None):
    if name not in GROUPS:
        GROUPS[name] = {'check': name, 'PASS': True, 'observations': 0, 'details': details}
        CHECKS.append(GROUPS[name])
    group = GROUPS[name]
    group['observations'] += 1
    if not ok:
        group.update({'PASS': False, 'details': details})
        raise AssertionError(name + ': ' + repr(details))

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def mode(path):
    return format(stat.S_IMODE(path.lstat().st_mode), '04o')

def pin(path, expected):
    need(stat.S_ISREG(path.lstat().st_mode), 'pinned input regular file', str(path))
    raw = path.read_bytes()
    actual = {'bytes': len(raw), 'SHA256': sha(raw), 'mode': mode(path)}
    need(actual == {key: expected[key] for key in actual}, 'exact whole-file pin', {'path': str(path), 'actual': actual})
    return actual

def load(path):
    return json.loads(path.read_bytes())

def git(repo, *args):
    need(args and args[0] in {'rev-parse', 'for-each-ref', 'ls-tree', 'cat-file'}, 'readonly Git allowlist', list(args))
    env = {key: value for key, value in os.environ.items() if not key.startswith('GIT_')}
    env.update({'GIT_OPTIONAL_LOCKS': '0', 'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': '/dev/null', 'GIT_NO_REPLACE_OBJECTS': '1', 'LC_ALL': 'C'})
    run = subprocess.run(['/usr/bin/git', '--no-optional-locks', '-c', 'core.hooksPath=/dev/null', '-c', 'core.fsmonitor=false', '-C', str(repo), *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, timeout=120)
    need(run.returncode == 0 and run.stderr == b'', 'readonly Git successful literal result', {'args': list(args), 'code': run.returncode, 'stderr': run.stderr.decode(errors='backslashreplace')})
    return run.stdout

def index_data(path, count):
    raw = path.read_bytes()
    need(raw[:4] == b'DIRC' and struct.unpack('>II', raw[4:12]) == (2, count) and hashlib.sha1(raw[:-20]).digest() == raw[-20:], 'bound v2 native index header checksum count', str(path))
    pos, records, counts = 12, {}, {b'': 0}
    for number in range(count):
        start = pos
        need(pos + 62 < len(raw) - 20, 'native entry bounds', number)
        flags = struct.unpack('>H', raw[pos + 60:pos + 62])[0]
        need(not (flags & 0x7000), 'native entries resolved stage zero without extended flag', number)
        end = raw.index(b'\0', pos + 62, len(raw) - 20)
        name = raw[pos + 62:end]
        need(name and name not in records, 'unique nonempty native path', repr(name))
        mod = format(struct.unpack('>I', raw[pos + 24:pos + 28])[0], 'o')
        oid = raw[pos + 40:pos + 60].hex()
        records[name] = (mod, oid)
        parts = name.split(b'/')
        for length in range(len(parts)):
            prefix = b'/'.join(parts[:length])
            counts[prefix] = counts.get(prefix, 0) + 1
        pos = end + 1
        pos += (-(pos - start)) % 8
        need(raw[end:pos] == b'\0' * (pos - end), 'native entry padding preserved', number)
    whole = raw[pos:-20]
    need(len(whole) == 35878 and sha(whole) == 'f12d2a0b795034ce5cab45ad6fa5da31b4d7ad6f4b22a5999ce27841b41350b3', 'whole TREE extension including header exact pin', str(path))
    need(whole[:4] == b'TREE' and struct.unpack('>I', whole[4:8])[0] == 35870 and len(whole) == 8 + struct.unpack('>I', whole[4:8])[0], 'known single TREE extension no unknown extension', str(path))
    payload = whole[8:]
    need(len(payload) == 35870 and sha(payload) == '6078bbaef4d39e7b0418bc6ed44ad8f37d2733ec6de4a4e4ba165fe7e665bfcb', 'TREE payload convention exact pin', str(path))
    return records, counts, whole, payload

def object_trees(commit, records):
    commitraw = git(W, 'cat-file', 'commit', commit)
    rootline = commitraw.split(b'\n', 1)[0]
    need(re.fullmatch(rb'tree [0-9a-f]{40}', rootline) is not None, 'commit root tree syntax', commit)
    directories = {b'': rootline[5:].decode()}
    leaves = {}
    for row in git(W, 'ls-tree', '-r', '-t', '-z', '--full-tree', commit).split(b'\0'):
        if not row:
            continue
        meta, name = row.split(b'\t', 1)
        mod, kind, oid = meta.split(b' ')
        if kind == b'tree':
            need(mod == b'040000' and name not in directories, 'unique native tree path from readonly Git objects', repr(name))
            directories[name] = oid.decode()
        else:
            need(name not in leaves and kind in (b'blob', b'commit'), 'unique Git object leaf path', repr(name))
            leaves[name] = (mod.decode(), oid.decode())
    need(leaves == records, 'all native index leaf modes and OIDs match corresponding commit objects for TREE semantics', commit)
    return directories

def cache_nodes(payload, counts, directories, label):
    pos, seen, nodes = 0, set(), []
    def parse(parent, root=False):
        nonlocal pos
        end = payload.index(b'\0', pos)
        name = payload[pos:end]
        need((root and name == b'') or (not root and name and b'/' not in name and name not in (b'.', b'..')), 'TREE cached local node name', [label, repr(name)])
        lineend = payload.index(b'\n', end + 1)
        numbers = payload[end + 1:lineend]
        need(re.fullmatch(rb'-?[0-9]+ [0-9]+', numbers) is not None, 'TREE cached numeric syntax', [label, repr(numbers)])
        entries, children = map(int, numbers.split(b' '))
        need(entries >= -1 and children <= len(directories), 'TREE cached counts valid bounds', [label, entries, children])
        pos = lineend + 1
        oid = None
        if entries >= 0:
            need(pos + 20 <= len(payload), 'valid TREE cached OID bytes bounded', label)
            oid = payload[pos:pos + 20].hex()
            pos += 20
        path = (parent + (b'/' if parent else b'') + name) if not root else b''
        need(path not in seen and path in counts and path in directories, 'TREE cached path unique actual native and object directory', [label, repr(path)])
        seen.add(path)
        node = {'path': os.fsdecode(path), 'entry_count': entries, 'subtrees': children, 'oid': oid, 'native_descendant_entries': counts[path], 'actual_object_tree_OID': directories[path]}
        if entries >= 0:
            need(entries == counts[path] and oid == directories[path], 'every valid cached TREE node exact native count and readonly object OID', [label, node])
            node['classification'] = 'VALID_COUNT_PATH_OID_VERIFIED'
        else:
            need(oid is None, 'invalidated TREE node carries no OID', [label, node])
            node['classification'] = 'EXPLICITLY_INVALIDATED_MINUS_ONE_NO_OID_PREEXISTING_CACHE'
        nodes.append(node)
        for child in range(children):
            parse(path)
    parse(b'', True)
    need(pos == len(payload), 'complete TREE payload recursion consumed', label)
    return {'nodes': len(nodes), 'valid_nodes_verified': sum(n['entry_count'] >= 0 for n in nodes), 'invalidated_nodes': [n for n in nodes if n['entry_count'] < 0], 'all_nodes': nodes}

def main():
    prior = load(OWN / 'PRIOR_PACKETS.json')
    for packet in prior['packets']:
        root = Path(packet['root'])
        need(sorted(str(x) for x in root.iterdir()) == sorted(x['path'] for x in packet['files']) and mode(root) == packet['root_mode'], 'prior packet exact finite extent and root mode', str(root))
        for item in packet['files']:
            pin(Path(item['path']), item)
    DETAILS['prior_packets'] = prior
    v2 = load(Path(prior['packets'][1]['root']) / 'AUDIT_RESULT.json')
    v3 = load(Path(prior['packets'][2]['root']) / 'AUDIT_RESULT.json')
    need(v2['schema'] == 'independent-post-publication-native-public-audit-v2' and v2['status'] == 'FAIL_STOP' and v3['schema'] == 'independent-post-publication-native-audit-v3' and v3['status'] == 'FAIL_STOP', 'all inherited literal failure statuses disclosed')
    need([x['check'] for x in v3['checks'] if not x['PASS']] == ['known baseline TREE cache exact'], 'precise v3 representation failure inherited')
    required = ['native index trailing checksum', 'native v2 record count', 'all 58698 untargeted whole raw records byte identical including stats flags padding', 'exact new target index mode and blob oid', 'full commit leaf delta exact fourteen paths', 'commit exact 12 additions 2 modifications', 'all fourteen commit target modes types and blob oids exact', 'all untargeted commit path mode type oid leaves exact', 'all foreign staging preserved relative to respective HEADs']
    need(all(any(x['check'] == name and x['PASS'] for x in v3['checks']) for name in required) and v3['details']['foreign_staging_paths'] == 0, 'exact inherited native core successful groups and zero foreign staging')
    DETAILS['inherited_native_core'] = {'source_schema': v3['schema'], 'source_status': v3['status'], 'started_UTC': v3['started_UTC'], 'completed_UTC': v3['completed_UTC'], 'successful_groups': required, 'index_before': v3['details']['native_index_before'], 'index_after': v3['details']['native_index_after'], 'old_commit_leaves': v3['details']['old_commit_leaves'], 'new_commit_leaves': v3['details']['new_commit_leaves'], 'foreign_staging_paths': 0, 'commit_delta': v3['details']['commit_delta']}
    DETAILS['inherited_public'] = v3['details']['inherited_public_evidence']
    pin(OLDIDX, {'bytes': 9056134, 'SHA256': '6e57311ffb524aabe230dec4962ebfa6983085674882606f5b8594aa1d4cee18', 'mode': '0644'})
    pin(W / '.git/index', {'bytes': 9057886, 'SHA256': 'e6285d49b7249ae2c88a1f624ca98c1dcf480424db272c4fe111ca91dbdafb5e', 'mode': '0644'})
    guards = load(GUARDS)
    DETAILS['native_guards'] = {}
    for label, repo in [('Math', M), ('Website', W)]:
        guard, observed = guards[label], {}
        for leaf, key in [('config', 'config'), ('HEAD', 'raw_HEAD')]:
            expected = {k: guard[key][k] for k in ('bytes', 'SHA256')}
            expected['mode'] = format(int(guard[key]['mode'], 8), '04o')
            observed[leaf] = pin(repo / '.git' / leaf, expected)
        if label == 'Math':
            expected = {k: guard['index'][k] for k in ('bytes', 'SHA256')}
            expected['mode'] = format(int(guard['index']['mode'], 8), '04o')
            observed['index'] = pin(repo / '.git/index', expected)
        expectedhead = guard['HEAD'] if label == 'Math' else NEW
        observed['resolved_HEAD'] = git(repo, 'rev-parse', 'HEAD').strip().decode()
        need(observed['resolved_HEAD'] == expectedhead, 'native HEAD exact Math baseline or website published commit', [label, observed['resolved_HEAD']])
        observed['local_heads'] = git(repo, 'for-each-ref', '--format=%(refname) %(objectname)', 'refs/heads').decode().strip().splitlines()
        expectedheads = guard['local_heads'].splitlines()
        if label == 'Website':
            expectedheads = [('refs/heads/master ' + NEW) if x.startswith('refs/heads/master ') else x for x in expectedheads]
        need(observed['local_heads'] == expectedheads, 'all local heads unchanged with only exact website master successor', label)
        DETAILS['native_guards'][label] = observed
    oldrecords, oldcounts, oldwhole, oldpayload = index_data(OLDIDX, 58700)
    newrecords, newcounts, newwhole, newpayload = index_data(W / '.git/index', 58712)
    need(oldwhole == newwhole, 'baseline and published whole TREE extension bytes identical')
    DETAILS['TREE_conventions'] = {'whole_bytes': len(newwhole), 'whole_SHA256': sha(newwhole), 'header_signature': 'TREE', 'header_payload_length': 35870, 'payload_bytes': len(newpayload), 'payload_SHA256': sha(newpayload)}
    DETAILS['TREE_before'] = cache_nodes(oldpayload, oldcounts, object_trees(OLD, oldrecords), 'baseline')
    DETAILS['TREE_after'] = cache_nodes(newpayload, newcounts, object_trees(NEW, newrecords), 'published')

if __name__ == '__main__':
    error = None
    try:
        main()
    except BaseException:
        error = traceback.format_exc()
    end = datetime.datetime.now(datetime.timezone.utc).isoformat()
    status = 'PASS' if error is None else 'FAIL_STOP'
    result = {'schema': 'independent-post-publication-tree-native-guards-audit-v4', 'status': status, 'started_UTC': START, 'completed_UTC': end, 'published_commit': NEW, 'checks': CHECKS, 'assertion_observations': sum(x['observations'] for x in CHECKS), 'details': DETAILS, 'literal_error': error, 'v4_invocations': 1, 'retained_old_auditor_invocations': [1, 1, 1], 'helper_invocations': 0, 'network_actions': 0, 'outside_own_lane_writes': 0, 'completion_percent': 100 if error is None else 90, 'fresh_scope': 'TREE conventions, every valid cached node count/path/object OID, invalidated nodes and native Math/website guards', 'inherited_scope': 'Pinned successful v2 public772/373 and sixassets; pinned successful v3 nativecore; all prior literal FAIL_STOP results retained', 'limits': ['Observed local snapshots; no future-persistence or global-concurrency certificate.', 'Public/asset observations inherited from v2, not freshly recounted here; no article-count assertion from the failed tag counter.', 'No fresh scientific, priority, deployment, HTTP, browser/mobile, PDF rendering or live-download certificate.', 'No prior auditor/helper/source execution, AST/compiler/tests, Git index/ref/object mutation, network, Sheet/AA/redirect work or external contact.']}
    (OWN / 'AUDIT_RESULT.json').write_text(json.dumps(result, indent=2) + '\n')
    (OWN / 'REPORT.md').write_text('# Independent TREE and native guards audit\n\n' + status + ': commit `' + NEW + '`.\n\nFresh scope: ' + result['fresh_scope'] + '.\n\nInherited scope: ' + result['inherited_scope'] + '.\n\n' + str(len(CHECKS)) + ' check groups; ' + str(result['assertion_observations']) + ' assertion observations. Completion estimate ' + str(result['completion_percent']) + '%. Literal error: ' + ('none' if error is None else 'retained in AUDIT_RESULT.json') + '.\n\n' + '\n'.join('- ' + x for x in result['limits']) + '\n')
    with (OWN / 'RESEARCH_LOG.md').open('a') as log:
        log.write('\n' + end + ' — Sole v4 invocation completed ' + status + ', ' + str(len(CHECKS)) + ' groups; completion estimate ' + str(result['completion_percent']) + '%. All earlier failures unchanged; no retry.\n')
    print(json.dumps({'schema': result['schema'], 'status': status, 'checks': len(CHECKS), 'literal_error': error, 'completion_percent': result['completion_percent']}))
    sys.exit(0 if error is None else 1)
