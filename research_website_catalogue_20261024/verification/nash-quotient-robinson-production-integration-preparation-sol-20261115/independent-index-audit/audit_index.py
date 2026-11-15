"""Read-only inventory of the existing website index; writes JSON to stdout only."""
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import os
import struct
import subprocess

W = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
S = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/verification/nash-quotient-robinson-private-stage-sol-20261115')
BASE = 'e2e064c48755452a56c2a31207fb12d7e55074fb'
SEAL = 'e0bb4ec8ae90cf48e0d71f9e66b723f65403d743610d5477916f7dda6a6a00e9'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def git(*args):
    env = {key: value for key, value in os.environ.items()
           if not key.startswith('GIT_')}
    env['GIT_OPTIONAL_LOCKS'] = '0'
    result = subprocess.run(['git', '-c', 'gc.auto=0', '-c', 'core.fsmonitor=false',
                             '-c', 'core.untrackedCache=false', *args],
                            cwd=W, env=env, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    need(result.returncode == 0, result.stderr.decode('utf8', 'replace'))
    return result.stdout


def parse_v2(raw):
    need(len(raw) >= 32, 'truncated index')
    magic, version, count = struct.unpack('!4sII', raw[:12])
    need(magic == b'DIRC' and version == 2, 'only DIRC v2 supported by this audit')
    need(hashlib.sha1(raw[:-20]).digest() == raw[-20:], 'index checksum')
    entries = []
    offset = 12
    for _ in range(count):
        start = offset
        need(start + 62 < len(raw) - 20, 'truncated entry')
        flags = struct.unpack('!H', raw[start+60:start+62])[0]
        need(not flags & 0x4000, 'unexpected extended flags in v2')
        nul = raw.index(b'\0', start+62, len(raw)-20)
        path = raw[start+62:nul]
        end = start + ((nul + 1 - start + 7) // 8 * 8)
        need(end <= len(raw)-20 and not any(raw[nul:end]), 'entry padding')
        need((flags & 0xfff) == min(len(path), 0xfff), 'path length flag')
        need(path and not path.startswith(b'/') and b'..' not in path.split(b'/'), 'path safety')
        entries.append({'path': path, 'stage': (flags >> 12) & 3,
                        'flags': flags, 'mode': struct.unpack('!I', raw[start+24:start+28])[0],
                        'object': raw[start+40:start+60], 'raw': raw[start:end]})
        offset = end
    keys = [(entry['path'], entry['stage']) for entry in entries]
    need(keys == sorted(keys) and len(keys) == len(set(keys)), 'sorted unique entries')
    extensions = []
    while offset < len(raw)-20:
        need(offset+8 <= len(raw)-20, 'truncated extension header')
        signature = raw[offset:offset+4]
        length = struct.unpack('!I', raw[offset+4:offset+8])[0]
        end = offset+8+length
        need(end <= len(raw)-20, 'truncated extension payload')
        extensions.append({'signature': signature.decode('ascii'), 'length': length,
                           'payload_SHA256': sha(raw[offset+8:end]),
                           'header_and_payload_SHA256': sha(raw[offset:end])})
        offset = end
    need(offset == len(raw)-20, 'extension boundary')
    return entries, extensions


def main():
    stage_seal = sha((S/'FINAL_SEAL.json').read_bytes())
    need(stage_seal == SEAL, 'stage seal changed')
    overlay_raw = (S/'OVERLAY_MANIFEST.json').read_bytes()
    overlay = json.loads(overlay_raw)['files']
    targets = {('public/'+row['path']).encode('ascii') for row in overlay}
    need(len(overlay) == len(targets) == 14, 'exact14 targets')
    index = W/'.git/index'
    before = index.read_bytes()
    entries, extensions = parse_v2(before)
    protected = [entry for entry in entries if entry['path'] not in targets]
    tuples = [row for row in git('ls-files', '--stage', '-z').split(b'\0') if row]
    protected_tuples = [row for row in tuples if row.split(b'\t', 1)[1] not in targets]
    status = [row for row in git('status', '--porcelain=v2', '-z', '--untracked-files=no').split(b'\0') if row]
    branch = git('symbolic-ref', '-q', 'HEAD').decode().strip()
    head = git('rev-parse', 'HEAD').decode().strip()
    need(branch == 'refs/heads/master' and head == BASE, 'fresh baseline changed')
    config = git('config', '--show-origin', '--get-regexp',
                 r'^(core\.(ignorecase|filemode|symlinks|splitindex|fsmonitor|untrackedcache|sparsecheckout|sparsecheckoutcone|precomposeunicode|hooksPath)|index\.|extensions\.|filter\.)').decode()
    public = W/'public'
    baseline = json.loads((S/'WEBSITE_BASELINE.json').read_bytes())
    need([baseline['public_count'], baseline['index_count'], baseline['sitemap_count']] == [593, 87, 88], 'sealed baseline counts')
    need(before == index.read_bytes(), 'concurrent index mutation during read-only audit')
    print(json.dumps({
        'UTC': datetime.now(timezone.utc).isoformat(),
        'status': 'PASS_READ_ONLY_INDEX_INVENTORY', 'completion_percent_this_audit': 100,
        'website': str(W), 'branch': branch, 'HEAD': head,
        'stage_FINAL_SEAL_SHA256': stage_seal, 'OVERLAY_MANIFEST_SHA256': sha(overlay_raw),
        'overlay_target_count': len(targets), 'baseline_counts': [593, 87, 88],
        'public_file_count_fresh': sum(p.is_file() for p in public.rglob('*')),
        'public_symlink_count': sum(p.is_symlink() for p in public.rglob('*')),
        'index_path': str(index), 'gitdir_is_directory': (W/'.git').is_dir(),
        'object_format': git('rev-parse', '--show-object-format').decode().strip(),
        'index_version': 2, 'index_bytes': len(before), 'index_SHA256': sha(before),
        'index_record_count': len(entries), 'protected_record_count_excluding14': len(protected),
        'protected_tuple_records_SHA256': sha(b'\0'.join(protected_tuples)+b'\0'),
        'protected_raw_entry_bytes_SHA256': sha(b''.join(entry['raw'] for entry in protected)),
        'protected_path_stage_keys_SHA256': sha(b''.join(entry['path']+b'\0'+str(entry['stage']).encode()+b'\0' for entry in protected)),
        'stage_histogram': dict(Counter(entry['stage'] for entry in entries)),
        'high_flag_bits_histogram': dict(Counter(hex(entry['flags'] & ~0xfff) for entry in entries)),
        'mode_histogram': dict(Counter(oct(entry['mode']) for entry in entries)),
        'non_ascii_path_count': sum(any(c > 127 for c in entry['path']) for entry in entries),
        'extensions': extensions,
        'target_existing_records': [{'path': entry['path'].decode(), 'stage': entry['stage'],
                                     'mode': oct(entry['mode']), 'object': entry['object'].hex(),
                                     'raw_entry_SHA256': sha(entry['raw'])}
                                    for entry in entries if entry['path'] in targets],
        'index_lock_exists': (W/'.git/index.lock').exists(),
        'split_index_files': [p.name for p in (W/'.git').glob('sharedindex.*')],
        'sparse_checkout_file_exists': (W/'.git/info/sparse-checkout').exists(),
        'config_relevant_read_only': config,
        'status_record_count': len(status),
        'status_xy_histogram': dict(Counter(row.split(b' ', 2)[1].decode() for row in status if row[:1] in (b'1', b'2'))),
        'cached_diff_raw_SHA256': sha(git('diff', '--cached', '--raw', '-z', '--no-abbrev', 'HEAD')),
        'read_only_operations': True, 'remote_checked': False,
        'website_or_Git_mutations_performed': False,
        'scientific_review_performed': False,
        'root_stage_adoption_evidence_available_to_auditor': False
    }, indent=2))


if __name__ == '__main__':
    main()
