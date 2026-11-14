"""Read-only exact custody, native-schema and recursive-archive verifier.

No source programs, network, installs, file writes or mathematical sampling.
All predicates remain active under optimized Python. Mathematical proof is in
DERIVATION.md and the immutable early reconstruction.
"""
from pathlib import Path, PurePosixPath
import copy
import hashlib
import io
import json
import stat
import sys
import zipfile

O=Path(__file__).resolve().parent
S=O.parents[1]/'sources'
PINS={'SOURCE_READY.json':'ccc7a9bd68b205f78886fbd51a84cfe4f6aa768d154d82f802918889cd9f6828',
 'SOURCE_READY_MANIFEST.json':'0dc2e9d5ac2c89f033ba18522eba92067c3a5422495af90bae644362eccbef3f',
 'SOURCE_READY_SEAL.json':'bd759f183997313109e614402cdd3a40fc155fe3e0148d3e7579a899d779d5bf'}


def require(ok, tag):
    if not ok:
        raise ValueError(tag)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def check_binding(entry):
    b=Path(entry['path']).read_bytes()
    require(len(b)==entry['bytes'] and sha(b)==entry['SHA256'],
            'immutable binding '+entry['path'])


def contract(ready,raw,normalized):
    require('all_assets_in_original_order' in ready, 'literal native schema')
    require(ready['record_id']==raw['id']==23383952, 'record identity')
    require(ready['version_field_present'] is True and ready['version']=='1.0.0', 'exact version')
    require(ready['publication_date']=='2026-10-13', 'declared date')
    require(ready['created']=='2026-10-15T04:00:37.039113+00:00', 'creation date')
    require(ready['updated']=='2026-10-15T04:00:37.346451+00:00', 'updated date')
    assets=ready['all_assets_in_original_order']
    require(len(assets)==2, 'complete native assets')
    require([a['original_api_file_object'] for a in assets]==raw['files'], 'whole native objects and order')
    require([a['original_api_file_object']['key'] for a in assets]==[
      'weighted-yamabe-heat-trace-note.pdf','weighted-yamabe-heat-trace-verification.zip'], 'PDF then ZIP')
    require(normalized['all_original_API_file_objects_in_original_order']==raw['files'], 'normalized whole native objects')
    require(normalized['metadata']==raw['metadata'], 'complete original metadata')
    require(normalized['all_assets']==assets, 'whole original asset receipts')
    require(raw['metadata']['version']==ready['version'] and raw['metadata']['publication_date']==ready['publication_date'], 'API version/date')
    require(raw['created']==ready['created'] and raw['updated']==ready['updated'], 'API exact timestamps')
    for a in assets:
        api=a['original_api_file_object']
        require(api['size']==a['bytes'] and api['checksum']=='md5:'+a['md5'], 'native size/checksum case')
        require(Path(a['path'])==S/api['key'], 'actual original asset path')
    reader=ready['selected_actual_PDF']
    require(reader==ready['actual_standalone_readers'][0], 'whole actual reader selection')
    require(reader['pages']==4 and reader['path']==assets[0]['path'] and reader['sha256']==assets[0]['sha256'], 'actual4pp reader')
    require(ready['archive_containers']==4 and ready['nested_archives']==3 and ready['safe_regular_occurrences']==142, 'complete recursive inventory')


def negatives(ready,raw,norm):
    trials=[]
    a=copy.deepcopy(ready);a['version']='1.0';trials.append(('version',a))
    a=copy.deepcopy(ready);a['publication_date']='2026-10-15';trials.append(('declaration versus creation',a))
    a=copy.deepcopy(ready);a['all_assets_in_original_order'].reverse();trials.append(('native order',a))
    a=copy.deepcopy(ready);a['all_assets']=a.pop('all_assets_in_original_order');trials.append(('schema alias',a))
    a=copy.deepcopy(ready);a['all_assets_in_original_order'][0]['original_api_file_object']['checksum']='MD5:'+a['all_assets_in_original_order'][0]['md5'];trials.append(('checksum case',a))
    a=copy.deepcopy(ready);a['selected_actual_PDF']['pages']=5;trials.append(('reader identity',a))
    a=copy.deepcopy(ready);a['nested_archives']=0;trials.append(('omitted nested archives',a))
    rejected=[]
    for name,a in trials:
        try:
            contract(a,raw,norm)
        except (ValueError,KeyError):
            rejected.append(name)
        else:
            raise ValueError('false acceptance '+name)
    return rejected


def recursive_zip(inventory):
    members={(m['container'],m['original_member_name']):m for m in inventory['members']}
    containers={c['container']:c for c in inventory['archive_containers']}
    total=[0,0,0]
    def visit(data,name,depth):
        require(depth<=3, 'bounded archive depth')
        c=containers[name]
        require(sha(data)==c['sha256'] and len(data)==c['bytes'], 'exact original archive container')
        total[0]+=1;seen=set()
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            for item in z.infolist():
                path=PurePosixPath(item.filename)
                require(not path.is_absolute() and '..' not in path.parts and '\\' not in item.filename, 'safe archive path')
                canonical='/'.join(path.parts)
                require(canonical not in seen, 'unique canonical archive path');seen.add(canonical)
                require(not item.flag_bits&1, 'no encrypted payload')
                mode=item.external_attr>>16
                require(not stat.S_ISLNK(mode), 'no archive symlink')
                if item.is_dir():
                    continue
                require(stat.S_IFMT(mode) in (0,stat.S_IFREG), 'regular archive payload')
                b=z.read(item)  # CRC checked by zipfile.
                total[1]+=1;total[2]+=len(b)
                require(total[2]<5_000_000, 'bounded total expansion')
                m=members[(name,item.filename)]
                require(len(b)==m['bytes'] and sha(b)==m['sha256'], 'member size/hash')
                require(f'{item.CRC:08x}'==m['CRC32'], 'member literal CRC')
                require(Path(m['extracted_path']).read_bytes()==b, 'original complete extraction')
                if m['nested_archive_kind'] is not None:
                    require(m['nested_archive_kind']=='zip', 'recognized original nested type')
                    visit(b,name+'::'+item.filename,depth+1)
    name='weighted-yamabe-heat-trace-verification.zip'
    visit((S/name).read_bytes(),name,0)
    require(total==[4,142,928042], 'whole recursive archive census')
    return total


def main():
    for name,pin in PINS.items():
        require(sha((S/name).read_bytes())==pin, 'pinned ready envelope')
    inputs=json.loads((O/'INPUT_BINDINGS.json').read_text());count=0
    for group in inputs['groups'].values():
        for b in group:
            check_binding(b);count+=1
    ready=json.loads((S/'SOURCE_READY.json').read_text());raw=json.loads((S/'record.raw.json').read_text());norm=json.loads((S/'normalized-metadata.json').read_text())
    contract(ready,raw,norm)
    for asset in ready['all_assets_in_original_order']:
        data=Path(asset['path']).read_bytes()
        require(len(data)==asset['bytes'] and sha(data)==asset['sha256'] and hashlib.md5(data).hexdigest()==asset['md5'], 'whole API asset bytes')
    receipts=json.loads((S/'api-receipts.json').read_text())
    require(len(receipts)==5, 'five actual source transports')
    for r in receipts:
        require(r['HTTP_status']==200 and r['fresh_ordinary_HTTPS'] is True, 'recorded actual transport')
        require(isinstance(r['response_headers_in_received_order'],list), 'whole ordered headers')
        data=Path(r['body']['path']).read_bytes()
        require(sha(data)==r['body']['sha256'] and len(data)==r['body']['bytes'], 'transport exact original body')
    census=recursive_zip(json.loads((S/'archive-members.json').read_text()))
    from pypdf import PdfReader
    require(len(PdfReader(ready['selected_actual_PDF']['path']).pages)==4, 'actual reader page count')
    require((S/'published-source/note.pdf').read_bytes()==Path(ready['selected_actual_PDF']['path']).read_bytes(), 'embedded reader byte identity')
    for b in json.loads((O/'EARLY_MANIFEST.json').read_text())['files']:
        check_binding(b)
    require(sha((O/'EARLY_MANIFEST.json').read_bytes())==json.loads((O/'EARLY_SEAL.json').read_text())['manifest_SHA256'], 'immutable early seal')
    rejected=negatives(ready,raw,norm);owned=0
    if (O/'FINAL_MANIFEST.json').exists():
        for b in json.loads((O/'FINAL_MANIFEST.json').read_text())['files']:
            data=(O/b['path']).read_bytes()
            require(len(data)==b['bytes'] and sha(data)==b['SHA256'], 'immutable final '+b['path']);owned+=1
        require(sha((O/'FINAL_MANIFEST.json').read_bytes())==json.loads((O/'FINAL_SEAL.json').read_text())['manifest_SHA256'], 'immutable final seal')
    return {'status':'PASS','optimization':sys.flags.optimize,'source_ready_original_files':len(inputs['groups']['source_ready_originals']),
      'external_and_cache_bindings':count,'owned_final_files':owned,'recursive_ZIP_containers':census[0],
      'regular_payload_occurrences':census[1],'expanded_bytes':census[2],
      'in_memory_changed_custody_contracts_rejected':rejected,'read_only':True,
      'arithmetic_and_universal_mathematics_are_separate_from_custody':True}


if __name__=='__main__':
    print(json.dumps(main(),indent=2))
