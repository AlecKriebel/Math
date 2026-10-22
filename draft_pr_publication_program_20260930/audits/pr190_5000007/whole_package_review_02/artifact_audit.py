"""Independent exact bytes, membership, replica, and publication-scope audit."""
from pathlib import Path, PurePosixPath
import datetime, hashlib, json, re, stat, zipfile
R=Path(__file__).resolve().parent; A=R.parent; P=A/'publication_package_v2'
def digest(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def need(x,m):
    if not x:raise ValueError(m)
def check(path,spec):
    b=path.read_bytes();actual=digest(b);need(actual=={k:spec[k] for k in ('bytes','sha256')},'byte mismatch '+str(path));return {'path':str(path.relative_to(A)),**actual,'mode':oct(stat.S_IMODE(path.stat().st_mode))}
authority=A/'ROOT_WHOLE_REVIEW_INPUT_02.json'
need(hashlib.sha256(authority.read_bytes()).hexdigest()=='0b92036ef757a041bc433c9a606bff802210dc76637c92e2abad093fd95006ff','authority changed')
auth=json.loads(authority.read_text()); bound=[]
for name,s in auth['other_exact_inputs'].items():bound.append(check(A/name,s))
fm=P/'FINAL_REVIEW_PACKET_MANIFEST.json';need(hashlib.sha256(fm.read_bytes()).hexdigest()==auth['package_manifest_SHA256'],'packet manifest mismatch')
packet=json.loads(fm.read_text());payloads=[check(P/n,s) for n,s in packet['payloads'].items()]
with zipfile.ZipFile(P/'verification-package.zip') as z:
    names=z.namelist();need(len(names)==len(set(names))==255,'zip duplicate/entry count')
    need(all(not n.endswith('/') and not PurePosixPath(n).is_absolute() and '..' not in PurePosixPath(n).parts for n in names),'unsafe ZIP member')
    need(all(not stat.S_ISLNK(i.external_attr>>16) for i in z.infolist()),'ZIP symlink')
    manifest=json.loads(z.read('MANIFEST.json')); files=manifest['files'];need(len(files)==254,'manifest count')
    need(set(names)==set(files)|{'MANIFEST.json'},'ZIP membership mismatch')
    ziprows=[];privacy=[];credential_hits=[]
    for n,s in files.items():
        b=z.read(n);need(digest(b)==s,'zip member hash mismatch '+n)
        need((P/'verification'/n).read_bytes()==b,'extracted member mismatch '+n)
        ziprows.append({'path':n,**s})
        if (b.startswith(b'%PDF-') and not (n=='manuscript/dodecahedron_endpoint.pdf' and b==(P/'dodecahedron_endpoint.pdf').read_bytes())) or b.startswith(b'PK\x03\x04') or re.search(r'(^|/)(private|private_sources|cache|cookies|\.env|\.git)(/|$)',n):privacy.append(n)
        for pat in (rb'gh[pousr]_[A-Za-z0-9]{30,}',rb'sk-(?:proj-)?[A-Za-z0-9_-]{32,}',rb'-----BEGIN [A-Z ]*PRIVATE KEY-----',rb'Bearer\s+[A-Za-z0-9._-]{24,}'):
            if re.search(pat,b):credential_hits.append(n)
    need(not privacy and not credential_hits,'privacy or credential hit: '+repr(privacy+credential_hits))
    need((P/'verification/MANIFEST.json').read_bytes()==z.read('MANIFEST.json'),'manifest copy mismatch')
    original=json.loads((A/'ORIGINAL_FILE_MANIFEST.json').read_text())['files'];original_rows=[]
    for s in original:
        n=s['path'];b=z.read('historical_original/'+n);need(digest(b)=={k:s[k] for k in ('bytes','sha256')},'historical original mismatch')
        need((A/'original_submission/files'/n).read_bytes()==b,'original submission mismatch')
        original_rows.append({'path':n,**digest(b)})
native_manifest=json.loads((A/'integration_preparation/CURRENT_TEMPLATE.json').read_text());N=A/'integration_preparation'/native_manifest['current_template']
actual={str(x.relative_to(N)) for x in N.rglob('*') if x.is_file()};need(actual==set(native_manifest['files']) and len(actual)==49,'native membership/count')
native_rows=[check(N/n,s) for n,s in native_manifest['files'].items()]
for s in original:
    name=s['path'].split('/5000007/',1)[1];check(N/'historical_original'/name,s)
replica_rows=[]
for name in ['check_certificate.py','check_half_turn.py','check_pinned_coordinates.py','run_verification.py','test_reconstruction.py']:
    expected=(P/'verification/current'/name).read_bytes()
    paths=[A/'current_verification'/name,N/'verification/current'/name]
    if (N/name).exists():paths.append(N/name)
    for p in paths:
        need(p.read_bytes()==expected,'current replica mismatch '+str(p));replica_rows.append({'path':str(p.relative_to(A)),**digest(expected)})
for p in [P/'verification/CURRENT_PROOF.md',N/'PROOF_V2.md']:
    need(p.read_bytes()==(A/'CURRENT_PROOF.md').read_bytes(),'proof replica mismatch');replica_rows.append({'path':str(p.relative_to(A)),**digest(p.read_bytes())})
md=json.loads((P/'zenodo-deposit.json').read_text());m=md['metadata'];need(m['title']=='A parity-selected endpoint theorem for the regular dodecahedron','title');need(m['creators']==[{'name':'Kriebel, Alec','affiliation':'Independent researcher','orcid':'0009-0001-9320-500X'}],'author');need(m['publication_date']=='2026-10-15' and m['version']=='1.0' and m['license']=='cc-by-4.0' and m['publication_type']=='preprint','scope metadata');need([f['path'] for f in md['files']]==['dodecahedron_endpoint.pdf','dodecahedron_endpoint.tex','verification-package.zip'],'uploader file set')
for t in ['unrefereed','AI tools','no','firstness','Ferudun','Athreya','Troubetzkoy','DOI-version']:
    need(t in m['description'],'metadata qualification missing '+t)
current_texts={n:(N/n).read_text() for n in ['CANDIDATE_PROOF.md','EXTERNAL_CERTIFICATE_AUDIT.md','LITERATURE_CHECK.md','PROOF_V2.md','PUBLICATION_RECEIPT.md','README.md','RESEARCH_LOG.md','SIMPLIFICATION_NOTE.md','source_interpretation.json','independent_review/FINAL_REVIEW.md']}
out={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'authority':digest(authority.read_bytes()),'bound_inputs':bound,'five_payloads':payloads,'ZIP':{'entries':len(names),'payloads':len(ziprows),'all_payloads':ziprows,'hashes_and_local_bytes_match':True,'safe_paths':True,'downloaded_bodies_archives_cache_credentials_found':privacy+credential_hits},'native':{'count':len(native_rows),'pointer':native_manifest['current_template'],'files':native_rows,'original22_authentic':True},'original22':original_rows,'current_replicas':replica_rows,'metadata':{'author_ORCID_title_date_scope_credits_verified':True,'upload_files':md['files']},'assembly_state':{'UTC':packet['UTC'],'reviews_complete_at_assembly':packet['whole_package_adversarial_reviews_complete'],'Zenodo_published_at_assembly':packet['Zenodo_published']},'result':'PASS'}
(R/'ARTIFACT_AUDIT_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k in ['UTC','result','assembly_state']},indent=2));print('Five payloads, 254 payload hashes + ZIP manifest, 49 native and 22 historical files authenticated; current replicas agree; credential/body/cache screening clear.')
