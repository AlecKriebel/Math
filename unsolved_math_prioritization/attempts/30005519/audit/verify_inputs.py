#!/usr/bin/env python3
"""Recheck full author/data/source identities from caller-supplied local files.

No network requests, mutations, embedded source content, or machine-specific
paths. Supply all five arguments. Hashes establish identity, not truth.
"""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import json
import zipfile


def require(test, message):
    if not test:
        raise RuntimeError(message)


def identity(data):
    return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    for arg in ('author-zip','problems','reports','catalog','source-dir'):
        ap.add_argument('--'+arg,required=True,type=Path)
    a=ap.parse_args()
    expected=json.loads((Path(__file__).parent/'PROVENANCE.json').read_text())
    archive=a.author_zip.read_bytes()
    require(identity(archive)==expected['author_archive'],'author archive mismatch')
    with zipfile.ZipFile(a.author_zip) as z:
        require(z.testzip() is None,'archive CRC mismatch')
        names=z.namelist()
        require(len(names)==len(set(names))==11,'duplicate or unexpected member count')
        for name in names:
            p=PurePosixPath(name)
            require(not p.is_absolute() and '..' not in p.parts,'unsafe member path')
        mbytes=z.read('safe/AUTHOR_MANIFEST.json')
        require(identity(mbytes)==expected['author_manifest'],'author manifest mismatch')
        manifest=json.loads(mbytes)
        wanted={'safe/AUTHOR_MANIFEST.json'} | {'safe/'+f['path'] for f in manifest['files']}
        require(set(names)==wanted,'unmanifested author member')
        for item in manifest['files']:
            data=z.read('safe/'+item['path'])
            require(identity(data)=={k:item[k] for k in ('bytes','sha256')},'author file mismatch')
    pb=a.problems.read_bytes(); rb=a.reports.read_bytes(); cb=a.catalog.read_bytes()
    for name,b in [('problems.json',pb),('research_results.json',rb),('catalog.json',cb)]:
        require(identity(b)==expected['full_inputs'][name],name+' mismatch')
    problems=json.loads(pb); reports=json.loads(rb); catalog=json.loads(cb)
    rows=[p for p in problems if str(p['id'])=='30005519']
    require(len(problems)==15458 and len(rows)==1,'problem count or identity')
    p=rows[0]
    require(p['problem_number']=='OWR-13750332-001','problem code')
    require(len(reports)==6701,'report count')
    require(not any(k.startswith('OWR') for k in reports),'unexpected OWR report')
    require(b'30005519' not in rb and b'OWR-13750332-001' not in rb,'unexpected report token')
    statement_hash=hashlib.sha256(p['statement'].encode()).hexdigest()
    review_hash=hashlib.sha256(json.dumps([p,{}],sort_keys=True).encode()).hexdigest()
    row=next(x for x in catalog if str(x['id'])=='30005519')
    require(statement_hash==expected['statement_hash']==row['statement_hash'],'statement hash')
    require(review_hash==expected['review_hash']==row['review_hash'],'review hash')
    blob=hashlib.sha1(b'blob '+str(len(cb)).encode()+b'\0'+cb).hexdigest()
    require(blob==expected['catalog_git_blob_sha'],'catalog Git blob')
    for item in expected['source_files']:
        b=(a.source_dir/item['local_filename']).read_bytes()
        require(identity(b)=={k:item[k] for k in ('bytes','sha256')},'source file mismatch')
    record=json.loads((a.source_dir/'zenodo.json').read_text())
    pdf=(a.source_dir/'ferudun_2026.pdf').read_bytes()
    entry=next(x for x in record['files'] if x['key']=='OWR-13750332-001-paper.pdf')
    require(entry['size']==len(pdf),'record PDF size')
    require(entry['checksum']=='md5:'+hashlib.md5(pdf).hexdigest(),'record PDF MD5')
    require(record['metadata']['version']=='1.0','record version')
    require(record['metadata']['publication_date']=='2026-09-30','record publication date')
    print(json.dumps({'status':'PASS','author_files_verified':10,
      'archive_members_verified':11,'full_input_files_hashed':3,
      'problem_records':len(problems),'report_keys':len(reports),
      'source_files_hashed':len(expected['source_files']),
      'statement_hash':statement_hash,'review_hash':review_hash,
      'pdf_matches_record_size_and_md5':True,
      'live_source_retrieval_claim':False},indent=2,sort_keys=True))


if __name__=='__main__':
    main()
