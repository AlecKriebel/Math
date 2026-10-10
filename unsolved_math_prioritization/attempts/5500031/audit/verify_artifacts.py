#!/usr/bin/env python3
"""Verify the author freeze and optional complete public provenance inputs.

Only hashes, counts, identifiers and match results are emitted. Source text and
dataset records are never emitted. Python 3 standard library only.
"""
import argparse
import hashlib
import html
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import zipfile

def sha(b): return hashlib.sha256(b).hexdigest()
def blobsha(b): return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def summary(b): return {'bytes':len(b),'sha256':sha(b)}
def load(p): return json.loads(Path(p).read_bytes())
def tree_sha(d):
    buf=b''
    for x in sorted(d['tree'],key=lambda z:z['path']+('/' if z['type']=='tree' else '')):
        buf+=x['mode'].lstrip('0').encode()+b' '+x['path'].encode()+b'\0'+bytes.fromhex(x['sha'])
    return hashlib.sha1(b'tree '+str(len(buf)).encode()+b'\0'+buf).hexdigest()

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--author-package',type=Path,required=True)
parser.add_argument('--author-zip',type=Path,required=True)
for name in ('problems','reports','catalog','dataset-manifest','dataset-descriptor','campaign-tree','attempts-tree','queue','primary-html'):
    parser.add_argument('--'+name,type=Path)
args=parser.parse_args()
out={'problem_id':5500031,'problem_code':'AMR-054-0031','status':'PASS'}
frozen=args.author_package
manifest_bytes=(frozen/'MANIFEST.json').read_bytes()
assert sha(manifest_bytes)=='ed99d8e8d377db851e03a09bc1b30c9e94ed2b8cc17f5b0cb7c73827506a10fe'
manifest=json.loads(manifest_bytes)
expected={x['path'] for x in manifest['files']}|{'MANIFEST.json'}
assert {x.name for x in frozen.iterdir() if x.is_file()}==expected
for item in manifest['files']:
    data=(frozen/item['path']).read_bytes()
    assert summary(data)=={'bytes':item['bytes'],'sha256':item['sha256']}
archive=args.author_zip.read_bytes()
assert sha(archive)=='7112c0fff3aaf9cbbd429af541d1e08b30677a380155382e5b96095e02ff57dd'
with zipfile.ZipFile(args.author_zip) as z:
    assert set(z.namelist())==expected and len(z.namelist())==len(expected)
    assert all(z.read(name)==(frozen/name).read_bytes() for name in expected)
    with tempfile.TemporaryDirectory(prefix='segment-mirror-freeze-') as tmp:
        z.extractall(tmp)
        replay=subprocess.check_output([sys.executable,str(Path(tmp)/'verify.py')],cwd=tmp)
        assert replay==(frozen/'check_results.json').read_bytes()
        author_result=json.loads(replay)
        assert author_result['assertions']==20012 and author_result['status']=='PASS'
out['author_freeze']={'zip':summary(archive),'manifest':summary(manifest_bytes),
                      'file_count':len(expected),'manifest_entries_verified':len(manifest['files']),
                      'zip_members_match_frozen_files':True,'relocated_replay_byte_identical':True,
                      'exact_assertions':author_result['assertions']}
independent_path=Path(__file__).with_name('independent_verify.py')
independent=subprocess.check_output([sys.executable,str(independent_path)])
assert independent==Path(__file__).with_name('independent_results.json').read_bytes()
result=json.loads(independent)
cert=dict(result['box_escape_certificate']); cert.pop('singular')
assert cert==author_result['box_escape_certificate']
out['independent_replay']={'exact_assertions':result['assertions'],'byte_identical':True,
                         'author_certificate_matches_independent_geometry':True,
                         'code_imports_author_implementation':False}

optional=(args.problems,args.reports,args.catalog,args.dataset_manifest,args.dataset_descriptor,
          args.campaign_tree,args.attempts_tree,args.queue,args.primary_html)
if any(optional):
    assert all(optional),'Supply all optional provenance inputs together.'
    dm=load(args.dataset_manifest); descriptor=load(args.dataset_descriptor)
    assert dm['revision']==descriptor['sha']=='37e53eabe540fb458758e198be61634bd02ee008'
    siblings={x['rfilename']:x for x in descriptor['siblings']}
    datasets={}
    for label,path in [('problems.json',args.problems),('research_results.json',args.reports)]:
        b=path.read_bytes(); datasets[label]=json.loads(b)
        assert summary(b)==dm['files'][label]
        assert sha(b)==siblings[label]['lfs']['sha256']
        assert len(b)==siblings[label]['size']==siblings[label]['lfs']['size']
    assert len(datasets['problems.json'])==15458
    assert len(datasets['research_results.json'])==6701
    matches=[x for x in datasets['problems.json'] if str(x['id'])=='5500031']
    assert len(matches)==1
    record=matches[0]; assert record['problem_number']=='AMR-054-0031'
    assert 'AMR-054-0031' in datasets['research_results.json']
    catalog_bytes=args.catalog.read_bytes();catalog=json.loads(catalog_bytes)
    assert len(catalog)==15458
    selected=[x for x in catalog if str(x['id'])=='5500031'];assert len(selected)==1
    selected=selected[0]
    assert selected['rank']==776 and selected['turns_used']==0 and selected['turn_limit']==5
    statement_hash=sha(record['statement'].encode())
    assert statement_hash==selected['statement_hash']=='1bab344ef6aa4837a9d4780a2dfad1bbb1e4235437022dd9bfaf9cb9263eb5ce'
    primary=args.primary_html.read_text()
    raw=re.search(r'Statement</dt>\s*<dd><p>(.*?)</p>',primary,re.S).group(1)
    statement=html.unescape(re.sub(r'<[^>]+>','',raw))
    assert statement==record['statement']
    campaign=load(args.campaign_tree); attempts=load(args.attempts_tree)
    assert not campaign.get('truncated') and not attempts.get('truncated')
    assert tree_sha(campaign)==campaign['sha']=='cd949ba4de14bdd9f56373cb8281f653d084e790'
    entries={x['path']:x for x in campaign['tree']}
    assert tree_sha(attempts)==attempts['sha']==entries['attempts']['sha']=='8a3df2ca533ab0b03db59563a593a0b55cf69fa3'
    assert len(attempts['tree'])==62
    assert not any(x['path']=='5500031' for x in attempts['tree'])
    for name,b in [('catalog.json',catalog_bytes),('manifest.json',args.dataset_manifest.read_bytes()),('QUEUE.md',args.queue.read_bytes())]:
        assert blobsha(b)==entries[name]['sha'] and len(b)==entries[name]['size']
    queue_lines=[line for line in args.queue.read_text().splitlines() if '5500031 / AMR-054-0031' in line]
    assert len(queue_lines)==1
    assert '| 776 |' in queue_lines[0] and '| queued | 0/5 |' in queue_lines[0]
    out['provenance']={'complete_problems':15458,'complete_prior_reports':6701,
                       'dataset_files':dm['files'],'dataset_revision':dm['revision'],
                       'fresh_descriptor':summary(args.dataset_descriptor.read_bytes()),
                       'both_files_match_manifest_and_descriptor':True,
                       'selected_record_count':1,'prior_report_key_present':True,
                       'catalog':dict(summary(catalog_bytes),git_blob_sha=blobsha(catalog_bytes)),
                       'statement_sha256':statement_hash,'live_primary_statement_exact_match':True,
                       'catalog_rank':776,'baseline_queue_status':'queued 0/5',
                       'attempts_tree_sha':attempts['sha'],'complete_attempt_directory_entries':62,
                       'baseline_target_attempt_directory_present':False,
                       'campaign_tree_sha':campaign['sha'],'campaign_and_attempt_tree_hashes_verified':True,
                       'queue_git_blob_sha':blobsha(args.queue.read_bytes()),
                       'dataset_manifest':summary(args.dataset_manifest.read_bytes())}
print(json.dumps(out,sort_keys=True,indent=2))
