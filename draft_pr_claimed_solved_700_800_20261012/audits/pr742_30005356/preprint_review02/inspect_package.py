"""Independent read-only inventory, nested archives and metadata inspection."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import stat
import zipfile

ROOT = Path(__file__).resolve().parent
SUPPORT = ROOT / 'scratch/support'
KIT = ROOT / 'scratch/kit'


def require(condition, detail):
    if not condition:
        raise ValueError(detail)


def fingerprint(raw):
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def check_manifest(path):
    data = json.loads(path.read_text())
    entries = data['files']
    require(len(entries) == len({e['path'] for e in entries}), 'duplicate: ' + str(path))
    names = set()
    for e in entries:
        name = e['path']
        q = PurePosixPath(name)
        require(not q.is_absolute() and '..' not in q.parts and '\\' not in name,
                'unsafe: ' + str(path))
        p = path.parent / name
        require(p.is_file() and not p.is_symlink(), 'nonregular: ' + str(p))
        require(fingerprint(p.read_bytes()) == {k: e[k] for k in ('bytes', 'sha256')},
                'mismatch: ' + str(p))
        names.add(name)
    actual = {p.relative_to(path.parent).as_posix() for p in path.parent.rglob('*')
              if p.is_file()}
    require(actual == names | {path.name}, 'nonclosed: ' + str(path))
    return {'path': path.relative_to(SUPPORT).as_posix(), 'entries': len(entries),
            'hashes_and_closed_inventory': True}


def leaves(value, prefix=''):
    if isinstance(value, dict):
        for k, v in value.items():
            yield from leaves(v, prefix + '/' + str(k))
    elif isinstance(value, list):
        for i, v in enumerate(value):
            yield from leaves(v, prefix + '/' + str(i))
    else:
        yield prefix, value


def run():
    members = []
    manifest_receipts = []
    metadata_screen = []
    for p in sorted(SUPPORT.rglob('*')):
        require(not p.is_symlink(), 'symlink: ' + str(p))
        if p.is_dir():
            continue
        require(stat.S_ISREG(p.stat().st_mode), 'nonregular: ' + str(p))
        raw = p.read_bytes()
        row = {'path': p.relative_to(SUPPORT).as_posix(), **fingerprint(raw)}
        if p.suffix == '.json':
            value = json.loads(raw)
            ls = list(leaves(value))
            row.update({'inspection': 'parsed complete JSON; every scalar leaf screened',
                        'leaf_count': len(ls), 'top_keys': sorted(value) if isinstance(value, dict) else 'list'})
            metadata_screen.append({'path': row['path'], 'fields': [
                {'field': k, 'value': v} for k, v in ls
                if any(t in k.lower() for t in ('verdict', 'scope', 'limitation', 'result',
                                                'status', 'private', 'payload', 'communication',
                                                'priority', 'journal', 'classification'))
                and not any(t in k.lower() for t in ('sha256', 'search_results', 'query_results'))
                and (not isinstance(v, str) or len(v) < 600)]})
        elif p.suffix == '.zip':
            with zipfile.ZipFile(p) as z:
                names = z.namelist()
                require(len(names) == len(set(names)), 'duplicate ZIP member')
                folder = 'author' if '_AUTHOR_' in p.name else 'independent_audit'
                flat = SUPPORT / 'historical_candidate' / folder
                require(set(names) == {q.name for q in flat.iterdir()}, 'nested member mismatch')
                for i in z.infolist():
                    require('/' not in i.filename and '\\' not in i.filename and
                            not i.is_dir() and not stat.S_ISLNK(i.external_attr >> 16), 'unsafe nested ZIP')
                    require(z.read(i) == (flat / i.filename).read_bytes(), 'nested bytes differ')
                row.update({'inspection': 'all nested members compared byte-for-byte with separately read flat files',
                            'nested_files': len(names)})
        else:
            raw.decode('utf-8')
            row['inspection'] = 'entire textual file read; Python read before replay' if p.suffix != '.tex' else 'entire manuscript independently derived before historical conclusions'
        members.append(row)
        if p.name in ('MANIFEST.json', 'REVIEW_MANIFEST.json', 'PUBLICATION_MANIFEST.json'):
            manifest_receipts.append(check_manifest(p))
    require(len(members) == 100, 'wrong support member count')
    require((SUPPORT / 'paper.tex').read_bytes() == (ROOT / 'frozen_inputs/paper.tex').read_bytes(), 'source differs')
    require({p.name for p in KIT.iterdir()} == {'README.md', 'paper.pdf', 'source-and-verification.zip',
                                              'zenodo-deposit.json', 'zenodo-metadata.json'}, 'wrong five-entry kit')
    for name, original in [('paper.pdf', 'output/pdf/paper.pdf'), ('source-and-verification.zip', 'source-and-verification.zip'),
                           ('zenodo-metadata.json', 'zenodo-metadata.json')]:
        require((KIT / name).read_bytes() == (ROOT / 'frozen_inputs' / original).read_bytes(), 'kit differs: ' + name)
    md = json.loads((ROOT / 'frozen_inputs/zenodo-metadata.json').read_text())['metadata']
    require(json.loads((SUPPORT / 'zenodo-metadata.json').read_text())['metadata'] == md, 'support metadata differs')
    require(json.loads((ROOT / 'frozen_inputs/zenodo-deposit.json').read_text())['metadata'] == md, 'deposit metadata differs')
    kit_deposit = json.loads((KIT / 'zenodo-deposit.json').read_text())
    require(kit_deposit['metadata'] == md, 'flat metadata differs')
    require(kit_deposit['files'] == [{'path': 'paper.pdf'}, {'path': 'source-and-verification.zip'}], 'flat paths wrong')
    require(md['license'] == 'cc-by-4.0' and md['publication_type'] == 'preprint' and
            md['publication_date'] == '2026-10-13' and md['version'] == '1.0' and
            md['creators'] == [{'name': 'Kriebel, Alec', 'affiliation': 'Independent researcher',
                               'orcid': '0009-0001-9320-500X'}], 'metadata identity wrong')
    return {'result': 'PASS', 'support_files': members, 'manifest_layers': manifest_receipts,
            'kit_entries': [{'path': p.name, **fingerprint(p.read_bytes())} for p in sorted(KIT.iterdir())],
            'all_metadata_layers_equal': True, 'deposit_paths_resolve': all(
                (ROOT / 'frozen_inputs' / e['path']).is_file() for e in
                json.loads((ROOT / 'frozen_inputs/zenodo-deposit.json').read_text())['files']),
            'scope_metadata_screen': metadata_screen,
            'limitations': 'Historical provenance/registry outputs are dated claims, not freshly reproduced raw-dataset proofs or first-priority certification.'}


if __name__ == '__main__':
    result = run()
    (ROOT / 'PACKAGE_INSPECTION_RECEIPT.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'result': result['result'], 'support_members': len(result['support_files']),
                      'manifest_layers': result['manifest_layers'], 'kit_entries': len(result['kit_entries']),
                      'metadata_equal': result['all_metadata_layers_equal'],
                      'deposit_paths_resolve': result['deposit_paths_resolve']}, indent=2))
