"""Externally authenticate this file before execution. Standard library only."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode):
    raise SystemExit('REFUSED: Python -I -S -B required')
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import tempfile
import zipfile

PINS = {'CONNECTED_SUM_30002054_AUTHOR_BOOTSTRAP.py': (1696, 'c1049c5196cf5103c707cca5a5a0ec30773f806eadfb67cc6e8bf76d1cd803cf'), 'CONNECTED_SUM_30002054_AUTHOR_EXTERNAL_MANIFEST.json': (1318, 'd2289568cc2231436d2bcd119fe58b56413815bd4f9c4e5ebf1f8b0f06635505'), 'CONNECTED_SUM_30002054_AUTHOR_SAFE_FREEZE.zip': (12848, 'b61e853074b015a1b3c3723aed57d6055586e18a64522e1a6b376c8c38a697c2'), 'CONNECTED_SUM_30002054_CORRECTED_BOOTSTRAP.py': (1696, 'af27add6987a9951cf647900ef8c63ff4ffc54b95da9ce1252563c6a9927f13a'), 'CONNECTED_SUM_30002054_CORRECTED_EXTERNAL_MANIFEST.json': (1334, 'bfb9fe96160fe5d430ce62ad5b98d56d98b83244fab2e6ded7779853caff597e'), 'CONNECTED_SUM_30002054_CORRECTED_SAFE.zip': (13833, '6dbac8c776c171134b62687639238c1dd00fab4684d0fa7c3c182699de430a4e'), 'CONNECTED_SUM_30002054_INDEPENDENT_AUDIT_BOOTSTRAP.py': (1708, '6bf0bc0dc00be21c9c37a0b20a5cb92d36e36a29cb504bd1a1f9eb1af19a6e79'), 'CONNECTED_SUM_30002054_INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json': (2194, '7d08be6281cae12f2d1ca0127366f0ea0fbc46af2adee25c1f19dd3895aa31ee'), 'CONNECTED_SUM_30002054_INDEPENDENT_AUDIT_RECEIPT.json': (3492, '268e3069bcdee8efc4f47acba2b9a7c6936db4bfd741833c1b4cd3dfd2791eae'), 'CONNECTED_SUM_30002054_INDEPENDENT_AUDIT_SAFE.zip': (24651, '8d948d1da08ce7116a70f4f25d56fbc2a849bad6cde0bd97a2b4ca45d1bb3f09')}

def need(ok, why):
    if not ok: raise ValueError(why)

def sha(b): return hashlib.sha256(b).hexdigest()

def unique(pairs):
    d = {}
    for k, v in pairs:
        need(k not in d, 'duplicate JSON key')
        d[k] = v
    return d

def parse(b): return json.loads(b, object_pairs_hook=unique)

def safe_path(p):
    p = Path(os.path.abspath(p))
    for ancestor in [p] + list(p.parents):
        need(not ancestor.is_symlink(), 'symlink path or ancestor')
    return p

def regular(p):
    safe_path(p)
    need(stat.S_ISREG(p.lstat().st_mode), 'nonregular file')
    need(p.stat().st_size < 2000000, 'file size ceiling')
    return p.read_bytes()

def verify(root, manifest_pin):
    root = safe_path(root)
    own = safe_path(__file__)
    need(own == root / 'publication_bootstrap.py', 'wrong operative entrypoint')
    need(stat.S_ISDIR(root.lstat().st_mode), 'non-directory root')
    mb = regular(root / 'PUBLICATION_MANIFEST.json')
    need(re.fullmatch('[0-9a-f]{64}', manifest_pin) is not None and sha(mb) == manifest_pin, 'external manifest pin mismatch')
    manifest = parse(mb)
    need(type(manifest) is dict and set(manifest) == {'schema', 'problem_id', 'files'}, 'manifest schema')
    need(type(manifest['schema']) is int and manifest['schema'] == 1, 'manifest version')
    need(type(manifest['problem_id']) is int and manifest['problem_id'] == 30002054, 'problem identity')
    entries = manifest['files']
    need(type(entries) is dict and entries, 'manifest entries')
    expected_dirs = set()
    for name, item in entries.items():
        path = PurePosixPath(name)
        need(type(name) is str and str(path) == name and not path.is_absolute() and '..' not in path.parts and '\\' not in name, 'unsafe manifest path')
        need(type(item) is dict and set(item) == {'bytes', 'sha256'}, 'entry schema')
        need(type(item['bytes']) is int and 0 <= item['bytes'] < 2000000, 'entry size')
        need(type(item['sha256']) is str and re.fullmatch('[0-9a-f]{64}', item['sha256']) is not None, 'entry digest')
        expected_dirs.update(str(p) for p in path.parents if str(p) != '.')
    files, dirs = set(), set()
    for base, names, fs in os.walk(root, followlinks=False):
        for name in names:
            p = Path(base) / name
            need(not p.is_symlink() and stat.S_ISDIR(p.lstat().st_mode), 'nonregular directory')
            dirs.add(str(p.relative_to(root)))
        for name in fs:
            p = Path(base) / name
            need(not p.is_symlink() and stat.S_ISREG(p.lstat().st_mode), 'nonregular inventory entry')
            files.add(str(p.relative_to(root)))
    need(files == set(entries) | {'PUBLICATION_MANIFEST.json'} and dirs == expected_dirs, 'strict package inventory')
    payload = {}
    for name, item in entries.items():
        b = regular(root / name)
        need(item == {'bytes': len(b), 'sha256': sha(b)}, 'package byte mismatch: ' + name)
        payload[name] = b
    for name, pin in PINS.items():
        b = payload[name]
        need((len(b), sha(b)) == pin, 'immutable input pin: ' + name)
    member_count = 0
    for folder, prefix in [('author', 'CONNECTED_SUM_30002054_AUTHOR'), ('corrected', 'CONNECTED_SUM_30002054_CORRECTED'), ('audit', 'CONNECTED_SUM_30002054_INDEPENDENT_AUDIT')]:
        zname = prefix + ('_SAFE_FREEZE.zip' if folder == 'author' else '_SAFE.zip')
        m = parse(payload[prefix + '_EXTERNAL_MANIFEST.json'])['files']
        with zipfile.ZipFile(io.BytesIO(payload[zname])) as z:
            infos = z.infolist()
            need(len(infos) == len(m) and {i.filename for i in infos} == set(m), 'archive inventory')
            for i in infos:
                need(i.create_system == 3 and stat.S_ISREG(i.external_attr >> 16) and not i.is_dir() and not i.flag_bits & 1, 'archive member type')
                need('/' not in i.filename and '\\' not in i.filename and i.filename not in ('.', '..'), 'archive path')
                b = z.read(i)
                need(m[i.filename] == {'bytes': len(b), 'sha256': sha(b)} and i.file_size == len(b), 'archive member binding')
                need(payload[folder + '/' + i.filename] == b, 'extracted member mismatch')
                member_count += 1

    acceptance = parse(payload['audit/ACCEPTANCE.json'])
    need(acceptance['intended_additivity'] == 'UNRESOLVED_BY_THIS_WORK' and acceptance['approaches_used'] == 4 and acceptance['approach_limit'] == 5, 'acceptance scope')
    need(acceptance['corrected_verdict'] == 'ACCEPT_PARTIAL_UNRESOLVED' and acceptance['correction_adds_research_approach'] is False, 'correction scope')
    need(acceptance['patch_acceptance']['files_changed'] == ['PROOF.md','README.md','STATUS.json'], 'patch scope')
    need(sha(payload['audit/CORRECTION.patch']) == 'edc843be6c6771c70f684087f592998cf35c9c79d44143100e88c677d656e624', 'exact patch pin')
    for folder in ('author','corrected'):
        status = parse(payload[folder+'/STATUS.json'])
        need(status['intended_problem_status'] == 'unsolved' and status['approaches_used'] == 4 and status['approach_limit'] == 5, 'status gate')
    a = parse(payload['corrected/SOURCES.json'])['sources']
    b = parse(payload['audit/SOURCE_CHECKS.json'])['sources']
    need(len(a) == len(b) == 5, 'source count')
    for x, y in zip(a, b):
        need((x['id'], x['bytes'], x['sha256'], x['retrieval_url']) == (y['id'], y['bytes'], y['sha256'], y['retrieval_url']), 'source metadata binding')
    return root, payload, {'verified': True, 'problem_id': 30002054, 'package_files': len(files), 'archive_members': member_count, 'source_metadata_matches': 5, 'overall': 'unsolved', 'turns': '4/5'}

def replay(root, payload):
    results = []
    with tempfile.TemporaryDirectory(prefix='connected-sum-publication-') as td:
        td = Path(td)
        # Apply the actual immutable patch; never regenerate a substitute diff.
        patched = td/'patched'; patched.mkdir()
        for name,b in payload.items():
            if name.startswith('author/'):
                (patched/Path(name).name).write_bytes(b)
        proc = subprocess.run(['patch','--batch','--fuzz=0','-p1'], input=payload['audit/CORRECTION.patch'], cwd=patched, capture_output=True, timeout=30)
        need(proc.returncode == 0 and b'fuzz' not in proc.stdout.lower() and b'offset' not in proc.stdout.lower(), 'actual patch failed')
        expected = {n.split('/',1)[1]:b for n,b in payload.items() if n.startswith('corrected/')}
        actual = {p.name:p.read_bytes() for p in patched.iterdir() if p.is_file()}
        need(actual == expected and len(list(patched.iterdir())) == len(expected), 'patch does not reproduce every corrected member')
        changed = sorted(n for n in expected if expected[n] != payload['author/'+n])
        need(changed == ['PROOF.md','README.md','STATUS.json'], 'patch changed unexpected files')
        results.append({'kind':'actual_correction_patch','zero_fuzz':True,'zero_offset':True,'all_six_members_exact':True,'changed_files':changed,'checker_unchanged':True,'result':'PASS'})
        for optimized in (False, True):
            flags = [sys.executable, '-I', '-S', '-B'] + (['-O'] if optimized else [])
            for folder, script, count in [('author','verify_math.py',914),('corrected','verify_math.py',914),('audit','independent_diagnostics.py',1377)]:
                proc = subprocess.run(flags + ['-c', payload[folder+'/'+script].decode()], cwd=td, capture_output=True, text=True, timeout=120)
                need(proc.returncode == 0 and not proc.stderr, 'authenticated diagnostics failed: '+folder+': '+proc.stderr)
                got = parse(proc.stdout)
                need(got['result'] == 'PASS' and got['checks'] == count, 'diagnostic count')
                if folder == 'audit': need(got == parse(payload['audit/INDEPENDENT_DIAGNOSTICS.json']), 'independent saved output mismatch')
                results.append({'kind':'diagnostics','folder':folder,'optimized':optimized,'checks':count,'stdout_sha256':sha(proc.stdout.encode()),'result':'PASS'})
            for folder,prefix,ext,saved in [('author','CONNECTED_SUM_30002054_AUTHOR','_SAFE_FREEZE.zip','author_replay'),('corrected','CONNECTED_SUM_30002054_CORRECTED','_SAFE.zip','corrected_replay')]:
                names=[prefix+ext,prefix+'_EXTERNAL_MANIFEST.json',prefix+'_BOOTSTRAP.py']
                args=[str(root/n) for n in names]+[PINS[n][1] for n in names]
                proc = subprocess.run(flags+['-c',payload['audit/replay_acceptance.py'].decode()]+args,cwd=td,capture_output=True,text=True,timeout=180)
                need(proc.returncode == 0 and not proc.stderr, 'authenticated integrity suite failed: '+folder+': '+proc.stderr)
                got=parse(proc.stdout)
                need(got['result']=='PASS' and len(got['tests'])==30 and all(x['result']=='PASS' for x in got['tests']), 'integrity control count')
                saved_key=saved+('_optimized_harness' if optimized else '')
                baseline=parse(payload['audit/ACCEPTANCE.json'])['suites'][saved_key]
                # Exception paths can differ after relocation; compare every outcome and accepted diagnostic count.
                need([(x['test'],x['expected_acceptance'],x['returncode'],x['result'],x.get('diagnostic_checks')) for x in got['tests']] == [(x['test'],x['expected_acceptance'],x['returncode'],x['result'],x.get('diagnostic_checks')) for x in baseline['tests']], 'saved integrity outcome mismatch')
                results.append({'kind':'integrity_suite','folder':folder,'optimized_harness':optimized,'controls':30,'result':got})
    return results

def main():
    need(len(sys.argv) in (3, 4) and (len(sys.argv) == 3 or sys.argv[3] == '--replay'), 'usage: publication_bootstrap.py ROOT MANIFEST_SHA256 [--replay]')
    root, payload, result = verify(sys.argv[1], sys.argv[2])
    if len(sys.argv) == 4:
        result['replays'] = replay(root, payload)
        again = verify(root, sys.argv[2])
        need(again[1] == payload, 'post-replay bytes changed')
    print(json.dumps(result, sort_keys=True, indent=2))

if __name__ == '__main__':
    try: main()
    except (ValueError, OSError, TypeError, KeyError, zipfile.BadZipFile, subprocess.TimeoutExpired) as e:
        print('PUBLICATION VERIFICATION FAILED: ' + str(e), file=sys.stderr)
        sys.exit(1)
