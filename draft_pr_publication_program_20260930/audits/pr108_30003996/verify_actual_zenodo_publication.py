#!/usr/bin/env python3
"""Public, credential-free readback of the exact independently reviewed PR108 deposit."""
from pathlib import Path, PurePosixPath
import datetime, hashlib, importlib.util, io, json, os, stat, sys, zipfile
from urllib.request import Request, urlopen

A = Path(__file__).resolve().parent
C = A.parents[2]
D = A / 'publication_ready_package_v2'
OUT = A / 'published_download_verification_20261006'
KIT = Path('/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py')
ID = 23181280
DOI = '10.5281/zenodo.23181280'

def require(ok, why):
    if not ok:
        raise RuntimeError(why)

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def sha(data):
    return hashlib.sha256(data).hexdigest()

def write_json(path, obj):
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False, allow_nan=False) + '\n')

def pin(path):
    b = path.read_bytes()
    return {'path': str(path.relative_to(C)), 'bytes': len(b), 'sha256': sha(b)}

def get(url, name, cap):
    start = now()
    request = Request(url, method='GET', headers={'User-Agent': 'Math-PR108-Public-Readback/1.0', 'Accept': '*/*'})
    with urlopen(request, timeout=30) as response:
        body = response.read(cap + 1)
        require(response.status == 200 and len(body) <= cap, 'HTTP status/body cap')
        require(response.url.startswith('https://zenodo.org/'), 'Unexpected public redirect')
        resolved = response.url
    target = OUT / name
    target.write_bytes(body)
    receipt = {'actual_receipt': True, 'PID': os.getpid(), 'exit_code': 0,
               'HTTP_method': 'GET', 'URL': url, 'resolved_URL': resolved,
               'status_code': 200, 'UTC_start': start, 'UTC_end': now(),
               'response_bytes': len(body), 'response_sha256': sha(body)}
    rp = OUT / (name + '.HTTP_GET.json')
    write_json(rp, receipt)
    return target, rp, receipt

def main():
    require(sha(KIT.read_bytes()) == '26f264df93b657137b343acc05ae87a3e8e60d46cbbb8b822bc327d77b89c277', 'Kit binding')
    gate = json.loads((A / 'ROOT_READY_FOR_PUBLICATION_20261006.json').read_bytes())
    require(gate['publication_ready'] is True and not gate['findings_remaining'], 'Root publication gate')
    pm_bytes = (D / 'PACKAGE_MANIFEST.json').read_bytes()
    require(sha(pm_bytes) == gate['package_manifest_sha256'], 'Exact reviewed package')
    pm = json.loads(pm_bytes)
    published = json.loads((A / 'actual_operations/zenodo_publication_v2_publish/stdout.bin').read_bytes())
    require(published['id'] == ID and published['doi'] == DOI and published['state'] == 'published', 'Actual publish receipt')
    spec = importlib.util.spec_from_file_location('reviewed_repo_zenodo', KIT)
    kit = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(kit)
    metadata, files = kit.load_manifest(D / 'zenodo-deposit.json')
    OUT.mkdir(exist_ok=False)
    record_file, record_receipt_file, record_receipt = get('https://zenodo.org/api/records/' + str(ID), 'record.json', 1024 * 1024)
    record = json.loads(record_file.read_bytes())
    require(record.get('id') == ID and record.get('doi') == DOI and record.get('submitted') is True, 'Published public record')
    public_meta = dict(record['metadata'])
    resource = public_meta['resource_type']
    require(resource['type'] == 'publication' and resource['subtype'] == 'preprint', 'Public resource schema')
    require(isinstance(public_meta['license'], dict) and public_meta['license']['id'] == metadata['license'], 'Public license schema')
    public_meta['upload_type'] = resource['type']
    public_meta['publication_type'] = resource['subtype']
    public_meta['license'] = public_meta['license']['id']
    normalizations = kit.verify({**record, 'metadata': public_meta}, metadata, files)
    transports = {}
    for item in files:
        target, rp, receipt = get('https://zenodo.org/api/records/' + str(ID) + '/files/' + item['name'] + '/content', item['name'], 8 * 1024 * 1024)
        data = target.read_bytes()
        require(len(data) == item['size'] and sha(data) == item['sha256'] and hashlib.md5(data).hexdigest() == item['md5'], 'Actual download differs: ' + item['name'])
        transports[item['name']] = (target, rp, receipt)
    archive, arp, areceipt = transports['root_dependent_spanning_trees_support.zip']
    require(sha(archive.read_bytes()) == gate['archive_sha256'], 'Reviewed archive')
    expected = {x['relative_path']: x for x in pm['files']}
    require(len(expected) == 46, 'Reviewed payload count')
    payloads = []
    with zipfile.ZipFile(io.BytesIO(archive.read_bytes())) as z:
        infos = z.infolist()
        require(len(infos) == 47 and len({x.filename for x in infos}) == 47 and {x.filename for x in infos} == set(expected) | {'PACKAGE_MANIFEST.json'}, 'Exact archive inventory')
        require(z.read('PACKAGE_MANIFEST.json') == pm_bytes, 'Published package manifest')
        for info in infos:
            name = info.filename
            parts = PurePosixPath(name)
            mode = info.external_attr >> 16
            require(not parts.is_absolute() and '..' not in parts.parts and not info.is_dir() and not stat.S_ISLNK(mode) and not info.flag_bits & 1, 'Archive member path/mode')
            if name == 'PACKAGE_MANIFEST.json':
                continue
            entry = expected[name]
            require(info.file_size == entry['bytes'], 'Archive expanded size')
            body = z.read(info)
            require(sha(body) == entry['sha256'] and body == (D / name).read_bytes(), 'Published logical payload: ' + name)
            local = OUT / 'extracted' / name
            local.parent.mkdir(parents=True, exist_ok=True)
            local.write_bytes(body)
            payloads.append({'relative_path': name, 'transport': 'zip_member', 'downloaded_file': pin(local),
                             'archive_file': pin(archive), 'member_path': name, 'HTTP_GET_receipt': pin(arp)})
    result = {'schema': 'pr108-actual-publication-receipt/v2', 'actual_receipt': True, 'published': True,
              'PR': 108, 'problem_id': 30003996, 'original_head': pm['original_head'],
              'effective_proof_sha256': pm['effective_proof_sha256'], 'package_manifest_sha256': sha(pm_bytes),
              'DOI': DOI, 'record_url': 'https://zenodo.org/records/' + str(ID),
              **record_receipt, 'metadata_response': pin(record_file), 'metadata_HTTP_GET_receipt': pin(record_receipt_file),
              'metadata_exact_after_documented_public_schema_mapping': True,
              'public_schema_mapping': {'resource_type.type': 'upload_type', 'resource_type.subtype': 'publication_type', 'license.id': 'license'},
              'kit_metadata_normalizations': normalizations,
              'individual_upload_downloads': [{'file': name, 'body': pin(t[0]), 'HTTP_GET_receipt': pin(t[1])} for name, t in transports.items()],
              'payload_readbacks': payloads, 'logical_payload_count': len(payloads), 'archive_member_count': 47,
              'verification_completed_UTC': now(), 'actual_publish_command': pin(A / 'actual_operations/zenodo_publication_v2_publish/execution.json')}
    write_json(A / 'ROOT_ACTUAL_PUBLICATION_RECEIPT_20261006.json', result)
    print(json.dumps({'published': True, 'DOI': DOI, 'logical_payloads_verified': len(payloads), 'both_uploaded_files_byte_identical': True, 'public_metadata_exact': True}))

if __name__ == '__main__':
    main()
