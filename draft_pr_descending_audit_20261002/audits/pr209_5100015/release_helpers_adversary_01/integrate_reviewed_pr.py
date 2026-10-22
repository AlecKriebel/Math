"""Integrate only actually reviewed/published PR209 bytes; no local Git mutations."""
import sys
if not __debug__ or sys.flags.optimize:raise RuntimeError('Optimized Python prohibited')
from release_binding import context,binding,unchanged,publication,tracker,acquire,exclusive_json,pr_identity,require,digest,durable_mkdir
from pathlib import Path
from datetime import datetime,timezone
import base64,hashlib,json,shutil,subprocess,zipfile
ROOT=Path('/Users/alec/Documents/Math');PUB=Path(__file__).resolve().parent;C=PUB.parent;R=C/'preprint';D=C/'initial_review_20261016'
GH='/opt/homebrew/Cellar/gh/2.85.0/bin/gh';API='repos/AlecKriebel/Math/'
OLD='fd09a95b479f376234835a4494693bb1316c85ec';PREFIX='unsolved_math_prioritization/attempts/5100015/'
require(not (PUB/'PR_PREPARED.json').exists() and not (PUB/'NATIVE_PREPARE_ATTEMPT.json').exists(),'Prior native preparation: reconcile read-only')
_LOCK=acquire(PUB);CTX=context(R);clear=CTX['clear'];z=publication(R,PUB,CTX);t=tracker(R,PUB,CTX,z)
T=PUB/'private_transport'/datetime.now(timezone.utc).strftime('native_prepare_%Y%m%dT%H%M%S%fZ');durable_mkdir(T,exist_ok=False);seq=0

def api(method,path,payload=None):
 global seq
 seq+=1;args=[GH,'api','--method',method,API+path]
 if payload is not None:
  q=T/f'{seq:03d}-request.json';q.write_text(json.dumps(payload));args+=['--input',str(q)]
 run=subprocess.run(args,capture_output=True,timeout=90);(T/f'{seq:03d}-stdout.json').write_bytes(run.stdout);(T/f'{seq:03d}-stderr.txt').write_bytes(run.stderr)
 require(run.returncode==0,'Native call failed; inspect saved result before any retry');return json.loads(run.stdout)

def safe(p,base):
 require(p.is_file() and not p.is_symlink() and p.resolve().is_relative_to(base.resolve()),'Unsafe owned payload')
 require(not any(x.startswith('private') or x in {'__pycache__','reproduction_environment','node_modules','.secrets','.zenodo-state'} for x in p.relative_to(base).parts),'Private payload excluded')
 return p.read_bytes()

pr=api('GET','pulls/209');pr_identity(pr,OLD,True)
i=json.loads((D/'INTAKE.json').read_text());oq=api('GET','contents/unsolved_math_prioritization/QUEUE.md?ref='+OLD);raw=base64.b64decode(oq['content'])
require(oq['sha']==i['Queue_blob'] and hashlib.sha256(raw).hexdigest()==i['Queue_sha256'],'Original QUEUE bytes changed')
original=[x for x in raw.decode().splitlines() if '5100015 / AMR-050-0015' in x];require(original==[i['queue_row']] and original[0].split('|')[8].strip()=='claimed_solved' and original[0].split('|')[9].strip()=='1/5','Exact eligibility/author budget not confirmed')
main=api('GET','git/ref/heads/main')['object']['sha'];mc=api('GET','git/commits/'+main);cache={}
def listing(sha):
 if sha not in cache:
  o=api('GET','git/trees/'+sha);require(not o['truncated'],'Truncated native tree');cache[sha]={r['path']:r for r in o['tree']}
 return cache[sha]
def lookup(path):
 sha=mc['tree']['sha']
 for part in path.split('/'):
  row=listing(sha).get(part)
  if row is None:return None
  sha=row['sha']
 return sha
require(lookup(PREFIX.rstrip('/')) is None,'Fresh main already has this scientific subtree; reconcile rather than overwrite')
mq=api('GET','contents/unsolved_math_prioritization/QUEUE.md?ref='+main);mainq=base64.b64decode(mq['content']).decode();rows=[x for x in mainq.splitlines() if '5100015 / AMR-050-0015' in x];require(len(rows)==1,'Ambiguous main row')
fields=rows[0].split('|');require(len(fields)==14,'Unexpected QUEUE columns')
placeholder=original[0].split('|');placeholder[8]=' queued ';placeholder[9]=' 0/5 '
for n in [10,11,12]:placeholder[n]='  '
require(rows[0]==original[0] or rows[0]=='|'.join(placeholder),'Main row is neither exact original claim nor untouched queued placeholder')
# Retain original 2021 journal source-year; do not silently convert it to the arXiv year.
fields[8]=' claimed_solved ';fields[9]=' 1/5 ';fields[11]=' [Audited outer center-pedal product; credited preprint](attempts/5100015/FINAL_DISPOSITION.md) ';fields[12]=' '+z['doi_url']+' '
queue_row='|'.join(fields);require(mainq.count(rows[0])==1,'Nonunique target text');newq=mainq.replace(rows[0],queue_row)
U=R/'pr_update/5100015';F=PUB/'native_current_source';require(not F.exists(),'Prepared native directory already exists; reconcile')
prefix='k303b_outer_center_pedal_product/pr_update/5100015/'
with zipfile.ZipFile(R/'k303b-source-verification.zip') as archive:
 names={p.relative_to(U).as_posix() for p in U.rglob('*') if p.is_file()};require(names=={s.removeprefix(prefix) for s in archive.namelist() if s.startswith(prefix)},'Native packet ZIP set differs')
 for name in names:require(safe(U/name,U)==archive.read(prefix+name),'Native packet differs from reviewed archive')
shutil.copytree(U,F)
ready=json.loads((F/'readiness.json').read_text());ready.update(current_assessment='claimed_solved audited and published; historical priority unestablished',preprint_upload_cleared=True,whole_package_reviews_completed=clear['fresh_manuscript_reviews'],published_DOI=z['doi'],publication_record=z['record_url'],current_release_receipt='RELEASE_RECEIPT.json');(F/'readiness.json').write_text(json.dumps(ready,indent=2)+'\n')
release=dict(utc=datetime.now(timezone.utc).isoformat(),status='claimed_solved',author_proof_turns='1/5',mathematical_verdict='PASS full signed outer/center-pedal product for strict confocal elliptical caustics and periods not divisible by4, admitted stars/reversal/repetitions',priority='Exact contemporary Ferudunv1.1 Thm2/Section6 and classical KLS/KS/AST/BT/Stachel/Jacobi/conic/meromorphic inputs credited; historical ordering/non-derivation/novelty undetermined; no first/exclusive/new-identity claim',source_year=2021,source_year_role='Published original conjecture edition; arXiv first appeared2020',original_native_head=OLD,original23files_archived_byte_identical=True,manuscript_reviews=clear,publication=z,tracker=t,unrefereed=True,extensive_AI_assistance=True,independent_human_peer_review=False,native_merge_at_receipt_creation='Not yet asserted; later case PR_MERGED.json/GitHub event records actual merge')
for name in ['FINAL_ACCEPTANCE.json','RELEASE_RECEIPT.json']:(F/name).write_text(json.dumps(release,indent=2)+'\n')
(F/'PUBLICATION_RECEIPT.json').write_text(json.dumps(dict(publication=z,tracker=t),indent=2)+'\n');(F/'PUBLICATION_METADATA.json').write_text(json.dumps(z['metadata'],indent=2)+'\n')
status='# Accepted outer center-pedal area product: claimed_solved\n\n'+(U/'STATUS.md').read_text()+'\n\nActual publication completion supersedes the dated preparation/pending language above: required NEW sequential whole-package reviews and every global repair are complete. Exact accepted PDF/verification archive and metadata published at '+z['doi_url']+'. One GWS append/all four cells verified at '+t['updated_range']+'. Exact contemporary and classical credits and historical-priority limitations remain unchanged. FINAL_ACCEPTANCE/RELEASE_RECEIPT bind actual review/publication facts. Native merge remains to be recorded separately; it is not forecast here. All23 originals and reviewed mathematical proof bytes remain unchanged.\n'
for name in ['PUBLICATION_STATUS.md','FINAL_DISPOSITION.md']:(F/name).write_text(status)
(F/'README.md').write_text((U/'README.md').read_text()+'\n\nActual publication update: '+z['doi_url']+'; one verified tracker row '+t['updated_range']+'. Required new sequential whole-package reviews/all fixes completed; dated preparation language above is historical. See RELEASE_RECEIPT.json. Native merge event is recorded separately.\n')
with (F/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+datetime.now(timezone.utc).isoformat()+' — case95%: required fresh whole-package reviews/fixes complete, exact preprint published '+z['doi_url']+', one GWS append/all4cells '+t['updated_range']+'. Native scientific readback and merge pending; author1/5 and23 originals retained.\n')
admin={'readiness.json','README.md','RESEARCH_LOG.md','PUBLICATION_STATUS.md','FINAL_DISPOSITION.md','FINAL_ACCEPTANCE.json','RELEASE_RECEIPT.json','PUBLICATION_RECEIPT.json','PUBLICATION_METADATA.json','MANIFEST.json','CURRENT_PACKET_MANIFEST.json'}
for p in U.rglob('*'):
 if p.is_file() and p.relative_to(U).as_posix() not in admin:require(safe(p,U)==safe(F/p.relative_to(U),F),'Reviewed science/history changed')
require(len(i['original_source_files'])==23,'Original count mismatch')
for row in i['original_source_files']:
 p=F/'history/original_submission_20261016'/Path(row['native_path']).relative_to(PREFIX.rstrip('/'));r=safe(p,F);require(len(r)==row['bytes'] and hashlib.sha256(r).hexdigest()==row['sha256'],'Original archive changed')
def pin(p,base):
 raw=safe(p,base);return dict(path=p.relative_to(base).as_posix(),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
(F/'MANIFEST.json').write_text(json.dumps(dict(scope='Current actual accepted administrative presentation; reviewed mathematics/history unchanged',files=[pin(p,F) for p in sorted(F.iterdir()) if p.is_file() and p.name not in {'MANIFEST.json','CURRENT_PACKET_MANIFEST.json'}]),indent=2)+'\n')
(F/'CURRENT_PACKET_MANIFEST.json').write_text(json.dumps(dict(schema='pr209-current-packet-v1',self_excluded=True,source_head=OLD,files=[pin(p,F) for p in sorted(F.rglob('*')) if p.is_file() and p.name!='CURRENT_PACKET_MANIFEST.json'],release_delta='Actual review/DOI/tracker administrative facts only'),indent=2)+'\n')
files={PREFIX+p.relative_to(F).as_posix():safe(p,F) for p in F.rglob('*') if p.is_file()}
# Select public case payloads explicitly, excluding private source/transport trees.
paths=[p for p in R.iterdir() if p.is_file() and p.suffix not in {'.log','.aux','.out'}]
sm=json.loads((R/'SOURCE_MANIFEST.json').read_text())
for row in sm['files']:
 p=R/row['path'];raw=safe(p,R);require(len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'],'Source manifest changed');paths.append(p)
paths += [p for p in D.iterdir() if p.is_file()]
for folder in ['submitted','root_reproduction_01','root_reproduction_02','root_reproduction_03']:
 paths += [p for p in (D/folder).rglob('*') if p.is_file() and not any(s.startswith('private') or s=='__pycache__' for s in p.relative_to(D/folder).parts)]
paths += [p for p in (D/'priority_public_chronology_01').iterdir() if p.is_file()]
# Any completed newer root replay is carried by its public receipts and non-input outputs.
for folder in D.glob('root_reproduction_04*'):
 for p in folder.rglob('*'):
  if p.is_file() and p.relative_to(folder).parts[0]=='executed' and 'inputs' not in p.relative_to(folder).parts:paths.append(p)
for family in ['source_domain_adversary_01','physical_geometry_adversary_01','meromorphic_divisor_adversary_01','priority_author_updates_01','priority_classical_general_01']:
 folder=D/family;m=json.loads((folder/'AUTHORED_MANIFEST.json').read_text());paths.append(folder/'AUTHORED_MANIFEST.json')
 for row in m.get('files',m.get('payloads')):
  p=folder/row['path'];raw=safe(p,folder);require(len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'],'Scoped audit seal changed');paths.append(p)
 if family=='priority_author_updates_01':
  seal=folder/'AUTHORED_MANIFEST_SUPPLEMENT_TIMESTAMP_CORRECTION.json';supp=json.loads(seal.read_text());paths.append(seal)
  for row in [supp['original_manifest'],*supp['original_payloads_unchanged'],*supp['supplemental_payloads']]:
   p=folder/row['path'];raw=safe(p,folder);require(len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'],'Supplement changed');paths.append(p)
for pattern in ['whole_package_adversary_*','release_helpers_adversary_*']:
 for folder in sorted(C.glob(pattern)):
  seal=folder/'AUTHORED_MANIFEST.json';require(seal.exists(),'Unsealed reviewer folder cannot be integrated');m=json.loads(seal.read_text());paths.append(seal)
  rows=m.get('authored_files',m.get('files',m.get('entries')));require(type(rows) is list,'Unknown review manifest schema')
  for row in rows:
   p=folder/row.get('path',row.get('relative_path'));raw=safe(p,folder);require(len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'],'Reviewer seal changed');paths.append(p)
paths += [p for p in PUB.iterdir() if p.is_file()]
for p in sorted(set(paths)):files[p.relative_to(ROOT).as_posix()]=safe(p,C)
files['unsolved_math_prioritization/QUEUE.md']=newq.encode();entries=[];pins=[]
for path,raw in sorted(files.items()):
 blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
 try:entry=dict(path=path,mode='100644',type='blob',content=raw.decode())
 except UnicodeDecodeError:
  require(api('POST','git/blobs',dict(content=base64.b64encode(raw).decode(),encoding='base64'))['sha']==blob,'Uploaded blob mismatch');entry=dict(path=path,mode='100644',type='blob',sha=blob)
 entries.append(entry);pins.append(dict(path=path,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),git_blob_sha1=blob))
tree=api('POST','git/trees',dict(base_tree=mc['tree']['sha'],tree=entries))['sha'];head=api('POST','git/commits',dict(message='Integrate PR209 audited outer center-pedal preprint and verified DOI/tracker; preserve23 original artifacts',tree=tree,parents=[OLD,main]))['sha']
pr_identity(api('GET','pulls/209'),OLD,True);unchanged(R,CTX);publication(R,PUB,CTX);tracker(R,PUB,CTX,z)
commit=api('GET','git/commits/'+head);require(commit['tree']['sha']==tree and [x['sha'] for x in commit['parents']]==[OLD,main],'Native commit mismatch')
exclusive_json(PUB/'NATIVE_PREPARE_ATTEMPT.json',dict(utc=datetime.now(timezone.utc).isoformat(),old=OLD,head=head,main=main,branch='dot/math-5100015',nonforce=True,release_binding=binding(CTX)))
api('PATCH','git/refs/heads/'+pr['head']['ref'],dict(sha=head,force=False))
receipt=dict(utc=datetime.now(timezone.utc).isoformat(),prepared_head=head,original_head=OLD,main_parent=main,parents=[OLD,main],tree=tree,target_queue_row=queue_row,included_owned_pins=pins,doi_url=z['doi_url'],tracker_range=t['updated_range'],native_merge='Pending full exact readback',local_Git_index_ref_mutations=0,foreign_main_tree_preserved=True,release_binding=binding(CTX),publication_receipt_sha256=digest(PUB/'ZENODO_VERIFIED_PUBLICATION.json'),tracker_receipt_sha256=digest(PUB/'TRACKER_VERIFIED_APPEND.json'))
(PUB/'PR_PREPARED.json').write_text(json.dumps(receipt,indent=2)+'\n')
body='Proves k303,b: signed product of the OUTER tangent-polygon area and actual center-perpendicular-foot area on its boundary tangent side lines, for strict confocal elliptical caustics and periods not divisible by four, admitted coprime stars/reversal/fixed repeats. All23 original artifacts and author turn1/5 preserved.\n\nExplicit fixed-linear edge-vector map, signed-area traces and classical odd Jacobi identity give the full proof and invariant value. KLS2002/KS2003-2004/AST-BT2020/Stachel/Jacobi/conic and established meromorphic methods credited. A.Ferudun2026v1.1 Theorem2/Section6 is the exact contemporary full theorem; v1.0 primitive-even subset distinguished. Historical ordering, non-derivation and novelty undetermined; no first/exclusive/new-identity/current-worldwide-open claim.\n\nExtensive mathematical/source reproduction, bounded priority audit and required NEW sequential whole-package adversaries/all global fixes completed. Exact controls and labelled uncertified diagnostics accompany the note. Extensive AI use; unrefereed, no independent human peer review or formal verification.\n\nVerified preprint/source archive: '+z['doi_url']+'. One GWS append/all4cells verified '+t['updated_range']+'.'
api('PATCH','pulls/209',dict(title='5100015: audited outer center-pedal area product and published preprint',body=body));require(api('GET','git/ref/heads/'+pr['head']['ref'])['object']['sha']==head,'Ref readback mismatch')
print(json.dumps({k:v for k,v in receipt.items() if k!='included_owned_pins'},indent=2))
