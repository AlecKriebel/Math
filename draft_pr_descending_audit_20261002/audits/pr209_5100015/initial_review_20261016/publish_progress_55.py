"""Checkpoint scientific review/repair and explicit open workflow findings, not release."""
from pathlib import Path
import ast,json,hashlib
D=Path(__file__).resolve().parent;p=D/'publish_progress_45.py';t=ast.parse(p.read_text())
t.body=[n for n in t.body[:-1] if not(isinstance(n,ast.Assert) and 'PROGRESS_45_CHECKPOINT_RECEIPT' in ast.unparse(n))]
ns={'__file__':str(p)};exec(compile(t,str(p)+'[definitions-only]','exec'),ns);source=ns['source']
assert not (D/'PROGRESS_55_CHECKPOINT_RECEIPT.json').exists()
extra="""C=D.parent
for name in ['whole_package_adversary_01','release_helpers_adversary_01']:
    folder=C/name;seal=folder/'AUTHORED_MANIFEST.json';m=json.loads(seal.read_text());paths.append(seal)
    for row in m['files']:
        q=folder/row['path'];raw=q.read_bytes()
        assert q.resolve().is_relative_to(folder.resolve()) and not q.is_symlink()
        assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
        paths.append(q)
    if name=='whole_package_adversary_01':
        seal=folder/'AUTHORED_MANIFEST_SUPPLEMENT_REPORT_CORRECTION.json';s=json.loads(seal.read_text());paths.append(seal)
        for row in [s['original_manifest'],*s['original_payloads_unchanged'],*s['supplemental_payloads']]:
            q=folder/row['path'];raw=q.read_bytes()
            assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
            paths.append(q)
paths += [p for p in (B/'history/review01_frozen').rglob('*') if p.is_file()]
paths += [p for p in (D/'root_reproduction_05_whole_review01_controls').iterdir() if p.is_file()]
paths.append(D/'root_reproduction_06_harness_failure_controls/HARNESS_FAILURE_CONTROLS.json')
R=D/'root_reproduction_07_portable_zip_review01_fixed/executed'
paths.append(R/'REPRODUCTION.json')
for folder in R.iterdir():
    if folder.is_dir():
        paths += [p for p in folder.rglob('*') if p.is_file() and 'inputs' not in p.relative_to(folder).parts]
PUB=C/'publication';paths.append(PUB/'PROGRESS_BASELINE.json')
paths += [p for p in (PUB/'progress_baseline_01').iterdir() if p.is_file()]
"""
changes=[
("OUT=D/'PROGRESS_45_CHECKPOINT_RECEIPT.json'","OUT=D/'PROGRESS_55_CHECKPOINT_RECEIPT.json'"),
("prior=json.loads((D/'PROGRESS_35_CHECKPOINT_RECEIPT.json').read_text())","prior=json.loads((D/'PROGRESS_45_CHECKPOINT_RECEIPT.json').read_text())"),
("assert prior['commit']=='f9862f73ca1589941876b0c2ebad0782ffbb4894'","assert prior['commit']=='d03508747f8fefc94f18793909372c16c3cd4ba8'"),
("assert state['completion_percent']==45 and state['preprint_preparation_cleared'] is True","assert state['completion_percent']==55 and state['preprint_preparation_cleared'] is True"),
("strftime('progress45_%Y%m%dT%H%M%S%fZ')","strftime('progress55_%Y%m%dT%H%M%S%fZ')"),
("paths += [OLD/'FINAL_COMPLETION_CHECKPOINT_PUBLICATION_RECEIPT.json'",extra+"paths += [OLD/'FINAL_COMPLETION_CHECKPOINT_PUBLICATION_RECEIPT.json'"),
("assert len(entries)<600","assert len(entries)<750"),
("Checkpoint PR209 at45%: credited five-page note and verified portable package, first whole-package review active","Checkpoint PR209 at55%: first whole-package repair and real ZIP replay; new review active, workflow findings open"),
("case_completion_percent=45","case_completion_percent=55"),
]
for old,new in changes:
 assert source.count(old)==1,old;source=source.replace(old,new)
# Preserve exact large request bytes losslessly without a duplicate giant plaintext file.
source=source.replace('import base64,hashlib,json,subprocess','import base64,hashlib,json,subprocess,gzip,os')
old="""    if payload is not None:
        q=T/f'{seq:03d}-request.json'
        q.write_text(json.dumps(payload))
        args+=['--input',str(q)]
    run=subprocess.run(args,capture_output=True,timeout=60)"""
new="""    request_bytes=None
    if payload is not None:
        request_bytes=json.dumps(payload).encode()
        if len(request_bytes)>262144:
            q=T/f'{seq:03d}-request.json.gz';packed=gzip.compress(request_bytes,compresslevel=9,mtime=0)
            with q.open('xb') as handle:
                handle.write(packed);handle.flush();os.fsync(handle.fileno())
            assert gzip.decompress(q.read_bytes())==request_bytes
            (T/f'{seq:03d}-request-pin.json').write_text(json.dumps(dict(method=method,path=path,bytes=len(request_bytes),sha256=hashlib.sha256(request_bytes).hexdigest(),retained_gzip=q.name,gzip_bytes=len(packed),round_trip_byte_identical=True)))
        else:
            q=T/f'{seq:03d}-request.json';q.write_bytes(request_bytes)
        args+=['--input','-']
    run=subprocess.run(args,input=request_bytes,capture_output=True,timeout=60)"""
assert source.count(old)==1;source=source.replace(old,new)
exec(compile(source,str(D/'publish_progress_55.py')+'[pinned-template]','exec'),{'__file__':str(D/'publish_progress_55.py'),'__name__':'__main__'})
