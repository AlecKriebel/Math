#!/usr/bin/env python3
"""Seal this private review tree; writes only beside this script."""
import pathlib,json,hashlib,datetime,subprocess,sys
W=pathlib.Path(__file__).resolve().parent
EXCLUDED=['FINAL_SEAL.json','PRIVATE_MANIFEST_SEAL.json','PUBLIC_MANIFEST.json','inputs/COMPLETE_MANIFEST.json']
PRIVATE={'inputs','downloads_private'}
def pin(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def dump(path,x):(W/path).write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
subprocess.run([sys.executable,str(W/'verify_review.py'),'--unsealed'],check=True)
log=W/'RESEARCH_LOG.md'
with log.open('a') as f:f.write('\n- '+datetime.datetime.now(datetime.timezone.utc).isoformat()+' — 100%: bounded PR883–905 review complete; no substantive blocker. Final report and sanitized/private manifest boundaries established. This final log is sealed; delivery requires the subsequent read-only final-seal verifier to pass. No global novelty/completeness or blind-rediscovery certification is made.\n')
paths=sorted(p for p in W.rglob('*') if p.is_file())
if any(p.is_symlink() for p in paths):raise SystemExit('Symlink in review tree')
files=[{'path':str(p.relative_to(W)),**pin(p)} for p in paths if str(p.relative_to(W)) not in EXCLUDED]
now=datetime.datetime.now(datetime.timezone.utc).isoformat();dump('inputs/COMPLETE_MANIFEST.json',{'schema':'bounded-review-complete-manifest-v1','at':now,'scope':'all23 cases and all public/private evidence payloads in this review folder','files':files,'excluded_seal_metadata':EXCLUDED,'exclusion_reason':'Nonrecursive seal metadata; complete manifest excludes itself and the three documents which pin it. All other file payloads included.'})
c=pin(W/'inputs/COMPLETE_MANIFEST.json');dump('PRIVATE_MANIFEST_SEAL.json',{'schema':'detached-complete-manifest-seal-v1','at':now,'manifest_path':'inputs/COMPLETE_MANIFEST.json',**c,'payload_file_count':len(files),'private_raw_body_roots':sorted(PRIVATE),'private_payload_file_count':sum(x['path'].split('/')[0] in PRIVATE for x in files),'scope':'Detached SHA256/size integrity binding, not an external timestamp/signature or publication action.'})
public_paths=sorted(p for p in W.rglob('*') if p.is_file() and p.relative_to(W).parts[0] not in PRIVATE and p.name not in {'PUBLIC_MANIFEST.json','FINAL_SEAL.json'})
public=[{'path':str(p.relative_to(W)),**pin(p)} for p in public_paths]
dump('PUBLIC_MANIFEST.json',{'schema':'explicit-sanitized-public-projection-v1','at':now,'files':public,'public_file_allowlist':[x['path'] for x in public]+['PUBLIC_MANIFEST.json','FINAL_SEAL.json'],'excluded_private_roots':sorted(PRIVATE),'excluded_content':'Raw ledger/inventory/global-state bodies, full source texts/PDFs/HTML, public-provider raw record/DOI bodies, downloads and page renders remain private. Public artifacts contain checkers, public mathematical scope summaries and integrity receipts only.','self_exclusions':['PUBLIC_MANIFEST.json','FINAL_SEAL.json'],'final_seal_rule':'FINAL_SEAL.json pins this manifest and the detached private seal; each manifest excludes its own recursive pin metadata.'})
dump('FINAL_SEAL.json',{'schema':'bounded-adversarial-review-final-seal-v1','at':now,'decision':'bounded_pass','fixed_pr_interval':[883,905],'completion_estimate_percent':100,'pins':{x:pin(W/x) for x in ['PUBLIC_MANIFEST.json','PRIVATE_MANIFEST_SEAL.json','inputs/COMPLETE_MANIFEST.json','REPORT.md','RESEARCH_LOG.md','SUMMARY.json']},'self_excluded':True,'claim_boundary':'No substantive blocker in23 pinned disposition/publication-coverage cases; no new proof/priority audit, global novelty/completeness or blind rediscovery certification.'})
subprocess.run([sys.executable,str(W/'verify_review.py')],check=True)
print(json.dumps({'public_files':len(public)+2,'all_manifested_payload_files':len(files),'complete_manifest':c,'final_seal':pin(W/'FINAL_SEAL.json'),'report':pin(W/'REPORT.md')},indent=2))
