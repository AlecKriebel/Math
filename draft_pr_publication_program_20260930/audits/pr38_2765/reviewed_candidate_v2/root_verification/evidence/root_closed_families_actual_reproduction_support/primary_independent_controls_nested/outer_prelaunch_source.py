from pathlib import Path
import subprocess,json,hashlib,datetime
out=Path(__file__).resolve().parent
pin=out/'original_pin';work=out/'ignoredtmp/review_runs';work.mkdir(parents=True,exist_ok=True)
source=(pin/'review/independent_checks.py').read_bytes();cases=[('original_72_checks',source),('corrupt_mod_two_quotient_order',source.replace(b"len(group)==6",b"len(group)==5")),('corrupt_cusped_volume',source.replace(b"==4*sp.pi**2",b"==8*sp.pi**2"))]
ledger=[]
for name,b in cases:
 d=work/name;d.mkdir(exist_ok=True);(d/'independent_checks.py').write_bytes(b)
 c=subprocess.run(['/usr/bin/python3',str(d/'independent_checks.py')],cwd=d,capture_output=True,text=True)
 entry={'case':name,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'runtime':'/usr/bin/python3','source_sha256':hashlib.sha256(b).hexdigest(),'exact_original_bytes':b==source,'exit_code':c.returncode,'stdout':c.stdout,'stderr':c.stderr}
 if c.returncode==0:
  entry.update(result=json.loads(c.stdout),exact_saved_json_equality=json.loads(c.stdout)==json.loads((pin/'review/independent_results.json').read_text()),exact_saved_stdout_bytes=c.stdout.encode()==(pin/'review/independent_results.json').read_bytes())
 ledger.append(entry)
(out/'ORIGINAL_REVIEW_HELPER_EXECUTION.json').write_text(json.dumps(ledger,indent=2)+'\n')
print(json.dumps([{'case':x['case'],'exit':x['exit_code'],'original':x['exact_original_bytes'],'saved_json_equal':x.get('exact_saved_json_equality'),'byte_equal':x.get('exact_saved_stdout_bytes')} for x in ledger],indent=2))
