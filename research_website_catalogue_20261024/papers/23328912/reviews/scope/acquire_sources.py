from pathlib import Path, PurePosixPath
from urllib.request import Request, urlopen
from concurrent.futures import ThreadPoolExecutor
import hashlib, json, stat, zipfile, datetime, subprocess

BASE=Path(__file__).resolve().parents[2]
SRC=BASE/'sources'; OUT=BASE/'reviews/scope'
record=json.loads((SRC/'record.json').read_text())
expected={'aim_5_2_two_cube_cubulation.pdf':(77863,'8b9c82c57c418e10a06ec92326c807be','3dfdfca7c0b9d41c54ed03dc9500afd8d8013fef2ebd589b2806712f84781841'),'aim_5_2_source.zip':(11430,'a6db282ae434ae4ceb656ca155a3e84c',None),'aim_5_2_verification.zip':(56309,'0688c42045cf2122e3d570f4aa810dd1',None)}
def fetch(f):
    name=f['key']; pp=PurePosixPath(name)
    if pp.is_absolute() or '..' in pp.parts or '\\' in name: raise ValueError(name)
    req=Request(f['links']['self'],headers={'User-Agent':'ResearchScope/1.0'})
    with urlopen(req,timeout=60) as resp:
        data=resp.read(); resolved=resp.url
    md5=hashlib.md5(data).hexdigest(); sha=hashlib.sha256(data).hexdigest()
    assert len(data)==f['size'] and f['checksum']=='md5:'+md5
    if name in expected:
        size, digest, sh=expected[name]
        assert size==len(data) and digest==md5 and (sh is None or sh==sha)
    path=SRC/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
    return {'name':name,'url':f['links']['self'],'resolved_url':resolved,'bytes':len(data),'md5':md5,'zenodo_checksum':f['checksum'],'sha256':sha,'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'integrity':'PASS'}
with ThreadPoolExecutor(max_workers=2) as pool: assets=list(pool.map(fetch,record['files']))
archives=[]
for a in assets:
    if not a['name'].endswith('.zip'):continue
    members=[]
    with zipfile.ZipFile(SRC/a['name']) as z:
        assert len(z.infolist()) < 10000 and sum(m.file_size for m in z.infolist()) < 200*1024*1024
        seen=set()
        for m in z.infolist():
            p=PurePosixPath(m.filename);mode=m.external_attr>>16
            key=str(p).casefold()
            if key in seen:raise ValueError('duplicate/case-colliding member '+m.filename)
            seen.add(key)
            if p.is_absolute() or '..' in p.parts or '\\' in m.filename: raise ValueError(m.filename)
            if stat.S_ISLNK(mode) or stat.S_IFMT(mode) not in (0,stat.S_IFREG,stat.S_IFDIR):raise ValueError(m.filename)
        for m in z.infolist():
            if m.is_dir(): continue
            data=z.read(m)
            dest=SRC/'published-source'/Path(a['name']).stem/m.filename;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
            members.append({'member':m.filename,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'crc32':f'{m.CRC:08x}'})
    archives.append({'name':a['name'],'extraction_root':'published-source/'+Path(a['name']).stem,'all_paths_types_and_member_crc_checked':True,'members':members})
receipt={'record_id':'23328912','complete':True,'record_sha256':hashlib.sha256((SRC/'record.json').read_bytes()).hexdigest(),'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':assets,'archives':archives}
(SRC/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
pdfs=[]
for p in SRC.rglob('*.pdf'):
    if p.name.startswith('._'):continue
    data=p.read_bytes()
    if not data.startswith(b'%PDF'):raise ValueError('Not PDF '+str(p))
    inf=subprocess.check_output(['pdfinfo',str(p)],text=True)
    pages=int(next(l for l in inf.splitlines() if l.startswith('Pages:')).split(':',1)[1])
    sha=hashlib.sha256(data).hexdigest();txt=OUT/f'reader-{sha[:12]}.txt'
    subprocess.run(['pdftotext','-layout',str(p),str(txt)],check=True)
    pdfs.append({'path':str(p.relative_to(BASE)),'pages':pages,'bytes':len(data),'sha256':sha,'text':str(txt.relative_to(BASE))})
(OUT/'reader_document_map.json').write_text(json.dumps({'documents':pdfs,'all_reader_pdfs_read':False},indent=2)+'\n')
print(json.dumps({'files':assets,'extracted_files':sum(len(a['members']) for a in archives),'reader_pdfs':pdfs},indent=2))
