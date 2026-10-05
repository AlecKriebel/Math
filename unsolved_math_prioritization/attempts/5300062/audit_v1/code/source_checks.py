#!/usr/bin/env python3
"""Optional full-file provenance checks. Inputs are deliberately not distributed."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

if sys.flags.optimize:
    raise SystemExit('Optimized Python is not supported.')

def check(ok,why):
    if not ok:raise RuntimeError(why)

def digest(b):return hashlib.sha256(b).hexdigest()
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()

def run():
    p=argparse.ArgumentParser()
    for name in ['catalog','problems','research','dataset-manifest','review','attempt-tree','source-dir']:p.add_argument('--'+name,required=True,type=Path)
    a=p.parse_args()
    expected={'catalog':(21735099,'891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566'),
              'problems':(68931837,'04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf'),
              'research':(80334822,'8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b')}
    records={};files={}
    for name,(size,sha) in expected.items():
        b=getattr(a,name).read_bytes();check((len(b),digest(b))==(size,sha),'full-file mismatch '+name)
        records[name]=json.loads(b);files[name]={'bytes':len(b),'sha256':digest(b),'git_blob_sha':blob(b)}
    b=a.dataset_manifest.read_bytes();check(blob(b)=='55589bae6bad2d3e2f696e08645330ff1219b709','pinned dataset manifest')
    manifest=json.loads(b)
    for disk,remote in [('problems','problems.json'),('research','research_results.json')]:
        check((files[disk]['bytes'],files[disk]['sha256'])==(manifest['files'][remote]['bytes'],manifest['files'][remote]['sha256']),'repository manifest binding')
    selected=[x for x in records['problems'] if x['id']==5300062];catalog=[x for x in records['catalog'] if x['id']=='5300062']
    check(len(selected)==len(catalog)==1,'unique selected records')
    problem=selected[0];cat=catalog[0];research=records['research'][problem['problem_number']]
    statement_hash=digest(problem['statement'].encode());review_hash=digest(json.dumps([problem,research],sort_keys=True).encode())
    check(statement_hash==cat['statement_hash']=='274cc9221703b1100e6794f4dc183dbd4c1189bf272795422699eb7660340b41','statement binding')
    check(review_hash==cat['review_hash']=='b7b442519b7489ed54933de971ba4f04b049ea50aedd2cf1e246a7d566e9b392','review binding')
    check(cat['rank']==796,'rank')
    b=a.review.read_bytes();check(blob(b)=='1dbdd0f736f70e70ebe84cf9ed93d1e71bdc6a23','desk review git blob')
    review_rows=[x for x in json.loads(b) if x['id']=='5300062'];check(len(review_rows)==1,'selected desk review')
    for key in ['p_solve','p_valid_open','route']:check(review_rows[0][key]==cat[key],'desk review field '+key)
    check(review_rows[0]['impact']==cat['base_impact'],'desk review base impact')
    desk={'bytes':len(b),'sha256':digest(b),'git_blob_sha':blob(b),'selected_row_count':1,'prior_proof':False}
    tree=json.loads(a.attempt_tree.read_bytes());check(not tree['truncated'],'truncated attempts tree')
    children={'':[]};expected_trees={'':tree['sha']}
    for e in tree['tree']:
        par,_,name=e['path'].rpartition('/');children.setdefault(par,[]).append((name,e))
        if e['type']=='tree':children.setdefault(e['path'],[]);expected_trees[e['path']]=e['sha']
    for par,items in children.items():
        items.sort(key=lambda x:(x[0]+('/' if x[1]['type']=='tree' else '')).encode())
        raw=b''.join((e['mode'].lstrip('0')+' '+n).encode()+b'\0'+bytes.fromhex(e['sha']) for n,e in items)
        check(hashlib.sha1(b'tree '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==expected_trees[par],'tree mismatch '+par)
    check(tree['sha']=='c6b68b279db013a0511bfd9a3f3aa2cc2673dc5e','pinned attempts root')
    prior_matches=[e for e in tree['tree'] if '5300062' in e['path']];check(not prior_matches,'prior attempt path appeared')
    pdf_expected={
      'ims92-7.pdf':(1151433,'e0dbfa6ad56d14971d4f901dc8568731e22359feeb1efb429b240f156b88d29e'),
      'fs05.pdf':(545994,'33b8e81e4474e885fc63d988ac263b79abe821176151b824bca6b1f13172ccd9'),
      'foerster06.pdf':(898212,'48d6850baa7c27406504266af9fc3bbc275d3af5b9fb2503068ba8ffdda6319b'),
      'viana88.pdf':(133261,'f45a4abfefbeaf2dc494ba1a0347a9fd554bc0ed8e460f398c5c51ae10e3bcc4'),
      'chwang26.pdf':(224733,'55ef807740350d22d8bb2269d833d7a2f7d03c2e34c305f6eeed5f342d8a4468')}
    pdfs={}
    for name,expected_pair in pdf_expected.items():
        b=(a.source_dir/name).read_bytes();check(b.startswith(b'%PDF-'),'not PDF '+name);check((len(b),digest(b))==expected_pair,'PDF mismatch '+name)
        pdfs[name]={'bytes':len(b),'sha256':digest(b)}
    return {'result':'PASS_FULL_FILE_PROVENANCE','problem_id':5300062,'rank':796,'full_files':files,
      'dataset_revision':manifest['revision'],'problem_records':len(records['problems']),
      'research_report_keys':len(records['research']),'selected_statement_utf8_bytes':len(problem['statement'].encode()),
      'statement_sha256':statement_hash,'review_sha256':review_hash,'review_hash_recomputed':True,
      'review_hash_serialization':'SHA256(json.dumps([selected_problem, selected_research_report], sort_keys=True).encode())',
      'desk_review':desk,'attempt_tree':{'root_sha':tree['sha'],'entries':len(tree['tree']),'git_tree_nodes_rebuilt':len(children),'all_nodes_match':True,'selected_path_matches':0,'truncated':False},
      'source_pdf_hashes':pdfs,'fresh_full_corpus_download':False,'limits':'Cached full bytes were independently rehashed; metadata was freshly checked at the pinned repository revision. Prior-attempt coverage is bounded.'}

if __name__=='__main__':print(json.dumps(run(),indent=2,sort_keys=True))
