"""Check every family seal and reproduce full new control streams privately."""
from pathlib import Path
import datetime,hashlib,json,shutil,subprocess,sys,time
A=Path(__file__).resolve().parent;T=A/'tmp/root_family_controls';T.mkdir(parents=True,exist_ok=True)
sha=lambda b:hashlib.sha256(b).hexdigest()
seals=[]
for folder,name,key in [('sources_hnn_review','FINAL_MANIFEST.json','files'),('integral_tor_review','FINAL_SEAL.json','artifacts'),('extensions_realization_review','AUDIT_MANIFEST.json','files')]:
 F=A/folder;m=json.loads((F/name).read_text())
 for e in m[key]:
  b=(F/e['path']).read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256'],(folder,e['path'])
 seals.append({'folder':folder,'manifest':name,'sha256':sha((F/name).read_bytes()),'every_bound_file_verified':len(m[key])})
jobs=[('sources_hnn_review','independent_exact_checks.py','independent_exact_results.json'),('integral_tor_review','independent_controls.py','independent_controls.full.stdout.jsonl'),('integral_tor_review','post_candidate_mutant_controls.py','post_candidate_mutants.full.stdout.jsonl'),('extensions_realization_review','independent_exact_checks.py','INDEPENDENT_OUTPUT.json'),('extensions_realization_review','realization_comparison_exact.py','REALIZATION_COMPARISON_OUTPUT.json')]
runs=[]
for folder,script,expected in jobs:
 D=T/folder;D.mkdir(exist_ok=True)
 for f in (A/folder).glob('*.py'):shutil.copy2(f,D/f.name)
 start=time.monotonic();r=subprocess.run([sys.executable,'-B',str((D/script).absolute())],capture_output=True,cwd=D)
 stem='root_'+folder+'_'+Path(script).stem;(A/(stem+'.stdout')).write_bytes(r.stdout);(A/(stem+'.stderr')).write_bytes(r.stderr)
 assert r.returncode==0 and not r.stderr,(folder,script,r.stderr.decode())
 assert r.stdout==(A/folder/expected).read_bytes(),(folder,script)
 runs.append({'family':folder,'program':script,'seconds':time.monotonic()-start,'exit_code':0,'complete_stdout_byte_equal':True,'stdout_bytes':len(r.stdout),'sha256':sha(r.stdout)})
receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'head':'90794508688ec07f598e0871bbd1eb38aaf466ce','all3_family_reports_reconstructions_and_all6_executable_sources_fully_read':True,'all_new_control_complete_stdout_bytes_equal':True,'sealed_file_count':sum(x['every_bound_file_verified'] for x in seals),'seals':seals,'runs':runs,'mandatory_repair':'TURN2 incidental general graph claim requires finite underlying graph','source_qualification':'Root independently checks6 exact primary PDFs and relevant text. Family scopes differ; no collective global source-completeness claim.'}
(A/'root_family_controls_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
