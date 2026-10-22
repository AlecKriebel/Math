#!/usr/bin/env python3
"""Read-only exact verification of authorized local provenance inputs.

Outputs hashes, byte counts, match results and public identifiers only.
It never copies source text, dataset rows, raw API payloads or local paths.
All command-line paths refer to inputs supplied separately, not package files.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import io
import json
from pathlib import Path
import stat
import zipfile

AUTHOR_ZIP_SHA = 'a945c97336f27b6cb4fc750e5eb7aa4819e3e459778422dd0a427cc78ac318b5'
AUTHOR_MANIFEST_SHA = 'b7cec3611fed2152a42b7e7b4c2daa7ca18d899b3f03603898df838ab9819fd6'
STATEMENT_SHA = '88d8794a2ce6506bc4b7e9d46e4717abd124f444c4d8519f8108a56f7a974082'
REVIEW_SHA = 'dbcdeb82111990e3cd26ef9a6fc2ccab7a1986e832bcc3eb042149c5608b3d1e'
FILES = {'PROOF.md','README.md','RESEARCH_LOG.md','SOURCE_VERIFICATION.json',
         'STATUS.json','readiness.json','verification_results.json',
         'verify.py','verify_manifest.py','AUTHOR_MANIFEST.json'}
PDF_NAMES = ['owr2021.pdf','liggett_steif.pdf','rath_valesin.pdf',
             'fernley_jacob.pdf','vandenberg.pdf','mixing2026.pdf']


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git_blob(data):
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()


def info(data):
    return {'bytes':len(data),'sha256':sha(data)}


def require(condition,label):
    if not condition:
        raise AssertionError(label)


def rebuild_tree(tree, recursive=True):
    require(tree['truncated'] is False,'untruncated tree')
    children = defaultdict(list)
    for entry in tree['tree']:
        parent,_,base = entry['path'].rpartition('/')
        children[parent].append((base,entry))
    computed = {}
    for parent in sorted(children,key=lambda s:s.count('/')+(bool(s)),reverse=True):
        rows = sorted(children[parent],key=lambda pair:pair[0]+('/' if pair[1]['type']=='tree' else ''))
        data = b''
        for base,entry in rows:
            if entry['type'] == 'tree' and recursive:
                require(computed[entry['path']] == entry['sha'],'child Git tree hash')
            data += str(int(entry['mode'])).encode()+b' '+base.encode()+b'\0'+bytes.fromhex(entry['sha'])
        computed[parent] = hashlib.sha1(b'tree '+str(len(data)).encode()+b'\0'+data).hexdigest()
    require(computed[''] == tree['sha'],'root Git tree hash')
    return len(computed)


def main():
    p = argparse.ArgumentParser()
    for arg in ('author-root','corpus-dir','catalog','remote-evidence','output'):
        p.add_argument('--'+arg,type=Path,required=True)
    args = p.parse_args()
    author = args.author_root/'deliverable'
    private = args.author_root/'private_sources'
    remote = args.remote_evidence
    raw = (args.author_root/'contact_process_30004594_authored.zip').read_bytes()
    require((len(raw),sha(raw)) == (24142,AUTHOR_ZIP_SHA),'author ZIP')
    require(sha((author/'AUTHOR_MANIFEST.json').read_bytes()) == AUTHOR_MANIFEST_SHA,'manifest anchor')
    require({x.name for x in author.iterdir()} == FILES,'strict frozen-directory allowlist')
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        members = z.infolist()
        require(len(members) == len(FILES),'ZIP number of entries')
        require({x.filename for x in members} == FILES,'ZIP allowlist and unique names')
        require(z.testzip() is None,'ZIP CRC')
        for member in members:
            require(not member.is_dir() and not stat.S_ISLNK(member.external_attr >> 16),'regular ZIP file')
            require(not member.flag_bits & 1,'unencrypted ZIP')
            require(z.read(member) == (author/member.filename).read_bytes(),'ZIP directory match')
    manifest = json.loads((author/'AUTHOR_MANIFEST.json').read_bytes())
    require({r['path'] for r in manifest['files']} == FILES-{'AUTHOR_MANIFEST.json'},'manifest coverage')
    for row in manifest['files']:
        require(info((author/row['path']).read_bytes()) == {k:row[k] for k in ('bytes','sha256')},'author file integrity')
    source = json.loads((author/'SOURCE_VERIFICATION.json').read_bytes())
    repo_manifest_bytes = (remote/'manifest_remote.json').read_bytes()
    repo_manifest = json.loads(repo_manifest_bytes)
    require(repo_manifest['revision'] == source['dataset']['revision'],'dataset revision')
    datasets = {}
    loaded = {}
    for name in ('problems.json','research_results.json'):
        data = (args.corpus_dir/name).read_bytes()
        require(info(data) == repo_manifest['files'][name],'complete corpus hash')
        datasets[name] = {**info(data),'matches_live_pinned_repository_manifest':True}
        loaded[name] = json.loads(data)
    problems = loaded['problems.json']
    reports = loaded['research_results.json']
    rows = [x for x in problems if str(x['id']) == '30004594']
    require(len(rows) == 1,'unique numeric problem')
    selected = rows[0]
    require(selected['problem_number'] == 'OWR-4990373-008','source problem code')
    require(Counter(x['problem_number'] for x in problems)[selected['problem_number']] == 1,'unique problem number')
    require(selected['problem_number'] not in reports,'absent prior report key')
    require(sha(selected['statement'].encode()) == STATEMENT_SHA,'statement binding')
    # The repository importer defaults an absent report key to {}, not null.
    # Use exactly json.dumps(...,sort_keys=True), including its default separators
    # and ensure_ascii=True, as the independently retrieved queue.py does.
    review_hash = sha(json.dumps([selected,{}],sort_keys=True).encode())
    require(review_hash == REVIEW_SHA,'descriptor review hash')
    queue_code = (remote/'queue_remote.py').read_bytes()
    require(b"reports.get(p['problem_number'],{})" in queue_code,'importer missing-report convention')
    require(b'review_hash=digest(json.dumps([p,r],sort_keys=True))' in queue_code,'review digest serialization')
    catalog_bytes = args.catalog.read_bytes()
    descriptors = [x for x in json.loads(catalog_bytes) if str(x['id']) == '30004594']
    require(len(descriptors) == 1,'catalog unique descriptor')
    descriptor = descriptors[0]
    require(descriptor['review_hash'] == REVIEW_SHA and descriptor['statement_hash'] == STATEMENT_SHA,'catalog hash fields')
    require(descriptor['rank'] == 780,'catalog rank')
    tree_bytes = (private/'repo_priority_tree.json').read_bytes()
    tree = json.loads(tree_bytes)
    verified_nodes = rebuild_tree(tree)
    entries = {x['path']:x for x in tree['tree']}
    for filename,data in [('catalog.json',catalog_bytes),('queue.py',queue_code),('manifest.json',repo_manifest_bytes)]:
        require(git_blob(data) == entries[filename]['sha'],'pinned repository blob binding')
    root = json.loads((remote/'root_remote.json').read_bytes())
    require(next(x for x in root['tree'] if x['path']=='unsolved_math_prioritization')['sha'] == tree['sha'],'live pinned parent tree binding')
    commit = json.loads((remote/'commit_remote.json').read_bytes())
    require(commit['sha'] == '24ae23df9ad6c9def619cdbdf2ec8066f506788f','pinned commit response')
    # A tree endpoint addressed by commit may echo that commit in its sha field.
    # Bind the entries to the actual tree ID in the independently read commit.
    root['sha'] = commit['tree']['sha']
    rebuild_tree(root,recursive=False)
    match_paths = [x for x in entries if any(token in x.lower() for token in ('30004594','4990373','contact'))]
    require(not match_paths,'no selected attempt path at observed pinned tree')
    fresh_searches = {}
    for kind in ('prs','commits'):
        data = json.loads((remote/f'prior_{kind}_remote.json').read_bytes())
        require(not data['incomplete_results'],'complete returned search status')
        require(data['total_count'] == 0 and not data['items'],'no exact numeric hit')
        fresh_searches[kind] = {'total_count':0,'incomplete_results':False}
    pdfs = []
    for name,row in zip(PDF_NAMES,source['sources']):
        data = (private/name).read_bytes()
        require(info(data) == row['pdf'],'whole scholarly PDF hash')
        pdfs.append({'title':row['title'],'url':row['url'],**info(data),'matches_author_metadata':True})
    status = json.loads((author/'STATUS.json').read_bytes())
    require(status['original_problem_solved'] is False and status['substantive_approaches_used']==5,'unresolved five-approach scope')
    result = {
        'status':'PASS_INDEPENDENT_PROVENANCE_BINDING',
        'problem_id':30004594,'problem_code':'OWR-4990373-008','rank':780,
        'author_zip':{**info(raw),'strict_member_allowlist':True,'members':len(FILES)},
        'author_manifest_sha256':AUTHOR_MANIFEST_SHA,
        'all_frozen_author_files_unchanged':True,
        'datasets':datasets,'dataset_revision':repo_manifest['revision'],
        'problem_records':len(problems),'research_report_entries':len(reports),
        'selected_numeric_matches':1,'selected_problem_number_matches':1,
        'selected_report_key_present':False,'importer_absent_report_value':'empty object',
        'statement_sha256':STATEMENT_SHA,'recalculated_review_hash':review_hash,
        'review_hash_recalculated_from_complete_corpora':True,
        'catalog':{**info(catalog_bytes),'git_blob_sha1':git_blob(catalog_bytes)},
        'repository_commit':'24ae23df9ad6c9def619cdbdf2ec8066f506788f',
        'root_tree_sha1_rebuilt':root['sha'],
        'priority_tree_sha1':tree['sha'],'priority_tree_entries':len(tree['tree']),
        'priority_tree_hash_nodes_rebuilt':verified_nodes,'priority_tree_truncated':False,
        'selected_attempt_path_matches':[], 'fresh_exact_numeric_searches':fresh_searches,
        'queue_implementation':{**info(queue_code),'git_blob_sha1':git_blob(queue_code),
            'url':'https://github.com/AlecKriebel/Math/blob/24ae23df9ad6c9def619cdbdf2ec8066f506788f/unsolved_math_prioritization/queue.py'},
        'source_pdfs':pdfs,
        'limits':'Hash and tree validation establish binding and declared search scope, not exhaustive literature status or absence of unpublished/deleted/unindexed work. No source or dataset content is copied into this output.'}
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print('PASS: author freeze, complete datasets, descriptor review hash, Git trees and six source PDFs')


if __name__ == '__main__':
    main()
