"""Trusted external validator for pinned data-only archives. Never executes payloads."""
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import zipfile

def require(condition, message):
    if not condition:
        raise ValueError(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate JSON key')
        result[key] = value
    return result

def parse(data):
    return json.loads(data.decode('utf-8'), object_pairs_hook=unique_object,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError('nonfinite JSON')))

def validate_record(row):
    require(isinstance(row, dict) and set(row) == {'path','bytes','sha256'}, 'bad member record')
    name=row['path']
    require(isinstance(name,str) and name and '/' not in name and '\\' not in name
            and name not in {'.','..'} and not PurePosixPath(name).is_absolute(), 'unsafe member path')
    require(Path(name).suffix in {'.md','.json','.txt'}, 'nondata member extension')
    require(type(row['bytes']) is int and 0 <= row['bytes'] <= 1048576, 'bad member size')
    require(isinstance(row['sha256'],str) and re.fullmatch('[0-9a-f]{64}',row['sha256']) is not None,'bad digest')

def run(archive_name, manifest_name, expected_archive_sha, expected_manifest_sha):
    archive=Path(archive_name); manifest=Path(manifest_name)
    require(not archive.is_symlink() and archive.is_file(), 'archive must be regular')
    require(not manifest.is_symlink() and manifest.is_file(), 'manifest must be regular')
    require(archive.stat().st_size <= 2097152 and manifest.stat().st_size <= 1048576, 'oversize outer input')
    raw=archive.read_bytes(); mraw=manifest.read_bytes()
    require(digest(raw)==expected_archive_sha, 'archive pin mismatch')
    require(digest(mraw)==expected_manifest_sha, 'manifest pin mismatch')
    ext=parse(mraw)
    require(ext.get('data_only') is True, 'data-only flag required')
    require(ext['archive']=={'name':archive.name,'bytes':len(raw),'sha256':expected_archive_sha}, 'archive binding mismatch')
    rows=ext['members']; require(isinstance(rows,list) and 0<len(rows)<=64,'bad inventory')
    for row in rows: validate_record(row)
    names=[x['path'] for x in rows]
    require(len(names)==len(set(names))==len(set(x.casefold() for x in names)), 'duplicate manifest member')
    require('MANIFEST.json' in names,'missing embedded manifest')
    payload={}
    with zipfile.ZipFile(archive) as z:
        require(not z.comment,'unexpected archive comment')
        infos=z.infolist(); znames=[i.filename for i in infos]
        require(len(znames)==len(set(znames)), 'duplicate ZIP member')
        require(set(znames)==set(names),'strict inventory mismatch')
        for i in infos:
            require(i.create_system==3 and stat.S_ISREG(i.external_attr>>16), 'nonregular member')
            require(not ((i.external_attr>>16)&0o111),'executable member')
            require(not (i.flag_bits&1),'encrypted member')
            require(not i.comment and not i.extra, 'unexpected hidden member metadata')
            row=next(x for x in rows if x['path']==i.filename)
            require(i.file_size==row['bytes'], 'ZIP size mismatch')
            b=z.read(i); require(len(b)==row['bytes'] and digest(b)==row['sha256'],'member binding mismatch')
            b.decode('utf-8')
            if i.filename.endswith('.json'): parse(b)
            payload[i.filename]=b
    embedded=parse(payload['MANIFEST.json'])
    require(embedded.get('executable_code') is False and embedded.get('formal_proof_checker') is False,'bad embedded flags')
    inner=embedded['files']; require(isinstance(inner,list),'bad inner inventory')
    for row in inner: validate_record(row)
    inames=[x['path'] for x in inner]
    require(len(inames)==len(set(inames)), 'duplicate inner inventory')
    require(sorted(inner,key=lambda x:x['path'])==sorted([x for x in rows if x['path']!='MANIFEST.json'],key=lambda x:x['path']), 'embedded inventory mismatch')
    return {'status':'PASS_DATA_ONLY_INTEGRITY','archive_sha256':expected_archive_sha,
            'manifest_sha256':expected_manifest_sha,'members':len(rows),'strict_inventory':True,
            'all_regular_nonexecutable':True,'embedded_manifest_matches':True,
            'payload_code_executed':False,'mathematics_formally_verified':False}

if __name__=='__main__':
    try:
        require(len(sys.argv)==5,'usage: validator archive manifest archive-sha256 manifest-sha256')
        result=run(*sys.argv[1:]); print(json.dumps(result,sort_keys=True))
    except Exception as exc:
        print(json.dumps({'status':'REJECT','reason':str(exc)},sort_keys=True)); sys.exit(1)
