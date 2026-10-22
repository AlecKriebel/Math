#!/usr/bin/env python3
"""Read local PR952 inputs and emit integration JSON; never write files or use services.
The root must independently authenticate/review the printed hashes before use.
"""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):raise SystemExit('Use Python -I -S -B')
import argparse,hashlib,json,re,stat
from pathlib import Path
from datetime import datetime,timezone
OWN=Path(__file__).resolve().parent;P=OWN.parents[2];ROOT=P.parent;A=P/'audits/pr952_10400145';D=A/'preprint'
HEAD='989a532ae1d50894190d010a0a02ba8c3d71ee05';KIT='zenodo_deposit_tool/zenodo.py';KIT_SHA='a91f961bcabadb15f92bb738c3194f0277cd47f1f87167ac8db8eb7c4fd3b9ca'
HELPERS=['accept_pr952.py','merge_pr952.py','run_pr952_zenodo.py','append_pr952_tracker.py','update_pr952_publication_ledger.py','finalize_pr952_and_gate_next.py']
PDF='habiro-rank-interpolation-v1.0.pdf';ZIP='habiro-rank-interpolation-verification-v1.0.zip'
FAMILIES={'algebra_falsifier_01':'ROOT_ALGEBRA01_AUTHENTICATION.json','quantum_bridge_01':'ROOT_QUANTUM_BRIDGE01_AUTHENTICATION.json','computation_01':'ROOT_COMPUTATION01_AUTHENTICATION.json','classical_priority_01':'ROOT_CLASSICAL_PRIORITY01_AUTHENTICATION.json','recent_priority_01':'ROOT_RECENT_PRIORITY01_AUTHENTICATION.json'}
def need(ok,m):
 if not ok:raise RuntimeError(m)
def raw(path):
 path=Path(path);relative=path.relative_to(ROOT)
 for ancestor in [ROOT,*[ROOT.joinpath(*relative.parts[:i]) for i in range(1,len(relative.parts)+1)]]:need(not ancestor.is_symlink(),'no symlink input: '+str(ancestor))
 need(path.is_file() and stat.S_ISREG(path.stat().st_mode),'regular input required: '+str(path));return path.read_bytes()
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(path):
 b=raw(path);return {'bytes':len(b),'sha256':sha(b)}
def encode(x):return (json.dumps(x,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()
parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--operations-only',action='store_true');args=parser.parse_args()
# Preserve exact serialized bytes printed as *_json fields; hashes refer to these.
inv={'schema':'pr952-operations-v1','pr':952,'problem_id':'10400145','original_pr_head':HEAD,'files':{(P/name).relative_to(ROOT).as_posix():pin(P/name) for name in HELPERS}}
inv['files'][KIT]=pin(ROOT/KIT);need(inv['files'][KIT]['sha256']==KIT_SHA,'standard Zenodo kit changed')
if args.operations_only:
 sys.stdout.buffer.write(encode(inv));raise SystemExit(0)
manifest=raw(D/'package/PACKAGE_MANIFEST.json');doc=json.loads(manifest);need(doc['schema']=='pr952-sourcefree-package-v1' and doc['problem_id']==10400145 and doc['original_head']==HEAD,'package identity')
files={name:pin(D/name) for name in [PDF,ZIP,'zenodo-deposit.json','FINDING_DISPOSITIONS.json','PR_DESCRIPTION.md','BUILD_RECEIPT.json',*['PACKAGE_REPLAY_'+x+'.json' for x in ['normal','O','OO','env2']]]}
extra_payloads=['README.md','AUDIT_LIMITS.md','AUTHORSHIP_PROVENANCE.md','SOURCE_MAP.md','SUPPLEMENT.md','VERIFICATION.md','note.tex','build_package.py','ZENODO_LOCAL_CHECK.json','ROOT_ACTUAL_COLD_REPLAY.json','COLD_RECEIPT_ENVELOPE_ASSEMBLY.json','authoring/main.tex','output/pdf/main.pdf','output/pdf/main.log']
extra_payloads += ['PACKAGE_REPLAY_'+mode+'.'+suffix for mode in ['normal','O','OO','env2'] for suffix in ['DRIVER_RECEIPT.json','stdout.json','stderr.txt','launch.json']]
for name in extra_payloads:files[name]=pin(D/name)
files['package/PACKAGE_MANIFEST.json']={'bytes':len(manifest),'sha256':sha(manifest)}
for name,item in doc['files'].items():
 need(set(item)=={'bytes','sha256','mode'} and item['mode']=='100644','package mode schema')
 actual=pin(D/'package'/name);need(actual=={k:item[k] for k in ('bytes','sha256')},'package bytes changed: '+name);files['package/'+name]=actual
need(files['package/verify_package.py']['sha256']=='ba18bdcd863c3dca65c86be711564527ce19e4c859204b66095e39d366f453d7','engineered verifier pin')
evidence_names=['ORIGINAL_FILE_RECORDS.json','ELIGIBILITY_GATE.json','TARGET_IDENTITY_PREFLIGHT.json','ORIGINAL_SNAPSHOT.json','NATIVE_ACCOUNTING_BASELINE.json','source_record_private.txt','INHERITED_FINDING_DISPOSITIONS.json','ROOT_PRIORITY_INTAKE.json','ROOT_OPERATIONAL_FINDINGS.json','ROOT_CANDIDATE01_ARCHIVE_BEFORE_SOURCE_REPAIR.json','ROOT_IMMUTABLE_OBJECT_PREFETCH_OBSERVATION.json','FULL_REVIEW_PROTOCOL.md','ROOT_PRIMARY_SELECTED_READINGS.json','ROOT_PORTABLE_REPLAY.json','ROOT_LINUX_AVAILABILITY_PROBE.json','ROOT_LINUX_AVAILABILITY_PROBE_INITIAL.json','ROOT_PACKAGE_ENGINEERING01_AUTHENTICATION.json','ROOT_PACKAGE_ENGINEERING01_INTAKE.json','package_engineering_01/MANIFEST.json','ROOT_OPERATIONS_ENGINEERING01_AUTHENTICATION.json','ROOT_OPERATIONS_ENGINEERING01_INTAKE.json','operations_engineering_01/MANIFEST.json','ROOT_PAPER_DRAFT01_QA.json','PR_DESCRIPTION_ANCHOR.md','ROOT_OPERATIONS_ENGINEERING02_AUTHENTICATION.json','ROOT_OPERATIONS_ENGINEERING02_INTAKE.json','operations_engineering_02/MANIFEST.json','ROOT_FULL01_AUTHENTICATION.json','ROOT_FULL01_INTAKE.json','ROOT_FULL01_EARLY_EXPOSURE_DISPOSITION.json','ROOT_FULL01_EDITORIAL_FIX.json','ROOT_FULL01_NATIVE_RECOVERY_FINDING_ACK.json','ROOT_CANDIDATE02_ARCHIVE_BEFORE_FULL01_FIXES.json','operations_engineering_03/MANIFEST.json','ROOT_OPERATIONS_ENGINEERING03_AUTHENTICATION.json','ROOT_OPERATIONS_ENGINEERING03_INTAKE.json']
evidence={(A/name).relative_to(ROOT).as_posix():pin(A/name) for name in evidence_names}
families={}
for family,auth_name in FAMILIES.items():
 mp=(A/'reviews'/family/'MANIFEST.json').relative_to(ROOT).as_posix();ap=(A/auth_name).relative_to(ROOT).as_posix();evidence[mp]=pin(ROOT/mp);evidence[ap]=pin(ROOT/ap)
 auth=json.loads(raw(ROOT/ap));need(auth['status']=='PASS_BYTES_BEFORE_FULL_REPORT_INTAKE' and auth['manifest_sha256']==evidence[mp]['sha256'],'root family authentication mismatch')
 families[family]={'manifest_path':mp,'manifest_sha256':evidence[mp]['sha256'],'root_authentication_path':ap,'root_authentication_sha256':evidence[ap]['sha256']}
# Prior adverse whole review is immutable history, never clean credit.
review_base=A/'reviews/full_package_01';review_manifest=raw(review_base/'MANIFEST.json');review_sha=sha(review_manifest)
need(review_sha=='c17f8f4c8812685a2b4a6442695ad99d84359750ab8a13467a21d71d8244e9d9','externally root-authenticated full01 seal changed')
root_auth=json.loads(raw(A/'ROOT_FULL01_AUTHENTICATION.json'));need(root_auth['manifest_sha256']==review_sha and root_auth['status']=='PASS_BYTES_BEFORE_FULL_REPORT_INTAKE','actual root full01 authentication')
review_doc=json.loads(review_manifest);records=review_doc['files'];allowed=review_doc['explicit_public_allowlist']
need(type(records) is dict and type(allowed) is list and len(allowed)==len(set(allowed)) and set(allowed)==set(records),'whole01 exact explicit public closure')
evidence[(review_base/'MANIFEST.json').relative_to(ROOT).as_posix()]=pin(review_base/'MANIFEST.json')
for name,record in records.items():
 need(type(name) is str and re.fullmatch(r'[A-Za-z0-9_./-]+',name) and not name.startswith('/') and all(x not in ('','.','..') for x in name.split('/')),'whole01 safe path')
 need(type(record) is dict and set(record)=={'bytes','sha256'},'actual whole01 fingerprint schema')
 got=pin(review_base/name);need(got==record,'whole01 public payload changed: '+name);evidence[(review_base/name).relative_to(ROOT).as_posix()]=got
prior_result=json.loads(raw(review_base/'RESULT.json'));need(prior_result['clean_for_preprint'] is False and prior_result['candidate_revision']==2,'full01 remains adverse candidate02 history')
prior_review_ids=[item['id'] for item in prior_result['required_issues']+prior_result['optional_issues']]
dispositions=json.loads(raw(D/'FINDING_DISPOSITIONS.json'));ids=[x['id'] for x in dispositions['findings']];need(len(ids)==28 and len(set(ids))==28,'exact current28 IDs')
for mode,opt in [('normal',0),('O',1),('OO',2),('env2',0)]:
 receipt=json.loads(raw(D/('PACKAGE_REPLAY_'+mode+'.json')))
 need(type(receipt.get('receipt')) is dict and receipt.get('returncode')==0 and type(receipt.get('returncode')) is int,'actual canonical replay envelope required')
 need(receipt['receipt']['manifest_sha256']==sha(manifest) and receipt['receipt']['outer_runtime']['optimize']==opt,'cold mode package/optimization mismatch')
freeze={'schema':'pr952-publication-freeze-v1','created_utc':datetime.now(timezone.utc).isoformat(),'revision_candidate':3,'pr':952,'problem_id':'10400145','original_pr_head':HEAD,'operations_inventory_sha256':sha(encode(inv)),'pr_description_sha256':sha(raw(A/'PR_DESCRIPTION_ANCHOR.md')),'package_manifest_sha256':sha(manifest),'package_pdf':'paper/'+PDF,'package_verifier':'verify_package.py','files':files,'evidence_files':evidence,'future_helpers':{name:inv['files'][(P/name).relative_to(ROOT).as_posix()] for name in HELPERS},'replay_normalization_ignored':[],'family_authentication':families,'inherited_finding_ids':ids}
# PDF path must match actual closed tree; fail rather than guess.
need('package/'+freeze['package_pdf'] in files and files['package/'+freeze['package_pdf']]==files[PDF],'upload PDF != closed paper PDF')
settings={'schema':'pr952-operations-root-handoff-v1','operations_inventory_sha256':sha(encode(inv)),'freeze_sha256':sha(encode(freeze)),'package_manifest_sha256':sha(manifest),'entry_verifier_sha256':files['package/verify_package.py']['sha256'],'original_pr_head':HEAD,'problem_id':'10400145','pr':952,'candidate_revision':3,'review_manifest_specs':['01:'+review_sha],'prior_review_issue_ids':prior_review_ids,'required_root_operational_findings':['R952-OPS-ROOT-01'],'acceptance_authority':False,'mutations_performed':False,'instructions':'Externally authenticate these printed hashes. Write exact *_json strings only after root validation. Preserve adverse full_package_01; fresh sequential complete current-candidate reviews remain required. Full01 issues accumulate through the unchanged review-chain logic.'}
print(json.dumps({'operations_inventory_json':encode(inv).decode(),'freeze_json':encode(freeze).decode(),'settings':settings},indent=2,ensure_ascii=False))
