"""Root read-only original/evidence custody. No mathematical programme replay."""
from pathlib import Path, PurePosixPath
from hashlib import sha256, md5
import datetime,json,stat,sys,zipfile
R=Path(__file__).resolve().parent;D=R.parents[1];P=D.parents[1];S=D/'sources';seen={}
def need(x,m):
    if not x:raise RuntimeError(m)
def H(p):return sha256(p.read_bytes()).hexdigest()
def obj(p):return json.loads(p.read_text())
def pin(p,h):need(H(p)==h,'external pin '+str(p))
def check(row,base):
    p=Path(row['path']);p=p if p.is_absolute() else base/p
    expected=row.get('sha256',row.get('SHA256'))
    need(p.is_file() and not p.is_symlink(),'regular '+str(p))
    need(type(row['bytes']) is int and p.stat().st_size==row['bytes'] and H(p)==expected,'binding '+str(p))
    if str(p) in seen:need(seen[str(p)]==expected,'binding conflict')
    seen[str(p)]=expected
def rows(p,base):
    for row in obj(p)['files']:check(row,base)
def main():
    pins={S/'SOURCE_READY.json':'ef9681061855c3e1c80e1f4e9b1b9538600bb7c9b15bba18d8fd78e98c38c478',S/'SOURCE_READY_MANIFEST.json':'b680fea3ffaa1ce5f6ebf1386d70da988b39bb437d04998de90e043618bd1f05',S/'SOURCE_READY_SEAL.json':'0b47008701fdf09019ae4ae87a09d648c90992ab4253b67481ec7bd7b36d355d',S/'SOURCE_FINAL_MANIFEST.json':'ef072d24156c6496476ca66f21164c5a40222f77bbfffadd129732284bb86880',S/'SOURCE_FINAL_SEAL.json':'99b77bd5786e2490f9df795aa8096860a61dd437dd23af8b6645310653e4a363',R/'INITIAL_SEAL.json':'ddaac49e5dcf9a7d712f4eda33fe4337a24d717697f97ab0fdd6c9990d160a18',D/'reviews/scope/FINAL_SEAL.json':'abff2715a0db699a7a3f3a556235502e7d1ea2c2cf7872104a3cb75329f4ee48',D/'reviews/analytic/SEAL.json':'8ca054159dfae751a443df36fdc92d302ca0ebf31856d1b7e63808df2f97adde',D/'reviews/adversarial/FINAL_SEAL.json':'cf390658d36992f27037a3e44e7342ef04e047c8992a3ad7d74dbaedc597faca'}
    for p,h in pins.items():pin(p,h)
    check(obj(R/'INITIAL_SEAL.json'),P)
    rows(S/'SOURCE_READY_MANIFEST.json',S);rows(S/'SOURCE_FINAL_MANIFEST.json',S)
    check(obj(S/'SOURCE_FINAL_SEAL.json')['manifest'],S)
    need(len(obj(S/'SOURCE_READY_MANIFEST.json')['files'])==163 and len(obj(S/'SOURCE_FINAL_MANIFEST.json')['files'])==165,'source envelopes')
    lane_counts={}
    for lane in ['scope','analytic','adversarial']:
        E=D/'reviews'/lane
        mf='MANIFEST.json' if lane=='analytic' else 'FINAL_MANIFEST.json'
        sf='SEAL.json' if lane=='analytic' else 'FINAL_SEAL.json'
        seal=obj(E/sf);pin(E/mf,seal.get('manifest_sha256',seal.get('manifest_SHA256')))
        rows(E/mf,E);lane_counts[lane]=len(obj(E/mf)['files'])
        if lane!='adversarial':rows(E/'CACHE_MANIFEST.json',E)
        if lane=='analytic':rows(E/'ORIGINAL_BINDINGS.json',E)
        if lane=='adversarial':
            for entries in obj(E/'INPUT_BINDINGS.json')['groups'].values():
                for row in entries:check(row,E)
    ready=obj(S/'SOURCE_READY.json');raw=obj(S/'record.raw.json')
    assets=ready['all_assets_in_original_order']
    need([a['original_api_file_object'] for a in assets]==raw['files'],'whole original native objects/order')
    need(raw['metadata']['version']==ready['version']=='1.0' and raw['metadata']['publication_date']==ready['publication_date']=='2026-10-12','edition/declared date')
    need(raw['created']==ready['created']=='2026-10-13T05:43:05.275367+00:00' and raw['updated']==ready['updated'],'actual timestamps')
    for a in assets:
        p=Path(a['path']);d=p.read_bytes();f=a['original_api_file_object']
        need(len(d)==a['bytes']==f['size'] and H(p)==a['sha256'],'asset SHA/size')
        need(md5(d).hexdigest()==a['md5'] and f['checksum']=='md5:'+a['md5'],'exact native MD5')
    receipts=obj(S/'api-receipts.json');need(len(receipts)==5,'five actual transports')
    for row in receipts:
        need(row['HTTP_status']==200 and row['fresh_ordinary_HTTPS'] is True,'transport status')
        check(row['body'],S)
    inventory=obj(S/'archive-members.json')['members'];by={x['original_member_name']:x for x in inventory};expanded=0;members=set()
    with zipfile.ZipFile(S/'local_deformation_devissage_source_verification_v1.zip') as z:
        need(len(z.infolist())==len(by)==154,'all archive members')
        for info in z.infolist():
            p=PurePosixPath(info.filename)
            need(not p.is_absolute() and '..' not in p.parts and '\\' not in info.filename and info.filename not in members,'safe unique archive path');members.add(info.filename)
            need(not info.is_dir() and not info.flag_bits&1 and stat.S_IFMT(info.external_attr>>16) in (0,stat.S_IFREG),'regular unencrypted archive body')
            d=z.read(info);row=by[info.filename];expanded+=len(d)
            need(sha256(d).hexdigest()==row['sha256'] and len(d)==row['bytes'] and f'{info.CRC:08x}'==row['CRC32'],'CRC/hash/size')
            need(Path(row['extracted_path']).read_bytes()==d,'existing original member exact')
    need(expanded==884320 and ready['nested_archives']==0,'whole archive census')
    need((S/'published-source/local_deformation_devissage_v1/research_note.pdf').read_bytes()==Path(ready['selected_actual_PDF']['path']).read_bytes(),'one identical embedded reader')
    result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_READ_ONLY_ROOT_CUSTODY','unique_existing_file_bindings_rehashed':len(seen),'source_ready_bindings':163,'source_final_bindings':165,'source_envelope_files':2,'lane_owned_entries':lane_counts,'original_ZIP_regular_bodies_checked':154,'expanded_original_bytes':expanded,'whole_native_order_edition_dates_MD5_and_actual_transports_exact':True,'source_or_mathematical_programme_replay':False,'root_inspected_read_only_family_verifiers_passed':['scope normal explicit PYTHONOPTIMIZE absent','analytic normal with wrong-hash control; no own replay','adversarial normal with six native changed-object controls'],'helper_sha256':H(Path(__file__))}
    if '--record' in sys.argv:
        out=R/'custody-recheck-20261025.json';need(not out.exists(),'no overwrite');out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
