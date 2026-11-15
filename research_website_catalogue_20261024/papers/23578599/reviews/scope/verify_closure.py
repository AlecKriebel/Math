#!/usr/bin/env python3
"""Pure offline custody/consistency checks; no target imports or executions.

Standard library only. No network/subprocess/write. --preseal omits terminal
SEAL/CLOSURE checks. In-memory corruptions test custody, not theorem universality.
"""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
import copy
import hashlib
import json
import stat
import sys
import zipfile
import zlib

P=Path(__file__).resolve().parent
S=P.parent.parent/'sources'
TERMINAL={'OWNED_MANIFEST.json','CLOSURE.json','SEAL.json'}
READY='c38e49d39bef6213a4703ee624be84eb110f1479a9c7b7e27b331bc39d417df4'
SOURCE_SEAL='1b465f294497cb8b9a60fb5bfb33e46b2b1ecc43f91975b71fd7f1a4d396a10d'
SOURCE_MANIFEST='8470aae7f8430743feed2c70484c01feb49bac30fa86dd431ae42e4baad76325'
INITIAL='26ec124cd3f33b4fc066026798a2f8f3a856dd163cf3c4005a9bb942d0ba9f69'
INITIAL_PROOF='71eb32bcaa7abbac5918de4d1aeb61f2c3ebc2a0373602cdc3d450fb0ce4f7a5'
PDF='b1ec29d959b658c2859ffa5d3b320797423c159616fa1bb9e361e911a3f95048'
TEX='e39f48a53353f499156461fe1068292cc6294bb07e19e5a72f4fb87946ef98ee'
ZIP='ac7cb8169be7003b2c13bb12ad7ab69f0d7b9ca533d916d31cc2941cb888b829'
NAMES=['free-chain-nash-intersections.pdf','free-chain-nash-intersections-source-and-verification.zip']
TITLE='A free-chain counterexample to a Nash-intersection conjecture'
CHECKS=0


def need(test,message):
    global CHECKS
    CHECKS+=1
    if not test:raise ValueError(message)


def sha(body):return hashlib.sha256(body).hexdigest()
def load(path):return json.loads(path.read_bytes())


def file_check(path,size,digest):
    need(path.is_file() and not path.is_symlink(),'missing/symbolic file: '+str(path))
    body=path.read_bytes()
    need(len(body)==size and sha(body)==digest,'bytes changed: '+str(path))
    return body


def safe_name(name,attrs):
    parts=PurePosixPath(name).parts
    return bool(name) and not name.startswith('/') and '\\' not in name and '..' not in parts and ':' not in parts[0] and stat.S_IFMT(attrs>>16) in (0,stat.S_IFREG)


def native_check(record,latest,versions,files,ready):
    for obj in (record,latest):
        need(obj['id']==23578599 and obj['doi']=='10.5281/zenodo.23578599' and obj['conceptrecid']=='23578598','native identity/concept type')
        need(obj['metadata']['title']==TITLE and obj['metadata']['version']=='1.0.0' and obj['metadata']['publication_date']=='2026-10-22','native title/version/date')
        need(obj['created']=='2026-10-22T21:24:54.317246+00:00' and obj['updated']=='2026-10-22T21:24:54.772321+00:00','native timestamps')
        need(obj['status']=='published' and obj['state']=='done' and obj['submitted'] is True,'native status fields')
        need(type(obj['swh']) is dict and obj['swh']=={},'native empty object changed')
        need(obj['metadata']['license']=={'id':'cc-by-4.0'},'native license object')
        need(obj['metadata']['resource_type']=={'title':'Preprint','type':'publication','subtype':'preprint'},'whole native resource type')
        need([x['key'] for x in obj['files']]==NAMES,'native PDF/ZIP order')
    need(type(versions['hits']['total']) is int and versions['hits']['total']==1 and len(versions['hits']['hits'])==1,'version count/type')
    hit=versions['hits']['hits'][0]
    need(hit['id']==23578599 and 'swh' in hit and hit['swh'] is None,'version present null')
    need(type(files['entries']) is list and [x['key'] for x in files['entries']]==NAMES,'native files type/order')
    need(type(files['order']) is list and files['order']==[] and files['default_preview'] is None,'native empty/null')
    need(record['files']==[x['original_api_file_object'] for x in ready['all_native_assets_in_original_order']],'whole API file objects')
    need(files['entries']==[x['whole_original_native_files_entry'] for x in ready['all_native_assets_in_original_order']],'whole opaque files entries')
    need(ready['native_schema_distinctions']['version_hit_swh_fields']==[{'present':True,'original_value':None}],'native presence wrapper')
    need(ready['printed_title_date_version_inspected'] is False and ready['printed_date'] is None and ready['completion_percent_at_preseal']==95,'historical unread/stage flags changed')


def result_check(result,verdict,ledger):
    need(result['status']=='PASS' and result['jet_cases']==1650 and result['random_parameter_substitutions']==8250,'own jet evidence changed')
    need(result['exact_prefix_pair_checks']==1650 and result['separator_cases']==1800 and result['divisibility_boundaries']==3081,'own finite scope changed')
    need(result['rational_chart_overlaps']==54 and result['satellite_contact_cases']==990,'own chart evidence changed')
    need(verdict['original_scope_preserved'] is True and verdict['remaining_mathematical_gap'] is None,'literal qualified disposition changed')
    claims=verdict['verified_claims']
    need(claims['complete_complex_all_free_family_not_selected_subfamily'] is True and claims['all_n_at_least_3_and_2_le_k_lt_n'] is True,'complete/all-integer scope weakened')
    need(claims['both_n5_examples_exclude_every_positive_j_q'] is True and claims['n5k2_thresholds']==[3,5] and claims['n5k3_thresholds']==[2,5],'all-reference thresholds changed')
    need(claims['other_primitive_toric_divisors_do_represent_intersections'] is True and claims['reduced_support_not_nonreduced_scheme_equality'] is True,'scope limits erased')
    need(verdict['native_execution_or_import_by_this_lane'] is False,'native campaign execution invented')
    need(verdict['follow_up'] is None and verdict['external_human_peer_review'] is False and verdict['formal_proof_assistant_certification'] is False,'followup/review status changed')
    need(verdict['prose_license']=='CC BY4.0' and verdict['code_license']=='MIT','distinct rights changed')
    need(ledger['paper_first_boundary']['foreign_body_code_results_archived_current_opinions_before_initial'] is False and ledger['current_sibling_or_root_science_read'] is False,'independence exposure changed')


def mutation_checks(record,latest,versions,files,ready,result,verdict,ledger):
    rejected=[]
    def reject(label,f):
        try:f()
        except (ValueError,KeyError,TypeError,IndexError):rejected.append(label)
        else:raise ValueError('mutation escaped: '+label)
    for label,edit in [
        ('native version changed',lambda x:x[0]['metadata'].__setitem__('version','latest')),
        ('PDF ZIP order reversed',lambda x:x[0]['files'].reverse()),
        ('record empty object changed to null',lambda x:x[0].__setitem__('swh',None)),
        ('version null changed to missing',lambda x:x[2]['hits']['hits'][0].pop('swh')),
        ('files entries list normalized to mapping',lambda x:x[3].__setitem__('entries',{})),
        ('opaque file metadata changed',lambda x:x[3]['entries'][0]['metadata'].__setitem__('width',999)),
        ('native version presence wrapper flattened',lambda x:x[4]['native_schema_distinctions'].__setitem__('version_hit_swh_fields',[None])),
        ('historical source inspection flag rewritten',lambda x:x[4].__setitem__('printed_title_date_version_inspected',True)),
    ]:
        x=copy.deepcopy([record,latest,versions,files,ready]);edit(x)
        reject(label,lambda:native_check(*x))
    for label,edit in [
        ('own finite count changed',lambda x:x[0].__setitem__('jet_cases',1649)),
        ('whole family weakened',lambda x:x[1]['verified_claims'].__setitem__('complete_complex_all_free_family_not_selected_subfamily',False)),
        ('all positive reference indices weakened',lambda x:x[1]['verified_claims'].__setitem__('both_n5_examples_exclude_every_positive_j_q',False)),
        ('threshold changed',lambda x:x[1]['verified_claims'].__setitem__('n5k2_thresholds',[2,5])),
        ('other toric divisor boundary erased',lambda x:x[1]['verified_claims'].__setitem__('other_primitive_toric_divisors_do_represent_intersections',False)),
        ('human peer review invented',lambda x:x[1].__setitem__('external_human_peer_review',True)),
        ('native execution invented',lambda x:x[1].__setitem__('native_execution_or_import_by_this_lane',True)),
        ('preinitial opinion exposure hidden',lambda x:x[2]['paper_first_boundary'].__setitem__('foreign_body_code_results_archived_current_opinions_before_initial',True)),
    ]:
        x=copy.deepcopy([result,verdict,ledger]);edit(x)
        reject(label,lambda:result_check(*x))
    for name,attrs in [('../escape',2175008768),('/absolute',2175008768),('link',(stat.S_IFLNK|0o644)<<16)]:
        reject('unsafe ZIP member '+name,lambda n=name,a=attrs:need(safe_name(n,a),'unsafe member'))
    body=(S/'assets/free-chain-nash-intersections.pdf').read_bytes()
    reject('altered PDF bytes',lambda:need(sha(body+b'bad')==PDF,'PDF bytes altered'))
    return rejected


def main():
    preseal=sys.argv[1:]==['--preseal']
    need(preseal or not sys.argv[1:],'only --preseal supported')
    for path,digest in [(S/'SOURCE_READY.json',READY),(S/'SOURCE_READY_SEAL.json',SOURCE_SEAL),(S/'SOURCE_READY_MANIFEST.json',SOURCE_MANIFEST),(P/'INITIAL_SEAL.json',INITIAL),(P/'INITIAL_RECONSTRUCTION.md',INITIAL_PROOF)]:
        need(sha(path.read_bytes())==digest,'fixed seal/hash changed: '+str(path))
    inputs,owned=load(P/'INPUT_MANIFEST.json'),load(P/'OWNED_MANIFEST.json')
    for item in inputs['files']:file_check(Path(item['path']),item['bytes'],item['SHA256'])
    for item in owned['files']:
        rel=PurePosixPath(item['path']);need(not rel.is_absolute() and '..' not in rel.parts,'unsafe owned path')
        file_check(P/item['path'],item['bytes'],item['SHA256'])
    need({str(q.relative_to(P)) for q in P.rglob('*') if q.is_file() and q.name not in TERMINAL}=={x['path'] for x in owned['files']},'owned file set changed')
    source_manifest=load(S/'SOURCE_READY_MANIFEST.json')
    for item in source_manifest['files']:file_check(S/item['path'],item['bytes'],item['SHA256'])
    need({str(q.relative_to(S)) for q in S.rglob('*') if q.is_file()}=={x['path'] for x in source_manifest['files']}|{'SOURCE_READY_MANIFEST.json','SOURCE_READY_CLOSURE.json','SOURCE_READY_SEAL.json'},'whole source file set changed')
    need(sha((S/'SOURCE_READY_CLOSURE.json').read_bytes())==load(S/'SOURCE_READY_SEAL.json')['CLOSURE_SHA256'],'source closure changed')
    ready=load(S/'SOURCE_READY.json')
    record,latest,versions,files=[load(S/n) for n in ['record.response.body','latest.response.body.redirect-01','versions-page001.response.body','files.response.body']]
    native_check(record,latest,versions,files,ready)
    receipts=load(S/'ALL_TRANSPORT_RECEIPTS.json')['receipts']
    need([x['HTTP_status'] for x in receipts]==[200,301,200,200,200,200,200],'native transport status/order changed')
    for row in receipts:
        need(type(row['response_headers_in_received_order']) is list,'native ordered headers normalized')
        file_check(Path(row['body_path']),row['body_bytes'],row['body_SHA256'])
    need(receipts[1]['body_bytes']==99,'native redirect body lost')
    for asset in ready['all_native_assets_in_original_order']:
        body=file_check(Path(asset['path']),asset['bytes'],asset['SHA256'])
        need(hashlib.md5(body).hexdigest()==asset['original_api_file_object']['checksum'].removeprefix('md5:'),'native original MD5 mismatch')
    need(ready['selected_actual_PDF']['SHA256']==PDF and ready['selected_actual_PDF']['pages']==5,'actual manuscript binding changed')
    tex=Path(ready['controlling_TeX']['extracted_path']).read_bytes()
    need(len(tex)==17933 and len(tex.splitlines())==380 and sha(tex)==TEX,'controlling TeX binding changed')
    for row in ready['embedded_PDFs']:
        body=file_check(Path(row['path']),row['bytes'],row['SHA256'])
        need(body==(S/'assets/free-chain-nash-intersections.pdf').read_bytes(),'embedded PDF not published bytes')
    archive=load(S/'ARCHIVE_CUSTODY.json');items=archive['all_safe_regular_occurrences'];central=archive['containers'][0]['whole_original_central_directory']
    need(len(items)==len(central)==archive['safe_regular_occurrences']==21 and archive['expanded_bytes_all_depths']==161736,'whole archive scope changed')
    need(archive['nested_archives']==0 and archive['unsafe_or_colliding_names']==archive['encrypted_or_nonregular_payloads']==archive['unsupported_archive_magic']==[],'archive safety changed')
    zp=S/'assets/free-chain-nash-intersections-source-and-verification.zip';need(sha(zp.read_bytes())==ZIP,'whole ZIP changed')
    with zipfile.ZipFile(zp) as z:
        infos=z.infolist();need(len(infos)==21 and z.testzip() is None,'ZIP directory/CRC changed')
        seen,total=set(),0
        for i,(info,item,cd) in enumerate(zip(infos,items,central)):
            need(safe_name(info.filename,info.external_attr) and not info.is_dir() and not(info.flag_bits&1) and info.filename.casefold() not in seen,'unsafe/encrypted/nonregular payload')
            seen.add(info.filename.casefold())
            actual={'ordinal_zero_based':i,'filename':info.filename,'original_filename':info.orig_filename,'is_directory':info.is_dir(),'bytes':info.file_size,'compressed_bytes':info.compress_size,'CRC32':f'{info.CRC:08x}','flags':info.flag_bits,'compression':info.compress_type,'native_date_time':list(info.date_time),'external_attr':info.external_attr,'internal_attr':info.internal_attr,'create_system':info.create_system,'create_version':info.create_version,'extract_version':info.extract_version,'header_offset':info.header_offset,'extra_hex':info.extra.hex(),'comment_hex':info.comment.hex()}
            need(actual==cd,'whole native central directory entry changed')
            need(info.filename==item['original_member_name'] and item['ordinal_zero_based']==i,'member occurrence name/order changed')
            body=z.read(info)
            need(len(body)==item['bytes'] and sha(body)==item['SHA256'] and f'{zlib.crc32(body)&0xffffffff:08x}'==item['CRC32'],'member bytes/CRC/hash changed')
            need(body==Path(item['extracted_path']).read_bytes(),'extracted bytes differ')
            total+=len(body)
        need(total==161736,'expanded total changed')
    primary_receipts=list((P/'primary').glob('*.receipt.json'));need(len(primary_receipts)==5,'primary receipt count changed')
    for path in primary_receipts:
        row=load(path);body=file_check(Path(row['path']),row['bytes'],row['SHA256'])
        need(row['status']==200 and row['actual_PDF'] is True and body.startswith(b'%PDF-') and type(row['response_headers_in_received_order']) is list,'actual primary body/ordered receipt changed')
    result,verdict,ledger=[load(P/n) for n in ['INDEPENDENT_CHECKS.json','VERDICT.json','READ_LEDGER.json']]
    result_check(result,verdict,ledger)
    mutants=mutation_checks(record,latest,versions,files,ready,result,verdict,ledger)
    if not preseal:
        seal=load(P/'SEAL.json')
        for n,k in [('INPUT_MANIFEST.json','INPUT_MANIFEST_SHA256'),('OWNED_MANIFEST.json','OWNED_MANIFEST_SHA256'),('CLOSURE.json','CLOSURE_SHA256'),('REPORT.md','REPORT_SHA256'),('VERDICT.json','VERDICT_SHA256'),('verify_closure.py','verifier_SHA256')]:
            need(sha((P/n).read_bytes())==seal[k],'terminal seal mismatch: '+n)
    return {'UTC':datetime.now(timezone.utc).isoformat(),'status':'PASS','mode':'preseal' if preseal else 'sealed','record_id':23578599,'checks':CHECKS,'input_files':len(inputs['files']),'owned_files':len(owned['files']),'native_ZIP_payloads':21,'native_transport_receipts':7,'fresh_primary_PDFs':5,'in_memory_mutants_rejected':mutants,'network_requests':[],'target_imports':[],'programs_executed':[],'writes':[],'scope':'Pure offline custody and literal packet consistency; proofs and independent finite controls are separately recorded.'}


if __name__=='__main__':
    try:print(json.dumps(main(),indent=2))
    except Exception as error:
        print(json.dumps({'UTC':datetime.now(timezone.utc).isoformat(),'status':'FAIL','checks_completed':CHECKS,'error':str(error),'network_requests':[],'target_imports':[],'programs_executed':[],'writes':[]},indent=2));sys.exit(1)
