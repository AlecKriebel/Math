#!/usr/bin/env python3
"""Read-only offline replay. Read this source and both own checkers first.

No provider calls, Git operations, imports of author code, file writes, or
candidate execution. Manifest authenticity must be established externally.
This script checks cached evidence and redoes finite mathematical searches;
it does not establish current provider state or universal novelty.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import zipfile


def require(ok, reason):
    if not ok:
        raise RuntimeError(reason)


def digest(b):
    return hashlib.sha256(b).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--optimized', action='store_true')
    args = ap.parse_args()
    root = Path(__file__).resolve().parent
    manifest = json.loads((root/'SEALED_MANIFEST.json').read_text())
    paths = set()
    for member in manifest['members']:
        rel = member['path']; p = root/rel
        require(not Path(rel).is_absolute() and '..' not in Path(rel).parts,
                'Unsafe manifest path')
        require(rel not in paths and not p.is_symlink(), 'Duplicate or linked member')
        paths.add(rel); data = p.read_bytes()
        require(len(data) == member['bytes'] and digest(data) == member['sha256'],
                'Manifest identity failed: '+rel)
        require(member['private'] == rel.startswith('private_sources/'), 'Privacy flag mismatch')
    actual = {str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()
              and p.name != 'SEALED_MANIFEST.json'}
    require(paths == actual, 'Unsealed or missing members')
    src = root/'private_sources'
    binding = json.loads((root/'LIVE_SOURCE_BINDING_CHECK.json').read_text())
    require(binding['head'] == 'e4cd1f31dbce8f60931012d96ea214de9c1e1ab7' and
            binding['base'] == '4b27092a448d53b61408355ce44ec38d103a1ce4' and
            binding['complete_paths_count'] == 8 and binding['queue_changed'] is False,
            'Wrong cached candidate binding')
    meta = json.loads((src/'LIVE_PR_BINDING_0.json').read_text())['value']['structuredContent']
    filepaths = json.loads((src/'LIVE_PR_BINDING_1.json').read_text())['value']['structuredContent']['filenames']
    compare = json.loads((src/'LIVE_PR_BINDING_2.json').read_text())['value']['structuredContent']
    api = json.loads((src/'LIVE_API_BLOBS.json').read_text())['blobs']
    prefix = 'unsolved_math_prioritization/attempts/2398/'
    expected = [prefix+x['file'] for x in binding['checks']]
    require(meta['head_sha'] == binding['head'] and meta['base_sha'] == binding['base'], 'Metadata mismatch')
    require(sorted(filepaths) == sorted(expected) == sorted(x['filename'] for x in compare['files'])
            and all(x['status'] == 'added' for x in compare['files']), 'Complete path mismatch')
    body = (src/'PR_BODY.md').read_bytes()
    require(body == meta['body'].encode() and digest(body) == binding['body_sha256'], 'Body mismatch')
    for item in binding['checks']:
        b = (src/('PR_'+item['file'])).read_bytes()
        a = next(x for x in api if x['file'] == item['file'])
        h = hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
        require(b == a['result']['structuredContent']['content'].encode() and
                digest(b) == item['sha256'] and h == item['git_blob'] == a['sha'],
                'Complete source identity mismatch')
    nber = (src/'NBERpdf.pdf').read_bytes()
    require(nber == (src/'NBERdoi.pdf').read_bytes() and
            digest(nber) == 'c20f54b865a2600905a7bcb3a0aa949ddc80ac8f83dac0d69ec48017354f107b',
            'Published PDF identity mismatch')
    archive = (src/'ChanReleaseArchive.zip').read_bytes()
    archive_sha = '01bcc4420465143dff00b605b2140ae225dc44a445a540c8e9c49ffec9de92d7'
    require(digest(archive) == archive_sha, 'Frozen supporting archive mismatch')
    registry = (src/'ChanDatacite.json').read_text()
    require(archive_sha in registry, 'Registered archive hash missing')
    inv = json.loads((root/'ARCHIVE_MEMBER_PINS.json').read_text())['members']
    with zipfile.ZipFile(src/'ChanReleaseArchive.zip') as z:
        require(sorted(x.filename for x in z.infolist() if not x.is_dir()) == sorted(x['path'] for x in inv),
                'Support inventory mismatch')
        for item in inv:
            b = z.read(item['path'])
            require(len(b) == item['bytes'] and digest(b) == item['sha256'], 'Support member mismatch')
    modes = [()] if not args.optimized else [(),('-O',),('-OO',)]
    outcomes = []
    env = dict(os.environ); env['PYTHONDONTWRITEBYTECODE'] = '1'
    for program, flags, expected_output in [
        ('verify_chan_independent.py', ['--edgelist',str(src/'Chan_graph__candidate60.edgelist'),
                                       '--graph6',str(src/'Chan_graph__candidate60.g6')],
         'd901772c1e72a4ea0cbb923a5de5f84917cfc7c01ef02f0485e17550b770d65d'),
        ('verify_chan_direct.py',[str(src/'Chan_graph__candidate60.edgelist')],
         '1cb63140d3776a4d28ba30abce4fa1576096c689bece48eff604acd14f1e3a91')]:
        for mode in modes:
            result = subprocess.run([sys.executable,'-B',*mode,str(root/program),*flags],
                                    capture_output=True,env=env,check=False)
            require(result.returncode == 0 and not result.stderr and digest(result.stdout) == expected_output,
                    'Independent finite replay failed: '+program+' '+str(mode))
            outcomes.append({'program':program,'mode':list(mode),'stdout_sha256':digest(result.stdout)})
    print(json.dumps({'sealed_members_checked':len(paths),'cached_complete_PR_texts_checked':8,
                      'support_archive_members_checked':len(inv),'finite_replays':outcomes,
                      'status':'PASS',
                      'limits':'Offline cached identity and finite proof replay only; no live ledger/provider state, Lean replay, infinite-family execution or priority certification.'},indent=2))


if __name__ == '__main__':
    main()
