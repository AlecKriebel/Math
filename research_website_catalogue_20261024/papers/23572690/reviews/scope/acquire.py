from pathlib import Path,PurePosixPath
import urllib.request,json,hashlib,datetime,zipfile,stat,subprocess,time
base=Path(__file__).resolve().parents[2];s=base/'sources';r=base/'reviews/scope'
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def fetch(url):
    req=urllib.request.Request(url,headers={'User-Agent':'Research source verification (public records)'})
    with urllib.request.urlopen(req,timeout=90) as f:return f.read()
def sha(data):return hashlib.sha256(data).hexdigest()
with (r/'research-log.md').open('a') as f:f.write('# Scope and acquisition log — Zenodo 23572690\n\n- '+utc()+' — Started exact queue-identity source acquisition. Scope only; no mathematical PASS assigned. Completion estimate: 0%.\n')
raw=fetch('https://zenodo.org/api/records/23572690');(s/'record.json').write_bytes(raw);meta=json.loads(raw)
assert str(meta['id'])=='23572690';assert meta['metadata']['title']=='BV generators for polynomial Weyl subalgebras'
receipt={'record_id':'23572690','retrieved_utc':utc(),'metadata_url':'https://zenodo.org/api/records/23572690','record_sha256':sha(raw),'files':[]}
for item in meta['files']:
    name=item['key'];assert PurePosixPath(name).name==name and not name.startswith('.')
    url=item['links'].get('content') or item['links']['self'];data=fetch(url);md5=hashlib.md5(data).hexdigest()
    assert len(data)==item['size'];assert item['checksum']=='md5:'+md5
    (s/name).write_bytes(data)
    receipt['files'].append({'name':name,'url':url,'bytes':len(data),'sha256':sha(data),'zenodo_checksum':item['checksum'],'md5':md5,'integrity':'PASS'})
assert next(x for x in receipt['files'] if x['name']=='bv-generators.pdf')['sha256']=='2c344b0baff06088f04f4468bd8f6365405e879f7004b169055aebedbdecd4e7'
receipt['complete']=True;(s/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
members=[]
for item in receipt['files']:
    p=s/item['name']
    if p.suffix!='.zip':continue
    out=s/'published-source'/p.stem
    with zipfile.ZipFile(p) as z:
        seen=set()
        for info in z.infolist():
            path=PurePosixPath(info.filename);assert not path.is_absolute() and '..' not in path.parts and '\\' not in str(path);assert str(path) not in seen;seen.add(str(path))
            mode=(info.external_attr>>16)&0xFFFF;assert not stat.S_ISLNK(mode)
            if info.is_dir():continue
            assert stat.S_IFMT(mode) in (0,stat.S_IFREG)
            data=z.read(info);target=out/Path(*path.parts);target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
            members.append({'archive':p.name,'member':str(path),'path':str(target.relative_to(s)),'bytes':len(data),'sha256':sha(data),'crc32':f'{info.CRC:08x}','original_mode':oct(mode)})
(s/'extraction-integrity.json').write_text(json.dumps({'verified_utc':utc(),'safe_paths_regular_files_no_duplicates':True,'zip_crc_verified':True,'members':members},indent=2)+'\n')
readers=[]
for p in sorted(s.rglob('*.pdf')):
    info=subprocess.check_output(['pdfinfo',str(p)],text=True);pages=int(next(line.split(':',1)[1] for line in info.splitlines() if line.startswith('Pages:')))
    readers.append({'source_relative_path':str(p.relative_to(s)),'sha256':sha(p.read_bytes()),'bytes':p.stat().st_size,'pages':pages,'top_level':p.parent==s})
(s/'reader-pdf-map.json').write_text(json.dumps({'created_utc':utc(),'readers':readers},indent=2)+'\n')
with (r/'research-log.md').open('a') as f:f.write('\n- '+utc()+' — Fresh public metadata and all '+str(len(receipt['files']))+' public assets authenticated; all '+str(len(members))+' ZIP regular files safely extracted/CRC-checked; '+str(len(readers))+' PDF(s) mapped. Exact queue main-PDF SHA matched. Completion estimate: 25%.\n')
print(json.dumps({'record_metadata':meta['metadata'],'files':receipt['files'],'extracted_files':len(members),'readers':readers},indent=2))
