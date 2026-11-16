#!/usr/bin/env python3
"""Default offline read-only closure of this audit's exact owned namespace.

No imports of project/source code, foreign paths, network, subprocesses, renderer,
scientific computations, fixtures or writes. This is custody, not fact proof.
"""
import hashlib
import json
import os
from pathlib import Path
import stat

D = Path(__file__).absolute().parent
checks = 0

def need(ok, why):
    global checks
    checks += 1
    if not ok:
        raise ValueError(why)

def read(path):
    need(path.is_relative_to(D), 'outside owned path')
    before = path.lstat()
    need(stat.S_ISREG(before.st_mode), 'nonordinary owned file')
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        held = os.fstat(fd)
        need((before.st_dev, before.st_ino) == (held.st_dev, held.st_ino), 'inode identity')
        pieces = []
        while True:
            piece = os.read(fd, 1048576)
            if not piece:
                break
            pieces.append(piece)
        after = os.fstat(fd)
        need((held.st_size, held.st_mtime_ns, held.st_ctime_ns) == (after.st_size, after.st_mtime_ns, after.st_ctime_ns), 'held file changed')
        body = b''.join(pieces)
        need(len(body) == held.st_size, 'short read')
        return body
    finally:
        os.close(fd)

def pin(body):
    return {'bytes': len(body), 'SHA256': hashlib.sha256(body).hexdigest()}

def scan(root):
    need(root.is_relative_to(D) and stat.S_ISDIR(root.lstat().st_mode), 'owned root directory')
    files, directories = [], []
    def visit(path):
        with os.scandir(path) as iterator:
            entries = sorted(iterator, key=lambda x: x.name)
        for entry in entries:
            q = path / entry.name
            rel = q.relative_to(root).as_posix()
            mode = q.lstat().st_mode
            if stat.S_ISDIR(mode):
                directories.append(rel)
                visit(q)
            elif stat.S_ISREG(mode):
                files.append({'path': rel, **pin(read(q))})
            else:
                raise ValueError('symlink or special entry ' + rel)
    visit(root)
    return {'files': sorted(files, key=lambda x: x['path']), 'directories': sorted(directories)}

seal_body = read(D / 'FINAL_SEAL.json')
seal = json.loads(seal_body)
manifest_body = read(D / 'FINAL_MANIFEST.json')
need(pin(manifest_body) == seal['manifest'], 'same-buffer final manifest authentication')
manifest = json.loads(manifest_body)
actual = scan(D)
terminals = {'FINAL_MANIFEST.json', 'FINAL_SEAL.json'}
need(terminals <= {x['path'] for x in actual['files']}, 'exact final root terminals')
actual['files'] = [x for x in actual['files'] if x['path'] not in terminals]
need(actual['files'] == manifest['payload_files'], 'complete owned files/content')
need(actual['directories'] == manifest['declared_directories'], 'complete owned directory extent')
need(manifest['exact_root_terminal_exclusions'] == sorted(terminals), 'root terminal schema')
need(manifest['subtree_exclusions'] == [] and manifest['future_directory_or_file_exemptions'] == [], 'no future carveouts')
initial_body = read(D / 'INITIAL_SEAL.json')
need(pin(initial_body)['SHA256'] == '166ad0e5a3fb42c773db3fa676bc5d8f8ab89c3feba28180ed674e55774788c0', 'immutable initial seal')
initial = json.loads(initial_body)
im_body = read(D / 'INITIAL_MANIFEST.json')
need(pin(im_body) == {k: initial['manifest'][k] for k in ['bytes', 'SHA256']}, 'initial manifest identity')
im = json.loads(im_body)
for row in im['payload_files']:
    need(pin(read(D / row['path'])) == {k: row[k] for k in ['bytes', 'SHA256']}, 'original initial payload changed')
need(set(im['declared_directories']) <= set(actual['directories']), 'initial directory missing')
producer_seal_body = read(D / 'custody/editorial/FINAL_SEAL.json')
need(pin(producer_seal_body) == {'bytes': 3822, 'SHA256': 'a6199b1d554dcfaae1201c2440ec0b92d97caf5c6d71fc6e24919bf781e898a5'}, 'immutable producer seal')
producer_contract = json.loads(read(D / 'EDITORIAL_CUSTODY_CONTRACT.json'))
producer_copy = scan(D / 'custody/editorial')
need(producer_copy['files'] == producer_contract['producer_full_exact_namespace']['files'], 'complete producer snapshot file identity')
need(producer_copy['directories'] == producer_contract['producer_full_exact_namespace']['directories'], 'complete producer snapshot directory identity')
verdict = json.loads(read(D / 'VERDICT.json'))
need(verdict['status'] == 'NO_GO_EDITORIAL_COPY_FACT_TRANSCRIPTION', 'bounded literal disposition')
need(verdict['source_scientific_defect'] is None and verdict['follow_up'] is None, 'no invented scientific disposition')
need(verdict['publication_authority'] is False and verdict['canonical_url'] is None and verdict['AA'] is None, 'authority separation')
print(json.dumps({'status': 'PASS_OWNED_CUSTODY_EDITORIAL_FACT_NO_GO', 'checks': checks, 'payload_files': len(actual['files']), 'declared_directories': len(actual['directories']), 'initial_immutable': True, 'producer_original_FINAL_immutable_copy': True, 'editorial_fact_disposition': verdict['status'], 'scientific_replay': False, 'outside_owned_reads_or_writes': False, 'publication_authority': False, 'canonical_url': None, 'AA': None}, sort_keys=True))
