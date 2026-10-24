#!/usr/bin/env python3
"""Read-only independent source-integrity checks; writes only own receipt.

Integrity checks do not prove mathematical theorems or literature absence.
"""
from pathlib import Path
from hashlib import sha256,md5
from datetime import datetime,timezone
import json

HERE=Path(__file__).resolve().parent
PREP=HERE.parent/'priority'

def digest(p):return sha256(p.read_bytes()).hexdigest()
def norm(s):return ' '.join(s.split())
def block(s):
    start=s.index('21.121.')
    finish=s.index('kourovka-mathematics.pdf).',start)+len('kourovka-mathematics.pdf).')
    return norm(s[start:finish])

def main():
    hashes={}
    seal=json.loads((PREP/'FINAL_SEAL.json').read_text())
    for n,h in seal['files'].items():
        assert digest(PREP/n)==h
        hashes['priority/'+n]=h
    package=json.loads((PREP/'PREPARATION_MANIFEST.json').read_text())
    for row in package['files']:
        p=PREP/row['file'];b=p.read_bytes();h=sha256(b).hexdigest()
        assert h==row['sha256'] and len(b)==row['bytes']
        hashes['priority/'+row['file']]=h
    manifest=json.loads((PREP/'SOURCE_MANIFEST.json').read_text())
    source_records=0
    for row in manifest['sources']:
        if not row.get('file') or not row.get('sha256'):continue
        p=PREP/row['file'];b=p.read_bytes();h=sha256(b).hexdigest()
        assert h==row['sha256'] and len(b)==row['bytes'],row['file']
        hashes['priority/'+row['file']]=h;source_records+=1
    provenance=json.loads((PREP/'OFFICIAL_CACHE_PROVENANCE.json').read_text())
    for row in provenance['reused_cache']:
        p=PREP/row['file'];b=p.read_bytes();h=sha256(b).hexdigest()
        assert h==row['sha256'] and len(b)==row['bytes']
        hashes[row['repository_relative_file']]=h
    versions=[]
    for text,pdf,metadata in [('jayadevan.txt','jayadevan.pdf','zenodo_record.json'),
                              ('jayadevan_latest.txt','jayadevan_latest.pdf','zenodo_latest.json')]:
        data=json.loads((PREP/'cache'/metadata).read_text())
        entry=next(f for f in data['files'] if f['key']=='kourovka-21-121a-paper.pdf')
        body=(PREP/'cache'/pdf).read_bytes()
        assert 'md5:'+md5(body).hexdigest()==entry['checksum']
        versions.append({'record':data['id'],'publication_date':data['metadata']['publication_date'],
                         'pdf_sha256':sha256(body).hexdigest(),'metadata_checksum':entry['checksum']})
    old=(PREP/'cache/jayadevan.txt').read_text()
    new=(PREP/'cache/jayadevan_latest.txt').read_text()
    old='\n'.join(line for line in old.splitlines() if 'Manipal Institute of Technology, MAHE' not in line)
    assert norm(old)==norm(new),'mathematical text differs beyond removed affiliation/whitespace'
    assert digest(HERE/'sources/kinyon_urban.pdf')==digest(PREP/'cache/kinyon_urban.pdf')
    assert digest(HERE/'sources/jayadevan_author.html')==digest(PREP/'cache/jayadevan_author.html')
    main_text=(HERE.parent.parent/'21_122/priority/sources/notebook21_fresh.txt').read_text()
    upd_text=(HERE/'sources/official_updates.txt').read_text()
    assert block(main_text)==block(upd_text)
    result={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS_SOURCE_INTEGRITY_ONLY',
      'package_files_checked':len(package['files']),'source_records_checked':source_records,
      'official_reused_cache_files_checked':len(provenance['reused_cache']),
      'original_and_current_zenodo_pdf_metadata':versions,
      'zenodo_text_change':'Only author affiliation removal and whitespace; normalized mathematical text identical.',
      'fresh_own_KU_pdf_and_author_exposition_match':True,
      'fresh_update_exact_problem_block_matches_main':True,
      'input_sha256':hashes,
      'scope_exclusion':'Does not prove global priority absence, independently rebuild Lean, or reprove each cited theorem.'}
    (HERE/'SOURCE_CHECK_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='input_sha256'},indent=2))

if __name__=='__main__':main()
