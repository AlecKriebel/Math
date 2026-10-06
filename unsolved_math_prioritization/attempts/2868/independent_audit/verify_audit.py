#!/usr/bin/env python3
"""Replay exact artifact acceptance. This program does not prove any topology."""
import argparse
import hashlib
import io
import json
import pathlib
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile

AUTHOR_ZIP = 'KNOT_SURGERY_2868_AUTHOR_SAFE_FREEZE.zip'
AUTHOR_EXTERNAL = 'KNOT_SURGERY_2868_AUTHOR_EXTERNAL_MANIFEST.json'
AUTHOR_PINS = {
    AUTHOR_ZIP: (11525, 'c3b899805315796d6023af73be74d7133f354703447cfe85dc2b5506ccf09b8d'),
    AUTHOR_EXTERNAL: (2207, '886febe0cac1758af13791337f7175a446b9ca0e4c4692909867a4982e0116ef'),
}
AUTHOR_FILES = frozenset(('ATTEMPT_LOG.md', 'INPUT_VERIFICATION.json', 'MANIFEST.json',
                         'README.md', 'REPORT.md', 'SOURCE_METADATA.json', 'STATUS.json',
                         'verify_release.py'))
AUDIT_FILES = frozenset((AUTHOR_ZIP, AUTHOR_EXTERNAL, 'README.md', 'AUDIT_REPORT.md',
                        'ACCEPTANCE.json', 'INPUT_VERIFICATION.json', 'SOURCE_VERIFICATION.json',
                        'HISTORY_VERIFICATION.json', 'REPLAY_RESULTS.json', 'verify_audit.py', 'independent_controls.py',
                        'MANIFEST.json'))
CONTROLS = ['changed_report', 'missing_metadata', 'unexpected_file', 'rehashed_solved_claim',
            'duplicate_json_key', 'unsafe_manifest_path', 'symlink_member']
CORPUS_PINS = {
 'catalog': (21735099, '891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566'),
 'problems': (68931837, '04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf'),
 'reports': (80334822, '8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b'),
}
STATEMENT = 'a2c03a6a84ff58dcf8addd47eb50432b6e2de7edf663d55c47521af103df36d4'
PAIR = '975b7dad9094fdaba765311a9d0f3891c4c3bb8f00b0ccab2fa4029b61a7f3fe'
class Rejected(Exception):
    pass

def need(ok, why):
    if not ok:
        raise Rejected(why)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def unique(pairs):
    value = {}
    for k, v in pairs:
        need(k not in value, 'duplicate JSON key')
        value[k] = v
    return value

def read_json(data):
    return json.loads(data.decode('utf-8'), object_pairs_hook=unique,
                      parse_constant=lambda _: (_ for _ in ()).throw(Rejected('nonfinite JSON')))

def pinned(data, pin, label):
    need((len(data), sha(data)) == pin, label + ' external pin mismatch')

def inspect_archive(data, external):
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        infos = z.infolist()
        need(len(infos) == len(AUTHOR_FILES), 'archive member count')
        need(len({i.filename for i in infos}) == len(infos), 'duplicate ZIP member')
        need({i.filename for i in infos} == AUTHOR_FILES, 'archive member set')
        need(z.testzip() is None, 'archive CRC')
        out = {}
        for i in infos:
            need(not i.is_dir() and '/' not in i.filename and '\\' not in i.filename,
                 'unsafe archive path')
            mode = (i.external_attr >> 16) & 0xFFFF
            need(stat.S_IFMT(mode) in (0, stat.S_IFREG), 'nonregular ZIP member')
            need(not i.flag_bits & 1, 'encrypted ZIP member')
            need(i.file_size <= 100000, 'oversized ZIP member')
            b = z.read(i)
            row = external['members'][i.filename]
            pinned(b, (row['bytes'], row['sha256']), i.filename)
            out[i.filename] = b
    inner = read_json(out['MANIFEST.json'])
    need(inner['schema_version'] == 1 and inner['problem_id'] == 2868, 'inner identity')
    need(set(inner['files']) == AUTHOR_FILES - {'MANIFEST.json'}, 'inner member set')
    for n, r in inner['files'].items():
        pinned(out[n], (r['bytes'], r['sha256']), 'inner ' + n)
    im = external['internal_manifest']
    pinned(out['MANIFEST.json'], (im['bytes'], im['sha256']), 'inner manifest')
    status = read_json(out['STATUS.json'])
    need(status['status'] == 'stalled_partial' and status['turns_used'] == 3 and
         status['turn_limit'] == 5 and status['rank'] == 915, 'conservative status')
    need(all(status[k] is False for k in ('full_problem_solved','full_problem_refuted','novelty_claim')),
         'mathematical overclaim')
    return out

def author_check(root):
    for n, p in AUTHOR_PINS.items():
        need((root/n).is_file() and not (root/n).is_symlink(), 'missing or linked author input')
        pinned((root/n).read_bytes(), p, n)
    external = read_json((root/AUTHOR_EXTERNAL).read_bytes())
    need(set(external['members']) == AUTHOR_FILES, 'external member set')
    return inspect_archive((root/AUTHOR_ZIP).read_bytes(), external)

def replay(root):
    members = author_check(root)
    runs = []
    for label, optimized in [('normal',False), ('optimized',True),
                             ('relocated_normal',False), ('relocated_optimized',True)]:
        with tempfile.TemporaryDirectory(prefix='audit-2868-') as tmp:
            base = pathlib.Path(tmp)
            packet = base / ('nested/unrelated/packet' if label.startswith('relocated') else 'packet')
            packet.mkdir(parents=True)
            for n, b in members.items():
                (packet/n).write_bytes(b)
            cwd = base/'unrelated_working_directory'; cwd.mkdir()
            cmd = [sys.executable, '-B'] + (['-O'] if optimized else [])
            cmd += [str(packet/'verify_release.py'), '--self-test']
            p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=30)
            need(p.returncode == 0, label + ' failed: ' + p.stderr)
            result = json.loads(p.stdout)
            need(result == {'result':'PASS_PACKAGE_INTEGRITY_ONLY','problem_id':2868,
                            'bound_files':7,'mathematical_proof_certified':False,
                            'source_pdfs_in_package':False,'rejected_negative_controls':CONTROLS},
                 'unexpected author result')
            need({x.name for x in packet.iterdir()} == AUTHOR_FILES, 'replay added a member')
            for n, b in members.items():
                need((packet/n).read_bytes() == b, 'replay mutated member')
            runs.append({'mode':label,'exit_code':0,'rejected_negative_controls':CONTROLS,
                         'result':'PASS_PACKAGE_INTEGRITY_ONLY','all_members_unchanged':True})
    return {'result':'PASS_EXACT_AUTHOR_REPLAYS','runs':runs,'normal_optimized_relocated_equal':True}

def full_inputs(paths):
    datasets = {}
    for role, p in zip(('catalog','problems','reports'), paths):
        b = pathlib.Path(p).read_bytes(); pinned(b, CORPUS_PINS[role], role)
        datasets[role] = read_json(b)
    rs = [r for r in datasets['problems'] if r['id'] == 2868]
    cs = [r for r in datasets['catalog'] if str(r['id']) == '2868']
    need(len(rs) == len(cs) == 1, 'exact identity uniqueness')
    r, c = rs[0], cs[0]; report = datasets['reports'].get(r['problem_number'], {})
    need(r['problem_number'] == c['problem_number'] == 'KP-3.70' and c['rank'] == 915,
         'record identity')
    need(sha(r['statement'].encode()) == c['statement_hash'] == STATEMENT, 'statement digest')
    need(sha(json.dumps([r,report],sort_keys=True).encode()) == c['review_hash'] == PAIR,
         'complete record-report pair digest')
    need(report == {}, 'nonempty inherited report')
    return 'PASS_FULL_CORPUS_AND_COMPLETE_PAIR'

def source_pdfs(directory, root):
    rows = read_json((root/'SOURCE_VERIFICATION.json').read_bytes())['sources']
    for row in rows:
        b = (pathlib.Path(directory)/(row['id']+'.pdf')).read_bytes()
        pinned(b,(row['bytes'],row['sha256']),row['id']+' PDF')
        need(b.startswith(b'%PDF-'), 'PDF signature')
    return 'PASS_THREE_PINNED_SOURCE_PDFS'

def packet_check(root, expected):
    need(root.is_dir() and not root.is_symlink(), 'invalid audit root')
    need({p.name for p in root.iterdir()} == AUDIT_FILES, 'audit member set')
    need(all(p.is_file() and not p.is_symlink() for p in root.iterdir()), 'audit nonregular member')
    b = (root/'MANIFEST.json').read_bytes()
    need(sha(b) == expected, 'audit manifest external pin mismatch')
    m = read_json(b)
    need(m['problem_id'] == 2868 and m['schema_version'] == 1, 'audit manifest identity')
    need(set(m['files']) == AUDIT_FILES-{'MANIFEST.json'}, 'audit manifest member set')
    for n, row in m['files'].items():
        pinned((root/n).read_bytes(),(row['bytes'],row['sha256']),n)
    acceptance = read_json((root/'ACCEPTANCE.json').read_bytes())
    need(acceptance['verdict'] == 'ACCEPT_UNCHANGED_STALLED_PARTIAL', 'acceptance verdict')
    need(acceptance['full_problem_solved'] is False and acceptance['novelty_claim'] is False,
         'acceptance overclaim')
    author_check(root)
    return True

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--expected-manifest-sha256',required=True)
    p.add_argument('--full-inputs',nargs=3,metavar=('CATALOG','PROBLEMS','REPORTS'))
    p.add_argument('--source-dir')
    a = p.parse_args(); root = pathlib.Path(__file__).absolute().parent
    try:
        packet_check(root,a.expected_manifest_sha256)
        result = replay(root)
        cmd = [sys.executable, '-B'] + (['-O'] if sys.flags.optimize else []) + [str(root/'independent_controls.py')]
        control_run = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        need(control_run.returncode == 0, 'independent controls failed: ' + control_run.stderr)
        controls = json.loads(control_run.stdout)
        need(len(controls['independent_negative_controls']) == 11 and
             all(c['result'] == 'REJECTED' for c in controls['independent_negative_controls']),
             'independent controls incomplete')
        result['independent_negative_controls'] = controls['independent_negative_controls']
        result['audit_packet'] = 'PASS_EXTERNALLY_PINNED_AUDIT'
        result['mathematical_proof_certified'] = False
        result['current_corpus_rehash'] = full_inputs(a.full_inputs) if a.full_inputs else 'NOT_REQUESTED'
        result['current_source_pdf_rehash'] = source_pdfs(a.source_dir,root) if a.source_dir else 'NOT_REQUESTED'
        print(json.dumps(result,indent=2,sort_keys=True))
        return 0
    except (Rejected, OSError, ValueError, KeyError, TypeError, zipfile.BadZipFile,
            subprocess.SubprocessError) as e:
        print('FAIL: '+str(e),file=sys.stderr)
        return 1
if __name__ == '__main__':
    sys.exit(main())
