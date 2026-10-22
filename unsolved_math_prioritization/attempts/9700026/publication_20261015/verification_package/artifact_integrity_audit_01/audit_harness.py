#!/usr/bin/env python3
"""Independent, source-free by default artifact audit. No network or Git writes.

Run: python3 -I -B audit_harness.py
Add --provenance to replay the original source checker using the complete local
corpora and separately fetched PDFs. All disposable private fixtures are removed.
This authenticates the frozen bytes, not mathematical validity or priority.
"""
import argparse
import ast
import gc
import hashlib
import io
import json
import math
import os
from pathlib import Path, PurePosixPath
import shutil
import stat
import subprocess
import sys
import tempfile
import time
import zipfile
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
SOURCE = AUDIT / 'source'
OUTER_SHA = 'b0b0cdc72798cfcffc5fefeec1de30ff422f54bde83d0f8a91fd2e6a87311d8b'
PUBLIC_SHA = '379efdd8506bb5f28c80ece66fc5b9e130a9668c5605343443cb811b84a23081'
PROOF_PIN = (5736, '8b0922482116df0b6510b4d5a6c089c3478765d4fecf2c151fd04c50a6814767')
HEAD = 'fba74a301786f9648e48722e76f440097b0746c2'
PAIR_PIN = (4409, '7b18458d71482e2c4e1c62601be1824eba6ad6243c78135d90d1b75223e8e193')
INPUTS = {
    'catalog.json': (21735099, '891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566'),
    'problems.json': (68931837, '04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf'),
    'research_results.json': (80334822, '8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b'),
    'cities-notes.pdf': (295226, '9cfbe9da2660fcea7e44d7ef013cb7a8a1604ff54a9e7734e71ef76959c38b89'),
    'cities-2012.pdf': (398185, 'eeecb371b6e6c2860c01e1b73d812468b619ddb7e3c4cd1d0e3affc056e8a077'),
}
MODES = [[], ['-O'], ['-I'], ['-I', '-O']]
# Only these observed behaviors in the immutable legacy bodies may be reported
# as accepted limitations. Any new accepted intended-rejection probe is fatal.
LEGACY_ACCEPTED_LIMITATIONS = {
    'legacy_resealed_duplicate_json_key', 'legacy_resealed_nan',
    'legacy_resealed_infinity', 'legacy_resealed_negative_infinity',
    'legacy_resealed_overflow', 'legacy_unlisted_empty_directory',
    'legacy_unlisted_fifo', 'legacy_certificate_duplicate_nan',
    'legacy_certificate_duplicate_overflow',
    'legacy_certificate_initial_weights_dictionary',
    'legacy_safe_path_a\\x', 'legacy_safe_path_C:x',
    'legacy_resealed_zip_symlink_metadata', 'legacy_resealed_zip_fifo_metadata',
    'legacy_resealed_zip_executable_metadata',
    'legacy_standalone_missing_audit_manifest_changed_report',
    'legacy_source_resealed_duplicate_catalog_id',
    'legacy_source_resealed_duplicate_record_id',
    'legacy_source_resealed_catalog_nan', 'legacy_source_resealed_catalog_overflow',
    'legacy_source_resealed_duplicate_report_key',
    'legacy_resealed_source_pdf_symlink',
}

def require(ok, message):
    if not ok:
        raise ValueError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def pin(data):
    return len(data), sha(data)

def pairs_hook(pairs):
    out = {}
    for k, v in pairs:
        require(k not in out, 'duplicate JSON key: ' + k)
        out[k] = v
    return out

def finite_float(value):
    x = float(value)
    require(math.isfinite(x), 'nonfinite or overflowing JSON number')
    return x

def strict_json(raw):
    def bad(value):
        raise ValueError('nonstandard JSON number: ' + value)
    return json.loads(raw, object_pairs_hook=pairs_hook, parse_constant=bad,
                      parse_float=finite_float)

def safe_name(name):
    require(type(name) is str and name and '\\' not in name and '\x00' not in name,
            'unsafe path spelling')
    p = PurePosixPath(name)
    require(not p.is_absolute() and name == p.as_posix() and
            all(t not in ('', '.', '..') for t in p.parts) and ':' not in name,
            'unsafe path components')
    return p

def regular_bytes(path):
    st = path.lstat()
    require(stat.S_ISREG(st.st_mode), 'not ordinary regular file: ' + path.name)
    require(st.st_nlink >= 1, 'invalid link count')
    # O_NOFOLLOW closes the final-component symlink race on this platform.
    fd = os.open(path, os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0))
    with os.fdopen(fd, 'rb') as f:
        require(stat.S_ISREG(os.fstat(f.fileno()).st_mode), 'file changed type')
        data = f.read()
    require(len(data) == st.st_size, 'file changed size while read')
    return data

def inventory(root):
    files, dirs = {}, set()
    require(root.is_dir() and not root.is_symlink(), 'unsafe root directory')
    def scan(path):
        for child in path.iterdir():
            name = child.relative_to(root).as_posix()
            safe_name(name)
            mode = child.lstat().st_mode
            if stat.S_ISDIR(mode):
                dirs.add(name)
                scan(child)
            elif stat.S_ISREG(mode):
                files[name] = child
            else:
                raise ValueError('nonregular tree entry: ' + name)
    scan(root)
    return files, dirs

def expected_dirs(names):
    return {p.as_posix() for n in names for p in PurePosixPath(n).parents
            if p.as_posix() != '.'}

def check_rows(root, rows, excludes=(), exact=False):
    require(type(rows) is list, 'manifest rows not list')
    names = []
    for r in rows:
        require(type(r) is dict and {'path', 'bytes', 'sha256'} <= set(r), 'bad manifest row')
        safe_name(r['path'])
        require(type(r['bytes']) is int and r['bytes'] >= 0, 'noninteger size')
        require(type(r['sha256']) is str and len(r['sha256']) == 64 and
                all(x in '0123456789abcdef' for x in r['sha256']), 'bad digest')
        names.append(r['path'])
    require(len(names) == len(set(names)), 'duplicate manifest member')
    if exact:
        files, dirs = inventory(root)
        wanted = set(names) | set(excludes)
        require(set(files) == wanted, 'closed file inventory mismatch')
        require(dirs == expected_dirs(wanted), 'closed directory inventory mismatch')
    for r in rows:
        require(pin(regular_bytes(root / r['path'])) == (r['bytes'], r['sha256']),
                'member pin mismatch: ' + r['path'])
    return len(rows)

def zip_check(raw, rows, expansion=None, expected_modes=None):
    names = [r['path'] for r in rows]
    require(len(names) == len(set(names)), 'duplicate ZIP manifest member')
    by_name = {r['path']: r for r in rows}
    result = []
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        infos = z.infolist()
        require(len(infos) == len(names) and {i.filename for i in infos} == set(names),
                'closed ZIP inventory mismatch')
        for i in infos:
            safe_name(i.filename)
            mode = i.external_attr >> 16
            require(not i.is_dir() and i.create_system == 3 and stat.S_ISREG(mode),
                    'ZIP member not Unix ordinary file')
            require(stat.S_IMODE(mode) in (0o444, 0o644), 'unsafe ZIP permission mode')
            if expected_modes is not None:
                require(mode == expected_modes[i.filename], 'ZIP mode differs')
            require(not (i.flag_bits & 1), 'encrypted ZIP member')
            row = by_name[i.filename]
            require(type(row['bytes']) is int and 0 <= row['bytes'] <= 1_000_000,
                    'member size outside artifact bound')
            require(i.file_size == row['bytes'], 'declared ZIP size mismatch')
            with z.open(i) as f:
                data = f.read(row['bytes'] + 1)
                require(len(data) == row['bytes'] and not f.read(1), 'expanded ZIP size mismatch')
            require(pin(data) == (row['bytes'], row['sha256']), 'ZIP member pin mismatch')
            if expansion is not None:
                require(regular_bytes(expansion / i.filename) == data, 'expanded duplicate differs')
            result.append({'path': i.filename, 'bytes': len(data), 'sha256': sha(data),
                           'mode_octal': oct(mode), 'crc32': format(i.CRC, '08x')})
        require(z.testzip() is None, 'ZIP CRC failure')
    return result

def authenticate(root=SOURCE):
    outer_raw = regular_bytes(AUDIT / 'SOURCE_MANIFEST.json')
    require(sha(outer_raw) == OUTER_SHA, 'outer manifest fixed pin mismatch')
    outer = strict_json(outer_raw)
    require(outer['frozen_head'] == HEAD and outer['problem_id'] == 9700026, 'wrong frozen identity')
    check_rows(root, outer['files'], exact=True)
    require(len(outer['files']) == 40 and sum(r['bytes'] for r in outer['files']) == 276581,
            'unexpected total source inventory')
    for r in outer['files']:
        data = regular_bytes(root / r['path'])
        blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        require(blob == r['git_blob'], 'Git blob identity mismatch')
        require(stat.S_IMODE((root / r['path']).lstat().st_mode) == 0o644, 'source permission differs')
        if r['path'].endswith('.json'):
            strict_json(data)
        if r['path'].endswith('.py'):
            ast.parse(data, filename=r['path'])
    public = regular_bytes(root / 'PUBLICATION_MANIFEST.json')
    require(sha(public) == PUBLIC_SHA, 'public manifest fixed pin mismatch')
    check_rows(root, strict_json(public)['files'], excludes=['PUBLICATION_MANIFEST.json'], exact=True)
    require(pin(regular_bytes(root / 'author/PROOF.md')) == PROOF_PIN, 'proof fixed pin mismatch')
    archives = {}
    for prefix, folder in [('AUTHOR', 'author'), ('INDEPENDENT_AUDIT', 'audit_a')]:
        name = 'CITY_STABILITY_9700026_' + prefix + '_SAFE' + ('_FREEZE' if prefix == 'AUTHOR' else '') + '.zip'
        m = strict_json(regular_bytes(root / ('CITY_STABILITY_9700026_' + prefix + '_EXTERNAL_MANIFEST.json')))
        raw = regular_bytes(root / name)
        require(pin(raw) == (m['zip']['bytes'], m['zip']['sha256']), 'external ZIP pin differs')
        archives[name] = zip_check(raw, m['files'], root / folder)
    author_raw = regular_bytes(root / 'CITY_STABILITY_9700026_AUTHOR_SAFE_FREEZE.zip')
    author_mraw = regular_bytes(root / 'CITY_STABILITY_9700026_AUTHOR_EXTERNAL_MANIFEST.json')
    require(regular_bytes(root / 'audit_a/AUTHOR_SAFE_FREEZE.zip') == author_raw, 'nested ZIP duplicate differs')
    require(regular_bytes(root / 'audit_a/AUTHOR_EXTERNAL_MANIFEST.json') == author_mraw, 'nested external manifest differs')
    with zipfile.ZipFile(io.BytesIO(regular_bytes(root / 'CITY_STABILITY_9700026_INDEPENDENT_AUDIT_SAFE.zip'))) as z:
        nested_raw = z.read('AUTHOR_SAFE_FREEZE.zip')
        require(nested_raw == author_raw, 'nested author ZIP differs')
        archives['audit_zip::AUTHOR_SAFE_FREEZE.zip'] = zip_check(nested_raw, strict_json(author_mraw)['files'], root/'audit_a/author')
    for folder, manifest in [('author','MANIFEST.json'), ('audit_a','MANIFEST.json'), ('review_b','MANIFEST_B.json')]:
        check_rows(root/folder, strict_json(regular_bytes(root/folder/manifest))['files'], [manifest], exact=True)
    return {'status': 'PASS', 'source_files': 40, 'source_bytes': 276581,
            'all_git_modes': '100644', 'outer_manifest_sha256': OUTER_SHA,
            'publication_manifest_sha256': PUBLIC_SHA, 'zip_members': archives,
            'python_paths_inspected': [r['path'] for r in outer['files'] if r['path'].endswith('.py')]}

def run(script, args=(), flags=(), cwd=None):
    t = time.monotonic()
    p = subprocess.run([sys.executable, '-B', *flags, str(script), *map(str, args)],
                       cwd=cwd, capture_output=True, text=True, timeout=90)
    row = {'script': str(script.relative_to(HERE)) if script.is_relative_to(HERE) else str(script.relative_to(AUDIT)),
           'args': [str(a) if not isinstance(a,Path) else a.name for a in args],
           'flags': list(flags), 'returncode': p.returncode, 'stderr': p.stderr,
           'elapsed_seconds': round(time.monotonic()-t, 3)}
    try:
        row['result'] = strict_json(p.stdout)
    except Exception:
        row['stdout'] = p.stdout[:2000]
    return row

def known_module(path, root=None):
    # The program body comes only from the fully authenticated frozen source.
    raw = regular_bytes(SOURCE/path)
    expected = next(r for r in strict_json(regular_bytes(AUDIT/'SOURCE_MANIFEST.json'))['files'] if r['path']==path)
    require(pin(raw) == (expected['bytes'], expected['sha256']), 'probe startup pin mismatch')
    namespace = {'__name__': 'independent_probe', '__file__': str((root or SOURCE)/path)}
    exec(compile(raw, str(SOURCE/path), 'exec'), namespace)
    return namespace

def attempt(label, thunk, expected_reject=True, **extra):
    try:
        value = thunk()
    except Exception as e:
        return {'label': label, 'intended_rejection': expected_reject, 'rejected': True,
                'exception': type(e).__name__, 'message': str(e),
                'classification': 'EXPECTED_REJECTION' if expected_reject else 'UNEXPECTED_REJECTION', **extra}
    return {'label': label, 'intended_rejection': expected_reject, 'rejected': False,
            'classification': 'LIMITATION_ACCEPTED' if expected_reject else 'EXPECTED_ACCEPTANCE', **extra}

def fixed_pin_probes(work):
    out = []
    tree = work/'attacked_tree'
    def reset():
        if tree.exists(): shutil.rmtree(tree)
        shutil.copytree(SOURCE, tree)
    # Check every ordinary payload and every manifest/code path, rather than a sample.
    for r in strict_json(regular_bytes(AUDIT/'SOURCE_MANIFEST.json'))['files']:
        reset(); p=tree/r['path']; p.write_bytes(p.read_bytes()+b'\n')
        out.append(attempt('fixed_pin_altered:' + r['path'], lambda: authenticate(tree)))
    for label, mutate in [
        ('unlisted_file', lambda: (tree/'unlisted.txt').write_text('x')),
        ('unlisted_empty_directory', lambda: (tree/'unlisted').mkdir()),
        ('unlisted_fifo', lambda: os.mkfifo(tree/'unlisted.fifo')),
        ('unlisted_symlink', lambda: (tree/'unlisted.link').symlink_to('README.md')),
        ('listed_symlink', lambda: ((tree/'README.md').unlink(), (tree/'README.md').symlink_to(SOURCE/'README.md'))),
        ('listed_fifo', lambda: ((tree/'README.md').unlink(), os.mkfifo(tree/'README.md'))),
        ('wrong_file_mode', lambda: (tree/'README.md').chmod(0o755)),
        ('missing_file', lambda: (tree/'README.md').unlink()),
    ]:
        reset(); mutate(); out.append(attempt('fixed_pin_'+label, lambda: authenticate(tree)))
    reset()
    marker=tree/'STARTUP_MARKER'
    p=tree/'verify_publication.py'
    p.write_text("from pathlib import Path\nPath(__file__).with_name('STARTUP_MARKER').write_text('executed')\n"+p.read_text())
    row=attempt('fixed_pin_malicious_startup_marker', lambda: authenticate(tree))
    row['marker_exists_after_gate']=marker.exists();row['mutated_program_executed']=False
    require(not marker.exists(), 'marker executed')
    out.append(row)
    shutil.rmtree(tree)
    return out

def resealed_parser_probes(work):
    out=[]; tree=work/'resealed_tree'; shutil.copytree(SOURCE, tree)
    known=known_module('verify_publication.py', tree)
    def manifest_probe(label, mutate, json_reject=False):
        path=tree/'PUBLICATION_MANIFEST.json'; original=path.read_bytes()
        changed=mutate(original); path.write_bytes(changed)
        out.append(attempt('legacy_resealed_'+label, lambda: known['manifest_check']('PUBLICATION_MANIFEST.json',sha(changed)), trust_model='new external digest supplied; known-good body'))
        if json_reject:
            out.append(attempt('strict_'+label, lambda: strict_json(changed)))
        path.write_bytes(original)
    manifest_probe('duplicate_json_key', lambda b:b.replace(b'{',b'{"problem_id":"WRONG",',1),True)
    for value,label in [('NaN','nan'),('Infinity','infinity'),('-Infinity','negative_infinity'),('1e999','overflow')]:
        manifest_probe(label, lambda b,v=value:b.replace(b'{',('{"probe":'+v+',').encode(),1),True)
    for label, mutate, cleanup in [
        ('unlisted_empty_directory',lambda:(tree/'extra').mkdir(),lambda:(tree/'extra').rmdir()),
        ('unlisted_fifo',lambda:os.mkfifo(tree/'extra.fifo'),lambda:(tree/'extra.fifo').unlink()),
        ('unlisted_symlink',lambda:(tree/'extra.link').symlink_to('README.md'),lambda:(tree/'extra.link').unlink()),
    ]:
        mutate();out.append(attempt('legacy_'+label,lambda:known['manifest_check']('PUBLICATION_MANIFEST.json',PUBLIC_SHA)));cleanup()
    # Legacy standalone author verifier checks a witness; it does not authenticate proof or metadata.
    author=known_module('author/verify.py')
    base=(SOURCE/'author/certificate.json').read_bytes()
    for value,label in [('NaN','nan'),('1e999','overflow')]:
        raw=base.replace(b'{',('{"alpha":'+value+',').encode(),1)
        out.append(attempt('legacy_certificate_duplicate_'+label,lambda r=raw:author['verify'](json.loads(r))))
        out.append(attempt('strict_certificate_duplicate_'+label,lambda r=raw:strict_json(r)))
    for label, value in [('initial_weights_dictionary',{'1/6':0,'1/3':0,'1/2':0}),('nonfinite_rational_string','NaN')]:
        cert=json.loads(base)
        cert['initial_weights' if label.startswith('initial') else 'alpha']=value
        out.append(attempt('legacy_certificate_'+label,lambda c=cert:author['verify'](c)))
    # Dictionary iteration happens to yield the correct rational strings in author
    # verify.py; audit A witness explicitly rejects this malformed container.
    cert=json.loads(base);cert['initial_weights']={'1/6':0,'1/3':0,'1/2':0}
    audit=known_module('audit_a/verify_audit.py')
    out.append(attempt('audit_certificate_initial_weights_dictionary',lambda:audit['witness'](cert)))
    shutil.rmtree(tree)
    return out

def zip_probes():
    out=[]
    def blob(names, mode=0o100644, declared_delta=0):
        bio=io.BytesIO()
        with zipfile.ZipFile(bio,'w') as z:
            for name in names:
                i=zipfile.ZipInfo(name);i.create_system=3;i.external_attr=mode<<16
                z.writestr(i,b'x')
        raw=bio.getvalue()
        if declared_delta:
            # Central directory uncompressed size field; local payload left intact.
            n=raw.index(b'PK\x01\x02')+24
            raw=raw[:n]+(1+declared_delta).to_bytes(4,'little')+raw[n+4:]
        rows=[{'path':n,'bytes':1,'sha256':sha(b'x')} for n in set(names)]
        return raw,rows
    for label,names,mode,delta in [
        ('absolute_path',['/x'],0o100644,0),('parent_traversal',['../x'],0o100644,0),
        ('dot_path',['./x'],0o100644,0),('backslash_path',['a\\x'],0o100644,0),
        ('windows_drive',['C:x'],0o100644,0),('duplicate_name',['x','x'],0o100644,0),
        ('symlink_mode',['x'],0o120777,0),('fifo_mode',['x'],0o010644,0),
        ('directory_mode',['x/'],0o040755,0),('executable_mode',['x'],0o100755,0),
        ('declared_size',['x'],0o100644,1),
    ]:
        raw,rows=blob(names,mode,delta)
        out.append(attempt('strict_zip_'+label,lambda b=raw,r=rows:zip_check(b,r)))
    raw,rows=blob(['x']);out.append(attempt('strict_zip_plain_regular',lambda:zip_check(raw,rows),False))
    # Separate legacy parser behavior from fixed-byte authentication of real archives.
    legacy=known_module('verify_publication.py')
    for name in ['/x','../x','./x','a\\x','C:x']:
        out.append(attempt('legacy_safe_path_'+name,lambda n=name:legacy['safe_path'](n)))
    return out

def legacy_inventory_probes(work):
    """Probe known-good legacy helpers under resealed synthetic metadata only."""
    tree=work/'legacy_helpers';tree.mkdir();out=[]
    module=known_module('verify_publication.py');module['ROOT']=tree
    expanded=tree/'expanded';expanded.mkdir();(expanded/'x').write_bytes(b'x')
    row={'path':'x','bytes':1,'sha256':sha(b'x')}
    (tree/'manifest.json').write_text(json.dumps({'files':[row]}))
    for label,mode in [('regular',0o100644),('symlink_metadata',0o120777),
                       ('fifo_metadata',0o010644),('executable_metadata',0o100755)]:
        bio=io.BytesIO()
        with zipfile.ZipFile(bio,'w') as z:
            i=zipfile.ZipInfo('x');i.create_system=3;i.external_attr=mode<<16;z.writestr(i,b'x')
        (tree/'archive.zip').write_bytes(bio.getvalue())
        out.append(attempt('legacy_resealed_zip_'+label,
                   lambda:module['archive_check']('archive.zip','manifest.json','expanded'),label!='regular',
                   trust_model='synthetic archive and external manifest resealed; no fixed-pin bypass'))
    shutil.rmtree(tree)
    tree=work/'legacy_standalone_audit';shutil.copytree(SOURCE/'audit_a',tree)
    (tree/'MANIFEST.json').unlink();(tree/'AUDIT_REPORT.md').write_text('changed metadata')
    audit=known_module('audit_a/verify_audit.py')
    out.append(attempt('legacy_standalone_missing_audit_manifest_changed_report',lambda:audit['verify'](tree)))
    shutil.rmtree(tree)
    return out

def positive_runs(work):
    moved=work/'relocated';shutil.copytree(SOURCE,moved)
    authenticate(moved)
    unrelated=work/'unrelated_working_directory';unrelated.mkdir()
    rows=[]
    for root,label in [(SOURCE,'frozen'),(moved,'relocated')]:
        for flags in MODES:
            for script in ['author/verify.py','audit_a/verify_audit.py']:
                for args in [[],['--self-test']]:
                    authenticate(root)
                    r=run(root/script,args,flags,unrelated);r['location']=label
                    require(r['returncode']==0 and r.get('result',{}).get('status')=='PASS','positive checker failed')
                    rows.append(r)
        for flags in MODES:
            authenticate(root)
            r=run(root/'verify_publication.py',['--manifest-sha256',PUBLIC_SHA],flags,unrelated);r['location']=label
            require(r['returncode']==0 and r.get('result',{}).get('status')=='PASS','publication replay failed')
            require(r['result']['external_inputs']['status']=='NOT_RUN','source-free status wrong')
            rows.append(r)
    return rows

def private_provenance(work, moved):
    repo=next(p for p in AUDIT.parents if (p/'unsolved_math_prioritization').is_dir())
    corpus=repo/'unsolved_math_prioritization'
    paths={'catalog.json':corpus/'catalog.json','problems.json':corpus/'cache/problems.json',
           'research_results.json':corpus/'cache/research_results.json',
           'cities-notes.pdf':AUDIT/'private_sources/cities-notes.pdf',
           'cities-2012.pdf':AUDIT/'private_sources/1209.5120v1.pdf'}
    # Exact ordinary-file hardlinks avoid a second large corpus allocation. The
    # inspected checker only read_bytes() these inputs; this harness never writes,
    # chmods or truncates a hardlink. Malformed tests unlink before creating bytes.
    fixture=work/'private_fixture';fixture.mkdir();cdir=fixture/'corpus';cdir.mkdir();pdf=fixture/'pdf';pdf.mkdir()
    cat=rec=report=None;input_rows=[]
    for name,path in paths.items():
        data=regular_bytes(path);require(pin(data)==INPUTS[name],'complete private input pin mismatch: '+name)
        dest=(cdir if name.endswith('.json') else pdf)/name
        os.link(path,dest)
        require(pin(regular_bytes(dest))==INPUTS[name],'linked input mismatch')
        input_rows.append({'name':name,'bytes':len(data),'sha256':sha(data)})
        if name.endswith('.json'):
            loaded=strict_json(data)
            if name in ('catalog.json','problems.json'):
                exact=[r for r in loaded if type(r.get('id')) in (str,int) and str(r['id'])=='9700026']
                require(len(exact)==1,'strict exact ID uniqueness failure')
                if name=='catalog.json':cat=exact[0]
                else:rec=exact[0]
            else:report=loaded[rec['problem_number']]
            del loaded
        del data
        gc.collect()
    pair=json.dumps([rec,report],sort_keys=True).encode();require(pin(pair)==PAIR_PIN,'canonical pair differs')
    require(cat['review_hash']==sha(pair) and cat['title']==rec['title'],'canonical identity mismatch')
    # Keep only exact private target objects in memory for minimal resealed probes.
    del pair
    rows=[]
    for root,label in [(SOURCE,'frozen'),(moved,'relocated')]:
        for flags in MODES:
            authenticate(root)
            r=run(root/'audit_a/verify_sources.py',[cdir,pdf],flags,work/'unrelated_working_directory');r['location']=label
            require(r['returncode']==0 and r.get('result',{}).get('status')=='PASS','complete source replay failed')
            rows.append(r)
        for flags in MODES:
            authenticate(root)
            r=run(root/'verify_publication.py',['--manifest-sha256',PUBLIC_SHA,'--corpus',cdir,'--sources',pdf],flags,work/'unrelated_working_directory');r['location']=label
            require(r['returncode']==0 and r.get('result',{}).get('external_inputs',{}).get('status')=='PASS','complete wrapper replay failed')
            rows.append(r)
    negatives=[]
    for name in INPUTS:
        path=(cdir if name.endswith('.json') else pdf)/name
        path.unlink()  # Detach the link before creating a malformed private fixture.
        path.write_bytes(b'independent deliberately invalid input')
        for flags in [[],['-O']]:
            authenticate()
            r=run(SOURCE/'audit_a/verify_sources.py',[cdir,pdf],flags,work/'unrelated_working_directory')
            require(r['returncode']!=0 and 'Input pin mismatch: '+name in r['stderr'],'source mutation did not fail at expected pin')
            r['target']=name;r['classification']='EXPECTED_REJECTION';negatives.append(r)
        path.unlink();os.link(paths[name],path)
    shutil.rmtree(fixture)
    probes=source_parser_probes(work,cat,rec,report)
    return {'status':'PASS','input_pins':input_rows,'strict_exact_id_count':1,
            'canonical_pair_bytes':PAIR_PIN[0],'canonical_pair_sha256':PAIR_PIN[1],
            'executions':rows,'source_input_negative_executions':negatives,
            'resealed_probes':probes,'private_fixtures_removed':True,
            'fixture_strategy':'Exact verified ordinary-file hardlinks with required basenames; no input writes/chmod/truncate. Malformed tests unlink the fixture link before writing a new independent file.'}

def source_parser_probes(work,cat,rec,report):
    tiny=work/'private_tiny';tiny.mkdir();c=tiny/'corpus';c.mkdir();p=tiny/'pdf';p.mkdir()
    # PDFs are tiny diagnostic stand-ins ONLY in this explicitly resealed model.
    for name in ['cities-notes.pdf','cities-2012.pdf']:(p/name).write_bytes(b'diagnostic placeholder')
    module=known_module('audit_a/verify_sources.py')
    base={'catalog.json':json.dumps([cat]).encode(),'problems.json':json.dumps([rec]).encode(),
          'research_results.json':json.dumps({rec['problem_number']:report}).encode()}
    out=[]
    def probe(label,changes,expected_reject=True):
        payloads={**base,**changes}
        for name,raw in payloads.items():(c/name).write_bytes(raw)
        module['PINS']={name:pin(regular_bytes((c if name.endswith('.json') else p)/name)) for name in INPUTS}
        out.append(attempt('legacy_source_resealed_'+label,lambda:module['verify'](c,p),expected_reject,
                           trust_model='input PINS resealed in known-good namespace; pair/statement constants unchanged'))
    probe('minimal_exact_pair',{},False)
    probe('duplicate_catalog_id',{'catalog.json':base['catalog.json'].replace(b'{',b'{"id":"WRONG",',1)})
    probe('duplicate_record_id',{'problems.json':base['problems.json'].replace(b'{',b'{"id":"WRONG",',1)})
    for literal,label in [('NaN','nan'),('1e999','overflow')]:
        probe('catalog_'+label,{'catalog.json':base['catalog.json'].replace(b'{',('{"probe":'+literal+',').encode(),1)})
    duplicate_report=b'{"'+rec['problem_number'].encode()+b'":null,'+base['research_results.json'][1:]
    probe('duplicate_report_key',{'research_results.json':duplicate_report})
    probe('duplicate_exact_catalog_row',{'catalog.json':json.dumps([cat,cat]).encode()})
    probe('duplicate_exact_record_row',{'problems.json':json.dumps([rec,rec]).encode()})
    probe('missing_report',{'research_results.json':b'{}'})
    changed=dict(cat);changed['rank']=935
    probe('wrong_rank',{'catalog.json':json.dumps([changed]).encode()})
    changed=dict(rec);changed['title']=rec['title']+' diagnostic mutation'
    probe('wrong_title',{'problems.json':json.dumps([changed]).encode()})
    changed=dict(rec);changed['statement']=rec['statement']+' diagnostic mutation'
    probe('wrong_statement',{'problems.json':json.dumps([changed]).encode()})
    for name,raw in [('duplicate_catalog_id',base['catalog.json'].replace(b'{',b'{"id":"WRONG",',1)),
                     ('catalog_nan',base['catalog.json'].replace(b'{',b'{"probe":NaN,',1)),
                     ('catalog_overflow',base['catalog.json'].replace(b'{',b'{"probe":1e999,',1)),
                     ('duplicate_report_key',duplicate_report)]:
        out.append(attempt('strict_source_'+name,lambda r=raw:strict_json(r)))
    for name,raw in base.items():(c/name).write_bytes(raw)
    pdf_path=p/'cities-notes.pdf';backing=tiny/'backing.pdf';backing.write_bytes(pdf_path.read_bytes())
    pdf_path.unlink();pdf_path.symlink_to(backing)
    module['PINS']={name:pin(((c if name.endswith('.json') else p)/name).read_bytes()) for name in INPUTS}
    out.append(attempt('legacy_resealed_source_pdf_symlink',lambda:module['verify'](c,p)))
    out.append(attempt('strict_source_pdf_symlink',lambda:regular_bytes(pdf_path)))
    fifo=tiny/'fifo';os.mkfifo(fifo)
    out.append(attempt('strict_source_fifo_before_open',lambda:regular_bytes(fifo)))
    shutil.rmtree(tiny)
    return out

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--provenance',action='store_true');args=parser.parse_args()
    require((HERE/'THREAT_SCOPE.md').is_file(),'write threat scope before execution')
    result={'timestamp_utc':datetime.now(timezone.utc).isoformat(),'python':sys.version,
            'harness_optimization':sys.flags.optimize,
            'harness_sha256':sha(regular_bytes(Path(__file__))),
            'scope':'Finite diagnostics, artifact identity and optional input provenance only; no theorem or priority certification.'}
    result['authentication']=authenticate()
    with tempfile.TemporaryDirectory(prefix='.disposable_',dir=HERE) as td:
        work=Path(td)
        result['positive_executions']=positive_runs(work)
        result['fixed_pin_probes']=fixed_pin_probes(work)
        result['resealed_parser_probes']=resealed_parser_probes(work)
        result['zip_probes']=zip_probes()
        result['legacy_inventory_probes']=legacy_inventory_probes(work)
        result['external_inputs']=private_provenance(work,work/'relocated') if args.provenance else {
            'status':'NOT_RUN','reason':'Optional complete-corpus/PDF provenance replay was not requested for this invocation.'}
    probes=result['fixed_pin_probes']+result['resealed_parser_probes']+result['zip_probes']+result['legacy_inventory_probes']
    if args.provenance:probes+=result['external_inputs']['resealed_probes']
    executions=result['positive_executions']+result['external_inputs'].get('executions',[])
    result['fresh_counts']={'top_level_positive_processes':len(executions),
                            'source_free_positive_processes':len(result['positive_executions']),
                            'optional_provenance_positive_processes':len(result['external_inputs'].get('executions',[])),
                            'probe_evaluations':len(probes),
                            'expected_rejections_observed':sum(r['classification']=='EXPECTED_REJECTION' for r in probes),
                            'legacy_limitations_accepted':sum(r['classification']=='LIMITATION_ACCEPTED' for r in probes),
                            'expected_acceptance_controls':sum(r['classification']=='EXPECTED_ACCEPTANCE' for r in probes),
                            'unexpected_rejections':sum(r['classification']=='UNEXPECTED_REJECTION' for r in probes),
                            'fixed_pin_probe_count':len(result['fixed_pin_probes']),
                            'fixed_pin_rejections':sum(r['rejected'] for r in result['fixed_pin_probes'])}
    result['fresh_counts']['source_input_negative_processes']=len(result['external_inputs'].get('source_input_negative_executions',[]))
    require(all(r['rejected'] for r in result['fixed_pin_probes']),'fixed-pin attack accepted')
    require(result['fresh_counts']['unexpected_rejections']==0,'positive control rejected')
    accepted={r['label'] for r in probes if r['classification']=='LIMITATION_ACCEPTED'}
    require(accepted <= LEGACY_ACCEPTED_LIMITATIONS,
            'unapproved intended-rejection acceptance: '+str(sorted(accepted-LEGACY_ACCEPTED_LIMITATIONS)))
    result['accepted_legacy_limitations_allowlist_check']='PASS'
    result['status']='PASS_WITH_DOCUMENTED_LEGACY_LIMITATIONS'
    output=HERE/('RESULTS_WITH_PROVENANCE.json' if args.provenance else 'RESULTS_SOURCE_FREE.json')
    output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':result['status'],'output':output.name,'counts':result['fresh_counts'],
                      'external_inputs':result['external_inputs']['status']},indent=2))

if __name__=='__main__':main()
