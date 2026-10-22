"""Independently verify every retained source-byte claim without fetching/running sources."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,zipfile

D=Path(__file__).resolve().parent
P=D.parents[2]
A=D/'priority_author_updates_01'
B=D/'priority_classical_general_01'
checked=[]

def verify(row,magic=None):
    path=Path(row['path'])
    assert path.resolve().is_relative_to(P.resolve()),str(path)
    data=path.read_bytes()
    assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256'],str(path)
    if 'md5' in row:assert hashlib.md5(data).hexdigest()==row['md5']
    if magic is not None:assert data.startswith(b'%PDF-')==magic,str(path)
    checked.append(dict(path=str(path.relative_to(P)),bytes=len(data),sha256=hashlib.sha256(data).hexdigest()))
    return data

inventory=json.loads((A/'SOURCE_BYTE_INVENTORY.json').read_text())
for row in inventory['existing_primary_files']:verify(row,True)
http=json.loads((A/'SOURCE_ACCESS_RECEIPTS.json').read_text())
for row in http:
    assert row['method']=='GET' and row['authentication']=='none'
    if row['success']:
        verify(dict(path=row['saved_private_path'],bytes=row['bytes'],sha256=row['sha256']))
    elif 'saved_private_error_path' in row:
        verify(dict(path=row['saved_private_error_path'],bytes=row['error_bytes'],sha256=row['error_sha256']))
archive_rows=[]
for row in inventory['source_archives']:
    verify(row['archive'])
    with zipfile.ZipFile(row['archive']['path']) as archive:
        assert archive.testzip() is None
        names=archive.namelist()
        assert len(names)==len(set(names))
        assert names==[x['path'] for x in row['members']]
        for item in row['members']:
            data=archive.read(item['path'])
            assert len(data)==item['bytes'] and hashlib.sha256(data).hexdigest()==item['sha256']
    archive_rows.append(dict(version=row['version'],members=len(names),all_actual_member_bytes_and_CRC_verified=True,downloaded_code_executed=False))
version_rows=[]
for row in inventory['original_arxiv_versions']:
    verify(row['byte_receipt'],True)
    text=(A/'private_reading'/('invariants_v'+str(row['version'])+'.txt')).read_text()
    matching=[line for line in text.splitlines() if 'k303,b' in line]
    assert len(matching)==1 and '?' in matching[0],(row['version'],matching)
    version_rows.append(dict(version=row['version'],actual_target_row=matching[0],recorded_locations=row['target_locations']))
sources=json.loads((B/'SOURCE_RECEIPTS.json').read_text())
for row in sources['primary_pdf_receipts']:verify(row,True)
verify(sources['retained_published_text_receipt'],False)
verify(sources['failed_pdf_returned_html_receipt'],False)
result=dict(utc=datetime.now(timezone.utc).isoformat(),status='PASS',all_actual_retained_source_byte_claims_verified=True,total_actual_byte_checks=len(checked),unique_actual_paths=len({x['path'] for x in checked}),A_existing_primary_PDF_count=len(inventory['existing_primary_files']),A_HTTP_attempts=len(http),A_HTTP_successes=sum(x['success'] for x in http),B_primary_PDF_count=len(sources['primary_pdf_receipts']),archive_checks=archive_rows,original_source_versions=version_rows,source_file_pins=checked,limits='Byte verification authenticates retained inputs and archive membership, not every historical availability time or all underlying theorem claims. Unavailable publisher PDF and partial web screens remain explicitly qualified in reports. No source or original scientific files modified; no downloaded code executed.')
(D/'ROOT_PRIORITY_SOURCE_BYTE_VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='source_file_pins'},indent=2))
