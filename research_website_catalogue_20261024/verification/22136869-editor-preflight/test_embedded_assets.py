"""Positive and semantic negative controls; original sources remain read-only."""
from pathlib import Path
from tempfile import TemporaryDirectory
from contextlib import contextmanager
from io import BytesIO
import sys, json, hashlib, shutil, zipfile, warnings, subprocess, datetime, copy
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from published_assets import PublishedAssets
PAPER=ROOT/'papers/22136869'
SOURCE=PAPER/'sources'
CONTENT=json.loads((PAPER/'reviews/scope/content.json').read_text())
RECEIPT=json.loads((SOURCE/'receipt.json').read_text())
BINDINGS=CONTENT['source_binding']['embedded_assets']
REPORT=[]
def sha(data):return hashlib.sha256(data).hexdigest()
def record(name,passed,**extra):
 REPORT.append({'control':name,'passed':bool(passed),**extra})
 if not passed:raise AssertionError(name)
@contextmanager
def fixture():
 with TemporaryDirectory(prefix='embedded-asset-fixture-')as tmp:
  s=Path(tmp)/'sources';shutil.copytree(SOURCE,s)
  yield s,copy.deepcopy(RECEIPT),copy.deepcopy(BINDINGS)
def reject(name,mutate,error,fragment):
 with fixture()as(s,r,b):
  target=mutate(s,r,b) or BINDINGS[0]['filename']
  try:PublishedAssets(s,r,b).resolve(target)
  except error as exc:
   record(name,fragment in str(exc),exception=type(exc).__name__,diagnostic=str(exc).replace(str(s),'<fixture>'))
  else:record(name,False)
def reseal_zip(s,r,transform):
 name=BINDINGS[0]['archive_filename'];p=s/name
 with zipfile.ZipFile(p)as z:entries=[(x,z.read(x))for x in z.infolist()]
 with warnings.catch_warnings():
  warnings.simplefilter('ignore',UserWarning)
  with zipfile.ZipFile(p,'w',compression=zipfile.ZIP_DEFLATED)as z:
   for n,data in transform(entries):z.writestr(n,data)
 a=next(x for x in r['files']if x['name']==name);a['bytes']=p.stat().st_size;a['sha256']=sha(p.read_bytes())
resolver=PublishedAssets(SOURCE,RECEIPT,BINDINGS)
for item in RECEIPT['files']:
 resolved=resolver.resolve(item['name']);record('unchanged deposited asset: '+item['name'],not resolved.embedded and sha(resolved.read_bytes())==item['sha256'])
for item in BINDINGS:
 resolved=resolver.resolve(item['filename'])
 pages=subprocess.check_output(['/opt/homebrew/bin/pdftotext',str(resolved.path),'-'],text=True).split('\f')
 if not pages[-1].strip():pages.pop()
 record('actual embedded PDF: '+item['filename'],resolved.embedded and sha(resolved.read_bytes())==item['sha256'] and len(pages)==item['pages']==2 and all(len(t.strip())>100 for t in pages),pages=len(pages),sha256=resolved.sha256)
# Existing receipt filename spelling remains accepted.
r=copy.deepcopy(RECEIPT)
for a in r['files']:a['filename']=a.pop('name')
record('legacy receipt filename key',PublishedAssets(SOURCE,r).resolve(CONTENT['pdf_filename']).sha256==CONTENT['source_binding']['pdf_sha256'])

def mutate_archive(s,r,b):
 p=s/b[0]['archive_filename'];p.write_bytes(p.read_bytes()+b'changed')
reject('tampered original ZIP',mutate_archive,ValueError,'Deposited asset SHA-256 mismatch')
def mutate_source(s,r,b):
 p=s/b[0]['source_relative_path'];p.write_bytes(p.read_bytes()+b'changed')
reject('tampered extracted PDF',mutate_source,ValueError,'Extracted source differs')
def mutate_member(s,r,b):
 target=b[0]['archive_member'];reseal_zip(s,r,lambda entries:[(x,data+b'changed'if x.filename==target else data)for x,data in entries])
reject('changed member even with fixture receipt resealed',mutate_member,ValueError,'Embedded ZIP member SHA-256 mismatch')
def wrong_sha(s,r,b):b[0]['sha256']='0'*64
reject('tampered member binding SHA256',wrong_sha,ValueError,'Embedded ZIP member SHA-256 mismatch')
def missing_member(s,r,b):
 target=b[0]['archive_member'];reseal_zip(s,r,lambda entries:[(x,data)for x,data in entries if x.filename!=target])
reject('missing original member',missing_member,ValueError,'Missing embedded ZIP member')
def missing_source(s,r,b):(s/b[0]['source_relative_path']).unlink()
reject('missing extracted PDF',missing_source,FileNotFoundError,BINDINGS[0]['filename'])
def missing_archive(s,r,b):(s/b[0]['archive_filename']).unlink()
reject('missing original ZIP',missing_archive,FileNotFoundError,BINDINGS[0]['archive_filename'])
def duplicate_binding(s,r,b):b.append(copy.deepcopy(b[0]))
reject('duplicate embedded filename binding',duplicate_binding,ValueError,'Duplicate or ambiguous embedded filename')
def duplicate_member_binding(s,r,b):b[1]['archive_member']=b[0]['archive_member']
reject('duplicate member under another binding',duplicate_member_binding,ValueError,'Duplicate embedded member/source binding')
def duplicate_source_binding(s,r,b):b[1]['source_relative_path']=b[0]['source_relative_path']
reject('duplicate extracted-source binding',duplicate_source_binding,ValueError,'Duplicate embedded member/source binding')
def duplicate_receipt(s,r,b):r['files'].append(copy.deepcopy(r['files'][0]))
reject('duplicate receipt filename',duplicate_receipt,ValueError,'Duplicate receipt asset')
def conflict_receipt(s,r,b):r['files'][0]['filename']='other.pdf'
reject('conflicting receipt name/filename',conflict_receipt,ValueError,'Conflicting receipt name and filename')
def duplicate_zip(s,r,b):
 target=b[0]['archive_member'];reseal_zip(s,r,lambda entries:entries+[next(x for x in entries if x[0].filename==target)])
reject('duplicate ZIP member with fixture receipt resealed',duplicate_zip,ValueError,'Duplicate ZIP member')
def unbound_zip(s,r,b):r['files']=[x for x in r['files']if x['name']!=b[0]['archive_filename']]
reject('archive absent from public receipt',unbound_zip,ValueError,'not a deposited ZIP')
def receipt_shadow(s,r,b):b[0]['filename']=CONTENT['pdf_filename']
reject('embedded binding shadows deposited file',receipt_shadow,ValueError,'Duplicate or ambiguous embedded filename')
for field,value in [('filename','../escape.pdf'),('archive_filename','/tmp/archive.zip'),('archive_member','../escape.pdf'),('archive_member','/absolute.pdf'),('archive_member','C:\\escape.pdf'),('source_relative_path','../escape.pdf'),('source_relative_path','/tmp/escape.pdf'),('source_relative_path','published-source/./a.pdf'),('source_relative_path','published-source//a.pdf')]:
 def bad_path(s,r,b,field=field,value=value):b[0][field]=value
 reject('unsafe '+field+': '+value,bad_path,ValueError,'Unsafe asset path')
def unsafe_zip(s,r,b):reseal_zip(s,r,lambda entries:entries+[('../escape.txt',b'outside')])
reject('unsafe unrelated ZIP member',unsafe_zip,ValueError,'Unsafe asset path')
def symlink_source(s,r,b):
 p=s/b[0]['source_relative_path'];dest=s.parent/'outside.pdf';dest.write_bytes(p.read_bytes());p.unlink();p.symlink_to(dest)
reject('symlink extracted source outside directory',symlink_source,ValueError,'Symlink in asset path')
def bad_pages(s,r,b):b[0]['pages']=True
reject('boolean page-count binding',bad_pages,ValueError,'Invalid embedded PDF page count')
def missing_binding(s,r,b):b.pop(0)
reject('requested PDF without provenance binding',missing_binding,ValueError,'no deposited or embedded binding')
# A file changed after resolution is rejected before a renderer can copy it.
with fixture()as(s,r,b):
 a=PublishedAssets(s,r,b).resolve(b[0]['filename']);a.path.write_bytes(a.path.read_bytes()+b'changed')
 try:a.read_bytes()
 except ValueError as e:record('post-resolution source tamper',str(e).startswith('Resolved asset changed'))
 else:record('post-resolution source tamper',False)
report={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'controls':REPORT,'passed':sum(x['passed']for x in REPORT),'failed':[x for x in REPORT if not x['passed']],'published_sources_modified':False,'scope':'asset resolver integrity only; no mathematical verifier or website generation'}
(HERE/'asset-controls.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'passed':report['passed'],'failed':report['failed']},indent=2))
