#!/usr/bin/env python3
"""Replay public-input bindings without bundling corpus contents or source PDFs."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

HERE=Path(__file__).resolve().parent

def metadata(data):
    return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}

def check_bytes(data,expected):
    assert metadata(data)=={k:expected[k] for k in ('bytes','sha256')}

def check_author(path):
    binding=json.loads((HERE/'author_binding.json').read_text())
    check_bytes(path.read_bytes(),binding['archive'])
    with zipfile.ZipFile(path) as z:
        assert set(z.namelist())=={r['path'] for r in binding['members']}
        assert len(z.namelist())==len(set(z.namelist()))
        for r in binding['members']:
            assert '/' not in r['path'] and '\\' not in r['path']
            check_bytes(z.read(r['path']),r)
    return {'archive_and_all_members':'PASS','members':len(binding['members'])}

def check_corpora(problems,research,catalog,manifest):
    expected=json.loads((HERE/'provenance_audit.json').read_text())
    pbytes=problems.read_bytes();rbytes=research.read_bytes();cbytes=catalog.read_bytes()
    check_bytes(pbytes,expected['full_corpora']['files']['problems.json'])
    check_bytes(rbytes,expected['full_corpora']['files']['research_results.json'])
    check_bytes(cbytes,expected['catalog'])
    m=json.loads(manifest.read_text())
    assert m['revision']==expected['full_corpora']['revision']
    assert m['files']['problems.json']==metadata(pbytes)
    assert m['files']['research_results.json']==metadata(rbytes)
    ps=json.loads(pbytes);rs=json.loads(rbytes);cs=json.loads(cbytes)
    assert len(ps)==15458 and len(rs)==6701
    selected=[p for p in ps if str(p['id'])=='30004730']
    selected_c=[c for c in cs if str(c['id'])=='30004730']
    assert len(selected)==len(selected_c)==1
    p,c=selected[0],selected_c[0]
    assert p['problem_number']=='OWR-8415335-002' and c['rank']==783
    assert sum(x['problem_number']==p['problem_number'] for x in ps)==1
    assert p['problem_number'] not in rs
    sh=hashlib.sha256(p['statement'].encode()).hexdigest()
    rh=hashlib.sha256(json.dumps([p,rs.get(p['problem_number'],{})],sort_keys=True).encode()).hexdigest()
    assert sh==c['statement_hash']==expected['identity']['statement_sha256']
    assert rh==c['review_hash']==expected['identity']['review_sha256']
    terms=['30004730','owr-8415335-002','consistent conical bicombings in metric spaces']
    matches=[k for k,v in rs.items() if any(t in (k+' '+json.dumps(v,ensure_ascii=False)).lower() for t in terms)]
    assert not matches
    return {'full_corpora_and_catalog':'PASS','problems':len(ps),'research_entries':len(rs),'statement_digest_matches':True,'review_digest_matches':True,'exact_research_matches':0}

def check_pdfs(path):
    expected=json.loads((HERE/'source_audit.json').read_text())
    for r in expected['pdf_sources']:
        check_bytes((path/r['file']).read_bytes(),r['pdf'])
    return {'pdf_input_hashes':'PASS','pdf_count':len(expected['pdf_sources'])}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--author-zip',type=Path)
    p.add_argument('--problems',type=Path)
    p.add_argument('--research',type=Path)
    p.add_argument('--catalog',type=Path)
    p.add_argument('--dataset-manifest',type=Path)
    p.add_argument('--pdf-dir',type=Path)
    a=p.parse_args();results={}
    if a.author_zip:results['author']=check_author(a.author_zip)
    flags=[a.problems,a.research,a.catalog,a.dataset_manifest]
    if any(flags):
        if not all(flags):p.error('Corpus replay needs all four of --problems, --research, --catalog and --dataset-manifest.')
        results['dataset']=check_corpora(*flags)
    if a.pdf_dir:results['sources']=check_pdfs(a.pdf_dir)
    if not results:p.error('Supply at least one public-input group; see --help.')
    print(json.dumps({'status':'PASS','checks':results,'limit':'Input hashes certify byte identity, not mathematical correctness or completeness of literature searches.'},indent=2))

if __name__=='__main__':main()
