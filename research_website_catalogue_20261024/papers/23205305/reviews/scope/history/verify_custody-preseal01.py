#!/usr/bin/env python3
"""Read-only source/initial/primary/final custody. No scientific execution.
No project imports, subprocesses, network, writes, website or tracker access.
Default requires the sealed complete namespace; --preseal checks frozen inputs.
Only exact root MANIFEST.json and FINAL_SEAL.json are final terminal exclusions.
"""
from pathlib import Path
import hashlib
import io
import json
import sys
import zipfile

E=Path(__file__).resolve().parent
checks=0
def require(ok,message):
    global checks
    checks+=1
    if not ok:raise ValueError(message)
def sha(b):return hashlib.sha256(b).hexdigest()
def readj(p):return json.loads(p.read_bytes())
def binding(p,row):
    require(p.is_file() and not p.is_symlink(),'regular file: '+str(p))
    b=p.read_bytes()
    require(len(b)==row['bytes'] and sha(b)==row['SHA256'],'byte binding: '+str(p))
    return b
def typed(x):
    if isinstance(x,dict):return ('dict',tuple((k,typed(v)) for k,v in x.items()))
    if isinstance(x,list):return ('list',tuple(typed(v) for v in x))
    return (type(x).__name__,x)
def namespace(base):
    files=[];dirs=[]
    for p in base.rglob('*'):
        require(not p.is_symlink(),'symlink forbidden: '+str(p))
        if p.is_file():files.append(p.relative_to(base).as_posix())
        elif p.is_dir():dirs.append(p.relative_to(base).as_posix())
        else:require(False,'nonregular entry: '+str(p))
    return sorted(files),sorted(dirs)

require(sys.argv[1:] in ([],['--preseal']),'only optional --preseal is accepted')
preseal=sys.argv[1:]==['--preseal']
initial_bytes=(E/'INITIAL_SEAL.json').read_bytes()
require(sha(initial_bytes)=='8fc4d01576ac71649627f80fec848ca6050c25f829c0a3e3aaff5a1660b79471','initial seal')
initial=json.loads(initial_bytes)
require(len(initial['payloads'])==154,'complete initial payload count')
for name,row in initial['payloads'].items():binding(E/name,row)
protected=readj(E/'PROTECTED_INPUTS.json')
require(len(protected['files'])==144,'source126 plus qualified core18')
for row in protected['files']:
    binding(Path(row['path']),row)
    binding(E/row['copy'],row)
ns=protected['source_namespace'];files,dirs=namespace(Path(ns['path']))
require(files==ns['files'] and dirs==ns['directories'],'complete live source namespace')
require(len(files)==126,'complete source126')
require(len(protected['core_files'])==18,'17original plus one authorized helper')
checkpoint=[r for r in protected['files'] if r['path'].endswith('/scripts/checkpoint_subtree.py')]
require(len(checkpoint)==1 and checkpoint[0]['SHA256']=='405b0357fd20a2e14893ce6c3c1a0f81910894ccd8ffaddac4e25014138fb9c0','sole separately authorized checkpoint helper')

protocol=readj(E/'SOURCE_PROTOCOL_BINDINGS.json')
wrappers=[protocol['whole_SOURCE_READY']]+protocol['whole_native_API_objects_in_original_role_order']
wrappers += [v for k,v in protocol.items() if k not in ('whole_SOURCE_READY','whole_native_API_objects_in_original_role_order')]
for row in wrappers:
    b=binding(E/row['copy'],row)
    require(typed(json.loads(b))==typed(row['whole_literal_object']),'whole literal object including key order/types/nulls')
require([r['role'] for r in protocol['whole_native_API_objects_in_original_role_order']]==['record','latest','versions-page001','files'],'actual API role order')
ready=protocol['whole_SOURCE_READY']['whole_literal_object']
require(ready['native_version_whole_field']=={'present':False,'original_value':None},'native version remains absent')
require(ready['mathematical_PDF_TeX_or_pixels_read'] is False and ready['source_programmes_executed'] is False,'historical source flags remain literal')
assets=ready['all_native_assets_in_original_order']
require([a['original_api_file_object']['key'] for a in assets]==['source.zip','verification.zip','paper.pdf','height-repair.pdf'],'native asset order')
for a in assets:binding(Path(a['path']),a)

archive=protocol['ARCHIVE_CUSTODY.json']['whole_literal_object'];payloads=0
for container in archive['containers']:
    raw=Path(container['input_path']).read_bytes()
    require(len(raw)==container['input_bytes'] and sha(raw)==container['input_SHA256'],'whole native ZIP')
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        infos=z.infolist();members=container['members']
        require([i.filename for i in infos if not i.is_dir()]==[m['original_member_name'] for m in members],'whole regular member order')
        require(z.comment.hex()==container['original_archive_comment_hex'],'archive comment')
        for m in members:
            info=z.getinfo(m['original_member_name']);body=z.read(info)
            require(info.CRC==int(m['CRC32'],16) and len(body)==m['bytes'] and sha(body)==m['SHA256'],'CRC/size/SHA whole native payload')
            require(Path(m['extracted_path']).read_bytes()==body,'whole extracted payload equals native')
            require(info.compress_size==m['compressed_bytes'] and info.compress_type==m['compression_method'] and info.external_attr==m['native_external_attr'] and info.create_system==m['native_create_system'] and info.flag_bits==m['native_flags'] and list(info.date_time)==m['native_date_time'],'literal ZIP central fields')
            payloads+=1
require(payloads==61 and len(archive['containers'])==2,'two containers/61 regular payloads')

# The whole transport JSON is final-manifest bound. Here verify each actual
# response body; retain failures/null status and every ordered header array.
transports=sorted((E/'primary').glob('*.transport.json'))
for path in transports:
    row=readj(path)
    require(isinstance(row['actual_request_headers_in_sent_order'],list),'ordered request headers')
    if row.get('body') is not None:
        binding(E/row['body'],row)
        require(isinstance(row['response_headers_in_received_order'],list),'ordered response headers')
    else:
        require(row.get('HTTP_status') is None and row.get('error') is not None,'literal failed transport')
for n in range(1,5):
    handoff=readj(E/('RAW_PRIMARY_HANDOFF_0'+str(n)+'.json'))
    require(handoff['raw_only_no_findings_or_control_results'] is True,'raw-only handoff')
    for row in handoff['records']:
        if row.get('raw_body_path') is not None:binding(Path(row['raw_body_path']),row)

control=readj(E/'CONTROL_COMPARISON.json')
require(control['normal']['process_exit_code']==0 and control['optimized']['process_exit_code']==0,'actual own control exits')
require(control['normal']['optimization_flag']==0 and control['optimized']['optimization_flag']==1,'flags are distinct from exits')
normal=binding(E/control['normal']['stdout']['path'],control['normal']['stdout'])
optimized=binding(E/control['optimized']['stdout']['path'],control['optimized']['stdout'])
require(normal==optimized and control['whole_stdout_byte_identity'] is True,'actual complete output identity')
for mode in ('normal','optimized'):
    require(binding(E/control[mode]['stderr']['path'],control[mode]['stderr'])==b'','actual control stderr')
require(json.loads(normal)['checks']==256,'bounded new controls count, no native replay')
verdict=readj(E/'CUSTOM_VERDICT.json')
require(verdict['record_id']==23205305 and verdict['followup'] is None,'own unique verdict identity and followup')
require(verdict['canonical_AA_assignment_authority'] is False and verdict['publication_authority'] is None,'no publication or tracker authority')

final_files=None
if not preseal:
    manifest_bytes=(E/'MANIFEST.json').read_bytes();seal=readj(E/'FINAL_SEAL.json')
    require(len(manifest_bytes)==seal['manifest']['bytes'] and sha(manifest_bytes)==seal['manifest']['SHA256'],'final manifest seal')
    manifest=json.loads(manifest_bytes);actual_files,actual_dirs=namespace(E)
    require(manifest['only_exact_root_terminal_exclusions']==['FINAL_SEAL.json','MANIFEST.json'],'exact root exclusions')
    require(sorted(set(actual_files)-{'FINAL_SEAL.json','MANIFEST.json'})==sorted(manifest['payloads']),'strict entire final file namespace')
    require(actual_dirs==manifest['directories'],'strict entire final directory namespace')
    for name,row in manifest['payloads'].items():binding(E/name,row)
    require(typed(verdict)==typed(seal['whole_literal_CUSTOM_VERDICT']),'whole custom verdict in seal')
    final_files=len(actual_files)
print(json.dumps({'schema':'scope23205305-readonly-custody-v1','mode':'preseal' if preseal else 'final',
 'checks':checks,'source_namespace_files':len(files),'qualified_core_inputs':18,
 'initial_payloads':154,'native_ZIP_regular_payloads':payloads,
 'primary_transport_receipts':len(transports),'final_namespace_files':final_files,
 'scientific_programmes_or_project_imports_or_network_subprocesses_writes':False},indent=2))
