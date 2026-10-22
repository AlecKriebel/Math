#!/usr/bin/env python3
"""Independent read-only streaming replay verification. Never extract archives."""
from pathlib import Path,PurePosixPath
import datetime,decimal,gzip,hashlib,json,lzma,stat,tarfile
HERE=Path(__file__).resolve().parent;OPS=HERE.parent/'operations'
def need(v,m):
    if not v:raise RuntimeError(m)
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def stamp():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def canonical(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def name(s):
    p=PurePosixPath(s);need(s=='payload' or s.startswith('payload/'),'Unexpected archive prefix')
    need(not p.is_absolute() and not any(x in {'.','..'} for x in p.parts) and '\\' not in s and '\0' not in s,'Unsafe archive path')
    return '' if s=='payload' else s[8:]
custody=json.loads((OPS/'REPLAY_ARCHIVE_CUSTODY.json').read_bytes());results=[];began=stamp()
for a in custody['archives']:
    archive=OPS/a['archive']['path'];invpath=OPS/a['inventory']['path']
    need(pin(archive.read_bytes())=={k:a['archive'][k] for k in ('bytes','sha256')},'Compressed archive pin')
    raw=invpath.read_bytes();need(pin(raw)=={k:a['inventory'][k] for k in ('bytes','sha256')},'Compressed inventory pin')
    inv=json.loads(lzma.decompress(raw));entries=inv['entries'];table={e['path']:e for e in entries}
    need(len(table)==len(entries)==a['original_entries'],'Inventory entry count')
    need(hashlib.sha256(canonical(entries)).hexdigest()==inv['canonical_inventory_sha256']==a['original_path_type_mode_mtime_bytes_sha256'],'Canonical full inventory')
    seen={};hardlinks=0;bytes_read=0
    with tarfile.open(archive,'r|gz') as tar:
        for m in tar:
            n=name(m.name);need(n in table and n not in seen,'Archive membership/duplicate');e=table[n]
            need(stat.S_IMODE(m.mode)==e['mode'],'Archive mode')
            need(int(decimal.Decimal(m.pax_headers.get('mtime',str(m.mtime)))*1000000000)==e['mtime_ns'],'Exact nanosecond archive mtime')
            if m.isdir():need(e['type']=='directory','Archive directory type');seen[n]={'type':'directory'}
            elif m.islnk():
                target=name(m.linkname);need(target in seen and seen[target]['type']=='file' and e['type']=='file','Hardlink target/type')
                actual={k:seen[target][k] for k in ('bytes','sha256')};need(actual=={k:e[k] for k in actual},'Hardlink byte pin');seen[n]={'type':'file',**actual};hardlinks+=1
            else:
                need(m.isfile() and e['type']=='file','Non-regular archive member');f=tar.extractfile(m);h=hashlib.sha256();size=0
                while True:
                    b=f.read(1048576)
                    if not b:break
                    h.update(b);size+=len(b)
                actual={'bytes':size,'sha256':h.hexdigest()};need(actual=={k:e[k] for k in actual},'Archive payload pin');seen[n]={'type':'file',**actual};bytes_read+=size
    need(set(seen)==set(table),'Full archive closure')
    with gzip.open(archive,'rb') as f:
        while f.read(1048576):pass
    results.append({'root':a['root'],'entries':len(entries),'hardlinks':hardlinks,'streamed_regular_file_bytes':bytes_read,'archive_sha256':a['archive']['sha256'],'canonical_inventory_sha256':inv['canonical_inventory_sha256'],'exact_ns_mtime_and_modes_and_bodies':True,'gzip_CRC':True})
    print(json.dumps({'verified':a['root'],'entries':len(entries)}),flush=True)
result={'at':stamp(),'started':began,'archives':results,'archive_count':len(results),'no_extraction_or_source_mutation':True,'publication_ready':False}
(HERE/'ARCHIVE_VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n')
