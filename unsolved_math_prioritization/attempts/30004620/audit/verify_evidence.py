#!/usr/bin/env python3
"""Verify supplied evidence without redistributing source records or PDF contents."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile

PIN = {
    'archive':(17582,'43caecab347e51a96dfbed59f9f61cfc354aa89121c3f6be8aea0916e205274b'),
    'catalog':(21735099,'891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566'),
    'problems':(68931837,'04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf'),
    'research':(80334822,'8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b'),
    'gh_pdf':(352055,'7128cbf5c8c2f3ab5729d8903e42e9a10b73e8b1c214b2157525d08cfba62fb5'),
    'vdg_pdf':(167177,'741d7857f5222c072a63805b33fa685380c4cec4143e9028bedb1487df57d942'),
    'owr_pdf':(578392,'76a52fd7f9e2dd19f7c317de8480c6576d027d3ba739baa705ae3a99b5c4586e'),
}
STATEMENT = '66d79ee91479b1e8c8ca329adeaca6e27a8a54ea1cafd98a6a35f905b578cff9'
REVIEW = 'b3f0019b864f0700a2943a882d9f11eef9e98dcee2299462ab55eabab2486fe9'
MANIFEST = '6dbce0c54fee5c33b7cca0e2209959287afe38b3780f6dcb28eb43c48d934073'

def digest(b):
    return hashlib.sha256(b).hexdigest()

def require(v,message):
    if not v:
        raise AssertionError(message)

parser = argparse.ArgumentParser(description=__doc__)
for key in PIN:
    parser.add_argument('--'+key.replace('_','-'),type=Path,required=True)
parser.add_argument('--queue-code',type=Path,help='Optional retrieved queue.py; serialization and Git blob identity are checked.')
args = parser.parse_args()
metadata, data = {}, {}
for key, expected in PIN.items():
    b = getattr(args,key).read_bytes()
    require((len(b),digest(b))==expected,key+' input pin')
    metadata[key] = {'bytes':len(b),'sha256':digest(b),'matches_expected':True,'redistributed':False}
    if key.endswith('_pdf'):
        require(b.startswith(b'%PDF-'),key+' valid PDF header')
        metadata[key]['valid_pdf_header'] = True
    elif key!='archive':
        data[key] = json.loads(b)

catalog = [x for x in data['catalog'] if str(x.get('id'))=='30004620']
problems = [x for x in data['problems'] if str(x.get('id'))=='30004620']
require(len(catalog)==len(problems)==1,'unique exact problem identity')
c,p = catalog[0],problems[0]
require(c['rank']==782 and c['problem_number']==p['problem_number']=='OWR-4990375-013','descriptor identity')
require(digest(p['statement'].encode())==c['statement_hash']==STATEMENT,'statement hash')
research = data['research']
prior = research.get(p['problem_number'],{})
require(prior=={},'no exact-key prior report')
require(digest(json.dumps([p,prior],sort_keys=True).encode())==c['review_hash']==REVIEW,'review hash independently recomputed')

terms = ['30004620','OWR-4990375-013','Effective Surface Cone of Principally Polarized Abelian Threefolds','2007.02995']
matches = {}
for term in terms:
    ids = [k for k,v in research.items() if term.casefold() in (k+' '+json.dumps(v)).casefold()]
    require(not ids,'no matching prior report: '+term)
    matches[term] = len(ids)

queue_check = {'checked':False}
if args.queue_code:
    b = args.queue_code.read_bytes()
    git_sha = hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
    require(git_sha=='e646cfc1a3b9653879777e4e1215e9a1043f3a3d','queue code Git blob')
    require(b'review_hash=digest(json.dumps([p,r],sort_keys=True))' in b,'queue review serialization')
    queue_check = {'checked':True,'git_blob_sha':git_sha,'serialization_matches':True,'redistributed':False}

with zipfile.ZipFile(args.archive) as archive:
    names = archive.namelist()
    expected = {'APPROACHES.json','AUTHOR_MANIFEST.json','README.md','RESULT.md','SOURCES.md','provenance.json','results.json','verify.py'}
    require(set(names)==expected and len(names)==8,'safe archive exact allowlist')
    require(digest(archive.read('AUTHOR_MANIFEST.json'))==MANIFEST,'author manifest pin')
    manifest = json.loads(archive.read('AUTHOR_MANIFEST.json'))
    require(len(manifest['payload_files'])==7,'manifest payload count')
    for item in manifest['payload_files']:
        b = archive.read(item['path'])
        require(len(b)==item['bytes'] and digest(b)==item['sha256'],'manifest '+item['path'])
    with tempfile.TemporaryDirectory(prefix='abelian-audit-replay-') as temp:
        directory = Path(temp)
        for name in names:
            (directory/name).write_bytes(archive.read(name))
        run = subprocess.run([sys.executable,'-B','verify.py'],cwd=directory,capture_output=True,check=True)
        require(run.stdout==archive.read('results.json'),'isolated author replay byte equality')
        result = json.loads(run.stdout)
        require(result['status']=='PASS' and result['assertions']==8800,'author 8800 controls')
        optimized = subprocess.run([sys.executable,'-O','-B','verify.py'],cwd=directory,capture_output=True)
        require(optimized.returncode!=0,'optimized invocation rejected')

result = {
    'status':'PASS','problem_id':30004620,'rank':782,
    'input_metadata':metadata,
    'descriptor':{'unique_match':True,'statement_sha256':STATEMENT,'review_sha256':REVIEW,'review_hash_recomputed':True,'review_serialization':'sha256(json.dumps([complete_problem_record, exact_key_prior_report_or_empty_object], sort_keys=True).encode())','observed_local_status':c['local_status'],'observed_turns_used':c['turns_used']},
    'prior_report_search_matches':matches,
    'prior_report_search_scope':'Complete supplied corpus scanned by exact ID, exact problem number, full title, and matching arXiv identifier. Broader generic surface-cone and author-name matches were inspected separately and concern different questions.',
    'queue_code_control':queue_check,
    'author_archive':{'safe_member_count':8,'manifest_payload_files':7,'manifest_sha256':MANIFEST,'isolated_replay_byte_equal':True,'author_assertions':8800,'optimized_invocation_rejected':True},
    'limitations':'Input hashes establish byte identity, not mathematical correctness or current worldwide literature status. Source text and data contents are excluded from this output.'
}
print(json.dumps(result,indent=2,sort_keys=True))
