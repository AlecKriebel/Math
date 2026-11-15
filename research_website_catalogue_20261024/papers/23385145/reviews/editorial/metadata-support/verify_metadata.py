#!/usr/bin/env python3
"""Pure offline source/metadata custody check; stdout only, no code replay.

No network/browser/subprocess/writes. ZIP payloads are read only as bytes for
CRC/hash equality, not interpreted as programs or scientific evidence.
"""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import zipfile
import zlib

BASE=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
PAPER=BASE/'papers/23385145'
OWN=Path(__file__).resolve().parent
ROOT_SHA256='7103359ae07eb8c6e6560c7c8626cd991cc0c69f222134e10bea642b50350331'
checks=[]
controls=[]


def data(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strict(a,b):
    if type(a) is not type(b):
        return False
    if isinstance(a,dict):
        return list(a)==list(b) and all(strict(a[k],b[k]) for k in a)
    if isinstance(a,list):
        return len(a)==len(b) and all(strict(x,y) for x,y in zip(a,b))
    return a==b


def require(test,name):
    if not test:
        raise RuntimeError(name)
    checks.append(name)


def reject(name,accepted):
    if accepted:
        raise RuntimeError('Metadata mutation survived: '+name)
    controls.append(name)


def bound_original(wrapper):
    f=Path(wrapper['path'])
    require(sha(f)==wrapper['sha256'],'Original hash: '+str(f.relative_to(BASE)))
    require(strict(data(f),wrapper['whole_literal_original_object']),
            'Whole literal original: '+str(f.relative_to(BASE)))


guard=data(OWN/'INPUT_MANIFEST.json')
for item in guard['files']:
    f=Path(item['path'])
    require(f.is_file() and f.stat().st_size==item['bytes'] and sha(f)==item['sha256'],
            'Immutable preexisting bytes: '+str(f.relative_to(BASE)))
protocol=data(OWN/'SOURCE_PROTOCOL_BINDINGS.json')
rights=data(OWN/'RIGHTS_AND_IDENTITY.json')
for key in ['root_authority','source_ready','source_manifest','source_seal',
            'actual_transport_aggregate','whole_archive_custody','native_schema_types','printed_identity']:
    bound_original(protocol[key])
root=protocol['root_authority']['whole_literal_original_object']
ready=protocol['source_ready']['whole_literal_original_object']
require(protocol['root_authority']['sha256']==ROOT_SHA256,'Exact assigned root authority')
require(strict(ready,root['whole_literal_source_ready']),'Root/source whole literal SOURCE_READY equality')
require(protocol['current_publication_or_AA_or_integration_authority'] is False
        and protocol['publication_configs_or_public_copy_authored'] is False,
        'Metadata support confers no public/config/copy authority')
manifest=protocol['source_manifest']['whole_literal_original_object']
for item in manifest['files']:
    f=PAPER/'sources'/item['path']
    require(f.stat().st_size==item['bytes'] and sha(f)==item['SHA256'],
            'Original acquisition manifest: '+item['path'])

api=protocol['all_four_native_API_objects_in_source_ready_order']
require(len(api)==4,'All four actual native API objects retained')
roles={}
for wrapper in api:
    f=Path(wrapper['actual_path']);reference=wrapper['source_ready_original_reference']
    require(f.stat().st_size==wrapper['bytes']==reference['bytes']
            and sha(f)==wrapper['sha256']==reference['SHA256'],
            'Exact native API body '+reference['role'])
    require(strict(data(f),wrapper['whole_literal_original_object']),
            'Complete native API object '+reference['role'])
    roles[reference['role']]=wrapper['whole_literal_original_object']
require(strict([x['source_ready_original_reference'] for x in api],ready['whole_native_API_objects']),
        'Native API reference order preserved')
record,versions,files=roles['record'],roles['versions_page_001'],roles['files']
require(Path(api[0]['actual_path']).read_bytes()==Path(api[1]['actual_path']).read_bytes(),
        'Successful retry record and latest bytes identical')
require(type(record['swh']) is dict and record['swh']=={}
        and versions['hits']['hits'][0]['swh'] is None,'Native empty swh versus version-null')
require(type(versions['hits']['total']) is int and versions['hits']['total']==1,
        'Native integer version total')
require(type(files['entries']) is list and type(files['order']) is list
        and files['order']==[] and files['default_preview'] is None,
        'Native files list, empty order and null preview')
require(record['metadata']['version']=='1.0' and type(record['metadata']['version']) is str,
        'Literal string API version1.0')
require(record['metadata']['publication_date']=='2026-10-14'
        and record['created']=='2026-10-15T05:18:05.239497+00:00'
        and record['updated']=='2026-10-15T05:18:05.515462+00:00',
        'Declared14Oct versus created/updated15Oct')

aggregate=protocol['actual_transport_aggregate']['whole_literal_original_object']
receipts=aggregate['receipts']
wrappers=protocol['all_seven_actual_transport_objects_in_original_collection_order']
require(len(receipts)==len(wrappers)==7,'Seven actual transport objects')
require([x['HTTP_status'] for x in receipts]==[403,200,200,200,200,200,200],
        'Native failure/six-success order retained')
require(strict([x['whole_literal_original_object'] for x in wrappers],receipts),
        'Complete actual transport collection order and objects')
for wrapper,receipt in zip(wrappers,receipts):
    f=Path(wrapper['actual_transport_file'])
    require(f.stat().st_size==wrapper['bytes'] and sha(f)==wrapper['sha256']
            and strict(data(f),receipt),'Actual individual receipt '+f.name)
    body=Path(receipt['path'])
    require(body.stat().st_size==receipt['bytes'] and sha(body)==receipt['SHA256']
            and hashlib.md5(body.read_bytes()).hexdigest()==receipt['MD5'],
            'Actual recorded body '+str(body.relative_to(PAPER/'sources')))
    require(type(receipt['request_headers']) is list
            and type(receipt['headers_in_received_order']) is list,
            'Original ordered header arrays '+f.name)
require(receipts[0]['bytes']==763 and receipts[0]['reason']=='Forbidden'
        and receipts[0]['path']!=api[0]['actual_path'],
        'Complete first403 body distinct from successful retry')
require(len(receipts[2]['redirect_hops'])==1
        and receipts[2]['redirect_hops'][0]['HTTP_status']==301
        and receipts[2]['HTTP_status']==200,'Latest301 hop and final200 both retained')
require(all(sum(pair[0]=='content-type' for pair in x['headers_in_received_order'])==2
            for x in receipts[-2:]),'Duplicate native asset response headers retained')

assets=ready['all_assets_in_original_order']
require([x['original_api_file_object']['key'] for x in assets]
        ==['weighted_centers.pdf','verification_package.zip'],
        'Actual PDF-before-ZIP native order')
for item,raw in zip(assets,record['files']):
    f=Path(item['path'])
    require(strict(item['original_api_file_object'],raw),'Whole original native file object '+raw['key'])
    require(f.stat().st_size==item['bytes']==raw['size'] and sha(f)==item['sha256']
            and hashlib.md5(f.read_bytes()).hexdigest()==item['md5']==raw['checksum'].split(':')[1],
            'Complete native asset bytes '+raw['key'])
require(Path(assets[0]['path']).read_bytes().startswith(b'%PDF-')
        and ready['selected_actual_PDF']['pages']==5
        and protocol['printed_identity']['whole_literal_original_object']['PDF']['pages']==5,
        'Actual five-page reader hash/identity binding')
custody=protocol['whole_archive_custody']['whole_literal_original_object']
members=custody['all_safe_regular_occurrences']
require(len(members)==93 and custody['safe_regular_occurrences']==93
        and custody['expanded_bytes_all_depths']==705178,'Whole93-payload archive envelope')
with zipfile.ZipFile(assets[1]['path']) as archive:
    infos=archive.infolist()
    require(len(infos)==93,'Native ZIP has93 entries')
    for member in members:
        zi=infos[member['ordinal_zero_based']];body=archive.read(zi)
        require(zi.filename==member['original_member_name']
                and zi.file_size==member['bytes'] and zi.compress_size==member['compressed_bytes']
                and zi.flag_bits==member['zip_flags'] and zi.compress_type==member['compression_method']
                and zi.external_attr==member['native_external_attr']
                and list(zi.date_time)==member['native_date_time']
                and format(zlib.crc32(body)&0xffffffff,'08x')==member['CRC32']
                and hashlib.sha256(body).hexdigest()==member['SHA256']
                and body==Path(member['extracted_path']).read_bytes(),
                'Original ZIP order/attributes/CRC/bytes '+zi.filename)

peers=protocol['all_three_whole_literal_scientific_verdicts']
require([x['lane'] for x in peers]==['scope','analytic','adversarial'],
        'All three literal scientific verdict lanes')
for item,root_item in zip(peers,root['whole_literal_peer_verdicts_and_seals']):
    f=Path(item['actual_verdict_path']);seal=Path(item['actual_seal_path'])
    require(f.stat().st_size==item['bytes'] and sha(f)==item['sha256']
            and strict(data(f),item['whole_literal_original_object'])
            and strict(data(f),root_item['whole_literal_verdict']),
            'Whole exact '+item['lane']+' verdict')
    require(sha(seal)==item['seal_sha256']==root_item['seal_sha256']
            and strict(data(seal),item['whole_literal_original_seal']),
            'Actual exact '+item['lane']+' seal')
require(peers[2]['actual_verdict_path'].endswith('/independent_20261115_sol/CUSTOM_VERDICT.json'),
        'Actual adversarial verdict path, not guessed flat path')

readme=Path(rights['actual_top_level_README_path'])
require(sha(readme)==rights['actual_top_level_README_sha256']
        and rights['actual_README_grant_verbatim'] in readme.read_text(),
        'Actual authored README license grant')
require(strict(rights['native_license_original'],record['metadata']['license'])
        and rights['authored_materials_license']=='CC BY 4.0'
        and rights['separate_code_license_file_found'] is False
        and rights['MIT_or_other_default_invented'] is False,
        'Actual CC-BY authored grant without separate invented code license')
require(rights['explicit_printed_version'] is None
        and rights['native_API_version']=='1.0'
        and rights['printed_version_source_statement_original']==ready['printed_version']
        and rights['declared_publication_date']=='2026-10-14',
        'Unprinted version and exact original date preserved')
require(rights['current_publication_or_AA_authority'] is False and rights['follow_up'] is None,
        'No public-stage authority or invented followup')
for copy in protocol['byte_identical_raw_copies']:
    original,owned=Path(copy['original_path']),OWN/copy['owned_copy_relative_path']
    require(original.stat().st_size==copy['bytes'] and sha(original)==copy['sha256']
            and owned.read_bytes()==original.read_bytes(),
            'Raw byte-identical copy '+copy['owned_copy_relative_path'])

# Bounded metadata falsifiers; all altered data stays in memory.
m=deepcopy(receipts);m.pop(0);reject('discard first403 failure',strict(m,receipts))
m=deepcopy(receipts);m[2]['redirect_hops']=[];reject('discard latest301 hop',strict(m,receipts))
m=deepcopy(receipts);m[-1]['headers_in_received_order']=dict(m[-1]['headers_in_received_order']);reject('flatten duplicate ordered headers',strict(m,receipts))
m=deepcopy(versions);m['hits']['hits'][0]['swh']={};reject('coerce version null to empty object',strict(m,versions))
m=deepcopy(files);m['order']=None;reject('coerce files empty list to null',strict(m,files))
reject('coerce bool to int',strict(True,1))
m=deepcopy(assets);m.reverse();reject('reverse native PDF-ZIP order',strict(m,assets))
m=deepcopy(rights);m['explicit_printed_version']='1.0';reject('invent printed version',strict(m,rights))
m=deepcopy(rights);m['declared_publication_date']='2026-10-15';reject('replace declared date by created date',strict(m,rights))
m=deepcopy(rights);m['authored_materials_license']='MIT';reject('invent MIT default',strict(m,rights))
m=deepcopy(peers);m[2]['whole_literal_original_object']['literal_custom_verdict']='PASS';reject('normalize whole custom verdict to PASS',strict(m,peers))
m=deepcopy(rights);m['current_publication_or_AA_authority']=True;reject('premature public authority',strict(m,rights))

print(json.dumps({'status':'PASS_BOUNDED_SOURCE_METADATA_CUSTODY_118',
                  'record_id':23385145,'checks':len(checks),
                  'immutable_preexisting_files_guarded':len(guard['files']),
                  'complete_native_API_objects':4,'whole_transport_objects':7,
                  'whole_literal_scientific_verdicts':3,'raw_byte_copies':len(protocol['byte_identical_raw_copies']),
                  'native_ZIP_payloads_checked':93,'negative_controls_rejected':len(controls),
                  'negative_controls':controls,'strict_types_key_order_list_header_order':True,
                  'preexisting_writes':False,'network_or_browser':False,
                  'scientific_code_or_old_content_verifier_executed':False,
                  'publication_configs_or_public_copy_authored':False,
                  'public_or_AA_or_current_stage_integration_authority':False},indent=2))
