#!/usr/bin/env python3
"""Portable integrity and finite-control replay, not an analytic proof certificate."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parent


def require(condition, label):
    if not condition:
        raise ValueError(label)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def safe(name):
    p = PurePosixPath(name)
    return bool(name) and not p.is_absolute() and '..' not in p.parts and str(p) == name


def inventory(root):
    paths = list(root.rglob('*'))
    require(all(not p.is_symlink() for p in paths), 'symlinks forbidden')
    require(all(p.is_file() or p.is_dir() for p in paths), 'nonregular object')
    return {p.relative_to(root).as_posix() for p in paths if p.is_file()}


def manifest_check(root, name='MANIFEST.json'):
    manifest = json.loads((root/name).read_bytes())
    rows = manifest['files']
    names = [r['path'] for r in rows]
    require(len(names) == len(set(names)), 'duplicate manifest entry')
    require(all(safe(n) for n in names), 'unsafe manifest path')
    require(inventory(root) == set(names) | {name}, 'recursive file inventory mismatch')
    for row in rows:
        b = (root/row['path']).read_bytes()
        require(len(b) == row['bytes'], 'size mismatch: '+row['path'])
        require(digest(b) == row['sha256'], 'hash mismatch: '+row['path'])
    return len(names)


def run(script, args=()):
    env = os.environ.copy()
    env.pop('PYTHONOPTIMIZE', None)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    # -I isolates Python configuration; no -O is inherited from this wrapper.
    return subprocess.check_output([sys.executable, '-I', '-B', str(ROOT/script),
                                    *map(str, args)], cwd=ROOT, env=env)


def queue_check(path, record):
    b = path.read_bytes()
    require(len(b) == record['after_bytes'] and digest(b) == record['after_sha256'],
            'published whole-queue identity mismatch')
    old, new = record['old_row'].encode(), record['new_row'].encode()
    require(b.count(new) == 1, 'new target row not unique')
    before = b.replace(new, old, 1)
    require(len(before) == record['before_bytes'] and digest(before) == record['before_sha256'],
            'reconstructed original whole-queue identity mismatch')
    require([i for i,(x,y) in enumerate(zip(old.split(b'|'),new.split(b'|'))) if x!=y]
            == [8,9,11], 'not exactly Status, Turns and Findings')
    require(len(old.split(b'|')) == len(new.split(b'|')), 'queue cell count changed')
    require(b.splitlines(keepends=True)[record['physical_line']-1] == new,
            'queue physical line mismatch')
    return {'status':'PASS', 'changed_cells':['Status','Turns','Findings'],
            'other_bytes_preserved':True, 'stale_header_preserved':True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--queue', type=Path)
    parser.add_argument('--catalog', type=Path)
    parser.add_argument('--problems', type=Path)
    parser.add_argument('--research-results', type=Path)
    parser.add_argument('--source-dir', type=Path)
    args = parser.parse_args()
    optional = [args.catalog,args.problems,args.research_results,args.source_dir]
    require(not any(optional) or all(optional), 'provide all four external-input arguments or none')
    count = manifest_check(ROOT, 'PUBLICATION_MANIFEST.json')
    verdict = json.loads((ROOT/'VERDICT.json').read_bytes())
    archive_results = []
    for row in verdict['archives']:
        archive = ROOT/row['path']
        b = archive.read_bytes()
        require(len(b) == row['bytes'] and digest(b) == row['sha256'], 'archive identity')
        directory = ROOT/row['extracted_directory']
        manifest_check(directory)
        names = inventory(directory)
        with zipfile.ZipFile(archive) as z:
            members = z.namelist()
            require(z.testzip() is None, 'archive CRC')
            require(len(members) == len(set(members)) == row['members'], 'archive member count')
            require(all(safe(n) for n in members), 'unsafe ZIP member')
            require(set(members) == names, 'ZIP/directory inventory')
            for name in members:
                require(z.read(name) == (directory/name).read_bytes(), 'ZIP/directory byte identity')
        archive_results.append({'path':row['path'],'members':len(names),'sha256':digest(b),'bytes':len(b)})
    for name in inventory(ROOT/'author'):
        require((ROOT/'author'/name).read_bytes() == (ROOT/'audit/author'/name).read_bytes(),
                'embedded author mismatch')
    manifest_check(ROOT/'audit/author')
    author = run('author/verify.py')
    require(author == (ROOT/'author/verification.json').read_bytes(), 'author output not byte-identical')
    require(json.loads(author)['assertions'] == 4187, 'author control count')
    first = run('audit/verify_independent.py')
    require(first == (ROOT/'audit/verification_portable.json').read_bytes(),
            'portable first audit output not byte-identical')
    require(json.loads(first)['assertions'] == 2911, 'portable count')
    author_zip = ROOT/'archives/QUASICONICAL_30005613_AUTHOR_SAFE_FREEZE.zip'
    first_zip = ROOT/'archives/QUASICONICAL_30005613_INDEPENDENT_AUDIT_SAFE_FREEZE.zip'
    with_zip = json.loads(run('audit/verify_independent.py', ['--author-zip', author_zip]))
    require(with_zip['assertions'] == 2923, 'first audit optional-archive count')
    require(with_zip['author']['author_assertions'] == 4187 and
            with_zip['author']['output_byte_reproduced'], 'nested author replay')
    second = json.loads(run('second_audit/verify_second.py',
                           ['--author-zip',author_zip,'--first-audit-zip',first_zip]))
    recorded = json.loads((ROOT/'second_audit/verification.json').read_bytes())
    require(second['status'] == 'PASS' and second['exact_tail_checks'] == 2304,
            'second audit replay')
    for key in ['inputs','not_certified','scope','exact_tail_checks','status']:
        require(second[key] == recorded[key], 'second audit frozen field mismatch: '+key)
    require(second['package']['manifest_matches'], 'second package manifest')
    external = {'status':'NOT_RUN','reason':'Optional source corpora and PDFs absent from the distribution.'}
    if all(optional):
        full = run('audit/verify_independent.py', ['--author-zip',author_zip,
                   '--catalog',args.catalog.resolve(),'--problems',args.problems.resolve(),
                   '--research-results',args.research_results.resolve(),'--source-dir',args.source_dir.resolve()])
        require(full == (ROOT/'audit/verification.json').read_bytes(),
                'full optional output not byte-identical')
        require(json.loads(full)['assertions'] == 2944, 'full optional count')
        external = {'status':'PASS','assertions':2944,'frozen_output_byte_identical':True}
    queue = queue_check(args.queue.resolve(),verdict['queue']) if args.queue else {'status':'NOT_RUN'}
    # Recheck that replay did not alter the distributed inventory or bytes.
    require(manifest_check(ROOT,'PUBLICATION_MANIFEST.json') == count, 'post-replay inventory')
    print(json.dumps({'status':'PASS','payload_files':count,'archives':archive_results,
                     'author_assertions':4187,'author_output_byte_identical':True,
                     'first_portable_assertions':2911,'first_portable_output_byte_identical':True,
                     'first_with_author_archive_assertions':2923,'second_exact_tail_checks':2304,
                     'second_recorded_input_fields_match':True,'external_inputs':external,'queue':queue,
                     'scope':'Finite diagnostics and file integrity only; analytic theorem, historical novelty and external expert acceptance are not certified by this program.'},indent=2,sort_keys=True))


if __name__ == '__main__':
    main()
