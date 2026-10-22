#!/usr/bin/env python3
"""Recompute source identities without printing or distributing source contents."""
import argparse
import hashlib
import json
import zipfile
from pathlib import Path


def digest(path):
    h=hashlib.sha256()
    count=0
    with path.open('rb') as f:
        while chunk:=f.read(1024*1024):
            count+=len(chunk)
            h.update(chunk)
    return {'bytes':count,'sha256':h.hexdigest()}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ['problems','research','catalog','pinned_tree','repository_manifest','author_zip','owr_pdf','article_pdf']:
        p.add_argument('--'+name.replace('_','-'),type=Path,required=True)
    a=p.parse_args()
    manifest=json.loads(a.repository_manifest.read_text())
    tree=json.loads(a.pinned_tree.read_text())
    result={'status':'PASS','problem_id':30005356,'problem_number':'OWR-12697685-001',
            'dataset_revision':manifest['revision'],'complete_file_checks':{}}
    assert manifest['revision']=='37e53eabe540fb458758e198be61634bd02ee008'
    for name,path in [('problems.json',a.problems),('research_results.json',a.research)]:
        actual=digest(path)
        assert actual==manifest['files'][name]
        entry=next(v for v in tree if v['path']==name)
        assert actual['bytes']==entry['size']==entry['lfs']['size']
        assert actual['sha256']==entry['lfs']['oid']
        result['complete_file_checks'][name]={**actual,'matches_pinned_LFS_and_repository_manifest':True}
    problems=json.loads(a.problems.read_text())
    matches=[(i,v) for i,v in enumerate(problems) if v.get('id')==30005356]
    assert len(matches)==1
    index,row=matches[0]
    assert row['problem_number']=='OWR-12697685-001'
    catalogue=json.loads(a.catalog.read_text())
    selected=[v for v in catalogue if str(v.get('id'))=='30005356']
    assert len(selected)==1
    cat=selected[0]
    assert cat['problem_number']==row['problem_number']
    assert cat['rank']==778
    statement_hash=hashlib.sha256(row['statement'].encode()).hexdigest()
    assert statement_hash==cat['statement_hash']
    canonical=json.dumps(row,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
    result['dataset_identity']={'records':len(problems),'selected_count':len(matches),'index':index,
        'statement_utf8_sha256':statement_hash,'canonical_record_sha256':hashlib.sha256(canonical).hexdigest(),
        'catalogue_statement_and_code_match':True}
    data=a.catalog.read_bytes()
    blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    assert blob=='bd5c23e4e6c7e1901717a7e596477a7f6dc72425'
    result['catalogue']={**digest(a.catalog),'git_blob_sha1':blob}
    reports=json.loads(a.research.read_text())
    assert row['problem_number'] not in reports
    review_hash=hashlib.sha256(json.dumps([row,{}],sort_keys=True).encode()).hexdigest()
    assert review_hash==cat['review_hash']=='00c719d497159151748580b116c2a138f20956fbd106b60808c144bf4ca63de8'
    result['review_identity']={'rank':cat['rank'],'review_hash':review_hash,'independently_recomputed':True,
        'recipe':'SHA-256 of UTF-8 json.dumps([problem_record, {}], sort_keys=True), other Python defaults; absent report normalized to {}.',
        'recipe_source':'https://github.com/AlecKriebel/Math/blob/cb8091dcfa69ed41defad72963836f5f8920648f/unsolved_math_prioritization/queue.py#L111'}
    tokens=['30005356','12697685','definable endomorphisms of generic multiplicative']
    matches=[k for k,v in reports.items() if any(s in (str(k)+' '+json.dumps(v)).lower() for s in tokens)]
    assert not matches
    result['prior_report_check']={'entries':len(reports),'exact_key_present':False,'id_code_title_matches':0,
        'absence_scope':'Complete pinned public dictionary only, not unpublished or deleted work.'}
    result['author_zip']=digest(a.author_zip)
    assert result['author_zip']=={'bytes':16791,'sha256':'b5d4c852204b60d7a91cfa0d1c6125bd9deac64d460fc1a0f49a196df01a9d96'}
    with zipfile.ZipFile(a.author_zip) as z:
        names=z.namelist()
        assert len(names)==len(set(names))==9
        assert all('/' not in n and '\\' not in n and n not in ['.','..'] for n in names)
        m=json.loads(z.read('MANIFEST.json'))
        assert set(names)=={v['path'] for v in m['files']}|{'MANIFEST.json'}
        for f in m['files']:
            data=z.read(f['path'])
            assert len(data)==f['bytes'] and hashlib.sha256(data).hexdigest()==f['sha256']
        result['author_zip']['files']=len(names)
        result['author_zip']['all_manifest_entries_verified']=True
        result['author_zip']['manifest_sha256']=hashlib.sha256(z.read('MANIFEST.json')).hexdigest()
    result['scholarly_pdfs']={
        'OWR_2023_2':digest(a.owr_pdf),
        'arxiv_2212_02115v4':digest(a.article_pdf)}
    assert result['scholarly_pdfs']['OWR_2023_2']=={'bytes':663768,'sha256':'b1b6888f062a085403d4c4b4b51df47a8421ed7210116c939a76c8463a653e14'}
    assert result['scholarly_pdfs']['arxiv_2212_02115v4']=={'bytes':726746,'sha256':'dcc2788d07ec952a6799a90844d5a2b3f4b0b8a943a223b80fed90c04885d06f'}
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__':
    main()
