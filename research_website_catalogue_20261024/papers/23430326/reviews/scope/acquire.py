#!/usr/bin/env python3
"""Fresh unauthenticated public Zenodo intake, with no source-code execution."""
from pathlib import Path,PurePosixPath
import datetime
import hashlib
import json
import stat
import urllib.request
import zipfile

PAPER=Path(__file__).resolve().parents[2]
S=PAPER/'sources'
ID='23430326'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def fetch(url):
    started=now()
    req=urllib.request.Request(url,headers={'User-Agent':'Independent research source verification (public scholarly record)'})
    with urllib.request.urlopen(req,timeout=50) as r:
        body=r.read();rec={'url':url,'final_url':r.url,'http_status':r.status,'started_utc':started,'retrieved_utc':now(),'headers':dict(r.headers),'bytes':len(body),'md5':hashlib.md5(body).hexdigest(),'sha256':hashlib.sha256(body).hexdigest()}
    return body,rec
def save(name,obj):
    with (S/name).open('x') as f:f.write(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
raw,request=fetch('https://zenodo.org/api/records/'+ID)
record=json.loads(raw)
assert str(record['id'])==ID
assert record['metadata']['title']=='An explicit noninduced Langlands quotient with vanishing unitary periods'
assert record['metadata']['version']=='1.1'
assert record['metadata']['publication_date']=='2026-10-16'
with (S/'record-raw.json').open('xb') as f:f.write(raw)
save('record.json',record)
expected={'paper.pdf':(106606,'b5eac802fb40161d2a129b0f9898d348'),'pr1032_supportkit_v1.1.zip':(394529,'c23fde2093aa0627daa36ba61d6bca1f')}
assert {x['key'] for x in record['files']}==set(expected)
files=[]
for item in record['files']:
    name=item['key'];size,md5=expected[name]
    assert item['size']==size and item['checksum']=='md5:'+md5
    data,rec=fetch(item['links']['self'])
    assert len(data)==size and rec['md5']==md5
    if name=='paper.pdf':assert rec['sha256']=='1144eb3999212084bef013e7984bfc54bf43a9f931d959b63ba2743d814cf0a9'
    with (S/name).open('xb') as f:f.write(data)
    rec.update({'name':name,'zenodo_checksum':item['checksum'],'verified_against_api':True,'verified_against_assignment':True})
    files.append(rec)
receipt={'record_id':ID,'retrieved_utc':now(),'record_url':'https://zenodo.org/api/records/'+ID,'record_raw_bytes':len(raw),'record_raw_sha256':request['sha256'],'record_request':request,'files':files,'model_identity':{'model':'gpt-6.1-sol','reasoning_effort':'ultra','fork_turns':'none','role':'fresh source intake and independent scope'}}
save('receipt.json',receipt)
archive=S/'pr1032_supportkit_v1.1.zip'
inventory=[]
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    names=set()
    for item in z.infolist():
        if item.is_dir():continue
        name=item.filename;parts=PurePosixPath(name).parts;mode=item.external_attr>>16
        assert not name.startswith('/') and '..' not in parts and '\\' not in name and not any(ord(c)<32 for c in name)
        assert name not in names;names.add(name)
        assert not item.flag_bits&1
        assert stat.S_IFMT(mode) in (0,stat.S_IFREG)
        data=z.read(item)
        assert not name.lower().endswith(('.zip','.tar','.gz','.7z','.rar'))
        target=S/'support'/name;target.parent.mkdir(parents=True,exist_ok=True)
        with target.open('xb') as f:f.write(data)
        if stat.S_IMODE(mode):target.chmod(stat.S_IMODE(mode))
        inventory.append({'member':name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'crc32':f'{item.CRC:08x}','mode':oct(mode),'hidden':any(x.startswith('.') for x in parts),'extracted_path':str(target),'regular':True})
save('asset-inventory.json',{'record_id':ID,'utc':now(),'archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'regular_members':len(inventory),'total_uncompressed_bytes':sum(x['bytes'] for x in inventory),'members':inventory,'unsafe_paths':[],'links_special_files':[],'nested_archives':[]})
print(json.dumps({'status':'SOURCE_READY','record_id':ID,'pdf_path':str(S/'paper.pdf'),'pdf_bytes':(S/'paper.pdf').stat().st_size,'pdf_sha256':hashlib.sha256((S/'paper.pdf').read_bytes()).hexdigest(),'zip_path':str(archive),'zip_sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'archive_regular_members':len(inventory),'receipt_sha256':hashlib.sha256((S/'receipt.json').read_bytes()).hexdigest()}))
