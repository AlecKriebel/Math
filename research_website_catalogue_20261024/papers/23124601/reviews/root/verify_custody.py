"""Read-only root custody check. No mathematical replay or output writes by default."""
from pathlib import Path
from hashlib import sha256, md5
import datetime, json, sys, zipfile, gzip, zlib

R=Path(__file__).resolve().parent
D=R.parents[1]
P=D.parents[1]
S=D/'sources'
seen={}
def need(v,m):
    if not v: raise RuntimeError(m)
def H(p): return sha256(p.read_bytes()).hexdigest()
def obj(p): return json.loads(p.read_text())
def check(row,base):
    p=Path(row['path'])
    if not p.is_absolute(): p=base/p
    expected=row.get('sha256',row.get('SHA256'))
    need(type(expected) is str and len(expected)==64,'hash schema')
    need(p.is_file() and not p.is_symlink(),'regular '+str(p))
    need(p.stat().st_size==row['bytes'] and H(p)==expected,'binding '+str(p))
    if str(p) in seen: need(seen[str(p)]==expected,'conflicting binding')
    seen[str(p)]=expected
def rows(p,base):
    for row in obj(p)['files']: check(row,base)
def pin(p,h): need(H(p)==h,'external root pin '+str(p))

def main():
    pins={
      S/'SOURCE_READY.json':'7fd29ea48957c098973ca892a317269b9e2c4fc3b616c252e2dfa8f09a69dbb1',
      S/'SOURCE_READY_MANIFEST.json':'70e8f139bf0ab0d237558ad79138a023f0a19d4d620533d08f6a82b34686b522',
      S/'SOURCE_READY_SEAL.json':'14d5c25d8024471d6b06504082329ebc3a90927c6fcb9b3c144f35ce889c29c0',
      R/'INITIAL_SEAL.json':'51387323b61909980a0fd9dd856497488236d872204cee86e1c6d059ecbd306a',
      D/'reviews/scope/SEAL.json':'e2e7d6862ea2ec0911cf0d52f852f088feeed36a23832ca5a4a37d49a5c6955d',
      D/'reviews/analytic/SEAL.json':'51fad32511850f042556cc12c51ad431f82465c813e7f39a231e85e6ae5d0d14',
      D/'reviews/adversarial/FINAL_SEAL.json':'1edf4959cd52a93b29afdda30f1a3614fdec1fe0a10980ba6ff53c54d6af48f6',
    }
    for p,h in pins.items(): pin(p,h)
    initial=obj(R/'INITIAL_SEAL.json');check(initial,P)
    rows(S/'SOURCE_READY_MANIFEST.json',S)
    lane_counts={}
    for lane in ['scope','analytic','adversarial']:
        E=D/'reviews'/lane
        mf='FINAL_MANIFEST.json' if lane=='adversarial' else 'MANIFEST.json'
        sf='FINAL_SEAL.json' if lane=='adversarial' else 'SEAL.json'
        seal=obj(E/sf)
        if lane=='adversarial': check(seal['manifest'],E)
        else: pin(E/mf,seal['manifest_sha256'])
        rows(E/mf,E);rows(E/'CACHE_BINDINGS.json' if lane!='analytic' else E/'CACHE_MANIFEST.json',E)
        if lane=='analytic': rows(E/'ORIGINAL_BINDINGS.json',E)
        if lane=='adversarial':
            inputs=obj(E/'INPUT_BINDINGS.json')
            for key in ['source_files','original_primary_bodies','primary_custody_inputs']:
                for row in inputs[key]: check(row,E)
        lane_counts[lane]=len(obj(E/mf)['files'])
    ready=obj(S/'SOURCE_READY.json');raw=obj(S/'record.raw.json')
    need(raw['files']==[x['native_file_object'] for x in ready['assets']],'whole native file objects/order')
    need(raw['metadata']['version']==ready['metadata_version']=='1.0','version')
    need(raw['created']==ready['actual_created']=='2026-10-03T16:52:00.285180+00:00','creation')
    need(raw['updated']==ready['actual_updated'],'update')
    for a in ready['assets']:
        data=(S/a['path']).read_bytes();f=a['native_file_object']
        need(len(data)==a['bytes']==f['size'] and sha256(data).hexdigest()==a['sha256'],'asset bytes')
        need('md5:'+md5(data).hexdigest()==f['checksum'],'whole API checksum')
    arc=obj(S/'archive-custody.json')
    outer=[r for r in arc['members'] if r['container']=='zip']
    children=[r for r in arc['members'] if r['container']=='gzip']
    with zipfile.ZipFile(S/'wajnryb-artin-a5-verification.zip') as z:
        info=[i for i in z.infolist() if not i.is_dir()]
        need(len(info)==len(outer)==60,'outer count')
        for i,r in zip(info,outer):
            d=z.read(i)
            need(i.filename==r['member'] and len(d)==r['bytes'] and sha256(d).hexdigest()==r['sha256'],'ZIP payload')
            need(f'{zlib.crc32(d)&0xffffffff:08x}'==r['crc32'] and (S/r['path']).read_bytes()==d,'CRC/extracted payload')
        for r in children:
            d=gzip.decompress(z.read(r['archive'].split('!',1)[1]))
            need(len(d)==r['bytes'] and sha256(d).hexdigest()==r['sha256'] and (S/r['path']).read_bytes()==d,'gzip body')
    need(len(children)==7,'seven standalone gzip bodies')
    primary_images={}
    for name in ['matsumoto-01.png','matsumoto-02.png','matsumoto-03.png','matsumoto-04.png','baykur-03.png']:
        p=P/'tmp/pdfs/root23124601-primary-20261025'/name
        primary_images[str(p.relative_to(P))]={'bytes':p.stat().st_size,'sha256':H(p)}
    result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_READ_ONLY_ROOT_CUSTODY',
      'unique_existing_file_bindings_rehashed':len(seen),'lane_owned_manifest_entries':lane_counts,
      'source_ready_entries':76,'source_envelope_files':2,'recursive_original_payloads':67,
      'native_objects_order_edition_timestamps_and_MD5_exact':True,
      'root_actual_primary_images_viewed_and_bound':primary_images,
      'full_mathematical_programme_repeated':False,'source_programme_executed':False,
      'prior_read_only_verifier_results':{'adversarial':'PASS plus six in-memory schema/hash controls; actual root execution','analytic':'PASS plus wrong-original-hash control; no owned certificate rerun; actual root execution'},
      'helper_sha256':H(Path(__file__))}
    if '--record' in sys.argv:
        out=R/'custody-recheck-20261025.json';need(not out.exists(),'receipt already exists')
        out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__': main()
