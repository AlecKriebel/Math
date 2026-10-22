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

PINS = {'MIXED_PERVERSE_30002888_AUTHOR_EXTERNAL_MANIFEST.json': (1028, '4bc74cfa1a957a2f9a6d87e5c0251bd30fc05195b1da8e86503da30d4611e56c'), 'MIXED_PERVERSE_30002888_AUTHOR_SAFE_FREEZE.zip': (11285, 'feb85b4fd09b96aced2438889fbc0866302a56478fef12ad447f95fc8da336be'), 'MIXED_PERVERSE_30002888_AUTHOR_VALIDATION_RECEIPT.json': (901, 'e6990dca2f0ced5265309528c89d4c9fc81b89c7862070e836ab022e5efd10b0'), 'MIXED_PERVERSE_30002888_INDEPENDENT_AUDIT_BOOTSTRAP.py': (2537, '725541fcbd9e32e588278a0ef2a1496e8b13ae31c97381b44c36cd4152212d7d'), 'MIXED_PERVERSE_30002888_INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json': (1416, '09389188505de2429983c79e3fa3b236d4a8643d0a68896cfd7137a52a1bf30d'), 'MIXED_PERVERSE_30002888_INDEPENDENT_AUDIT_RECEIPT.json': (2532, '3d8ace88dcb88f1b56f66f389a89369ad08f6344ad5ad74c88dc96ae46d6e53b'), 'MIXED_PERVERSE_30002888_INDEPENDENT_AUDIT_SAFE.zip': (12920, 'aa321a9ae8924ae198223e314d45706ac056ab8111de9d161b611ff71df43d95')}

def need(ok, why):
    if not ok: raise ValueError(why)

def sha(b): return hashlib.sha256(b).hexdigest()

def unique(pairs):
    d = {}
    for k, v in pairs:
        need(k not in d, 'duplicate JSON key')
        d[k] = v
    return d

def nonfinite(_): raise ValueError('nonfinite JSON number')

def parse(b): return json.loads(b.decode('utf-8'), object_pairs_hook=unique, parse_constant=nonfinite)

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
    need(type(manifest['problem_id']) is int and manifest['problem_id'] == 30002888, 'problem identity')
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
    for folder, prefix in [('author', 'AUTHOR'), ('audit', 'INDEPENDENT_AUDIT')]:
        stem = 'MIXED_PERVERSE_30002888_' + prefix
        aname = stem + ('_SAFE_FREEZE.zip' if folder == 'author' else '_SAFE.zip')
        am = parse(payload[stem + '_EXTERNAL_MANIFEST.json'])
        need(am['archive']['filename'] == aname and am['archive']['bytes'] == len(payload[aname]) and am['archive']['sha256'] == sha(payload[aname]), 'archive manifest binding')
        member_count += check_archive(payload[aname], am['files'])
        with zipfile.ZipFile(io.BytesIO(payload[aname])) as z:
            for name in z.namelist(): need(payload[folder + '/' + name] == z.read(name), 'extracted member mismatch')
    acceptance = parse(payload['audit/acceptance.json'])
    checks = parse(payload['author/checks.json'])
    meta = parse(payload['PUBLICATION_METADATA.json'])
    need(acceptance['verdict'] == 'accepted_unchanged_as_partial_conditional_investigation' and acceptance['general_problem_solved'] is False and acceptance['novelty_certified'] is False and acceptance['correction_patch_required'] is False, 'acceptance scope')
    need(checks['outcome'] == 'partial_conditional_results_only' and checks['approaches_used'] == 5 and checks['full_solution_claimed'] is False and checks['novelty_claimed'] is False, 'author status')
    need(meta['canonical_status'] == 'unsolved' and meta['turns'] == '5/5' and meta['new_proof_attempts_added'] == 0 and meta['mandatory_correction_required'] is False, 'canonical status')
    old = parse(payload['audit/source_check_metadata.json'])
    fresh = parse(payload['PUBLICATION_SOURCE_BINDINGS.json'])
    need(fresh['review_sha256'] == old['complete_record_checks']['complete_review_sha256'] == '3dcca041cf7ee4aa81a06d69853b63996e0f8346f845c61fac3ad5a52f2b8b3a', 'complete record binding')
    need(fresh['statement_sha256'] == old['complete_record_checks']['statement_sha256'] == '30bf98cff2ec1b6f28805453b4ab3f33039e5c89749df05b992d8825dd247a52', 'statement binding')
    need(fresh['rank'] == 863 and fresh['complete_catalog_problem_report_snapshot_match'] is True and fresh['inherited_report_key_present'] is False, 'catalog binding')
    need(len(fresh['corpora']) == len(old['public_dataset_identity']) == 3, 'corpus count')
    for a, b in zip(old['public_dataset_identity'], fresh['corpora']):
        need(all(b[k] == v for k, v in a.items()) and b['fresh_retained_bytes_match'] is True, 'corpus metadata binding')
    sources = parse(payload['author/source_metadata.json'])['sources']
    need(len(sources) == len(old['sources']) == len(fresh['source_pdfs']) == 4, 'four PDF sources')
    for a, b, c in zip(sources, old['sources'], fresh['source_pdfs']):
        need(all(a[k] == b[k] == c[k] for k in ('title', 'pdf_url', 'pdf_bytes', 'pdf_sha256')) and a['landing_url'] == b['public_url'] == c['public_url'] and c['fresh_retained_bytes_match'] is True, 'PDF source metadata binding')
    return root, payload, {'verified': True, 'problem_id': 30002888, 'package_files': len(files), 'archive_members': member_count, 'overall': 'unsolved', 'turns': '5/5', 'correction_required': False, 'full_source_binding': True, 'mathematical_truth_certified_by_code': False}

def check_archive(raw,entries):
    need(type(entries) is list and entries,'archive manifest entries')
    expected={}
    for e in entries:
        need(type(e) is dict and set(e)=={'path','bytes','sha256'},'archive entry schema')
        name=e['path'];path=PurePosixPath(name)
        need(name not in expected and str(path)==name and not path.is_absolute() and '..' not in path.parts and '\\' not in name,'unsafe or duplicate archive path')
        need(type(e['bytes']) is int and 0<=e['bytes']<2000000,'archive entry size')
        expected[name]=e
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        infos=z.infolist();need(len(infos)==len(expected) and {i.filename for i in infos}==set(expected),'strict archive inventory')
        need(z.testzip() is None and not z.comment,'archive CRC or comment')
        for i in infos:
            need(i.filename == i.orig_filename, 'archive name rewriting')
            mode=i.external_attr>>16
            need(i.create_system==3 and stat.S_IFMT(mode) in (0, stat.S_IFREG) and not mode&0o111 and not i.is_dir() and not i.flag_bits&1,'archive member type or executable')
            need(PurePosixPath(i.filename).suffix in ('.md','.json','.py'),'archive extension')
            b=z.read(i);s=b.decode('utf-8');need('\0' not in s,'binary text')
            need(len(b)==expected[i.filename]['bytes'] and sha(b)==expected[i.filename]['sha256'],'archive bytes mismatch')
            if i.filename.endswith('.json'):parse(b)
    return len(expected)

def hostile_archives():
    import warnings
    b=b'{}\n';entry=lambda name,body:[{'path':name,'bytes':len(body),'sha256':sha(body)}]
    base=entry('test.json',b)
    cases=[('extra member',[('test.json',b,0o100444),('extra.md',b'extra',0o100444)],base),('missing member',[],base),('duplicate member',[('test.json',b,0o100444)]*2,base),('payload changed',[('test.json',b'[]\n',0o100444)],base),('path traversal',[('../test.json',b,0o100444)],entry('../test.json',b)),('executable mode',[('test.json',b,0o100555)],base),('symbolic link',[('test.json',b,0o120444)],base),('invalid UTF-8',[('test.json',b'\xff',0o100444)],entry('test.json',b'\xff')),('duplicate JSON keys',[('test.json',b'{"x":1,"x":2}',0o100444)],entry('test.json',b'{"x":1,"x":2}')),('nonfinite JSON',[('test.json',b'{"x":NaN}',0o100444)],entry('test.json',b'{"x":NaN}')),('invalid JSON',[('test.json',b'{]',0o100444)],entry('test.json',b'{]')),('NUL text',[('test.md',b'x\0y',0o100444)],entry('test.md',b'x\0y'))]
    records=[]
    for name,items,spec in cases:
        out=io.BytesIO()
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            with zipfile.ZipFile(out,'w') as z:
                for path,body,mode in items:
                    i=zipfile.ZipInfo(path);i.create_system=3;i.external_attr=mode<<16;z.writestr(i,body)
        try:check_archive(out.getvalue(),spec)
        except (ValueError,UnicodeDecodeError,zipfile.BadZipFile) as e:records.append({'case':name,'rejected':True,'reason':str(e)})
        else:raise ValueError('hostile archive accepted: '+name)
    return records

def replay(root, payload):
    results = {}
    flags = [sys.executable, '-I', '-S', '-B'] + (['-O'] if sys.flags.optimize else [])
    with tempfile.TemporaryDirectory(prefix='mixed-perverse-publication-') as td:
        for label, script, archive, manifest in [
            ('author_integrity', 'audit/verify_author_freeze.py', 'MIXED_PERVERSE_30002888_AUTHOR_SAFE_FREEZE.zip', 'MIXED_PERVERSE_30002888_AUTHOR_EXTERNAL_MANIFEST.json'),
            ('audit_integrity', 'MIXED_PERVERSE_30002888_INDEPENDENT_AUDIT_BOOTSTRAP.py', 'MIXED_PERVERSE_30002888_INDEPENDENT_AUDIT_SAFE.zip', 'MIXED_PERVERSE_30002888_INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json')]:
            code = 'import sys;sys.argv=sys.argv[1:];__file__=sys.argv[0];exec(compile(' + repr(payload[script]) + ',__file__,"exec"))'
            p = subprocess.run(flags + ['-c', code, str(root/script), str(root/archive), str(root/manifest)], cwd=td, capture_output=True, timeout=40)
            need(p.returncode == 0 and not p.stderr, 'pinned integrity utility failed')
            result = parse(p.stdout); need(result['ok'] is True, 'pinned integrity result')
            results[label] = result
        results['hostile_archives'] = hostile_archives()
        need(len(results['hostile_archives']) == 12, 'hostile archive case count')
    return results

def main():
    need(len(sys.argv) in (3,4) and (len(sys.argv)==3 or sys.argv[3]=='--replay'),'usage: publication_bootstrap.py ROOT MANIFEST_SHA256 [--replay]')
    root,payload,result=verify(sys.argv[1],sys.argv[2])
    if len(sys.argv)==4:
        result['replays']=replay(root,payload)
        need(verify(root,sys.argv[2])[1]==payload,'input bytes mutated')
    print(json.dumps(result,sort_keys=True,indent=2))
if __name__=='__main__':
    try:main()
    except (ValueError,OSError,TypeError,KeyError,zipfile.BadZipFile,subprocess.TimeoutExpired) as e:
        print('PUBLICATION VERIFICATION FAILED: '+str(e),file=sys.stderr);sys.exit(1)
