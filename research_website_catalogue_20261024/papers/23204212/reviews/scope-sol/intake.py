"""Saved passive custody, native metadata and fresh Poppler reading only."""
import datetime, hashlib, json, os, re, stat, subprocess, time, zipfile
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath

P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
SRC=P/'papers/23204212/sources'
OWN=P/'papers/23204212/reviews/scope-sol'
CONTROLS={'SOURCE_FINAL.json':'b68fbb425b7d910a2508c46ff311491a1c797568dcf39d3c7deb0a0545e1afd5','SOURCE_MANIFEST.json':'afa64c126da0aabc4a44ec242553e5b2354540eb1b0b60e55ab7b1a9855a09be'}
def write(n,data):
    with (OWN/n).open('x') as f:json.dump(data,f,ensure_ascii=False,indent=2);f.write('\n')
def pin(p):
    a=p.lstat();assert stat.S_ISREG(a.st_mode) and not p.is_symlink()
    with p.open('rb') as f:
        s=os.fstat(f.fileno());assert (a.st_dev,a.st_ino)==(s.st_dev,s.st_ino)
        raw=f.read();z=os.fstat(f.fileno())
    end=p.lstat();fields=lambda s:(s.st_dev,s.st_ino,s.st_size,s.st_mode,s.st_mtime_ns,s.st_ctime_ns)
    assert fields(a)==fields(z)==fields(end) and len(raw)==z.st_size
    return dict(bytes=len(raw),SHA256=hashlib.sha256(raw).hexdigest(),MD5=hashlib.md5(raw).hexdigest(),mode=oct(stat.S_IMODE(a.st_mode)))
def census(root):
    files,dirs={},{'.':oct(stat.S_IMODE(root.lstat().st_mode))};todo=[root]
    while todo:
        here=todo.pop();a=here.lstat();assert stat.S_ISDIR(a.st_mode) and not here.is_symlink()
        for p in sorted(here.iterdir()):
            n=p.relative_to(root).as_posix();s=p.lstat();assert not p.is_symlink()
            if stat.S_ISDIR(s.st_mode):dirs[n]=oct(stat.S_IMODE(s.st_mode));todo.append(p)
            else:files[n]=pin(p)
        z=here.lstat();assert (a.st_dev,a.st_ino,a.st_mode,a.st_mtime_ns,a.st_ctime_ns)==(z.st_dev,z.st_ino,z.st_mode,z.st_mtime_ns,z.st_ctime_ns)
    return dict(root=str(root),root_mode=dirs['.'],files=files,directories={n:m for n,m in dirs.items() if n!='.'},hidden_paths=[n for n in sorted(set(files)|set(dirs)) if n!='.' and any(x.startswith('.') for x in n.split('/'))],empty_files=[n for n,v in sorted(files.items()) if v['bytes']==0],empty_directories=[n for n in sorted(dirs) if n!='.' and not any(x.startswith(n+'/') for x in set(files)|set(dirs))])

started=datetime.datetime.now(datetime.timezone.utc).isoformat()
before=census(SRC);assert len(before['files'])==55 and len(before['directories'])==14
assert all(before['files'][n]['SHA256']==v for n,v in CONTROLS.items())
manifest=json.loads((SRC/'SOURCE_MANIFEST.json').read_bytes())
assert manifest['schema']=='source-custody-finite-manifest-v1' and manifest['other_exclusions']==[]
assert set(manifest['excluded_control_files'])==set(CONTROLS)
assert manifest['terminal_modes']=={n:'0o644' for n in CONTROLS}
names=[r['path'] for r in manifest['entries']];assert len(names)==len(set(names))
files,dirs={},{}
for row in manifest['entries']:
    n=row['path'];assert n=='.' or (not n.startswith('/') and all(x not in ('','.','..') for x in n.split('/')))
    if row['kind']=='file':
        assert set(row)=={'path','kind','bytes','sha256','md5','mode_octal'}
        files[n]=dict(bytes=row['bytes'],SHA256=row['sha256'],MD5=row['md5'],mode=row['mode_octal'])
    else:
        assert row['kind']=='directory' and set(row)=={'path','kind','mode_octal','empty'}
        dirs[n]=row['mode_octal'];assert row['empty']==(n in before['empty_directories'])
assert files=={n:v for n,v in before['files'].items() if n not in CONTROLS}
assert dirs==dict({'.':before['root_mode']},**before['directories'])
assert len(files)==manifest['file_count']==53 and len(dirs)==manifest['directory_count']==15
write('SOURCE_BEFORE.json',before)
api=json.loads((SRC/'native-metadata/record-api.json').read_bytes())
assert api['id']==23204212
assert [r['key'] for r in api['files']]==['thompson-cstar-verification.zip','thompson-cstar-source.zip','paper.pdf']
for row in api['files']:
    value=before['files']['zenodo-files/'+row['key']]
    assert value['bytes']==row['size'] and row['checksum']=='md5:'+value['MD5']
pdf=SRC/'zenodo-files/paper.pdf'
assert before['files']['zenodo-files/paper.pdf']['SHA256']=='527ac7feb6f2c889998559122296dd8caab2def0cf7aeac00f79c1f8b0c8a978'
archives=[]
for row in api['files']:
    if not row['key'].endswith('.zip'):continue
    path=SRC/'zenodo-files'/row['key'];seen=set();members=[]
    with zipfile.ZipFile(path) as z:
        for m in z.infolist():
            n=m.filename;trim=n.rstrip('/');parts=PurePosixPath(trim).parts
            assert trim and not n.startswith('/') and '\\' not in n and all(t not in ('','.','..') for t in trim.split('/'))
            assert not re.match(r'^[A-Za-z]:',n) and n not in seen
            seen.add(n);mode=(m.external_attr>>16)&0xffff;assert not stat.S_ISLNK(mode)
            members.append(dict(path=n,is_directory=m.is_dir(),uncompressed_bytes=m.file_size,compressed_bytes=m.compress_size,CRC32=hex(m.CRC),archive_mode=oct(mode)))
    archives.append(dict(name=row['key'],whole_archive=pin(path),members=members,safe_relative_paths_unique=True,extraction_or_code_read=False))
write('ARCHIVE_PATH_CENSUS.json',dict(archives=archives,scope='ZIP central directory names/sizes/modes only; no member program/audit contents read or executed'))

class NativePage(HTMLParser):
    def __init__(self):super().__init__(convert_charrefs=True);self.hidden=0;self.visible=[];self.metas=[];self.links=[];self.jsonld=[];self.in_json=False
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag in ('script','style'):
            self.hidden+=1
            if tag=='script' and a.get('type')=='application/ld+json':self.in_json=True;self.jsonld.append('')
        if tag=='meta':self.metas.append(a)
        if tag in ('link','a') and 'href' in a:self.links.append(dict(tag=tag,**a))
        if tag in ('p','div','section','h1','h2','h3','li','tr','br'):self.visible.append('\n')
    def handle_endtag(self,tag):
        if tag in ('script','style'):
            self.hidden-=1
            if tag=='script':self.in_json=False
        if tag in ('p','div','section','h1','h2','h3','li','tr'):self.visible.append('\n')
    def handle_data(self,data):
        if self.in_json:self.jsonld[-1]+=data
        if not self.hidden:self.visible.append(data)
page=NativePage();page.feed((SRC/'native-metadata/record-page.html').read_text());page.close()
visible='\n'.join(' '.join(line.split()) for line in ''.join(page.visible).splitlines() if line.strip())
with (OWN/'NATIVE_HTML_VISIBLE.txt').open('x') as f:f.write(visible+'\n')
write('NATIVE_HTML_METADATA.json',dict(source_pin=before['files']['native-metadata/record-page.html'],metas=page.metas,links=page.links,JSON_LD_literal_scripts=page.jsonld,full_API_Description=api['metadata']['description'],API_version_field_present='version' in api['metadata'],API_version=api['metadata'].get('version'),declared_publication_date=api['metadata']['publication_date'],created=api['created'],updated=api['updated'],license=api['metadata']['license'],native_order=api['files'],all_original_author_assertions_unverified=True))
calls=[]
def run(label,argv):
    start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
    with (OWN/(label+'.stdout.txt')).open('xb') as out,(OWN/(label+'.stderr.txt')).open('xb') as err:r=subprocess.run(argv,cwd=OWN,stdout=out,stderr=err,check=False)
    calls.append(dict(label=label,argv=argv,started_UTC=start,finished_UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),elapsed_seconds=time.monotonic()-t,exit_code=r.returncode,stdout=pin(OWN/(label+'.stdout.txt')),stderr=pin(OWN/(label+'.stderr.txt'))))
    write(label+'.invocation.json',calls[-1]);assert r.returncode==0,label
run('PDFINFO',['/opt/homebrew/bin/pdfinfo',str(pdf)])
assert re.search(r'^Pages:\s+4\s*$',(OWN/'PDFINFO.stdout.txt').read_text(),re.M)
run('PDFTEXT',['/opt/homebrew/bin/pdftotext','-layout',str(pdf),str(OWN/'native-paper.txt')])
pages=(OWN/'native-paper.txt').read_text().split('\f')
assert len(pages)==5 and not pages[-1].strip()
for i,text in enumerate(pages[:-1],1):
    with (OWN/('native-page-'+str(i)+'.txt')).open('x') as f:f.write(text)
(OWN/'pixels').mkdir()
run('PDFRENDER',['/opt/homebrew/bin/pdftoppm','-f','1','-l','4','-r','120','-png',str(pdf),str(OWN/'pixels/native-page')])
assert sorted(p.name for p in (OWN/'pixels').iterdir())==['native-page-1.png','native-page-2.png','native-page-3.png','native-page-4.png']
after=census(SRC);assert before==after
write('SOURCE_AFTER.json',after)
write('INTAKE_RECEIPT.json',dict(started_UTC=started,finished_UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),source_files=55,source_childdirs=14,source_manifest_schema=manifest['schema'],control_pins=CONTROLS,full_source_before_after_exact=True,original_TeX=before['files']['archives/02-thompson-cstar-source.zip.extracted/main.tex'],outer_PDF=before['files']['zenodo-files/paper.pdf'],native_API=before['files']['native-metadata/record-api.json'],fresh_page_texts={str(i):pin(OWN/('native-page-'+str(i)+'.txt')) for i in range(1,5)},fresh_page_pixels={str(i):pin(OWN/('pixels/native-page-'+str(i)+'.png')) for i in range(1,5)},Poppler_calls=calls,native_scientific_program_contents_opened=0,support_or_peer_or_primary_contents_opened=0,source_or_support_program_execution_imports=0,own_reader=pin(OWN/'intake.py'),reader_fully_personally_read_before_invocation=True,scope='Original-only INITIAL gate; author assertions remain unverified; no mathematical verdict'))
print(json.dumps(dict(status='FRESH_ORIGINAL_READING_ARTIFACTS_READY',source_files=55,source_childdirs=14,PDF_pages=4,guard_exact=True,support_code_exposure_count=0)))
