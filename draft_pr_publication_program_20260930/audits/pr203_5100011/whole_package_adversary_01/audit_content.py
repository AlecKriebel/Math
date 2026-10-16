from pathlib import Path
import json,hashlib,re,zipfile,subprocess,stat
from datetime import datetime,timezone
HERE=Path(__file__).resolve().parent;P=HERE.parent/'publication_package_v1';M=P/'materials';A=M/'audit'
def need(c,n):
 if not c:raise RuntimeError(n)
def pin(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def no_constant(c):raise ValueError('Nonstandard JSON constant '+c)
parsed={};text_inventory=[];privacy=[]
secret=re.compile(r'gh[pousr]_[A-Za-z0-9]{30,}|sk-[A-Za-z0-9]{24,}|xox[baprs]-[A-Za-z0-9-]{20,}|Bearer\s+[A-Za-z0-9._-]{20,}|-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----')
for f in sorted(M.rglob('*')):
 if not f.is_file():continue
 rel=str(f.relative_to(M));b=f.read_bytes();t=b.decode('utf8')
 need(not secret.search(t),'credential-like text '+rel)
 if f.suffix=='.json':parsed[rel]=json.loads(t,parse_constant=no_constant)
 if f.suffix=='.jsonl':parsed[rel]=[json.loads(x,parse_constant=no_constant) for x in t.splitlines() if x.strip()]
 text_inventory.append({'path':rel,**pin(f),'kind':f.suffix,'absolute_local_paths':len(re.findall(r'/Users/[^\s"\\]+',t))})
# All nested authored pin maps bind actual files. Read-only input maps are not repackaged.
pinmaps=[]
for f in sorted(A.rglob('*MANIFEST.json')):
 j=json.loads(f.read_bytes());key='authored_files' if 'authored_files' in j else 'files'
 mapping=j.get(key,{})
 if isinstance(mapping,list):mapping={x['path']:{k:v for k,v in x.items() if k!='path'} for x in mapping}
 for n,p in mapping.items():
  file=f.parent/n;need(file.is_file(),'nested manifest missing '+str(file));q=pin(file)
  need(q['sha256']==(p if isinstance(p,str) else p['sha256']),'nested manifest hash '+str(file))
  if isinstance(p,dict) and 'bytes' in p:need(q['bytes']==p['bytes'],'nested manifest size '+str(file))
 pinmaps.append({'manifest':str(f.relative_to(M)),'verified_pins':len(j.get(key,{}))})
# Lowercase reviewer manifest has a different shape.
f=A/'original_submitted_head/independent_review/review_manifest.json';j=json.loads(f.read_bytes())
for n,h in j['files'].items():need(pin(f.parent/n)['sha256']==h,'review manifest '+n)
pinmaps.append({'manifest':str(f.relative_to(M)),'verified_pins':len(j['files'])})
for gate in ['ROOT_MATHEMATICAL_GATE_01.json','ROOT_PRIORITY_AND_EDITORIAL_GATE_01.json']:
 j=json.loads((A/gate).read_bytes())
 for n,p in j['safe_files'].items():need(pin(A/n)==p,'gate pin '+n)
 pinmaps.append({'manifest':gate,'verified_pins':len(j['safe_files'])})
# Historical result counts/code hashes and ordinary receipt byte equivalence.
for n in ['CHECK_RESULTS.json','CHECK_RESULTS_OPT.json']:
 j=parsed['audit/math_direct_geometry_01/'+n];need(j['status']=='PASS' and j['checks']==len(j['passed_labels'])==282,'282 exact labels')
 need(j['script_sha256']==pin(A/'math_direct_geometry_01/verify_exact_controls.py')['sha256'],'282 source pin')
for n in ['independent_results.json','independent_optimized_results.json']:
 j=parsed['audit/math_algebra_physical_01/'+n]
 need(sum(j['counts'].values())==107962 and len(j['cases'])==39,'39 scope/counts')
 need(j['script_sha256']==pin(A/'math_algebra_physical_01/physical_audit.py')['sha256'],'physical script pin')
for n in ['signed_edges_ordinary.json','signed_edges_optimized.json']:
 j=parsed['audit/math_algebra_physical_01/'+n];need(sum(j['counts'].values())==2000,'signed edge count')
 need(j['script_sha256']==pin(A/'math_algebra_physical_01/signed_edge_checks.py')['sha256'],'signed source pin')
for who,receipt in [('author','verification.json'),('reviewer','independent_review/independent_receipt.json')]:
 rows=parsed['audit/math_algebra_physical_01/ram_'+who+'_replay.json']
 need(len(rows)==4,'RAM scope')
 for row in rows:
  expected_exit=1 if not row['optimized'] and row['mutated_actual_identity'] else 0
  need(row['returncode']==expected_exit,'RAM mutation enforcement')
  if not row['optimized'] and not row['mutated_actual_identity']:
   need(row['stdout'].encode()==(A/'original_submitted_head'/receipt).read_bytes(),'ordinary exact bytes')
# Root's fresh ordinary original replay retained outside immutable publication package.
rr=HERE.parent/'portable_reproduction_v1';r=json.loads((rr/'ROOT_PORTABLE_REPLAY_RECEIPT.json').read_bytes())
for x in r['runs']:
 for channel in ['stdout','stderr']:need(pin(rr/(x['name']+'.'+channel))==x[channel],'Root replay pin')
legacy=json.loads((rr/'legacy_ordinary.stdout').read_bytes())
for row,receipt in zip(legacy['reports'][-2:],['verification.json','independent_review/independent_receipt.json']):
 need(row['stdout'].encode()==(A/'original_submitted_head'/receipt).read_bytes(),'fresh legacy stdout bytes')
# Current render/PDF custody pins and PDF security inventory.
qa=json.loads((HERE.parent/'ROOT_PDF_VISUAL_QA_V1.json').read_bytes())
need(pin(P/'original_pedal_flag.pdf')==qa['pdf'] and pin(P/'original_pedal_flag.tex')==qa['tex'],'PDF render binding')
for n,p in qa['renders'].items():need(pin(HERE.parent/'private_pdf_qa_v1'/n)==p,'render pin '+n)
with zipfile.ZipFile(P/'verification-package.zip') as z:
 need(not z.comment,'archive comment')
 for i in z.infolist():
  need(not i.comment and not i.extra,'ZIP hidden comments/extra')
  need(stat.S_ISREG(i.external_attr>>16),'ZIP nonregular file')
  need('\\' not in i.filename and ':' not in i.filename,'ZIP platform path')
 zip_bytes=sum(i.file_size for i in z.infolist())
# Scan no fulltext binaries/dependency implementations; every material file is authored UTF8.
allowed={'.json','.jsonl','.md','.py','.txt','.stdout','.tex'}
need(all(Path(x['path']).suffix in allowed for x in text_inventory),'unexpected material type')
report={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','strict_json_or_jsonl_files':len(parsed),'all_UTF8_files':len(text_inventory),'nested_pin_maps':pinmaps,'zip_uncompressed_bytes':zip_bytes,'archive_comments_extra_fields_or_nonregular_entries':False,'credential_like_patterns_found':False,'PDF_and_seven_renders_bound_to_current_source':True,'historical_full_sweep_scope_and_script_pins_consistent':True,'Root_fresh_original_ordinary_stdout_matches_archived_bytes':True,'all_file_content_inventory':text_inventory,'privacy_limit':'Pattern scan and full inventory/code/metadata review, not a cryptographic privacy proof. Historical tracebacks contain benign author workspace paths; public author/ORCID, source URLs, hashes and record metadata are intentionally present.'}
(HERE/'CONTENT_PRIVACY_PROVENANCE_RECEIPT.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ['all_file_content_inventory','nested_pin_maps']}))
