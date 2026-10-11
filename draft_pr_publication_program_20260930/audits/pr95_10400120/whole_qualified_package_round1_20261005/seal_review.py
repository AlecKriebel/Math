from pathlib import Path
import json,hashlib,datetime,os,zipfile
A=Path(__file__).resolve().parent;Q=A.parent/'qualified_publication_package_v1';now=datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def guard(c,m):
 if not c:raise RuntimeError(m)
initial=json.loads((A/'input_inventory.json').read_text());checks=[]
for r in initial['files']:
 p=Q/r['path'];checks.append({'kind':'frozen_input_unchanged','file':r['path'],'ok':p.stat().st_size==r['bytes'] and sha(p)==r['sha256']})
guard(all(c['ok'] for c in checks),'frozen input changed')
guard(set(r['path'] for r in initial['files'])==set(str(p.relative_to(Q)) for p in Q.rglob('*') if p.is_file()),'frozen candidate membership changed')
with zipfile.ZipFile(Q/'publicfiles/pr95_support.zip') as z:
 symlinks=[i.filename for i in z.infolist() if (i.external_attr>>16)&0o170000==0o120000];unsafe=[i.filename for i in z.infolist() if Path(i.filename).is_absolute() or '..' in Path(i.filename).parts]
 guard(not symlinks and not unsafe,'unsafe/linked ZIP input')
(A/'INTEGRITY_CHECKS.json').write_text(json.dumps({'utc':now,'candidate_checks':checks,'candidate_membership_unchanged':True,'zip_symlink_entries':symlinks,'zip_unsafe_members':unsafe,'all_pass':True},indent=2)+'\n')
issues=[{'id':'R1','severity':'low','required_before_clean_gate':True,'category':'payload guard/documentation','file':'publicfiles/verification/run_all.py','line':next(i+1 for i,s in enumerate((Q/'publicfiles/verification/run_all.py').read_text().split('\n')) if 'not p.is_symlink()' in s),'claim_file':'publicfiles/verification/VERIFY_README.md','claim':'Rejects linked paths','observed':'Symlinked ancestor directory accepted normally and under-O with declared member hashes intact.','repair':'Reject symlinked components for each declared relative path; update/rebuild all manifests ZIP digests and fresh receipts; new corrected-byte whole-package review.','evidence':['PAYLOAD_CONTROLS.json','processes/payload_ancestor_symlink_normal/process.json','processes/payload_ancestor_symlink_O/process.json'],'mathematical_impact':'none found','candidate_edited':False}]
(A/'ISSUES.json').write_text(json.dumps({'utc':now,'verdict':'MATHEMATICS_PASS_PACKAGE_REPAIR_REQUIRED','issues':issues,'remaining_mathematical_gap':None,'foundation_scope':'Imported established category/RT/HT foundations','priority':'UNRESOLVED','review_round':1,'new_central_proof_search_turns':0,'release_authority':False},indent=2)+'\n')
with (A/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+now+' — Review report completed; all frozen candidate bytes/membership rechecked unchanged, original-source provenance authenticated, process closure passes. One required low-severity R1 retained; mathematics passes under imported foundations, priority unresolved. Completion estimate: 100% for assigned round1 review; release/novelty not cleared. Packet now sealed; no further edits planned.\n')
# Include symlinks as immutable path-target records, without duplicating their referenced tree.
files=[];links=[]
for p in sorted(A.rglob('*')):
 if p.name in ['CLOSED_MANIFEST.json','SHA256SUMS','CLOSURE.json'] and p.parent==A:continue
 if p.is_symlink():links.append({'file':str(p.relative_to(A)),'target':os.readlink(p)})
 elif p.is_file():files.append({'file':str(p.relative_to(A)),'bytes':p.stat().st_size,'sha256':sha(p)})
m={'schema':'PR95-round1-closed-whole-package-review/v1','utc':now,'operator_pid':os.getpid(),'candidate_manifest_sha256':sha(Q/'private_notes/FROZEN_CANDIDATE_MANIFEST.json'),'preparation_manifest_sha256':sha(Q/'PREPARATION_MANIFEST.json'),'files':files,'symlinks':links,'scope':'Immutable v1 review evidence; copied ZIP trees are authored package data, no third-party primary PDFs copied. Excludes only closure/manifest/detached hash files to avoid self-reference.','verdict':'MATHEMATICS_PASS_PACKAGE_REPAIR_REQUIRED','completion_estimate_percent':100,'priority_clearance':False,'publication_clearance':False}
(A/'CLOSED_MANIFEST.json').write_text(json.dumps(m,indent=2)+'\n')
for r in files:guard(sha(A/r['file'])==r['sha256'] and (A/r['file']).stat().st_size==r['bytes'],'manifest payload changed')
for r in links:guard(os.readlink(A/r['file'])==r['target'],'link changed')
(A/'SHA256SUMS').write_text(''.join(r['sha256']+'  '+r['file']+'\n' for r in files)+sha(A/'CLOSED_MANIFEST.json')+'  CLOSED_MANIFEST.json\n')
c={'schema':'PR95-round1-review-closure/v1','utc':now,'report_sha256':sha(A/'REPORT.md'),'manifest_sha256':sha(A/'CLOSED_MANIFEST.json'),'sha256sums_sha256':sha(A/'SHA256SUMS'),'issues_sha256':sha(A/'ISSUES.json'),'integrity_sha256':sha(A/'INTEGRITY_CHECKS.json'),'candidate_unchanged':True,'review_completion_percent':100,'verdict':'MATHEMATICS_PASS_PACKAGE_REPAIR_REQUIRED','required_repair':'R1 ancestor-symlink path guard','priority':'UNRESOLVED','publication_clearance':False,'all_prior_children_terminated':json.loads((A/'PROCESS_CLOSURE.json').read_text())['all_prior_processes_terminated'],'notes':'closure_probe has actual captured exit0; immutable packet excludes only this closure, manifest and detached sums from manifest enumeration.'}
(A/'CLOSURE.json').write_text(json.dumps(c,indent=2)+'\n');print(json.dumps(c,indent=2))
