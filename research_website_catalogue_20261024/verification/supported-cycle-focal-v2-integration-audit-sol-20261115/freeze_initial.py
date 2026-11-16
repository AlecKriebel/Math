#!/usr/bin/env python3
"""One-time source/prior-packet custody capture; no V2 writer or website access."""
from pathlib import Path
import hashlib
import json
import stat
from datetime import datetime, timezone

BASE = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
OWN = Path(__file__).resolve().parent
OLD_AUDIT = BASE/'verification/supported-cycle-focal-independent-code-audit-sol-20261115'
OLD_WRITER = BASE/'verification/supported-cycle-focal-private-stage-sol-20261115'

def require(test, message):
    if not test:
        raise RuntimeError(message)

def read(path):
    require(stat.S_ISREG(path.lstat().st_mode), 'not ordinary file: '+str(path))
    return path.read_bytes()

def pin(raw):
    return {'bytes': len(raw), 'SHA256': hashlib.sha256(raw).hexdigest()}

def dump(name, obj):
    dest = OWN/name
    require(not dest.exists() and not dest.is_symlink(), 'destination exists: '+str(dest))
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes((json.dumps(obj, ensure_ascii=False, indent=2)+'\n').encode())

def extent(root):
    require(stat.S_ISDIR(root.lstat().st_mode), 'not ordinary root')
    files, dirs = {}, []
    for p in root.rglob('*'):
        rel=p.relative_to(root).as_posix()
        mode=p.lstat().st_mode
        if stat.S_ISDIR(mode):
            dirs.append(rel)
        else:
            require(stat.S_ISREG(mode), 'nonregular namespace entry: '+str(p))
            require(rel not in files, 'duplicate file')
            files[rel]=pin(read(p))
    return {'root': str(root), 'files': dict(sorted(files.items())), 'directories': sorted(dirs)}

def authenticate_old(root, expected, manifest_name, manifest_sha):
    require(pin(read(root/'FINAL_SEAL.json'))['SHA256']==expected, 'old final pin')
    require(pin(read(root/manifest_name))['SHA256']==manifest_sha, 'old manifest pin')
    m=json.loads(read(root/manifest_name))
    records=m.get('payloads')
    if records is None:
        paths=[r['path'] for r in m['files']]
        require(len(paths)==len(set(paths)), 'duplicate manifest files')
        records={r['path']: {'bytes':r['bytes'],'SHA256':r['SHA256']} for r in m['files']}
    actual=extent(root)
    terminals=[manifest_name,'FINAL_SEAL.json']
    expected_names=list(records)+terminals
    require(len(expected_names)==len(set(expected_names)), 'terminal overlap')
    require(sorted(actual['files'])==sorted(expected_names), 'old exact file closure')
    require(actual['directories']==sorted(m['directories']), 'old exact directory closure')
    for name, record in records.items():
        require(actual['files'][name]==record, 'old payload mismatch: '+name)
    return actual

def copy(source, relative):
    raw=read(source)
    dest=OWN/'inputs'/relative
    require(not dest.exists(), 'copy already exists')
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_bytes(raw)
    bindings.append({'source':str(source),'copy':dest.relative_to(OWN).as_posix(),**pin(raw)})

def typed(left,right,path='root'):
    require(type(left) is type(right), 'type mismatch '+path)
    if isinstance(left,dict):
        require(list(left)==list(right), 'key/order mismatch '+path)
        for k in left: typed(left[k],right[k],path+'/'+k)
    elif isinstance(left,list):
        require(len(left)==len(right), 'array size '+path)
        for i,(a,b) in enumerate(zip(left,right)):typed(a,b,path+'/'+str(i))
    else: require(left==right,'scalar mismatch '+path)

require(OWN==BASE/'verification/supported-cycle-focal-v2-integration-audit-sol-20261115','own namespace')
require(not (OWN/'INITIAL_SEAL.json').exists(), 'initial already frozen')
bindings=[]
old_audit=authenticate_old(OLD_AUDIT,'780e71570c61a0604c582b2a851b4fe8165105652ddf46446c06182995f36412','FINAL_MANIFEST.json','28bc99a4dd4ff2ec4916e7936a6c1c3681c6d18f8387047aa57032f662468b43')
old_writer=authenticate_old(OLD_WRITER,'edf8e4e64ea345e950f6d94e678b4d6c8530df37089e80ef6681a519b7fedf54','OWNED_MANIFEST.json','614e78a7b4f8ab357d93d36dba8f330ecc27297608c37eb4617cb7d4d4396b4b')
dump('PRIOR_CLOSED_EXTENTS.json',[old_audit,old_writer])
source_extents=[]
for record in ['23578142','23306203']:
    paper=BASE/'papers'/record
    source_extents.extend([extent(paper/'sources'),extent(paper/'reviews/editorial')])
    for name in ['SOURCE_READY.json','SOURCE_READY_SEAL.json','SOURCE_READY_MANIFEST.json','record.response.body','latest.response.body','latest.response.body.redirect-01','versions-page001.response.body','files.response.body','ALL_TRANSPORT_RECEIPTS.json','NATIVE_SCHEMA_TYPES.json','ACQUIRED_NATIVE.json','ARCHIVE_CUSTODY.json','MANUSCRIPT_CUSTODY.json']:
        copy(paper/'sources'/name,Path(record)/'sources'/name)
    for name in ['PUBLIC_MAIN.html','RIGHTS_AND_IDENTITY.json','SCHOLARLY_METADATA.json','SCHEMA_ADAPTER.json','PUBLICATION_REQUIREMENTS.json','citation.bib','publication.json','promotion.json']:
        copy(paper/'reviews/editorial'/name,Path(record)/'editorial'/name)
    source=paper/'sources'
    r=json.loads(read(source/'record.response.body'))
    typed(r,json.loads(read(source/'latest.response.body.redirect-01')))
    require(read(source/'record.response.body')==read(source/'latest.response.body.redirect-01'),'latest raw differs')
    v=json.loads(read(source/'versions-page001.response.body'))
    require(list(v)==['hits','links'] and v['hits']['total']==1 and type(v['hits']['total']) is int,'version envelope')
    require(len(v['hits']['hits'])==1 and list(v['hits']['hits'][0])==list(r),'version order')
    expected=json.loads(read(source/'record.response.body')); expected['swh']=None
    typed(expected,v['hits']['hits'][0])
    for asset in r['files']:
        copy(source/'assets'/asset['key'],Path(record)/'assets'/asset['key'])
    rights=json.loads(read(paper/'reviews/editorial/RIGHTS_AND_IDENTITY.json'))
    if record=='23578142':
        for role in ['original_prose_license','original_code_license']:
            item=rights[role];require(read(Path(item['path'])).decode()==item['whole_literal_text'],'actual license binding')
            copy(Path(item['path']),Path(record)/'rights'/Path(item['path']).name)
    else:
        license_path=source/'published-source/asset-001/LICENSE.md'
        require(read(license_path).decode()==rights['whole_original_license_text'],'actual broad license binding')
        copy(license_path,Path(record)/'rights/LICENSE.md')
        for name in ['ORIGINAL_PRINTED_ABSTRACT.tex','NATIVE_DEPOSIT_DESCRIPTION.html']:
            copy(paper/'reviews/editorial'/name,Path(record)/'editorial'/name)
    copy(BASE/'verification'/('root-editorial-'+record+'-20261115.json'),Path('root')/('root-editorial-'+record+'.json'))
dump('SOURCE_CLOSED_EXTENTS.json',source_extents)
for name in ['REPORT.md','VERDICT.json','INITIAL_EXPECTATIONS.json','BASELINE_FRAME_EXPECTATIONS.json','ACTUAL623_QUALIFIED_CORE.json','EXPECTED_SOURCE_OBJECTS.json','SOURCE_ROOT_BINDINGS.json','FINAL_SEAL.json','FINAL_MANIFEST.json']:
    copy(OLD_AUDIT/name,Path('prior-audit')/name)
for name in ['ADAPTER_REQUIREMENTS.json','OVERLAY_MANIFEST.json','INSTALLATION_PLAN.json','FINAL_SEAL.json','OWNED_MANIFEST.json']:
    copy(OLD_WRITER/name,Path('prior-writer')/name)
overlay=json.loads(read(OLD_WRITER/'OVERLAY_MANIFEST.json'))
for item in overlay['files']:
    rel=item['path']
    a=read(OLD_WRITER/'candidate-a/public'/rel)
    require(a==read(OLD_WRITER/'candidate-b/public'/rel),'old pair mismatch')
    require(pin(a)=={'bytes':item['bytes'],'SHA256':item['SHA256']},'old output pin')
    copy(OLD_WRITER/'candidate-a/public'/rel,Path('prior-outputs')/rel)
copy(BASE/'verification/root-supported-cycle-focal-corrective-private-v2-authorization-20261115.json',Path('root/corrective-authorization.json'))
dump('INPUT_BINDINGS.json',bindings)
print(json.dumps({'status':'SOURCE_AND_PRIOR_ONLY_CUSTODY_FROZEN','source_namespace_file_counts':[len(x['files']) for x in source_extents],'prior_closed_files':[len(old_audit['files']),len(old_writer['files'])],'literal_selected_copies':len(bindings),'new_V2_writer_exposed':False,'actual_website_or_Git_access':False,'scientific_execution':False}))
