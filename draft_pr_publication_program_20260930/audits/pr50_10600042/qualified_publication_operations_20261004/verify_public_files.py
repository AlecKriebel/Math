"""Read PR50's published files without authentication and bind exact local bytes.

The repository upload kit must have already performed authenticated metadata,
file-domain and checksum inspection. This helper does not create or publish.
"""
import argparse
import datetime as dt
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
from urllib.parse import quote
from urllib.request import Request, urlopen

def sha(body): return hashlib.sha256(body).hexdigest()
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest',type=Path,required=True)
    parser.add_argument('--inspection-receipt',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    if sys.flags.optimize: raise RuntimeError('Optimization is forbidden')
    own=Path(__file__).resolve().parent; repo=own.parents[3]
    manifest=args.manifest.resolve(); receipt_path=args.inspection_receipt.resolve()
    output=args.output.resolve()
    if manifest != own.parent/'publication_package_v3/zenodo-deposit.json':
        raise RuntimeError('Only the operative PR50 manifest is accepted')
    if output.exists(): raise RuntimeError('Never overwrite an earlier verification')
    output.relative_to(own.parent)
    spec=importlib.util.spec_from_file_location('pr50_public_readback_kit',repo/'zenodo_deposit_tool/zenodo.py')
    kit=importlib.util.module_from_spec(spec); spec.loader.exec_module(kit)
    metadata,files=kit.load_manifest(manifest)
    receipt=json.loads(receipt_path.read_bytes())
    if receipt.get('environment')!='production' or receipt.get('state')!='published':
        raise RuntimeError('Actual production published inspection required')
    record_id=receipt.get('id'); doi=receipt.get('doi')
    if type(record_id) is not int or doi!='10.5281/zenodo.'+str(record_id):
        raise RuntimeError('Actual Zenodo record DOI/ID mismatch')
    if receipt.get('title')!=metadata['title']:
        raise RuntimeError('Inspection title differs from operative metadata')
    expected=[{'name':f['name'],'size':f['size'],'sha256':f['sha256']} for f in files]
    if receipt.get('files')!=expected:
        raise RuntimeError('Inspection file domain or actual local pins differ')
    readbacks=[]
    for item in files:
        url='https://zenodo.org/records/'+str(record_id)+'/files/'+quote(item['name'],safe='')+'?download=1'
        request=Request(url,headers={'User-Agent':'Math-PR-Publication-Review/1.0'},method='GET')
        with urlopen(request,timeout=30) as response:
            body=response.read(item['size']+1)
            row={'name':item['name'],'url':url,'HTTP_status':response.status,
                 'final_url':response.url,'bytes':len(body),'sha256':sha(body),
                 'md5':hashlib.md5(body).hexdigest(),'authentication_sent':False}
        if not 200<=row['HTTP_status']<300 or len(body)!=item['size'] or sha(body)!=item['sha256'] or body!=item['path'].read_bytes():
            raise RuntimeError('Public file bytes differ: '+item['name'])
        readbacks.append(row)
    record={'schema':'pr50-qualified-note-publication-verification/v1',
            'UTC':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_pid':os.getpid(),
            'DOI':doi,'record_id':record_id,'record_url':'https://zenodo.org/records/'+str(record_id),
            'published':True,'all_public_bytes_identical':True,
            'public_file_readbacks':readbacks,'DOI_resolution':receipt.get('doi_resolution'),
            'manifest':{'path':manifest.relative_to(repo).as_posix(),'sha256':sha(manifest.read_bytes())},
            'inspection_receipt':{'path':receipt_path.relative_to(repo).as_posix(),'sha256':sha(receipt_path.read_bytes())},
            'authenticated_metadata_and_file_inspection':'Repository kit inspect verified intended metadata and exact domain/size/checksums; no new metadata inference by this download readback.',
            'historical_priority_certified':False,'present_openness_certified':False,
            'publication_kind':'Verified research note with explicit unresolved Nencka priority/access limitations',
            'tracker_row_written':False,'native_merged':False,'new_central_attempts':0}
    output.parent.mkdir(parents=True,exist_ok=True)
    with output.open('x') as stream: json.dump(record,stream,indent=2); stream.write('\n')
    print(json.dumps(record,indent=2))
if __name__=='__main__': main()
