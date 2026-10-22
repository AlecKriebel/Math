#!/usr/bin/env python3
"""Hash and identity checks using locally supplied, excluded source inputs."""
import argparse
import hashlib
import json
from pathlib import Path


def digest(data):
    return hashlib.sha256(data).hexdigest()


def file_metadata(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': digest(data)}


def run(problems_path, research_path, catalog_path, pdf_dir=None):
    root=Path(__file__).resolve().parents[1]
    expected=json.loads((root/'SOURCE_AUDIT.json').read_text())
    actual={}
    for name,path in [('problems.json',problems_path),('research_results.json',research_path),('catalog.json',catalog_path)]:
        actual[name]=file_metadata(path)
        assert actual[name] == expected['complete_local_files'][name], name
    problems=json.loads(problems_path.read_bytes())
    research=json.loads(research_path.read_bytes())
    catalog=json.loads(catalog_path.read_bytes())
    assert len(problems)==15458 and len(research)==6701
    selected=[p for p in problems if str(p['id'])=='30005114']
    assert len(selected)==1
    p=selected[0]
    assert p['problem_number']=='OWR-10252930-024'
    assert sum(x['problem_number']==p['problem_number'] for x in problems)==1
    assert p['problem_number'] not in research
    matches=sum('30005114' in json.dumps(x) or p['problem_number'] in json.dumps(x) for x in research.values())
    assert matches==0
    selected_catalog=[x for x in catalog if str(x['id'])=='30005114']
    assert len(selected_catalog)==1
    c=selected_catalog[0]
    assert digest(p['statement'].encode())==c['statement_hash']==expected['identity']['statement_sha256']
    assert digest(json.dumps([p,{}],sort_keys=True).encode())==c['review_hash']==expected['identity']['review_sha256']
    assert digest(p['original_statement'].encode())==expected['identity']['original_extraction_sha256']
    cb=catalog_path.read_bytes()
    blob=hashlib.sha1(b'blob '+str(len(cb)).encode()+b'\0'+cb).hexdigest()
    assert blob==expected['repository']['catalog_git_blob']
    assert c['rank']==790
    pdfs={}
    if pdf_dir:
        for source in expected['sources']:
            if 'audit_input_filename' in source:
                name=source['audit_input_filename']
                pdfs[name]=file_metadata(pdf_dir/name)
                assert pdfs[name]==source['pdf'],name
    return {'status':'PASS','complete_local_files':actual,'pdfs':pdfs,
            'selected_id_count':1,'selected_code_count':1,'research_record_count':6701,
            'research_value_match_count':matches,'statement_hash_match':True,
            'canonical_review_hash_match':True,'catalog_git_blob_match':True,
            'raw_source_contents_in_output':False}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--problems',required=True,type=Path)
    parser.add_argument('--research',required=True,type=Path)
    parser.add_argument('--catalog',required=True,type=Path)
    parser.add_argument('--pdf-dir',type=Path)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    result=json.dumps(run(args.problems,args.research,args.catalog,args.pdf_dir),indent=2,sort_keys=True)+'\n'
    if args.output:args.output.write_text(result)
    print(result,end='')
