#!/usr/bin/env python3
"""Offline read-only custody verification; no evidence execution or network."""
import argparse
import hashlib
import json
import re
import stat
import sys
from pathlib import Path, PurePosixPath

PUBLIC = {'.gitignore', 'CHECK_RESULTS.json', 'RESEARCH_LOG.md', 'REVIEW.md',
          'verify_artifact.py'}
HEX = re.compile(r'[0-9a-f]{64}')
COMMIT = 'd567ec8640e4115286db34a19d6c806bd37fb6a5'

def require(ok, message):
    if not ok:
        raise ValueError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def strict(data):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, 'duplicate JSON key')
            result[key] = value
        return result
    def invalid(value):
        raise ValueError('nonfinite JSON')
    return json.loads(data.decode('utf-8'), object_pairs_hook=unique,
                      parse_constant=invalid)

def read(path):
    require(stat.S_ISREG(path.lstat().st_mode), 'not a regular file: '+str(path))
    return path.read_bytes()

def safe(value):
    require(type(value) is str and value and '\\' not in value and '\x00' not in value,
            'bad relative path')
    p = PurePosixPath(value)
    require(not p.is_absolute() and p.as_posix() == value and
            all(x not in ('', '.', '..') for x in p.parts), 'unsafe path')
    return p

def inventory(root, skip_private=False):
    require(stat.S_ISDIR(root.lstat().st_mode), 'not a real directory')
    found = set()
    def walk(folder):
        for path in folder.iterdir():
            name = path.relative_to(root).as_posix()
            mode = path.lstat().st_mode
            require(not stat.S_ISLNK(mode), 'symlink in inventory')
            if stat.S_ISDIR(mode):
                if not (skip_private and name == 'private'):
                    walk(path)
            else:
                require(stat.S_ISREG(mode), 'nonregular inventory item')
                found.add(name)
    walk(root)
    return found

def entries(root, rows):
    require(type(rows) is list, 'files must be an array')
    names, folded = set(), set()
    for row in rows:
        require(type(row) is dict and set(row) == {'path', 'bytes', 'sha256'},
                'file entry keys')
        name = row['path']
        parts = safe(name).parts
        require(name not in names and name.casefold() not in folded, 'path alias')
        names.add(name)
        folded.add(name.casefold())
        require(type(row['bytes']) is int and row['bytes'] >= 0, 'bad byte count')
        require(type(row['sha256']) is str and HEX.fullmatch(row['sha256']),
                'bad digest syntax')
        path = root
        for component in parts:
            path /= component
            require(not stat.S_ISLNK(path.lstat().st_mode), 'symlink ancestor')
        data = read(path)
        require(len(data) == row['bytes'] and sha(data) == row['sha256'],
                'payload differs: '+name)
    return names

def manifest(root, name, expected=None):
    data = read(root/(name+'.json'))
    require(read(root/(name+'.sha256')) == (sha(data)+'\n').encode('ascii'),
            'manifest sidecar mismatch')
    if expected is not None:
        require(type(expected) is str and HEX.fullmatch(expected) and expected == sha(data),
                'external anchor mismatch')
    return strict(data), sha(data)

def semantic(result):
    require(type(result) is dict and type(result['schema_version']) is int and
            result['schema_version'] == 1, 'result schema')
    require(result['outcome'] == 'no_actionable_findings' and
            result['substantive_findings'] == [], 'verdict')
    require(result['immutable_remote_checkpoint'] == COMMIT, 'checkpoint')
    require(result['scope'] == {'first_pr':1071, 'last_pr':1080, 'pr_count':10,
            'new_proof_priority_or_global_acceptance':False}, 'bounded scope')
    require(result['scope']['new_proof_priority_or_global_acceptance'] is False and
            all(type(result['scope'][key]) is int for key in
                ('first_pr','last_pr','pr_count')), 'scope value types')
    expected = {'cases':10, 'missing_QUEUE_cases':10,
        'actual_nonnull_changed_blobs':63, 'partial_unsolved':7,
        'credited_prior_applications':1, 'existing_publications':2,
        'new_publications_by_reviewer':0, 'provider_writes_by_reviewer':0,
        'sheet_writes_by_reviewer':0}
    require(set(result['counts']) == set(expected), 'count keys')
    for key, value in expected.items():
        require(type(result['counts'][key]) is int and result['counts'][key] == value,
                'count differs: '+key)
    cases = result['cases']
    require([x['pr'] for x in cases] == list(range(1071,1081)) and
            [x['paths'] for x in cases] == [9,5,6,6,6,6,6,6,7,6], 'case sequence')
    for row in cases:
        require(row['no_QUEUE_edit'] is True and row['journal_exactly_once'] is True
                and row['live_head_base_body_equal'] is True, 'case binding')
        for key in ('head','base'):
            require(type(row[key]) is str and re.fullmatch('[0-9a-f]{40}',row[key])
                    and row[key] != '0'*40, 'null or malformed Git identity')
        require(type(row['body_sha256']) is str and HEX.fullmatch(row['body_sha256']),
                'body digest')
    pubs = result['publications']
    require([x['pr'] for x in pubs] == [1071,1080], 'publication sequence')
    for row, pr, doi, ledger, members, payloads, originals in zip(pubs,
            [1071,1080], ['10.5281/zenodo.23430906','10.5281/zenodo.23430927'],
            [143,144], [225,299], [224,298], [9,6]):
        require(row['pr'] == pr and row['doi'] == doi and row['ledger_row'] == ledger
                and row['archive_members'] == members and row['manifest_payloads'] == payloads
                and row['exact_actual_head_originals'] == originals
                and row['unique_exact_row'] is True and row['published_and_DOI_HTTP200'] is True
                and row['safe_unique_CRC_closed_manifest'] is True
                and row['all_authored_provider_metadata_fields_equal'] is True,
                'publication coverage')
    controls = result['new_finite_controls']
    require(controls == {'exact_pairing':'4/45045','exact_Gram_controls':49,
        'metric_transfer_cases':31,'SL2_insertion_cases':55987,'proper_insertions':54894,
        'normal_O_OO_stdout_equal':True,'archived_programs_executed':0,
        'universal_proof_or_priority_certificate':False}, 'finite control scope')
    require(controls['normal_O_OO_stdout_equal'] is True and
            controls['universal_proof_or_priority_certificate'] is False and
            type(controls['archived_programs_executed']) is int,
            'finite control value types')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--with-private', action='store_true')
    parser.add_argument('--expected-public-sha256')
    args = parser.parse_args()
    root = args.root.absolute()
    for path in [root, *root.parents]:
        require(not stat.S_ISLNK(path.lstat().st_mode), 'root symlink ancestor')
    m, digest = manifest(root, 'OUTPUT_MANIFEST', args.expected_public_sha256)
    require(type(m) is dict and set(m) == {'schema_version','scope','files',
            'private_manifest_sha256'}, 'public manifest keys')
    require(type(m['schema_version']) is int and m['schema_version'] == 1 and
            m['scope'] == 'PR1071–1080 bounded review custody only', 'manifest scope')
    require(type(m['private_manifest_sha256']) is str and
            HEX.fullmatch(m['private_manifest_sha256']), 'private anchor')
    names = entries(root, m['files'])
    require(names == PUBLIC and inventory(root,True) ==
            PUBLIC|{'OUTPUT_MANIFEST.json','OUTPUT_MANIFEST.sha256'}, 'public closure')
    require(read(root/'.gitignore') == b'private/\n', 'private ignore boundary')
    result = strict(read(root/'CHECK_RESULTS.json'))
    semantic(result)
    private_count = None
    if args.with_private:
        private = root/'private'
        pm, pd = manifest(private,'PRIVATE_MANIFEST',m['private_manifest_sha256'])
        require(type(pm) is dict and set(pm) == {'schema_version','files'} and
                type(pm['schema_version']) is int and pm['schema_version'] == 1,
                'private manifest schema')
        pn = entries(private,pm['files'])
        require(inventory(private) == pn|{'PRIVATE_MANIFEST.json','PRIVATE_MANIFEST.sha256'},
                'private closure')
        ids = strict(read(private/'IDENTITY_CHECKS.json'))
        require(ids['checkpoint'] == COMMIT, 'private checkpoint')
        require([{k:c[k] for k in ('pr','head','base','paths','no_QUEUE_edit',
                'journal_exactly_once','body_sha256')} for c in ids['cases']] ==
                [{k:c[k] for k in ('pr','head','base','paths','no_QUEUE_edit',
                'journal_exactly_once','body_sha256')} for c in result['cases']],
                'private/public case binding')
        private_count = len(pn)
    print(json.dumps({'status':'PASS','public_payloads':len(names),
        'private_payloads':private_count,
        'scope':'Offline byte custody only; no mathematical, priority, provider or global completion certification'},sort_keys=True))

if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print(json.dumps({'status':'FAIL','error':str(error)},sort_keys=True),file=sys.stderr)
        sys.exit(1)
