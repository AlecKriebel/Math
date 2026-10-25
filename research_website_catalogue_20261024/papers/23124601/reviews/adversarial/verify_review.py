"""Read-only custody verification; no large mathematical replay or source writes.

Root-known FINAL_SEAL hash is the external anchor. All actual source objects,
original data, early objects, primary bodies and own artifacts are rehashed.
"""
from pathlib import Path
from hashlib import sha256,md5
import json,zipfile,gzip,zlib,copy,sys

O=Path(__file__).resolve().parent
S=O.parents[1]/'sources'
def req(c,why):
    if not c:raise RuntimeError(why)
def H(data):return sha256(data).hexdigest()
def check(row,base=None):
    p=Path(row['path'])
    if not p.is_absolute():
        req(base is not None,'relative path base');p=base/p
    data=p.read_bytes();digest=row['SHA256'] if 'SHA256' in row else row['sha256']
    req(len(data)==row['bytes'] and H(data)==digest,'changed binding '+str(p))
    return data
def native(record,ready):
    req(record['files']==[a['native_file_object'] for a in ready['assets']],'native object/order')
    req(record['metadata']['version']==ready['metadata_version']=='1.0','native version')
    req(record['created']==ready['actual_created'] and record['updated']==ready['actual_updated'],'native dates')
    for a in ready['assets']:
        data=(S/a['path']).read_bytes();f=a['native_file_object']
        req(len(data)==a['bytes']==f['size'],'native assetsize')
        req('md5:'+md5(data).hexdigest()==f['checksum'],'native checksum case/content')
        req(H(data)==a['sha256'],'actual SHA256')
def main():
    seal=json.loads((O/'FINAL_SEAL.json').read_text())
    req(seal['status']=='IMMUTABLE_COMPLETE_ADVERSARIAL_PACKET','seal status')
    manifest=json.loads(check(seal['manifest'],O))
    for r in manifest['files']:check(r,O)
    inputs=json.loads((O/'INPUT_BINDINGS.json').read_text())
    for key in ['source_files','original_primary_bodies','primary_custody_inputs']:
        for r in inputs[key]:check(r)
    cache=json.loads((O/'CACHE_BINDINGS.json').read_text())
    for r in cache['files']:check(r)
    for name,digest in [('SOURCE_READY_MANIFEST.json','70e8f139bf0ab0d237558ad79138a023f0a19d4d620533d08f6a82b34686b522'),
                        ('SOURCE_READY_SEAL.json','14d5c25d8024471d6b06504082329ebc3a90927c6fcb9b3c144f35ce889c29c0')]:
        req(H((S/name).read_bytes())==digest,'source ready control')
    for r in json.loads((S/'SOURCE_READY_MANIFEST.json').read_text())['files']:check(r,S)
    for name,digest in [('EARLY_MANIFEST.json','12d18d98fc8d9c5551eacdfd7098ad3396327311f891f261abaf9abea597f955'),
                        ('EARLY_SEAL.json','ac4910297f6b65c0f57d4dc3ec03d75b2d3c3b3f2770382bd69ee508c352ad55')]:
        req(H((O/name).read_bytes())==digest,'independent early control')
    for r in json.loads((O/'EARLY_MANIFEST.json').read_text())['files']:check(r)
    ready=json.loads((S/'SOURCE_READY.json').read_text());record=json.loads((S/'record.raw.json').read_text());native(record,ready)
    arc=json.loads((S/'archive-custody.json').read_text());outer=[r for r in arc['members'] if r['container']=='zip'];children=[r for r in arc['members'] if r['container']=='gzip']
    with zipfile.ZipFile(S/'wajnryb-artin-a5-verification.zip') as z:
        info=[i for i in z.infolist() if not i.is_dir()];req(len(info)==len(outer)==60,'outer regular count')
        for i,r in zip(info,outer):
            req(i.filename==r['member'],'member order/name');d=z.read(i)
            req(len(d)==r['bytes'] and H(d)==r['sha256'] and f'{zlib.crc32(d)&0xffffffff:08x}'==r['crc32'],'zip payload')
            req((S/r['path']).read_bytes()==d,'zip extracted payload')
        for r in children:
            d=gzip.decompress(z.read(r['archive'].split('!',1)[1]))
            req(len(d)==r['bytes'] and H(d)==r['sha256'] and (S/r['path']).read_bytes()==d,'gzip payload')
    req(len(children)==7,'gzip count')
    result=json.loads((O/'CERTIFICATE_CHECKS.json').read_text())
    req(result['length20']['full_original_action_records_checked']==810 and result['length30']['coaccessible_edges_full_literal_checked']==261810,'full mathematical audit record')
    verdict=json.loads((O/'VERDICT.json').read_text())
    req(verdict['assignment_status']=='COMPLETE' and verdict['completion_percent']==100,'completion')
    req(verdict['human_peer_review'] is False and verdict['formal_certification'] is False and verdict['publication_clearance'] is False and verdict['root_authority_retained'] is True,'authority limits')
    rejected=[]
    if '--self-check' in sys.argv:
        d=(S/'fixed_generator_classification.pdf').read_bytes();req(H(d)!=H(d[:-1]+bytes([d[-1]^1])),'changed byte rejection');rejected.append('changed PDF byte hash')
        for label,mutate in [('native id removal',lambda x:x['files'][0].pop('id')),
                             ('native order reversal',lambda x:x['files'].reverse()),
                             ('native checksum case change',lambda x:x['files'][0].__setitem__('checksum',x['files'][0]['checksum'].upper())),
                             ('native version change',lambda x:x['metadata'].__setitem__('version','1.0.0')),
                             ('native timestamp truncation',lambda x:x.__setitem__('created','2026-10-03'))]:
            x=copy.deepcopy(record);mutate(x)
            try:native(x,ready)
            except (RuntimeError,KeyError):rejected.append(label)
            else:raise RuntimeError('false accept '+label)
    print(json.dumps({'status':'PASS','owned_files':len(manifest['files']),'source_bindings':len(inputs['source_files']),
                      'original_primary_PDFs':len(inputs['original_primary_bodies']),'primary_PS_receipts_conversion_inputs':len(inputs['primary_custody_inputs']),
                      'own_ignored_cache_files':len(cache['files']),'original_recursive_payloads':len(outer)+len(children),
                      'in_memory_rejections':rejected,'large_finite_audit_repeated':False,'whole_release_program_execution':False,'writes':False},indent=2))
if __name__=='__main__':main()
