"""Safe complete archive-byte custody. Does not interpret or execute contents."""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
from hashlib import sha256
import io
import json
import stat
import tarfile
import unicodedata
import zipfile
import zlib

HERE=Path(__file__).resolve().parent
containers=[]
payloads=[]


def safe(names):
    seen=set()
    for name in names:
        p=PurePosixPath(name)
        if p.is_absolute() or '..' in p.parts or '\\' in name or ':' in name or not p.parts:
            raise ValueError('unsafe member name: '+repr(name))
        fold=unicodedata.normalize('NFC',name).casefold()
        if fold in seen:raise ValueError('duplicate/case-colliding member name')
        seen.add(fold)


def kind(body,name):
    if zipfile.is_zipfile(io.BytesIO(body)):return 'zip'
    if body[257:262]==b'ustar' or name.lower().endswith(('.tar','.tgz','.tar.gz','.txz','.tar.xz','.tbz2','.tar.bz2')):
        try:
            with tarfile.open(fileobj=io.BytesIO(body),mode='r:*'):return 'tar'
        except tarfile.TarError:raise ValueError('archive-like member failed native parse')
    return None


def scan(path,depth,archive_kind,root):
    identifier='container-%03d'%(len(containers)+1)
    if root is None:root=HERE/'nested'/identifier
    native=path.read_bytes()
    item={'container_id':identifier,'container_path':str(path),'depth':depth,
          'archive_kind':archive_kind,'bytes':len(native),'SHA256':sha256(native).hexdigest(),
          'extraction_root':str(root)}
    containers.append(item)
    pending=[]
    if archive_kind=='zip':
        with zipfile.ZipFile(io.BytesIO(native)) as archive:
            members=archive.infolist();safe([m.filename for m in members])
            for ordinal,m in enumerate(members):
                mode=stat.S_IFMT(m.external_attr>>16)
                if m.flag_bits&1:raise ValueError('encrypted member')
                if m.is_dir():
                    if mode not in (0,stat.S_IFDIR):raise ValueError('non-directory mode')
                    continue
                if mode not in (0,stat.S_IFREG):raise ValueError('nonregular archive member')
                body=archive.read(m)
                if len(body)!=m.file_size or (zlib.crc32(body)&0xffffffff)!=m.CRC:
                    raise ValueError('native size/CRC mismatch')
                target=root/m.filename
                target.parent.mkdir(parents=True,exist_ok=True)
                with target.open('xb') as out:out.write(body)
                nested=kind(body,m.filename)
                rec={'container_id':identifier,'container_depth':depth,'ordinal_zero_based':ordinal,
                     'original_member_name':m.filename,'canonical_extraction_relative_path':m.filename,
                     'extracted_path':str(target),'bytes':len(body),'SHA256':sha256(body).hexdigest(),
                     'CRC32':'%08x'%m.CRC,'compressed_bytes':m.compress_size,
                     'zip_flags':m.flag_bits,'compression_method':m.compress_type,
                     'native_external_attr':m.external_attr,'native_date_time':list(m.date_time),
                     'safe_regular_body':True,'nested_archive_kind':nested}
                payloads.append(rec)
                if nested:pending.append((target,depth+1,nested,None))
    else:
        with tarfile.open(fileobj=io.BytesIO(native),mode='r:*') as archive:
            members=archive.getmembers();safe([m.name for m in members])
            for ordinal,m in enumerate(members):
                if m.isdir():continue
                if not m.isfile():raise ValueError('nonregular tar member')
                body=archive.extractfile(m).read()
                if len(body)!=m.size:raise ValueError('native tar size mismatch')
                target=root/m.name;target.parent.mkdir(parents=True,exist_ok=True)
                with target.open('xb') as out:out.write(body)
                nested=kind(body,m.name)
                payloads.append({'container_id':identifier,'container_depth':depth,
                  'ordinal_zero_based':ordinal,'original_member_name':m.name,
                  'canonical_extraction_relative_path':m.name,'extracted_path':str(target),
                  'bytes':len(body),'SHA256':sha256(body).hexdigest(),'native_mode':m.mode,
                  'native_mtime':m.mtime,'native_type_hex':m.type.hex(),
                  'safe_regular_body':True,'nested_archive_kind':nested})
                if nested:pending.append((target,depth+1,nested,None))
    item['native_members_including_directories']=len(members)
    for task in pending:scan(*task)


if __name__=='__main__':
    started=datetime.now(timezone.utc).isoformat()
    target=HERE/'archive-custody.json'
    if target.exists():raise FileExistsError(str(target))
    scan(HERE/'assets/cellularization-vanishing-source-and-verification.zip',0,'zip',HERE/'published-source')
    result={'started_UTC':started,'completed_UTC':datetime.now(timezone.utc).isoformat(),
       'containers':containers,'all_safe_regular_occurrences':payloads,
       'safe_regular_occurrences':len(payloads),
       'expanded_bytes_all_depths':sum(p['bytes'] for p in payloads),
       'archive_containers':len(containers),'nested_archives':len(containers)-1,
       'unsafe_names':[],'duplicate_or_case_colliding_names':[],'nonregular_payloads':[],
       'all_native_CRC_size_SHA256_and_whole_extracted_bytes_verified':True,
       'source_scientifically_read_or_executed':False}
    target.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('containers','all_safe_regular_occurrences')},indent=2))
