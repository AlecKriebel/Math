"""Read-only native source custody; never reads science semantically or executes payloads."""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import io
import json
import stat
import tarfile
import zipfile

A=Path(__file__).resolve().parent
S=A.parent/'sources'

def require(x,m):
    if not x:raise RuntimeError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_bytes())
def same(a,b):
    if type(a) is not type(b):return False
    if isinstance(a,dict):return list(a)==list(b) and all(same(a[k],b[k]) for k in a)
    if isinstance(a,list):return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
    return a==b
def check(e):
    p=Path(e['path']);require(p.is_file() and not p.is_symlink(),'missing/nonregular '+str(p))
    require(p.stat().st_size==e['bytes'] and sha(p)==e['sha256'],'file identity '+str(p))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--require-seal',action='store_true');args=ap.parse_args()
    ready=read(S/'SOURCE_READY.json');record=read(S/'record.raw.json');latest=read(S/'latest.raw.json')
    versions=read(S/'versions.raw.json');receipts=read(S/'api-receipts.json');arch=read(S/'archive-members.json')
    require(ready['record_id']==record['id']==latest['id']==23331080,'native identity')
    require(versions['hits']['total']==1 and [x['id'] for x in versions['hits']['hits']]==[23331080]
            and not versions['links'].get('next'),'complete native version census')
    require(ready['version']=='1.0' and ready['publication_date']=='2026-10-12','native declared edition')
    require(ready['created']==record['created'] and ready['updated']==record['updated'],'native creation/update')
    require(len(receipts)==5 and all(x['HTTP_status']==200 for x in receipts),'five actual native responses')
    for x in receipts:
        check(x['body'])
        require(isinstance(x['response_headers_in_received_order'],list)
                and all(isinstance(y,list) and len(y)==2 for y in x['response_headers_in_received_order']),
                'native ordered header pairs')
    require(same([a['original_api_file_object'] for a in ready['all_assets_in_original_order']],record['files']),
            'whole original API file objects/order/types')
    require([a['original_api_file_object']['key'] for a in ready['all_assets_in_original_order']]==
            ['positivity_loss.pdf','verification_package.zip'],'native PDF/ZIP order')
    for asset in ready['all_assets_in_original_order']:
        check(asset);body=Path(asset['path']).read_bytes();alg,wanted=asset['original_api_file_object']['checksum'].split(':',1)
        require(hashlib.new(alg,body).hexdigest()==wanted,'native provider checksum')
        require(hashlib.md5(body).hexdigest()==asset['md5'],'native local MD5 binding')
    rows=arch['members'];count=0;expanded=0;seen=set()
    with zipfile.ZipFile(S/'verification_package.zip') as z:
        for ordinal,info in enumerate(z.infolist()):
            name=PurePosixPath(info.filename);key=str(name).casefold()
            require(not name.is_absolute() and '..' not in name.parts and '\\' not in info.filename,'safe archive path')
            require(key not in seen,'duplicate or case-colliding member');seen.add(key)
            require((info.external_attr>>16)&0o170000 in [0,stat.S_IFREG,stat.S_IFDIR],'regular member')
            if info.is_dir():continue
            body=z.read(info);entry=rows[count]
            require(entry['ordinal_zero_based']==ordinal and entry['original_member_name']==info.filename,'member identity/order')
            require(entry['bytes']==len(body) and entry['CRC32']==format(info.CRC,'08x')
                    and entry['sha256']==hashlib.sha256(body).hexdigest(),'CRC/size/SHA256 native member')
            require(Path(entry['extracted_path']).read_bytes()==body,'original extracted bytes')
            require(not zipfile.is_zipfile(Path(entry['extracted_path'])),'unexpected nested ZIP')
            try:
                nested=tarfile.open(fileobj=io.BytesIO(body),mode='r:*')
            except tarfile.ReadError:
                pass
            else:
                nested.close()
                raise RuntimeError('unexpected nested tar/compressed tar')
            count+=1;expanded+=len(body)
    require(count==40 and expanded==198877 and arch['safe_regular_occurrences']==40,'whole archive census')
    require(ready['selected_actual_PDF']['pages']==4,'actual metadata page count')
    tex=ready['controlling_TeX'];p=Path(tex['extracted_path']);check({'path':str(p),'bytes':tex['bytes'],'sha256':tex['sha256']})
    data=p.read_bytes();require(data.count(b'\n')+(0 if data.endswith(b'\n') else 1)==272,'opaque TeX line count')
    for field in ['target_manuscript_scientifically_read','target_PDF_rendered_or_text_extracted',
                  'source_programs_executed_or_scientifically_read','archived_current_opinions_or_inventory_triage_read',
                  'foreign_primary_scientific_bodies_read']:
        require(ready[field] is False,'acquisition-only boundary')
    require(ready['originals_now_immutable'] is True,'source frozen')
    identity=read(A/'IDENTITY_AUTHORITY.json')
    require(sha(Path(identity['queue_path']))==identity['queue_sha256'],'authenticated local queue binding')
    for k in ['spreadsheet_snapshot','zenodo_snapshot']:
        require(sha(Path(identity[k]['path']))==identity[k]['sha256'],'native inventory snapshot')
    seals={}
    if args.require_seal:
        sm=read(S/'SOURCE_READY_MANIFEST.json');ss=read(S/'SOURCE_READY_SEAL.json')
        require(sha(S/'SOURCE_READY_MANIFEST.json')==ss['manifest_sha256'],'source manifest seal')
        require(sha(S/'SOURCE_READY.json')==ss['source_ready_sha256'],'source readiness seal')
        for e in sm['files']:check(e)
        actual={str(p.resolve()) for p in S.rglob('*') if p.is_file()}
        expected={e['path'] for e in sm['files']}|{str(S/'SOURCE_READY_MANIFEST.json'),str(S/'SOURCE_READY_SEAL.json')}
        require(actual==expected,'frozen source tree census')
        am=read(A/'MANIFEST.json');aseal=read(A/'SEAL.json')
        require(sha(A/'MANIFEST.json')==aseal['manifest_sha256'],'acquisition manifest seal')
        require(sha(S/'SOURCE_READY_SEAL.json')==aseal['source_ready_seal_sha256'],'cross source seal')
        for e in am['files']:check({'path':str(A/e['path']),'bytes':e['bytes'],'sha256':e['sha256']})
        require({str(p.relative_to(A)) for p in A.rglob('*') if p.is_file()}==
                {e['path'] for e in am['files']}|{'MANIFEST.json','SEAL.json'},'acquisition packet census')
        seals={'source_ready_sha256':sha(S/'SOURCE_READY.json'),'source_ready_seal_sha256':sha(S/'SOURCE_READY_SEAL.json'),
               'acquisition_seal_sha256':sha(A/'SEAL.json')}
    print(json.dumps({'status':'PASS_ACQUISITION_ONLY_NATIVE_CUSTODY','record_id':23331080,'native_regular_payloads':count,
                      'native_API_responses':len(receipts),'version_count':1,'scientific_body_reading':False,
                      'source_program_execution':False,'file_writes':False,**seals},sort_keys=True))

if __name__=='__main__':main()
