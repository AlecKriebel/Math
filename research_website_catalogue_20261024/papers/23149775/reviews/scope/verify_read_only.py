"""Read-only, offline custody/closure verifier. Does not rerun proof campaigns."""
from pathlib import Path,PurePosixPath
import json,hashlib,zipfile,zlib,stat,sys
P=Path(__file__).resolve().parent
S=P.parent.parent/'sources'
checks=0
def ck(ok,label):
    global checks
    checks+=1
    if not ok:raise RuntimeError(label)
def sha(b):return hashlib.sha256(b).hexdigest()
def obj(p):return json.loads(p.read_text())
def bound(base,rows):
    for r in rows:
        f=base/r['path'];b=f.read_bytes()
        ck(len(b)==r['bytes'],'size '+str(f));ck(sha(b)==r['SHA256'],'hash '+str(f))
ready=obj(S/'SOURCE_READY.json');srcseal=obj(S/'SOURCE_READY_SEAL.json')
ck(sha((S/'SOURCE_READY.json').read_bytes())=='4cd6366eabab646cbb7837b7b3854cf931b3fa57fc7de0152d0ff210ab35c16a','ready pin')
ck(srcseal['SOURCE_READY_SHA256']==sha((S/'SOURCE_READY.json').read_bytes()),'source seal ready')
ck(srcseal['manifest_SHA256']==sha((S/'SOURCE_READY_MANIFEST.json').read_bytes()),'source seal manifest')
bound(S,obj(S/'SOURCE_READY_MANIFEST.json')['files'])
ck(ready['version']=='1.0' and ready['publication_date_declared']=='2026-10-04','literal version/date')
record=obj(Path(ready['native_record_body_path']))
ck(record['files']==[x['original_api_file_object'] for x in ready['all_native_assets_in_original_order']],'whole native ordered file objects')
for r in ready['all_native_assets_in_original_order']:
    b=Path(r['path']).read_bytes();native=r['original_api_file_object']
    ck(sha(b)==r['SHA256'],'native asset SHA');ck(len(b)==native['size'],'native size')
    ck('md5:'+hashlib.md5(b).hexdigest()==native['checksum'],'native MD5')
custody=obj(S/'archive-custody.json');ck(len(custody['regular_members'])==24,'all payloads')
for container in custody['containers']:
    with zipfile.ZipFile(container['source_path']) as z:
        infos=z.infolist();rows=[x for x in custody['regular_members'] if x['container']==container['container']]
        ck(len(infos)==len(rows)==24,'complete directory');ck(z.testzip() is None,'CRC test')
        ck(len({i.filename for i in infos})==len(infos),'no duplicate names')
        for i,r in zip(infos,rows):
            pp=PurePosixPath(i.filename);mode=(i.external_attr>>16)&0xffff
            ck(not pp.is_absolute() and '..' not in pp.parts and '\\' not in i.filename and '\0' not in i.filename,'safe path')
            ck(stat.S_IFMT(mode) in (0,stat.S_IFREG) and not i.is_dir(),'regular payload')
            ck(i.filename==r['original_member_name'] and infos[r['entry_ordinal']-1] is i,'original directory order')
            ck(i.CRC==int(r['CRC32'],16) and i.file_size==r['declared_uncompressed_bytes'] and i.compress_size==r['compressed_bytes'],'native zip sizes/CRC')
            ck(i.flag_bits==r['flag_bits'] and i.compress_type==r['compression_method'] and list(i.date_time)==r['date_time'],'zip flags/time')
            ck(i.external_attr==r['external_attr'] and i.create_system==r['create_system'] and i.extra.hex()==r['extra_hex'] and i.comment.hex()==r['comment_hex'],'zip opaque directory fields')
            b=z.read(i);ck(sha(b)==r['SHA256'],'member SHA');ck(zlib.crc32(b)&0xffffffff==i.CRC,'member CRC')
            ck(b==Path(r['extracted_path']).read_bytes(),'extracted original bytes')
            ck(not b.startswith((b'PK\x03\x04',b'\x1f\x8b',b'BZh',b'\xfd7zXZ\x00',b'7z\xbc\xaf\x27\x1c',b'Rar!')),'no hidden nested archive')
for rid in ['23079799','23089778','23088516']:
    rr=obj(P/('cache/primary/Recent-'+rid+'.record.json'));bb=(P/('cache/primary/Recent-'+rid+'.pdf')).read_bytes()
    nf=next(x for x in rr['files'] if x['key']=='main.pdf')
    ck(bb.startswith(b'%PDF') and len(bb)==nf['size'],'recent actual PDF');ck('md5:'+hashlib.md5(bb).hexdigest()==nf['checksum'],'recent native MD5')
for name in ['original-foot','outer-foot']:
    connector=obj(P/('cache/primary/'+name+'-connector.json'))['value']['structuredContent'];b=(P/('cache/primary/'+name+'.md')).read_bytes()
    ck(b==connector['content'].encode(),'connector exact UTF8')
    ck(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==connector['sha'],'connector git blob')
ck(not (P/'cache/primary/RGK-journal.pdf').read_bytes().startswith(b'%PDF'),'HTML failure not passed off as journal')
ck((P/'cache/primary/RGK-journal-AMJ.pdf').read_bytes().startswith(b'%PDF'),'genuine journal')
for r in obj(P/'replay/RUN_RECEIPTS.json'):
    ck(r['exit_code']==0 and r['stderr_bytes']==0 and r['original_sha256_matches_copy'],'bounded replay result')
for r in obj(P/'replay/RESULT_COMPARISON.json'):
    ck((P/r['replay']).read_bytes()==Path(r['native_result']).read_bytes(),'native result actual byte comparison')
own=obj(P/'independent_checks.json');ck(own['status']=='PASS' and own['exact_zero_checks']==36,'own exact result')
ck(all(r['residual']=='0' for r in own['records']),'all explicit exact residuals')
initial=obj(P/'INITIAL_SEAL.json')
# Full initial object is itself bound by the input and final owned manifests.
ck(sha((P/'INITIAL_SEAL.json').read_bytes())=='23aff14861098fefd279847275aa25cfc6785da1f0aa03278017d3f0d33d4d84','initial seal immutable')
ck(sha((P/'INITIAL_RECONSTRUCTION.md').read_bytes())=='64ba00c622762747436650f04e3c5ad54e28290cb00500f2ef7e9c810d2236a3','initial reconstruction immutable')
if (P/'INPUT_MANIFEST.json').exists():bound(Path('/'),obj(P/'INPUT_MANIFEST.json')['files'])
if (P/'OWNED_MANIFEST.json').exists():
    owned=obj(P/'OWNED_MANIFEST.json')['files'];bound(P,owned)
    actual={str(f.relative_to(P)) for f in P.rglob('*') if f.is_file() and f.name not in ['OWNED_MANIFEST.json','SEAL.json']}
    ck(actual=={r['path'] for r in owned},'complete owned file inventory')
sealed=(P/'SEAL.json').exists()
if sealed:
    for name,h in obj(P/'SEAL.json')['bound_files_SHA256'].items():ck(sha((P/name).read_bytes())==h,'final seal '+name)
print(json.dumps({'status':'PASS','checks':checks,'sealed':sealed,'mode':'offline read-only bytes/native schemas/ordered objects/ZIP directory and stored-result closure; no network, campaign execution, source edits or publication'},indent=2))
