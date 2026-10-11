import datetime,hashlib,json,os,pathlib
ROOT=pathlib.Path(__file__).resolve().parent
v=json.loads((ROOT/'VERDICT.json').read_text());c=json.loads((ROOT/'SOURCE_CATALOG.json').read_text())
checks=[]
def check(name,condition):
 checks.append({'name':name,'passed':bool(condition)})
 if not condition:raise AssertionError(name)
check('no_root_adjudication_or_publication_clearance',v['publication_authorized'] is False and v['root_adjudication'] is False and v['novelty_clearance'] is False)
check('exact_prior_general_pencil_finding',v['prior_theorem']['closed_alpha_required'] is False and v['mapping']['pencil_cover_verified'] is True)
t22=json.dumps(json.loads((ROOT/'source_pages_22_web.json').read_text()),ensure_ascii=False)
t25=json.dumps(json.loads((ROOT/'source_pages_25_web.json').read_text()),ensure_ascii=False)
check('original2012_def_theorem_proof_pins_in_actual_tool_output','L524:' in t22 and 'L664:' in t22)
check('original2012_intermediate_and_final_body_read_coverage','L809:' in t25 and 'L1090:' in t25 and 'L1208:' in t25)
for rfile in ['HTTP_PROCESS_RECORDS.json','HTTP_PROCESS_RECORDS_02.json','HTTP_PROCESS_RECORDS_03.json']:
 for rec in json.loads((ROOT/rfile).read_text()):
  if 'saved_path' in rec:
   p=ROOT/rec['saved_path'];check('HTTP_body_hash_'+rec['key'],p.exists() and hashlib.sha256(p.read_bytes()).hexdigest()==rec['sha256'])
  if 'pdftotext' in rec:check('pdftotext_exit_'+rec['key'],rec['pdftotext']['returncode']==0)
for rec in json.loads((ROOT/'RENDER_PROCESS_RECORDS.json').read_text()):
 check('render_exit_'+rec['output'],rec['returncode']==0)
 check('render_hash_'+rec['output'],hashlib.sha256((ROOT/rec['output']).read_bytes()).hexdigest()==rec['sha256'])
validation={'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'operator_pid':os.getpid(),'checks':checks,'passed':all(c['passed'] for c in checks),'bounded_family_complete':True,'global_priority_clearance':False}
(ROOT/'VALIDATION_CLOSE.json').write_text(json.dumps(validation,indent=2)+'\n')
files=[]
for p in sorted(ROOT.rglob('*')):
 if p.is_file() and p.name!='CLOSED_SHA256_MANIFEST.json':
  files.append({'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
manifest={'schema':'closed_sha256_source_audit.v1','closed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'operator_pid':os.getpid(),'artifact_root':str(ROOT),'excluded_self':'CLOSED_SHA256_MANIFEST.json','file_count':len(files),'files':files,'read_only_borrowed_inputs':c['read_only_gate_and_candidate']+[e for s in c['source_catalog'] for e in s.get('local_evidence',[]) if 'borrowed_read_only_path' in e],'scope':'priorityfamilyonly; no service/PR/queue/main/outreach mutations; original2/5proofsearchbudgetnotextended'}
p=ROOT/'CLOSED_SHA256_MANIFEST.json';p.write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
for item in files:
 p2=ROOT/item['path'];assert hashlib.sha256(p2.read_bytes()).hexdigest()==item['sha256']
print(json.dumps({'closed_utc':manifest['closed_utc'],'file_count':len(files),'total_local_bytes':sum(f['bytes'] for f in files),'validation_checks':len(checks),'manifest_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'report_sha256':hashlib.sha256((ROOT/'REPORT.md').read_bytes()).hexdigest(),'verdict_sha256':hashlib.sha256((ROOT/'VERDICT.json').read_bytes()).hexdigest()},indent=2))

