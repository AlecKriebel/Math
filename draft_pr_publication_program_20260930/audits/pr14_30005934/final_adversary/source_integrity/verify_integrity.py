#!/usr/bin/env python3
"""Read-only Git and manifest checks; writes only this audit's JSON receipt."""
import hashlib,json,subprocess,sys
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[5]
AUDIT=ROOT/'draft_pr_publication_program_20260930/audits/pr14_30005934'
OUT=Path(__file__).resolve().parent
HEAD='a81fa89f6613791dd55ad5b79bfe8053bd1585f3'
PREFIX='unsolved_math_prioritization/attempts/30005934/'
def digest(b): return hashlib.sha256(b).hexdigest()
def git(*args): return subprocess.check_output(['git','-C',str(ROOT),*args])
manifest=json.loads((AUDIT/'snapshot_manifest.json').read_text())
original=[]
for f in manifest['files']:
 p=f['path']; b=git('show',f'{HEAD}:{PREFIX}{p}'); snap=(AUDIT/'source_snapshot'/p).read_bytes()
 listing=git('ls-tree',HEAD,'--',PREFIX+p).decode().strip().split()
 actual_blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
 original.append({'path':p,'sha256_git':digest(b),'sha256_snapshot':digest(snap),'size_git':len(b),'git_blob_computed':actual_blob,'mode_git':listing[0],
 'pass':b==snap and digest(b)==f['sha256'] and len(b)==f['size'] and actual_blob==f['git_blob'] and listing[0]==f['mode']})
original_git_paths={p[len(PREFIX):] for p in git('ls-tree','-r','--name-only',HEAD,'--',PREFIX).decode().splitlines()}
manifest_original_paths={f['path'] for f in manifest['files']}
snapshot_paths={str(p.relative_to(AUDIT/'source_snapshot')) for p in (AUDIT/'source_snapshot').rglob('*') if p.is_file()}
source_path_sets_match=original_git_paths==manifest_original_paths==snapshot_paths
actual_changed_paths=git('diff','--name-only',manifest['base'],HEAD).decode().splitlines()
original_diff_paths_match=actual_changed_paths==manifest['changed_paths']
candidate_path=AUDIT/'reviewed_candidate/MANIFEST.json'; current=json.loads(candidate_path.read_text())
candidate=[]
for p,h in current['sha256'].items():
 actual=digest((candidate_path.parent/p).read_bytes()); candidate.append({'path':p,'advertised':h,'actual':actual,'pass':actual==h})
candidate_unlisted=sorted(str(p.relative_to(candidate_path.parent)) for p in candidate_path.parent.rglob('*') if p.is_file() and p!=candidate_path and str(p.relative_to(candidate_path.parent)) not in current['sha256'])
family_path=AUDIT/'FAMILY_MANIFEST.json'; fam=json.loads(family_path.read_text()); families=[]
for family,entries in fam['sha256'].items():
 for p,h in entries.items():
  actual=digest((AUDIT/family/p).read_bytes()); families.append({'family':family,'path':p,'advertised':h,'actual':actual,'pass':actual==h})
family_unlisted={family:sorted(str(p.relative_to(AUDIT/family)) for p in (AUDIT/family).rglob('*') if p.is_file() and 'tmp' not in p.relative_to(AUDIT/family).parts and str(p.relative_to(AUDIT/family)) not in entries) for family,entries in fam['sha256'].items()}
receipt={'timestamp_utc':datetime.now(timezone.utc).isoformat(),'auditor':'fresh source-integrity challenge','review_target':HEAD,
 'local_main_at_check':git('rev-parse','HEAD').decode().strip(),'branch':git('branch','--show-current').decode().strip(),
 'snapshot_manifest_sha256':digest((AUDIT/'snapshot_manifest.json').read_bytes()),'reviewed_candidate_manifest_sha256':digest(candidate_path.read_bytes()),'family_manifest_sha256':digest(family_path.read_bytes()),
 'source_path_sets_match':source_path_sets_match,'original_git_paths':sorted(original_git_paths),'snapshot_paths':sorted(snapshot_paths),'snapshot_manifest_head_matches':manifest['head']==HEAD,'original_diff_paths_match':original_diff_paths_match,
 'original12':original,'current16':candidate,'family24':families,'candidate_unlisted':candidate_unlisted,'family_unlisted_excluding_tmp':family_unlisted,
 'pass':all(x['pass'] for x in original+candidate+families) and not candidate_unlisted and not any(family_unlisted.values()) and source_path_sets_match and original_diff_paths_match and manifest['head']==HEAD}
(OUT/'integrity_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:receipt[k] for k in ['timestamp_utc','branch','review_target','local_main_at_check','snapshot_manifest_sha256','reviewed_candidate_manifest_sha256','family_manifest_sha256','candidate_unlisted','family_unlisted_excluding_tmp','pass']},indent=2))
print('counts',len(original),len(candidate),len(families))
sys.exit(0 if receipt['pass'] else 1)
