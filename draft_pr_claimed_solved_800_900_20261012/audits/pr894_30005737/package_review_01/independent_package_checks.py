#!/usr/bin/env python3
"""Independent frozen-package representation checks; no archival execution.

Usage: python -I -S -B independent_package_checks.py CANDIDATE REVIEW
Writes only REVIEW/private_tmp and REVIEW/REPRESENTATION_CHECKS.json.
The ZIP writer is implemented directly, independently of portable.py/zipfile.
"""
from pathlib import Path
import datetime, hashlib, io, json, stat, struct, sys, zlib, zipfile

def pin(b): return {"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()}
def stamp(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def check(ok, why):
    if not ok: raise ValueError(why)

def manual_zip(blobs):
    local=bytearray(); central=bytearray()
    date=((2026-1980)<<9)|(10<<5)|16
    for name,raw in sorted(blobs.items()):
        encoded=name.encode('ascii'); compressor=zlib.compressobj(9,zlib.DEFLATED,-15)
        compressed=compressor.compress(raw)+compressor.flush(); crc=zlib.crc32(raw)
        offset=len(local)
        local+=struct.pack('<4s5H3I2H',b'PK\x03\x04',20,0,8,0,date,crc,len(compressed),len(raw),len(encoded),0)+encoded+compressed
        central+=struct.pack('<4s6H3I5H2I',b'PK\x01\x02',788,20,0,8,0,date,crc,len(compressed),len(raw),len(encoded),0,0,0,0,(stat.S_IFREG|0o644)<<16,offset)+encoded
    return bytes(local+central+struct.pack('<4s4H2IH',b'PK\x05\x06',0,0,len(blobs),len(blobs),len(central),len(local),0))

def raw_zip_check(raw,blobs,generated):
    end=struct.unpack_from('<4s4H2IH',raw,len(raw)-22)
    check(end[:5]==(b'PK\x05\x06',0,0,len(blobs),len(blobs)) and end[-1]==0,'EOCD metadata')
    check(end[5]+end[6]==len(raw)-22,'EOCD extent')
    local=0;central=end[6]
    with zipfile.ZipFile(io.BytesIO(raw)) as arc:
        check(arc.namelist()==sorted(blobs) and not arc.comment,'sorted closed membership')
        for info in arc.infolist():
            name=info.filename;payload=blobs[name];nb=name.encode('ascii')
            check(info.header_offset==local and info.flag_bits==0 and info.compress_type==8,'local offset/flags')
            check(info.create_system==3 and info.create_version==20 and info.extract_version==20,'ZIP versions')
            check(not info.extra and not info.comment and info.volume==info.internal_attr==0,'no extra ZIP metadata')
            mode=info.external_attr>>16
            check(stat.S_ISREG(mode) and stat.S_IMODE(mode) in ((0o644,) if generated else (0o444,0o644)),'regular modes')
            if generated:check(info.date_time==(2026,10,16,0,0,0),'fixed date')
            l=struct.unpack_from('<4s5H3I2H',raw,local)
            c=struct.unpack_from('<4s6H3I5H2I',raw,central)
            dt=((info.date_time[0]-1980)<<9)|(info.date_time[1]<<5)|info.date_time[2]
            tm=(info.date_time[3]<<11)|(info.date_time[4]<<5)|(info.date_time[5]//2)
            check(l==(b'PK\x03\x04',20,0,8,tm,dt,info.CRC,info.compress_size,len(payload),len(nb),0),'local header exact')
            check(c==(b'PK\x01\x02',788,20,0,8,tm,dt,info.CRC,info.compress_size,len(payload),len(nb),0,0,0,0,info.external_attr,local),'central header exact')
            check(raw[local+30:local+30+len(nb)]==nb and raw[central+46:central+46+len(nb)]==nb,'header names')
            start=local+30+len(nb); local=start+info.compress_size;central+=46+len(nb)
            decoder=zlib.decompressobj(-15);inflated=decoder.decompress(raw[start:local],len(payload)+1)
            check(inflated==payload and decoder.eof and not decoder.unused_data and not decoder.unconsumed_tail,'exact DEFLATE consumption')
            check(zlib.crc32(payload)==info.CRC and arc.read(info)==payload,'CRC/member payload')
        check(local==end[6] and central==len(raw)-22,'no prefixes/gaps/trailers')

def main():
    C=Path(sys.argv[1]);R=Path(sys.argv[2]);A=C.parent.parent
    started=stamp();core=json.loads((A/'FROZEN_CANDIDATE_CORE.json').read_bytes());rows=[]
    for p in sorted(C.rglob('*')):
        if p.is_dir():continue
        check(stat.S_ISREG(p.lstat().st_mode) and stat.S_IMODE(p.lstat().st_mode)==0o644,'core mode')
        rows.append(dict(path=p.relative_to(C).as_posix(),git_mode='100644',**pin(p.read_bytes())))
    check(rows==core['files'],'253 core rows')
    digest=hashlib.sha256(json.dumps(rows,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    check(digest=='c06bf8dfd12c840d0f4af7af32ef6253de1c9f8d3b47f7a0618dedd7fd17ed2b','external core pin')
    outer=json.loads((C/'CURRENT_PUBLICATION_MANIFEST.json').read_bytes());inner=json.loads((C/'verification/package_index.json').read_bytes())
    for root,index,selfname in [(C,outer,'CURRENT_PUBLICATION_MANIFEST.json'),(C/'verification',inner,'package_index.json')]:
        names={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
        check(names=={r['path'] for r in index['files']}|{selfname},'closed index tree')
        check(len(index['files'])==len({r['path'] for r in index['files']}),'unique index rows')
        for row in index['files']:check(pin((root/row['path']).read_bytes())=={k:row[k] for k in ['bytes','sha256']},'index row')
    original=json.loads((A/'SOURCE_MANIFEST.json').read_bytes());source=C/'verification/source'
    check(len(original['files'])==18,'18 original files')
    for row in original['files']:
        b=(source/row['path']).read_bytes();check(pin(b)=={k:row[k] for k in ['bytes','sha256']},'source SHA256')
        check(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==row['git_blob'],'original Git blob ID')
        check((A/'source'/row['path']).read_bytes()==b,'original source copy equality')
    inneroriginal=json.loads((source/'authored/MANIFEST.json').read_bytes())
    originalblobs={'MANIFEST.json':(source/'authored/MANIFEST.json').read_bytes(),**{x['path']:(source/'authored'/x['path']).read_bytes() for x in inneroriginal['files']}}
    raw_zip_check((source/'AUTHOR_CANDIDATE.zip').read_bytes(),originalblobs,False)
    blobs={p.relative_to(C/'verification').as_posix():p.read_bytes() for p in (C/'verification').rglob('*') if p.is_file()}
    check(len(blobs)==242,'242 portable members');raw=(C/'post-lie-verification.zip').read_bytes()
    raw_zip_check(raw,blobs,True);rebuilt=manual_zip(blobs);check(rebuilt==raw,'independent raw ZIP rebuild equality')
    (R/'private_tmp/independent-post-lie-verification.zip').write_bytes(rebuilt)
    for name in ['portable.py','note.tex','metadata.json','zenodo-deposit.json','README.md','EDITION_HISTORY.md']:
        check((C/name).read_bytes()==blobs[name],'current/portable copy '+name)
    md=json.loads((C/'metadata.json').read_bytes());dep=json.loads((C/'zenodo-deposit.json').read_bytes())
    check(dep['metadata']==md and dep['files']==[{'name':x,'path':x} for x in ['post-lie-note.pdf','post-lie-verification.zip']],'metadata/deposit/asset equality')
    check((C/'post-lie-note.pdf').read_bytes().startswith(b'%PDF-'),'PDF header only')
    envelopes=[]
    for family in sorted((C/'verification/audits').iterdir()):
        manifest=json.loads((family/'SAFE_MANIFEST.json').read_bytes())
        entries=manifest['files']
        for row in entries:check(pin((family/row['path']).read_bytes())=={k:row[k] for k in ['bytes','sha256']},'safe envelope row '+family.name)
        check({p.relative_to(family).as_posix() for p in family.rglob('*') if p.is_file()}=={r['path'] for r in entries}|{'SAFE_MANIFEST.json'},'complete accepted safe envelope '+family.name)
        envelopes.append({'family':family.name,'manifest':pin((family/'SAFE_MANIFEST.json').read_bytes()),'rows_authenticated':len(entries),'schema_keys':sorted(manifest)})
    out={'started_utc':started,'ended_utc':stamp(),'status':'PASS','core_files':253,'core_sha256':digest,'outer_rows':len(outer['files']),'portable_members':242,'original_files':18,'original_bytes':sum(x['bytes'] for x in original['files']),'original_git_blob_ids_checked':18,'source_copy_equalities':18,'original_archive_members':9,'independent_manual_zip_writer':'struct headers, CRC32 and raw zlib; neither portable nor zipfile writer used','exact_zip':pin(rebuilt),'python':sys.version.split()[0],'zlib_runtime':zlib.ZLIB_RUNTIME_VERSION,'safe_envelopes':envelopes,'pdf_scope':'HEADER_ONLY; visual QA recorded separately'}
    (R/'REPRESENTATION_CHECKS.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,sort_keys=True))
if __name__=='__main__':main()
