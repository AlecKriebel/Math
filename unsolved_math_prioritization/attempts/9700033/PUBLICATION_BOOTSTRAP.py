#!/usr/bin/env python3
"""Externally anchored publication replay. Full corpus/source inputs are mandatory.

Run a separately reviewed/trusted copy of this script against --publication-root.
A hash supplied by the same untrusted download is not an authenticity anchor.
No theorem, current literature openness, or novelty is certified by these tests.
"""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile

PROBLEM_ID = 9700033
PREFIX = 'SIRSN_UNBOUNDED_9700033_'
PINS = {
    'AUTHOR_EXTERNAL_MANIFEST.json': (999, '47cf2deb9dc39191fe5a7ff78aa2cef3bf245f4e9e47eae3092583e6735ea5c9'),
    'AUTHOR_SAFE_FREEZE.zip': (10738, '5bd8726384871fa1f3f97543db1a88d7340d2474287f8e90feb4509a73746523'),
    'INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json': (4039, '03bae1e769cbbd8ce9d7ae2f9b4dc8e340856528d1367192e9be0b0a475b27b6'),
    'INDEPENDENT_AUDIT_SAFE.zip': (59373, '303460b01cfc4a01aa7c44e9fa6787a8326eadfa4b20f89e708495acc9616df8'),
}
FLAGS = [[], ['-O'], ['-I'], ['-I', '-O']]
DIAGNOSTICS = {'scaling_rectangles':625, 'intensity_tail_sums':100,
               'last_exit_controls':9841, 'negative_math_controls':3}


def require(value, message):
    if not value:
        raise ValueError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def metadata(raw):
    return {'bytes':len(raw), 'sha256':digest(raw)}


def strict_json(raw):
    def unique(items):
        result = {}
        for key, value in items:
            require(key not in result, 'duplicate JSON key: ' + key)
            result[key] = value
        return result
    return json.loads(raw, object_pairs_hook=unique,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError('nonfinite JSON')))


def safe_name(name):
    p = PurePosixPath(name)
    require(isinstance(name, str) and name and str(p) == name and
            not p.is_absolute() and not any(x in ('..', '.') for x in p.parts) and
            '\\' not in name and '\x00' not in name, 'unsafe relative name')
    return p


def regular(path):
    path = Path(os.path.abspath(path))
    for part in [path, *path.parents]:
        require(not part.is_symlink(), 'symlink input: ' + str(part))
    require(stat.S_ISREG(path.stat().st_mode), 'not a regular file: ' + str(path))
    return path.read_bytes()


def bound(raw, entry, label):
    require(type(entry['bytes']) is int and entry['bytes'] >= 0 and
            len(raw) == entry['bytes'] and digest(raw) == entry['sha256'],
            'byte binding mismatch: ' + label)


def inventory(root):
    root = Path(os.path.abspath(root))
    for part in [root, *root.parents]:
        require(not part.is_symlink(), 'symlink directory: ' + str(part))
    require(root.is_dir(), 'missing root directory')
    files, dirs = {}, set()
    for p in root.rglob('*'):
        require(not p.is_symlink(), 'symlink member')
        name = p.relative_to(root).as_posix()
        safe_name(name)
        if p.is_dir():
            dirs.add(name)
        else:
            files[name] = regular(p)
    return files, dirs


def compare_tree(root, expected):
    files, dirs = inventory(root)
    allowed_dirs = {q.as_posix() for n in expected for q in PurePosixPath(n).parents if q.as_posix() != '.'}
    require(set(files) == set(expected) and dirs == allowed_dirs, 'extracted inventory mismatch')
    for name, raw in files.items():
        bound(raw, expected[name], name)
        if name.endswith('.json'):
            strict_json(raw)
    return files


def archive(raw, manifest):
    bound(raw, manifest['zip'], 'archive')
    entries = manifest['files']
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        infos = z.infolist()
        names = [i.filename for i in infos]
        require(len(names) == len(set(names)) and set(names) == set(entries), 'ZIP member inventory')
        files = {}
        for info in infos:
            safe_name(info.filename)
            kind = stat.S_IFMT(info.external_attr >> 16)
            require(not info.is_dir() and kind in (0, stat.S_IFREG) and not info.flag_bits & 1,
                    'ZIP special node or encrypted member')
            require(info.file_size == entries[info.filename]['bytes'], 'ZIP advertised size mismatch')
            data = z.read(info)
            bound(data, entries[info.filename], 'ZIP member ' + info.filename)
            if info.filename.endswith('.json'):
                strict_json(data)
            files[info.filename] = data
    return files


def publication_gate(root, pin):
    require(re.fullmatch('[0-9a-f]{64}', pin) is not None, 'invalid external publication pin')
    raw = regular(root / 'PUBLICATION_MANIFEST.json')
    require(digest(raw) == pin, 'external publication manifest pin mismatch')
    manifest = strict_json(raw)
    require(manifest['schema'] == 1 and manifest['problem_id'] == PROBLEM_ID and
            manifest['result'] == 'UNSOLVED_SCOPED_PARTIAL_ACCEPT_CORRECTED' and
            manifest['approaches_used'] == 3 and manifest['approach_limit'] == 5,
            'publication disposition mismatch')
    entries = manifest['files']
    require('PUBLICATION_MANIFEST.json' not in entries, 'manifest may not bind itself')
    for name in entries:
        safe_name(name)
    files = compare_tree(root, {**entries, 'PUBLICATION_MANIFEST.json':metadata(raw)})
    frozen = {}
    for suffix, (size, sha) in PINS.items():
        name = 'archives/' + PREFIX + suffix
        bound(files[name], {'bytes':size, 'sha256':sha}, 'fixed frozen ' + suffix)
        frozen[suffix] = files[name]
    am = strict_json(frozen['AUTHOR_EXTERNAL_MANIFEST.json'])
    au = strict_json(frozen['INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json'])
    author = archive(frozen['AUTHOR_SAFE_FREEZE.zip'], am)
    audit = archive(frozen['INDEPENDENT_AUDIT_SAFE.zip'], au)
    for prefix, contents in [('author/', author), ('audit/', audit)]:
        actual = {n[len(prefix):]:b for n,b in files.items() if n.startswith(prefix)}
        require(actual == contents, 'published extracted tree differs from archive: ' + prefix)
    require(audit['AUTHOR_SAFE_FREEZE.zip'] == frozen['AUTHOR_SAFE_FREEZE.zip'] and
            audit['AUTHOR_EXTERNAL_MANIFEST.json'] == frozen['AUTHOR_EXTERNAL_MANIFEST.json'],
            'nested original freeze mismatch')
    require({n[9:]:b for n,b in audit.items() if n.startswith('original/')} == author,
            'audit original differs from author archive')
    accepted = strict_json(audit['ACCEPTANCE.json'])
    require(accepted['status'] == 'ACCEPT_CORRECTED_SCOPED_PARTIAL' and
            accepted['disposition'] == 'UNSOLVED' and accepted['approaches_used'] == 3,
            'exact acceptance scope mismatch')
    for name, entry in accepted['corrected_files'].items():
        bound(audit['corrected/' + name], entry, 'accepted corrected ' + name)
    bound(audit['MEASURABILITY_CORRECTION.patch'], accepted['patch'], 'accepted correction patch')
    bound(audit['AUDIT.md'], accepted['audit_report'], 'accepted audit report')
    return manifest, author, audit, am, au, frozen['INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json']


def corpus_source_gate(args, audit, work):
    binding = strict_json(audit['INPUT_BINDINGS.json'])
    source_manifest = strict_json(audit['corrected/SOURCE_MANIFEST.json'])
    corpus = {}
    result = {'corpora':{}, 'source_files':{}, 'pdf_extractions':[]}
    for name, path in [('problems', args.problems), ('research_results', args.research_results), ('catalog', args.catalog)]:
        raw = regular(path)
        expected = binding['corpora'][name]
        bound(raw, expected, 'full corpus ' + name)
        bound(raw, source_manifest['corpora'][name], 'corrected source metadata ' + name)
        corpus[name] = strict_json(raw)
        require(len(corpus[name]) == expected['records'], 'corpus record count: ' + name)
        result['corpora'][name] = {**metadata(raw), 'records':len(corpus[name])}
    require(isinstance(corpus['problems'], list) and isinstance(corpus['catalog'], list)
            and isinstance(corpus['research_results'], dict), 'full corpus shape mismatch')
    records = [p for p in corpus['problems'] if str(p.get('id')) == str(PROBLEM_ID)]
    catalogs = [p for p in corpus['catalog'] if str(p.get('id')) == str(PROBLEM_ID)]
    require(len(records) == len(catalogs) == 1, 'exact ID not unique')
    record, catalog = records[0], catalogs[0]
    require(record['problem_number'] == catalog['problem_number'] == 'AMR-096-0033' and
            catalog['rank'] == 935, 'exact target identity mismatch')
    require(record['problem_number'] in corpus['research_results'], 'research report omitted')
    pair = json.dumps([record, corpus['research_results'].get(record['problem_number'], {})], sort_keys=True).encode()
    bound(pair, binding['canonical_pair'], 'reconstructed full canonical pair')
    bound(pair, source_manifest['canonical_pair'], 'canonical source metadata')
    require(catalog['review_hash'] == digest(pair), 'catalog review hash mismatch')
    require(regular(args.source_dir / 'canonical_pair.private.json') == pair, 'saved canonical pair differs')
    require(strict_json(regular(args.source_dir / 'catalog_record.private.json')) == catalog, 'saved catalog record differs')
    result['canonical_pair'] = {**metadata(pair), 'exact_saved_byte_match':True,
                                'catalog_review_hash_match':True, 'rank':935,
                                'problem_number':'AMR-096-0033'}
    extraction_checks = strict_json(audit['PDF_EXTRACTION_CHECKS.json'])
    source_pdf_pins = {s['local_pdf']['sha256']:s['local_pdf'] for s in source_manifest['sources'] if s.get('local_pdf')}
    for filename, expected in binding['source_files'].items():
        raw = regular(args.source_dir / filename)
        bound(raw, expected, 'source PDF ' + filename)
        require(expected['sha256'] in source_pdf_pins, 'PDF absent from corrected metadata')
        bound(raw, source_pdf_pins[expected['sha256']], 'corrected PDF metadata')
        local = work / filename
        local.write_bytes(raw)
        extracted = work / (Path(filename).stem + '.txt')
        proc = subprocess.run(['pdftotext', '-layout', str(local), str(extracted)], capture_output=True, timeout=60)
        require(proc.returncode == 0, 'PDF re-extraction failed: ' + filename)
        fresh = regular(extracted)
        saved = regular(args.source_dir / (Path(filename).stem + '.txt'))
        require(fresh == saved, 'fresh PDF extraction differs from saved extraction')
        check = [x for x in extraction_checks if x['source'] == Path(filename).stem]
        require(len(check) == 1, 'PDF extraction manifest entry')
        bound(fresh, {'bytes':check[0]['fresh_text_bytes'], 'sha256':check[0]['fresh_text_sha256']}, 'extracted text metadata')
        result['source_files'][filename] = metadata(raw)
        result['pdf_extractions'].append({'source':Path(filename).stem, **metadata(fresh), 'saved_match':True})
    require(len(result['source_files']) == 3, 'source PDF count mismatch')
    return result


def write_tree(root, files):
    root.mkdir()
    for name, raw in files.items():
        p = root / safe_name(name)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(raw)


def run(command, cwd):
    p = subprocess.run(command, cwd=cwd, capture_output=True, text=True, timeout=180)
    return {'returncode':p.returncode, 'stdout':p.stdout.strip(), 'stderr':p.stderr.strip()}


def expect(result, success, label):
    require((result['returncode'] == 0) == success, 'unexpected execution result: ' + label)
    return {'test':label, 'expected':'pass' if success else 'reject', **result}


def check_package_output(raw):
    value = strict_json(raw)
    require(value['status'] == 'PASS' and value['problem_id'] == PROBLEM_ID and
            value['diagnostics'] == DIAGNOSTICS, 'finite diagnostic counts mismatch')


def execute_verified(author, audit, am, au, audit_manifest_raw, work):
    # All archives, published extracted bytes, mandatory datasets and sources have
    # been checked before reaching here. Write only previously verified bytes.
    author_root, audit_root = work/'relocated author package', work/'relocated audit package'
    write_tree(author_root, author)
    write_tree(audit_root, audit)
    compare_tree(author_root, am['files'])
    compare_tree(audit_root, au['files'])
    manifest_path = work/'audit external manifest.json'
    manifest_path.write_bytes(audit_manifest_raw)
    audit_controls = []
    for flags in FLAGS:
        result = run([sys.executable, *flags, '-B', str(audit_root/'verify_audit.py'), str(manifest_path), PINS['INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json'][1]], work)
        label = 'relocated audit verifier ' + (' '.join(flags) or 'normal')
        audit_controls.append(expect(result, True, label))
        value = strict_json(result['stdout'])
        require(value['status'] == 'PASS' and value['files_bound'] == 22, 'audit summary mismatch')
        for entry in value['executions']:
            check_package_output(json.dumps(entry['result']))
    replay = run([sys.executable, '-I', '-B', str(audit_root/'replay_author_controls.py')], work)
    require(replay['returncode'] == 0, 'archived control replay failed: ' + replay['stderr'])
    controls = strict_json(replay['stdout'])
    require(controls['status'] == 'PASS' and controls['author_control_count'] == 21 and
            controls['independent_control_count'] == 17, 'archived control count mismatch')
    for group in ['author_controls', 'independent_controls']:
        for entry in controls[group]:
            if entry.get('returncode') == 0:
                check_package_output(entry['stdout'])
    tampered = work/'tampered audit'
    shutil.copytree(audit_root, tampered)
    (tampered/'corrected/RESULT.md').write_bytes(audit['corrected/RESULT.md'] + b'\n')
    audit_controls.append(expect(run([sys.executable, '-I', '-B', str(tampered/'verify_audit.py'), str(manifest_path), PINS['INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json'][1]], work), False, 'mutated corrected proof rejected by outer audit pin'))
    audit_controls.append(expect(run([sys.executable, '-I', '-B', str(audit_root/'verify_audit.py'), str(manifest_path), '0'*64], work), False, 'wrong external audit trust pin rejected'))
    patched = work/'exact patched derivative'
    write_tree(patched, author)
    patch = run(['patch', '-p1', '--batch', '--forward', '--fuzz=0', '-i', str(audit_root/'MEASURABILITY_CORRECTION.patch')], patched)
    require(patch['returncode'] == 0 and 'offset' not in patch['stdout'].lower() and 'fuzz' not in patch['stdout'].lower(), 'patch did not apply exactly')
    corrected = {n[10:]:b for n,b in audit.items() if n.startswith('corrected/')}
    expected = {n:metadata(b) for n,b in corrected.items()}
    actual = compare_tree(patched, expected)
    require(actual == corrected, 'exact patch replay differs from accepted derivative')
    require(len(actual) == 5, 'patch output file count')
    return {'author_control_count':21, 'fresh_control_count':17, 'audit_control_count':6,
            'author_and_fresh_controls':controls, 'audit_controls':audit_controls,
            'exact_patch_replay':{'status':'PASS', 'all_five_corrected_files':expected,
                                  'patch_stdout':patch['stdout']}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--publication-root', type=Path, required=True)
    parser.add_argument('--manifest-sha256', required=True)
    parser.add_argument('--problems', type=Path, required=True)
    parser.add_argument('--research-results', type=Path, required=True)
    parser.add_argument('--catalog', type=Path, required=True)
    parser.add_argument('--source-dir', type=Path, required=True)
    parser.add_argument('--receipt', type=Path)
    args = parser.parse_args()
    args.publication_root = args.publication_root.absolute()
    args.source_dir = args.source_dir.absolute()
    for name in ['problems', 'research_results', 'catalog']:
        setattr(args, name, getattr(args, name).absolute())
    manifest, author, audit, am, au, audit_manifest_raw = publication_gate(args.publication_root, args.manifest_sha256)
    with tempfile.TemporaryDirectory(prefix='sirsn-publication-') as tmp:
        work = Path(tmp)
        sources = corpus_source_gate(args, audit, work)
        execution = execute_verified(author, audit, am, au, audit_manifest_raw, work)
    receipt = {'status':'PASS', 'problem_id':PROBLEM_ID, 'disposition':'UNSOLVED_SCOPED_PARTIAL_ACCEPT_CORRECTED',
               'approaches_used':3, 'approach_limit':5, 'publication_manifest_sha256':args.manifest_sha256,
               'publication_files_bound':len(manifest['files']), 'full_corpus_source_validation':sources,
               'execution':execution, 'all_expected_outcomes':True,
               'limits':'External byte anchoring and finite diagnostics are not a continuum proof, human review, novelty certification, or standalone authenticity. Full corpus/source inputs are mandatory and never published by this program.'}
    if args.receipt:
        out = args.receipt.absolute()
        require(args.publication_root not in out.parents, 'receipt must be outside publication root')
        out.write_text(json.dumps(receipt, indent=2, sort_keys=True)+'\n')
    print(json.dumps(receipt, sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, TypeError, OSError, json.JSONDecodeError,
            subprocess.SubprocessError, zipfile.BadZipFile) as exc:
        print('FAIL: ' + str(exc), file=sys.stderr)
        sys.exit(1)
