"""Check frozen scientific identity and independently bind primary sources."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess,os,io,zipfile,struct
HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent.parent
ROOT=Path('/Users/alec/Documents/Math')
BIND=json.loads((HERE/'INPUT_BINDING.json').read_bytes())
GATE=json.loads((AUDIT/'FINAL_PUBLICATION_GATE.json').read_bytes())
def pin(b):return {'size':len(b),'sha256':hashlib.sha256(b).hexdigest()}
native={}
archive_bytes=(AUDIT/'publication/gns_verification.zip').read_bytes()
with zipfile.ZipFile(io.BytesIO(archive_bytes))as z:
    if len(z.namelist())!=len(set(z.namelist())):raise RuntimeError('Duplicate ZIP members')
    for rel,receipt in GATE['reviewed_inputs'].items():
        if not rel.startswith('native/'):continue
        gitpath=rel[len('native/'):]
        blob=subprocess.run(['git','cat-file','blob',GATE['original_pr_head']+':'+gitpath],cwd=ROOT,env={**os.environ,'GIT_OPTIONAL_LOCKS':'0'},capture_output=True,check=True).stdout
        member='candidate/'+gitpath.split('/attempts/30001184/',1)[1]
        native[rel]={'original_blob_matches':pin(blob)==receipt,'zip_member_matches':pin(z.read(member))==receipt,'archive_member':member}
    manifest=json.loads(z.read('PACKAGE_MANIFEST.json'))
    receipts=manifest['files']if isinstance(manifest,dict)and'files'in manifest else manifest
    integrity={r['path']:pin(z.read(r['path']))=={'size':r['bytes'],'sha256':r['sha256']}for r in receipts}
    names=set(z.namelist());expected=set(integrity)|{'PACKAGE_MANIFEST.json'}
    if names!=expected or len(integrity)!=87:raise RuntimeError('ZIP inventory mismatch')
    transport_in_zip=any('native_transport'in n or b'native_transport'in z.read(n)for n in names)
if len(native)!=29 or not all(v['original_blob_matches']and v['zip_member_matches']for v in native.values())or not all(integrity.values())or transport_in_zip:raise RuntimeError('Scientific identity drift')
pdf=AUDIT/'publication/gns_generation_counterexample.pdf'
text=subprocess.run(['pdftotext',str(pdf),'-'],capture_output=True,check=True).stdout
if b'native_transport'in text or b'native transport'in text.lower():raise RuntimeError('Transport unexpectedly in paper')
info=subprocess.run(['pdfinfo','-f','1','-l','5','-box',str(pdf)],capture_output=True,check=True).stdout
if info.count(b'612 x 792 pts')!=5 or info.count(b'rot:   0')!=5:raise RuntimeError('Independent geometry mismatch')
(HERE/'PDF_GEOMETRY.txt').write_bytes(info)
eocd=archive_bytes.rfind(b'PK\x05\x06');toc=struct.unpack_from('<I',archive_bytes,eocd+16)[0]
if toc!=218946 or archive_bytes[toc:toc+4]!=b'PK\x01\x02':raise RuntimeError('Raw EOCD mismatch')
primary={}
sourcebind=json.loads((AUDIT/'reviews/native_transport_review2/PRIMARY_SOURCE_BINDING.json').read_bytes())
for name,receipt in sourcebind.items():
    path=ROOT/receipt['snapshot'];data=path.read_bytes()
    if pin(data)!={'size':receipt['size'],'sha256':receipt['sha256']}:raise RuntimeError('Primary source drift '+name)
    primary[name]={'path':str(path),'size':len(data),'sha256':hashlib.sha256(data).hexdigest()}
for name in ('file_service_config.py','file_schema.py','extractor_zip.py'):
    path=AUDIT/'reviews/native_transport_author/tmp/primary'/name;data=path.read_bytes()
    expected=next(r['sha256']for r in json.loads((AUDIT/'reviews/native_transport_author/SOURCE_RECEIPT.json').read_bytes())['F5_primary_sources']if r['name']==name)
    if hashlib.sha256(data).hexdigest()!=expected:raise RuntimeError('F5 source drift '+name)
    primary[name]={'path':str(path),**pin(data)}
report={'checked_utc':datetime.now(timezone.utc).isoformat(),'gate45_match':all(pin((AUDIT/n).read_bytes())==r for n,r in GATE['reviewed_inputs'].items()),'original_head':GATE['original_pr_head'],'native29':native,'native29_original_equal':True,'native29_zip_equal':True,'zip_manifest87':integrity,'zip_manifest87_valid':True,'transport_absent_pdf_zip':True,'pdf_geometry_each_page':[612,792],'pdf_rotation_each_page':0,'raw_EOCD_position':eocd,'raw_EOCD_directory_offset':toc,'central_directory_signature_hex':archive_bytes[toc:toc+4].hex(),'primary_source_pins':primary,'network_calls':0,'unchanged_math_reproved':False}
if not report['gate45_match']:raise RuntimeError('Accepted gate drift')
(HERE/'ORIGINAL_ARCHIVE_PRIMARY_BINDING.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items()if k not in('native29','zip_manifest87','primary_source_pins')},indent=2))
