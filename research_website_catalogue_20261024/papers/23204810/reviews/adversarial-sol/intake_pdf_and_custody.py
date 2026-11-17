"""Passive native-byte custody plus Poppler document extraction/render only."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT.parents[1]/'sources'
assert ROOT.name=='adversarial-sol' and SOURCE.parent.name=='23204810'
PINS={'SOURCE_MANIFEST.json':'045d57f33015c343ca7441d602d37425a746d93954e88e812782abfda2612820',
      'SOURCE_FINAL.json':'4d62403dbe129bb77393b73492dc92ae8504d5081e84d311cb7905c7323638df'}
def encode(value):
    return (json.dumps(value,indent=2,ensure_ascii=False)+'\n').encode()
def save(name,value):
    with (ROOT/name).open('xb') as handle:
        handle.write(encode(value))
def guard():
    for name,expected in PINS.items():
        assert hashlib.sha256((SOURCE/name).read_bytes()).hexdigest()==expected
    manifest=json.loads((SOURCE/'SOURCE_MANIFEST.json').read_bytes())
    assert manifest['schema']=='source-custody-finite-manifest-v1'
    assert manifest['root']==str(SOURCE)
    assert manifest['excluded_control_files']==['SOURCE_FINAL.json','SOURCE_MANIFEST.json']
    assert manifest['file_count']==59 and manifest['directory_count']==14
    expected={row['path']:row for row in manifest['entries']}
    objects=[SOURCE]+sorted(SOURCE.rglob('*'),key=lambda p:p.relative_to(SOURCE).as_posix())
    assert {'.' if p==SOURCE else p.relative_to(SOURCE).as_posix() for p in objects}==set(expected)|set(PINS)
    entries=[]
    for path in objects:
        name='.' if path==SOURCE else path.relative_to(SOURCE).as_posix()
        info=path.lstat()
        row={'path':name,'mode':oct(stat.S_IMODE(info.st_mode)),'mtime_ns':info.st_mtime_ns,'ctime_ns':info.st_ctime_ns,
             'device':info.st_dev,'inode':info.st_ino,'hidden':any(x.startswith('.') for x in Path(name).parts if x!='.')}
        assert stat.S_ISREG(info.st_mode) or stat.S_ISDIR(info.st_mode)
        if stat.S_ISDIR(info.st_mode):
            row.update(kind='directory',empty=not any(path.iterdir()))
            old=expected[name]
            assert old['kind']=='directory' and row['mode']==old['mode_octal'] and row['empty']==old['empty']
        else:
            raw=path.read_bytes()
            row.update(kind='file',bytes=len(raw),empty=not raw,SHA256=hashlib.sha256(raw).hexdigest(),MD5=hashlib.md5(raw).hexdigest())
            if name in PINS:
                assert row['SHA256']==PINS[name] and row['mode']==manifest['terminal_modes'][name]
            else:
                old=expected[name]
                assert old['kind']=='file' and (row['bytes'],row['SHA256'],row['MD5'],row['mode'])==(old['bytes'],old['sha256'],old['md5'],old['mode_octal'])
        entries.append(row)
    assert sum(r['kind']=='file' for r in entries)==61
    assert sum(r['kind']=='directory' for r in entries)==14
    return {'root':str(SOURCE),'files':61,'child_directories':13,'root_including_directories':14,'external_terminal_SHA256':PINS,'entries':entries}

started=datetime.datetime.now(datetime.timezone.utc).isoformat()
before=guard()
save('SOURCE_BEFORE.json',before)
PDF=SOURCE/'zenodo-files/paper.pdf'
assert len(PDF.read_bytes())==73479 and hashlib.sha256(PDF.read_bytes()).hexdigest()=='ae0526dfe7442b63e9c3f4754c324970b0d4e8ccd15d85b6f9585ed3ee45a119'
operations=[]
def run(label,argv):
    start=datetime.datetime.now(datetime.timezone.utc).isoformat()
    result=subprocess.run(argv,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    (ROOT/(label+'.stdout.txt')).write_bytes(result.stdout)
    (ROOT/(label+'.stderr.txt')).write_bytes(result.stderr)
    record={'label':label,'argv':argv,'cwd':str(ROOT),'started_UTC':start,'finished_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':result.returncode,'stdout_bytes':len(result.stdout),'stderr_bytes':len(result.stderr)}
    operations.append(record)
    save(label+'.operation.json',record)
    assert result.returncode==0,record
    return result.stdout
info=run('pdfinfo',['/opt/homebrew/bin/pdfinfo',str(PDF)])
assert any(line.split()==[b'Pages:',b'5'] for line in info.splitlines())
run('pdftotext',['/opt/homebrew/bin/pdftotext','-layout',str(PDF),str(ROOT/'paper-fresh.txt')])
text=(ROOT/'paper-fresh.txt').read_text()
pages=text.split('\f')
if pages[-1]=='':
    pages.pop()
assert len(pages)==5 and all(page.strip() for page in pages)
for number,page in enumerate(pages,1):
    with (ROOT/('page-'+str(number)+'.txt')).open('x') as handle:
        handle.write(page)
(ROOT/'rasters').mkdir()
run('pdftoppm',['/opt/homebrew/bin/pdftoppm','-f','1','-l','5','-r','120','-png',str(PDF),str(ROOT/'rasters/page')])
images=sorted((ROOT/'rasters').iterdir())
assert [p.name for p in images]==['page-1.png','page-2.png','page-3.png','page-4.png','page-5.png']
after=guard()
save('SOURCE_AFTER_INTAKE.json',after)
assert before==after
save('INTAKE_RESULT.json',{'started_UTC':started,'finished_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASSIVE_CUSTODY_AND_FRESH_DOCUMENT_EXTRACTION_COMPLETE','source_before_after_exact':True,'source_files':61,'source_child_directories':13,'PDF_pages':5,'fresh_rasters':5,'operations':operations,'scientific_or_native_source_support_code_execution':0,'upstream_primary_or_support_semantic_body_reads':0,'mathematical_verdict':None})
print(json.dumps({'status':'PASSIVE_CUSTODY_AND_FRESH_DOCUMENT_EXTRACTION_COMPLETE','source': [61,13],'pages':5,'rasters':5,'programs':'Poppler document programs only','scientific_or_native_source_support_code_execution':0}))
