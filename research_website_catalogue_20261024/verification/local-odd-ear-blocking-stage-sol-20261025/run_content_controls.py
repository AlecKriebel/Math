"""Bounded actual subprocess controls of the two new target branches only."""
from pathlib import Path
import concurrent.futures,datetime,hashlib,json,subprocess,sys,time
O=Path(__file__).resolve().parent
cases=['visible_date','header_version','citation_version','omit_status','truncate_abstract','omit_result','alter_proof','add_human_review','wrong_iframe','wrong_original_pdf','borrow_code_license','h1_destination','Research_destination','ORCID_destination','footer_destination','paper_jump','PDF_hash_read','ZIP_hash_read','BibTeX_read']
root=O/'content-controls';root.mkdir(exist_ok=True)
sentinel=root/'DISPATCH.json'
if sentinel.exists():raise RuntimeError('controls already dispatched; inspect actual results')
sentinel.write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'records':['23576280','23331258'],'cases':cases,'modes':['normal','optimized'],'actual_single_target_runs':76},indent=2)+'\n')
def run(job):
 mode,rid,case=job;out=root/mode/rid/case;out.mkdir(parents=True)
 cmd=[sys.executable,'-B']+(['-O'] if mode=='optimized' else [])+[str(O/'execute.py'),str(O/'public_fault.py'),rid,case,str(out)]
 started=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
 r=subprocess.run(cmd,capture_output=True,timeout=90)
 (out/'stdout').write_bytes(r.stdout);(out/'stderr').write_bytes(r.stderr)
 mutation=json.loads((out/'mutation.json').read_text()) if (out/'mutation.json').exists() else None
 qa=json.loads((out/'qa.json').read_text()) if (out/'qa.json').exists() else None
 failed=[name for name,v in (qa or {}).get('papers',{}).get(rid,{}).get('checks',{}).items() if not v]
 expected=(mutation or {}).get('expected_failed_checks',[])
 valid=r.returncode==1 and not r.stderr and qa and qa['status']=='ISSUES_FOUND' and set(qa['papers'])=={rid} and expected and set(expected)<=set(failed)
 if case in ('h1_destination','Research_destination','ORCID_destination','footer_destination','paper_jump'):valid=valid and failed==expected
 receipt={'started_utc':started,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':cmd,'exit_code':r.returncode,'stderr_bytes':len(r.stderr),'elapsed_seconds':time.monotonic()-t,'mode':mode,'record_id':rid,'case':case,'failed_checks':failed,'expected_failed_checks':expected,'actual_rejection_verified':bool(valid)}
 (out/'execution.json').write_text(json.dumps(receipt,indent=2)+'\n');return receipt
jobs=[(mode,rid,case) for mode in ('normal','optimized') for rid in ('23576280','23331258') for case in cases]
results=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 for row in pool.map(run,jobs):
  results.append(row)
  if len(results)%19==0:print(json.dumps({'completed':len(results),'expected':76,'verified':sum(x['actual_rejection_verified'] for x in results)}),flush=True)
summary={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS' if all(x['actual_rejection_verified'] for x in results) else 'FAIL','actual_runs':len(results),'normal_runs':38,'optimized_runs':38,'results':results,'no_fixture_files_created':True,'binary_controls_scope':'virtual hash-read rejection only; actual parser files unchanged'}
(root/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k!='results'}));sys.exit(0 if summary['status']=='PASS' else 1)
