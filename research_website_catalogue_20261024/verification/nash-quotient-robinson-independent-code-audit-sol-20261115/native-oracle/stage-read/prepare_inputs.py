"""Freeze only this triplet's private inputs; no source/site/Git mutation.

All raw snapshots live in ignored blobs/. This is a new bounded custody tool,
not an acquisition, scientific campaign, legacy builder, or publication tool.
"""
import datetime
import hashlib
import json
import pathlib
import re
import sys
import xml.etree.ElementTree as ET

A = pathlib.Path(__file__).resolve().parent
P = A.parent.parent
W = pathlib.Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
IDS = ['23578599', '23423736', '23333002']
AUTH = ['82285503c698166536196e2f3ece128d44544bd47c03c64dee8b86caaac2bbac',
        '6391146d989750994bc8270af220d5e57781540c5b30066eb63b90cd08380d5c',
        '715f777230917df4e6c798468fe7659ab7ba69b155ecb515601765fe632f61cc']
FACT = P / 'verification/nash-quotient-robinson-editorial-fact-audit-sol-20261115'


def need(ok, why):
    if not ok:
        raise ValueError(why)


def digest(b):
    return hashlib.sha256(b).hexdigest()


def listing(root):
    paths = list(root.rglob('*'))
    need(not any(p.is_symlink() for p in paths), 'no source snapshot symlinks')
    return sorted(p for p in paths if p.is_file())


def write_json(name, data):
    path = A / name
    need(not path.exists(), 'immutable freeze already exists: ' + name)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def snapshot(path):
    b = path.read_bytes()
    h = digest(b)
    dest = A / 'blobs' / h
    if dest.exists():
        need(dest.read_bytes() == b, 'existing content-address blob identity')
    else:
        dest.write_bytes(b)
    return {'path': str(path), 'bytes': len(b), 'SHA256': h, 'blob': 'blobs/' + h}


def fresh613():
    m = json.loads((FACT / 'INPUT_MANIFEST.json').read_bytes())
    need(digest((FACT / 'INPUT_MANIFEST.json').read_bytes()) ==
         '5fe174024fe1855b2be5ff3f099d8e2b01ef29dac74a3ab32ff667e105efa102', 'fact input pin')
    need(len(m['files']) == 613, 'all613 originals')
    for r in m['files']:
        b = pathlib.Path(r['path']).read_bytes()
        need(len(b) == r['bytes'] and digest(b) == r['SHA256'], 'original613: ' + r['path'])
    ns = []
    for rid, sc, ed in zip(IDS, [58, 232, 122], [56, 62, 77]):
        for folder, count in [('sources', sc), ('reviews/editorial', ed)]:
            root = P / 'papers' / rid / folder
            actual = [str(p) for p in listing(root)]
            expected = sorted(r['path'] for r in m['files'] if str(root) + '/' in r['path'])
            need(actual == expected and len(actual) == count, 'entire namespace: ' + str(root))
            ns.append({'root': str(root), 'files': actual, 'count': count})
    return m, ns


def sources():
    original, namespaces = fresh613()  # MUST precede every raw input copy.
    all_paths = []
    for rid, h in zip(IDS, AUTH):
        auth = P / ('verification/root-editorial-' + rid + '-20261115.json')
        need(digest(auth.read_bytes()) == h, 'whole root editorial adoption')
        root = P / 'papers' / rid
        found = listing(root)
        namespaces.append({'root': str(root), 'files': [str(x) for x in found], 'count': len(found)})
        all_paths += found
        all_paths += [auth, P / ('verification/root-clearance-' + rid + '-20261115.json')]
    all_paths += [FACT / n for n in ['INPUT_MANIFEST.json', 'SEAL.json', 'VERDICT.json', 'verify_custody_read_only.py']]
    all_paths += [P / 'verification/root-nash-quotient-robinson-fact-audit-closure-20261115.json']
    rows = [snapshot(p) for p in sorted(set(all_paths))]
    fresh613()
    for n in namespaces:
        need([str(x) for x in listing(pathlib.Path(n['root']))] == n['files'], 'namespace unchanged across copy')
    write_json('SOURCE_INPUTS.json', {'UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'fresh_guarded_originals_613': original, 'namespaces': namespaces, 'files': rows,
               'raw_copies_ignored_before_creation': True, 'all_scientific_objects_preserved_as_whole_bytes': True,
               'row125_owner_filtered72_not_full77_limitation_retained': True})
    print(json.dumps({'phase': 'source freeze', 'original613': 613, 'full_editorial_files': 195,
                      'full_paper_and_authority_snapshot_files': len(rows), 'namespaces': len(namespaces)}))


def website():
    need((A / 'SOURCE_INPUTS.json').exists(), 'source freeze must precede website freeze')
    fresh613()
    # Parent supplied this exact GO after its separate ten-path installation.
    commit = 'e2e064c48755452a56c2a31207fb12d7e55074fb'
    receipt = P / 'verification/cellularization-tree-production-integration-root-20261115/installation.json'
    old = json.loads(receipt.read_bytes())
    need(old['commit'] == commit and old['public_files'] == 593 and
         old['index_entries'] == 87 and old['sitemap_locations'] == 88, 'actual parent installation receipt')
    public = listing(W / 'public')
    need(len(public) == 593, 'fresh actual593 public files')
    index = (W / 'public/research/index.html').read_text()
    match = re.search(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', index, re.S)
    need(match is not None, 'current actual index JSONLD')
    schema = json.loads(match[1])
    need(schema['mainEntity']['numberOfItems'] == 87 and
         len(schema['mainEntity']['itemListElement']) == 87, 'actual87 typed ItemList records')
    sitemap = (W / 'public/research/sitemap.xml').read_bytes()
    need(len(ET.fromstring(sitemap)) == 88, 'actual88 complete sitemap nodes')
    rows = [snapshot(p) for p in public]
    configs = [snapshot(W / n) for n in ['firebase.json', '.firebaserc']]
    write_json('WEBSITE_BASELINE.json', {'UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'root_GO_commit': commit, 'installation_receipt': snapshot(receipt), 'website_root': str(W),
               'public_files': rows, 'site_configs': configs, 'prior_index_whole_schema': schema,
               'public_count': 593, 'index_count': 87, 'sitemap_count': 88,
               'expected_virtual_counts': [605, 90, 91], 'Git_index_or_ref_control_frozen': False,
               '121122_live_browser_native_publication_complete_claimed': False})
    print(json.dumps({'phase': 'website freeze', 'GO_commit': commit, 'public_files': len(rows),
                      'index_entries': 87, 'sitemap_nodes': 88, 'virtual_expected': [605, 90, 91]}))


if __name__ == '__main__':
    need(sys.argv[1:] in (['sources'], ['website']), 'choose current sources or authorized website freeze')
    ignore = (A / '.gitignore').read_text().splitlines()
    need('inputs/' in ignore and 'blobs/' in ignore, 'entire raw input/blob directories ignored first')
    (A / 'inputs').mkdir(exist_ok=True)
    (A / 'blobs').mkdir(exist_ok=True)
    sources() if sys.argv[1] == 'sources' else website()
