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

PINS = {'HEIGHT_COUNTS_30002439_AUTHOR_BOOTSTRAP.py': (3058, '6602a795c3fad2853e7f8ab4a3dc5ce801282d71f91e5acb52020ab23845eeb3'), 'HEIGHT_COUNTS_30002439_AUTHOR_EXTERNAL_MANIFEST.json': (1364, '3527edc41af60fc640160c63416aacccc212d99d04f6f9a0c54cd7e477b4cfec'), 'HEIGHT_COUNTS_30002439_AUTHOR_SAFE_FREEZE.zip': (11301, '94ec6adf37a9b6cdd4532ef448ae72ed46ac739b50c81c69686ffa34370e7304'), 'HEIGHT_COUNTS_30002439_AUTHOR_VALIDATION_RECEIPT.json': (6573, '139402f214a9747f7cab976a30c69f0def3ca522018d745eeb96ed5480863803'), 'HEIGHT_COUNTS_30002439_INDEPENDENT_AUDIT_BOOTSTRAP.py': (3117, '25ef91ec8febfebd73879615734755af3dfd01bd6fff88a2bdd25e5a412fff06'), 'HEIGHT_COUNTS_30002439_INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json': (2599, '8a56f4e9440b01505d3ca2ea3eda9796283e84ec2df6f428a78906c305fd9d56'), 'HEIGHT_COUNTS_30002439_INDEPENDENT_AUDIT_RECEIPT.json': (22544, '5aeb073772d5ebaeccb9ccff2c47c37ad18523c63c0d1869b26ac44d7e4a67f7'), 'HEIGHT_COUNTS_30002439_INDEPENDENT_AUDIT_SAFE.zip': (32964, '5c8e4a4bc0590f562a42b779b19c3923b794715f515a5079e7216495cf717700')}

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
    need(type(manifest['problem_id']) is int and manifest['problem_id'] == 30002439, 'problem identity')
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
    for folder, prefix in [('author', 'HEIGHT_COUNTS_30002439_AUTHOR'), ('audit', 'HEIGHT_COUNTS_30002439_INDEPENDENT_AUDIT')]:
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
    need(acceptance['decision'] == 'ACCEPT_AS_PARTIAL_NOT_SOLVED' and acceptance['approaches_used'] == 4 and acceptance['correction_required'] is False, 'acceptance scope')
    status = parse(payload['author/STATUS.json'])
    need(status['classification'] == 'PARTIAL_NOT_SOLVED' and status['approaches_used'] == 4 and status['approach_limit'] == 5 and status['general_conjecture_resolved'] is False, 'status gate')
    source = parse(payload['audit/PUBLIC_SOURCE_AUDIT.json'])
    need(source['review_match'] is True and source['statement_match'] is True, 'source gate')
    need(source['fresh_salberger_comparison']['same_pdf_bytes'] is False and source['fresh_salberger_comparison']['article_pages_after_cover_extracted_text_identical'] is True and source['fresh_salberger_comparison']['printed_p1095_rendered_pixels_identical'] is True, 'separate PDF identities')
    for name in ('HEIGHT_COUNTS_30002439_AUTHOR_BOOTSTRAP.py', 'HEIGHT_COUNTS_30002439_AUTHOR_EXTERNAL_MANIFEST.json', 'HEIGHT_COUNTS_30002439_AUTHOR_SAFE_FREEZE.zip', 'HEIGHT_COUNTS_30002439_AUTHOR_VALIDATION_RECEIPT.json'):
        need(payload[name] == payload['audit/'+name], 'original duplicate changed')
    return root, payload, {'verified': True, 'problem_id': 30002439, 'package_files': len(files), 'archive_members': member_count, 'overall': 'unsolved', 'turns': '4/5', 'correction_required': False}


def replay(root, payload):
    results = []
    with tempfile.TemporaryDirectory(prefix='height-counts-publication-') as td:
        td = Path(td)
        clean = td/'clean'; clean.mkdir()
        for name,b in payload.items():
            p=clean/name; p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(b)
        for optimized in (False, True):
            flags = [sys.executable, '-I', '-S', '-B'] + (['-O'] if optimized else [])
            for folder,prefix,outname in [('author','HEIGHT_COUNTS_30002439_AUTHOR','RESULTS.json'),('audit','HEIGHT_COUNTS_30002439_INDEPENDENT_AUDIT','DIAGNOSTICS_RESULTS.json')]:
                script=prefix+'_BOOTSTRAP.py';zname=prefix+('_SAFE_FREEZE.zip' if folder=='author' else '_SAFE.zip')
                code='import sys;sys.argv=sys.argv[1:];__file__=sys.argv[0];exec(compile('+repr(payload[script])+',__file__,"exec"))'
                proc=subprocess.run(flags+['-c',code,str(clean/script),str(clean/folder),str(clean/zname),str(clean/(prefix+'_EXTERNAL_MANIFEST.json'))],cwd=td,capture_output=True,timeout=120)
                need(proc.returncode==0 and not proc.stderr and proc.stdout==payload[folder+'/'+outname], 'authenticated '+folder+' diagnostics failed: '+proc.stderr.decode())
                results.append({'kind':'diagnostics','folder':folder,'optimized':optimized,'result':'PASS','checks':parse(proc.stdout)['checks'],'stdout_sha256':sha(proc.stdout)})
            for script,inp,count,label in [('audit/recheck_author_controls.py',clean/'audit',65,'author'),('recheck_audit_controls.py',clean,79,'audit')]:
                out=td/('controls-'+label+str(optimized)+'.json')
                code='import sys;sys.argv=sys.argv[1:];__file__=sys.argv[0];exec(compile('+repr(payload[script])+',__file__,"exec"))'
                proc=subprocess.run(flags+['-c',code,str(clean/script),str(inp),str(out)],cwd=td,capture_output=True,timeout=180)
                need(proc.returncode==0 and not proc.stderr,'authenticated controls failed: '+proc.stderr.decode())
                got=parse(out.read_bytes());need(got['control_count']==count and got['all_controls_passed'] is True and all(x['result']=='PASS' for x in got['controls']),'control count')
                results.append({'kind':'integrity_suite','folder':label,'optimized_harness':optimized,'controls':count,'result':got})
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
