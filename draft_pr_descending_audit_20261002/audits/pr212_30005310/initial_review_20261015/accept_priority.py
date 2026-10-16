from pathlib import Path
import hashlib,json,subprocess,shutil,datetime
D=Path(__file__).resolve().parent;P=D.parents[2];rows=[]
assert json.loads((D/'ROOT_COMPLETE_MATHEMATICAL_ACCEPTANCE.json').read_text())['status']=='PASS_THREE_INDEPENDENT_MATHEMATICAL_SOURCE_FAMILIES'
for family,code,out in [('priority_classical_01','check_certificates.py','certificates.json'),('priority_author_update_01','CONTROL.py','CONTROL_RESULTS.json')]:
 F=D/family;m=json.loads((F/'MANIFEST.json').read_text())
 for row in m['files']:
  q=F/row.get('path',row.get('relative_path'));raw=q.read_bytes();assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
 if family=='priority_classical_01':
  for line in (F/'SEAL.sha256').read_text().splitlines():
   h,name=line.split('  ',1);assert hashlib.sha256((F/name).read_bytes()).hexdigest()==h
 else:
  seal=json.loads((F/'FINAL_SEAL.json').read_text());assert hashlib.sha256((F/'MANIFEST.json').read_bytes()).hexdigest()==seal['manifest_sha256']
 dst=D/'root_priority_replays'/family;dst.mkdir(parents=True,exist_ok=True);shutil.copyfile(F/code,dst/code)
 r=subprocess.run(['/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3',str(dst/code)],capture_output=True,text=True,timeout=60);assert r.returncode==0,r.stderr
 (dst/'stdout.json').write_text(r.stdout);(dst/'stderr.txt').write_text(r.stderr);assert json.loads(r.stdout)==json.loads((F/out).read_text())
 rows.append(dict(family=family,report_sha256=hashlib.sha256((F/'REPORT.md').read_bytes()).hexdigest(),manifest_sha256=hashlib.sha256((F/'MANIFEST.json').read_bytes()).hexdigest(),all_safe_payloads_and_seal_verified=True,root_read_complete_report_and_primary_reconstruction=True,isolated_exact_certificate_replay_matches=True))
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
result=dict(utc=now,status='PASS_EXACT_PRIOR_COVERAGE',mathematics='PASS',recommendation='already_solved credit correction for full literal numerical question only',prior_routes=['Same singletonK44 counterexample: GS2015+BS2017','Different genuinely coloredC4 counterexample: HKS2026 Prop3.26 and exact ideal bridge'],bare_mechanism_alternative_resolved=False,earlier_exact_tied_variant_publication_certified=False,first_explicit_error_recognition_certified=False,new_preprint_cleared=False,native_repair_cleared=False,final_packet_adversary_required=True,root_priority_audit_sha256=hashlib.sha256((D/'ROOT_PRIORITY_AUDIT.md').read_bytes()).hexdigest(),reviewer_families=rows)
(D/'ROOT_PRIORITY_ACCEPTANCE.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
