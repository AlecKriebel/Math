"""Construct one reproducible authored PR196 supplement; no remote operations."""
from pathlib import Path
import datetime,hashlib,json,subprocess,sys,zipfile
A=Path(__file__).resolve().parent.parent;D=A/'publication_package_v1';W=A/'package_work_01'
def enc(j):return (json.dumps(j,indent=2,ensure_ascii=True)+'\n').encode()
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def put(n,b):
 p=D/n
 with p.open('xb') as f:f.write(b)
def require(x,m):
 if not x:raise RuntimeError(m)
stamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
mg=json.loads((A/'ROOT_MATHEMATICAL_GATE_01.json').read_bytes());pg=json.loads((A/'ROOT_PRIORITY_GATE_01.json').read_bytes())
require(mg['mathematical_clearance'] and pg['bounded_priority_audit_complete'] and not pg['historical_priority_established'],'gates')
title='An interior second-order defect from a Hele-Shaw contact arc'
metadata={'title':title,'upload_type':'publication','publication_type':'preprint','description':"A detailed attributed proof/application of Ross–Witt Nyström's smooth Hele-Shaw contact-arc construction. The associated bounded weak homogeneous complex Monge–Ampère solution on P1 times the disc lacks a second-order real Taylor expansion at a genuine interior point, despite smooth strictly positive fibre boundary forms. A zero-area arc filling gives a strict Green-function time-slope gap; finite negative curvature on the smooth covering-space family and global concavity give incompatible Legendre quadratic coefficients. The contact geometry, strong flow, obstacle identity and duality are prior. Witt Nyström's joint-work Oberwolfach2021 contribution with Ross already announces and sketches an interior construction and is prominently credited. This is a modest proof/application note, not a first-discovery claim or certification of a currently open problem's novel resolution. A bounded18-entry source/list and64-query audit found no complete exact predecessor within its inspected scope; historical priority and independent discovery remain unresolved. The deposit contains a five-page note, LaTeX source, exact standard-library scalar certificates, analytic dependency audits and a source/priority record. Computation checks scalar algebra only. AI tools were used extensively. The preprint is unrefereed and has not undergone conventional human peer review.",'creators':[{'name':'Kriebel, Alec','affiliation':'Independent researcher','orcid':'0009-0001-9320-500X'}],'access_right':'open','license':'cc-by-4.0','publication_date':'2026-10-15','language':'eng','keywords':['homogeneous complex Monge-Ampere equation','Hele-Shaw flow','interior regularity','Green functions','Legendre duality','research note'],'related_identifiers':[{'identifier':x,'relation':'references','scheme':'doi'} for x in ['10.5802/aif.3237','10.1007/s10240-015-0074-0','10.1112/S0010437X15007526','10.2140/apde.2019.12.493','10.4171/owr/2021/25']]+[{'identifier':'https://arxiv.org/abs/1712.00405v2','relation':'references','scheme':'url'}]}
readme='''# Attributed interior contact-arc proof note

This package proves an interior second-order Taylor defect for the particular smooth strictly positive Ross–Witt Nyström contact-arc example. The five-page note states all imported construction/duality contracts and supplies the Green slope/curvature/Legendre deduction. No numerical PDE solve or closed-form potential is claimed.

The earlier OWR2021 joint-work contribution already announces/sketches an interior construction. All prior machinery is credited. Historical priority, first discovery, independent discovery and current worldwide openness are unestablished. The current note is a proof/application contribution. The supplement records18 source/list entries and64 discovery queries with explicit full/partial inspection scope, versions, hashes and gaps. Search absence is not proof of literature absence.

## Reproduce the scalar checks

Extract verification-package.zip into a fresh directory, then run Python3.11 or later from that directory:

    python3 -E -S -B -P verify_package.py

Only the Python standard library is required. The verifier checks every archive file against ARCHIVE_INVENTORY.json and replays the independent exact rational scalar certificate both normally and under optimization, plus the legacy81-case/486-assertion control normally. It writes only to stdout. Explicit exceptions protect the wrapper and new scalar checker under optimization. The legacy checker uses assertions, so it is deliberately launched without -O; its printed count alone under -O is not evidence of executed checks.

Computation verifies scalar normal-form algebra/support signs, not the Hele-Shaw geometry, elliptic dependence or weak PDE. Read the analytic proof and dependency reports for those inputs. Independent AI checks do not constitute human peer review.

## Contents and provenance

The archive includes the paper, source, authored source/geometry/Legendre/priority audits, Root mathematical and qualified-priority gates, original19 submitted artifacts and their custody record, scalar scripts/certificates, metadata and inventory. Historical original artifacts are immutable records: their imported open-status language is corrected by the current note, CLAIM_SCOPE.json and priority gate. Original effort remains4 recovered substantive author turns plus unknown/nonzero interrupted history; audits are separate work.

Copyrighted third-party PDFs, extracted texts, screenshots, raw web outputs, credentials, caches and upload state are excluded. SOURCE_REFERENCES.json and audit source-access records identify the inspected copies; relative private-copy paths are historical inspection locations, not promised archive members. Whole-package publication reviews and actual later deposit/integration receipts are recorded separately in the repository, avoiding circular inclusion of reviews that bind this archive.

The top-level zenodo-deposit.json is the exact intended metadata and three-file upload manifest for the repository kit. It does not assert that uploading has occurred. All authored materials are supplied under CC BY4.0. AI tools were used extensively. This is an unrefereed preprint without conventional human peer review.
'''
license_text='''Copyright (c)2026 Alec Kriebel. Authored note, code, certificates and research records are licensed under Creative Commons Attribution4.0 International (CC BY4.0): https://creativecommons.org/licenses/by/4.0/ . Third-party works are cited, not relicensed or included. Standard mathematical facts and bibliographic facts retain their ordinary status.
'''
verifier='''"""Authenticate extracted authored supplement and replay scalar certificates.
Python3.11+ standard library; no network and no writes.
"""
from pathlib import Path
import hashlib,json,subprocess,sys
def require(condition,message):
    if not condition:raise RuntimeError(message)
def main():
    require(sys.version_info >= (3,11),'Python3.11 or later required')
    root=Path(__file__).resolve().parent
    inventory=json.loads((root/'ARCHIVE_INVENTORY.json').read_bytes())['files']
    for name,pin in inventory.items():
        rel=Path(name);require(not rel.is_absolute() and '..' not in rel.parts,'unsafe path')
        p=root/rel;require(p.is_file() and not p.is_symlink() and p.resolve().is_relative_to(root),'missing/unsafe '+name)
        b=p.read_bytes();require(len(b)==pin['bytes'] and hashlib.sha256(b).hexdigest()==pin['sha256'],'identity '+name)
    specs=[('audits/legendre_regularity_audit_01/exact_scalar_verifier.py','audits/legendre_regularity_audit_01/EXACT_SCALAR_CERTIFICATE.json',False),('audits/legendre_regularity_audit_01/exact_scalar_verifier.py','audits/legendre_regularity_audit_01/EXACT_SCALAR_CERTIFICATE.json',True),('original_submitted_head/independent_review/scalar_duality_check.py','original_submitted_head/independent_review/scalar_duality_output.json',False)]
    runs=[]
    for script,certificate,optimize in specs:
        args=[sys.executable,'-E','-S','-B','-P']+(['-O'] if optimize else [])+[str(root/script)]
        p=subprocess.run(args,cwd=root,capture_output=True,text=True,check=True)
        require(not p.stderr,'unexpected stderr '+script)
        value=json.loads(p.stdout);require(value==json.loads((root/certificate).read_bytes()),'certificate mismatch '+script)
        runs.append({'script':script,'optimization_enabled':optimize,'certificate_exact_match':True,'result':value})
    print(json.dumps({'inventory_files_verified':len(inventory),'exact_scalar_replays':runs,'scalar_only':True,'geometric_or_PDE_computation_certified':False,'historical_priority_certified':False,'verification_writes':False},indent=2))
if __name__=='__main__':main()
'''
source_refs=json.loads((A/'priority_audit_01/SOURCE_ACCESS.json').read_bytes())
scope={'exact_theorem':mg['exact_verified_result'],'current_proof_contribution':pg['exact_current_contribution'],'all_prior_inputs_credited':True,'OWR2021_prior_interior_announcement_credited':True,'historical_priority':'UNRESOLVED','independent_discovery_certified':False,'worldwide_openness_certified':False,'coherent_normalization':'dc=i/(4pi)(barpartial-partial); ddc=i/(2pi)partialbarpartial; unit log-squared Green pole; FSarea1','source_prefactor_note':'See separate normalization addendum; apparent printed factor-two inconsistency is not an author-confirmed erratum.','earlier_historical_status_metadata':'Original source_record open/unresolved triage is preserved as historical bytes, superseded by literal-source/priority corrections here.','original_effort':'4 recovered substantive author turns plus unknown/nonzero interrupted history, not reset','AI_use':'Extensive solving, verification, literature audit, drafting and packaging','review_status':'Unrefereed; no conventional human peer review','computation_scope':'Exact scalar algebra only; analytic PDE and geometry checked by proof and source contracts.'}
put('README.md',readme.encode());put('LICENSE.txt',license_text.encode());put('verify_package.py',verifier.encode());put('SOURCE_REFERENCES.json',enc(source_refs));put('CLAIM_SCOPE.json',enc(scope))
archive={n:(D/n).read_bytes() for n in ['interior_contact_arc.tex','interior_contact_arc.pdf','README.md','LICENSE.txt','verify_package.py','SOURCE_REFERENCES.json','CLAIM_SCOPE.json']}
archive['PUBLICATION_METADATA.json']=enc(metadata)
for n in ['ROOT_MATHEMATICAL_GATE_01.json','ROOT_PRIORITY_GATE_01.json','ROOT_THREE_FAMILY_AUTHENTICATION_01.json','ORIGINAL_SUBMISSION_CUSTODY.json']:archive['research/'+n]=(A/n).read_bytes()
for folder,row in mg['three_NEW_independent_audit_families'].items():
 for n,x in row['safe_files'].items():
  b=(A/folder/n).read_bytes();require(pin(b)==x,folder+'/'+n);archive['audits/'+folder+'/'+n]=b
for n,x in mg['normalization_addendum_safe_files'].items():
 b=(A/'original_source_audit_01'/n).read_bytes();require(pin(b)==x,n);archive['audits/original_source_audit_01/'+n]=b
for n,x in pg['safe_priority_files'].items():
 b=(A/'priority_audit_01'/n).read_bytes();require(pin(b)==x,n);archive['audits/priority_audit_01/'+n]=b
cust=json.loads((A/'ORIGINAL_SUBMISSION_CUSTODY.json').read_bytes())
for n,x in cust['files'].items():
 b=(A/'original_submitted_head'/n).read_bytes();require(pin(b)=={k:x[k] for k in ['bytes','sha256']},n);archive['original_submitted_head/'+n]=b
inventory={'schema_version':1,'hash_algorithm':'SHA-256','files':{n:pin(b) for n,b in sorted(archive.items())},'self_hash_excluded':True,'scope':'All authored archive members except this inventory; third-party reading copies excluded.'}
put('ARCHIVE_INVENTORY.json',enc(inventory));archive['ARCHIVE_INVENTORY.json']=enc(inventory)
with zipfile.ZipFile(D/'verification-package.zip','x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for n,b in sorted(archive.items()):
  require(not Path(n).is_absolute() and '..' not in Path(n).parts,n);i=zipfile.ZipInfo(n,date_time=(2026,10,15,0,0,0));i.compress_type=zipfile.ZIP_DEFLATED;i.external_attr=0o100444<<16;z.writestr(i,b)
with zipfile.ZipFile(D/'verification-package.zip') as z:
 require(set(z.namelist())==set(archive) and len(z.namelist())==len(archive),'zip paths')
 for n,b in archive.items():require(z.read(n)==b,'zip bytes '+n)
 replay=W/'private_replay';replay.mkdir();z.extractall(replay)
p=subprocess.run([sys.executable,'-E','-S','-B','-P',str(replay/'verify_package.py')],capture_output=True,text=True,check=True);require(not p.stderr,'replay stderr');result=json.loads(p.stdout);put('verification_stdout.json',p.stdout.encode())
manifest={'metadata':metadata,'files':[{'path':n} for n in ['interior_contact_arc.pdf','interior_contact_arc.tex','verification-package.zip']]};put('zenodo-deposit.json',enc(manifest))
put('RESEARCH_LOG.md',('# Package preparation log\n\n'+stamp+' — Attributed proof-note package75% of PR196 workflow prepared locally. Five-page manuscript compiles with built-in compiler and cached TeX engine. Root visually inspected all5 rendered pages without layout defects. Authored-only archive identities and3 exact scalar replays verified. Mathematical and qualified-priority gates passed; historical firstness unresolved. Whole-package review loop, publication, tracking and integration remain. Original effort unknown/nonzero history plus4 recovered author turns retained.\n').encode())
safe=sorted(p.name for p in D.iterdir() if p.is_file())+['SAFE_ALLOWLIST.json','PACKAGE_SEAL.json']
put('SAFE_ALLOWLIST.json',enc({'safe_authored_files':sorted(safe),'excluded':'No glob copies; PDF reading copies, renders, private replay, caches, raw outputs and credentials stay excluded.'}))
seal={'UTC':stamp,'PR':196,'package':'publication_package_v1','safe_files':{n:pin((D/n).read_bytes()) for n in sorted(safe) if n!='PACKAGE_SEAL.json'},'self_hash_excluded':True,'archive_entries':len(archive),'archive_inventory_files':len(inventory['files']),'actual_upload_files':{n:pin((D/n).read_bytes()) for n in ['interior_contact_arc.pdf','interior_contact_arc.tex','verification-package.zip']},'original_head':'a229ac722a3b1733bcb590a5f796b4a52f68cc73','qualified_priority_scope_only':True,'historical_priority_established':False,'whole_publication_reviews_complete':False,'publication_ready':False}
put('PACKAGE_SEAL.json',enc(seal))
for n in safe:(D/n).chmod(0o444)
print(json.dumps({'package_safe_files':len(safe),'archive_entries':len(archive),'seal':pin((D/'PACKAGE_SEAL.json').read_bytes()),'upload_files':seal['actual_upload_files'],'replay_inventory_files':result['inventory_files_verified'],'scalar_replays':len(result['exact_scalar_replays'])}))
