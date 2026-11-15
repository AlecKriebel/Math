"""Acquisition only: opaque bytes, ZIP/tar metadata, CRC/hash and safe extraction."""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
import hashlib
import io
import json
import stat
import tarfile
import urllib.request
import zipfile

A=Path(__file__).resolve().parent
S=A.parent/'sources'
MAX_ASSET=50*1024*1024
MAX_EXPANDED=100*1024*1024
rows=[]
containers=[]
expanded=0


def now(): return datetime.now(timezone.utc).isoformat()
def require(x,m):
    if not x: raise RuntimeError(m)
def sha(b): return hashlib.sha256(b).hexdigest()
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def safe(name):
    p=PurePosixPath(name)
    require(name and '\x00' not in name and '\\' not in name and not p.is_absolute()
            and '..' not in p.parts,'unsafe archive path')
    return p


def unpack(data,container,dest,depth=0):
    global expanded
    require(depth<=5,'nested archive depth')
    if zipfile.is_zipfile(io.BytesIO(data)):
        kind='zip'
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            infos=z.infolist(); seen=set()
            require(sum(i.file_size for i in infos)<=MAX_EXPANDED-expanded,'ZIP expanded-size budget')
            for info in infos:
                name=safe(info.filename); key=str(name).casefold()
                require(key not in seen,'duplicate/case-colliding archive name');seen.add(key)
                mode=(info.external_attr>>16)&0o170000
                require(mode in (0,stat.S_IFREG,stat.S_IFDIR),'nonregular archive payload')
            containers.append({'container':container,'kind':kind,'depth':depth,'bytes':len(data),'sha256':sha(data)})
            dest.mkdir(parents=True,exist_ok=False)
            for ordinal,info in enumerate(infos):
                out=dest/str(safe(info.filename))
                if info.is_dir():out.mkdir(parents=True,exist_ok=True);continue
                body=z.read(info) # ZIP decompression verifies native CRC32.
                require(len(body)==info.file_size,'ZIP member size')
                expanded+=len(body);require(expanded<=MAX_EXPANDED,'expanded byte budget')
                out.parent.mkdir(parents=True,exist_ok=True)
                with out.open('xb') as f:f.write(body)
                nested='zip' if zipfile.is_zipfile(io.BytesIO(body)) else None
                row={'container':container,'container_depth':depth,'ordinal_zero_based':ordinal,
                     'original_member_name':info.filename,'canonical_extraction_relative_path':str(out.relative_to(S/'published-source')),
                     'extracted_path':str(out),'bytes':len(body),'sha256':sha(body),'CRC32':format(info.CRC,'08x'),
                     'compressed_bytes':info.compress_size,'zip_flags':info.flag_bits,'native_external_attr':info.external_attr,
                     'safe_regular_body':True,'nested_archive_kind':nested}
                rows.append(row)
                if nested:
                    child=S/'published-source-nested'/('d'+str(depth+1)+'-'+sha(body)[:20]+'-'+str(len(containers)))
                    unpack(body,container+'!'+info.filename,child,depth+1)
        return True
    try:
        tf=tarfile.open(fileobj=io.BytesIO(data),mode='r:*')
    except tarfile.ReadError:
        return False
    with tf:
        infos=tf.getmembers(); seen=set()
        require(sum(i.size for i in infos)<=MAX_EXPANDED-expanded,'tar expanded-size budget')
        for info in infos:
            name=safe(info.name);key=str(name).casefold()
            require(key not in seen,'duplicate/case-colliding tar name');seen.add(key)
            require(info.isfile() or info.isdir(),'nonregular tar entry')
        containers.append({'container':container,'kind':'tar','depth':depth,'bytes':len(data),'sha256':sha(data)})
        dest.mkdir(parents=True,exist_ok=False)
        for ordinal,info in enumerate(infos):
            out=dest/str(safe(info.name))
            if info.isdir():out.mkdir(parents=True,exist_ok=True);continue
            body=tf.extractfile(info).read();require(len(body)==info.size,'tar member size')
            expanded+=len(body);out.parent.mkdir(parents=True,exist_ok=True)
            with out.open('xb') as f:f.write(body)
            rows.append({'container':container,'container_depth':depth,'ordinal_zero_based':ordinal,
                         'original_member_name':info.name,'extracted_path':str(out),'bytes':len(body),'sha256':sha(body),
                         'CRC32':None,'compressed_bytes':None,'safe_regular_body':True,'nested_archive_kind':None})
    return True


def main():
    record=json.loads((S/'record.raw.json').read_bytes())
    latest=json.loads((S/'latest.raw.json').read_bytes())
    versions=json.loads((S/'versions.raw.json').read_bytes())
    require(record['id']==23331080 and latest['id']==23331080,'target/latest identity')
    require(versions['hits']['total']==1 and len(versions['hits']['hits'])==1
            and versions['hits']['hits'][0]['id']==23331080,'full one-version census')
    require(not versions.get('links',{}).get('next'),'unconsumed versions pagination')
    receipts=json.loads((S/'api-receipts.json').read_bytes());assets=[]
    files=record['files'];require(len({i['key'].casefold() for i in files})==len(files),'native asset collision')
    for item in files:
        name=item['key'];require(Path(name).name==name and name not in ['SOURCE_READY.json','api-receipts.json'],'unsafe native asset name')
        require(item['size']<=MAX_ASSET,'large asset requires separate cache review')
        out=S/name;require(not out.exists(),'native asset already exists, do not overwrite')
        url=item['links'].get('self') or item['links']['content'];start=now()
        with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Research catalogue native acquisition'}),timeout=60) as response:
            data=response.read(MAX_ASSET+1);status=response.status;final=response.url;headers=list(response.headers.raw_items())
        require(len(data)==item['size'] and len(data)<=MAX_ASSET,'native asset byte size')
        algorithm,expected=item['checksum'].split(':',1)
        require(hashlib.new(algorithm,data).hexdigest()==expected,'native provider checksum')
        with out.open('xb') as f:f.write(data)
        receipts.append({'requested_url':url,'started_utc':start,'completed_utc':now(),'HTTP_status':status,'final_url':final,
                         'response_headers_in_received_order':[list(x) for x in headers],
                         'body':{'path':str(out),'bytes':len(data),'sha256':sha(data)},'fresh_ordinary_HTTPS':True,'not_reused_cache':True})
        save(S/'api-receipts.json',receipts)
        assets.append({'original_api_file_object':item,'path':str(out),'bytes':len(data),'sha256':sha(data),'md5':hashlib.md5(data).hexdigest()})
    archives=[a for a in assets if zipfile.is_zipfile(a['path']) or a['path'].lower().endswith(('.tar','.tar.gz','.tgz'))]
    for asset in archives:
        dest=S/'published-source' if len(archives)==1 else S/'published-source'/Path(asset['path']).stem
        unpack(Path(asset['path']).read_bytes(),Path(asset['path']).name,dest)
    save(S/'archive-members.json',{'UTC':now(),'acquisition_only_opaque_payloads':True,'containers':containers,'members':rows,
                                 'safe_regular_occurrences':len(rows),'expanded_bytes_all_depths':expanded,
                                 'unsafe_names':[],'duplicate_or_case_colliding_names':[],'nonregular_payloads':[],
                                 'all_native_CRC_sizes_and_SHA256_checked':True,'scientific_bodies_read':False})
    save(A/'ASSET_ACQUISITION.json',{'UTC':now(),'all_assets_in_original_order':assets,'native_asset_total_bytes':sum(a['bytes'] for a in assets),
                                  'large_asset_threshold_bytes':MAX_ASSET,'all_below_large_threshold':True,'nested_archive_count':max(0,len(containers)-len(archives))})
    tex=[r for r in rows if r['original_member_name'].lower().endswith('.tex')]
    pdf=[r for r in rows if r['original_member_name'].lower().endswith('.pdf')]
    print(json.dumps({'status':'NATIVE_ASSETS_AND_OPAQUE_ARCHIVE_ACQUIRED','assets':assets,'containers':containers,
                      'regular_payloads':len(rows),'expanded_bytes':expanded,'TeX_candidates':tex,'embedded_PDF_candidates':pdf,
                      'scientific_manuscript_code_results_or_review_read':False},ensure_ascii=False,indent=2))


if __name__=='__main__':main()
