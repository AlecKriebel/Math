#!/usr/bin/env python3
"""Pure stdlib custody closure. Does not import/run scientific or packaging code."""
from pathlib import Path
import json,hashlib,zipfile
E=Path(__file__).resolve().parent
P=E.parent.parent
S=P/'sources'
count=0
def need(ok,msg):
    global count
    count+=1
    if not ok:raise RuntimeError(msg)
def h(f):return hashlib.sha256(f.read_bytes()).hexdigest()
def obj(f):return json.loads(f.read_bytes())
def filematch(f,z):
    need(f.is_file() and not f.is_symlink(),'not regular: '+str(f))
    need(f.stat().st_size==z['bytes'],'size: '+str(f))
    need(h(f)==z['SHA256'],'hash: '+str(f))
def main():
    manifest=obj(E/'MANIFEST.json')
    actual={f.relative_to(E).as_posix() for f in E.rglob('*') if f.is_file()}-{'MANIFEST.json','SEAL.json'}
    need(actual=={z['path'] for z in manifest['owned_files']},'closed owned set')
    for z in manifest['owned_files']:filematch(E/z['path'],z)
    if (E/'SEAL.json').exists():
        seal=obj(E/'SEAL.json');need(h(E/'MANIFEST.json')==seal['MANIFEST_SHA256'],'manifest seal')
        for key,name in [('REPORT_SHA256','REPORT.md'),('VERDICT_SHA256','VERDICT.json'),('READ_ONLY_VERIFIER_SHA256','verify_packet_read_only.py')]:need(h(E/name)==seal[key],key)
    inp=obj(E/'INPUT_MANIFEST.json')['whole_source_directory']
    need({str(f) for f in S.rglob('*') if f.is_file()}=={z['path'] for z in inp},'whole source set')
    for z in inp:filematch(Path(z['path']),z)
    need(h(S/'SOURCE_READY.json')=='64b0c9408ee2d24da06d20d3c9bd7653e2ed9537f571a1051d40826ee5e0ab73','native ready external pin')
    need(h(S/'SOURCE_READY_SEAL.json')=='a64546bb326bcd18764d67fabbe3dd20f78fe1b472d0dc3449f86a52df71e18e','native seal external pin')
    need(h(E/'INITIAL_SEAL.json')=='5226270023651bdda20a50fb9ace62535e26f0d9d2e4739b28db39adcd37ffc1','initial seal pin')
    need(h(E/'OWN_PROOF_RESULTS_SEAL.json')=='2f21b7142426c16a0133706433c1e4fa17d159c51456c7a23c2518db474a1e62','own proof freeze pin')
    for name in ['INITIAL_SEAL.json','OWN_PROOF_RESULTS_SEAL.json']:
        for z in obj(E/name)['files']:filematch(Path(z['path']),z)
    for f in (E/'native-objects').iterdir():need(f.read_bytes()==(S/f.name).read_bytes(),'literal native body: '+f.name)
    ready=obj(S/'SOURCE_READY.json')
    need(ready['native_schema_distinctions']['record_swh']['original_value']=={},'native empty object')
    need(ready['native_schema_distinctions']['versions_swh_fields'][0]['original_value'] is None,'native null')
    need(ready['native_schema_distinctions']['files_order']['original_value']==[],'native empty order list')
    need(ready['selected_actual_PDF']['pages_visually_or_scientifically_read'] is False,'historical flag untouched')
    need(ready['controlling_TeX']['preamble_or_mathematical_body_read'] is False,'historical TeX flag untouched')
    need([x['original_api_file_object']['key'] for x in ready['all_native_assets_in_original_order']]==['periodic-lefschetz-source-and-verification.zip','periodic-lefschetz.pdf'],'original asset order')
    for a in ready['all_native_assets_in_original_order']:
        f=Path(a['path']);need(hashlib.md5(f.read_bytes()).hexdigest()==a['original_api_file_object']['checksum'].split(':')[1],'native MD5')
    archive=obj(E/'CUSTODY.json')['all_18_archive_payload_occurrences']
    with zipfile.ZipFile(S/'assets/periodic-lefschetz-source-and-verification.zip') as z:
        need(z.testzip() is None,'whole ZIP CRC')
        need(len(z.infolist())==len(archive)==18,'whole ZIP member count')
        for i,(f,a) in enumerate(zip(z.infolist(),archive)):
            need(i==a['ordinal_zero_based'] and f.filename==a['native_filename'],'native ZIP order/name')
            need(not f.is_dir() and f.file_size==a['native_uncompressed_bytes'] and f.compress_size==a['native_compressed_bytes'],'native ZIP sizes')
            need(f'{f.CRC:08x}'==a['native_CRC32'] and f.external_attr==a['native_external_attr'] and f.flag_bits==a['native_flags'] and f.create_system==a['native_create_system'] and list(f.date_time)==a['native_date_time'] and f.compress_type==a['native_compression_method'],'whole ZIP metadata')
            b=z.read(f);need(hashlib.sha256(b).hexdigest()==a['SHA256'],'ZIP SHA')
            need(b==Path(a['extracted_path']).read_bytes(),'ZIP literal extraction')
    native=S/'published-source/asset-001/periodic_lefschetz_source'
    copied=E/'native-isolated'
    original_files={f.relative_to(native).as_posix() for f in native.rglob('*') if f.is_file()}
    need(original_files=={f.relative_to(copied).as_posix() for f in copied.rglob('*') if f.is_file()},'isolated native member set')
    for name in original_files:need((native/name).read_bytes()==(copied/name).read_bytes(),'isolated copy bytes')
    public=obj(native/'PUBLIC_MANIFEST.json')['files']
    need(original_files==set(public)|{'PUBLIC_MANIFEST.json'},'whole native public manifest')
    for name,z in public.items():need((native/name).stat().st_size==z['bytes'] and h(native/name)==z['sha256'],'native public binding')
    need((native/'paper.pdf').read_bytes()==(S/'assets/periodic-lefschetz.pdf').read_bytes(),'embedded standalone PDF')
    wanted=(native/'verification/EXPECTED.json').read_bytes()
    replay=obj(E/'NATIVE_REPLAY.json')
    need(len(replay['runs'])==3,'three mode receipts')
    for run in replay['runs']:
        name=run['mode'];out=(E/f'NATIVE_{name}.stdout').read_bytes();err=(E/f'NATIVE_{name}.stderr').read_bytes()
        need(run['exit_code']==0 and run['whole_stdout_equals_unchanged_EXPECTED'] is True,'native recorded success')
        need(out==wanted and not err,'whole retained output/empty stderr')
        need(hashlib.sha256(out).hexdigest()==run['stdout_SHA256'] and hashlib.sha256(err).hexdigest()==run['stderr_SHA256'],'native output hashes')
    receipts=obj(E/'cache/primary/GET_RECEIPTS.json')
    for r,name in zip(receipts,['roemer-owr2020-31.pdf','seceleanu-sega-v1.pdf']):
        need(r['status']==200,'primary ordinary200');filematch(E/'cache/primary'/name,r)
    need(len(receipts)==2,'bounded primary receipts')
    verdict=obj(E/'VERDICT.json')
    need(verdict['record_id']==23570763 and verdict['followup'] is None and verdict['publication_authority'] is False,'verdict identity/gates')
    need(verdict['mathematical_remaining_gap'] is None,'verdict recorded scope')
    print(json.dumps({'status':'PASS_PURE_CUSTODY_ONLY','checks':count,'owned_payloads':len(manifest['owned_files']),'original_source_files_unchanged':len(inp),'native_ZIP_payloads':len(archive),'scientific_programs_rerun':False,'network_used':False,'writes_performed':False},indent=2))
if __name__=='__main__':main()
