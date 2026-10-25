"""Read-only verification of this complete analytic packet and original inputs.

Root's independently recorded FINAL_SEAL SHA256 is the external anchor. This
programme never writes, downloads or executes any archived mathematical code.
"""
from pathlib import Path
from hashlib import sha256,md5
import json,zipfile,zlib,sys,copy

O=Path(__file__).resolve().parent
S=O.parents[1]/'sources'

def require(c,message):
    if not c:raise RuntimeError(message)

def H(data):return sha256(data).hexdigest()

def check(row,base=None):
    p=Path(row['path'])
    if not p.is_absolute():
        require(base is not None,'relative binding needs base')
        p=base/p
    data=p.read_bytes();digest=row['SHA256'] if 'SHA256' in row else row['sha256']
    require(len(data)==row['bytes'] and H(data)==digest,'binding changed: '+str(p))
    return data

def native(record,ready):
    require(record['files']==[a['original_api_file_object'] for a in ready['all_assets']],'whole native API objects/order changed')
    require(record['metadata']['version']==ready['version']=='1.0','version changed')
    require(record['created']==ready['created'] and record['updated']==ready['updated'],'source dates changed')
    for a in ready['all_assets']:
        d=Path(a['path']).read_bytes();f=a['original_api_file_object']
        require(len(d)==f['size']==a['bytes'],'native size')
        require('md5:'+md5(d).hexdigest()==f['checksum'],'native checksum case/content')
        require(H(d)==a['sha256'],'actual SHA256')

def main():
    seal=json.loads((O/'FINAL_SEAL.json').read_text())
    require(seal['status']=='IMMUTABLE_COMPLETE_ANALYTIC_PACKET','seal status')
    manifest=json.loads(check(seal['manifest'],O))
    for row in manifest['files']:check(row,O)
    inputs=json.loads((O/'INPUT_BINDINGS.json').read_text())
    for key in ['source_files','additive_source_final_controls','original_primary_bodies','original_primary_receipts_and_publisher_metadata']:
        for row in inputs[key]:check(row)
    cache=json.loads((O/'CACHE_BINDINGS.json').read_text())
    for row in cache['files']:check(row)
    for n,h in [('SOURCE_READY_MANIFEST.json','427d17a871bae870139756077ec84c31c8bbd9a2037d3f7c12850f3587784669'),
                ('SOURCE_READY_SEAL.json','63049ed28a1f1070c5030b4009aa79ecee6b339a9a1cfb114bbfe058b242f1f6')]:
        require(H((S/n).read_bytes())==h,'original ready control changed')
    for row in json.loads((S/'SOURCE_READY_MANIFEST.json').read_text())['files']:check(row,S)
    for n,h in [('EARLY_MANIFEST.json','0705cbc62ccb2159b72b1f6f6593d129e483b4b5cae2fb5bed8f72c7d22ca775'),
                ('EARLY_SEAL.json','dd3e40ed8cfe2531485114d210e1a1e12a024e4884d996265992163cbcadae92')]:
        require(H((O/n).read_bytes())==h,'early control changed')
    for row in json.loads((O/'EARLY_MANIFEST.json').read_text())['files']:check(row)
    ready=json.loads((S/'SOURCE_READY.json').read_text());record=json.loads((S/'record.raw.json').read_text());native(record,ready)
    arc=json.loads((S/'archive-members.json').read_text());member_count=0
    for container in arc['archive_containers']:
        rows=[r for r in arc['members'] if r['container']==container['container']]
        with zipfile.ZipFile(S/container['container']) as z:
            regular=[i for i in z.infolist() if not i.is_dir()]
            require(len(regular)==len(rows),'archive member count')
            for info,row in zip(regular,rows):
                require(info.filename==row['member'],'archive member name/order')
                d=z.read(info)
                require(H(d)==row['sha256'] and len(d)==row['bytes'],'archive payload')
                require(f'{zlib.crc32(d)&0xffffffff:08x}'==row['CRC32'],'archive CRC')
                require(Path(row['extracted_path']).read_bytes()==d,'archive extraction')
                member_count+=1
    require(member_count==13,'all original regular members')
    require((O/'independent-exact-controls.json').read_bytes()==(O/'independent-exact-controls.optimized.json').read_bytes(),'normal/optimized exact result differs')
    verdict=json.loads((O/'VERDICT.json').read_text())
    require(verdict['assignment_status']=='COMPLETE' and verdict['completion_percent']==100,'completion')
    require(verdict['human_peer_review'] is False and verdict['formal_certification'] is False and verdict['publication_clearance'] is False and verdict['root_authority_retained'] is True,'authority limits')
    rejected=[]
    if '--self-check' in sys.argv:
        d=(S/'mtp2-edge-closure-note.pdf').read_bytes()
        require(H(d)!=H(d[:-1]+bytes([d[-1]^1])),'changed-byte control')
        rejected.append('changed PDF byte hash')
        for label,mutate in [
            ('native object deletion',lambda r:r['files'][0].pop('id')),
            ('native asset order reversal',lambda r:r['files'].reverse()),
            ('native checksum case alteration',lambda r:r['files'][0].__setitem__('checksum',r['files'][0]['checksum'].upper())),
            ('API version alteration',lambda r:r['metadata'].__setitem__('version','1.0.0')),
            ('API creation date truncation',lambda r:r.__setitem__('created','2026-10-04'))]:
            x=copy.deepcopy(record);mutate(x)
            try:native(x,ready)
            except (RuntimeError,KeyError):rejected.append(label)
            else:raise RuntimeError('false accept: '+label)
    print(json.dumps({'status':'PASS','owned_files':len(manifest['files']),'frozen_ready_source_bindings':len(inputs['source_files']),
                      'additive_source_final_controls':len(inputs['additive_source_final_controls']),
                      'original_primary_bodies':len(inputs['original_primary_bodies']),'primary_receipts_metadata':len(inputs['original_primary_receipts_and_publisher_metadata']),
                      'ignored_cache_bindings':len(cache['files']),'source_ZIP_members':member_count,'in_memory_rejections':rejected,
                      'writes':False,'release_program_execution':False},indent=2))

if __name__=='__main__':main()
