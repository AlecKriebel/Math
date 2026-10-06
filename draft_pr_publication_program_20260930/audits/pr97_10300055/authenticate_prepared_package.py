from pathlib import Path, PurePosixPath
import json, hashlib, datetime, os, zipfile

A=Path(__file__).resolve().parent
D=A/'contingent_credited_note_v1'
M=D/'CLOSED_MANIFEST.json'
expected='ca4ce63be4957fc836b9e0a5d30dc7049eb22e33cc50d15994444d8e4638adc3'
def require(c,m):
    if not c: raise RuntimeError(m)
def sha(b): return hashlib.sha256(b).hexdigest()
def checked(path,row):
    require(path.is_file() and not path.is_symlink(),'Invalid file '+str(path))
    b=path.read_bytes()
    require(len(b)==row['bytes'] and sha(b)==row['sha256'],'Pin mismatch '+str(path))
    return b
raw=M.read_bytes();require(sha(raw)==expected,'Closed manifest changed')
r=json.loads(raw);own=[];borrow=[]
for row in r['files']:
    rel=PurePosixPath(row['path'])
    require(not rel.is_absolute() and '..' not in rel.parts,'Unsafe manifest path')
    p=D/row['path'];require(p.resolve().is_relative_to(D.resolve()),'Own path escape')
    checked(p,row);own.append(row)
actual={p.relative_to(D).as_posix() for p in D.rglob('*') if p.is_file()}
require(len(own)==len({x['path'] for x in own}),'Duplicate own manifest member')
require(actual=={x['path'] for x in own}|set(r['excluded']),'Closed inventory differs')
require(r['excluded']==['CLOSED_MANIFEST.json'],'Unexpected excluded body')
for row in r['borrowed_input_bindings']:
    p=A/row['reference'];require(p.resolve().is_relative_to(A.resolve()),'Borrowed escape')
    checked(p,row);borrow.append(row)
public=D/'publicfiles';pm=public/'MANIFEST.json';pr=json.loads(pm.read_text())
with zipfile.ZipFile(D/'pr97_support.zip') as z:
    names=z.namelist()
    require(len(names)==len(set(names)),'ZIP duplicate')
    require(set(names)=={x['path'] for x in pr['files']}|{'MANIFEST.json'},'ZIP closure differs')
    for name in names:
        require(z.read(name)==(public/name).read_bytes(),'ZIP/directory body differs')
for dest,source in [('support/CANDIDATE.md','credited_verification_candidate_v2/CANDIDATE.md'),('support/review/author_replay/CANDIDATE.md','credited_verification_candidate_v2/CANDIDATE.md'),('support/verify.py','credited_verification_candidate_v2/verify.py'),('support/review/independent_checks.py','credited_verification_candidate_v2/review/independent_checks.py')]:
    require((public/dest).read_bytes()==(A/source).read_bytes(),'Current proof/code copy differs')
custody=json.loads((D/'CUSTODY.json').read_text())
for key,rel in [('source_sha256','publicfiles/pr97_note.tex'),('pdf_sha256','publicfiles/pr97_note.pdf'),('payload_manifest_sha256','publicfiles/MANIFEST.json'),('zip_sha256','pr97_support.zip'),('metadata_sha256','publicfiles/zenodo_metadata.proposed.json')]:
    require(sha((D/rel).read_bytes())==custody[key],'Custody mismatch '+key)
deposit=json.loads((D/'zenodo-deposit.proposed.json').read_text())
metadata=json.loads((public/'zenodo_metadata.proposed.json').read_text())
require(deposit['metadata']==metadata,'Proposed metadata wrapper differs')
require(sha(M.read_bytes())==expected,'Manifest changed during authentication')
receipt={'schema':'pr97-root-prepared-package-custody-authentication/v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'operator_PID':os.getpid(),'package':str(D),'closed_manifest_sha256':expected,'own_files_authenticated':len(own),'borrowed_inputs_authenticated':len(borrow),'payload_files':len(pr['files']),'zip_members':len(names),'zip_directory_byte_identity':True,'adopted_proof_and_mathematical_code_byte_identity':True,'custody_and_metadata_bindings_match':True,'ROOT_full_preparation_report_and_long_candidate_read':True,'all_file_content_substantively_reviewed_by_ROOT':False,'whole_package_adversary':'pr97_whole_package_round1_20261006','whole_package_acceptance':False,'priority_clearance':False,'publication_authorized':False,'original_effort':'2/5','new_central_proof_search_turns':0,'program_completion_percent':13/99*100,'workflow_estimate_percent':40,'own_pins':own,'borrowed_pins':borrow}
(A/'ROOT_PREPARED_PACKAGE_AUTHENTICATION_20261006.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k not in ['own_pins','borrowed_pins']}))
