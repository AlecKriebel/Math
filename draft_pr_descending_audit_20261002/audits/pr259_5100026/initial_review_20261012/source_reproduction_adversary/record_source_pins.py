#!/usr/bin/env python3
import pathlib,hashlib,json,re,datetime,subprocess,os
ROOT=pathlib.Path(__file__).resolve().parent
WORKSPACE=pathlib.Path('/Users/alec/Documents/Math')
SOURCE=ROOT.parent/'submitted/unsolved_math_prioritization/attempts/5100026'
sha=lambda b:hashlib.sha256(b).hexdigest()
manifest=json.loads((SOURCE/'source_manifest.json').read_text())
pins=[]
for item in manifest['sources']:
 filename=item['reading_filename']
 local=ROOT/'reading_private'/('stachel_download.pdf' if filename=='stachel_published.pdf' else filename)
 b=local.read_bytes();pins.append({**item,'local_reading_path':str(local),'bytes':len(b),'actual_sha256':sha(b),'matched':sha(b)==item['sha256']})
p=WORKSPACE/'unsolved_math_prioritization/cache/problems.json';b=p.read_bytes();d=json.loads(b);rec=next(x for x in d if x['id']==5100026)
expected=json.loads((WORKSPACE/'unsolved_math_prioritization/manifest.json').read_text())
headers=(ROOT/'reading_private/DATASET_HEAD.headers').read_text()
remote_commit=re.search(r'x-repo-commit:\s*(\w+)',headers).group(1)
remote_etag=re.search(r'x-linked-etag:\s*"([a-f0-9]+)"',headers).group(1)
remote_size=int(re.search(r'x-linked-size:\s*(\d+)',headers).group(1))
localrec=ROOT/'reading_private/imported_problem_5100026.json'
record={'input_file':str(p),'dataset_repository':'ulamai/UnsolvedMath','pinned_revision':manifest['dataset_revision'],'remote_repo_commit':remote_commit,'remote_x_linked_etag':remote_etag,'remote_x_linked_size':remote_size,'actual_file_sha256':sha(b),'actual_bytes':len(b),'matched':sha(b)==expected['files']['problems.json']['sha256']==remote_etag and len(b)==expected['files']['problems.json']['bytes']==remote_size and remote_commit==manifest['dataset_revision']==expected['revision'],'record_id':rec['id'],'problem_number':rec['problem_number'],'statement_sha256':sha(rec['statement'].encode()),'private_record_copy_sha256':sha(localrec.read_bytes()),'private_record_copy_path':str(localrec),'literal_least_or_primitive_wording_present':bool(re.search(r'least|primitive',rec['statement'],re.I))}
probes=[]
for executable in ['/opt/homebrew/bin/python3','/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3']:
 env=dict(os.environ);env.pop('PYTHONPATH',None);env['PYTHONDONTWRITEBYTECODE']='1'
 r=subprocess.run([executable,'-c','import sys; print(sys.version); import sympy,mpmath; print(sympy.__version__,mpmath.__version__)'],env=env,capture_output=True)
 probes.append({'executable':executable,'exit_code':r.returncode,'stdout':r.stdout.decode(),'stderr':r.stderr.decode()})
obj={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_pdf_pins':pins,'imported_problem_pin':record,'source_DLMF_consulted_URLs':['https://dlmf.nist.gov/22.2','https://dlmf.nist.gov/22.4','https://dlmf.nist.gov/22.8'],'default_environment_probe_failures_retained':probes,'all_source_pins_match':all(x['matched'] for x in pins) and record['matched'],'private_reading_material_excluded_from_publication':True}
(ROOT/'SOURCE_PINS.json').write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
print(json.dumps(obj,indent=2,sort_keys=True))
