#!/usr/bin/env python3
"""Replay integrity and bounded sanity checks, not a formal proof verifier.

Read-only inputs; no network, extraction, execution of archive members, or uploads.
The human mathematical and source audit is recorded separately in AUDIT.md.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path, PurePosixPath
import stat
import zipfile

AUTHOR_ZIP = (9846, '8131ce688a36e732a7fc6a97e59179c4b2d6a4c5131e49ce305566f811439f64')
AUTHOR_MANIFEST = (1517, '04af8441ecfc9b46c1ffde3cb679d42ce4968aac5ae9df5cf60fe2c155d8b710')
DATASETS = {
 'catalog': (21735099, '891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566'),
 'problems': (68931837, '04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf'),
 'reports': (80334822, '8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b'),
}
PDFS = {
 'wcnt1989.pdf': (12795383, '0bf278cd5df293f04915b5a93264368b4f7cebcabd17c364eca07060f4c06d7e'),
 'katz_tao.pdf': (113580, '4175c00f29cbc9de195ab998db8d907fc8b5f57ea490c218fb6e6780f4592841'),
 'lemm.pdf': (99984, 'e6cae3a82a086b704409be54aedd4486e0775e3dbe422fb3066abf6328703b1d'),
 'georgiev_et_al.pdf': (12141713, '77b43844077c98c26dfc76ad391cadbbd53d48a1d290ddae575ff4d1bcdef9d2'),
}
MEMBERS = ['APPROACH_LOG.md', 'PROOF.md', 'REFERENCES.md', 'REPORT.md', 'STATUS.json', 'VERIFICATION_METADATA.json']

def require(condition, label):
    if not condition:
        raise ValueError(label)

def digest(b):
    return hashlib.sha256(b).hexdigest()

def checked_bytes(path, expected):
    b = Path(path).read_bytes()
    require((len(b), digest(b)) == expected, 'Pin mismatch: ' + Path(path).name)
    return b

def differences(a):
    return {y-x for x in a for y in a if y != x and 2*y-x in a}

def run(args):
    raw = checked_bytes(args.author_archive, AUTHOR_ZIP)
    m = json.loads(checked_bytes(args.author_manifest, AUTHOR_MANIFEST))
    member_pins = []
    with zipfile.ZipFile(args.author_archive) as z:
        require(z.namelist() == MEMBERS, 'Unexpected member order, names, or duplicates')
        require(z.testzip() is None, 'ZIP CRC failure')
        require(len(m['members']) == len(MEMBERS), 'Manifest member count')
        for entry in m['members']:
            name = entry['path']
            pp = PurePosixPath(name)
            require(not pp.is_absolute() and '..' not in pp.parts, 'Unsafe member path')
            info = z.getinfo(name)
            mode = info.external_attr >> 16
            require(stat.S_ISREG(mode) and not (mode & 0o111), 'Unexpected archive member mode')
            require(not (info.flag_bits & 1), 'Encrypted member')
            b = z.read(name)
            require((len(b), digest(b)) == (entry['bytes'], entry['sha256']), 'Member pin mismatch')
            require(name.endswith(('.md', '.json')), 'Unexpected member format')
            b.decode('utf-8')
            if name.endswith('.json'):
                json.loads(b)
            member_pins.append(dict(entry))
    datasets = {}
    parsed = {}
    for name, expected in DATASETS.items():
        b = checked_bytes(getattr(args, name), expected)
        parsed[name] = json.loads(b)
        datasets[name] = {'bytes': len(b), 'sha256': digest(b), 'pin_match': True}
    records = [p for p in parsed['problems'] if p['id'] == 2487]
    cats = [c for c in parsed['catalog'] if str(c['id']) == '2487']
    require(len(records) == len(cats) == 1, 'Nonunique exact ID')
    p, cat = records[0], cats[0]
    require(p['problem_number'] == cat['problem_number'] == 'EP-1097', 'Problem number mismatch')
    r = parsed['reports'].get(p['problem_number'], {})
    pair_hash = digest(json.dumps([p, r], sort_keys=True).encode('utf-8'))
    statement_hash = digest(p['statement'].encode('utf-8'))
    require(pair_hash == cat['review_hash'] == '663b152e01a8b4f63b20c09df050ed879d3be91cd151ec711f936c718307706b', 'Pair hash mismatch')
    require(statement_hash == cat['statement_hash'] == '2befcb408ac4d5dc5640cc40296890b42e63c4f5837952f617b56864fa134efd', 'Statement hash mismatch')
    require('EP-1097' not in parsed['reports'] and r == {}, 'Changed report-key state')
    require(cat['rank'] == 904 and cat['turns_used'] == 0 and cat['turn_limit'] == 5, 'Catalog scheduling fields')
    pdfs = []
    for name, expected in PDFS.items():
        b = checked_bytes(Path(args.pdf_directory)/name, expected)
        require(b.startswith(b'%PDF-'), 'Not a PDF')
        pdfs.append({'name': name, 'bytes': len(b), 'sha256': digest(b), 'pin_match': True})
    forward_count = 0
    universe = list(range(-3, 4))
    for mask in range(1 << len(universe)):
        a = {x for i,x in enumerate(universe) if mask >> i & 1}
        edges = {(u,v) for u in a for v in a if u != v and (u+v)%2 == 0 and (u+v)//2 in a}
        c = {u+v for u,v in edges}
        e = {u-v for u,v in edges}
        require(c <= {2*x for x in a}, 'Forward sum inclusion')
        require(e == {-2*d for d in differences(a)}, 'Forward difference equality')
        forward_count += 1
    reverse_count = 0
    uv = {-1, 0, 1}
    possible = list(itertools.product(sorted(uv), repeat=2))
    for mask in range(1 << len(possible)):
        g = {edge for i,edge in enumerate(possible) if mask >> i & 1}
        c = {u+v for u,v in g}
        e = {u-v for u,v in g}
        s = {2*x for x in uv} | c
        n = max(len(uv), len(c))
        require(len(s) <= 3*n, 'Reverse size bound')
        require({-d for d in e if d} <= differences(s), 'Reverse inclusion')
        require(len(e) <= len(differences(s))+1, 'Zero adjustment')
        reverse_count += 1
    seeds = []
    for k in range(1, 7):
        b = {sum(d*5**i for i,d in enumerate(t)) for t in itertools.product([0,1], repeat=k)}
        c = {sum(d*5**i for i,d in enumerate(t)) for t in itertools.product([1,2], repeat=k)}
        twice_b = {2*x for x in b}
        s = twice_b | c
        require(len(b) == len(c) == 2**k, 'Seed factor count')
        require(len(twice_b & c) == 1 and len(s) == 2**(k+1)-1, 'Seed union count')
        actual = differences(s)
        witnessed = set()
        for t in itertools.product([-1,0,1], repeat=k):
            pairs = [{-1:(1,0), 0:(1,1), 1:(0,1)}[digit] for digit in t]
            u = sum(pair[0]*5**i for i,pair in enumerate(pairs))
            v = sum(pair[1]*5**i for i,pair in enumerate(pairs))
            d = sum(x*5**i for i,x in enumerate(t))
            require(2*u in s and u+v in s and 2*v in s, 'Seed AP witness')
            require(d == v-u, 'Seed difference')
            witnessed.add(d)
        require(len(witnessed) == 3**k and (witnessed-{0}) <= actual, 'Seed distinct differences')
        require(len({d for d in actual if d > 0})*2 == len(actual), 'Signed convention')
        require(differences({x+1 for x in s}) == actual, 'Positive translation convention')
        seeds.append({'k': k, 'set_size': len(s), 'witnessed_nonzero_differences': 3**k-1, 'actual_nonzero_differences': len(actual), 'pass': True})
    return {
        'schema': 'independent-audit-replay-v1', 'problem_id': 2487, 'problem_number': 'EP-1097',
        'all_checks_passed': True,
        'author_archive': {'bytes': len(raw), 'sha256': digest(raw), 'member_count': len(MEMBERS), 'original_unchanged': True},
        'author_members': member_pins,
        'dataset_integrity': datasets,
        'identity': {'statement_sha256': statement_hash, 'pair_sha256': pair_hash, 'exact_report_key_present': False, 'reports_get_fallback_is_empty_object': True, 'rank': cat['rank'], 'turns_used': cat['turns_used'], 'turn_limit': cat['turn_limit']},
        'source_pdf_integrity': pdfs,
        'bounded_sanity_checks': {'forward_all_subsets_of_minus3_to3': forward_count, 'reverse_all_graphs_on_three_by_three': reverse_count, 'seed_replays': seeds},
        'scope': 'Integrity and bounded examples only. General mathematical correctness is established by the authored human-readable audit; published optimization values are not certified by this program.'
    }

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    for flag in ['author-archive','author-manifest','catalog','problems','reports','pdf-directory']:
        parser.add_argument('--'+flag, required=True)
    print(json.dumps(run(parser.parse_args()), indent=2, sort_keys=True))
