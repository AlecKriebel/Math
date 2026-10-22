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

PINS = {'LEAF_SPACE_10300026_AUTHOR_V2_BOOTSTRAP.py': (2994, 'a1dfd605ea34bdc4df5e350cbf0704ab2025363f8e3e5fb59790c54ab322770a'), 'LEAF_SPACE_10300026_AUTHOR_V2_EXTERNAL_MANIFEST.json': (1232, 'a826f34dcfe07ba474ddb7022907bc090faa120569d49a3b262a575e257fb88c'), 'LEAF_SPACE_10300026_AUTHOR_V2_SAFE_FREEZE.zip': (19002, '7f36eececb5ddcbdfd17e34a7dd015d081641b2d5aa555f093576ae9713df454'), 'LEAF_SPACE_10300026_AUTHOR_V2_VALIDATION_RECEIPT.json': (4596, '3f11cf550f9eec5089c06c7334b7d17bf8afc3b7ae9ec64020c28b94279c2845'), 'LEAF_SPACE_10300026_INDEPENDENT_AUDIT_BOOTSTRAP.py': (3344, 'd4efff22c8177dc5a8ab381261357771c3508269be41f49aef190c44bec10ec3'), 'LEAF_SPACE_10300026_INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json': (2426, 'a283473e7b2218168af7a057a0939fa1f03d8978163526203be09d3fc351c3e6'), 'LEAF_SPACE_10300026_INDEPENDENT_AUDIT_RECEIPT.json': (13930, '1e80862c2e9e7fad2e09eefe89f90641f4e77c354c932efaec00b3ecf7ab9b6b'), 'LEAF_SPACE_10300026_INDEPENDENT_AUDIT_SAFE.zip': (26615, '5ab0184a795e411b965ca6cdeada6272f35fd60a2f84fe4ca0254e1d7bf375cc')}

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
    p = Path(p)
    need(p.is_absolute() and str(p.resolve()) == str(p), 'canonical absolute path required')
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
    need(type(manifest['problem_id']) is int and manifest['problem_id'] == 10300026, 'problem identity')
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
    for folder, prefix in [('author', 'LEAF_SPACE_10300026_AUTHOR_V2'), ('audit', 'LEAF_SPACE_10300026_INDEPENDENT_AUDIT')]:
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
    need(acceptance['disposition'] == 'ACCEPTED_SCOPED_AUDIT_NO_GENERAL_SOLUTION' and acceptance['substantive_approaches'] == 4 and acceptance['mathematical_patch_required'] is False, 'acceptance scope')
    need(acceptance['full_solution'] is False and acceptance['new_mathematical_result_claimed'] is False and acceptance['exact_original_current_status'] == 'NOT_ESTABLISHED_BY_THIS_AUDIT', 'unresolved status')
    status = parse(payload['author/STATUS.json'])
    need(status['status'] == 'UNRESOLVED_IN_THIS_AUDIT' and status['substantive_approaches'] == 4 and status['full_solution'] is False and status['new_mathematical_result_claimed'] is False, 'status gate')
    source = parse(payload['audit/CORPUS_BINDINGS.json'])
    need(source['review_match'] is True and source['statement_match'] is True and source['catalog_rank'] == 844, 'corpus gate')
    for name in PINS:
        if '_AUTHOR_V2_' in name: need(payload[name] == payload['audit/'+name], 'original duplicate changed')
    return root, payload, {'verified': True, 'problem_id': 10300026, 'package_files': len(files), 'archive_members': member_count, 'overall': 'unsolved', 'turns': '4/5', 'correction_required': False}


def run_bytes(path, raw, arguments, flags, cwd):
    code = 'import sys;sys.argv=sys.argv[1:];__file__=sys.argv[0];exec(compile('+repr(raw)+',__file__,"exec"))'
    p = subprocess.run(flags+['-c',code,str(path)]+[str(a) for a in arguments],cwd=cwd,capture_output=True,timeout=180)
    need(p.returncode == 0 and not p.stderr, 'authenticated execution failed: '+p.stderr.decode())
    return parse(p.stdout), p.stdout

def replay(root, payload, corpus=None):
    results = []
    with tempfile.TemporaryDirectory(prefix='leaf-space-publication-') as td:
        td = Path(td)
        clean = td/'clean'; clean.mkdir()
        for name,b in payload.items():
            p=clean/name; p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(b)
        for optimized in (False, True):
            flags = [sys.executable, '-I', '-S', '-B'] + (['-O'] if optimized else [])
            if corpus:
                script='audit/verify_corpus_bindings.py'
                got,raw=run_bytes(clean/script,payload[script],corpus,flags,td)
                need(got == parse(payload['audit/CORPUS_BINDINGS.json']), 'corpus result mismatch')
                results.append({'kind':'complete_corpus_binding','optimized':optimized,'result':got,'stdout_sha256':sha(raw)})
                continue
            for folder,prefix,key in [('author','LEAF_SPACE_10300026_AUTHOR_V2','metadata_validation'),('audit','LEAF_SPACE_10300026_INDEPENDENT_AUDIT','audit_metadata')]:
                script=prefix+'_BOOTSTRAP.py';zname=prefix+('_SAFE_FREEZE.zip' if folder=='author' else '_SAFE.zip')
                got,raw=run_bytes(clean/script,payload[script],[clean/zname,clean/folder,clean/(prefix+'_EXTERNAL_MANIFEST.json')],flags,td)
                need(got[key]=='PASS' and got['full_solution'] is False and got['problem_id']==10300026, 'metadata scope')
                results.append({'kind':'metadata','folder':folder,'optimized':optimized,'result':got,'stdout_sha256':sha(raw)})
            for script,inp,count,label in [('audit/replay_author.py',clean/'audit',45,'author'),('replay_audit_controls.py',clean,43,'audit')]:
                got,raw=run_bytes(clean/script,payload[script],[inp],flags,td)
                need(got['test_count']==count and got['all_tests_pass'] is True and all(x['pass'] is True for x in got['tests']), 'control result')
                results.append({'kind':'integrity_suite','folder':label,'optimized_harness':optimized,'controls':count,'result':got,'stdout_sha256':sha(raw)})
    return results

def main():
    need((len(sys.argv)==3) or (len(sys.argv)==4 and sys.argv[3]=='--replay') or (len(sys.argv)==7 and sys.argv[3]=='--corpus'), 'usage: publication_bootstrap.py ROOT MANIFEST_SHA256 [--replay | --corpus CATALOG PROBLEMS REPORTS]')
    root, payload, result = verify(sys.argv[1], sys.argv[2])
    if len(sys.argv)>3:
        result['replays'] = replay(root, payload, sys.argv[4:] if sys.argv[3]=='--corpus' else None)
        again = verify(root, sys.argv[2])
        need(again[1] == payload, 'post-replay bytes changed')
    print(json.dumps(result, sort_keys=True, indent=2))

if __name__ == '__main__':
    try: main()
    except (ValueError, OSError, TypeError, KeyError, zipfile.BadZipFile, subprocess.TimeoutExpired) as e:
        print('PUBLICATION VERIFICATION FAILED: ' + str(e), file=sys.stderr)
        sys.exit(1)
