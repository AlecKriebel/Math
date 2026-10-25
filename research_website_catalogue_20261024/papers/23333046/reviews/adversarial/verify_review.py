"""Read-only custody verifier. No source execution, writes, or network access.

The mathematical theorem is justified by DERIVATION.md. This verifier checks
the exact original objects/bytes, safe ZIP correspondence, and sealed evidence.
All rejection predicates remain active under -O and -OO.
"""
from pathlib import Path, PurePosixPath
import copy
import hashlib
import json
import stat
import sys
import zipfile

O = Path(__file__).resolve().parent
S = O.parents[1] / 'sources'
PINS = {
 'SOURCE_READY.json':'ef9681061855c3e1c80e1f4e9b1b9538600bb7c9b15bba18d8fd78e98c38c478',
 'SOURCE_READY_MANIFEST.json':'b680fea3ffaa1ce5f6ebf1386d70da988b39bb437d04998de90e043618bd1f05',
 'SOURCE_READY_SEAL.json':'0b47008701fdf09019ae4ae87a09d648c90992ab4253b67481ec7bd7b36d355d'}


def require(ok, tag):
    if not ok:
        raise ValueError(tag)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def binding(entry):
    data=Path(entry['path']).read_bytes()
    require(len(data)==entry['bytes'], 'binding size: '+entry['path'])
    require(sha(data)==entry['SHA256'], 'binding hash: '+entry['path'])


def ready_contract(ready, raw, normalized):
    require('all_assets_in_original_order' in ready, 'literal source schema')
    require(ready['record_id']==23333046 and raw['id']==23333046, 'record identity')
    require(ready['version_field_present'] is True and ready['version']=='1.0', 'version')
    require(ready['publication_date']=='2026-10-12', 'declared date')
    require(ready['created']=='2026-10-13T05:43:05.275367+00:00', 'creation date')
    assets=ready['all_assets_in_original_order']
    require(len(assets)==2, 'whole asset count')
    require([x['original_api_file_object'] for x in assets]==raw['files'], 'whole native file objects and order')
    require(normalized['all_original_API_file_objects_in_original_order']==raw['files'], 'normalized whole native objects')
    require(normalized['metadata']==raw['metadata'], 'complete metadata unchanged')
    require(normalized['all_assets']==assets, 'normalized complete asset receipts')
    require([x['original_api_file_object']['key'] for x in assets]==[
      'local_deformation_devissage_source_verification_v1.zip',
      'characteristic_two_counterexample_local_deformation_devissage.pdf'], 'native ZIP then PDF order')
    require(raw['metadata']['version']==ready['version'] and raw['metadata']['publication_date']==ready['publication_date'], 'API date/version exact')
    require(raw['created']==ready['created'] and raw['updated']==ready['updated'], 'API timestamps exact')
    for item in assets:
        api=item['original_api_file_object']
        require(api['size']==item['bytes'], 'native asset size')
        require(api['checksum']=='md5:'+item['md5'], 'native checksum spelling/case')
        require(Path(item['path'])==S/api['key'], 'actual source path')
    reader=ready['selected_actual_PDF']
    require(reader['pages']==5 and reader['actual_standalone_API_asset'] is True, 'actual reader selection')
    require(reader['path']==assets[1]['path'] and reader['sha256']==assets[1]['sha256'], 'reader exact asset')


def negative_contracts(ready, raw, normalized):
    mutations=[]
    a=copy.deepcopy(ready);a['version']='1.0.0';mutations.append(('version',a,raw,normalized))
    a=copy.deepcopy(ready);a['publication_date']='2026-10-13';mutations.append(('declared date',a,raw,normalized))
    a=copy.deepcopy(ready);a['all_assets_in_original_order'].reverse();mutations.append(('asset order',a,raw,normalized))
    a=copy.deepcopy(ready);a['files']=a.pop('all_assets_in_original_order');mutations.append(('schema alias',a,raw,normalized))
    a=copy.deepcopy(ready);a['all_assets_in_original_order'][0]['original_api_file_object']['checksum']='MD5:'+a['all_assets_in_original_order'][0]['md5'];mutations.append(('checksum case',a,raw,normalized))
    a=copy.deepcopy(ready);a['selected_actual_PDF']['pages']=4;mutations.append(('reader pages',a,raw,normalized))
    rejected=[]
    for name,a,b,c in mutations:
        try:
            ready_contract(a,b,c)
        except (ValueError,KeyError):
            rejected.append(name)
        else:
            raise ValueError('false acceptance: '+name)
    return rejected


def main():
    for name,pin in PINS.items():
        require(sha((S/name).read_bytes())==pin, 'pinned ready envelope: '+name)
    inputs=json.loads((O/'INPUT_BINDINGS.json').read_text())
    total=0
    for entries in inputs['groups'].values():
        for entry in entries:
            binding(entry);total+=1
    ready=json.loads((S/'SOURCE_READY.json').read_text())
    raw=json.loads((S/'record.raw.json').read_text())
    normalized=json.loads((S/'normalized-metadata.json').read_text())
    ready_contract(ready,raw,normalized)
    for asset in ready['all_assets_in_original_order']:
        data=Path(asset['path']).read_bytes()
        require(sha(data)==asset['sha256'] and len(data)==asset['bytes'], 'asset SHA/size')
        require(hashlib.md5(data).hexdigest()==asset['md5'], 'asset MD5')
    receipts=json.loads((S/'api-receipts.json').read_text())
    require(len(receipts)==5, 'five original transport receipts')
    for receipt in receipts:
        require(receipt['HTTP_status']==200 and receipt['fresh_ordinary_HTTPS'] is True,
                'actual recorded transport status')
        require(isinstance(receipt['response_headers_in_received_order'],list), 'ordered whole transport headers')
        entry=receipt['body'];data=Path(entry['path']).read_bytes()
        require(len(data)==entry['bytes'] and sha(data)==entry['sha256'], 'transport exact body')
    inventory=json.loads((S/'archive-members.json').read_text())
    by_name={m['original_member_name']:m for m in inventory['members']}
    seen=set();expanded=0;regular=0
    with zipfile.ZipFile(S/'local_deformation_devissage_source_verification_v1.zip') as archive:
        for item in archive.infolist():
            path=PurePosixPath(item.filename)
            require(not path.is_absolute() and '..' not in path.parts and '\\' not in item.filename, 'safe ZIP path')
            canonical='/'.join(path.parts)
            require(canonical not in seen, 'unique ZIP path');seen.add(canonical)
            require(not item.flag_bits&1, 'ZIP unencrypted')
            mode=item.external_attr>>16
            require(not stat.S_ISLNK(mode), 'ZIP no symlinks')
            if item.is_dir():
                continue
            require(stat.S_IFMT(mode) in (0,stat.S_IFREG), 'ZIP regular payload')
            regular+=1;expanded+=item.file_size
            require(expanded<5_000_000, 'bounded expansion')
            data=archive.read(item)  # zipfile validates the actual CRC.
            record=by_name[item.filename]
            require(sha(data)==record['sha256'] and len(data)==record['bytes'], 'ZIP member inventory bytes')
            require(f'{item.CRC:08x}'==record['CRC32'], 'ZIP CRC recorded exact')
            require(Path(record['extracted_path']).read_bytes()==data, 'complete original extraction')
    require(regular==154 and expanded==884320, 'whole ZIP count and expansion')
    require(ready['nested_archives']==0, 'no unclaimed nested archives')
    from pypdf import PdfReader
    require(len(PdfReader(ready['selected_actual_PDF']['path']).pages)==5, 'actual PDF page count')
    require((S/'published-source/local_deformation_devissage_v1/research_note.pdf').read_bytes()==Path(ready['selected_actual_PDF']['path']).read_bytes(), 'embedded PDF identical')
    require((S/'published-source/local_deformation_devissage_v1/evidence/package_review_02/research_note_review_copy.tex').read_bytes()==(S/'published-source/local_deformation_devissage_v1/research_note.tex').read_bytes(), 'duplicate TeX identical')
    early=json.loads((O/'EARLY_MANIFEST.json').read_text())
    # The early object retains its original literal shape; do not normalize it.
    for entry in early['files']:
        data=(O/entry['path']).read_bytes()
        require(len(data)==entry['bytes'] and sha(data)==entry['SHA256'], 'immutable early content')
    seal=json.loads((O/'EARLY_SEAL.json').read_text())
    require(sha((O/'EARLY_MANIFEST.json').read_bytes())==seal['manifest_SHA256'], 'early manifest seal')
    rejected=negative_contracts(ready,raw,normalized)
    owned=0
    if (O/'FINAL_MANIFEST.json').exists():
        manifest=json.loads((O/'FINAL_MANIFEST.json').read_text())
        for entry in manifest['files']:
            data=(O/entry['path']).read_bytes()
            require(len(data)==entry['bytes'] and sha(data)==entry['SHA256'], 'immutable final content: '+entry['path'])
            owned+=1
        require(sha((O/'FINAL_MANIFEST.json').read_bytes())==json.loads((O/'FINAL_SEAL.json').read_text())['manifest_SHA256'], 'final seal')
    return {'status':'PASS','optimization':sys.flags.optimize,'bound_inputs':total,
            'source_originals':len(inputs['groups']['source_ready_originals']),
            'ZIP_regular_members':regular,'expanded_bytes':expanded,
            'owned_final_files':owned,'in_memory_changed_contracts_rejected':rejected,
            'read_only':True,'mathematical_proof_not_a_custody_test':True}


if __name__=='__main__':
    print(json.dumps(main(),indent=2))
