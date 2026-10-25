"""Read-only custody verifier. No download, source repair or archive execution.

The root-known FINAL_SEAL hash is the external authenticity anchor. This
programme verifies its manifest and all bound payloads and original schemas.
Use --self-check for in-memory changed-byte/object/order rejection controls.
"""
from pathlib import Path
from hashlib import sha256, md5
import json
import sys
import zipfile
import zlib
import copy

O=Path(__file__).resolve().parent
S=O.parents[1]/'sources'

def require(c,msg):
    if not c:
        raise RuntimeError(msg)

def data_hash(data):
    return sha256(data).hexdigest()

def checked(row,base=None):
    path=Path(row['path'])
    if not path.is_absolute():
        require(base is not None,'relative path without base')
        path=base/path
    data=path.read_bytes()
    digest=row['SHA256'] if 'SHA256' in row else row['sha256']
    require(len(data)==row['bytes'] and data_hash(data)==digest,'binding changed: '+str(path))
    return data

def native_objects(record,ready):
    originals=[r['original_api_file_object'] for r in ready['all_assets']]
    require(record['files']==originals,'native API file objects or order changed')
    require(record['metadata']['version']==ready['version']=='1.0.0','API version changed')
    require(record['created']==ready['created'] and record['updated']==ready['updated'],'record dates changed')
    for a in ready['all_assets']:
        data=Path(a['path']).read_bytes();obj=a['original_api_file_object']
        require(len(data)==obj['size']==a['bytes'],'native size changed')
        require('md5:'+md5(data).hexdigest()==obj['checksum'],'native MD5 changed')
        require(data_hash(data)==a['sha256'],'actual SHA256 changed')

def main():
    seal=json.loads((O/'FINAL_SEAL.json').read_text())
    require(seal['status']=='IMMUTABLE_COMPLETE_SOURCE_SCOPE_PACKET','seal status')
    mdata=checked(seal['manifest'],O)
    manifest=json.loads(mdata)
    for r in manifest['files']:
        checked(r,O)
    inputs=json.loads((O/'INPUT_BINDINGS.json').read_text())
    for r in inputs['source_files']+inputs['borrowed_original_inputs']:
        checked(r)
    cache=json.loads((O/'CACHE_BINDINGS.json').read_text())
    for r in cache['files']:
        checked(r)
    original=json.loads((S/'SOURCE_READY_MANIFEST.json').read_text())
    for r in original['files']:
        checked(r,S)
    early=json.loads((O/'EARLY_MANIFEST.json').read_text())
    for r in early['files']:
        checked(r,O)
    require(data_hash((O/'EARLY_MANIFEST.json').read_bytes())=='facfa38bf9911d1b49e5ed5ad1e8a03e14004084520e3bc80c56bd957180db7d','independent early manifest')
    require(data_hash((O/'EARLY_SEAL.json').read_bytes())=='a26bbf990c59b9d7855de67d6bc5cf4f9067a68c06c6cdbe8a649ea831b33178','independent early seal')
    ready=json.loads((S/'SOURCE_READY.json').read_text());record=json.loads((S/'record.raw.json').read_text())
    native_objects(record,ready)
    arc=json.loads((S/'archive-members.json').read_text());member_count=0
    for c in arc['all_containers']:
        rows=[r for r in arc['members'] if r['container']==c['container']]
        with zipfile.ZipFile(S/c['container']) as z:
            regular=[i for i in z.infolist() if not i.is_dir()]
            require(len(regular)==len(rows),'archive member count')
            for info,r in zip(regular,rows):
                require(info.filename==r['member'],'archive member order/name')
                data=z.read(info)
                require(data_hash(data)==r['sha256'] and len(data)==r['bytes'],'archive payload')
                require(f'{zlib.crc32(data)&0xffffffff:08x}'==r['CRC32'],'archive CRC')
                require(Path(r['extracted_path']).read_bytes()==data,'archive extraction')
                member_count+=1
    require(member_count==118,'complete regular source members')
    verdict=json.loads((O/'VERDICT.json').read_text())
    require(verdict['assignment_status']=='COMPLETE' and verdict['completion_percent']==100,'completion')
    require(verdict['human_peer_review'] is False and verdict['formal_certification'] is False and verdict['publication_clearance'] is False and verdict['root_authority_retained'] is True,'authority limits')
    rejected=[]
    if '--self-check' in sys.argv:
        original_pdf=Path(ready['selected_readers'][0]['published']['path']).read_bytes()
        require(data_hash(original_pdf)!=data_hash(original_pdf[:-1]+bytes([original_pdf[-1]^1])),'changed byte rejection')
        rejected.append('single changed PDF byte: SHA256 rejection without writing')
        for label,mutate in [
            ('native object key deletion',lambda x:x['files'][0].pop('id')),
            ('native asset order reversal',lambda x:x['files'].reverse()),
            ('native checksum case change',lambda x:x['files'][0].__setitem__('checksum',x['files'][0]['checksum'].upper())),
            ('API version replacement',lambda x:x['metadata'].__setitem__('version','1.0')),
            ('creation timestamp replacement',lambda x:x.__setitem__('created','2026-09-05'))]:
            mutant=copy.deepcopy(record);mutate(mutant)
            try:
                native_objects(mutant,ready)
            except (RuntimeError,KeyError):
                rejected.append(label)
            else:
                raise RuntimeError('mutation falsely accepted: '+label)
    print(json.dumps({'status':'PASS','owned_files':len(manifest['files']),'frozen_source_files':len(inputs['source_files']),'borrowed_original_inputs':len(inputs['borrowed_original_inputs']),'ignored_cache_bindings':len(cache['files']),'original_ZIP_regular_members':member_count,'in_memory_rejection_controls':rejected,'source_execution':False,'writes':False},indent=2))

if __name__=='__main__':
    main()
