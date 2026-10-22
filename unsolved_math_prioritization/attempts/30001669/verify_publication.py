#!/usr/bin/env python3
"""Strict externally pinned publication replay, not a theorem proof checker."""
import argparse
import hashlib
import json
import stat
import subprocess
import sys
import zipfile
from pathlib import Path, PurePosixPath

ARCHIVES = {
 'author': ('DOMINATING_DIGRAPH_30001669_AUTHOR_SAFE_FREEZE.zip', 10114,
  '15bb36b2d492b2ace008a6b851b31a3893ec0a559ccc3853a2d709f58f3ed96f',
  'd1d79514b2851823f47345677bfa66f53152f1922562b1040f7dd8882028c620'),
 'audit': ('DOMINATING_DIGRAPH_30001669_INDEPENDENT_AUDIT_SAFE.zip', 24877,
  '637a9051786e69d9d2d12591d9e99fe76044076082ba1777c57e652430c3779b',
  'cc8b4329029939eabb9f2c91e4a33e5c1345911e9e5e0417904f364c809352b1')}
MANIFEST = 'PUBLICATION_MANIFEST.json'

def need(ok, text):
    if not ok:
        raise ValueError(text)

def sha(b): return hashlib.sha256(b).hexdigest()

def unique(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, 'duplicate JSON key')
        result[key] = value
    return result

def parse(raw): return json.loads(raw, object_pairs_hook=unique)

def regular(p):
    s = p.lstat()
    need(stat.S_ISREG(s.st_mode) and s.st_nlink == 1, 'nonregular or aliased file: ' + str(p))

def bind(root, pin):
    need(stat.S_ISDIR(root.lstat().st_mode), 'root must be a real directory')
    regular(root / MANIFEST)
    raw = (root / MANIFEST).read_bytes()
    need(sha(raw) == pin, 'external manifest pin mismatch')
    manifest = parse(raw)
    need(set(manifest) == {'schema', 'files'} and manifest['schema'] == 'dominating-digraph-strict-publication-v1', 'manifest schema')
    files = manifest['files']
    need(type(files) is dict and bool(files), 'manifest files')
    for name in files:
        p = PurePosixPath(name)
        need(name == str(p) and not p.is_absolute() and '..' not in p.parts and '\\' not in name and name not in ('', '.', MANIFEST), 'unsafe manifest path')
    expected_dirs = {str(p) for n in files for p in PurePosixPath(n).parents if str(p) != '.'}
    actual_files, actual_dirs = set(), set()
    for p in root.rglob('*'):
        name = p.relative_to(root).as_posix()
        s = p.lstat()
        if stat.S_ISREG(s.st_mode):
            regular(p)
            actual_files.add(name)
        elif stat.S_ISDIR(s.st_mode):
            actual_dirs.add(name)
        else:
            raise ValueError('nonregular entry: ' + name)
    need(actual_files == set(files) | {MANIFEST}, 'strict file inventory')
    need(actual_dirs == expected_dirs, 'strict directory inventory')
    for name, rec in files.items():
        b = (root / name).read_bytes()
        need(type(rec.get('bytes')) is int and rec == {'bytes': len(b), 'sha256': sha(b)}, 'payload pin: ' + name)
    metadata = parse((root / 'PUBLICATION_METADATA.json').read_bytes())
    need(metadata['schema'] == 'dominating-digraph-publication-v1', 'metadata schema')
    need(metadata['problem_id'] == 30001669 and metadata['problem_number'] == 'OWR-4791-028' and metadata['rank'] == 832, 'identity')
    need(metadata['classification'] == 'already_solved' and metadata['answer'] == 'negative' and metadata['turns'] == '1/5' and type(metadata['approaches_used']) is int and metadata['approaches_used'] == 1, 'disposition/count')
    for flag in ['novel_resolution_claim', 'computed_adjacency_certificate_claim', 'human_peer_review_of_this_packet_claim', 'formal_proof_claim']:
        need(metadata[flag] is False, 'invalid scope: ' + flag)
    need(metadata['prior_result_year'] == 2015 and metadata['source_theorem'] == 11 and metadata['source_publication_status'] == 'Published conference proceedings', 'prior citation')
    need(metadata['credit'] == 'Yogesh Anbalagan, Hao Huang, Shachar Lovett, Sergey Norin, Adrian Vetta, and Hehui Wu', 'credit')
    need(metadata['source_url'] == 'https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.APPROX-RANDOM.2015.78', 'source URL')
    need(metadata['specialization'] == {'k':101,'l':100,'base_girth':9901,'positive_walk_lengths':[1,99],'maximum_lifted_closed_walk_length':9900,'subset_sizes':'0 through 100 inclusive','witness_orientation':'witness to every target'}, 'specialization')
    need(metadata['mathematical_corrections_required'] == [], 'mathematical correction scope')
    q = metadata['queue_edit']
    need(q['changed_cells'] == ['Status','Turns','Findings'] and q['other_bytes_preserved'] is True, 'queue scope')
    need(len(metadata['archives']) == 2, 'archive count')
    for record in metadata['archives']:
        role = record['role']
        need(role in ARCHIVES, 'archive role')
        filename, size, digest, mpin = ARCHIVES[role]
        need(record == {'role':role,'path':'archives/'+filename,'bytes':size,'sha256':digest,'manifest_sha256':mpin,'unchanged':True}, 'archive metadata')
        b = (root / 'archives' / filename).read_bytes()
        need(len(b) == size and sha(b) == digest, 'immutable archive pin')
        directory = root / role
        need(sha((directory/'MANIFEST.json').read_bytes()) == mpin, 'inner manifest pin')
        with zipfile.ZipFile(root/'archives'/filename) as z:
            members = z.infolist()
            need(len(members) == len({i.filename for i in members}), 'duplicate ZIP members')
            need({i.filename for i in members} == {p.name for p in directory.iterdir()}, 'ZIP inventory')
            for i in members:
                need(i.filename == PurePosixPath(i.filename).name and not i.is_dir() and stat.S_ISREG(i.external_attr >> 16), 'unsafe ZIP member')
                need(z.read(i) == (directory/i.filename).read_bytes(), 'ZIP member bytes')
    need({a['role'] for a in metadata['archives']} == set(ARCHIVES), 'archive roles')
    need((root/'audit/AUTHOR_SAFE_FREEZE.zip').read_bytes() == (root/'archives'/ARCHIVES['author'][0]).read_bytes(), 'nested author archive')
    accepted = parse((root/'audit/ACCEPTANCE.json').read_bytes())
    need(accepted['accepted'] is True and accepted['classification'] == 'already_solved' and accepted['answer'] == 'negative' and accepted['mathematical_objections'] == [], 'acceptance')
    return {'status':'pass','files':len(files)+1,'archive_member_equivalence':True,'historical_freezes_unchanged':True}

def full(root):
    flags = ['-I','-B'] + (['-O'] if sys.flags.optimize else [])
    def run(path, args=()):
        p = subprocess.run([sys.executable,*flags,str(root/path),*args],capture_output=True,text=True,cwd='/tmp',timeout=180)
        need(p.returncode == 0 and not p.stderr, path + ': ' + p.stderr)
        return p.stdout.encode()
    apin, ipin = ARCHIVES['author'][3], ARCHIVES['audit'][3]
    av = parse(run('author/verify.py',['--manifest-sha256',apin]))
    iv = parse(run('audit/verify_audit.py',['--manifest-sha256',ipin]))
    ah = run('author/audit_checks.py',['--manifest-sha256',apin])
    ih = run('audit/independent_checks.py')
    need(ah == (root/'author/VERIFICATION.json').read_bytes(), 'author recorded output')
    need(ih == (root/'audit/AUDIT_VERIFICATION.json').read_bytes(), 'independent recorded output')
    a, i = parse(ah), parse(ih)
    need(av['status'] == iv['status'] == i['status'] == 'pass', 'replay status')
    return {'author_verifier':av,'audit_verifier':iv,'author_recorded_output_matches':True,'independent_recorded_output_matches':True,'author_integrity_controls':len(a['integrity_controls']),'author_semantic_controls':len(a['semantic_controls']),'independent_integrity_controls':len(i['integrity_controls']),'independent_semantic_controls':len(i['semantic_controls']),'graph_and_arithmetic_controls':i['graph_and_arithmetic_controls'],'formal_theorem_proof':False,'source_documents_reauthenticated':False}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest-sha256',required=True)
    parser.add_argument('--root',type=Path,default=Path(__file__).absolute().parent)
    parser.add_argument('--full',action='store_true')
    args = parser.parse_args()
    root = args.root.absolute()
    result = bind(root,args.manifest_sha256)
    if args.full:
        result['replay'] = full(root)
        bind(root,args.manifest_sha256)
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__ == '__main__': main()
