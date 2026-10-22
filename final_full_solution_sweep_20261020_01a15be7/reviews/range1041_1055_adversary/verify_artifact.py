#!/usr/bin/env python3
"""Read-only offline custody checks, not mathematical or provider certification.

Usage: python3 -I -B verify_artifact.py --root FOLDER [--with-private]
       [--expected-public-sha256 EXTERNALLY_RETAINED_SHA256]
No evidence code is imported or executed. No writes, subprocesses or networking.
"""
import argparse
import hashlib
import json
import re
import stat
import sys
from pathlib import Path, PurePosixPath

PUBLIC_NAMES = {'.gitignore','CHECK_RESULTS.json','REVIEW.md','RESEARCH_LOG.md','verify_artifact.py'}
MANIFEST = 'OUTPUT_MANIFEST.json'
SEAL = 'OUTPUT_MANIFEST.sha256'
PMANIFEST = 'PRIVATE_MANIFEST.json'
PSEAL = 'PRIVATE_MANIFEST.sha256'

def require(ok, reason):
    if not ok:
        raise ValueError(reason)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def exact_keys(value, keys, label):
    require(type(value) is dict and set(value) == set(keys), label+' keys')

def integer(value, expected=None):
    require(type(value) is int and value >= 0, 'nonnegative integer expected')
    if expected is not None:
        require(value == expected, 'integer value mismatch')

def hexdigest(value):
    require(type(value) is str and re.fullmatch('[0-9a-f]{64}', value) is not None, 'SHA-256 syntax')

def strict_json(data):
    def unique(pairs):
        obj={}
        for k,v in pairs:
            require(k not in obj, 'duplicate JSON key')
            obj[k]=v
        return obj
    def nonfinite(value):
        raise ValueError('nonfinite JSON constant')
    return json.loads(data.decode('utf-8'),object_pairs_hook=unique,parse_constant=nonfinite)

def path_name(value):
    require(type(value) is str and value != '' and '\\' not in value and '\x00' not in value, 'bad path')
    parts=PurePosixPath(value).parts
    require(not value.startswith('/') and all(p not in ('','.','..') for p in parts), 'unsafe path')
    require('/'.join(parts)==value, 'noncanonical path')
    return value

def read_regular(path):
    require(stat.S_ISREG(path.lstat().st_mode), 'not a regular file: '+str(path))
    return path.read_bytes()

def inventory(root, exclude_private=False):
    require(stat.S_ISDIR(root.lstat().st_mode), 'root must be real directory')
    found=set()
    def walk(folder):
        for p in folder.iterdir():
            rel=p.relative_to(root).as_posix()
            mode=p.lstat().st_mode
            require(not stat.S_ISLNK(mode), 'symlink forbidden: '+rel)
            if stat.S_ISDIR(mode):
                if exclude_private and rel=='private':
                    continue
                walk(p)
            elif stat.S_ISREG(mode):
                found.add(rel)
            else:
                raise ValueError('nonregular member: '+rel)
    walk(root)
    return found

def anchored_manifest(root, manifest_name, seal_name, external=None):
    data=read_regular(root/manifest_name)
    seal=read_regular(root/seal_name).decode('ascii')
    require(re.fullmatch('[0-9a-f]{64}\n',seal) is not None, 'seal syntax')
    require(sha(data)==seal.strip(), 'manifest seal mismatch')
    if external is not None:
        hexdigest(external)
        require(external==sha(data), 'external anchor mismatch')
    return strict_json(data),sha(data)

def entries(root, rows):
    require(type(rows) is list, 'manifest file list')
    names=set()
    folded=set()
    for row in rows:
        exact_keys(row, ('path','bytes','sha256'),'file entry')
        name=path_name(row['path'])
        require(name not in names and name.casefold() not in folded, 'duplicate manifest path')
        names.add(name);folded.add(name.casefold())
        integer(row['bytes']);hexdigest(row['sha256'])
        p=root
        for part in PurePosixPath(name).parts:
            p=p/part
            require(not stat.S_ISLNK(p.lstat().st_mode), 'symlink path')
        data=read_regular(p)
        require(len(data)==row['bytes'] and sha(data)==row['sha256'], 'file bytes mismatch: '+name)
    return names

def validate_results(results):
    require(type(results) is dict, 'results object')
    integer(results['schema_version'],1)
    scope=results['scope']
    for key,value in [('first_pr',1041),('last_pr',1055),('pr_count',15)]:
        integer(scope[key],value)
    require(scope['new_proof_or_priority_audit'] is False and scope['global_completion_claim'] is False, 'scope overclaim')
    require(results['outcome']=='no_actionable_defect_found' and results['actionable_findings']==[], 'bounded verdict mismatch')
    expected={'published_covered':3,'partial_unsolved':7,'credited_prior_application':4,'scoped_prior_proof_audit':1,'all_missing_own_queue_edit':15,'actual_changed_nonnull_blobs':132,'fresh_live_pr_reads':15,'exact_once_journal_dispositions':15,'new_publications':0,'provider_writes':0,'spreadsheet_writes':0}
    exact_keys(results['counts'],expected,'counts')
    for key,value in expected.items():
        integer(results['counts'][key],value)
    cases=results['cases'];require(type(cases) is list and len(cases)==15, 'case count')
    require([x['pr'] for x in cases]==list(range(1041,1056)), 'case order or identities')
    for case in cases:
        integer(case['pr']);integer(case['paths'])
        for key in ['head','base']:
            require(type(case[key]) is str and re.fullmatch('[0-9a-f]{40}',case[key]) is not None, 'null/invalid object identity')
        hexdigest(case['body_sha256'])
        require(case['no_QUEUE_edit'] is True and case['journal_exactly_once'] is True, 'scope binding flags')
    require(sum(x['paths'] for x in cases)==132, 'path count')
    require(results['capture']['remote_checkpoint']=='1d755db267c68355d728c47e9a86d0d2fdefd500', 'checkpoint identity')
    expected_pubs=[(1041,23430642,139,538,536,11),(1047,23430660,140,204,203,9),(1052,23430681,141,163,162,8)]
    pubs=results['publications'];require(type(pubs) is list and len(pubs)==3, 'publication count')
    for pub,expect in zip(pubs,expected_pubs):
        for key,value in zip(('pr','record','ledger_row','archive_members','manifest_payloads','original_files'),expect):
            integer(pub[key],value)
        require(pub['doi']=='10.5281/zenodo.'+str(pub['record']), 'DOI identity')
        for key in ('pdf_sha256','archive_sha256'):
            hexdigest(pub[key])
        for key in ('pdf_bytes','archive_bytes'):
            integer(pub[key])
        for key in ('all_ledger_keys_unique','all_original_pinned_head_bytes_equal','provider_published_and_doi_resolved','archive_integrity_and_member_manifest_closed','type_license_equal'):
            require(pub[key] is True, 'publication check flag')
        require(pub['separate_pdf_intentional'] is (pub['pr']==1047), 'separate PDF scope')
    runs=results['reproductions'];require([x['pr'] for x in runs]==[1041,1047,1052], 'replay list')
    for run in runs:
        require(run['status']=='PASS' and run['original_theoretical_executable_replay'] is False and run['universal_proof_role']=='finite corroboration only', 'replay overclaim')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parent)
    parser.add_argument('--with-private',action='store_true')
    parser.add_argument('--expected-public-sha256')
    args=parser.parse_args()
    root=args.root.absolute()
    public,digest=anchored_manifest(root,MANIFEST,SEAL,args.expected_public_sha256)
    exact_keys(public,('schema_version','files','private_manifest_sha256','private_payload_files','scope'),'public manifest')
    integer(public['schema_version'],1);hexdigest(public['private_manifest_sha256']);integer(public['private_payload_files'])
    require(public['scope']=='PR1041–1055 bounded review custody only', 'manifest scope')
    names=entries(root,public['files'])
    require(names==PUBLIC_NAMES, 'public payload member set')
    require(inventory(root,exclude_private=True)==names|{MANIFEST,SEAL}, 'public closed inventory')
    require(read_regular(root/'.gitignore')==b'private/\n', 'private ignore convention')
    validate_results(strict_json(read_regular(root/'CHECK_RESULTS.json')))
    if args.with_private:
        private_root=root/'private'
        private,pdigest=anchored_manifest(private_root,PMANIFEST,PSEAL,public['private_manifest_sha256'])
        exact_keys(private,('schema_version','files'),'private manifest')
        integer(private['schema_version'],1)
        pnames=entries(private_root,private['files'])
        integer(public['private_payload_files'],len(pnames))
        require(PMANIFEST not in pnames and PSEAL not in pnames, 'noncircular private inventory')
        require(inventory(private_root)==pnames|{PMANIFEST,PSEAL}, 'private closed inventory')
    print(json.dumps({'status':'PASS','public_manifest_sha256':digest,'public_payload_files':len(names),'private_checked':args.with_private,'scope':'offline custody only; no theorem/priority/provider recertification'},sort_keys=True))

if __name__=='__main__':
    try:
        main()
    except Exception as exc:
        print(json.dumps({'status':'FAIL','error':str(exc)},sort_keys=True),file=sys.stderr)
        sys.exit(1)
