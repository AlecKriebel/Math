#!/usr/bin/env python3
"""Read-only exact custody of the actual heterogeneous117 native objects."""
from pathlib import Path
import hashlib, json, sys, zipfile
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent; PAPER=HERE.parents[1]; SOURCE=PAPER/'sources'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def need(ok,why):
    if not ok:raise RuntimeError(why)
def main():
    need(len(sys.argv)==1,'no overrides')
    for n,h in {
      'SOURCE_READY.json':'3833194084fd0343a18c5640400418893203c6e575272997c114bc326d34e2af',
      'SOURCE_READY_MANIFEST.json':'116c685e1dcfcc58e8b96c92f93174633106ff690323ac5af512a7c804618381',
      'SOURCE_READY_SEAL.json':'04aeb3a92833a1888c083f27788f96bcbb8d9da37e414a42a0ac7ebf3a3a02ac'}.items():need(sha(SOURCE/n)==h,'native pin '+n)
    man=load(SOURCE/'SOURCE_READY_MANIFEST.json'); paths=set()
    for r in man['files']:
      p=Path(r['path']);paths.add(p)
      need(p.stat().st_size==r['bytes'] and sha(p)==r['sha256'],'native entire payload '+p.name)
    actual={p for p in SOURCE.rglob('*') if p.is_file()}
    need(actual==paths|{SOURCE/'SOURCE_READY_MANIFEST.json',SOURCE/'SOURCE_READY_SEAL.json'},'whole original native file set')
    need(len(paths)==49,'49 native manifested payloads')
    ready=load(SOURCE/'SOURCE_READY.json');record=load(SOURCE/'record.raw.json')
    need('schema' not in ready and 'all_assets_in_original_order' in ready,'actual readiness fields/absent schema retained')
    need(record==load(SOURCE/'latest.raw.json'),'whole actual record/latest native object')
    assets=ready['all_assets_in_original_order']
    need(record['files']==[r['original_api_file_object'] for r in assets],'whole original API file objects and order')
    need([r['original_api_file_object']['key'] for r in assets]==['positivity_loss.pdf','verification_package.zip'],'original PDF first ZIP second')
    for a in assets:
      p=Path(a['path']);data=p.read_bytes();md5=hashlib.md5(data).hexdigest()
      need(len(data)==a['bytes']==a['original_api_file_object']['size'],'native asset exact size')
      need(sha(p)==a['sha256'] and md5==a['md5'] and 'md5:'+md5==a['original_api_file_object']['checksum'],'native asset SHA256 and MD5')
    meta=record['metadata']
    need(meta['version']==ready['version']=='1.0','actual native version')
    need(meta['publication_date']==ready['publication_date']=='2026-10-12','declared publication date')
    need(record['created']==ready['created']=='2026-10-13T04:01:15.568262+00:00','distinct creation date')
    need(record['updated']==ready['updated']=='2026-10-13T04:01:16.394637+00:00','distinct update date')
    need(meta['license']=={'id':'cc-by-4.0'},'whole original license object')
    need(meta['creators']==[{'name':'Kriebel, Alec','affiliation':'Independent researcher','orcid':'0009-0001-9320-500X'}],'whole original author objects')
    need(meta['resource_type']=={'title':'Preprint','type':'publication','subtype':'preprint'},'whole native resource type')
    need(record['doi']==ready['doi']=='10.5281/zenodo.23331080' and str(record['conceptrecid'])=='23331079','exact DOI and concept identity')
    custody=load(SOURCE/'archive-members.json');members=custody['members'];snapshot=load(HERE/'ZIP_NATIVE_OBJECT_BINDINGS.json')['entries']
    need(len(members)==len(snapshot)==40,'40 full native archive members')
    with zipfile.ZipFile(Path(assets[1]['path'])) as z:
      infos=z.infolist();need(len(infos)==40,'no omitted ZIP entries')
      total=0
      for n,(info,r,exact) in enumerate(zip(infos,members,snapshot)):
        need(not info.is_dir(),'all original entries regular')
        data=z.read(info);total+=len(data)
        obj={'ordinal_zero_based':n,'filename':info.filename,'CRC32':format(info.CRC,'08x'),
          'file_size':info.file_size,'compress_size':info.compress_size,'flag_bits':info.flag_bits,
          'compress_type':info.compress_type,'date_time':list(info.date_time),'external_attr':info.external_attr,
          'create_system':info.create_system,'comment_hex':info.comment.hex(),'extra_hex':info.extra.hex(),
          'SHA256':hashlib.sha256(data).hexdigest()}
        need(obj==exact,'whole ZIP native-header/body object '+info.filename)
        need(r['ordinal_zero_based']==n and r['original_member_name']==info.filename,'native zero-based archive order')
        need(r['bytes']==info.file_size and r['compressed_bytes']==info.compress_size and r['zip_flags']==info.flag_bits and r['native_external_attr']==info.external_attr,'actual heterogeneous member schema')
        need(r['CRC32']==obj['CRC32'] and r['sha256']==obj['SHA256'],'source original member CRC/SHA')
        need(Path(r['extracted_path']).read_bytes()==data,'complete unchanged extracted source '+info.filename)
      need(total==198877,'all expanded original bytes')
    need(ready['all_embedded_PDF_members']==[],'actual single standalone reader only')
    for key,pathkey in [('selected_actual_PDF','path'),('controlling_TeX','extracted_path')]:
      r=ready[key];p=Path(r[pathkey]);need(p.stat().st_size==r['bytes'] and sha(p)==r['sha256'],'actual controlling PDF/TeX identity')
    need(sha(HERE/'INITIAL_SEAL.json')=='3ce1782de3c68ee334ceb944225540e4a41240dac4e692dac511b76097ff91f8','independent pre-exposure initial seal')
    initial=load(HERE/'INITIAL_SEAL.json')
    need(sha(HERE/'INITIAL_MANIFEST.json')==initial['manifest_SHA256'],'initial independent manifest')
    for r in load(HERE/'INITIAL_MANIFEST.json')['files']:
      p=HERE/r['path'];need(p.stat().st_size==r['bytes'] and sha(p)==r['SHA256'],'unchanged initial payload '+r['path'])
    primary=load(HERE/'PRIMARY_BINDINGS.json')['bindings'];need(len(primary)==5,'five distinct actual primary objects')
    for r in primary:
      p=Path(r['path']);need(p.stat().st_size==r['bytes'] and sha(p)==r['SHA256'],'actual primary body '+p.name)
    variants=load(HERE/'cache/primary/PUBLISHER_VARIANT_COMPARISON.json')
    need(not variants['native_PDFs_byte_identical'] and variants['remaining_full_extracted_text_identical'],'publisher watermark variant distinction')
    root=SOURCE/'published-source/positivity-loss-30003571'
    for copied,original in [('author/verify.py','original/public/verify.py'),('geometry/verify_independent.py','reviews/geometry01/verify_independent.py')]:
      need((HERE/'cache/replay'/copied).read_bytes()==(root/original).read_bytes(),'byte-identical isolated mathematical copy '+copied)
    need((HERE/'NATIVE_AUTHOR_NORMAL.json').read_bytes()==(root/'original/public/verification_results.json').read_bytes(),'whole normal author stdout equals original receipt')
    g=load(HERE/'cache/replay/geometry/verification_results.json');originalg=load(root/'reviews/geometry01/verification_results.json')
    need([k for k in g.keys()|originalg.keys() if g.get(k)!=originalg.get(k)]==['python'],'geometry only native runtime-metadata difference')
    need(g['status']=='PASS_GEOMETRY_AND_EXACT_ALGEBRA' and g['exact_checks']==57,'literal geometry custom status')
    need(load(HERE/'NATIVE_AUTHOR_NORMAL.json')['status']=='PASS','literal author status')
    guards=load(HERE/'NATIVE_GUARD_MODE.json')['records']
    need(guards[0]['wrong_initial_weight_rejected'] and not guards[1]['wrong_initial_weight_rejected'] and guards[1]['literal_stdout_status']=='PASS','native wrong-weight optimized assertion limitation retained')
    print(json.dumps({'assessment':'NATIVE_HETEROGENEOUS_OBJECTS_ORDER_ALL_SOURCE_BYTES_INITIAL_AND_PRIMARY_CUSTODY_RECONFIRMED',
      'native_manifest_payloads':49,'native_files_including_manifest_seal':51,'original_archive_payloads':40,
      'original_expanded_bytes':198877,'initial_manifest_payloads':8,'critical_primary_objects':5,
      'native_asset_order':['PDF','ZIP'],'native_schema_normalized_or_replaced':False,
      'literal_native_author_status':'PASS','literal_native_geometry_status':'PASS_GEOMETRY_AND_EXACT_ALGEBRA',
      'native_optimized_false_weight_literal_PASS_is_validation':False,'sources_or_packets_modified':False},indent=2,sort_keys=True))
if __name__=='__main__':main()
