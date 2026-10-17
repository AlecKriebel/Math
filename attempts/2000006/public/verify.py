#!/usr/bin/env python3
"""Optimization-independent, read-only payload and acceptance-chain verifier."""
from pathlib import Path, PurePosixPath
import hashlib,json,re
ROOT=Path(__file__).resolve().parent


def require(condition, detail):
    if not condition:
        raise ValueError(str(detail))


def bound_entries(o):
    if isinstance(o,dict):
        if {'path','bytes','sha256'}<=o.keys():yield o
        for v in o.values():yield from bound_entries(v)
    elif isinstance(o,list):
        for v in o:yield from bound_entries(v)


def validate_record(e):
    require(isinstance(e,dict),'file record must be an object')
    require(isinstance(e.get('path'),str),'file path must be a string')
    name=e['path'];rel=PurePosixPath(name)
    require(bool(name) and not rel.is_absolute() and '..' not in rel.parts and name==rel.as_posix() and '\\' not in name and all(ord(c)>=32 for c in name),('unsafe file path',name))
    require(type(e.get('bytes')) is int and e['bytes']>=0,('invalid byte count',name))
    require(isinstance(e.get('sha256'),str) and re.fullmatch('[0-9a-f]{64}',e['sha256']) is not None,('invalid SHA-256',name))
    return Path(name)


def check_record(base,e):
    rel=validate_record(e);p=base/rel
    require(p.is_file() and not p.is_symlink(),('missing or nonregular file',e['path']))
    data=p.read_bytes()
    require(len(data)==e['bytes'],(e['path'],'byte count'))
    require(hashlib.sha256(data).hexdigest()==e['sha256'],(e['path'],'SHA-256'))


def verify():
    require(not any(p.is_symlink() for p in ROOT.rglob('*')),'symlinks are not permitted')
    manifest=json.loads((ROOT/'PACKAGE_MANIFEST.json').read_text())
    require(isinstance(manifest,dict),'manifest must be an object')
    for key,value in {'schema_version':1,'problem':'E-6322','source_code':'AMR-019-0006','queue_row':1791,'terminal_status':'UNSOLVED 5/5','benchmark_proved':False,'benchmark_counterexample':False,'source_documents_included':False,'private_coordination_included':False,'dataset_contents_included':False}.items():
        require(type(manifest.get(key)) is type(value) and manifest.get(key)==value,('manifest scope field',key))
    payload=manifest.get('files');originals=manifest.get('original_artifacts')
    require(isinstance(payload,list) and len(payload)>0,'files must be a nonempty list')
    require(isinstance(originals,list) and len(originals)==109,'109 original artifacts required')
    for e in payload+originals:validate_record(e)
    expected={e['path'] for e in payload}
    require(len(expected)==len(payload),'duplicate manifest path')
    require('PACKAGE_MANIFEST.json' not in expected,'manifest cannot list itself')
    require(len({e['path'] for e in originals})==109,'duplicate original artifact')
    actual={str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file()}
    wanted=expected|{'PACKAGE_MANIFEST.json'}
    require(actual==wanted,('unexpected/missing files',sorted(actual^wanted)))
    for e in payload:
        check_record(ROOT,e);p=Path(e['path'])
        require(not {'private_sources','__pycache__','queue_preview'}&set(p.parts),('excluded directory',str(p)))
        require(p.suffix in {'.md','.json','.py'} or str(p) in {'requirements.txt','.gitignore'},('excluded file type',str(p)))
        data=(ROOT/p).read_text()
        for token in ('/'+'workspace/','codex'+':/'+'/', 'chatgpt.com/'+'c/','chatgpt.com/'+'share/','agent_'+'notes/','BEGIN '+'PRIVATE KEY','api_'+'key='):
            require(token not in data,(str(p),'excluded content marker',token))
    for e in originals:
        require(e['path'] in expected,('original missing from payload',e['path']))
        check_record(ROOT,e)
    chain=[]
    for n,count in enumerate((19,21,23,22,30),1):
        p=ROOT/f'research_elasticity_1791_pass{n}_20261016/audit/AUDIT_MANIFEST.json'
        entries=list(bound_entries(json.loads(p.read_text())))
        require(len(entries)==count,('unexpected original-chain record count',n))
        for e in entries:check_record(ROOT,e)
        chain.append({'pass':n,'verified_record_occurrences':len(entries)})
    return {'status':'pass','problem':'E-6322','terminal_status':'UNSOLVED 5/5','payload_files':len(payload),'payload_bytes':sum(e['bytes'] for e in payload),'unchanged_original_artifacts':len(originals),'original_audit_chain':chain,'optimization_independent_gates':True,'private_or_third_party_source_files_included':False,'benchmark_proved':False,'benchmark_counterexample':False}

if __name__=='__main__':print(json.dumps(verify(),indent=2))
