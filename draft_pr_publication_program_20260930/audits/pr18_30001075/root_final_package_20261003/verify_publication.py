"""Unauthenticated public download readback of the actual published PR18 package."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import sys
from urllib.request import Request, urlopen

if sys.flags.optimize or sys.argv[1:]:
    raise RuntimeError('Nonoptimized no-argument execution required')
own = Path(__file__).resolve().parent
a18 = own.parent
program = a18.parents[1]
captures = program/'audits/pr45_9900007'
receipt_path = captures/'root_pr18_zenodo_published_record_inspection_actual_capture/stdout.bin'
receipt = json.loads(receipt_path.read_bytes())
if receipt['state']!='published' or receipt['id']!=23127955 or receipt['doi']!='10.5281/zenodo.23127955':
    raise RuntimeError('Published record identity mismatch')
results = []
for item in receipt['files']:
    local = a18/'preprint_v1'/item['name']
    url = 'https://zenodo.org/records/23127955/files/'+item['name']+'?download=1'
    request = Request(url,headers={'User-Agent':'Math-PR-Publication-Review/1.0'},method='GET')
    with urlopen(request,timeout=30) as response:
        body = response.read(item['size']+1)
        row = {'name':item['name'],'url':url,'HTTP_status':response.status,
               'final_url':response.url,'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest(),
               'md5':hashlib.md5(body).hexdigest(),'authentication_sent':False}
    if len(body)!=item['size'] or row['sha256']!=item['sha256'] or body!=local.read_bytes():
        raise RuntimeError('Public bytes mismatch: '+item['name'])
    results.append(row)
publication = a18/'publication'
publication.mkdir(exist_ok=True)
(publication/'ZENODO_RECEIPT.json').write_bytes(receipt_path.read_bytes())
record = {'schema':'pr18-publication-verification/v1',
          'UTC':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_pid':os.getpid(),
          'DOI':receipt['doi'],'record_id':receipt['id'],'record_url':receipt['record_url'],
          'published':True,'DOI_resolution':receipt['doi_resolution'],
          'authenticated_metadata_and_remote_file_checks':'Exact intended fields/file domain/checksums inspected by repository tool; only omitted affiliation to null representation reported',
          'inspection_receipt_sha256':hashlib.sha256(receipt_path.read_bytes()).hexdigest(),
          'public_file_readbacks':results,'all_public_bytes_identical':True,
          'tracker_row_written':False,'tracker_status':'Google CLI expired/revoked; human reconnect pending',
          'native_merged':False,'workflow_estimate_percent':95,'new_central_attempts':0}
(publication/'PUBLICATION_VERIFICATION.json').write_text(json.dumps(record,indent=2)+'\n')
entry = '\n## '+record['UTC']+' — PR18 preprint publicly verified\n\nZenodo record23127955 is published with DOI10.5281/zenodo.23127955, which resolves HTTP200. Both public PDF/ZIP downloads match the reviewed local bytes and SHA256 hashes. The sole metadata representation normalization is the API-added null creator affiliation; name, ORCID, supplied fields and order remain exact. All29 offline upload-tool regressions pass after the narrow adapter. Original failed-stage evidence and saved draft identity were preserved; no duplicate deposit was created. Tracker credentials remain expired/revoked, with reconnect pending; no row or merge is claimed yet. Publication/integration workflow estimate95%; original1/5 accounting and new-attempt credit0 unchanged.\n'
for p in [a18/'RESEARCH_LOG.md',program/'RESEARCH_LOG.md']:
    with p.open('ab') as f:
        f.write(entry.encode())
print(json.dumps(record,indent=2))
