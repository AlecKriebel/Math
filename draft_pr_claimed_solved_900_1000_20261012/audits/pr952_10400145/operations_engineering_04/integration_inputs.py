#!/usr/bin/env python3
"""Print root integration inputs without writes/services. Full output requires installation.
Operations-only proposal preview is explicitly uninstalled and has no freeze authority.
"""
import sys
if not(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):raise SystemExit('Use -I -S -B')
import argparse,hashlib,json,stat
from pathlib import Path
from datetime import datetime,timezone
OWN=Path(__file__).resolve().parent;P=OWN.parents[2];ROOT=P.parent;A=P/'audits/pr952_10400145';D=A/'preprint'
BASE='888a068e26e0adcc3f493817ef46c46b6bdd5a4f848a4d907e4f4af2b5f592a8';OLD_FREEZE='87e6753c48153e6bbc82ad77181339dd4d4fe64e0c855be507da6b47b7438424'
HISTORY='f1e27cc4e126a787de3c98f409a96b0fa15d033a1f78434bb5f216203f4bb234'
HELPERS=['accept_pr952.py','merge_pr952.py','run_pr952_zenodo.py','append_pr952_tracker.py','update_pr952_publication_ledger.py','finalize_pr952_and_gate_next.py'];KIT='zenodo_deposit_tool/zenodo.py';KIT_SHA='a91f961bcabadb15f92bb738c3194f0277cd47f1f87167ac8db8eb7c4fd3b9ca'
REVIEWS=[('01','c17f8f4c8812685a2b4a6442695ad99d84359750ab8a13467a21d71d8244e9d9',2),('02','a131470b039f4e75b967d476a705c144258dbc29d8393da1f50eff10b01aef8a',3)]
def need(ok,m):
 if not ok:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def raw(path):
 path=Path(path);parts=path.relative_to(ROOT).parts;need(all(x not in ('','.','..') for x in parts),'safe relative path')
 for i in range(len(parts)+1):need(not ROOT.joinpath(*parts[:i]).is_symlink(),'no linked input')
 need(path.is_file() and stat.S_ISREG(path.stat().st_mode),'regular input required');return path.read_bytes()
def pin(path):
 b=raw(path);return {'bytes':len(b),'sha256':sha(b)}
def encode(x):return (json.dumps(x,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()
def add(evidence,path,expected=None):
 item=pin(path)
 if expected is not None:need(item['sha256']==expected,'external input pin '+str(path))
 evidence[Path(path).relative_to(ROOT).as_posix()]=item;return raw(path)
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--proposal-sha256',required=True);p.add_argument('--operations-only',action='store_true');p.add_argument('--proposal-preview',action='store_true');p.add_argument('--own-readiness-sha256');p.add_argument('--extra-evidence',nargs=2,action='append',default=[],metavar=('REPOSITORY_PATH','SHA256'));a=p.parse_args()
proposed=raw(OWN/'PROPOSED_accept_pr952.py');need(sha(proposed)==a.proposal_sha256,'external proposal pin')
actual=raw(P/'accept_pr952.py')
if a.proposal_preview:need(a.operations_only and sha(actual)==BASE,'preview is operations-only with unchanged installation')
else:need(actual==proposed,'explicitly authorized installation must precede actual candidate4 integration')
inv={'schema':'pr952-operations-v1','pr':952,'problem_id':'10400145','original_pr_head':'989a532ae1d50894190d010a0a02ba8c3d71ee05','files':{(P/name).relative_to(ROOT).as_posix():pin(P/name) for name in HELPERS}}
if a.proposal_preview:inv['files'][(P/'accept_pr952.py').relative_to(ROOT).as_posix()]={'bytes':len(proposed),'sha256':sha(proposed)}
inv['files'][KIT]=pin(ROOT/KIT);need(inv['files'][KIT]['sha256']==KIT_SHA,'unchanged kit')
if a.operations_only:
 print(json.dumps({'proposal_preview_only':a.proposal_preview,'installed_actual_core':not a.proposal_preview,'operations_inventory_json':encode(inv).decode(),'operations_inventory_sha256':sha(encode(inv)),'acceptance_authority':False},indent=2));raise SystemExit(0)
need(a.own_readiness_sha256 is not None,'root-authenticated current readiness required')
old=raw(D/'reviewed_candidates/candidate03/FREEZE.json');need(sha(old)==OLD_FREEZE,'immutable archived candidate03 freeze');freeze=json.loads(old)
# Freshly read each science payload and every current manifest member. No old
# byte equality is assumed; newly added root evidence is explicit below/CLI.
files={name:pin(D/name) for name in freeze['files']}
manifest=json.loads(raw(D/'package/PACKAGE_MANIFEST.json'));need(manifest['schema']=='pr952-sourcefree-package-v1','package schema')
for name,record in manifest['files'].items():
 got=pin(D/'package'/name);need(got=={k:record[k] for k in ('bytes','sha256')},'current package member pin');files['package/'+name]=got
need({name[len('package/'):] for name in files if name.startswith('package/') and name!='package/PACKAGE_MANIFEST.json'}==set(manifest['files']),'complete current package scope')
evidence={name:pin(ROOT/name) for name in freeze['evidence_files']}
prior_specs=[];prior_issues=[]
for number,external,candidate in REVIEWS:
 base=A/('reviews/full_package_'+number);doc=json.loads(add(evidence,base/'MANIFEST.json',external));records=doc['files'];allowed=doc['explicit_public_allowlist'];need(type(records) is dict and type(allowed) is list and len(allowed)==len(set(allowed)) and set(allowed)==set(records),'complete numbered review closure')
 for name,record in records.items():need(pin(base/name)==record,'numbered review payload mismatch');add(evidence,base/name)
 auth=json.loads(add(evidence,A/('ROOT_FULL'+number+'_AUTHENTICATION.json')));need(auth['manifest_sha256']==external and auth['status']=='PASS_BYTES_BEFORE_FULL_REPORT_INTAKE','root numbered review authentication')
 result=json.loads(raw(base/'RESULT.json'));need(result['candidate_revision']==candidate and result['clean_for_preprint'] is False,'adverse whole review remains adverse')
 prior_specs.append(number+':'+external);prior_issues.extend(item['id'] for item in result['required_issues']+result['optional_issues'])
for name in ['ROOT_FULL02_INTAKE.json','ROOT_FULL02_REPORTED_FINDING_ACK.json','ROOT_CANDIDATE03_ARCHIVE_BEFORE_FULL02_FIXES.json','ROOT_OPERATIONS04_PROPOSAL_AUTHENTICATION.json','ROOT_OPERATIONS04_PROPOSAL_INTAKE_01_REQUIREMENTS.json','ROOT_OPERATIONS04_V01_SNAPSHOT_AUTHENTICATION.json','FULL_REVIEW_PROTOCOL.md','ROOT_OPERATIONAL_FINDINGS.json']:
 add(evidence,A/name)
history=json.loads(add(evidence,A/'operations04_v01_public_snapshot/MANIFEST.json',HISTORY))
for original,item in history['files'].items():need(pin(ROOT/item['path'])=={k:item[k] for k in ('bytes','sha256')},'portable exact old proposal evidence');add(evidence,ROOT/item['path'])
readiness=json.loads(add(evidence,OWN/'PROPOSAL_READINESS.json',a.own_readiness_sha256))
for name,item in readiness['files'].items():need(pin(ROOT/name)=={k:item[k] for k in ('bytes','sha256')},'new proposal readiness payload');add(evidence,ROOT/name)
for name,external in a.extra_evidence:add(evidence,ROOT/name,external)
freeze.update(created_utc=datetime.now(timezone.utc).isoformat(),revision_candidate=4,operations_inventory_sha256=sha(encode(inv)),package_manifest_sha256=sha(raw(D/'package/PACKAGE_MANIFEST.json')),files=files,evidence_files=evidence,future_helpers={name:inv['files'][(P/name).relative_to(ROOT).as_posix()] for name in HELPERS})
for mode,opt in [('normal',0),('O',1),('OO',2),('env2',0)]:
 receipt=json.loads(raw(D/('PACKAGE_REPLAY_'+mode+'.json')));need(receipt['returncode']==0 and receipt['receipt']['manifest_sha256']==freeze['package_manifest_sha256'] and receipt['receipt']['outer_runtime']['optimize']==opt,'fresh canonical cold receipt')
settings={'schema':'pr952-operations-root-handoff-v1','candidate_revision':4,'pr':952,'problem_id':'10400145','original_pr_head':inv['original_pr_head'],'operations_inventory_sha256':sha(encode(inv)),'freeze_sha256':sha(encode(freeze)),'package_manifest_sha256':freeze['package_manifest_sha256'],'entry_verifier_sha256':files['package/verify_package.py']['sha256'],'review_manifest_specs':prior_specs,'prior_review_issue_ids':prior_issues,'required_root_operational_findings':['R952-OPS-ROOT-01'],'acceptance_authority':False,'mutations_performed':False,'instructions':'Root must authenticate all printed bytes, add its final installation/intake/protocol evidence explicitly, preserve full01/full02 adverse chronology and all required/optional issues, and obtain fresh sequential full03/full04 ENTIRE current-candidate reviews. This read-only generator grants no installation or acceptance authority.'}
print(json.dumps({'operations_inventory_json':encode(inv).decode(),'freeze_json':encode(freeze).decode(),'settings':settings},indent=2,ensure_ascii=False))
