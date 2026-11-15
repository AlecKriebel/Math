#!/usr/bin/env python3
"""Pure offline custody: no writes, extraction, scientific reading or source execution."""
from pathlib import Path, PurePosixPath
import hashlib, json, re, zipfile, stat, binascii

ROOT=Path(__file__).resolve().parent
TERMINALS={'SOURCE_READY_MANIFEST.json','SOURCE_READY_SEAL.json','SOURCE_READY_CLOSURE.json'}


def require(x,m):
    if not x:raise RuntimeError(m)


def sha(b):return hashlib.sha256(b).hexdigest()


def safe(name,directory=False):
    require(type(name) is str and name and '\\' not in name and ':' not in name and '\x00' not in name,'Unsafe path')
    n=name[:-1] if directory and name.endswith('/') else name
    q=PurePosixPath(n)
    require(n and not q.is_absolute() and '..' not in q.parts and q.as_posix()==n,'Unsafe/noncanonical path')
    return Path(n)


def blob(b,r):
    require(type(r['bytes']) is int and len(b)==r['bytes'] and sha(b)==r['SHA256'],'Whole-byte mismatch')


def negative_controls():
    n=0
    for s in ['', '../x', '/x', 'a/../x', 'a\\x', 'a:x', 'a//x']:
        try:safe(s)
        except RuntimeError:n+=1
        else:raise RuntimeError('Path negative control escaped')
    for b,r in [(b'a',{'bytes':2,'SHA256':sha(b'a')}),(b'b',{'bytes':1,'SHA256':sha(b'a')}),(b'a',{'bytes':True,'SHA256':sha(b'a')})]:
        try:blob(b,r)
        except RuntimeError:n+=1
        else:raise RuntimeError('Byte negative control escaped')
    return n


def main():
    mb=(ROOT/'SOURCE_READY_MANIFEST.json').read_bytes();m=json.loads(mb);seal=json.loads((ROOT/'SOURCE_READY_SEAL.json').read_bytes())
    require(seal['source_ready_manifest_SHA256']==sha(mb),'Manifest seal mismatch')
    require(seal['record_id']==22983513 and m['record_id']==22983513,'Wrong record')
    files=m['files'];names=[r['path'] for r in files]
    require(len(names)==len(set(names)),'Duplicate manifest names')
    actual=set()
    for q in ROOT.rglob('*'):
        require(not q.is_symlink(),'Unexpected symlink')
        if q.is_file():actual.add(q.relative_to(ROOT).as_posix())
    require(set(names)==actual-TERMINALS,'Source inventory mismatch')
    for r in files:
        q=ROOT/safe(r['path']);require(q.is_file() and q.resolve().is_relative_to(ROOT),'Missing/escaped file');blob(q.read_bytes(),r)
    ready_bytes=(ROOT/'SOURCE_READY.json').read_bytes();require(seal['SOURCE_READY_SHA256']==sha(ready_bytes),'Readiness seal mismatch');d=json.loads(ready_bytes)
    require(d['status']=='SOURCE_READY' and d['record_id']==22983513 and d['sheet_row']==119,'Wrong readiness')
    require(d['version']=='1.0.1' and d['publication_date']=='2026-09-23' and d['versions_total_original']==1 and d['all_version_ids']==[22983513] and d['all_versions_pagination_complete'] is True,'Native version/date identity mismatch')
    require(d['target_manuscript_scientifically_read'] is False and d['source_programs_executed_or_scientifically_read'] is False,'Unread source-only boundary changed')
    require(d['native_license_object']=={'id':'cc-by-4.0'},'License identity mismatch')
    assets=d['all_assets_in_original_order'];require([r['original_api_file_object']['key'] for r in assets]==['source-and-verification.zip','paper.pdf','SHA256SUMS.txt'],'Native asset order changed')
    paths={}
    for r in assets:
        p=Path(r['path']);require(p.resolve().is_relative_to(ROOT),'Asset escaped source');b=p.read_bytes();blob(b,r);api=r['original_api_file_object'];alg,value=api['checksum'].split(':',1)
        require(len(b)==api['size'] and hashlib.new(alg,b).hexdigest()==value,'Native asset checksum mismatch');paths[api['key']]=p
    checks=(paths['SHA256SUMS.txt']).read_text().splitlines();require(len(checks)==2,'Deposited checksum line count')
    for line in checks:
        z=re.fullmatch(r'([0-9a-f]{64})  (.+)',line);require(z is not None,'Malformed deposited checksum');name=z.group(2);safe(name);require(name in paths and sha(paths[name].read_bytes())==z.group(1),'Deposited SHA mismatch')
    trans_path=Path(d['actual_transport_receipt_path']);require(sha(trans_path.read_bytes())==d['actual_transport_receipt_SHA256'],'Transport ledger mismatch');tr=json.loads(trans_path.read_bytes());require(len(tr)==8 and sum(r['HTTP_status']==200 for r in tr)==7,'Actual transport count mismatch')
    for r in tr:
        p=Path(r['body_path']);require(p.resolve().is_relative_to(ROOT),'Transport body escaped source');blob(p.read_bytes(),r);require(type(r['request_headers_in_order']) is list and type(r['response_headers_in_order']) is list,'Ordered native header container lost')
    require([r['HTTP_status'] for r in tr if r['HTTP_status']!=200]==[400],'Failed transport was removed or misrepresented')
    native={r['role']:json.loads(Path(r['path']).read_bytes()) for r in d['whole_native_API_objects']}
    require(native['latest']['id']==22983513,'Latest record identity changed')
    versions=native['versions_page_001_success'];require(versions['hits']['total']==1 and len(versions['hits']['hits'])==1 and 'next' not in versions['links'],'Version pagination not complete')
    require(native['files']['default_preview'] is None and native['files']['order']==[] and native['files']['entries'][2]['metadata']=={},'Native null/empty distinctions changed')
    require(native['versions_page_001_failed_HTTP400']['status']==400,'Original failed native body changed')
    cp=Path(d['whole_archive_custody_path']);require(sha(cp.read_bytes())==d['whole_archive_custody_SHA256'],'Archive custody mismatch');c=json.loads(cp.read_bytes());require(c['nested_archive_count']==0 and len(c['archive_containers'])==1,'Unexpected archive scope')
    records=c['archive_containers'][0]['entries_in_original_order'];regular=[];folded=set();all_paths={}
    with zipfile.ZipFile(paths['source-and-verification.zip']) as z:
        infos=z.infolist();require(len(infos)==len(records),'Original ZIP member count changed')
        for ordinal,(i,r) in enumerate(zip(infos,records)):
            name=safe(i.filename,i.is_dir());fold=name.as_posix().casefold();require(fold not in folded,'Duplicate/case collision');folded.add(fold);all_paths[name.as_posix()]=i.is_dir()
            kind=stat.S_IFMT(i.external_attr>>16);require(kind in (0,stat.S_IFDIR if i.is_dir() else stat.S_IFREG) and not(i.flag_bits&1),'Nonregular/encrypted ZIP payload')
            b=z.read(i);require(i.filename==r['original_member_name'] and ordinal==r['ordinal_zero_based'] and i.CRC==(binascii.crc32(b)&0xffffffff) and '%08x'%i.CRC==r['CRC32'],'ZIP order/CRC mismatch');blob(b,r)
            if not i.is_dir():
                p=Path(r['extracted_path']);require(p.resolve().is_relative_to(ROOT),'Extracted path escaped source');require(p.read_bytes()==b,'Extracted whole bytes changed');regular.append(r)
        for name in all_paths:
            for parent in PurePosixPath(name).parents:
                if str(parent) in all_paths:require(all_paths[str(parent)] is True,'File/directory prefix collision')
    require(len(regular)==30 and sum(x['bytes'] for x in regular)==255407,'Archive payload scope mismatch')
    pdf=Path(d['selected_actual_PDF']['path']);embedded=d['all_embedded_PDF_members'];require(pdf.read_bytes().startswith(b'%PDF-') and d['selected_actual_PDF']['pages']==3 and len(embedded)==1,'Actual PDF structural identity mismatch');require(Path(embedded[0]['extracted_path']).read_bytes()==pdf.read_bytes(),'Published/embedded PDFs differ')
    tex=d['controlling_TeX'];require(tex['SHA256']=='073f7e31a0037fa09ead605b5028d7c921e0188d2117734c7d1ba12a4b1ef051' and tex['bytes']==10427 and tex['lines_mechanically_counted_not_displayed']==173,'Sole source identity mismatch')
    print(json.dumps({'status':'SOURCE_CUSTODY_PASS','record_id':22983513,'bound_files':len(files),'safe_regular_ZIP_payloads':len(regular),'native_assets':len(assets),'native_transport_attempts':len(tr),'preserved_failed_attempts':1,'deposited_SHA256SUMS_lines':len(checks),'custody_negative_controls':negative_controls(),'source_programs_run':0,'scientific_text_read':False,'network':0,'file_writes':0},sort_keys=True))


if __name__=='__main__':main()
